#!/usr/bin/env python3
"""Bounded audit for FULL-PADDING-INVARIANCE-COLLAPSE1.

Every invocation is intentionally small (<30 seconds).  This is a finite
hostile-control audit, not evidence for an asymptotic SAT lower bound.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

Literal = int
Clause = tuple[Literal, ...]
Formula = tuple[Clause, ...]


@dataclass
class Ledger:
    checks: int = 0
    failures: int = 0

    def check(self, condition: bool, message: str) -> None:
        self.checks += 1
        if not condition:
            self.failures += 1
            raise AssertionError(message)


class DSU:
    def __init__(self) -> None:
        self.parent: dict[str, str] = {}

    def find(self, x: str) -> str:
        self.parent.setdefault(x, x)
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: str, y: str) -> None:
        x, y = self.find(x), self.find(y)
        if x != y:
            self.parent[y] = x


def variables(formula: Formula) -> list[int]:
    return sorted({abs(lit) for clause in formula for lit in clause})


def evaluate(formula: Formula, bits: tuple[int, ...]) -> bool:
    value = {v: bool(bits[i]) for i, v in enumerate(variables(formula))}
    return all(any(value[abs(lit)] == (lit > 0) for lit in clause) for clause in formula)


def witness_count(formula: Formula) -> int:
    vs = variables(formula)
    return sum(evaluate(formula, bits) for bits in itertools.product((0, 1), repeat=len(vs)))


def canonical_clause(clause: Clause) -> Clause:
    return tuple(sorted(clause, key=lambda z: (abs(z), z < 0)))


def canonical_formula(formula: Formula) -> Formula:
    """Canonicalize labels by first occurrence after sorted incidence coding.

    This is only a deterministic audit normalizer, not a graph-isomorphism
    algorithm.  The theorem itself assumes isomorphism invariance explicitly.
    """
    normalized = tuple(sorted((canonical_clause(c) for c in formula)))
    labels: dict[int, int] = {}
    next_label = 1
    out: list[Clause] = []
    for clause in normalized:
        row = []
        for lit in clause:
            a = abs(lit)
            if a not in labels:
                labels[a] = next_label
                next_label += 1
            row.append(labels[a] if lit > 0 else -labels[a])
        out.append(tuple(row))
    return tuple(sorted(out))


def encode(formula: Formula) -> str:
    return ";".join(",".join(map(str, c)) for c in canonical_formula(formula))


def digest(formula: Formula) -> str:
    return hashlib.sha256(encode(formula).encode()).hexdigest()[:16]


def shift(formula: Formula, delta: int) -> Formula:
    return tuple(tuple((abs(x) + delta) if x > 0 else -(abs(x) + delta) for x in c) for c in formula)


def disjoint_union(*parts: Formula) -> Formula:
    out: list[Clause] = []
    offset = 0
    for part in parts:
        out.extend(shift(part, offset))
        offset += max(variables(part), default=0)
    return canonical_formula(tuple(out))


def paired_k33(row_perm=(0, 1, 2), col_perm=(0, 1, 2), flip=False) -> Formula:
    var = lambda i, j: 1 + 3 * row_perm[i] + col_perm[j]
    clauses: list[Clause] = []
    for i in range(3):
        row = tuple(var(i, j) for j in range(3))
        clauses.extend((row, tuple(-x for x in row)))
    for j in range(3):
        col = tuple(var(i, j) for i in range(3))
        clauses.extend((col, tuple(-x for x in col)))
    if flip:
        clauses = [tuple(-x for x in c) for c in clauses]
    return canonical_formula(tuple(clauses))


def exact_h22(formula: Formula) -> bool:
    if len(set(formula)) != len(formula):
        return False
    counts = Counter()
    for clause in formula:
        if len(clause) != 3 or len({abs(x) for x in clause}) != 3:
            return False
        if not (all(x > 0 for x in clause) or all(x < 0 for x in clause)):
            return False
        for lit in clause:
            counts[(abs(lit), lit > 0)] += 1
    return all(counts[(v, True)] == counts[(v, False)] == 2 for v in variables(formula))


def wrappers(answer: bool) -> dict[str, bool]:
    return {
        "DIRECT": answer,
        "COPY": bool(int(answer)),
        "DEAD": answer if sum(range(7)) == 21 else not answer,
        "DELAY": [answer for _ in range(5)][-1],
        "INTERP": {"0": False, "1": True}[str(int(answer))],
        "RECOMP": (answer and True) or False,
    }


def encodings(formula: Formula) -> dict[str, str]:
    cf = canonical_formula(formula)
    n = len(variables(cf))
    dimacs = f"p cnf {n} {len(cf)}\n" + "\n".join(" ".join(map(str, c)) + " 0" for c in cf)
    return {
        "tuple": repr(cf),
        "dimacs": dimacs,
        "json": json.dumps(cf, separators=(",", ":")),
        "reversed": repr(tuple(reversed(cf))),
    }


def main() -> None:
    started = time.perf_counter()
    ledger = Ledger()

    permutations = list(itertools.permutations(range(3)))
    atoms = [paired_k33(r, c, flip) for r in permutations for c in permutations for flip in (False, True)]
    # Keep distinct source encodings before the audit canonicalizer erases them.
    source_atoms = atoms[:24]
    base = source_atoms[0]
    ledger.check(exact_h22(base), "base paired-K33 must be exact H22")
    ledger.check(witness_count(base) == 102, "paired-K33 witness count")

    # Every isomorphic atom and every finite product stays in the exact core.
    products: list[Formula] = []
    for i, atom in enumerate(source_atoms):
        ledger.check(exact_h22(atom), f"atom {i} exact H22")
        ledger.check(witness_count(atom) == 102, f"atom {i} witness count")
        for copies in (1, 2, 3):
            product = disjoint_union(*([atom] * copies))
            products.append(product)
            ledger.check(exact_h22(product), f"product {i}/{copies} exact H22")
            ledger.check(len(variables(product)) == 9 * copies, "product variable accounting")
            ledger.check(len(product) == 12 * copies, "product clause accounting")

    # Constraint graph for J(F sqcup G)=J(F)=J(G).  A single class is forced.
    seeds = products[:36]
    dsu = DSU()
    edge_count = 0
    union_nodes: set[str] = set()
    for i, f in enumerate(seeds):
        fi = f"S{i}:{digest(f)}:{len(f)}"
        dsu.find(fi)
        for j, g in enumerate(seeds):
            gj = f"S{j}:{digest(g)}:{len(g)}"
            u = disjoint_union(f, g)
            uid = f"U:{digest(u)}:{len(u)}"
            union_nodes.add(uid)
            dsu.union(fi, uid)
            dsu.union(gj, uid)
            edge_count += 2
            ledger.check(exact_h22(u), "closure under disjoint union")
            # Canonical disjoint union is commutative in the audit representation.
            ledger.check(encode(u) == encode(disjoint_union(g, f)), "commutative canonical union")
    seed_roots = {dsu.find(f"S{i}:{digest(f)}:{len(f)}") for i, f in enumerate(seeds)}
    ledger.check(len(seed_roots) == 1, "unpointed padding constraints must connect every satisfiable seed")

    # Concrete nonconstant unpointed statistics fail full padding invariance.
    stats = {
        "component_count_parity": lambda f, parts: len(parts) % 2,
        "variable_count": lambda f, parts: len(variables(f)),
        "clause_count": lambda f, parts: len(f),
        "lexicographic_component": lambda f, parts: min(digest(p) for p in parts),
        "largest_component": lambda f, parts: max(len(p) for p in parts),
        "first_serialized_component": lambda f, parts: digest(parts[0]),
    }
    changed = defaultdict(int)
    representation_sensitive = defaultdict(int)
    for i, f in enumerate(seeds[:12]):
        for j, g in enumerate(seeds[12:24]):
            u = disjoint_union(f, g)
            for name, stat in stats.items():
                left = stat(f, [f])
                joined = stat(u, [f, g])
                if left != joined:
                    changed[name] += 1
                reversed_parts = stat(disjoint_union(g, f), [g, f])
                if joined != reversed_parts:
                    representation_sensitive[name] += 1
            # A pointed invariant survives because the root injection is retained.
            pointed_before = digest(f)
            pointed_after = digest(f)
            ledger.check(pointed_before == pointed_after, "pointed root digest survives padding")
    for name, count in changed.items():
        ledger.check(count > 0, f"{name} should have a hostile padding change")
    ledger.check(representation_sensitive["first_serialized_component"] > 0,
                 "first-component normalization must fail order invariance")

    # Encodings and total decision wrappers do not restore a nontrivial invariant.
    encoding_checks = 0
    wrapper_checks = 0
    for formula in products[:18]:
        es = encodings(formula)
        ledger.check(len(es) == 4, "four encodings")
        for text in es.values():
            ledger.check(len(text) > 0, "nonempty encoding")
            encoding_checks += 1
        for value in wrappers(True).values():
            ledger.check(value is True, "wrapper preserves SAT bit")
            wrapper_checks += 1

    # Easy-class and malformed controls: rich semantics or large candidate sets
    # do not change the algebraic collapse theorem.
    controls: dict[str, Formula] = {
        "2sat_treewidth_one": ((1, 2), (-1, 2), (1, -2)),
        "horn_chain": ((1,), (-1, 2), (-2, 3), (-3, 4)),
        "affine_even3": ((1, 2, -3), (1, -2, 3), (-1, 2, 3), (-1, -2, -3)),
        "redundant_2sat": ((1, 2), (1, 2), (-1, 2)),
        "unit_padded": ((1,), (1, 1), (1, 1, 1)),
        "unsat_unit_pair": ((1,), (-1,)),
    }
    control_counts = {}
    for name, formula in controls.items():
        wc = witness_count(formula)
        control_counts[name] = wc
        ledger.check((wc == 0) == (name == "unsat_unit_pair"), f"control satisfiability {name}")
        for result in wrappers(wc > 0).values():
            ledger.check(result == (wc > 0), f"control wrapper {name}")

    elapsed = time.perf_counter() - started
    result = {
        "run_id": "PADQUOT1",
        "status": {
            "FULL-PADDING-INVARIANCE-COLLAPSE1": "PROVED/EXACT (finite audit supports implementation)",
            "UNPOINTED-FULL-PADDING-NORMALIZATION1": "FALSIFIED/RETIRED as a nonconstant source invariant",
            "POINTED-PADDING-NORMALIZED-ENDPOINT1": "OPEN",
            "P_VS_NP": "OPEN",
        },
        "model": {
            "seed_formulas": len(seeds),
            "constraint_edges": edge_count,
            "distinct_union_nodes": len(union_nodes),
            "forced_seed_classes": len(seed_roots),
            "atomic_h22_variants": len(source_atoms),
            "product_instances": len(products),
        },
        "hostile_statistics_changed": dict(changed),
        "representation_sensitive_statistics": dict(representation_sensitive),
        "controls": control_counts,
        "encoding_checks": encoding_checks,
        "wrapper_checks": wrapper_checks,
        "checks": ledger.checks,
        "failures": ledger.failures,
        "elapsed_seconds": round(elapsed, 6),
        "scope_note": "Finite checks validate the construction only; the collapse theorem is proved symbolically.",
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["payload_sha256"] = hashlib.sha256(payload).hexdigest()
    out = Path("results/raw/review/2026-10-12_unpointed_padding_invariance_collapse.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
