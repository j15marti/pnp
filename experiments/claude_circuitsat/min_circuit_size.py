"""Exact minimum fan-in-2 circuit size (basis B2 = all 16 binary gates, free negation
folded into gates) for every n-input Boolean function, n<=3, by BFS over sets of
available functions (inputs + computed gates). Runs in a few seconds."""
import itertools, json, sys
def run(n):
    N=1<<n; full=(1<<N)-1
    ins=[]
    for i in range(n):
        v=0
        for x in range(N):
            if (x>>i)&1: v|=1<<x
        ins.append(v)
    ops=[lambda a,b,t=t:((a&b if t&1 else 0)|(a&~b&full if t&2 else 0)|(~a&full&b if t&4 else 0)|(~a&~b&full if t&8 else 0)) for t in range(16)]
    best={0:0,full:0}
    for v in ins: best[v]=0; best[full^v]=0
    frontier={frozenset(ins)}; size=0
    seen={frozenset(ins)}
    while frontier and size<8:
        size+=1; nxt=set()
        for S in frontier:
            L=sorted(S)
            for a,b in itertools.combinations(L,2):
                for o in ops:
                    r=o(a,b)
                    if r in S: continue
                    if r not in best: best[r]=size
                    T=frozenset(S|{r})
                    if T not in seen: seen.add(T); nxt.add(T)
        frontier=nxt
        if len(best)==1<<N: break
    return best
out={}
for n in (1,2,3):
    b=run(n); hist={}
    for v in b.values(): hist[v]=hist.get(v,0)+1
    out[n]={"max_size":max(b.values()),"histogram":hist,"count":len(b)}
    print(n,out[n])
json.dump(out,open("min_circuit_size_results.json","w"),indent=1)
