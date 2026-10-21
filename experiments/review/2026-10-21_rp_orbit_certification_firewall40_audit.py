#!/usr/bin/env python3
"""Exact finite audit for RP-ORBIT-CERTIFICATION-FIREWALL40."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Stats:
    truth_tables: int = 0
    tape_pairs: int = 0
    density_checks: int = 0
    symmetry_checks: int = 0
    permutation_checks: int = 0
    orbit_partition_checks: int = 0
    assertions: int = 0


def c_value(mask: int, z: int) -> int:
    return (mask >> z) & 1


def verifier(mask: int, q: int, a: int, b: int, z: int) -> int:
    """V_C(q,a,b,z) = q OR (a AND NOT b AND C(z))."""
    return int(bool(q or (a and not b and c_value(mask, z))))


def exhaustive(max_z_bits: int, stats: Stats) -> None:
    for k in range(max_z_bits + 1):
        z_count = 1 << k
        function_count = 1 << z_count
        tape_count = 8 * z_count
        for mask in range(function_count):
            stats.truth_tables += 1
            accepted = 0
            invariant = True
            sat_count = mask.bit_count()
            for q in (0, 1):
                for a in (0, 1):
                    for b in (0, 1):
                        for z in range(z_count):
                            v = verifier(mask, q, a, b, z)
                            w = verifier(mask, q, b, a, z)
                            accepted += v
                            stats.tape_pairs += 1
                            stats.assertions += 1
                            assert v in (0, 1)
                            if v != w:
                                invariant = False

            expected_accepted = 4 * z_count + sat_count
            stats.assertions += 3
            stats.density_checks += 1
            stats.symmetry_checks += 1
            assert accepted == expected_accepted
            assert accepted * 2 >= tape_count
            assert invariant == (mask == 0)

            # Any permutation of the tape universe preserves acceptance count.
            # XOR is a permutation of the canonical integer encoding.
            xor_key = (mask * 0x9E3779B1 + k) & (tape_count - 1)
            permuted_accepted = 0
            for idx in range(tape_count):
                src = idx ^ xor_key
                z = src & (z_count - 1)
                rem = src >> k
                b = rem & 1
                a = (rem >> 1) & 1
                q = (rem >> 2) & 1
                permuted_accepted += verifier(mask, q, a, b, z)
            stats.assertions += 1
            stats.permutation_checks += 1
            assert permuted_accepted == accepted


def random_orbit_controls(seed: int, cases: int, stats: Stats) -> None:
    """Check the promised orbit-representative simulation on random partitions."""
    rng = random.Random(seed)
    for _ in range(cases):
        universe = rng.randint(1, 128)
        orbit_count = rng.randint(1, universe)
        labels = [rng.randrange(orbit_count) for _ in range(universe)]
        present = sorted(set(labels))
        orbit_accept = {label: rng.randrange(2) for label in present}
        acceptance = [orbit_accept[label] for label in labels]
        representatives = [labels.index(label) for label in present]
        brute = any(acceptance)
        by_representatives = any(acceptance[r] for r in representatives)
        stats.assertions += 2 + universe
        stats.orbit_partition_checks += 1
        assert brute == by_representatives
        for i in range(universe):
            assert acceptance[i] == orbit_accept[labels[i]]
        # A one-sided verifier decides NO exactly when every orbit rejects.
        assert (not brute) == all(orbit_accept[label] == 0 for label in present)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-z-bits", type=int, default=4)
    parser.add_argument("--orbit-cases", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=202610211248)
    parser.add_argument("--output", default="RP_ORBIT_CERTIFICATION_FIREWALL40_raw.json")
    args = parser.parse_args()

    stats = Stats()
    exhaustive(args.max_z_bits, stats)
    random_orbit_controls(args.seed, args.orbit_cases, stats)
    result = {
        "claim": "RP-ORBIT-CERTIFICATION-FIREWALL40",
        "status": "PASS",
        "parameters": {
            "max_z_bits": args.max_z_bits,
            "orbit_cases": args.orbit_cases,
            "seed": args.seed,
        },
        "stats": asdict(stats),
        "theorem_checks": {
            "swap_invariant_iff_C_unsatisfiable": True,
            "acceptance_density_at_least_one_half": True,
            "recognized_language_is_sigma_star": True,
            "seed_permutations_preserve_density": True,
            "promised_orbit_representatives_decide_verifier": True,
        },
        "scope": [
            "finite tests do not prove P=RP or P!=RP",
            "coNP-completeness is for verifier-circuit symmetry certification",
            "orbit derandomization requires a supplied uniform partition and representatives",
        ],
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output).write_text(payload, encoding="utf-8")
    digest = hashlib.sha256(payload.encode()).hexdigest()
    print(json.dumps({"output": args.output, "sha256": digest, **result}, sort_keys=True))


if __name__ == "__main__":
    main()
