#!/usr/bin/env python3
"""Finite audit of the exogenous-challenge model trilemma.

This checks quantifier and accounting identities.  It is not an asymptotic
SAT lower-bound experiment.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path


OUT = Path("results/raw/review/2026-10-12_exogenous_challenge_model_trilemma.json")
FAMILIES = [
    "2SAT", "Horn", "affine_Tseitin", "bounded_treewidth",
    "independent_product", "padding", "redundant_clauses",
    "alternate_encoding", "signed_clean_core",
]
ENCODINGS = ["indexed", "renamed", "auxiliary", "padded", "streamed"]
WRAPPERS = ["DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP"]
CHALLENGES = range(256)


def decision(family: str, encoding: str) -> int:
    digest = hashlib.sha256(f"{family}|{encoding}".encode()).digest()
    return digest[0] & 1


def run_mode(bit: int, challenge: int, mode: str) -> tuple[int, int]:
    """Return (decision output, audit response)."""
    if mode == "exact_audit":
        return bit, ((challenge * 29) ^ (bit * 113)) & 255
    if mode == "challenge_dependent":
        return bit ^ (challenge.bit_count() & 1), challenge
    if mode == "bounded_error":
        return bit ^ int(challenge == 255), challenge
    if mode == "length_advice":
        # Models a supplied length/input table bit, not a uniform computation.
        return challenge & 1, challenge
    raise ValueError(mode)


def wrap_output(value: tuple[int, int], wrapper: str) -> tuple[int, int]:
    # Wrappers alter charged work/presentation but preserve the declared pair.
    if wrapper not in WRAPPERS:
        raise ValueError(wrapper)
    return value


def main() -> None:
    started = time.perf_counter()
    assertions = 0
    failures = 0
    challenge_reads = 0
    response_ops = 0
    preprocessing_ops = 0
    rows = []

    for family in FAMILIES:
        for encoding in ENCODINGS:
            truth = decision(family, encoding)
            for wrapper in WRAPPERS:
                mode_summary = {}
                for mode in ("exact_audit", "challenge_dependent", "bounded_error", "length_advice"):
                    outputs = []
                    responses = []
                    for challenge in CHALLENGES:
                        out, response = wrap_output(run_mode(truth, challenge, mode), wrapper)
                        outputs.append(out)
                        responses.append(response)
                        challenge_reads += 1
                        response_ops += 1
                        preprocessing_ops += 1

                    wrong = sum(out != truth for out in outputs)
                    all_challenge_exact = wrong == 0
                    canonical_fixed_exact = outputs[0] == truth
                    audit_varies = len(set(responses)) > 1
                    mode_summary[mode] = {
                        "wrong_challenges": wrong,
                        "all_challenge_exact": all_challenge_exact,
                        "canonical_fixed_exact": canonical_fixed_exact,
                        "audit_varies": audit_varies,
                    }

                    assertions += 1
                    if mode == "exact_audit" and not all_challenge_exact:
                        failures += 1
                    assertions += 1
                    if mode == "exact_audit" and not canonical_fixed_exact:
                        failures += 1
                    assertions += 1
                    if mode == "exact_audit" and not audit_varies:
                        failures += 1
                    assertions += 1
                    if mode == "challenge_dependent" and wrong != 128:
                        failures += 1
                    assertions += 1
                    if mode == "bounded_error" and wrong != 1:
                        failures += 1
                    assertions += 1
                    if mode == "length_advice" and all_challenge_exact:
                        failures += 1

                rows.append({
                    "family": family,
                    "encoding": encoding,
                    "wrapper": wrapper,
                    "truth": truth,
                    "modes": mode_summary,
                })

    payload = {
        "run_id": "EXOGATE1",
        "status": "COMPUTATIONAL",
        "claim_tested": "Fresh external challenges alone give an exact uniform deterministic SAT lower-bound bridge.",
        "symbolic_theorem_tested": "All-challenge exactness permits canonical challenge fixing; weaker correctness changes the model.",
        "families": FAMILIES,
        "encodings": ENCODINGS,
        "wrappers": WRAPPERS,
        "challenge_count_per_cell": len(CHALLENGES),
        "rows": rows,
        "assertions": assertions,
        "failures": failures,
        "preprocessing_ops": preprocessing_ops,
        "challenge_reads": challenge_reads,
        "response_ops": response_ops,
        "compatibility_extraction_calls": 0,
        "witness_reconstruction_calls": 0,
        "runtime_seconds": round(time.perf_counter() - started, 6),
        "scope_warning": "Finite truth-table controls verify quantifier/accounting behavior only; the symbolic theorem is proved separately.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("run_id", "assertions", "failures", "runtime_seconds")}, sort_keys=True))


if __name__ == "__main__":
    main()
