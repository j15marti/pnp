#!/usr/bin/env python3
"""Finite controls for log-support observed-port quotient; not a native Rmix341 proof checker."""
import itertools, json

def outputs(bits):
    n = len(bits)
    return [int(all(bits)), int(any(bits)), sum(bits)%2,
            int(sum(bits)>=(n+1)//2), int(bits[0]),
            int(not bits[-1]), int(bits[0] and not bits[-1])]

def eval_dnf(terms,bits):
    return int(any(all(bool(v)==bool(t) for v,t in zip(bits,term)) for term in terms))

def trial(b):
    assignments = list(itertools.product((0,1), repeat=b))
    observed = [[outputs(bits)[j] for bits in assignments] for j in range(7)]
    banks = [[bits for bits,val in zip(assignments,obs) if val] for obs in observed]
    for bits in assignments:
        original=outputs(bits)
        replacement=[eval_dnf(terms,bits) for terms in banks]
        assert original==replacement,(b,bits,original,replacement)
    return dict(b=b,r=7,assignments=len(assignments),
                truth_masks=[''.join(map(str,obs)) for obs in observed],
                true_minterms=[len(ts) for ts in banks],budget_gates=7*b*2**b,
                all_joint_vectors_equal=True)

def grammar(clauses):
    return all(bool(c) and all(1<=abs(l)<=2 for l in c)
               and len(set(abs(l) for l in c))==len(c) for c in clauses)

def sat(clauses):
    return any(all(any((values[abs(l)-1] if l>0 else not values[abs(l)-1])
                       for l in clause) for clause in clauses)
               for values in itertools.product((False,True),repeat=2))

def nmodels(charges):
    edges=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    return sum(all(sum(vals[i] for i,e in enumerate(edges) if v in e)%2==charges[v]
                   for v in range(4))
               for vals in itertools.product((0,1), repeat=6))

def main():
    trials=[trial(b) for b in range(1,7)]
    cases={'SAT':[[(1,)],[(1,2),(-1,2)]],
           'UNSAT':[[(1,),(-1,)],[(1,2),(-1,),(-2,)]],
           'MALFORMED':[[(0,)],[(3,)],[(1,-1,0)]]}
    counts={}
    for expected,items in cases.items():
        for clauses in items:
            label='MALFORMED' if not grammar(clauses) else 'SAT' if sat(clauses) else 'UNSAT'
            assert label==expected,(expected,clauses,label)
        counts[expected]=len(items)
    assert nmodels((0,0,0,0))==8
    assert nmodels((1,0,0,0))==0
    record=dict(id='LSPV1_389_LOG_SUPPORT_GLOBAL_BIT_BUDGET',
                model='syntactic observed-port fragment, NOT full Rmix341',
                trials=trials,controls=counts,k4_parity=dict(even_models=8,odd_models=0),
                assertions=sum(x['assignments']*7 for x in trials)+sum(counts.values())+2,
                independence='producer Python; verifier JS separately implemented')
    print(json.dumps(record,indent=2,sort_keys=True))
if __name__=='__main__':
    main()
