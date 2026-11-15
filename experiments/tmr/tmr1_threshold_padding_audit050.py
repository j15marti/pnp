#!/usr/bin/env python3
"""TMR-1/034 exact small-circuit and sparse-threshold padding controls.
Finite semantic tests and numeric inequalities only, NOT an asymptotic theorem.
Python 3 standard library. Run: python3 tmr1_threshold_padding_audit050.py
"""
from itertools import combinations
from math import ceil, floor, log2
from json import dumps

checks = 0

def require(x, msg):
    global checks
    checks += 1
    if not x:
        raise AssertionError(msg)

def truth_var(n, i):
    return sum(((j >> i) & 1) << j for j in range(1 << n))

def bounded_circuit_outputs(n, s):
    """Enumerate all <=s gate functions, AND/OR/NOT with free constants."""
    full = (1 << (1 << n)) - 1
    inputs = [truth_var(n, i) for i in range(n)] + [0, full]
    outputs = set(inputs)
    circuits = {()}
    for _ in range(s):
        nxt = set()
        for state in circuits:
            wires = inputs + list(state)
            for a in wires:
                nxt.add(state + (full ^ a,))
            for a in wires:
                for b in wires:
                    nxt.add(state + (a & b,))
                    nxt.add(state + (a | b,))
        circuits = nxt
        outputs.update(c[-1] for c in circuits)
    return outputs

def repeat_table(x, n, nprime):
    require(nprime >= n, "cannot unpad")
    N = 1 << n
    return sum(x << (j * N) for j in range(1 << (nprime-n)))

def log_D(n, s):
    from math import log2
    return log2(s+1) + log2(n+s+2) + s*(log2(3)+2*log2(n+s+2))

finite = []
for n in (2, 3):
    a1 = bounded_circuit_outputs(n, 1)
    a2 = bounded_circuit_outputs(n, 2)
    b1 = bounded_circuit_outputs(n+1, 1)
    b2 = bounded_circuit_outputs(n+1, 2)
    for x in range(1 << (1 << n)):
        y = repeat_table(x, n, n+1)
        require((x in a1) == (y in b1), "padding changed one-gate complexity")
        require((x in a2) == (y in b2), "padding changed two-gate complexity")
    finite.append({"arity": n, "tables": 1 << (1 << n), "one_gate_functions": len(a1), "two_gate_functions":len(a2)})

# Construct explicit fixed-arity threshold split, using NAND of two inputs.
n = 2
N = 1 << n
x0, x1 = truth_var(n,0), truth_var(n,1)
full = (1 << N) - 1
nand = full ^ (x0 & x1)
require(nand not in bounded_circuit_outputs(n,1), "NAND should require >1 gate")
require(nand in bounded_circuit_outputs(n,2), "NAND should require <=2 gates")
require(floor(N**.25) == 1 and floor(N**.50) == 2, "source threshold mismatch")
padded = repeat_table(nand, 2, 4)
require(padded in bounded_circuit_outputs(4,2), "padded NAND should be <=2 gates")
require(padded not in bounded_circuit_outputs(4,1), "padded NAND should be >1 gate")
require(floor((1 << 4)**.25) == 2, "padded lower parameter threshold not equal")

# Exact sparse-monomial DNF upper-bound by constructing OR of minterms.
for n in (2,3,4):
    N=1<<n
    for r in (1,2,3):
        if r>N:continue
        for support in combinations(range(N),r):
            direct = ''.join('1' if i in support else '0' for i in range(N))
            generated=''.join(str(int(any(all(((i>>b)&1)==((j>>b)&1) for b in range(n)) for j in support))) for i in range(N))
            require(direct==generated, "minterm DNF semantic discrepancy")

asymptotic=[]
mu_low=.25
mu_high=.50
K=4
for n in (16,24,32,40,48,64,80):
    N=1<<n
    s_low=floor(2**(mu_low*n))
    s_high=floor(2**(mu_high*n))
    r=ceil(K*s_low)
    upper=n+r*n-1
    log_sparse_lower=r*(n-log2(r))
    log_circuit_upper=log_D(n,s_low)
    require(r<N,"support weight invalid")
    if n>=32:
        require(upper<s_high,"large threshold not enough for sparse DNF")
        require(log_sparse_lower>log_circuit_upper,"sparse counting margin missing")
    asymptotic.append({"n":n,"N":str(N),"s_low":s_low,"s_high":s_high,"r":r,"minterm_gate_upper":upper,"log2_sparse_lower":round(log_sparse_lower,3),"log2_circuit_upper":round(log_circuit_upper,3),"separated_by_bounds":(upper<s_high and log_sparse_lower>log_circuit_upper)})

ratios=[]
for a in (1.1,1.5,1.95,1.97,1.99,2,4,8):
    ratios.append({"padding_arity_ratio":a,"output_exponent":round(a,6),"ideal_one_work_solver_exponent":round(1.01*a,6),"below_known_1_99":1.01*a<1.99})

print(dumps({"claim_id":"TMR1_THRESHOLD_PAD050","status":"COMPUTATIONAL finite audits; asymptotic counting and padding proofs separate", "assertions":checks,"failures":0,"finite_circuits":finite,"nand_threshold_gap":{"n":2,"high_mu":.5,"low_mu":.25,"source_tt":format(nand,'04b'),"padded_arity":4}, "sparse":asymptotic,"padding_exponents":ratios},indent=2,sort_keys=True))
