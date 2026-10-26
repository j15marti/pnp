#!/usr/bin/env python3
"""ARC187: exact source-authenticated sorted memory history for a bit-indexed RAM.
Standard-library-only reproducibility. No arbitrary-SAT lower-bound claim.
"""
from __future__ import annotations
import copy, itertools, json, random, hashlib
from pathlib import Path

SEED=18720261026
ROOT=Path(__file__).resolve().parent

def encode_formula(clauses,n):
    w=max(1,n.bit_length()); out=[]
    for clause in clauses:
        assert 0<=len(clause)<=3
        out.extend(map(int,f'{len(clause):02b}'))
        for j in range(3):
            z=clause[j] if j<len(clause) else 0
            v=abs(z); s=int(z>0)
            assert v<(1<<w)
            out.extend(map(int,f'{v:0{w}b}'+str(s)))
    return tuple(out),w

def truth(clauses,n,pins=()):
    p=dict(pins)
    for a in range(1<<n):
        if any(((a>>(v-1))&1)!=b for v,b in p.items()):continue
        if all(any(bool((a>>(abs(l)-1))&1)==(l>0) for l in c) for c in clauses):return True
    return False

def restrict(clauses,pins):
    p=dict(pins); out=[]
    for c in clauses:
        if any((abs(l) in p) and (p[abs(l)]==int(l>0)) for l in c):continue
        out.append(tuple(l for l in c if abs(l) not in p))
    return out

# State = (phase, assignment, init_idx, clause, literal, bit_index,
#          binary_buffer, clause_length, clause_hit, temp_variable, desired_bit)
INITIAL=('W',0,0,0,0,0,0,0,0,0,0)

def op_address(st,n,m,w):
    ph,a,i,c,j,k,buf,clen,hit,v,s=st
    if ph in ('SAT','UNSAT'):return None
    if ph=='W':return ('W',i)
    base=c*(2+3*(w+1))
    if ph=='L':return ('I',base+k)
    if ph=='D':return ('I',base+2+j*(w+1)+k)
    if ph=='R':return ('R',v-1)
    raise AssertionError(st)

def next_step(st,rb,n,m,w):
    ph,a,i,c,j,k,buf,clen,hit,v,s=st
    typ,addr=op_address(st,n,m,w)
    wb=rb
    if ph=='W':
        wb=(a>>i)&1
        if i+1==n:nxt=('L',a,0,0,0,0,0,0,0,0,0)
        else:nxt=('W',a,i+1,0,0,0,0,0,0,0,0)
    elif ph=='L':
        buf1=2*buf+rb
        if k+1<2:nxt=('L',a,i,c,j,k+1,buf1,0,0,0,0)
        else:
            if buf1==0:nxt=after_clause(st,n,m,w,False)
            elif buf1<=3:nxt=('D',a,i,c,0,0,0,buf1,0,0,0)
            else:raise AssertionError('invalid source length')
    elif ph=='D':
        buf1=2*buf+rb
        if k+1<w+1:nxt=('D',a,i,c,j,k+1,buf1,clen,hit,v,s)
        else:
            vv=buf1>>1; ss=buf1&1
            if not 1<=vv<=n:nxt=after_literal(st,n,m,w,hit)
            else:nxt=('R',a,i,c,j,0,0,clen,hit,vv,ss)
    elif ph=='R':
        newhit=hit or rb==s
        nxt=after_literal(st,n,m,w,newhit)
    return nxt,wb

def after_literal(st,n,m,w,newhit):
    ph,a,i,c,j,k,buf,clen,hit,v,s=st
    if j+1<clen:return ('D',a,i,c,j+1,0,0,clen,int(newhit),0,0)
    return after_clause(st,n,m,w,bool(newhit))

def after_clause(st,n,m,w,hit):
    ph,a,i,c,j,k,buf,clen,oldhit,v,s=st
    if not hit:
        aa=a+1
        return ('UNSAT',aa,0,0,0,0,0,0,0,0,0) if aa==(1<<n) else ('W',aa,0,0,0,0,0,0,0,0,0)
    if c+1>=m:return ('SAT',a,0,0,0,0,0,0,0,0,0)
    return ('L',a,0,c+1,0,0,0,0,0,0,0)

