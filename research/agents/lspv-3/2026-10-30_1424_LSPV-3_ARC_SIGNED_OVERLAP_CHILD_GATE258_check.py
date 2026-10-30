#!/usr/bin/env python3
"""ARC258 independent verification: does not import producer/solver.
Recomputes signed-22 exact overlap identities, original S/U modes, endpoint
complements, source-checked cube-cover integrity and SAT/UNSAT truth tables.
"""
import json, math, itertools, random, sys
from collections import Counter
from fractions import Fraction

def valid(F, bits):
    return all(any(((bits>>(abs(l)-1))&1)==(l>0) for l in clause) for clause in F)

def classify(F, pins):
    kept=[];deleted=0;counts=[];bad=None
    for j,c in enumerate(F,1):
        t=sum(pins[abs(l)]==(l>0) for l in c if abs(l) in pins)
        counts.append(t)
        if t:deleted+=1
        else:
            c2=[l for l in c if abs(l) not in pins]
            if not c2:bad=j
            else:kept.append(c2)
    return (None if bad else kept),bad,deleted,counts

def independent_cover(F, bit_limit, policy):
    n=max(abs(l) for c in F for l in c)
    m=len(F);b=1+math.ceil(math.log2(n+1))
    H=math.ceil(math.log2(n+1))+math.ceil(math.log2(m+1))
    stack=[{}];cnt=Counter();mass=Counter();nodes=0
    while stack:
        pins=stack.pop();nodes+=1;k=len(pins)
        R,bad,deleted,tt=classify(F,pins)
        if bad is not None:
            assert all(abs(l) in pins and pins[abs(l)]!=(l>0) for l in F[bad-1])
            cnt['source_conflict']+=1;mass['source_conflict']+=1<<(n-k);continue
        bits=H+sum(2+b*len(c) for c in R)
        if bits<=bit_limit:
            cnt['emitted']+=1;mass['emitted']+=1<<(n-k)
            remaining=[v for v in range(1,n+1) if v not in pins]
            sat=False
            for mask in range(1<<len(remaining)):
                q=dict(pins)|{v:((mask>>i)&1) for i,v in enumerate(remaining)}
                if all(any(q[abs(l)]==(l>0) for l in c) for c in F):sat=True;break
            cnt['SAT_guest' if sat else 'UNSAT_guest']+=1
            continue
        unassigned=[v for v in range(1,n+1) if v not in pins]
        assert unassigned
        if policy=='maxdeg':
            degrees=Counter(abs(l) for c in R for l in c)
            v=max(unassigned,key=lambda x:(degrees[x],-x))
        else:v=unassigned[0]
        stack.extend((dict(pins)|{v:1}, dict(pins)|{v:0}))
    assert sum(mass.values())==1<<n
    return {'nodes':nodes,'leaf_counts':dict(cnt),'covered_assignments':dict(mass)}

