from itertools import product
from functools import lru_cache

@lru_cache(None)
def path(r):
    return min((2**(k-1)*(path(r[:i])+path(r[i+1:])) for i,k in enumerate(r)),default=1)
def cycle(r):
    return min(2**k*path(r[i+1:]+r[:i]) for i,k in enumerate(r))

def cnf(r,closed=True,charges=None):
    n=len(r) if closed else len(r)+1
    inc=[[] for _ in range(n)]; m=0
    for i,k in enumerate(r):
        for _ in range(k):
            m+=1;inc[i].append(m);inc[(i+1)%n].append(m)
    charges=charges if charges is not None else [1]+[0]*(n-1)
    return m,tuple(tuple(-x if b else x for x,b in zip(xs,bits)) for xs,c in zip(inc,charges) for bits in product((0,1),repeat=len(xs)) if sum(bits)%2!=c)

def exact(m,clauses):
    masks=[(sum(1<<(abs(x)-1) for x in c),sum(1<<(abs(x)-1) for x in c if x<0)) for c in clauses]
    @lru_cache(None)
    def go(assigned,ones):
        if any(assigned&mask==mask and ones&mask==pat for mask,pat in masks):return (1,0)
        if assigned==(1<<m)-1: raise ValueError('SAT')
        bestl=bestd=10**100
        for i in range(m):
            bit=1<<i
            if assigned&bit:continue
            l0,d0=go(assigned|bit,ones);l1,d1=go(assigned|bit,ones|bit)
            bestl=min(bestl,l0+l1);bestd=min(bestd,1+max(d0,d1))
        return bestl,bestd
    return go(0,0)

def minimal(m,cs):
    seen=set()
    for a in range(1<<m):
        bad=[i for i,c in enumerate(cs) if all(bool(a&(1<<(abs(x)-1)))==(x<0) for x in c)]
        assert bad
        if len(bad)==1:seen.add(bad[0])
    return len(seen)

if __name__=='__main__':
    for closed,r in [(False,(1,)),(False,(2,2)),(False,(2,1,3)),(True,(1,1,1)),(True,(2,2,2)),(True,(2,2,2,2)),(True,(1,2,3,1)),(True,(3,3,3))]:
        m,cs=cnf(r,closed);l,d=exact(m,cs);assert l==(cycle(r) if closed else path(r))
        print('cycle' if closed else 'path',r,m,len(cs),l,d,minimal(m,cs))
    for n,k in [(4,1),(4,2),(8,2),(16,4),(64,6),(256,8)]:
        r=(k,)*n;print('formula',n,k,n*k,n*2**(2*k-1),cycle(r),k*(1+(n.bit_length()-1)))
