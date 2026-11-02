#!/usr/bin/env python3
"""LSPV-1 326 hostile NONCANONICAL mixed-polarity DP pivot counterexample.
A single pivot introduces 18, not 12, y-neighbors while the global bound 108 survives.
"""
import itertools,json,random
ROWS=[(1,2,3,4),(1,5,6,7),(1,8,9,10),(1,11,12,13),(-1,2,14,15),(-1,16,17,18),(-1,19,20,21),(-1,22,23,24)]
def graph(rows):
    out={abs(v):set() for c in rows for v in c}
    for c in rows:
        s=set(map(abs,c))
        for x in s:out[x]|=s-{x}
    return out
def eliminate(rows,x):
    p=[set(c)-{x} for c in rows if x in c]
    n=[set(c)-{-x} for c in rows if -x in c]
    other=[c for c in rows if x not in c and -x not in c]
    return [tuple(a|b) for a in p for b in n if all(-v not in a|b for v in a|b)]+other
def sat(rows,a):return all(any(a[abs(v)]==(v>0) for v in c) for c in rows)
def main():
    before=graph(ROWS);proj=eliminate(ROWS,1);after=graph(proj);new=after[2]-before[2]
    assert len(before[2])==5 and len(after[2])==22 and len(new)==18
    P=4;w=4;d=max(map(len,before.values()))
    assert len(after[2])<=d+2*P*(P*(w-1)-1)
    rng=random.Random(326)
    for _ in range(128):
        a={i:rng.choice((False,True)) for i in range(2,25)}
        assert sat(proj,a)==any(sat(ROWS,{**a,1:b}) for b in (False,True))
    return {'status':'PASS','canonical_original':False,'per_sign_P':4,'clause_width':4,
       'old_y_degree':5,'new_y_degree':22,'added_new_y_neighbors':18,
       'naive_per_pivot_12_bound':'FALSIFIED','global_amortized_bound':'SURVIVES',
       'random_original_CNF_vs_projected_circuit_cofactor_checks':128}
if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))