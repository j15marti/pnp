# Exact min #gates (fan-in 2, all 16 binary gates, free negation) for all n-input functions, n<=3.
# Method: iterative deepening over circuits (sequence of gates, each reading two earlier nodes). Runs in seconds.
import sys, itertools, json
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
inputs=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
ops=[(lambda a,b,t=t:sum(((t>>(2*((a>>x)&1)+((b>>x)&1)))&1)<<x for x in range(N))) for t in range(16)]
best={}  # f -> (gates, wires used)
def target(f): return min(f, f^M)
def dfs(nodes,k,limit):
    if len(nodes)-n==k:
        return
    pass
found={}
def rec(nodes,depth,maxd):
    for i in range(len(nodes)):
        for j in range(i+1,len(nodes)):
            for t in range(1,15):
                if t in (0,15,3,5,10,12): continue  # skip constants/projections
                g=ops[t](nodes[i],nodes[j])
                key=target(g)
                if key not in found or found[key]>depth+1: found[key]=depth+1
                if depth+1<maxd: rec(nodes+[g],depth+1,maxd)
for d in range(1,int(sys.argv[2])+1):
    rec(list(inputs),0,d)
funcs=set(target(f) for f in range(1<<N))
dist={}
for f in funcs:
    c=0 if f in map(target,inputs) or f==0 else found.get(f)
    dist[c]=dist.get(c,0)+1
print(n,sorted(dist.items(),key=lambda x:(x[0] is None,x[0])))
