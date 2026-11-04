#!/usr/bin/env python3
"""Finite controls for REFEREE343.

This is deliberately tiny and independent of the full R_mix341 implementation.
It checks (i) exact minimum shared-DAG Resolution costs for every CNF over two
variables, (ii) lexicographic prefix extraction of a minimum fixed-width proof,
(iii) malformed proof rejection, (iv) K4 Tseitin parity controls, and (v) the
material-implication quantifier distinction used in the reflection lemma.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, deque
from itertools import product
from pathlib import Path

LITS = (-2, -1, 1, 2)


def clause_key(c):
    return tuple(sorted(c, key=lambda z: (abs(z), z < 0)))


CLAUSES = [
    clause_key(c)
    for c in (
        (-1,), (1,), (-2,), (2,),
        (-1, -2), (-1, 2), (1, -2), (1, 2),
    )
]
CLAUSES = sorted(set(CLAUSES), key=lambda c: (len(c), c))
EMPTY = ()
CID = {c: i for i, c in enumerate([EMPTY] + CLAUSES)}


def sat_clause(c, a):
    return any(a[abs(lit) - 1] == (lit > 0) for lit in c)


def is_sat(source):
    return any(all(sat_clause(c, a) for c in source)
               for a in product((False, True), repeat=2))


def resolvents(a, b):
    out = set()
    sa, sb = set(a), set(b)
    for p in (1, 2):
        for lp in (p, -p):
            if lp in sa and -lp in sb:
                r = (sa - {lp}) | (sb - {-lp})
                if any(-x in r for x in r):
                    continue
                out.add((p, clause_key(r)))
    return sorted(out)


def exact_min_proofs(source, max_q=3):
    """Return minimum q and all content-record proofs of that q (small universe)."""
    source = frozenset(source)
    start = (frozenset(), tuple())
    frontier = [start]
    for q in range(1, max_q + 1):
        nxt = {}
        solutions = set()
        for derived, trace in frontier:
            avail = sorted(source | derived, key=lambda c: CID[c])
            for i, a in enumerate(avail):
                for b in avail[i:]:
                    for pivot, child in resolvents(a, b):
                        record = (CID[a], CID[b], pivot - 1, CID[child])
                        new_trace = trace + (record,)
                        if child == EMPTY:
                            solutions.add(new_trace)
                            continue
                        new_derived = frozenset(set(derived) | {child})
                        key = (new_derived, new_trace)
                        nxt[key] = key
        if solutions:
            return q, sorted(solutions)
        frontier = list(nxt.values())
    return None, []


def encode_proof(q, trace):
    # 2 header bits plus three 14-bit records: parent, parent, pivot, child.
    bits = f"{q:02b}"
    for pa, pb, piv, ch in trace:
        bits += f"{pa:04b}{pb:04b}{piv:02b}{ch:04b}"
    bits += "0" * (44 - len(bits))
    assert len(bits) == 44
    return bits


def decode_and_verify(source, bits):
    if not isinstance(bits, str) or len(bits) != 44 or set(bits) - {"0", "1"}:
        return False
    q = int(bits[:2], 2)
    if q not in (1, 2, 3):
        return False
    pos = 2
    avail = set(source)
    for _ in range(q):
        pa = int(bits[pos:pos + 4], 2); pos += 4
        pb = int(bits[pos:pos + 4], 2); pos += 4
        piv = int(bits[pos:pos + 2], 2) + 1; pos += 2
        ch = int(bits[pos:pos + 4], 2); pos += 4
        universe = [EMPTY] + CLAUSES
        if pa >= len(universe) or pb >= len(universe) or ch >= len(universe):
            return False
        a, b, child = universe[pa], universe[pb], universe[ch]
        if a not in avail or b not in avail:
            return False
        if (piv, child) not in resolvents(a, b):
            return False
        if child == EMPTY:
            if _ != q - 1:
                return False
        else:
            avail.add(child)
    if bits[pos:] and int(bits[pos:], 2) != 0:
        return False
    return child == EMPTY


def prefix_extract(candidates):
    prefix = ""
    queries = 0
    for _ in range(44):
        queries += 1
        if any(x.startswith(prefix + "0") for x in candidates):
            prefix += "0"
        else:
            assert any(x.startswith(prefix + "1") for x in candidates)
            prefix += "1"
    return prefix, queries


def k4_count(charges):
    vertices = range(4)
    edges = [(i, j) for i in vertices for j in vertices if i < j]
    count = 0
    for values in product((0, 1), repeat=len(edges)):
        ok = True
        for v in vertices:
            parity = 0
            for idx, e in enumerate(edges):
                if v in e:
                    parity ^= values[idx]
            ok &= parity == charges[v]
        count += int(ok)
    return count


def main():
    counts = Counter()
    prefix_queries = 0
    malformed_rejected = 0
    sat_no_proof = 0
    extracted = 0
    cases = []
    for mask in range(256):
        source = [CLAUSES[i] for i in range(8) if (mask >> i) & 1]
        sat = is_sat(source)
        q, traces = exact_min_proofs(source)
        if sat:
            assert q is None and not traces
            sat_no_proof += 1
            continue
        assert q in (1, 2, 3) and traces
        encodings = sorted({encode_proof(q, t) for t in traces})
        chosen, nq = prefix_extract(encodings)
        prefix_queries += nq
        assert decode_and_verify(source, chosen)
        extracted += 1
        counts[q] += 1
        # Four malformed/corrupt controls per UNSAT source.
        bad = [chosen[:-1], chosen + "0", "2" + chosen[1:], chosen[:-1] + "1"]
        for x in bad:
            assert not decode_and_verify(source, x)
            malformed_rejected += 1
        cases.append({"mask": mask, "q": q, "proof": chosen})

    assert sat_no_proof == 95
    assert extracted == 161
    assert dict(counts) == {1: 112, 2: 48, 3: 1}
    assert k4_count((1, 0, 0, 0)) == 0
    assert k4_count((0, 0, 0, 0)) == 8

    truth = []
    for sat_p, wbar_poly in product((False, True), repeat=2):
        b3 = (not sat_p) or wbar_poly
        universal_reflection = (not sat_p) or wbar_poly
        existential_machine_and_short = sat_p and wbar_poly
        assert b3 == universal_reflection
        truth.append({
            "sat_in_p": sat_p,
            "wbar_poly": wbar_poly,
            "B3": b3,
            "forall_A_if_P_then_short_HA": universal_reflection,
            "exists_A_P_and_short_HA": existential_machine_and_short,
        })

    packed = [{"parameter_n": n, "paid_nodes": 1, "payload_bits": 2 ** n}
              for n in range(1, 17)]
    assert packed[-1]["payload_bits"] == 65536

    summary = {
        "model": "ordinary shared-DAG Resolution over all 2-variable non-tautological clauses",
        "cnf_cases": 256,
        "sat_cases": sat_no_proof,
        "unsat_cases": extracted,
        "minimum_paid_nodes": dict(sorted(counts.items())),
        "prefix_queries": prefix_queries,
        "fixed_proof_bits": 44,
        "malformed_or_corrupt_rejected": malformed_rejected,
        "k4_tseitin_models": {"odd_charge": 0, "even_zero_charge": 8},
        "reflection_quantifier_truth_table": truth,
        "packed_payload_control": packed,
        "cases_sha256": hashlib.sha256(
            json.dumps(cases, sort_keys=True).encode()).hexdigest(),
    }
    out = Path("results/raw/arc/2026-11-04_1248_LSPV5_343_REFLECTION_BALANCE.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
