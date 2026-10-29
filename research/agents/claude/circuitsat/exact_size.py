"""Exact fan-in-2 circuit size C(f) over the full binary basis B2, n<=3 exhaustive,
n=4 selected symmetric functions. Each call finishes in <30 s (see CLI arg)."""
import sys, json, itertools, time
def tt_inputs(n):
    N=1<<n; mask=(1<<N)-1; xs=[]
    for i in range(n):
        v=0
        for a in range(N):
            if (a>>i)&1: v|=1<<a
        xs.append(v)
    return xs,mask
OPS=[lambda a,b,m:a&b, lambda a,b,m:a&~b&m, lambda a,b,m:~a&b&m, lambda a,b,m:a|b,
     lambda a,b,m:a^b, lambda a,b,m:~(a&b)&m, lambda a,b,m:~(a|b)&m, lambda a,b,m:~(a^b)&m,
     lambda a,b,m:~a&~b&m*0|(~a&~b)&m, lambda a,b,m:(a|~b)&m, lambda a,b,m:(~a|b)&m]
OPS=OPS[:8]+OPS[9:]  # nonredundant gate types (AND/OR/XOR families with negations)
def cost_all(n,limit,deadline):
    xs,m=tt_inputs(n); best={0:0,m:0}
    for x in xs: best[x]=0; best[~x&m]=0
    # iterative deepening DFS: record min #gates at which each function appears as last gate
    def dfs(wires,k,K):
        for i in range(len(wires)):
            for j in range(i+1,len(wires)):
                a,b=wires[i],wires[j]
                for op in OPS:
                    f=op(a,b,m)
                    if best.get(f,99)>k+1: best[f]=k+1
                    if k+1<K and f not in wires: dfs(wires+[f],k+1,K)
        if time.time()>deadline: raise TimeoutError
    dfs(list(xs),0,limit)
    return best,m,xs
if __name__=="__main__":
    n=int(sys.argv[1]); K=int(sys.argv[2])
    t=time.time(); best,m,xs=cost_all(n,K,t+28)
    from collections import Counter
    c=Counter(best.values())
    print(n,K,"funcs found",len(best),"of",1<<(1<<n),dict(sorted(c.items())))
    json.dump({"n":n,"K":K,"hist":dict(sorted(c.items()))},open(f"exact_n{n}.json","w"))
