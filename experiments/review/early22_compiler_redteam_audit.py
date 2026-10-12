#!/usr/bin/env python3
"""Bounded audit of the EARLY22 exact-(2,2) compiler and separate controls."""

from __future__ import annotations

import itertools
import json
import random
from collections import Counter
from pathlib import Path


W1 = [
    (-1, 3, -14), (2, -8, 9), (10, -13, 14), (3, 7, -13),
    (-4, -9, -11), (5, 8, -14), (4, -8, -11), (1, 7, 13),
    (1, -7, 10), (-5, -6, -15), (-2, -6, 12), (-4, 9, -10),
    (-2, 5, -12), (-3, 6, -15), (6, -7, 11), (2, -9, 11),
    (4, 8, -10), (-3, 12, 15), (-5, -12, 15), (-1, 13, 14),
]
C0 = 7
PORTS = (1, 7, 13)


def sat_clause(clause, assignment):
    return any(assignment[abs(lit)] == (lit > 0) for lit in clause)


def models(clauses, variables):
    out = []
    for bits in itertools.product((False, True), repeat=len(variables)):
        a = dict(zip(variables, bits))
        if all(sat_clause(c, a) for c in clauses):
            out.append(a)
    return out


def proper(clauses):
    return all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in clauses)


def signed_occurrences(clauses, n):
    pos = Counter()
    neg = Counter()
    for clause in clauses:
        for lit in clause:
            (pos if lit > 0 else neg)[abs(lit)] += 1
    return [(pos[i], neg[i]) for i in range(1, n + 1)]


def simplify(clauses, partial):
    result = []
    for clause in clauses:
        reduced = []
        satisfied = False
        for lit in clause:
            var = abs(lit)
            if var in partial:
                if partial[var] == (lit > 0):
                    satisfied = True
                    break
            else:
                reduced.append(lit)
        if satisfied:
            continue
        if not reduced:
            return None
        result.append(tuple(reduced))
    return result


def dpll(clauses, partial=None):
    assignment = {} if partial is None else dict(partial)
    clauses = simplify(clauses, assignment)
    if clauses is None:
        return None
    while True:
        units = [c[0] for c in clauses if len(c) == 1]
        if not units:
            break
        changed = False
        for lit in units:
            v, value = abs(lit), lit > 0
            if v in assignment and assignment[v] != value:
                return None
            if v not in assignment:
                assignment[v] = value
                changed = True
        if not changed:
            break
        clauses = simplify(clauses, assignment)
        if clauses is None:
            return None
    if not clauses:
        return assignment
    lit = min((x for c in clauses for x in c), key=lambda x: abs(x))
    v = abs(lit)
    for value in (False, True):
        trial = dpll(clauses, {**assignment, v: value})
        if trial is not None:
            return trial
    return None


def clause_falsifying_bits(clause):
    return {abs(lit): lit < 0 for lit in clause}


def k4_source():
    vertices = range(4)
    edges = [(u, v) for u in vertices for v in vertices if u < v]
    edge_id = {e: i + 1 for i, e in enumerate(edges)}
    charge = {0: 1, 1: 0, 2: 0, 3: 0}
    clauses = []
    meta = []
    for v in vertices:
        inc = sorted(e for e in edges if v in e)
        for bits in itertools.product((0, 1), repeat=3):
            if (sum(bits) % 2) == charge[v]:
                continue
            clause = tuple(edge_id[e] if bit == 0 else -edge_id[e]
                           for e, bit in zip(inc, bits))
            clauses.append(clause)
            meta.append((v, inc, dict(zip(inc, bits))))
    return edges, edge_id, clauses, meta


def compile_k4():
    edges, edge_id, source, meta = k4_source()
    clone = {}
    next_var = 1
    for e in edges:
        for endpoint in e:
            for kind in ("a", "b"):
                clone[(e, endpoint, kind)] = next_var
                next_var += 1

    transformed = []
    for clause, (v, inc, bad) in zip(source, meta):
        local = []
        for e in inc:
            j = inc.index(e)
            y = inc[(j + 1) % 3]
            kind = "a" if bad[y] == 0 else "b"
            cv = clone[(e, v, kind)]
            local.append(cv if bad[e] == 0 else -cv)
        transformed.append(tuple(local))

    implications = []
    for e in edges:
        u, v = e
        cyc = [clone[(e, u, "a")], clone[(e, u, "b")],
               clone[(e, v, "a")], clone[(e, v, "b")]]
        implications.extend([(-cyc[i], cyc[(i + 1) % 4]) for i in range(4)])

    full = list(transformed)
    padded_indices = []
    internal_indices = []
    q_offsets = []
    for group in range(8):
        offset = next_var - 1
        q_offsets.append(offset)
        next_var += 15
        for k in range(3):
            imp_index = 3 * group + k
            p = offset + PORTS[k]
            padded_indices.append(len(full))
            full.append(tuple(implications[imp_index]) + (p,))
        for idx, clause in enumerate(W1):
            if idx == C0:
                continue
            internal_indices.append((len(full), group, idx))
            full.append(tuple((offset + abs(l)) if l > 0 else -(offset + abs(l))
                              for l in clause))
    return {
        "edges": edges,
        "edge_id": edge_id,
        "source": source,
        "transformed": transformed,
        "implications": implications,
        "clone": clone,
        "full": full,
        "padded_indices": padded_indices,
        "internal_indices": internal_indices,
        "q_offsets": q_offsets,
        "nvars": next_var - 1,
    }


