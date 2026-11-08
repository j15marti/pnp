#!/usr/bin/env python3
"""LSPV-5/420: recovered-checker reachability and ordinary-RES unit-discharge audit."""
from __future__ import annotations

import copy
import hashlib
import itertools
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKET = ROOT / "replay/413/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json"
CHECKER = ROOT / "replay/413/lspv2_341_independent_verify.js"
OUT = ROOT / "results/raw/review/2026-11-07_1648_LSPV5_REACHABILITY_DISCHARGE420.json"


def compact(obj):
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False) + "\n"


def run_checker(obj):
    raw = compact(obj)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        f.write(raw)
        name = f.name
    try:
        cp = subprocess.run(["node", str(CHECKER), name], capture_output=True, text=True, timeout=30)
    finally:
        Path(name).unlink(missing_ok=True)
    return {
        "accepted": cp.returncode == 0,
        "returncode": cp.returncode,
        "stdout_sha256": hashlib.sha256(cp.stdout.encode()).hexdigest(),
        "stderr_first": cp.stderr.splitlines()[0] if cp.stderr else "",
        "raw_bytes": len(raw.encode()),
    }


def fixture_reachability(f):
    by_id = {x["id"]: x for x in f["proof"]}
    used = set()

    def visit(node_id):
        if node_id in used:
            return
        used.add(node_id)
        p = by_id.get(node_id)
        if p:
            for parent in p["parents"]:
                visit(parent)

    visit(f["proof"][-1]["id"])
    proof_ids = {x["id"] for x in f["proof"]}
    source_ids = {x["id"] for x in f["clauses"]}
    return {
        "proof_records": len(proof_ids),
        "reachable_proof_records": len(proof_ids & used),
        "source_records": len(source_ids),
        "reachable_source_records": len(source_ids & used),
        "unreachable_proof_ids": sorted(proof_ids - used),
        "unreachable_source_ids": sorted(source_ids - used),
    }


def norm(clause):
    return tuple(sorted(set(clause), key=lambda x: (abs(x), x)))


def taut(c):
    s = set(c)
    return any(-x in s for x in s)


def resolve(a, b, pivot):
    assert pivot in a and -pivot in b
    c = norm([x for x in a if x != pivot] + [x for x in b if x != -pivot])
    assert not taut(c)
    return c


def derive_closure(sources, assumption):
    """One deterministic complete Resolution closure, retaining parent/pivot bytes."""
    nodes = []
    known = {}
    for c in sources:
        if c not in known:
            known[c] = len(nodes)
            nodes.append({"kind": "source", "clause": c})
    assumption_id = len(nodes)
    nodes.append({"kind": "assumption", "clause": (assumption,)})
    known.setdefault((assumption,), assumption_id)
    changed = True
    while changed and () not in known:
        changed = False
        snapshot = list(known.items())
        for a, ia in snapshot:
            for b, ib in snapshot:
                if ia >= ib:
                    continue
                for pivot in a:
                    if -pivot not in b:
                        continue
                    c = norm([x for x in a if x != pivot] + [x for x in b if x != -pivot])
                    if taut(c) or c in known:
                        continue
                    known[c] = len(nodes)
                    nodes.append({"kind": "res", "clause": c, "parents": (ia, ib), "pivot": pivot})
                    changed = True
                    if c == ():
                        break
                if () in known:
                    break
            if () in known:
                break
    if () not in known:
        return None
    sink = known[()]
    keep = set()

    def visit(i):
        if i in keep:
            return
        keep.add(i)
        if nodes[i]["kind"] == "res":
            visit(nodes[i]["parents"][0])
            visit(nodes[i]["parents"][1])

    visit(sink)
    ordered = sorted(keep)
    remap = {old: new for new, old in enumerate(ordered)}
    trimmed = []
    for old in ordered:
        n = dict(nodes[old])
        if n["kind"] == "res":
            n["parents"] = tuple(remap[x] for x in n["parents"])
        trimmed.append(n)
    return trimmed, remap[sink]


