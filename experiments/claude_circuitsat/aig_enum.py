"""Exhaustive AIG (AND + free edge negation) enumeration, n inputs, g gates.
Counts circuits where every input and every non-final gate is used (no dead
nodes), split by output function: constant-0/1 (UNSAT/valid) vs non-constant.
Usage: aig_enum.py n g [first_gate_index_mod chunk]"""
import sys, json, itertools
n, g = int(sys.argv[1]), int(sys.argv[2])
M = (1 << (1 << n)) - 1
inp = []
for i in range(n):
    t = 0
    for a in range(1 << n):
        if (a >> i) & 1: t |= 1 << a
    inp.append(t)
res = {"n": n, "g": g, "circuits": 0, "const": 0, "nonconst": 0, "wires": 2 * g}
def rec(tts, used, k):
    if k == g:
        # every node except last gate must be used
        if all(used[: n + g - 1]) :
            res["circuits"] += 1
            f = tts[-1]
            if f == 0 or f == M: res["const"] += 1
            else: res["nonconst"] += 1
        return
    m = len(tts)
    remaining = g - k
    # pruning: unused nodes count (excluding future) must be fixable: each new gate uses 2 slots
    unused = sum(1 for u in used if not u)
    if unused > 2 * remaining + 0 and True:
        # each remaining gate can consume at most 2 unused, but new gate itself is unused (+1)
        if unused - 2 * remaining > 1 - 0: return
    for a in range(m):
        for b in range(a + 1, m):
            for na in (0, 1):
                for nb in (0, 1):
                    x = tts[a] ^ (M if na else 0)
                    y = tts[b] ^ (M if nb else 0)
                    u2 = used[:]; u2[a] = u2[b] = True
                    rec(tts + [x & y], u2 + [False], k + 1)
rec(inp, [False] * n, 0)
print(json.dumps(res))
