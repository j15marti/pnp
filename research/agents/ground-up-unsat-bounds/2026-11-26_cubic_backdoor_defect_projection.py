from itertools import product, combinations
from functools import lru_cache

def graph(r):
    if r==2: return 4,list(combinations(range(4),2))
    return 2*r, sorted({tuple(sorted((i+j*r,(i+1)%r+j*r))) for j in range(2) for i in range(r)}|{(i,i+r) for i in range(r)})
def cnf(v,E):
    S=[[i+1 for i,e in enumerate(E) if j in e] for j in range(v)]
    F=[tuple(-i if a else i for i,a in zip(s,p)) for j,s in enumerate(S) for p in product((0,1),repeat=3) if sum(p)%2!=(j==0)]
    return S,F

def pair(F,n):
    return [tuple(-(2*abs(x)-(x>0)) for x in c) for c in F]+[(2*i-1,2*i) for i in range(1,n+1)]
def masks(F):
    return [(sum(1<<(x-1) for x in c if x>0),sum(1<<(-x-1) for x in c if x<0)) for c in F]
def optimum(F,n,fix=()):
    C=masks(F); full=(1<<n)-1
    @lru_cache(None)
    def dp(z,o):
        if any(p&z==p and q&o==q for p,q in C): return 1,0
        rem=full&~(z|o); best=10**20; depth=n+1
        if not rem: raise ValueError('SAT')
        while rem:
            b=rem&-rem; rem-=b
            a,d=dp(z|b,o); c,e=dp(z,o|b)
            best=min(best,a+c); depth=min(depth,1+max(d,e))
        return best,depth
    z=sum(1<<i for i,a in fix if a==0); o=sum(1<<i for i,a in fix if a==1)
    return dp(z,o)
def minimal(F,n):
    # Track witnesses that falsify exactly one clause, and check no SAT.
    C=masks(F); witness=set(); full=(1<<n)-1
    for a in range(1<<n):
        z=full^a; bad=-1
        for j,(p,q) in enumerate(C):
            if p&z==p and q&a==q:
                if bad>=0: break
                bad=j
        else:
            if bad<0: return False
            witness.add(bad)
    return len(witness)==len(F)
def backdoor(F,n):
    supports=[sum(1<<(abs(x)-1) for x in c) for c in F if len(c)==3]
    for k in range(n+1):
        for I in combinations(range(n),k):
            b=sum(1<<i for i in I)
            if all(b&s for s in supports): return k

def bits(F,n):
    # unary n,m and clause lengths (each integer a encoded as a ones then zero), signed IDs fixed ceil(log2(n+1)) + sign.
    return n+1+len(F)+1+sum(len(c)+1+len(c)*(n.bit_length()+1) for c in F)

def projected(v,E,D,b):
    D=set(D); J=[i for i,(u,w) in enumerate(E) if u in D or w in D]; good=set(range(v))-D; comps=[]
    while good:
        Q=[good.pop()]; C=set(Q)
        for u in Q:
            for x,y in E:
                if u not in (x,y): continue
                w=y if x==u else x
                if w in good: good.remove(w); Q.append(w); C.add(w)
        comps.append(C)
    equations=[]
    for C in comps:
        mask=sum(1<<j for j,i in enumerate(J) if sum(x in C for x in E[i])==1)
        rhs=sum(b[x] for x in C)%2
        if not mask and rhs:return J,set(),None
        if mask:equations.append((mask,rhs))
    q=len(J)-len(equations)
    P={a for a in range(1<<len(J)) if all((a&m).bit_count()%2==r for m,r in equations)}
    assert len(P)==2**q
    return J,P,q

def check_projection(v,E):
    b=[1]+[0]*(v-1); S,_=cnf(v,E); check=0
    for d in range(min(3,v)+1):
        for D in combinations(range(v),d):
            J,P,q=projected(v,E,D,b); B=set()
            for a in range(1<<len(E)):
                if all(sum((a>>(i-1))&1 for i in S[j])%2==b[j] for j in range(v) if j not in D):
                    B.add(sum(((a>>i)&1)<<k for k,i in enumerate(J)))
            assert P==B; check+=1
    return check

if __name__=='__main__':
    for r in (2,3,4):
        v,E=graph(r); S,F=cnf(v,E); n=len(E); G=pair(F,n)
        assert minimal(F,n)
        if r<=3: assert minimal(G,2*n)
        print('graph',v,'edges',n,'clauses',len(F),'paired clauses',len(G),'bits',bits(F,n),bits(G,2*n),'tree',optimum(F,n),'paired tree',optimum(G,2*n) if r==2 else 'not run','backdoors',backdoor(F,n),backdoor(G,2*n) if r<=3 else 'not run','projection tests',check_projection(v,E),flush=True)
    v,E=graph(2); S,F=cnf(v,E); G=pair(F,len(E))
    # fix all edges to zero and unfix a prescribed prefix
    print('reverse K4',[(j,optimum(F,len(E),[(i,0) for i in range(j,len(E))])) for j in range(len(E)+1)])

def elimination(F,n):
    # Generate resolution DAG, keep only ancestors of empty clause.
    clauses=list(map(frozenset,F)); parents=[None]*len(F); active={c:i for i,c in enumerate(clauses)}
    remaining=set(range(1,n+1))
    while frozenset() not in active and remaining:
        x=min(remaining,key=lambda x:(sum(x in c for c in active)*sum(-x in c for c in active),x));remaining.remove(x)
        pos=[(c,i) for c,i in active.items() if x in c];neg=[(c,i) for c,i in active.items() if -x in c]
        active={c:i for c,i in active.items() if x not in c and -x not in c}
        for c,i in pos:
            for d,j in neg:
                e=(c-{x})|(d-{-x})
                if any(-a in e for a in e) or e in active:continue
                active[e]=len(clauses);clauses.append(e);parents.append((i,j,x))
    Q=[active[frozenset()]]; seen=set(Q)
    for i in Q:
        if parents[i] is None:continue
        a,b,x=parents[i];assert x in clauses[a] and -x in clauses[b] and clauses[i]==(clauses[a]-{x})|(clauses[b]-{-x})
        for j in (a,b):
            if j not in seen:seen.add(j);Q.append(j)
    return sum(parents[i] is not None for i in seen)
if __name__=='__main__':
    for r in (2,3,4):
        v,E=graph(r); S,F=cnf(v,E); G=pair(F,len(E)); print('DAG',v,elimination(F,len(E)),elimination(G,2*len(E)))

def mixed_tests(v,E):
    import random
    rng=random.Random(20261126+v); b=[1]+[0]*(v-1); S,_=cnf(v,E); counts=[0,0]
    for _ in range(100):
        D=set(rng.sample(range(v),rng.randint(1,min(v,3))))
        tables={j:rng.randrange(1,256) for j in D}; J,P,q=projected(v,E,D,b); pos={e:i for i,e in enumerate(J)}
        # Build local tests separately to avoid closure over j in comparison.
        def local(a,j,ids): return (tables[j]>>sum(((a>>ids[i-1])&1)<<k for k,i in enumerate(S[j])))&1
        ans=any(all(local(a,j,pos) for j in D) for a in P)
        brute=any(all(local(a,j,range(len(E))) if j in D else sum((a>>(i-1))&1 for i in S[j])%2==b[j] for j in range(v)) for a in range(1<<len(E)))
        assert ans==brute; counts[ans]+=1
    return counts
if __name__=='__main__':
    for r in (2,3,4):
        v,E=graph(r);print('mixed tests UNSAT/SAT',v,mixed_tests(v,E))
