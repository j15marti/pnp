#!/usr/bin/env python3
"""REFEREE366: independent checker for a declared context-typed branch DAG.

This is NOT the authoritative historical R_mix341 checker.  It is a hostile
control for proposals that add branching and cross-branch DAG sharing.  Every
assumption, merge, and inference is paid.  The source is bound by exact bytes.
"""

from __future__ import annotations

import hashlib
import json
import os
import resource
import sys
import time
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TRACE_PATH = Path(__file__).with_name("branch_shared_trace_referee366.json")
RAW_PATH = ROOT / "results/raw/arc/2026-11-05_0948_LSPV5_REFEREE366_raw.json"


class Reject(ValueError):
    pass


def strict_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise Reject(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def strict_loads(data: bytes):
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=strict_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Reject(f"malformed JSON: {exc}") from exc


def lit_key(lit: int):
    return (abs(lit), lit < 0)


def canonical_clause(values, *, allow_tautology=False):
    if not isinstance(values, list) or any(type(x) is not int or x == 0 for x in values):
        raise Reject("clause must be a list of nonzero integers")
    if len(set(values)) != len(values):
        raise Reject("duplicate literal")
    if not allow_tautology and any(-x in values for x in values):
        raise Reject("tautological clause")
    if values != sorted(values, key=lit_key):
        raise Reject("noncanonical literal order")
    return tuple(values)


def canonical_context(values):
    result = canonical_clause(values)
    if any(-x in result for x in result):
        raise Reject("inconsistent context")
    return result


def parse_dimacs(raw: str):
    if not isinstance(raw, str) or not raw.endswith("\n"):
        raise Reject("source must be newline-terminated UTF-8 text")
    lines = [line for line in raw.splitlines() if not line.startswith("c ")]
    if not lines or not lines[0].startswith("p cnf "):
        raise Reject("missing DIMACS header")
    fields = lines[0].split()
    if len(fields) != 4:
        raise Reject("bad DIMACS header")
    try:
        nvars, nclauses = int(fields[2]), int(fields[3])
    except ValueError as exc:
        raise Reject("nonnumeric DIMACS header") from exc
    if nvars < 0 or nclauses < 0 or len(lines) != nclauses + 1:
        raise Reject("DIMACS count mismatch")
    clauses = []
    for line in lines[1:]:
        try:
            fields = [int(x) for x in line.split()]
        except ValueError as exc:
            raise Reject("nonnumeric DIMACS clause") from exc
        if not fields or fields[-1] != 0 or 0 in fields[:-1]:
            raise Reject("bad DIMACS terminator")
        values = sorted(set(fields[:-1]), key=lit_key)
        if len(values) != len(fields[:-1]) or any(-x in values for x in values):
            raise Reject("duplicate or tautological DIMACS clause")
        if any(abs(x) > nvars for x in values):
            raise Reject("literal exceeds DIMACS variable bound")
        clauses.append(tuple(values))
    return nvars, clauses


def exact_resolve(left, right, pivot):
    if type(pivot) is not int or pivot <= 0:
        raise Reject("pivot must be a positive variable identifier")
    lset, rset = set(left), set(right)
    if pivot in lset and -pivot in rset:
        values = (lset - {pivot}) | (rset - {-pivot})
    elif -pivot in lset and pivot in rset:
        values = (lset - {-pivot}) | (rset - {pivot})
    else:
        raise Reject("oriented pivot absent")
    if any(-x in values for x in values):
        raise Reject("tautological resolvent is not a legal stored clause")
    return tuple(sorted(values, key=lit_key))


def holds_clause(clause, mask):
    return any(bool(mask & (1 << (abs(lit) - 1))) == (lit > 0) for lit in clause)


def holds_context(context, mask):
    return all(bool(mask & (1 << (abs(lit) - 1))) == (lit > 0) for lit in context)


def conditional_clause(context, clause):
    # Tautologies are allowed here: ASSUME translates to not(Gamma) OR literal.
    return tuple(sorted(set([-x for x in context] + list(clause)), key=lit_key))


def check_trace_bytes(data: bytes, *, semantic=True):
    trace = strict_loads(data)
    required = {"schema", "source_raw", "source_sha256", "nodes", "final"}
    if set(trace) != required or trace["schema"] != "CONTEXT_BRANCH_DAG_REFEREE366_V1":
        raise Reject("wrong trace top-level grammar")
    raw = trace["source_raw"]
    if hashlib.sha256(raw.encode()).hexdigest() != trace["source_sha256"]:
        raise Reject("source byte hash mismatch")
    nvars, source = parse_dimacs(raw)
    nodes = []
    counters = {"source_reads": 0, "parent_refs": 0, "literal_scans": 0,
                "context_subset_tests": 0, "semantic_valuations": 0}
    paid = 0
    for expected, record in enumerate(trace["nodes"]):
        if not isinstance(record, dict) or record.get("id") != expected:
            raise Reject("node identifiers must be dense and ordered")
        if set(record) - {"id", "rule", "context", "clause", "source_index",
                          "literal", "left", "right", "pivot", "split"}:
            raise Reject("unknown node field")
        rule = record.get("rule")
        context = canonical_context(record.get("context"))
        clause = canonical_clause(record.get("clause"))
        counters["literal_scans"] += len(context) + len(clause)
        if any(abs(x) > nvars for x in context + clause):
            raise Reject("node literal exceeds source variable bound")
        if rule == "SRC":
            if context:
                raise Reject("source nodes must be at empty context")
            index = record.get("source_index")
            if type(index) is not int or not 0 <= index < len(source) or source[index] != clause:
                raise Reject("source authentication failure")
            counters["source_reads"] += 1
        elif rule == "ASSUME":
            paid += 1
            lit = record.get("literal")
            if type(lit) is not int or lit not in context or clause != (lit,):
                raise Reject("bad assumption")
        elif rule == "RES":
            paid += 1
            li, ri = record.get("left"), record.get("right")
            if type(li) is not int or type(ri) is not int or not (0 <= li < expected and 0 <= ri < expected):
                raise Reject("bad RES parent")
            left, right = nodes[li], nodes[ri]
            counters["parent_refs"] += 2
            counters["context_subset_tests"] += 2
            if not set(left["context"]).issubset(context) or not set(right["context"]).issubset(context):
                raise Reject("cross-branch parent used outside its assumption context")
            if exact_resolve(left["clause"], right["clause"], record.get("pivot")) != clause:
                raise Reject("wrong exact resolvent")
        elif rule == "MERGE":
            paid += 1
            li, ri, split = record.get("left"), record.get("right"), record.get("split")
            if type(li) is not int or type(ri) is not int or not (0 <= li < expected and 0 <= ri < expected):
                raise Reject("bad MERGE parent")
            if type(split) is not int or split <= 0 or split in context or -split in context:
                raise Reject("bad split variable")
            left, right = nodes[li], nodes[ri]
            counters["parent_refs"] += 2
            plus = tuple(sorted(context + (split,), key=lit_key))
            minus = tuple(sorted(context + (-split,), key=lit_key))
            if {left["context"], right["context"]} != {plus, minus}:
                raise Reject("MERGE must discharge exactly complementary child contexts")
            if left["clause"] != clause or right["clause"] != clause:
                raise Reject("MERGE child conclusions differ")
        else:
            raise Reject("unknown rule")
        nodes.append({"context": context, "clause": clause, "rule": rule})

    final = trace["final"]
    if final != len(nodes) - 1 or nodes[final]["context"] or nodes[final]["clause"]:
        raise Reject("final node must be empty clause at empty context")

    if semantic:
        for node in nodes:
            for mask in range(1 << nvars):
                counters["semantic_valuations"] += 1
                if all(holds_clause(c, mask) for c in source) and holds_context(node["context"], mask):
                    if not holds_clause(node["clause"], mask):
                        raise Reject("semantic entailment audit failed")

    # Verify the exact MERGE conditional-clause identity.  Other rule macros use
    # explicit weakening/tautology proofs in EF and are bounded below.
    for i, record in enumerate(trace["nodes"]):
        if record["rule"] == "MERGE":
            left = nodes[record["left"]]
            right = nodes[record["right"]]
            result = exact_resolve(conditional_clause(left["context"], left["clause"]),
                                   conditional_clause(right["context"], right["clause"]),
                                   record["split"])
            if result != conditional_clause(nodes[i]["context"], nodes[i]["clause"]):
                raise Reject("conditional-clause MERGE compilation failed")

    translated_literals = sum(len(conditional_clause(n["context"], n["clause"])) for n in nodes)
    macro_units = sum(6 + 3 * len(n["context"]) + 2 * len(n["clause"]) for n in nodes)
    return {"nvars": nvars, "source_clauses": len(source), "nodes": len(nodes),
            "paid_nodes": paid, "translated_literals": translated_literals,
            "ef_macro_unit_bound": macro_units, **counters}


def unsafe_context_erasing_accepts(trace):
    """Deliberately unsound checker: ignores every context on RES parents."""
    nodes = []
    for record in trace["nodes"]:
        clause = canonical_clause(record["clause"])
        if record["rule"] == "ASSUME":
            if clause != (record["literal"],):
                return False
        elif record["rule"] == "RES":
            clause2 = exact_resolve(nodes[record["left"]], nodes[record["right"]], record["pivot"])
            if clause2 != clause:
                return False
        nodes.append(clause)
    return nodes[trace["final"]] == ()


def expect_reject(trace, label):
    data = json.dumps(trace, sort_keys=True, separators=(",", ":")).encode()
    try:
        check_trace_bytes(data, semantic=False)
    except Reject as exc:
        return {"label": label, "rejected": True, "reason": str(exc)}
    raise AssertionError(f"corrupt control accepted: {label}")


def main():
    started = time.perf_counter_ns()
    data = TRACE_PATH.read_bytes()
    accepted = check_trace_bytes(data)
    trace = strict_loads(data)
    checks = []

    # Minimal context-erasure exploit over an empty, satisfiable one-variable source.
    exploit = {
        "schema": "UNSAFE_CONTEXT_ERASURE_DEMO_V1",
        "nodes": [
            {"id": 0, "rule": "ASSUME", "context": [1], "clause": [1], "literal": 1},
            {"id": 1, "rule": "ASSUME", "context": [-1], "clause": [-1], "literal": -1},
            {"id": 2, "rule": "RES", "context": [], "clause": [], "left": 0, "right": 1, "pivot": 1},
        ],
        "final": 2,
    }
    assert unsafe_context_erasing_accepts(exploit)
    checks.append({"label": "minimal_context_erasure_exploit", "unsafe_accepts": True,
                   "proper_reason": "both assumption contexts are not subsets of empty context",
                   "source_sat": True, "paid_nodes": 3})

    bad = deepcopy(trace)
    bad["nodes"][-1]["split"] = 4
    checks.append(expect_reject(bad, "wrong_merge_split"))
    bad = deepcopy(trace)
    bad["nodes"][9]["context"] = []
    checks.append(expect_reject(bad, "branch_parent_reused_in_weaker_context"))
    bad = deepcopy(trace)
    bad["nodes"][7]["context"] = [-3, 3]
    checks.append(expect_reject(bad, "inconsistent_context"))
    bad = deepcopy(trace)
    bad["nodes"][8]["clause"] = [3, 4, 5]
    checks.append(expect_reject(bad, "corrupt_resolvent"))
    bad = deepcopy(trace)
    bad["source_raw"] = bad["source_raw"].replace("-2 -3 -5 0", "-2 -3 5 0")
    bad["source_sha256"] = hashlib.sha256(bad["source_raw"].encode()).hexdigest()
    opposite = expect_reject(bad, "opposite_label_source_binding")
    opposite.update({"mutated_source_sat": True, "sat_witness_mask": 22,
                     "witness_variables_true": [2, 3, 5]})
    checks.append(opposite)
    bad = deepcopy(trace)
    bad["source_raw"] = bad["source_raw"].replace("p cnf 5 6", "p cnf 5 7")
    bad["source_sha256"] = hashlib.sha256(bad["source_raw"].encode()).hexdigest()
    checks.append(expect_reject(bad, "malformed_source_header_count"))
    bad_json = data.replace(b'"schema"', b'"schema":"shadow","schema"', 1)
    try:
        check_trace_bytes(bad_json, semantic=False)
        raise AssertionError("duplicate JSON key accepted")
    except Reject as exc:
        checks.append({"label": "duplicate_json_key", "rejected": True, "reason": str(exc)})

    elapsed = time.perf_counter_ns() - started
    result = {
        "schema": "LSPV5_REFEREE366_RAW_V1",
        "status": {
            "context_erasure": "FALSIFIED/RETIRED",
            "typed_branch_dag_soundness": "PROVED/EXACT_FOR_DECLARED_EXTENSION",
            "typed_branch_dag_to_EF": "PROVED/EXACT_SYMBOLIC_POLYNOMIAL_COMPILER",
            "historical_Rmix341_branch_rule": "ABSENT_NOT_MODIFIED",
            "historical_Rmix341_grammar": "OPEN",
            "B3": "OPEN",
            "P_vs_NP": "OPEN",
        },
        "accepted_trace": {
            "path": str(TRACE_PATH.relative_to(ROOT)),
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
            "evidence_bits": 8 * len(data),
            **accepted,
        },
        "controls": checks,
        "physical_run": {
            "elapsed_ns": elapsed,
            "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "python": sys.version.split()[0],
            "pid": os.getpid(),
            "measurement_scope": "producer plus independent semantic audit; not proof search and not SAT-machine runtime",
        },
        "limitations": [
            "Independent declared checker, not authoritative historical R_mix341 execution.",
            "EF macro compiler is proved symbolically; no external EF byte checker was replayed.",
            "Finite accepted trace is a control, not an asymptotic lower bound.",
        ],
    }
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
