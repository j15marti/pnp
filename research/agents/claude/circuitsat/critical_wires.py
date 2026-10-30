"""Verify the 'every gate critical' family U_k: n=1 input x, two OR-buffer chains of length k,
out = AND(a_k, b_k).  U_k is UNSAT; for every gate there is a one-edge redirection making it SAT."""
import json
def build(k):
    # nodes: ('x'), gates list of (op, in1, in2); literals are (node, neg)
    gates = []  # each gate: [op, (src,neg), (src,neg)] ; src = 'x' or gate index
    a_prev = ('x', 0); b_prev = ('x', 1)
    a_ids = []; b_ids = []
    for j in range(k):
        gates.append(['OR', a_prev, a_prev]); a_prev = (len(gates) - 1, 0); a_ids.append(len(gates) - 1)
        gates.append(['OR', b_prev, b_prev]); b_prev = (len(gates) - 1, 0); b_ids.append(len(gates) - 1)
    gates.append(['AND', a_prev, b_prev])
    return gates, a_ids, b_ids
def ev(gates, x):
    val = {}
    def lit(l):
        v = x if l[0] == 'x' else val[l[0]]
        return v ^ l[1]
    for i, (op, p, q) in enumerate(gates):
        val[i] = (lit(p) | lit(q)) if op == 'OR' else (lit(p) & lit(q))
    return val[len(gates) - 1]
def sat(g): return any(ev(g, x) for x in (0, 1))
res = {}
for k in range(1, 9):
    g, A, B = build(k)
    assert not sat(g)
    crit = 0
    for gi in range(len(g)):
        ok = False
        for e in (1, 2):
            for src in ['x'] + list(range(gi)):
                for neg in (0, 1):
                    h = [[o, p, q] for o, p, q in g]
                    h[gi][e] = (src, neg)
                    if sat(h): ok = True
        crit += ok
    res[k] = {"gates": len(g), "critical_gates": crit}
    assert crit == len(g)
json.dump(res, open("critical_wires_results.json", "w"), indent=1); print(res)
