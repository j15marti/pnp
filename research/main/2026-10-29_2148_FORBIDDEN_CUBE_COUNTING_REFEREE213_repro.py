#!/usr/bin/env python3
"""Finite controls for FORBIDDEN-CUBE-COUNTING-REFEREE213.

Dependency-free, exhaustive on the declared small graph/XOR controls.
The symbolic #P classification is proved in the accompanying LaTeX report;
this program checks the identities and compares charged finite strategies.
"""

from __future__ import annotations

import itertools
import json
import time
import tracemalloc
from collections import defaultdict

SEED = 202610292148  # no randomized cases in this run


def lit_true(lit, assignment):
    value = assignment.get(abs(lit) - 1)
    if value is None:
        return None
    return value if lit > 0 else not value


def clause_status(clause, assignment):
    vals = [lit_true(l, assignment) for l in clause]
    if True in vals:
        return True
    if None in vals:
        return None
    return False


def formula_status(clauses, assignment):
    vals = [clause_status(c, assignment) for c in clauses]
    if False in vals:
        return False
    if all(v is True for v in vals):
        return True
    return None


def graph_formula(n, edges):
    """Horn proper width-3 source; vertices first, one selector per edge."""
    clauses = []
    for ei, (u, v) in enumerate(edges):
        assert 0 <= u < v < n
        x = n + ei + 1
        clauses.append((x, -(u + 1), -(v + 1)))
        clauses.append((-x, -(u + 1), -(v + 1)))
    return clauses, n + len(edges)


def occurrence_table(clauses, assignment=None, partial=None):
    assignment = assignment or {}
    partial = partial or {}
    out = []
    for j, clause in enumerate(clauses):
        for slot, lit in enumerate(clause):
            var = abs(lit) - 1
            sign = 1 if lit > 0 else -1
            full = lit_true(lit, assignment)
            pval = lit_true(lit, partial)
            out.append({
                "occurrence": f"x_{{{var},{j}}}", "variable": var,
                "source_clause": j, "slot": slot, "sign": sign,
                "preferred_sat_value": 1 if sign > 0 else 0,
                "full_literal_state": "unset" if full is None else bool(full),
                "partial_literal_state": "unset" if pval is None else bool(pval),
            })
    return out


def resolve(c, d, pivot):
    cp, dn = pivot + 1, -(pivot + 1)
    if cp in c and dn in d:
        left = [x for x in c if x != cp]
        right = [x for x in d if x != dn]
    elif dn in c and cp in d:
        left = [x for x in c if x != dn]
        right = [x for x in d if x != cp]
    else:
        return None
    lits = set(left + right)
    if any(-x in lits for x in lits):
        return "tautology"
    return tuple(sorted(lits, key=lambda z: (abs(z), z < 0)))


def all_first_resolvents(clauses):
    pos, neg = defaultdict(list), defaultdict(list)
    for j, c in enumerate(clauses):
        for lit in c:
            (pos if lit > 0 else neg)[abs(lit) - 1].append(j)
    records = []
    for v in sorted(set(pos) | set(neg)):
        for j in pos[v]:
            for k in neg[v]:
                r = resolve(clauses[j], clauses[k], v)
                records.append((v, j, k, r))
    return records


def profiles(clauses, nvars):
    hist = defaultdict(int)
    checks = 0
    for bits in itertools.product((False, True), repeat=nvars):
        a = dict(enumerate(bits))
        counts = [0, 0, 0, 0]
        for c in clauses:
            h = sum(bool(lit_true(l, a)) for l in c)
            counts[h] += 1
            checks += 1
        comp = {i: not b for i, b in a.items()}
        ccounts = [0, 0, 0, 0]
        for c in clauses:
            h = sum(bool(lit_true(l, comp)) for l in c)
            ccounts[h] += 1
            checks += 1
        assert ccounts == list(reversed(counts))
        E = counts[0] + counts[3]
        D = counts[3] - counts[0]
        assert E == ccounts[0] + ccounts[3]
        assert -D == ccounts[3] - ccounts[0]
        hist[(tuple(counts), E, D)] += 1
    return {str(k): v for k, v in hist.items()}, checks