def assignment_satisfies(clauses, assignment, skip=None):
    return all(i == skip or sat_clause(c, assignment) for i, c in enumerate(clauses))


def gf2_rank(rows, ncols):
    rows = list(rows)
    rank = 0
    pivots = []
    for col in range(ncols):
        pivot = next((i for i in range(rank, len(rows)) if (rows[i] >> col) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and ((rows[i] >> col) & 1):
                rows[i] ^= rows[rank]
        pivots.append(col)
        rank += 1
    return rank, rows[:rank], pivots


def nullspace_basis(rows, ncols):
    rank, reduced, pivots = gf2_rank(rows, ncols)
    pivot_set = set(pivots)
    basis = []
    for free in range(ncols):
        if free in pivot_set:
            continue
        x = 1 << free
        for row, pivot in reversed(list(zip(reduced, pivots))):
            if ((row & x).bit_count() & 1):
                x |= 1 << pivot
        basis.append(x)
    return rank, basis


def substitution_audit(data):
    source_images = []
    tautologies = 0
    constants_true = 0
    clone_to_source = {}
    for (edge, _endpoint, _kind), cv in data["clone"].items():
        clone_to_source[cv] = data["edge_id"][edge]
    for i, clause in enumerate(data["full"]):
        image = []
        true = False
        for lit in clause:
            v = abs(lit)
            if v <= 24:
                mapped = clone_to_source[v]
                image.append(mapped if lit > 0 else -mapped)
            elif lit < 0:
                true = True
        if true:
            constants_true += 1
        elif any(-x in image for x in image):
            tautologies += 1
        else:
            source_images.append(tuple(image))
    return {
        "source_images": len(source_images),
        "source_image_multiset_matches": Counter(source_images) == Counter(data["source"]),
        "tautological_images": tautologies,
        "constant_true_images": constants_true,
    }


def deletion_audit(data, w1_deletion_models):
    source_models = models(data["source"], list(range(1, 7)))
    assert not source_models
    source_delete = []
    for i in range(len(data["source"])):
        ms = models(data["source"][:i] + data["source"][i + 1:], list(range(1, 7)))
        assert ms
        source_delete.append(ms[0])

    skeleton = list(data["transformed"]) + list(data["implications"])
    assert dpll(skeleton) is None
    implication_delete = []
    for j in range(24):
        witness = dpll(skeleton[:16 + j] + skeleton[17 + j:])
        assert witness is not None
        implication_delete.append(witness)

    full = data["full"]
    clone = data["clone"]
    verified = {"source": 0, "padded": 0, "internal_q": 0}

    for i, src_wit in enumerate(source_delete):
        a = {}
        for (edge, _endpoint, _kind), cv in clone.items():
            a[cv] = src_wit[data["edge_id"][edge]]
        for off in data["q_offsets"]:
            a.update({off + q: False for q in range(1, 16)})
        assert assignment_satisfies(full, a, skip=i)
        verified["source"] += 1

    for j, target_idx in enumerate(data["padded_indices"]):
        a = {v: implication_delete[j].get(v, False) for v in range(1, 25)}
        for off in data["q_offsets"]:
            a.update({off + q: False for q in range(1, 16)})
        assert assignment_satisfies(full, a, skip=target_idx)
        verified["padded"] += 1

    for target_idx, group, w1_idx in data["internal_indices"]:
        qwit = w1_deletion_models[w1_idx]
        true_ports = [p for p in PORTS if qwit[p]]
        assert true_ports
        port = true_ports[0]
        local_k = PORTS.index(port)
        implication_index = 3 * group + local_k
        a = {v: implication_delete[implication_index].get(v, False) for v in range(1, 25)}
        for g, off in enumerate(data["q_offsets"]):
            if g == group:
                a.update({off + q: qwit[q] for q in range(1, 16)})
            else:
                a.update({off + q: False for q in range(1, 16)})
        assert assignment_satisfies(full, a, skip=target_idx)
        verified["internal_q"] += 1
    return verified


def zero_boundary(data):
    supports = [(tuple(sorted(abs(x) for x in c)),
                 sum(1 for x in c if x < 0) & 1) for c in data["full"]]
    rows = []
    for v in range(1, data["nvars"] + 1):
        mask = 0
        for i, clause in enumerate(data["full"]):
            if any(abs(x) == v for x in clause):
                mask |= 1 << i
        rows.append(mask)
    rank, basis = nullspace_basis(rows, len(data["full"]))
    rng = random.Random(20261013)
    weight96 = None
    vector = 0
    for _ in range(10000):
        vector = 0
        for b in basis:
            if rng.getrandbits(1):
                vector ^= b
        if vector.bit_count() == 96:
            weight96 = vector
            break
    even = weight96 is not None and all((row & weight96).bit_count() % 2 == 0 for row in rows)
    return {
        "support_parity_blocks": len(set(supports)),
        "all_singleton": len(set(supports)) == len(supports),
        "unsigned_supports_distinct": len({s for s, _ in supports}) == len(supports),
        "incidence_rank": rank,
        "kernel_dimension": len(basis),
        "weight_96_kernel_word_found": weight96 is not None,
        "weight_96_even_boundary_verified": even,
    }


def monotone_control():
    triples = list(itertools.combinations(range(6), 3))
    halves = []
    for cs in itertools.combinations(triples, 4):
        deg = Counter(v for c in cs for v in c)
        if all(deg[v] == 2 for v in range(6)):
            halves.append(cs)
    histogram = Counter()
    equivalence_checks = 0
    for pos in halves:
        for neg in halves:
            count = 0
            for bits in itertools.product((False, True), repeat=6):
                formula = all(any(bits[v] for v in c) for c in pos) and \
                          all(any(not bits[v] for v in c) for c in neg)
                t_covers_pos = all(any(bits[v] for v in c) for c in pos)
                comp_covers_neg = all(any(not bits[v] for v in c) for c in neg)
                assert formula == (t_covers_pos and comp_covers_neg)
                equivalence_checks += 1
                count += int(formula)
            histogram[count] += 1
    return {
        "halves": len(halves),
        "ordered_pairs": len(halves) ** 2,
        "model_histogram": {str(k): histogram[k] for k in sorted(histogram)},
        "all_pairs_satisfiable": 0 not in histogram,
        "assignment_equivalence_checks": equivalence_checks,
    }


def affine_control(data):
    counts = []
    affine = []
    for i in range(len(data["source"])):
        ms = models(data["source"][:i] + data["source"][i + 1:], list(range(1, 7)))
        bitsets = {sum((int(a[v]) << (v - 1)) for v in range(1, 7)) for a in ms}
        counts.append(len(bitsets))
        base = next(iter(bitsets))
        diffs = {x ^ base for x in bitsets}
        affine.append(all((x ^ y) in diffs for x in diffs for y in diffs))
    return {
        "punctures": len(counts),
        "model_counts": counts,
        "all_affine": all(affine),
        "scope": "source-clause punctures only",
    }


def main():
    assert proper(W1)
    assert signed_occurrences(W1, 15) == [(2, 2)] * 15
    assert not models(W1, list(range(1, 16)))
    q = W1[:C0] + W1[C0 + 1:]
    q_models = models(q, list(range(1, 16)))
    assert len(q_models) == 244
    assert all(not a[p] for a in q_models for p in PORTS)
    w1_deletion_models = {}
    for i in range(len(W1)):
        ms = models(W1[:i] + W1[i + 1:], list(range(1, 16)))
        assert ms
        w1_deletion_models[i] = ms[0]

    data = compile_k4()
    assert data["nvars"] == 144
    assert len(data["full"]) == 192
    assert proper(data["full"])
    assert len(set(data["full"])) == len(data["full"])
    assert signed_occurrences(data["full"], 144) == [(2, 2)] * 144

    result = {
        "status": "COMPUTATIONAL",
        "scope": "bounded K4 and n=6 monotone controls; no asymptotic inference",
        "w1_q": {
            "w1_variables": 15,
            "w1_clauses": 20,
            "w1_unsat": True,
            "w1_all_20_deletions_sat": True,
            "q_clauses": len(q),
            "q_models": len(q_models),
            "ports_forced_false": list(PORTS),
            "q_occurrences_ports": [signed_occurrences(q, 15)[p - 1] for p in PORTS],
            "q_occurrences_nonports": sorted(set(signed_occurrences(q, 15)[i]
                                                      for i in range(15) if i + 1 not in PORTS)),
        },
        "compiled_k4": {
            "variables": data["nvars"],
            "clauses": len(data["full"]),
            "proper": proper(data["full"]),
            "distinct_clauses": len(set(data["full"])) == len(data["full"]),
            "exact_signed_2_2": signed_occurrences(data["full"], 144) == [(2, 2)] * 144,
            "substitution": substitution_audit(data),
            "deletion_witnesses": deletion_audit(data, w1_deletion_models),
            "zero_boundary": zero_boundary(data),
        },
        "affine_continuation_control": affine_control(data),
        "monotone_cubic_pair_control": monotone_control(),
    }
    out = Path("results/raw/review/2026-10-13_early22_compiler_redteam.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
