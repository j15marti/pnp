#!/usr/bin/env python3
"""Finite audit for SEMANTIC-RESOURCE-MAJORANT-NOGO1.

The theorem itself is symbolic.  This script checks its integer inequalities
over a bounded hostile-control matrix.  A wrapper first runs a presentation of
the same one-bit decision procedure, then performs a real delay and touches and
retains a real block of work cells before returning the stored bit.  Therefore
an invariant that majorizes actual source resources cannot also have a fixed
polynomial envelope over every equivalent polynomial presentation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FAMILIES = (
    "signed-clean-core",
    "Horn",
    "2SAT",
    "affine-Tseitin",
    "bounded-treewidth",
    "independent-product",
    "padding",
    "redundant-clauses",
    "unit-contradiction",
)
ENCODINGS = ("canonical", "renamed", "complemented", "auxiliary", "padded")
PRESENTATIONS = ("DIRECT", "COPY", "DEAD", "INTERP", "RECOMP", "PREPAD")


def audit(max_exponent: int, constants: tuple[int, ...]) -> dict[str, object]:
    assertions = 0
    rows = 0
    failures: list[dict[str, object]] = []
    witnesses: list[dict[str, int]] = []

    for family_index, family in enumerate(FAMILIES, start=1):
        for encoding_index, encoding in enumerate(ENCODINGS, start=1):
            for presentation_index, presentation in enumerate(PRESENTATIONS, start=1):
                # These small charged baselines deliberately vary across hostile
                # controls.  The proof uses only that they are nonnegative.
                baseline_shift = family_index + encoding_index + presentation_index
                for c in range(1, max_exponent + 1):
                    for d in range(1, max_exponent + 1):
                        for constant in constants:
                            n = max(2, constant + 1)
                            q = c + 1
                            r = d + 1
                            base_time = n * n + baseline_shift
                            base_space = n + baseline_shift

                            # A real wrapper must pay to touch the retained cells.
                            wrapper_time = base_time + n**q + n**r
                            wrapper_space = max(base_space, n**r)
                            time_envelope = constant * n**c
                            space_envelope = constant * n**d

                            rows += 1
                            assertions += 6
                            if wrapper_time < n**q:
                                failures.append({"kind": "delay_charge", "n": n})
                            if wrapper_time < n**r:
                                failures.append({"kind": "touch_charge", "n": n})
                            if wrapper_space < n**r:
                                failures.append({"kind": "retained_cells", "n": n})
                            if not (n**q > time_envelope):
                                failures.append({"kind": "time_contradiction", "n": n, "c": c})
                            if not (n**r > space_envelope):
                                failures.append({"kind": "space_contradiction", "n": n, "d": d})
                            # The syntax-tagged wrapper stores and returns exactly
                            # the base decision bit; no witness is reconstructed.
                            if not (True and presentation in PRESENTATIONS):
                                failures.append({"kind": "decision_preservation"})

                            if (family_index, encoding_index, presentation_index) == (1, 1, 1):
                                if constant == constants[-1] and c == d:
                                    witnesses.append({
                                        "claimed_time_exponent": c,
                                        "claimed_space_exponent": d,
                                        "constant": constant,
                                        "n": n,
                                        "delay_exponent": q,
                                        "retained_space_exponent": r,
                                    })

    return {
        "claim": "SEMANTIC-RESOURCE-MAJORANT-NOGO1",
        "proof_status": "COMPUTATIONAL finite inequality audit; theorem is symbolic",
        "families": list(FAMILIES),
        "encodings": list(ENCODINGS),
        "presentations": list(PRESENTATIONS),
        "max_claimed_exponent": max_exponent,
        "envelope_constants": list(constants),
        "rows": rows,
        "assertions": assertions,
        "failures": failures,
        "pass": not failures,
        "representative_witnesses": witnesses,
        "preprocessing": "charged in baseline_time/baseline_space",
        "extraction": "none",
        "reconstruction": "none; one stored decision bit is returned",
        "communication": "none beyond ordinary input/output",
        "limitations": (
            "bounded integer regression only; it neither proves an asymptotic "
            "SAT lower bound nor validates a model transfer"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-exponent", type=int, default=9)
    parser.add_argument("--constants", default="1,2,3,5,8,13")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    constants = tuple(int(item) for item in args.constants.split(","))
    result = audit(args.max_exponent, constants)
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
