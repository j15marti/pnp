#!/usr/bin/env python3
"""CA01: independent finite checks of proof-composition obligations.

Standard-library only. These exhaustive reference computations are an audit,
not a proposed polynomial-time SAT algorithm. Run:
  python3 CA01_check.py --output CA01_results.json
Optionally compare the recovered first reserve experiment's summary:
  --prior-reserve-results /absolute/path/tetra_matching_reserve_results.json
"""
import argparse
import itertools as it
import json
import random
from functools import lru_cache
from math import prod
from pathlib import Path


def graph(n, edges):
    neighbors = [0] * n
    for u, v in edges:
        neighbors[u] |= 1 << v
        neighbors[v] |= 1 << u
    return neighbors


def matching_oracle(neighbors):
    """Exact exponential subset recurrence, used only as a small reference."""
    @lru_cache(None)
    def maximum(mask):
        if not mask:
            return 0
        bit = mask & -mask
        u = bit.bit_length() - 1
        rest = mask ^ bit
        best = maximum(rest)
        available = neighbors[u] & rest
        while available:
            vbit = available & -available
            available ^= vbit
            best = max(best, 1 + maximum(rest ^ vbit))
        return best
    return maximum


def gf2_rank(vectors):
    basis = {}
    for value in vectors:
        while value:
            pivot = value.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = value
                break
            value ^= basis[pivot]
    return len(basis)


def reserve_controls():
    # Same seed, input generator, and 120 graph domain as the recovered script.
    rng = random.Random(20261124)
    result = dict(seed=20261124, reserve_graphs=0, reserve_masks=0,
                  saturation_true=0, saturation_false=0)
    for _ in range(120):
        b = rng.randint(2, 8)
        k = 2 * rng.randint(1, 3)
        edges = [e for e in it.combinations(range(b), 2)
                 if rng.random() < .45]
        h = graph(b, edges)
        nu = matching_oracle(h)
        augmented = edges + list(it.combinations(range(b, b+k), 2))
        augmented += list(it.product(range(b), range(b, b+k)))
        pm = matching_oracle(graph(b+k, augmented))
        reserve = ((1 << k) - 1) << b
        alpha, all_even = 0, True
        for mask in range(1 << b):
            size = mask.bit_count()
            demand = size - 2 * nu(mask)
            predicted = size % 2 == 0 and demand <= k
            actual = 2 * pm(mask | reserve) == size + k
            assert predicted == actual
            if all(not (mask & h[u]) for u in range(b) if mask >> u & 1):
                alpha = max(alpha, size)
            if size % 2 == 0 and not actual:
                all_even = False
            result['reserve_masks'] += 1
        assert all_even == (alpha <= k + 1)
        result['saturation_true' if all_even else 'saturation_false'] += 1
        result['reserve_graphs'] += 1
    # An even affine hull does not certify full support.
    support = [x for x in range(1 << 8)
               if x.bit_count() % 2 == 0 and x.bit_count() <= 2]
    assert len(support) == 29 and gf2_rank(support) == 7
    assert 0b1111 not in support
    result['hull_hole'] = dict(boundary_ports=8, reserve_vertices=2,
                               actual_rows=len(support), affine_hull_rows=128,
                               affine_rank=7, missing_row=0b1111)
    # Retain guards. Every pinned conditional hull in this control is full,
    # although the global even support still omits the weight-eight words.
    guards = 0
    for g in range(4):
        for pins in it.combinations(range(9), g):
            fixed = sum(1 << i for i in pins)
            free = [i for i in range(9) if not fixed >> i & 1]
            for values in it.product((0, 1), repeat=g):
                anchor = sum(v << i for i, v in zip(pins, values))
                if anchor.bit_count() % 2:
                    anchor |= 1 << free[0]
                assert anchor.bit_count() <= 6
                for i, j in it.combinations(free, 2):
                    word = anchor ^ (1 << i) ^ (1 << j)
                    assert word & fixed == anchor & fixed
                    assert word.bit_count() % 2 == 0 and word.bit_count() <= 6
                guards += 1
    assert guards == 835
    result['conditional_guard_checks'] = guards
    return result


def literal(lit, word):
    return ((word >> (abs(lit)-1)) & 1) == int(lit > 0)


def cnf_satisfied(clauses, word):
    return all(any(literal(lit, word) for lit in clause) for clause in clauses)


