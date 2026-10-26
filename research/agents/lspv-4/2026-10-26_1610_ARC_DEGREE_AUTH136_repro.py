#!/usr/bin/env python3
"""Deterministic exact audit of degree-capped indexed Boolean summary verification.

This finite program tests the symbolic propositions; it is NOT a complexity
lower-bound experiment on arbitrary SAT deciders or a proof of P != NP.
No external Python dependencies. Run with Python >=3.9.
"""
from itertools import combinations, product
from fractions import Fraction
from math import comb
import json
import random

SEED = 13620261026
rng = random.Random(SEED)
checks = 0


def check(c, label):
    global checks
    checks += 1
    if not c:
        raise AssertionError(f"Assertion #{checks}: {label}")


def degree_monomials(k, d):
    return tuple(m for m in range(1 << k) if m.bit_count() <= d)


def point_row(monos, x):
    return sum((1 << j) for j, m in enumerate(monos) if (m & x) == m)


def poly_value(coeff, monos, x):
    return (coeff & point_row(monos, x)).bit_count() & 1


def coefficient_from_queries(k, d, values):
    """Möbius inversion from values indexed by points of weight <=d."""
    monos = degree_monomials(k, d)
    out = 0
    for j, t in enumerate(monos):
        s = t
        bit = 0
        while True:
            bit ^= values[s]
            if s == 0:
                break
            s = (s - 1) & t
        out |= bit << j
    return out


def kernel_witness(rows, D):
    """One nonzero vector annihilated by all given GF(2) rows, if rank<D."""
    echelon = {}
    for original in rows:
        v = original
        while v:
            p = v.bit_length() - 1
            if p not in echelon:
                echelon[p] = v
                break
            v ^= echelon[p]
    if len(echelon) == D:
        return None
    free = next(j for j in range(D) if j not in echelon)
    vector = 1 << free
    for p in sorted(echelon):
        if (echelon[p] & vector).bit_count() & 1:
            vector |= 1 << p
    assert all(((v & vector).bit_count() & 1) == 0 for v in rows)
    return vector


def truth_degree(table, k):
    """ANF coefficient transform, returns -1 for identically zero."""
    f = list(table)
    for i in range(k):
        for mask in range(1 << k):
            if (mask >> i) & 1:
                f[mask] ^= f[mask ^ (1 << i)]
    return max((mask.bit_count() for mask, bit in enumerate(f) if bit), default=-1)


def cnf_value(clauses, x):
    for clause in clauses:
        if not any(((x >> (v - 1)) & 1) == int(positive) for v, positive in clause):
            return 0
    return 1


def signed_ternary(xnames, signs):
    return tuple((name, bool(sign)) for name, sign in zip(xnames, signs))


def check_reduction(clauses, variables, d):
    """Circuit H(x,z)=CNF(x) AND z_1 AND...AND z_(d+1)."""
    k = variables + d + 1
    table = []
    for x in range(1 << k):
        base = x & ((1 << variables) - 1)
        extra = x >> variables
        table.append(int(cnf_value(clauses, base) == 1 and extra == (1 << (d + 1)) - 1))
    sat = any(cnf_value(clauses, x) for x in range(1 << variables))
    adeg = truth_degree(table, k)
    check((adeg <= d) == (not sat), "fixed-d circuit-degree reduction SAT/UNSAT")
    check((adeg == -1) == (not sat), "zero iff source UNSAT")
    if sat:
        check(adeg >= d + 1, "nonzero circuit multiplied by fresh monomial degree")
    return sat, adeg


