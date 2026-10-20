"""Verify MINIMAL-UNSAT-PROJECTION20 F_m/G_m and probe the boundary-witness repair:
deletion witnesses of a minimally-UNSAT formula violate EXACTLY the deleted clause,
while deletion children of the SAT twin G_m admit a witness violating NO clause."""
import itertools, json, sys

def build(m, twin):
    # vars: x1..xm = 1..m ; a_i,b_i for i in {0,m}: ; c_i
    nv = [0]
    def new():
        nv[0] += 1; return nv[0]
    x = [None] + [new() for _ in range(m)]
    a0, b0, am, bm = new(), new(), new(), new()
    c = [None] + [new() for _ in range(m - 1)]
    cl = []
    for s in (1, -1):
        for t in (1, -1):
            cl.append((x[1], s * a0, t * b0))
    for i in range(1, m):
        cl.append((-x[i], x[i + 1], c[i])); cl.append((-x[i], x[i + 1], -c[i]))
    for s in (1, -1):
        for t in (1, -1):
            cl.append((-x[m], s * am, t * bm))
    if twin:
        k = cl.index((-x[m], am, bm)); cl[k] = (-x[m], am, x[1])
    return nv[0], cl

def sat_assignments(n, cl, skip=None):
    for bits in range(1 << n):
        ok = True; viol = []
        for j, C in enumerate(cl):
            if not any((bits >> (abs(l) - 1) & 1) == (l > 0) for l in C):
                viol.append(j)
        yield bits, viol

def solve(n, cl, skip=()):
    # DPLL-free brute force is fine for n<=19; use incremental check on violations
    for bits, viol in sat_assignments(n, cl):
        if all(v in skip for v in viol):
            return bits, viol
    return None

out = {}
for m in range(2, 7):
    row = {}
    for twin in (False, True):
        n, cl = build(m, twin)
        assert len(set(cl)) == len(cl) == 2 * m + 6 and n == 2 * m + 3
        full = solve(n, cl)
        dels = []
        for j in range(len(cl)):
            w = solve(n, cl, skip=(j,))
            dels.append(None if w is None else w[1])
        row['twin' if twin else 'F'] = dict(SAT=full is not None,
            all_deletions_sat=all(d is not None for d in dels),
            witness_violation_sets=[d for d in dels])
    # claims
    assert not row['F']['SAT'] and row['twin']['SAT']
    assert row['F']['all_deletions_sat'] and row['twin']['all_deletions_sat']
    # boundary-witness probe: minimum violation set over ALL witnesses
    row['F_exact'] = all(v == [j] for j, v in enumerate(row['F']['witness_violation_sets']))
    row['twin_exists_zero_violation_witness'] = row['twin']['SAT']
    out[m] = {k: row[k] for k in ('F_exact', 'twin_exists_zero_violation_witness')}
    out[m]['F_SAT'] = row['F']['SAT']; out[m]['G_SAT'] = row['twin']['SAT']
    print(m, out[m]); sys.stdout.flush()
json.dump(out, open('results/2026-10-20/2026-10-20_minunsat_exact_violation_probe.json', 'w'), indent=1)
