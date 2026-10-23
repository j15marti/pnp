#!/usr/bin/env python3
"""GAUGEFORK81, deterministic reproducibility audit (Python stdlib only).

Run from any directory inside a checkout of j15marti/pnp:
    python research/agents/lspv-1/2026-10-23_1201_GAUGEFORK81_minirepro.py

UNSAT(U) depends on the independently stored DOECKER-CORE-CERT61 projection
certificate. This script verifies the final 8-clause projected contradiction
but does not replay the six local projection certificates.
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt"
WITNESS_HEX = "39a2b53c16ab15bc16ab15ca4b9715c4faa7143d31b0f26598"
CORE = [
    (-194, 197), (-195, 196, -198), (193, -195, -197),
    (195, -197), (193, 194, -196), (-193, 198),
    (-193, -196, -198), (194, 196, 197),
]
assert SOURCE.exists(), "Fetch the project source file from the repository."

def read_source():
    content = SOURCE.read_text(encoding="utf8")
    return [tuple(c) for c in json.loads(content[content.index("[["):])]

def validate(F, n):
    assert len(F) * 3 == 4 * n
    assert len(set(F)) == len(F)
    signed = Counter(l for clause in F for l in clause)
    assert all(len(clause) == 3 and len({abs(l) for l in clause}) == 3
               for clause in F)
    assert all(signed[v] == signed[-v] == 2 for v in range(1, n + 1))

def false_clauses(F, assignment):
    return [i for i, clause in enumerate(F) if not any(
        (assignment[abs(l) - 1] == 1) == (l > 0) for l in clause)]

def first_positive_normalize(F, n):
    flip = {}
    for clause in F:
        for lit in clause:
            v = abs(lit)
            if v not in flip:
                flip[v] = lit < 0
    assert len(flip) == n
    return tuple(tuple(-l if flip[abs(l)] else l for l in c) for c in F)

def gauge_block(B, g, block):
    shift = 198 * block
    return [tuple(
        (-1 if (lit < 0) ^ bool(g[abs(lit) - 1]) else 1) *
        (shift + abs(lit)) for lit in clause) for clause in B]

def evaluate_core():
    counts = [0] * 8
    accepted = 0
    for a in range(64):
        ok = [any((((a >> (abs(l) - 193)) & 1) == 1) == (l > 0)
                  for l in clause) for clause in CORE]
        accepted += all(ok)
        for i in range(8):
            counts[i] += all(ok[j] for j in range(8) if j != i)
    assert accepted == 0
    assert counts == [8, 2, 4, 8, 4, 6, 4, 4]
    return counts

def main():
    U = read_source()
    V = list(U)
    V[3] = (-2, 3, -194)
    V[13] = (-3, 9, 10)
    assert len(U) == 264
    validate(U, 198)
    validate(V, 198)
    assert U[3] == (-2, -3, -194) and U[13] == (3, 9, 10)
    a = [((int(WITNESS_HEX, 16) >> (197 - i)) & 1)
         for i in range(198)]
    assert false_clauses(V, a) == []
    assert false_clauses(U, a) == [3]
    assert first_positive_normalize(U, 198) != first_positive_normalize(V, 198)
    core_delete = evaluate_core()

    positions = [(i, j) for i, c in enumerate(U) for j, lit in enumerate(c)
                 if abs(lit) == 3]
    changed = {(3, 1), (13, 0)}
    unchanged = set(positions) - changed
    assert set(positions) == {(3, 1), (5, 0), (13, 0), (14, 0)}
    pairs = []
    for i, p in enumerate(positions):
        for q in positions[i + 1:]:
            uxor = (U[p[0]][p[1]] > 0) != (U[q[0]][q[1]] > 0)
            vxor = (V[p[0]][p[1]] > 0) != (V[q[0]][q[1]] > 0)
            assert (uxor != vxor) == (
                (p in changed) != (q in changed))
            pairs.append((p, q, uxor != vxor))
    assert sum(x[-1] for x in pairs) == 4

    seed, rows = 20261023, []
    def nextbit():
        nonlocal seed
        seed = (1664525 * seed + 1013904223) & 0xffffffff
        return (seed >> 17) & 1

    for t in (1, 2, 3):
        yes = no = 0
        for trial in range(130):
            eta = []
            gauges = []
            F = []
            for block in range(t):
                tag = nextbit()
                g = [nextbit() for _ in range(198)]
                eta.append(tag)
                gauges.append(g)
                F.extend(gauge_block(V if tag else U, g, block))
            validate(F, 198 * t)
            bits = []
            for block in range(t):
                s1 = F[264 * block + 3][1] > 0
                s2 = F[264 * block + 5][0] > 0
                bits.append(int(s1 != s2))
                assert bits[-1] == eta[block]
                chunk = F[264 * block: 264 * (block + 1)]
                shifted = [tuple((1 if l > 0 else -1) *
                                 (abs(l) - block * 198) for l in c)
                           for c in chunk]
                target = V if eta[block] else U
                assert first_positive_normalize(shifted, 198) == (
                    first_positive_normalize(target, 198))
            assert all(bits) == all(eta)
            if all(eta):
                witness = [
                    a[i] ^ gauges[block][i]
                    for block in range(t) for i in range(198)]
                assert false_clauses(F, witness) == []
                yes += 1
            else:
                no += 1
        w = (64 * (462 * t + 1) - 1).bit_length()
        rows.append({
            "blocks": t, "samples": 130, "yes": yes, "no": no,
            "n": 198 * t, "m": 264 * t,
            "N_bits": (1056 * t + 2) * w,
            "sign_orbit_size_power_two": 198 * t,
            "full_family_size_power_two": 199 * t,
            "exact_yes_input_query_lower_bound": 2 * t,
        })
    print(json.dumps({
        "id": "GAUGEFORK81_MINIREPRO", "source": str(SOURCE),
        "U_failure_on_V_witness": [3], "V_witness_verified": True,
        "local_projected_core_unsat": True,
        "core_deletion_counts": core_delete,
        "x3_query_pairs": len(pairs),
        "informative_two_field_pairs": 4,
        "rows": rows, "failed_assertions": 0,
        "U_UNSAT_proof_dependency": "DOECKER-CORE-CERT61, not replayed here"
    }, indent=2))

if __name__ == "__main__":
    main()
