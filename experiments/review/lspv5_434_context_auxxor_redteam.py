#!/usr/bin/env python3
"""Independent LSPV-5/434 contextual auxiliary-XOR audit.

This checks a separately declared context/DEF/LOCAL/GF2/DISCHARGE grammar.
It is not the historical R_mix341 checker.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import resource
import time


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


ORIGINALS = ("r", "x")
SOURCE = (
    ("-r", "x"),
    ("-r", "-x"),
    ("r", "x"),
    ("r", "-x"),
)
DEF = {"z": ("xor", "r", "x")}


def lit_value(literal: str, assignment: dict[str, int]) -> bool:
    negative = literal.startswith("-")
    name = literal[1:] if negative else literal
    require(name in assignment, "literal outside assignment")
    value = bool(assignment[name])
    return not value if negative else value


def clause_value(clause: tuple[str, ...], assignment: dict[str, int]) -> bool:
    return any(lit_value(literal, assignment) for literal in clause)


def wire_value(name: str, assignment: dict[str, int], stack: tuple[str, ...] = ()) -> int:
    if name in assignment:
        return assignment[name]
    require(name in DEF and name not in stack, "undefined or cyclic wire")
    op, left, right = DEF[name]
    require(op == "xor", "unsupported gate")
    return wire_value(left, assignment, stack + (name,)) ^ wire_value(
        right, assignment, stack + (name,)
    )


def row_value(row: dict, assignment: dict[str, int]) -> bool:
    value = 0
    for term in row["terms"]:
        value ^= wire_value(term, assignment)
    return value == row["rhs"]


TRACE = (
    {"id": "d1", "rule": "DEF", "parents": (), "context": (), "wire": "z"},
    {
        "id": "d2",
        "rule": "LOCAL",
        "parents": ("s0", "d1"),
        "context": ("r",),
        "row": {"terms": ("z",), "rhs": 0},
    },
    {
        "id": "d3",
        "rule": "LOCAL",
        "parents": ("s1", "d1"),
        "context": ("r",),
        "row": {"terms": ("z",), "rhs": 1},
    },
    {
        "id": "d4",
        "rule": "GF2ADD",
        "parents": ("d2", "d3"),
        "context": ("r",),
        "row": {"terms": (), "rhs": 1},
    },
    {
        "id": "d5",
        "rule": "LOCAL",
        "parents": ("s2", "d1"),
        "context": ("-r",),
        "row": {"terms": ("z",), "rhs": 1},
    },
    {
        "id": "d6",
        "rule": "LOCAL",
        "parents": ("s3", "d1"),
        "context": ("-r",),
        "row": {"terms": ("z",), "rhs": 0},
    },
    {
        "id": "d7",
        "rule": "GF2ADD",
        "parents": ("d5", "d6"),
        "context": ("-r",),
        "row": {"terms": (), "rhs": 1},
    },
    {
        "id": "d8",
        "rule": "DISCHARGE",
        "parents": ("d4", "d7"),
        "context": (),
        "pivot": "r",
        "row": {"terms": (), "rhs": 1},
    },
)


def xor_rows(left: dict, right: dict) -> dict:
    terms: set[str] = set(left["terms"])
    for term in right["terms"]:
        if term in terms:
            terms.remove(term)
        else:
            terms.add(term)
    return {"terms": tuple(sorted(terms)), "rhs": left["rhs"] ^ right["rhs"]}


def verify_trace(trace=TRACE, source=SOURCE) -> dict:
    index: dict[str, dict] = {
        f"s{i}": {"kind": "source", "clause": clause} for i, clause in enumerate(source)
    }
    locals_checked = 0
    add_checks = 0
    for node in trace:
        require(node["id"] not in index, "duplicate ID")
        require(all(parent in index for parent in node["parents"]), "missing/forward parent")
        context = tuple(node["context"])
        require(not ({literal for literal in context} & {"-" + literal for literal in context}), "inconsistent context")
        if node["rule"] == "DEF":
            require(node["id"] == "d1" and node["wire"] == "z", "wrong definition")
            require(not context and not node["parents"], "definition must be global")
        elif node["rule"] == "LOCAL":
            source_parent, def_parent = node["parents"]
            require(index[source_parent]["kind"] == "source", "LOCAL source provenance")
            require(def_parent == "d1", "LOCAL definition provenance")
            for bits in itertools.product((0, 1), repeat=2):
                assignment = dict(zip(ORIGINALS, bits))
                if all(lit_value(literal, assignment) for literal in context) and clause_value(
                    index[source_parent]["clause"], assignment
                ):
                    require(row_value(node["row"], assignment), "LOCAL semantic failure")
                locals_checked += 1
        elif node["rule"] == "GF2ADD":
            left, right = (index[parent] for parent in node["parents"])
            require(left["context"] == context == right["context"], "cross-context addition")
            require(xor_rows(left["row"], right["row"]) == node["row"], "wrong GF2 sum")
            for bits in itertools.product((0, 1), repeat=2):
                assignment = dict(zip(ORIGINALS, bits))
                if all(lit_value(literal, assignment) for literal in context):
                    if row_value(left["row"], assignment) and row_value(right["row"], assignment):
                        require(row_value(node["row"], assignment), "unsound GF2 sum")
                    add_checks += 1
        elif node["rule"] == "DISCHARGE":
            left, right = (index[parent] for parent in node["parents"])
            pivot = node["pivot"]
            require(left["context"] == context + (pivot,), "missing positive branch")
            require(right["context"] == context + ("-" + pivot,), "missing negative branch")
            require(left["row"] == node["row"] == right["row"], "branch conclusions differ")
            require(node["row"] == {"terms": (), "rhs": 1}, "discharge target not false")
        else:
            raise AssertionError("unknown rule")
        index[node["id"]] = {"kind": "derived", **node}
    require(index[trace[-1]["id"]]["row"] == {"terms": (), "rhs": 1}, "no final false")
    return {"local_assignment_checks": locals_checked, "gf2_assignment_checks": add_checks}


def resolve(left: tuple[str, ...], right: tuple[str, ...], pivot: str) -> tuple[str, ...]:
    require(pivot in left and "-" + pivot in right, "oriented pivot absent")
    output = []
    for literal in left + right:
        if literal in (pivot, "-" + pivot):
            continue
        if literal not in output:
            output.append(literal)
    require(not any(("-" + literal) in output for literal in output if not literal.startswith("-")), "tautological resolvent")
    return tuple(output)


def verify_target_resolution() -> dict:
    minus_r = resolve(SOURCE[0], SOURCE[1], "x")
    plus_r = resolve(SOURCE[2], SOURCE[3], "r") if False else None
    # Orient the second branch on x first, then discharge on r.
    plus_r = resolve(SOURCE[2], SOURCE[3], "x")
    empty = resolve(plus_r, minus_r, "r")
    require(minus_r == ("-r",) and plus_r == ("r",) and empty == (), "compiled target mismatch")
    return {"target_paid_resolution_nodes": 3, "target_final_lines": [minus_r, plus_r, empty]}


def wide_affine_control(width: int = 12) -> dict:
    names = tuple(f"u{i}" for i in range(width))
    checks = 0
    projection_lines = []
    for r, x in itertools.product((0, 1), repeat=2):
        projection_lines.append({"guard_assignment": {"r": r, "x": x}, "rhs": r ^ x})
    for bits in itertools.product((0, 1), repeat=width + 2):
        assignment = {"r": bits[0], "x": bits[1], **dict(zip(names, bits[2:]))}
        direct = wire_value("z", assignment)
        for name in names:
            direct ^= assignment[name]
        rhs = assignment["r"] ^ assignment["x"]
        projected = rhs
        for name in names:
            projected ^= assignment[name]
        require((direct == 0) == (projected == 0), "compact affine projection mismatch")
        checks += 1
    return {
        "direct_original_terms": width,
        "auxiliary_ancestor_cone": 2,
        "respc_projection_lines": len(projection_lines),
        "ordinary_canonical_support": width + 2,
        "ordinary_canonical_false_clauses": 1 << (width + 1),
        "semantic_checks": checks,
    }


def reject_mutations() -> list[str]:
    rejected = []

    def attempt(name: str, mutate) -> None:
        trace = json.loads(json.dumps(TRACE))
        source = json.loads(json.dumps(SOURCE))
        mutate(trace, source)
        try:
            verify_trace(trace, source)
        except (AssertionError, KeyError, TypeError):
            rejected.append(name)
            return
        raise AssertionError(f"mutation accepted: {name}")

    attempt("missing-negative-branch", lambda t, s: t.__delitem__(6))
    attempt("cross-branch-row-reuse", lambda t, s: t[6].update(parents=["d2", "d6"]))
    attempt("branch-scoped-definition", lambda t, s: t[0].update(context=["r"]))
    attempt("wrong-gf2-rhs", lambda t, s: t[3].update(row={"terms": [], "rhs": 0}))
    attempt("wrong-local-row", lambda t, s: t[1].update(row={"terms": ["z"], "rhs": 1}))
    attempt("missing-source-parent", lambda t, s: t[1].update(parents=["ghost", "d1"]))
    attempt("bad-discharge-pivot", lambda t, s: t[7].update(pivot="x"))
    attempt("source-sign-mutation", lambda t, s: s[0].__setitem__(0, "r"))
    return rejected


def malformed_controls() -> int:
    bad = [
        "p cnf 2 1\n1 -0",
        "p cnf 2 1\n3 0",
        "p cnf 2 1\n1",
        "p cnf 2 2\n1 0",
        "p cnf -2 1\n1 0",
    ]
    rejected = 0
    for text in bad:
        tokens = text.split()
        valid = len(tokens) >= 5 and tokens[:2] == ["p", "cnf"] and tokens[2].isdigit() and tokens[3].isdigit()
        if valid:
            n, m = int(tokens[2]), int(tokens[3])
            clauses, current = [], []
            try:
                for token in tokens[4:]:
                    require(token == "0" or (token.lstrip("-").isdigit() and token not in ("-0", "")), "token")
                    value = int(token)
                    if value == 0:
                        clauses.append(tuple(current)); current = []
                    else:
                        require(1 <= abs(value) <= n, "range")
                        current.append(value)
                require(not current and len(clauses) == m, "termination/count")
            except AssertionError:
                valid = False
        if not valid:
            rejected += 1
    require(rejected == len(bad), "malformed input accepted")
    return rejected


def main() -> None:
    started = time.perf_counter_ns()
    trace_checks = verify_trace()
    target = verify_target_resolution()
    wide = wide_affine_control()
    rejected = reject_mutations()
    malformed = malformed_controls()
    models = []
    for bits in itertools.product((0, 1), repeat=2):
        assignment = dict(zip(ORIGINALS, bits))
        if all(clause_value(clause, assignment) for clause in SOURCE):
            models.append(bits)
    require(not models, "source should be UNSAT")
    deletion_models = []
    for omit in range(len(SOURCE)):
        witnesses = []
        for bits in itertools.product((0, 1), repeat=2):
            assignment = dict(zip(ORIGINALS, bits))
            if all(clause_value(clause, assignment) for i, clause in enumerate(SOURCE) if i != omit):
                witnesses.append("".join(map(str, bits)))
        require(witnesses, "single deletion should be SAT")
        deletion_models.append(witnesses[0])
    trace_bytes = json.dumps(TRACE, sort_keys=True, separators=(",", ":"), default=list).encode()
    result = {
        "status": "PASS",
        "claim": "P2-L5-434",
        "system": "distinct R_ctx_extxor434; NOT historical R_mix341",
        "source": [list(clause) for clause in SOURCE],
        "source_unsat_models": len(models),
        "single_deletion_sat_witnesses": deletion_models,
        "paid_nodes": len(TRACE),
        "shared_global_definitions": 1,
        "local_nodes": 4,
        "gf2_add_nodes": 2,
        "discharge_nodes": 1,
        "max_auxiliary_ancestor_cone": 2,
        "trace_bytes": len(trace_bytes),
        "trace_sha256": hashlib.sha256(trace_bytes).hexdigest(),
        **trace_checks,
        **target,
        "wide_affine_control": wide,
        "corrupted_controls_rejected": rejected,
        "malformed_controls_rejected": malformed,
        "elapsed_ns": time.perf_counter_ns() - started,
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "limitations": [
            "No historical R_mix341 checker executed for the new contextual trace.",
            "Finite controls do not prove the symbolic compiler theorem.",
            "LOCAL is a declared semantic/source-authenticated rule in the distinct test calculus.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
