import sys, itertools, json, time
def run(n, K, targets=None):
    N=1<<n; M=(1<<N)-1
    xs=[]
    for i in range(n):
        t=0
        for a in range(N):
            if (a>>i)&1: t|=1<<a
        xs.append(t)
    ops=[lambda a,b:a&b, lambda a,b:a&~b&M, lambda a,b:~a&b&M, lambda a,b:a|b, lambda a,b:a^b]
    best={}  # table(normal)->min gates
    for x in xs: best[x]=0
    seen={}
    def dfs(nodes,k,limit):
        key=frozenset(nodes)
        if seen.get(key,-1)>=limit-k and False: return
        for t in nodes[n:]:
            pass
        m=len(nodes)
        if k==limit: return
        for i in range(m):
            for j in range(i+1,m):
                for op in ops:
                    t=op(nodes[i],nodes[j])
                    if t in nodes: continue
                    if t not in best or best[t]>k+1: best[t]=k+1
                    nodes.append(t)
                    dfs(nodes,k+1,limit)
                    nodes.pop()
    dfs(list(xs),0,K)
    return best
if __name__=="__main__":
    n=int(sys.argv[1]);K=int(sys.argv[2]);t=time.time()
    b=run(n,K)
    from collections import Counter
    print(n,K,len(b),Counter(b.values()),time.time()-t)
