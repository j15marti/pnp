#!/usr/bin/env python3
"""LSPV-3 paired-extreme compact independent spotcheck; Python stdlib only.
All clauses and S/U demands retain original source IDs. No value scores.
Run: python 2026-10-29_2228_LSPV-3_PAIRED-EXTREME-CONTROLLER241_spotcheck.py
"""
import itertools
import json

def lit_truth(z, assignment):
    return assignment[abs(z)] == int(z > 0)

def count(c, assignment):
    return sum(lit_truth(z, assignment) for z in c)

def local(c, mode):
    # S means every literal true, U every literal false.
    return {abs(z): int(z > 0) if mode == "S" else int(z < 0) for z in c}

def compatible(c, d, modes):
    a = local(c, modes[0])
    b = local(d, modes[1])
    return all(i not in a or a[i] == v for i, v in b.items())

def matrix(c, d):
    # Source-indexed SS/SU/US/UU, not disjunctive SAT.
    shared = set(map(abs, c)) & set(map(abs, d))
    sign_c = {abs(z): int(z > 0) for z in c}
    sign_d = {abs(z): int(z > 0) for z in d}
    same = any(sign_c[i] == sign_d[i] for i in shared)
    opposite = any(sign_c[i] != sign_d[i] for i in shared)
    return {"SS": not opposite, "SU": not same,
            "US": not same, "UU": not opposite}

def paired(binary):
    # Fresh pivot j+3 for binary clause j; core variables 1 and 2.
    out = []
    for j, d in enumerate(binary):
        p = j + 3
        out.extend([tuple(d) + (p,), tuple(d) + (-p,)])
    return tuple(out)

def all_full(n):
    for mask in range(1 << n):
        yield {i + 1: (mask >> i) & 1 for i in range(n)}

def sat(F, a):
    return all(count(c, a) > 0 for c in F)

def up(F, assignment):
    a = dict(assignment)
    while True:
        change = False
        for c in F:
            if any(abs(z) in a and lit_truth(z, a) for z in c):
                continue
            u = [z for z in c if abs(z) not in a]
            if not u:
                return None
            if len(u) == 1:
                z = u[0]
                a[abs(z)] = int(z > 0)
                change = True
        if not change:
            return a

def dpll_nodes(F, order):
    nodes = 0
    def rec(a):
        nonlocal nodes
        nodes += 1
        a = up(F, a)
        if a is None:
            return False
        if all(any(abs(z) in a and lit_truth(z, a) for z in c) for c in F):
            return True
        v = next(i for i in order if i not in a)
        for value in (0, 1):
            b = dict(a); b[v] = value
            if rec(b):
                return True
        return False
    outcome = rec({})
    return outcome, nodes

def run():
    clauses = []
    for ids in itertools.combinations(range(1, 5), 3):
        for signs in itertools.product((-1, 1), repeat=3):
            clauses.append(tuple(i*s for i, s in zip(ids, signs)))
    checks = 0
    full = list(all_full(4))
    for c, d in itertools.combinations(clauses, 2):
        expected = matrix(c, d)
        for modes, should in expected.items():
            seen = any(count(c, a) == (3 if modes[0] == "S" else 0)
                       and count(d, a) == (3 if modes[1] == "S" else 0)
                       for a in full)
            assert should == seen == compatible(c, d, modes)
            checks += 1

    # Both kinds of shared signs, therefore every extreme mode impossible.
    C0, C1 = (1, 2, 3), (1, 2, -3)
    assert not any(matrix(C0, C1).values())
    a = {1: 1, 2: 0, 3: 0}
    assert count(C0, a) > 0 and count(C1, a) > 0

    G = ((1,2),(1,-2),(-1,2),(-1,-2))
    rows = []
    for M in (4, 5, 6, 7, 8):
        base = G + ((1,2),) * (M-4)
        F = paired(base)
        n = M + 2
        assert all(len(c) == 3 and len(set(map(abs, c))) == 3 for c in F)
        # Each pair shares the same-sign core and opposite-sign pivot.
        assert all(not any(matrix(F[2*j], F[2*j+1]).values())
                   for j in range(M))
        for assignment in all_full(n):
            core = {1: assignment[1], 2: assignment[2]}
            assert sat(F, assignment) == sat(base, core)
        b_sat, b_nodes = dpll_nodes(F, list(range(3,n+1))+[1,2])
        c_sat, c_nodes = dpll_nodes(F, [1,2]+list(range(3,n+1)))
        assert not b_sat and not c_sat
        assert b_nodes == (1 << (M+2)) - 1
        assert c_nodes == 7
        rows.append({"M":M,"baseline_pivot_first_nodes":b_nodes,
                     "core_first_nodes":c_nodes,
                     "source_pair_all_modes_incompatible":True,
                     "source_binary_resolvents":M})

    # Exact original occurrence example, including inversion and legal flip.
    F = ((1,2,3),(1,2,-3))
    source = []
    for j,c in enumerate(F):
        s = local(c,"S"); u=local(c,"U")
        assert all(1-v == u[i] for i,v in s.items())
        source.append({"source_clause_index":j,"signed_literals":c,
                       "S_all_true":s,"invert_S_to_U":{i:1-v for i,v in s.items()},
                       "U_all_false":u,"invert_U_to_S":{i:1-v for i,v in u.items()},
                       "occurrences":[{"x_ij":f"x_{abs(z)},{j}",
                         "sign":"+" if z>0 else "-",
                         "preferred_S":s[abs(z)],"preferred_U":u[abs(z)]}
                         for z in c]})
    trail = []
    for bits in ((0,0,0),(1,1,1),(1,0,0),(0,1,1)):
        a = dict(enumerate(bits,1))
        counts = [count(c,a) for c in F]
        trail.append({"assignment":bits,"t_by_source_index":counts,
                      "N0123":[counts.count(k) for k in range(4)]})
    assert [r["t_by_source_index"] for r in trail] == [[0,1],[3,2],[1,2],[2,1]]
    print(json.dumps({"pair_matrix_exact_truth_checks":checks,
                      "local_occurrence_controls":source,
                      "complete_and_flip_trail":trail,
                      "unsat_paired_2sat_controls":rows,
                      "status":"COMPUTATIONAL controls; restricted theorem needs symbolic proof",
                      "P_vs_NP":"OPEN"},indent=2))
if __name__ == "__main__":
    run()
