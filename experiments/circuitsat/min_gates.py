"""Exact minimum fan-in-2 circuit size (basis B2: all 10 nondegenerate binary gates)
for every n-input Boolean function, n<=3, by BFS over sets of computed truth tables.
Wires = 2*gates (+1 output wire). Stage budget: depth cap argv[2] (default 5), n=argv[1]."""
import sys, json, itertools, time
n=int(sys.argv[1]); cap=int(sys.argv[2]) if len(sys.argv)>2 else 5
N=1<<n; M=(1<<N)-1
inp=[sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)]
ops=[lambda a,b:a&b,lambda a,b:a&~b&M,lambda a,b:~a&b&M,lambda a,b:a|b,lambda a,b:(a^b),
     lambda a,b:~(a^b)&M,lambda a,b:~(a|b)&M,lambda a,b:~(a&b)&M,lambda a,b:(a|~b)&M,lambda a,b:(~a|b)&M]
best={f:0 for f in inp}; best[0]=None; 
layer={frozenset()}; t0=time.time(); found={}
for f in inp: found[f]=0
for d in range(1,cap+1):
    new=set()
    for S in layer:
        T=list(inp)+list(S); have=set(T)
        for a,b in itertools.combinations(T,2):
            for op in ops:
                c=op(a,b)
                if c in have or c in (0,M): 
                    if c in (0,M) and c not in found: found[c]=d
                    continue
                if c not in found: found[c]=d
                new.add(S|{c})
    layer=new
    print(d,len(layer),len(found),round(time.time()-t0,1),file=sys.stderr)
    if time.time()-t0>20: cap=d; break
from collections import Counter
cnt=Counter(found.values())
print(json.dumps({"n":n,"depth_completed":d,"functions_total":1<<N,"functions_resolved":len(found),
  "histogram_gates":dict(sorted(cnt.items())),
  "single_point_min_gates":found.get(1<<(N-1)),"note":"constants cost 1 gate here (x AND NOT x)" }))
