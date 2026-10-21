"""Independent check of Lemma 59A (blocked parent scans): exactness + pass count."""
import random, math
def blocked(parent, queries, B):
    ans=[False]*len(queries); passes=0
    for s in range(0,len(queries),B):
        d={}
        for i in range(s,min(s+B,len(queries))): d.setdefault(queries[i],[]).append(i)
        passes+=1
        for k in parent:
            for i in d.get(k,()): ans[i]=True
    return ans,passes
random.seed(1)
bad=0
for t in range(300):
    N=random.randint(1,200); U=random.randint(1,300)
    parent=[random.randrange(U) for _ in range(N)]
    Q=random.randint(1,120); qs=[random.randrange(U) for _ in range(Q)]
    B=random.randint(1,Q)
    a,p=blocked(parent,qs,B); S=set(parent)
    if a!=[q in S for q in qs] or p!=math.ceil(Q/B): bad+=1
print("mismatches",bad,"of 300")
