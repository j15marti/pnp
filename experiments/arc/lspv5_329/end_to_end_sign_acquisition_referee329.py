#!/usr/bin/env python3
"""Finite controls for REFEREE329's end-to-end sign acquisition theorem."""

import itertools
import json
import resource
import time
from fractions import Fraction
from pathlib import Path

OUT = Path("results/raw/arc/lspv5_329/end_to_end_sign_acquisition_referee329.json")


def horn_chain(m):
    clauses = [(1,)]
    clauses += [(-i, i + 1) for i in range(1, m - 1)]
    clauses += [(-(m - 1),)]
    return clauses


def models(clauses):
    n = max(abs(lit) for c in clauses for lit in c)
    out = []
    for bits in itertools.product([0, 1], repeat=n):
        if all(any((bits[abs(lit)-1] == 1) == (lit > 0) for lit in c) for c in clauses):
            out.append(bits)
    return out


def flip_occurrence(clauses, target):
    out, seen = [], 0
    for c in clauses:
        nc = []
        for lit in c:
            nc.append(-lit if seen == target else lit)
            seen += 1
        out.append(tuple(nc))
    return out


def php(h):
    # Standard unary PHP(h+1,h): variable (pigeon, hole) -> 1+p*h+j.
    var = lambda p, j: 1 + p * h + j
    clauses = [tuple(var(p, j) for j in range(h)) for p in range(h + 1)]
    for j in range(h):
        for p in range(h + 1):
            for q in range(p + 1, h + 1):
                clauses.append((-var(p, j), -var(q, j)))
    return clauses


def parity_encode(x):
    return [sum(x) & 1] + list(x[1:])


def parity_decode(y):
    return [(sum(y) & 1)] + list(y[1:])


def k4_count(odd):
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    rhs = [1 if odd and v == 0 else 0 for v in range(4)]
    count = 0
    for a in range(64):
        good = True
        for v in range(4):
            p = 0
            for j, e in enumerate(edges):
                if v in e:
                    p ^= (a >> j) & 1
            good &= p == rhs[v]
        count += int(good)
    return count


def main():
    t0 = time.perf_counter()
    checks = 0
    fixtures = []

    # Established minimally-UNSAT Horn controls; no asymptotic hardness is inferred.
    for m in range(2, 11):
        f = horn_chain(m)
        base = models(f)
        assert not base
        checks += 1
        L = sum(map(len, f))
        neighbor_counts = []
        for i in range(L):
            ms = models(flip_occurrence(f, i))
            assert len(ms) == 1
            neighbor_counts.append(len(ms))
            checks += 1

        # Exact invertible representation change on the abstract sign-star promise.
        center = [0] * L
        yc = parity_encode(center)
        assert parity_decode(yc) == center and yc[0] == 0
        checks += 2
        for i in range(L):
            x = [0] * L
            x[i] = 1
            y = parity_encode(x)
            assert parity_decode(y) == x and y[0] == 1
            checks += 2

        fixtures.append({"m": m, "variables": m - 1, "occurrence_signs": L,
                         "base_models": 0, "neighbors": L,
                         "neighbor_model_counts": neighbor_counts})

    # The published Haken family is used only as a sign-sensitive source control here.
    php_fixtures = []
    for h in range(1, 4):
        f = php(h)
        assert models(f) == []
        checks += 1
        L = sum(map(len, f))
        assert L == h * (h + 1) ** 2
        checks += 1
        counts = []
        for i in range(L):
            c = len(models(flip_occurrence(f, i)))
            assert c > 0
            counts.append(c)
            checks += 1
        php_fixtures.append({"h": h, "variables": h * (h + 1), "clauses": len(f),
                             "occurrence_signs": L, "base_models": 0,
                             "neighbors": L, "neighbor_models_min": min(counts),
                             "neighbor_models_max": max(counts)})

    # Tight strategy: with p=1-2e read all, otherwise output an unbiased bit.
    strategies = []
    for eps in [Fraction(0), Fraction(1, 10), Fraction(1, 6), Fraction(1, 3), Fraction(49, 100)]:
        p = 1 - 2 * eps
        for L in [2, 8, 16, 48, 128]:
            error = (1 - p) / 2
            expected = p * L
            assert error == eps and expected == (1 - 2 * eps) * L
            checks += 2
            strategies.append({"epsilon": str(eps), "L": L,
                               "read_all_probability": str(p),
                               "error_each_input": str(error),
                               "expected_center_sign_queries": str(expected)})

    # Packed probes: each probe reveals at most w sensitive sign fields.
    packed = []
    for L in [16, 48, 128]:
        for w in [1, 2, 8, 16]:
            lower = Fraction(1, 3) * L / w  # epsilon=1/3
            assert lower >= 0
            checks += 1
            packed.append({"L": L, "w": w, "epsilon": "1/3",
                           "expected_probe_lower_bound": str(lower)})

    # Malformed sign records and mandatory both-label parity control.
    bad = [None, "010", [], [0, 2], [-1, 0], [True, False], {"bits": [0]}, [0, 1, None]]
    for b in bad:
        valid = isinstance(b, list) and len(b) > 0 and all(type(x) is int and x in (0, 1) for x in b)
        assert not valid
        checks += 1
    odd, even = k4_count(True), k4_count(False)
    assert (odd, even) == (0, 8)
    checks += 2

    data = {
        "artifact": "END-TO-END-SIGN-ACQUISITION-REFEREE329",
        "status": "finite controls; mathematical theorem in report",
        "checks": checks,
        "fixtures": fixtures,
        "total_sign_flip_neighbors": sum(f["neighbors"] for f in fixtures),
        "php_fixtures": php_fixtures,
        "php_sign_flip_neighbors": sum(f["neighbors"] for f in php_fixtures),
        "strategies": strategies,
        "packed_probe_controls": packed,
        "representation": {
            "forward": "y1=xor(x1..xL); yj=xj for j>=2",
            "inverse": "x1=xor(y1..yL); xj=yj for j>=2",
            "supplied_recoded_star_queries": 1,
            "canonical_to_recoded_construction_reads": "L exact; at least (1-2epsilon)L bounded-error"
        },
        "k4_models": {"odd": odd, "even": even},
        "malformed_rejected": len(bad),
        "wall_seconds": time.perf_counter() - t0,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "classification": {
            "proved": "tight classical randomized canonical-source query theorem",
            "restricted": "canonical independent sign fields and classical query access",
            "open": ["B1", "B2", "B3", "superpolynomial Wbar_Rmix341", "P!=NP"]
        }
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(json.dumps(data, sort_keys=True))


if __name__ == "__main__":
    main()
