# Exact min B2 circuit size (fan-in 2, all 16 binary gates, free negation) for all f:{0,1}^n->{0,1}, n<=3.
# BFS over sets of computed truth tables (dedup). Runtime ~ seconds.
import itertools, json, sys
def run(n, maxs):
    N=1<<(1<<n); full=N-1
    inputs=[]
    for i in range(n):
        t=0
        for a in range(1<<n):
            if (a>>i)&1: t|=1<<a
        inputs.append(t)
    M=(1<<(1<<n))-1
    best={}  # truth table -> min size
    for t in [0,M]+inputs: best[t]=0
    for t in list(best): best[M^t]=0
    # gate ops: nondegenerate: AND-type 8 (with negations) + XOR, XNOR; closed under free negation of outputs
    def gates(a,b):
        na,nb=M^a,M^b
        out=set()
        for x in (a,na):
            for y in (b,nb):
                v=x&y; out.add(v); out.add(M^v)
        v=a^b; out.add(v); out.add(M^v)
        return out
    frontier={frozenset(inputs)}
    seen=set(frontier)
    for s in range(1,maxs+1):
        nxt=set()
        for st in frontier:
            L=list(st)
            for i in range(len(L)):
                for j in range(i+1,len(L)):
                    for g in gates(L[i],L[j]):
                        if g in st or g in (0,M): continue
                        if (M^g) in st: continue
                        ns=frozenset(st|{g})
                        if ns in seen: continue
                        seen.add(ns); nxt.add(ns)
                        for h in (g,M^g):
                            if h not in best: best[h]=s
        frontier=nxt
        print("n",n,"size",s,"states",len(frontier),"covered",len(best),"/",N,file=sys.stderr)
        if len(best)==N: break
    return best
res={}
for n,ms in [(1,1),(2,3),(3,6)]:
    b=run(n,ms)
    N=1<<(1<<n)
    from collections import Counter
    c=Counter(b.values())
    # needles: exactly one satisfying assignment
    needle=[b[t] for t in b if bin(t).count('1')==1]
    res[n]={"complete":len(b)==N,"hist":dict(c),"maxsize":max(b.values()),"needle_min":sorted(set(needle)),
            "bysat":{k:max(v for t,v in b.items() if bin(t).count('1')==k) for k in range(1,(1<<n)+1) if any(bin(t).count('1')==k for t in b)}}
print(json.dumps(res,indent=1))
json.dump(res,open("mincirc_results.json","w"),indent=1)
