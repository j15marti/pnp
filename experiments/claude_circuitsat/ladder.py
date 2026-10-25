"""Claude CircuitSAT ladder: exact minimum gates/wires (fan-in-2 AND with free negation, i.e. De Morgan basis)
for every Boolean function on n=1,2,3 inputs, via breadth-first search over sets of computed functions.
Each gate = 2 wires. Reproducible, stdlib only, chunked by n and depth cap."""
import json, sys, time, itertools
def run(n, cap=7, tlimit=25):
    N=1<<n; M=(1<<N)-1
    def canon(f): return min(f, M^f)
    ins=[]
    for i in range(n):
        t=0
        for a in range(N):
            if (a>>i)&1: t|=1<<a
        ins.append(canon(t))
    best={}                      # canonical function -> min gates
    for f in ins: best[f]=0
    best[canon(0)]=0
    start=frozenset(ins+[canon(0)])
    level={start}; seen={start}
    t0=time.time(); done_depth=0
    for d in range(1,cap+1):
        nxt=set()
        for S in level:
            L=list(S)
            for a,b in itertools.combinations_with_replacement(L,2):
                for fa in (a,M^a):
                    for fb in (b,M^b):
                        g=canon(fa&fb)
                        if g in S: continue
                        T=S|{g}
                        if T in seen: continue
                        seen.add(T); nxt.add(T)
                        if g not in best: best[g]=d
            if time.time()-t0>tlimit: return best,done_depth,False,len(best)
        level=nxt; done_depth=d
        if len(best)==(1<<(N-1)) : break   # all canonical functions found
    return best,done_depth,len(best)==(1<<(N-1)),len(best)
out={}
for n in (1,2,3):
    best,dd,complete,cnt=run(n)
    hist={}
    for f,g in best.items(): hist[g]=hist.get(g,0)+1
    out[n]={"canonical_functions":1<<((1<<n)-1),"found":cnt,"complete":complete,"depth_searched":dd,
            "gate_histogram":{str(k):v for k,v in sorted(hist.items())},
            "max_gates":max(best.values()),"max_wires":2*max(best.values())}
print(json.dumps(out,indent=1))
json.dump(out,open(sys.argv[1],"w"),indent=1)
