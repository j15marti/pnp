#!/usr/bin/env python3
"""Dependency-free exact audit of two-level R15 encoded lengths and conditional bounds.
No SAT lower bound is asserted. Python int counters are logical arithmetic, not TM steps.
"""
import json
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path

RUN = "ARC_R15_LENGTH_AUDIT126"
CHECKS=0

def check(test, label):
    global CHECKS
    CHECKS += 1
    if not test:
        raise AssertionError(label)

def ceil_log2_plus1(n):
    assert n>=0
    return n.bit_length()  # ceil(log2(n+1)) for integer n>=1

def encode_bits(v,m):
    """Exact LSPV-2 fixed-width binary proper-CNF layout.
    Header 4 fixed bits plus two max-sized counts; three (sign,id) records/row.
    """
    assert v>0 and m>0
    w=ceil_log2_plus1(v)
    wh=ceil_log2_plus1(max(v,m))
    return 4 + 2*wh + 3*m*(1+w)

def r15(v,m):
    return 33*m+48*v,44*m+64*v

def beta(c):
    return (((c+2)/(c*c))-c)/2

def fraction_dict(q):
    return {"rational":f"{q.numerator}/{q.denominator}","decimal":format(float(q),".15f")}

d=Q(901,500)
D=d*d
cstar=Q(241,200)
sstar=Q(11642479,23232400)
ctwo=Q(6,5)
C=max(1+1/d,(2*d-1)/(d*(d-1)))
qstar=D/(D-1)

check(beta(cstar)==sstar,"FLMV exact beta")
check(beta(ctwo)==Q(23,45),"FLMV curved beta")
check(cstar-ctwo==Q(1,200),"rectangle time margin")
check(sstar-Q(1,2)==Q(26279,23232400),"rectangle space margin")
check(beta(ctwo)-Q(1,2)==Q(1,90),"curved space margin")
check(C==Q(651000,361301),"two-algorithm c frontier")
check(qstar==Q(811801,561801),"circuit q frontier")
q2=(2*D-2)/(D*(D-2))
check(q2<qstar,"first Theorem 6.3 branch is stronger at D=d^2")
check(d-C==Q(32201,180650500),"single-child guest upper exponent exceeds C(d)")
check((qstar-1)*D==qstar,"Theorem 6.3 equality")
check(not ((qstar-1)*D < qstar),"q boundary not strict")
check((C*d*(d-1)-2*d+1)==0,"Theorem 1.3 equality")
check(not(C*d*(d-1)-2*d+1<0),"coNTIME boundary not strict")

# Rank-one count operator A=[[48,33],[64,44]] on (v,m): A^2=92A.
check(48*44-33*64==0,"R15 count matrix determinant")
for v,m in [(1,1),(3,4),(6,17),(15,20),(198,264),(1001,901),(10**6,10**8)]:
    v1,m1=r15(v,m)
    v2,m2=r15(v1,m1)
    v3,m3=r15(v2,m2)
    check(3*m1==4*v1,"image exact incidence")
    check((v2,m2)==(92*v1,92*m1),"rank-one matrix square")
    check((v3,m3)==(92*v2,92*m2),"rank-one cube")

rows=[]
for k in [1,2,4,16,1024,10**6]:
    v,m=3*k,4*k
    v1,m1=r15(v,m)
    v2,m2=r15(v1,m1)
    b0,b1,b2=[encode_bits(*pair) for pair in [(v,m),(v1,m1),(v2,m2)]]
    check(v1==92*v and m1==92*m,"one-level exact (2,2) 92 factor")
    check(v2==8464*v and m2==8464*m,"two-level exact (2,2) 8464 factor")
    check(b2>b1>b0,"actual encoded bit lengths strictly increase")
    check(b1>=92*b0-500 and b2>=8464*b0-5000,"bit length generally tracks expansion")
    rows.append({"family":"exact_2p2n", "k":k, "root":[v,m,b0], "child":[v1,m1,b1], "grandchild":[v2,m2,b2], "ratio_child_over_parent":round(b1/b0,9),"ratio_grandchild_over_parent":round(b2/b0,9)})

