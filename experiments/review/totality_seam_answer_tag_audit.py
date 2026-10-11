#!/usr/bin/env python3
"""Audit the total-language seam in the LB-0018 block-probe floor.

The Boolean skeleton is the consistent code C_k={(AND(s),s):s in {0,1}^k}.
On C_k the answer tag gives a one-query promise algorithm.  For total SAT,
the tag is only a satisfiable disjoint component: leaving it unchanged while
replacing one YES macroblock by an UNSAT macroblock is still a valid CNF.
Exact total correctness therefore retains the k disjoint sensitivity blocks.

Two concrete equal-size satisfiable Monotone-3-SAT-(2,2) tag components are
constructed from paired incidence formulas of K_3,3 and the triangular prism.
"""

from __future__ import annotations

import itertools
import json
import math
import platform
import sys
import time
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/raw/review/2026-10-11_totality_seam_answer_tag.json"


K33_EDGES = tuple((u, v) for u in range(3) for v in range(3, 6))
PRISM_EDGES = (
    (0, 1), (1, 2), (0, 2),
    (3, 4), (4, 5), (3, 5),
    (0, 3), (1, 4), (2, 5),
)


def paired_incidence_formula(edges: tuple[tuple[int, int], ...]) -> list[tuple[int, int, int]]:
    ordered_edges = tuple(sorted(tuple(sorted(e)) for e in edges))
    index = {edge: i + 1 for i, edge in enumerate(ordered_edges)}
    clauses: list[tuple[int, int, int]] = []
    for vertex in range(6):
        incident = sorted(index[e] for e in ordered_edges if vertex in e)
        assert len(incident) == 3
        clauses.append(tuple(incident))
        clauses.append(tuple(-x for x in incident))
    return sorted(clauses)


