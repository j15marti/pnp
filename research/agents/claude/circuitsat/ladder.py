"""Exact B2 circuit-size ladder for n<=3 (gates = 2-input gates, any of 16 binary functions
incl. degenerate ones excluded).  Wires = 2*gates (every gate has fan-in 2).
Method: BFS over sets of computed functions up to 3 gates, then one extra gate closure for 4.
Runtime ~ seconds."""
import itertools, json, sys
n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
N = 1 << n; FULL = (1 << N) - 1
def var(i): return sum(1 << a for a in range(N) if (a >> i) & 1)
inputs = [var(i) for i in range(n)]
# nondegenerate binary ops as truth-table lambdas on bitmasks (a,b)
def ops(a, b):
    na, nb = ~a & FULL, ~b & FULL
    return {a & b, a & nb, na & b, na & nb | 0 if False else (na & nb), a | b, a | nb, na | b, na | nb, a ^ b, ~(a ^ b) & FULL}
best = {0: 0, FULL: 0}
for v in inputs: best[v] = 0; best[~v & FULL] = 0  # negation free in B2 (absorbed into next gate); inputs/negs cost 0
# NOTE: negated input as free literal: standard "B2 with free literal negation" convention
start = frozenset(inputs)
layer = {start}
for g in range(1, 4):
    nxt = set()
    for S in layer:
        L = list(S)
        for a, b in itertools.combinations(L, 2):
            for f in ops(a, b):
                if f not in S:
                    nxt.add(S | {f})
                    best.setdefault(f, g)
    layer = nxt
    print(g, len(layer), len(best), file=sys.stderr)
# gate 4: closure of layer-3 sets
for S in layer:
    L = list(S)
    for a, b in itertools.combinations(L, 2):
        for f in ops(a, b):
            best.setdefault(f, 4)
# literals are cost 0 (negation of an input is free): add ops over negated literals too -> handled since ops include negations of a,b
from collections import Counter
cnt = Counter(best.values())
print(json.dumps({"n": n, "functions_found": len(best), "of": 1 << N, "by_gates": dict(sorted(cnt.items()))}))
