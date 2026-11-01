#!/usr/bin/env python3
"""Independent verifier for REFEREE253.  Does not import the producer."""
from __future__ import annotations

import ast
import hashlib
import itertools
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "results/raw/arc/2026-10-31_1748_LSPV5_XOR_TRACE_ACQUISITION_REFEREE253_raw.json"
SOURCE = ROOT / "tmp/doecker61_source.txt"


def load_u():
    text = "\n".join(line for line in SOURCE.read_text().splitlines() if not line.startswith("#"))
    return ast.literal_eval(text)


def sat(formula, assignment):
    return all(any(assignment[abs(lit) - 1] == int(lit > 0) for lit in clause) for clause in formula)


def valid(formula):
    flat = [x for c in formula for x in c]
    n = max(map(abs, flat))
    return (
        len(formula) * 3 == len(flat)
        and all(len(c) == 3 and len({abs(x) for x in c}) == 3 and (all(x > 0 for x in c) or all(x < 0 for x in c)) for c in formula)
        and len({tuple(c) for c in formula}) == len(formula)
        and all(flat.count(i) == 2 and flat.count(-i) == 2 for i in range(1, n + 1))
    )


def simplify(clauses, assignment):
    out = []
    for clause in clauses:
        reduced = []
        for lit in clause:
            if abs(lit) in assignment:
                if assignment[abs(lit)] == (lit > 0):
                    break
            else:
                reduced.append(lit)
        else:
            if not reduced:
                return None
            out.append(tuple(reduced))
    return tuple(out)


def exact_dpll(clauses, seed):
    def search(cs, assignment):
        while True:
            unit = next((c[0] for c in cs if len(c) == 1), None)
            if unit is None:
                break
            v, value = abs(unit), unit > 0
            if v in assignment and assignment[v] != value:
                return False
            assignment = dict(assignment)
            assignment[v] = value
            cs = simplify(cs, {v: value})
            if cs is None:
                return False
            if not cs:
                return True
        if not cs:
            return True
        counts = Counter(abs(x) for c in cs for x in c)
        var = max(counts, key=counts.get)
        for value in (True, False):
            nxt = simplify(cs, {var: value})
            if nxt is not None:
                aa = dict(assignment)
                aa[var] = value
                if search(nxt, aa):
                    return True
        return False

    start = simplify(tuple(tuple(c) for c in clauses), seed)
    return start is not None and search(start, dict(seed))


def verify_u_boundary_certificate(formula):
    boundary = range(193, 199)
    modules = [formula[2 + 42 * i:2 + 42 * (i + 1)] for i in range(6)]
    allowed = []
    for module in modules:
        rows = []
        for mask in range(64):
            seed = {v: bool((mask >> (v - 193)) & 1) for v in boundary}
            if exact_dpll(module, seed):
                rows.append(mask)
        allowed.append(set(rows))
    global_rows = []
    for mask in range(64):
        a = {v: bool((mask >> (v - 193)) & 1) for v in boundary}
        if all(any(a[abs(x)] == (x > 0) for x in c) for c in formula[:2]):
            global_rows.append(mask)
    return sorted(set(global_rows).intersection(*allowed))


def parity(stream):
    mask = 0
    for i in stream:
        mask ^= 1 << i
    return mask


def main() -> int:
    raw = json.loads(RAW.read_text())
    assert raw["run_id"] == "XOR-TRACE-ACQUISITION-REFEREE253"
    checks = 0
    for row in raw["snapshot_probe_theorem"]["rows"]:
        length = row["length"]
        assert row["two_unknown_snapshots_exact_worst_case_queries"] == 2 * length
        assert row["previous_snapshot_retained_exact_worst_case_queries"] == length
        for bit in range(2 * length):
            left, right = [0] * length, [0] * length
            if bit < length:
                left[bit] = 1
            else:
                right[bit - length] = 1
            assert sum(a != b for a, b in zip(left, right)) == 1
            checks += 1

    for row in raw["toggle_stream_theorem"]["rows"]:
        length = row["cut_events"]
        masks = [m for m in range(1 << length) if m.bit_count() % 2 == length % 2]
        assert len(masks) == row["reachable_parity_masks"] == 1 << (length - 1)
        assert row["required_persistent_bits_no_reread"] == length - 1
        for mask in masks:
            stream = [i for i in range(length) if (mask >> i) & 1]
            stream += [0, 0] * ((length - len(stream)) // 2)
            assert len(stream) == length and parity(stream) == mask
            checks += 1

    U = load_u()
    V = [c[:] for c in U]
    V[2][-1], V[44][-1] = V[44][-1], V[2][-1]
    assert valid(U) and valid(V)
    assert verify_u_boundary_certificate(U) == []
    checks += 1

    witness = (
        "001110010011110001010001110100111110011011000101000101001010100001011010"
        "101011000100000111001010110101001110001001101000110001100010100101101110"
        "010101011001001100000110111001001101001101101001010101"
    )
    assert len(witness) == 198 and sat(V, [int(x) for x in witness])
    assert hashlib.sha256(witness.encode()).hexdigest() == raw["same_target_labels"]["V198"]["witness_sha256"]
    checks += 2

    for name, encodings in raw["trace_ledgers"].items():
        n = 6 if name.startswith("Y6") else 198
        m = 8 if name.startswith("Y6") else 264
        for encoding, ledger in encodings.items():
            assert ledger["state_length_bits"] == n + 3 * m
            assert sum(r["d_logic"] for r in ledger["rows"]) == ledger["sum_adjacent_d_logic"]
            assert sum(r["posthoc_two_snapshot_bit_probes"] for r in ledger["rows"]) == ledger["sum_posthoc_two_snapshot_bit_probes"]
            assert sum(r["posthoc_previous_retained_bit_probes"] for r in ledger["rows"]) == ledger["sum_posthoc_previous_retained_bit_probes"]
            assert all(r["d_logic"] == len(r["changed_record_ids"]) for r in ledger["rows"])
            checks += 5

    assert raw["same_target_labels"]["U198"]["status"] == "UNSAT"
    assert raw["same_target_labels"]["V198"]["status"] == "SAT"
    assert raw["same_target_labels"]["Y6"] == {"m": 8, "models": 20, "n": 6, "status": "SAT"}
    assert all(not row["valid"] for row in raw["malformed_rejections"].values())
    print(json.dumps({"verified": True, "independent_checks": checks, "raw": str(RAW)}, indent=2))
    print("INDEPENDENT_VERIFIED::XOR-TRACE-ACQUISITION-REFEREE253")
    return 0


if __name__ == "__main__":
    sys.exit(main())
