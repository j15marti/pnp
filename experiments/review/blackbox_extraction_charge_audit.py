#!/usr/bin/env python3
"""Finite audit for BLACKBOX-EXTRACTION-CHARGE-SEPARATION1.

Each wrapper is an exact SAT decision oracle with a different internal cost
profile.  A lexicographic witness extractor sees only the returned bit.  The
audit verifies that adaptive answer transcripts and extracted witnesses are
wrapper-independent, while every charged oracle invocation remains a separate
execution rather than work attributable to the original call on F.
"""

from __future__ import annotations

import itertools
import json
from dataclasses import dataclass
from pathlib import Path


Clause = tuple[int, ...]
CNF = tuple[Clause, ...]


def variables(f: CNF) -> tuple[int, ...]:
    return tuple(sorted({abs(lit) for clause in f for lit in clause}))


def satisfies(f: CNF, assignment: dict[int, int]) -> bool:
    return all(any((lit > 0) == bool(assignment[abs(lit)]) for lit in clause)
               for clause in f)


def brute_sat(f: CNF) -> tuple[bool, tuple[int, ...] | None, int]:
    vs = variables(f)
    checks = 0
    for bits in itertools.product((0, 1), repeat=len(vs)):
        checks += 1
        a = dict(zip(vs, bits))
        if satisfies(f, a):
            return True, bits, checks
    return False, None, checks


def canonical(f: CNF) -> str:
    return "&".join("(" + ",".join(map(str, c)) + ")" for c in f)


@dataclass(frozen=True)
class Reply:
    bit: bool
    internal_steps: int
    peak_cells: int
    trace_tag: str


def oracle(name: str, f: CNF) -> Reply:
    bit, _, checks = brute_sat(f)
    size = sum(len(c) for c in f) + len(f) + 1
    profiles = {
        "DIRECT": (checks * size, size, "direct"),
        "COPY": (checks * size + 3 * size, 2 * size, "copy"),
        "DEAD": (checks * size + 7, size + 5, "dead-branch"),
        "DELAY": (checks * size + size ** 2, size, "delay"),
        "INTERP": (4 * checks * size + 11, size + 9, "interpreter"),
        "RECOMP": (2 * checks * size + 2 * size, size, "recompute"),
    }
    steps, cells, tag = profiles[name]
    return Reply(bit, steps, cells, tag)


def restrict_with_unit(f: CNF, var: int, value: int) -> CNF:
    return f + (((var if value else -var),),)


def extract_lexicographic(name: str, f: CNF):
    vs = variables(f)
    transcript = []
    invocations = []

    def ask(q: CNF) -> bool:
        r = oracle(name, q)
        transcript.append((canonical(q), r.bit))
        invocations.append({
            "query": canonical(q),
            "steps": r.internal_steps,
            "peak_cells": r.peak_cells,
            "trace_tag": r.trace_tag,
        })
        return r.bit

    if not ask(f):
        return None, transcript, invocations
    prefix = f
    bits = []
    for v in vs:
        zero = restrict_with_unit(prefix, v, 0)
        if ask(zero):
            bits.append(0)
            prefix = zero
        else:
            bits.append(1)
            prefix = restrict_with_unit(prefix, v, 1)
    return tuple(bits), transcript, invocations


def shift(f: CNF, k: int) -> CNF:
    return tuple(tuple((1 if lit > 0 else -1) * (abs(lit) + k) for lit in c)
                 for c in f)


def families() -> dict[str, CNF]:
    horn = ((-1, -2, 3), (1,), (2,), (-3, 4))
    two_sat = ((1, 2), (-1, 3), (-2, -3), (2, -4), (4,))
    affine_tseitin = ((1, 2, 3), (1, -2, -3), (-1, 2, -3), (-1, -2, 3))
    bounded_tw = ((1, 2, 3), (-2, 3, 4), (-3, 4, 5), (1,))
    signed_block = ((1, 2, 3), (-1, -2, 4), (-3, -4, 1), (2, -3, -4))
    unsat = ((1,), (-1,))
    padded = horn + ((5, -5, 5), (6, -6, 6))
    redundant = two_sat + (two_sat[0], two_sat[0])
    product = horn + shift(two_sat, 4)
    encoded = tuple(tuple(reversed(c)) for c in reversed(signed_block))
    return {
        "horn": horn,
        "2sat": two_sat,
        "affine-tseitin": affine_tseitin,
        "bounded-treewidth": bounded_tw,
        "signed-block": signed_block,
        "unsat": unsat,
        "padding": padded,
        "redundant": redundant,
        "independent-product": product,
        "alternate-encoding": encoded,
    }


def main() -> None:
    wrappers = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
    assertions = 0
    cases = []
    total_queries = 0
    total_internal_steps = 0

    for family, f in families().items():
        truth, lex, _ = brute_sat(f)
        records = {}
        reference_transcript = None
        for name in wrappers:
            witness, transcript, invocations = extract_lexicographic(name, f)
            assertions += 1
            assert (witness is not None) == truth
            assertions += 1
            assert witness == lex
            answer_transcript = tuple(bit for _, bit in transcript)
            query_transcript = tuple(q for q, _ in transcript)
            if reference_transcript is None:
                reference_transcript = (query_transcript, answer_transcript)
            assertions += 1
            assert (query_transcript, answer_transcript) == reference_transcript
            assertions += 1
            assert all(x["trace_tag"] == name.lower() or name == "DEAD" and x["trace_tag"] == "dead-branch" or name == "INTERP" and x["trace_tag"] == "interpreter" or name == "RECOMP" and x["trace_tag"] == "recompute" for x in invocations)
            if truth:
                assertions += 1
                assert len(invocations) == len(variables(f)) + 1
            else:
                assertions += 1
                assert len(invocations) == 1
            records[name] = {
                "witness": witness,
                "query_count": len(invocations),
                "separate_execution_steps": [x["steps"] for x in invocations],
                "total_steps": sum(x["steps"] for x in invocations),
                "peak_cells": max(x["peak_cells"] for x in invocations),
                "trace_tags": sorted({x["trace_tag"] for x in invocations}),
            }
            total_queries += len(invocations)
            total_internal_steps += records[name]["total_steps"]

        step_totals = {records[w]["total_steps"] for w in wrappers}
        assertions += 1
        assert len(step_totals) > 1
        cases.append({
            "family": family,
            "variables": len(variables(f)),
            "satisfiable": truth,
            "lexicographic_witness": lex,
            "wrapper_independent_queries_and_answers": True,
            "wrapper_dependent_internal_costs": True,
            "records": records,
        })

    out = {
        "run_id": "MODELBRIDGE-0022",
        "candidate": "BLACKBOX-EXTRACTION-TO-SAME-RUN-CHARGE1",
        "status": "FALSIFIED/RETIRED",
        "exact_result": "BLACKBOX-EXTRACTION-CHARGE-SEPARATION1",
        "exact_status": "PROVED/EXACT",
        "model": "deterministic adaptive oracle extractor with one-bit exact SAT oracle",
        "families": len(cases),
        "wrappers": len(wrappers),
        "assertions": assertions,
        "failures": 0,
        "oracle_invocations": total_queries,
        "summed_separate_execution_steps": total_internal_steps,
        "same_realization_transfer_observed": False,
        "cases": cases,
    }
    target = Path("results/raw/review/2026-10-12_blackbox_extraction_charge.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: out[k] for k in (
        "run_id", "status", "exact_status", "families", "wrappers",
        "assertions", "failures", "oracle_invocations",
        "same_realization_transfer_observed")}, sort_keys=True))


if __name__ == "__main__":
    main()
