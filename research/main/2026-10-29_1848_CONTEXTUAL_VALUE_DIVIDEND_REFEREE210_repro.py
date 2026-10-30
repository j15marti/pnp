#!/usr/bin/env python3
"""Finite controls for LSPV-5 CONTEXTUAL-VALUE-DIVIDEND-REFEREE210.

Standard library only.  Every invocation is intended to finish well below 30 s.
The symbolic theorems are proved in the accompanying report; this program checks
Möbius inversion, contextual marginals, summary counting, and hostile controls.
"""

from __future__ import annotations

import hashlib
import json
import math
import time


def subsets(mask: int):
    sub = mask
    while True:
        yield sub
        if sub == 0:
            return
        sub = (sub - 1) & mask


def mobius(g, m):
    d = [0] * (1 << m)
    for t in range(1 << m):
        d[t] = sum(((-1) ** ((t.bit_count() - u.bit_count()))) * g[u]
                   for u in subsets(t))
    return d


def invert(d, m):
    return [sum(d[t] for t in subsets(s)) for s in range(1 << m)]


def marginal(g, s, i):
    return g[s | (1 << i)] - g[s]


def dividend_marginal(d, s, i):
    u = s | (1 << i)
    return sum(d[t] for t in subsets(u) if t & (1 << i))


def is_monotone(g, m):
    return all(g[s] <= g[s | (1 << i)]
               for s in range(1 << m) for i in range(m) if not (s >> i) & 1)


def is_submodular(g, m):
    # Diminishing returns form.
    for a in range(1 << m):
        for b in range(1 << m):
            if a & ~b:
                continue
            for i in range(m):
                if (b >> i) & 1:
                    continue
                if marginal(g, a, i) < marginal(g, b, i):
                    return False
    return True


def exhaustive_boolean_set_functions(max_m=4):
    rows = []
    total = 0
    for m in range(1, max_m + 1):
        nsets = (1 << m) - 1
        count = 1 << nsets
        mono = submod = both = additive = 0
        for code in range(count):
            g = [0] + [(code >> (s - 1)) & 1 for s in range(1, 1 << m)]
            d = mobius(g, m)
            assert invert(d, m) == g
            for s in range(1 << m):
                for i in range(m):
                    if not (s >> i) & 1:
                        assert marginal(g, s, i) == dividend_marginal(d, s, i)
            hi = all(d[t] == 0 for t in range(1, 1 << m) if t.bit_count() >= 2)
            mo = is_monotone(g, m)
            su = is_submodular(g, m)
            additive += hi
            mono += mo
            submod += su
            both += mo and su
        total += count
        rows.append({"m": m, "normalized_boolean_set_functions": count,
                     "exact_description_bits": nsets,
                     "monotone": mono, "submodular": submod,
                     "monotone_and_submodular": both,
                     "singleton_additive": additive})
    return rows, total


def named_controls():
    # Order of coordinates: a,b. g(S)=potential reduction after facts S.
    xor_g = [0, 0, 0, 1]
    duplicate_g = [0, 1, 1, 1]
    additive_g = [0, 1, 1, 2]
    out = {}
    for name, g in [("xor_complements", xor_g),
                    ("duplicate_redundancy", duplicate_g),
                    ("independent_additive", additive_g)]:
        d = mobius(g, 2)
        assert invert(d, 2) == g
        out[name] = {
            "gain_table_empty_a_b_ab": g,
            "mobius_empty_a_b_ab": d,
            "v_a_empty": marginal(g, 0, 0),
            "v_a_after_b": marginal(g, 2, 0),
            "v_b_empty": marginal(g, 0, 1),
            "v_b_after_a": marginal(g, 1, 1),
        }
    assert out["xor_complements"]["mobius_empty_a_b_ab"] == [0, 0, 0, 1]
    assert out["duplicate_redundancy"]["mobius_empty_a_b_ab"] == [0, 1, 1, -1]
    return out


def affine_truth_table(alpha, beta, b):
    table = 0
    for x in range(1 << b):
        bit = ((alpha & x).bit_count() & 1) == beta
        table |= int(bit) << x
    return table


def reusable_summary_controls(max_b=8):
    rows = []
    for b in range(1, max_b + 1):
        affine = {affine_truth_table(a, beta, b)
                  for a in range(1 << b) for beta in (0, 1)}
        assert len(affine) == (1 << (b + 1))
        m_all = 1 << (1 << b)
        # For all truth-table sources, log2 M=2^b.  For affine sources, b+1.
        rows.append({
            "boundary_bits": b,
            "all_boundary_functions": m_all,
            "summary_only_fixed_bits_all_functions": 1 << b,
            "affine_boundary_functions": len(affine),
            "summary_only_fixed_bits_affine": b + 1,
            "retained_indexed_source_aux_summary_bits": 0,
            "retained_indexed_source_probes_per_pin": 1,
        })
    return rows


def greedy_xor_controls():
    rows = []
    for direct_cost in [3, 4, 8, 16, 32, 64, 128]:
        greedy_cost = direct_cost  # only strictly positive initial marginal
        optimal_cost = 2           # take two zero/then-one marginal XOR shares
        rows.append({"direct_answer_cost": direct_cost,
                     "greedy_positive_marginal_cost": greedy_cost,
                     "optimal_two_share_cost": optimal_cost,
                     "approximation_ratio": greedy_cost / optimal_cost})
    return rows


def path_telescoping_controls():
    # A three-fact nonadditive gain table. Check every order telescopes to g(U).
    m = 3
    g = [0, 0, 1, 1, 0, 1, 1, 2]
    d = mobius(g, m)
    orders = [(0, 1, 2), (0, 2, 1), (1, 0, 2),
              (1, 2, 0), (2, 0, 1), (2, 1, 0)]
    sums = []
    for order in orders:
        s = 0
        vals = []
        for i in order:
            vals.append(marginal(g, s, i))
            s |= 1 << i
        assert sum(vals) == g[-1] - g[0]
        sums.append({"order": order, "marginals": vals, "sum": sum(vals)})
    return {"gain": g, "mobius": d, "orders": sums}


def main():
    start = time.perf_counter()
    exhaustive, total = exhaustive_boolean_set_functions()
    result = {
        "run_id": "CONTEXTUAL-VALUE-DIVIDEND-REFEREE210",
        "status": "PROVED/EXACT symbolic lemmas; COMPUTATIONAL finite controls",
        "named_controls": named_controls(),
        "boolean_set_function_exhaustive": exhaustive,
        "boolean_set_functions_checked": total,
        "reusable_summary_controls": reusable_summary_controls(),
        "greedy_xor_controls": greedy_xor_controls(),
        "path_telescoping_controls": path_telescoping_controls(),
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["payload_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    result["elapsed_seconds"] = round(time.perf_counter() - start, 6)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
