#!/usr/bin/env python3
"""
RESOLVE-MATCH1.

Exact finite catalog + synthetic adversarial tests for the RESOLVE-MATCH rule.

Part A:
  Enumerate all same-pair degree-2 mediator resolvents on two type-1 chains.
  There are 36 pair terms per mediator side and 324 distinct non-tautological
  relation schemas. Solve Liu's characteristic system exactly over Q.

Part B:
  Generate synthetic low-degree clean-core mediator patterns:
    pair_rich -- both sides use the same chain pair
    star      -- pair-resolvents all concentrate through one chain
    spread4   -- positive/negative pair terms use four distinct chains
    triple    -- positive/negative pair terms span exactly three chains
    random    -- independent random pair terms
  Build the exposed pair graph, combine all constraints per pair, compute
  characteristic gains, and choose a maximum-weight matching.

The experiment is a finite structural diagnostic, not a general 3-SAT bound.
"""

import collections, itertools, json, math, random
from fractions import Fraction

import networkx as nx
import numpy as np

D=[s for s in itertools.product([0,1],repeat=3) if any(s)]
L1=Fraction(3,7)
LIND=L1*L1

def litv(st,i,neg):
    v=st[i]
    return 1-v if neg else v

def solve_q(A,b):
    n=len(A)
    M=[list(map(Fraction,row))+[Fraction(b[i])] for i,row in enumerate(A)]
    for col in range(n):
        p=next(i for i in range(col,n) if M[i][col])
        M[col],M[p]=M[p],M[col]
        q=M[col][col]
        M[col]=[x/q for x in M[col]]
        for i in range(n):
            if i==col:continue
            q=M[i][col]
            if q:
                M[i]=[M[i][j]-q*M[col][j] for j in range(n+1)]
    return [M[i][-1] for i in range(n)]

def characteristic_exact(allowed):
    states=[D[a]+D[b] for a,b in allowed]
    M=[]
    for star in states:
        row=[]
        for a in states:
            d=sum(x!=y for x,y in zip(a,star))
            row.append(Fraction(1,2**d))
        M.append(row)
    q=solve_q(M,[1]*len(M))
    lam=Fraction(1,1)/sum(q)
    pi=[lam*x for x in q]
    assert min(pi)>=0
    return lam

def relation(clauses):
    out=[]
    for a,b in itertools.product(range(7),repeat=2):
        ass=[D[a],D[b]]
        if all(any(litv(ass[s],i,n) for s,i,n in C) for C in clauses):
            out.append((a,b))
    return out

def normalize(lits):
    s=set(lits)
    for c,i,n in tuple(s):
        if (c,i,not n) in s:return None
    return tuple(sorted(s))

def pair_catalog():
    terms=[]
    for i,j in itertools.product(range(3),repeat=2):
        for ni,nj in itertools.product([False,True],repeat=2):
            terms.append(((0,i,ni),(1,j,nj)))
    seen={}
    for A in terms:
        for B in terms:
            C=normalize(A+B)
            if C is None:continue
            R=relation([C])
            mask=sum(1<<(7*a+b) for a,b in R)
            if mask not in seen:
                seen[mask]=(C,characteristic_exact(R),len(R))
    hist=collections.Counter(lam for _,lam,_ in seen.values())
    return seen,hist

def rand_lit(c,rng):
    return (c,rng.randrange(3),bool(rng.randrange(2)))

def pair_term(pair,rng):
    a,b=pair
    return (rand_lit(a,rng),rand_lit(b,rng))

def gen_pattern(k,m,kind,seed):
    rng=random.Random(seed);M=[]
    for t in range(m):
        if kind=="pair_rich":
            p=tuple(rng.sample(range(k),2));q=p
        elif kind=="star":
            p=(0,1+t%(k-1));q=p
        elif kind=="spread4":
            a,b,c,d=rng.sample(range(k),4);p=(a,b);q=(c,d)
        elif kind=="triple":
            a,b,c=rng.sample(range(k),3);p=(a,b);q=(a,c)
        elif kind=="random":
            p=tuple(rng.sample(range(k),2));q=tuple(rng.sample(range(k),2))
        else:
            raise ValueError(kind)
        M.append((pair_term(p,rng),pair_term(q,rng)))
    return M

def float_characteristic(allowed):
    states=[D[a]+D[b] for a,b in allowed]
    n=len(states)
    M=np.empty((n,n))
    for i,star in enumerate(states):
        for j,a in enumerate(states):
            d=sum(x!=y for x,y in zip(a,star))
            M[i,j]=2.0**(-d)
    q=np.linalg.solve(M,np.ones(n))
    lam=1.0/q.sum()
    if (lam*q).min() < -1e-8:return None
    return lam

def resolve_match(k,mediators):
    pairs=collections.defaultdict(list)
    for A,B in mediators:
        C=normalize(A+B)
        if C is None:continue
        chains=sorted({c for c,_,_ in C})
        if len(chains)!=2:continue
        x,y=chains
        local=tuple((0 if c==x else 1,i,n) for c,i,n in C)
        pairs[(x,y)].append(local)

    G=nx.Graph();G.add_nodes_from(range(k))
    for (x,y),Cs in pairs.items():
        R=relation(Cs)
        lam=float_characteristic(R)
        if lam is None:continue
        gain=math.log(lam/float(LIND))
        if gain>1e-12:
            G.add_edge(x,y,weight=gain,lam=lam)

    mat=nx.max_weight_matching(G,weight="weight")
    gain=sum(G[u][v]["weight"] for u,v in mat)
    return {
        "pair_edges":G.number_of_edges(),
        "matched_pairs":len(mat),
        "coverage":2*len(mat)/k,
        "relative_dls_factor":math.exp(-gain),
    }

def main():
    catalog,hist=pair_catalog()
    lo=min(hist);hi=max(hist)

    patterns={}
    for kind in ["pair_rich","star","spread4","triple","random"]:
        rows=[]
        for seed in range(30):
            rows.append(resolve_match(12,gen_pattern(12,24,kind,20261005+seed)))
        patterns[kind]={
            "mean_pair_edges":sum(r["pair_edges"] for r in rows)/len(rows),
            "mean_coverage":sum(r["coverage"] for r in rows)/len(rows),
            "min_coverage":min(r["coverage"] for r in rows),
            "max_coverage":max(r["coverage"] for r in rows),
            "mean_relative_dls_factor":sum(r["relative_dls_factor"] for r in rows)/len(rows),
        }

    out={
      "distinct_same_pair_resolvent_relations":len(catalog),
      "distinct_characteristic_values":len(hist),
      "minimum_lambda":str(lo),
      "maximum_lambda":str(hi),
      "independent_pair_lambda":str(LIND),
      "minimum_gain_factor_independent_over_pair":str(LIND/lo),
      "lambda_histogram":{str(k):v for k,v in sorted(hist.items())},
      "synthetic_k":12,
      "synthetic_mediators":24,
      "seeds_per_pattern":30,
      "patterns":patterns
    }
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
