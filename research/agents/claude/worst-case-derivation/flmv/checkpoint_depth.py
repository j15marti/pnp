#!/usr/bin/env python3
"""WCD-FLMV-0001: checkpoint (binary-search) conversion of a space-bounded
configurational Res(+) refutation into a parity decision DAG.

Claim checked exhaustively on small instances:
  depth  <= FS * ceil(log2 L)
  nodes  <= 2 * L * (FS + 1) * 2^(3 FS)
where L = number of configurations and FS = max number of distinct linear
forms held in memory. Every run must end at a falsified source clause.
Single stage, pure Python, a few seconds. JSON on stdout.
"""
import itertools, json, math, sys, time
T0 = time.time()

def par(x): return bin(x).count("1") & 1
def line_true(line, x): return any(par(x & m) == b for (m, b) in line)
def forms(cfg): return sorted({m for line in cfg for (m, _) in line})

def build_configs(n, steps, axioms):
    """steps: ('ax', line) | ('inf', line) | ('del', line). Returns configs M_0..M_L and kinds.
    Every 'inf' is checked sound by truth table: memory |= line."""
    mem = []; cfgs = [tuple()]; kinds = [None]
    axset = {frozenset(a) for a in axioms}
    for kind, line in steps:
        line = frozenset(line)
        if kind == "ax": assert line in axset; mem = mem + [line]
        elif kind == "inf":
            for x in range(1 << n):
                if all(line_true(l, x) for l in mem): assert line_true(line, x), "unsound"
            mem = mem + [line]
        else: mem = [l for l in mem if l != line]
        cfgs.append(tuple(mem)); kinds.append(kind)
    assert frozenset() in cfgs[-1]
    return cfgs, kinds

def convert_and_check(n, cfgs, kinds, axioms):
    L = len(cfgs) - 1
    FS = max(len(forms(c)) for c in cfgs)
    nodes = set(); maxdepth = 0
    for x in range(1 << n):
        lo, hi = 0, L; depth = 0
        known = {}                          # form -> value, only forms of M_lo and M_hi are kept
        while hi - lo > 1:
            mid = (lo + hi) // 2
            for j, m in enumerate(forms(cfgs[mid])):
                nodes.add((lo, hi, j, tuple(sorted(known.items()))))
                if m not in known: known[m] = par(x & m); depth += 1   # a repeated form is free
            ok = all(any(known[m] == b for (m, b) in l) for l in cfgs[mid])
            if ok: lo = mid
            else:  hi = mid
            keep = set(forms(cfgs[lo])) | set(forms(cfgs[hi]))
            known = {m: v for m, v in known.items() if m in keep}
        nodes.add((lo, hi, -1, tuple(sorted(known.items()))))
        # terminal: M_lo all true, M_hi has a false line, which must be a downloaded source clause
        assert all(line_true(l, x) for l in cfgs[lo])
        bad = [l for l in cfgs[hi] if not line_true(l, x)]
        assert bad and kinds[hi] == "ax" and all(l in {frozenset(a) for a in axioms} for l in bad)
        maxdepth = max(maxdepth, depth)
    bd = FS * math.ceil(math.log2(L)); bs = 2 * L * (FS + 1) * 2 ** (3 * FS)
    assert maxdepth <= bd and len(nodes) <= bs
    return {"n": n, "L": L, "FS": FS, "depth": maxdepth, "depth_bound": bd,
            "nodes": len(nodes), "log2_node_bound": round(math.log2(bs), 1)}

# ---- test proofs ----
def lit(v, val): return (1 << v, val)

def tseitin_proof(nv, E, rows_first=True):
    """Odd Tseitin: per vertex download its clauses, infer the parity row (1 form), delete clauses,
    add into a running sum row. Memory: one vertex's clauses + 2 rows."""
    inc = [[e for e, (u, w) in enumerate(E) if v in (u, w)] for v in range(nv)]
    charge = [1] + [0] * (nv - 1); axioms = []; steps = []; acc = None
    for v in range(nv):
        cls = []
        for z in itertools.product((0, 1), repeat=len(inc[v])):
            if (sum(z) & 1) != charge[v]: cls.append([lit(e, 1 - zi) for e, zi in zip(inc[v], z)])
        axioms += cls
        for c in cls: steps.append(("ax", c))
        row = [(sum(1 << e for e in inc[v]), charge[v])]
        steps.append(("inf", row))
        for c in cls: steps.append(("del", c))
        if acc is None: acc = row
        else:
            m = acc[0][0] ^ row[0][0]; b = acc[0][1] ^ row[0][1]
            new = [(m, b)] if m else ([] if b else None)
            steps.append(("inf", new)); steps.append(("del", acc)); steps.append(("del", row)); acc = new
    return len(E), steps, axioms

def chain_proof(n):
    """x0, (x_i -> x_{i+1}), not x_{n-1}: resolution, memory 2 clauses, depth n bottom-up."""
    axioms = [[lit(0, 1)]] + [[lit(i, 0), lit(i + 1, 1)] for i in range(n - 1)] + [[lit(n - 1, 0)]]
    steps = [("ax", axioms[0])]; cur = axioms[0]
    for i in range(n - 1):
        steps += [("ax", axioms[i + 1]), ("inf", [lit(i + 1, 1)]), ("del", axioms[i + 1]), ("del", cur)]
        cur = [lit(i + 1, 1)]
    steps += [("ax", axioms[-1]), ("inf", [])]
    return n, steps, axioms

GR = {"K4": (4, [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]),
      "K33": (6, [(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5)]),
      "cube": (8, [(0,1),(1,3),(3,2),(2,0),(4,5),(5,7),(7,6),(6,4),(0,4),(1,5),(2,6),(3,7)])}

def region(sigma):
    """exponent e with log2(time) >= n^e forced at form space n^sigma (w = Theta(n), constants dropped)."""
    return round(2 - 2 * sigma, 4) if sigma >= 2 / 3 else round(1 - sigma / 2, 4)

def main():
    out = {"id": "WCD-FLMV-0001", "tests": {}}
    for name, (nv, E) in GR.items():
        n, steps, ax = tseitin_proof(nv, E)
        cfgs, kinds = build_configs(n, steps, ax)
        out["tests"]["tseitin_" + name] = convert_and_check(n, cfgs, kinds, ax)
    for n in (8, 14):
        n_, steps, ax = chain_proof(n)
        cfgs, kinds = build_configs(n_, steps, ax)
        out["tests"]["chain_%d" % n] = convert_and_check(n_, cfgs, kinds, ax)
    out["flmv_box"] = {"t_lt": 241 / 200, "s_lt": 11642479 / 23232400}
    out["forced_log_time_exponent_at_space_exponent"] = {str(s): region(s) for s in
        (0.0, 0.25, 0.5, round(11642479 / 23232400, 4), 2 / 3, 0.75, 0.9, 1.0)}
    out["seconds"] = round(time.time() - T0, 2)
    json.dump(out, sys.stdout, indent=1, sort_keys=True); print()

if __name__ == "__main__": main()
