import itertools,sys,time
def res(c1,c2):
    out=[]
    for l in c1:
        if -l in c2:
            r=(c1-{l})|(c2-{-l})
            if any(-x in r for x in r): continue
            out.append(frozenset(r))
    return out
def minsteps(clauses,maxk,tl=25):
    t0=time.time()
    start=frozenset(frozenset(c) for c in clauses)
    empty=frozenset()
    best=[None]
    seen={}
    def dfs(S,k):
        if time.time()-t0>tl: raise TimeoutError
        if empty in S: return True
        if k==0: return False
        key=(S,k)
        if key in seen: return False
        L=list(S)
        cands=set()
        for a,b in itertools.combinations(L,2):
            for r in res(a,b):
                if r in S: continue
                if any(c<=r for c in S): continue  # subsumed: skip
                cands.add(r)
        # prune: need at least k steps; empty clause must be reachable
        for r in sorted(cands,key=len):
            if dfs(S|{r},k-1): return True
        seen[key]=1
        return False
    for k in range(1,maxk+1):
        if dfs(start,k): return k
    return None
def php(n):  # n+1 pigeons, n holes
    v=lambda i,j:i*n+j+1
    cl=[[v(i,j) for j in range(n)] for i in range(n+1)]
    for j in range(n):
        for i1 in range(n+1):
            for i2 in range(i1+1,n+1): cl.append([-v(i1,j),-v(i2,j)])
    return cl
if __name__=="__main__":
    print("PHP_1^2 steps",minsteps(php(1),10))
    try: print("PHP_2^3 steps",minsteps(php(2),14))
    except TimeoutError: print("PHP_2^3 timeout")
    # all 8 width-3 clauses on 3 vars
    full=[[a*1,b*2,c*3] for a in(1,-1) for b in(1,-1) for c in(1,-1)]
    print("full3",minsteps(full,10))
