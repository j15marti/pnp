#!/usr/bin/env python3
"""Independent verifier for CUT-ACQUISITION266, reconstructs the source from raw.
Not importing or executing the producer. Python stdlib only.
"""
import sys,json,itertools,math,collections,hashlib

def actual_true(clause,mask):
    return sum(1 for l in clause if bool(mask & (1<<(abs(l)-1)))==(l>0))

def original_models(n,cls):
    count=0;wit=None;ring={};
    for a in range(1<<n):
        if all(actual_true(c,a)>0 for c in cls):
            count+=1
            if wit is None:wit=a
    return count,wit

def possible_extremes(c1,c2,mode):
    union=sorted(set(abs(x) for x in c1+c2))
    for bits in range(1<<len(union)):
        values={v:(bits>>i)&1 for i,v in enumerate(union)}
        z=[]
        for c in (c1,c2):
            z.append(sum(values[abs(l)]==int(l>0) for l in c))
        if all(z[i]==(len(c1) if i==0 else len(c2)) if mode[i]=='S' else z[i]==0 for i in range(2)):
            return True
    return False

def prism_vertices(k):
    d=[[] for x in range(k*2)]
    for j in range(k):
        for a,b,var in [(j,(j+1)%k,j+1),(k+j,k+(j+1)%k,k+j+1),(j,k+j,2*k+j+1)]:
            d[a].append(var);d[b].append(var)
    return [sorted(v) for v in d]

def expected_source(k,charge):
    ans=[]
    for v,labels in enumerate(prism_vertices(k)):
        for bits in itertools.product((0,1),repeat=3):
            if sum(bits)%2!=charge[v]:
                ans.append([x if bit==0 else -x for x,bit in zip(labels,bits)])
    return ans

def clauses_encode_len(n,cls):
    width=(n+1).bit_length()-1 if (n+1)&n==0 else (n+1).bit_length()
    return n+1+len(cls)+1+sum((len(c)+1)+len(c)*(1+width) for c in cls)

def source_affine_rows(cls):
    groups=collections.defaultdict(list)
    for c in cls:
        if len(c)!=3 or len({abs(l) for l in c})!=3:return None
        groups[tuple(sorted(abs(l) for l in c))].append(c)
    rows=[]
    for key,block in sorted(groups.items()):
        if len(block)!=4:return None
        truth=[]
        for a in itertools.product([0,1],repeat=3):
            sat=all(any((a[key.index(abs(l))]==int(l>0)) for l in c) for c in block)
            truth.append((a,sat))
        good=[a for a,sat in truth if sat]
        if len(good)!=4:return None
        rhs=sum(good[0])%2
        if any((sum(a)%2==rhs)!=sat for a,sat in truth):return None
        rows.append((sum(1<<(v-1) for v in key),rhs,key))
    return rows

def independent_gauss(n,rows):
    work=[(m,b) for m,b,_ in rows];pivot={}
    for m,b in work:
        while m:
            bit=(m&(-m));p=bit.bit_length()-1
            if p not in pivot:pivot[p]=(m,b);break
            m^=pivot[p][0];b^=pivot[p][1]
        else:
            if b:return False
    return True

def count_replay_nodes(cls,n,order=None,cut=None):
    nodes=0;prune=0
    def recurse(state):
        nonlocal nodes,prune
        nodes+=1
        state=dict(state)
        while True:
            pending=None
            for c in cls:
                seen=False;undecided=[]
                for l in c:
                    v=abs(l)
                    if v in state and state[v]==(l>0):seen=True;break
                    if v not in state:undecided.append(l)
                if seen:continue
                if not undecided:return False
                if len(undecided)==1:pending=undecided[0];break
            if pending is None:break
            state[abs(pending)]=(pending>0)
        if cut:
            ids,par=cut
            if all(v in state for v in ids) and sum(state[v] for v in ids)%2!=par:
                prune+=1;return False
        if all(any(abs(l) in state and state[abs(l)]==(l>0) for l in c) for c in cls):return True
        avail=[v for v in (order or range(1,n+1)) if v not in state]
        if not avail:return False
        v=avail[0]
        return recurse({**state,v:False}) or recurse({**state,v:True})
    result=recurse({})
    return result,nodes,prune

