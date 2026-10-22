"""Independent re-check of UNIVERSAL-SHIFT29 Theorems 29A/29B (small parameters). Runtime ~ seconds."""
import itertools, random
MOD=0x11B
def mul(a,b):
    r=0
    while b:
        if b&1:r^=a
        a<<=1
        if a&0x100:a^=MOD
        b>>=1
    return r
def tr(x):
    t=0;y=x
    for _ in range(8):
        t^=y;y=mul(y,y)
    assert t in(0,1);return t
def powr(z,i):
    r=1
    for _ in range(i):r=mul(r,z)
    return r
TR=[tr(x) for x in range(256)]
def universal_set(m):
    pw=[[powr(z,i) for i in range(m)] for z in range(256)]
    return {tuple(TR[mul(a,pw[z][i])] for i in range(m)) for a in range(256) for z in range(256)}
def check_universal(m,k):
    A=universal_set(m); bad=0
    for B in itertools.combinations(range(m),k):
        seen={tuple(r[b] for b in B) for r in A}
        if len(seen)<2**k:bad+=1
    return len(A),bad
def hit_test(m,k,d,trials,seed):
    rnd=random.Random(seed); A=universal_set(m)
    H=[t for w in range(d+1) for c in itertools.combinations(range(m),w) for t in [sum(1<<i for i in c)]]
    L={sum(b<<i for i,b in enumerate(a))^t for a in A for t in H}
    fails=0
    for _ in range(trials):
        B=rnd.sample(range(m),k); rest=[i for i in range(m) if i not in B]
        # f nonzero; for each B-assignment c, restricted slice is a random degree<=d poly in rest vars (ANF), at least one slice nonzero
        slices={}
        for c in range(2**k):
            mons=[frozenset(s) for w in range(d+1) for s in itertools.combinations(rest,w) if rnd.random()<0.3]
            slices[c]=mons
        if not any(slices.values()):slices[rnd.randrange(2**k)]=[frozenset(rnd.sample(rest,d))]
        def f(x):
            c=sum(((x>>b)&1)<<j for j,b in enumerate(B))
            return sum(all((x>>i)&1 for i in mn) for mn in slices[c])&1
        if not any(f(x) for x in L):
            # genuinely nonzero? (ANF mod 2 could cancel only identical monomials; mons distinct so nonzero iff list nonempty)
            if any(slices.values()):fails+=1
    return len(L),2**m,fails
for m,k in((8,3),):
    print("universal m,k",m,k,check_universal(m,k))
for m,k,d in((24,2,1),(26,2,1)):
    print("hit m,k,d",m,k,d,hit_test(m,k,d,15,1))
