"""Quickcheck, POINTWISE-DIFFERENTIAL64: proper 3CNF source bit differences."""
import itertools
def route(b, kind):
    h=int(not any(b))
    if kind=="balanced": return tuple(v^h for v in b)
    return (sum(b)%2,)+tuple(0 for _ in b[1:])
def source(sigma):
    q=len(sigma);V=2*q+3
    edges=[(1,2),(2,3),(3,1)]
    for i in range(q):
        x=4+2*i
        edges += [(1,x),(1,x+1),(x,x+1)]
    for i,b in enumerate(sigma):
        x=4+2*i
        edges.append((4+2*((i+1)%q),x if b else x+1))
    def a(v,c): return 3*(v-1)+c
    clauses=[];binary=[]
    for v in range(1,V+1):
        clauses.append(tuple(a(v,j) for j in (1,2,3)))
        binary += [(-a(v,1),-a(v,2)),(-a(v,1),-a(v,3)),(-a(v,2),-a(v,3))]
    for u,v in edges:
        binary += [(-a(u,j),-a(v,j)) for j in (1,2,3)]
    n=3*V
    for x,y in binary:
        n+=1
        clauses += [(x,y,n),(x,y,-n)]
    m=len(clauses)
    assert (n,m)==(24*q+27,38*q+39)
    W=(64*(n+m+1)-1).bit_length()
    words=[n,m]
    for c in clauses:
        assert len(set(map(abs,c)))==3
        words += [3]+[2*abs(x)+(x<0) for x in c]
    return words,W
def bitdiff(a,b,W):
    changed=set()
    for j,(x,y) in enumerate(zip(a,b)):
        v=x^y
        for k in range(W):
            if v>>k&1: changed.add(j*W+k)
    return changed
def cover(sets,q):
    masks={}
    for i,s in enumerate(sets):
        for j in s: masks[j]=masks.get(j,0)|(1<<i)
    dp=[q+1]*(1<<q);dp[0]=0
    for mm in set(masks.values()):
        for z in range((1<<q)-1,-1,-1):
            dp[z|mm]=min(dp[z|mm],dp[z]+1)
    return dp[-1]
count=0
for q in (4,6,8):
    for b in itertools.product((0,1),repeat=q):
        for kind in ("balanced","collapsed"):
            assert sum(route(b,kind))%2==sum(b)%2
            count+=1
    for label,base in (("SAT",(1,)*q),("UNSAT",(1,)*(q-1)+(0,))):
        for kind in ("balanced","collapsed"):
            original,W=source(route(base,kind))
            diff=[]
            for i in range(q):
                other=list(base);other[i]^=1
                words,W2=source(route(other,kind))
                assert W==W2 and len(words)==len(original)
                diff.append(bitdiff(original,words,W))
            required=cover(diff,q)
            assert required==(q if kind=="balanced" else 1)
            print(q,label,kind,"N",len(original)*W,"minimum_bit_reads",required)
print("PASS parity label checks",count)
