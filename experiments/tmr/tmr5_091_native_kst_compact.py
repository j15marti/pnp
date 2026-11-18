"""TMR-5/091 native T5 Kst degree-sequence firewall, independent stdlib verifier."""
from itertools import product
from collections import defaultdict
from math import comb

Y=((0,0,1),(0,0,1),(1,1,0))
N=((0,0,1),(0,1,0),(1,0,1))

def r(a,b):return (b-a)%5 in (1,3)

def get(s,t,positive):
    seed=Y if positive else N
    return [[seed[i if i<3 else 0][j if j<3 else 0] for j in range(t)]
            for i in range(s)]

def deg(mat):
    s,t=len(mat),len(mat[0])
    return tuple(t-sum(row) for row in mat)+tuple(sum(mat[i][j] for i in range(s)) for j in range(t))

def onto(n,k):
    return sum((-1)**(k-i)*comb(k,i)*i**n for i in range(k+1))

def count(mat):
    """Independent generic twin-support algorithm for an oriented biclique."""
    s,t=len(mat),len(mat[0]);left=defaultdict(list);right=defaultdict(list)
    for i in range(s):left[tuple(mat[i])].append(i)
    for j in range(t):right[tuple(mat[i][j] for i in range(s))].append(j)
    groups=list(left.values());rgroups=list(right.values())
    supports=[[(tuple(a for a in range(5) if mask>>a&1),onto(len(g),mask.bit_count()))
               for mask in range(1,32)] for g in groups]
    total=0
    for choice in product(*supports):
        ways=1
        for _,n in choice:ways*=n
        if not ways:continue
        for rg in rgroups:
            j=rg[0]
            allowed=sum(all(all(r(a,b) if mat[lg[0]][j] else r(b,a) for a in S)
                            for lg,(S,_) in zip(groups,choice)) for b in range(5))
            ways*=allowed**len(rg)
            if not ways:break
        total+=ways
    return total,(len(groups),len(rgroups))

def independent(mat):
    """Enumerate each left tuple; eliminate each right vertex independently."""
    s,t=len(mat),len(mat[0]);out=0
    for a in product(range(5),repeat=s):
        n=1
        for j in range(t):
            n*=sum(all(r(a[i],b) if mat[i][j] else r(b,a[i]) for i in range(s))
                   for b in range(5))
        out+=n
    return out

def check():
    patterns={}
    for d in range(5):
        patterns[d]={(int(r(0,z)),int(r(d,z))) for z in range(5) if z not in (0,d)}
        assert not {(0,0),(0,1),(1,0)} <= patterns[d]
    private=sum(1 for a,b,c in product(range(5),repeat=3)
                if r(0,a) and r(a,b) and r(b,c) and r(0,c))
    assert private==1
    for u,v in product(range(5),repeat=2):
        ext=sum(1 for a,b,c in product(range(5),repeat=3)
                if r(u,a) and r(a,b) and r(b,c) and r(u,c) and r(c,v))
        assert ext==int((v-u)%5 in (1,4))
    for s,t in ((3,3),(4,4),(6,7),(25,30),(101,103)):
        yes,no=get(s,t,True),get(s,t,False)
        assert deg(yes)==deg(no)
        assert sum(yes[i][j]!=no[i][j] for i in range(s) for j in range(t))==4
        a,ga=count(yes);b,gb=count(no)
        assert a==5*(2**(s-1)+2**(t-1)) and b==0
        assert ga==(2,2) and gb==(3,3)
        if s<=4 and t<=4:
            assert independent(yes)==a and independent(no)==b
        print('s=',s,'t=',t,'yes=',a,'no=',b,'tw=',min(s,t),
              'cycle_rank=',(s-1)*(t-1),'directions_reversed=',4)
    print('ALL CHECKS PASS')

if __name__=='__main__':check()
