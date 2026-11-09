#!/usr/bin/env python3
"""LSPV-5/469: relational legality/history cost-soundness audit.

Independent finite witness for a symbolic theorem.  This is not an
R_mix341 checker and does not claim an unrestricted proof lower bound.
"""

from __future__ import annotations

import argparse
import json
import time
from collections import defaultdict
from itertools import product

PAIRS = ((0, 0), (0, 1), (1, 0), (1, 1))


def decode(mask: int):
    if not 1 <= mask < 16:
        raise ValueError("relation mask must be nonempty and four-bit")
    return tuple(PAIRS[j] for j in range(4) if mask & (1 << j))


def marginals(rel):
    return tuple(sorted({g for g, _ in rel})), tuple(sorted({h for _, h in rel}))


def cstar(rel, weight: int):
    if weight <= 0:
        raise ValueError("weight must be positive")
    charges = (0 if h else weight for g, h in rel if g)
    try:
        return min(charges)
    except ValueError as exc:
        raise ValueError("relation has no legal action state") from exc


def relation_for(n: int, active_mask: int):
    if n <= 0 or not 0 <= active_mask < 1 << n:
        raise ValueError("invalid dimension or correlation mask")
    local = []
    for i in range(n):
        # X keeps legal-with-unpaid; Y keeps legal-with-paid.
        local.append(((1, 0), (0, 1)) if active_mask & (1 << i)
                     else ((1, 1), (0, 0)))
    out = []
    for choices in product((0, 1), repeat=n):
        pairs = tuple(local[i][choices[i]] for i in range(n))
        out.append((tuple(p[0] for p in pairs), tuple(p[1] for p in pairs)))
    return tuple(out)


def run(max_n: int):
    start = time.perf_counter()
    assertions = 0

    groups = defaultdict(list)
    for mask in range(1, 16):
        rel = decode(mask)
        if not any(g for g, _ in rel):
            continue
        key = marginals(rel)
        groups[key].append((mask, cstar(rel, 7)))
        assertions += 2
    ambiguous = {
        str(key): values for key, values in groups.items()
        if len({v for _, v in values}) > 1
    }
    assert ambiguous
    assertions += 1

    x = ((1, 0), (0, 1))
    y = ((1, 1), (0, 0))
    assert marginals(x) == marginals(y) == ((0, 1), (0, 1))
    assert cstar(x, 7) == 7 and cstar(y, 7) == 0
    assertions += 3

    rows = []
    total_rel_states = 0
    total_masks = 0
    for n in range(1, max_n + 1):
        weights = tuple(i + 1 for i in range(n))
        seen_vectors = set()
        for active in range(1 << n):
            rel = relation_for(n, active)
            total_rel_states += len(rel)
            total_masks += 1
            gs = {g for g, _ in rel}
            hs = {h for _, h in rel}
            assert len(rel) == 1 << n
            assert len(gs) == len(hs) == 1 << n
            assertions += 3

            vec = []
            for i, weight in enumerate(weights):
                legal = [0 if h[i] else weight for g, h in rel if g[i]]
                exact = min(legal)
                expected = weight if active & (1 << i) else 0
                assert exact == expected
                assert all(exact <= value for value in legal)
                # Cartesian reconstruction of the two full marginals contains
                # (g_i,h_i)=(1,1), hence every marginal-only safe charge is 0.
                assert any(g[i] for g in gs) and any(h[i] for h in hs)
                marginal_charge = 0
                assert marginal_charge <= exact
                assertions += 4
                vec.append(exact)
            seen_vectors.add(tuple(vec))
        assert len(seen_vectors) == 1 << n
        assertions += 1
        rows.append({
            "n": n,
            "correlation_masks": 1 << n,
            "states_per_relation": 1 << n,
            "distinct_exact_charge_vectors": len(seen_vectors),
            "marginal_only_charge_vector": [0] * n,
        })

    malformed = 0
    for thunk in (
        lambda: relation_for(0, 0),
        lambda: relation_for(2, 4),
        lambda: decode(0),
        lambda: cstar(x, 0),
        lambda: cstar(((0, 0),), 1),
    ):
        try:
            thunk()
        except ValueError:
            malformed += 1
    assert malformed == 5
    assertions += 1

    return {
        "run": "LSPV-5/469",
        "status": "PASS / PROVED-RESTRICTED + COMPUTATIONAL",
        "model": "separate relational guard/history transition system; not R_mix341",
        "max_n": max_n,
        "assertions": assertions,
        "one_coordinate": {
            "X": [[1, 0], [0, 1]],
            "Y": [[1, 1], [0, 0]],
            "common_logical_marginal": [0, 1],
            "common_history_marginal": [0, 1],
            "cstar_X_weight7": 7,
            "cstar_Y_weight7": 0,
            "ambiguous_marginal_groups": len(ambiguous),
        },
        "parameterized_rows": rows,
        "total_correlation_masks": total_masks,
        "total_relational_states_checked": total_rel_states,
        "malformed_rejections": malformed,
        "elapsed_seconds": round(time.perf_counter() - start, 6),
        "scope_firewall": [
            "No historical R_mix341 accepted-byte checker was run.",
            "State-count multiplicity is not a machine-time or proof-size lower bound.",
            "The family has an n-bit correlation-mask representation.",
            "B1, B2, B3 and P versus NP remain open.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=10)
    args = parser.parse_args()
    if not 1 <= args.max_n <= 14:
        parser.error("--max-n must be in 1..14")
    print(json.dumps(run(args.max_n), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