def mixed_compile(clauses, n):
    binary, affine = [], []
    for i, clause in enumerate(clauses):
        ys = [n + 3*i + j + 1 for j in range(3)]
        binary.extend((-ys[j], -ys[k]) for j, k in it.combinations(range(3), 2))
        binary.extend((-ys[j], clause[j]) for j in range(3))
        affine.append(sum(1 << (v-1) for v in ys))
    return n + 3*len(clauses), binary, affine


def mixed_satisfied(binary, affine, word):
    return cnf_satisfied(binary, word) and all((a & word).bit_count() % 2 for a in affine)


def composition_controls():
    clauses = [tuple((i+1) if signs >> i & 1 else -(i+1) for i in range(3))
               for signs in range(8)]
    result = dict(formulas=0, source_sat=0, source_unsat=0,
                  full_mixed_enumerations=0, full_mixed_words=0,
                  known_sat_wrapper_checks=0, forced_switches=0)
    source_counts, extension_counts = [], []
    for mask in range(256):
        formula = [clauses[i] for i in range(8) if mask >> i & 1]
        source = sum(cnf_satisfied(formula, x) for x in range(8))
        extension = sum(prod(sum(literal(lit, x) for lit in clause)
                             for clause in formula) for x in range(8))
        assert bool(source) == bool(extension)
        n, binary, affine = mixed_compile(formula, 3)
        assert cnf_satisfied(binary, 0)
        affine_model = sum(1 << (3 + 3*i) for i in range(len(formula)))
        assert all((row & affine_model).bit_count() % 2 for row in affine)
        if len(formula) <= 3:
            actual = sum(mixed_satisfied(binary, affine, x) for x in range(1 << n))
            assert actual == extension
            result['full_mixed_enumerations'] += 1
            result['full_mixed_words'] += 1 << n
        # Always-SAT G(F,z) = AND_C (z OR C). Full forced-bit acquisition
        # detects original UNSAT, unlike a free polynomial local closure.
        allowed_z = {z for z in (0, 1) for x in range(8)
                     if all(z or any(literal(lit, x) for lit in c) for c in formula)}
        assert 1 in allowed_z
        assert (allowed_z == {1}) == (source == 0)
        result['known_sat_wrapper_checks'] += 1
        result['forced_switches'] += allowed_z == {1}
        result['formulas'] += 1
        result['source_sat' if source else 'source_unsat'] += 1
        source_counts.append(source)
        extension_counts.append(extension)
    neighbors = [255 ^ (1 << i) for i in range(8)]
    assert source_counts[255] == extension_counts[255] == 0
    assert [source_counts[i] for i in neighbors] == [1]*8
    assert [extension_counts[i] for i in neighbors] == [24]*8
    result['cube_source_neighbor_models'] = [source_counts[i] for i in neighbors]
    result['cube_mixed_neighbor_models'] = [extension_counts[i] for i in neighbors]
    return result


def reserve_affine_compile(clauses):
    """Seven satisfying local truth rows per clause, one global weight cap."""
    observations, equations = {}, []
    m = len(clauses)
    for i, clause in enumerate(clauses):
        equations.append((127 << (7*i), 1))
        for j, lit in enumerate(clause):
            observed = sum(1 << (7*i+a-1) for a in range(1, 8) if a >> j & 1)
            variable, sign = abs(lit)-1, int(lit < 0)
            if variable in observations:
                old, old_sign = observations[variable]
                equations.append((old ^ observed, old_sign ^ sign))
            else:
                observations[variable] = observed, sign
    if m % 2:
        equations.append((1 << (7*m), 1))
    return 7*m + m % 2, m + m % 2, equations, observations


def reserve_source_controls():
    clauses = [tuple((i+1) if signs >> i & 1 else -(i+1) for i in range(3))
               for signs in range(8)]
    formulas = [[clauses[i] for i in range(8) if mask >> i & 1]
                for mask in range(256) if mask.bit_count() <= 2]
    formulas += [[(1, 1, 1), (-1, -1, -1)], [(1, 1, -1)]]
    result = dict(formulas=0, sat=0, unsat=0, enumerated_words=0, lifted_witnesses=0)
    for formula in formulas:
        expected = any(cnf_satisfied(formula, x) for x in range(8))
        width, cap, eq, obs = reserve_affine_compile(formula)
        found = None
        # Exhaust all Boolean variables of the affine encoding in these small cases.
        for word in range(1 << width):
            result['enumerated_words'] += 1
            if word.bit_count() > cap or word.bit_count() % 2:
                continue
            if any(((a & word).bit_count() & 1) != b for a, b in eq):
                continue
            assert all(((word >> (7*i)) & 127).bit_count() == 1
                       for i in range(len(formula)))
            original = sum((((a & word).bit_count() & 1) ^ sign) << variable
                           for variable, (a, sign) in obs.items())
            assert cnf_satisfied(formula, original)
            found = word
            result['lifted_witnesses'] += 1
        assert (found is not None) == expected
        result['formulas'] += 1
        result['sat' if expected else 'unsat'] += 1
    return result


