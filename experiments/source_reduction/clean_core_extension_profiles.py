#!/usr/bin/env python3
"""
CLEANCORE-EXT1.

Finite exact diagnostics for the partial-extension map of mediator-eliminated
7-state type-1-chain CSPs.

Families:
  clean    -- random low-degree externally mediated clean cores, then exact mediator elimination
  2sat     -- random 2-CNF control on one representative bit per chain
  path     -- bounded-pathwidth 2-CNF control
  indprod  -- independent-pair product control
  xor      -- affine/XOR control, evaluated by canonical GF(2) elimination

Metrics:
  exact primal treewidth (k <= 7)
  exact vertex-separation/pathwidth
  balanced edge expansion
  reduced ordered 8-ary MDD size/width for EXT_F(rho), where each challenge
    coordinate is either '*' or one of the seven chain states
  maximum balanced-cut partial-extension communication distinct-row count
    and GF(2) rank for k <= 6

These are finite representation diagnostics, not unrestricted SAT lower bounds.
"""

import argparse, collections, csv, itertools, math, random, statistics
from functools import lru_cache
import networkx as nx

STATES=[b for b in itertools.product([0,1], repeat=3) if any(b)]
FALSE=(("FALSE",),)

def litv(s,i,neg=False):
    v=s[i]
    return 1-v if neg else v

def norm_clause(lits):
    z=set(lits)
    for c,i,n in tuple(z):
        if (c,i,not n) in z:
            return None
    return tuple(sorted(z))

def simplify(clauses):
    out=[]
    for c in clauses:
        if c==(): return FALSE
        out.append(tuple(sorted(set(c))))
    uniq=sorted(set(out),key=lambda x:(len(x),x))
    kept=[]; sets=[]
    for c in uniq:
        sc=set(c)
        if any(k.issubset(sc) for k in sets): continue
        kept.append(c); sets.append(sc)
    return tuple(kept)

def restrict(cnf,ch,state):
    if cnf==FALSE:return FALSE
    out=[]
    for cl in cnf:
        sat=False; rem=[]
        for c,i,n in cl:
            if c==ch:
                if litv(state,i,n): sat=True; break
            else: rem.append((c,i,n))
        if sat: continue
        if not rem:return FALSE
        out.append(tuple(rem))
    return simplify(out)

def term_lits(t):
    a,i,na,b,j,nb=t
    return [(a,i,na),(b,j,nb)]

def pair_term(k,rng):
    a,b=rng.sample(range(k),2)
    return (a,rng.randrange(3),bool(rng.randrange(2)),
            b,rng.randrange(3),bool(rng.randrange(2)))

def clean_core(k,seed):
    rng=random.Random(seed); meds=[]
    for _ in range(2*k):
        d=rng.randint(2,4); p=rng.randint(1,d-1)
        P=[pair_term(k,rng) for _ in range(p)]
        N=[pair_term(k,rng) for _ in range(d-p)]
        meds.append((P,N))
    clauses=[]
    for P,N in meds:
        for a in P:
            for b in N:
                c=norm_clause(term_lits(a)+term_lits(b))
                if c is not None: clauses.append(c)
    return simplify(clauses)

def control_2sat(k,seed):
    rng=random.Random(seed); cs=[]
    for _ in range(2*k):
        a,b=rng.sample(range(k),2)
        cs.append(((a,0,bool(rng.randrange(2))),(b,0,bool(rng.randrange(2)))))
    return simplify(cs)

def control_path(k,seed):
    rng=random.Random(seed); cs=[]
    for a in range(k-1):
        for _ in range(2):
            cs.append(((a,0,bool(rng.randrange(2))),
                       (a+1,0,bool(rng.randrange(2)))))
    return simplify(cs)

def control_indprod(k,seed):
    rng=random.Random(seed); cs=[]
    for a in range(0,k-1,2):
        cs.append(((a,0,bool(rng.randrange(2))),
                   (a+1,0,bool(rng.randrange(2)))))
    return simplify(cs)

