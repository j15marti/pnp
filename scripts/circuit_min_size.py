# Exact minimum fan-in-2 circuit size (basis B2: all 16 binary gates) for all n-input functions.
# n=1..3 exhaustive (runs in a few seconds). Wires = 2*gates (+ output tap).
import sys, json, itertools
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
inp=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
best={}  # function(tt)->min gates
def gates(a,b):
    for g in range(16):
        r=0
        for k,(x,y) in enumerate(((0,0),(0,1),(1,0),(1,1))):
            if (g>>k)&1:
                r|=(a if x else ~a&M)&(b if y else ~b&M)
        yield r
for f in inp+[0,M]: best[f]=0
def dfs(sigs,k,limit):
    for f in sigs:
        if f not in best or best[f]>len(sigs)-n: pass
    for i in range(len(sigs)):
        for j in range(i+1,len(sigs)):
            for r in gates(sigs[i],sigs[j]):
                if r in sigs: continue
                g=len(sigs)+1-n
                if r not in best or best[r]>g: best[r]=g
                if g<limit: dfs(sigs+[r],k,limit)
L=int(sys.argv[2])
dfs(list(inp),0,L)
tot={}
for f,g in best.items(): tot[g]=tot.get(g,0)+1
print(n,"covered",len(best),"of",1<<N,"hist",sorted(tot.items()))
essential=lambda f:all(any(((f>>x)&1)!=((f>>(x^(1<<i)))&1) for x in range(N)) for i in range(n))
ess=[g for f,g in best.items() if essential(f)]
print("max size over all covered:",max(best.values()),"; all-inputs-essential: min",min(ess),"max",max(ess))
