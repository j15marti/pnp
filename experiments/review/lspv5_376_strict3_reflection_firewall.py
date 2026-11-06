#!/usr/bin/env python3
"""Finite strict-3-CNF control for REFEREE376.

This is an executable illustration of a proof-triggered SAT-decider wrapper.
It is not a formalization of Goedel's theorem and not an R_mix341 checker.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import pathlib
import time
import tracemalloc

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "results/raw/review/2026-11-05_1958_LSPV5_STRICT3_REFLECTION376.json"


def parity_clauses(vars3: tuple[int, int, int], rhs: int) -> list[tuple[int, ...]]:
    """Width-3 clauses forbidding assignments whose parity differs from rhs."""
    out: list[tuple[int, ...]] = []
    for a in itertools.product((0, 1), repeat=3):
        if (sum(a) & 1) != rhs:
            out.append(tuple(v if bit == 0 else -v for v, bit in zip(vars3, a)))
    return out


def k4_block(offset: int, charge: tuple[int, int, int, int] = (0, 0, 0, 0)) -> list[tuple[int, ...]]:
    # Edges 01,02,03,12,13,23 in that order.
    e01, e02, e03, e12, e13, e23 = [offset + i for i in range(1, 7)]
    rows = ((e01, e02, e03), (e01, e12, e13), (e02, e12, e23), (e03, e13, e23))
    clauses: list[tuple[int, ...]] = []
    for row, rhs in zip(rows, charge):
        clauses.extend(parity_clauses(row, rhs))
    assert len(clauses) == 16
    return clauses


def sat_code_clauses(bits: str) -> tuple[int, list[tuple[int, ...]]]:
    if not bits or any(b not in "01" for b in bits):
        raise ValueError("code must be a nonempty binary string")
    clauses: list[tuple[int, ...]] = []
    for i, bit in enumerate(bits):
        block = k4_block(6 * i)
        # Two source-byte encodings of the same K4 relation carry one code bit.
        if bit == "1":
            block[0], block[1] = block[1], block[0]
        clauses.extend(block)
    return 6 * len(bits), clauses


def dimacs(nvars: int, clauses: list[tuple[int, ...]]) -> str:
    body = "".join(" ".join(map(str, c)) + " 0\n" for c in clauses)
    return f"p cnf {nvars} {len(clauses)}\n" + body


def parse_dimacs(text: str):
    try:
        lines = [line.strip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith("c")]
        if not lines or len(lines[0].split()) != 4 or lines[0].split()[:2] != ["p", "cnf"]:
            return None
        nvars, nclauses = map(int, lines[0].split()[2:])
        if nvars < 0 or nclauses < 0 or len(lines) != nclauses + 1:
            return None
        clauses = []
        for line in lines[1:]:
            vals = list(map(int, line.split()))
            if not vals or vals[-1] != 0 or any(v == 0 for v in vals[:-1]):
                return None
            clause = tuple(vals[:-1])
            if any(abs(v) > nvars for v in clause):
                return None
            clauses.append(clause)
        return nvars, clauses
    except (ValueError, TypeError):
        return None


def recognize_sat_code(parsed) -> str | None:
    if parsed is None:
        return None
    nvars, clauses = parsed
    if nvars == 0 or nvars % 6 or len(clauses) != (nvars // 6) * 16:
        return None
    bits = []
    for i in range(nvars // 6):
        got = clauses[16 * i : 16 * (i + 1)]
        zero = k4_block(6 * i)
        one = zero.copy()
        one[0], one[1] = one[1], one[0]
        if got == zero:
            bits.append("0")
        elif got == one:
            bits.append("1")
        else:
            return None
    return "".join(bits)


def eval_cnf(clauses, assignment: tuple[int, ...]) -> bool:
    return all(any((assignment[abs(lit) - 1] == 1) == (lit > 0) for lit in c) for c in clauses)


def exact_label(parsed) -> str:
    if parsed is None:
        return "MALFORMED"
    nvars, clauses = parsed
    if nvars > 20:
        raise ValueError("finite exact control limited to 20 variables")
    for a in itertools.product((0, 1), repeat=nvars):
        if eval_cnf(clauses, a):
            return "SAT"
    return "UNSAT"


def wrapped_label(text: str, toy_proofs: set[str]) -> tuple[str, int, str | None]:
    parsed = parse_dimacs(text)
    if parsed is None:
        return "MALFORMED", 0, None
    code = recognize_sat_code(parsed)
    if code is not None:
        # A real theorem uses a polynomial-time verifier for T-proofs of 0=1.
        return ("UNSAT" if code in toy_proofs else "SAT"), 1, code
    return exact_label(parsed), 0, None


def main() -> None:
    tracemalloc.start()
    start = time.perf_counter()
    checks = 0
    records = []
    for bits in ("0", "1", "01", "101"):
        nv, cs = sat_code_clauses(bits)
        source = dimacs(nv, cs)
        parsed = parse_dimacs(source)
        assert parsed is not None; checks += 1
        assert recognize_sat_code(parsed) == bits; checks += 1
        assert all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in cs); checks += 1
        assert eval_cnf(cs, (0,) * nv); checks += 1
        consistent = wrapped_label(source, set())
        hostile = wrapped_label(source, {"101"})
        assert consistent[0] == "SAT"; checks += 1
        assert hostile[0] == ("UNSAT" if bits == "101" else "SAT"); checks += 1
        records.append({
            "proof_code": bits,
            "variables": nv,
            "clauses": len(cs),
            "bytes": len(source.encode()),
            "sha256": hashlib.sha256(source.encode()).hexdigest(),
            "all_zero_witness": True,
            "consistent_wrapper": consistent[0],
            "hostile_toy_wrapper": hostile[0],
            "toy_verifier_calls": hostile[1],
            "dimacs": source,
        })

    odd = k4_block(0, (1, 0, 0, 0))
    odd_source = dimacs(6, odd)
    assert exact_label(parse_dimacs(odd_source)) == "UNSAT"; checks += 1
    assert recognize_sat_code(parse_dimacs(odd_source)) is None; checks += 1
    assert wrapped_label(odd_source, {"101"})[0] == "UNSAT"; checks += 1

    sat_source = "p cnf 1 1\n1 0\n"
    unsat_source = "p cnf 1 2\n1 0\n-1 0\n"
    assert wrapped_label(sat_source, {"101"})[0] == "SAT"; checks += 1
    assert wrapped_label(unsat_source, {"101"})[0] == "UNSAT"; checks += 1

    malformed = [
        "",
        "p cnf 1 2\n1 0\n",
        "p cnf 1 1\n2 0\n",
        "p cnf 1 1\n1\n",
        "p cnf x 1\n1 0\n",
        "p cnf 1 -1\n",
    ]
    for bad in malformed:
        assert wrapped_label(bad, {"101"})[0] == "MALFORMED"; checks += 1

    # Corrupt an authenticated special source: it must not retain the embedded code identity.
    corrupt = records[-1]["dimacs"].replace("1 2 -3 0", "1 2 3 0", 1)
    cp = parse_dimacs(corrupt)
    assert cp is not None and recognize_sat_code(cp) is None; checks += 1

    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    result = {
        "artifact": "LSPV5_REFEREE376_STRICT3_REFLECTION_FIREWALL",
        "status": "COMPUTATIONAL finite toy-proof controls; mathematical reflection theorem is separate",
        "scope": "Canonical strict-3-CNF K4 parity blocks encode candidate proof strings by clause order. Not R_mix341 bytes, not a Goedel formalization, not B3.",
        "records": records,
        "odd_k4_control": {
            "variables": 6,
            "clauses": 16,
            "label": "UNSAT",
            "sha256": hashlib.sha256(odd_source.encode()).hexdigest(),
            "dimacs": odd_source,
        },
        "general_controls": {"sat": "SAT", "unsat": "UNSAT", "malformed_rejections": len(malformed)},
        "corrupt_special_rejected": True,
        "assertions": checks,
        "python_elapsed_seconds": elapsed,
        "python_tracemalloc_peak_bytes": peak,
        "logical_cost_note": "No W_R nodes are inferred. Wrapper recognition, proof verification, parsing and output are machine work.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(OUT), "assertions": checks, "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(), "peak": peak}))


if __name__ == "__main__":
    main()