def xor_instance(k,seed):
    rng=random.Random(seed); eq=[]
    for _ in range(max(1,k//2)):
        q=rng.randint(2,min(4,k))
        eq.append((tuple(sorted(rng.sample(range(k),q))),rng.randrange(2)))
    return tuple(eq)

def make_sat():
    @lru_cache(None)
    def sat(f):
        if f==FALSE:return False
        if not f:return True
        vs=tuple(sorted({c for cl in f for c,_,_ in cl}))
        if not vs:return False
        cnt=collections.Counter(c for cl in f for c,_,_ in cl)
        ch=max(vs,key=lambda c:cnt[c])
        return any(sat(restrict(f,ch,s)) for s in STATES)
    return sat

def generate(kind,k,seed):
    if kind=="xor":
        off=0
        while True:
            e=xor_instance(k,seed+10000*off)
            if xor_rref(e,k)!=("INC",):return ("xor",e)
            off+=1
    maker={"clean":clean_core,"2sat":control_2sat,
           "path":control_path,"indprod":control_indprod}[kind]
    off=0
    while True:
        f=maker(k,seed+10000*off)
        if f and f!=FALSE and make_sat()(f):return ("cnf",f)
        off+=1

def graph_cnf(f,k):
    G=nx.Graph();G.add_nodes_from(range(k))
    for cl in f:
        vs=sorted({c for c,_,_ in cl})
        for a,b in itertools.combinations(vs,2):G.add_edge(a,b)
    return G

def graph_xor(eq,k):
    G=nx.Graph();G.add_nodes_from(range(k))
    for vs,_ in eq:
        for a,b in itertools.combinations(vs,2):G.add_edge(a,b)
    return G

def treewidth_exact(G):
    ns=tuple(G.nodes());best=len(ns)
    for order in itertools.permutations(ns):
        H={v:set(G.neighbors(v)) for v in ns};w=0
        for v in order:
            nb=H[v];w=max(w,len(nb))
            if w>=best:break
            for a,b in itertools.combinations(nb,2):
                H[a].add(b);H[b].add(a)
            for a in tuple(nb):H[a].discard(v)
            del H[v]
        else:best=min(best,w)
    return best

def pathwidth_exact(G):
    ns=tuple(G.nodes());n=len(ns);idx={v:i for i,v in enumerate(ns)}
    adj=[]
    for v in ns:
        m=0
        for w in G.neighbors(v):m|=1<<idx[w]
        adj.append(m)
    N=1<<n;full=N-1;sep=[0]*N
    for S in range(N):
        out=full^S
        sep[S]=sum(1 for i in range(n) if (S>>i)&1 and adj[i]&out)
    dp=[n+1]*N;dp[0]=0
    for S in range(1,N):
        m=S;v=n+1
        while m:
            b=m&-m;prev=S^b
            v=min(v,max(dp[prev],sep[S]))
            m-=b
        dp[S]=v
    return dp[-1]

def balanced_expansion(G):
    ns=list(G.nodes());n=len(ns);q=n//2;best=float("inf")
    for C in itertools.combinations(ns,q):
        S=set(C);cut=sum(1 for a,b in G.edges() if (a in S)!=(b in S))
        best=min(best,cut/min(len(S),n-len(S)))
    return best

def ext_mdd_cnf(f,k,order):
    sat=make_sat();uniq={};memo={};nxt=[2];width=collections.Counter()
    def rec(d,g):
        if d==k:return 1 if sat(g) else 0
        key=(d,g)
        if key in memo:return memo[key]
        ch=order[d]
        kids=[rec(d+1,g)]+[rec(d+1,restrict(g,ch,s)) for s in STATES]
        kids=tuple(kids)
        if len(set(kids))==1:memo[key]=kids[0];return kids[0]
        u=(d,kids)
        if u not in uniq:
            uniq[u]=nxt[0];nxt[0]+=1;width[d]+=1
        memo[key]=uniq[u];return memo[key]
    rec(0,f)
    return nxt[0]-2,max(width.values(),default=0)

def best_mdd_cnf(f,k,seed,samples):
    rng=random.Random(seed);deg=[0]*k
    for cl in f:
        for c,_,_ in cl:deg[c]+=1
    orders=[tuple(range(k)),tuple(sorted(range(k),key=lambda c:deg[c])),
            tuple(sorted(range(k),key=lambda c:-deg[c]))]
    seen=set(orders)
    while len(orders)<min(samples,math.factorial(k)):
        o=list(range(k));rng.shuffle(o);o=tuple(o)
        if o not in seen:seen.add(o);orders.append(o)
    vals=[(*ext_mdd_cnf(f,k,o),o) for o in orders]
    vals.sort()
    return vals[0],statistics.median(v[0] for v in vals)

def xor_rref(eq,k):
    A=[]
    for vs,b in eq:
        m=0
        for v in vs:m^=1<<v
        A.append([m,b])
    r=0
    for col in range(k):
        p=next((i for i in range(r,len(A)) if (A[i][0]>>col)&1),None)
        if p is None:continue
        A[r],A[p]=A[p],A[r];pm,pb=A[r]
        for i in range(len(A)):
            if i!=r and ((A[i][0]>>col)&1):
                A[i][0]^=pm;A[i][1]^=pb
        r+=1
    if any(m==0 and b for m,b in A):return ("INC",)
    return tuple(sorted((m,b) for m,b in A if m))

def xor_restrict(st,v,val,k):
    if st==("INC",):return st
    return xor_rref(tuple((tuple(i for i in range(k) if (m>>i)&1),
                           b^(val if (m>>v)&1 else 0))
                          for m,b in st if not ((m>>v)&1 and (m^(1<<v))==0 and (b^val)==0)
                         ),k) if False else _xor_restrict(st,v,val,k)

def _xor_restrict(st,v,val,k):
    if st==("INC",):return st
    rows=[]
    for m,b in st:
        if (m>>v)&1:m^=1<<v;b^=val
        rows.append((m,b))
    # canonicalize raw mask rows
    A=[[m,b] for m,b in rows];r=0
    for col in range(k):
        p=next((i for i in range(r,len(A)) if (A[i][0]>>col)&1),None)
        if p is None:continue
        A[r],A[p]=A[p],A[r];pm,pb=A[r]
        for i in range(len(A)):
            if i!=r and ((A[i][0]>>col)&1):
                A[i][0]^=pm;A[i][1]^=pb
        r+=1
    if any(m==0 and b for m,b in A):return ("INC",)
    return tuple(sorted((m,b) for m,b in A if m))

def ext_mdd_xor(eq,k,order):
    st=xor_rref(eq,k);uniq={};memo={};nxt=[2];width=collections.Counter()
    def rec(d,g):
        if g==("INC",):return 0
        if d==k:return 1
        key=(d,g)
        if key in memo:return memo[key]
        v=order[d]
        kids=[rec(d+1,g)]+[rec(d+1,_xor_restrict(g,v,s[0],k)) for s in STATES]
        kids=tuple(kids)
        if len(set(kids))==1:memo[key]=kids[0];return kids[0]
        u=(d,kids)
        if u not in uniq:uniq[u]=nxt[0];nxt[0]+=1;width[d]+=1
        memo[key]=uniq[u];return memo[key]
    rec(0,st)
    return nxt[0]-2,max(width.values(),default=0)

def best_mdd_xor(eq,k,seed,samples):
    rng=random.Random(seed);G=graph_xor(eq,k);deg=dict(G.degree())
    orders=[tuple(range(k)),tuple(sorted(range(k),key=lambda c:deg[c])),
            tuple(sorted(range(k),key=lambda c:-deg[c]))]
    seen=set(orders)
    while len(orders)<min(samples,math.factorial(k)):
        o=list(range(k));rng.shuffle(o);o=tuple(o)
        if o not in seen:seen.add(o);orders.append(o)
    vals=[(*ext_mdd_xor(eq,k,o),o) for o in orders];vals.sort()
    return vals[0],statistics.median(v[0] for v in vals)

def gf2_rank(rows,ncols):
    basis={};rank=0
    for rb in rows:
        x=0
        for i,b in enumerate(rb):
            if b:x|=1<<i
        while x:
            p=x.bit_length()-1
            if p in basis:x^=basis[p]
            else:basis[p]=x;rank+=1;break
    return rank

def partial_residuals(f,vars_):
    arr=[f]
    for v in vars_:
        nxt=[]
        for g in arr:nxt.append(g);nxt.extend(restrict(g,v,s) for s in STATES)
        arr=nxt
    return arr

def comm_cnf(f,k,left):
    left=tuple(left);right=tuple(i for i in range(k) if i not in set(left));sat=make_sat()
    @lru_cache(None)
    def profile(g,d):
        if d==len(right):return bytes([1 if sat(g) else 0])
        v=right[d]
        return b"".join([profile(g,d+1)]+[profile(restrict(g,v,s),d+1) for s in STATES])
    rows=[profile(g,0) for g in partial_residuals(f,left)]
    cols=8**len(right)
    return len(set(rows)),gf2_rank(rows,cols),sum(sum(r) for r in rows)/(len(rows)*cols)

def comm_xor(eq,k,left):
    left=tuple(left);right=tuple(i for i in range(k) if i not in set(left))
    arr=[xor_rref(eq,k)]
    for v in left:
        nxt=[]
        for g in arr:nxt.append(g);nxt.extend(_xor_restrict(g,v,s[0],k) for s in STATES)
        arr=nxt
    @lru_cache(None)
    def profile(g,d):
        if d==len(right):return bytes([0 if g==("INC",) else 1])
        v=right[d]
        return b"".join([profile(g,d+1)]+[profile(_xor_restrict(g,v,s[0],k),d+1) for s in STATES])
    rows=[profile(g,0) for g in arr];cols=8**len(right)
    return len(set(rows)),gf2_rank(rows,cols),sum(sum(r) for r in rows)/(len(rows)*cols)

def max_comm(kind,obj,k):
    a=k//2;cuts=list(itertools.combinations(range(k),a))
    if k%2==0:cuts=[c for c in cuts if 0 in c]
    best=None
    for c in cuts:
        d,rho,den=(comm_xor(obj,k,c) if kind=="xor" else comm_cnf(obj,k,c))
        score=(rho,d)
        if best is None or score>best[0]:best=(score,d,rho,den)
    return best[1:]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default="clean_core_extension_profiles.csv")
    args=ap.parse_args()
    kinds=["clean","2sat","path","indprod","xor"];rows=[]
    for k in range(4,8):
        for seedidx in range(3):
            seed=20261005+1000*k+seedidx
            for kind in kinds:
                typ,obj=generate(kind,k,seed)
                G=graph_xor(obj,k) if typ=="xor" else graph_cnf(obj,k)
                if typ=="xor":best,med=best_mdd_xor(obj,k,seed,10 if k<7 else 6)
                else:best,med=best_mdd_cnf(obj,k,seed,10 if k<7 else 6)
                comm=max_comm(kind,obj,k) if k<=6 else (None,None,None)
                rows.append(dict(kind=kind,k=k,seed=seedidx,desc_size=len(obj),
                    edges=G.number_of_edges(),treewidth=treewidth_exact(G),
                    pathwidth=pathwidth_exact(G),balanced_edge_expansion=balanced_expansion(G),
                    best_ext_mdd_nodes=best[0],best_ext_mdd_width=best[1],
                    median_ext_mdd_nodes=med,comm_distinct_rows=comm[0],
                    comm_gf2_rank=comm[1],comm_density=comm[2]))
    with open(args.out,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)

if __name__=="__main__":
    main()
