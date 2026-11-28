# Finite sanity checks for the Res+GE_in restriction lemma (Grok 2026-11-28 1956 KST).
import itertools, random
random.seed(20261128)
def php(n):
    V={(i,j):1+i*n+j for i in range(n+1) for j in range(n)}
    C=[frozenset(V[i,j] for j in range(n)) for i in range(n+1)]
    for j in range(n):
        for a,b in itertools.combinations(range(n+1),2): C.append(frozenset((-V[a,j],-V[b,j])))
    return V,C
def xors(C,maxk=6):
    # CryptoMiniSat-style syntactic XOR detection: all 2^{k-1} sign patterns of one parity present
    by={}
    for c in C:
        if 2<=len(c)<=maxk: by.setdefault(frozenset(abs(l) for l in c),set()).add(c)
    found=0
    for vs,cl in by.items():
        k=len(vs); vs=sorted(vs)
        for rhs in (0,1):
            need={frozenset(v if ((s>>t)&1)==0 else -v for t,v in enumerate(vs))
                  for s in range(2**k) if bin(s).count('1')%2!=rhs}
            if need<=cl: found+=1
    return found
print("(a) syntactic XORs (arity 2..6) in PHP_n^{n+1}:",{n:xors(php(n)[1]) for n in range(2,7)})
# (b) key step: rho satisfying L satisfies every clause implied by L (exhaustive, small)
def implied_ok(nv,L,trials=300):
    sols=[a for a in itertools.product((0,1),repeat=nv) if all(sum(a[v] for v in eq)%2==r for eq,r in L)]
    if not sols: return None
    bad=0
    for _ in range(trials):
        w=random.randint(1,nv); vs=random.sample(range(nv),w); sg=[random.randint(0,1) for _ in vs]
        imp=all(any(a[v]==s for v,s in zip(vs,sg)) for a in sols)
        if imp:
            Lv={v for eq,_ in L for v in eq}
            for a in sols:   # rho = a restricted to vars(L); check C satisfied on vars(L) part
                if not any(v in Lv and a[v]==s for v,s in zip(vs,sg)): bad+=1
    return bad
tot=0
for t in range(200):
    nv=7; Lvars=random.sample(range(nv),4)
    L=[(random.sample(Lvars,random.randint(1,4)),random.randint(0,1)) for _ in range(2)]
    r=implied_ok(nv,L); tot+= (r or 0)
print("(b) violations of 'rho |= L implies rho satisfies every L-implied clause':",tot)
# (c) Corollary construction: homogeneous L on Z (|Z|=k<=n/2) -> PHP_{n-k'}^{n+1-k'} after restriction
def construct(n,k):
    V,C=php(n); allv=list(V)
    Z=random.sample(allv,k); rho={V[z]:0 for z in Z}
    I0=sorted({i for i,_ in Z}); used=set()
    for i in I0:
        j=next(j for j in range(n) if j not in used and (i,j) not in Z); used.add(j)
        rho[V[i,j]]=1
        for jj in range(n):
            if jj!=j: rho.setdefault(V[i,jj],0)
        for ii in range(n+1):
            if ii!=i: rho[V[ii,j]]=0
    R=[]
    for c in C:
        if any((l>0 and rho.get(l)==1) or (l<0 and rho.get(-l)==0) for l in c): continue
        R.append(frozenset(l for l in c if abs(l) not in rho))
    m=n-len(I0); _,P=php(m)
    shape=lambda F: sorted(sorted(len(c) for c in F))
    ok = (frozenset() not in R) and shape(R)==shape(P) and len(R)==len(P)
    return ok,len(I0)
res=[construct(n,k) for n in (6,8,10) for k in range(1,n//2+1) for _ in range(20)]
print("(c) restricted formula is an exact PHP_{n-|I0|}^{n+1-|I0|} copy (clause-shape check):",
      sum(o for o,_ in res),"/",len(res))
