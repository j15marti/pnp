#!/usr/bin/env python3
"""Independent source-side verifier, no imports from producer, finite exhaustive checks."""
import collections, itertools, json, random, sys, math

def source(c):return tuple(tuple(int(x) for x in t.split()) for t in c.split(';'))
def literals_true(F,a):return tuple(sum(a[abs(z)]==int(z>0) for z in clause) for clause in F)
def count(F,a):
    u=literals_true(F,a);return tuple(u.count(i) for i in range(4))
def full_sat(F,a):return all(any(a[abs(z)]==int(z>0) for z in clause) for clause in F)
def up(F,pin):
    a=dict(pin)
    while True:
        progress=False
        for j,c in enumerate(F,1):
            if any(abs(z) in a and a[abs(z)]==int(z>0) for z in c):continue
            free=[z for z in c if abs(z) not in a]
            if not free:return None,j
            if len(free)==1:
                z=free[0];a[abs(z)]=int(z>0);progress=True;break
        if not progress:return a,None

def check_tree(F,n,node,decisions=None):
    if decisions is None:decisions={}
    forced,conf=up(F,decisions)
    if conf is not None:
        assert 'conflict' in node
        assert node['conflict']['falsified_original_clause']==conf
        assert node['conflict']['pin']==forced if forced is not None else True
        return 1
    assert 'children' in node and len(node['children'])==2
    x=next((i for i in range(1,n+1) if i not in forced),None)
    assert x is not None
    out=0
    for v,c in enumerate(node['children']):
        assert c['x']==x and c['value']==v
        D=dict(forced);D[x]=v
        out+=check_tree(F,n,c['subproof'],D)
    return out

def run(path):
    data=json.load(open(path));stats=collections.Counter();rand=random.Random(202610300245)
    for item in data['cases']:
        F=tuple(tuple(x) for x in [r['literals'] for r in item['local_S_U_targets_with_inversions']]);n=item['n']
        assert set(abs(z) for c in F for z in c)==set(range(1,n+1))
        # Source signed occurrence targets and their inverses.
        for row in item['local_S_U_targets_with_inversions']:
            for z in row['source_occurrences']:
                lit=z['signed_literal'];S=int(lit>0);U=int(lit<0)
                assert z['S_local_literal_true']==S and z['invert_S_gives_U']==U
                assert z['U_local_literal_false']==U and z['invert_U_gives_S']==S
                stats['independently_checked_signed_occurrences']+=1
        for mode in item['coherent_endpoint_and_flip_trails'].values():
            for snap in mode:
                a={i+1:v for i,v in enumerate(snap['assignment'])}
                assert list(literals_true(F,a))==snap['original_clause_true_literal_counts']
                assert list(count(F,a))==snap['N0_N1_N2_N3']
                assert full_sat(F,a)==snap['source_formula_SAT']
                stats['coherent_flip_trail_steps']+=1
        # Separate pair checker uses direct all assignments on combined scopes.
        for row in item['source_clause_SS_SU_US_UU_matrix']:
            j=row['source_clause_j']-1;k=row['source_clause_k']-1
            scope=sorted(set(abs(z) for c in [F[j],F[k]] for z in c))
            o={q:False for q in ('SS','SU','US','UU')}
            for bits in itertools.product((0,1),repeat=len(scope)):
                a=dict(zip(scope,bits));T=[sum(a[abs(z)]==int(z>0) for z in F[v]) for v in (j,k)]
                code=''.join('S' if u==len(F[v]) else 'U' if u==0 else 'M' for u,v in zip(T,(j,k)))
                if code in o:o[code]=True
                stats['pair_source_enumeration_assignments']+=1
            assert o==row['SS_SU_US_UU']
        # Exhaustively validate every full three-flip coherent assignment for n<=15.
        a0={i:0 for i in range(1,n+1)}
        if n<=15:
            observed=collections.Counter()
            for triple in itertools.combinations(range(1,n+1),3):
                a=dict(a0)
                for x in triple:a[x]=1
                observed[count(F,a)]+=1
            expected={tuple(z['N0_N1_N2_N3']):z['count'] for z in item['three_flip_spectrum']['three_flip_histogram']}
            assert observed==expected
            stats['coherent_exhaustive_three_flip_assignments']+=math.comb(n,3)
        else:
            for trial in range(min(500,math.comb(n,3))):
                triple=rand.sample(range(1,n+1),3);a=dict(a0)
                for x in triple:a[x]=1
                target=count(F,a)
                assert any(tuple(v['N0_N1_N2_N3'])==target and v['count']>0 for v in item['three_flip_spectrum']['three_flip_histogram'])
                stats['sampled_large_three_flip_assignments']+=1
        # Every recorded resolved cube is a source-parent RUP contradiction.
        res=item['one_source_parent_resolvent_and_forbidden_cube']
        if res:
            parents=[F[j-1] for j in res['source_clause_parents']]
            p=res['pivot'];z={int(i):v for i,v in res['forbidden_source_variable_cube'].items()}
            l=[z[abs(u)]==int(u>0) for u in res['non_tautological_resolvent']]
            assert not any(l)
            a,bad=up(parents,z)
            assert bad is not None
            stats['source_authenticated_resolvent_cubes']+=1
        comp=item.get('solver_comparison')
        if comp:
            for name in ('baseline','spectrum_fallback','endpoint_first'):
                sol=comp[name]
                if sol['sat']:
                    assert full_sat(F,{int(i):int(v) for i,v in sol['witness'].items()})
                    stats['independent_SAT_witnesses_checked']+=1
                else:
                    assert sol['unsat_certificate'] is not None
                    leaves=check_tree(F,n,sol['unsat_certificate'])
                    assert leaves>0
                    stats['DPLL_UNSAT_refutation_leaves_replayed']+=leaves
    for case in data['width2_controls']:
        F=tuple(tuple(r['literals']) for r in case['source_extremes']);n=case['n']
        for mask in range(1<<n):
            a={i:mask>>(i-1)&1 for i in range(1,n+1)}
            u=count(F,a);b={i:1-v for i,v in a.items()};v=count(F,b)
            assert u[0]==v[2] and u[1]==v[1] and u[2]==v[0] and u[3]==v[3]==0
            stats['width2_complement_checks']+=1
        if case['SAT']:
            assert full_sat(F,{int(k):int(v) for k,v in case['SAT_witness'].items()})
        else:
            stats['width2_UNSAT_refutation_leaves_replayed']+=check_tree(F,n,case['UNSAT_refutation_tree'])
    return dict(stats)
if __name__=='__main__':
    x=run(sys.argv[1]);print(json.dumps(x,indent=2))
    with open(sys.argv[2] if len(sys.argv)>2 else 'independent_check.json','w') as f:json.dump(x,f,indent=2)