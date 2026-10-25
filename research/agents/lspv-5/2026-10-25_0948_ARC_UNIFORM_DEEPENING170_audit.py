#!/usr/bin/env python3
"""ARC-UNIFORM-DEEPENING170 deterministic restricted audit.

This checks exact exponent identities, the uniform-vs-depth-indexed
polylogarithmic-access distinction, and two genuine ordinary-CNF recursive
levels on disjoint proper-3CNF packets.  It is not an FLMV machine profiler
and does not construct the missing all-input transformer.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


RUN_ID = "ARC-UNIFORM-DEEPENING170"
OUT = Path("2026-10-25_0948_ARC_UNIFORM_DEEPENING170_raw.json")
checks = 0


def check(value: bool, label: str) -> None:
    global checks
    checks += 1
    if not value:
        raise AssertionError(label)


def frac_text(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}"


def exponent_audit() -> dict:
    a = Fraction(3, 5)
    beta = Fraction(1, 2)
    r = Fraction(11, 10)
    delta = Fraction(1, 2)
    c_star = Fraction(241, 200)
    d_star = Fraction(11642479, 23232400)
    limit = a / (1 - beta)
    check(limit == Fraction(6, 5), "tree fixed point")
    check(max(r, limit) == Fraction(6, 5), "time envelope")
    check(delta < d_star, "space strictness")
    check(limit < c_star, "time strictness")
    check(c_star - limit == Fraction(1, 200), "time margin")
    check(d_star - delta == Fraction(26279, 23232400), "space margin")

    rows = []
    for depth in range(0, 65):
        beta_d = beta**depth
        nodes = a * (1 - beta_d) / (1 - beta)
        local = nodes + r * beta_d
        leaf = nodes
        expected = limit + (r - limit) * beta_d
        check(local == expected, f"level identity {depth}")
        check(local <= limit, f"local bounded {depth}")
        check(leaf <= limit, f"leaf bounded {depth}")
        if depth in (0, 1, 2, 4, 8, 16, 32, 64):
            rows.append({
                "depth": depth,
                "node_exponent": frac_text(nodes),
                "local_work_exponent": frac_text(local),
            })

    # At N=2^(2^D), n_i=N^(2^-i).  A fixed polylog degree C contributes
    # C(D-i)/2^D to the exponent at level i; their sum vanishes.  If the
    # degree is illegally depth-indexed as 2^i, the sum tends to 2 instead.
    access_rows = []
    fixed_c = 7
    previous_fixed = None
    previous_bad = None
    for D in range(4, 25):
        fixed = Fraction(fixed_c * D * (D + 1), 2 * (2**D))
        bad = sum((Fraction(D - i, 2 ** (D - i)) for i in range(D)), Fraction(0))
        bad_closed = Fraction(2) - Fraction(D + 2, 2**D)
        check(bad == bad_closed, f"nonuniform closed form {D}")
        check(fixed > 0, f"fixed positive {D}")
        check(bad < 2, f"bad below two {D}")
        if previous_fixed is not None and D >= 8:
            check(fixed < previous_fixed, f"fixed decreases {D}")
            check(bad > previous_bad, f"bad increases {D}")
        previous_fixed, previous_bad = fixed, bad
        if D in (4, 8, 12, 16, 20, 24):
            access_rows.append({
                "D": D,
                "fixed_degree_exponent": frac_text(fixed),
                "depth_indexed_degree_exponent": frac_text(bad),
            })
    check(previous_fixed < Fraction(1, 100), "uniform polylog is subpolynomial")
    check(previous_bad > Fraction(199, 100), "depth-indexed overhead is polynomial")
    return {
        "a": frac_text(a),
        "beta": frac_text(beta),
        "r": frac_text(r),
        "delta": frac_text(delta),
        "time_limit": frac_text(limit),
        "c_star": frac_text(c_star),
        "d_star": frac_text(d_star),
        "depth_rows": rows,
        "access_rows": access_rows,
    }


def all_clauses(base: int) -> tuple[tuple[int, ...], ...]:
    vars_ = (base, base + 1, base + 2)
    return tuple(
        tuple(v if bit else -v for v, bit in zip(vars_, signs))
        for signs in itertools.product((0, 1), repeat=3)
    )


def packet(base: int, satisfiable: bool) -> tuple[tuple[int, ...], ...]:
    clauses = all_clauses(base)
    return clauses[:-1] if satisfiable else clauses


def packet_sat(clauses: tuple[tuple[int, ...], ...]) -> bool:
    vars_ = sorted({abs(z) for c in clauses for z in c})
    for bits in itertools.product((0, 1), repeat=len(vars_)):
        val = dict(zip(vars_, bits))
        if all(any(val[abs(z)] == int(z > 0) for z in c) for c in clauses):
            return True
    return False


def serialize(clauses: tuple[tuple[int, ...], ...], nvars: int) -> str:
    body = "".join(" ".join(map(str, c)) + " 0\n" for c in clauses)
    return f"p cnf {nvars} {len(clauses)}\n" + body


def parse(text: str) -> tuple[int, tuple[tuple[int, ...], ...]]:
    lines = text.splitlines()
    tag, kind, nvars, nclauses = lines[0].split()
    check((tag, kind) == ("p", "cnf"), "header")
    out = []
    for line in lines[1:]:
        row = tuple(map(int, line.split()))
        check(bool(row) and row[-1] == 0, "terminator")
        out.append(row[:-1])
    check(len(out) == int(nclauses), "clause count")
    return int(nvars), tuple(out)


def partition(items: list, width: int) -> list[list]:
    return [items[i : i + width] for i in range(0, len(items), width)]


def cnf_two_level_audit() -> dict:
    cases = []
    total_bytes = 0
    first_children = 0
    second_children = 0
    for p in (1, 2, 4, 9, 16, 25, 36):
        patterns = [
            [True] * p,
            [False] + [True] * (p - 1),
            [True] * (p - 1) + [False],
        ]
        for labels in patterns:
            packets = [packet(3 * j + 1, labels[j]) for j in range(p)]
            root_clauses = tuple(c for pack in packets for c in pack)
            nvars = 3 * p
            root_text = serialize(root_clauses, nvars)
            pn, parsed = parse(root_text)
            check(pn == nvars and parsed == root_clauses, "root round trip")
            direct = all(packet_sat(pack) for pack in packets)
            check(direct == all(labels), "packet direct label")
            width1 = max(1, math.ceil(math.sqrt(p)))
            level1 = partition(packets, width1)
            labels1 = []
            for child in level1:
                clauses1 = tuple(c for pack in child for c in pack)
                text1 = serialize(clauses1, nvars)
                _, parsed1 = parse(text1)
                check(parsed1 == clauses1, "level1 round trip")
                label1 = all(packet_sat(pack) for pack in child)
                labels1.append(label1)
                width2 = max(1, math.ceil(math.sqrt(len(child))))
                level2 = partition(child, width2)
                labels2 = []
                for grandchild in level2:
                    clauses2 = tuple(c for pack in grandchild for c in pack)
                    text2 = serialize(clauses2, nvars)
                    _, parsed2 = parse(text2)
                    check(parsed2 == clauses2, "level2 round trip")
                    labels2.append(all(packet_sat(pack) for pack in grandchild))
                    total_bytes += len(text2.encode())
                    second_children += 1
                check(all(labels2) == label1, "second join")
                total_bytes += len(text1.encode())
                first_children += 1
            check(all(labels1) == direct, "first join")
            total_bytes += len(root_text.encode())
            cases.append({
                "packets": p,
                "root_sat": direct,
                "first_children": len(level1),
                "root_bytes": len(root_text.encode()),
            })
    return {
        "roots": len(cases),
        "sat_roots": sum(c["root_sat"] for c in cases),
        "unsat_roots": sum(not c["root_sat"] for c in cases),
        "first_children": first_children,
        "second_children": second_children,
        "serialized_bytes": total_bytes,
        "cases": cases,
        "control": "disjoint packet direct recognizer is polynomial; this is scheduling evidence only",
    }


def main() -> None:
    result = {
        "run_id": RUN_ID,
        "date": "2026-10-25 America/Los_Angeles",
        "seed": None,
        "classification": "COMPUTATIONAL support for exact symbolic theorem",
        "model_limit": "logical serialization and exact rational accounting, not physical FLMV traces",
        "exponents": exponent_audit(),
        "ordinary_cnf": cnf_two_level_audit(),
    }
    result["assertions"] = checks
    result["failures"] = 0
    script_bytes = Path(__file__).read_bytes()
    result["script_sha256"] = hashlib.sha256(script_bytes).hexdigest()
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
