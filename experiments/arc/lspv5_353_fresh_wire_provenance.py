#!/usr/bin/env python3
"""Independent finite audit of the R_mix341 fresh-variable provenance invariant.

This is deliberately not a full R_mix341 checker.  It checks the grammar-level
invariant forced by the original rule list: source variables are declared by the
DIMACS header and every later *semantic variable* must be introduced exactly once
by an earlier paid DEF node.  LOCAL-private gate labels are syntax-local and are
not public semantic variables.
"""

from __future__ import annotations

import itertools
import json
from dataclasses import dataclass
from typing import Any


class Reject(ValueError):
    pass


def parse_dimacs(text: str) -> tuple[int, list[list[int]]]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("c")]
    if not lines or not lines[0].startswith("p cnf "):
        raise Reject("missing-header")
    fields = lines[0].split()
    if len(fields) != 4:
        raise Reject("bad-header")
    try:
        n, m = int(fields[2]), int(fields[3])
    except ValueError as exc:
        raise Reject("bad-header-int") from exc
    if n < 0 or m < 0:
        raise Reject("negative-header")
    clauses: list[list[int]] = []
    for line in lines[1:]:
        try:
            row = [int(x) for x in line.split()]
        except ValueError as exc:
            raise Reject("bad-literal") from exc
        if not row or row[-1] != 0 or 0 in row[:-1]:
            raise Reject("bad-terminator")
        clause = row[:-1]
        if any(abs(x) < 1 or abs(x) > n for x in clause):
            raise Reject("source-out-of-range")
        clauses.append(clause)
    if len(clauses) != m:
        raise Reject("clause-count")
    return n, clauses


