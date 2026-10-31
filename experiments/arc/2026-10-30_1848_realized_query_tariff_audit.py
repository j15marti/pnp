#!/usr/bin/env python3
"""Realized-query tariff firewall 230.

The experiment keeps the exact canonical proper-3CNF A_f family used by
firewalls 228--229 and wraps its one-word point accessor in deliberately
different *correct* executions.  All wrappers compute the same answer on the
same YES/NO source family, but have the same distinct-source-address count and
widely different charged work or peak live storage.  This is a finite control
for the theorem that distinct source addresses alone cannot certify an ARC
time/space recurrence.

The counters below are explicitly selected abstract bit-machine events, not
native FLMV measurements.  They separate address-generation work, source
reads, output writes, guest steps, retained bits, and strategy/failure work.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
PREVIOUS = HERE / "2026-10-30_1748_source_retention_quantifier_audit.py"


def load_previous():
    spec = importlib.util.spec_from_file_location("firewall229", PREVIOUS)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {PREVIOUS}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


P229 = load_previous()
P228 = P229.P


def source_bits_fixed_width(clauses: list[list[int]]) -> int:
    max_var = max(abs(lit) for clause in clauses for lit in clause)
    index_bits = max(1, max_var.bit_length())
    # One sign bit plus a fixed-width identifier for every literal word.
    return sum(len(clause) for clause in clauses) * (index_bits + 1)


def answer_and_address(mask: int, b: int, a: int):
    clauses, _, _ = P228.build_padded_formula(mask, b)
    answer, probe = P229.indexed_decode(clauses, a, b)
    assert answer == P228.bit(mask, a)
    return clauses, answer, probe["clause_address"]


def trace_row(name: str, answer: int, addresses: list[int], *,
              address_steps: int, delay_steps: int = 0,
              output_writes: int = 1, guest_steps: int = 0,
              failed_strategy_steps: int = 0,
              retained_bits_peak: int = 0,
              child_buffer_bits_peak: int = 0):
    source_reads = len(addresses)
    distinct = len(set(addresses))
    work = (address_steps + delay_steps + source_reads + output_writes
            + guest_steps + failed_strategy_steps)
    peak = max(retained_bits_peak, child_buffer_bits_peak)
    return {
        "policy": name,
        "answer": answer,
        "distinct_source_addresses": distinct,
        "source_reads_including_repeats": source_reads,
        "address_generation_steps": address_steps,
        "delay_steps": delay_steps,
        "output_writes": output_writes,
        "guest_steps": guest_steps,
        "failed_strategy_steps": failed_strategy_steps,
        "selected_total_work": work,
        "retained_bits_peak": retained_bits_peak,
        "child_buffer_bits_peak": child_buffer_bits_peak,
        "selected_peak_live_bits": peak,
    }


def policy_controls(mask: int, b: int, a: int):
    clauses, answer, address = answer_and_address(mask, b, a)
    nbits = source_bits_fixed_width(clauses)
    q = 128
    child_count = 32
    child_bits = 256
    rows = []
    rows.append(trace_row(
        "direct_one_probe", answer, [address], address_steps=b + 1))
    rows.append(trace_row(
        "delay_2^12_then_one_probe", answer, [address],
        address_steps=b + 1, delay_steps=1 << 12))
    rows.append(trace_row(
        "repeat_same_probe_no_cache", answer, [address] * q,
        address_steps=q * (b + 1), output_writes=q))
    rows.append(trace_row(
        "repeat_same_query_cached", answer, [address],
        address_steps=q * (b + 1), output_writes=q,
        retained_bits_peak=b + 1))
    rows.append(trace_row(
        "one_probe_materialize_32_children", answer, [address],
        address_steps=b + 1, output_writes=child_count * child_bits,
        child_buffer_bits_peak=child_bits))
    rows.append(trace_row(
        "one_probe_retain_32_ancestor_records", answer, [address],
        address_steps=b + 1, output_writes=1,
        retained_bits_peak=child_count * child_bits))
    rows.append(trace_row(
        "compiler_zero_probe_parent_fallback", answer, [],
        address_steps=0, guest_steps=nbits * nbits,
        child_buffer_bits_peak=nbits))
    return {
        "mask": mask,
        "b": b,
        "point": a,
        "answer": answer,
        "source_clauses": len(clauses),
        "source_bits_fixed_width": nbits,
        "rows": rows,
    }


def exponent_case(name: str, alpha, gamma, lam, nu, k, sigma, ell,
                  omitted=Fraction(0, 1)):
    time_claim = max(alpha, gamma + nu + lam * k)
    true_with_omitted = max(time_claim, omitted)
    space = max(sigma, lam * ell)
    return {
        "case": name,
        "alpha": str(alpha),
        "gamma": str(gamma),
        "lambda": str(lam),
        "nu": str(nu),
        "guest_K": str(k),
        "sigma": str(sigma),
        "guest_L": str(ell),
        "omitted_realized_cost_exponent": str(omitted),
        "claimed_K_prime_without_omitted_term": str(time_claim),
        "charged_K_prime": str(true_with_omitted),
        "charged_L_prime": str(space),
        "omission_changes_time_bound": omitted > time_claim,
    }


def clause_controls(mask: int, b: int):
    c = P228.source_control("same_family_control", mask, b)
    # Keep only compact exact fields needed by the independent checker/report.
    return {
        "SAT": c["SAT"],
        "boundary_model_count": mask.bit_count(),
        "dpll_answer": c["SAT"],
        "dpll_nodes": c["dpll"]["nodes"],
        "occurrence_extreme_checks": len(c["local_targets"]),
        "pair_mode_checks": 4 * len(c["pair_compatibility"]),
        "complement_checks": len(c["flip_trail"]),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    b = 4
    a = 15
    sat_mask = 1 << a
    unsat_mask = 0
    sat = policy_controls(sat_mask, b, a)
    unsat = policy_controls(unsat_mask, b, a)
    assert sat["answer"] == 1 and unsat["answer"] == 0
    assert [r["policy"] for r in sat["rows"]] == [r["policy"] for r in unsat["rows"]]
    for sr, ur in zip(sat["rows"], unsat["rows"]):
        # Resource ledgers are label-blind for this paired family.
        for key in sr:
            if key != "answer":
                assert sr[key] == ur[key]

    exponent_cases = [
        exponent_case("declared_controller_no_omission", Fraction(11, 10),
                      Fraction(3, 5), Fraction(1, 2), Fraction(0),
                      Fraction(6, 5), Fraction(1, 2), Fraction(1, 2)),
        exponent_case("same_union_hidden_delay", Fraction(11, 10),
                      Fraction(3, 5), Fraction(1, 2), Fraction(0),
                      Fraction(6, 5), Fraction(1, 2), Fraction(1, 2),
                      Fraction(7, 5)),
        exponent_case("same_union_hidden_output", Fraction(11, 10),
                      Fraction(3, 5), Fraction(1, 2), Fraction(0),
                      Fraction(6, 5), Fraction(1, 2), Fraction(1, 2),
                      Fraction(13, 10)),
    ]

    result = {
        "id": "ARC-REALIZED-QUERY-TARIFF-FIREWALL230",
        "date": "2026-10-30 18:48 America/Los_Angeles",
        "status": {
            "realized_trace_composition_lemma": "PROVED/EXACT restricted declared controller",
            "small_distinct_probe_union_implies_ARC": "FALSIFIED/RETIRED",
            "finite_controls": "COMPUTATIONAL",
            "arbitrary_A_to_Phi_A": "OPEN",
            "P_vs_NP": "OPEN",
        },
        "falsified_claim": (
            "A small union of distinct original-source addresses, by itself, "
            "upper-bounds controller time or peak space and therefore certifies "
            "a hereditary ARC contraction."
        ),
        "paired_same_family_controls": {"SAT": sat, "UNSAT": unsat},
        "symbolic_exponent_controls": exponent_cases,
        "same_source_clause_extreme_and_dpll_controls": {
            "SAT": clause_controls(sat_mask, b),
            "UNSAT": clause_controls(unsat_mask, b),
        },
        "exact_ledger_identity": (
            "selected_total_work = address_generation + delay + all_source_reads "
            "+ output_writes + guest_steps + failed_strategy_steps"
        ),
        "interpretation": [
            "Distinct-address union U is at most the total number R of source reads, but U gives no upper bound on R.",
            "Even R=1 gives no upper bound on address-generation/delay work, output volume, guest work, or retained live bits.",
            "The delay and repeated-read wrappers are algorithm controls, not unavoidable lower bounds for every algorithm.",
            "The parent fallback has compiler-layer U=0 but retains the original input scale and therefore gives no ARC shrinkage.",
            "The selected counters are reproducible abstract events, not native FLMV machine timings.",
        ],
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
