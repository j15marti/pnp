#!/usr/bin/env python3
"""Finite controls for PROJECTION-IDEMPOTENCE-REFEREE191.

Exact private-variable projection for mixed 2CNF/GF(2), fixed-boundary
idempotence, and the unsoundness of separately forgetting a shared variable.
Dependency-free; prints canonical JSON.
"""
from __future__ import annotations

import collections
import itertools
import json
import random

A = collections.Counter()


def ck(cond, tag):
    A["assertions"] += 1
    if not cond:
        raise AssertionError(tag)


def lit_key(x):
    return (abs(x), x < 0)


def canon_clauses(clauses):
    out = set()
    for clause in clauses:
        s = set(clause)
        if any(-x in s for x in s):
            continue
        c = tuple(sorted(s, key=lit_key))
        ck(len(c) <= 2, "2CNF width")
        out.add(c)
    if () in out:
        return ((),)
    return tuple(sorted(out, key=lambda c: (len(c), tuple(map(lit_key, c)))))


def project_2cnf(clauses, n, keep):
    cur = canon_clauses(clauses)
    pairs = resolvents = 0
    for v in sorted(set(range(n)) - set(keep)):
        if cur == ((),):
            break
        p, q = v + 1, -(v + 1)
        pos = [c for c in cur if p in c]
        neg = [c for c in cur if q in c]
        rest = [c for c in cur if p not in c and q not in c]
        made = []
        for cp in pos:
            for cn in neg:
                pairs += 1
                r = (set(cp) - {p}) | (set(cn) - {q})
                if any(-x in r for x in r):
                    continue
                made.append(tuple(r))
                resolvents += 1
        cur = canon_clauses(rest + made)
    return cur, {"candidate_pairs": pairs, "resolvents": resolvents}


def rref_rows(rows, n, column_order):
    work = []
    for support, rhs in rows:
        mask = sum(1 << v for v in support)
        work.append([mask, int(rhs) & 1])
    r = 0
    xors = 0
    for col in column_order:
        pivot = next((i for i in range(r, len(work)) if work[i][0] >> col & 1), None)
        if pivot is None:
            continue
        work[r], work[pivot] = work[pivot], work[r]
        for j in range(len(work)):
            if j != r and (work[j][0] >> col & 1):
                work[j][0] ^= work[r][0]
                work[j][1] ^= work[r][1]
                xors += 1
        r += 1
    return work, xors


def project_affine(rows, n, keep):
    keep = set(keep)
    private = sorted(set(range(n)) - keep)
    work, x1 = rref_rows(rows, n, private + sorted(keep))
    private_mask = sum(1 << v for v in private)
    if any(mask == 0 and rhs for mask, rhs in work):
        return ((frozenset(), 1),), {"row_xors": x1, "inconsistent": True}
    constraints = []
    for mask, rhs in work:
        if mask and not (mask & private_mask):
            constraints.append((frozenset(v for v in keep if mask >> v & 1), rhs))
    work2, x2 = rref_rows(constraints, n, sorted(keep))
    if any(mask == 0 and rhs for mask, rhs in work2):
        return ((frozenset(), 1),), {"row_xors": x1 + x2, "inconsistent": True}
    out = []
    for mask, rhs in work2:
        if mask:
            out.append((frozenset(v for v in keep if mask >> v & 1), rhs))
    out.sort(key=lambda row: (min(row[0]), tuple(sorted(row[0])), row[1]))
    return tuple(out), {"row_xors": x1 + x2, "inconsistent": False}


def project_private(C, R, n, boundary):
    """Sound when boundary contains every variable shared by C and R."""
    cs, cstat = project_2cnf(C, n, boundary)
    rs, rstat = project_affine(R, n, boundary)
    return (cs, rs), {**cstat, **rstat}


def support_c(C):
    return {abs(l) - 1 for c in C for l in c}


def support_r(R):
    return set().union(*(set(s) for s, _ in R)) if R else set()


def sat_clause(c, assignment):
    return any(assignment[abs(l) - 1] == (l > 0) for l in c)


def sat_mixed(C, R, assignment):
    return (all(sat_clause(c, assignment) for c in C) and
            all((sum(assignment[v] for v in s) & 1) == rhs for s, rhs in R))


def relation(C, R, n, boundary):
    boundary = tuple(sorted(boundary))
    out = set()
    for bits in itertools.product((0, 1), repeat=n):
        if sat_mixed(C, R, bits):
            out.add(tuple(bits[v] for v in boundary))
    return out


def child_relation(C, R, n, boundary):
    boundary = tuple(sorted(boundary))
    out = set()
    for bits in itertools.product((0, 1), repeat=len(boundary)):
        full = [0] * n
        for v, bit in zip(boundary, bits):
            full[v] = bit
        if sat_mixed(C, R, full):
            out.add(bits)
    return out


def encode(C, R, n, boundary):
    lines = [f"MIX {n} {len(C)} {len(R)}", "B " + " ".join(str(v + 1) for v in sorted(boundary))]
    lines += ["C " + " ".join(map(str, c)) + " 0" for c in C]
    lines += ["A " + " ".join(str(v + 1) for v in sorted(s)) + f" = {rhs}" for s, rhs in R]
    return ("\n".join(lines) + "\n").encode()


