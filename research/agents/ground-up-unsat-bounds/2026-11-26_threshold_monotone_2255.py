from functools import lru_cache
from itertools import combinations, product
from math import comb, inf

def canonical(clauses):
    return tuple(sorted(set(tuple(sorted(c)) for c in clauses)))

def restrict(F, v, val):
    l = v if val else -v
    return canonical(tuple(x for x in c if x != -l) for c in F if l not in c)

@lru_cache(None)
def optimum(F):
    if () in F: return (1, 0)
    if not F: return (inf, inf)
    pairs = [(optimum(restrict(F,v,0)),optimum(restrict(F,v,1)))
             for v in {abs(x) for c in F for x in c}]
    return min(a[0]+b[0] for a,b in pairs), min(1+max(a[1],b[1]) for a,b in pairs)

def phase(F,G,k,t,n):
    S=range(n+1,n+k+1)
    return canonical([c+P for c in F for P in combinations(S,k-t+1)] +
                     [d+tuple(-x for x in Q) for d in G for Q in combinations(S,t)])

def verify(F,n):
    hits=[0]*len(F); sat=0
    for values in product((0,1),repeat=n):
        bad=[i for i,c in enumerate(F) if all(values[abs(l)-1] != (l>0) for l in c)]
        if not bad: sat+=1
        if len(bad)==1: hits[bad[0]]+=1
    return sat, sum(x>0 for x in hits)

def bits(F,n):
    return n+2*len(F)+2+sum(map(len,F))*(2+n.bit_length())

def main():
    F=canonical([(1,),(-1,)])
    G=canonical([(1,2),(-1,2),(-2,)])
    print('k t variables clauses literals bits leaves depth necessary_clauses SAT_assignments SAT_neighbor_assignments')
    for k,t in [(1,1),(2,1),(2,2),(3,2),(4,2),(4,3),(5,3),(6,3),(6,4)]:
        H=phase(F,G,k,t,2); n=k+2
        L,D=optimum(H); sat,necessary=verify(H,n)
        assert L==2*comb(k,t-1)+3*comb(k,t)
        assert sat==0 and necessary==len(H)
        neighbor=phase(F[:-1],G,k,t,2)
        s,_=verify(neighbor,n); assert s>0
        print(k,t,n,len(H),sum(map(len,H)),bits(H,n),L,D,necessary,sat,s)
    H=phase(F,G,6,3,2)
    # begin with all selectors pinned, unfix alternately so boundary moves
    order=[1,0,1,0,1,0]
    print('reverse: free selectors, threshold, leaves, depth')
    for u in range(7):
        J=H
        for j,val in enumerate(order[u:],start=u+3): J=restrict(J,j,val)
        r=3-sum(order[u:]); L,D=optimum(J)
        expected=3 if r<=0 else 2 if r>u else 2*comb(u,r-1)+3*comb(u,r)
        assert L==expected
        print(u,r,L,D)
    # all nonnegative shared AND patterns, compare feasibility characterization
    masks=[1,2,3,5,6,7]
    total=0
    for target in product((0,1),repeat=len(masks)):
        U=0
        for a,b in zip(masks,target):
            if b: U|=a
        pred=all(b or (a&U)!=a for a,b in zip(masks,target))
        actual=any(all(((a&x)==a)==bool(b) for a,b in zip(masks,target)) for x in range(8))
        assert pred==actual
        total+=1
    print('shared positive AND target patterns verified:',total)
if __name__=='__main__':main()

def monotone_lift(F):
    n=max(abs(x) for c in F for x in c)
    return canonical([(2*i-1,2*i) for i in range(1,n+1)]+[
        tuple(-(2*abs(l)-1 if l>0 else 2*abs(l)) for l in c) for c in F])

if __name__=='__main__':
    print('monotone lift: n,m,base leaves,lift leaves,depth,necessary clauses,lower,upper')
    cases=[[(1,),(-1,)],[(1,2),(1,-2),(-1,)],[(1,2),(1,-2),(-1,2),(-1,-2)],
           [(1,),(-1,2),(-2,3),(-3,)],[(1,2),(-1,-2),(-2,3),(2,-3),(-3,1),(3,-1)]]
    for C in cases:
        F=canonical(C); n=max(abs(x) for c in F for x in c); H=monotone_lift(F)
        L,_=optimum(F); LH,D=optimum(H); sat,nec=verify(H,2*n)
        assert sat==0 and nec==len(H) and L+n<=LH<=2*L-1
        print(n,len(F),L,LH,D,nec,L+n,2*L-1)
