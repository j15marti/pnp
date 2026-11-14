#!/usr/bin/env python3
"""TMR-5/011: independent 8-mask SAT 5/6/7-sign certificate audit.

No SAT oracle, graph matching routine, or peer code imports. 40,320 possible
UNSAT eight-row permutations are enumerated explicitly, with one bit per
completion. A source observation is a partial assignment to 24 sign bits.

Usage: python tmr5_minimal_seven_audit011.py balanced_projection
Outputs one raw JSON document. Each invocation processes one case.
"""
import itertools
import json
import math
import sys
import time

FIXTURES = {
    "balanced_projection": (0,0,1,1,6,6,7,7),
    "balanced_even": (0,0,3,3,5,5,6,6),
    "unbalanced_prior": (1,2,3,4,5,6,7,7),
    "unsat_permutation": (0,1,2,3,4,5,6,7),
    "all_equal": (7,7,7,7,7,7,7,7),
    "five_equal": (7,7,7,7,7,0,0,0),
    "six_equal": (7,7,7,7,7,7,0,0),
}

def choose(n, k):
    return math.comb(n,k) if 0 <= k <= n else 0

def predicted_counts(a):
    full = [sum(x == m for x in a) for m in range(8)]
    pairs = sum(choose(z,2) for z in full)
    triple = 0
    for j,k in itertools.combinations(range(3),2):
        for bj,bk in itertools.product(range(2),repeat=2):
            cnt = sum(((x>>j)&1)==bj and ((x>>k)&1)==bk for x in a)
            triple += choose(cnt,3)
    n5 = 0; extensions = 0
    for j,b in itertools.product(range(3),range(2)):
        n = sum(((x>>j)&1)==b for x in a)
        n5 += choose(n,5)
        extensions += choose(n,6)+(24-n)*choose(n,5)
    # NEW: seven-bit *minimal* certificates. Ordered pair of distinct
    # coordinate halfcubes with four and three observed rows, respectively.
    # Partition the chosen first four rows by i in the halfcube intersection.
    n7_min = 0
    for j,b,k,c in itertools.product(range(3),range(2),range(3),range(2)):
        if j==k: continue
        nH=sum(((x>>j)&1)==b for x in a)
        nJ=sum(((x>>k)&1)==c for x in a)
        inter=sum(((x>>j)&1)==b and ((x>>k)&1)==c for x in a)
        for i in range(5):
            n7_min += choose(inter,i)*choose(nH-inter,4-i)*choose(nJ-i,3)
    return {"N5":n5,"N6":pairs+triple+extensions,
            "N6_pairs":pairs,"N6_projections":triple,
            "N6_extensions":extensions,"M7_minimal":n7_min}

def make_completion_masks(a):
    good = [0]*24
    count=0
    for idx, perm in enumerate(itertools.permutations(range(8))):
        flag=1<<idx
        for row in range(8):
            mask=perm[row]
            for j in range(3):
                pos=3*row+j
                if ((mask>>j)&1)==((a[row]>>j)&1):
                    good[pos]|=flag
        count+=1
    assert count==40320
    return good,(1<<count)-1

def minimal_seven_shape(a,Q):
    if len({p//3 for p in Q})!=7: return False
    groups={}
    for p in Q:
        j=p%3; b=(a[p//3]>>j)&1
        groups[(j,b)]=groups.get((j,b),0)+1
    if len(groups)!=2 or sorted(groups.values())!=[3,4]:return False
    (j,_),(k,_)=list(groups)
    return j!=k

def intersection(Q, compatible, universe):
    z=universe
    for p in Q:
        z &= compatible[p]
        if not z:break
    return z

def audit(case):
    a=FIXTURES[case]
    start=time.monotonic()
    expected=predicted_counts(a)
    compatible, universe=make_completion_masks(a)
    checked={}; actual={}; witnesses={}; failures=[]
    for k in (5,6,7):
        ncert=0; nminimal=0; first_cert=None; first_min=None
        for Q in itertools.combinations(range(24),k):
            iscert=intersection(Q,compatible,universe)==0
            if iscert:
                ncert+=1
                if first_cert is None:first_cert=Q
            if k==7:
                ismin=iscert and all(intersection(Q[:j]+Q[j+1:],compatible,universe)!=0 for j in range(7))
                structural=minimal_seven_shape(a,Q)
                if structural != ismin:
                    failures.append({"Q":Q,"actual_minimal":ismin,"shape":structural})
                    if len(failures)>8:break
                if ismin:
                    nminimal+=1
                    if first_min is None:first_min=Q
        checked[str(k)]=math.comb(24,k)
        actual[f"N{k}"]=ncert
        witnesses[str(k)]={"first_certificate":first_cert}
        if k==7:
            actual["M7_minimal"]=nminimal
            witnesses["7"]["first_minimal_7"]=first_min
    assert actual["N5"]==expected["N5"],("N5",actual,expected)
    assert actual["N6"]==expected["N6"],("N6",actual,expected)
    assert actual["M7_minimal"]==expected["M7_minimal"],("M7",actual,expected)
    assert not failures,failures
    return {"version":"TMR5-M7-011","fixture":case,"tuple":a,
            "status":"COMPUTATIONAL; mathematical claim pending independent TMR-2/TMR-1 review",
            "method":"native CPython, 40320 UNSAT permutation bitsets, 5/6/7 full observations and all seven 6-subsets for minimality",
            "predicted":expected,"observed":actual,"subsets_checked":checked,
            "first_witnesses":witnesses,"failed_assertions":len(failures),
            "errors":failures,"elapsed_seconds":round(time.monotonic()-start,3)}

if __name__=="__main__":
    if len(sys.argv)!=2 or sys.argv[1] not in FIXTURES:
        raise SystemExit("Choose case: "+", ".join(FIXTURES))
    print(json.dumps(audit(sys.argv[1]),indent=2))