def discharge(proof, sink, assumption):
    """Independent implementation of the LSPV-1/489 subset/bypass transform."""
    output = {}
    emitted = []
    source_set = set()
    for i, node in enumerate(proof):
        c = node["clause"]
        if node["kind"] == "source":
            output[i] = c
            source_set.add(c)
        elif node["kind"] == "assumption":
            output[i] = None
        else:
            left, right = node["parents"]
            a, b, p = output[left], output[right], node["pivot"]
            if a is None:
                assert b is not None and -assumption in b
                output[i] = b
            elif b is None:
                assert assumption in proof[right]["clause"] or assumption in proof[left]["clause"]
                output[i] = a
            elif p in a and -p in b:
                child = resolve(a, b, p)
                emitted.append((a, b, p, child))
                output[i] = child
            elif p not in a:
                output[i] = a
            else:
                assert -p not in b
                output[i] = b
            assert output[i] is None or set(output[i]).issubset(set(c) | {-assumption})
    result = output[sink]
    assert result in ((), (-assumption,))
    available = set(source_set)
    for a, b, p, c in emitted:
        assert a in available and b in available and c == resolve(a, b, p)
        available.add(c)
    assert result in available
    original_res = sum(n["kind"] == "res" for n in proof)
    return {
        "original_res": original_res,
        "emitted_res": len(emitted),
        "result": list(result),
        "strict_saving": original_res - len(emitted),
    }


def clause_sat(c, assignment):
    return any(assignment[abs(x) - 1] == (x > 0) for x in c)


def formula_sat(formula, nvars=3, fixed=None):
    for bits in itertools.product((False, True), repeat=nvars):
        if fixed and any(bits[abs(l) - 1] != (l > 0) for l in fixed):
            continue
        if all(clause_sat(c, bits) for c in formula):
            return True
    return False


def exhaustive_discharge_controls():
    clauses = []
    for signs in itertools.product((-1, 0, 1), repeat=3):
        c = tuple((i + 1) * s for i, s in enumerate(signs) if s)
        if c:
            clauses.append(norm(c))
    tested = 0
    emitted = 0
    strict_savings = 0
    by_assumption = {}
    for assumption in (-3, -2, -1, 1, 2, 3):
        count = 0
        for size in (1, 2, 3):
            for formula in itertools.combinations(clauses, size):
                if not formula_sat(formula):
                    continue
                if formula_sat(formula, fixed=(assumption,)):
                    continue
                built = derive_closure(formula, assumption)
                assert built is not None
                proof, sink = built
                ans = discharge(proof, sink, assumption)
                assert ans["emitted_res"] <= ans["original_res"]
                tested += 1
                count += 1
                emitted += ans["emitted_res"]
                strict_savings += ans["strict_saving"]
        by_assumption[str(assumption)] = count
    return {
        "universe_nonempty_nontaut_clauses": len(clauses),
        "formula_sizes": [1, 2, 3],
        "variables": 3,
        "branch_refutations_transformed": tested,
        "emitted_resolution_nodes": emitted,
        "bypassed_resolution_nodes": strict_savings,
        "by_assumption": by_assumption,
    }


def peer_489_certificate_check():
    def AND(a, b, o):
        return [(-o, a), (-o, b), (o, -a, -b)]

    def TT(a, b, o, fn):
        return [tuple((-a if x else a, -b if y else b, -o if z else o))
                for x, y, z in itertools.product(range(2), repeat=3) if z != fn(x, y)]

    gates = (AND(2, 3, 4) + AND(-1, -4, 5) + TT(4, 2, 8, lambda a, b: int(a == b))
             + AND(1, 8, 6) + TT(1, 3, 9, lambda a, b: a ^ b)
             + TT(4, 3, 10, lambda a, b: int(a == b)) + AND(9, 10, 7))
    clauses = {i + 1: norm(v) for i, v in enumerate(gates)}
    parents = {}
    steps = [(25, 6, 13, 1), (26, 6, 16, 1), (34, 15, 13, 1), (35, 1, 10, 2),
             (36, 7, 3, 2), (37, 2, 21, 3), (40, 2, 34, 3), (45, 18, 36, 3),
             (49, 26, 19, 3), (63, 25, 37, 4), (64, 25, 40, 4), (79, 45, 35, 4),
             (82, 49, 35, 4), (101, 79, 63, 8), (104, 82, 64, 8), (119, 104, 24, 9),
             (122, 101, 119, 10)]
    for out, a, b, p in steps:
        clauses[out] = resolve(clauses[a], clauses[b], p)
        parents[out] = (a, b)
    assert clauses[122] == (5, 6, 7)
    for i in range(3):
        t, z = 5 + i, 11 + i
        a, b = 200 + 2 * i, 201 + 2 * i
        clauses[a], clauses[b] = norm((-t, z)), norm((-t, -z))
        clauses[500 + i] = resolve(clauses[a], clauses[b], z)
        parents[500 + i] = (a, b)
    for out, a, b, p in [(600, 122, 500, 5), (601, 600, 501, 6), (602, 601, 502, 7)]:
        clauses[out] = resolve(clauses[a], clauses[b], p)
        parents[out] = (a, b)
    assert clauses[602] == ()
    used = set()

    def visit(i):
        if i in used:
            return
        used.add(i)
        if i in parents:
            visit(parents[i][0])
            visit(parents[i][1])

    visit(602)

    def depth(i):
        return 0 if i not in parents else 1 + max(depth(parents[i][0]), depth(parents[i][1]))

    source_controls = 0
    for p, u, v in itertools.product(range(2), repeat=3):
        q = u & v
        values = {1: p, 2: u, 3: v, 4: q, 5: (1 - p) & (1 - q),
                  6: p & int(q == u), 7: (p ^ v) & int(q == v),
                  8: int(q == u), 9: p ^ v, 10: int(q == v)}
        assert all(any(values[abs(l)] == (l > 0) for l in c) for c in gates)
        assert any(values[t] for t in (5, 6, 7))
        source_controls += 1
    return {
        "peer_source_sha": "486bb82733155b84ffbc1b1a71ceeada43abf310",
        "gate_facets": len(gates),
        "cover_res": len(steps),
        "global_res": sum(i in parents for i in used),
        "used_source_nodes": sum(i not in parents for i in used),
        "used_total_nodes": len(used),
        "cover_span": depth(122),
        "global_span": depth(602),
        "source_assignment_controls": source_controls,
    }