def trace(source,n,m,w,fault=None):
    mem=[0]*n;st=INITIAL;arr=[];count=0
    while st[0] not in ('SAT','UNSAT'):
        typ,addr=op_address(st,n,m,w)
        rb=source[addr] if typ=='I' else mem[addr]
        if fault=='input' and typ=='I' and not any(z['typ']=='I' for z in arr):rb^=1
        if fault=='work' and typ=='R' and not any(z['typ']=='R' for z in arr):rb^=1
        nxt,wb=next_step(st,rb,n,m,w)
        arr.append({'t':count,'before':list(st),'typ':typ,'addr':addr,
                    'rb':rb,'wb':wb,'after':list(nxt)})
        if typ=='W':mem[addr]=wb
        st=nxt;count+=1
        if count>300000:raise RuntimeError('toy control too long')
    return arr,st[0]

def verify(source,n,m,w,arr,accept='UNSAT',
           check_work=True,check_source=True,check_local=True):
    st=INITIAL;hist=[]
    try:
        for t,e in enumerate(arr):
            if st[0] in ('SAT','UNSAT'):return False
            if e['t']!=t or e['before']!=list(st):return False
            typ,addr=op_address(st,n,m,w)
            if e['typ']!=typ or e['addr']!=addr:return False
            rb=e['rb'];wb=e['wb']
            if rb not in (0,1) or wb not in (0,1):return False
            if check_source and typ=='I' and source[addr]!=rb:return False
            expected,write=next_step(st,rb,n,m,w)
            if check_local and (e['after']!=list(expected) or wb!=write):return False
            if typ in ('R','W'):hist.append((addr,t,rb,wb))
            st=tuple(e['after'])
        if st[0]!=accept:return False
        if check_work:
            hist.sort(key=lambda z:(z[0],z[1]))
            last_addr=None;last_val=0
            for addr,t,rb,wb in hist:
                if addr!=last_addr:last_addr=addr;last_val=0
                if rb!=last_val:return False
                last_val=wb
        return True
    except (ValueError,IndexError,TypeError,AssertionError,KeyError):
        return False

def grammar_exact22(clauses,n):
    pos=[0]*n;neg=[0]*n
    for c in clauses:
        assert len(c)==3 and len({abs(x) for x in c})==3
        for x in c:
            target=pos if x>0 else neg
            target[abs(x)-1]+=1
    return all(x==2 for x in pos+neg)

