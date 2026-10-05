#!/usr/bin/env python3
"""
CLAUSECHAR1.

Exact characteristic formula for a single non-tautological clause over
r=2,3,4 type-1 chains, where the local type-1 domain is
D={0,1}^3 \\ {000} and k=3 Liu kernel is 2^{-Hamming distance}.

For each chain i in the clause, B_i is the subset of D on which all literals
from that chain are false.  Let K be the 7x7 local kernel, N=K^{-1},
z=N*1, t=1^T z=7/3, and
    a(B)=z_B^T (N[B,B])^{-1} z_B.
Then for A=D^r \\ (B_1 x ... x B_r):
    lambda(A) = 1 / ( t^r - product_i a(B_i) ).

The script:
  * computes the finite local a(B) table exactly;
  * enumerates all 3132 legal non-tautological degree-2 mediator resolvent
    schemas on 2-4 chains;
  * verifies the exact formula against direct characteristic solves for all
    324 rank-2 schemas;
  * reports exact worst/best lambda by rank.
"""

from fractions import Fraction
import collections, itertools, json

D=[s for s in itertools.product([0,1],repeat=3) if any(s)]

def inv_frac(M):
    n=len(M)
    A=[list(row)+[Fraction(int(i==j)) for j in range(n)] for i,row in enumerate(M)]
    for c in range(n):
        p=next(i for i in range(c,n) if A[i][c])
        A[c],A[p]=A[p],A[c]
        q=A[c][c]
        A[c]=[x/q for x in A[c]]
        for i in range(n):
            if i==c:continue
            q=A[i][c]
            if q:
                A[i]=[A[i][j]-q*A[c][j] for j in range(2*n)]
    return [row[n:] for row in A]

def solve_frac(M,b):
    n=len(M)
    A=[list(row)+[Fraction(b[i])] for i,row in enumerate(M)]
    for c in range(n):
        p=next(i for i in range(c,n) if A[i][c])
        A[c],A[p]=A[p],A[c]
        q=A[c][c]
        A[c]=[x/q for x in A[c]]
        for i in range(n):
            if i==c:continue
            q=A[i][c]
            if q:
                A[i]=[A[i][j]-q*A[c][j] for j in range(n+1)]
    return [A[i][-1] for i in range(n)]

K=[
    [Fraction(1,2**sum(x!=y for x,y in zip(a,b))) for b in D]
    for a in D
]
N=inv_frac(K)
z=[sum(row) for row in N]
t=sum(z)
assert t==Fraction(7,3)

def local_forbidden(lits):
    out=[]
    for i,s in enumerate(D):
        ok=True
        for c,neg in lits:
            v=s[c]
            literal=(1-v) if neg else v
            if literal:
                ok=False;break
        if ok:out.append(i)
    return out

def submatrix(M,I):
    return [[M[i][j] for j in I] for i in I]

def a_of(lits):
    I=local_forbidden(lits)
    if not I:return Fraction(0,1)
    NB=submatrix(N,I)
    invNB=inv_frac(NB)
    zb=[z[i] for i in I]
    u=[sum(invNB[i][j]*zb[j] for j in range(len(I))) for i in range(len(I))]
    return sum(zb[i]*u[i] for i in range(len(I)))

def normalize(C):
    s=set(C)
    for v,c,n in tuple(s):
        if (v,c,not n) in s:return None
    return tuple(sorted(s))

def clause_lambda(C):
    groups=collections.defaultdict(list)
    for v,c,n in C:groups[v].append((c,n))
    p=Fraction(1,1)
    for lits in groups.values():p*=a_of(lits)
    r=len(groups)
    return Fraction(1,1)/(t**r-p)

def direct_rank2_lambda(C):
    allowed=[]
    for a,b in itertools.product(range(7),repeat=2):
        ass=[D[a],D[b]]
        if any(((1-ass[v][c]) if n else ass[v][c]) for v,c,n in C):
            allowed.append(D[a]+D[b])
    M=[
      [Fraction(1,2**sum(x!=y for x,y in zip(a,b))) for b in allowed]
      for a in allowed
    ]
    q=solve_frac(M,[1]*len(M))
    lam=Fraction(1,1)/sum(q)
    assert min(lam*x for x in q)>=0
    return lam

def schemas():
    terms=[]
    for a,b in itertools.combinations(range(4),2):
        for i,j in itertools.product(range(3),repeat=2):
            for ni,nj in itertools.product([False,True],repeat=2):
                terms.append(((a,i,ni),(b,j,nj)))
    out=set()
    for A in terms:
        for B in terms:
            C=normalize(A+B)
            if C is None:continue
            vs=sorted({v for v,_,_ in C})
            mp={v:i for i,v in enumerate(vs)}
            out.add(tuple(sorted((mp[v],c,n) for v,c,n in C)))
    return out

def main():
    local=collections.defaultdict(collections.Counter)
    for q in range(1,4):
        for coords in itertools.combinations(range(3),q):
            for signs in itertools.product([False,True],repeat=q):
                lits=tuple(zip(coords,signs))
                local[q][a_of(lits)]+=1

    S=schemas()
    byrank=collections.defaultdict(list)
    checked=0
    for C in S:
        lam=clause_lambda(C)
        r=len({v for v,_,_ in C})
        byrank[r].append(lam)
        if r==2:
            assert lam==direct_rank2_lambda(C)
            checked+=1

    out={
      "local_t":str(t),
      "local_lambda":str(Fraction(1,1)/t),
      "local_a_histogram":{
        str(q):{str(k):v for k,v in sorted(H.items())}
        for q,H in sorted(local.items())
      },
      "total_resolvent_schemas":len(S),
      "rank_counts":{str(r):len(v) for r,v in sorted(byrank.items())},
      "rank2_direct_crosschecks":checked,
      "rank_bounds":{
        str(r):{
          "minimum_lambda":str(min(v)),
          "maximum_lambda":str(max(v)),
          "independent_lambda":str(Fraction(3,7)**r),
          "weakest_relative_DLS_factor":str((Fraction(3,7)**r)/min(v))
        }
        for r,v in sorted(byrank.items())
      }
    }
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
