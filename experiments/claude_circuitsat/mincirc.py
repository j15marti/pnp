import itertools,json,sys
def run(n,maxg):
    N=1<<n; M=(1<<N)-1
    ins=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
    best={0:0,M:0}
    for f in ins: best[f]=0; best[M^f]=0   # free negation at inputs/outputs only for reporting: count "monotone-free" B2 gates
    # B2 basis: all 16 binary functions
    def gates(a,b):
        for t in range(16):
            r=0
            for (x,ai,bi) in ((0,a,b),):
                pass
            res=0
            for k,(u,v) in enumerate(((0,0),(0,1),(1,0),(1,1))):
                if (t>>k)&1:
                    res|=((a if u else M^a)&(b if v else M^b))
            yield res
    best={}
    for f in [0,M]+ins: best[f]=0
    def dfs(sigs,g,limit):
        for i in range(len(sigs)):
            for j in range(i+1,len(sigs)):
                for r in set(gates(sigs[i],sigs[j])):
                    if r in sigs: continue
                    if r not in best or best[r]>g+1: best[r]=g+1
                    if g+1<limit: dfs(sigs+[r],g+1,limit)
    dfs(ins[:],0,maxg)
    return best,M
for n,mg in ((2,3),(3,4)):
    b,M=run(n,mg)
    # best may be truncated at mg; report distribution
    from collections import Counter
    c=Counter(b.get(f,'>%d'%mg) for f in range(M+1))
    print(n,sorted(c.items(),key=str),len(b))
