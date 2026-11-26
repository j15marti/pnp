from functools import lru_cache
from itertools import combinations,product

def patch(q):
    V=[(a,b,q-a-b) for a in range(q+1) for b in range(q-a+1)];ix={v:i for i,v in enumerate(V)}
    F=[]
    def v(a,b):return (a,b,q-a-b)
    for a in range(q):
        for b in range(q-a):
            F.append([v(a,b),v(a+1,b),v(a,b+1)])
            if a+b+2<=q:F.append([v(a+1,b),v(a,b+1),v(a+1,b+1)])
    B=[sum(1<<ix[u] for u in f) for f in F];inc=[[j for j,b in enumerate(B) if b>>i&1] for i in range(len(V))]
    @lru_cache(None)
    def cover(mask):
        if not mask:return ()
        p=min((i for i in range(len(V)) if mask>>i&1),key=lambda i:sum(B[j]&mask==B[j] for j in inc[i]))
        for j in inc[p]:
            if B[j]&mask==B[j]:
                z=cover(mask^B[j])
                if z is not None:return (j,)+z
        return None
    out={}
    for edge in product([0,1],repeat=3):
        for corn in [0,1]:
            mask=sum(1<<i for i,v in enumerate(V) if min(v)>0 or (v.count(0)==1 and edge[v.index(0)]) or (v.count(0)==2 and corn))
            w=cover(mask);out[(edge,corn)]=None if w is None else [F[j] for j in w]
    return out
if __name__=='__main__':
    for q in [4,7,10,13]:
        R=patch(q);print(q,[(s,c,len(w) if w is not None else None) for (s,c),w in R.items()],flush=True)
