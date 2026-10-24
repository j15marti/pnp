#!/usr/bin/env python3
"""M22-QUAD-NEUTRAL102 independent standalone portable theorem control."""
from itertools import combinations, product
from collections import Counter

P=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
Q=((1,2,4),(1,3,6),(2,3,5),(4,5,6))

def source(neg=Q):
    return tuple(P)+tuple(tuple(-x for x in c) for c in neg)

def valid(F):
    c=Counter(x for clause in F for x in clause)
    k=max(abs(x) for clause in F for x in clause)
    paired={tuple(sorted(cl)) for cl in F}
    return (all(len(cl)==3 and len({abs(x) for x in cl})==3
             and (all(x>0 for x in cl) or all(x<0 for x in cl)) for cl in F)
            and len(paired)==len(F) and all(c[x]==c[-x]==2 for x in range(1,k+1))
            and any(tuple(sorted(-x for x in cl)) not in paired for cl in F))

def quad(F,ids):
    old=[F[j] for j in ids]
    X=[x for cl in old if cl[0]>0 for x in cl]
    Z=[-x for cl in old if cl[0]<0 for x in cl]
    assert len(X)==len(Z)==6
    a,b,c,d,e,f=range(max(abs(x) for cl in F for x in cl)+1,
                       max(abs(x) for cl in F for x in cl)+7)
    plus=((a,d,X[0]),(a,e,X[1]),(b,e,X[2]),(b,f,X[3]),
          (c,f,X[4]),(c,d,X[5]))
    minus=((-a,-d,-Z[0]),(-a,-f,-Z[1]),(-b,-d,-Z[2]),
           (-b,-e,-Z[3]),(-c,-e,-Z[4]),(-c,-f,-Z[5]))
    return tuple(v for i,v in enumerate(F) if i not in set(ids)),\
           tuple(v for i,v in enumerate(F) if i not in set(ids))+plus+minus

def holds(F,word):
    return all(any((word>>(abs(v)-1)&1)==(v>0) for v in c) for c in F)

def models(F):
    k=max(abs(v) for c in F for v in c)
    return sum(holds(F,a) for a in range(1<<k))

def main():
    checks=0
    for base in (source(),source(P)):
        for po,ne in product(combinations(range(4),2),combinations(range(4,8),2)):
            rest,G=quad(base,po+ne)
            assert valid(G)
            checks+=1
            for orig in range(64):
                n=sum(holds(G,orig+(ext<<6)) for ext in range(64))
                assert (n>0)==holds(rest,orig)
                assert holds(G,orig+(7<<6))==holds(rest,orig)
                checks+=2
    Y=source(); r,A=quad(Y,(0,1,4,5))
    r,B=quad(A,(4,5,10,11))
    assert valid(B) and models(Y)==20 and models(A)==314 and models(B)==5936
    checks+=4
    for h in (0,3,6,9):
        for dp,dn in product(range(5),repeat=2):
            t_possible=[t for t in range(h+1) if
                        2*t>=dp+2*h//3 and 2*(h-t)>=dn+2*h//3]
            if h==6 and dp+dn>4: assert not t_possible; checks+=1
            if h==3 and dp==dn==2: assert not t_possible; checks+=1
    print('M22-QUAD-NEUTRAL102: PASS; assertion-accounted checks',checks)
if __name__=='__main__':main()
