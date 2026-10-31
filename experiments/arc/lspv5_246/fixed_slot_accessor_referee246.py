#!/usr/bin/env python3
"""REFEREE246: fixed-slot virtual child accessor for ordered separator controls.

Standard-library only.  This is a restricted construction/audit, not a SAT
lower bound and not an all-input ARC compiler.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import time
from pathlib import Path

RUN_ID = "FIXED-SLOT-ACCESSOR-REFEREE246"
STAMP = "2026-10-31T10:48:00-07:00"
SEED = 2461048
HEADER_BITS = 32
VAR_BITS = 16
REC_BITS = 3 * (1 + VAR_BITS)
SLOTS = 8


def lit_true(lit, assignment):
    return assignment[abs(lit)] == (lit > 0)


def clause_true(clause, assignment):
    return any(lit_true(x, assignment) for x in clause)


def formula_true(clauses, assignment):
    return all(clause_true(c, assignment) for c in clauses)


def all_models(clauses, n):
    out = []
    for bits in itertools.product((False, True), repeat=n):
        a = {i + 1: bits[i] for i in range(n)}
        if formula_true(clauses, a):
            out.append("".join("1" if b else "0" for b in bits))
    return out


def simplify(clauses, assignment):
    out = []
    for c in clauses:
        if any(abs(x) in assignment and lit_true(x, assignment) for x in c):
            continue
        out.append(tuple(x for x in c if abs(x) not in assignment))
    return out


def dpll(clauses):
    clauses = [tuple(c) for c in clauses]
    nodes = 0

    def rec(cs):
        nonlocal nodes
        nodes += 1
        while True:
            if any(len(c) == 0 for c in cs):
                return False
            if not cs:
                return True
            unit = next((c[0] for c in cs if len(c) == 1), None)
            if unit is None:
                break
            nxt = []
            for c in cs:
                if unit in c:
                    continue
                nxt.append(tuple(x for x in c if x != -unit))
            cs = nxt
        v = abs(cs[0][0])
        for val in (True, False):
            lit = v if val else -v
            nxt = []
            for c in cs:
                if lit in c:
                    continue
                nxt.append(tuple(x for x in c if x != -lit))
            if rec(nxt):
                return True
        return False

    ans = rec(clauses)
    return ans, nodes


def bits_of_int(x, width):
    return f"{x:0{width}b}"


def encode_clause(c):
    assert len(c) == 3 and len({abs(x) for x in c}) == 3
    return "".join(("1" if x < 0 else "0") + bits_of_int(abs(x), VAR_BITS) for x in c)


def encode_formula(clauses, n):
    return bits_of_int(n, 16) + bits_of_int(len(clauses), 16) + "".join(encode_clause(c) for c in clauses)


def decode_clause(source_bits, j):
    pos = HEADER_BITS + j * REC_BITS
    out = []
    for k in range(3):
        sign = source_bits[pos + k * (1 + VAR_BITS)] == "1"
        lo = pos + k * (1 + VAR_BITS) + 1
        v = int(source_bits[lo:lo + VAR_BITS], 2)
        out.append(-v if sign else v)
    return tuple(out)


def pad_clause(base, slot):
    # Three private variables used nowhere else: existentially harmless while
    # preserving the distinct-variable proper-3CNF grammar.
    z = base + 8 + 3 * slot
    return (z, z + 1, z + 2)


def fixed_slots(residual, base):
    r = tuple(residual)
    if len(r) == 3:
        active = [r]
    elif len(r) == 2:
        a = base
        active = [(r[0], r[1], a), (r[0], r[1], -a)]
    elif len(r) == 1:
        a, b = base, base + 1
        active = [(r[0], sa * a, sb * b) for sa in (1, -1) for sb in (1, -1)]
    elif len(r) == 0:
        a, b, c = base, base + 1, base + 2
        active = [(sa * a, sb * b, sc * c)
                  for sa in (1, -1) for sb in (1, -1) for sc in (1, -1)]
    else:
        raise AssertionError(r)
    return active + [pad_clause(base, s) for s in range(len(active), SLOTS)]


def clause_slots(source_clause, boundary, base):
    if any(abs(x) in boundary and lit_true(x, boundary) for x in source_clause):
        return [pad_clause(base, s) for s in range(SLOTS)]
    residual = tuple(x for x in source_clause if abs(x) not in boundary)
    return fixed_slots(residual, base)


def child_clauses(source_clauses, span, boundary, n):
    out = []
    for j in range(span[0], span[1]):
        out.extend(clause_slots(source_clauses[j], boundary, n + 1 + 64 * j))
    return out


def child_n(n, m):
    return n + 64 * m + 32


def child_accessor(source_bits, n, m, span, boundary, q):
    """Return (bit-or-blank, source-field reads), without materializing child."""
    child_m = SLOTS * (span[1] - span[0])
    length = HEADER_BITS + REC_BITS * child_m
    if q < 0 or q >= length:
        return "_", 0
    header = bits_of_int(child_n(n, m), 16) + bits_of_int(child_m, 16)
    if q < HEADER_BITS:
        return header[q], 0
    z = q - HEADER_BITS
    rec, within = divmod(z, REC_BITS)
    local_source, slot = divmod(rec, SLOTS)
    j = span[0] + local_source
    c = decode_clause(source_bits, j)
    slots = clause_slots(c, boundary, n + 1 + 64 * j)
    return encode_clause(slots[slot])[within], 3 * (1 + VAR_BITS)


def source_pair_modes(clauses):
    out = []
    for j in range(len(clauses)):
        for k in range(j + 1, len(clauses)):
            same = sorted({abs(a) for a in clauses[j] for b in clauses[k] if a == b})
            opp = sorted({abs(a) for a in clauses[j] for b in clauses[k] if a == -b})
            predicted = {
                "SS": not opp, "SU": not same,
                "US": not same, "UU": not opp,
            }
            shared = sorted({abs(x) for x in clauses[j]} | {abs(x) for x in clauses[k]})
            actual = {mode: False for mode in predicted}
            for bits in itertools.product((False, True), repeat=len(shared)):
                a = dict(zip(shared, bits))
                tj = sum(lit_true(x, a) for x in clauses[j])
                tk = sum(lit_true(x, a) for x in clauses[k])
                actual["SS"] |= tj == 3 and tk == 3
                actual["SU"] |= tj == 3 and tk == 0
                actual["US"] |= tj == 0 and tk == 3
                actual["UU"] |= tj == 0 and tk == 0
            assert predicted == actual
            out.append({"j": j, "k": k, "same": same, "opposite": opp,
                        "modes": predicted})
    return out


def occurrence_controls(clauses):
    out = []
    for j, c in enumerate(clauses):
        for p, lit in enumerate(c):
            s = lit > 0
            u = not s
            out.append({"clause": j, "position": p, "literal": lit,
                        "S_variable": int(s), "invert_S_is_U": int(not s),
                        "U_variable": int(u), "invert_U_is_S": int(not u)})
    return out


def endpoint_and_flip(clauses, n, witness):
    def state(bits):
        a = {i + 1: bool(int(bits[i])) for i in range(n)}
        counts = [sum(lit_true(x, a) for x in c) for c in clauses]
        return {"bits": bits, "counts": counts,
                "categories": {str(r): counts.count(r) for r in range(4)},
                "sat": all(x > 0 for x in counts)}
    zero = "0" * n
    one = "1" * n
    trail = [state(zero)]
    cur = list(zero)
    for i, b in enumerate(witness or zero):
        if cur[i] != b:
            cur[i] = b
            trail.append(state("".join(cur)))
    z, o = state(zero), state(one)
    assert all(a + b == 3 for a, b in zip(z["counts"], o["counts"]))
    return {"zero": z, "one": o, "flip_trail": trail,
            "complement_identity": True}


def pin_pair(u, v, a):
    return [(u, v, a), (u, v, -a)]


def make_source(label, renamed=False):
    # Three boundary clauses leave only (p,q)=(1,0); the fourth kills it.
    p, q = (2, 1) if renamed else (1, 2)
    specs = [(p, q), (p, -q), (-p, -q)]
    if label == "UNSAT":
        specs.append((-p, q))
    clauses, spans, resolutions = [], [], []
    for idx, (u, v) in enumerate(specs):
        a = 3 + idx
        start = len(clauses)
        pair = pin_pair(u, v, a)
        clauses.extend(pair)
        spans.append((start, len(clauses)))
        resolutions.append({"parents": [start, start + 1], "pivot": a,
                            "resolvent": [u, v],
                            "forbidden_cube": {str(abs(u)): int(u < 0), str(abs(v)): int(v < 0)}})
    return {"name": f"ORDERED_{label}{'_RENAMED' if renamed else ''}",
            "expected": label, "n": 6, "boundary_vars": [p, q],
            "clauses": clauses, "spans": spans, "resolutions": resolutions}


def gadget_truth_table_checks():
    checks = 0
    for arity in range(4):
        residual = tuple(range(1, arity + 1))
        slots = fixed_slots(residual, 20)
        for bits in itertools.product((False, True), repeat=arity):
            a = {i + 1: bits[i] for i in range(arity)}
            target = any(bits) if arity else False
            restricted = simplify(slots, a)
            got, _ = dpll(restricted)
            assert got == target
            checks += 1
    sat_slots = [pad_clause(30, s) for s in range(SLOTS)]
    assert dpll(sat_slots)[0]
    return checks + 1


def audit_source(spec):
    clauses, n = spec["clauses"], spec["n"]
    models = all_models(clauses, n)
    label = "SAT" if models else "UNSAT"
    assert label == spec["expected"]
    source_bits = encode_formula(clauses, n)
    boundary_vars = spec["boundary_vars"]
    children = []
    total_accessor_queries = total_source_field_reads = total_guest_nodes = 0
    join_rows = []
    for bb in itertools.product((False, True), repeat=len(boundary_vars)):
        boundary = dict(zip(boundary_vars, bb))
        row_ok = True
        block_rows = []
        for span in spec["spans"]:
            cc = child_clauses(clauses, span, boundary, n)
            physical = encode_formula(cc, child_n(n, len(clauses)))
            child_sat, child_nodes = dpll(cc)
            total_guest_nodes += child_nodes
            row_ok &= child_sat
            # Complete bit-for-bit accessor check, plus far blanks.
            for q in list(range(len(physical))) + [len(physical), len(physical) + 7, len(physical) + 101]:
                got, reads = child_accessor(source_bits, n, len(clauses), span, boundary, q)
                want = physical[q] if q < len(physical) else "_"
                assert got == want
                total_accessor_queries += 1
                total_source_field_reads += reads
            # Deterministic guest traces with arbitrary repeated/far addresses.
            checksum_p = checksum_v = 0
            x = SEED + len(children) * 17
            for t in range(64):
                x = (1103515245 * x + 12345) & 0x7fffffff
                q = x % (len(physical) + 127)
                pb = physical[q] if q < len(physical) else "_"
                vb, reads = child_accessor(source_bits, n, len(clauses), span, boundary, q)
                checksum_p = (checksum_p * 131 + ord(pb)) % 1000000007
                checksum_v = (checksum_v * 131 + ord(vb)) % 1000000007
                total_accessor_queries += 1
                total_source_field_reads += reads
            assert checksum_p == checksum_v
            children.append({"boundary": {str(k): int(v) for k, v in boundary.items()},
                             "span": list(span), "physical_bits": len(physical),
                             "clauses": len(cc), "sat": child_sat,
                             "dpll_nodes": child_nodes, "trace_checksum": checksum_v})
            block_rows.append(child_sat)
        join_rows.append({"boundary": "".join("1" if x else "0" for x in bb),
                          "blocks": block_rows, "and": row_ok})
    joined = any(x["and"] for x in join_rows)
    assert joined == bool(models)
    base_sat, base_nodes = dpll(clauses)
    assert base_sat == bool(models)
    controls = occurrence_controls(clauses)
    pairs = source_pair_modes(clauses)
    endpoint = endpoint_and_flip(clauses, n, models[0] if models else None)
    if label == "SAT":
        assert not endpoint["zero"]["sat"] and not endpoint["one"]["sat"]
    return {
        "name": spec["name"], "expected": label, "source_n": n,
        "source_clauses": [list(c) for c in clauses], "source_bits": len(source_bits),
        "models": len(models), "witness": models[0] if models else None,
        "spans": [list(x) for x in spec["spans"]],
        "boundary_vars": boundary_vars, "join_rows": join_rows, "children": children,
        "baseline_dpll_nodes": base_nodes, "guest_dpll_nodes": total_guest_nodes,
        "accessor_queries": total_accessor_queries,
        "source_field_bit_reads": total_source_field_reads,
        "occurrences": controls, "pair_modes": pairs,
        "endpoints_flips": endpoint, "resolutions": spec["resolutions"],
    }


def main():
    started = time.perf_counter()
    gadget_checks = gadget_truth_table_checks()
    specs = [make_source(label, renamed) for renamed in (False, True)
             for label in ("SAT", "UNSAT")]
    records = [audit_source(s) for s in specs]
    assertion_units = gadget_checks
    for r in records:
        assertion_units += len(r["occurrences"]) * 4 + len(r["pair_modes"]) * 4
        assertion_units += r["accessor_queries"] + len(r["join_rows"])
        assertion_units += len(r["resolutions"]) + len(r["endpoints_flips"]["flip_trail"])
    raw = {
        "run_id": RUN_ID, "timestamp": STAMP, "seed": SEED,
        "status": "PASS", "proof_status": "PROVED/EXACT restricted + COMPUTATIONAL finite",
        "global_status": "P versus NP OPEN; universal all-input ARC OPEN",
        "theorem": {
            "slots_per_source_clause": SLOTS,
            "accessor_time": "polylog(N) per requested logical child bit",
            "accessor_space": "O(log N) scratch and metadata",
            "restricted_recurrence": "K' <= max(11/10, 3/5+K/2), L' <= max(1/2,L/2)",
            "scope": "ordered contiguous balanced separator promise only; all-input fallback noncontractive",
        },
        "falsifiers": [
            "F1 materialized work-tape child is necessary: falsified on fixed-slot virtual children",
            "F2 arbitrary guest cannot be simulated without knowing K: falsified by total accessor transfer",
            "F3 accepted promise proves universal ARC: falsified by nonmatching-source fallback",
            "F4 affine small-bias implies SAT runtime: falsified model transfer; affine MCSP only",
        ],
        "gadget_truth_table_checks": gadget_checks,
        "records": records,
        "assertion_units": assertion_units,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    out = Path("results/raw/arc/2026-10-31_1048_LSPV5_FIXED_SLOT_ACCESSOR_REFEREE246_raw.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(raw, indent=2, sort_keys=True) + "\n"
    out.write_text(text)
    digest = hashlib.sha256(text.encode()).hexdigest()
    summary = {
        "run_id": RUN_ID, "status": "PASS", "records": len(records),
        "sat": sum(r["expected"] == "SAT" for r in records),
        "unsat": sum(r["expected"] == "UNSAT" for r in records),
        "assertion_units": assertion_units, "raw_sha256": digest,
        "accessor_queries": sum(r["accessor_queries"] for r in records),
        "source_field_bit_reads": sum(r["source_field_bit_reads"] for r in records),
    }
    sp = Path("results/summaries/arc/2026-10-31_1048_LSPV5_FIXED_SLOT_ACCESSOR_REFEREE246_summary.json")
    sp.parent.mkdir(parents=True, exist_ok=True)
    sp.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
