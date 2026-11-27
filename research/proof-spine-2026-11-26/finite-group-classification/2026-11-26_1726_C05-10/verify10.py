from itertools import combinations
from fractions import Fraction
G=[((1,1),(2,1)),((1,1),(4,1)),((2,1),(5,1)),((3,0),(8,0)),((3,1),(4,1)),((3,1),(13,1)),((5,0),(14,0)),((5,1),(13,1))]
E=[(0,3),(0,7),(1,5),(1,6),(2,3),(2,5),(2,6),(2,7),(3,5),(3,6),(3,7),(4,5),(4,6),(5,6),(5,7)]
E={frozenset(e) for e in E}
def hit(F,x):return all((v&x).bit_count()%2==b for v,b in F)
def clique(S):return all(frozenset(e) in E for e in combinations(S,2))
# Independently check a perfect elimination order exists and maximum clique is four.
V=set(range(8));order=[]
while V:
    v=next(v for v in sorted(V) if clique([w for w in V-{v} if frozenset((v,w)) in E]))
    order.append(v);V.remove(v)
C=[S for k in range(1,9) for S in combinations(range(8),k) if clique(S)]
assert max(map(len,C))==4
assert all(sum(hit(F,x) for x in range(16))==4 for F in G)
assert max(sum(hit(F,x) and hit(H,x) for x in range(16)) for F,H in combinations(G,2))==2
P=[sum((-1)**(len(S)+1) for S in C if all(hit(G[i],x) for i in S)) for x in range(16)]
assert all(v>=0 and (v==0)==(not any(hit(F,x) for F in G)) for x,v in enumerate(P))
assert sum(P)==16 and sum(v*v for v in P)==24
print({'order':order,'forest_mean_lower_bound':str(Fraction(9,8)),'chordal_mean':str(Fraction(sum(P),16)),'chordal_variance':str(Fraction(sum(v*v for v in P),16)-1),'values':P})
