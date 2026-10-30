"""Exact min #gates (all 16 binary gates, fan-in 2, unbounded fan-out) per n-var function, n<=3.
Iterative deepening over gate sequences. Wires = 2*gates. Runtime: a few seconds."""
import itertools, json, sys
def run(n):
    N=1<<n; full=(1<<N)-1
    inputs=[sum(((m>>i)&1)<<m for m in range(N)) for i in range(n)]
    best={}  # function -> min gates
    best.update({f:0 for f in inputs}); best[0]=0; best[full]=0
    inputs_=inputs
    def gate(g,a,b):
        r=0
        for k in range(4):
            if (g>>k)&1:
                x,y=k&1,k>>1
                r|=((a if x else ~a)&(b if y else ~b))
        return r&full
    seen={}
    def dfs(nodes,depth,limit):
        for f in nodes[n:]:
            if best.get(f,99)>depth: best[f]=depth
        if depth==limit: return
        key=(frozenset(nodes),)
        if seen.get(key,99)<=depth: return
        seen[key]=depth
        L=len(nodes)
        for i in range(L):
            for j in range(i+1,L):
                for g in range(16):
                    f=gate(g,nodes[i],nodes[j])
                    if f in nodes: continue
                    dfs(nodes+[f],depth+1,limit)
    for lim in range(0,{1:0,2:1,3:4}[n]+1):
        seen.clear(); dfs(list(inputs),0,lim)
    return best
out={}
for n in (1,2,3):
    b=run(n); N=1<<n
    allf=range(1<<N)
    # essential vars
    def ess(f):
        c=0
        for i in range(n):
            if any(((f>>m)&1)!=((f>>(m^(1<<i)))&1) for m in range(N)): c+=1
        return c
    tab={}
    for f in allf:
        if f in b or ess(f)==0 or True:
            gates=b.get(f)
            tab.setdefault(ess(f),[]).append(gates)
    out[n]={k:{"count":len(v),"min":min(x for x in v if x is not None),"max":max(x for x in v if x is not None),"unreached":sum(x is None for x in v)} for k,v in tab.items()}
print(json.dumps(out,indent=1)); json.dump(out,open(sys.argv[1],"w"),indent=1)
