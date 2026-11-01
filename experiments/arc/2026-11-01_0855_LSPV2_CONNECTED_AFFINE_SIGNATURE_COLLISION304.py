#!/usr/bin/env python3
"""LSPV-2 304: exact canonical connected F9 splicing and signature collision.
No solver oracle is used. This is NOT a P/NP complexity claim.
"""
from itertools import combinations, product
from collections import Counter, defaultdict
from pathlib import Path
import json, gzip, hashlib
ROOT=Path(__file__).resolve().parent
POS=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
NEG=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
BASE=[(1,x) for x in POS]+[(-1,x) for x in NEG]
PA=(1,0,1,0,None,None,None,0,None)
PB=(1,1,0,0,None,None,None,0,None)

def canonical(t,spliced):
    out=[]
    for i in range(t):
        for j,(sg,trip) in enumerate(BASE):
            a=[x+9*i for x in trip]
            if spliced and t>1 and j==0:
                a[1]=9*((i+1)%t)+5
            out.append((sg,tuple(sorted(a))))
    return out

def grammar(c,n):
    if n<=0 or len(c)*3!=4*n:return False
    cnt=Counter();seen=set()
    for sg,vs in c:
        if sg not in (-1,1) or len(vs)!=3 or len(set(vs))!=3:return False
        if any(not isinstance(x,int) or x<1 or x>n for x in vs):return False
        k=(sg,tuple(sorted(vs)))
        if k in seen:return False
        seen.add(k)
        for x in vs:cnt[(sg,x)]+=1
    return all(cnt[(s,x)]==2 for x in range(1,n+1) for s in (-1,1))

def connected(c,n):
    ad=[set() for _ in range(n+1)]
    for _,vs in c:
        for a,b in combinations(vs,2):ad[a].add(b);ad[b].add(a)
    seen={1};stack=[1]
    while stack:
        for v in ad[stack.pop()]:
            if v not in seen:seen.add(v);stack.append(v)
    return len(seen)==n

def pinvec(t,onebad=False):
    return tuple(v for i in range(t) for v in (PB if onebad and i==0 else PA))

def residual(c,p):
    covered=[];uncovered=[];pos=Counter();neg=Counter();empty=[]
    for j,(sg,trip) in enumerate(c):
        if any(p[x-1] is not None and p[x-1]==(sg==1) for x in trip):
            covered.append(j)
            for x in trip:
                if p[x-1] is None:(pos if sg==1 else neg)[x]+=1
        else:
            rem=tuple(x for x in trip if p[x-1] is None)
            if not rem:empty.append(j)
            uncovered.append((j,sg,rem))
    free=[x for x,v in enumerate(p,1) if v is None]
    edges=[(j,sg,*vs) for j,sg,vs in uncovered if len(vs)==2]
    adj=defaultdict(list)
    for j,sg,u,v in edges:
        adj[u].append((j,v));adj[v].append((j,u))
    tris=[];comparisons=0
    for j,sg,u,v in edges:
        for k,w in adj[u]:
            if k<=j:continue
            for h,z in adj[v]:
                if h<=j:continue
                comparisons+=1
                if w==z and len({j,k,h})==3:tris.append(tuple(sorted((j,k,h))))
    tris=sorted(set(tris));used=set();packing=[]
    for tr in tris:
        if not used.intersection(tr):used.update(tr);packing.append(tr)
    eta=sum(min(pos[x],neg[x]) for x in free)
    f=len(free);u=len(uncovered);e=2*f-u
    return {'free':free,'covered':covered,'uncovered':uncovered,'empty':empty,
            'edges':edges,'packing':packing,'triangle_comparisons':comparisons,
            'f':f,'u':u,'eta':eta,'e':e,'nu':len(packing),'delta':e-eta-len(packing),
            'width_hist':[sum(len(vs)==w for _,_,vs in uncovered) for w in (0,1,2,3)],
            'sp':pos,'sn':neg}

def models(c,p,max_free=18):
    free=[i for i,v in enumerate(p) if v is None]
    assert len(free)<=max_free
    found=[]
    for v in product((0,1),repeat=len(free)):
        a=list(p)
        for j,x in zip(free,v):a[j]=x
        if all(any(a[x-1]==(sg==1) for x in trip) for sg,trip in c):found.append(tuple(a))
    return found

