#!/usr/bin/env python3
"""Checks for the equality family F_{a,b} = A_a & P_k & B_b (CLAUDE ONETAPE-0001).

Encoding: every clause has exactly three literals; a literal is a sign bit
plus a fixed-width binary variable id.  Unit constraints [x_i = a_i] use the
4-clause gadget with two fresh auxiliary variables, so all inputs of a given k
have identical length and block positions.

Checks
1. All 4^k inputs for small k have the same length and block boundaries.
2. F_{a,b} is satisfiable iff a = b (small DPLL with unit propagation).
3. N_k / (k log2 k) stays bounded (N_k = Theta(k log k)).
4. Smallest k at which the union bound L*q*2^{k/2} < 2^k holds, for several q.
Writes verify_family_results.json.  Runs in a few seconds.
"""

import itertools
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def build(k, a, b):
    # variable numbering
    x = list(range(1, k + 1))
    nxt = k + 1
    auxA = [(nxt + 2 * i, nxt + 2 * i + 1) for i in range(k)]
    nxt += 2 * k
    auxB = [(nxt + 2 * i, nxt + 2 * i + 1) for i in range(k)]
    nxt += 2 * k
    pad = list(range(nxt, nxt + 3 * k))
    nvars = nxt + 3 * k - 1

    def unit(lit, u, v):
        return [(lit, u, v), (lit, u, -v), (lit, -u, v), (lit, -u, -v)]

    A = [c for i in range(k) for c in unit(x[i] if a[i] else -x[i], *auxA[i])]
    P = [(pad[3 * i], pad[3 * i + 1], pad[3 * i + 2]) for i in range(k)]
    B = [c for i in range(k) for c in unit(x[i] if b[i] else -x[i], *auxB[i])]
    return A, P, B, nvars


def encode(clauses, nvars):
    w = max(1, math.ceil(math.log2(nvars + 1)))
    bits = []
    for cl in clauses:
        for lit in cl:
            bits.append('1' if lit > 0 else '0')
            bits.append(format(abs(lit), '0%db' % w))
    return ''.join(bits)


def dpll(clauses, assign=None):
    assign = dict(assign or {})
    changed = True
    while changed:
        changed = False
        for cl in clauses:
            if any(assign.get(abs(l)) == (l > 0) for l in cl):
                continue
            free = [l for l in cl if abs(l) not in assign]
            if not free:
                return False
            if len(free) == 1:
                assign[abs(free[0])] = free[0] > 0
                changed = True
    for cl in clauses:
        if not any(assign.get(abs(l)) == (l > 0) for l in cl):
            free = [l for l in cl if abs(l) not in assign]
            v = abs(free[0])
            return dpll(clauses, {**assign, v: True}) or dpll(clauses, {**assign, v: False})
    return True


def main():
    out = {'per_k': {}, 'growth': [], 'union_bound_k0': {}}
    for k in range(1, 6):
        lengths, cuts, ok = set(), set(), True
        for a in itertools.product((0, 1), repeat=k):
            for b in itertools.product((0, 1), repeat=k):
                A, P, B, nv = build(k, a, b)
                s = encode(A + P + B, nv)
                lengths.add(len(s))
                cuts.add((len(encode(A, nv)), len(encode(A + P, nv))))
                if dpll(A + P + B) != (a == b):
                    ok = False
        out['per_k'][k] = {'pairs_checked': 4 ** k, 'distinct_lengths': len(lengths),
                           'distinct_block_cuts': len(cuts), 'sat_iff_equal': ok,
                           'N': lengths.pop()}
    for k in (10, 100, 1000, 10000, 100000):
        A, P, B, nv = build(k, [0] * k, [0] * k)
        N = len(encode(A + P + B, nv))
        Lmid = len(encode(P, nv))
        out['growth'].append({'k': k, 'N': N, 'middle_boundaries': Lmid,
                              'N_over_klogk': round(N / (k * math.log2(k)), 3)})
    for q in (2 ** 4, 2 ** 10, 2 ** 20):
        k = 2
        while True:
            A, P, B, nv = build(k, [0] * k, [0] * k)
            L = len(encode(P, nv))
            if math.log2(L) + math.log2(q) + k / 2 < k:
                break
            k += 1
        out['union_bound_k0'][str(q)] = k
    (HERE / 'verify_family_results.json').write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
