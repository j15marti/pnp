#!/usr/bin/env python3
"""Exact worst-case minimum DAG-resolution refutation cost over ALL UNSAT CNFs on n variables.

R = ordinary DAG resolution: sources free, each DISTINCT derived non-tautological clause costs 1,
no weakening.  Wbar(n) = max over UNSAT F on variables {1..n} of min refutation cost.
Lemma A (monotonicity): F subset G => W(G) <= W(F); hence the max is attained on minimally
unsatisfiable (MU) F.  Lemma B (subsumption normalization): some minimum refutation never derives
a clause subsumed by an available clause.  Both are proved in the accompanying report.

Clause encoding: pair (P,Nn) of bitmasks, P&Nn==0.  Usage: wbar_exact.py n [chunk k of K]
"""
import sys, json, itertools, time

def clauses(n):
    out=[]
    for signs in itertools.product((0,1,2),repeat=n):
        P=sum(1<<i for i,s in enumerate(signs) if s==1)
        N=sum(1<<i for i,s in enumerate(signs) if s==2)
        out.append((P,N))
    return out

def falsified(c,n):
    P,N=c; m=0
    for a in range(1<<n):
        if (a&P)==0 and (a&N)==N: m|=1<<a
    return m

def subsumes(d,c): return (d[0]&~c[0])==0 and (d[1]&~c[1])==0

def resolvents(c,d):
    out=[]
    for piv in (c[0]&d[1], c[1]&d[0]):
        b=piv
        while b:
            x=b&-b; b^=x
            P=(c[0]|d[0])&~x; N=(c[1]|d[1])&~x
            if P&N==0: out.append((P,N))
    return out

def enum_mu(n):
    cl=[c for c in clauses(n) if c!=(0,0)]
    cov=[falsified(c,n) for c in cl]; full=(1<<(1<<n))-1
    res=[]
    # minimal covers: DFS choosing clause covering the lowest uncovered point
    def dfs(chosen,covered):
        if covered==full:
            # minimality: each chosen clause has a private point
            for i in chosen:
                rest=0
                for j in chosen:
                    if j!=i: rest|=cov[j]
                if rest==full: return
            res.append(tuple(sorted(chosen))); return
        low=(~covered)&(covered+1)  # lowest uncovered bit
        for i,cv in enumerate(cov):
            if cv&low and i not in chosen:
                # canonical: only allow i if no chosen clause j>i... use set dedup instead
                dfs(chosen+[i],covered|cv)
    dfs([],0)
    uniq=sorted(set(res))
    return cl,[[cl[i] for i in f] for f in uniq]

def perms_signs(n):
    G=[]
    for perm in itertools.permutations(range(n)):
        for flip in range(1<<n):
            G.append((perm,flip))
    return G

def act(g,c):
    perm,flip=g; P,N=c; P2=N2=0
    for i in range(len(perm)):
        b=1<<i; t=1<<perm[i]
        pos=bool(P&b); neg=bool(N&b)
        if flip&b: pos,neg=neg,pos
        if pos: P2|=t
        if neg: N2|=t
    return (P2,N2)

def canon(F,G):
    return min(tuple(sorted(act(g,c) for c in F)) for g in G)

def min_refutation(F, cap=64, prune=True):
    """Exact min number of distinct derived clauses.  BFS over sets S of derived clauses, by |S|.
    prune=True applies Lemma B (skip resolvents subsumed by an available clause)."""
    src=frozenset(F)
    if (0,0) in src: return 0,[]
    frontier=[frozenset()]; parent={frozenset():None}
    for k in range(1,cap+1):
        nxt=[]
        for S in frontier:
            K=list(src|S); seen=set()
            for a,b in itertools.combinations(K,2):
                for r in resolvents(a,b):
                    if r in seen or r in src or r in S: continue
                    seen.add(r)
                    if prune and any(subsumes(d,r) for d in K): continue
                    T=S|{r}
                    if T in parent: continue
                    parent[T]=(S,a,b,r)
                    if r==(0,0):
                        steps=[]; cur=T
                        while parent[cur] is not None:
                            P,a_,b_,r_=parent[cur]; steps.append([list(a_),list(b_),list(r_)]); cur=P
                        return k,steps[::-1]
                    nxt.append(T)
        frontier=nxt
        if not frontier: return None,None
    return None,None

if __name__=="__main__":
    n=int(sys.argv[1]); ck=int(sys.argv[2]) if len(sys.argv)>2 else 0; K=int(sys.argv[3]) if len(sys.argv)>3 else 1
    t=time.time()
    cl,mus=enum_mu(n)
    G=perms_signs(n)
    classes={}
    for F in mus: classes.setdefault(canon(F,G),0); classes[canon(F,G)]+=1
    reps=sorted(classes)
    mine=[r for i,r in enumerate(reps) if i%K==ck]
    rows=[]
    for r in mine:
        w,pf=min_refutation(list(r))
        rows.append({"F":[list(c) for c in r],"m":len(r),"orbit":classes[r],"W":w,"proof":pf})
    out={"n":n,"chunk":[ck,K],"num_MU":len(mus),"num_classes":len(reps),"rows":rows,"secs":round(time.time()-t,2)}
    json.dump(out,open(f"wbar_n{n}_chunk{ck}of{K}.json","w"))
    print(n,ck,K,"MU",len(mus),"classes",len(reps),"maxW",max(r["W"] for r in rows),"secs",out["secs"])
