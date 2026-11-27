"""Ground-up UNSAT bounds, 2026-11-27. Python standard library only."""
from itertools import product, combinations
from functools import lru_cache
from collections import Counter, defaultdict
import random


def parity(edges, v, charges):
    E = list(edges)
    out=[]
    for i in range(v):
        ids=[j+1 for j,e in enumerate(E) if i in e]
        for bits in product((0,1),repeat=len(ids)):
            if sum(bits)%2 != charges[i]:
                out.append(tuple(-j if b else j for j,b in zip(ids,bits)))
    return tuple(out)


def mask(F,n):
    return tuple(c+(s*z,) for i,c in enumerate(F) for z in [n+i+1] for s in (1,-1))


def encoding(F,n):
    m=len(F); ell=sum(map(len,F)); return n+2*m+2+(n.bit_length()+2)*ell


def restrict(F,x,b):
    p=x if b else -x
    return tuple(sorted(set(tuple(l for l in c if l!=-p) for c in F if p not in c)))


def canon(F): return tuple(sorted(set(tuple(sorted(c)) for c in F)))


def tree(F):
    @lru_cache(None)
    def dp(G):
        if () in G:return (1,0)
        if not G:return (float('inf'),float('inf'))
        ans=[float('inf'),float('inf')]
        for x in sorted({abs(l) for c in G for l in c}):
            a,b=[dp(restrict(G,x,k)) for k in (0,1)]
            ans[0]=min(ans[0],a[0]+b[0]);ans[1]=min(ans[1],1+max(a[1],b[1]))
        return tuple(ans)
    return dp(canon(F))


def witness_mask(F,n):
    # For every base clause, find unique-violation witness, lift to both signs.
    seen={}
    for a in product((0,1),repeat=n):
        bad=[i for i,c in enumerate(F) if not any(a[abs(l)-1]==(l>0) for l in c)]
        if len(bad)==1:seen[bad[0]]=a
    assert len(seen)==len(F)
    G=mask(F,n)
    for i,a in seen.items():
        for j in (0,1):
            vals=a+tuple(j if k==i else 0 for k in range(len(F)))
            bad=[k for k,c in enumerate(G) if not any(vals[abs(l)-1]==(l>0) for l in c)]
            assert bad==[2*i+j]
    return len(G)


def raw_min(F,n,kind):
    # Literal-level brute force of every candidate and every branch; for RH,
    # enumerate all renamings, independently of graph structure.
    for k in range(n+1):
        for S in combinations(range(1,n+1),k):
            ok=True
            for bits in product((0,1),repeat=k):
                G=F
                for x,b in zip(S,bits):G=restrict(G,x,b)
                if kind=='2':valid=all(len(c)<=2 for c in G)
                else:
                    U=sorted({abs(l) for c in G for l in c})
                    valid=False
                    for flip in product((0,1),repeat=len(U)):
                        r=dict(zip(U,flip))
                        if all(sum((l>0)^r[abs(l)] for l in c)<=1 for c in G):valid=True;break
                if not valid:ok=False;break
            if ok:return k,S


def branch_requirements(F,n,S):
    """Independent literal-sign scan, not graph formula. For every assignment
    to original pins return minimal mask sets for each possible RH renaming,
    and the one mandatory mask set for 2-CNF (None means impossible)."""
    U=sorted(set(range(1,n+1))-set(S))
    for vals in product((0,1),repeat=len(S)):
        a=dict(zip(S,vals)); alive=[]
        for i,c in enumerate(F):
            if any(abs(l) in a and a[abs(l)]==(l>0) for l in c):continue
            alive.append((i,tuple(l for l in c if abs(l) not in a)))
        two=None if any(len(c)>2 for _,c in alive) else sum(1<<i for i,c in alive if len(c)==2)
        rh=set()
        for vals2 in product((0,1),repeat=len(U)):
            flip=dict(zip(U,vals2));req=0
            for i,c in alive:
                pos=sum((l>0)^flip[abs(l)] for l in c)
                if pos>1:break
                if pos==1:req|=1<<i
            else:rh.add(req)
        # Remove supersets, as those never help to meet a subset budget.
        rh=tuple(q for q in rh if not any(p!=q and p&q==p for p in rh))
        yield (two,rh)


