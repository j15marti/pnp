import math, sys
from math import comb, lgamma
import pandas as pd
from scipy.stats import beta

def log_ratio(N,m,d):
    if N-d<m: return -1e300
    return lgamma(N-d+1)-lgamma(N-d-m+1)-lgamma(N+1)+lgamma(N-m+1)

def tau(N,m,p):
    if p>=1: return 0
    if p<=0: return N-m+1
    target=math.log(p); lo,hi=0,N-m+1
    while lo<hi:
        mid=(lo+hi)//2
        if log_ratio(N,m,mid)<=target: hi=mid
        else: lo=mid+1
    return lo

inp=sys.argv[1]; outp=sys.argv[2]
df=pd.read_csv(inp); rows=[]
for _,r in df.iterrows():
    n=int(r.n);m=int(r.m);k=int(r.unsat);s=int(r.samples);N=8*comb(n,3);p=k/s
    plo=0.0 if k==0 else float(beta.ppf(.025,k,s-k+1))
    phi=1.0 if k==s else float(beta.ppf(.975,k+1,s-k))
    d_sat=tau(N,m,phi)
    d_unsat=tau(N,m,1-plo)
    d95=min(d_sat,d_unsat)
    dp=tau(N,m,max(p,1-p))
    rows.append(dict(n=n,alpha=float(r.alpha),m=m,N_clause_bits=N,unsat=k,samples=s,
                     p_unsat_hat=p,p_unsat_lo95=plo,p_unsat_hi95=phi,
                     cut_bestpol_point=dp,contacts_bestpol_point=2*dp,
                     cut_bestpol_95=d95,contacts_bestpol_95=2*d95,
                     median_dpll_nodes=int(r.median_nodes),p90_dpll_nodes=int(r.p90_nodes)))
pd.DataFrame(rows).to_csv(outp,index=False)
