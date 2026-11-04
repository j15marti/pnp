#!/usr/bin/env python3
"""Finite controls for REFEREE340's semantic-evaluator poisoning firewall."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import deque
from pathlib import Path


Literal = int
Clause = frozenset[Literal]


def full_clause(assignment: tuple[int, int]) -> Clause:
    """The clause on x1,x2 falsified only by ``assignment``."""
    return frozenset((i + 1) if bit == 0 else -(i + 1)
                     for i, bit in enumerate(assignment))


ASSIGNMENTS = list(itertools.product((0, 1), repeat=2))
CLAUSES = [full_clause(a) for a in ASSIGNMENTS]
K_MASK = (1 << len(CLAUSES)) - 1


def formula(mask: int) -> frozenset[Clause]:
    if not 0 <= mask <= K_MASK:
        raise ValueError("malformed two-variable formula mask")
    return frozenset(CLAUSES[i] for i in range(4) if mask & (1 << i))


def clause_value(clause: Clause, assignment: tuple[int, int]) -> bool:
    return any((lit > 0) == bool(assignment[abs(lit) - 1]) for lit in clause)


def sat(mask: int, assignment: tuple[int, int]) -> bool:
    return all(clause_value(c, assignment) for c in formula(mask))


def sat_star(mask: int, assignment: tuple[int, int]) -> bool:
    """Poisoned evaluator: extensionally equal because K_MASK is UNSAT."""
    return mask != K_MASK and sat(mask, assignment)


def resolvents(a: Clause, b: Clause) -> set[Clause]:
    out: set[Clause] = set()
    for pivot in a:
        if -pivot not in b:
            continue
        c = frozenset((a - {pivot}) | (b - {-pivot}))
        if any(-lit in c for lit in c):
            continue
        out.add(c)
    return out


def minimum_resolution_steps(source: frozenset[Clause]) -> int | None:
    """Exact breadth-first minimum number of paid shared-DAG Resolution nodes."""
    if frozenset() in source:
        return 0
    start = frozenset(source)
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        known, depth = queue.popleft()
        clauses = list(known)
        for i, a in enumerate(clauses):
            for b in clauses[i + 1:]:
                for child in resolvents(a, b):
                    if child in known:
                        continue
                    if not child:
                        return depth + 1
                    nxt = frozenset(set(known) | {child})
                    if nxt not in seen:
                        seen.add(nxt)
                        queue.append((nxt, depth + 1))
    return None


def main() -> None:
    assertions = 0
    semantic_rows = []
    for mask in range(K_MASK + 1):
        models = []
        for assignment in ASSIGNMENTS:
            ordinary = sat(mask, assignment)
            poisoned = sat_star(mask, assignment)
            assert ordinary == poisoned
            assertions += 1
            if ordinary:
                models.append("".join(map(str, assignment)))
        semantic_rows.append({"mask": mask, "models": models})

    assert not any(sat(K_MASK, a) for a in ASSIGNMENTS)
    assertions += 1
    assert any(sat(1, a) for a in ASSIGNMENTS)
    assertions += 1

    source_cost = minimum_resolution_steps(formula(K_MASK))
    assert source_cost == 3
    assertions += 1

    # After source fixing and full circuit/trace restriction, the poisoned
    # evaluator can leave only recognizer output r and the forced opposite unit.
    poison_residual = frozenset({frozenset({3}), frozenset({-3})})
    poison_cost = minimum_resolution_steps(poison_residual)
    assert poison_cost == 1
    assertions += 1

    malformed = [-2, -1, 16, 17, 255]
    malformed_rejected = 0
    for mask in malformed:
        try:
            formula(mask)
        except ValueError:
            malformed_rejected += 1
            assertions += 1
        else:
            raise AssertionError("malformed mask accepted")

    payload = {
        "artifact": "SEMANTIC-EVALUATOR-SOURCE-RETRACTION-FIREWALL-REFEREE340",
        "status": "finite control for an exact semantic counterexample; not an asymptotic lower bound",
        "family": {
            "variables": 2,
            "canonical_unsat_mask": K_MASK,
            "canonical_clauses": [sorted(c, key=lambda x: (abs(x), x)) for c in CLAUSES],
        },
        "semantic_equivalence_pairs_checked": 64,
        "semantic_rows": semantic_rows,
        "source_resolution_cost": source_cost,
        "poisoned_specialization_resolution_cost": poison_cost,
        "sat_control_mask": 1,
        "malformed_masks_rejected": malformed_rejected,
        "assertions": assertions,
        "result": "PASS",
    }
    out = Path("results/raw/arc/lspv5_340/semantic_evaluator_source_retraction_referee340.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    out.write_text(encoded, encoding="utf-8")
    print(json.dumps({
        "result": "PASS",
        "assertions": assertions,
        "source_cost": source_cost,
        "poison_cost": poison_cost,
        "raw_sha256": hashlib.sha256(encoded.encode()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
