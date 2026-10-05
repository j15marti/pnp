#!/usr/bin/env python3
"""
CONSISTENCY-PAIR1.

Exact characteristic values for two type-1 chains linked by one coordinate
equality or disequality constraint.

Uses Liu's LP definition with k=3:
  lambda = sum_a pi(a) * (1/2)^{d(a,a*)}, for every a* in A,
  sum pi = 1.

The linear system is solved exactly with fractions.

Also computes:
  * relative DLS factor versus two independent type-1 chains;
  * conditional all-paired bottleneck base;
  * guaranteed matching coverage and resulting DLS base for the
    exactly-4-occurrence 3-SAT dual-encoding control.
"""

from fractions import Fraction
import itertools, math, json

D=[s for s in itertools.product([0,1],repeat=3) if any(s)]

def solve_linear(A,b):
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

def characteristic(states):
    N=len(states)
    M=[]
    for star in states:
        row=[]
        for a in states:
            d=sum(x!=y for x,y in zip(a,star))
            row.append(Fraction(1,2**d))
        M.append(row)
    q=solve_linear(M,[1]*N)     # M q = 1
    lam=Fraction(1,1)/sum(q)
    pi=[lam*x for x in q]
    assert all(x>=0 for x in pi)
    assert sum(pi)==1
    return lam,pi

def paired_base(lam):
    # Balance 3^nu with (4/3)^(n-3nu) lam^(-nu/2).
    den=math.log(3)+3*math.log(4/3)+0.5*math.log(float(lam))
    x=math.log(4/3)/den
    return math.exp(x*math.log(3)),x

def mixed_balance_base(f,lam_pair,lam1=Fraction(3,7)):
    den=(math.log(3)+3*math.log(4/3)
         +(f/2)*math.log(float(lam_pair))
         +(1-f)*math.log(float(lam1)))
    x=math.log(4/3)/den
    return math.exp(x*math.log(3)),x

def dls_only_base(f,lam_pair,lam1=Fraction(3,7)):
    # All variables covered by m disjoint 1-chains, n=3m.
    return math.exp(((1-f)*math.log(1/float(lam1))
                     +(f/2)*math.log(1/float(lam_pair)))/3)

eq=[a+b for a in D for b in D if a[0]==b[0]]
ne=[a+b for a in D for b in D if a[0]!=b[0]]

leq,_=characteristic(eq)
lne,_=characteristic(ne)
ind=Fraction(9,49)

# Exactly-four-occurrence 3-SAT: 3m=4n_src.  A path through the four
# occurrences of each variable gives 3 edges per source variable, hence
# E=9m/4.  The occurrence-consistency multigraph has maximum degree <=6.
# Greedy matching >= E/(2Delta-1)=9m/44, covering >=9m/22 chain vertices.
f=9/22
worst=min(leq,lne)

out={
  "equality_joint_states":len(eq),
  "disequality_joint_states":len(ne),
  "lambda_independent_pair":str(ind),
  "lambda_equality":str(leq),
  "lambda_equality_float":float(leq),
  "lambda_disequality":str(lne),
  "lambda_disequality_float":float(lne),
  "relative_factor_equality":str(ind/leq),
  "relative_factor_disequality":str(ind/lne),
  "all_equality_paired_balance_base":paired_base(leq)[0],
  "all_disequality_paired_balance_base":paired_base(lne)[0],
  "guaranteed_matching_covered_chain_fraction_exact":"9/22",
  "guaranteed_matching_covered_chain_fraction_float":f,
  "mixed_balance_base_at_9_over_22":mixed_balance_base(f,worst)[0],
  "dls_only_base_when_all_variables_are_chain_variables_at_9_over_22":dls_only_base(f,worst),
  "dls_only_independent_chain_base":dls_only_base(0,worst),
  "dls_only_all_paired_equality_base":dls_only_base(1,leq)
}
print(json.dumps(out,indent=2))

if __name__=="__main__":
    pass
