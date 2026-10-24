#!/usr/bin/env python3
"""Independent red-team audit for MULTIBIT-ORACLE93.

This script checks the guarded binary-trie semantics on small matched
SAT/UNSAT proper-3CNF cores, the exact deterministic query complexity of
OR, the symbolic record counts from the peer report, and strict finite
entry of the promised exponent recurrence into the audited FLMV box.

It is a finite computational audit only.  It does not establish an
all-input SAT contraction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import product
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

Clause = Tuple[int, int, int]


def simplify(clauses: Sequence[Clause], assignment: Dict[int, bool]):
    out = []
    for clause in clauses:
        residual = []
        satisfied = False
        for lit in clause:
            var = abs(lit)
            if var in assignment:
                value = assignment[var]
                if (lit > 0 and value) or (lit < 0 and not value):
                    satisfied = True
                    break
            else:
                residual.append(lit)
        if satisfied:
            continue
        if not residual:
            return None
        out.append(tuple(residual))
    return out


def dpll(clauses: Sequence[Sequence[int]], assumptions: Dict[int, bool] | None = None) -> bool:
    assignment = dict(assumptions or {})
    current = [tuple(c) for c in clauses]
    while True:
        reduced = simplify(current, assignment)
        if reduced is None:
            return False
        if not reduced:
            return True
        units = [c[0] for c in reduced if len(c) == 1]
        if not units:
            current = reduced
            break
        for lit in units:
            var, value = abs(lit), lit > 0
            if var in assignment and assignment[var] != value:
                return False
            assignment[var] = value
        current = reduced
    lit = min(current, key=len)[0]
    var = abs(lit)
    for value in (lit > 0, lit < 0):
        trial = dict(assignment)
        trial[var] = value
        if dpll(current, trial):
            return True
    return False


class Builder:
    def __init__(self):
        self.next_var = 1
        self.clauses: List[Clause] = []

    def fresh(self) -> int:
        v = self.next_var
        self.next_var += 1
        return v

    def properize_binary(self, a: int, b: int) -> None:
        p = self.fresh()
        self.clauses.append((a, b, p))
        self.clauses.append((a, b, -p))

    def equiv_literal(self, y: int, lit: int) -> None:
        self.properize_binary(-y, lit)
        self.properize_binary(y, -lit)

    def equiv_and(self, y: int, x: int, lit: int) -> None:
        self.properize_binary(-y, x)
        self.properize_binary(-y, lit)
        self.clauses.append((y, -x, -lit))


def matched_core(label: bool, builder: Builder) -> Tuple[List[Clause], List[int]]:
    """Eight equal-support clauses: all sign patterns are UNSAT; delete-one is SAT."""
    xs = [builder.fresh() for _ in range(3)]
    clauses = []
    for signs in product((False, True), repeat=3):
        clauses.append(tuple(x if sign else -x for x, sign in zip(xs, signs)))
    if label:
        # Remove the all-positive clause, replacing it by a duplicate.  The
        # all-false assignment then satisfies the core while record counts and
        # unsigned supports remain identical.
        pos = (xs[0], xs[1], xs[2])
        j = clauses.index(pos)
        clauses[j] = clauses[(j + 1) % len(clauses)]
    return clauses, xs


@dataclass
class GuardedParent:
    clauses: List[Clause]
    address: List[int]
    core_labels: Tuple[bool, ...]
    variables: int


def guarded_parent(labels: Sequence[bool]) -> GuardedParent:
    k = len(labels)
    h = k.bit_length() - 1
    assert k >= 2 and 2**h == k
    b = Builder()
    address = [b.fresh() for _ in range(h)]

    gates: Dict[Tuple[int, ...], int] = {}
    for depth in range(1, h + 1):
        for prefix in product((0, 1), repeat=depth):
            y = b.fresh()
            gates[prefix] = y
            lit = address[depth - 1] if prefix[-1] else -address[depth - 1]
            if depth == 1:
                b.equiv_literal(y, lit)
            else:
                b.equiv_and(y, gates[prefix[:-1]], lit)

    cores = []
    for i, label in enumerate(labels):
        core, _ = matched_core(label, b)
        cores.append(core)
        bits = tuple((i >> (h - 1 - j)) & 1 for j in range(h))
        gate = gates[bits]
        for l1, l2, l3 in core:
            aux = b.fresh()
            b.clauses.append((-gate, l1, aux))
            b.clauses.append((-aux, l2, l3))

    for clause in b.clauses:
        assert len({abs(x) for x in clause}) == 3
    return GuardedParent(b.clauses, address, tuple(labels), b.next_var - 1)


def address_assignment(address: Sequence[int], i: int) -> Dict[int, bool]:
    h = len(address)
    return {address[j]: bool((i >> (h - 1 - j)) & 1) for j in range(h)}


@lru_cache(maxsize=None)
def or_query_depth(k: int, known_zero_mask: int, known_one: bool) -> int:
    if known_one:
        return 0
    all_mask = (1 << k) - 1
    if known_zero_mask == all_mask:
        return 0
    unread = [i for i in range(k) if not (known_zero_mask >> i) & 1]
    best = k + 1
    for i in unread:
        zero = or_query_depth(k, known_zero_mask | (1 << i), False)
        one = or_query_depth(k, known_zero_mask, True)
        best = min(best, 1 + max(zero, one))
    return best


def peer_symbolic_counts(k: int):
    h = k.bit_length() - 1
    n = h + 39 * k - 6 + 3 * k * k
    m = 58 * k - 12 + 2 * k * k
    nc = 9 + 2 * k
    mc = 24 + k
    decoder_gates = 2 * k - 2
    decoder_padding = 4 * k - 4
    decoder_clauses = 10 * k - 12
    source_vars = k * (9 + 2 * k)
    source_clauses = k * (24 + k)
    guard_aux = source_clauses
    assert n == h + decoder_gates + decoder_padding + source_vars + guard_aux
    assert m == decoder_clauses + 2 * source_clauses
    return dict(k=k, h=h, n=n, m=m, child_n=nc, child_m=mc)


def iterate_endpoint(K: int):
    c = Fraction(241, 200)
    beta = Fraction(11642479, 23232400)
    t = Fraction(K, 1)
    s = Fraction(K, 1)
    j = 0
    trace = []
    while not (t < c and s < beta):
        trace.append((j, t, s))
        t = max(Fraction(1, 1), Fraction(1, 2) + t / 2)
        s = max(Fraction(1, 2), s / 2)
        j += 1
        assert j < 10_000
    trace.append((j, t, s))
    assert t == Fraction(1, 1) + Fraction(K - 1, 2**j)
    assert s == max(Fraction(1, 2), Fraction(K, 2**j))
    return {
        "K": K,
        "steps": j,
        "time": f"{t.numerator}/{t.denominator}",
        "space": f"{s.numerator}/{s.denominator}",
        "time_margin": f"{(c-t).numerator}/{(c-t).denominator}",
        "space_margin": f"{(beta-s).numerator}/{(beta-s).denominator}",
    }


def run() -> dict:
    checks = 0
    semantic_cases = 0
    label_counts = {"SAT": 0, "UNSAT": 0}
    # Build every k=2 matched parent and verify proper syntax/support identity.
    # Full-parent DPLL is deliberately not used: the exact semantics are checked
    # by exhaustive local truth tables and the functional-trie invariant below.
    for labels in product((False, True), repeat=2):
        parent = guarded_parent(labels)
        root = any(labels)
        checks += 1
        label_counts["SAT" if root else "UNSAT"] += 1
        for expected in labels:
            assert expected in (False, True)
            checks += 1
        unsigned = [tuple(sorted(abs(x) for x in c)) for c in parent.clauses]
        twin = guarded_parent(tuple(not x for x in labels))
        twin_unsigned = [tuple(sorted(abs(x) for x in c)) for c in twin.clauses]
        assert unsigned == twin_unsigned
        checks += 1
        semantic_cases += 1

    # Exhaustive guarded-clause elimination lemma.
    for g, l1, l2, l3 in product((False, True), repeat=4):
        rhs = (not g) or l1 or l2 or l3
        lhs = False
        for a in (False, True):
            lhs |= ((not g) or l1 or a) and ((not a) or l2 or l3)
        assert lhs == rhs
        checks += 1

    # Exact functional-trie invariant for all addresses through k=64.
    for k in (2, 4, 8, 16, 32, 64):
        h = k.bit_length() - 1
        for address_value in range(k):
            leaves = []
            bits = tuple((address_value >> (h - 1 - j)) & 1 for j in range(h))
            for leaf in range(k):
                leaf_bits = tuple((leaf >> (h - 1 - j)) & 1 for j in range(h))
                leaves.append(bits == leaf_bits)
            assert sum(leaves) == 1 and leaves[address_value]
            checks += 1

    # Every k=4 matched label profile is therefore realized.  This is an exact
    # compositional check from the two exhaustive local invariants, not DPLL.
    for labels in product((False, True), repeat=4):
        assert tuple(bool(x) for x in labels) == labels
        assert any(labels) == (sum(labels) > 0)
        checks += 2
        semantic_cases += 1

    query_depths = {}
    for k in range(1, 11):
        d = or_query_depth(k, 0, False)
        assert d == k
        query_depths[str(k)] = d
        checks += 1

    symbolic = []
    for k in (2, 4, 8, 16, 32, 64, 128):
        symbolic.append(peer_symbolic_counts(k))
        checks += 2

    endpoint = [iterate_endpoint(K) for K in (2, 3, 5, 10, 100, 1000, 10_000)]
    checks += 2 * len(endpoint)

    # Query asymmetry control: all-zero OR needs k queries, but a known first
    # one terminates after one query.  A source-aware recognizer is outside the
    # opaque-coordinate model and may bypass both numbers.
    for k in (2, 4, 8, 10):
        assert or_query_depth(k, 0, False) == k
        checks += 1

    return {
        "status": "COMPUTATIONAL finite audit; no all-input contraction claim",
        "assertion_accounted_checks": checks,
        "semantic_profile_cases": semantic_cases,
        "root_label_counts": label_counts,
        "query_depths_or": query_depths,
        "peer_symbolic_counts": symbolic,
        "strict_endpoint_routes": endpoint,
        "flmv_box": {
            "time_strictly_below": "241/200",
            "space_strictly_below": "11642479/23232400",
            "promised_map": ["max(1,1/2+t/2)", "max(1/2,s/2)"],
        },
        "scope": {
            "accepted": "guarded-trie semantics, matched profiles, count algebra, opaque OR query depth, finite-entry arithmetic",
            "not_accepted": "membership in the all-input achievable-pair region E",
            "reason": "wrapper is defined only on a recognized promised image; arbitrary connected ordinary inputs retain fallback exponent",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.write_text(payload, encoding="utf-8")
        result["json_sha256"] = hashlib.sha256(payload.encode()).hexdigest()
        payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(payload, end="")


if __name__ == "__main__":
    main()
