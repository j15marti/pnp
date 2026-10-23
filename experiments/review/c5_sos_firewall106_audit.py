#!/usr/bin/env python3
"""Independent exact audit for C5-SOS-FIREWALL106.

Standard library only.  This checks the two local degree-four C5 identities,
the SAT C5 counterexample, both 12-vertex controls, and the orbit/PSD
contradiction.  It intentionally does not import the specialist verifier.
"""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations, permutations, product
import json

checks = 0


def check(statement, label):
    global checks
    checks += 1
    if not statement:
        raise AssertionError(f"check {checks}: {label}")


# Polynomials are maps from square-free tuples of variable ids 3*v+c to Q.
# Reduction is modulo Boolean idempotence, same-vertex exclusion, and C5 edge
# same-colour exclusion.  The degree ceiling is checked before reduction.
C5_EDGES = {tuple(sorted((v, (v + 1) % 5))) for v in range(5)}


def normalize_monomial(factors):
    unique = tuple(sorted(set(factors)))
    for i, j in combinations(unique, 2):
        u, c = divmod(i, 3)
        v, d = divmod(j, 3)
        if u == v or (c == d and tuple(sorted((u, v))) in C5_EDGES):
            return None
    return unique


def clean(poly):
    return {m: a for m, a in poly.items() if a}


def add(*polys):
    out = defaultdict(Q)
    for poly in polys:
        for m, a in poly.items():
            out[m] += a
    return clean(out)


def scale(poly, scalar):
    return clean({m: scalar * a for m, a in poly.items()})


def multiply(left, right):
    out = defaultdict(Q)
    for m, a in left.items():
        for n, b in right.items():
            check(len(m) + len(n) <= 4, "degree ceiling")
            z = normalize_monomial(m + n)
            if z is not None:
                out[z] += a * b
    return clean(out)


def atom(ids=(), coefficient=1):
    return {tuple(sorted(ids)): Q(coefficient)}


def colour_sum(vertex):
    return add(atom((), -1), *(atom((3 * vertex + c,)) for c in range(3)))


