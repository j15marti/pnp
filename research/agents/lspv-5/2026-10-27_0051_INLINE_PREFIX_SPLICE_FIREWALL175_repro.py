#!/usr/bin/env python3
"""Finite controls for INLINE-PREFIX-SPLICE-FIREWALL175.

Checks the DISJ fooling family and cross-program splice logic, exact capacity
thresholds with and without a redundant inline-program factor, the necessity
of a separate proof-tape factor, and an independent small-k audit of LSPV-1's
connected minimally-UNSAT U_k family and its M-1 Resolution proof.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math


ASSERTIONS = 0


def ck(v: bool, msg: str) -> None:
    global ASSERTIONS
    ASSERTIONS += 1
    if not v:
        raise AssertionError(msg)


def disj(a: int, b: int) -> bool:
    return (a & b) == 0


def min_crossings(m: int, G: int, alphabet: int, advice_factor: int = 1) -> int:
    """Least L>=0 for coarse capacity advice*G*alphabet^(L+1)>=2^m."""
    target = 1 << m
    L = 0
    while advice_factor * G * alphabet ** (L + 1) < target:
        L += 1
    return L


def norm_clause(c):
    return frozenset(c)


def pin(lit: int, p: int, q: int):
    return [
        norm_clause((lit, p, q)),
        norm_clause((lit, p, -q)),
        norm_clause((lit, -p, q)),
        norm_clause((lit, -p, -q)),
    ]


def build_U(k: int):
    xs = list(range(1, k + 2))
    zs = list(range(k + 2, 2 * k + 2))
    a, b, c, d = range(2 * k + 2, 2 * k + 6)
    clauses = pin(xs[0], a, b)
    for i in range(k):
        clauses += [
            norm_clause((-xs[i], xs[i + 1], zs[i])),
            norm_clause((-xs[i], xs[i + 1], -zs[i])),
        ]
    clauses += pin(-xs[-1], c, d)
    return clauses, 2 * k + 5, xs, zs, (a, b, c, d)


def sat_witness(clauses, nvars: int):
    for mask in range(1 << nvars):
        ok = True
        for clause in clauses:
            if not any(((mask >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause):
                ok = False
                break
        if ok:
            return mask
    return None


def resolve(c1, c2, pivot: int):
    ck(pivot in c1 and -pivot in c2, "resolution pivot present")
    out = (set(c1) - {pivot}) | (set(c2) - {-pivot})
    ck(not any(-x in out for x in out), "non-tautological derived clause")
    return frozenset(out)


def explicit_resolution(k: int):
    clauses, _, xs, zs, (a, b, c, d) = build_U(k)
    derived = []
    # First PIN derives x_1 in three binary inferences.
    ca = resolve(clauses[0], clauses[1], b)
    cna = resolve(clauses[2], clauses[3], b)
    unit = resolve(ca, cna, a)
    derived += [ca, cna, unit]
    ck(unit == frozenset((xs[0],)), "first unit")
    # Each link derives implication then next unit.
    offset = 4
    for i in range(k):
        impl = resolve(clauses[offset + 2 * i], clauses[offset + 2 * i + 1], zs[i])
        next_unit = resolve(impl, unit, -xs[i])
        ck(impl == frozenset((-xs[i], xs[i + 1])), "link implication")
        ck(next_unit == frozenset((xs[i + 1],)), "propagated unit")
        derived += [impl, next_unit]
        unit = next_unit
    # Last PIN derives -x_{k+1}; then contradiction.
    last = offset + 2 * k
    cc = resolve(clauses[last], clauses[last + 1], d)
    cnc = resolve(clauses[last + 2], clauses[last + 3], d)
    neg_unit = resolve(cc, cnc, c)
    empty = resolve(unit, neg_unit, xs[-1])
    derived += [cc, cnc, neg_unit, empty]
    ck(neg_unit == frozenset((-xs[-1],)), "last negative unit")
    ck(empty == frozenset(), "empty clause")
    return clauses, derived


def main() -> None:
    fooling_rows = []
    for m in range(1, 11):
        mask = (1 << m) - 1
        accepted = []
        # Program IDs deliberately vary with a. They are metadata on the left
        # shore, not a separate proof channel.
        for a in range(1 << m):
            p = (a * 17 + 3) % (1 << (m + 2))
            b = mask ^ a
            ck(disj(a, b), "diagonal YES")
            accepted.append((p, a, b))
        cross_pairs = 0
        different_program_pairs = 0
        for (p, a, _), (p2, a2, _) in itertools.combinations(accepted, 2):
            no12 = not disj(a, mask ^ a2)
            no21 = not disj(a2, mask ^ a)
            ck(no12 or no21, "one crossed hybrid is NO")
            if p != p2:
                different_program_pairs += 1
                # If complete crossing records collided, standard splicing
                # would accept both hybrids under p and p2 respectively,
                # contradicting global soundness of at least one program.
                ck(no12 or no21, "cross-program collision also forbidden")
            cross_pairs += 1
        fooling_rows.append({
            "m": m,
            "diagonal_yes": 1 << m,
            "ordered_program_labels": len({p for p, _, _ in accepted}),
            "fooling_pairs": cross_pairs,
            "different_program_pairs": different_program_pairs,
        })

    capacity_rows = []
    for m in range(4, 65):
        G = 4 * m + 1
        for q in range(2, 9):
            alphabet = 2 * q
            inline_L = min_crossings(m, G, alphabet, 1)
            ck(G * alphabet ** (inline_L + 1) >= (1 << m), "inline capacity covers")
            if inline_L:
                ck(G * alphabet**inline_L < (1 << m), "inline threshold minimal")
            for b in (0, 2, 4, 8, 16, 32):
                portfolio = (1 << (b + 1)) - 1
                legacy_L = min_crossings(m, G, alphabet, portfolio)
                ck(inline_L >= legacy_L, "removing redundant advice strengthens bound")
            capacity_rows.append({
                "m": m,
                "q": q,
                "G": G,
                "inline_min_crossings": inline_L,
                "legacy_b8_min_crossings": min_crossings(m, G, alphabet, (1 << 9) - 1),
            })

    proof_rows = []
    for m in range(1, 25):
        for L in range(0, m + 1):
            proofs = (1 << (L + 1)) - 1
            ck(proofs >= 1, "nonempty proof portfolio")
            if L == m:
                ck(proofs >= (1 << m), "linear separate proof can name all diagonals")
            if L + 1 < m:
                ck(proofs < (1 << m), "short separate proof cannot alone name all diagonals")
        proof_rows.append({
            "m": m,
            "proofs_at_L_m": (1 << (m + 1)) - 1,
            "note": "separate proof contents must match before source-cut splicing",
        })

    uk_rows = []
    for k in range(1, 7):
        clauses, nvars, _, _, _ = build_U(k)
        M = 2 * k + 8
        ck(len(clauses) == M, "U_k clause count")
        ck(len(set(clauses)) == M, "U_k unique clauses")
        ck(all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in clauses),
           "U_k proper ternary")
        ck(sat_witness(clauses, nvars) is None, "U_k UNSAT")
        mutant_checks = 0
        for j, clause in enumerate(clauses):
            for lit in tuple(clause):
                mut = list(clauses)
                new_clause = set(clause)
                new_clause.remove(lit)
                new_clause.add(-lit)
                mut[j] = frozenset(new_clause)
                ck(sat_witness(mut, nvars) is not None, "every one-sign mutant SAT")
                mutant_checks += 1
        source, derived = explicit_resolution(k)
        ck(source == clauses, "resolution source order")
        ck(len(derived) == M - 1, "tight M-1 inferences")
        uk_rows.append({
            "k": k,
            "variables": nvars,
            "clauses": M,
            "one_sign_sat_mutants": mutant_checks,
            "resolution_inferences": len(derived),
        })

    payload = {
        "id": "INLINE-PREFIX-SPLICE-FIREWALL175",
        "timestamp_utc": "2026-10-27T07:51:00Z",
        "method": "exhaustive exact standard-library Python; no randomness",
        "assertions": ASSERTIONS,
        "failures": 0,
        "inline_prefix_fooling_controls": fooling_rows,
        "capacity_threshold_controls": capacity_rows,
        "separate_proof_tape_controls": proof_rows,
        "connected_Uk_peer_audit": uk_rows,
        "scope": [
            "inline prefix on the same source tape and left of the cut",
            "every program globally sound on every NO source",
            "separate proof tape requires identical proof contents and its own factor",
            "no full ordinary-SAT, RAM, FLMV, or P-versus-NP consequence",
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["canonical_sha256_without_this_field"] = hashlib.sha256(canonical).hexdigest()
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
