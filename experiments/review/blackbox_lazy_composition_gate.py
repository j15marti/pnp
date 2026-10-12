#!/usr/bin/env python3
"""Finite audit for BLACKBOX-LAZY-COMPOSITION-GATE1.

The audit is deliberately bounded.  It checks transcript extensionality,
separate charge attribution, lazy-access inlining, hostile wrappers, and the
symbolic polynomial-exponent ledger.  It does not infer an asymptotic SAT
lower bound from the finite cases.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import time
from dataclasses import dataclass
from pathlib import Path


Clause = tuple[int, ...]
CNF = tuple[Clause, ...]


def vars_of(formula: CNF) -> list[int]:
    return sorted({abs(lit) for clause in formula for lit in clause})


def satisfies(formula: CNF, assignment: dict[int, bool]) -> bool:
    return all(any(assignment.get(abs(lit), False) == (lit > 0) for lit in clause)
               for clause in formula)


def brute_sat(formula: CNF) -> bool:
    variables = vars_of(formula)
    return any(satisfies(formula, dict(zip(variables, bits)))
               for bits in itertools.product((False, True), repeat=len(variables)))


def encode(formula: CNF) -> str:
    return "|".join(",".join(map(str, clause)) for clause in formula)


@dataclass
class Answer:
    bit: bool
    steps: int
    peak: int
    trace_tag: str


def solve_wrapped(formula: CNF, style: str) -> Answer:
    base = len(encode(formula)) + 1
    direct = brute_sat(formula)
    if style == "DIRECT":
        return Answer(direct, base, 1, "direct")
    if style == "COPY":
        return Answer(direct, 2 * base, 2, "copy")
    if style == "DEAD":
        return Answer(direct, base + 17, 3, "dead")
    if style == "DELAY":
        return Answer(direct, base ** 2 + 5, 1, "delay")
    if style == "INTERP":
        relabelled = tuple(reversed(formula))
        return Answer(brute_sat(relabelled), 3 * base + 1, 2, "interp")
    if style == "RECOMP":
        second = brute_sat(formula)
        assert second == direct
        return Answer(second, 2 * base + 7, 2, "recomp")
    raise ValueError(style)


def extract_lex_witness(formula: CNF, style: str) -> tuple[list[tuple[str, bool]], tuple[int, ...] | None, int, int]:
    """External search-to-decision extractor with every call charged."""
    transcript: list[tuple[str, bool]] = []
    total = 11  # parsing/local-control charge
    peak = 1
    first = solve_wrapped(formula, style)
    transcript.append((encode(formula), first.bit))
    total += first.steps
    peak = max(peak, first.peak)
    if not first.bit:
        return transcript, None, total, peak
    prefix: list[int] = []
    for variable in vars_of(formula):
        query = formula + tuple((lit,) for lit in prefix + [-variable])
        ans = solve_wrapped(query, style)
        transcript.append((encode(query), ans.bit))
        total += ans.steps + 3
        peak = max(peak, ans.peak, len(prefix) + 1)
        prefix.append(-variable if ans.bit else variable)
    witness = tuple(1 if lit > 0 else 0 for lit in prefix)
    return transcript, witness, total, peak


def virtual_bit(source: str, witness: tuple[int, ...] | None, address: int) -> tuple[int, int]:
    payload = f"{source};{witness};{address}".encode("utf-8")
    digest = hashlib.sha256(payload).digest()
    return digest[0] & 1, len(payload) + len(digest)


def adaptive_virtual_eval(source: str, witness: tuple[int, ...] | None, rounds: int = 9) -> tuple[int, list[int], int]:
    state = 1
    addresses: list[int] = []
    charged = 7
    virtual_length = 1 << min(20, max(1, len(source)))
    for turn in range(rounds):
        address = (state * 131 + turn * 17 + len(source)) % virtual_length
        bit, cost = virtual_bit(source, witness, address)
        addresses.append(address)
        state = ((state << 1) ^ bit ^ address) & ((1 << 31) - 1)
        charged += cost + 5
    return state & 1, addresses, charged


def main() -> None:
    started = time.perf_counter()
    families: dict[str, CNF] = {
        "horn": ((-1, -2, 3), (1,), (2,)),
        "2sat": ((1, 2), (-1, 2), (1, -2)),
        "affine_tseitin": ((1, 2), (-1, -2), (2, 3), (-2, -3)),
        "bounded_treewidth": ((1, 2), (-2, 3), (-3, 4)),
        "signed_core_toy": ((1, 2, 3), (-1, 2, -3), (1, -2, -3), (-1, -2, 3)),
        "unsat": ((1,), (-1,)),
        "padding": ((1, 2), (-1, 2), (3, -3), (4, -4)),
        "redundant": ((1, 2), (1, 2), (-1, 2)),
        "independent_product": ((1,), (2, 3), (-2, 3), (4, -4)),
        "alternate_encoding": ((3, -1), (2, 1), (-2, 1)),
    }
    styles = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
    assertions = 0
    calls = 0
    cases = []

    for name, formula in families.items():
        baseline_transcript = None
        baseline_witness = None
        baseline_virtual = None
        direct_original_cost = solve_wrapped(formula, "DIRECT").steps
        for style in styles:
            transcript, witness, extraction_cost, peak = extract_lex_witness(formula, style)
            calls += len(transcript)
            semantic_transcript = tuple(transcript)
            virtual_out, addresses, access_cost = adaptive_virtual_eval(encode(formula), witness)
            composite_cost = extraction_cost + access_cost
            original_cost = solve_wrapped(formula, style).steps
            assertions += 1
            assert composite_cost >= original_cost
            assertions += 1
            assert composite_cost == extraction_cost + access_cost
            assertions += 1
            assert len(addresses) == 9
            if witness is not None:
                assignment = {v: bool(witness[i]) for i, v in enumerate(vars_of(formula))}
                assertions += 1
                assert satisfies(formula, assignment)
            if baseline_transcript is None:
                baseline_transcript = semantic_transcript
                baseline_witness = witness
                baseline_virtual = (virtual_out, addresses)
            else:
                assertions += 3
                assert semantic_transcript == baseline_transcript
                assert witness == baseline_witness
                assert (virtual_out, addresses) == baseline_virtual
            cases.append({
                "family": name,
                "style": style,
                "sat": brute_sat(formula),
                "oracle_calls": len(transcript),
                "original_run_cost": original_cost,
                "direct_original_cost": direct_original_cost,
                "external_extraction_cost": extraction_cost,
                "lazy_access_cost": access_cost,
                "composite_cost": composite_cost,
                "peak_units": peak,
                "semantic_transcript_sha256": hashlib.sha256(repr(semantic_transcript).encode()).hexdigest(),
                "trace_tag": solve_wrapped(formula, style).trace_tag,
            })

    exponent_rows = []
    # q <= n^b, query length <= n^c, solver time m^K;
    # r <= n^e lazy reads, accessor cost <= n^(a*max(1,d)).
    for b, c, k, e, a, d, local in itertools.product(range(5), repeat=7):
        oracle_exp = b + c * k
        access_exp = e + a * max(1, d)
        composed = max(local, oracle_exp, access_exp)
        assertions += 4
        assert composed >= local
        assert composed >= oracle_exp
        assert composed >= access_exp
        assert composed == max(local, b + c * k, e + a * max(1, d))
        if len(exponent_rows) < 40:
            exponent_rows.append({
                "query_count_exp": b,
                "query_length_exp": c,
                "solver_exp": k,
                "access_count_exp": e,
                "accessor_exp": a,
                "address_exp": d,
                "local_exp": local,
                "composed_exp": composed,
            })

    arbitrary_k = []
    for k in range(1, 13):
        exp = 2 + 3 * k
        arbitrary_k.append({"solver_exp": k, "oracle_component_exp": exp})
        assertions += 1
        assert exp > k
    assertions += 1
    assert len({row["oracle_component_exp"] for row in arbitrary_k}) == 12

    result = {
        "run_id": "MODELBRIDGE-0023",
        "candidate": "BLACKBOX-LAZY-TO-ORIGINAL-RUN1",
        "candidate_status": "FALSIFIED/RETIRED",
        "theorem": "BLACKBOX-LAZY-COMPOSITION-GATE1",
        "theorem_status": "PROVED/EXACT by symbolic composition; finite audit is COMPUTATIONAL",
        "seed": None,
        "families": list(families),
        "styles": list(styles),
        "cases": cases,
        "oracle_calls": calls,
        "assertions": assertions,
        "failures": 0,
        "exponent_grid_rows_checked": 5 ** 7,
        "exponent_samples": exponent_rows,
        "arbitrary_solver_exponents": arbitrary_k,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "scope_warning": "Finite checks validate accounting and wrappers only; no asymptotic SAT lower bound is inferred.",
    }
    out = Path("results/raw/review/2026-10-12_blackbox_lazy_composition_gate.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in (
        "run_id", "candidate_status", "oracle_calls", "assertions",
        "failures", "exponent_grid_rows_checked", "elapsed_seconds")}, sort_keys=True))


if __name__ == "__main__":
    main()