def k_instance(b, rhs):
    C = tuple((i + 1, (i + 1) % b + 1) for i in range(b))
    R = tuple((frozenset({i}), rhs) for i in range(b))
    return canon_clauses(C), R


def padded_k(b, rhs, copies):
    C, R = k_instance(b, rhs)
    C, R = list(C), list(R)
    nxt = b
    for z in range(b):
        for _ in range(copies):
            u = nxt
            v = nxt + 1
            nxt += 2
            C.extend(((z + 1, u + 1), (-(z + 1), -(u + 1))))
            R.append((frozenset({z, v}), 0))
    return canon_clauses(C), tuple(R), nxt


rng = random.Random(20261028)
random_cases = 0
for n in range(1, 7):
    for _ in range(80):
        C = []
        for __ in range(rng.randrange(0, 2 * n + 2)):
            width = rng.randrange(0, min(2, n) + 1)
            vs = rng.sample(range(n), width)
            C.append(tuple((v + 1) * rng.choice((-1, 1)) for v in vs))
        R = []
        for __ in range(rng.randrange(0, n + 2)):
            s = frozenset(v for v in range(n) if rng.randrange(2))
            R.append((s, rng.randrange(2)))
        C, R = canon_clauses(C), tuple(R)
        shared = support_c(C) & support_r(R)
        # A valid private projection must retain every shared variable.
        boundary = shared | {v for v in range(n) if rng.random() < .35}
        (pc, pr), _ = project_private(C, R, n, boundary)
        ck(relation(C, R, n, boundary) == child_relation(pc, pr, n, boundary), "exact private projection")
        (pc2, pr2), _ = project_private(pc, pr, n, boundary)
        ck((pc2, pr2) == (pc, pr), "fixed-boundary idempotence")
        random_cases += 1


# Minimal shared-variable falsifier: each component alone is satisfiable after
# forgetting z, but their conjunction is not.
counter_C = ((1,),)
counter_R = ((frozenset({0}), 0),)
ck(not relation(counter_C, counter_R, 1, set()), "joint shared counterexample UNSAT")
(sep_C, sep_R), _ = project_private(counter_C, counter_R, 1, set())
ck(child_relation(sep_C, sep_R, 1, set()) == {()}, "separate forgetting counterfeit SAT")


fixed_rows = []
for b in (3, 4, 8, 16, 32, 64):
    for rhs, label in ((1, "SAT"), (0, "UNSAT")):
        C, R = k_instance(b, rhs)
        if b <= 8:
            truth = bool(relation(C, R, b, set()))
            ck(truth == (label == "SAT"), "K_b label")
        else:
            # Symbolic control: singleton affine rows force every z_i=rhs;
            # the positive cycle is true exactly for rhs=1.
            ck((rhs == 1) == (label == "SAT"), "K_b symbolic label")
        (pc, pr), _ = project_private(C, R, b, set(range(b)))
        ck((pc, pr) == (C, R), "K_b exact fixed point")
        # Unsafe separate deletion of all shared variables accepts both sides.
        (badc, badr), _ = project_private(C, R, b, set())
        ck(child_relation(badc, badr, b, set()) == {()}, "unsafe shared drop says SAT")
        P_C, P_R, pn = padded_k(b, rhs, 2)
        (fc, fr), _ = project_private(P_C, P_R, pn, set(range(b)))
        ck((fc, fr) == (C, R), "padded first projection")
        parent_bytes = len(encode(P_C, P_R, pn, set(range(b))))
        child_bytes = len(encode(C, R, b, set(range(b))))
        ck(parent_bytes > child_bytes, "first shrink")
        fixed_rows.append({
            "b": b,
            "label": label,
            "parent_bytes": parent_bytes,
            "first_child_bytes": child_bytes,
            "second_child_bytes": child_bytes,
            "separate_shared_drop_answer": "SAT",
            "correct_answer": label,
        })


out = {
    "run": "PROJECTION-IDEMPOTENCE-REFEREE191",
    "status": "PASS",
    "assertions": A["assertions"],
    "random_exact_projection_cases": random_cases,
    "fixed_point_rows": fixed_rows,
    "minimal_shared_drop_counterexample": {
        "two_cnf": "(z)",
        "affine": "z=0",
        "joint_projection": "FALSE",
        "separate_component_projections": "TRUE AND TRUE",
    },
    "symbolic_result": {
        "private_projection": "exact when every shared variable is retained",
        "same_boundary_second_projection": "idempotent after canonicalization",
        "shared_variable_componentwise_drop": "unsound",
    },
    "limitations": [
        "The fixed-point theorem constrains the declared projection compiler, not every SAT algorithm.",
        "A joint compatibility algorithm can escape; on unrestricted mixed 2CNF/XOR it is NP-complete.",
        "Finite truth tables and byte counts are not native TM transition measurements.",
        "No ordinary-SAT N^lambda successor or P-vs-NP separation is proved.",
    ],
}
print(json.dumps(out, indent=2, sort_keys=True))
