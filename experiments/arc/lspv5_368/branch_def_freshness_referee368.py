#!/usr/bin/env python3
"""REFEREE368: branch-local extension freshness counterexample and repair.

This is a declared comparison format, not the authoritative historical
R_mix341 checker.  It demonstrates why a branch wrapper around extension
rules must make definition outputs globally fresh from source/context names.
"""

from __future__ import annotations

import copy
import hashlib
import itertools
import json
import resource
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
RAW = ROOT / "results/raw/arc/2026-11-05_1148_LSPV5_REFEREE368_raw.json"


def canon_clause(xs):
    xs = [int(x) for x in xs]
    if 0 in xs:
        raise ValueError("zero literal")
    if len(set(xs)) != len(xs):
        raise ValueError("duplicate literal")
    if any(-x in xs for x in xs):
        raise ValueError("tautological clause")
    return sorted(xs, key=lambda z: (abs(z), z < 0))


def canon_ctx(xs):
    return canon_clause(xs)


def parse_dimacs(text):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.startswith("c")]
    if not lines or not lines[0].startswith("p cnf "):
        raise ValueError("missing strict header")
    parts = lines[0].split()
    if len(parts) != 4:
        raise ValueError("bad header arity")
    nvars, nclauses = int(parts[2]), int(parts[3])
    clauses = []
    for ln in lines[1:]:
        toks = [int(x) for x in ln.split()]
        if not toks or toks[-1] != 0 or 0 in toks[:-1]:
            raise ValueError("bad clause terminator")
        c = canon_clause(toks[:-1])
        if any(abs(x) > nvars for x in c):
            raise ValueError("source literal out of range")
        clauses.append(c)
    if len(clauses) != nclauses:
        raise ValueError("clause count mismatch")
    return nvars, clauses


def clause_true(clause, assignment):
    return any(assignment[abs(l)] == (l > 0) for l in clause)


def model_count(nvars, clauses):
    total = 0
    for bits in itertools.product((False, True), repeat=nvars):
        a = {i + 1: bits[i] for i in range(nvars)}
        total += all(clause_true(c, a) for c in clauses)
    return total


def facet_valid(output, inputs, table, clause):
    variables = sorted(set([output, *inputs]))
    if len(table) != 4 or any(ch not in "01" for ch in table):
        return False
    for bits in itertools.product((False, True), repeat=len(variables)):
        a = dict(zip(variables, bits))
        idx = 2 * int(a[inputs[0]]) + int(a[inputs[1]])
        if a[output] == (table[idx] == "1") and not clause_true(clause, a):
            return False
    return True


def resolve(c1, c2, pivot):
    if pivot not in c1 or -pivot not in c2:
        raise ValueError("oriented pivot absent")
    out = [x for x in c1 if x != pivot] + [x for x in c2 if x != -pivot]
    return canon_clause(out)


def make_unsafe_trace():
    # SAT source with four models.  A flawed branch-local freshness discipline
    # lets each branch redefine the assumption variable incompatibly.
    return {
        "format": "REFEREE368-branch-def-v1",
        "source_dimacs": "p cnf 2 0\n",
        "nodes": [
            {"rule": "ASSUME", "ctx": [1], "clause": [1]},
            {"rule": "DEF", "ctx": [1], "output": 1, "inputs": [2, 2], "table": "0000", "clause": [-1]},
            {"rule": "RES", "ctx": [1], "parents": [0, 1], "pivot": 1, "clause": []},
            {"rule": "ASSUME", "ctx": [-1], "clause": [-1]},
            {"rule": "DEF", "ctx": [-1], "output": 1, "inputs": [2, 2], "table": "1111", "clause": [1]},
            {"rule": "RES", "ctx": [-1], "parents": [4, 3], "pivot": 1, "clause": []},
            {"rule": "MERGE", "ctx": [], "parents": [2, 5], "pivot": 1, "clause": []},
        ],
    }


