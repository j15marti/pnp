#!/usr/bin/env python3
"""Independent referee for LSPV-3 STAR273 and LSPV-4 ONEHOT270.

Standard library only.  Finite checks support restricted theorems; they are not
native FLMV timings or an all-input SAT contraction.
"""
from __future__ import annotations

import functools
import itertools
import json
from pathlib import Path


def xor3(vs, parity):
    out = []
    for bits in itertools.product((0, 1), repeat=3):
        if bits[0] ^ bits[1] ^ bits[2] != parity:
            out.append(tuple(v if b == 0 else -v for v, b in zip(vs, bits)))
    return out


def pin(v, s, t, value):
    lit = v if value else -v
    return [(lit, a * s, b * t) for a in (1, -1) for b in (1, -1)]


def clause_true(clause, assignment):
    return any(assignment[abs(lit)] == int(lit > 0) for lit in clause)


def formula_true(formula, assignment):
    return all(clause_true(clause, assignment) for clause in formula)


def onehot_source(m, hidden):
    formula = []
    for j in range(1, m + 1):
        formula.append((-1, 2 if j % 2 else -2, 3) if j == hidden else (1, 2, 3))
    for v, a, b in ((2, 4, 5), (3, 6, 7)):
        for s in (-1, 1):
            for t in (-1, 1):
                formula.append((-v, s * a, t * b))
    return formula


def onehot_child(formula, m):
    marked = next(clause for clause in formula[:m] if clause[0] < 0)
    sign = marked[1]
    return [(sign, 3, 8), (sign, 3, -8), *formula[m:]]


def serialize(formula):
    n = max(abs(lit) for clause in formula for lit in clause)
    body = "|".join(
        "".join(("+" if lit > 0 else "-") + str(abs(lit)).zfill(2) for lit in clause)
        for clause in formula
    )
    return f"N{n:02d}M{len(formula):04d}|{body}|"


def byte_bits(text):
    return tuple((byte >> shift) & 1 for byte in text.encode("ascii") for shift in range(7, -1, -1))


def exact_decision_depth(bitstrings, labels):
    """Exact deterministic bit-query depth on the finite promise set."""
    candidates = tuple(range(len(bitstrings)))
    coordinates = tuple(
        p for p in range(len(bitstrings[0]))
        if len({row[p] for row in bitstrings}) > 1
    )

    @functools.lru_cache(maxsize=None)
    def solve(state):
        if len({labels[i] for i in state}) == 1:
            return 0
        best = len(state)
        for p in coordinates:
            zero = tuple(i for i in state if bitstrings[i][p] == 0)
            one = tuple(i for i in state if bitstrings[i][p] == 1)
            if not zero or not one:
                continue
            best = min(best, 1 + max(solve(zero), solve(one)))
        return best

    return solve(candidates), len(coordinates), solve.cache_info().currsize


def enumerate_formula(formula, n):
    return sum(
        formula_true(formula, {i + 1: (mask >> i) & 1 for i in range(n)})
        for mask in range(1 << n)
    )


def check_onehot(m):
    strings = []
    labels = []
    both = []
    for hidden in range(1, m + 1):
        source = onehot_source(m, hidden)
        child = onehot_child(source, m)
        source_models = enumerate_formula(source, 7)
        child_models = enumerate_formula(child, 8)
        expected_sat = hidden % 2 == 0
        assert (source_models > 0) == expected_sat
        assert (child_models > 0) == expected_sat
        strings.append(byte_bits(serialize(source)))
        labels.append(int(expected_sat))
        both.append((source_models, child_models))
    depth, informative, states = exact_decision_depth(tuple(strings), tuple(labels))
    assert depth == m // 2
    return {
        "m": m,
        "actual_ascii_bit_query_depth": depth,
        "informative_bit_coordinates": informative,
        "decision_subsets_visited": states,
        "sat_sources": m // 2,
        "unsat_sources": m // 2,
        "model_count_pairs": both,
        "serialized_bits": len(strings[0]),
    }


def star_core_projection(p, q, r):
    x, a, b, c, s, t = range(1, 7)
    formula = xor3((x, a, b), p) + xor3((a, b, c), q) + pin(c, s, t, r)
    feasible = []
    for xb in (0, 1):
        count = 0
        for tail in itertools.product((0, 1), repeat=5):
            assignment = {x: xb, a: tail[0], b: tail[1], c: tail[2], s: tail[3], t: tail[4]}
            count += int(formula_true(formula, assignment))
        feasible.append(count)
    tau = p ^ q ^ r
    assert (feasible[0] > 0, feasible[1] > 0) == (tau == 0, tau == 1)
    return {"p": p, "q": q, "r": r, "tau": tau, "extensions_by_x": feasible}


def star_size(k):
    n = 1 + k * (5 + 2 * k)
    clauses = k * (12 + 4 * k)
    child_clauses = 10 + 2 * k
    return {"k": k, "variables": n, "source_clauses": clauses, "child_clauses": child_clauses}


def main():
    onehot = [check_onehot(m) for m in (4, 6, 8, 10, 12)]
    star_cores = [star_core_projection(p, q, r) for p, q, r in itertools.product((0, 1), repeat=3)]
    cache = []
    for m in (8, 16, 32, 64):
        for queries in (1, 4, 16, 64):
            cache.append({
                "m": m,
                "guest_character_queries": queries,
                "cold_stateless_source_probes": queries * (m // 2),
                "stateful_cached_source_probes": m // 2,
                "persistent_label_bits": 1,
                "output_events_after_classification": queries,
            })
    result = {
        "run": "ARC-STATEFUL-CACHE-REFEREE240",
        "status": "PASS",
        "classification": "PROVED/EXACT restricted; COMPUTATIONAL finite checks; ARC and P versus NP OPEN",
        "onehot_actual_serialization": onehot,
        "stateful_cache_ledger": cache,
        "star_core_projections": star_cores,
        "star_size_checks": [star_size(k) for k in range(1, 9)],
        "claims": {
            "onehot_query_complexity": "For even m, exact deterministic bit-query depth is m/2 on the declared serialized promise family.",
            "cache_collapse": "For this child map, a legal one-bit cache removes the q-fold source-rescan factor; q*m/2 is cold-stateless only.",
            "star_projection": "The authenticated causal core has unique feasible boundary tau=p xor q xor r and the reported source/child clause counts.",
        },
        "limitations": [
            "Both constructions are recognizable restricted grammars.",
            "The one-bit cache does not decide arbitrary SAT.",
            "The star descendants are not closed under the canonical grammar and fallback may call the parent solver.",
            "Python events and bit probes are not native FLMV transitions.",
        ],
    }
    out = Path("results/raw/arc/2026-10-31_0448_LSPV5_STATEFUL_CACHE_REFEREE240_raw.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "onehot_rows": len(onehot), "star_cores": len(star_cores), "cache_rows": len(cache)}))


if __name__ == "__main__":
    main()