def run(path):
    s=json.load(open(path));rng=random.Random(982345)
    total=0;rows=[]
    for obj in s['cases']:
        F=[list(v['lits']) for v in obj['local_targets']]
        n=obj['n'];m=obj['m']; assert len(F)==m
        count=Counter()
        for c in F:
            assert len(c)==3 and len({abs(l) for l in c})==3
            for l in c:count[(abs(l),l>0)]+=1
        assert all(count[(v,True)]==2 and count[(v,False)]==2 for v in range(1,n+1)); total+=2*n
        for T in obj['local_targets']:
            c=T['lits'];j=T['j'];S=T['S_j'];U=T['U_j']
            assert set(map(int,S))==set(map(abs,c)) and {str(abs(l)):int(l>0) for l in c}=={str(k):v for k,v in S.items()}
            assert {str(k):1-v for k,v in S.items()}=={str(k):v for k,v in U.items()}
            assert T['invert_S_to_U']==U and T['invert_U_to_S']==S
            assert [d['literal'] for d in T['occurrences']]==c
            total+=len(c)+4
        def merge(A,B):
            return all(str(z) not in B or B[str(z)]==value for z,value in A.items())
        for P in obj['pair_compatibility']:
            A=obj['local_targets'][P['j']-1];B=obj['local_targets'][P['k']-1]
            for key,sa,sb in [('SS','S_j','S_j'),('SU','S_j','U_j'),('US','U_j','S_j'),('UU','U_j','U_j')]:
                assert P['modes'][key]==merge(A[sa],B[sb]);total+=1
        for val,label in [(0,'zero'),(1,'one')]:
            a={v:val for v in range(1,n+1)}
            cc=Counter(sum(a[abs(l)]==(l>0) for l in c) for c in F)
            assert obj['endpoint_audit'][label]['counts']==[cc[i] for i in range(4)];total+=m
        for _ in range(3072):
            pins={v:rng.randrange(2) for v in range(1,n+1) if rng.randrange(4)==0}
            t=[sum(pins[abs(l)]==(l>0) for l in c if abs(l) in pins) for c in F]
            d=sum(x>0 for x in t);omega=sum(max(0,x-1) for x in t)
            assert sum(t)==2*len(pins) and d==2*len(pins)-omega
            R,bad,dd,tt=classify(F,pins);assert d==dd and t==tt
            if R is not None:assert len(R)==m-d
            total+=3
        if n<=15:
            for policy in ('min','maxdeg'):
                truth=independent_cover(F,obj['FLMV_proposed_child_bit_cap'],policy)
                want=obj['literal_bit_budget_cover'][policy]
                assert truth['nodes']==want['visited_nodes']
                for k in ('emitted','source_conflict'):
                    assert truth['leaf_counts'].get(k,0)==want['leaf_counts'].get(k,0)
                    assert truth['covered_assignments'].get(k,0)==want['covered_assignments'].get(k,0)
                assert truth['leaf_counts'].get('SAT_guest',0)==want['child_sat']
                assert truth['leaf_counts'].get('UNSAT_guest',0)==want['child_unsat']
                total+=truth['nodes']
            models=sum(valid(F,mask) for mask in range(1<<n))
            assert models==obj['exact_number_of_models']
            assert bool(models)==obj['SAT'];total+=1<<n
        for typ in ('optimistic_clause_count_cover','literal_bit_budget_cover'):
            for key,v in obj.get(typ,{}).items():
                if v.get('capped'):continue
                assert v['partition_fraction']=='1'
                assert sum(v['covered_assignments'].values())==1<<n
                assert sum(v['leaf_counts'].values())*2-1==v['visited_nodes']
                if v['metric']=='bits':assert v['maximum_actual_emitted_child_bits']<=obj['FLMV_proposed_child_bit_cap']
                if v['minimum_emitted_cube_depth'] is not None:
                    # Strengthened polarity-aware necessary depth.
                    rr=(obj['certified_min_cube_depth_exact22_polarity_and_min_unit_bitwidth'] if v['metric']=='bits' else max(0,math.ceil((m-obj['FLMV_proposed_child_bit_cap'])/2)))
                    assert v['minimum_emitted_cube_depth']>=rr
                    assert v['leaf_counts']['emitted']>=math.ceil(v['covered_assignments']['emitted']/(2**(n-rr)))
                if v['SAT_by_OR_children'] is not None:assert v['SAT_by_OR_children']==obj['SAT']
                total+=7
        rows.append({'source':obj['name'],'n':n,'m':m,'models':obj.get('exact_number_of_models'),'pair_mode_checks':len(obj['pair_compatibility'])*4})
    assert s['cover_verifier_coNP']['checked_G']==256
    print(json.dumps({'status':'passed','checked_claims':total,'source_results':rows,'note':'independent finite verification; no arbitrary-machine runtime conclusion'},sort_keys=True,indent=2))

if __name__=='__main__':run(sys.argv[1] if len(sys.argv)>1 else '/mnt/data/arc258/raw.json')
