#!/usr/bin/env python3
"""ARC-BATCH-UNION-PROBE-FIREWALL227 finite audit.

Tests the exact batch-union interpretation of inverse-source transcript
counting.  Repeated child calls may reuse cached answers, so the number of
rounds cannot multiply an information lower bound unless fresh independent
demands are proved.  Clause order is the source permutation; SAT/UNSAT labels
are checked independently and clause-extreme controls are retained.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path


def truth(lit: int, mask: int) -> bool:
    return ((mask >> (abs(lit) - 1)) & 1) == (1 if lit > 0 else 0)


def models(formula: list[tuple[int, int, int]], nvars: int) -> list[int]:
    return [
        a for a in range(1 << nvars)
        if all(any(truth(lit, a) for lit in clause) for clause in formula)
    ]


def counts(formula: list[tuple[int, int, int]], mask: int) -> list[int]:
    h = [0, 0, 0, 0]
    for clause in formula:
        h[sum(truth(lit, mask) for lit in clause)] += 1
    return h


def extrema(formula: list[tuple[int, int, int]]) -> list[dict]:
    out = []
    for j, clause in enumerate(formula):
        occ = []
        for k, lit in enumerate(clause):
            s = 1 if lit > 0 else 0
            occ.append({
                "occurrence": f"x_{abs(lit)},{j + 1}",
                "position": k,
                "variable": abs(lit),
                "sign": "+" if lit > 0 else "-",
                "S_all_true": s,
                "inverse_S_is_U": 1 - s,
                "U_all_false": 1 - s,
                "inverse_U_is_S": s,
            })
        out.append({"clause_index": j, "clause": list(clause), "occurrences": occ})
    return out


def pair_matrix(formula: list[tuple[int, int, int]]) -> list[dict]:
    out = []
    for j in range(len(formula)):
        for k in range(j + 1, len(formula)):
            c, d = formula[j], formula[k]
            same = any(lit in d for lit in c)
            opposite = any(-lit in d for lit in c)
            out.append({
                "clauses": [j, k],
                "shared_same": same,
                "shared_opposite": opposite,
                "SS": not opposite,
                "SU": not same,
                "US": not same,
                "UU": not opposite,
            })
    return out


def flip_trail(formula: list[tuple[int, int, int]], nvars: int) -> list[dict]:
    full = (1 << nvars) - 1
    seq = [0, 1, 3, full, 0]
    return [
        {
            "assignment": a,
            "histogram_N0_N1_N2_N3": counts(formula, a),
            "SAT": counts(formula, a)[0] == 0,
            "complement_SAT": counts(formula, a)[3] == 0,
        }
        for a in seq
    ]


def dpll(formula: list[tuple[int, int, int]], nvars: int) -> dict:
    stats = {"nodes": 0, "clause_visits": 0, "literal_tests": 0, "branches": 0}

    def rec(assignment: list[int]) -> list[int] | None:
        stats["nodes"] += 1
        a = assignment[:]
        while True:
            unit = None
            all_sat = True
            for clause in formula:
                stats["clause_visits"] += 1
                sat = False
                unknown = []
                for lit in clause:
                    stats["literal_tests"] += 1
                    value = a[abs(lit)]
                    if value < 0:
                        unknown.append(lit)
                    elif value == (1 if lit > 0 else 0):
                        sat = True
                        break
                if sat:
                    continue
                all_sat = False
                if not unknown:
                    return None
                if len(unknown) == 1:
                    lit = unknown[0]
                    unit = (abs(lit), 1 if lit > 0 else 0)
                    break
            if all_sat:
                return [0 if x < 0 else x for x in a]
            if unit is None:
                break
            v, b = unit
            if a[v] >= 0 and a[v] != b:
                return None
            a[v] = b
        v = next(i for i in range(1, nvars + 1) if a[i] < 0)
        stats["branches"] += 1
        for b in (0, 1):
            child = a[:]
            child[v] = b
            answer = rec(child)
            if answer is not None:
                return answer
        return None

    witness = rec([-1] * (nvars + 1))
    return {"SAT": witness is not None, "stats": stats, "witness": witness[1:] if witness else None}


def inverse_positions(pi: tuple[int, ...]) -> list[int]:
    inv = [0] * len(pi)
    for pos, value in enumerate(pi):
        inv[value] = pos
    return inv


def memo_strategy(pi: tuple[int, ...], rounds: list[list[int]]) -> dict:
    cache: dict[int, int] = {}
    probes = 0
    outputs = []
    round_probes = []
    for queries in rounds:
        before = probes
        missing = {value for value in queries if value not in cache}
        if missing:
            for pos, seen in enumerate(pi):
                probes += 1
                if seen in missing:
                    cache[seen] = pos
                    missing.remove(seen)
                    if not missing:
                        break
        row = []
        for value in queries:
            row.append(cache[value])
        outputs.append(row)
        round_probes.append(probes - before)
    return {
        "outputs": outputs,
        "source_word_probes": probes,
        "round_probes": round_probes,
        "cache_entries": len(cache),
        "cache_bits": len(cache) * math.ceil(math.log2(len(pi))),
    }


def naive_round_scan(pi: tuple[int, ...], rounds: list[list[int]]) -> int:
    probes = 0
    for queries in rounds:
        missing = set(queries)
        for seen in pi:
            probes += 1
            missing.discard(seen)
            if not missing:
                break
    return probes


def falling(m: int, t: int) -> int:
    answer = 1
    for j in range(t):
        answer *= m - j
    return answer


def schedule_audit(name: str, rounds: list[list[int]], m: int = 8) -> dict:
    union = sorted(set(itertools.chain.from_iterable(rounds)))
    t = len(union)
    lower = math.log2(falling(m, t))
    max_memo = 0
    max_naive = 0
    min_memo = 10**9
    sum_memo = 0
    permutations = 0
    sample = None
    for pi in itertools.permutations(range(m)):
        inv = inverse_positions(pi)
        memo = memo_strategy(pi, rounds)
        expected = [[inv[v] for v in row] for row in rounds]
        assert memo["outputs"] == expected
        naive = naive_round_scan(pi, rounds)
        max_memo = max(max_memo, memo["source_word_probes"])
        min_memo = min(min_memo, memo["source_word_probes"])
        max_naive = max(max_naive, naive)
        sum_memo += memo["source_word_probes"]
        permutations += 1
        if pi == tuple(range(m)):
            sample = {"permutation": list(pi), "memo": memo, "naive_probes": naive}
    word_bits = math.ceil(math.log2(m))
    # The actual transcript bound depends on distinct demanded answers, not rounds.
    assert max_memo * math.log2(m) >= lower
    fake_multiplied_rhs = len(rounds) * lower
    available_bits_at_worst = max_memo * word_bits + t * word_bits
    return {
        "name": name,
        "rounds": rounds,
        "round_count": len(rounds),
        "union": union,
        "distinct_demands_t": t,
        "permutations_exhausted": permutations,
        "exact_union_information_bits": lower,
        "memo_probe_min": min_memo,
        "memo_probe_max": max_memo,
        "memo_probe_average": sum_memo / permutations,
        "naive_round_scan_probe_max": max_naive,
        "word_bits": word_bits,
        "cache_bits": t * word_bits,
        "actual_bound_lhs_at_max": max_memo * math.log2(m),
        "invalid_round_multiplied_rhs": fake_multiplied_rhs,
        "memo_probe_plus_cache_bits": available_bits_at_worst,
        "invalid_round_multiplier_falsified": available_bits_at_worst < fake_multiplied_rhs,
        "sample_identity": sample,
    }


def sign_clause(mask: int) -> tuple[int, int, int]:
    # Clause falsified by the assignment encoded by mask.
    return tuple(-v if (mask >> (v - 1)) & 1 else v for v in (1, 2, 3))


def case(name: str, formula: list[tuple[int, int, int]], nvars: int) -> dict:
    mods = models(formula, nvars)
    solver = dpll(formula, nvars)
    assert solver["SAT"] == bool(mods)
    h0, h1 = counts(formula, 0), counts(formula, (1 << nvars) - 1)
    assert h0 == list(reversed(h1))
    return {
        "name": name,
        "nvars": nvars,
        "clauses": len(formula),
        "SAT": bool(mods),
        "model_count": len(mods),
        "dpll": solver,
        "local_targets": extrema(formula),
        "pair_compatibility": pair_matrix(formula),
        "endpoints": {"zero": h0, "one": h1},
        "flip_trail": flip_trail(formula, nvars),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    # Seven of eight sign patterns leave one assignment on x1,x2,x3; the
    # eighth clause is on fresh variables and leaves seven complete models.
    sat_formula = [sign_clause(mask) for mask in range(7)] + [(4, 5, 6)]
    unsat_formula = [sign_clause(mask) for mask in range(8)]
    schedules = [
        schedule_audit("sixteen_repeated_children", [[0, 1]] * 16),
        schedule_audit("overlapping_children", [[0, 1], [1, 2], [2, 3], [0, 3]]),
        schedule_audit("disjoint_cover", [[0, 1], [2, 3], [4, 5], [6, 7]]),
    ]
    assert schedules[0]["invalid_round_multiplier_falsified"]
    assert not schedules[1]["invalid_round_multiplier_falsified"]  # no claim either way

    cases = [
        case("ordered_clause_metadata_SAT", sat_formula, 6),
        case("ordered_clause_metadata_UNSAT", unsat_formula, 3),
    ]
    assert cases[0]["SAT"] and not cases[1]["SAT"]
    result = {
        "id": "ARC-BATCH-UNION-PROBE-FIREWALL227",
        "date": "2026-10-30 America/Los_Angeles",
        "status": {
            "batch_union_bound": "PROVED/EXACT restricted transcript theorem",
            "round_multiplication": "FALSIFIED/RETIRED without fresh-demand independence",
            "finite_audit": "COMPUTATIONAL",
            "ARC": "OPEN",
            "P_vs_NP": "OPEN",
        },
        "claim": "For q online child rounds whose union contains t distinct inverse-permutation demands, transcript counting yields s+Q log2(m) >= log2((m)_t); q is absent unless fresh independent demand is proved.",
        "schedules": schedules,
        "source_cases": cases,
        "charged_scope": [
            "source word probes",
            "cached inverse-answer bits",
            "query outputs",
            "DPLL nodes, clause visits, literal tests and branches",
        ],
        "limitations": [
            "Clause-order metadata is an easy restricted interface, not SAT hardness.",
            "Host-language probe counts are not native FLMV instructions.",
            "The theorem gives no power-short ordinary-SAT child.",
            "A direct-sum factor requires a separately proved fresh independent-demand hypothesis.",
        ],
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
