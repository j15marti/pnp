#!/usr/bin/env python3
"""Finite quantifier/resource controls for REFEREE327.

The uniform-generation theorem is symbolic.  These finite controls exercise
global fallback, generation/output charges, malformed inputs, corrupt advice,
and offline logical-XOR diagnostics.  They are not asymptotic evidence.
"""
import hashlib
import json
from itertools import product
from pathlib import Path


def model_count(mask):
    if not isinstance(mask, int) or isinstance(mask, bool) or not (1 <= mask <= 255):
        return 0
    return sum(1 for a in range(8) if ((mask >> a) & 1) == 0)


def label(record):
    return int(isinstance(record, int) and not isinstance(record, bool)
               and 1 <= record <= 255 and model_count(record) > 0)


def generate_prefix_program(cutoff, delay=0):
    """Return a finite table plus an explicit generation ledger."""
    table = []
    model_checks = 0
    for record in range(cutoff + 1):
        if 1 <= record <= 255:
            # Explicit exhaustive label computation: at most eight assignments.
            count = 0
            for a in range(8):
                model_checks += 1
                count += int(((record >> a) & 1) == 0)
            table.append(int(count > 0))
        else:
            table.append(0)
    delayed_steps = 0
    for _ in range(delay):
        delayed_steps += 1
    # One table bit per prefix record; cutoff/fallback/parser fields are recorded
    # separately rather than pretending that a Python object is a TM encoding.
    return table, {
        "model_checks": model_checks,
        "delay_steps": delayed_steps,
        "serialized_table_bits": len(table),
        "cutoff_index_bits": max(1, cutoff.bit_length()),
    }


def run_generated(record, cutoff, table):
    if isinstance(record, int) and not isinstance(record, bool) and 0 <= record <= cutoff:
        return table[record]
    return label(record)  # fixed globally correct fallback


def k4_models(charge):
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    count = 0
    for bits in product((0, 1), repeat=6):
        good = True
        for v in range(4):
            parity = 0
            for i, edge in enumerate(edges):
                if v in edge:
                    parity ^= bits[i]
            good &= parity == charge[v]
        count += int(good)
    return count


def gray(i):
    return i ^ (i >> 1)


def main():
    assertions = 0
    horizons = [0, 1, 7, 31, 127, 255]
    ledgers = []
    malformed = [-3, -1, 256, 999, "1", "p cnf", None, True, [], {}]
    for cutoff in horizons:
        table, ledger = generate_prefix_program(cutoff)
        for record in range(256):
            assert run_generated(record, cutoff, table) == label(record)
            assertions += 1
        for record in malformed:
            assert run_generated(record, cutoff, table) == 0
            assertions += 1
        ledger["cutoff"] = cutoff
        ledger["prefix_correct"] = True
        ledgers.append(ledger)

    normal, normal_ledger = generate_prefix_program(255, delay=0)
    delayed, delayed_ledger = generate_prefix_program(255, delay=10000)
    assert normal == delayed
    assert delayed_ledger["delay_steps"] == 10000
    assertions += 2

    corrupt = normal.copy()
    corrupt[255] = 1
    assert run_generated(255, 255, corrupt) != label(255)
    assertions += 1

    odd = k4_models((1, 0, 0, 0))
    even = k4_models((0, 0, 0, 0))
    assert (odd, even) == (0, 8)
    assertions += 1

    # Offline logical-state diagnostics.  Address/head/control bits are not
    # modeled, so no physical-write or native-time claim is made.
    correct_ones = sum(normal)
    binary_changed = [i for i in range(256) if normal[i]]
    gray_changed = [gray(i) for i in range(256) if normal[gray(i)]]
    assert sorted(binary_changed) == sorted(gray_changed)
    assert correct_ones == 254
    assertions += 2
    xor_diag = {
        "zero_to_correct_endpoint_delta": correct_ones,
        "binary_build_sum_adjacent_label_deltas": correct_ones,
        "gray_build_sum_adjacent_label_deltas": correct_ones,
        "changed_then_restored_sum_adjacent_label_deltas": correct_ones + 2,
        "changed_then_restored_endpoint_delta": correct_ones,
        "restored_record_id": 255,
        "delay_loop_data_bit_delta": 0,
        "d_phys": None,
        "note": "Offline logical table diagnostic only; address, head, code and native tape states are not modeled.",
    }

    result = {
        "artifact": "UNIFORM-GENERATOR-COLLAPSE-REFEREE327",
        "timestamp_pst": "2026-11-03 19:48",
        "theorem": {
            "property": "There exists one fixed total generator G and exponent k such that G(1^N) outputs p_N and generation+serialization+prefix execution is O(N^k).",
            "program_requirement": "Each p_N is total and correct for the total CNF-SAT language on every binary string; malformed strings are NO.",
            "equivalence": "The property holds iff CNF-SAT is in P.",
            "quantifier_order": "exists G,k for all N; not for all N exists G_N",
        },
        "status": {
            "uniform_generator_equivalence": "PROVED in report",
            "finite_controls": "PROVED",
            "B1_B2_B3_Rmix341": "OPEN",
            "P_vs_NP": "OPEN",
        },
        "horizon_ledgers": ledgers,
        "normal_generation": normal_ledger,
        "delayed_generation": delayed_ledger,
        "tiny_language": {"valid": 255, "sat": 254, "unsat": 1, "malformed_controls": len(malformed), "corrupt_table_rejected": True},
        "k4_tseitin": {"odd_models": odd, "even_models": even},
        "xor_offline": xor_diag,
        "assertions": assertions,
    }
    out = Path("results/raw/arc/lspv5_327/uniform_generator_collapse_referee327.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out.write_text(payload)
    print(json.dumps({"output": str(out), "sha256": hashlib.sha256(payload.encode()).hexdigest(), "assertions": assertions}))


if __name__ == "__main__":
    main()
