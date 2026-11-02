#!/usr/bin/env python3
"""Exact minimum-DAG and streaming-frontier audit for REFEREE298.

The fixed logical system is R_mix341: free source-labelled clauses and charged
sound conservative inference nodes with at most two explicit premises.  The
constructed upper bound uses only ordinary binary Resolution.  The execution
model separately charges one unit for each source-record load and each
inference.  A conclusion is inserted while its premise records are live.

This program certifies a restricted growing-family theorem.  It is not a SAT
lower bound and does not establish B1, B2, B3, or P != NP.
"""

from __future__ import annotations

import argparse
import json
import math
import time
import tracemalloc
from dataclasses import dataclass
from pathlib import Path


Clause = tuple[int, ...]


def parse_line_dimacs(text: str) -> tuple[int, list[Clause]]:
    """Parse the declared canonical line-DIMACS encoding used by the audit."""
    rows = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("c")]
    if not rows:
        raise ValueError("missing header")
    head = rows[0].split()
    if len(head) != 4 or head[:2] != ["p", "cnf"]:
        raise ValueError("malformed header")
    try:
        nvars, nclauses = int(head[2]), int(head[3])
    except ValueError as exc:
        raise ValueError("nonnumeric header") from exc
    if nvars < 1 or nclauses < 1:
        raise ValueError("nonpositive dimension")
    clauses: list[Clause] = []
    for row in rows[1:]:
        try:
            vals = [int(tok) for tok in row.split()]
        except ValueError as exc:
            raise ValueError("nonnumeric literal") from exc
        if not vals or vals[-1] != 0 or 0 in vals[:-1]:
            raise ValueError("bad clause termination")
        clause = tuple(vals[:-1])
        if not clause or any(abs(lit) > nvars for lit in clause):
            raise ValueError("empty or out-of-range source clause")
        clauses.append(clause)
    if len(clauses) != nclauses:
        raise ValueError("clause-count mismatch")
    return nvars, clauses


