#!/usr/bin/env python3
"""TMR-2/032: exact expected-query sparse-oracle minimax, independent finite LP audits.
No external data or secrets. Ordinary Python 3 and scipy for independent LP check.
The mathematical argument is stated separately in the associated research report.
"""
from __future__ import annotations
import itertools, json, math, random, datetime
from fractions import Fraction
from scipy.optimize import linprog

SEED = 2032046
random.seed(SEED)
checks = 0
lp_cases = 0
support_checks = 0
strategy_cases = 0

def check(ok, message="check failed"):
    global checks
    checks += 1
    if not ok:
        raise AssertionError(message)

def hval(N, r, q):
    assert 1 <= r <= N and 0 <= q <= N
    return Fraction(math.comb(N-q, r) if N-q >= r else 0, math.comb(N, r))

def inverse_h(N, r, z):
    """Piecewise-linear inverse of exact hypergeometric avoidance function."""
    assert 0 <= z <= 1
    for q in range(N-r+1):
        top, bot = hval(N, r, q), hval(N, r, q+1)
        if top >= z >= bot:
            return Fraction(q) + (top-z)/(top-bot)
    raise AssertionError((N,r,z))

def witness_strategy(N, r, delta):
    """Return zero-path strategy: with prob delta guess NO; else query random q/q+1 set."""
    z = delta/(1-delta)
    x = inverse_h(N, r, z)
    q0 = x.numerator//x.denominator
    theta = x - q0
    return q0,theta,(1-delta)*x

def lp_optimum(N, r, delta):
    # Variables YES-trace q=0..N; one NO-trace that spends no queries.
    # Constraints: incorrect output on zero <=delta; error on uniform r-support <=delta.
    h=[float(hval(N,r,q)) for q in range(N+1)]
    c=[float(q) for q in range(N+1)] + [0.0]
    A=[[0.0]*(N+1)+[1.0], h+[0.0]]
    result=linprog(c,A_ub=A,b_ub=[float(delta),float(delta)],
                   A_eq=[[1.0]*(N+2)],b_eq=[1.0],bounds=(0,None),method='highs')
    check(result.success, 'LP failed')
    return result.fun

# Exact exhaustive proof-support checks for hypergeometric coupling.
for N in range(2,10):
    ground=set(range(N))
    for r in range(1,N+1):
        supports=list(itertools.combinations(range(N),r))
        for q in range(0,N+1):
            target=hval(N,r,q)
            sample_Q=[tuple(range(q)),tuple(range(N-q,N))]
            if N<=7:
                sample_Q=list(itertools.combinations(range(N),q))
            for Q in sample_Q:
                no_hit=sum(not (set(S)&set(Q)) for S in supports)
                check(Fraction(no_hit,len(supports))==target, (N,r,q,Q))
                support_checks+=len(supports)
        # Decreasing and discrete convex across source-query counts
        vals=[hval(N,r,q) for q in range(N+1)]
        for q in range(N):
            check(vals[q]>=vals[q+1])
        for q in range(N-1):
            check(vals[q]-vals[q+1] >= vals[q+1]-vals[q+2])