def main():
    data = json.loads(PACKET.read_text())
    baseline = run_checker(data)
    assert baseline["accepted"]
    f0 = data["fixtures"][0]
    extra = copy.deepcopy(f0["proof"][0])
    extra["id"] = "junk420"
    cases = []

    def case(name, mutate, expected):
        obj = copy.deepcopy(data)
        mutate(obj["fixtures"][0])
        got = run_checker(obj)
        assert got["accepted"] == expected, (name, got)
        got.update(name=name, expected_accept=expected)
        cases.append(got)

    case("positive_independent_topological_reorder",
         lambda f: f["proof"].__setitem__(slice(0, 4), [f["proof"][3], f["proof"][0], f["proof"][1], f["proof"][2]]), True)
    case("insert_legal_unreachable_before_sink", lambda f: f["proof"].insert(-1, copy.deepcopy(extra)), False)
    case("append_legal_record_after_sink", lambda f: f["proof"].append(copy.deepcopy(extra)), False)
    case("insert_and_raise_reported_inferences", lambda f: (f["proof"].insert(-1, copy.deepcopy(extra)),
         f["properties"].__setitem__("inferences", f["properties"]["inferences"] + 1)), False)
    case("drop_first_proof_record", lambda f: f["proof"].pop(0), False)
    case("replace_sink_by_legal_nonsink", lambda f: f["proof"].__setitem__(-1, copy.deepcopy(extra)), False)
    case("duplicate_inference_id", lambda f: f["proof"].__setitem__(1, copy.deepcopy(f["proof"][0])), False)

    reach = [fixture_reachability(f) for f in data["fixtures"]]
    assert all(x["unreachable_proof_ids"] == [] and x["unreachable_source_ids"] == [] for x in reach)
    discharge_controls = exhaustive_discharge_controls()
    peer = peer_489_certificate_check()
    out = {
        "experiment": "LSPV-5/420 reachability and ordinary-Resolution unit-discharge audit",
        "timestamp_pst": "2026-11-07 16:48 PST",
        "status": "PROVED-RESTRICTED/COMPUTATIONAL",
        "packet_sha256": hashlib.sha256(PACKET.read_bytes()).hexdigest(),
        "checker_sha256": hashlib.sha256(CHECKER.read_bytes()).hexdigest(),
        "baseline": baseline,
        "checker_cases": cases,
        "fixture_reachability": reach,
        "discharge_controls": discharge_controls,
        "peer_489_certificate": peer,
        "revised_claim": "Recovered checker rejects extra proof records and all seven fixtures have complete sink ancestry. LSPV-1/489 unit-assumption elimination is valid in ordinary Resolution, but historical R_mix341 RES/DEF/branch admissibility remains open.",
        "open": ["P2-D1", "P2-C3", "P2-B1", "P2-B2"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS",
        "checker_cases": len(cases),
        "fixtures_full_ancestry": len(reach),
        "branch_refutations_transformed": discharge_controls["branch_refutations_transformed"],
        "peer_global_res": peer["global_res"],
        "output": str(OUT.relative_to(ROOT)),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