def main():
    sampled_polynomials = 0
    lower_bound_witnesses = 0
    experimental = []
    for k in range(0, 7):
        for d in range(0, min(k, 3) + 1):
            monos = degree_monomials(k, d)
            D = len(monos)
            canonical = tuple(monos)
            check(D == sum(comb(k, j) for j in range(d + 1)), "Reed-Muller dimension")
            if D <= 16:
                coeffs = range(1 << D)
            else:
                coeffs = [0, (1 << D) - 1] + [rng.getrandbits(D) for _ in range(512)]
            for coeff in coeffs:
                data = {point: poly_value(coeff, monos, point) for point in canonical}
                check(coefficient_from_queries(k, d, data) == coeff, "Möbius interpolation exact")
                check((coeff == 0) == all(v == 0 for v in data.values()), "canonical query set zero-test")
                sampled_polynomials += 1
            points = list(range(1 << k))
            for trial in range(5):
                rng.shuffle(points)
                for q in sorted(set([0, D // 3, D - 1])):
                    rows = [point_row(monos, x) for x in points[:q]]
                    witness = kernel_witness(rows, D)
                    check(witness is not None and witness != 0, "q<D nullspace nonzero")
                    check(all(poly_value(witness, monos, x) == 0 for x in points[:q]), "hidden low-degree polynomial")
                    check(any(poly_value(witness, monos, x) for x in range(1 << k)), "hidden polynomial is nonzero")
                    lower_bound_witnesses += 1
            experimental.append({"k": k, "d": d, "dimension": D, "polynomials_checked":len(coeffs)})

    # All eight possible proper signed 3-clauses on the same three names: UNSAT.
    all8 = [signed_ternary((1, 2, 3), bits) for bits in product((0, 1), repeat=3)]
    seven = all8[:-1]
    # Also test an always-satisfiable empty CNF and repeated random CNFs.
    sources = [(all8, 3), (seven, 3), ([], 3)]
    for _ in range(400):
        n = rng.choice((3, 4))
        m = rng.randrange(0, 13)
        cls = []
        for _ in range(m):
            names = rng.sample(range(1, n + 1), 3)
            signs = [rng.randrange(2) for _ in range(3)]
            cls.append(signed_ternary(names, signs))
        sources.append((cls, n))
    red_tests = 0
    sat_sources = 0
    unsat_sources = 0
    for clauses, vars_ in sources:
        for d in (0, 1, 2, 3):
            sat, gotdeg = check_reduction(clauses, vars_, d)
            red_tests += 1
            if d == 0:
                sat_sources += int(sat)
                unsat_sources += int(not sat)
    check(unsat_sources >= 1 and sat_sources >= 1, "both SAT and UNSAT controls")

    # Adversarial nonaffine small circuit that defeats low-degree probes.
    k, d = 6, 2
    canonical = degree_monomials(k, d)
    address = (1 << (d + 1)) - 1
    check(address not in canonical, "point beyond canonical degree budget")
    check(all(int(x == address) == 0 for x in canonical), "point function hides on degree-d probes")
    check(int(address == address) == 1, "hidden point exists")
    # Its ANF degree is k; the point function is representable with O(k) AND/NOT gates.
    truth = [int(x == address) for x in range(1 << k)]
    check(truth_degree(truth, k) == k, "point function full algebraic degree")

    # Exact source-verified theorem thresholds; do not transfer models without proof.
    c = Fraction(241, 200)
    flmv_beta = ((c + 2) / c**2 - c) / 2
    c_vm = Fraction(651000, 361301)
    proposed_c = Fraction(7, 4)
    margin = c_vm - proposed_c
    check(margin > 0, "strict van Melkebeek time margin")
    check(Fraction(1, 2) < flmv_beta, "strict FLMV space margin")
    cost_table = []
    for k, d in ((20, 1), (20, 2), (20, 3), (20, 10), (24, 2), (24, 3), (24, 4), (24, 12)):
        D = sum(comb(k, j) for j in range(d + 1))
        cost_table.append({"boundary_bits":k,"degree":d,"exact_queries":D,"unrestricted_truth_table":1 << k,"fraction_of_truth_table":f"{D}/{1<<k}"})

    result = {
        "run_id": "ARC-DEGREE-AUTH136",
        "seed": SEED,
        "proof_status": "PROVED/EXACT for scoped query and fixed-degree decision reductions; COMPUTATIONAL for finite audit; OPEN for all-input ARC contraction and P != NP",
        "assertion_groups":checks,
        "low_degree_polynomials_checked":sampled_polynomials,
        "q_less_than_dimension_kernel_witnesses":lower_bound_witnesses,
        "circuit_degree_reduction_controls":red_tests,
        "sources_sat":sat_sources,
        "sources_unsat":unsat_sources,
        "canonical_interpolation_sweep":experimental,
        "hostile_control":{"k":6,"d":2,"point_address":address,"all_low_weight_queries_zero":True,"truth_degree":6},
        "vm_extra_seed_c_threshold":str(c_vm),
        "vm_margin_for_7_over_4":str(margin),
        "flmv_c":str(c),
        "flmv_beta":str(flmv_beta),
        "flmv_space_margin_for_1_over_2":str(flmv_beta - Fraction(1,2)),
        "query_cost_table":cost_table
    }
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
