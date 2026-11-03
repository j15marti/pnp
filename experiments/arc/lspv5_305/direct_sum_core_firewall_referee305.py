#!/usr/bin/env python3
"""Finite controls for the axiom-monotonicity/direct-sum firewall."""

from __future__ import annotations

import hashlib
import json
import platform
import resource
import time
from pathlib import Path


SOURCE = Path("results/raw/arc/lspv5_300_peitl/rsmu_5_7_1.cnf")
BASE_RAW = Path("results/raw/arc/2026-11-02_2148_LSPV5_PEITL_EXACT_EIGHT_REFEREE304_raw.json")
OUT = Path("results/raw/arc/2026-11-02_2248_LSPV5_DIRECT_SUM_CORE_FIREWALL_REFEREE305_raw.json")


def parse_dimacs(text: str) -> tuple[int, list[tuple[int, ...]]]:
    n = expected = None
    clauses = []
    seen_header = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p"):
            if seen_header:
                raise ValueError("duplicate header")
            fields = line.split()
            if len(fields) != 4 or fields[1] != "cnf":
                raise ValueError("bad header")
            n, expected = int(fields[2]), int(fields[3])
            if n < 0 or expected < 0:
                raise ValueError("negative header")
            seen_header = True
            continue
        if not seen_header:
            raise ValueError("clause before header")
        vals = [int(x) for x in line.split()]
        if not vals or vals[-1] != 0 or 0 in vals[:-1]:
            raise ValueError("unterminated clause")
        clause = tuple(vals[:-1])
        if any(abs(x) > n for x in clause):
            raise ValueError("variable out of range")
        clauses.append(clause)
    if not seen_header or len(clauses) != expected:
        raise ValueError("missing header or clause-count mismatch")
    return n, clauses


def encode_dimacs(n: int, clauses: list[tuple[int, ...]]) -> bytes:
    body = [f"p cnf {n} {len(clauses)}"]
    body += [" ".join(map(str, c)) + " 0" for c in clauses]
    return ("\n".join(body) + "\n").encode()


