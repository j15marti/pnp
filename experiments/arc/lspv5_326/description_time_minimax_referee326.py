#!/usr/bin/env python3
"""Finite controls for REFEREE326; not asymptotic lower-bound evidence."""
import hashlib
import json
from itertools import product
from pathlib import Path

def model_count(mask: int) -> int:
    return sum(1 for a in range(8) if not ((mask >> a) & 1))

def total_sat_label(record) -> int:
    return int(isinstance(record, int) and not isinstance(record, bool)
               and 1 <= record <= 255 and model_count(record) > 0)

def fallback_decider(record) -> int:
    return total_sat_label(record)

def prefix_program(record, cutoff: int, table: list[int]) -> int:
    if isinstance(record, int) and not isinstance(record, bool) and 0 <= record <= cutoff:
        return table[record]
    return fallback_decider(record)

def k4_tseitin_models(charge: tuple[int, int, int, int]) -> int:
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    count = 0
    for bits in product((0, 1), repeat=6):
        ok = True
        for v in range(4):
            parity = 0
            for i, (u, w) in enumerate(edges):
                if v == u or v == w:
                    parity ^= bits[i]
            ok &= parity == charge[v]
        count += int(ok)
    return count

def main() -> None:
    assertions = 0
    table = [total_sat_label(x) for x in range(256)]
    for x in range(256):
        assert prefix_program(x, 255, table) == total_sat_label(x)
        assertions += 1
    malformed = [-3, -1, 256, 999, "1", "p cnf", None, True, [], {}]
    for x in malformed:
        assert fallback_decider(x) == 0
        assert prefix_program(x, 255, table) == 0
        assertions += 2
    assert sum(table) == 254 and table[255] == 0
    assertions += 2
    corrupt = table.copy(); corrupt[255] = 1
    assert prefix_program(255, 255, corrupt) != total_sat_label(255)
    assertions += 1
    odd = k4_tseitin_models((1, 0, 0, 0))
    even = k4_tseitin_models((0, 0, 0, 0))
    assert odd == 0 and even == 8
    assertions += 2
    result = {
        "artifact": "DESCRIPTION-TIME-MINIMAX-POLY-CIRCUIT-REFEREE326",
        "timestamp_pst": "2026-11-03 18:48",
        "status": {"finite_controls": "PROVED", "asymptotic_equivalence": "proved in report, not by enumeration", "B1_B2_B3_Rmix341": "OPEN", "P_vs_NP": "OPEN"},
        "tiny_complete_clause_universe": {"valid_records": 255, "sat_records": 254, "unsat_records": 1, "malformed_controls": len(malformed), "globally_correct_prefix_program": True, "corrupt_advice_detected": True},
        "k4_tseitin": {"odd_charge_models": odd, "even_charge_models": even},
        "accounting": {"table_label_bits": 256, "fixed_width_index_bits": 8, "abstract_lookup_bit_probes_upper_bound": 8, "description_plus_lookup_lower_bookkeeping": 264, "correct_to_corrupt_table_offline_xor_popcount": 1, "d_phys": None, "xor_note": "Offline diagnostic only; no fixed-tape native execution is claimed."},
        "assertions": assertions,
        "theorem_metadata": {"measure": "K_U(N)=min_p(|p|+max_{|x|<=N}T_U(p,x))", "program_domain": "fixed U; p total and correct for total SAT language on every binary string", "quantifiers": "for every N there exists p_N; p_N may vary with N", "equivalence": "K_U(N)=N^O(1) for all N iff CNF-SAT is in P/poly", "physical_charge": "T includes parse, code access, representation construction, bit access/update, verification and output; peak space recorded separately"},
    }
    out = Path("results/raw/arc/lspv5_326/description_time_minimax_referee326.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out.write_text(payload)
    print(json.dumps({"output": str(out), "sha256": hashlib.sha256(payload.encode()).hexdigest(), "assertions": assertions}))

if __name__ == "__main__":
    main()