def star_controls():
    local_checks = 0
    for u, v in it.product(range(4), repeat=2):
        options = [w for w in range(4)
                   if all((u ^ w) != s for s in (1, 2, 3)) and (v ^ w) != 0]
        assert len(options) == int(u != v)
        local_checks += 1
    edges = list(it.combinations(range(5), 2))
    all_models, star_models = [], []
    for omit in [None] + list(range(len(edges))):
        active = [e for i, e in enumerate(edges) if i != omit]
        direct, compiled = 0, 0
        for x in it.product(range(4), repeat=5):
            direct += all(x[u] != x[v] for u, v in active)
            compiled += all(any(all((x[u] ^ w) != s for s in (1, 2, 3))
                                    and (x[v] ^ w) != 0 for w in range(4))
                            for u, v in active)
        assert direct == compiled
        all_models.append(direct)
        star_models.append(compiled)
    assert all_models == [0] + [24]*10
    return dict(local_endpoint_checks=local_checks, graph_controls=11,
                central_assignments=11*4**5,
                original_models=all_models, compiled_models=star_models)


def determinant(matrix):
    from fractions import Fraction
    a = [[Fraction(x) for x in row] for row in matrix]
    result = Fraction(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return 0
        if pivot != j:
            a[pivot], a[j] = a[j], a[pivot]
            result = -result
        value = a[j][j]
        result *= value
        for k in range(j, len(a)):
            a[j][k] /= value
        for i in range(j+1, len(a)):
            scale = a[i][j]
            for k in range(j, len(a)):
                a[i][k] -= scale*a[j][k]
    assert result.denominator == 1
    return int(result)


def modular_and_mask_controls():
    triples = [(0, 5, 6), (1, 2, 5), (0, 1, 2),
               (2, 3, 6), (3, 4, 5), (4, 5, 6)]
    counts = []
    for omit in [None] + list(range(6)):
        active = [row for i, row in enumerate(triples) if i != omit]
        counts.append(sum(all(sum((x >> j) & 1 for j in row) == 1
                              for row in active) for x in range(128)))
    assert counts == [0, 1, 1, 1, 2, 1, 1]
    integer = [0, 2, -1, 1, 0, 0, 1]
    assert all(sum(integer[j] for j in row) == 1 for row in triples)
    columns = [0, 1, 2, 3, 4, 6]
    det = determinant([[int(j in row) for j in columns] for row in triples])
    assert det == 1
    from fractions import Fraction
    assert all(sum(Fraction(1, 3) for _ in row) == 1 for row in triples)
    a = b = {0, 1, 2}
    full = {x ^ y for x in a for y in b}
    pinned = {0 ^ y for y in b}
    assert full == {0, 1, 2, 3} and 3 not in pinned
    parity_support = {linear: sorted({(linear & x).bit_count() % 2 for x in a})
                      for linear in (1, 2, 3)}
    assert all(values == [0, 1] for values in parity_support.values())
    assert gf2_rank(a) == 2 and 3 not in a
    return dict(exact_one_models=counts, integer_witness=integer,
                unimodular_minor=det, fractional_witness='all coordinates 1/3',
                unpinned_sumset=sorted(full), pinned_sumset=sorted(pinned),
                three_row_all_linear_parities=parity_support,
                three_row_missing_joint_target=3)


def potential_controls():
    checks = []
    for c in (1, 2, 3, 4, 8):
        n = 4*c + 1
        assert 2*(n-1)**c > n**c
        checks.append(dict(c=c, n=n, child_sum=2*(n-1)**c, parent=n**c))
    volumes = []
    for n in (2, 4, 8, 16, 32, 64, 128):
        p = 1 << n
        credit = 2*p-1
        assert 2*(2*(p//2)-1) == credit-1
        volumes.append(dict(binary_types=n, volume=str(p), credit_bits=credit.bit_length()))
    return dict(raw_size_potential_falsifiers=checks, count_box_volumes=volumes)


def tagged_image(columns, word):
    value = 0
    for i, column in enumerate(columns):
        if word >> i & 1:
            value ^= column
    return value


def joint_probe_margin_controls():
    """M10 -> joint probes. Exhaustive references, not a polynomial backend."""
    checks, lifts, affine_words = 0, 0, 0
    scales = []
    for k in (8, 10, 12):
        columns, net = list(range(k)), k - 2
        assert len(set(columns)) == k  # actual distinct tag classes
        buckets = {}
        forbidden = []
        for word in range(1 << k):
            if word.bit_count() % 2 != net % 2:
                continue
            buckets.setdefault(tagged_image(columns, word), []).append(word)
            if word.bit_count() > net or word.bit_count() > 2*k-net:
                forbidden.append(word)
        assert forbidden == [(1 << k)-1]
        sizes = {len(a) for a in buckets.values()}
        assert len(sizes) == 1 and next(iter(sizes)) > 4*len(forbidden)
        affine_words += sum(map(len, buckets.values()))
        for target, affine in sorted(buckets.items()):
            for i, j in it.combinations(range(k), 2):
                for value in range(4):
                    fiber = [p for p in affine
                             if (((p >> i) & 1) | (((p >> j) & 1) << 1)) == value]
                    actual = [p for p in fiber if p not in forbidden]
                    assert bool(fiber) == bool(actual)
                    checks += 1
                    if not actual:
                        continue
                    p = actual[0]
                    totals = [(p >> a) & 1 for a in range(k)]
                    remaining = net-sum(totals)
                    for a in range(k):
                        extra = min(remaining, 2-totals[a]) // 2 * 2
                        totals[a] += extra
                        remaining -= extra
                    assert remaining == 0 and sum(totals) == net
                    assert all(0 <= y <= 2 and y % 2 == (p >> a) & 1
                               for a, y in enumerate(totals))
                    # Two original unit arcs per class, actual reconstructed values.
                    arcs = [int(jj < y) for y in totals for jj in (0, 1)]
                    assert sum(arcs) == net
                    assert tagged_image([g for g in columns for _ in (0, 1)],
                                        sum(v << a for a, v in enumerate(arcs))) == target
                    lifts += 1
        scales.append(dict(classes=k, affine_cosets=len(buckets),
                           coset_size=next(iter(sizes)), ambient_bad_bound=1))
    # Infinite-pattern countercontrol at r=4: distinct full tag columns enforce
    # each block of r parity bits to be constant. k=2r, widths=2, net=2r-2.
    # For any even r>=4, feasible patterns are 00, 10, 01; 11 is missing.
    r = 4
    columns = [(1 << (r-1))-1] + [1 << j for j in range(r-1)]
    columns += [g << (r-1) for g in columns]
    k, net = 2*r, 2*r-2
    assert len(set(columns)) == k
    affine = [p for p in range(1 << k) if tagged_image(columns, p) == 0
              and p.bit_count() % 2 == net % 2]
    actual = [p for p in affine if p.bit_count() <= net]
    assert affine == [0, 15, 240, 255] and actual == [0, 15, 240]
    scalar_checks = 0
    for row in range(1 << k):
        assert {(row & p).bit_count() % 2 for p in actual} == {
            (row & p).bit_count() % 2 for p in affine}
        scalar_checks += 1
    joint = {((p & 1), ((p >> r) & 1)) for p in actual}
    assert joint == {(0, 0), (1, 0), (0, 1)}
    return dict(two_bit_queries=checks, verified_original_arc_lifts=lifts,
                reference_affine_words=affine_words, positive_scales=scales,
                sharp_margin_counterexample=dict(classes=k, tag_columns=columns,
                    required_net=net, affine_words=affine, actual_words=actual,
                    M=4, B=1, scalar_probes=scalar_checks,
                    missing_joint_target=[1, 1],
                    note='Refutes single-parity-to-joint inference; exact thin M10 terminal can still decide it'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--prior-reserve-results', type=Path)
    args = parser.parse_args()
    result = {
        'audit': 'CA01',
        'scope': 'Independent finite checks; no universal polynomial-time claim',
        'reserve': reserve_controls(),
        'composition': composition_controls(),
        'reserve_source_compiler': reserve_source_controls(),
        'regional_star': star_controls(),
        'modular_and_mask': modular_and_mask_controls(),
        'potentials': potential_controls(),
        'joint_probe_margin': joint_probe_margin_controls(),
    }
    if args.prior_reserve_results:
        prior = json.loads(args.prior_reserve_results.read_text())
        keys = ('seed', 'reserve_graphs', 'reserve_masks', 'saturation_true', 'saturation_false')
        assert all(prior[k] == result['reserve'][k] for k in keys)
        result['prior_reserve_summary_match'] = list(keys)
    result['assertions_failed'] = 0
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