def rref_count(c,p,r):
    if r['delta']!=0 or r['empty']:return None
    free=r['free'];idx={x:i for i,x in enumerate(free)}
    byid={j:(sg,vs) for j,sg,vs in r['uncovered']}
    cycle_ids={j for cyc in r['packing'] for j in cyc}
    pref=[]
    for x in free:
        s0=r['sp'][x];s1=r['sn'][x]
        if s0>s1:pref.append((1<<idx[x],0,'prefer '+str(x)))
        elif s1>s0:pref.append((1<<idx[x],1,'prefer '+str(x)))
    off=[]
    for j,sg,vs in r['uncovered']:
        if j in cycle_ids:continue
        mask=sum(1<<idx[x] for x in vs)
        off.append((mask,1 if sg==1 else 1^(len(vs)%2),'clause '+str(j)))
    branch_counts=[];contradictions=[];first_witness=None;elims=0
    for picked in product(*r['packing']):
        rows=list(pref)+list(off)
        for cyc,chosen in zip(r['packing'],picked):
            for j in cyc:
                sg,vs=byid[j];assert len(vs)==2
                if j==chosen:
                    for x in vs:rows.append((1<<idx[x],int(sg==1),'selected '+str(j)+' x'+str(x)))
                else:rows.append((sum(1<<idx[x] for x in vs),1,'single '+str(j)))
        basis={};fail=None
        for k,(mask,rhs,label) in enumerate(rows):
            support=1<<k
            while mask:
                elims+=1
                bit=mask.bit_length()-1
                if bit not in basis: basis[bit]=(mask,rhs,support);break
                m,v,q=basis[bit];mask^=m;rhs^=v;support^=q
            else:
                if rhs:fail=(support,[rows[i][2] for i in range(len(rows)) if support>>i&1]);break
        if fail:
            contradictions.append({'picked':list(picked),'xor_row_ids':fail[1]})
            branch_counts.append(0);continue
        a=list(p);vector=0
        for k in sorted(basis):
            mask,rhs,_=basis[k]
            val=rhs^((mask&vector).bit_count()%2)
            if val:vector|=1<<k
        for x,k in idx.items():a[x-1]=(vector>>k)&1
        assert all(any(a[x-1]==(sg==1) for x in tri) for sg,tri in c)
        if first_witness is None:first_witness=a
        branch_counts.append(1<<(len(free)-len(basis)))
    return {'models':sum(branch_counts),'branches':len(branch_counts),
            'branch_counts':branch_counts,'row_xor_refutations':contradictions,
            'row_eliminations':elims,'first_witness':first_witness}

def dpll(c,p):
    stats={'nodes':0,'literal_probes':0,'unit_scans':0,'branches':0,'refutation_leaves':0}
    def go(a):
        stats['nodes']+=1
        while True:
            units=[];allgood=True
            for j,(sg,vs) in enumerate(c):
                unknown=[];true=False
                for x in vs:
                    stats['literal_probes']+=1
                    v=a[x-1]
                    if v is None:unknown.append(x)
                    elif v==(sg==1):true=True;break
                if true:continue
                allgood=False
                if not unknown:
                    stats['refutation_leaves']+=1;return False
                if len(unknown)==1:units.append((unknown[0],int(sg==1)))
            if allgood:return tuple(0 if x is None else x for x in a)
            if not units:break
            changed=False
            for x,val in units:
                if a[x-1] is not None:
                    if a[x-1]!=val:
                        stats['refutation_leaves']+=1;return False
                else:a[x-1]=val;changed=True
            stats['unit_scans']+=1
            if not changed:break
        x=next(i for i,v in enumerate(a) if v is None)
        stats['branches']+=1
        for val in (0,1):
            b=a.copy();b[x]=val
            out=go(b)
            if out:return out
        return False
    w=go(list(p))
    assert not w or all(any(w[x-1]==(sg==1) for x in vs) for sg,vs in c)
    return bool(w),stats

def gamma(n):
    assert n>0
    s=bin(n)[2:];return '0'*(len(s)-1)+s

def encode(c,n):
    w=n.bit_length();return gamma(n)+gamma(len(c))+''.join(('1' if sg==1 else '0')+''.join(format(x,'0'+str(w)+'b') for x in vs) for sg,vs in c)

