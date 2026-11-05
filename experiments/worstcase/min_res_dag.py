"""Exact minimum DAG-resolution refutation size (number of resolvent steps) for all
unsat 3-CNFs-with-all-clauses-over-n-vars subsets-minimal tiny cases.  Iterative deepening, <30s."""
import itertools, sys, json, time
def res(c,d):
    out=[]
    for l in c:
        if -l in d:
            r=frozenset((c|d)-{l,-l})
            if not any(-x in r for x in r): out.append(r)
    return out
def minsteps(F,limit):
    F=frozenset(F); seen={}
    def dfs(S,k):
        if frozenset() in S: return True
        if k==0: return False
        key=(S,k)
        if key in seen: return False
        L=list(S)
        for i in range(len(L)):
            for j in range(i+1,len(L)):
                for r in res(L[i],L[j]):
                    if r in S: continue
                    if dfs(S|{r},k-1): return True
        seen[key]=1; return False
    for k in range(1,limit+1):
        seen.clear()
        if dfs(F,k): return k
    return None
def allclauses(n,w):
    out=[]
    for vs in itertools.combinations(range(1,n+1),w):
        for sg in itertools.product([1,-1],repeat=w):
            out.append(frozenset(v*s for v,s in zip(vs,sg)))
    return out
if __name__=="__main__":
    t=time.time(); res_out={}
    for n in (1,2,3):
        F=allclauses(n,n)  # complete CNF: 2^n clauses of width n
        res_out[f"complete_n{n}"]=minsteps(F,2**n-1+1)
    print(json.dumps(res_out),time.time()-t)
