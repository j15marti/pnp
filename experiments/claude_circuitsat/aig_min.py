"""Exact minimum AIG size (AND gates, free negation) per truth table, n<=3 full, n=4 up to size cap.
Wires = 2*gates (each AND gate has two input wires). Iterative-deepening DFS over DAGs,
with gates required to be introduced in strictly increasing (tt) order to kill permutation symmetry
(valid: any DAG can be topologically sorted; ties broken by tt; we only require nondecreasing
topological compatibility via 'new gate must use the last gate or tt larger' pruning is NOT done -- we
use plain DFS with dedup of equal tts)."""
import sys, json, itertools
def run(n, cap):
    N=1<<n; M=(1<<N)-1
    base=[]
    for i in range(n):
        t=0
        for a in range(N):
            if (a>>i)&1: t|=1<<a
        base.append(t)
    best={0:0,M:0}  # constants free
    def rec(sigs, g, limit):
        for t in sigs:
            for u in (t,t^M):
                if u not in best or best[u]>g: best[u]=g
        if g==limit: return
        L=len(sigs); seen=set(sigs)|{s^M for s in sigs}
        for i in range(L):
            for j in range(i+1,L):
                for a in (sigs[i],sigs[i]^M):
                    for b in (sigs[j],sigs[j]^M):
                        c=a&b
                        if c in seen: continue
                        rec(sigs+[c],g+1,limit)
    for lim in range(0,cap+1):
        rec(base,0,lim)
    return best
if __name__=="__main__":
    n=int(sys.argv[1]); cap=int(sys.argv[2])
    best=run(n,cap); N=1<<n
    # constants cost 0
    out={}
    for t,g in best.items():
        s=bin(t).count("1")
        out.setdefault(s,[]).append(g)
    tab={s:{"min_gates":min(v),"count_functions_found":len(v)} for s,v in sorted(out.items())}
    print(json.dumps({"n":n,"cap":cap,"functions_found":len(best),"of":1<<N,"by_sat_count":tab}))