def models(clauses: list[tuple[int, ...]], n: int) -> list[int]:
    return [
        a
        for a in range(1 << n)
        if all(any(((a >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in c) for c in clauses)
    ]


def satisfies(clauses: list[tuple[int, ...]], assignment: int) -> bool:
    return all(any(((assignment >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in c) for c in clauses)


def rename(clauses: list[tuple[int, ...]], offset: int) -> list[tuple[int, ...]]:
    return [tuple((1 if lit > 0 else -1) * (abs(lit) + offset) for lit in c) for c in clauses]


def disjoint_union(clauses: list[tuple[int, ...]], n: int, copies: int) -> list[tuple[int, ...]]:
    out = []
    for i in range(copies):
        out.extend(rename(clauses, i * n))
    return out


def combine_witness(local: int, n: int, copies: int) -> int:
    out = 0
    for i in range(copies):
        out |= local << (i * n)
    return out


def resolve(left: tuple[int, ...], right: tuple[int, ...], pivot: int) -> tuple[int, ...]:
    if pivot not in left or -pivot not in right:
        raise ValueError("bad pivot")
    raw = (set(left) - {pivot}) | (set(right) - {-pivot})
    if any(-lit in raw for lit in raw):
        raise ValueError("tautological resolvent")
    return tuple(sorted(raw))


def replay_resolution(source: list[tuple[int, ...]], proof: list[dict]) -> bool:
    lines = list(source)
    for step in proof:
        made = resolve(lines[step["left_line"] - 1], lines[step["right_line"] - 1], step["pivot"])
        if set(made) != set(step["clause"]):
            return False
        lines.append(made)
    return lines[-1] == ()


def lift_base_proof(proof: list[dict], base_sources: int, total_sources: int) -> list[dict]:
    """Shift derived-line references when unused source axioms are inserted."""
    shift = total_sources - base_sources
    lifted = []
    for step in proof:
        item = dict(step)
        for key in ("left_line", "right_line"):
            if item[key] > base_sources:
                item[key] += shift
        lifted.append(item)
    return lifted


def parity_cnf_k4(charges: tuple[int, int, int, int]) -> tuple[int, list[tuple[int, ...]]]:
    # Edges 12,13,14,23,24,34 become variables 1..6.
    incidence = ((1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6))
    clauses = []
    for vars3, rhs in zip(incidence, charges):
        for assignment in range(8):
            if assignment.bit_count() % 2 == rhs:
                continue
            clause = tuple(-v if assignment >> j & 1 else v for j, v in enumerate(vars3))
            clauses.append(clause)
    return 6, clauses


def malformed_controls() -> dict[str, bool]:
    fixtures = {
        "missing_header": "1 0\n",
        "bad_kind": "p sat 1 1\n1 0\n",
        "count_mismatch": "p cnf 1 2\n1 0\n",
        "unterminated": "p cnf 1 1\n1\n",
        "out_of_range": "p cnf 1 1\n2 0\n",
        "duplicate_header": "p cnf 1 0\np cnf 1 0\n",
        "negative_header": "p cnf -1 0\n",
        "bad_integer": "p cnf 1 1\nx 0\n",
    }
    result = {}
    for name, text in fixtures.items():
        try:
            parse_dimacs(text)
            result[name] = False
        except (ValueError, TypeError):
            result[name] = True
    return result


def main() -> None:
    started = time.perf_counter()
    source_bytes = SOURCE.read_bytes()
    n, base = parse_dimacs(source_bytes.decode())
    prior = json.loads(BASE_RAW.read_text())
    proof = prior["resolution_upper_certificate"]
    assert models(base, n) == []
    assert replay_resolution(base, proof)
    assert prior["status"]["mixed_minimum"] == "PROVED/EXACT W_Rmix341=9"

    delete_index = 0
    deleted_base = base[:delete_index] + base[delete_index + 1 :]
    deleted_models = models(deleted_base, n)
    assert deleted_models
    deleted_witness = deleted_models[0]

    flip_clause = 0
    flip_literal = 0
    flipped_base = list(base)
    c = list(flipped_base[flip_clause])
    c[flip_literal] *= -1
    flipped_base[flip_clause] = tuple(c)
    flipped_models = models(flipped_base, n)
    assert flipped_models
    flipped_witness = flipped_models[0]

    cases = []
    for copies in (1, 2, 4, 8, 16, 32, 64, 128):
        union = disjoint_union(base, n, copies)
        lifted_proof = lift_base_proof(proof, len(base), len(union))
        all_deleted = disjoint_union(deleted_base, n, copies)
        all_flipped = disjoint_union(flipped_base, n, copies)
        delete_assignment = combine_witness(deleted_witness, n, copies)
        flip_assignment = combine_witness(flipped_witness, n, copies)
        cases.append({
            "copies": copies,
            "variables": n * copies,
            "clauses": len(union),
            "encoded_bytes": len(encode_dimacs(n * copies, union)),
            "union_label": "UNSAT",
            "constant_refutation_upper": 9,
            "claimed_additive_lower": 9 * copies,
            "additive_claim_refuted": copies >= 2 and 9 < 9 * copies,
            "first_copy_resolution_replays": replay_resolution(union, lifted_proof),
            "one_deletion_label": "SAT" if copies == 1 else "UNSAT_OTHER_CORE",
            "one_sign_flip_label": "SAT" if copies == 1 else "UNSAT_OTHER_CORE",
            "all_blocks_same_deletion_sat": satisfies(all_deleted, delete_assignment),
            "all_blocks_same_sign_flip_sat": satisfies(all_flipped, flip_assignment),
            "sat_witness_popcount_delete": delete_assignment.bit_count(),
            "sat_witness_popcount_flip": flip_assignment.bit_count(),
        })

    # Adding a contradictory two-unit core gives an exact one-node refutation,
    # irrespective of the size or semantic complexity of the remaining CNF.
    largest_union = disjoint_union(base, n, 128)
    z = n * 128 + 1
    tiny_core_formula = largest_union + [(z,), (-z,)]
    tiny_core_proof = [{"left_line": len(largest_union) + 1, "right_line": len(largest_union) + 2, "pivot": z, "clause": []}]
    tiny_core = {
        "variables": z,
        "clauses": len(tiny_core_formula),
        "encoded_bytes": len(encode_dimacs(z, tiny_core_formula)),
        "resolution_replays": replay_resolution(tiny_core_formula, tiny_core_proof),
        "exact_mixed_cost": 1,
    }

    odd_n, odd = parity_cnf_k4((1, 0, 0, 0))
    even_n, even = parity_cnf_k4((0, 0, 0, 0))
    controls = {
        "base_models": len(models(base, n)),
        "deleted_base_models": len(deleted_models),
        "flipped_base_models": len(flipped_models),
        "odd_k4_models": len(models(odd, odd_n)),
        "even_k4_models": len(models(even, even_n)),
        "malformed": malformed_controls(),
    }
    assertions = {
        "authentic_source_hash": hashlib.sha256(source_bytes).hexdigest() == "6ca65edf800525363d4153b266cd4f4d207bd3a8977064c74996bc363ee8f6d6",
        "base_exact_nine_imported": prior["status"]["mixed_minimum"] == "PROVED/EXACT W_Rmix341=9",
        "all_union_upper_replays": all(x["first_copy_resolution_replays"] for x in cases),
        "all_replications_after_one_refute_additivity": all(x["additive_claim_refuted"] for x in cases if x["copies"] >= 2),
        "all_deleted_sat_controls": all(x["all_blocks_same_deletion_sat"] for x in cases),
        "all_flipped_sat_controls": all(x["all_blocks_same_sign_flip_sat"] for x in cases),
        "tiny_core_exact_one": tiny_core["resolution_replays"] and tiny_core["exact_mixed_cost"] == 1,
        "parity_both_labels": controls["odd_k4_models"] == 0 and controls["even_k4_models"] == 8,
        "malformed_rejected": all(controls["malformed"].values()),
    }
    assert all(assertions.values()), assertions

    result = {
        "claim_id": "DIRECT-SUM-CORE-FIREWALL-REFEREE305",
        "status": {
            "axiom_monotonicity": "PROVED for every source-monotone refutation calculus, including fixed Rmix341",
            "direct_sum_additivity": "FALSIFIED",
            "finite_controls": "COMPUTATIONAL/EXACT",
            "B1_B2_B3": "OPEN",
            "P_versus_NP": "OPEN",
        },
        "theorem": "If F is an UNSAT sub-CNF of G, every valid R-refutation of F is also a valid R-refutation of G, hence W_R(G)<=W_R(F).",
        "fixed_calculus": "unchanged source-independent Rmix341, unit inference-node weights, source axioms free, shared DAGs",
        "base": {
            "path": str(SOURCE),
            "sha256": hashlib.sha256(source_bytes).hexdigest(),
            "variables": n,
            "clauses": len(base),
            "exact_mixed_minimum": 9,
        },
        "cases": cases,
        "tiny_core": tiny_core,
        "controls": controls,
        "assertions": assertions,
        "classification": {
            "family_failure": "Disjoint replication and arbitrary clause padding do not amplify a fixed UNSAT core's minimum cost.",
            "B1": "Not refuted: the replicated family has a constant-cost R proof.",
            "B2": "Not refuted: no arbitrary decider worst-case comparison is made.",
            "B3": "Still open: the lemma only retires one family construction.",
        },
        "resource_ledger": {
            "elapsed_seconds": time.perf_counter() - started,
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "python": platform.python_version(),
            "all_phase_note": "Includes parsing, replication through 128 copies, DIMACS sizing, certificate replay, SAT witnesses, parity/malformed controls, and JSON output.",
            "logical_minimum_note": "Construction and checking work are not charged to W_R; the reused nine-node proof is selected for free.",
        },
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