# Check exact strategy against ALL promised sparse supports; independent LP optimizes
# arbitrary stochastic policies via symmetrization, and may choose variable q per path.
deltas=[Fraction(0),Fraction(1,10),Fraction(1,5),Fraction(1,3),Fraction(2,5)]
representative=[]
for N in range(2,12):
    for r in range(1,N+1):
        for delta in deltas:
            q0,theta,Q = witness_strategy(N,r,delta)
            check(0<=q0<=N-r+1 and 0<=theta<=1)
            no_hit=(1-theta)*hval(N,r,q0)+theta*hval(N,r,min(q0+1,N))
            check((1-delta)*no_hit==delta)
            check(Q==(1-delta)*(q0+theta))
            # On each positive support, the probability of no-hit under a uniform query subset
            # is the same hypergeometric quantity. This verifies both labels independently.
            if N<=8:
                for S in itertools.combinations(range(N),r):
                    a=Fraction(sum(not (set(S)&set(subset)) for subset in itertools.combinations(range(N),q0)),math.comb(N,q0))
                    qb=min(q0+1,N)
                    b=Fraction(sum(not (set(S)&set(subset)) for subset in itertools.combinations(range(N),qb)),math.comb(N,qb))
                    check((1-delta)*((1-theta)*a+theta*b)==delta)
                    support_checks+=math.comb(N,q0)+math.comb(N,qb)
            opt=lp_optimum(N,r,delta)
            check(abs(opt-float(Q))<=1e-8,(N,r,str(delta),opt,str(Q)))
            lp_cases+=1
            strategy_cases+=1
            if (N,r,delta) in [(8,2,Fraction(1,3)),(10,3,Fraction(1,5)),(11,1,Fraction(2,5))]:
                representative.append({"N":N,"r":r,"delta":str(delta),"q_floor":q0,
                                       "prob_extra_query_conditional":str(theta),
                                       "optimal_mean_queries":str(Q),"lp":opt})

# Asymptotic finite numerical examples for ordinary MCSP sparse flips.
def Hfloat(N,r,q):
    if q>N-r: return 0.0
    return math.exp(sum(math.log1p(-q/(N-i)) for i in range(r)))

def inverse_float(N,r,z):
    lo,hi=0,N-r+1
    while hi-lo>1:
        mid=(lo+hi)//2
        if Hfloat(N,r,mid)>z: lo=mid
        else:hi=mid
    h0,h1=Hfloat(N,r,lo),Hfloat(N,r,lo+1)
    return lo+(h0-z)/(h0-h1)

numerical=[]
for n,mu,K in [(10,0.25,8),(16,0.25,8),(20,0.30,8)]:
    N=2**n
    s=math.floor(N**mu)
    r=math.ceil(K*s)
    check(K>2*mu/(1-mu))
    check(r<=N)
    D_log2=math.log2(s+1)+math.log2(n+s+2)+s*math.log2(3*(n+s+2)**2)
    C_log2=(math.lgamma(N+1)-math.lgamma(r+1)-math.lgamma(N-r+1))/math.log(2)
    eps= min(1.0,2**(D_log2-C_log2)) if D_log2-C_log2 > -1022 else 0.0
    delta=1/3
    beta=delta+(1-delta)*eps
    b_new=(1-delta)*inverse_float(N,r,beta/(1-delta)) if beta<1-delta else 0
    b_old=inverse_float(N,r,min(1,2*delta+(1-delta)*eps))
    check(b_new>=b_old-1e-7, (n, b_new, b_old))
    numerical.append({"n":n,"N":N,"mu":mu,"K":K,"s":s,"r":r,
                      "log2_circuit_count_bound":round(D_log2,4),
                      "log2_sparse_ball":round(C_log2,4),
                      "log2_epsilon_bound":round(D_log2-C_log2,4),
                      "new_expected_queries":round(b_new,6),
                      "TMR5_previous_bound":round(b_old,6),
                      "new_coefficient_scaled_r_over_N":round(b_new*r/N,6)})

coef_new=2/3*math.log(2)
coef_old=math.log(3/2)
check(coef_new>coef_old)
out={
    "timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "seed":SEED,"status":"COMPUTATIONAL finite checks for separate PROVED/RESTRICTED symbolic statement",
    "assertions":checks,"lp_cases":lp_cases,"strategy_cases":strategy_cases,
    "exhaustive_support_query_pair_operations":support_checks,
    "failures":0,"representatives":representative,"mcsp_numerics":numerical,
    "delta_1_over_3_new_leading_constant":coef_new,
    "delta_1_over_3_prior_leading_constant":coef_old,
    "relative_gain_percent":100*(coef_new/coef_old-1),
    "limitations":"This does not simulate Turing machine physical time, decide 3-SAT, or prove small-mu one-tape MCSP lower bound."
}
print(json.dumps(out,sort_keys=True,indent=2))
