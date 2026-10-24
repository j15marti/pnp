# Exact min fan-in-2 (basis B2: all 16 binary gates) circuit size per function, n<=3, via BFS over signal sets.
import sys, itertools, json, time
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
inp=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
best={}  # function -> min gates
start=frozenset(inp+[0,M]); 
for f in start: best[f]=0
frontier={start}; seen={start}; g=0; t=time.time()
while frontier and g<6:
    g+=1; nxt=set()
    for S in frontier:
        L=list(S)
        for a,b in itertools.combinations(L,2):
            for op in range(16):
                r=0
                for x in (0,1):
                    for y in (0,1):
                        if (op>>(2*x+y))&1:
                            r|=((a if x else a^M)&(b if y else b^M))
                S2=S|{r}
                if r in S or S2 in seen: continue
                seen.add(S2); nxt.add(S2)
                if r not in best: best[r]=g
    frontier=nxt
    print(n,"gates",g,"states",len(nxt),"funcs",len(best),round(time.time()-t,1),flush=True)
    if len(best)==1<<N: break
dep=lambda f:[i for i in range(n) if any(((f>>a)&1)!=((f>>(a^(1<<i)))&1) for a in range(N))]
hist={}
for f,s in best.items():
    d=len(dep(f)); hist.setdefault((d,s),0); hist[(d,s)]+=1
print(sorted(hist.items()))
json.dump({"n":n,"hist":{f"{d},{s}":c for (d,s),c in hist.items()}},open(f"minsize_n{n}.json","w"))
