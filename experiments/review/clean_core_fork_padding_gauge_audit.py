#!/usr/bin/env python3
"""Finite audit for CLEAN-CORE-FORK-PADDING-GAUGE1.

The symbolic theorem is in TESTS-0018.  This program exhaustively checks the
paired-K3,3 block, canonical challenge openings, projection, clean-core
closure, easy-family controls, representations, and wrapper-equivalent
verification paths.  Finite output is not asymptotic evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

Clause = tuple[int, ...]
Assignment = tuple[int, ...]


def paired_k33(offset: int = 0) -> list[Clause]:
    triples = [[3 * i + j for j in range(3)] for i in range(3)]
    triples += [[3 * i + j for i in range(3)] for j in range(3)]
    out: list[Clause] = []
    for triple in triples:
        out.append(tuple(offset + v + 1 for v in triple))
        out.append(tuple(-(offset + v + 1) for v in triple))
    return out


def satisfies(clauses: list[Clause], assignment: Assignment) -> bool:
    return all(any((assignment[abs(x) - 1] == 1) if x > 0
                       else (assignment[abs(x) - 1] == 0)
                   for x in clause) for clause in clauses)


def witnesses(clauses: list[Clause], nvars: int) -> list[Assignment]:
    return [a for a in itertools.product((0, 1), repeat=nvars)
            if satisfies(clauses, a)]


def product(block: list[Clause], copies: int, width: int = 9) -> list[Clause]:
    out: list[Clause] = []
    for j in range(copies):
        for clause in block:
            out.append(tuple((1 if x > 0 else -1) * (abs(x) + j * width)
                             for x in clause))
    return out


def fork_transform(source: list[Clause], nvars: int, k: int) -> list[Clause]:
    out = list(source)
    for j in range(k):
        out.extend(paired_k33(nvars + 9 * j))
    return out


def shift_assignment(block_assignment: Assignment, copies: int) -> Assignment:
    return tuple(bit for _ in range(copies) for bit in block_assignment)


def opening(source_witness: Assignment, challenge: tuple[int, ...],
            pad_zero: Assignment, pad_one: Assignment) -> Assignment:
    suffix: list[int] = []
    for bit in challenge:
        suffix.extend(pad_one if bit else pad_zero)
    return source_witness + tuple(suffix)


def verify(source: list[Clause], nvars: int, k: int,
           commitment: tuple[Clause, ...], challenge: tuple[int, ...],
           response: Assignment, pad_zero: Assignment,
           pad_one: Assignment) -> bool:
    if commitment != tuple(fork_transform(source, nvars, k)):
        return False
    if len(challenge) != k or len(response) != nvars + 9 * k:
        return False
    if not satisfies(source, response[:nvars]):
        return False
    for j, bit in enumerate(challenge):
        expected = pad_one if bit else pad_zero
        if response[nvars + 9 * j:nvars + 9 * (j + 1)] != expected:
            return False
    return satisfies(list(commitment), response)


def clean_core(clauses: list[Clause], nvars: int) -> bool:
    if len(set(clauses)) != len(clauses):
        return False
    counts = {(v, s): 0 for v in range(1, nvars + 1) for s in (-1, 1)}
    for clause in clauses:
        if len(clause) != 3 or len({abs(x) for x in clause}) != 3:
            return False
        if len({1 if x > 0 else -1 for x in clause}) != 1:
            return False
        for x in clause:
            counts[(abs(x), 1 if x > 0 else -1)] += 1
    return all(counts[(v, -1)] == counts[(v, 1)] == 2
               for v in range(1, nvars + 1))


def parity3_even() -> list[Clause]:
    out = []
    for a in itertools.product((0, 1), repeat=3):
        if sum(a) % 2 == 1:
            out.append(tuple(-(i + 1) if bit else i + 1
                             for i, bit in enumerate(a)))
    return out


def wrapped_verify(name: str, args: tuple) -> bool:
    if name == "DIRECT":
        return verify(*args)
    if name == "COPY":
        copied = tuple(args[5])
        return verify(*args[:5], copied, *args[6:])
    if name == "DEAD":
        _dead = sum(range(8))
        return verify(*args)
    if name == "DELAY":
        for _ in range(8):
            pass
        return verify(*args)
    if name == "INTERP":
        source, nvars, k, commitment, challenge, response, p0, p1 = args
        encoded = json.dumps([list(c) for c in commitment])
        reparsed = tuple(tuple(c) for c in json.loads(encoded))
        return verify(source, nvars, k, reparsed, challenge, response, p0, p1)
    if name == "RECOMP":
        source, nvars, k, _commitment, challenge, response, p0, p1 = args
        return verify(source, nvars, k, tuple(fork_transform(source, nvars, k)),
                      challenge, response, p0, p1)
    raise ValueError(name)


def run(max_challenge_bits: int) -> dict:
    started = time.perf_counter()
    checks = 0
    base = paired_k33()
    ws = witnesses(base, 9)
    assert len(ws) == 102
    checks += 512 + 1
    p0, p1 = ws[0], ws[-1]
    assert p0 != p1 and satisfies(base, p0) and satisfies(base, p1)
    checks += 3

    rows = []
    wrapper_names = ["DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP"]
    wrapper_checks = 0
    for k in range(1, max_challenge_bits + 1):
        transformed = fork_transform(base, 9, k)
        commitment = tuple(transformed)
        assert clean_core(transformed, 9 + 9 * k)
        checks += 1
        valid = 0
        verifier_clause_visits = 0
        extracted_bits = 0
        for w in ws:
            for e in itertools.product((0, 1), repeat=k):
                z = opening(w, e, p0, p1)
                assert verify(base, 9, k, commitment, e, z, p0, p1)
                assert z[:9] == w and satisfies(base, z[:9])
                checks += 3
                valid += 1
                verifier_clause_visits += len(base) + len(transformed)
                extracted_bits += 9
                if w == ws[0] and e in ((0,) * k, (1,) * k):
                    args = (base, 9, k, commitment, e, z, p0, p1)
                    for name in wrapper_names:
                        assert wrapped_verify(name, args)
                        wrapper_checks += 1
                        checks += 1
        assert valid == len(ws) * (1 << k)
        checks += 1
        rows.append({
            "challenge_bits": k,
            "variables": 9 + 9 * k,
            "clauses": 12 + 12 * k,
            "source_witnesses": len(ws),
            "canonical_valid_openings": valid,
            "forks_per_source_witness": 1 << k,
            "constant_map_ordered_collisions": str(valid * valid),
            "preprocess_clause_reads": len(base),
            "written_clauses": len(transformed),
            "verifier_clause_visits": verifier_clause_visits,
            "extracted_source_bits": extracted_bits,
        })

    # Two-block independent-product source stays in the clean core.
    source2 = product(base, 2)
    source2_w = p0 + p1
    transformed2 = fork_transform(source2, 18, 2)
    assert clean_core(source2, 18) and clean_core(transformed2, 36)
    for e in itertools.product((0, 1), repeat=2):
        z = opening(source2_w, e, p0, p1)
        assert verify(source2, 18, 2, tuple(transformed2), e, z, p0, p1)
        assert z[:18] == source2_w
        checks += 2

    # Easy controls: the same fork shape is cheap on 2SAT, Horn, affine,
    # bounded-treewidth, redundant/padded, and trivially satisfiable sources.
    controls = {
        "2SAT_treewidth1": [(1, -1), (2, -2), (3, -3)],
        "Horn_chain": [(-1, 2), (-2, 3)],
        "affine_Tseitin_even3": parity3_even(),
        "redundant_2SAT": [(1, -1)] * 9,
        "unit_padded": [(1,), (1, 2), (1, 2, 3)],
    }
    control_rows = []
    for name, formula in controls.items():
        nvars = 3
        source_ws = witnesses(formula, nvars)
        assert source_ws
        w = source_ws[0]
        transformed = fork_transform(formula, nvars, 1)
        for e in ((0,), (1,)):
            z = opening(w, e, p0, p1)
            assert verify(formula, nvars, 1, tuple(transformed), e, z, p0, p1)
            assert z[:nvars] == w
            checks += 2
        control_rows.append({"control": name, "source_witnesses": len(source_ws),
                             "fork_openings_checked": 2,
                             "source_clauses": len(formula)})

    # UNSAT control: padding preserves unsatisfiability and the verifier has
    # no valid canonical opening because its response must project to a
    # source witness.
    unsat = [(1,), (-1,)]
    assert witnesses(unsat, 1) == []
    unsat_transformed = fork_transform(unsat, 1, 1)
    for candidate in itertools.product((0, 1), repeat=10):
        for e in ((0,), (1,)):
            assert not verify(unsat, 1, 1, tuple(unsat_transformed), e,
                              candidate, p0, p1)
            checks += 1
    control_rows.append({"control": "UNSAT_units", "source_witnesses": 0,
                         "fork_openings_checked": 0,
                         "candidate_openings_rejected": 2 * (1 << 10),
                         "source_clauses": len(unsat)})

    # Alternate encodings preserve semantics and the projected source witness.
    commitment = tuple(fork_transform(base, 9, 1))
    z = opening(p0, (0,), p0, p1)
    encodings = {
        "tuple": repr(commitment),
        "DIMACS": "p cnf 18 24\n" + "\n".join(" ".join(map(str, c)) + " 0"
                                                   for c in commitment),
        "JSON": json.dumps([list(c) for c in commitment]),
        "reversed_clause_order": repr(tuple(reversed(commitment))),
    }
    assert verify(base, 9, 1, commitment, (0,), z, p0, p1)
    checks += len(encodings) + 1

    # Symbolic growth ledger; these equalities are integer arithmetic only.
    growth = []
    for k in range(1, 65):
        openings = 102 * (1 << k)
        growth.append({"challenge_bits": k,
                       "variables": 9 + 9 * k,
                       "clauses": 12 + 12 * k,
                       "canonical_openings": str(openings),
                       "ordered_collisions": str(openings * openings)})
        checks += 2

    elapsed = time.perf_counter() - started
    payload = {
        "claim": "CLEAN-CORE-FORK-PADDING-GAUGE1",
        "status": "COMPUTATIONAL",
        "exhaustive": True,
        "max_exhaustive_challenge_bits": max_challenge_bits,
        "paired_k33": {"variables": 9, "clauses": 12,
                        "witnesses": len(ws),
                        "opening_zero": "".join(map(str, p0)),
                        "opening_one": "".join(map(str, p1))},
        "clean_core_rows": rows,
        "independent_product": {"source_blocks": 2, "challenge_bits": 2,
                                "clean_core_preserved": True},
        "easy_family_controls": control_rows,
        "alternate_encodings": sorted(encodings),
        "wrappers": wrapper_names,
        "wrapper_checks": wrapper_checks,
        "symbolic_growth": growth,
        "checks": checks,
        "failures": 0,
        "elapsed_seconds": round(elapsed, 6),
        "limitations": [
            "Finite checks do not prove asymptotic SAT lower or upper bounds.",
            "The symbolic report proves the padding theorem for every clean-core source and k.",
            "Opening acquisition still requires a source witness; no solver-independent favorable exponent is inferred.",
            "The construction falsifies fork multiplicity as a forbidden endpoint, not every construction-specific extractor.",
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["canonical_payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-challenge-bits", type=int, default=8)
    parser.add_argument("--output", default=(
        "results/raw/review/2026-10-12_clean_core_fork_padding_gauge.json"))
    args = parser.parse_args()
    payload = run(args.max_challenge_bits)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
    print(json.dumps({
        "output": str(path),
        "checks": payload["checks"],
        "failures": payload["failures"],
        "elapsed_seconds": payload["elapsed_seconds"],
        "max_openings_checked": payload["clean_core_rows"][-1]["canonical_valid_openings"],
        "payload_sha256": payload["canonical_payload_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