def run():
    rng=random.Random(SEED);assertions=0;cases=[];attack=[]
    def ck(x,what):
        nonlocal assertions
        assertions+=1
        if not x:raise AssertionError(what)
    y=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),
       (-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
    ck(grammar_exact22(y,6),'Y 2P2N grammar')
    cube=list(itertools.product([0,1],repeat=3))
    u=[tuple(j+1 if value==0 else -(j+1) for j,value in enumerate(bits))
       for bits in cube]
    ck(not truth(u,3),'full 8 cube clauses must be UNSAT')
    base=[('signed_full_cube_UNSAT',u,3),
          ('signed_missing_clause_SAT',u[:-1],3),
          ('monotone_Y_exact22_SAT',y,6),
          ('monotone_Y_plus_empty_UNSAT',y+[()],6)]
    for name,form,n in base:
        for pins in [(),((1,0),),((1,1),),((1,0),(2,0)),
                     ((1,0),(2,1)),((1,1),(2,0)),((1,1),(2,1))]:
            child=restrict(form,pins)
            src,w=encode_formula(child,n)
            if not child:continue
            tr,label=trace(src,n,len(child),w)
            expected='SAT' if truth(child,n) else 'UNSAT'
            ck(label==expected,f'{name} {pins} decision')
            ck(verify(src,n,len(child),w,tr,expected),f'{name} {pins} authentic')
            ck(not verify(src,n,len(child),w,tr,'SAT' if expected=='UNSAT' else 'UNSAT'),
               f'{name} {pins} false label')
            dig=hashlib.sha256(json.dumps(tr,separators=(',',':')).encode()).hexdigest()
            cases.append({'formula':name,'pins':[list(t) for t in pins],
                          'n':n,'m':len(child),'input_bits':len(src),
                          'T_events':len(tr),'label':label,'trace_sha256':dig})
            if not pins and name=='signed_full_cube_UNSAT':
                for fault,disabled in [('input','check_source'),('work','check_work')]:
                    forged,forged_label=trace(src,n,len(child),w,fault=fault)
                    ck(not verify(src,n,len(child),w,forged,forged_label),
                       f'{fault} must reject')
                    kwargs={disabled:False}
                    ck(verify(src,n,len(child),w,forged,forged_label,**kwargs),
                       f'{fault} omitted audit falsely accepts')
                    attack.append({'tamper':fault,'forged_label':forged_label,
                                   'accepted_unsafe_without_check':True,
                                   'rejected_full':True,'trace_records':len(forged)})
                bad=copy.deepcopy(tr);bad[0]['after'][1]=99
                ck(not verify(src,n,len(child),w,bad,label),'bad transition must reject')
                bad=copy.deepcopy(tr);bad[2],bad[3]=bad[3],bad[2]
                ck(not verify(src,n,len(child),w,bad,label),'reorder must reject')
    def build_tree_leaves(parent,n,forge_unsat=None):
        leaves=[]
        for bits in itertools.product([0,1],repeat=2):
            pins=((1,bits[0]),(2,bits[1]))
            correct=restrict(parent,pins)
            supplied=forge_unsat if forge_unsat is not None else correct
            ss,ww=encode_formula(supplied,n)
            tt,ll=trace(ss,n,len(supplied),ww)
            leaves.append({'pins':pins,'clauses':supplied,
                           'source':ss,'w':ww,'trace':tt,'label':ll})
        return leaves
    def check_twolevel(parent,n,leaves,check_projection=True):
        if len(leaves)!=4:return False
        expectedpins=set(itertools.product([0,1],repeat=2))
        gotpins=set((x['pins'][0][1],x['pins'][1][1]) for x in leaves)
        if gotpins!=expectedpins:return False
        for leaf in leaves:
            if check_projection and leaf['clauses']!=restrict(parent,leaf['pins']):
                return False
            cc=leaf['clauses'];ss,ww=encode_formula(cc,n)
            if ss!=leaf['source'] or ww!=leaf['w']:return False
            if not verify(ss,n,len(cc),ww,leaf['trace'],'UNSAT'):return False
        return True
    for name,parent,n in [('cube_UNSAT',u,3),('Y_SAT',y,6),
                          ('Y_empty_UNSAT',y+[()],6)]:
        real=build_tree_leaves(parent,n)
        result=check_twolevel(parent,n,real)
        ck(result==(not truth(parent,n)),f'{name} two-level exact join')
        cases.append({'formula':'twolevel_'+name,'pins':[],'n':n,
                      'm':len(parent),'input_bits':len(encode_formula(parent,n)[0]),
                      'T_events':sum(len(x['trace']) for x in real),
                      'label':'UNSAT' if result else 'SAT',
                      'all_four_leaves_checked':True})
    fake=build_tree_leaves(y,6,forge_unsat=u)
    ck(check_twolevel(y,6,fake,check_projection=False),
       'false UNSAT of Y if parent-child authentication is disabled')
    ck(not check_twolevel(y,6,fake,check_projection=True),
       'forged UNSAT children must be rejected by source-consistent join')
    attack.append({'tamper':'all_four_child_sources_replaced_with_unrelated_UNSAT',
                   'accepted_unsafe_without_check':True,'rejected_full':True,
                   'trace_records':sum(len(x['trace']) for x in fake)})
    for idx in range(10):
        subset=rng.sample(u,rng.randrange(0,9))
        if not subset:subset=[u[0]]
        src,w=encode_formula(subset,3)
        tr,label=trace(src,3,len(subset),w)
        ck(label==('SAT' if truth(subset,3) else 'UNSAT'),'random decision')
        ck(verify(src,3,len(subset),w,tr,label),'random trace')
        cases.append({'formula':f'random_clause_order_{idx}','pins':[],
                      'n':3,'m':len(subset),'input_bits':len(src),
                      'T_events':len(tr),'label':label})
    out={'run_id':'ARC187-SORTED-TRACE-SOURCE-AUTH','seed':SEED,
         'assertions':assertions,'cases':cases,'attacks':attack,
         'status':'COMPUTATIONAL finite controls; symbolic proof in report',
         'maximum_trace_records':max(z['T_events'] for z in cases),
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'arc187_raw.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'assertions':assertions,'cases':len(cases),
                      'SAT':sum(z['label']=='SAT' for z in cases),
                      'UNSAT':sum(z['label']=='UNSAT' for z in cases),
                      'max_events':out['maximum_trace_records'],
                      'attacks':attack},indent=2))
if __name__=='__main__':run()
