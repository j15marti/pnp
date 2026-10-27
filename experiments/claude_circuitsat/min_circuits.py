"""Exact minimum B2 circuit sizes (fan-in-2, all 16 binary gates, wires=2*gates) for n<=3 inputs,
by closure over sets of truth tables (DP over subsets of computed functions is too big; use
BFS on 'circuit states' = frozenset of available functions, depth-limited). Runtime <30s."""
import itertools, json, sys
def run(n, maxg):
    N=1<<n; mask=(1<<N)-1
    ins=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
    gates=range(16)
    def ap(g,x,y):
        r=0
        for b in range(N):
            if (g>>(2*((x>>b)&1)+((y>>b)&1)))&1: r|=1<<b
        return r
    best={f:None for f in range(mask+1)}
    # f computable with s gates: iterative deepening search over circuits (canonical: gates ordered)
    best[0]=best[mask]=0
    for v in ins: best[v]=0; best[mask^v]=0  # negation free? no: count NOT as free via B2 gate absorbing
    seen=set()
    def dfs(avail,s):
        key=(frozenset(avail),s)
        if key in seen: return
        seen.add(key)
        for f in avail:
            if best[f] is None or best[f]>s-0: pass
        if s==maxg: return
        L=list(avail)
        for i in range(len(L)):
            for j in range(i+1,len(L)):
                for g in range(16):
                    h=ap(g,L[i],L[j])
                    if h in avail: continue
                    if best[h] is None or best[h]>s+1: best[h]=s+1
                    dfs(avail|{h},s+1)
    # complement-closed to cut search: treat f and ~f equivalent
    dfs(frozenset(ins+[mask^v for v in ins]),0)
    return best
if __name__=="__main__":
    n=int(sys.argv[1]); mg=int(sys.argv[2])
    b=run(n,mg)
    from collections import Counter
    c=Counter(v for v in b.values())
    print(n,mg,sorted(c.items(),key=lambda x:(x[0] is None,x[0])))
    json.dump({"n":n,"maxg":mg,"hist":{str(k):v for k,v in c.items()}},open(f"/home/user/pnp/results/raw/claude_circuitsat_n{n}.json","w"))
