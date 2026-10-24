#!/usr/bin/env python3
"""Exact finite controls for PINNED-CHILD-SEPARATOR124.

Standard library only.  The symbolic theorem is in the companion report;
these computations check serialization, SAT labels, first differing window,
and hostile promise escapes on finite instances.
"""
from __future__ import annotations

import hashlib
import json
import math
import time


def force(lit: int, a: int, b: int):
    return [(lit, sa * a, sb * b) for sa in (1, -1) for sb in (1, -1)]


def family(M: int, sat: bool):
    assert M >= 16 and M & (M - 1) == 0
    m = (M - 6) // 2
    a0, b0, am, bm = 2 * m, 2 * m + 1, 2 * m + 2, 2 * m + 3
    clauses = force(1, a0, b0)
    for i in range(1, m):
        clauses += [(-i, i + 1, m + i), (-i, i + 1, -(m + i))]
    clauses += force(-m, am, bm)
    if sat:
        clauses[-4] = (-m, am, 1)
    assert len(clauses) == M and len(set(clauses)) == M
    return dict(n=M - 3, m=m, am=am, bm=bm, clauses=clauses)


def simplify(clauses, var, value):
    true_lit = var if value else -var
    false_lit = -true_lit
    out = []
    for clause in clauses:
        if true_lit in clause:
            continue
        reduced = tuple(l for l in clause if l != false_lit)
        if not reduced:
            return None
        out.append(reduced)
    return out


def dpll(clauses):
    clauses = [tuple(c) for c in clauses]
    while True:
        if not clauses:
            return True
        if any(len(c) == 0 for c in clauses):
            return False
        units = [c[0] for c in clauses if len(c) == 1]
        if units:
            lit = units[0]
            nxt = simplify(clauses, abs(lit), lit > 0)
            if nxt is None:
                return False
            clauses = nxt
            continue
        counts = {}
        for c in clauses:
            for lit in c:
                counts.setdefault(abs(lit), set()).add(lit > 0)
        pure = next((v for v, signs in counts.items() if len(signs) == 1), None)
        if pure is not None:
            val = next(iter(counts[pure]))
            nxt = simplify(clauses, pure, val)
            if nxt is None:
                return False
            clauses = nxt
            continue
        var = abs(clauses[0][0])
        left = simplify(clauses, var, False)
        if left is not None and dpll(left):
            return True
        right = simplify(clauses, var, True)
        return right is not None and dpll(right)


def width(n: int, m: int):
    return (64 * (n + m + 1) - 1).bit_length()


def enc_len(n: int, m: int):
    return (4 * m + 2) * width(n, m)


def literal_code(lit: int):
    return 2 * abs(lit) + int(lit < 0)


def child_indices(M: int, K: int, j: int):
    return tuple((j * K + i) % M for i in range(K))


def pin_gadgets(n: int, m: int, am: int, bm: int):
    # Pin x_m=1, a_m=0, b_m=0 using three ordinary proper-3CNF unit blocks.
    pins = []
    for k, lit in enumerate((m, -am, -bm)):
        pins += force(lit, n + 2 * k + 1, n + 2 * k + 2)
    return pins


def scheduled_child(data, K: int, j: int, pinned: bool):
    C = [data["clauses"][i] for i in child_indices(len(data["clauses"]), K, j)]
    if pinned:
        C += pin_gadgets(data["n"], data["m"], data["am"], data["bm"])
    return C


def exact_row(M: int):
    F, G = family(M, False), family(M, True)
    N = enc_len(F["n"], M)
    raw = int(math.sqrt(N) / math.log2(N))
    K = max(3, raw if raw % 2 else raw + 1)
    Q = min(M, int(N ** 0.6))
    assert math.gcd(M, K) == 1 and 2 * K <= M and K < M
    changed = M - 4
    jstar = changed // K
    assert jstar < Q and changed in child_indices(M, K, jstar)

    checks = 0
    # Unpinned deletion children remain SAT on both labels.
    for j in range(Q):
        assert dpll(scheduled_child(F, K, j, False))
        assert dpll(scheduled_child(G, K, j, False))
        checks += 2

    # Before j*, encodings (not only statuses) coincide.  At j*, three
    # fixed pins falsify the F-only clause; the G child remains satisfiable.
    for j in range(jstar):
        assert child_indices(M, K, j).count(changed) == 0
        assert scheduled_child(F, K, j, True) == scheduled_child(G, K, j, True)
        assert dpll(scheduled_child(F, K, j, True))
        checks += 3
    assert not dpll(scheduled_child(F, K, jstar, True))
    assert dpll(scheduled_child(G, K, jstar, True))
    checks += 2

    # A restricted controller may jump directly to j*.  Reading the one
    # changed literal field after canonical recognition is cheaper still.
    code_f = literal_code(F["bm"])
    code_g = literal_code(1)
    source_field_hamming = (code_f ^ code_g).bit_count()
    assert source_field_hamming >= 1
    checks += 1

    n_pin, m_pin = F["n"] + 6, K + 12
    return dict(
        M=M, n=F["n"], N=N, K=K, Q=Q, changed_clause_index=changed,
        first_differing_window=jstar, prefix_queries=jstar + 1,
        direct_jump_queries=1, unpinned_child_bits=enc_len(F["n"], K),
        pinned_child_bits=enc_len(n_pin, m_pin), pin_blocks=3,
        added_clauses=12, added_variables=6,
        changed_source_literal_field_hamming=source_field_hamming,
        checks=checks,
    )


