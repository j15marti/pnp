"""Exact minimum circuit gates (fan-in-2, full basis B2, free inputs, no negation cost beyond B2)
and minimum formula leaves for all Boolean functions on n<=3 inputs. Runtime ~ few seconds."""
import json, itertools, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    inp=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
    ops=[lambda a,b,t=t:sum((((t>>(2*((a>>x)&1)+((b>>x)&1)))&1)<<x) for x in range(N)) for t in range(16)]
    # formula leaves DP
    F={}
    for f in inp: F[f]=1
    F[0]=0;F[M]=0  # constants free (leaf cost 0) -- B2 constants arise anyway
    for L in range(2,12):
        new={}
        for a,la in list(F.items()):
            for b,lb in list(F.items()):
                if la+lb!=L: continue
                for op in ops:
                    c=op(a,b)
                    if c not in F and c not in new: new[c]=L
        F.update(new)
        if len(F)==1<<N: break
    # gate-count BFS over circuits: states = frozenset of available functions (inputs + gates)
    start=frozenset(inp)
    best={}
    for f in list(inp)+[0,M]: best[f]=0
    frontier={start}; g=0; seen={start}
    while len(best)<(1<<N) and g<8:
        g+=1; nxt=set()
        for S in frontier:
            Sl=list(S)
            for i in range(len(Sl)):
                for j in range(i,len(Sl)):
                    for op in ops:
                        c=op(Sl[i],Sl[j])
                        if c in S: continue
                        T=S|{c}
                        if T in seen: continue
                        seen.add(T); nxt.add(T)
                        if c not in best: best[c]=g
        frontier=nxt
        if g>=int(sys.argv[2]) if len(sys.argv)>2 else False: break
    return best,F
if __name__=="__main__":
    n=int(sys.argv[1]); best,F=run(n)
    from collections import Counter
    out={"n":n,"gates_hist":dict(Counter(best.values())),"formula_leaf_hist":dict(Counter(F.values())),
         "max_gap_gates_vs_leaves":max(F[f]-best[f] for f in best if f in F)}
    # unique-SAT point functions (|f^-1(1)|=1)
    N=1<<n
    pts=[f for f in best if bin(f).count("1")==1]
    out["unique_sat_gates"]=sorted(set(best[f] for f in pts)); out["unique_sat_leaves"]=sorted(set(F[f] for f in pts))
    print(json.dumps(out))
