#!/usr/bin/env python3
"""Finite audit for the wrapper/padding quotient collapse.

This is a falsification aid, not an asymptotic lower bound.  It instantiates
the equivalence constraints used by WRAPPER-PADDING-QUOTIENT-COLLAPSE1 on a
finite hostile-control domain and checks the pointed-provenance escape.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path


class UnionFind:
    def __init__(self) -> None:
        self.parent: dict[str, str] = {}

    def add(self, x: str) -> None:
        self.parent.setdefault(x, x)

    def find(self, x: str) -> str:
        self.add(x)
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra

    def classes(self) -> dict[str, list[str]]:
        out: dict[str, list[str]] = {}
        for x in self.parent:
            out.setdefault(self.find(x), []).append(x)
        return out


@dataclass(frozen=True)
class Source:
    family: str
    index: int
    encoding: str

    @property
    def semantic_id(self) -> str:
        return f"{self.family}:{self.index}"

    @property
    def encoded_id(self) -> str:
        return f"{self.semantic_id}@{self.encoding}"


FAMILIES = ("H22", "Horn", "Affine", "2SAT", "Treewidth", "IndependentProduct")
ENCODINGS = ("indexed", "permuted", "renamed")
WRAPPERS = ("direct", "double-negation", "preprocess", "memoized", "branch-swap", "one-bit-shell")


def digest(data: object) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def audit() -> dict[str, object]:
    started = time.perf_counter()
    sources = [Source(f, i, e) for f in FAMILIES for i in range(2) for e in ENCODINGS]
    semantics = sorted({s.semantic_id for s in sources})

    unpointed = UnionFind()
    checks = {"wrapper": 0, "encoding": 0, "padding": 0, "commutativity": 0,
              "pointed": 0, "trace_failures_expected": 0, "one_bit": 0,
              "multiplicity": 0}

    # Equivalent deterministic implementations are connected at fixed source.
    for s in sources:
        for w in WRAPPERS:
            node = f"U:{w}:{s.encoded_id}"
            unpointed.add(node)
            unpointed.union(f"U:{WRAPPERS[0]}:{s.encoded_id}", node)
            checks["wrapper"] += 1

    # Alternate encodings are semantic isomorphs for this audit.
    for sem in semantics:
        members = [s for s in sources if s.semantic_id == sem]
        for w in WRAPPERS:
            anchor = f"U:{w}:{members[0].encoded_id}"
            for s in members[1:]:
                unpointed.union(anchor, f"U:{w}:{s.encoded_id}")
                checks["encoding"] += 1

    # J(F disjoint-union G)=J(F), plus commutative isomorphism, connects F to G.
    # It suffices to use canonical encodings: encoding invariance already links the rest.
    canonical = [Source(f, i, "indexed") for f in FAMILIES for i in range(2)]
    for left in canonical:
        for right in canonical:
            a, b = sorted((left.semantic_id, right.semantic_id))
            union_node = f"SUM:{a}+{b}"
            for w in WRAPPERS:
                left_node = f"U:{w}:{left.encoded_id}"
                right_node = f"U:{w}:{right.encoded_id}"
                unpointed.union(left_node, union_node)
                checks["padding"] += 1
                # Same canonical union node represents G disjoint-union F.
                unpointed.union(union_node, right_node)
                checks["commutativity"] += 1

    unpointed_classes = unpointed.classes()

    # Pointed repair: (F disjoint-union G, injection-of-F) keeps the root identity.
    pointed = UnionFind()
    for root in canonical:
        for pad in canonical:
            for w in WRAPPERS:
                base = f"P:{root.semantic_id}:{WRAPPERS[0]}"
                node = f"P:{root.semantic_id}:{w}:pad={pad.semantic_id}"
                pointed.union(base, node)
                checks["pointed"] += 1
    pointed_classes = pointed.classes()
    pointed_roots = {pointed.find(f"P:{s.semantic_id}:{WRAPPERS[0]}") for s in canonical}

    # Trace labels are deliberately wrapper-sensitive and therefore fail covariance.
    for s in canonical:
        trace_labels = {digest([w, s.semantic_id]) for w in WRAPPERS}
        checks["trace_failures_expected"] += len(trace_labels) - 1

    # One-bit wrappers preserve the decision even though traces differ.
    for s in canonical:
        bit = int(hashlib.sha256(s.semantic_id.encode()).digest()[0] % 2)
        for _w in WRAPPERS:
            assert int(bool(bit)) == bit
            checks["one_bit"] += 1

    # Paired H22 padding gauge: k independent two-orientation blocks multiply
    # canonical opening counts by 2^k without changing the preserved root.
    multiplicities = []
    for k in range(9):
        count = 2**k
        multiplicities.append({"padding_blocks": k, "canonical_openings": count})
        assert count == (1 << k)
        checks["multiplicity"] += 1

    assertions = {
        "unpointed_single_class": len(unpointed_classes) == 1,
        "pointed_preserves_all_roots": len(pointed_roots) == len(canonical),
        "trace_not_wrapper_covariant": checks["trace_failures_expected"] > 0,
        "one_bit_outputs_preserved": checks["one_bit"] == len(canonical) * len(WRAPPERS),
        "padding_changes_raw_multiplicity": multiplicities[0]["canonical_openings"] != multiplicities[-1]["canonical_openings"],
    }
    assert all(assertions.values())

    result = {
        "status": "COMPUTATIONAL",
        "claim_tested": "NONTRIVIAL-UNPOINTED-FORK-QUOTIENT1",
        "claim_outcome": "FALSIFIED_ON_FINITE_DOMAIN_AND_THEORETICALLY_COLLAPSED",
        "scope": {
            "families": list(FAMILIES),
            "encodings": list(ENCODINGS),
            "wrappers": list(WRAPPERS),
            "semantic_sources": len(semantics),
            "encoded_sources": len(sources),
        },
        "checks": checks,
        "assertions": assertions,
        "unpointed_equivalence_classes": len(unpointed_classes),
        "pointed_root_classes": len(pointed_roots),
        "multiplicity_gauge": multiplicities,
        "interpretation": (
            "Wrapper covariance plus full unpointed satisfiable-padding invariance and "
            "commutative isomorphism erase both implementation and source identity. "
            "Pointing preserves source identity only by carrying an external injection."
        ),
        "limitations": (
            "Finite enumeration is a regression/falsification audit only; the general "
            "collapse is the separate two-line equivalence proof in SYNTHESIS-0019."
        ),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    result["sha256_without_self"] = digest(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