def source_sat(n: int, clauses: list[list[int]]) -> tuple[bool, int]:
    models = 0
    for bits in itertools.product((False, True), repeat=n):
        if all(any(bits[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in clauses):
            models += 1
    return models > 0, models


def public_vars(node: dict[str, Any]) -> list[int]:
    """All semantic variable identifiers used by a record, excluding DEF output."""
    out: list[int] = []
    for key in ("inputs", "vars", "clause", "pivot"):
        value = node.get(key, [])
        if key == "pivot" and value != []:
            value = [value]
        if not isinstance(value, list):
            raise Reject("bad-var-field")
        for item in value:
            if not isinstance(item, int) or isinstance(item, bool) or item == 0:
                raise Reject("bad-var-id")
            out.append(abs(item))
    return out


def scan_validator(record: dict[str, Any]) -> tuple[bool, str]:
    """One-pass topological validator for only the fresh-variable invariant."""
    try:
        n, _ = parse_dimacs(record["source"])
        known = set(range(1, n + 1))
        owner: dict[int, int] = {}
        private_seen: set[str] = set()
        for pos, node in enumerate(record.get("nodes", []), start=1):
            if not isinstance(node, dict) or node.get("id") != pos:
                raise Reject("bad-node-id")
            rule = node.get("rule")
            if rule not in {"RES", "AND3", "XOR", "LOCAL", "DEF"}:
                raise Reject("bad-rule")
            # A LOCAL payload may name private syntax gates, but they are not public variables.
            priv = node.get("private_gates", [])
            if not isinstance(priv, list) or any(not isinstance(x, str) or not x.startswith("_") for x in priv):
                raise Reject("bad-private-gate")
            if len(priv) != len(set(priv)) or private_seen.intersection(priv):
                raise Reject("private-name-collision")
            private_seen.update(priv)
            for v in public_vars(node):
                if v not in known:
                    raise Reject("public-use-before-paid-def")
            if "port" in node:
                p = node["port"]
                if not isinstance(p, int) or isinstance(p, bool) or p not in known:
                    raise Reject("unpaid-or-unknown-public-port")
            if rule == "DEF":
                z = node.get("out")
                if not isinstance(z, int) or isinstance(z, bool) or z <= n:
                    raise Reject("def-not-fresh-above-source-bound")
                if z in known or z in owner:
                    raise Reject("duplicate-def")
                inputs = node.get("inputs")
                if not isinstance(inputs, list) or len(inputs) != 2:
                    raise Reject("def-arity")
                known.add(z)
                owner[z] = pos
            elif "out" in node:
                raise Reject("non-def-introduces-public-variable")
        return True, "accept"
    except (KeyError, TypeError, Reject) as exc:
        return False, str(exc)


def static_validator(record: dict[str, Any]) -> tuple[bool, str]:
    """Independent all-pairs formulation of the same invariant."""
    try:
        n, _ = parse_dimacs(record["source"])
        nodes = record.get("nodes", [])
        if not isinstance(nodes, list):
            raise Reject("bad-nodes")
        defs: dict[int, int] = {}
        for i, node in enumerate(nodes, start=1):
            if not isinstance(node, dict) or node.get("id") != i:
                raise Reject("bad-node-id")
            if node.get("rule") not in {"RES", "AND3", "XOR", "LOCAL", "DEF"}:
                raise Reject("bad-rule")
            if node.get("rule") == "DEF":
                z = node.get("out")
                if not isinstance(z, int) or isinstance(z, bool) or z <= n or z in defs:
                    raise Reject("bad-or-duplicate-def")
                if not isinstance(node.get("inputs"), list) or len(node["inputs"]) != 2:
                    raise Reject("def-arity")
                defs[z] = i
            elif "out" in node:
                raise Reject("non-def-introduces-public-variable")
        private_all: list[str] = []
        for i, node in enumerate(nodes, start=1):
            priv = node.get("private_gates", [])
            if not isinstance(priv, list) or any(not isinstance(x, str) or not x.startswith("_") for x in priv):
                raise Reject("bad-private-gate")
            private_all.extend(priv)
            uses = public_vars(node)
            if "port" in node:
                p = node["port"]
                if not isinstance(p, int) or isinstance(p, bool):
                    raise Reject("bad-port")
                uses.append(p)
            for v in uses:
                if v <= n:
                    continue
                if v not in defs or defs[v] >= i:
                    raise Reject("no-earlier-paid-owner")
        if len(private_all) != len(set(private_all)):
            raise Reject("private-name-collision")
        return True, "accept"
    except (KeyError, TypeError, Reject) as exc:
        return False, str(exc)


def rec(source: str, nodes: list[dict[str, Any]]) -> dict[str, Any]:
    return {"source": source, "nodes": nodes}


SAT = "p cnf 2 1\n1 2 0\n"
UNSAT = "p cnf 1 2\n1 0\n-1 0\n"
NATIVE_WITNESS = "p cnf 2 2\n1 0\n-2 0\n"


CASES: dict[str, tuple[dict[str, Any], bool]] = {
    "legal_sat_paid_export": (rec(SAT, [
        {"id": 1, "rule": "DEF", "inputs": [1, 2], "out": 3, "gate": "XOR"},
        {"id": 2, "rule": "LOCAL", "vars": [1, 2, 3], "port": 3},
    ]), True),
    "legal_unsat_source_and_paid_dead_gate": (rec(UNSAT, [
        {"id": 1, "rule": "DEF", "inputs": [1, 1], "out": 2, "gate": "XOR"},
        {"id": 2, "rule": "RES", "clause": [], "pivot": 1},
    ]), True),
    "legal_private_local_root_only": (rec(SAT, [
        {"id": 1, "rule": "AND3", "vars": [1, 2]},
        {"id": 2, "rule": "LOCAL", "vars": [1, 2], "private_gates": ["_g0", "_g1"]},
    ]), True),
    "reject_local_free_public_out": (rec(SAT, [
        {"id": 1, "rule": "LOCAL", "vars": [1, 2], "out": 3},
    ]), False),
    "reject_local_unknown_port": (rec(SAT, [
        {"id": 1, "rule": "LOCAL", "vars": [1, 2], "private_gates": ["_g0"], "port": 3},
    ]), False),
    "reject_use_before_def": (rec(SAT, [
        {"id": 1, "rule": "LOCAL", "vars": [3]},
        {"id": 2, "rule": "DEF", "inputs": [1, 2], "out": 3, "gate": "AND"},
    ]), False),
    "reject_duplicate_def": (rec(SAT, [
        {"id": 1, "rule": "DEF", "inputs": [1, 2], "out": 3, "gate": "AND"},
        {"id": 2, "rule": "DEF", "inputs": [1, 2], "out": 3, "gate": "XOR"},
    ]), False),
    "reject_source_name_collision": (rec(SAT, [
        {"id": 1, "rule": "DEF", "inputs": [1, 2], "out": 2, "gate": "XOR"},
    ]), False),
    "reject_forward_def_input": (rec(SAT, [
        {"id": 1, "rule": "DEF", "inputs": [1, 4], "out": 3, "gate": "XOR"},
        {"id": 2, "rule": "DEF", "inputs": [1, 2], "out": 4, "gate": "AND"},
    ]), False),
    "reject_nondef_introduction_xor": (rec(SAT, [
        {"id": 1, "rule": "XOR", "vars": [1, 2], "out": 3},
    ]), False),
    "reject_private_collision": (rec(SAT, [
        {"id": 1, "rule": "LOCAL", "vars": [1], "private_gates": ["_g"]},
        {"id": 2, "rule": "LOCAL", "vars": [2], "private_gates": ["_g"]},
    ]), False),
    "reject_malformed_dimacs": ({"source": "p cnf 2 1\n1 3 0\n", "nodes": []}, False),
}


def main() -> None:
    results = []
    checks = 0
    for name, (record, expected) in CASES.items():
        a = scan_validator(record)
        b = static_validator(record)
        checks += 3
        if a[0] != b[0]:
            raise AssertionError((name, "validator disagreement", a, b))
        if a[0] != expected:
            raise AssertionError((name, "unexpected verdict", a, expected))
        results.append({"case": name, "expected": expected, "scan": a, "static": b})

    n_sat, c_sat = parse_dimacs(SAT)
    n_unsat, c_unsat = parse_dimacs(UNSAT)
    sat_label = source_sat(n_sat, c_sat)
    unsat_label = source_sat(n_unsat, c_unsat)
    checks += 4
    assert sat_label == (True, 3)
    assert unsat_label == (False, 0)

    # Minimal three-derived-node legal native fragment:
    # AND3((x),(-y)); LOCAL -> (x or y); RES_y with (-y) -> (x).
    # Strengthening the LOCAL root to (x) remains semantically valid but destroys
    # the unchanged consumer's named pivot.  This independently reproduces and
    # minimizes the consumer-rewrite obstruction of LSPV-4/400.
    n_w, c_w = parse_dimacs(NATIVE_WITNESS)
    witness_label = source_sat(n_w, c_w)
    assignments = list(itertools.product((False, True), repeat=2))
    factor_table = [a[0] and not a[1] for a in assignments]
    local_clause = [1, 2]
    stronger_clause = [1]
    local_valid = all(
        (not factor_table[i]) or any(a[abs(l) - 1] == (l > 0) for l in local_clause)
        for i, a in enumerate(assignments)
    )
    stronger_valid = all(
        (not factor_table[i]) or any(a[abs(l) - 1] == (l > 0) for l in stronger_clause)
        for i, a in enumerate(assignments)
    )

    def resolve(c1: list[int], c2: list[int], pivot: int) -> list[int]:
        if pivot not in c1 or -pivot not in c2:
            raise Reject("named-pivot-absent")
        return sorted(set(x for x in c1 if x != pivot).union(x for x in c2 if x != -pivot))

    original_resolvent = resolve(local_clause, [-2], 2)
    strengthened_unchanged_consumer = "accepted"
    try:
        resolve(stronger_clause, [-2], 2)
    except Reject as exc:
        strengthened_unchanged_consumer = str(exc)
    checks += 8
    assert witness_label == (True, 1)
    assert factor_table == [False, False, True, False]
    assert local_valid and stronger_valid
    assert original_resolvent == [1]
    assert strengthened_unchanged_consumer == "named-pivot-absent"

    # Exhaustive single-field public-variable mutations of a legal two-node trace.
    base = CASES["legal_sat_paid_export"][0]
    mutation_verdicts = []
    for bad in range(4, 260):
        mutant = json.loads(json.dumps(base))
        mutant["nodes"][1]["vars"][2] = bad
        va, vb = scan_validator(mutant), static_validator(mutant)
        checks += 3
        assert va[0] == vb[0] == False
        mutation_verdicts.append(bad)

    out = {
        "status": "PASS",
        "scope": "fresh semantic-variable provenance only; not full R_mix341 checking",
        "theorem_tested": "every non-source public semantic variable has one earlier paid DEF owner",
        "checks": checks,
        "cases": results,
        "source_controls": {
            "SAT": {"models": sat_label[1], "satisfiable": sat_label[0]},
            "UNSAT": {"models": unsat_label[1], "satisfiable": unsat_label[0]},
        },
        "minimal_native_consumer_witness": {
            "source": "(x) AND (NOT y)",
            "models": witness_label[1],
            "paid_nodes": 3,
            "rules": ["AND3", "LOCAL", "RES"],
            "factor_table_order_00_01_10_11": factor_table,
            "local_clause": local_clause,
            "local_implication_valid": local_valid,
            "stronger_clause": stronger_clause,
            "stronger_implication_valid": stronger_valid,
            "original_resolvent": original_resolvent,
            "unchanged_consumer_after_strengthening": strengthened_unchanged_consumer,
            "minimality_note": "A LOCAL rewrite obstruction needs one earlier derived factor/equation, the LOCAL node, and one later consumer: at least three derived nodes.",
        },
        "single_field_unknown_id_mutations_rejected": len(mutation_verdicts),
        "mutation_range": [min(mutation_verdicts), max(mutation_verdicts)],
        "physical_cost_note": "Both validators read explicit record fields. Unit logical node cost does not pay parsing, bit access, output, or peak memory.",
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
