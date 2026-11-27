#!/usr/bin/env python3
"""Grok work 2026-11-28 KST: (A) exact zero-overlap (d=0) merge of two full-or-one-hole cosets;
(B) iterated merge of full-or-one-hole factors is NP-complete: verified reduction from
positive 1-in-3-SAT to MULTI-CHOICE-F2-SUM with 3-element factors (= dim-2 coset minus one hole).
Vectors in F2^r are Python ints (bitmasks). Seeded, deterministic."""
import itertools, random, json, time
rng = random.Random(20261128)
def span(gens):
    S={0}
    for g in gens: S|={s^g for s in S}
    return S
def rand_subspace(r, k):
    while True:
        g=[rng.randrange(1,1<<r) for _ in range(k)]
        S=span(g)
        if len(S)==1<<k: return S
def sumset(A,B): return {a^b for a in A for b in B}
res={}
# ---- (A) zero-overlap exact decomposition, and the fiber count formula (all d) ----
t0=time.time(); checks=0; d0_checks=0
for trial in range(3000):
    r=rng.randint(2,6); kp=rng.randint(0,min(3,r)); kq=rng.randint(0,min(3,r))
    P=rand_subspace(r,kp); Q=rand_subspace(r,kq)
    a=rng.randrange(1<<r); b=rng.randrange(1<<r)
    CA={a^p for p in P}; CB={b^q for q in Q}
    u=rng.choice(sorted(CA)) if rng.random()<0.8 else None
    v=rng.choice(sorted(CB)) if rng.random()<0.8 else None
    A=CA-{u}; B=CB-{v}
    d=len(P&Q).bit_length()-1
    PQ=sumset(P,Q); amb={a^b^w for w in PQ}
    for t in amb:
        M=sum(1 for x in A if (t^x) in B)
        al=int(u is not None and (t^u) in CB); be=int(v is not None and (t^v) in CA)
        ga=int(u is not None and v is not None and t==u^v)
        assert M==2**d-al-be+ga; checks+=1
    S=sumset(A,B)
    if d==0 and A and B:
        # exact descriptor: amb minus [(u+b+Q) U (a+P+v)] (terms present only if the hole exists)
        rem=set()
        if u is not None: rem|={u^y for y in CB}
        if v is not None: rem|={x^v for x in CA}
        assert S==amb-rem, (P,Q,a,b,u,v)
        if u is not None and v is not None:
            assert len(rem)==len(Q)+len(P)-1  # two cosets meeting exactly at u+v
        d0_checks+=1
    if d>=1:
        miss=amb-S
        assert len(miss)<=(1 if d==1 else 0)
res['A_fiber_formula_target_checks']=checks
res['A_zero_overlap_descriptor_checks']=d0_checks
res['A_seconds']=round(time.time()-t0,2)
# ---- (B) reduction positive 1-in-3-SAT -> multi-choice F2 sum ----
def reduce_1in3(nvars, clauses):
    """clauses: list of 3-tuples of distinct variables. Duplicate every clause so every used
    variable occurs >=2 times. Rows: for each variable, consecutive occurrence pairs (chain).
    Factor per clause copy: three vectors w_j = sum of rows incident to occurrence (c,j). Target 0."""
    cl=[c for c in clauses for _ in (0,1)]
    occ={}
    for ci,c in enumerate(cl):
        for j,x in enumerate(c): occ.setdefault(x,[]).append((ci,j))
    rowof={}; nrows=0; inc={}
    for x,os in occ.items():
        for o1,o2 in zip(os,os[1:]):
            inc.setdefault(o1,0); inc.setdefault(o2,0)
            inc[o1]|=1<<nrows; inc[o2]|=1<<nrows; nrows+=1
    factors=[[inc[(ci,j)] for j in range(3)] for ci in range(len(cl))]
    return factors, nrows, 0
def brute_1in3(nvars, clauses):
    for z in itertools.product((0,1),repeat=nvars):
        if all(z[a]+z[b]+z[c]==1 for a,b,c in clauses): return True
    return False
def brute_choice(factors, t):
    # meet-in-the-middle over choices
    h=len(factors)//2
    L={}
    for ch in itertools.product(range(3),repeat=h):
        s=0
        for f,c in zip(factors[:h],ch): s^=f[c]
        L[s]=1
    for ch in itertools.product(range(3),repeat=len(factors)-h):
        s=t
        for f,c in zip(factors[h:],ch): s^=f[c]
        if s in L: return True
    return False
t0=time.time(); agree=0; sat=0; distinct_ok=0; inst=0; nontrivial_merges=0
for trial in range(400):
    n=rng.randint(3,6); m=rng.randint(1,8)
    clauses=[tuple(rng.sample(range(n),3)) for _ in range(m)]
    F,nr,t=reduce_1in3(n,clauses)
    assert all(len(set(f))==3 for f in F)  # each factor = dim-2 coset minus hole f0^f1^f2
    distinct_ok+=1
    a=brute_1in3(n,clauses); b=brute_choice(F,t)
    assert a==b, (n,clauses)
    agree+=1; sat+=a; inst+=1
res['B_instances']=inst; res['B_agree']=agree; res['B_satisfiable']=sat
res['B_factors_are_3_distinct_points']=distinct_ok
res['B_seconds']=round(time.time()-t0,2)
# ---- (C) illustrate where the two-factor closure stops: left-to-right cumulative merge class ----
def is_full_or_one_hole(S, r):
    if not S: return False
    s0=next(iter(S)); W={s^s0 for s in S}
    # smallest affine hull
    basis=[]; 
    for w in W:
        x=w
        for bvec in basis: x=min(x,x^bvec)
        if x: basis.append(x)
    hull={s0^w for w in span(basis)}
    return len(hull)-len(S)<=1
out_cls=[]
for trial in range(200):
    n=rng.randint(4,7); m=rng.randint(2,5)
    clauses=[tuple(rng.sample(range(n),3)) for _ in range(m)]
    F,nr,t=reduce_1in3(n,clauses)
    S={0}; first_exit=None
    for i,f in enumerate(F):
        S=sumset(S,set(f))
        if not is_full_or_one_hole(S,nr) and first_exit is None: first_exit=i
    out_cls.append(first_exit)
res['C_cumulative_leaves_class_fraction']=sum(1 for x in out_cls if x is not None)/len(out_cls)
print(json.dumps(res,indent=1))