def exact_clause_equity(clauses, nvars):
    q = [0] * len(clauses)
    checks = 0
    for bits in itertools.product((False, True), repeat=nvars):
        a = dict(enumerate(bits))
        status = [clause_status(c, a) for c in clauses]
        checks += len(clauses)
        false = [j for j, v in enumerate(status) if v is False]
        if len(false) == 1:
            q[false[0]] += 1
    return q, checks


def independent_sets(n, edges):
    count = 0
    by_size = [0] * (n + 1)
    for bits in itertools.product((0, 1), repeat=n):
        if all(not (bits[u] and bits[v]) for u, v in edges):
            count += 1
            by_size[sum(bits)] += 1
    return count, by_size


def forbidden_union_vertex_count(n, edges):
    count = 0
    overlap_hist = defaultdict(int)
    for bits in itertools.product((0, 1), repeat=n):
        hit = sum(bool(bits[u] and bits[v]) for u, v in edges)
        overlap_hist[hit] += 1
        if hit:
            count += 1
    return count, dict(sorted(overlap_hist.items()))


class Stats:
    def __init__(self):
        self.nodes = 0
        self.memo_hits = 0
        self.clause_scans = 0
        self.literal_reads = 0
        self.unit_writes = 0
        self.failed_probes = 0
        self.resolution_candidates = 0
        self.max_depth = 0
        self.peak_memo = 0

    def asdict(self):
        return self.__dict__.copy()


def unit_propagate(clauses, assignment, stats):
    assignment = dict(assignment)
    changed = True
    while changed:
        changed = False
        for c in clauses:
            stats.clause_scans += 1
            vals = []
            for l in c:
                stats.literal_reads += 1
                vals.append(lit_true(l, assignment))
            if True in vals:
                continue
            unset = [l for l, v in zip(c, vals) if v is None]
            if not unset:
                return None
            if len(unset) == 1:
                l = unset[0]
                v, val = abs(l) - 1, l > 0
                if v in assignment and assignment[v] != val:
                    return None
                if v not in assignment:
                    assignment[v] = val
                    stats.unit_writes += 1
                    changed = True
    return assignment


def dpll(clauses, nvars, failed_literal=False):
    stats, memo = Stats(), {}

    def rec(assignment, depth):
        stats.nodes += 1
        stats.max_depth = max(stats.max_depth, depth)
        a = unit_propagate(clauses, assignment, stats)
        if a is None:
            return False, None
        state = tuple(a.get(i, None) for i in range(nvars))
        if state in memo:
            stats.memo_hits += 1
            return memo[state]
        fs = formula_status(clauses, a)
        if fs is True:
            witness = dict(a)
            for i in range(nvars):
                witness.setdefault(i, False)
            result = (True, witness)
            memo[state] = result
            stats.peak_memo = max(stats.peak_memo, len(memo))
            return result
        if failed_literal:
            for v in range(nvars):
                if v in a:
                    continue
                outcomes = []
                for val in (False, True):
                    stats.failed_probes += 1
                    trial = dict(a); trial[v] = val
                    outcomes.append(unit_propagate(clauses, trial, stats))
                if outcomes[0] is None and outcomes[1] is None:
                    memo[state] = (False, None)
                    stats.peak_memo = max(stats.peak_memo, len(memo))
                    return False, None
                if outcomes[0] is None or outcomes[1] is None:
                    a = outcomes[1] if outcomes[0] is None else outcomes[0]
                    return rec(a, depth + 1)
                break  # charge one variable's two probes at this state
        v = next(i for i in range(nvars) if i not in a)
        for val in (False, True):
            b = dict(a); b[v] = val
            sat, witness = rec(b, depth + 1)
            if sat:
                memo[state] = (sat, witness)
                stats.peak_memo = max(stats.peak_memo, len(memo))
                return sat, witness
        memo[state] = (False, None)
        stats.peak_memo = max(stats.peak_memo, len(memo))
        return False, None

    sat, witness = rec({}, 0)
    if sat:
        assert formula_status(clauses, witness) is True
    return sat, stats.asdict()


