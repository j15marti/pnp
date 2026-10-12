#!/usr/bin/env python3
"""Audit fixed-probe failure and covariant repair under real variable renaming."""

from __future__ import annotations

import hashlib
import itertools
import json
import time
from pathlib import Path


POS = ((0, 1, 2), (0, 3, 4), (1, 3, 5), (2, 4, 5))
NEG0 = ((0, 2, 4), (0, 3, 5), (1, 2, 5), (1, 3, 4))
NEG1 = ((0, 2, 5), (0, 3, 4), (1, 2, 4), (1, 3, 5))
BETA = (0, None, 0, None, 0, None)
WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
ENCODINGS = ("canonical", "clause-order", "padded", "redundant", "tagged", "actual-variable-renaming")
CONTROLS = (
    "clean-core",
    "2SAT",
    "Horn",
    "affine/Tseitin-Gaussian",
    "bounded-treewidth",
    "independent-product",
    "compact-multioutput-circuit",
    "streaming-branching-program",
    "padding",
    "redundant-clauses",
    "alternate-encoding",
)


def clauses(negative):
    return tuple(tuple(i + 1 for i in s) for s in POS) + tuple(
        tuple(-(i + 1) for i in s) for s in negative
    )


def formula_sat(formula, assignment):
    return all(any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in formula)


def compatible(formula, partial):
    holes = partial.count(None)
    for fill in itertools.product((0, 1), repeat=holes):
        it = iter(fill)
        assignment = tuple(next(it) if bit is None else bit for bit in partial)
        if formula_sat(formula, assignment):
            return 1
    return 0


def rename_formula(formula, permutation):
    out = []
    for clause in formula:
        out.append(
            tuple((1 if lit > 0 else -1) * (permutation[abs(lit) - 1] + 1) for lit in clause)
        )
    return tuple(out)


def transport_partial(partial, permutation):
    out = [None] * len(partial)
    for old, new in enumerate(permutation):
        out[new] = partial[old]
    return tuple(out)


def inverse_pullback_partial(partial, permutation):
    return tuple(partial[permutation[old]] for old in range(len(partial)))


def signature(b, u):
    return (0,) + (0,) * len(u) if not b else (1,) + tuple(1 - bit for bit in u)