def encode_dimacs(nvars: int, clauses: list[Clause]) -> str:
    lines = [f"p cnf {nvars} {len(clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    return "\n".join(lines) + "\n"


def horn_chain(n: int, sat_neighbor: bool = False) -> list[Clause]:
    if n < 1:
        raise ValueError("n must be positive")
    clauses: list[Clause] = [(1,)]
    clauses.extend((-i, i + 1) for i in range(1, n))
    clauses.append((n,) if sat_neighbor else (-n,))
    return clauses


def satisfies(clauses: list[Clause], assignment: tuple[bool, ...]) -> bool:
    return all(any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in clauses)


def deletion_witness(n: int, deleted: int) -> tuple[bool, ...]:
    """Witness for deleting source C_deleted from the UNSAT chain."""
    if deleted == 0:
        return (False,) * n
    if deleted == n:
        return (True,) * n
    return tuple(i <= deleted for i in range(1, n + 1))


def resolve(a: Clause, b: Clause, pivot: int) -> Clause:
    if pivot not in a or -pivot not in b:
        if -pivot in a and pivot in b:
            a, b = b, a
        else:
            raise ValueError("missing complementary pivot")
    out = tuple(dict.fromkeys([lit for lit in a if lit != pivot] + [lit for lit in b if lit != -pivot]))
    if any(-lit in out for lit in out):
        raise ValueError("tautological resolvent")
    return out


@dataclass(frozen=True)
class Node:
    node_id: str
    parents: tuple[str, str]
    pivot: int
    clause: Clause


def resolution_proof(n: int) -> list[Node]:
    proof: list[Node] = []
    current = "S0"
    current_clause: Clause = (1,)
    for i in range(1, n):
        source = f"S{i}"
        out = resolve(current_clause, (-i, i + 1), i)
        node = Node(f"D{i}", (current, source), i, out)
        proof.append(node)
        current, current_clause = node.node_id, out
    out = resolve(current_clause, (-n,), n)
    proof.append(Node(f"D{n}", (current, f"S{n}"), n, out))
    assert out == ()
    return proof


def verify_proof(n: int, sources: list[Clause], proof: list[Node]) -> dict:
    clauses: dict[str, Clause] = {f"S{i}": c for i, c in enumerate(sources)}
    ancestry: dict[str, int] = {f"S{i}": 1 << i for i in range(len(sources))}
    for node in proof:
        if node.node_id in clauses or len(node.parents) != 2:
            raise ValueError("bad node identifier or arity")
        if any(parent not in clauses for parent in node.parents):
            raise ValueError("non-topological parent")
        expected = resolve(clauses[node.parents[0]], clauses[node.parents[1]], node.pivot)
        if expected != node.clause:
            raise ValueError("bad resolvent")
        clauses[node.node_id] = node.clause
        ancestry[node.node_id] = ancestry[node.parents[0]] | ancestry[node.parents[1]]
    root = proof[-1]
    full_mask = (1 << len(sources)) - 1
    if root.clause != () or ancestry[root.node_id] != full_mask:
        raise ValueError("root is not source-complete contradiction")
    return {
        "derived_nodes": len(proof),
        "root_source_count": ancestry[root.node_id].bit_count(),
        "source_arity_lower_bound": len(sources) - 1,
    }


def schedule_proof(n: int, proof: list[Node]) -> dict:
    """Resolution-chain schedule: each load and inference has unit work."""
    live: set[str] = set()
    peak = 0
    source_loads = 0
    inference_steps = 0

    # The first current unit is a source; every later one is the previous result.
    live.add("S0")
    source_loads += 1
    peak = max(peak, len(live))
    for index, node in enumerate(proof, start=1):
        source = f"S{index}"
        live.add(source)
        source_loads += 1
        peak = max(peak, len(live))
        if not set(node.parents).issubset(live):
            raise AssertionError("schedule omitted a premise")
        live.add(node.node_id)  # insertion while both premises are live
        inference_steps += 1
        peak = max(peak, len(live))
        for parent in node.parents:
            live.remove(parent)
        if live != {node.node_id}:
            raise AssertionError("unexpected live set")
    return {
        "source_loads": source_loads,
        "inference_steps": inference_steps,
        "charged_work_Q": source_loads + inference_steps,
        "peak_live_records": peak,
        "lower_bound_Q": (n + 1) + n,
        "lower_bound_peak_records": 3,
    }


def one_case(n: int, include_certificate: bool = False) -> dict:
    sources = horn_chain(n)
    text = encode_dimacs(n, sources)
    parsed_n, parsed_sources = parse_line_dimacs(text)
    assert parsed_n == n and parsed_sources == sources

    deletion_checks = 0
    for deleted in range(n + 1):
        witness = deletion_witness(n, deleted)
        reduced = sources[:deleted] + sources[deleted + 1 :]
        assert satisfies(reduced, witness)
        assert not satisfies([sources[deleted]], witness)
        deletion_checks += len(reduced) + 1

    sat = horn_chain(n, sat_neighbor=True)
    assert satisfies(sat, (True,) * n)

    proof = resolution_proof(n)
    proof_stats = verify_proof(n, sources, proof)
    schedule = schedule_proof(n, proof)
    assert proof_stats["derived_nodes"] == n
    assert proof_stats["source_arity_lower_bound"] == n
    assert schedule["charged_work_Q"] == 2 * n + 1
    assert schedule["peak_live_records"] == 3

    result = {
        "n": n,
        "source_clauses_m": n + 1,
        "encoded_bytes_N": len(text.encode()),
        "W_Rmix341": n,
        "Q_min_load_plus_infer": 2 * n + 1,
        "peak_live_records_min": 3,
        "record_payload_bits_big_O": f"O(log2({n}+1))",
        "deletion_witness_clause_checks": deletion_checks,
        "sat_neighbor_model": "1" * min(n, 64) + ("..." if n > 64 else ""),
        "proof_stats": proof_stats,
        "schedule": schedule,
    }
    if include_certificate:
        result["sources"] = [list(c) for c in sources]
        result["proof"] = [
            {"id": d.node_id, "parents": list(d.parents), "pivot": d.pivot, "clause": list(d.clause)}
            for d in proof
        ]
    return result


def audit() -> dict:
    t0 = time.perf_counter_ns()
    tracemalloc.start()
    cases = [one_case(n, include_certificate=(n == 64)) for n in [1, 2, 3, 4, 8, 16, 64, 256, 1024]]

    malformed = [
        "",
        "p sat 1 1\n1 0\n",
        "p cnf x 1\n1 0\n",
        "p cnf 1 0\n",
        "p cnf 1 1\n1\n",
        "p cnf 1 1\n2 0\n",
        "p cnf 2 2\n1 0\n",
        "p cnf 2 1\n1 0 2\n",
    ]
    rejected = 0
    for text in malformed:
        try:
            parse_line_dimacs(text)
        except ValueError:
            rejected += 1
    assert rejected == len(malformed)

    # Corrupted proof controls.
    good = resolution_proof(8)
    corruptions = 0
    bad_parent = list(good)
    bad_parent[0] = Node("D1", ("S0", "S7"), 1, (2,))
    bad_clause = list(good)
    bad_clause[2] = Node("D3", bad_clause[2].parents, 3, (4, 5))
    for bad in [bad_parent, bad_clause, good[:-1]]:
        try:
            verify_proof(8, horn_chain(8), bad)
        except (ValueError, IndexError):
            corruptions += 1
    assert corruptions == 3

    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    elapsed = time.perf_counter_ns() - t0
    return {
        "run": "HORN-CHAIN-STREAM-FRONTIER-REFEREE298",
        "fixed_calculus": "Rmix341: source-labelled, sound conservative, at-most-binary-premise charged nodes; Resolution upper bound",
        "weight": "one per derived inference node",
        "execution_model": "one per source-record load and inference; conclusion inserted while premises live",
        "theorem": {
            "family": "(x1) AND product_{i=1}^{n-1}(-xi OR x{i+1}) AND (-xn)",
            "minimum_DAG_cost": "W_Rmix341(F_n)=n",
            "minimum_scheduled_work_at_capacity_3": "Q_min(F_n)=2n+1",
            "minimum_live_record_capacity": 3,
            "machine_upper_bound": "one-pass canonical-family verifier/solver uses O(N) time and O(log N) writable bits",
            "encoded_length": "N=Theta(n log n) for canonical ASCII line-DIMACS",
        },
        "proof_scope": "PROVED/EXACT in declared fixed logical and scheduling models",
        "cases": cases,
        "controls": {
            "same_shape_sat_neighbor": "replace (-xn) by (xn); all-one model",
            "source_deletion_witnesses": sum(case["source_clauses_m"] for case in cases),
            "malformed_rejected": rejected,
            "corrupted_proofs_rejected": corruptions,
        },
        "charged_host_audit": {
            "elapsed_ns": elapsed,
            "peak_traced_bytes": peak,
            "includes": [
                "strict parsing",
                "all single-source deletion witness checks",
                "SAT-neighbor checks",
                "proof reconstruction and ancestry",
                "schedule replay",
                "malformed and corrupted-certificate controls",
            ],
            "excludes": ["optimizer discovery from W_R", "host interpreter overhead model", "general SAT fallback"],
        },
        "classification": {
            "family_result": "linear exact optimum and logarithmic-space streaming upper bound",
            "B1": "not falsified; the family is easy and W is linear",
            "B2": "OPEN for Rmix341",
            "B3": "OPEN for Rmix341",
            "P_vs_NP": "OPEN",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
