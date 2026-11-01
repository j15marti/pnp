# Exact minimum #gates (hence wires = 2*gates, fan-in 2, free negation on wires) for all
# Boolean functions on n<=3 inputs, basis {AND} with negations on wires (== AND/OR/NOT De Morgan).
# BFS over sets of available functions (negation-closed). Chunk: n given on argv; <30s.
import sys, itertools, time
n=int(sys.argv[1]); maxg=int(sys.argv[2]); N=1<<n; FULL=(1<<N)-1
xs=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
def close(fs): return frozenset(fs)
start=frozenset(xs)
best={}  # function -> min gates
for f in list(xs)+[FULL^x for x in xs]+[0,FULL]: best[f]=0
frontier={start}; seen={start}
for g in range(1,maxg+1):
    new=set()
    for S in frontier:
        L=list(S)+[FULL^x for x in S]
        for a,b in itertools.combinations(L,2):
            h=a&b
            if h in (0,FULL) or h in S or (FULL^h) in S: continue
            for f in (h,FULL^h):
                if f not in best: best[f]=g
            T=S|{h}
            if T not in seen: seen.add(T); new.add(T)
    frontier=new
    print("gates",g,"states",len(new),"functions solved",len(best),"of",1<<N,flush=True)
from collections import Counter
print(sorted(Counter(best.values()).items()))
# minterm (unique satisfying point) cost
mt=[f for f in best if bin(f).count('1')==1]
print("single-minterm fns:",len(mt),"gates:",set(best[f] for f in mt))
