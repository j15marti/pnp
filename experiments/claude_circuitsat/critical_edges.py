"""Max number of SAT-critical edges in an n-input, g-gate AIG (AND + edge negation).
Edge e is SAT-critical iff flipping its polarity changes satisfiability of the circuit.
Probe-model lower bound: any algorithm must probe every critical edge (adversary).
Usage: python critical_edges.py n g [first_gate_lo first_gate_hi]  (chunking by first gate index)"""
import sys, json, itertools
n, g = int(sys.argv[1]), int(sys.argv[2])
M = (1 << (1 << n)) - 1
X = []
for i in range(n):
    t = 0
    for a in range(1 << n):
        if (a >> i) & 1: t |= 1 << a
    X.append(t)
def gate_choices(N):
    return [(a, b, pa, pb) for a in range(N) for b in range(a + 1, N) for pa in (0, 1) for pb in (0, 1)]
choices = [gate_choices(n + k) for k in range(g)]
lo = int(sys.argv[3]) if len(sys.argv) > 3 else 0
hi = int(sys.argv[4]) if len(sys.argv) > 4 else len(choices[0])
def ev(gates, flip=None):
    v = list(X)
    for k, (a, b, pa, pb) in enumerate(gates):
        ta = v[a] ^ (M if pa ^ (flip == (k, 0)) else 0)
        tb = v[b] ^ (M if pb ^ (flip == (k, 1)) else 0)
        v.append(ta & tb)
    return v[-1]
best = {}   # (inputs_used) -> max critical
bestc = {}
def used(gates):
    s = set()
    for k, (a, b, _, _) in enumerate(gates):
        s.add(a); s.add(b)
    # reachability from output
    reach = {n + g - 1}; 
    for k in range(g - 1, -1, -1):
        if n + k in reach:
            reach.add(gates[k][0]); reach.add(gates[k][1])
    return sum(1 for i in range(n) if i in reach), len(reach) - sum(1 for i in range(n) if i in reach) == g
for first in choices[0][lo:hi]:
    for rest in itertools.product(*choices[1:]):
        gates = (first,) + rest
        base = ev(gates) != 0
        u, allg = used(gates)
        if not allg: continue          # every gate must be reachable
        c = sum(1 for k in range(g) for s in (0, 1) if (ev(gates, (k, s)) != 0) != base)
        if c > best.get(u, -1): best[u] = c; bestc[u] = gates
print(json.dumps({"n": n, "g": g, "chunk": [lo, hi], "max_critical_by_inputs_used": best,
                  "witness": {str(k): v for k, v in bestc.items()}}))