def independent_gray(n,cls):
    scanned=0
    for j in range(1<<n):
        val=j^(j>>1); valid=True
        for c in cls:
            scanned+=1
            if actual_true(c,val)==0:
                valid=False;break
        if valid:return (j+1,scanned,val)
    return (1<<n,scanned,None)

def main(path):
    data=json.load(open(path));errors=[];assert data['run_id']=='CUT-ACQUISITION266'
    cases=data['formulas'];assert len(cases)==16
    checks=0
    for r in cases:
        cls=r['clauses'];n=r['n'];m=len(cls)
        assert m==r['m'];assert clauses_encode_len(n,cls)==r['physical_source_bits'];checks+=1
        for idx,c in enumerate(cls):
            e=r['diagnostics']['occurrences'][idx]
            assert idx+1==e['clause_index'] and c==e['literals'];checks+=1
            for l in c:
                x=str(abs(l));val=int(l>0)
                assert e['S'][x]==val and e['U'][x]==1-val and e['invert_S_is_U'][x]==1-val
                assert e['invert_U_is_S'][x]==val;checks+=4
        for i,c in enumerate(cls):
            for j,d in enumerate(cls[i+1:],start=i+1):
                flags=r['diagnostics']['pair_matrix_4bit'][i][j-i-1]
                for bit,mode in enumerate(['SS','SU','US','UU']):
                    assert bool(flags&(1<<bit))==possible_extremes(c,d,mode),(r['name'],i,j,mode)
                    checks+=1
        for end in r['diagnostics']['endpoints']:
            msk=end['mask'];counts=[actual_true(c,msk) for c in cls]
            assert end['statuses']==counts
            assert end['histogram']==[counts.count(i) for i in range(4)]
            assert end['sat']==all(z>=1 for z in counts)
            checks+=3
        for step in r['diagnostics']['gray_first']:
            i=step['step'];a=i^(i>>1)
            assert step['assignment']==a
            cnt=[actual_true(c,a) for c in cls]
            assert step['N0']==cnt.count(0) and step['N3']==cnt.count(3)
            for j in range(len(cls)):
                assert actual_true(cls[j],a)+actual_true(cls[j],((1<<n)-1)^a)==len(cls[j]);checks+=1
        for step in r['diagnostics']['adaptive_flip_first']:
            a=step['assignment'];ct=[actual_true(c,a) for c in cls]
            assert (ct.count(0),ct.count(3))==(step['N0'],step['N3']);checks+=1
        num,known=original_models(n,cls)
        gvis,gcost,gwitness=independent_gray(n,cls)
        assert (gvis,gcost,gwitness)==(r['diagnostics']['gray_full']['visits'],
           r['diagnostics']['gray_full']['source_clause_tests'],
           r['diagnostics']['gray_full']['witness']);checks+=3
        ledger=r['controller_work_ledger']
        assert r['controller_selected_work']==sum(ledger[v] for v in
           ('source_bit_parse','acquisition_and_switches','DPLL_fallback_guest',
             'child_output_bits','original_witness_check_lits'));checks+=1
        assert num==r['diagnostics']['full_enumeration_models'];checks+=1
        assert r['controller_sat']==(num>0)==r['baseline_sat'];checks+=1
        base,base_nodes,base_prune=count_replay_nodes(cls,n)
        assert base==(num>0) and base_nodes==r['baseline']['nodes'],(r['name'],base_nodes,r['baseline']['nodes']);checks+=2
        rows=source_affine_rows(cls)
        if rows is None:
            assert r['affine_decision'] is None
        else:
            decision=independent_gauss(n,rows)
            assert decision==(num>0)==r['affine_decision']['sat'];checks+=1
            cert=r['affine_decision']
            if decision: assert all(actual_true(c,cert['witness'])>0 for c in cls)
            else:
                sel=cert['dependency'];v=0;b=0
                for j in sel:v^=rows[j][0];b^=rows[j][1]
                assert v==0 and b==1
            checks+=1
        if r['k'] is not None:
            k=r['k'];charges=r['source_charges'];assert len(charges)==2*k
            assert cls==expected_source(k,charges),r['name'];checks+=1
            assert r['canonical_acquisition']['block_queries']==2*k
            assert r['canonical_acquisition']['literal_reads']==24*k
            assert r['terminal_child']['decision']==(sum(charges)%2==0)
            assert r['terminal_child']['physical_bits']<math.sqrt(r['physical_source_bits']);checks+=4
            cut=r['cut_certificate'];assert cut['boundary']==list(range(2*k+1,3*k+1))
            assert cut['required_parity']==sum(charges[:k])%2
            assert len(cut['forbidden_boundary_patterns'])==2**(k-1)
            observed=set()
            for msk in range(1<<n):
                lhs=sum((msk>>(v-1))&1 for v in cut['boundary'])%2
                # For every complete assignment satisfying *top local blocks*, boundary parity follows.
                if all(actual_true(c,msk)>0 for c in cls[:4*k]):
                    assert lhs==cut['required_parity']
                    observed.add(sum(((msk>>(v-1))&1)<<i for i,v in enumerate(cut['boundary'])))
            assert observed=={a for a in range(1<<k) if a.bit_count()%2==cut['required_parity']}
            checks+=1<<n
            order=list(range(2*k+1,3*k+1))+list(range(1,2*k+1))
            plain,pnodes,_=count_replay_nodes(cls,n,order=order)
            cutdec,cnodes,prunes=count_replay_nodes(cls,n,order=order,cut=(cut['boundary'],cut['required_parity']))
            assert plain==cutdec==(num>0)
            assert pnodes==r['rung_order_baseline']['nodes'] and cnodes==r['rung_order_cut']['nodes']
            assert prunes==r['rung_order_cut'].get('cut_prunes',0);checks+=3
        print('VERIFIED',r['name'],'SAT' if num else 'UNSAT','models',num,'baseline_nodes',base_nodes,flush=True)
    # Query lower-bound finite adversarial verification: every one-block charge toggle changes label.
    for k in (3,4):
        q=2*k;views=prism_vertices(k)
        for b in itertools.product([0,1],repeat=q):
            F=expected_source(k,b);rows=source_affine_rows(F)
            assert independent_gauss(3*k,rows)==(sum(b)%2==0);checks+=1
            for v in range(q):
                flip=list(b);flip[v]^=1
                FF=expected_source(k,flip)
                assert F[:4*v]==FF[:4*v] and F[4*(v+1):]==FF[4*(v+1):]
                assert (sum(flip)%2)!=(sum(b)%2);checks+=2
    import copy
    # Deliberate corruptions must fail the *independently reconstructed* invariants.
    sample=next(r for r in cases if r['name']=='prism_q6_SAT')
    broken=copy.deepcopy(sample);broken['terminal_child']['decision']=not broken['terminal_child']['decision']
    assert broken['terminal_child']['decision']!=(sum(broken['source_charges'])%2==0)
    broken=copy.deepcopy(sample);broken['diagnostics']['pair_matrix_4bit'][0][0]^=1
    assert bool(broken['diagnostics']['pair_matrix_4bit'][0][0]&1)!=possible_extremes(broken['clauses'][0],broken['clauses'][1],'SS')
    broken=copy.deepcopy(sample);broken['cut_certificate']['required_parity']^=1
    assert broken['cut_certificate']['required_parity']!=sum(broken['source_charges'][:broken['k']])%2
    print('REJECTED 3 corrupted certificate/compatibility/decision records')
    print('PASS independent checks',checks,'sha256_input' ,hashlib.sha256(open(path,'rb').read()).hexdigest())
    return checks
if __name__=='__main__':main(sys.argv[1])