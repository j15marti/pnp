#!/usr/bin/env python3
"""
HIGHINC-PATTERN1.

Exact finite audit of all local center-pattern branch types for a positive
type-1 chain D={0,1}^3\{000}.

A resolved clause incident to a fixed chain T contains at most two literals
from T in the current rank-<=4 clean-core schema. Up to coordinate permutation,
the 18 possible non-tautological local patterns reduce to five sign types:
  1+, 1-, 2++, 2+-, 2--.

Branch on the local clause Q:
  child A: Q is true;
  child B: Q is false, so every selected incident clause Q OR P_i exposes P_i.

When the outside supports of the selected clauses are pairwise chain-disjoint,
their DLS gains multiply. We conservatively use g=440/441, the weakest
rank-<=3 single-resolvent gain among the currently catalogued petal types.

This script computes exact local characteristic ratios and the smallest m with
  a_Q + b_Q g^m < 1.
"""

from fractions import Fraction
import itertools, json

D=[s for s in itertools.product([0,1],repeat=3) if any(s)]
L1=Fraction(3,7)
G=Fraction(440,441)

def solve_frac(M,b):
    n=len(M)
    A=[list(row)+[Fraction(b[i])] for i,row in enumerate(M)]
    for c in range(n):
        p=next(i for i in range(c,n) if A[i][c])
        A[c],A[p]=A[p],A[c]
        q=A[c][c]
        A[c]=[x/q for x in A[c]]
        for i in range(n):
            if i==c: continue
            q=A[i][c]
            if q:
                A[i]=[A[i][j]-q*A[c][j] for j in range(n+1)]
    return [A[i][-1] for i in range(n)]

def characteristic(states):
    M=[
      [Fraction(1,2**sum(x!=y for x,y in zip(a,b))) for b in states]
      for a in states
    ]
    q=solve_frac(M,[1]*len(M))
    lam=Fraction(1,1)/sum(q)
    assert min(lam*x for x in q)>=0
    return lam

def lit(s,coord,neg):
    v=s[coord]
    return 1-v if neg else v

def q_true_ratio(signs):
    states=[s for s in D if any(lit(s,i,neg) for i,neg in enumerate(signs))]
    lam=characteristic(states)
    return L1/lam,lam,len(states)

def threshold(a,b):
    m=0
    p=Fraction(1,1)
    while a+b*p >= 1:
        m+=1
        p*=G
    return m,a+b*p

def main():
    rows=[]

    # one-literal center
    one = [
      ("1+", Fraction(16,21), Fraction(5,7), 3),
      ("1-", Fraction(5,7), Fraction(16,21), 3),
    ]
    for name,a,b,mult in one:
        m,ratio=threshold(a,b)
        rows.append({
          "type":name,
          "multiplicity_among_18_patterns":mult,
          "true_branch_ratio":str(a),
          "false_branch_ratio_before_petals":str(b),
          "minimum_petals_for_strict_ratio_below_1":m,
          "ratio_at_threshold":str(ratio),
          "ratio_at_threshold_float":float(ratio),
        })

    # two-literal patterns, representative coordinates x1,x2
    cases=[
      ("2++",(False,False), Fraction(3,7),3),
      ("2+-",(False,True), Fraction(4,7),6),
      ("2--",(True,True), Fraction(4,7),3),
    ]
    for name,signs,b,mult in cases:
        a,lam,size=q_true_ratio(signs)
        m,ratio=threshold(a,b)
        rows.append({
          "type":name,
          "multiplicity_among_18_patterns":mult,
          "q_true_characteristic":str(lam),
          "q_true_local_state_count":size,
          "true_branch_ratio":str(a),
          "false_branch_ratio_before_petals":str(b),
          "minimum_petals_for_strict_ratio_below_1":m,
          "ratio_at_threshold":str(ratio),
          "ratio_at_threshold_float":float(ratio),
        })

    q=max(r["minimum_petals_for_strict_ratio_below_1"] for r in rows)
    B4=1
    B3=1+18*(q-1)*B4
    B2=1+36*(q-1)*B3
    B1=1+54*(q-1)*B2
    Dstar=18*B1

    out={
      "petal_gain_g":str(G),
      "pattern_rows":rows,
      "worst_petals_q_star":q,
      "link_recurrence":{
        "B4":B4,"B3":B3,"B2":B2,"B1":B1,
        "incidence_threshold_D_star":Dstar
      },
      "bounded_incidence_active_chain_coverage_lower_bound":
        f"1/{8*Dstar}",
      "scope":
        "Resolved rank<=4 type-1-chain interaction model; exact local DLS potential calculation, not unrestricted SAT runtime."
    }
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
