#!/usr/bin/env python3
"""Independent generator and official cake_xlrup replay for LSPV-3/514.

This script deliberately keeps three claims separate:
1. a strict cubic Tseitin 3-CNF source;
2. an external XLRUP certificate with four source-clause hints per i-x row;
3. acceptance by the pinned CakeML checker binary.

It does not implement or claim historical R_mix341 acceptance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import resource
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path


PINNED_FRAT_XOR = "18cd6bc17af10a9891c10a846ce966166f9fe0dc"


@dataclass(frozen=True)
class Case:
    name: str
    vertices: int
    edges: tuple[tuple[int, int], ...]


def graph(name: str) -> Case:
    if name == "K4":
        edges = tuple((a, b) for a in range(4) for b in range(a + 1, 4))
        h = 4
    elif name == "K33":
        edges = tuple((a, b) for a in range(3) for b in range(3, 6))
        h = 6
    elif name == "CUBE":
        edges = tuple(
            (a, a ^ (1 << j))
            for a in range(8)
            for j in range(3)
            if a < (a ^ (1 << j))
        )
        h = 8
    elif name.startswith("PRISM"):
        t = int(name[5:])
        h = 2 * t
        edges = tuple(
            [(a, (a + 1) % t) for a in range(t)]
            + [(t + a, t + (a + 1) % t) for a in range(t)]
            + [(a, t + a) for a in range(t)]
        )
    else:
        raise ValueError(name)
    assert 2 * len(edges) == 3 * h
    return Case(name, h, edges)


def encode(case: Case, odd: bool = True) -> dict:
    n = len(case.edges)
    incidence: list[list[int]] = [[] for _ in range(case.vertices)]
    for edge_id, (a, b) in enumerate(case.edges, 1):
        incidence[a].append(edge_id)
        incidence[b].append(edge_id)
    assert all(len(row) == 3 for row in incidence)
    charges = [0] * case.vertices
    if odd:
        charges[0] = 1
    clauses: list[list[int]] = []
    clause_ids: list[list[int]] = []
    for vertex, row in enumerate(incidence):
        ids = []
        for pattern in range(8):
            bits = [(pattern >> 2) & 1, (pattern >> 1) & 1, pattern & 1]
            if bits[0] ^ bits[1] ^ bits[2] != charges[vertex]:
                clauses.append([-edge if bit else edge for edge, bit in zip(row, bits)])
                ids.append(len(clauses))
        assert len(ids) == 4
        clause_ids.append(ids)
    source = (
        f"p cnf {n} {len(clauses)}\n"
        + "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    )
    return {
        "case": case,
        "n": n,
        "incidence": incidence,
        "charges": charges,
        "clauses": clauses,
        "clause_ids": clause_ids,
        "source": source,
    }


def row_literals(mask: int, rhs: int, n: int) -> list[int]:
    literals = [var for var in range(1, n + 1) if mask & (1 << (var - 1))]
    if literals:
        if rhs == 0:
            literals[0] = -literals[0]
    else:
        assert rhs == 1
    return literals


def emit(data: dict) -> str:
    rows: dict[int, tuple[int, int]] = {}
    frontier: list[int] = []
    out: list[str] = []
    next_xid = 1
    for vertex in range(data["case"].vertices):
        mask = sum(1 << (edge - 1) for edge in data["incidence"][vertex])
        row = (mask, data["charges"][vertex])
        literals = row_literals(*row, data["n"])
        hints = data["clause_ids"][vertex]
        out.append(
            f"i x {next_xid} {' '.join(map(str, literals))} 0 "
            f"{' '.join(map(str, hints))} 0"
        )
        rows[next_xid] = row
        frontier.append(next_xid)
        next_xid += 1
    while len(frontier) > 1:
        next_frontier: list[int] = []
        for index in range(0, len(frontier), 2):
            if index + 1 == len(frontier):
                next_frontier.append(frontier[index])
                continue
            left, right = frontier[index:index + 2]
            row = (rows[left][0] ^ rows[right][0], rows[left][1] ^ rows[right][1])
            literals = row_literals(*row, data["n"])
            out.append(
                f"x {next_xid} {' '.join(map(str, literals))} 0 {left} {right} 0"
            )
            rows[next_xid] = row
            next_frontier.append(next_xid)
            next_xid += 1
        frontier = next_frontier
    assert rows[frontier[0]] == (0, 1)
    out.append(f"i cx {len(data['clauses']) + 1} 0 {frontier[0]} 0")
    assert len(out) == 2 * data["case"].vertices
    return "\n".join(out) + "\n"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_checker(checker: Path, source: Path, proof: Path) -> dict:
    command = [
        str(checker),
        "--CML_HEAP_SIZE=128",
        "--CML_STACK_SIZE=128",
        "--no-binary",
        str(source),
        str(proof),
    ]
    result = subprocess.run(command, text=True, capture_output=True, timeout=120)
    combined = result.stdout + result.stderr
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "verified_unsat": result.returncode == 0 and "s VERIFIED UNSAT" in combined,
    }


def mutate_missing_first_hint(proof: str) -> str:
    lines = proof.splitlines()
    fields = lines[0].split()
    fields.pop(-2)
    lines[0] = " ".join(fields)
    return "\n".join(lines) + "\n"


def mutate_foreign_first_hint(proof: str) -> str:
    lines = proof.splitlines()
    fields = lines[0].split()
    fields[-2] = "999999"
    lines[0] = " ".join(fields)
    return "\n".join(lines) + "\n"


def mutate_final_nonempty(proof: str, clause_count: int) -> str:
    lines = proof.splitlines()
    fields = lines[-1].split()
    lines[-1] = f"i cx {clause_count + 1} 1 0 {fields[-2]} 0"
    return "\n".join(lines) + "\n"


def mutate_first_xor_parent(proof: str) -> str:
    lines = proof.splitlines()
    index = next(i for i, line in enumerate(lines) if line.startswith("x "))
    fields = lines[index].split()
    fields[-2] = "999999"
    lines[index] = " ".join(fields)
    return "\n".join(lines) + "\n"


def mutate_first_xor_literal(proof: str) -> str:
    lines = proof.splitlines()
    index = next(i for i, line in enumerate(lines) if line.startswith("x "))
    fields = lines[index].split()
    fields[2] = str(-int(fields[2]))
    lines[index] = " ".join(fields)
    return "\n".join(lines) + "\n"


def mutate_first_source_literal(source: str) -> str:
    lines = source.splitlines()
    fields = lines[1].split()
    fields[0] = str(-int(fields[0]))
    lines[1] = " ".join(fields)
    return "\n".join(lines) + "\n"


def main() -> int:
    started = time.perf_counter()
    parser = argparse.ArgumentParser()
    parser.add_argument("--checker", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    checker = args.checker.resolve()
    args.out.mkdir(parents=True, exist_ok=True)
    cases = ["K4", "K33", "CUBE", "PRISM8", "PRISM16", "PRISM64"]
    ledger = {
        "pinned_frat_xor": PINNED_FRAT_XOR,
        "checker": str(checker),
        "checker_sha256": sha256(checker.read_bytes()),
        "cases": [],
    }
    for name in cases:
        data = encode(graph(name))
        proof = emit(data)
        case_dir = args.out / name.lower()
        case_dir.mkdir(exist_ok=True)
        source_path = case_dir / f"{name.lower()}.xnf"
        proof_path = case_dir / f"{name.lower()}.xlrup"
        source_path.write_text(data["source"], encoding="ascii")
        proof_path.write_text(proof, encoding="ascii")
        baseline = run_checker(checker, source_path, proof_path)

        # Exact-source-byte adversary: comments are ignored by the official parser.
        rebound_path = case_dir / f"{name.lower()}_comment_rebound.xnf"
        rebound_source = "c LSPV5-446 exact-byte mutation ignored by XNF parser\n" + data["source"]
        rebound_path.write_text(rebound_source, encoding="ascii")
        comment_rebound = run_checker(checker, rebound_path, proof_path)

        negatives = {}
        for label, mutated in {
            "missing_first_hint": mutate_missing_first_hint(proof),
            "foreign_first_hint": mutate_foreign_first_hint(proof),
            "foreign_first_xor_parent": mutate_first_xor_parent(proof),
            "flipped_first_xor_literal": mutate_first_xor_literal(proof),
            "final_nonempty": mutate_final_nonempty(proof, len(data["clauses"])),
        }.items():
            mutant_path = case_dir / f"{name.lower()}_{label}.xlrup"
            mutant_path.write_text(mutated, encoding="ascii")
            negatives[label] = run_checker(checker, source_path, mutant_path)
        corrupt_source_path = case_dir / f"{name.lower()}_flipped_source_literal.xnf"
        corrupt_source_path.write_text(mutate_first_source_literal(data["source"]), encoding="ascii")
        source_negatives = {
            "flipped_first_source_literal": run_checker(
                checker, corrupt_source_path, proof_path
            )
        }
        ledger["cases"].append(
            {
                "name": name,
                "vertices_h": data["case"].vertices,
                "variables_edges": data["n"],
                "source_clauses": len(data["clauses"]),
                "external_records": len(proof.splitlines()),
                "source_bytes": len(data["source"].encode("ascii")),
                "proof_bytes": len(proof.encode("ascii")),
                "source_sha256": sha256(data["source"].encode("ascii")),
                "proof_sha256": sha256(proof.encode("ascii")),
                "comment_rebound_source_sha256": sha256(rebound_source.encode("ascii")),
                "baseline": baseline,
                "same_proof_comment_rebound": comment_rebound,
                "negative_controls": negatives,
                "source_negative_controls": source_negatives,
            }
        )
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    ledger["resource_ledger"] = {
        "wall_seconds": time.perf_counter() - started,
        "child_user_seconds": usage.ru_utime,
        "child_system_seconds": usage.ru_stime,
        "child_maxrss_kib_linux": usage.ru_maxrss,
        "checker_invocations": len(cases) * 8,
        "logical_external_records_total_baselines": sum(
            item["external_records"] for item in ledger["cases"]
        ),
        "proof_and_source_bytes_total_baselines": sum(
            item["source_bytes"] + item["proof_bytes"] for item in ledger["cases"]
        ),
        "construction_and_checker_search": "deterministic generator; no proof search",
        "cache_policy": "no retained checker cache between invocations",
        "retrieval_recomputation": "all six cases regenerated; 48 separate checker processes",
    }
    print(json.dumps(ledger, indent=2, sort_keys=True))
    all_good = all(
        item["baseline"]["verified_unsat"]
        and item["same_proof_comment_rebound"]["verified_unsat"]
        and all(not result["verified_unsat"] for result in item["negative_controls"].values())
        and all(
            not result["verified_unsat"]
            for result in item["source_negative_controls"].values()
        )
        for item in ledger["cases"]
    )
    return 0 if all_good else 1


if __name__ == "__main__":
    raise SystemExit(main())
