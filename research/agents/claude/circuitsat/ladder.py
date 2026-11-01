# Exact minimum fan-in-2 circuit size (basis B2: all 16 binary ops) for all functions on n<=3 inputs.
# BFS over states = frozenset of computed truth tables. Runs < 30 s.
import itertools, json, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    ins=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
    ops=range(16)
    def ap(op,x,y):
        r=0
        for b in range(4):
            if (op>>b)&1:
                xs = x if (b&1) else (~x&M)
                ys = y if (b&2) else (~y&M)
                r|= xs&ys
        return r
    best={0:0,M:0}
    for t in ins: best[t]=0; best[~t&M]=0
    start=frozenset(ins); layer={start}; seen={start}; g=0
    while len(best)<(1<<N) and g<8:
        g+=1; nxt=set()
        for S in layer:
            L=sorted(S)
            for x,y in itertools.combinations(L,2):
                for op in ops:
                    z=ap(op,x,y)
                    if z in S: continue
                    T=S|{z}
                    if T in seen: continue
                    seen.add(T); nxt.add(T)
                    for f in (z,~z&M):
                        if f not in best: best[f]=g
        layer=nxt
        print(n,g,len(layer),len(best),file=sys.stderr)
    return best
out={}
for n in (1,2,3):
    b=run(n)
    N=1<<n
    prof={}
    for f,g in b.items():
        k=bin(f).count('1')   # number of satisfying assignments
        prof.setdefault(k,[]).append(g)
    out[n]={"max_gates":max(b.values()),"hist":{g:list(b.values()).count(g) for g in sorted(set(b.values()))},
            "by_sat_count":{k:[min(v),max(v)] for k,v in sorted(prof.items())}}
    print(n,out[n])
json.dump(out,open("ladder_results.json","w"),indent=1)
