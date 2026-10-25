#!/usr/bin/env python3
"""M22-NAE-PSD-CLIQUE150 peer-readable finite six-name exhaustive audit.
Only six-name exhaustive enumeration is claimed; analytic clique proof is in .tex.
"""
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

N = 6
TRIPLES = list(itertools.combinations(range(N), 3))


def degree_two_families():
    families = []
    for ix in itertools.combinations(range(len(TRIPLES)), 4):
        cs = tuple(TRIPLES[i] for i in ix)
        if all(sum(v in c for c in cs) == 2 for v in range(N)):
            families.append(cs)
    assert len(families) == 75
    return families


def sat_models(pos, neg):
    return [
        bits for bits in itertools.product((0, 1), repeat=N)
        if all(any(bits[v] for v in clause) for clause in pos)
        and all(any(not bits[v] for v in clause) for clause in neg)
    ]


def clique_number(pos, neg):
    edges = {p for clause in pos + neg
             for p in itertools.combinations(clause, 2)}
    for k in range(N, 1, -1):
        for group in itertools.combinations(range(N), k):
            if all(pair in edges for pair in itertools.combinations(group, 2)):
                return k, group
    return 1, (0,)


def from_strings(words):
    return tuple(tuple(int(s)-1 for s in word) for word in words)


def audit():
    six = [bits for bits in itertools.product((0, 1), repeat=3)
           if 0 < sum(bits) < 3]
    assert len(six) == 6
    spin = [tuple(2*b-1 for b in bits) for bits in six]
    for i in range(3):
        assert sum(row[i] for row in spin) == 0
    for i, j in itertools.combinations(range(3), 2):
        assert sum(row[i]*row[j] for row in spin) == -2
    families = degree_two_families()
    qhist, chist, cross, modelhist = Counter(), Counter(), Counter(), Counter()
    for pos in families:
        for neg in families:
            assert len(set(pos)) == 4 and len(set(neg)) == 4
            for group in (pos, neg):
                assert all(len(set(c)) == 3 for c in group)
                assert all(sum(v in c for c in group) == 2 for v in range(N))
            q = 4 - len(set(pos) & set(neg))
            omega, clique = clique_number(pos, neg)
            models = sat_models(pos, neg)
            qhist[q] += 1
            chist[omega] += 1
            cross[(q, omega)] += 1
            modelhist[bool(models)] += 1
            if omega >= 5:
                assert Fraction(omega*(4-omega), 3) < 0
    assert sum(qhist.values()) == 5625
    assert qhist == {0:75, 2:1260, 3:1680, 4:2610}
    assert chist == {3:915, 5:3420, 6:1290}
    assert modelhist[True] == 5625
    y_pos = from_strings(("123","145","246","356"))
    y_neg = from_strings(("124","136","235","456"))
    z_pos = from_strings(("123","124","356","456"))
    z_neg = from_strings(("125","126","345","346"))
    assert len(sat_models(y_pos, y_neg)) == 20
    assert len(sat_models(z_pos, z_neg)) == 22
    assert clique_number(y_pos, y_neg)[0] == 5
    assert clique_number(z_pos, z_neg)[0] == 6
    assert 4-len(set(y_pos) & set(y_neg)) == 4
    assert 4-len(set(z_pos) & set(z_neg)) == 4
    assert (0,0,1,1,0,0) in sat_models(z_pos, z_neg)
    result = {
        "valid_formulas": 5625,
        "canonical_nonpaired": 5550,
        "q_histogram": dict(sorted(qhist.items())),
        "omega_histogram": dict(sorted(chist.items())),
        "q_by_omega": {f"{q},{w}":n for (q,w),n in sorted(cross.items())},
        "sat_histogram": {str(s):n for s,n in sorted(modelhist.items())},
        "Y": {"models":20, "omega":5, "negative_quadratic_form":"-5/3"},
        "Z": {"models":22, "omega":6, "negative_quadratic_form":"-4"},
        "failures":0,
        "claim_scope":"finite six-name semantic audit, not FLMV bit runtime"
    }
    outfile = Path(__file__).with_name(
        "2026-10-24_2004_M22_NAE_PSD_CLIQUE150_results.json")
    outfile.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    audit()