def timed_strategy(name, clauses, nvars, mode):
    tracemalloc.start()
    t0 = time.perf_counter_ns()
    if mode == "source":
        sat, stats = dpll(clauses, nvars, False)
    elif mode == "failed":
        sat, stats = dpll(clauses, nvars, True)
    elif mode == "resolved":
        recs = all_first_resolvents(clauses)
        derived = sorted(set(r for _, _, _, r in recs if r not in (None, "tautology")))
        sat, stats = dpll(clauses + derived, nvars, False)
        stats["resolution_candidates"] = len(recs)
        stats["derived_clauses"] = len(derived)
    elif mode == "pair_compress":
        recs = all_first_resolvents(clauses)
        derived = sorted(set(r for _, _, _, r in recs if r not in (None, "tautology")))
        sat, stats = dpll(derived, nvars, False)
        stats["resolution_candidates"] = len(recs)
        stats["derived_clauses"] = len(derived)
    elif mode == "horn_witness":
        witness = {i: False for i in range(nvars)}
        reads = sum(len(c) for c in clauses)
        sat = formula_status(clauses, witness) is True
        stats = {"nodes": 1, "literal_reads": reads, "clause_scans": len(clauses),
                 "unit_writes": 0, "memo_hits": 0, "failed_probes": 0,
                 "resolution_candidates": 0, "max_depth": 0, "peak_memo": 0}
    else:
        raise ValueError(mode)
    elapsed = time.perf_counter_ns() - t0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {"name": name, "sat": sat, "elapsed_ns": elapsed,
            "python_peak_bytes": peak, **stats}


def xor3_clauses(rhs):
    # Forbid assignments whose parity differs from rhs.
    clauses = []
    for bits in itertools.product((0, 1), repeat=3):
        if (sum(bits) & 1) != rhs:
            clauses.append(tuple((i + 1) if not bits[i] else -(i + 1) for i in range(3)))
    return clauses


