#!/usr/bin/env python3
"""Exhaustive audit for minimum auxiliary pure-sign equality blocks.

No randomness.  A source port uses one signed occurrence.  The gadget must
complete every port and every fresh auxiliary to exact (2 positive, 2
negative) degree using unique proper pure-sign ternary clauses.  Projection
onto ports is existential over auxiliaries.
"""

from itertools import combinations, product
import json


def triples(n):
    return [sum(1 << i for i in c) for c in combinations(range(n), 3)]


def quota_families(n, target):
    clauses = triples(n)
    count = sum(target) // 3
    out = []

    def visit(start, left, degree, chosen):
        if left == 0:
            if not any(degree):
                out.append(tuple(clauses[i] for i in chosen))
            return
        if sum(degree) != 3 * left:
            return
        for i in range(start, len(clauses)):
            edge = clauses[i]
            vertices = [v for v in range(n) if edge >> v & 1]
            if all(degree[v] for v in vertices):
                nxt = list(degree)
                for v in vertices:
                    nxt[v] -= 1
                visit(i + 1, left - 1, nxt, chosen + [i])

    visit(0, count, list(target), [])
    return out


def satisfies(word, positives, negatives):
    return all(word & c for c in positives) and all(word & c != c for c in negatives)


def projection(r, a, positives, negatives):
    relation = set()
    for ports in range(1 << r):
        for aux in range(1 << a):
            if satisfies(ports | (aux << r), positives, negatives):
                relation.add(ports)
                break
    return relation


def audit_case(r, a, signs):
    n = r + a
    positive_degree = [2 - s for s in signs] + [2] * a
    negative_degree = [1 + s for s in signs] + [2] * a
    positive_slots = sum(positive_degree)
    negative_slots = sum(negative_degree)
    admissible = (positive_slots % 3 == 0 and negative_slots % 3 == 0)
    row = {
        "r": r,
        "a": a,
        "port_signs": "".join(map(str, signs)),
        "positive_ports": sum(signs),
        "positive_slots": positive_slots,
        "negative_slots": negative_slots,
        "syntactically_admissible": admissible,
        "positive_families": 0,
        "negative_families": 0,
        "formula_pairs": 0,
        "pairs_admitting_both_constant_port_words": 0,
        "minimum_projected_models_with_both_constants": None,
        "equality_gadgets": 0,
    }
    if not admissible:
        return row
    positives = quota_families(n, positive_degree)
    negatives = quota_families(n, negative_degree)
    row["positive_families"] = len(positives)
    row["negative_families"] = len(negatives)
    equality = {0, (1 << r) - 1}
    minimum = None
    both = hits = pairs = 0
    for pf in positives:
        for nf in negatives:
            pairs += 1
            rel = projection(r, a, pf, nf)
            if equality <= rel:
                both += 1
                minimum = len(rel) if minimum is None else min(minimum, len(rel))
            if rel == equality:
                hits += 1
    row["formula_pairs"] = pairs
    row["pairs_admitting_both_constant_port_words"] = both
    row["minimum_projected_models_with_both_constants"] = minimum
    row["equality_gadgets"] = hits
    return row


def congruence_audit():
    checked = 0
    failures = []
    for r in range(1, 21):
        for a in range(0, 13):
            for p in range(r + 1):
                total_ok = (3 * r + 4 * a) % 3 == 0
                sign_ok = (2 * (r + a) - p) % 3 == 0
                predicted = (a % 3 == 0 and (p - 2 * r) % 3 == 0)
                observed = total_ok and sign_ok
                checked += 1
                if observed != predicted:
                    failures.append([r, a, p, observed, predicted])
    return {"triples_checked": checked, "failures": failures}


def main():
    cases = []
    for r in (3, 4):
        for signs in product((0, 1), repeat=r):
            cases.append(audit_case(r, 3, signs))
    out = {
        "run_id": "M22-AUX-PORT-CONGRUENCE148",
        "status": "COMPUTATIONAL finite exhaustive; symbolic congruence proved separately",
        "random_seed": None,
        "congruence_sanity": congruence_audit(),
        "cases": cases,
        "summary": {
            "formula_pairs_exhausted": sum(x["formula_pairs"] for x in cases),
            "equality_gadgets": sum(x["equality_gadgets"] for x in cases),
            "r3_admissible_sign_patterns": [x["port_signs"] for x in cases if x["r"] == 3 and x["syntactically_admissible"]],
            "r4_admissible_sign_patterns": [x["port_signs"] for x in cases if x["r"] == 4 and x["syntactically_admissible"]],
        },
    }
    assert not out["congruence_sanity"]["failures"]
    assert out["summary"]["formula_pairs_exhausted"] == 196650
    assert out["summary"]["equality_gadgets"] == 0
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