def make_safe_trace():
    # Established branch pattern on an UNSAT 2-CNF core, augmented by two
    # genuinely fresh branch-local definitions.  The definitions are not
    # needed for the contradiction; they are positive grammar controls.
    return {
        "format": "REFEREE368-branch-def-v1",
        "source_dimacs": "p cnf 2 3\n1 2 0\n-1 2 0\n-2 0\n",
        "nodes": [
            {"rule": "SRC", "ctx": [], "source": 0, "clause": [1, 2]},
            {"rule": "SRC", "ctx": [], "source": 1, "clause": [-1, 2]},
            {"rule": "SRC", "ctx": [], "source": 2, "clause": [-2]},
            {"rule": "ASSUME", "ctx": [1], "clause": [1]},
            {"rule": "RES", "ctx": [1], "parents": [3, 1], "pivot": 1, "clause": [2]},
            {"rule": "DEF", "ctx": [1], "output": 3, "inputs": [2, 2], "table": "0001", "clause": [-3, 2]},
            {"rule": "ASSUME", "ctx": [-1], "clause": [-1]},
            {"rule": "RES", "ctx": [-1], "parents": [0, 6], "pivot": 1, "clause": [2]},
            {"rule": "DEF", "ctx": [-1], "output": 4, "inputs": [2, 2], "table": "0001", "clause": [-4, 2]},
            {"rule": "MERGE", "ctx": [], "parents": [4, 7], "pivot": 1, "clause": [2]},
            {"rule": "RES", "ctx": [], "parents": [9, 2], "pivot": 2, "clause": []},
        ],
    }


def verify(trace, freshness):
    if freshness not in {"unsafe_branch_local", "safe_global"}:
        raise ValueError("unknown freshness mode")
    nvars, sources = parse_dimacs(trace["source_dimacs"])
    records = []
    def_owners = set()
    ops = {"source_reads": 0, "parent_reads": 0, "literal_scans": 0, "context_tests": 0}
    for idx, node in enumerate(trace["nodes"]):
        rule = node["rule"]
        ctx = canon_ctx(node["ctx"])
        clause = canon_clause(node["clause"])
        ops["literal_scans"] += len(ctx) + len(clause)
        if rule == "SRC":
            if ctx:
                raise ValueError("source under nonempty context")
            s = int(node["source"])
            if s < 0 or s >= len(sources) or clause != sources[s]:
                raise ValueError("source authentication failure")
            ops["source_reads"] += 1
        elif rule == "ASSUME":
            if len(clause) != 1 or clause[0] not in ctx:
                raise ValueError("bad assumption")
        elif rule == "DEF":
            output = int(node["output"])
            inputs = [int(x) for x in node["inputs"]]
            if len(inputs) != 2 or min(output, *inputs) <= 0:
                raise ValueError("bad definition identifiers")
            if freshness == "unsafe_branch_local":
                owner = (tuple(ctx), output)
                if owner in def_owners:
                    raise ValueError("duplicate branch-local owner")
            else:
                owner = output
                if output <= nvars or output in inputs or output in map(abs, ctx):
                    raise ValueError("definition output not globally fresh from source/context/input")
                if owner in def_owners:
                    raise ValueError("duplicate global owner")
            def_owners.add(owner)
            if not facet_valid(output, inputs, node["table"], clause):
                raise ValueError("invalid definition facet")
        elif rule == "RES":
            a, b = map(int, node["parents"])
            if not (0 <= a < idx and 0 <= b < idx):
                raise ValueError("bad/cyclic parent")
            ops["parent_reads"] += 2
            r1, r2 = records[a], records[b]
            ops["context_tests"] += 2
            if not set(r1[0]).issubset(ctx) or not set(r2[0]).issubset(ctx):
                raise ValueError("context leak")
            if resolve(r1[1], r2[1], int(node["pivot"])) != clause:
                raise ValueError("wrong resolvent")
        elif rule == "MERGE":
            a, b = map(int, node["parents"])
            if not (0 <= a < idx and 0 <= b < idx):
                raise ValueError("bad/cyclic merge parent")
            ops["parent_reads"] += 2
            ra, rb = records[a], records[b]
            p = int(node["pivot"])
            if ra[1] != clause or rb[1] != clause:
                raise ValueError("merge conclusions differ")
            expected = {tuple(canon_ctx([*ctx, p])), tuple(canon_ctx([*ctx, -p]))}
            if {tuple(ra[0]), tuple(rb[0])} != expected:
                raise ValueError("omitted/wrong AND branch")
        else:
            raise ValueError("unknown rule")
        records.append((ctx, clause))
    if not records or records[-1] != ([], []):
        raise ValueError("final node is not unconditional contradiction")
    return {"nvars": nvars, "source_clauses": len(sources), "nodes": len(records), "ops": ops}


