"""Exact minimum gate/wire counts for small n (B2 basis, fan-in 2, unbounded fan-out).
Circuit with k gates has exactly 2k wires into gates (+1 output tag). Iterative BFS over
sets of computed functions (inputs included), dedup by frozenset. Stops at a time budget."""
import sys, time, json, itertools
n=int(sys.argv[1]); budget=float(sys.argv[2]) if len(sys.argv)>2 else 20
N=1<<n; M=(1<<N)-1
inputs=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
ops=[lambda x,y,t=t:(( (M^x)&(M^y) if t&1 else 0)|((M^x)&y if t&2 else 0)|(x&(M^y) if t&4 else 0)|(x&y if t&8 else 0)) for t in range(16)]
start=frozenset(inputs); best={}
for f in inputs: best[f]=0
best[0]=best[M]=None
level={start}; seen={start}; k=0; t0=time.time(); done=True
while level and time.time()-t0<budget:
    k+=1; nxt=set()
    for S in level:
        L=sorted(S)
        for i in range(len(L)):
            for j in range(i+1,len(L)):
                for op in ops:
                    g=op(L[i],L[j])
                    if g in S: continue
                    S2=S|{g}
                    if S2 in seen: continue
                    seen.add(S2); nxt.add(S2)
                    if g not in best: best[g]=k
        if time.time()-t0>budget: done=False;break
    level=nxt
    print("k",k,"states",len(nxt),"known",len(best),file=sys.stderr)
else:
    done=not level
# constants cost: 1 gate (x AND NOT x)
cnt={}
for f,v in best.items():
    if v is not None: cnt[v]=cnt.get(v,0)+1
print(json.dumps({"n":n,"complete":done and len(best)==2**N,"funcs":2**N,"classified":len(best),"hist":cnt,"max_gates":max(v for v in best.values() if v is not None),"note":"constants cost 1 gate, excluded"}))