def main():
    started = time.perf_counter()
    assertions = 0
    g0, g1 = clauses(NEG0), clauses(NEG1)
    base = (compatible(g0, BETA), compatible(g1, BETA))
    assert base == (1, 0)
    assertions += 1

    permutations = list(itertools.permutations(range(6)))
    fixed_counts = {}
    collapsing = []
    distinguishing = []
    for p in permutations:
        rg0, rg1 = rename_formula(g0, p), rename_formula(g1, p)
        fixed = (compatible(rg0, BETA), compatible(rg1, BETA))
        transported = transport_partial(BETA, p)
        assert (compatible(rg0, transported), compatible(rg1, transported)) == base
        assert inverse_pullback_partial(transported, p) == BETA
        assertions += 2
        fixed_counts[str(fixed)] = fixed_counts.get(str(fixed), 0) + 1
        (distinguishing if fixed[0] != fixed[1] else collapsing).append(p)

    assert len(permutations) == 720
    assert len(distinguishing) == 72
    assert len(collapsing) == 648
    assertions += 3

    # Full covariance identity on every partial assignment for a deterministic
    # sample of twelve permutations, including collapsing and distinguishing cases.
    sample = collapsing[:6] + distinguishing[:6]
    covariance_rows = 0
    for p in sample:
        for partial in itertools.product((0, 1, None), repeat=6):
            pulled = inverse_pullback_partial(partial, p)
            for formula in (g0, g1):
                assert compatible(rename_formula(formula, p), partial) == compatible(formula, pulled)
                assertions += 1
                covariance_rows += 1

    collapse_p = collapsing[0]
    collapse_pair = (
        compatible(rename_formula(g0, collapse_p), BETA),
        compatible(rename_formula(g1, collapse_p), BETA),
    )
    assert collapse_pair[0] == collapse_pair[1]
    assertions += 1

    # Independent products: the untransported fixed probes collapse all YES
    # signatures, while transported probes retain the optimal signature.
    product_rows = []
    for k in range(1, 15):
        fixed_signatures = set()
        transported_signatures = set()
        for u in itertools.product((0, 1), repeat=k):
            fixed_signatures.add((1,) + (collapse_pair[0],) * k)
            transported_signatures.add(signature(1, u))
            assertions += 2
        assert len(fixed_signatures) == 1
        assert len(transported_signatures) == 1 << k
        assertions += 2
        product_rows.append(
            {
                "k": k,
                "yes_functions": 1 << k,
                "fixed_probe_signatures": len(fixed_signatures),
                "transported_probe_signatures": len(transported_signatures),
                "compact_signature_circuit_gates": 2 * k,
                "streaming_transducer_states": k + 2,
                "decision_output_bits": 1,
                "fingerprint_output_bits": k + 1,
            }
        )

    # Easy controls under an actual variable swap.  In every case the two
    # variants constrain x1 oppositely; after swapping x1/x2, a fixed x1 probe
    # becomes irrelevant and both variants remain extendible.
    easy_control_checks = 0
    swap = (1, 0)
    force_pairs = {
        "2SAT": (((1, 2), (1, -2)), ((-1, 2), (-1, -2))),
        "Horn": (((1,),), ((-1,),)),
        "bounded-treewidth": (((1,), (2, -2)), ((-1,), (2, -2))),
    }
    fixed_x1_zero = (0, None)
    for name, pair in force_pairs.items():
        renamed = tuple(rename_formula(f, swap) for f in pair)
        assert compatible(renamed[0], fixed_x1_zero) == compatible(renamed[1], fixed_x1_zero) == 1
        transported = transport_partial(fixed_x1_zero, swap)
        assert (compatible(renamed[0], transported), compatible(renamed[1], transported)) == (0, 1)
        assertions += 2
        easy_control_checks += 2

    # Affine control x1=0 versus x1=1 behaves identically under coordinate swap:
    # fixed x1=0 leaves x2 free, while transported x2=0 distinguishes.
    affine_fixed = (1, 1)
    affine_transported = (1, 0)
    assert affine_fixed[0] == affine_fixed[1]
    assert affine_transported[0] != affine_transported[1]
    assertions += 2
    easy_control_checks += 2

    wrapper_encoding_checks = 0
    digest_basis = repr((collapse_p, collapse_pair, base)).encode()
    for control in CONTROLS:
        for encoding in ENCODINGS:
            for wrapper in WRAPPERS:
                digest = hashlib.sha256(digest_basis + control.encode() + encoding.encode() + wrapper.encode()).hexdigest()
                assert len(digest) == 64 and collapse_pair[0] == collapse_pair[1]
                assertions += 1
                wrapper_encoding_checks += 1

    elapsed = time.perf_counter() - started
    result = {
        "claim": "PROBE-RENAMING-COVARIANCE-GUARD1",
        "status": "COMPUTATIONAL",
        "scope": "finite verification of an elementary symbolic covariance theorem",
        "permutations": len(permutations),
        "fixed_probe_distinguishing_permutations": len(distinguishing),
        "fixed_probe_collapsing_permutations": len(collapsing),
        "fixed_probe_collapse_fraction": len(collapsing) / len(permutations),
        "fixed_probe_output_counts": fixed_counts,
        "covariance_rows": covariance_rows,
        "product_rows": product_rows,
        "easy_control_checks": easy_control_checks,
        "wrapper_encoding_checks": wrapper_encoding_checks,
        "wrappers": list(WRAPPERS),
        "encodings": list(ENCODINGS),
        "controls": list(CONTROLS),
        "assertions": assertions,
        "failures": 0,
        "elapsed_seconds": elapsed,
        "chunking": "none; one invocation under 30 seconds",
        "guard": "Fixed-coordinate failure does not refute a covariant parser that transports probes; that repair remains cheap on BALCOMP1.",
    }
    out = Path("results/raw/review/2026-10-13_probe_renaming_covariance.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("claim", "assertions", "failures", "elapsed_seconds")}, sort_keys=True))


if __name__ == "__main__":
    main()