def physical_parent_to_child(a,b):
    n=9*len(a)//12;source=encode(a,n);target=encode(b,n)
    assert len(source)==len(target)
    # Read-only source; output tape initially all zeros. Full sequential source-copy,
    # followed by exact changed-bit patching. No semantic SAT oracle is present.
    tape=['0']*len(source);events=[];reads=len(source)
    for i,v in enumerate(source):
        old=tape[i];events.append([i,old,v]);tape[i]=v
    for i,v in enumerate(target):
        if tape[i]!=v:
            old=tape[i];events.append([i,old,v]);tape[i]=v
    assert ''.join(tape)==target
    dphys=sum(a!=b for _,a,b in events)
    endpoint=sum(x!=y for x,y in zip('0'*len(target),target))
    return {'input_bits':len(source),'output_bits':len(target),'source_reads_at_least':reads,
            'write_events':len(events),'sum_adjacent_dphys':dphys,
            'endpoint_dphys':endpoint,'source_child_hamming':sum(x!=y for x,y in zip(source,target)),
            'changed_clause_ids':[12*i for i in range(len(a)//12)],'events':events}

def source_controls(c):
    n=max(x for _,vs in c for x in vs)
    def hist(a):return [sum(sum(a[x-1]==(sg==1) for x in vs)==k for sg,vs in c) for k in range(4)]
    a=[0]*n;b=[1]*n
    controls={'zero_hist':hist(a),'one_hist':hist(b),'complement_reversed':hist(a)==hist(b)[::-1]}
    if n==9:
        pairs=0
        for i,(si,vi) in enumerate(c):
            for j,(sj,vj) in enumerate(c):
                if j<=i:continue
                for u,v in product((0,1),repeat=2):
                    # all-literals true / false assignments for the pair
                    mi={x:int(si==1)^v for x in vi}
                    mj={x:int(sj==1)^u for x in vj}
                    possible=all(mi[x]==mj[x] for x in mi.keys()&mj.keys())
                    op=bool((set(vi)&set(vj))) and si!=sj
                    sp=bool((set(vi)&set(vj))) and si==sj
                    expected=not (op if u==v else sp)
                    assert possible==expected
                    pairs+=1
        controls['pair_extreme_modes']=pairs
    return controls

def main():
    output={'id':'LSPV2_CONNECTED_SATUNSAT_SIGNATURE_COLLISION304','status':'COMPUTATIONAL plus proved symbolic theorem','cases':[],'literature_note':'See report'}
    assert source_controls(canonical(1,False))['pair_extreme_modes']==264
    for t in (1,2,3,4,8):
        a=canonical(t,False);b=canonical(t,True);n=9*t
        assert grammar(a,n) and grammar(b,n)
        assert connected(b,n)
        x=pinvec(t,False);y=pinvec(t,True)
        rx=residual(b,x);ry=residual(b,y)
        sig=lambda r:(r['f'],r['u'],r['eta'],r['nu'],r['delta'],r['width_hist'],r['packing'])
        assert sig(rx)==sig(ry),(t,sig(rx),sig(ry))
        assert rx['delta']==0 and not rx['empty'] and not ry['empty']
        px=rref_count(b,x,rx) if t<=4 else None
        py=rref_count(b,y,ry) if t<=4 else None
        if t<=4:
            assert px['models']==1 and py['models']==0
            assert len(py['row_xor_refutations'])==3**t
        if t<=3:
            assert len(models(b,x))==1 and len(models(b,y))==0
        if t<=4:
            satx,dx=dpll(b,x);saty,dy=dpll(b,y)
            assert satx and not saty
        else:dx=dy=None
        ph=physical_parent_to_child(a,b) if t in (2,4) else None
        if ph:
            with gzip.open(ROOT/f'xor_events_t{t}.json.gz','wt') as f:
                json.dump({'n':n,'events':ph.pop('events')},f,separators=(',',':'))
        output['cases'].append({'t':t,'n':n,'m':len(b),'grammar':True,'connected':True,
          'same_free_names':rx['free']==ry['free'],'same_packed_clause_ids':rx['packing'],
          'common_signature':{'f':rx['f'],'u':rx['u'],'eta':rx['eta'],'nu':rx['nu'],
                              'delta':rx['delta'],'width_hist':rx['width_hist']},
          'SAT_pin':list(x),'UNSAT_pin':list(y),'affine_YES':px,'affine_NO':py,
          'UP_DPLL_YES':dx,'UP_DPLL_NO':dy,'physical_splice':ph})
    bad=canonical(2,True)
    mal=[bad[:-1],bad+[(1,(1,2,3))],bad[:-1]+[bad[0]],bad[:-1]+[(1,(1,1,2))]]
    assert all(not grammar(x,18) for x in mal)
    output['malformed_rejected']=len(mal)
    output['original_source_controls']=source_controls(canonical(1,False))
    (ROOT/'raw304.json').write_text(json.dumps(output,indent=2,default=list))
    print(json.dumps({'cases':[(z['t'],z['common_signature'],z['affine_YES']['models'] if z['affine_YES'] else None,z['affine_NO']['models'] if z['affine_NO'] else None) for z in output['cases']], 'malformed':len(mal)},indent=2))
if __name__=='__main__':main()