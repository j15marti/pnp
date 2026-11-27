from itertools import product, combinations
from functools import lru_cache
from math import ceil,log2
import random

def parity_graph(edges):
    v=max(max(e) for e in edges)+1
    C=[]
    for i in range(v):
        E=[j+1 for j,e in enumerate(edges) if i in e]
        for a in product((0,1),repeat=len(E)):
            if sum(a)%2 != int(i==0):
                C.append(tuple(j if not x else -j for j,x in zip(E,a)))
    return C,len(edges)

def lift(C,S):
    return [tuple(c)+tuple(j if not b else -j for j,b in zip(s,a)) for c,s in zip(C,S) for a in product((0,1),repeat=len(s))]

def masks(C):
    return [(sum(1<<(abs(j)-1) for j in c),sum(1<<(abs(j)-1) for j in c if j<0)) for c in C]

def optimize(C,n,weights=None,extra=None,fix=(0,0)):
    M=masks(C);weights=weights or [1]*len(C);extra=extra or [0]*len(C)
    @lru_cache(None)
    def dp(p,a):
        hits=[i for i,(m,w) in enumerate(M) if p&m==m and a&m==w]
        l=min((weights[i] for i in hits),default=10**20);d=min((extra[i] for i in hits),default=10**9)
        if l==1 and d==0:return l,d
        for j in range(n):
            b=1<<j
            if p&b:continue
            x=dp(p|b,a);y=dp(p|b,a|b)
            l=min(l,x[0]+y[0]);d=min(d,1+max(x[1],y[1]))
        return l,d
    return dp(*fix)

def violations(C,n):
    M=masks(C);counts=[0]*len(C);sat=0
    for a in range(1<<n):
        hits=[i for i,(m,w) in enumerate(M) if a&m==w]
        if not hits:sat+=1
        if len(hits)==1:counts[hits[0]]+=1
    return sat,counts

def encode_bits(C,n):
    # unary n,m, then unary width, each literal one sign + n.bit_length() bits
    return n+len(C)+2+sum(1+len(c)*(n.bit_length()+2) for c in C)

def recover(C):
    # deterministic smallest lexicographic complementary pair; exact equivalence
    F=set(frozenset(c) for c in C);steps=0
    while True:
        pair=None
        for c in sorted(F,key=lambda c:(len(c),tuple(sorted(c)))):
            for x in sorted(c):
                d=(c-{x})|{-x}
                if d in F:
                    pair=(c,d,c-{x});break
            if pair:break
        if not pair:return F,steps
        c,d,b=pair;F.remove(c);F.remove(d);F.add(b);steps+=1

def restrict(C,p):
    return [tuple(x for x in c if abs(x) not in p) for c in C if not any(p.get(abs(x))==int(x>0) for x in c)]

def gf2(rows):
    piv={}
    for m,b in rows:
        while m:
            j=m.bit_length()-1
            if j not in piv:piv[j]=(m,b);break
            u,c=piv[j];m^=u;b^=c
        if not m and b:return None
    x=0
    for j,(m,b) in sorted(piv.items()):
        if (m&x).bit_count()%2!=b:x|=1<<j
    return x

def masked_parity_decide(C):
    # Sound partial decider; None means unsupported, not NO. No provenance supplied.
    F=set(frozenset(c) for c in C)
    if any(len(c)!=4 for c in F):return None
    while True:
        pair=None
        for c in F:
            if len(c)!=4:continue
            for x in c:
                d=(c-{x})|{-x}
                if d in F:pair=(c,d,c-{x});break
            if pair:break
        if not pair:break
        c,d,b=pair;F.remove(c);F.remove(d);F.add(b)
    for c in list(F):
        if len(c)==4:
            if not any(all(abs(x) not in {abs(y) for y in d} for d in F if d!=c) for x in c):return None
            F.remove(c) # existentially eliminate a singleton variable
    groups={}
    for c in F:
        if len(c)!=3:return None
        key=tuple(sorted(abs(x) for x in c));pat=sum(1<<i for i,j in enumerate(key) if -j in c)
        groups.setdefault(key,set()).add(pat)
    rows=[];defects=[]
    for key,forbidden in groups.items():
        allowed=set(range(8))-forbidden
        if len(allowed)==4 and len({i.bit_count()%2 for i in allowed})==1:
            rows.append((sum(1<<(j-1) for j in key),next(iter(allowed)).bit_count()%2))
        else:defects.append((key,allowed))
    if len(defects)>1:return None
    if not defects:return gf2(rows) is not None
    key,allowed=defects[0]
    return any(gf2(rows+[(1<<(j-1),(a>>i)&1) for i,j in enumerate(key)]) is not None for a in allowed)

