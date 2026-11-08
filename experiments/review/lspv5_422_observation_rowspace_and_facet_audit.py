#!/usr/bin/env python3
"""LSPV-5/422: exact facet-sign and GF(2) observation-rowspace audit."""

from itertools import product
import json


checks = 0


def ck(value, message):
    global checks
    checks += 1
    if not value:
        raise AssertionError(message)


def clause_value(clause, assignment):
    return any(assignment[abs(lit)] == (lit > 0) for lit in clause)


def resolve(pos, neg, pivot):
    ck(pivot in pos and -pivot in neg, "oriented pivot polarity")
    out = sorted(set([x for x in pos if x != pivot] + [x for x in neg if x != -pivot]))
    ck(not any(-x in out for x in out), "non-tautological resolvent")
    return out


def affine_truth(a0, a1, a2):
    return tuple(a0 ^ (a1 & u) ^ (a2 & v) for u, v in product((0, 1), repeat=2))


def polar_rank(table):
    def f(x):
        return table[(x >> 1, x & 1)]

    matrix = [[f(1 << (1 - i)) ^ f(1 << (1 - j)) ^ f((1 << (1 - i)) ^ (1 << (1 - j))) ^ f(0)
               for j in range(2)] for i in range(2)]
    rows = [row[0] | (row[1] << 1) for row in matrix]
    rank = 0
    for col in range(2):
        pivot = next((i for i in range(rank, 2) if (rows[i] >> col) & 1), None)
        if pivot is not None:
            rows[rank], rows[pivot] = rows[pivot], rows[rank]
            for i in range(2):
                if i != rank and ((rows[i] >> col) & 1):
                    rows[i] ^= rows[rank]
            rank += 1
    return rank


# Facet-sign referee for v = w OR t, e = w AND v.
w, t, v, e = 1, 2, 3, 4
or_facet = [-w, v]
bad_published_and_facet = [w, -v, e]
correct_and_facet = [-w, -v, e]
bad_models = []
for wv, tv in product((0, 1), repeat=2):
    vv, ev = wv | tv, wv & (wv | tv)
    assignment = {w: bool(wv), t: bool(tv), v: bool(vv), e: bool(ev)}
    ck(clause_value(or_facet, assignment), "OR facet valid")
    ck(clause_value(correct_and_facet, assignment), "correct AND facet valid")
    ck(ev == wv, "absorption identity")
    if not clause_value(bad_published_and_facet, assignment):
        bad_models.append({"w": wv, "t": tv, "v": vv, "e": ev})
ck(bad_models == [{"w": 0, "t": 1, "v": 1, "e": 0}], "unique bad-facet witness")
ck(resolve(or_facet, correct_and_facet, v) == [-w, e], "correct implication resolvent")
try:
    resolve(or_facet, bad_published_and_facet, v)
except AssertionError:
    bad_resolution_rejected = True
else:
    bad_resolution_rejected = False
ck(bad_resolution_rejected, "published-sign resolution rejected as tautological")

# Distinct nonlinear gates whose exported XOR is affine.
points = list(product((0, 1), repeat=2))
q1 = {(u, z): u & z for u, z in points}
q2 = {(u, z): u & (1 ^ z) for u, z in points}
exported = {p: q1[p] ^ q2[p] for p in points}
affines = {affine_truth(*a) for a in product((0, 1), repeat=3)}
q1_tuple = tuple(q1[p] for p in points)
q2_tuple = tuple(q2[p] for p in points)
exported_tuple = tuple(exported[p] for p in points)
ck(q1_tuple != q2_tuple, "gate coordinates distinct")
ck(q1_tuple not in affines and q2_tuple not in affines, "both gates nonlinear")
ck(exported_tuple == tuple(u for u, _ in points), "XOR export cancels quadratics")
ck(exported_tuple in affines, "export is affine")

rank_spectrum = {}
for mask in range(4):
    table = {p: ((mask & 1) and q1[p]) ^ (((mask >> 1) & 1) and q2[p]) for p in points}
    rank_spectrum[f"{mask:02b}"] = polar_rank(table)
ck(rank_spectrum == {"00": 0, "01": 2, "10": 2, "11": 0}, "full rank spectrum")

full_best = 0
for a in product((0, 1), repeat=6):
    matches = 0
    for u, z in points:
        p1 = a[0] ^ (a[1] & u) ^ (a[2] & z)
        p2 = a[3] ^ (a[4] & u) ^ (a[5] & z)
        matches += (p1, p2) == (q1[(u, z)], q2[(u, z)])
    full_best = max(full_best, matches)
export_best = max(sum((a0 ^ (a1 & u) ^ (a2 & z)) == exported[(u, z)] for u, z in points)
                  for a0, a1, a2 in product((0, 1), repeat=3))
ck(full_best == 3, "full two-output best affine agreement")
ck(export_best == 4, "observed output exact affine agreement")

# U(Q)=2^(n-m) sum_s 2^(-rank/2); for L=[1 1], im(L^T)={00,11}.
full_u = (2 ** (2 - 2)) * sum(2 ** (-r / 2) for r in rank_spectrum.values())
observed_u = (2 ** (2 - 1)) * sum(2 ** (-rank_spectrum[s] / 2) for s in ("00", "11"))
ck(full_u == 3 and observed_u == 4, "rowspace-restricted union-bound values")

result = {
    "status": "PASS",
    "scope": "finite exact facet and quadratic observation control; not historical R_mix341",
    "assertions": checks,
    "published_bad_facet_countermodel": bad_models[0],
    "correct_and_facet": correct_and_facet,
    "correct_resolvent": [-w, e],
    "distinct_nonlinear_outputs": [q1_tuple, q2_tuple],
    "exported_xor": exported_tuple,
    "polar_rank_spectrum": rank_spectrum,
    "full_best_affine_agreement": full_best,
    "export_best_affine_agreement": export_best,
    "full_union_bound": full_u,
    "observation_rowspace_union_bound": observed_u,
}
print(json.dumps(result, indent=2, sort_keys=True))
