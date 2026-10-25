"""Exact wire-sensitivity of AIG circuit-SAT for small (n,g). Each run well under 30s.
Usage: python3 wire_sensitivity.py n g
Model: n inputs, g AND-gates; gate i has two wires, each choosing one of (n+i) earlier
nodes with a polarity bit (2(n+i) choices). Output = last gate. Encoding length 2g wires.
Outputs JSON: instance count, #sat, max wire-sensitivity on SAT and UNSAT instances,
and the max, over UNSAT instances, of #wires whose single rewire makes it SAT."""
import sys, json, numpy as np
n, g = int(sys.argv[1]), int(sys.argv[2])
radix = []
for i in range(g):
    radix += [2*(n+i)]*2
N = int(np.prod(radix, dtype=object))
assert N <= 40_000_000, N
idx = np.arange(N, dtype=np.int64)
digs = []
r = idx.copy()
for b in reversed(radix):
    digs.append(r % b); r //= b
digs = digs[::-1]
full = (1 << (1 << n)) - 1
tt = []
for j in range(n):
    t = 0
    for x in range(1 << n):
        if (x >> j) & 1: t |= 1 << x
    tt.append(np.full(N, t, dtype=np.int64))
for i in range(g):
    ops = []
    for w in (0, 1):
        d = digs[2*i+w]; node = d >> 1; neg = d & 1
        val = np.zeros(N, dtype=np.int64)
        for k in range(n+i):
            val = np.where(node == k, tt[k], val)
        ops.append(np.where(neg == 1, full ^ val, val))
    tt.append(ops[0] & ops[1])
sat = (tt[-1] != 0).reshape(radix)
nsat = int(sat.sum())
sens = np.zeros(radix, dtype=np.int16)
usat_to_sat = np.zeros(radix, dtype=np.int16)
for a in range(2*g):
    anysat = sat.any(axis=a, keepdims=True)
    anyuns = (~sat).any(axis=a, keepdims=True)
    flip = np.where(sat, anyuns, anysat)
    sens += flip
    usat_to_sat += (~sat) & anysat
res = dict(n=n, g=g, wires=2*g, instances=N, sat=nsat,
           max_sens_unsat=int(sens[~sat].max()), max_sens_sat=int(sens[sat].max()),
           max_sens_all=int(sens.max()))
print(json.dumps(res))
