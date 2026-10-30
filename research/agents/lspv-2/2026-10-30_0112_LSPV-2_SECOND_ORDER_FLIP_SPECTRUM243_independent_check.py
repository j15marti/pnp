#!/usr/bin/env python3
"""Independent brute checker of source-indexed raw Hamming-2 spectrum and DPLL proof trees.

No dependency on the producer's SAT/UP/evaluation implementations.
Usage: python *_independent_check.py path_to_raw.json
"""
import collections,itertools,json,sys

def clause_status(c,a):return sum((l>0)==bool(a[abs(l)]) for l in c)

def grade(F,a):
    count=[0,0,0,0]
    for c in F:count[clause_status(c,a)]+=1
    return tuple(count)

def independent_UP(F,a):
    a=dict(a)
    while True:
        unit=None
        for j,c in enumerate(F):
            if any(abs(l) in a and ((l>0)==bool(a[abs(l)])) for l in c):continue
            rest=[l for l in c if abs(l) not in a]
            if not rest:return a,j+1
            if len(rest)==1:
                unit=rest[0];break
        if unit is None:return a,None
        a[abs(unit)]=int(unit>0)

def replay_unsat(F,n,tree,assigned=None):
    a,conflict=independent_UP(F,{} if assigned is None else assigned)
    if conflict is not None:
        assert 'conflict' in tree and 'branches' not in tree
        return (1,1)
    assert 'branches' in tree and 'conflict' not in tree
    branches=tree['branches']
    assert len(branches)==2 and branches[0]['value']==0 and branches[1]['value']==1
    x=branches[0]['decision_original_var']
    assert x not in a and all(z['decision_original_var']==x for z in branches)
    states=1;leaves=0
    for z in branches:
        nexta=dict(a);nexta[x]=z['value']
        s,l=replay_unsat(F,n,z['child'],nexta);states+=s;leaves+=l
    return states,leaves

def check(raw):
    good=0;hamming_cases=0;quad_status_checks=0;proof_leaves=0;pair_checks=0
    for c in raw['cases']:
        F=[tuple(z) for z in c['clauses']];n=c['n']
        s=c['four_category_radius2_spectrum_from_zero']
        if s is not None:
            a={i:0 for i in range(1,n+1)}
            for d in range(3):
                observed=collections.Counter()
                for S in itertools.combinations(range(1,n+1),d):
                    v=dict(a)
                    for i in S:v[i]^=1
                    original=grade(F,v)
                    observed[original]+=1
                    comp={i:1-w for i,w in v.items()}
                    assert grade(F,comp)==tuple(reversed(original))
                    quad_status_checks+=len(F)
                recorded={tuple(x['N']):x['count'] for x in s[f'hamming{d}_histogram']}
                assert dict(observed)==recorded,(c['case'],d,observed,recorded)
                hamming_cases+=len(list(itertools.combinations(range(1,n+1),d)))
        for x in c['original_occurrences_and_S_U_targets']:
            j=x['j'];cl=F[j-1]
            for occ in x['occurrences']:
                l=occ['source_literal'];v=abs(l)
                assert occ['source_clause']==j and occ['variable']==v
                assert occ['S_local_target']==int(l>0)
                assert occ['U_local_target']==int(l<0)
                assert occ['inverse_of_S_is_U']==occ['U_local_target']
                assert occ['inverse_of_U_is_S']==occ['S_local_target']
        for pair in c['source_indexed_four_way_compatibility']:
            a=F[pair['source_j']-1];b=F[pair['source_k']-1]
            scopes=sorted({abs(z) for z in a+b})
            em={p:False for p in ('SS','SU','US','UU')}
            for bits in itertools.product((0,1),repeat=len(scopes)):
                y=dict(zip(scopes,bits));ta=clause_status(a,y);tb=clause_status(b,y)
                key=('S' if ta==len(a) else 'U' if ta==0 else 'M')+('S' if tb==len(b) else 'U' if tb==0 else 'M')
                if key in em:em[key]=True
                pair_checks+=1
            assert em==pair['SS_SU_US_UU']
        for a in (c['baseline_solver'],c['two_endpoints_then_fallback']):
            if a['SAT']:
                w={int(i):v for i,v in a['witness'].items()}
                assert all(clause_status(cl,w)>=1 for cl in F)
            else:
                nodes,leaves=replay_unsat(F,n,a['unsat_certificate'])
                assert nodes==a['stats']['DPLL_states']
                proof_leaves+=leaves
        cube=c['source_parent_prohibited_cube']
        if cube:
            j,k=cube['original_parents'];u=F[j-1];v=F[k-1];i=cube['pivot_original_variable']
            pin={int(x):val for x,val in cube['forbidden_original_variable_cube'].items()}
            ru=[z for z in u if abs(z) not in pin]
            rv=[z for z in v if abs(z) not in pin]
            assert len(ru)==len(rv)==1 and ru[0]==-rv[0] and abs(ru[0])==i
            assert all(not ((z>0)==bool(pin[abs(z)])) for z in u+v if abs(z) in pin)
        good+=1
    return {'independently_checked_sources':good,'Hamming_0_to_2_candidate_states':hamming_cases,
            'clause_status_complement_checks':quad_status_checks,
            'source_pair_assignment_checks':pair_checks,'independently_replayed_UNSAT_DPLL_leaves':proof_leaves,
            'status':'PASS'}
if __name__=='__main__':
    raw=json.load(open(sys.argv[1]));result=check(raw)
    print(json.dumps(result,indent=2))
