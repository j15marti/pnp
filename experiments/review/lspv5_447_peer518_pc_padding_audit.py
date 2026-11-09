#!/usr/bin/env python3
"""Independent red-team audit of LSPV-1/518.

This does not execute R_mix341 and does not establish any mixed-system transfer.
It checks the exact source-count convention and the two elementary PC padding
simulations used to transfer a published fixed-r Res(PC_r/F_2) lower bound.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import resource
import time
from dataclasses import dataclass
from pathlib import Path


Monomial = tuple[str, ...]
Polynomial = frozenset[Monomial]


def add(*ps: Polynomial) -> Polynomial:
    """Addition over F_2: symmetric difference of monomial supports."""
    out: set[Monomial] = set()
    for p in ps:
        for m in p:
            if m in out:
                out.remove(m)
            else:
                out.add(m)
    return frozenset(out)


def mul(p: Polynomial, q: Polynomial) -> Polynomial:
    """Formal polynomial multiplication over F_2, without multilinearizing."""
    terms: list[Polynomial] = []
    for a in p:
        for b in q:
            terms.append(frozenset((tuple(sorted(a + b)),)))
    return add(*terms) if terms else frozenset()


ONE: Polynomial = frozenset(((),))
ZERO: Polynomial = frozenset()


def var(name: str) -> Polynomial:
    return frozenset(((name,),))


@dataclass(frozen=True)
class Lit:
    name: str
    positive: bool


def literal_falsity(lit: Lit) -> Polynomial:
    # Pang: Q_x=1-x and Q_not-x=x. In F_2, subtraction is addition.
    return add(ONE, var(lit.name)) if lit.positive else var(lit.name)


def clause_falsity(clause: tuple[Lit, ...]) -> Polynomial:
    p = ONE
    for lit in clause:
        p = mul(p, literal_falsity(lit))
    return p


def substitute_z_zero(p: Polynomial) -> Polynomial:
    return frozenset(m for m in p if "z" not in m)


def canonical_clause(clause: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(clause, key=lambda x: (abs(x), x < 0)))


def uniqueness_clauses(edge: int, ordered: bool) -> list[tuple[int, int]]:
    pairs = (
        ((a, b) for a in range(3) for b in range(3) if a != b)
        if ordered
        else itertools.combinations(range(3), 2)
    )
    return [canonical_clause((-(3 * edge + a + 1), -(3 * edge + b + 1))) for a, b in pairs]


def source_counts(h: int) -> dict[str, int]:
    if h % 2:
        raise ValueError("a cubic graph has even order")
    edges = 3 * h // 2
    unordered = [c for e in range(edges) for c in uniqueness_clauses(e, False)]
    ordered = [c for e in range(edges) for c in uniqueness_clauses(e, True)]
    ordered_set = set(ordered)
    return {
        "vertices": h,
        "edges": edges,
        "existence": edges,
        "flow_forbidden": 18 * h,
        "uniqueness_unordered_records": len(unordered),
        "uniqueness_ordered_records": len(ordered),
        "uniqueness_ordered_distinct_clauses": len(ordered_set),
        "canonical_original_clauses": edges + len(ordered_set) + 18 * h,
        "strict_clauses_from_canonical_set": edges + 2 * len(ordered_set) + 18 * h,
    }


def check_padding_identities() -> dict[str, object]:
    checks = 0
    examples = []
    signs = (False, True)
    # Exhaust every signed binary clause on two distinct old variables.
    for sx, sy in itertools.product(signs, repeat=2):
        b = (Lit("x", sx), Lit("y", sy))
        bp = b + (Lit("z", True),)
        bm = b + (Lit("z", False),)
        qb, qbp, qbm = map(clause_falsity, (b, bp, bm))
        assert add(qbp, qbm) == qb
        assert substitute_z_zero(qbp) == qb
        assert substitute_z_zero(qbm) == ZERO
        # A same-polarity corruption must not pass as a complementary pair.
        assert add(qbp, qbp) != qb
        checks += 4
        examples.append({
            "signs_positive": [sx, sy],
            "degrees": [max(map(len, qb), default=0), max(map(len, qbp), default=0), max(map(len, qbm), default=0)],
        })

    # Negative controls: freshness and properness are syntactic obligations.
    nonfresh = (Lit("x", True), Lit("y", True), Lit("x", False))
    repeated = (Lit("x", True), Lit("y", True), Lit("x", True))
    assert len({l.name for l in nonfresh}) != 3
    assert len({l.name for l in repeated}) != 3
    checks += 2

    # PC inference commutation, exhaustively for a finite basis of small lines.
    basis = [
        ZERO,
        ONE,
        var("x"),
        var("y"),
        var("z"),
        add(ONE, var("x")),
        mul(var("x"), add(ONE, var("z"))),
    ]
    for f, g in itertools.product(basis, repeat=2):
        assert substitute_z_zero(add(f, g)) == add(substitute_z_zero(f), substitute_z_zero(g))
        for name in ("x", "y", "z"):
            left = substitute_z_zero(mul(var(name), f))
            right = ZERO if name == "z" else mul(var(name), substitute_z_zero(f))
            assert left == right
            checks += 1
        checks += 1

    return {"checks": checks, "examples": examples}


def main() -> None:
    started = time.perf_counter_ns()
    pang_tex = Path("pang518/deg--size.tex")
    tex_bytes = pang_tex.read_bytes()
    tex = tex_bytes.decode("utf-8")
    exact_fragments = [
        r"\neg x_{e,a}\vee \neg x_{e,b}$ for $a\neq b$",
        r"A refutation is a finite DAG ending with the empty clause.",
        r"Its \emph{size} $S$ is the number of nodes in the DAG.",
        r"for a fixed prime $q\ne p$ and a family of fixed-degree regular edge expanders",
    ]
    for fragment in exact_fragments:
        assert fragment in tex, fragment

    counts = [source_counts(h) for h in (4, 6, 8, 10)]
    for row in counts:
        h = row["vertices"]
        assert row["canonical_original_clauses"] == 24 * h
        assert row["strict_clauses_from_canonical_set"] == 57 * h // 2
        assert row["uniqueness_ordered_records"] == 2 * row["uniqueness_ordered_distinct_clauses"]

    padding = check_padding_identities()
    out = {
        "status": "PASS",
        "scope": "independent finite symbolic/source audit; not R_mix341",
        "pang_source": {
            "file": str(pang_tex),
            "sha256": hashlib.sha256(tex_bytes).hexdigest(),
            "arxiv_source_archive_sha256": hashlib.sha256(Path("pang518/2610.00837v2.tar.gz").read_bytes()).hexdigest(),
            "version": "2610.00837v2",
            "publication_status": "2026 preprint",
        },
        "source_count_controls": counts,
        "padding_pc_controls": padding,
        "finding": (
            "The a!=b notation emits each uniqueness clause twice if read as ordered records, "
            "but Pang defines a CNF/clause collection as a set for Q(F); canonical deduplication "
            "gives 24h original clauses and 57h/2 strict clauses. Exact byte encoders must state "
            "the unordered-pair or deduplication convention. Both PC degree simulations pass."
        ),
        "open": [
            "all-rule historical R_mix341 transfer",
            "superpolynomial Wbar_Rmix341",
            "noncircular same-calculus B3",
        ],
    }
    out["resource_observation"] = {
        "elapsed_ns": time.perf_counter_ns() - started,
        "max_rss_kib_platform_reported": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "note": "single local CPython replay; not an asymptotic proof-search bound",
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
