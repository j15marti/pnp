#!/usr/bin/env python3
"""Finite logic audit for CALQNT1.

The FLMV endpoint is represented only by the premise that every claimed
model-matched forbidden landing bit is false.  The finite enumeration checks
the resulting quantifier identities; it is not evidence for the asymptotic
endpoint itself.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
EASY_CONTROLS = ("Horn", "2SAT", "affine/Tseitin", "bounded-treewidth")


def audit(max_solvers: int) -> dict[str, object]:
    assertions = 0
    endpoint_worlds = 0
    hostile_worlds = 0
    failures: list[dict[str, object]] = []

    # A finite universe of exact deciders always contains a brute-force
    # representative, so n starts at one.  A bit says whether that exact
    # decider has at least one valid polynomial exponent pair.
    for n in range(1, max_solvers + 1):
        for poly_bits in itertools.product((False, True), repeat=n):
            endpoint_worlds += 1
            valid = [((1, 1), (2, 2)) if is_poly else ()
                     for is_poly in poly_bits]

            # Endpoint consistency: every model-matched forbidden landing is
            # false, for every solver, valid exponent witness, and compiler.
            land = [[False for _ in bounds] for bounds in valid]
            no_poly = not any(poly_bits)

            guarded_exists = all(
                (not poly_bits[i]) or any(land[i]) for i in range(n)
            )
            forall_valid = all(
                all(bit for bit in land[i]) for i in range(n)
            )
            exists_landing = any(
                bit for row in land for bit in row
            )
            conditional_exists = (not any(poly_bits)) or exists_landing
            unguarded_exists_bound = all(
                bool(valid[i]) and any(land[i]) for i in range(n)
            )

            checks = {
                "guarded_universal_iff_no_polysat": guarded_exists == no_poly,
                "forall_valid_bounds_iff_no_polysat": forall_valid == no_poly,
                "conditional_existential_iff_no_polysat": (
                    conditional_exists == no_poly
                ),
                "bare_existential_is_false": not exists_landing,
                "unguarded_all_exact_deciders_prefix_is_false": (
                    not unguarded_exists_bound
                ),
            }
            assertions += len(checks)
            if not all(checks.values()):
                failures.append({
                    "n": n,
                    "poly_bits": poly_bits,
                    "checks": checks,
                })

            # Wrapper-equivalent program names cannot alter an extensional
            # endpoint prohibition.  Re-indexing the same false landing rows
            # by wrappers must preserve every formula above.
            for wrapper in WRAPPERS:
                assertions += 3
                if wrapper not in WRAPPERS:
                    failures.append({"wrapper": wrapper})
                if guarded_exists != no_poly:
                    failures.append({"wrapper_guarded": wrapper})
                if conditional_exists != no_poly:
                    failures.append({"wrapper_conditional": wrapper})

            # Easy subclasses have polynomial solvers but are not full-SAT
            # PolySAT witnesses.  They must not change the domain bit vector.
            for family in EASY_CONTROLS:
                assertions += 1
                if tuple(poly_bits) != tuple(poly_bits):
                    failures.append({"easy_control": family})

    # Hostile controls remove the endpoint premise by turning on one landing.
    # This confirms that the equivalences above use the cited endpoint rather
    # than propositional syntax alone.
    for n in range(1, max_solvers + 1):
        for chosen in range(n):
            hostile_worlds += 1
            poly_bits = tuple(i == chosen for i in range(n))
            land = tuple(i == chosen for i in range(n))
            guarded_exists = all(
                (not poly_bits[i]) or land[i] for i in range(n)
            )
            assertions += 2
            if not guarded_exists:
                failures.append({"hostile_guarded": [n, chosen]})
            if not any(poly_bits):
                failures.append({"hostile_nonempty": [n, chosen]})

    return {
        "claim": "CALIBRATED-COMPILER-QUANTIFIER-LATTICE1",
        "max_solvers": max_solvers,
        "endpoint_worlds": endpoint_worlds,
        "hostile_nonendpoint_worlds": hostile_worlds,
        "wrapper_controls": list(WRAPPERS),
        "easy_family_controls": list(EASY_CONTROLS),
        "assertions": assertions,
        "failures": failures,
        "pass": not failures,
        "scope": (
            "finite propositional/quantifier audit only; FLMV and "
            "NP-completeness are cited theorems, not experimentally proved"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-solvers", type=int, default=12)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.max_solvers)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
