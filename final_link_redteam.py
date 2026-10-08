#!/usr/bin/env python3
"""Bounded hostile audit for the remaining COVER-SHRINK / Route-B link.

The experiment is intentionally restricted.  It verifies exact arithmetic and
tests a finite portfolio of concrete structural mechanisms.  It is not a SAT
lower bound and does not decide P versus NP.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import signal
import time
from collections import defaultdict, deque
from fractions import Fraction
from pathlib import Path


Clause = tuple[int, ...]
CNF = tuple[Clause, ...]


def alarm_handler(_signum, _frame):
    raise TimeoutError("25-second internal deadline exceeded")


def variables(cnf: CNF) -> list[int]:
    return sorted({abs(lit) for clause in cnf for lit in clause})


def encoding_bits(cnf: CNF, source_n: int | None = None) -> int:
    """Declared indexed-clause-list measure with the original index width."""
    n = source_n if source_n is not None else max(variables(cnf), default=1)
    width = max(1, math.ceil(math.log2(n + 1)))
    return sum(1 + len(clause) * (width + 1) for clause in cnf)


def canonical_clause(clause: Clause) -> Clause | None:
    lits = set(clause)
    if any(-lit in lits for lit in lits):
        return None
    return tuple(sorted(lits, key=lambda z: (abs(z), z < 0)))


def normalize(cnf: CNF, subsumption: bool = True) -> CNF:
    clauses: set[Clause] = set()
    for clause in cnf:
        c = canonical_clause(clause)
        if c is not None:
            clauses.add(c)
    if () in clauses:
        return ((),)
    ordered = sorted(clauses, key=lambda c: (len(c), c))
    if not subsumption:
        return tuple(ordered)
    kept: list[Clause] = []
    kept_sets: list[frozenset[int]] = []
    for clause in ordered:
        s = frozenset(clause)
        if any(t <= s for t in kept_sets):
            continue
        kept.append(clause)
        kept_sets.append(s)
    return tuple(kept)


def restrict_once(cnf: CNF, assignment: dict[int, bool]) -> CNF:
    out: list[Clause] = []
    for clause in cnf:
        residual: list[int] = []
        satisfied = False
        for lit in clause:
            v = abs(lit)
            if v not in assignment:
                residual.append(lit)
                continue
            value = assignment[v]
            if (lit > 0 and value) or (lit < 0 and not value):
                satisfied = True
                break
        if not satisfied:
            out.append(tuple(residual))
    return normalize(tuple(out), subsumption=True)


def unit_propagate(cnf: CNF, initial: dict[int, bool] | None = None) -> tuple[CNF, dict[int, bool], bool]:
    assignment = dict(initial or {})
    current = restrict_once(cnf, assignment)
    while True:
        if () in current:
            return ((),), assignment, True
        units = [c[0] for c in current if len(c) == 1]
        if not units:
            return current, assignment, False
        changed = False
        for lit in units:
            v, value = abs(lit), lit > 0
            if v in assignment and assignment[v] != value:
                return ((),), assignment, True
            if v not in assignment:
                assignment[v] = value
                changed = True
        if not changed:
            return current, assignment, False
        current = restrict_once(current, assignment)


def brute_sat(cnf: CNF) -> bool:
    vs = variables(cnf)
    for bits in itertools.product((False, True), repeat=len(vs)):
        a = dict(zip(vs, bits))
        if all(any((lit > 0) == a[abs(lit)] for lit in clause) for clause in cnf):
            return True
    return False


def is_horn(cnf: CNF) -> bool:
    return all(sum(lit > 0 for lit in clause) <= 1 for clause in cnf)


def is_antihorn(cnf: CNF) -> bool:
    return all(sum(lit < 0 for lit in clause) <= 1 for clause in cnf)


def is_2cnf(cnf: CNF) -> bool:
    return all(len(clause) <= 2 for clause in cnf)


def clause_components(cnf: CNF) -> list[CNF]:
    nonempty = [c for c in cnf if c]
    if not nonempty:
        return [cnf] if cnf else []
    var_to_clauses: dict[int, list[int]] = defaultdict(list)
    for i, clause in enumerate(nonempty):
        for v in {abs(l) for l in clause}:
            var_to_clauses[v].append(i)
    unseen = set(range(len(nonempty)))
    comps: list[CNF] = []
    while unseen:
        root = unseen.pop()
        q = deque([root])
        ids = {root}
        seen_vars: set[int] = set()
        while q:
            i = q.popleft()
            for v in {abs(l) for l in nonempty[i]}:
                if v in seen_vars:
                    continue
                seen_vars.add(v)
                for j in var_to_clauses[v]:
                    if j in unseen:
                        unseen.remove(j)
                        ids.add(j)
                        q.append(j)
        comps.append(tuple(nonempty[i] for i in sorted(ids)))
    return comps


def pack_components(comps: list[CNF], limit_bits: int, source_n: int) -> int | None:
    sizes = sorted((encoding_bits(c, source_n) for c in comps), reverse=True)
    bins: list[int] = []
    for size in sizes:
        if size > limit_bits:
            return None
        for i, used in enumerate(bins):
            if used + size <= limit_bits:
                bins[i] += size
                break
        else:
            bins.append(size)
    return len(bins)


def primal_adjacency(cnf: CNF, n: int) -> list[int]:
    adj = [0] * n
    for clause in cnf:
        vs = sorted({abs(l) - 1 for l in clause})
        for i, u in enumerate(vs):
            for v in vs[i + 1 :]:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
    return adj


def exact_vertex_separation(cnf: CNF, n: int) -> int:
    """Exact vertex-separation number, equal to primal-graph pathwidth."""
    adj = primal_adjacency(cnf, n)
    total = 1 << n
    boundary = [0] * total
    full = total - 1
    for mask in range(total):
        outside = full ^ mask
        b = 0
        x = mask
        while x:
            bit = x & -x
            v = bit.bit_length() - 1
            if adj[v] & outside:
                b += 1
            x ^= bit
        boundary[mask] = b
    dp = [n + 1] * total
    dp[0] = 0
    for mask in range(1, total):
        best = n + 1
        x = mask
        while x:
            bit = x & -x
            candidate = max(dp[mask ^ bit], boundary[mask])
            if candidate < best:
                best = candidate
            x ^= bit
        dp[mask] = best
    return dp[-1]


def minimum_strong_2cnf_backdoor(cnf: CNF, n: int) -> int:
    clause_vars = [{abs(l) for l in clause} for clause in cnf if len(clause) > 2]
    for h in range(n + 1):
        for subset in itertools.combinations(range(1, n + 1), h):
            b = set(subset)
            if all(len(vs - b) <= 2 for vs in clause_vars):
                return h
    raise AssertionError("unreachable")


def count_subsumed(cnf: CNF) -> int:
    raw = []
    for c in cnf:
        cc = canonical_clause(c)
        if cc is not None:
            raw.append(frozenset(cc))
    count = 0
    for i, s in enumerate(raw):
        if any(j != i and t < s for j, t in enumerate(raw)):
            count += 1
    return count


def shannon_shrink_search(cnf: CNF, n: int, h_cap: int, child_limit: int) -> dict | None:
    vs = variables(cnf)
    for h in range(h_cap + 1):
        for subset in itertools.combinations(vs, h):
            worst = 0
            okay = True
            for bits in itertools.product((False, True), repeat=h):
                residual, _, _ = unit_propagate(cnf, dict(zip(subset, bits)))
                size = encoding_bits(residual, n)
                worst = max(worst, size)
                if size > child_limit:
                    okay = False
                    break
            if okay:
                return {"h": h, "variables": list(subset), "worst_child_bits": worst, "leaves": 2**h}
    return None


def separator_plan_search(cnf: CNF, n: int, h_cap: int, child_limit: int, q_limit: int) -> dict | None:
    vs = variables(cnf)
    for h in range(h_cap + 1):
        for subset in itertools.combinations(vs, h):
            total_children = 0
            worst = 0
            okay = True
            for bits in itertools.product((False, True), repeat=h):
                residual, _, conflict = unit_propagate(cnf, dict(zip(subset, bits)))
                if conflict:
                    continue
                comps = clause_components(residual)
                packed = pack_components(comps, child_limit, n)
                if packed is None:
                    okay = False
                    break
                total_children += packed
                worst = max(worst, max((encoding_bits(c, n) for c in comps), default=0))
                if total_children > q_limit:
                    okay = False
                    break
            if okay:
                return {
                    "h": h,
                    "variables": list(subset),
                    "total_children": total_children,
                    "worst_component_bits": worst,
                }
    return None


def solve_gf2(rows: list[tuple[int, int]], n: int) -> bool:
    basis: dict[int, tuple[int, int]] = {}
    for mask, rhs in rows:
        while mask:
            pivot = mask.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = (mask, rhs)
                break
            bm, br = basis[pivot]
            mask ^= bm
            rhs ^= br
        if mask == 0 and rhs:
            return False
    return True


def xor_system_recognizer(cnf: CNF, n: int) -> bool | None:
    groups: dict[tuple[int, ...], list[Clause]] = defaultdict(list)
    for clause in cnf:
        key = tuple(sorted({abs(l) for l in clause}))
        if len(clause) != 3 or len(key) != 3:
            return None
        groups[key].append(clause)
    rows: list[tuple[int, int]] = []
    for key, clauses in groups.items():
        if len(clauses) != 4:
            return None
        forbidden: set[tuple[int, int, int]] = set()
        for clause in clauses:
            signs = {abs(l): l > 0 for l in clause}
            forbidden.add(tuple(0 if signs[v] else 1 for v in key))
        parities = {sum(bits) & 1 for bits in forbidden}
        if len(forbidden) != 4 or len(parities) != 1:
            return None
        allowed_parity = 1 - next(iter(parities))
        mask = sum(1 << (v - 1) for v in key)
        rows.append((mask, allowed_parity))
    return solve_gf2(rows, n)


def petersen_tseitin(odd_charge: bool = True, perturb: bool = False) -> tuple[CNF, int]:
    outer = [(i, (i + 1) % 5) for i in range(5)]
    spokes = [(i, i + 5) for i in range(5)]
    inner = [(5 + i, 5 + ((i + 2) % 5)) for i in range(5)]
    edges = outer + spokes + inner
    incidence: dict[int, list[int]] = defaultdict(list)
    for idx, (u, v) in enumerate(edges, 1):
        incidence[u].append(idx)
        incidence[v].append(idx)
    clauses: list[Clause] = []
    for vertex in range(10):
        edge_vars = sorted(incidence[vertex])
        charge = 1 if odd_charge and vertex == 0 else 0
        for bits in itertools.product((0, 1), repeat=3):
            if (sum(bits) & 1) != charge:
                clauses.append(tuple(v if bit == 0 else -v for v, bit in zip(edge_vars, bits)))
    if perturb:
        clauses.append((1, 2, 3))
    return normalize(tuple(clauses), subsumption=False), len(edges)


def random_3cnf(n: int, m: int, seed: int) -> CNF:
    rng = random.Random(seed)
    clauses: set[Clause] = set()
    while len(clauses) < m:
        vs = sorted(rng.sample(range(1, n + 1), 3))
        clause = tuple(v if rng.randrange(2) else -v for v in vs)
        clauses.add(canonical_clause(clause) or ())
    return normalize(tuple(clauses), subsumption=False)


def independent_3clauses(m: int) -> tuple[CNF, int]:
    clauses = tuple((3 * i + 1, 3 * i + 2, 3 * i + 3) for i in range(m))
    return clauses, 3 * m


def signed_complete_triples(n: int, seed: int) -> CNF:
    rng = random.Random(seed)
    clauses = []
    for triple in itertools.combinations(range(1, n + 1), 3):
        clauses.append(tuple(v if rng.randrange(2) else -v for v in triple))
    return normalize(tuple(clauses), subsumption=False)


def portfolio_audit(name: str, cnf: CNF, n: int) -> dict:
    start = time.monotonic()
    normalized, _, conflict = unit_propagate(cnf)
    m_bits = encoding_bits(cnf, n)
    q_limit = max(1, math.floor(m_bits ** (1 / 3)))
    child_limit = max(1, math.floor(m_bits ** (2 / 3)))
    h_cap = max(0, math.floor(math.log2(q_limit)))
    pw_cap = max(0, math.floor(math.log2(max(2.0, math.log2(max(4, m_bits))))))
    comps = clause_components(normalized)
    packed = pack_components(comps, child_limit, n) if not conflict else 0
    pathwidth = exact_vertex_separation(normalized, n) if n <= 18 and not conflict else 0
    backdoor = minimum_strong_2cnf_backdoor(normalized, n) if not conflict else 0
    shannon = None if conflict else shannon_shrink_search(normalized, n, h_cap, child_limit)
    separator = None if conflict else separator_plan_search(normalized, n, h_cap, child_limit, q_limit)
    xor_answer = xor_system_recognizer(normalized, n) if not conflict else False
    base = conflict or not normalized or is_horn(normalized) or is_antihorn(normalized) or is_2cnf(normalized)
    component_success = packed is not None and packed <= q_limit and len(comps) > 1
    backdoor_success = (2**backdoor) <= q_limit
    pathwidth_success = pathwidth <= pw_cap
    dominance_success = count_subsumed(cnf) > 0 and encoding_bits(normalize(cnf), n) <= child_limit
    basic_winners = []
    if base:
        basic_winners.append("base_or_unit")
    if component_success:
        basic_winners.append("component_pack")
    if backdoor_success:
        basic_winners.append("strong_2cnf_backdoor")
    if pathwidth_success:
        basic_winners.append("polylog_pathwidth")
    if shannon is not None:
        basic_winners.append("small_shannon")
    if separator is not None:
        basic_winners.append("small_separator")
    if dominance_success:
        basic_winners.append("clause_dominance")
    enhanced = list(basic_winners)
    if xor_answer is not None:
        enhanced.append("xor_system")
    reference = brute_sat(cnf) if n <= 18 else None
    if xor_answer is not None and reference is not None:
        assert xor_answer == reference
    return {
        "name": name,
        "variables": n,
        "clauses": len(cnf),
        "encoded_bits_M": m_bits,
        "q_limit_floor_M_1_3": q_limit,
        "child_limit_floor_M_2_3": child_limit,
        "branch_variable_cap_floor_log2_q": h_cap,
        "polylog_pathwidth_cap": pw_cap,
        "reference_sat": reference,
        "unit_conflict": conflict,
        "horn": is_horn(normalized),
        "antihorn": is_antihorn(normalized),
        "two_cnf": is_2cnf(normalized),
        "components": len(comps),
        "packed_component_children": packed,
        "subsumed_clauses": count_subsumed(cnf),
        "minimum_strong_2cnf_backdoor": backdoor,
        "exact_primal_pathwidth": pathwidth,
        "shannon_plan": shannon,
        "separator_plan": separator,
        "xor_recognized_answer": xor_answer,
        "basic_portfolio_winners": basic_winners,
        "enhanced_portfolio_winners": enhanced,
        "basic_portfolio_covered": bool(basic_winners),
        "enhanced_portfolio_covered": bool(enhanced),
        "elapsed_seconds": time.monotonic() - start,
    }


def route_b_arithmetic() -> dict:
    c = Fraction(4, 3)
    k = Fraction(2, 1)
    d = Fraction(2, 1) / c - c
    assert d == Fraction(1, 6)
    cases = []
    parameters = [
        ("old_half_scale_single_child", Fraction(0), Fraction(1, 12), Fraction(1, 2)),
        ("half_scale_all_blocks", Fraction(1, 2), Fraction(1, 12), Fraction(1, 2)),
        ("cover_shrink_target", Fraction(1, 3), Fraction(0), Fraction(2, 3)),
        ("corrected_near_space_boundary", Fraction(5, 6), Fraction(1, 6) - Fraction(1, 120), Fraction(1, 6) - Fraction(1, 120)),
        ("beta_zero_boundary", Fraction(2, 3), Fraction(0), Fraction(1, 3)),
    ]
    for name, a, beta, lam in parameters:
        single = beta + lam * k
        global_cost = a + beta + lam * k
        interface_1 = beta < (c - 1) * (1 - lam)
        interface_2 = beta < c - 1 + lam
        cases.append(
            {
                "name": name,
                "a": str(a),
                "beta": str(beta),
                "lambda": str(lam),
                "single_child_exponent": str(single),
                "global_pointwise_exponent": str(global_cost),
                "single_child_below_C": single < c,
                "global_below_C": global_cost < c,
                "explicit_cover_a_plus_lambda_ge_1": a + lam >= 1,
                "tt_interface_1": interface_1,
                "tt_interface_2": interface_2,
                "space_beta_below_D1": beta < d,
            }
        )
    grid_checks = 0
    equivalence_errors = 0
    for ai in range(0, 13):
        for bi in range(0, 13):
            for li in range(0, 13):
                a = Fraction(ai, 12)
                beta = Fraction(bi, 12)
                lam = Fraction(li, 12)
                lhs = a + beta + lam * k < c
                rhs = lam < (c - a - beta) / k
                grid_checks += 1
                equivalence_errors += lhs != rhs
    assert equivalence_errors == 0
    return {
        "C": str(c),
        "selected_solver_k": str(k),
        "D1_of_C": str(d),
        "single_child_condition": "beta + lambda*k < C",
        "global_condition": "a + beta + lambda*k < C",
        "all_block_fanout": "a = 1 - lambda",
        "all_block_k2_C4_3_condition": "lambda + beta < 1/3",
        "explicit_cover_condition": "a + lambda >= 1",
        "explicit_cover_implies": "lambda + beta < 1/3 for k=2,C=4/3",
        "grid_equivalence_checks": grid_checks,
        "grid_errors": equivalence_errors,
        "cases": cases,
    }


def arc_endpoint_arithmetic() -> dict:
    gamma = 2 * math.cos(math.pi / 7)
    lam = Fraction(1, 2)
    p = Fraction(1, 2)
    threshold = (gamma - 1.5) / 2
    rows = []
    for label, beta in (
        ("one_sixth", Fraction(1, 6)),
        ("one_seventh", Fraction(1, 7)),
        ("three_twentieth", Fraction(3, 20)),
    ):
        w = 1 - float(lam) + float(beta)
        c_star = w / (1 - float(lam))
        total = c_star + float(p)
        rows.append(
            {
                "label": label,
                "beta": str(beta),
                "w": w,
                "C_star": c_star,
                "S_star_floor": str(p),
                "C_star_plus_S_star": total,
                "strictly_below_gamma": total < gamma,
            }
        )
    return {
        "gamma_2cos_pi_over_7": gamma,
        "typed_recurrence": "C*=max(r,w/(1-lambda)); S*=p",
        "all_block_w": "1-lambda+beta+g",
        "lambda": str(lam),
        "p_floor": str(p),
        "g": "0",
        "strict_beta_threshold": threshold,
        "strict_condition": "beta < (gamma-3/2)/2",
        "rows": rows,
    }


def combinatorial_controls() -> dict:
    independent_rows = []
    for m in (12, 24, 48, 96, 192):
        cnf, n = independent_3clauses(m)
        m_bits = encoding_bits(cnf, n)
        child_limit = math.floor(m_bits ** (2 / 3))
        unit_clause_cost = 1 + (math.ceil(math.log2(n + 1)) + 1)
        r = min(m, child_limit // unit_clause_cost)
        log2_q_lower = max(0, (m - r) * math.log2(7 / 4))
        q_target = m_bits ** (1 / 3)
        independent_rows.append(
            {
                "blocks_m": m,
                "M_bits": m_bits,
                "child_limit_bits": child_limit,
                "max_residual_clauses_from_unit_cost": r,
                "log2_restriction_solution_cover_lower_bound": log2_q_lower,
                "q_target_M_1_3": q_target,
                "lower_bound_exceeds_target": log2_q_lower > math.log2(q_target),
            }
        )
    backdoor_rows = []
    for n in (8, 10, 12, 14, 16, 18, 20):
        cnf = signed_complete_triples(n, 20261007 + n)
        m_bits = encoding_bits(cnf, n)
        q_lower = 2 ** (n - 2)
        q_target = m_bits ** (1 / 3)
        backdoor_rows.append(
            {
                "variables_n": n,
                "clauses": len(cnf),
                "M_bits": m_bits,
                "minimum_term_domain": n - 2,
                "tautological_2cnf_backdoor_dnf_terms_lower_bound": q_lower,
                "q_target_M_1_3": q_target,
                "lower_bound_exceeds_target": q_lower > q_target,
            }
        )
    return {"restriction_solution_cover": independent_rows, "backdoor_dnf": backdoor_rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="final_link_redteam_results.json")
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(25)
    started = time.monotonic()

    ind, ind_n = independent_3clauses(5)
    tseitin, tseitin_n = petersen_tseitin(odd_charge=True)
    perturbed, perturbed_n = petersen_tseitin(odd_charge=False, perturb=True)
    random_formula = random_3cnf(16, 55, 20261007)
    cases = [
        portfolio_audit("independent_positive_3clauses", ind, ind_n),
        portfolio_audit("petersen_odd_tseitin", tseitin, tseitin_n),
        portfolio_audit("petersen_even_tseitin_plus_clause", perturbed, perturbed_n),
        portfolio_audit("seeded_random_3cnf", random_formula, 16),
    ]

    result = {
        "status": "COMPUTATIONAL_RESTRICTED_MODEL",
        "claim_guard": "No unrestricted SAT lower bound and no P-versus-NP conclusion.",
        "seed": 20261007,
        "deadline_seconds": 25,
        "encoding_measure": "sum over clauses of 1 + |C|*(1+ceil(log2(n+1))), retaining source variable index width",
        "route_b": route_b_arithmetic(),
        "arc_endpoint": arc_endpoint_arithmetic(),
        "combinatorial_controls": combinatorial_controls(),
        "portfolio_cases": cases,
        "elapsed_seconds": time.monotonic() - started,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    checks = result["route_b"]["grid_equivalence_checks"]
    checks += len(result["combinatorial_controls"]["restriction_solution_cover"])
    checks += len(result["combinatorial_controls"]["backdoor_dnf"])
    checks += len(cases)
    result["declared_check_groups"] = checks
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    signal.alarm(0)
    print(json.dumps({"status": result["status"], "checks": checks, "elapsed_seconds": result["elapsed_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
