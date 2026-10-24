#!/usr/bin/env python3
"""Finite audit for BOUNDARY-ORACLE-FACTOR128.

For a proper 3CNF F and a proper-Tseitin encoded Boolean circuit C(b),
construct a connected-to-the-source proper 3CNF H with

    SAT(H[b]) = C(b) AND SAT(F),    SAT(H) = SAT(F)

whenever C has nonempty support.  Adaptive boundary-query transcripts then
factor through one cached source-label bit.  Finite checks validate the
construction and simulator; the general identities are proved symbolically
in the accompanying report.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
from pathlib import Path
from typing import Callable

Clause = tuple[int, int, int]
Formula = tuple[Clause, ...]
Word = tuple[bool, ...]


def simplify(formula: tuple[tuple[int, ...], ...], assignment: dict[int, bool]):
    out: list[tuple[int, ...]] = []
    for clause in formula:
        kept: list[int] = []
        for lit in clause:
            if abs(lit) in assignment:
                if assignment[abs(lit)] == (lit > 0):
                    break
            else:
                kept.append(lit)
        else:
            if not kept:
                return (), False
            out.append(tuple(kept))
    return tuple(out), True


def sat(formula: Formula, fixed: dict[int, bool] | None = None) -> bool:
    def rec(f: tuple[tuple[int, ...], ...], a: dict[int, bool]) -> bool:
        while True:
            f, ok = simplify(f, a)
            if not ok:
                return False
            if not f:
                return True
            unit = next((c[0] for c in f if len(c) == 1), None)
            if unit is None:
                break
            v, val = abs(unit), unit > 0
            if v in a and a[v] != val:
                return False
            a[v] = val
        counts: dict[int, int] = {}
        for c in f:
            for lit in c:
                counts[abs(lit)] = counts.get(abs(lit), 0) + 1
        v = max(counts, key=counts.get)
        for val in (True, False):
            b = dict(a)
            b[v] = val
            if rec(f, b):
                return True
        return False
    return rec(formula, {} if fixed is None else dict(fixed))


def brute_label(formula: Formula, nvars: int) -> bool:
    for bits in itertools.product((False, True), repeat=nvars):
        if all(any(bits[abs(l)-1] == (l > 0) for l in c) for c in formula):
            return True
    return False


class ProperBuilder:
    def __init__(self, nvars: int):
        self.nvars = nvars
        self.clauses: list[Clause] = []

    def var(self) -> int:
        self.nvars += 1
        return self.nvars

    def add(self, *lits: int) -> None:
        if len(lits) == 3:
            assert len({abs(x) for x in lits}) == 3, lits
            self.clauses.append(tuple(lits))  # type: ignore[arg-type]
        elif len(lits) == 2:
            assert abs(lits[0]) != abs(lits[1]), lits
            z = self.var()
            self.add(lits[0], lits[1], z)
            self.add(lits[0], lits[1], -z)
        elif len(lits) == 1:
            a, b = self.var(), self.var()
            self.add(lits[0], a, b)
            self.add(lits[0], a, -b)
            self.add(lits[0], -a, b)
            self.add(lits[0], -a, -b)
        else:
            raise ValueError("only widths 1..3")

    def equiv_copy(self, y: int, p: int) -> None:
        self.add(-p, y)
        self.add(p, -y)

    def equiv_not(self, y: int, p: int) -> None:
        self.add(p, y)
        self.add(-p, -y)

    def equiv_and(self, y: int, p: int, q: int) -> None:
        self.add(-p, -q, y)
        self.add(p, -y)
        self.add(q, -y)

    def equiv_or(self, y: int, p: int, q: int) -> None:
        self.add(p, q, -y)
        self.add(-p, y)
        self.add(-q, y)

    def equiv_xor(self, y: int, p: int, q: int) -> None:
        self.add(-p, -q, -y)
        self.add(p, q, -y)
        self.add(p, -q, y)
        self.add(-p, q, y)


def fold(builder: ProperBuilder, lits: tuple[int, ...], op: str) -> int:
    out = builder.var()
    builder.equiv_copy(out, lits[0])
    for lit in lits[1:]:
        nxt = builder.var()
        (builder.equiv_and if op == "and" else builder.equiv_or)(nxt, out, lit)
        out = nxt
    return out


def support(builder: ProperBuilder, boundary: tuple[int, ...], kind: str):
    d = len(boundary)
    if kind == "singleton_zero":
        out = fold(builder, tuple(-x for x in boundary), "and")
        fn = lambda w: not any(w)
    elif kind == "co_singleton_one":
        out = fold(builder, tuple(-x for x in boundary), "or")
        fn = lambda w: not all(w)
    elif kind == "subcube":
        out = builder.var(); builder.equiv_not(out, boundary[0])
        fn = lambda w: not w[0]
    elif kind == "even_parity":
        parity = builder.var(); builder.equiv_copy(parity, boundary[0])
        for x in boundary[1:]:
            nxt = builder.var(); builder.equiv_xor(nxt, parity, x); parity = nxt
        out = builder.var(); builder.equiv_not(out, parity)
        fn = lambda w: sum(w) % 2 == 0
    elif kind == "two_corners":
        z = fold(builder, tuple(-x for x in boundary), "and")
        o = fold(builder, boundary, "and")
        out = builder.var(); builder.equiv_or(out, z, o)
        fn = lambda w: (not any(w)) or all(w)
    elif kind == "prefix_union":
        if d == 1:
            out = builder.var(); builder.equiv_copy(out, boundary[0])
            fn = lambda w: w[0]
        else:
            a = builder.var(); builder.equiv_and(a, -boundary[0], -boundary[1])
            b = builder.var(); builder.equiv_and(b, boundary[0], boundary[1])
            out = builder.var(); builder.equiv_or(out, a, b)
            fn = lambda w: w[0] == w[1]
    else:
        raise ValueError(kind)
    return out, fn


def construct(base: Formula, nbase: int, d: int, kind: str):
    boundary = tuple(range(nbase + 1, nbase + d + 1))
    b = ProperBuilder(nbase + d)
    c, fn = support(b, boundary, kind)
    # Root requires the support circuit to accept; existential boundary choice
    # keeps the root equivalent to F when the support is nonempty.
    b.add(c)
    circuit_clauses = len(b.clauses)
    # Existential split of (-c OR l1 OR l2 OR l3).
    for l1, l2, l3 in base:
        a = b.var()
        b.add(-c, l1, a)
        b.add(-a, l2, l3)
    return tuple(b.clauses), b.nvars, boundary, fn, circuit_clauses


def all_sign_clauses() -> tuple[Clause, ...]:
    return tuple(tuple((i + 1) if bit else -(i + 1) for i, bit in enumerate(row))
                 for row in itertools.product((False, True), repeat=3))


def properize_binary(a: int, b: int, z: int) -> tuple[Clause, Clause]:
    return ((a, b, z), (a, b, -z))


def hostile_controls() -> list[tuple[str, Formula, int]]:
    parity0 = ((1, 2, 3), (1, -2, -3), (-1, 2, -3), (-1, -2, 3))
    parity1 = ((-1, -2, -3), (-1, 2, 3), (1, -2, 3), (1, 2, -3))
    horn = ((-1, -2, 3), (-2, -3, 4), (-3, -4, 5), (-4, -5, 1))
    two: list[Clause] = []
    for j, pair in enumerate(((1, 2), (-1, 2), (1, -2)), start=3):
        two.extend(properize_binary(*pair, j))
    two_u = list(two); two_u.extend(properize_binary(-1, -2, 6))
    comps = parity0 + tuple(tuple((abs(x)+3) if x > 0 else -(abs(x)+3) for x in c)
                            for c in parity0)
    return [("affine_sat", parity0, 3), ("affine_unsat", parity0+parity1, 3),
            ("horn_sat", horn, 5), ("dual_horn_sat", tuple(tuple(-x for x in c) for c in horn), 5),
            ("padded_2sat_sat", tuple(two), 5), ("padded_2sat_unsat", tuple(two_u), 6),
            ("independent_components", comps, 6)]


def components(words: list[Word]) -> int:
    pool = set(words); ans = 0
    while pool:
        ans += 1; stack = [pool.pop()]
        while stack:
            w = stack.pop()
            for i in range(len(w)):
                v = w[:i] + (not w[i],) + w[i+1:]
                if v in pool:
                    pool.remove(v); stack.append(v)
    return ans


def anf_degree(fn: Callable[[Word], bool], d: int) -> int:
    vals = [int(fn(tuple(bool((x >> i) & 1) for i in range(d)))) for x in range(1 << d)]
    for i in range(d):
        for mask in range(1 << d):
            if mask & (1 << i): vals[mask] ^= vals[mask ^ (1 << i)]
    return max((mask.bit_count() for mask, v in enumerate(vals) if v), default=-1)


def adaptive_transcript(fn: Callable[[Word], bool], source_bit: bool, d: int, seed: int, steps: int):
    rng = random.Random(seed); history: list[bool] = []; direct: list[bool] = []
    cached: bool | None = None; factored: list[bool] = []; source_calls = 0
    for j in range(steps):
        salt = sum((i+1)*(3 if x else 1) for i, x in enumerate(history))
        value = (rng.randrange(1 << d) ^ salt ^ (j * 0x9E37)) & ((1 << d)-1)
        w = tuple(bool((value >> i) & 1) for i in range(d))
        c = fn(w); ans = c and source_bit; direct.append(ans)
        if not c:
            got = False
        else:
            if cached is None:
                cached = source_bit; source_calls += 1
            got = cached
        factored.append(got); history.append(got)
    assert direct == factored and source_calls <= 1
    return source_calls, len(direct)


def encoded_bits(n: int, m: int) -> int:
    h = math.ceil(math.log2(max(2, 64*(n+m+1))))
    return (4*m+2)*h


def main() -> None:
    kinds = ("singleton_zero", "co_singleton_one", "subcube", "even_parity", "two_corners", "prefix_union")
    stats = {k: 0 for k in ("base_cases", "base_sat", "base_unsat", "constructions", "root_checks",
                            "boundary_checks", "support_nonempty", "adaptive_transcripts", "adaptive_queries",
                            "source_label_calls", "properness_checks", "size_checks")}
    geometry: list[dict] = []

    def run_case(name: str, base: Formula, nbase: int, d: int) -> None:
        z = brute_label(base, nbase); stats["base_cases"] += 1
        stats["base_sat"] += int(z); stats["base_unsat"] += int(not z)
        for kind in kinds:
            h, nv, boundary, fn, circuit_m = construct(base, nbase, d, kind)
            assert all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in h)
            stats["properness_checks"] += len(h)
            words = [tuple(bool((v >> i) & 1) for i in range(d)) for v in range(1 << d)]
            supp = [w for w in words if fn(w)]; assert supp; stats["support_nonempty"] += 1
            assert sat(h) == z; stats["root_checks"] += 1
            for w in words:
                got = sat(h, dict(zip(boundary, w)))
                assert got == (fn(w) and z), (name, kind, w, got, z)
                stats["boundary_checks"] += 1
            for seed in range(5):
                calls, q = adaptive_transcript(fn, z, d, seed + 131*d, 2*(1 << d)+3)
                stats["adaptive_transcripts"] += 1; stats["adaptive_queries"] += q
                stats["source_label_calls"] += calls
            assert encoded_bits(nv, len(h)) >= encoded_bits(nbase, len(base))
            stats["size_checks"] += 1; stats["constructions"] += 1
            if (name in {"allclauses", "single"} and
                    not any(row["base"] == name and row["support"] == kind for row in geometry)):
                geometry.append({"base": name, "base_sat": z, "d": d, "support": kind,
                                 "support_size": len(supp), "hamming_components": components(supp),
                                 "anf_degree": anf_degree(fn, d), "circuit_clauses": circuit_m,
                                 "total_clauses": len(h), "variables": nv})

    signs = all_sign_clauses()
    for mask in range(1, 1 << 8):
        base = tuple(signs[i] for i in range(8) if mask & (1 << i))
        run_case("allclauses" if mask == 255 else ("single" if mask & (mask-1) == 0 else f"mask{mask}"), base, 3, 3)
    for name, base, nv in hostile_controls(): run_case(name, base, nv, 4)
    rng = random.Random(128)
    for j in range(48):
        clauses: list[Clause] = []
        for _ in range(rng.randint(1, 8)):
            vs = rng.sample(range(1, 6), 3)
            clauses.append(tuple(v if rng.getrandbits(1) else -v for v in vs))  # type: ignore[arg-type]
        run_case(f"random{j}", tuple(dict.fromkeys(clauses)), 5, 4)

    source = Path(__file__).read_bytes()
    result = {
        "run_id": "BOUNDARY-ORACLE-FACTOR128",
        "status": "COMPUTATIONAL finite audit; symbolic theorem in report",
        "seed": 128,
        "identity": "SAT(H[F,C][b]) = C(b) AND SAT(F); nonempty C implies SAT(H)=SAT(F)",
        "adaptive_factor": "all boundary transcripts use at most one cached SAT(F) bit",
        "size": "n+m+O(|C|) variables and 2m+O(|C|) proper clauses; pinned children remain exponent-1 scale",
        "stats": stats,
        "assertion_accounted_checks": sum(stats.values()),
        "geometry_examples": geometry[:36],
        "script_sha256": hashlib.sha256(source).hexdigest(),
    }
    Path("boundary_oracle_factor128_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__": main()