def main():
    ring,n=parity_graph([(0,1),(1,2),(2,0)])
    k4,n4=parity_graph(list(combinations(range(4),2)))
    cases=[('unit',[(1,),(-1,)],1,[(2,),(2,)]),('unit disjoint',[(1,),(-1,)],1,[(2,3),(4,)]),('ring shared',ring,n,[(4,5)]*len(ring)),('ring mixed',ring,n,[(4,5),(5,),(),(4,),(6,), (4,6)]),('ring private',ring,n,[(4+i,) for i in range(len(ring))]),('K4 shared',k4,n4,[(7,8)]*len(k4)),('K4 mixed',k4,n4,[((7,8) if i%5==0 else (8,) if i%3==0 else ()) for i in range(len(k4))])]
    for name,C,n,S in cases:
        G=lift(C,S);v=max(n,max((x for s in S for x in s),default=n));k=[len(s) for s in S]
        base=optimize(C,n);pred=optimize(C,n,[2**i for i in k],k);direct=optimize(G,v)
        assert pred==direct
        sat,counts=violations(G,v);assert sat==0 and min(counts)>0
        F,steps=recover(G);assert not violations(list(F),v)[0]
        print(name,'n,m,N',v,len(G),encode_bits(G,v),'base L,D',base,'lift L,D',direct,'DAG add',len(G)-len(C),'recovery steps',steps,'min deletion witnesses',min(counts))
    # Reverse unfix shared selectors of mixed ring, then independently solve each restricted CNF
    C=ring;n=3;S=cases[3][3];v=6;G=lift(C,S)
    for t in range(v+1):
        p={j:0 for j in range(t+1,v+1)};H=restrict(G,p)
        pred=optimize(restrict(C,{j:b for j,b in p.items() if j<=n}),t) if t<n else optimize(C,n,[2**len(set(s)-p.keys()) for s in S],[len(set(s)-p.keys()) for s in S])
        direct=optimize(H,t)
        assert pred==direct,(t,pred,direct)
        print('reverse',t,direct)
    # Random signed/renamed mixed lifts with both labels. Recover by exact pair elimination, compare SAT.
    rng=random.Random(20261127);counts=[0,0]
    for _ in range(100):
        C=list(ring)
        if rng.randrange(2):del C[rng.randrange(len(C))]
        S=[tuple(j for j in (4,5,6) if rng.randrange(2)) for _ in C];G=lift(C,S)
        perm=list(range(1,7));rng.shuffle(perm);sgn=[rng.choice((-1,1)) for _ in perm]
        G=[tuple((1 if x>0 else -1)*sgn[abs(x)-1]*perm[abs(x)-1] for x in c) for c in G];rng.shuffle(G)
        F,_=recover(G);sat=bool(violations(G,6)[0]);assert sat==bool(violations(list(F),6)[0]);counts[sat]+=1
    print('random renamed/signed equivalence checks UNSAT,SAT',counts)
    # Private masked cubic parity, hidden identifiers/signs and one-clause SAT neighbors.
    checks=[0,0]
    for h in (3,4,8,16,32):
        edges=[(r*h+i,r*h+(i+1)%h) for r in (0,1) for i in range(h)]+[(i,h+i) for i in range(h)]
        C,n=parity_graph(edges);G=lift(C,[(n+i+1,) for i in range(len(C))]);v=n+len(C)
        for _ in range(5):
            for label in (0,1):
                H=G[:]
                if label:del H[rng.randrange(len(H))]
                perm=list(range(1,v+1));rng.shuffle(perm);sgn=[rng.choice((-1,1)) for _ in perm]
                H=[tuple((1 if x>0 else -1)*sgn[abs(x)-1]*perm[abs(x)-1] for x in c) for c in H];rng.shuffle(H)
                assert masked_parity_decide(H)==bool(label);checks[label]+=1
        print('masked prism',h,'n,m,N',v,len(G),encode_bits(G,v))
    print('masked parity both-label checks',checks)
    # Recheck earlier prism values without using its decision tree optimizer.
    for h in (3,4):
        e=3*h;C=[]
        for rail in range(2):
            for i in range(h):
                ps=[rail*h+(i-1)%h+1,rail*h+i+1,2*h+i+1]
                for a,b,c in product((0,1),repeat=3):
                    ok=((c if rail==0 else 1-c)==(b & (1-a))) if i==0 else (a==(b&c) if rail==0 else b==(a|c))
                    if not ok:C.append(tuple(j if not x else -j for j,x in zip(ps,(a,b,c))))
        a=optimize(C,e);assert a[0]==4*h+2
        sat,counts=violations(C,e);assert not sat and sum(x>0 for x in counts)==4*h+2
        print('prior prism independent',h,'L,D',a,'essential clauses',sum(x>0 for x in counts))
if __name__=='__main__':main()
