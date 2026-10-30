"""Exact minimum circuit size (fan-in-2 gates, all 2-input gates, free negation)
for every n-input Boolean function, n<=3, by BFS over sets of computed wires.
Tables are stored modulo complement (negation free). Runs well under 30 s."""
import sys, itertools, json
n=int(sys.argv[1]); N=1<<(1<<n); full=N-1
def canon(t): return min(t, full^t)
ins=[]
for i in range(n):
    t=0
    for x in range(1<<n):
        if (x>>i)&1: t|=1<<x
    ins.append(canon(t))
def ops(a,b):
    out=set()
    for na in (0,1):
        for nb in (0,1):
            A=a^full if na else a; B=b^full if nb else b
            out.add(canon(A&B))
    out.add(canon(a^b))
    return out
start=frozenset(ins)
best={canon(0):0}
for t in ins: best[t]=0
frontier={start}; seen={start}; k=0
while len(best)<(N//2) and k<8:
    k+=1; nxt=set()
    for S in frontier:
        L=list(S)
        for a,b in itertools.combinations(L,2):
            for t in ops(a,b):
                if t in S: continue
                S2=S|{t}
                if S2 in seen: continue
                seen.add(S2); nxt.add(S2)
                if t not in best: best[t]=k
    frontier=nxt
    print("gates",k,"states",len(frontier),"classes known",len(best),"/",N//2,file=sys.stderr)
from collections import Counter
c=Counter(best.values())
print(json.dumps({"n":n,"classes_mod_complement":N//2,"count_by_min_gates":dict(sorted(c.items())),"max":max(best.values()) if len(best)==N//2 else None}))
