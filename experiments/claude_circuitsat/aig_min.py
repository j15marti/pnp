"""Exact minimum AND-gate count (free negation, fan-in 2, so wires=2*gates) for all
n-input Boolean functions, n=1..3, by level-wise BFS over sets of computed function classes.
Classes are functions modulo complement. Runtime ~ seconds for n<=3."""
import itertools, json, sys, time
def run(n):
    N=1<<n; full=(1<<N)-1
    def cls(f): return min(f, full^f)
    ins=[]
    for i in range(n):
        f=0
        for x in range(N):
            if (x>>i)&1: f|=1<<x
        ins.append(cls(f))
    start=frozenset(ins+[cls(0)])  # constant free
    best={}  # class -> min gates
    for f in start: best[f]=0
    level={start}; seen={start}; g=0
    total=1<<(N-1)
    while level and len(best)<total:
        g+=1; nxt=set()
        for S in level:
            L=list(S)
            for a,b in itertools.combinations_with_replacement(L,2):
                for pa in (a,full^a):
                    for pb in (b,full^b):
                        c=cls(pa&pb)
                        if c in S: continue
                        T=S|{c}
                        if T not in seen: seen.add(T); nxt.add(T)
                        if c not in best: best[c]=g
        level=nxt
        print(n,g,len(level),len(best),file=sys.stderr)
    hist={}
    for v in best.values(): hist[v]=hist.get(v,0)+1
    return {"n":n,"max_gates":max(best.values()),"hist":dict(sorted(hist.items())),"classes":len(best)}
if __name__=="__main__":
    t=time.time(); out=[run(n) for n in (1,2,3)]
    print(json.dumps(out)); print("secs",time.time()-t,file=sys.stderr)
