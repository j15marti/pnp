#!/usr/bin/env python3
"""MULTISAT-CIRCUIT-COMPOSE1 exact reproducible finite checks, Python stdlib."""
from itertools import product, combinations
import json

def monotone(table,k):
    return all(not (x & ~y == 0 and table[x] > table[y])
               for x in range(1<<k) for y in range(1<<k))
def closure(table,b):
    return int(any(table[u] for u in range(len(table)) if u & ~b == 0))
def check_outer(k):
    count_mon=count_exact=0; counterexample=None
    for v in range(1<<(1<<k)):
        t=[(v>>x)&1 for x in range(1<<k)]
        mon=monotone(t,k)
        exact=all(t[b]==closure(t,b) for b in range(1<<k))
        assert mon==exact
        count_mon+=mon; count_exact+=exact
        if not exact and counterexample is None:
            b=next(b for b in range(1<<k) if t[b]!=closure(t,b))
            counterexample={"truth_table":t,"oracle_b":b,
                           "oracle_value":t[b],"existential_value":closure(t,b)}
    return {"k":k,"tested":1<<(1<<k),"monotone":count_mon,
            "exact":count_exact,"counterexample":counterexample}
def eval_3cnf(patterns,x):
    return int(all(any(x[j]!=s[j] for j in range(3)) for s in patterns))
def outputs_3cnf(patterns):
    return sorted({eval_3cnf(patterns,x) for x in product((0,1),repeat=3)})
def identity_gadget(e):
    return int(any(all(e or a!=sa or b!=sb for sa,sb in product((0,1),repeat=2))
               for a,b in product((0,1),repeat=2)))
def has_triangle(g,n=4):
    edges=list(combinations(range(n),2))
    present={e for j,e in enumerate(edges) if (g>>j)&1}
    return int(any(all(edge in present for edge in combinations(t,2))
               for t in combinations(range(n),3)))
def clique_check():
    n=4; k=n*(n-1)//2
    for g in range(1<<k):
        b=sum(identity_gadget((g>>j)&1)<<j for j in range(k))
        assert has_triangle(g,n)==has_triangle(b,n)
    return {"graphs":1<<k,"mismatches":0}
def query_check():
    count=0
    for k in range(1,5):
        for m in range(2,6):
            a=[int(j%m==0) for j in range(k*m)]
            f=lambda x:int(all(sum(x[i*m:(i+1)*m])%2 for i in range(k)))
            assert f(a)==1
            for j in range(k*m):
                z=a[:];z[j]^=1;assert f(z)==0;count+=1
    return {"sensitivity_assertions":count}
def run():
    patterns=list(product((0,1),repeat=3))
    assert outputs_3cnf(patterns)==[0]
    assert outputs_3cnf(patterns[:-1])==[0,1]
    assert [identity_gadget(0),identity_gadget(1)]==[0,1]
    r={"report":"MULTISAT-CIRCUIT-COMPOSE1",
       "outer_k2":check_outer(2),"outer_k3":check_outer(3),
       "threecnf":{"all8":outputs_3cnf(patterns),
                   "seven":outputs_3cnf(patterns[:-1]),
                   "identity":[identity_gadget(0),identity_gadget(1)]},
       "clique":clique_check(),"query":query_check()}
    print(json.dumps(r,indent=2))
if __name__=="__main__": run()
