"""Exact minimum AND-gate count (free complemented edges) of every n-variable
Boolean function, n=1..3, by iterative-deepening search over gate sequences.
Wires of a size-g circuit: 2g gate-input wires (+1 output wire)."""
import json, sys, itertools, time
def run(n):
    N=1<<n; M=(1<<N)-1
    xs=[]
    for i in range(n):
        v=0
        for a in range(N):
            if (a>>i)&1: v|=1<<a
        xs.append(v)
    best={0:0,M:0}
    for v in xs: best[v]=0; best[M^v]=0
    def dfs(avail,g,limit):
        # avail: tuple of base functions (uncomplemented) ; record min size
        lits=[]
        for f in avail: lits.append(f); lits.append(M^f)
        seen=set()
        for i in range(len(lits)):
            for j in range(i+1,len(lits)):
                h=lits[i]&lits[j]
                if h in seen or h in avail: continue
                seen.add(h)
                for t in (h,M^h):
                    if best.get(t,99)>g+1: best[t]=g+1
                if g+1<limit: dfs(avail+(h,),g+1,limit)
    lim=1
    while True:
        dfs(tuple(xs),0,lim)
        if len(best)==1<<N or lim>=7: break
        lim+=1
    return best
out={}
for n in (1,2,3):
    t=time.time(); b=run(n); N=1<<n
    hist={}
    for f,g in b.items(): hist[g]=hist.get(g,0)+1
    needle=[b[1<<a] for a in range(N)]
    out[n]={"functions_found":len(b),"of":1<<N,"hist_by_gates":dict(sorted(hist.items())),
            "max_gates":max(b.values()),"needle_gates":sorted(set(needle)),"secs":round(time.time()-t,2)}
    print(n,out[n],flush=True)
json.dump(out,open(sys.argv[1],"w"),indent=1)
