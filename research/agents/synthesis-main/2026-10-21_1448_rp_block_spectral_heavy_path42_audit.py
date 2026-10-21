#!/usr/bin/env python3
"""Exact finite audit for RP-BLOCK-SPECTRAL-HEAVY-PATH42.

Only Python's standard library is used.  The checks are finite controls for
the displayed combinatorial/Fourier inequalities, not a P-vs-RP result.
"""

from fractions import Fraction
from itertools import product
import json
from pathlib import Path


CHECKS = 0


def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(message)


def walsh_coefficients(values):
    """Normalized {0,1}-valued Fourier coefficients on {0,1}^b."""
    n = len(values)
    out = []
    for mask in range(n):
        total = 0
        for x, value in enumerate(values):
            parity = (mask & x).bit_count() & 1
            total += value * (-1 if parity else 1)
        out.append(Fraction(total, n))
    return out


def subset_bias(points, n):
    """Maximum absolute nonconstant parity bias of uniform points."""
    return max(
        abs(Fraction(sum((-1 if ((mask & x).bit_count() & 1) else 1)
                         for x in points), len(points)))
        for mask in range(1, n)
    )


def audit_fourier():
    cases = 0
    hitting_cases = 0
    for b in range(1, 4):
        n = 1 << b
        for point_mask in range(1, 1 << n):
            points = [x for x in range(n) if (point_mask >> x) & 1]
            eps = subset_bias(points, n)
            for truth_mask in range(1 << n):
                values = [(truth_mask >> x) & 1 for x in range(n)]
                coeffs = walsh_coefficients(values)
                l1_nonconstant = sum(abs(c) for c in coeffs[1:])
                uniform_mean = coeffs[0]
                sample_mean = Fraction(sum(values[x] for x in points), len(points))
                check(abs(sample_mean - uniform_mean) <= eps * l1_nonconstant,
                      "Fourier small-bias inequality failed")
                cases += 1
                if uniform_mean > eps * l1_nonconstant:
                    check(sample_mean > 0, "edge-hitting corollary failed")
                    hitting_cases += 1

    singleton = {}
    for b in range(1, 9):
        n = 1 << b
        coeffs = walsh_coefficients([1] + [0] * (n - 1))
        l1 = sum(abs(c) for c in coeffs)
        check(l1 == 1, "singleton Fourier L1 should equal one")
        singleton[str(b)] = {"density": str(Fraction(1, n)), "fourier_l1": str(l1)}
    return {"inequality_cases": cases, "hitting_cases": hitting_cases,
            "singleton_controls": singleton}


def path_statistics(transitions, alphabet_size, accepting):
    ell = len(transitions)
    accepting_runs = []
    edge_probs = []
    for layer in transitions:
        w = len(layer)
        edge_probs.append([
            [Fraction(row.count(q2), alphabet_size) for q2 in range(w)]
            for row in layer
        ])
    for tape in product(range(alphabet_size), repeat=ell):
        q = 0
        used = []
        for i, symbol in enumerate(tape):
            q2 = transitions[i][q][symbol]
            used.append(edge_probs[i][q][q2])
            q = q2
        if q in accepting:
            accepting_runs.append((tape, used))
    return accepting_runs, edge_probs


def audit_heavy_path():
    systems = 0
    rp_systems = 0
    rare_union_checks = 0
    # Exhaust all layered systems for w=2, binary blocks, ell<=3.
    # Each layer has 2^(w*k)=16 transition tables.
    for ell in range(1, 4):
        w = 2
        k = 2
        layer_tables = []
        for bits in product(range(w), repeat=w * k):
            layer_tables.append([list(bits[q*k:(q+1)*k]) for q in range(w)])
        for layer_ids in product(range(len(layer_tables)), repeat=ell):
            transitions = [layer_tables[i] for i in layer_ids]
            for accepting in ({0}, {1}, {0, 1}):
                runs, edge_probs = path_statistics(transitions, k, accepting)
                systems += 1
                acceptance = Fraction(len(runs), k ** ell)
                delta = Fraction(1, 4 * ell * w)

                # Exact probability that a random run traverses a rare edge.
                rare_runs = 0
                for tape in product(range(k), repeat=ell):
                    q = 0
                    rare = False
                    for i, symbol in enumerate(tape):
                        q2 = transitions[i][q][symbol]
                        rare |= edge_probs[i][q][q2] <= delta
                        q = q2
                    rare_runs += int(rare)
                rare_probability = Fraction(rare_runs, k ** ell)
                check(rare_probability <= ell * w * delta,
                      "rare-edge union bound failed")
                rare_union_checks += 1

                if acceptance >= Fraction(1, 2):
                    rp_systems += 1
                    check(any(all(p > delta for p in used) for _, used in runs),
                          "RP-heavy accepting path missing")
    return {"systems": systems, "rp_systems": rp_systems,
            "rare_union_checks": rare_union_checks,
            "parameters": "w=2, block alphabet=2, ell=1..3, all layered transitions"}


def main():
    fourier = audit_fourier()
    heavy = audit_heavy_path()
    result = {
        "name": "RP-BLOCK-SPECTRAL-HEAVY-PATH42",
        "status": "COMPUTATIONAL finite audit; theorem proof is separate",
        "fourier": fourier,
        "heavy_path": heavy,
        "assertions": CHECKS,
        "failures": 0,
        "scope_firewall": [
            "Does not derandomize arbitrary RP verifiers.",
            "Does not prove P=RP, P!=RP, or P!=NP.",
            "Does not supply either open P-vs-NP load-bearing arrow."
        ]
    }
    path = Path("RP_BLOCK_SPECTRAL_HEAVY_PATH42_raw.json")
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
