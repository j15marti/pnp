#!/usr/bin/env python3
"""TMR-2/097. Compact standard-library independent exact private-head audit.
Every graph on n=3..5 vertices; original coloring candidate costs explicit.
Does not claim polynomial counting time or physical RAM measurement.
"""
import itertools, json
R=lambda a,b: (b-a)%5 in (1,3)
Q=lambda h,u,v: R(h,u)!=R(h,v)
assert [[j for j in range(5) if R(i,j)] for i in range(5)] == [[1,3],[2,4],[0,3],[1,4],[0,2]]
assert sum(Q(*x) for x in itertools.product(range(5),repeat=3))==60
assert sum(R(x[0],x[1]) and R(x[0],x[2]) for x in itertools.product(range(5),repeat=3))==20
counts={"graphs":0,"assignments":0,"prefix_edge_tests":0,"digit_checks":0,"palindrome_checks":0}
for n in (3,4,5):
    pairs=list(itertools.combinations(range(n),2))
    for mask in range(1<<len(pairs)):
        es=[p for i,p in enumerate(pairs) if mask>>i&1]
        m=len(es); c=[0]*(m+1)
        for x in itertools.product(range(5),repeat=n):
            counts["assignments"]+=1; s=0; good=True
            for u,v in es:
                counts["prefix_edge_tests"]+=1
                d=(x[u]-x[v])%5
                if not d: good=False;break
                s+=d in (1,4)
            if good:c[s]+=1
        assert c==c[::-1]; counts["palindrome_checks"]+=m+1
        if m:
            assert all(y%10==0 for y in c)
            if m%2==0:assert c[m//2]%20==0
        t=3*n+1; B=1<<t
        # Simulated oracle output obtained by exact original-label enumeration.
        z=(1<<(t*m))*sum(y*B**i for i,y in enumerate(c))
        digits=[]; k=z>>(t*m)
        for _ in range(m+1):
            digits.append(k%B);k//=B
        assert k==0 and digits==c
        counts["digit_checks"]+=m+1;counts["graphs"]+=1
assert counts=={"graphs":1096,"assignments":3241000,"prefix_edge_tests":10450225,"digit_checks":6420,"palindrome_checks":6420}
print(json.dumps({"status":"PASS","counts":counts},sort_keys=True))
