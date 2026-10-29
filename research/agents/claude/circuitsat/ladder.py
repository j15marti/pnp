"""Exact min-gate (B2, fan-in 2, free negation) ladder for tiny functions.
Usage: python ladder.py N [MAXG]   (runs < 30 s for N<=3)"""
import sys, json, itertools
N=int(sys.argv[1]); MAXG=int(sys.argv[2]) if len(sys.argv)>2 else 6
M=1<<N; FULL=(1<<M)-1
inp=[sum(1<<a for a in range(M) if (a>>i)&1) for i in range(N)]
# 10 nondegenerate binary gates as 4-bit tables; closure under negation covers all via free NOT
gates=[t for t in range(16) if t not in (0,15,3,12,5,10)]
def ap(t,x,y):
    r=0
    for b in range(4):
        if (t>>b)&1:
            m=(x if b&1 else ~x)&(y if b&2 else ~y)
            r|=m
    return r&FULL
best={}   # function -> min gates
seen=set()
def dfs(nodes,g):
    key=frozenset(nodes)
    if (key,g) in seen: return
    seen.add((key,g))
    for f in nodes[N:]+inp+[0,FULL]:
        pass
    last=nodes[-1]
    for f in nodes:
        for h in (f,~f&FULL):
            if best.get(h,99)>g: best[h]=g
    if g==MAXG: return
    L=len(nodes)
    for i in range(L):
        for j in range(i+1,L):
            for t in gates:
                v=ap(t,nodes[i],nodes[j])
                if v in nodes or (~v&FULL) in nodes: continue
                dfs(nodes+[v],g+1)
best[0]=0;best[FULL]=0
dfs(list(inp),0)
hist={}
for f in range(1<<M):
    g=best.get(f); hist[g]=hist.get(g,0)+1
needles=[f for f in range(1<<M) if bin(f).count('1')==1]
nd=sorted({best[f] for f in needles if f in best})
print(json.dumps({"n":N,"maxg":MAXG,"hist_mingates":{str(k):v for k,v in sorted(hist.items(),key=lambda kv:(kv[0] is None,kv[0]))},"needle_mingates":nd}))
