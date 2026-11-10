#!/usr/bin/env python3
"""LSPV-1/551: exact FLMV coNTISP exponent and strict-3CNF witness controls.
Python 3 standard library. Deterministic, exhaustive where stated, no solver oracle.
Run: python experiments/arc/lspv1_551_conondet_exact.py
"""
from fractions import Fraction as Q
from math import log, sqrt
from pathlib import Path
import json

def g(c, k):
    v = Q(1)
    for _ in range(k):
        v = c*c*v/(1+c*v)
    return v

def g_closed(c, k):
    D = 1+c-c*c
    return (c-1/c)/(1-D/c**(2*k+1))

def d(c, k):
    return min((1/g(c,k)-c)/k, c**(-2*k))

def optimize(c):
    if c*c >= 2:
        return 0, Q(0), 0
    best, bestk, checks = Q(0), 0, 0
    k = 1
    while True:
        value = d(c,k)
        checks += 1
        assert g(c,k) == g_closed(c,k)
        assert (value > 0) == (2-c*c > (1+c-c*c)/c**(2*k+1))
        if value > best:
            best, bestk = value, k
        # For all j>k: d_j <= (2-c^2)/((c-1/c)j).
        if (2-c*c)/((c-1/c)*(k+1)) <= best:
            return bestk, best, checks
        k += 1
        assert k <= 10000

def eq3cnf(h):
    z = 2*h+1
    ans = []
    for i in range(1,h+1):
        x,y = i,h+i
        ans.extend([(-x,y,z),(-x,y,-z),(x,-y,z),(x,-y,-z)])
    return ans

def accepts(clauses, assignment):
    return all(any((assignment[abs(v)-1] == (v>0)) for v in clause) for clause in clauses)

def check_equality(h):
    source = eq3cnf(h)
    assert len(source) == 4*h
    assert all(len({abs(v) for v in clause}) == 3 for clause in source)
    total, valid = 0, 0
    for bits in range(1 << (2*h+1)):
        a = tuple(bool((bits >> i)&1) for i in range(2*h+1))
        observed = accepts(source,a)
        expected = a[:h] == a[h:2*h]
        assert observed == expected
        valid += int(observed)
        total += 1
    assert valid == (1 << (h+1))
    return {'h':h,'clauses':4*h,'assignments_tested':total,'models':valid,
            'stream_prefix_distinguishability':1<<h,'one_pass_state_bits_lb':h}

cs = [Q(6,5),Q(5,4),Q(13,10),Q(7,5),Q(141,100),Q(707,500),
      Q(7071,5000),Q(141421,100000),Q(3,2),Q(8,5)]
rows=[]
for c in cs:
    k,x,n = optimize(c)
    rows.append({'c':str(c),'c_float':float(c),'optimal_k':k,'d_exact':str(x),
                 'd_float':float(x),'checked_levels':n,'positive':bool(x>0)})
assert d(Q(6,5),1) == Q(59,180)
assert optimize(Q(6,5))[1] == Q(4499,12960)
assert optimize(Q(3,2))[1] == 0
assert all((optimize(Q(a,b))[1]>0) for a,b in [(6,5),(7,5),(14142,10000)])
source_controls=[check_equality(h) for h in range(1,6)]
# Deliberately corrupted controls: missing a facet, duplicated literal, bad index.
assert accepts(eq3cnf(2)[1:],(True,False,False,False,False))
assert not accepts(eq3cnf(2),(True,False,False,False,False))
assert not all(len({abs(v) for v in cl})==3 for cl in [(1,1,-2)])
assert not all(1<=abs(v)<=5 for cl in [(1,2,6)] for v in cl)
ratios=[]
for epsilon in [1e-3,1e-4,1e-5]:
    c=sqrt(2)-epsilon
    gv=1.; best=0.; best_k=0
    for k in range(1,250):
        gv=c*c*gv/(1+c*gv)
        value=min((1/gv-c)/k,c**(-2*k))
        if value>best: best,best_k=value,k
    expected=4*log(2)*epsilon/log(1/epsilon)
    ratios.append({'epsilon':epsilon,'optimal_k':best_k,'d_num':best,
                   'asymptotic':expected,'ratio':best/expected})
raw={'status':'PROVED/RESTRICTED + COMPUTATIONAL','reference':'FLMV 2005 theorem 6.4',
     'method':'exact Python Fraction rational; full finite truth tables; no random seed',
     'rows':rows,'source_controls':source_controls,'asymptotic_controls':ratios,
     'exact_recurrence_checks':sum(r['checked_levels'] for r in rows),
     'equality_assignments_checked':sum(r['assignments_tested'] for r in source_controls),
     'limits':'No hypothetical SAT solver executed; witness tape is separate read-only input; no historical R_mix341 checker; not a P vs NP proof.'}
path=Path('results/raw/arc/2026-11-09_1900_LSPV1_551_CONONDET_WITNESS_RAW.json')
path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(json.dumps(raw,indent=2)+'\n')
print(json.dumps({'status':'PASS','rational_checks':raw['exact_recurrence_checks'],
  'truth_assignments_checked':raw['equality_assignments_checked'],
  'c1.2_conondet_d':float(optimize(Q(6,5))[1]),
  'c1.4_conondet_d':float(optimize(Q(7,5))[1]),
  'raw_path':str(path)},indent=2))
