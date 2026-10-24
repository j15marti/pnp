"""Exact min #gates (B2 basis: all 16 binary gates) to compute each n-var function.
Method: BFS over sets of computed truth tables (inputs + gates), canonical frozenset.
Records, per function, min gates g and the wire count 2g of an optimal circuit.
n=2,3 exact. Runtime <30s each. Usage: python min_circuit_size.py N"""
import sys, itertools, json, time
n=int(sys.argv[1]); M=1<<n; FULL=(1<<M)-1
ins=[sum(((x>>i)&1)<<x for x in range(M)) for i in range(n)]
def gates(a,b):
    na,nb=FULL^a,FULL^b
    out=set()
    for A in (a,na):
        for B in (b,nb):
            out.add(A&B); out.add(A|B); out.add(A^B)   # covers all 16 with complements
    out|={FULL^o for o in out}
    return out
t0=time.time()
start=frozenset(ins)|{0,FULL}  # constants free
best={f:0 for f in start}
frontier={start}; seen={start}; g=0
while frontier and time.time()-t0<25:
    g+=1; nxt=set()
    for S in frontier:
        L=sorted(S)
        for a,b in itertools.combinations(L,2):
            for o in gates(a,b):
                if o in S: continue
                T=S|{o}
                if T in seen: continue
                seen.add(T); nxt.add(T)
                if o not in best: best[o]=g
    frontier=nxt
    print("g",g,"states",len(frontier),"covered",len(best),"/",1<<M,flush=True)
    if len(best)==1<<M: break
from collections import Counter
c=Counter(best.values())
print(sorted(c.items()), "complete" if len(best)==1<<M else "PARTIAL")
# restricted: functions with exactly one satisfying assignment (unique-SAT)
uni={f:v for f,v in best.items() if bin(f).count("1")==1}
print("unique-SAT min gates:",Counter(uni.values()))
json.dump({"n":n,"hist":sorted(c.items()),"complete":len(best)==1<<M,"uniqueSAT":sorted(Counter(uni.values()).items())},open(f"experiments/circuitsat/result_n{n}.json","w"))
