#!/usr/bin/env python3
"""Finite controls for REFEREE331's explicit proof-padding firewall."""
import json
import resource
import time
from pathlib import Path

OUT = Path("results/raw/arc/lspv5_331/proof_padding_firewall_referee331.json")


def parse_formula(text):
    if not isinstance(text, str) or not text.isascii():
        raise ValueError("non-ASCII source")
    if text == "X" or (text.startswith("X;") and set(text[2:]) <= {"a"}):
        return "SAT"
    if text == "X&!X" or (text.startswith("X&!X;") and set(text[5:]) <= {"a"}):
        return "UNSAT"
    raise ValueError("malformed source")


def base_verify(text, base):
    return parse_formula(text) == "UNSAT" and base == "UNIT-CONFLICT"


def unary_verify(text, proof):
    if not isinstance(proof, dict) or set(proof) != {"base", "ticks"}:
        return False
    if not base_verify(text, proof["base"]):
        return False
    ticks = proof["ticks"]
    return isinstance(ticks, str) and set(ticks) <= {"T"} and len(ticks) == 2 ** len(text)


def macro_verify(text, proof):
    if not isinstance(proof, dict) or set(proof) != {"base", "run"}:
        return False
    return (base_verify(text, proof["base"]) and isinstance(proof["run"], int)
            and proof["run"] == 2 ** len(text))


def unsat_source(n):
    if n < 4:
        raise ValueError
    return "X&!X" if n == 4 else "X&!X;" + "a" * (n - 5)


def sat_source(n):
    if n < 1:
        raise ValueError
    return "X" if n == 1 else "X;" + "a" * (n - 2)


def main():
    started = time.perf_counter()
    checks = 0
    rows = []
    for n in range(4, 15):
        f = unsat_source(n)
        assert len(f) == n and parse_formula(f) == "UNSAT"; checks += 1
        count = 2 ** n
        unary = {"base": "UNIT-CONFLICT", "ticks": "T" * count}
        macro = {"base": "UNIT-CONFLICT", "run": count}
        assert unary_verify(f, unary); checks += 1
        assert not unary_verify(f, {"base": "UNIT-CONFLICT", "ticks": "T" * (count - 1)}); checks += 1
        assert not unary_verify(f, {"base": "UNIT-CONFLICT", "ticks": "T" * (count + 1)}); checks += 1
        assert not unary_verify(f, macro); checks += 1
        assert macro_verify(f, macro); checks += 1
        rows.append({
            "source_bits": n,
            "explicit_tick_nodes": count,
            "explicit_tick_payload_bytes": count,
            "indexed_tick_upper_bytes": n * count,
            "stream_counter_bits": n + 1,
            "compact_run_integer_bits": count.bit_length(),
            "unary_to_compact_payload_ratio_lower": count / max(1, count.bit_length()),
        })

    both_label = []
    for n in (1, 4, 8, 12):
        s = sat_source(n)
        assert len(s) == n and parse_formula(s) == "SAT"; checks += 1
        fake = {"base": "UNIT-CONFLICT", "ticks": "T" * (2 ** n)}
        assert not unary_verify(s, fake); checks += 1
        assert not macro_verify(s, {"base": "UNIT-CONFLICT", "run": 2 ** n}); checks += 1
        both_label.append({"source_bits": n, "label": "SAT", "both_verifiers_reject": True})

    malformed = ["", "!", "X&", "X&!", "X&!X;z", "Y", "X;;", "\u03c0"]
    rejected = 0
    for text in malformed:
        try:
            parse_formula(text)
        except ValueError:
            rejected += 1
    assert rejected == len(malformed); checks += len(malformed)

    data = {
        "artifact": "PROOF-PADDING-FIREWALL-REFEREE331",
        "checks": checks,
        "grammar": {
            "unary": "base proof followed by exactly 2^N explicit T bytes; no repeat macro",
            "compact_alternative": "base proof plus binary RUN count; a different proof system",
        },
        "rows": rows,
        "both_label_controls": both_label,
        "malformed_rejected": rejected,
        "charged_ledger": {
            "unary_output_and_construction": "Theta(2^N) bytes/steps (Theta(N*2^N) with explicit N-bit indices)",
            "unary_stream_verification": "Theta(2^N) token reads; O(N) counter bits",
            "unary_materialized_peak": "Theta(2^N) bytes if retained",
            "unary_stream_peak": "O(N) writable bits plus base-verifier space",
            "compact_macro": "O(N) description and arithmetic check, but outside unary Pad grammar",
        },
        "classification": {
            "proved": [
                "fixed exponential padding preserves soundness, completeness, and effective checking",
                "polynomial translations preserve polynomial boundedness in the translated direction",
            ],
            "counterexample": "sound+complete+effective does not imply B3 for an arbitrary fixed proof system",
            "padded_system": {
                "B1": "false for one fixed exhaustive uniform decider on minimally-UNSAT Horn chains",
                "B2": "false for the same decider under binary-index CNF encoding",
                "B3": "equivalent to SAT not in P because padded Wbar is unconditionally superpolynomial",
            },
            "open": ["B1_Rmix341", "B2_Rmix341", "B3_Rmix341", "superpolynomial_Wbar_Rmix341", "P!=NP"],
        },
        "wall_seconds": time.perf_counter() - started,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"artifact": data["artifact"], "checks": checks,
                      "peak_rss_kib": data["peak_rss_kib"]}, sort_keys=True))


if __name__ == "__main__":
    main()
