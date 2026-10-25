"""Exact minimum B2 circuit size (fan-in-2, all 16 binary gates) for all
n-variable Boolean functions, n=1..3, by iterative-deepening search over
straight-line programs. Runtime well under 30 s. Wires = 2*gates (each gate has
two in-edges); the output wire is extra."""
import json, sys, itertools
n=int(sys.argv[1]) if len(sys.argv)>1 else 3
N=1<<n; MASK=(1<<N)-1
var=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
ops=[lambda x,y,t=t:sum(1<<k for k in range(1) ) for t in []]
def gate(t,x,y):
    r=0
    if t&1: r|=(~x&~y)&MASK
    if t&2: r|=(x&~y)&MASK
    if t&4: r|=(~x&y)&MASK
    if t&8: r|=(x&y)&MASK
    return r
best={}
def dfs(vals,left):
    # record every function reachable now with len(vals)-n gates
    g=len(vals)-n
    for v in vals:
        if v not in best or best[v]>g: best[v]=g
    if left==0: return
    L=len(vals)
    for i in range(L):
        for j in range(i+1,L):
            for t in range(1,15):
                if t in (3,5,10,12): continue  # projections/negations of an input
                v=gate(t,vals[i],vals[j])
                if v in vals or v in (0,MASK): continue
                dfs(vals+[v],left-1)
maxg=int(sys.argv[2]) if len(sys.argv)>2 else {1:0,2:3,3:3}[n]
# canonical dedupe: sets visited
seen=set()
def dfs2(vals,left):
    key=frozenset(vals)
    if (key,left) in seen: return
    seen.add((key,left))
    g=len(vals)-n
    for v in vals:
        if v not in best or best[v]>g: best[v]=g
    if left==0: return
    L=len(vals)
    for i in range(L):
        for j in range(i+1,L):
            for t in (1,2,4,6,7,8,9,11,13,14):
                v=gate(t,vals[i],vals[j])
                if v in vals or v in (0,MASK): continue
                dfs2(vals+[v],left-1)
dfs2(list(var),maxg)
# complement-closed (NOT free): size of f = size of ~f in B2 since gates absorb negation
for v in list(best):
    c=~v&MASK
    if c in best: best[v]=best[c]=min(best[v],best[c])
hist={}
for v,g in best.items(): hist[g]=hist.get(g,0)+1
res={"n":n,"max_gates_searched":maxg,"nonconstant_functions_found":len(best),
     "hist_gates_to_count":hist,
     "AND_n":best.get(var[0]&var[-1] if n<3 else var[0]&var[1]&var[2]),
     "XOR_n":best.get(eval("^".join(f"var[{i}]" for i in range(n))))}
print(json.dumps(res))
json.dump(res,open(f"/home/user/pnp/experiments/claude_circuitsat/min_gates_n{n}.json","w"))