for p in [2,3,5,8,16,32,128,1024,10**6]:
    v,m=4*p+1,8*p
    v1,m1=r15(v,m)
    v2,m2=r15(v1,m1)
    b0,b1,b2=[encode_bits(*pair) for pair in [(v,m),(v1,m1),(v2,m2)]]
    check((v1,m1)==(456*p+48,608*p+64),"parity family first counts")
    check((v2,m2)==(41952*p+4416,55936*p+5888),"parity family second counts")
    check(b2>b1>b0,"parity source bit expansion")
    check(3*m1==4*v1 and 3*m2==4*v2,"target exact 2,2 incidence")
    rows.append({"family":"parity_template", "p":p, "root":[v,m,b0], "child":[v1,m1,b1], "grandchild":[v2,m2,b2], "ratio_child_over_parent":round(b1/b0,9),"ratio_grandchild_over_parent":round(b2/b0,9)})

invalid_claim={
 "claim":"Two locally addressable R15 levels are power-short ordinary SAT grandchildren of length O(N^(1/4))",
 "status":"FALSIFIED/RETIRED",
 "counterexample":"any cofinal encoded exact-(2,2) family with n=3k,m=4k, k→∞",
 "true_length":"M_2=Theta(N); exact counts (v_2,m_2)=8464(v_0,m_0)",
 "false_guest_t_when_d_6_5":"(1/4)*(6/5)=3/10",
 "actual_guest_t_from_length_when_d_6_5":"6/5 (upper-bound exponent scale), not a proven lower bound on guest runtime",
 "eager_peak":"Omega(N) bits if an explicit grandchild is stored, not N^(1/4)",
 "lazy":"polylog service only on fixed-incidence/indexed source subfamily; does not shorten ordinary child",
}

res={
 "run": RUN, "date":"2026-10-26T00:36:00-07:00", "status":"PROVED/EXACT arithmetic and conditional-model falsifier; P vs NP OPEN",
 "assertions":CHECKS, "sample_count":len(rows),
 "source_model":"LSPV-2 R15 fixed-width binary grammar; complete child described at every level; 4+2wh+3m(1+w)",
 "source_requirements":"fixed-incidence proper 3CNF with a paid Lit/Count/Rank/Select interface; no all-input construction inferred",
 "strict_bounds":{"FLMV_cstar":fraction_dict(cstar),"FLMV_beta_cstar":fraction_dict(sstar),"point_t":fraction_dict(ctwo),"point_s":fraction_dict(Q(1,2)),"rectangle_time_slack":fraction_dict(cstar-ctwo),"rectangle_space_slack":fraction_dict(sstar-Q(1,2)),"curved_space_slack_at_1p2":fraction_dict(beta(ctwo)-Q(1,2)),"extra_seed_d":fraction_dict(d),"coNTIME_C_d":fraction_dict(C),"Sigma2_d_squared":fraction_dict(D),"circuit_qstar":fraction_dict(qstar),"circuit_secondary_branch_q":fraction_dict(q2),"d_minus_coNTIME_frontier":fraction_dict(d-C)},
 "rows":rows,
 "falsifier":invalid_claim,
 "matrix_proved_identity":"A=[[48,33],[64,44]], rank(A)=1, A^2=92A, A^h=92^(h-1)A for all fixed h>=1",
 "limitations":"finite arithmetic is not a time/space experiment on FLMV machine; model bit layout is an explicitly scoped encoding; source exact-R15 correctness is adopted from peer and not independently SAT-proved here; output length lower bound applies to this particular construction not any possible reduction"
}
out=Path(__file__).with_name("2026-10-26_0036_ARC_R15_LENGTH_AUDIT126_raw.json")
out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps({"assertions":CHECKS,"samples":len(rows),"FLMV_slack":res['strict_bounds'],"first":rows[0],"last":rows[-1],"raw_sha256":sha256(out.read_bytes()).hexdigest()},indent=2))
