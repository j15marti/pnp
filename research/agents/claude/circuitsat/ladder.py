"""Exact minimum B2 (fan-in 2, all 16 gates) circuit size for all Boolean functions
on n<=3 inputs, by BFS over sets of computed truth tables. Also minimum #wires
(= 2*gates, fan-in 2, fanout free to count) and a fanout-1 formula-size check is omitted.
Runs well under 30s."""
import json, itertools, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    inputs=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
    consts=[0,M]
    ops=range(16)
    def g(op,x,y):
        r=0
        for b in range(4):
            if (op>>b)&1:
                xb,yb=b&1,b>>1
                r|=(x if xb else M^x)&(y if yb else M^y)
        return r
    best={f:None for f in range(M+1)}
    for f in consts+inputs: best[f]=0
    start=frozenset(inputs)
    layer={start}; seen={start}; size=0
    while layer and any(v is None for v in best.values()):
        size+=1; nxt=set()
        for S in layer:
            L=list(S)+consts
            for x,y in itertools.combinations(L,2):
                for op in ops:
                    z=g(op,x,y)
                    if z in S or z in consts: continue
                    T=S|{z}
                    if T in seen: continue
                    seen.add(T); nxt.add(T)
                    if best[z] is None: best[z]=size
        layer=nxt
    return best
out={}
for n in (1,2,3):
    b=run(n)
    hist={}
    for v in b.values(): hist[v]=hist.get(v,0)+1
    out[n]={"max_gates":max(b.values()),"histogram":hist,
            "AND_n":b[(1<<(1<<n))-1 and sum(1<<a for a in range(1<<n) if a==(1<<n)-1)],
            "XOR_n":b[sum(1<<a for a in range(1<<n) if bin(a).count('1')%2)],
            "MAJ_or_thr":None}
print(json.dumps(out,indent=1))
json.dump(out,open("ladder_results.json","w"),indent=1)
