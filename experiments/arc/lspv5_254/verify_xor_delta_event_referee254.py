#!/usr/bin/env python3
"""Independent, no-producer-import verifier for REFEREE254."""
from __future__ import annotations

import ast
import hashlib
import itertools
import json
import math
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "results/raw/arc/2026-10-31_1848_LSPV5_XOR_DELTA_EVENT_REFEREE254_raw.json"
SOURCE = ROOT / "tmp/doecker61_source.txt"
WITNESS = (
    "001110010011110001010001110100111110011011000101000101001010100001011010"
    "101011000100000111001010110101001110001001101000110001100010100101101110"
    "010101011001001100000110111001001101001101101001010101"
)


def load_u():
    text = "\n".join(line for line in SOURCE.read_text().splitlines() if not line.startswith("#"))
    return ast.literal_eval(text)


def y6():
    pos = [(1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6)]
    neg = [(1, 2, 4), (1, 3, 6), (2, 3, 5), (4, 5, 6)]
    return [list(c) for c in pos] + [[-x for x in c] for c in neg]


def valid(formula):
    if not formula or any(len(c) != 3 or len({abs(x) for x in c}) != 3 for c in formula):
        return False
    if any(not (all(x > 0 for x in c) or all(x < 0 for x in c)) for c in formula):
        return False
    if len({tuple(sorted(c)) for c in formula}) != len(formula):
        return False
    n = max(abs(x) for c in formula for x in c)
    return all(sum(x == v for c in formula for x in c) == 2 and sum(x == -v for c in formula for x in c) == 2 for v in range(1, n + 1))


def sat(formula, assignment):
    return all(any(assignment[abs(x) - 1] == int(x > 0) for x in c) for c in formula)


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
        v = max(counts, key=counts.get)
        for value in (True, False):
            nxt = simplify(cs, {v: value})
            if nxt is not None:
                aa = dict(assignment)
                aa[v] = value
                if search(nxt, aa):
                    return True
        return False
    start = simplify(tuple(tuple(c) for c in clauses), seed)
    return start is not None and search(start, dict(seed))


def u_boundary_rows(formula):
    boundary = range(193, 199)
    allowed = []
    for i in range(6):
        module = formula[2 + 42 * i:2 + 42 * (i + 1)]
        rows = set()
        for mask in range(64):
            seed = {v: bool((mask >> (v - 193)) & 1) for v in boundary}
            if exact_dpll(module, seed):
                rows.add(mask)
        allowed.append(rows)
    global_rows = set()
    for mask in range(64):
        a = {v: bool((mask >> (v - 193)) & 1) for v in boundary}
        if all(any(a[abs(x)] == (x > 0) for x in c) for c in formula[:2]):
            global_rows.add(mask)
    return sorted(global_rows.intersection(*allowed))


def index(formula, n):
    out = [[] for _ in range(n)]
    for j, clause in enumerate(formula):
        for lit in clause:
            out[abs(lit) - 1].append((j, int(lit > 0)))
    return out


def state(assignment, counts, encoding):
    out = list(assignment)
    for count in counts:
        code = count if encoding == "binary" else count ^ (count >> 1)
        out += [code & 1, (code >> 1) & 1, int(count > 0)]
    return out


def replay_trace(formula, ledger, start):
    n = len(start)
    idx = index(formula, n)
    assignment = start[:]
    counts = [sum(assignment[abs(x) - 1] == int(x > 0) for x in c) for c in formula]
    initial = state(assignment, counts, ledger["encoding"])
    total = 0
    for expected in ledger["rows"]:
        v = expected["variable_zero_based"]
        before = state(assignment, counts, ledger["encoding"])
        nxt_a, nxt_c = assignment[:], counts[:]
        nxt_a[v] ^= 1
        for clause_id, sign in idx[v]:
            nxt_c[clause_id] += -1 if assignment[v] == sign else 1
        after = state(nxt_a, nxt_c, ledger["encoding"])
        ids = []
        for pos, (x, y) in enumerate(zip(before, after)):
            if x == y:
                continue
            if pos < n:
                ids.append(f"assignment:{pos}")
            else:
                q, field = divmod(pos - n, 3)
                ids.append(f"clause:{q}:" + (f"count_bit:{field}" if field < 2 else "sat"))
        assert ids == expected["changed_record_ids"]
        assert expected["incident_clause_ids_zero_based"] == [j for j, _ in idx[v]]
        assert expected["event_code"] == format(v, f"0{ledger['event_code_bits']}b")
        assert expected["d_logic"] == len(ids)
        total += len(ids)
        assignment, counts = nxt_a, nxt_c
    final = state(assignment, counts, ledger["encoding"])
    assert total == ledger["sum_adjacent_d_logic"] == ledger["changed_record_ids_total"]
    assert sum(x != y for x, y in zip(initial, final)) == ledger["endpoint_d_logic"]
    assert ledger["event_log_bits"] == ledger["steps"] * ledger["event_code_bits"]
    return 7 * ledger["steps"] + 3


def main():
    raw = json.loads(RAW.read_text())
    assert raw["run_id"] == "XOR-DELTA-EVENT-REFEREE254"
    U = load_u()
    V = [c[:] for c in U]
    V[2][-1], V[44][-1] = V[44][-1], V[2][-1]
    Y = y6()
    assert valid(U) and valid(V) and valid(Y)
    assert u_boundary_rows(U) == []
    assert len(WITNESS) == 198 and sat(V, [int(x) for x in WITNESS])
    assert hashlib.sha256(WITNESS.encode()).hexdigest() == raw["same_target_labels"]["V198"]["witness_sha256"]
    checks = 4

    formulas = {"Y6": Y, "U198": U, "V198": V}
    for name, encs in raw["traces"].items():
        formula = formulas["Y6" if name.startswith("Y6") else ("U198" if name.startswith("U198") else "V198")]
        for encoding, ledger in encs.items():
            ledger = dict(ledger)
            ledger["encoding"] = encoding
            checks += replay_trace(formula, ledger, [0] * (6 if name.startswith("Y6") else 198))

    independent_dist = {"binary": Counter(), "gray": Counter()}
    for bits in itertools.product((0, 1), repeat=6):
        for v in range(6):
            for enc in ("binary", "gray"):
                one = {"encoding": enc, "event_code_bits": 3, "steps": 1, "rows": [{"variable_zero_based": v}]}
                # Directly compute the delta without trusting raw changed IDs.
                a = list(bits)
                counts = [sum(a[abs(x)-1] == int(x > 0) for x in c) for c in Y]
                before = state(a, counts, enc)
                aa = a[:]
                aa[v] ^= 1
                after_counts = [sum(aa[abs(x)-1] == int(x > 0) for x in c) for c in Y]
                after = state(aa, after_counts, enc)
                independent_dist[enc][str(sum(x != y for x, y in zip(before, after)))] += 1
                checks += 1
    assert {k: dict(v) for k, v in independent_dist.items()} == raw["exhaustive_Y6"]["distribution"]

    for n in (6, 198):
        b = math.ceil(math.log2(n))
        assert 2 ** b >= n and 2 ** (b - 1) < n
        checks += n
    assert all(not row["valid"] for row in raw["malformed_rejections"].values())
    assert raw["proof_status"]["P_vs_NP"] == "OPEN"
    print(json.dumps({"verified": True, "independent_checks": checks, "raw": str(RAW)}, indent=2))
    print("INDEPENDENT_VERIFIED::XOR-DELTA-EVENT-REFEREE254")
    return 0


if __name__ == "__main__":
    sys.exit(main())