def hostile_controls():
    # SAT parent made UNSAT by an incompatible pin: a pinned child answer is
    # not a parent label on unrestricted inputs.
    sat_parent = force(-1, 2, 3)
    sat_child = sat_parent + force(1, 4, 5)
    # UNSAT parent whose selected strict child is SAT.
    unsat_parent = force(1, 2, 3) + force(-1, 4, 5)
    unsat_child = force(1, 2, 3) + force(1, 6, 7)
    result = dict(
        sat_parent=dpll(sat_parent),
        sat_parent_pinned_child=dpll(sat_child),
        unsat_parent=dpll(unsat_parent),
        unsat_parent_selected_child=dpll(unsat_child),
    )
    assert result == dict(sat_parent=True, sat_parent_pinned_child=False,
                          unsat_parent=False, unsat_parent_selected_child=True)
    return result


def horn_forward(clauses):
    rules = []
    for clause in clauses:
        pos = [lit for lit in clause if lit > 0]
        assert len(pos) <= 1
        body = frozenset(-lit for lit in clause if lit < 0)
        head = pos[0] if pos else None
        rules.append((body, head))
    true = set()
    changed = True
    while changed:
        changed = False
        for body, head in rules:
            if body <= true:
                if head is None:
                    return False
                if head not in true:
                    true.add(head)
                    changed = True
    return True


def two_sat_scc(clauses):
    vars_ = sorted({abs(l) for c in clauses for l in c})
    nodes = [l for v in vars_ for l in (v, -v)]
    graph = {l: [] for l in nodes}
    rev = {l: [] for l in nodes}
    for clause in clauses:
        assert 1 <= len(clause) <= 2
        a, b = (clause[0], clause[-1])
        for u, v in ((-a, b), (-b, a)):
            graph[u].append(v)
            rev[v].append(u)
    seen, order = set(), []
    def dfs(u):
        seen.add(u)
        for v in graph[u]:
            if v not in seen:
                dfs(v)
        order.append(u)
    for u in nodes:
        if u not in seen:
            dfs(u)
    comp = {}
    def rdfs(u, k):
        comp[u] = k
        for v in rev[u]:
            if v not in comp:
                rdfs(v, k)
    for u in reversed(order):
        if u not in comp:
            rdfs(u, len(comp))
    return all(comp[v] != comp[-v] for v in vars_)


def affine_gaussian(equations, nvars):
    rows = [[(mask >> i) & 1 for i in range(nvars)] + [rhs]
            for mask, rhs in equations]
    r = 0
    for c in range(nvars):
        pivot = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                rows[i] = [a ^ b for a, b in zip(rows[i], rows[r])]
        r += 1
    return not any(not any(row[:-1]) and row[-1] for row in rows)


def adaptive_controls():
    # A finite experimental policy menu, explicitly not all-decider coverage.
    F, G = family(16, False), family(16, True)
    all8 = [tuple(((-1 if (a >> i) & 1 else 1) * (i + 1))
                  for i in range(3)) for a in range(8)]
    cases = [
        ("canonical-direct-field", dpll(G["clauses"]), True),
        ("canonical-direct-field", dpll(F["clauses"]), False),
        ("Horn-forward", horn_forward([(-1, 2), (-2, 3)]), True),
        ("Horn-forward", horn_forward([(1,), (-1,)]), False),
        ("SCC-2SAT", two_sat_scc([(1, 2), (-1, 2)]), True),
        ("SCC-2SAT", two_sat_scc([(1,), (-1,)]), False),
        ("affine-Gaussian", affine_gaussian([(0b11, 0)], 2), True),
        ("affine-Gaussian", affine_gaussian([(0b11, 0), (0b11, 1)], 2), False),
        ("DPLL-fallback", dpll(all8[:-1]), True),
        ("DPLL-fallback", dpll(all8), False),
    ]
    counts = {}
    failures = 0
    for rule, got, expected in cases:
        failures += got != expected
        key = f"{rule}_{'SAT' if expected else 'UNSAT'}"
        counts[key] = counts.get(key, 0) + 1
    assert failures == 0
    return dict(cases=len(cases), failures=failures, rule_label_counts=counts,
                warning="finite declared policy menu, not coverage of every SAT algorithm")


def main():
    start = time.perf_counter()
    rows = [exact_row(M) for M in (16, 32, 64, 128, 256, 1024, 4096)]
    result = dict(
        run_id="PINNED-CHILD-SEPARATOR124",
        status="PASS",
        rows=rows,
        total_assertion_accounted_checks=sum(r["checks"] for r in rows) + 4 + 10,
        hostile_controls=hostile_controls(),
        adaptive_controls=adaptive_controls(),
        symbolic_claim=(
            "For j<floor((M-4)/K), the pinned F/G child encodings coincide; "
            "at j*=floor((M-4)/K), pins x_m=1,a_m=0,b_m=0 make F UNSAT "
            "and leave G SAT. This is restricted-promise separation only."
        ),
        all_input_ARC_successor="OPEN",
        P_versus_NP="OPEN",
    )
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["canonical_payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    result["elapsed_seconds"] = round(time.perf_counter() - start, 6)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
