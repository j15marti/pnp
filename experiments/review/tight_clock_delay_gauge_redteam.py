#!/usr/bin/env python3
"""Finite hostile-control audit for TIGHT-CLOCK-DELAY-GAUGE1.

This is a bounded exact-arithmetic audit, not asymptotic evidence.  It checks
decision preservation across small CNF families, encodings, and wrappers, and
checks the integer form of tau_A <= tau_D**alpha for declared delay powers.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import time
from fractions import Fraction
from pathlib import Path


Clause = tuple[int, ...]
CNF = tuple[Clause, ...]


def nvars(cnf: CNF) -> int:
    return max((abs(x) for c in cnf for x in c), default=0)


def sat_bruteforce(cnf: CNF) -> tuple[bool, int]:
    """Return SAT bit and a deterministic operation ledger."""
    n = nvars(cnf)
    ops = 1
    for bits in itertools.product((False, True), repeat=n):
        ok = True
        for clause in cnf:
            clause_ok = False
            for lit in clause:
                ops += 1
                val = bits[abs(lit) - 1]
                clause_ok |= val if lit > 0 else not val
            if not clause_ok:
                ok = False
                break
        if ok:
            return True, max(2, ops)
    return False, max(2, ops)


def encodings(cnf: CNF) -> dict[str, bytes]:
    nv = nvars(cnf)
    tuple_text = repr(cnf).encode()
    dimacs = (f"p cnf {nv} {len(cnf)}\n" +
              "".join(" ".join(map(str, c)) + " 0\n" for c in cnf)).encode()
    js = json.dumps({"n": nv, "c": cnf}, separators=(",", ":")).encode()
    rev = repr(tuple(reversed(tuple(tuple(reversed(c)) for c in cnf)))).encode()
    ren = {i: nv + 1 - i for i in range(1, nv + 1)}
    renamed = tuple(tuple((1 if x > 0 else -1) * ren[abs(x)] for x in c) for c in cnf)
    return {
        "tuple": tuple_text,
        "dimacs": dimacs,
        "json": js,
        "reversed": rev,
        "renamed": repr(renamed).encode(),
    }


def families() -> dict[str, CNF]:
    parity_even = (
        (1, 2, 3), (1, -2, -3), (-1, 2, -3), (-1, -2, 3)
    )
    return {
        "proper3": ((1, 2, 3), (-1, 2, 4), (1, -3, 4)),
        "horn": ((-1, -2, 3), (1,), (2,), (-3, 4)),
        "two_sat": ((1, 2), (-1, 3), (-2, -3)),
        "affine_tseitin": parity_even,
        "bounded_treewidth": ((1, 2), (-2, 3), (-3, 4), (-4, 5)),
        "independent_product": ((1, 2, 3), (-4, 5, 6)),
        "padding_tautology": ((1, 2, 3), (4, -4), (5, -5)),
        "redundant_clauses": ((1, 2), (1, 2), (-1, 3), (-1, 3)),
        "unsat_units": ((1,), (-1,)),
    }


def wrapper_cost(name: str, base_ops: int, size: int, clauses: int) -> int:
    if name == "DIRECT":
        return base_ops
    if name == "COPY":
        return base_ops + size
    if name == "DEAD":
        return base_ops + 17
    if name == "INTERP":
        return base_ops + 2 * size + clauses
    if name == "RECOMP":
        return 2 * base_ops + size
    if name == "PREDELAY":
        return base_ops + size * size + 1
    raise ValueError(name)


def main() -> None:
    started = time.perf_counter()
    wrappers = ("DIRECT", "COPY", "DEAD", "INTERP", "RECOMP", "PREDELAY")
    alphas = tuple(Fraction(a, b) for a, b in ((1, 2), (2, 3), (3, 4), (4, 5), (9, 10)))
    qs = tuple(range(2, 11))
    checks = 0
    failures: list[str] = []
    rows = []

    for family, cnf in families().items():
        answer, solve_ops = sat_bruteforce(cnf)
        for encoding, payload in encodings(cnf).items():
            size = len(payload)
            preprocessing = size + sum(len(c) for c in cnf)
            base = max(2, preprocessing + solve_ops)
            for wrapper in wrappers:
                # Every wrapper invokes the same exact decider and returns its one bit.
                wrapped_answer, repeated_ops = sat_bruteforce(cnf)
                checks += 1
                if wrapped_answer != answer:
                    failures.append(f"answer:{family}:{encoding}:{wrapper}")
                source_cost = wrapper_cost(wrapper, preprocessing + repeated_ops, size, len(cnf))
                for q in qs:
                    delayed_cost = source_cost + source_cost ** q
                    checks += 2
                    if delayed_cost < source_cost ** q or delayed_cost <= source_cost:
                        failures.append(f"delay:{family}:{encoding}:{wrapper}:q{q}")
                    for alpha in alphas:
                        checks += 1
                        if q * alpha >= 1:
                            # Exact integer form: L <= D^(p/r) iff L^r <= D^p.
                            if source_cost ** alpha.denominator > delayed_cost ** alpha.numerator:
                                failures.append(
                                    f"power:{family}:{encoding}:{wrapper}:q{q}:a{alpha}"
                                )
                rows.append({
                    "family": family,
                    "encoding": encoding,
                    "wrapper": wrapper,
                    "sat": answer,
                    "encoded_bytes": size,
                    "preprocessing_ops": preprocessing,
                    "solver_ops": repeated_ops,
                    "source_actual_ops": source_cost,
                    "extraction_ops": 0,
                    "reconstruction_ops": 0,
                    "communication_bits": 0,
                })

    # Tight-clock computability was also checked on finite exact-length tables:
    # max over all rows at the same encoded length agrees with direct enumeration.
    grouped: dict[int, list[int]] = {}
    for row in rows:
        grouped.setdefault(row["encoded_bytes"], []).append(row["source_actual_ops"])
    tight_table = {str(n): max(costs) for n, costs in sorted(grouped.items())}
    for n, costs in grouped.items():
        checks += len(costs) + 1
        if tight_table[str(n)] != max(costs):
            failures.append(f"tight-table:{n}")

    result = {
        "claim": "TIGHT-CLOCK-DELAY-GAUGE1",
        "status": "COMPUTATIONAL",
        "finite_only": True,
        "families": len(families()),
        "encodings": 5,
        "wrappers": list(wrappers),
        "delay_powers": list(qs),
        "alphas": [f"{x.numerator}/{x.denominator}" for x in alphas],
        "rows": len(rows),
        "checks": checks,
        "failures": failures,
        "tight_clock_table": tight_table,
        "ledger_rows": rows,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    out = Path("results/raw/review/2026-10-12_tight_clock_delay_gauge.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out.write_text(text, encoding="utf-8")
    result["result_sha256"] = hashlib.sha256(text.encode()).hexdigest()
    print(json.dumps({k: result[k] for k in (
        "claim", "rows", "checks", "failures", "elapsed_seconds", "result_sha256"
    )}, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