def gaussian_xor(equations, nvars):
    rows = [(mask, rhs) for mask, rhs in equations]
    rank = 0
    for col in range(nvars):
        pivot = next((i for i in range(rank, len(rows)) if (rows[i][0] >> col) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and ((rows[i][0] >> col) & 1):
                rows[i] = (rows[i][0] ^ rows[rank][0], rows[i][1] ^ rows[rank][1])
        rank += 1
    inconsistent = any(mask == 0 and rhs for mask, rhs in rows)
    return {"sat": not inconsistent, "rank": rank, "row_xors": len(equations) * nvars}


def graph_cases():
    return {
        "edge": (2, [(0, 1)]),
        "path4": (4, [(0, 1), (1, 2), (2, 3)]),
        "cycle4": (4, [(0, 1), (1, 2), (2, 3), (0, 3)]),
        "star5": (5, [(0, 1), (0, 2), (0, 3), (0, 4)]),
        "complete5": (5, [(i, j) for i in range(5) for j in range(i + 1, 5)]),
        "house5": (5, [(0, 1), (1, 2), (2, 3), (0, 3), (1, 4), (2, 4)]),
    }


def main():
    started = time.perf_counter()
    out = {"run_id": "FORBIDDEN-CUBE-COUNTING-REFEREE213", "seed": SEED,
           "method": "exhaustive small controls plus symbolic identities",
           "graphs": {}, "xor_controls": {}, "checks": 0}

    for name, (n, edges) in graph_cases().items():
        clauses, nvars = graph_formula(n, edges)
        assert all(len(c) == 3 and len(set(map(abs, c))) == 3 for c in clauses)
        assert all(sum(l > 0 for l in c) <= 1 for c in clauses)  # Horn
        recs = all_first_resolvents(clauses)
        non_taut = [r for _, _, _, r in recs if r != "tautology"]
        expected = sorted(tuple(sorted((-(u + 1), -(v + 1)), key=lambda z: (abs(z), z < 0)))
                          for u, v in edges)
        assert sorted(non_taut) == expected
        indep, by_size = independent_sets(n, edges)
        union_v, overlap = forbidden_union_vertex_count(n, edges)
        assert union_v == 2 ** n - indep
        union_full = union_v * 2 ** len(edges)
        q, qchecks = exact_clause_equity(clauses, nvars)
        out["checks"] += qchecks + 4
        full_prof, pchecks = profiles(clauses, nvars) if nvars <= 9 else ({"skipped": "nvars>9"}, 0)
        out["checks"] += pchecks
        sample_full = {i: False for i in range(nvars)}
        sample_partial = {0: True} if n else {}
        occs = occurrence_table(clauses, sample_full, sample_partial)
        var_scores = {}
        for v in range(nvars):
            pos = sum(1 for c in clauses if v + 1 in c)
            neg = sum(1 for c in clauses if -(v + 1) in c)
            var_scores[str(v)] = {"d_plus": pos, "d_minus": neg,
                                  "opposite_pairs": pos * neg}
        clause_pair_participation = [0] * len(clauses)
        for _, j, k, r in recs:
            if r != "tautology":
                clause_pair_participation[j] += 1
                clause_pair_participation[k] += 1
        runs = [
            timed_strategy("source_UP_DPLL", clauses, nvars, "source"),
            timed_strategy("failed_literal_DPLL", clauses, nvars, "failed"),
            timed_strategy("all_first_resolvents", clauses, nvars, "resolved"),
            timed_strategy("paired_tail_2CNF", clauses, nvars, "pair_compress"),
            timed_strategy("recognized_Horn_witness", clauses, nvars, "horn_witness"),
        ]
        assert all(r["sat"] for r in runs)
        out["graphs"][name] = {
            "n_vertices": n, "m_edges": len(edges), "n_source_variables": nvars,
            "n_source_clauses": len(clauses), "proper_width3": True, "horn": True,
            "connected_graph_control": True,
            "non_tautological_first_resolvents": len(non_taut),
            "raw_cube_weight": len(edges) / 4,
            "exact_union_vertex_assignments": union_v,
            "exact_union_full_assignments": union_full,
            "exact_union_density": union_v / (2 ** n),
            "independent_sets": indep, "independent_sets_by_size": by_size,
            "overlap_multiplicity_histogram": overlap,
            "clause_equity_Q": q,
            "clause_resolvent_participation": clause_pair_participation,
            "variable_occurrence_scores": var_scores,
            "first_occurrences": occs[:min(12, len(occs))],
            "complement_profiles": full_prof,
            "strategies": runs,
        }

    even = xor3_clauses(0)
    odd = xor3_clauses(1)
    even_recs = all_first_resolvents(even)
    assert len(even) == 4
    assert all(r == "tautology" for _, _, _, r in even_recs)
    xor_sat = gaussian_xor([(0b111, 0)], 3)
    xor_unsat = gaussian_xor([(0b111, 0), (0b111, 1)], 3)
    assert xor_sat["sat"] and not xor_unsat["sat"]
    dpll_even = timed_strategy("xor_even_CNF_DPLL", even, 3, "source")
    dpll_both = timed_strategy("xor_inconsistent_CNF_DPLL", even + odd, 3, "source")
    assert dpll_even["sat"] and not dpll_both["sat"]
    out["xor_controls"] = {
        "even_parity_clause_count": len(even),
        "opposite_pairs": len(even_recs),
        "non_tautological_resolvents": 0,
        "gaussian_sat": xor_sat, "gaussian_unsat": xor_unsat,
        "cnf_dpll_sat": dpll_even, "cnf_dpll_unsat": dpll_both,
        "interpretation": "high signed opposition but all first resolvents tautological; affine switch is easy",
    }

    out["formal_identities"] = {
        "source_equivalence": "AND_e[(x_e OR ~u OR ~v) AND (~x_e OR ~u OR ~v)] == AND_e(~u OR ~v)",
        "union_count": "U(H)=2^m*(2^n-I(H))",
        "star_density": "for K_1,r: (1/2)*(1-2^-r), while raw weight=r/4",
        "complexity_scope": "exact U is #P-complete under polynomial-time Turing reductions even on connected proper Horn width-3 sources; source SAT remains trivial",
    }
    out["checks"] += 8
    out["elapsed_seconds"] = time.perf_counter() - started
    out["limitations"] = [
        "graph family is not strict signed exact-(2,2)",
        "finite timings are CPython observations, not machine-independent bounds",
        "#P-completeness is a classification, not an unconditional FP lower bound",
        "the exact-overlap statistic is optional; a solver may switch to Horn/2SAT or retain the source",
    ]
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
