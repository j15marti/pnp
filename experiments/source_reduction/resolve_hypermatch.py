#!/usr/bin/env python3
"""
RESOLVE-HYPERMATCH1.

Polynomial greedy weighted hypermatching diagnostic for exact relations exposed
by degree-2 mediator elimination.

Each mediator produces one non-tautological clause supported on 2-4 type-1
chains.  CLAUSECHAR1 gives its exact characteristic lambda.  Edge weight is
log(lambda / (3/7)^rank).  Edges are processed by decreasing weight, selecting
a disjoint block whenever possible.

This is an implementable maximal hypermatching, not an NP-hard maximum
weighted set-packing computation.

Synthetic patterns:
  pair_rich, star, spread4, triple, random.

The experiment demonstrates:
  * rank-<=4 credit closes pair-only SPREAD4/TRIPLE loss on typical samples;
  * concentration through one chain still destroys constant-fraction coverage.
"""

import collections, itertools, json, math, random
from fractions import Fraction

D=[s for s in itertools.product([0,1],repeat=3) if any(s)]
L1=Fraction(3,7)
T=Fraction(7,3)

# Local a(B) values for all possible falsifying patterns on one type-1 chain.
# Compute directly from the exact local kernel.

def inv_frac(M):
    n=len(M)
    A=[list(row)+[Fraction(int(i==j)) for j in range(n)] for i,row in enumerate(M)]
    for c in range(n):
        p=next(i for i in range(c,n) if A[i][c])
        A[c],A[p]=A[p],A[c]
        q=A[c][c]; A[c]=[x/q for x in A[c]]
        for i in range(n):
            if i==c:continue
            q=A[i][c]
            if q:A[i]=[A[i][j]-q*A[c][j] for j in range(2*n)]
    return [row[n:] for row in A]

K=[[Fraction(1,2**sum(x!=y for x,y in zip(a,b))) for b in D] for a in D]
N=inv_frac(K)
z=[sum(row) for row in N]

def forbidden(lits):
    I=[]
    for i,s in enumerate(D):
        if all(((1-s[c]) if neg else s[c])==0 for c,neg in lits):
            I.append(i)
    return I

def sub(M,I):return [[M[i][j] for j in I] for i in I]

def a_of(lits):
    I=forbidden(lits)
    if not I:return Fraction(0,1)
    NB=sub(N,I); Z=[z[i] for i in I]; R=inv_frac(NB)
    u=[sum(R[i][j]*Z[j] for j in range(len(I))) for i in range(len(I))]
    return sum(Z[i]*u[i] for i in range(len(I)))

def normalize(C):
    s=set(C)
    for v,c,n in tuple(s):
        if (v,c,not n) in s:return None
    return tuple(sorted(s))

def characteristic(C):
    groups=collections.defaultdict(list)
    for v,c,n in C:groups[v].append((c,n))
    p=Fraction(1,1)
    for L in groups.values():p*=a_of(L)
    r=len(groups)
    return Fraction(1,1)/(T**r-p),r

def lit(chain,rng):return (chain,rng.randrange(3),bool(rng.randrange(2)))
def term(pair,rng):
    a,b=pair
    return (lit(a,rng),lit(b,rng))

def gen(k,m,kind,seed):
    rng=random.Random(seed);out=[]
    for j in range(m):
        if kind=="pair_rich":
            A=tuple(rng.sample(range(k),2));B=A
        elif kind=="star":
            A=(0,1+j%(k-1));B=A
        elif kind=="spread4":
            a,b,c,d=rng.sample(range(k),4);A=(a,b);B=(c,d)
        elif kind=="triple":
            a,b,c=rng.sample(range(k),3);A=(a,b);B=(a,c)
        elif kind=="random":
            A=tuple(rng.sample(range(k),2));B=tuple(rng.sample(range(k),2))
        else:raise ValueError(kind)
        out.append((term(A,rng),term(B,rng)))
    return out

def greedy(k,mediators):
    E=[]
    for A,B in mediators:
        C=normalize(A+B)
        if C is None:continue
        lam,r=characteristic(C)
        gain=math.log(float(lam/(L1**r)))
        S=frozenset(v for v,_,_ in C)
        E.append((gain,S,lam,r,C))
    E.sort(reverse=True,key=lambda x:x[0])
    used=set();sel=[]
    for e in E:
        if not (used & e[1]):
            sel.append(e);used.update(e[1])
    return {
      "non_tautological_edges":len(E),
      "selected_blocks":len(sel),
      "covered_chains":len(used),
      "coverage":len(used)/k,
      "relative_DLS_factor":math.exp(-sum(e[0] for e in sel)),
      "selected_rank_counts":dict(collections.Counter(e[3] for e in sel))
    }

def main():
    kinds=["pair_rich","star","spread4","triple","random"]
    out={}
    for kind in kinds:
        rows=[greedy(12,gen(12,24,kind,20261005+s)) for s in range(30)]
        out[kind]={
          "mean_edges":sum(x["non_tautological_edges"] for x in rows)/30,
          "mean_selected_blocks":sum(x["selected_blocks"] for x in rows)/30,
          "mean_coverage":sum(x["coverage"] for x in rows)/30,
          "min_coverage":min(x["coverage"] for x in rows),
          "max_coverage":max(x["coverage"] for x in rows),
          "mean_relative_DLS_factor":sum(x["relative_DLS_factor"] for x in rows)/30
        }
    print(json.dumps({
      "k":12,"mediators":24,"seeds_per_pattern":30,
      "patterns":out
    },indent=2))

if __name__=="__main__":
    main()
