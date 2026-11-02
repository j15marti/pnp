#!/usr/bin/env python3
"""Finite controls for REFEREE296's black-box relativization firewall.

The asymptotic barrier is a symbolic oracle argument.  This program checks the
declared ordinary CNF grammar, a one-query exact SAT oracle decider, the
failure of transcript-only UNSAT evidence, and ordinary Resolution+Weakening
proof verification on both labels.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
import tracemalloc
from dataclasses import dataclass

Clause = frozenset[int]


@dataclass(frozen=True)
class CNF:
    nvars: int
    clauses: tuple[Clause, ...]


def parse_dimacs(text: str) -> CNF:
    lines = [line.strip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith("c")]
    if not lines:
        raise ValueError("empty")
    head = lines[0].split()
    if len(head) != 4 or head[:2] != ["p", "cnf"]:
        raise ValueError("bad header")
    try:
        nvars, nclauses = int(head[2]), int(head[3])
    except ValueError as exc:
        raise ValueError("noninteger header") from exc
    if nvars < 1 or nclauses < 1 or len(lines) != nclauses + 1:
        raise ValueError("bad counts")
    clauses: list[Clause] = []
    for line in lines[1:]:
        try:
            vals = [int(x) for x in line.split()]
        except ValueError as exc:
            raise ValueError("noninteger literal") from exc
        if len(vals) < 2 or vals[-1] != 0 or 0 in vals[:-1]:
            raise ValueError("bad terminator")
        lits = vals[:-1]
        if any(abs(x) > nvars for x in lits):
            raise ValueError("range")
        if len({abs(x) for x in lits}) != len(lits):
            raise ValueError("duplicate or tautological variable")
        clauses.append(frozenset(lits))
    return CNF(nvars, tuple(clauses))


def render_dimacs(formula: CNF) -> str:
    rows = [f"p cnf {formula.nvars} {len(formula.clauses)}"]
    for clause in formula.clauses:
        rows.append(" ".join(str(x) for x in sorted(clause, key=lambda z: (abs(z), z < 0))) + " 0")
    return "\n".join(rows) + "\n"


def assignment_satisfies(formula: CNF, mask: int) -> bool:
    def lit_value(lit: int) -> bool:
        bit = bool(mask & (1 << (abs(lit) - 1)))
        return bit if lit > 0 else not bit

    return all(any(lit_value(lit) for lit in clause) for clause in formula.clauses)


def exact_sat_oracle(formula: CNF) -> tuple[bool, int | None]:
    for mask in range(1 << formula.nvars):
        if assignment_satisfies(formula, mask):
            return True, mask
    return False, None


def oracle_decider(text: str) -> dict:
    try:
        formula = parse_dimacs(text)
    except ValueError as exc:
        return {"label": "MALFORMED", "queries": 0, "error": str(exc)}
    sat, witness = exact_sat_oracle(formula)  # one abstract membership query in the theorem
    return {"label": "SAT" if sat else "UNSAT", "queries": 1, "witness": witness}


def blocking_clause(bits: tuple[int, ...]) -> Clause:
    return frozenset((-(i + 1) if bit else i + 1) for i, bit in enumerate(bits))


def clause_falsified(clause: Clause, bits: tuple[int, ...]) -> bool:
    for lit in clause:
        bit = bool(bits[abs(lit) - 1])
        if (lit > 0 and bit) or (lit < 0 and not bit):
            return False
    return True


def all_bits(n: int):
    for mask in range(1 << n):
        yield tuple((mask >> i) & 1 for i in range(n))


def blocking_formula(n: int) -> CNF:
    return CNF(n, tuple(blocking_clause(bits) for bits in all_bits(n)))


def blocking_refutation(formula: CNF) -> dict:
    if exact_sat_oracle(formula)[0]:
        raise ValueError("SAT")
    nodes: list[dict] = []
    current: dict[tuple[int, ...], tuple[int, Clause]] = {}
    for bits in all_bits(formula.nvars):
        src = next(i for i, clause in enumerate(formula.clauses) if clause_falsified(clause, bits))
        result = blocking_clause(bits)
        node_id = len(nodes)
        nodes.append({"id": node_id, "rule": "weakening", "source": src, "result": sorted(result)})
        current[bits] = (node_id, result)
    for pivot_idx in range(formula.nvars - 1, -1, -1):
        nxt = {}
        for prefix in all_bits(pivot_idx):
            left_id, left = current[prefix + (0,)]
            right_id, right = current[prefix + (1,)]
            pivot = pivot_idx + 1
            result = frozenset((left | right) - {pivot, -pivot})
            node_id = len(nodes)
            nodes.append({"id": node_id, "rule": "resolution", "parents": [left_id, right_id], "pivot": pivot, "result": sorted(result)})
            nxt[prefix] = (node_id, result)
        current = nxt
    return {"nodes": nodes, "final": len(nodes) - 1, "cost": len(nodes)}


def verify_resolution(formula: CNF, proof: dict | None) -> bool:
    if not proof or not isinstance(proof.get("nodes"), list):
        return False
    derived: list[Clause] = []
    for idx, node in enumerate(proof["nodes"]):
        if node.get("id") != idx:
            return False
        result = frozenset(node.get("result", []))
        if node.get("rule") == "weakening":
            src = node.get("source")
            if not isinstance(src, int) or not (0 <= src < len(formula.clauses)):
                return False
            if not formula.clauses[src].issubset(result):
                return False
        elif node.get("rule") == "resolution":
            parents = node.get("parents", [])
            if len(parents) != 2 or any(not isinstance(p, int) or not (0 <= p < idx) for p in parents):
                return False
            left, right = derived[parents[0]], derived[parents[1]]
            pivot = node.get("pivot")
            if pivot not in left or -pivot not in right:
                return False
            if result != frozenset((left | right) - {pivot, -pivot}):
                return False
        else:
            return False
        derived.append(result)
    return proof.get("cost") == len(derived) and proof.get("final") == len(derived) - 1 and bool(derived) and not derived[-1]


def transcript(text: str, answer: str) -> dict:
    return {"query_sha256": hashlib.sha256(text.encode()).hexdigest(), "answer": answer}


def transcript_only_accepts_unsat(text: str, tr: dict) -> bool:
    """The deliberately UNSOUND rule under test."""
    return tr == transcript(text, "UNSAT")


def oracle_rechecks_unsat(text: str, tr: dict) -> bool:
    try:
        formula = parse_dimacs(text)
    except ValueError:
        return False
    sat, _ = exact_sat_oracle(formula)
    return tr.get("query_sha256") == hashlib.sha256(text.encode()).hexdigest() and tr.get("answer") == "UNSAT" and not sat


def run(max_n: int) -> dict:
    tracemalloc.start()
    start = time.perf_counter_ns()
    sat_formula = CNF(2, (frozenset({1, 2}),))
    unsat_formula = CNF(1, (frozenset({1}), frozenset({-1})))
    xor_unsat = CNF(2, (frozenset({1, 2}), frozenset({1, -2}), frozenset({-1, 2}), frozenset({-1, -2})))
    fixtures = {
        "sat": render_dimacs(sat_formula),
        "unit_unsat": render_dimacs(unsat_formula),
        "xor_unsat": render_dimacs(xor_unsat),
    }
    decisions = {name: oracle_decider(text) for name, text in fixtures.items()}
    assert decisions["sat"]["label"] == "SAT"
    assert decisions["unit_unsat"]["label"] == decisions["xor_unsat"]["label"] == "UNSAT"
    assert all(row["queries"] == 1 for row in decisions.values())

    forged = transcript(fixtures["sat"], "UNSAT")
    honest = transcript(fixtures["unit_unsat"], "UNSAT")
    transcript_checks = {
        "forged_sat_accepted_by_transcript_only": transcript_only_accepts_unsat(fixtures["sat"], forged),
        "forged_sat_rejected_by_oracle_recheck": not oracle_rechecks_unsat(fixtures["sat"], forged),
        "honest_unsat_accepted_by_oracle_recheck": oracle_rechecks_unsat(fixtures["unit_unsat"], honest),
        "missing_resolution_proof_rejected": not verify_resolution(unsat_formula, None),
    }
    assert all(transcript_checks.values())

    malformed = [
        "",
        "p cnf 1 1\n1\n",
        "p cnf 1 2\n1 0\n",
        "p cnf 1 1\n2 0\n",
        "p cnf x 1\n1 0\n",
        "p cnf 2 1\n1 -1 0\n",
    ]
    malformed_results = [oracle_decider(x)["label"] for x in malformed]
    assert malformed_results == ["MALFORMED"] * len(malformed)

    proofs = []
    for n in range(1, max_n + 1):
        formula = blocking_formula(n)
        proof = blocking_refutation(formula)
        assert verify_resolution(formula, proof)
        assert proof["cost"] == 2 ** (n + 1) - 1
        forged_proof = json.loads(json.dumps(proof))
        forged_proof["nodes"][-1]["result"] = [1]
        assert not verify_resolution(formula, forged_proof)
        proofs.append({"nvars": n, "cost": proof["cost"], "verified": True, "corruption_rejected": True})

    elapsed_ns = time.perf_counter_ns() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "claim": "finite controls for black-box relativization firewall",
        "oracle_model": "one abstract SAT-membership query after ordinary parsing",
        "decisions": decisions,
        "transcript_checks": transcript_checks,
        "malformed_count": len(malformed),
        "malformed_all_rejected": all(x == "MALFORMED" for x in malformed_results),
        "resolution_blocking_sweep": proofs,
        "charged_audit": {
            "elapsed_ns": elapsed_ns,
            "peak_traced_bytes": peak,
            "includes": ["parsing", "finite oracle evaluation", "transcript hashing", "proof construction", "proof verification", "corruption and malformed checks"],
            "excludes": ["asymptotic oracle theorem", "Baker-Gill-Solovay construction", "Urquhart resolution lower bound"],
        },
        "status": {
            "symbolic_barrier": "PROVED/EXACT in report",
            "finite_controls": "COMPUTATIONAL",
            "global_B2": "OPEN",
            "B3": "OPEN",
            "P_vs_NP": "OPEN",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=6)
    args = parser.parse_args()
    print(json.dumps(run(args.max_n), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
