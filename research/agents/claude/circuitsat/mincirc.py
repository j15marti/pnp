# Exact minimum fan-in-2 circuit size (basis B2 = all 16 binary gates, free negation) for n<=3 inputs.
# Method: BFS over sets of computed functions, normalized (f ~ not f); iterative deepening on gate count.
import sys, json, itertools
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
def norm(f): return min(f,M^f)
inputs=[]
for i in range(n):
    f=0
    for x in range(N):
        if (x>>i)&1: f|=1<<x
    inputs.append(norm(f))
ops=[lambda a,b:a&b, lambda a,b:a&(M^b), lambda a,b:(M^a)&b, lambda a,b:(M^a)&(M^b)]
# AND-type gates with free negation of output cover AND/OR/NAND/..; add XOR
ops.append(lambda a,b:a^b)
best={}  # function -> min gates
start=frozenset(inputs|{0}) if False else frozenset(inputs+[0])
level={start}; seen={start}; g=0
for f in start: best.setdefault(f,0)
while level and g<8:
    g+=1; nxt=set()
    for S in level:
        L=list(S)
        for a,b in itertools.combinations(L,2):
            for op in ops:
                for A in (a,M^a):
                  for B in (b,M^b):
                    c=norm(op(A,B))
                    if c in S: continue
                    T=S|{c}
                    if T not in seen:
                        seen.add(T); nxt.add(T)
                    best.setdefault(c,g)
    level=nxt
    if len(best)>=(1<<(N-1)): break
from collections import Counter
dep=lambda f: all(any(((f>>x)&1)!=((f>>(x^(1<<i)))&1) for x in range(N)) for i in range(n))
cnt=Counter(best.values())
print(n,"dist",sorted(cnt.items()),"max",max(best.values()),"funcs",len(best),"of",1<<(N-1))
alld=[v for f,v in best.items() if dep(f)]
print("min gates among functions depending on all inputs:",min(alld),"max:",max(alld))
