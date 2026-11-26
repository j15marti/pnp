"""C01-02. Recognize full octahedral triangulations from tuple IDs, then lift
covers through verified factor-13 subdivision. No numerical optimizer needed.
A failed recognition or a violated guard means OPEN, not NO.
"""
import itertools as I, json, collections, math, random
from functools import lru_cache
from sphere import make
from macro import patch
from cps07 import verify

def faces_of(k):
    T,n,V=make(k,True)
    return {tuple(sorted(V[c][v] for c,v in enumerate(t))) for t in T}

def exact_small(T,n,zero=(),one=()):
    # Deterministic exact cover on bounded base only in the polynomial solver.
    B=[sum(1<<(c*n+v) for c,v in enumerate(t)) for t in T]
    mask=(1<<(3*n))-1; selected=[];Z=set(zero)
    for j in one:
        if j in Z or B[j]&mask!=B[j]:return None,0
        mask^=B[j];selected.append(j)
    inc=[[] for _ in range(3*n)]
    for j,b in enumerate(B):
        if j not in Z:
            for c,v in enumerate(T[j]):inc[c*n+v].append(j)
    calls=0
    @lru_cache(None)
    def rec(R):
        nonlocal calls;calls+=1
        if not R:return ()
        best=None;tmp=R
        while tmp:
            bit=tmp&-tmp;tmp^=bit
            q=[j for j in inc[bit.bit_length()-1] if B[j]&R==B[j]]
            if not q:return None
            if best is None or len(q)<len(best):best=q
        for j in best:
            z=rec(R^B[j])
            if z is not None:return (j,)+z
        return None
    a=rec(mask)
    return (None if a is None else selected+list(a)),calls

def recognize(T,n):
    # For untrusted inputs, cap all candidate arithmetic by actual source size.
    if len(T)%8:return None
    k=math.isqrt(len(T)//8)
    if k<=0 or len(T)!=8*k*k or k%3==0 or 3*n!=4*k*k+2:return None
    G={(c,v):set() for c in range(3) for v in range(n)}
    if len(set(T))!=len(T):return None
    for t in T:
        if len(t)!=3 or any(not 0<=v<n for v in t):return None
        for a,b in I.combinations(enumerate(t),2):G[a].add(b);G[b].add(a)
    if any(len(L) not in (4,6) for L in G.values()):return None
    poles=sorted(v for v,L in G.items() if len(L)==4)
    if len(poles)!=6:return None
    def bfs(v):
        d={v:0};Q=collections.deque([v])
        while Q:
            u=Q.popleft()
            for w in G[u]:
                if w not in d:d[w]=d[u]+1;Q.append(w)
        return d
    ds={p:bfs(p) for p in poles}
    if any(len(d)!=len(G) for d in ds.values()):return None
    rem=set(poles);axes=[]
    while rem:
        p=min(rem);rem.remove(p);op=[q for q in rem if ds[p][q]==2*k]
        if len(op)!=1:return None
        rem.remove(op[0]);axes.append(p)
    D={v:tuple(k-ds[p][v] for p in axes) for v in G}
    if len(set(D.values()))!=len(D) or any(sum(map(abs,v))!=k for v in D.values()):return None
    ids={tuple(sorted(D[c,v] for c,v in enumerate(t))):j for j,t in enumerate(T)}
    if ids.keys()!=faces_of(k):return None
    return k,ids

@lru_cache(None)
def verified_patches():
    q=13;R=patch(q);P={}
    for E in I.product((0,1),repeat=3):
        for C in (0,1):
            if C and E!=(1,1,1):continue
            F=R[E,C];assert F is not None
            V={(a,b,q-a-b) for a in range(q+1) for b in range(q-a+1) if min(a,b,q-a-b)>0 or ((a,b,q-a-b).count(0)==1 and E[(a,b,q-a-b).index(0)]) or ((a,b,q-a-b).count(0)==2 and C)}
            seen=[v for f in F for v in f]
            assert len(seen)==len(set(seen)) and set(seen)==V
            for f in F:assert len(f)==3 and all(sum(abs(x-y) for x,y in zip(a,b))==2 for a,b in I.combinations(f,2))
            P[E,C]=F
    return P

def lift(F,W):
    # Every edge is owned exactly once; selected faces receive all their edges.
    inc=collections.defaultdict(list)
    for f in sorted(F):
        for e in I.combinations(f,2):inc[e].append(f)
    own={}
    for e,ff in inc.items():
        assert len(ff)==2
        sel=[f for f in ff if f in W];assert len(sel)<=1
        own[e]=sel[0] if sel else ff[0]
    P=verified_patches();out=set()
    for f in sorted(F):
        E=tuple(int(own[tuple(v for j,v in enumerate(f) if j!=i)]==f) for i in range(3))
        C=int(f in W)
        for p in P[E,C]:
            face=tuple(sorted(tuple(sum(w*v[d] for w,v in zip(b,f)) for d in range(3)) for b in p))
            assert face not in out;out.add(face)
    return out

def solve(T,n,zero=(),one=()):
    z=recognize(T,n)
    if z is None:return 'OPEN',None,{'reason':'recognition'}
    k,ids=z;b=k;levels=0
    while b%13==0:b//=13;levels+=1
    if b not in (1,4,5):return 'OPEN',None,{'reason':'base cap'}
    # A bounded base search, with actual base guard if levels=0.
    S,m,V=make(b,True);face_list=[tuple(sorted(V[c][v] for c,v in enumerate(t))) for t in S]
    inv={f:j for j,f in enumerate(face_list)}; rev={j:f for f,j in ids.items()}
    zz=[inv[rev[j]] for j in zero] if levels==0 else []
    oo=[inv[rev[j]] for j in one] if levels==0 else []
    w,calls=exact_small(S,m,zz,oo)
    if w is None:
        return ('NO' if levels==0 else 'OPEN'),None,{'base_nodes':calls}
    F=set(face_list);W={face_list[j] for j in w};j=b
    for _ in range(levels):
        W=lift(F,W);j*=13
        if j!=k:F=faces_of(j)
    try:ans=sorted(ids[f] for f in W)
    except KeyError:raise AssertionError('invalid patch lift')
    assert verify(T,n,ans)
    if set(ans)&set(zero) or not set(one)<=set(ans):return 'OPEN',None,{'reason':'guard not satisfied','base_nodes':calls}
    return 'YES',ans,{'levels':levels,'base_nodes':calls,'macro_patches':len(verified_patches())}

if __name__=='__main__':
    out=[]
    for k in (1,4,5,13,52,65,169):
        T,n,_=make(k,True)
        # Relabel every color and tuple order; solver has no geometric metadata.
        r=random.Random(26112602+k);P=[list(range(n)) for _ in range(3)]
        for a in P:r.shuffle(a)
        T=[tuple(P[c][v] for c,v in enumerate(t)) for t in T];r.shuffle(T)
        s,w,stats=solve(T,n);assert s=='YES';print(k,len(T),s,stats,flush=True)
        out.append(dict(k=k,n=n,triples=len(T),status=s,stats=stats,witness=w))
        json.dump(out,open('refinement_results.json','w'))
    json.dump({str(k):v for k,v in verified_patches().items()},open('patch_certificates.json','w'))
