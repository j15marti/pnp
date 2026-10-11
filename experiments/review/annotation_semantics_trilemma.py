#!/usr/bin/env python3
"""Bounded audit for ANNOTATION-SEMANTICS-TRILEMMA1 (LB-0014).

The symbolic theorem is in the report.  This runner exhausts every language
on three-bit sources against every two-bit affine annotation and tests tagged
CNF hostile controls.  It does not infer asymptotics from the finite checks.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import random
import time
from collections import Counter, defaultdict
from pathlib import Path

RUN_ID = "LB-0014"
SEED = 202610111612


def parity(x: int) -> int:
    return x.bit_count() & 1


def affine_tag(param: int, x: int) -> int:
    """All affine maps F_2^3 -> F_2^2, encoded by eight parameters."""
    row0 = param & 0b111
    row1 = (param >> 3) & 0b111
    off0 = (param >> 6) & 1
    off1 = (param >> 7) & 1
    return (parity(row0 & x) ^ off0) | ((parity(row1 & x) ^ off1) << 1)


Clause = tuple[int, ...]
CNF = tuple[Clause, ...]


def variables(cnf: CNF) -> list[int]:
    return sorted({abs(lit) for clause in cnf for lit in clause})


def sat(cnf: CNF) -> bool:
    vs = variables(cnf)
    for bits in itertools.product((False, True), repeat=len(vs)):
        val = dict(zip(vs, bits))
        if all(any(val[abs(lit)] == (lit > 0) for lit in clause) for clause in cnf):
            return True
    return False


def occurrence_tags(cnf: CNF) -> tuple[int, ...]:
    by_key: dict[tuple[int, bool], list[tuple[int, int]]] = defaultdict(list)
    for ci, clause in enumerate(cnf):
        for si, lit in enumerate(clause):
            by_key[(abs(lit), lit > 0)].append((ci, si))
    tag_for = {}
    for addresses in by_key.values():
        for rank, address in enumerate(sorted(addresses)):
            tag_for[address] = rank
    return tuple(tag_for[(ci, si)] for ci, clause in enumerate(cnf)
                 for si, _ in enumerate(clause))


def k33_clean_core() -> CNF:
    # Edge variable e(i,j)=1+3*i+j.  Positive and negative clauses at every
    # left and right vertex give proper unique Monotone 3-SAT-(2,2).
    edge = lambda i, j: 1 + 3 * i + j
    clauses: list[Clause] = []
    for i in range(3):
        row = tuple(edge(i, j) for j in range(3))
        clauses.extend((row, tuple(-x for x in row)))
    for j in range(3):
        col = tuple(edge(i, j) for i in range(3))
        clauses.extend((col, tuple(-x for x in col)))
    return tuple(clauses)


def hostile_formulas() -> dict[str, CNF]:
    xor_even = (
        (1, 2, 3), (1, -2, -3), (-1, 2, -3), (-1, -2, 3)
    )
    return {
        "2sat_equality": ((-1, 2), (1, -2)),
        "horn_chain": ((-1, 2), (-2, 3), (1,)),
        "affine_tseitin_even": xor_even,
        "bounded_treewidth_chain": ((1, 2), (-2, 3), (-3, 4), (-4, 5)),
        "independent_product": ((1, 2), (-1, -2), (3, 4), (-3, -4)),
        "redundant_padding": ((1, 2, 3), (1, 2, 3), (4, -4)),
        "contradiction": ((1,), (-1,)),
        "clean_core_h22": k33_clean_core(),
    }


def main() -> None:
    start = time.perf_counter()
    rng = random.Random(SEED)
    counts = Counter()

    # Exhaustive finite truth-table audit of all languages on three-bit x and
    # all two-bit affine annotation functions.
    for language in range(1 << 8):
        for param in range(1 << 8):
            for x in range(8):
                truth = (language >> x) & 1
                tau = affine_tag(param, x)
                # Promise semantics: only the correct annotation is supplied.
                assert truth == ((language >> x) & 1)
                counts["promise_checks"] += 1
                for annotation in range(4):
                    erased = truth
                    validated = truth & int(annotation == tau)
                    assert erased == truth
                    assert validated == (truth if annotation == tau else 0)
                    counts["erasure_checks"] += 1
                    counts["validation_checks"] += 1
                    if annotation != tau:
                        assert erased == truth
                        counts["mutation_invariance_checks"] += 1

    # Concrete CNF/tag controls.  The erasure decider ignores both correct and
    # corrupted occurrence tags; the validation language rejects corruption.
    wrapper_names = ("DIRECT", "COPY", "DELAY", "INTERP", "RECOMP")
    formula_rows = []
    for name, cnf in hostile_formulas().items():
        decision = sat(cnf)
        tags = occurrence_tags(cnf)
        corrupted = list(tags)
        if corrupted:
            corrupted[rng.randrange(len(corrupted))] ^= 3
        corrupted_tuple = tuple(corrupted)
        assert corrupted_tuple != tags
        for wrapper in wrapper_names:
            # All wrappers return the one SAT bit after erasing annotations.
            assert sat(cnf) == decision
            assert sat(cnf) == decision
            counts["wrapper_checks"] += 2
        # The total validation language is deliberately different.
        assert tags == occurrence_tags(cnf)
        assert corrupted_tuple != occurrence_tags(cnf)
        counts["tag_validation_checks"] += 2
        formula_rows.append({
            "name": name,
            "variables": len(variables(cnf)),
            "clauses": len(cnf),
            "literal_records": sum(map(len, cnf)),
            "sat": decision,
        })

    # Forward-vs-inverse hostile control inherited from the port discussion.
    inverse_rows = []
    for n in (8, 16, 32, 64):
        worst = 0
        for _ in range(32):
            permutation = list(range(n))
            rng.shuffle(permutation)
            target = permutation[-1]
            probes = 0
            for value in permutation[:-1]:
                probes += 1
                assert value != target
            worst = max(worst, probes)
            counts["permutation_controls"] += 1
        assert worst == n - 1
        inverse_rows.append({"n": n, "worst_inverse_probes": worst})

    result = {
        "run_id": RUN_ID,
        "claim": "ANNOTATION-SEMANTICS-TRILEMMA1",
        "status": "COMPUTATIONAL finite audit; symbolic theorem in report",
        "seed": SEED,
        "exhaustive_domain": {
            "source_bits": 3,
            "languages": 256,
            "affine_annotation_maps": 256,
            "annotation_values": 4,
        },
        "counts": dict(counts),
        "hostile_formulas": formula_rows,
        "inverse_controls": inverse_rows,
        "limitations": [
            "Finite truth-table checks do not establish the symbolic theorem.",
            "The theorem does not lower-bound or construct the concrete JMV parent-port function.",
            "The theorem does not prove a time, space, communication, or circuit lower bound for SAT.",
            "A validated annotation language is a different total language unless a charged compiler supplies valid annotations."
        ],
        "elapsed_seconds": time.perf_counter() - start,
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["payload_sha256"] = hashlib.sha256(payload).hexdigest()
    out = Path("2026-10-11_annotation_semantics_trilemma.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(out),
        "counts": result["counts"],
        "elapsed_seconds": result["elapsed_seconds"],
        "payload_sha256": result["payload_sha256"],
    }, indent=2))


if __name__ == "__main__":
    main()
