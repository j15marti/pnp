#!/usr/bin/env python3
"""Compact independently runnable mathematical controls for MINCOST-DAG-FANIN339.
Full BFS optimizer, independent verifier and raw certificates are in companion archive.
"""
import itertools,json

def forbidden_clause(bits):
    return tuple((i+1 if bit==0 else -(i+1)) for i,bit in enumerate(bits))

def sat(F,assign):
    return all(any((x>0)==assign[abs(x)-1] for x in C) for C in F)

def models(F,n):
    return [a for a in itertools.product((0,1),repeat=n) if sat(F,a)]

def parity_clauses(support,rhs):
    return [tuple(v if b==0 else -v for v,b in zip(support,a))
            for a in itertools.product((0,1),repeat=len(support))
            if sum(a)%2!=rhs]

def fanin_lower(m,d):
    return (m-2)//(d-1)+1 if m>1 else 0

def main():
    F=[forbidden_clause(a) for a in itertools.product((0,1),repeat=3)]
    assert len(F)==8 and not models(F,3)
    assert all(len(models(F[:j]+F[j+1:],3))==1 for j in range(8))
    p0=parity_clauses((1,2,3),0);p1=parity_clauses((1,2,3),1)
    assert len(p0)==len(p1)==4
    assert set(p0)|set(p1)==set(F)
    assert len(models(p0,3))==len(models(p1,3))==4
    # Two 4-antecedent parity recognizers and a 2-antecedent XOR sum.
    assert fanin_lower(8,4)==3
    assert fanin_lower(8,2)==7
    edges=list(itertools.combinations(range(4),2));K4=[]
    for v,charge in enumerate((1,0,0,0)):
        K4+=parity_clauses(tuple(i+1 for i,e in enumerate(edges) if v in e),charge)
    assert len(K4)==16 and not models(K4,6)
    K4even=[]
    for v in range(4):
        K4even+=parity_clauses(tuple(i+1 for i,e in enumerate(edges) if v in e),0)
    assert len(models(K4even,6))==8
    data={'R4_full_cube_exact_inference_nodes':3,'pure_resolution_exact':7,
          'K4_R4_lower':fanin_lower(16,4),'K4_affine_upper':7,
          'parity_half_sat_models':4,'K4_even_sat_models':8,
          'proof':{'steps':['four-source XOR=0','four-source XOR=1','xor contradiction'],
                   'all_eight_original_clause_dependencies':True},
          'limitation':'No arbitrary-decider simulation or unrestricted SAT lower bound'}
    print(json.dumps(data,indent=2,sort_keys=True))
if __name__=='__main__':main()