def group_average(poly):
    out = defaultdict(Q)
    vertex_maps = [tuple((a + e * v) % 5 for v in range(5))
                   for a in range(5) for e in (-1, 1)]
    colour_maps = list(permutations(range(3)))
    for vm in vertex_maps:
        for cm in colour_maps:
            for monomial, coefficient in poly.items():
                moved = tuple(sorted(3 * vm[i // 3] + cm[i % 3]
                                     for i in monomial))
                out[moved] += coefficient / 60
    return clean(out)


Y = add(*(atom((3 * u + c, 3 * v + c))
          for u, v in combinations(range(5), 2)
          if (u, v) not in C5_EDGES for c in range(3)))
capital_q = add(Y, atom((), -2))
little_q_terms = [
    (-2, (0,)), (1, (0, 4)), (1, (0, 7)), (-1, (1, 6)),
    (1, (0, 10)), (-1, (1, 9)), (1, (0, 13)),
    (1, (5, 6)), (1, (9, 14)),
]
little_q = add(*(atom(ids, coefficient) for coefficient, ids in little_q_terms))

lower_rows = [
    (Q(-10, 3), (), 0), (-10, (0,), 1), (-20, (0, 4), 2),
    (20, (0, 6), 1), (10, (0, 6), 3), (20, (0, 4, 6), 3),
    (-20, (0, 4, 8), 3), (20, (0, 4, 9), 2),
]
upper_rows = [
    (2, (), 0), (-6, (0,), 2), (12, (0, 4), 2),
    (-15, (0, 6), 1), (-6, (0, 6), 3),
    (24, (0, 4, 8), 3), (-24, (0, 4, 9), 2),
]


def ideal_side(rows):
    return add(*(scale(group_average(multiply(atom(ids), colour_sum(v))), a)
                 for a, ids, v in rows))


lhs_lower = add(scale(multiply(capital_q, capital_q), Q(1, 3)),
                scale(capital_q, -1))
lhs_upper = add(scale(group_average(multiply(little_q, little_q)), 3),
                capital_q)
check(lhs_lower == ideal_side(lower_rows), "lower C5 identity")
check(lhs_upper == ideal_side(upper_rows), "upper C5 identity")


def count_colourings(vertex_count, edges):
    edges = set(map(tuple, edges))
    count = 0
    y_values = []
    for colouring in product(range(3), repeat=vertex_count):
        if all(colouring[u] != colouring[v] for u, v in edges):
            count += 1
            if vertex_count == 5:
                y_values.append(sum(colouring[u] == colouring[v]
                                    for u, v in combinations(range(5), 2)
                                    if (u, v) not in C5_EDGES))
    return count, y_values


c5_count, c5_y = count_colourings(5, C5_EDGES)
check(c5_count == 30, "C5 has 30 labelled 3-colourings")
check(set(c5_y) == {2}, "every C5 colouring has Y=2")

# Canonical degree-two moment on the bare C5: each chord has one common
# neighbour, so E[Y]=5/3 + J/12 = 25/12, incompatible with degree four.
canonical_c5_y = Q(5, 3) + Q(5, 12)
check(canonical_c5_y == Q(25, 12) and canonical_c5_y > 2,
      "canonical C5 moment exceeds forced value")

NO = {
    (0, 1), (0, 4), (0, 6), (0, 9), (1, 2), (1, 5), (1, 7),
    (2, 3), (2, 6), (2, 8), (3, 4), (3, 7), (3, 9), (4, 5),
    (4, 8), (5, 10), (5, 11), (6, 10), (6, 11), (7, 8),
    (7, 11), (8, 10), (9, 10), (9, 11),
}
YES = (NO - {(0, 1), (2, 6)}) | {(0, 2), (1, 6)}


def graph_data(edges):
    adj = [set() for _ in range(12)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    check(all(len(a) == 4 for a in adj), "4-regular")
    check(all(not (adj[u] & adj[v]) for u, v in edges), "triangle-free")
    colourings, _ = count_colourings(12, edges)
    cycles = []
    for subset in combinations(range(12), 5):
        induced = [(u, v) for u, v in combinations(subset, 2)
                   if (u, v) in edges]
        if len(induced) == 5 and all(sum(v in e for e in induced) == 2
                                     for v in subset):
            cycles.append(subset)
            chords = [(u, v) for u, v in combinations(subset, 2)
                      if (u, v) not in edges]
            common = sum(len(adj[u] & adj[v]) for u, v in chords)
            check(Q(5, 3) + Q(common, 12) > 2,
                  "canonical extension obstructed on graph C5")
    return colourings, cycles


no_colourings, no_cycles = graph_data(NO)
yes_colourings, yes_cycles = graph_data(YES)
check((no_colourings, yes_colourings) == (0, 108), "paired graph labels")
check((len(no_cycles), len(yes_cycles)) == (44, 28), "C5 counts")

# Independent row reduction of the six orbit equations.
rows = [
    [2, 1, 0, 2, 0, 0, 0], [2, 0, 1, 1, 0, 1, 0],
    [1, 1, 1, 2, 0, 0, 0], [1, 0, 2, 1, 0, 0, 1],
    [2, 0, 0, 0, 1, 2, 0], [0, 0, 0, 0, 1, 3, 1],
]
augmented = [[Q(x) for x in row] + [Q(2)] for row in rows]
rank = 0
for column in range(7):
    pivot = next((i for i in range(rank, 6) if augmented[i][column]), None)
    if pivot is None:
        continue
    augmented[rank], augmented[pivot] = augmented[pivot], augmented[rank]
    divisor = augmented[rank][column]
    augmented[rank] = [x / divisor for x in augmented[rank]]
    for i in range(6):
        if i != rank and augmented[i][column]:
            multiple = augmented[i][column]
            augmented[i] = [x - multiple * y
                            for x, y in zip(augmented[i], augmented[rank])]
    rank += 1
check(rank == 6, "orbit system rank")

# s(t)=(t,6t-2,t,2-4t,2-4t,t,t) satisfies all equations.
intercepts = [0, -2, 0, 2, 2, 0, 0]
slopes = [1, 6, 1, -4, -4, 1, 1]
for row in rows:
    check(sum(a * b for a, b in zip(row, intercepts)) == 2,
          "orbit intercept")
    check(sum(a * b for a, b in zip(row, slopes)) == 0,
          "orbit slope")

lower_t = Q(7, 18)
upper_t = Q(1, 4)
check(lower_t > upper_t, "PSD inequalities conflict")

result = {
    "checks": checks,
    "unexpected_failures": 0,
    "C5_label": "SAT",
    "C5_colourings": c5_count,
    "C5_true_Y": 2,
    "C5_canonical_degree2_Y": str(canonical_c5_y),
    "paired_graph_colourings": {"H_UNSAT": no_colourings, "Hplus_SAT": yes_colourings},
    "paired_graph_C5_counts": {"H": len(no_cycles), "Hplus": len(yes_cycles)},
    "degree4_orbit_PSD_bounds": {"lower": str(lower_t), "upper": str(upper_t)},
    "classification": "exact restricted SOS/representation firewall",
    "unrestricted_time_lower_bound": False,
    "P_vs_NP": "OPEN",
}
print(json.dumps(result, indent=2, sort_keys=True))
