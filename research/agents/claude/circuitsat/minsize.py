# Exact minimum B2 (all 2-input gates) circuit size for all functions on n<=3 inputs.
# Iterative deepening DFS over circuits; each gate = 2 wires, so min wires = 2*size.
import json, itertools, sys
def run(n, maxs):
    N=1<<n; full=(1<<N)-1
    ins=[sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)]
    ops=[lambda a,b,t=t:sum(1<<k for k in range(4) if (t>>k)&1 and False) for t in ()]
    def gate(t,a,b,full=full):
        # t: 4-bit truth table over (a,b): bit (2a+b)
        r=0
        if t&1: r|=~a&~b
        if t&2: r|=~a&b
        if t&4: r|=a&~b
        if t&8: r|=a&b
        return r&full
    types=[t for t in range(16) if t not in (0,3,5,10,12,15)]  # drop constants/projections/negations of one input
    best={}
    seen=set()
    def dfs(nodes,k):
        f=nodes[-1]
        for g in nodes[n:] if False else nodes: 
            pass
    # BFS on sets of reachable node-lists is large; use depth-limited DFS recording every node function.
    def rec(nodes,k):
        for f in nodes:
            for v in (f, f^full):
                if v not in best or best[v]>k: best[v]=k
        if k==maxs: return
        L=len(nodes)
        for i in range(L):
            for j in range(i+1,L):
                for t in types:
                    v=gate(t,nodes[i],nodes[j])
                    if v in nodes: continue
                    rec(nodes+[v],k+1)
    rec(ins,0)
    best[0]=0;best[full]=0
    return best
res={}
for n in (1,2,3):
    b=run(n,4 if n==3 else 2)
    hist={}
    for v,k in b.items(): hist[k]=hist.get(k,0)+1
    res[n]=dict(sorted(hist.items()),total=len(b),expected=1<<(1<<n))
print(json.dumps(res))
json.dump(res,open('minsize_results.json','w'))