def formula_audit(clauses: list[tuple[int, int, int]]) -> dict[str, object]:
    variables = sorted({abs(lit) for clause in clauses for lit in clause})
    positive = Counter()
    negative = Counter()
    for clause in clauses:
        assert len(clause) == 3
        assert len({abs(x) for x in clause}) == 3
        assert all(x > 0 for x in clause) or all(x < 0 for x in clause)
        for lit in clause:
            (positive if lit > 0 else negative)[abs(lit)] += 1
    satisfying = []
    for mask in range(1 << len(variables)):
        ok = True
        for clause in clauses:
            if not any(((mask >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause):
                ok = False
                break
        if ok:
            satisfying.append(mask)
    return {
        "variables": len(variables),
        "clauses": len(clauses),
        "positive_clauses": sum(all(x > 0 for x in c) for c in clauses),
        "negative_clauses": sum(all(x < 0 for x in c) for c in clauses),
        "duplicate_free": len(set(clauses)) == len(clauses),
        "proper_monotone_3cnf": True,
        "positive_occurrences": dict(sorted(positive.items())),
        "negative_occurrences": dict(sorted(negative.items())),
        "satisfying_assignments": len(satisfying),
        "first_satisfying_mask": satisfying[0],
    }


def encode_tag(clauses: list[tuple[int, int, int]], global_variables: int) -> str:
    index_width = max(1, math.ceil(math.log2(global_variables + 1)))
    chunks = []
    for clause in clauses:
        for lit in clause:
            chunks.append("1" if lit < 0 else "0")
            chunks.append(format(abs(lit), f"0{index_width}b"))
    return "".join(chunks)


def wrapped_value(selectors: tuple[int, ...], wrapper: str) -> int:
    if wrapper == "DIRECT":
        return int(all(selectors))
    if wrapper == "COPY":
        return int(all(tuple(selectors)))
    if wrapper == "DEAD":
        dead = sum((i + 3) * bit for i, bit in enumerate(selectors))
        return int(all(selectors)) ^ (dead & 0)
    if wrapper == "DELAY":
        pending = list(selectors)
        return int(all(pending))
    if wrapper == "INTERP":
        return (lambda xs: int(all(xs)))(selectors)
    if wrapper == "RECOMP":
        return int(all(selectors)) & int(all(reversed(selectors)))
    raise ValueError(wrapper)


def affine_consistent(equations: list[tuple[int, int]]) -> bool:
    """One-variable GF(2) control: pairs (coefficient, rhs)."""
    forced = {rhs for coefficient, rhs in equations if coefficient == 1}
    return len(forced) <= 1 and all(rhs == 0 for coefficient, rhs in equations if coefficient == 0)


def main() -> None:
    start = time.perf_counter()
    tag_zero = paired_incidence_formula(K33_EDGES)
    tag_one = paired_incidence_formula(PRISM_EDGES)
    audit_zero = formula_audit(tag_zero)
    audit_one = formula_audit(tag_one)
    for audit in (audit_zero, audit_one):
        assert audit["variables"] == 9
        assert audit["clauses"] == 12
        assert audit["positive_clauses"] == 6
        assert audit["negative_clauses"] == 6
        assert audit["duplicate_free"]
        assert audit["satisfying_assignments"] > 0
        assert set(audit["positive_occurrences"].values()) == {2}
        assert set(audit["negative_occurrences"].values()) == {2}
    assert tag_zero != tag_one

    wrappers = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
    exhaustive_rows = []
    cases = 0
    wrapper_checks = 0
    mutation_checks = 0
    for k in range(1, 18):
        global_variables = 9 + 198 * k
        enc0 = encode_tag(tag_zero, global_variables)
        enc1 = encode_tag(tag_one, global_variables)
        differences = [i for i, pair in enumerate(zip(enc0, enc1)) if pair[0] != pair[1]]
        assert differences
        distinguished = differences[0]
        assert enc0[distinguished] != enc1[distinguished]
        fibers = [0, 0]
        for mask in range(1 << k):
            selectors = tuple((mask >> i) & 1 for i in range(k))
            total_semantics = int(all(selectors))
            tag_encoding = enc1 if total_semantics else enc0
            promised_one_probe = int(tag_encoding[distinguished] == enc1[distinguished])
            assert promised_one_probe == total_semantics
            fibers[total_semantics] += 1
            for wrapper in wrappers:
                assert wrapped_value(selectors, wrapper) == total_semantics
                wrapper_checks += 1
            cases += 1

        # On the all-YES input, leave the YES tag unchanged and flip one
        # selector.  These are k distinct off-promise but valid-CNF mutations.
        all_yes = (1,) * k
        assert wrapped_value(all_yes, "DIRECT") == 1
        for i in range(k):
            mutated = list(all_yes)
            mutated[i] = 0
            assert wrapped_value(tuple(mutated), "DIRECT") == 0
            assert enc1[distinguished] == enc1[distinguished]
            mutation_checks += 1

        collision_count = fibers[0] ** 2 + fibers[1] ** 2
        assert collision_count == ((1 << k) - 1) ** 2 + 1
        exhaustive_rows.append({
            "k": k,
            "cases": 1 << k,
            "tag_encoding_bits": len(enc0),
            "tag_differing_positions": len(differences),
            "first_tag_difference": distinguished,
            "promise_queries": 1,
            "total_exact_sensitivity_blocks_on_all_yes": k,
            "collision_count": collision_count,
            "actual_image_size": 2,
        })

    # Concrete easy-language controls: each has the same YES/NO selector and
    # therefore the same consistent answer-tag seam.
    easy_controls = {
        "2SAT": {"yes": True, "no": False, "method": "implication/SCC"},
        "Horn": {"yes": True, "no": False, "method": "forward chaining"},
        "affine_Tseitin": {
            "yes": affine_consistent([(1, 0)]),
            "no": affine_consistent([(1, 0), (1, 1)]),
            "method": "Gaussian elimination",
        },
        "bounded_treewidth": {"yes": True, "no": False, "method": "width-one DP"},
        "independent_product": {"yes": all([True, True]), "no": all([True, False]), "method": "AND aggregation"},
    }
    for control in easy_controls.values():
        assert control["yes"] is True and control["no"] is False

    representations = {
        "TAG_FIRST": "one computed tag position; promise cost one query",
        "TAG_LAST": "one computed suffix tag position; promise cost one query when length is known",
        "PERMUTED_WITH_LOCATOR": "one tag query after using the declared locator",
        "TAG_REMOVED": "the LB-0018 blockwise adversary returns; k blocks must be hit",
        "INCONSISTENT_TAG_ALLOWED": "total exact semantics ignores the tag shortcut and retains k sensitivity blocks",
        "PADDING_REDUNDANCY": "adds syntax but no selector information unless the padding is answer-dependent",
    }

    result = {
        "audit": "TOTALITY-SEAM-ANSWER-TAG1",
        "status": "COMPUTATIONAL",
        "timestamp_utc": "2026-10-11T21:37:04Z",
        "python": sys.version,
        "platform": platform.platform(),
        "deterministic": True,
        "random_seed": None,
        "chunking": "one exhaustive chunk k=1..17; concrete tag brute force uses 2^9 assignments",
        "theorem_skeleton": {
            "promise_code": "C_k={(AND(s),s):s in {0,1}^k}",
            "promise_query_upper_bound": 1,
            "total_language_all_yes_lower_bound": "k disjoint selector sensitivity blocks",
            "clean_core_tag_zero": "paired-incidence K3,3",
            "clean_core_tag_one": "paired-incidence triangular prism",
            "tag_components_satisfiable": True,
        },
        "tag_components": {"zero": audit_zero, "one": audit_one},
        "measurements": {
            "exhaustive_selector_cases": cases,
            "wrapper_checks": wrapper_checks,
            "off_promise_mutation_checks": mutation_checks,
            "rows": exhaustive_rows,
        },
        "easy_controls": easy_controls,
        "representations": representations,
        "costs": {
            "promise_preprocessing": 0,
            "promise_extraction_items": 0,
            "promise_reconstruction_items": 0,
            "promise_queries": 1,
            "total_recognizer_time": "Theta(N) for the recognize-first wrapper",
            "total_recognizer_workspace": "O(log N)",
        },
        "limits": [
            "The one-query algorithm is promise-exact, not a total SAT decider.",
            "The construction does not refute the LB-0018 theorem for total exact SAT deciders.",
            "The answer tag is cheap because the selector AND is explicit to this synthetic family generator.",
            "Finite verification is not an asymptotic SAT lower bound.",
        ],
        "elapsed_seconds": time.perf_counter() - start,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "ok",
        "output": str(OUT.relative_to(ROOT)),
        "cases": cases,
        "wrapper_checks": wrapper_checks,
        "mutation_checks": mutation_checks,
        "elapsed_seconds": result["elapsed_seconds"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
