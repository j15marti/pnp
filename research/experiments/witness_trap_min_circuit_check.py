"""Finite check of CANONICAL-WITNESS-TRAP9: exact SAT count and exact minimum
fan-in-2 (all 16 gate types) circuit size of canonical witness W0 vs alternate W1.
Runs in a few seconds for n=1..3."""
import itertools, sys

def sat_assignments(n):
    N = 1 << n
    sols = []
    for bits in itertools.product((0, 1), repeat=N + 1):
        b, y = bits[0], bits[1:]
        if all((i % 2 == 1 and y[i] == 1 - b) or (i % 2 == 0 and y[i] == 0) for i in range(N)):
            sols.append(bits)
    return sols

def tt(f, k):
    v = 0
    for x in range(1 << k):
        if f([(x >> j) & 1 for j in range(k)]):
            v |= 1 << x
    return v

def min_gates(target, k, cap):
    full = (1 << (1 << k)) - 1
    inputs = [tt(lambda a, j=j: a[j], k) for j in range(k)]
    def gate(op, a, c):
        r = 0
        for m in range(4):
            if (op >> m) & 1:
                A = a if (m & 1) else full ^ a
                C = c if (m & 2) else full ^ c
                r |= A & C
        return r
    if target in inputs or target in (0, full): return 0
    def dfs(avail, left):
        if left == 0: return False
        for x in range(len(avail)):
            for y in range(x + 1, len(avail)):
                for op in range(16):
                    v = gate(op, avail[x], avail[y])
                    if v == target: return True
                    if left > 1 and v not in avail and dfs(avail + [v], left - 1): return True
        return False
    for g in range(1, cap + 1):
        if dfs(inputs, g): return g
    return None

for n in (1, 2, 3):
    sols = sat_assignments(n)
    N = 1 << n
    W0 = tt(lambda a: (1 - a[0]) & (bin(sum(a[1 + j] << j for j in range(n))).count("1") & 1), n + 1)
    W1 = tt(lambda a: a[0], n + 1)
    print(n, "num_sat", len(sols), "W0 gates", min_gates(W0, n + 1, n + 2), "W1 gates", min_gates(W1, n + 1, 2), "bound n-1 =", n - 1)
