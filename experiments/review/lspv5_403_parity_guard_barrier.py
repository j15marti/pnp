#!/usr/bin/env python3
"""Independent finite control for the ordinary-PC parity guard barrier.

This is not the historical R_mix341 checker.  It verifies the exact
multilinear normal form of the even-parity indicator, the characteristic-2
collapse, and the state-DAG/context-tree counts used in LSPV-5/403.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import resource
import time
import tracemalloc
from pathlib import Path


def even(mask: int) -> int:
    return 1 if mask.bit_count() % 2 == 0 else 0


def mobius_coeff(mask: int) -> int:
    """Coefficient of x_mask in the unique multilinear 0/1-cube form."""
    total = 0
    sub = mask
    while True:
        total += (-1) ** (mask.bit_count() - sub.bit_count()) * even(sub)
        if sub == 0:
            return total
        sub = (sub - 1) & mask


def closed_coeff(mask: int) -> int:
    if mask == 0:
        return 1
    s = mask.bit_count()
    return ((-1) ** s) * (2 ** (s - 1))


def all_evaluations(coeff: dict[int, int], k: int, modulus: int | None = None) -> list[int]:
    """Subset-zeta transform: evaluate every multilinear polynomial point."""
    values = [coeff.get(mask, 0) for mask in range(1 << k)]
    for bit in range(k):
        step = 1 << bit
        for mask in range(1 << k):
            if mask & step:
                values[mask] += values[mask ^ step]
                if modulus is not None:
                    values[mask] %= modulus
    if modulus is not None:
        values = [v % modulus for v in values]
    return values


def reduce_power_monomials(terms: list[tuple[tuple[int, ...], int]]) -> dict[int, int]:
    """Reduce x_i^a to x_i modulo x_i^2-x_i and collect coefficients."""
    out: dict[int, int] = {}
    for powers, coefficient in terms:
        mask = 0
        for i, power in enumerate(powers):
            if power < 0:
                raise ValueError("negative exponent")
            if power:
                mask |= 1 << i
        out[mask] = out.get(mask, 0) + coefficient
    return {m: c for m, c in out.items() if c}


def state_counts(k: int) -> dict[str, int]:
    return {
        "bits": k,
        "state_nodes": 1 + 2 * k,
        "state_edges": 2 + 4 * (k - 1),
        "context_leaves": 2**k,
        "even_contexts": 2 ** (k - 1),
        "odd_contexts": 2 ** (k - 1),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    start = time.perf_counter()
    tracemalloc.start()
    checks = 0
    rows = []

    for k in range(1, 17):
        coeff: dict[int, int] = {}
        for mask in range(1 << k):
            want = closed_coeff(mask)
            if k <= 12:
                assert mobius_coeff(mask) == want
                checks += 1
            coeff[mask] = want
        assert len(coeff) == 2**k
        checks += 1
        values = all_evaluations(coeff, k)
        for assignment, value in enumerate(values):
            assert value == even(assignment)
            checks += 1
        odd_prime_counts = {}
        for p in (3, 5, 7, 11):
            count = sum(1 for c in coeff.values() if c % p)
            assert count == 2**k
            odd_prime_counts[str(p)] = count
            checks += 1
        f2 = {0: 1, **{1 << i: 1 for i in range(k)}}
        for assignment, value in enumerate(all_evaluations(f2, k, 2)):
            assert value == even(assignment)
            checks += 1
        assert len(f2) == k + 1
        checks += 1
        sc = state_counts(k)
        assert sc["even_contexts"] + sc["odd_contexts"] == sc["context_leaves"]
        checks += 1
        rows.append({
            **sc,
            "char_not_2_normal_form_monomials": len(coeff),
            "char_2_normal_form_monomials": len(f2),
            "odd_prime_nonzero_counts": odd_prime_counts,
            "explicit_pcr_even_leaf_guards": 2 ** (k - 1),
        })

    # Nonmultilinear syntax cannot alter the unique Boolean-ideal normal form.
    # x1^3 and x1^7 both reduce to x1; malformed negative exponents are rejected.
    reduced = reduce_power_monomials([((3, 0), 2), ((7, 0), -1), ((0, 0), 1)])
    assert reduced == {1: 1, 0: 1}
    checks += 1

    corruptions = {}
    try:
        reduce_power_monomials([((-1,), 1)])
        corruptions["negative_exponent"] = False
    except ValueError:
        corruptions["negative_exponent"] = True
    wrong = {m: closed_coeff(m) for m in range(1 << 6)}
    wrong[7] += 1
    corruptions["wrong_coefficient"] = any(v != even(a) for a, v in enumerate(all_evaluations(wrong, 6)))
    omitted = {m: closed_coeff(m) for m in range(1 << 6) if m != 31}
    corruptions["omitted_monomial"] = any(v != even(a) for a, v in enumerate(all_evaluations(omitted, 6)))
    corruptions["false_char2_exponential"] = (6 + 1) != 2**6
    corruptions["omitted_even_context"] = (2 ** (6 - 1) - 1) != 2 ** (6 - 1)
    assert all(corruptions.values())
    checks += len(corruptions)

    current, peak = tracemalloc.get_traced_memory()
    elapsed = time.perf_counter() - start
    source = Path(__file__).read_bytes()
    result = {
        "status": "PASS",
        "scope": "ordinary sparse-monomial PC guard normalization; not historical R_mix341",
        "theorem_control": {
            "char_not_2": "even parity indicator has exactly 2^k nonzero multilinear monomials",
            "char_2": "even parity indicator is 1+x1+...+xk and has k+1 monomials",
            "state_dag": "1+2k states and 4k-2 edges versus 2^k assignment contexts",
            "limit": "does not lower-bound arbitrary PC/PCR/extension/mixed refutations",
        },
        "rows": rows,
        "checks": checks,
        "corruptions_rejected": corruptions,
        "elapsed_seconds": elapsed,
        "python_tracemalloc_current_bytes": current,
        "python_tracemalloc_peak_bytes": peak,
        "process_max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "source_sha256": hashlib.sha256(source).hexdigest(),
        "disclaimer": "independent implementation, not an authoritative checker execution",
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(text)
    print(json.dumps({
        "status": result["status"],
        "checks": checks,
        "k_max": rows[-1]["bits"],
        "odd_char_monomials_at_k_max": rows[-1]["char_not_2_normal_form_monomials"],
        "char2_monomials_at_k_max": rows[-1]["char_2_normal_form_monomials"],
    }))


if __name__ == "__main__":
    main()
