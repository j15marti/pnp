"""Exact minimum fan-in-2 circuit size (gates; wires=2*gates) for n<=3 inputs.
basis 'B2': all 16 binary gates. basis 'DM': AND/OR with free edge negation (NOT-free De Morgan, XOR costs 3).
BFS over sets of computed truth tables; each run <30s. usage: mincirc.py n basis maxg"""
import sys, json, itertools, time
n=int(sys.argv[1]); basis=sys.argv[2]; maxg=int(sys.argv[3])
N=1<<n; M=(1<<N)-1
ins=[sum(1<<r for r in range(N) if (r>>i)&1) for i in range(n)]
def gates(a,b):
    out=set()
    if basis=='B2':
        for t in range(16):
            r=0
            for k,(x,y) in enumerate([(0,0),(1,0),(0,1),(1,1)]):
                if (t>>k)&1:
                    r|=(a if x else ~a&M)&(b if y else ~b&M)
            out.add(r)
    else:
        for x in (a,~a&M):
            for y in (b,~b&M):
                out.add(x&y); out.add(x|y)
    return out
start=frozenset([0,M]+ins)  # constants free
best={}; 
for f in start: best[f]=0
level={start}; seen={start}
t0=time.time()
for g in range(1,maxg+1):
    nxt=set()
    for S in level:
        L=sorted(S)
        for a,b in itertools.combinations(L,2):
            for r in gates(a,b):
                if r in S: continue
                T=S|{r}
                if T in seen: continue
                seen.add(T); nxt.add(T)
                if r not in best: best[r]=g
    level=nxt
    print(g,len(level),len(best),round(time.time()-t0,1),file=sys.stderr)
    if time.time()-t0>20: print("time cut at g=",g,file=sys.stderr); break
else: g=maxg
json.dump({"n":n,"basis":basis,"complete_through_gates":g,"cost":{str(k):v for k,v in best.items()}},open(f"mincirc_n{n}_{basis}.json","w"))
from collections import Counter
print(n,basis,"funcs found",len(best),"of",1<<N,sorted(Counter(best.values()).items()))
par=0
for i in ins: par^=i
print("parity cost",best.get(par),"AND cost",best.get(ins[0]&ins[1] if n>1 else ins[0]))
