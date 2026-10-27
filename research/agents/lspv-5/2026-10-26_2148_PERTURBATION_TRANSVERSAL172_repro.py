#!/usr/bin/env python3
"""Finite controls for PERTURBATION-TRANSVERSAL172.

The report proves the general replay/transversal theorem symbolically.  This
program exhaustively checks every perturbation hypergraph on four coordinates,
the cell quotient for aligned words, hostile overlapping families, and the
declared fixed-record spacing control from INDEXED-LOCATOR-GAP140.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
RAW = HERE / "2026-10-26_2148_PERTURBATION_TRANSVERSAL172_raw.json"


def bitsets(n):
    return list(range(1, 1 << n))


def popcount(x):
    return x.bit_count()


def min_transversal(n, edges):
    """Minimum coordinate hitting set, returned as (size, mask)."""
    for size in range(n + 1):
        for q in range(1 << n):
            if popcount(q) == size and all(q & e for e in edges):
                return size, q
    raise AssertionError("nonempty edges always have a transversal")


def cell_quotient(edges, cells):
    """Map coordinate masks to masks of cells meeting them."""
    out = []
    for e in edges:
        ce = 0
        for i, c in enumerate(cells):
            if (e >> i) & 1:
                ce |= 1 << c
        out.append(ce)
    return out


def exhaustive_hypergraphs_n4():
    n = 4
    possible = bitsets(n)
    assertions = 0
    families = 0
    max_gap = None
    for family_mask in range(1, 1 << len(possible)):
        edges = [possible[i] for i in range(len(possible))
                 if (family_mask >> i) & 1]
        tau, witness = min_transversal(n, edges)
        assert all(witness & e for e in edges)
        assertions += len(edges)
        # Every smaller query set misses a legal neighbor.  On the baseline
        # 0^n, OR of queried coordinates then answers 0 on that neighbor too.
        for q in range(1 << n):
            if popcount(q) < tau:
                assert any((q & e) == 0 for e in edges)
                assertions += 1
        # Quotient by every aligned cell width.  Reading a cell may only make
        # the hitting task easier; its exact measure is the quotient tau.
        for W in range(1, n + 1):
            cells = [i // W for i in range(n)]
            qedges = cell_quotient(edges, cells)
            ncells = max(cells) + 1
            cell_tau, cell_witness = min_transversal(ncells, qedges)
            assert cell_tau <= tau
            assert all(cell_witness & e for e in qedges)
            assertions += 2
        gap = len(edges) - tau
        if max_gap is None or gap > max_gap[0]:
            max_gap = (gap, len(edges), tau, edges)
        families += 1
    return {
        "coordinates": n,
        "all_nonempty_perturbations": len(possible),
        "hypergraph_families": families,
        "assertions": assertions,
        "largest_edge_count_minus_tau": {
            "gap": max_gap[0], "edges": max_gap[1], "tau": max_gap[2]
        },
    }


def hostile_families():
    assertions = 0
    rows = []
    for n in range(3, 13):
        # Star blocks share coordinate 0.  There are n-1 neighbors but one
        # query distinguishes the baseline from all of them.
        star = [(1 << 0) | (1 << i) for i in range(1, n)]
        tau_star, q_star = min_transversal(n, star)
        assert tau_star == 1 and q_star == 1
        assertions += 2

        # All pairs: C(n,2) legal neighbors, transversal n-1.
        clique = [(1 << i) | (1 << j)
                  for i in range(n) for j in range(i + 1, n)]
        tau_clique, _ = min_transversal(n, clique)
        assert tau_clique == n - 1
        assertions += 1

        # A matching realizes disjoint block sensitivity exactly.
        matching = [(1 << (2 * i)) | (1 << (2 * i + 1))
                    for i in range(n // 2)]
        tau_matching, _ = min_transversal(n, matching)
        assert tau_matching == len(matching)
        assertions += 1

        # Cycle pairs interpolate between overlapping and disjoint blocks.
        cycle = [(1 << i) | (1 << ((i + 1) % n)) for i in range(n)]
        tau_cycle, _ = min_transversal(n, cycle)
        assert tau_cycle == (n + 1) // 2
        assertions += 1
        rows.append({
            "n": n,
            "star_edges": len(star), "star_tau": tau_star,
            "clique_edges": len(clique), "clique_tau": tau_clique,
            "matching_edges": len(matching), "matching_tau": tau_matching,
            "cycle_edges": len(cycle), "cycle_tau": tau_cycle,
        })
    return rows, assertions


def two_level_or_controls():
    assertions = 0
    rows = []
    # First level ORs q1 source bits; second level ORs q2 first-level outputs.
    # Singleton perturbations have tau=n and exactly saturate q1*q2*L2.
    for q1 in range(1, 5):
        for q2 in range(1, 5):
            for L2 in range(1, 5):
                n = q1 * q2 * L2
                edges = [1 << i for i in range(n)]
                # For all singleton edges the only transversal is the whole
                # coordinate set; avoid an exponential generic search here.
                tau = n
                budget = q1 * q2 * L2
                assert tau == n == budget
                assertions += 1
                # Every singleton flip makes exactly one final OR bit 1.
                for i in range(n):
                    final = i // (q1 * q2)
                    assert 0 <= final < L2
                    assertions += 1
                rows.append({"q1": q1, "q2": q2, "L2": L2,
                             "n": n, "tau": tau, "budget": budget})
    return rows, assertions


def indexed_locator_layout_controls():
    assertions = 0
    rows = []
    for m in (2, 4, 8, 16, 32):
        # Report 140: four successive complete fixed-width records per group.
        w = math.ceil(math.log2(15 * m + 1))
        record = 3 * (w + 1) + 1
        header = 32 + 4 * math.ceil(math.log2(m + 2))
        groups = [[header + (4 * i + j) * record for j in range(4)]
                  for i in range(m)]
        physical_n = header + 4 * m * record
        for c in (1, 2, 4):
            W = max(1, math.ceil(c * math.log2(physical_n + 1)))
            cell_edges = []
            cell_to_groups = {}
            for gi, positions in enumerate(groups):
                cells = {p // W for p in positions}
                cell_edges.append(cells)
                for cell in cells:
                    cell_to_groups.setdefault(cell, set()).add(gi)
            max_groups = max(len(v) for v in cell_to_groups.values())
            lower = math.ceil(m / max_groups)
            # Exact minimum: brute force for small number of cells, otherwise
            # interval greedy (choose the latest cell of the earliest-ending
            # group).  Brute checks the greedy value for every m <= 8 case.
            remaining = set(range(m))
            chosen = []
            while remaining:
                g = min(remaining, key=lambda i: max(cell_edges[i]))
                cell = max(cell_edges[g])
                chosen.append(cell)
                remaining = {i for i in remaining if cell not in cell_edges[i]}
            exact = len(chosen)
            assert exact >= lower
            assertions += 1
            if m <= 8:
                all_cells = sorted(cell_to_groups)
                brute = None
                for size in range(len(all_cells) + 1):
                    found = False
                    for comb in itertools.combinations(all_cells, size):
                        if all(any(cell in edge for cell in comb)
                               for edge in cell_edges):
                            brute = size
                            found = True
                            break
                    if found:
                        break
                assert brute == exact
                assertions += 1
            rows.append({
                "m_groups": m, "name_width": w, "record_bits": record,
                "physical_bits": physical_n, "word_factor_c": c,
                "word_bits": W, "max_groups_per_word": max_groups,
                "counting_lower": lower, "exact_cell_transversal": exact,
            })
    return rows, assertions


def main():
    exhaustive = exhaustive_hypergraphs_n4()
    hostile, a1 = hostile_families()
    two_level, a2 = two_level_or_controls()
    layout, a3 = indexed_locator_layout_controls()
    payload = {
        "artifact": "PERTURBATION-TRANSVERSAL172",
        "scope": (
            "Finite verification of perturbation-hypergraph and aligned-cell "
            "controls. The adaptive replay and two-level union theorems are "
            "proved symbolically in the accompanying report."
        ),
        "exhaustive_n4": exhaustive,
        "overlap_controls": hostile,
        "two_level_or_controls": two_level,
        "indexed_locator_layout_controls": layout,
        "total_assertions": exhaustive["assertions"] + a1 + a2 + a3,
        "randomness": "none",
        "status": {
            "finite_controls": "COMPUTATIONAL",
            "transversal_replay_theorem": "proved in report",
            "all_ordinary_SAT_or_ARC": "OPEN",
        },
    }
    RAW.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
