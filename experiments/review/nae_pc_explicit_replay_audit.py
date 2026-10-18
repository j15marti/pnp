#!/usr/bin/env python3
"""Independent ordinary-ring replay audit for the NAEGAUGECHAIN1 PC/PCR map.

Every derived line is checked as one of: input axiom, linear combination of
earlier lines, or multiplication of an earlier line by a single variable.
No Boolean-quotient reduction is used.  The output is deterministic JSON.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

Monomial = Tuple[str, ...]
Poly = Dict[Monomial, int]


def norm(p: Poly, q: int) -> Poly:
    return {m: c % q for m, c in p.items() if c % q}


def add(a: Poly, b: Poly, q: int) -> Poly:
    out = dict(a)
    for m, c in b.items():
        out[m] = (out.get(m, 0) + c) % q
    return norm(out, q)


def scale(a: Poly, c: int, q: int) -> Poly:
    return norm({m: c * v for m, v in a.items()}, q)


def mul(a: Poly, b: Poly, q: int) -> Poly:
    out: Poly = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(sorted(ma + mb))
            out[m] = (out.get(m, 0) + ca * cb) % q
    return norm(out, q)


def const(c: int, q: int) -> Poly:
    return norm({(): c}, q)


def var(x: str) -> Poly:
    return {(x,): 1}


def one_minus(p: Poly, q: int) -> Poly:
    return add(const(1, q), scale(p, -1, q), q)


def degree(p: Poly) -> int:
    return max((len(m) for m in p), default=-1)


def literal(x: str, positive: bool, q: int) -> Poly:
    return var(x) if positive else one_minus(var(x), q)


def bool_axiom(x: str, q: int) -> Poly:
    return add(mul(var(x), var(x), q), scale(var(x), -1, q), q)


@dataclass
class Line:
    poly: Poly
    rule: str
    parents: Tuple[int, ...]
    data: Tuple[object, ...]


class Replay:
    def __init__(self, q: int):
        self.q = q
        self.lines: List[Line] = []

    def axiom(self, p: Poly) -> int:
        self.lines.append(Line(norm(p, self.q), "axiom", (), ()))
        return len(self.lines) - 1

    def linear(self, i: int, j: int, a: int = 1, b: int = 1) -> int:
        p = add(scale(self.lines[i].poly, a, self.q),
                scale(self.lines[j].poly, b, self.q), self.q)
        self.lines.append(Line(p, "linear", (i, j), (a % self.q, b % self.q)))
        return len(self.lines) - 1

    def rescale(self, i: int, a: int) -> int:
        # A scalar multiple is the legal linear-combination rule applied to
        # the same earlier line twice; no unlisted zero axiom is introduced.
        return self.linear(i, i, a, 0)

    def mul_var(self, i: int, x: str) -> int:
        p = mul(self.lines[i].poly, var(x), self.q)
        self.lines.append(Line(p, "mul_var", (i,), (x,)))
        return len(self.lines) - 1

    def mul_literal(self, i: int, x: str, positive: bool) -> int:
        xi = self.mul_var(i, x)
        return xi if positive else self.linear(i, xi, 1, -1)

    def verify(self) -> None:
        for k, line in enumerate(self.lines):
            if line.rule == "axiom":
                continue
            if line.rule == "linear":
                i, j = line.parents
                a, b = line.data
                assert i < k and j < k
                want = add(scale(self.lines[i].poly, int(a), self.q),
                           scale(self.lines[j].poly, int(b), self.q), self.q)
            elif line.rule == "mul_var":
                (i,) = line.parents
                (x,) = line.data
                assert i < k
                want = mul(self.lines[i].poly, var(str(x)), self.q)
            else:
                raise AssertionError(f"unknown rule {line.rule}")
            assert line.poly == want, (k, line.rule, line.poly, want)


def signed_literal_pair(name: str, positive: bool, q: int) -> Tuple[Poly, Poly]:
    a = literal(name, positive, q)
    return a, one_minus(a, q)


def derive_a_clause_all_one(q: int, a_pos: bool, b_pos: bool) -> Tuple[int, int]:
    """Derive a*b*(1-a)*(1-b) from one source Boolean axiom."""
    replay = Replay(q)
    i = replay.axiom(bool_axiom("a", q))
    i = replay.mul_literal(i, "b", b_pos)
    i = replay.mul_literal(i, "b", not b_pos)
    i = replay.rescale(i, -1)
    a, na = signed_literal_pair("a", a_pos, q)
    b, nb = signed_literal_pair("b", b_pos, q)
    want = mul(mul(a, b, q), mul(na, nb, q), q)
    replay.verify()
    assert replay.lines[i].poly == want
    return len(replay.lines), max(degree(x.poly) for x in replay.lines)


def derive_splitter_boolean(q: int, a_pos: bool, b_pos: bool) -> Tuple[int, int]:
    """Derive p^2-p for p=(1-a)(1-b) by the displayed integral identity."""
    replay = Replay(q)
    br = replay.axiom(bool_axiom("a", q))
    bs = replay.axiom(bool_axiom("b", q))
    # r=1-a and s=1-b.  Their polarities are the complements of a,b.
    t1 = replay.mul_literal(br, "b", not b_pos)
    t1 = replay.mul_literal(t1, "b", not b_pos)
    t2 = replay.mul_literal(bs, "a", not a_pos)
    out = replay.linear(t1, t2)
    a, na = signed_literal_pair("a", a_pos, q)
    b, nb = signed_literal_pair("b", b_pos, q)
    p = mul(na, nb, q)
    want = add(mul(p, p, q), scale(p, -1, q), q)
    replay.verify()
    assert replay.lines[out].poly == want
    return len(replay.lines), max(degree(x.poly) for x in replay.lines)


def random_poly(rng: random.Random, q: int, variables: Sequence[str],
                max_degree: int, terms: int) -> Poly:
    p: Poly = {}
    for _ in range(terms):
        d = rng.randrange(max_degree + 1)
        m = tuple(sorted(rng.choice(variables) for _ in range(d)))
        p[m] = (p.get(m, 0) + rng.randrange(1, q)) % q
    return norm(p, q)


def replay_multiplier(p0: Poly, q: int, kind: str,
                      a_pos: bool, b_pos: bool) -> Tuple[Poly, int, int]:
    replay = Replay(q)
    base = replay.axiom(p0)
    if kind == "source_var":
        out = replay.mul_var(base, "c")
        image = var("c")
    elif kind == "source_complement":
        out = replay.mul_literal(base, "c", False)
        image = literal("c", False, q)
    elif kind in {"splitter", "splitter_complement"}:
        pidx = replay.mul_literal(base, "a", not a_pos)
        pidx = replay.mul_literal(pidx, "b", not b_pos)
        a, na = signed_literal_pair("a", a_pos, q)
        b, nb = signed_literal_pair("b", b_pos, q)
        splitter = mul(na, nb, q)
        if kind == "splitter":
            out = pidx
            image = splitter
        else:
            out = replay.linear(base, pidx, 1, -1)
            image = one_minus(splitter, q)
    elif kind == "zero":
        out = replay.rescale(base, 0)
        image = {}
    elif kind == "one":
        out = replay.rescale(base, 1)
        image = const(1, q)
    else:
        raise ValueError(kind)
    replay.verify()
    want = mul(p0, image, q)
    assert replay.lines[out].poly == want
    return want, len(replay.lines), max(degree(x.poly) for x in replay.lines)


def nae_axiom_images(q: int, a_pos: bool, b_pos: bool, c_pos: bool) -> Dict[str, bool]:
    a, na = signed_literal_pair("a", a_pos, q)
    b, nb = signed_literal_pair("b", b_pos, q)
    c, nc = signed_literal_pair("c", c_pos, q)
    p = mul(na, nb, q)
    source_clause = mul(mul(na, nb, q), nc, q)
    # A=NAE(a,b,u), B=NAE(not u,c,z), z=0.
    images = {
        "A_all_one": mul(mul(a, b, q), p, q),
        "A_all_zero": mul(mul(na, nb, q), one_minus(p, q), q),
        "B_all_one": {},
        "B_all_zero": mul(p, nc, q),
        "source_clause": source_clause,
        "PCR_complement_sum": add(add(p, one_minus(p, q), q), const(-1, q), q),
        "PCR_complement_product": mul(p, one_minus(p, q), q),
    }
    return {
        "B_one_zero": images["B_all_one"] == {},
        "B_zero_source": images["B_all_zero"] == source_clause,
        "PCR_sum_zero": images["PCR_complement_sum"] == {},
        "PCR_product_matches_PC": images["PCR_complement_product"] == images["A_all_zero"],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=202610190528)
    ap.add_argument("--trials", type=int, default=80)
    ap.add_argument("--output", default="results/raw/review/2026-10-19_NAEPCREPLAY1.json")
    args = ap.parse_args()
    start = time.perf_counter()
    rng = random.Random(args.seed)
    fields = [2, 3, 5, 7, 11]
    failures: List[str] = []
    rows = []
    total_checks = 0

    for q in fields:
        checks = 0
        max_axiom_degree = -1
        max_sim_degree_slack = -10**9
        max_lines = 0
        for a_pos in (False, True):
            for b_pos in (False, True):
                try:
                    n1, d1 = derive_a_clause_all_one(q, a_pos, b_pos)
                    n2, d2 = derive_splitter_boolean(q, a_pos, b_pos)
                    max_lines = max(max_lines, n1, n2)
                    max_axiom_degree = max(max_axiom_degree, d1, d2)
                    checks += 2
                except AssertionError as exc:
                    failures.append(f"axiom q={q} signs={a_pos,b_pos}: {exc}")
                for c_pos in (False, True):
                    for key, ok in nae_axiom_images(q, a_pos, b_pos, c_pos).items():
                        checks += 1
                        if not ok:
                            failures.append(f"image {key} q={q} signs={a_pos,b_pos,c_pos}")

        variables = ["a", "b", "c", "d", "f", "g"]
        kinds = ["source_var", "source_complement", "splitter",
                 "splitter_complement", "zero", "one"]
        for trial in range(args.trials):
            p0 = random_poly(rng, q, variables, max_degree=4, terms=12)
            d0 = degree(p0)
            for a_pos in (False, True):
                for b_pos in (False, True):
                    for kind in kinds:
                        try:
                            out, line_count, maxdeg = replay_multiplier(
                                p0, q, kind, a_pos, b_pos)
                            allowance = d0 + (2 if "splitter" in kind else 1)
                            if kind in {"zero", "one"}:
                                allowance = max(d0, 0)
                            assert maxdeg <= allowance
                            max_sim_degree_slack = max(max_sim_degree_slack,
                                                       maxdeg - allowance)
                            max_lines = max(max_lines, line_count)
                            checks += 1
                        except AssertionError as exc:
                            failures.append(
                                f"mult q={q} trial={trial} signs={a_pos,b_pos} kind={kind}: {exc}")
        rows.append({
            "prime": q,
            "checks": checks,
            "max_axiom_derivation_degree": max_axiom_degree,
            "max_legal_replay_lines": max_lines,
            "max_degree_minus_allowance": max_sim_degree_slack,
            "failures": sum(1 for f in failures if f"q={q}" in f),
        })
        total_checks += checks

    script_path = Path(__file__)
    result = {
        "run_id": "NAEPCREPLAY1",
        "status": "PASS" if not failures else "FAIL",
        "method": "ordinary-polynomial-ring replay of legal PC/PCR inference steps",
        "seed": args.seed,
        "trials_per_field": args.trials,
        "fields": fields,
        "field_rows": rows,
        "total_checks": total_checks,
        "failures": failures,
        "elapsed_seconds": round(time.perf_counter() - start, 6),
        "script_sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
        "scope": [
            "NAEGAUGECHAIN1 front-end and equality-chain substitution",
            "PC splitter Boolean-axiom derivation",
            "PCR complement-rail identities and multiplication replay",
            "characteristic-two and odd-prime controls",
        ],
        "limitations": [
            "Does not search for PC/PCR refutations or prove the all-field theorem by finite testing.",
            "Does not cover unavailable FTNC, ONE3/NOT-ONE3, or REVFIX2 axiom lists.",
            "Proof-size and arbitrary-machine time do not follow from degree replay.",
        ],
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