def masked_check_all(F,n,k,kind):
    """Enumerate ALL size-k backdoors. Private mask pins need not be assigned
    explicitly: either mask value retains exactly the same base clause, or an
    unpinned mask contributes both signs. The sign scan is exact for each."""
    m=len(F);tested=passed=0;first=None
    for q in range(max(0,k-m),min(n,k)+1):
        for S in combinations(range(1,n+1),q):
            req=list(branch_requirements(F,n,S))
            for Z in combinations(range(m),k-q):
                z=sum(1<<i for i in Z);tested+=1
                def accept(t,r):
                    a=t is not None and t&z==t
                    b=any(p&z==p for p in r)
                    return a if kind=='2' else b if kind=='RH' else a or b
                if all(accept(t,r) for t,r in req):
                    passed+=1
                    if first is None:first=(S,Z)
    return tested,passed,first


def affine(groups):
    # Track XOR combinations, check every contradiction or recovered witness.
    rows=[(sum(1<<(i-1) for i in ids),charge) for ids,charge in groups]
    piv={}
    for k,(a,b) in enumerate(rows):
        trace=1<<k
        while a:
            j=a.bit_length()-1
            if j not in piv:piv[j]=(a,b,trace);break
            aa,bb,tt=piv[j];a^=aa;b^=bb;trace^=tt
        if a==0 and b:
            u=v=0
            for i,(aa,bb) in enumerate(rows):
                if trace>>i&1:u^=aa;v^=bb
            assert (u,v)==(0,1)
            return None
    word=0
    for j,(a,b,_) in sorted(piv.items()):
        if ((a&word).bit_count()%2)!=b:word|=1<<j
    assert all((a&word).bit_count()%2==b for a,b in rows)
    return word


def recognize(G):
    counts=Counter(abs(l) for c in G for l in c)
    private={x for x,c in counts.items() if c<=2}; owners=defaultdict(list)
    for c in G:
        if len(c)!=4 or len(set(map(abs,c)))!=4 or 0 in c:return None
        z=[l for l in c if abs(l) in private]
        if len(z)!=1:return None
        owners[abs(z[0])].append((z[0],tuple(sorted(l for l in c if l!=z[0]))))
    base=[];exception=0;free={}
    for x,p in owners.items():
        if len(p)==1 or (len(p)==2 and p[0]==p[1]):
            exception+=1;free[x]=int(p[0][0]>0);continue
        if len(p)!=2 or p[0][0]!=-p[1][0] or p[0][1]!=p[1][1]:return None
        base.append(p[0][1])
    if exception>1:return None
    by=defaultdict(set)
    for c in base:by[tuple(sorted(map(abs,c)))].add(c)
    eq=[];other=[]
    for ids,cs in by.items():
        allowed=[a for a in product((0,1),repeat=3) if tuple(sorted(-i if b else i for i,b in zip(ids,a))) not in cs]
        parity={sum(a)%2 for a in allowed}
        if len(allowed)==4 and len(parity)==1:eq.append((ids,parity.pop()))
        else:other.append((ids,allowed))
    if len(other)>1:return None
    if not other:word=affine(eq)
    else:
        ids,allowed=other[0];word=None
        for a in allowed:
            word=affine(eq+[((i,),b) for i,b in zip(ids,a)])
            if word is not None:break
    if word is None:return False
    for x,b in free.items():
        if b:word|=1<<(x-1)
        else:word&=~(1<<(x-1))
    assert all(any(bool(word>>(abs(l)-1)&1)==(l>0) for l in c) for c in G)
    return True


def encode(F,n):
    unary=lambda k:'1'*k+'0'
    w=n.bit_length()
    return unary(n)+unary(len(F))+''.join(unary(len(c))+''.join(format(abs(l),f'0{w}b')+str(int(l<0)) for l in c) for c in F)