def expect_reject(trace, freshness, label):
    try:
        verify(trace, freshness)
    except ValueError as exc:
        return {"label": label, "rejected": True, "reason": str(exc)}
    raise AssertionError(f"control unexpectedly accepted: {label}")


def canonical_bytes(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode()


def main():
    start = time.perf_counter_ns()
    unsafe = make_unsafe_trace()
    safe = make_safe_trace()

    unsafe_path = HERE / "unsafe_branch_def_referee368.json"
    safe_path = HERE / "safe_branch_def_referee368.json"
    unsafe_path.write_bytes(canonical_bytes(unsafe))
    safe_path.write_bytes(canonical_bytes(safe))

    unsafe_result = verify(unsafe, "unsafe_branch_local")
    safe_result = verify(safe, "safe_global")
    controls = []
    controls.append(expect_reject(unsafe, "safe_global", "source/context variable reused as DEF output"))

    bad = copy.deepcopy(safe)
    bad["nodes"][5]["output"] = 1
    bad["nodes"][5]["clause"] = [-1, 2]
    controls.append(expect_reject(bad, "safe_global", "branch assumption reused as output"))

    bad = copy.deepcopy(safe)
    bad["nodes"][8]["output"] = 3
    bad["nodes"][8]["clause"] = [-3, 2]
    controls.append(expect_reject(bad, "safe_global", "global output owner reused across branches"))

    bad = copy.deepcopy(safe)
    bad["nodes"][5]["clause"] = [3, 2]
    controls.append(expect_reject(bad, "safe_global", "corrupt DEF facet"))

    bad = copy.deepcopy(safe)
    bad["nodes"][9]["parents"] = [4, 4]
    controls.append(expect_reject(bad, "safe_global", "omitted negative AND branch"))

    bad = copy.deepcopy(safe)
    bad["nodes"][7]["ctx"] = []
    controls.append(expect_reject(bad, "safe_global", "branch-local conclusion leaked"))

    bad = copy.deepcopy(safe)
    bad["source_dimacs"] = bad["source_dimacs"].replace("p cnf 2 3", "p cnf 2 4")
    controls.append(expect_reject(bad, "safe_global", "malformed source clause count"))

    elapsed = time.perf_counter_ns() - start
    payload = {
        "artifact": "REFEREE368",
        "status": {
            "unsafe_wrapper": "explicit accepted false refutation in declared flawed checker",
            "safe_wrapper": "finite accepted scope/freshness control",
            "historical_rmix341": "not executed; grammar authentication remains open",
            "b3": "open",
            "p_vs_np": "open",
        },
        "unsafe": {
            **unsafe_result,
            "source_models": model_count(*parse_dimacs(unsafe["source_dimacs"])),
            "bytes": len(canonical_bytes(unsafe)),
            "sha256": hashlib.sha256(canonical_bytes(unsafe)).hexdigest(),
        },
        "safe": {
            **safe_result,
            "source_models": model_count(*parse_dimacs(safe["source_dimacs"])),
            "bytes": len(canonical_bytes(safe)),
            "sha256": hashlib.sha256(canonical_bytes(safe)).hexdigest(),
        },
        "controls": controls,
        "runtime": {
            "elapsed_ns": elapsed,
            "ru_maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        },
    }
    RAW.write_bytes((json.dumps(payload, indent=2, sort_keys=True) + "\n").encode())
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
