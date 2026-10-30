"""Min AIG size (AND gates, free edge negation) for all n-input functions, n<=3.
Wires = 2*gates + 1 (output).  Also: SAT-critical wire counts.  Runs in seconds."""
import sys, json, itertools
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
base=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
best={}  # tt -> min gates
def rec(funcs,g,maxg):
    for t in funcs: 
        for u in (t,M^t):
            if u not in best or best[u]>g: best[u]=g
    if g==maxg: return
    L=len(funcs)
    seen=set()
    cand=[]
    for i in range(L):
        for j in range(i,L):
            for a in (0,1):
                for b in (0,1):
                    x=funcs[i]^(M if a else 0); y=funcs[j]^(M if b else 0)
                    z=x&y
                    if z in funcs or z in seen: continue
                    seen.add(z); cand.append(z)
    for z in cand: rec(funcs+[z],g+1,maxg)
maxg=int(sys.argv[2])
rec([0]+base,0,maxg)
hist={}
for t,g in best.items(): hist[g]=hist.get(g,0)+1
print(n,"covered",len(best),"of",1<<N,"hist(gates:count)",dict(sorted(hist.items())))
print("max gates among covered",max(best.values()))
json.dump({"n":n,"maxg":maxg,"covered":len(best),"total":1<<N,"hist":hist},open(f"aig_n{n}.json","w"))