def obscure(F,n,rng):
    ids=list(range(1,n+1));rng.shuffle(ids);s=[rng.choice((-1,1)) for _ in ids]
    out=[tuple((1 if l>0 else -1)*s[abs(l)-1]*ids[abs(l)-1] for l in c) for c in F]
    rng.shuffle(out);return tuple(out)


def prism(h):return [(i,(i+1)%h) for i in range(h)]+[(h+i,h+(i+1)%h) for i in range(h)]+[(i,h+i) for i in range(h)]


def main():
    rng=random.Random(20261127)
    # Ground-up: unit, split, parity triangle, K4, prism. Direct masked tree
    # optimization only for small cases; K4/prism via independently proved lift.
    unit=((1,),(-1,));split=((1,2),(1,-2),(-1,))
    triangle=parity([(0,1),(1,2),(2,0)],3,[1,0,0])
    K4=list(combinations(range(4),2))
    for name,F,n in [('unit',unit,1),('split',split,2),('triangle',triangle,3),('K4',parity(K4,4,[1,0,0,0]),6),('prism3',parity(prism(3),6,[1,0,0,0,0,0]),9)]:
        G=mask(F,n);L,D=tree(F);nn=n+len(F)
        direct=tree(G) if nn<=9 else None
        if direct:assert direct==(2*L,D+1)
        print(name,'n,m,N',n,len(F),encoding(F,n),'masked n,m,N',nn,len(G),encoding(G,nn),'base L,D',(L,D),'masked L,D by lift',(2*L,D+1),'direct',direct,'deletion witnesses',witness_mask(F,n),flush=True)
        if name=='triangle':
            # unfix original variables then masks, all other bits fixed zero
            vals=[]
            for k in range(nn+1):
                H=G
                for x in range(k+1,nn+1):H=restrict(H,x,0)
                vals.append(tree(H))
            print('triangle masked reverse L,D',vals,flush=True)
    F=parity(K4,4,[1,0,0,0]);n=6
    for kind in ('2','RH'):
        print('K4 raw exact backdoor',kind,raw_min(F,n,kind),flush=True)
    for kind,k in [('2',4),('RH',6),('union',4)]:
        a=masked_check_all(F,n,k-1,kind);b=masked_check_all(F,n,k,kind)
        assert a[1]==0 and b[1]>0
        print('K4 masked',kind,'size',k-1,a,'size',k,b,flush=True)
    # Verify all original charge patterns, odd and even, independent raw RH search.
    counts=Counter()
    for ch in product((0,1),repeat=4):
        k,_=raw_min(parity(K4,4,ch),6,'RH');counts[(sum(ch)%2,k)]+=1
    print('K4 raw RH all charge patterns',sorted(counts.items()),flush=True)
    for h in (3,4,8,16,32):
        E=prism(h);v=2*h;n=len(E)
        for _ in range(4):
            ch=[rng.randrange(2) for i in range(v)]
            ch[0]^=sum(ch)%2^1
            F=parity(E,v,ch);G=mask(F,n);nn=n+len(F)
            assert recognize(obscure(G,nn,rng)) is False
            j=rng.randrange(len(G));assert recognize(obscure(G[:j]+G[j+1:],nn,rng)) is True
            # Same length, final sign bit only: duplicate the opposite mask clause.
            H=G[:-1]+(G[-1][:-1]+(-G[-1][-1],),)
            a,b=encode(G,nn),encode(H,nn);assert len(a)==encoding(G,nn) and a[:-1]==b[:-1] and a[-1]!=b[-1]
            assert recognize(H) is True and recognize(obscure(H,nn,rng)) is True
            ch[0]^=1;G=mask(parity(E,v,ch),n)
            assert recognize(obscure(G,nn,rng)) is True
        print('recognizer prism v',v,'masked N',encoding(G,nn),'16 randomized cases + 4 final-bit checks OK',flush=True)
    print('ALL CHECKS PASSED',flush=True)

if __name__=='__main__':main()
