"""Exact B2 circuit size (gates; wires=2*gates, fan-in 2) of all n-variable Boolean
functions, n=1..3, by BFS over normalized sets of computed functions.
Negation is free (B2): functions are normalized so truth-table bit 0 = 0.
Runtime well under 30 s for n<=3."""
import json, itertools, sys
def run(n):
    N=1<<n; full=(1<<N)-1
    norm=lambda t: t^full if t&1 else t
    xs=[]
    for i in range(n):
        t=0
        for a in range(N):
            if (a>>i)&1: t|=1<<a
        xs.append(norm(t))
    # 16 binary ops on (x,y) with free negation of inputs/outputs: AND-type and XOR-type suffice
    def combos(a,b):
        na,nb=a^full,b^full
        out=set()
        for x in (a,na):
            for y in (b,nb):
                out.add(norm(x&y))
        out.add(norm(a^b))
        return out
    size={0:None}
    best={}
    for x in xs: best[x]=0
    best[0]=0
    level={frozenset(xs)}
    seen={frozenset(xs)}
    k=0
    while len(best)<(1<<(N-1)):
        k+=1; nxt=set()
        for st in level:
            L=sorted(st)
            for a,b in itertools.combinations(L,2):
                for g in combos(a,b):
                    if g in st: continue
                    ns=st|{g}
                    if ns in seen: continue
                    seen.add(ns); nxt.add(ns)
                    if g not in best: best[g]=k
        level=nxt
        print(n,"gates",k,"states",len(level),"functions found",len(best),file=sys.stderr)
    return best,N
res={}
for n in (1,2,3):
    best,N=run(n)
    full=(1<<N)-1
    # expand to all 2^N functions (f and ~f same size)
    tab={}
    for t,s in best.items():
        tab[t]=s; tab[t^full]=s
    bysat={}
    for t,s in tab.items():
        w=bin(t).count("1")
        bysat.setdefault(w,[]).append(s)
    summ={w:{"min":min(v),"max":max(v),"count":len(v)} for w,v in sorted(bysat.items())}
    res[n]={"max_size":max(tab.values()),"size_hist":{s:sum(1 for v in tab.values() if v==s) for s in sorted(set(tab.values()))},"by_satcount":summ}
    print(n,res[n])
json.dump(res,open("exact_size_results.json","w"),indent=1)
