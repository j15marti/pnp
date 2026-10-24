"""Exact B2 circuit size for all Boolean functions on n<=3 inputs (BFS over sets of computed functions).
Chunk: n given as argv; each run < 30s. Output JSON histogram + SAT-relevant profile."""
import sys, json, itertools
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
ins=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
ops=[lambda a,b,s=s:(((a if s&1 else ~a)&M)&((b if s&2 else ~b)&M))^(M if s&4 else 0) for s in range(8)]+[lambda a,b:a^b]
best={}  # f -> min gates
for f in [0,M]+ins+[~i&M for i in ins]: best[f]=0
start=frozenset(ins)
level={start}; seen={start}; k=0
while level and len(best)<(1<<N):
    k+=1; nxt=set()
    for S in level:
        L=sorted(S)
        for a,b in itertools.combinations(L,2):
            for op in ops:
                g=op(a,b)
                for h in (g,~g&M):
                    if h in S: continue
                    if h not in best: best[h]=k
                    T=S|{h}
                    # prune: at most 5 gates needed for n=3
                    if T not in seen: seen.add(T); nxt.add(T)
    level=nxt
    print("level",k,"states",len(level),"covered",len(best),file=sys.stderr)
hist={}
for f,c in best.items(): hist[c]=hist.get(c,0)+1
# unique-SAT point functions
pts={}
for a in range(N): pts[a]=best[1<<a]
# SAT-hardest: max over functions; also 'all-variable' functions
print(json.dumps({"n":n,"hist":hist,"max":max(best.values()),"point_fn_sizes":sorted(set(pts.values()))}))
