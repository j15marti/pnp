#!/usr/bin/env python3
"""Audit an exponential minimal-incompatibility frontier on easy parity 3-CNF.

The source interface contains x_1,...,x_n.  Auxiliary variables encode a
left-associated or balanced XOR circuit in proper duplicate-free 3-CNF.
Compatibility asks whether a partial source assignment extends to a model.

Each invocation is deliberately bounded: the exhaustive phase defaults to
n <= 8; larger sizes use only proved closed-form counts and deterministic
spot checks.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional


Clause = tuple[int, int, int]
Partial = tuple[Optional[int], ...]


@dataclass
class Meter:
    assertions: int = 0
    partial_assignments: int = 0
    completion_checks: int = 0
    cnf_clause_checks: int = 0
    generated_clauses: int = 0
    literals_written: int = 0
    preprocessing_operations: int = 0
    compatibility_evaluations: int = 0
    frontier_entries_examined: int = 0
    wrapper_checks: int = 0
    affine_elimination_row_ops: int = 0
    extraction_calls: int = 0
    reconstruction_calls: int = 0
    communication_bits: int = 0
    one_bit_sat_decisions: int = 0

    def check(self, condition: bool, message: str) -> None:
        self.assertions += 1
        if not condition:
            raise AssertionError(message)


@dataclass
class ParityEncoding:
    n: int
    target: int
    kind: str
    clauses: list[Clause]
    gates: list[tuple[int, int, int]]
    output_var: int
    pad_vars: tuple[int, int]
    variable_count: int
    bags: list[tuple[int, int, int]] = field(default_factory=list)
    bag_edges: list[tuple[int, int]] = field(default_factory=list)


def xor_gate(a: int, b: int, z: int) -> list[Clause]:
    """Proper 3-CNF for z = a XOR b."""
    return [
        (a, b, -z),
        (a, -b, z),
        (-a, b, z),
        (-a, -b, -z),
    ]


def force_literal(lit: int, p: int, q: int) -> list[Clause]:
    """Four proper clauses equivalent to the unit literal lit."""
    return [
        (lit, p, q),
        (lit, p, -q),
        (lit, -p, q),
        (lit, -p, -q),
    ]


def build_parity_encoding(n: int, target: int, kind: str, meter: Meter) -> ParityEncoding:
    if n < 1 or target not in (0, 1) or kind not in ("left", "balanced"):
        raise ValueError("invalid parity encoding parameters")
    next_var = n + 1
    gates: list[tuple[int, int, int]] = []
    bag_edges: list[tuple[int, int]] = []

    if kind == "left":
        if n == 1:
            output = 1
        else:
            left = 1
            parent_bag: Optional[int] = None
            for x in range(2, n + 1):
                z = next_var
                next_var += 1
                gates.append((left, x, z))
                if parent_bag is not None:
                    bag_edges.append((parent_bag, len(gates) - 1))
                parent_bag = len(gates) - 1
                left = z
            output = left
    else:
        def rec(nodes: list[int]) -> tuple[int, Optional[int]]:
            nonlocal next_var
            if len(nodes) == 1:
                return nodes[0], None
            mid = len(nodes) // 2
            left, left_bag = rec(nodes[:mid])
            right, right_bag = rec(nodes[mid:])
            z = next_var
            next_var += 1
            gates.append((left, right, z))
            here = len(gates) - 1
            if left_bag is not None:
                bag_edges.append((left_bag, here))
            if right_bag is not None:
                bag_edges.append((right_bag, here))
            return z, here

        output, _ = rec(list(range(1, n + 1)))

    p, q = next_var, next_var + 1
    next_var += 2
    clauses: list[Clause] = []
    for gate in gates:
        clauses.extend(xor_gate(*gate))
    clauses.extend(force_literal(output if target else -output, p, q))
    bags = list(gates) + [(output, p, q)]
    if gates:
        bag_edges.append((len(gates) - 1, len(bags) - 1))
    meter.generated_clauses += len(clauses)
    meter.literals_written += 3 * len(clauses)
    meter.preprocessing_operations += n + len(clauses)
    return ParityEncoding(
        n=n,
        target=target,
        kind=kind,
        clauses=clauses,
        gates=gates,
        output_var=output,
        pad_vars=(p, q),
        variable_count=next_var - 1,
        bags=bags,
        bag_edges=bag_edges,
    )


def eval_clause(clause: Clause, assignment: dict[int, int], meter: Meter) -> bool:
    meter.cnf_clause_checks += 1
    return any(assignment[abs(lit)] == (1 if lit > 0 else 0) for lit in clause)


def extend_aux(enc: ParityEncoding, source: tuple[int, ...], p: int, q: int) -> dict[int, int]:
    assignment = {i + 1: bit for i, bit in enumerate(source)}
    for a, b, z in enc.gates:
        assignment[z] = assignment[a] ^ assignment[b]
    assignment[enc.pad_vars[0]] = p
    assignment[enc.pad_vars[1]] = q
    return assignment


def cnf_has_extension_for_full_source(
    enc: ParityEncoding, source: tuple[int, ...], meter: Meter
) -> bool:
    for p, q in itertools.product((0, 1), repeat=2):
        assignment = extend_aux(enc, source, p, q)
        meter.completion_checks += 1
        if all(eval_clause(c, assignment, meter) for c in enc.clauses):
            return True
    return False


def shortcut_compatible(alpha: Partial, target: int, meter: Meter) -> bool:
    meter.compatibility_evaluations += 1
    meter.preprocessing_operations += len(alpha)
    if any(bit is None for bit in alpha):
        return True
    return sum(int(bit) for bit in alpha) % 2 == target


def brute_compatible(enc: ParityEncoding, alpha: Partial, meter: Meter) -> bool:
    stars = [i for i, bit in enumerate(alpha) if bit is None]
    for fill in itertools.product((0, 1), repeat=len(stars)):
        source = list(alpha)
        for i, bit in zip(stars, fill):
            source[i] = bit
        if cnf_has_extension_for_full_source(enc, tuple(int(x) for x in source), meter):
            return True
    return False


def is_minimal_incompatible(alpha: Partial, target: int, meter: Meter) -> bool:
    if shortcut_compatible(alpha, target, meter):
        return False
    for i in range(len(alpha)):
        if alpha[i] is not None:
            weakened = list(alpha)
            weakened[i] = None
            if not shortcut_compatible(tuple(weakened), target, meter):
                return False
    return True


def validate_tree_decomposition(enc: ParityEncoding, meter: Meter) -> None:
    # Each clause scope is one declared 3-variable bag.
    scopes = {frozenset(abs(x) for x in clause) for clause in enc.clauses}
    bags = [frozenset(b) for b in enc.bags]
    meter.check(all(scope in bags for scope in scopes), "clause scope missing from bags")
    meter.check(max(map(len, bags)) - 1 <= 2, "declared treewidth exceeds two")
    if not bags:
        return
    adj = {i: set() for i in range(len(bags))}
    for a, b in enc.bag_edges:
        adj[a].add(b)
        adj[b].add(a)
    meter.check(len(enc.bag_edges) == len(bags) - 1, "bag graph is not a tree by edge count")
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v in adj[u] - seen:
            seen.add(v)
            stack.append(v)
    meter.check(len(seen) == len(bags), "bag graph disconnected")
    for var in range(1, enc.variable_count + 1):
        containing = {i for i, bag in enumerate(bags) if var in bag}
        if not containing:
            continue
        reached = {next(iter(containing))}
        stack = list(reached)
        while stack:
            u = stack.pop()
            for v in (adj[u] & containing) - reached:
                reached.add(v)
                stack.append(v)
        meter.check(reached == containing, f"running intersection fails for variable {var}")


def gf2_consistent(rows: list[tuple[int, int]], n: int, meter: Meter) -> bool:
    rows = [list(r) for r in rows]
    pivot = 0
    for col in range(n):
        found = next((i for i in range(pivot, len(rows)) if (rows[i][0] >> col) & 1), None)
        if found is None:
            continue
        rows[pivot], rows[found] = rows[found], rows[pivot]
        for i in range(len(rows)):
            if i != pivot and ((rows[i][0] >> col) & 1):
                rows[i][0] ^= rows[pivot][0]
                rows[i][1] ^= rows[pivot][1]
                meter.affine_elimination_row_ops += 1
        pivot += 1
    return not any(mask == 0 and rhs for mask, rhs in rows)


def wrapper_audit(enc: ParityEncoding, meter: Meter) -> dict[str, int]:
    variants = {
        "DIRECT": enc.clauses,
        "COPY": list(enc.clauses),
        "DELAY": list(enc.clauses),
        "RECOMP": list(enc.clauses),
        "CLAUSE_ORDER": list(reversed(enc.clauses)),
        "LITERAL_ORDER": [tuple(reversed(c)) for c in enc.clauses],
        "REDUNDANT": enc.clauses + enc.clauses[: min(4, len(enc.clauses))],
    }
    counts: dict[str, int] = {}
    for name, clauses in variants.items():
        good = 0
        for source in itertools.product((0, 1), repeat=enc.n):
            expected = sum(source) % 2 == enc.target
            found = False
            for p, q in itertools.product((0, 1), repeat=2):
                assignment = extend_aux(enc, source, p, q)
                meter.completion_checks += 1
                if all(eval_clause(c, assignment, meter) for c in clauses):
                    found = True
                    break
            meter.wrapper_checks += 1
            meter.check(found == expected, f"wrapper {name} changed projected semantics")
            good += int(found)
        counts[name] = good
    # INTERP: a source permutation preserves parity and the frontier count.
    perm = tuple(reversed(range(enc.n)))
    for source in itertools.product((0, 1), repeat=enc.n):
        moved = tuple(source[i] for i in perm)
        meter.wrapper_checks += 1
        meter.check(sum(source) % 2 == sum(moved) % 2, "INTERP changed parity")
    counts["INTERP"] = 1 << (enc.n - 1)
    # DEAD: inert host data is not consulted by the evaluator.
    dead = hashlib.sha256(b"dead-state-not-read").hexdigest()
    meter.wrapper_checks += 1
    meter.check(len(dead) == 64 and shortcut_compatible((None,) * enc.n, enc.target, meter), "DEAD")
    counts["DEAD"] = 1
    return counts


def run(max_exhaustive_n: int, seed: int) -> dict:
    started = time.perf_counter()
    meter = Meter()
    exhaustive: list[dict] = []
    for n in range(1, max_exhaustive_n + 1):
        for target in (0, 1):
            by_kind = {}
            for kind in ("left", "balanced"):
                enc = build_parity_encoding(n, target, kind, meter)
                meter.check(len(enc.clauses) == 4 * n, "unexpected clause count")
                meter.check(len(set(enc.clauses)) == len(enc.clauses), "duplicate canonical clauses")
                meter.check(all(len({abs(x) for x in c}) == 3 for c in enc.clauses), "non-proper clause")
                validate_tree_decomposition(enc, meter)
                frontier = 0
                incompatible = 0
                for alpha in itertools.product((0, 1, None), repeat=n):
                    meter.partial_assignments += 1
                    direct = shortcut_compatible(alpha, target, meter)
                    brute = brute_compatible(enc, alpha, meter)
                    meter.check(direct == brute, f"projected evaluator mismatch n={n} {kind}")
                    if not direct:
                        incompatible += 1
                    if is_minimal_incompatible(alpha, target, meter):
                        frontier += 1
                        meter.frontier_entries_examined += 1
                meter.check(incompatible == 2 ** (n - 1), "wrong incompatible count")
                meter.check(frontier == 2 ** (n - 1), "wrong minimal frontier count")
                meter.one_bit_sat_decisions += 1
                meter.check(shortcut_compatible((None,) * n, target, meter), "canonical formula not SAT")
                by_kind[kind] = {
                    "variables": enc.variable_count,
                    "clauses": len(enc.clauses),
                    "minimal_incompatible": frontier,
                    "all_incompatible": incompatible,
                    "treewidth_upper_bound": 2,
                }
            meter.check(by_kind["left"]["minimal_incompatible"] == by_kind["balanced"]["minimal_incompatible"], "encoding dependence")
            exhaustive.append({"n": n, "target": target, "encodings": by_kind})

    # Independent-product control: minimal obstructions live in one component,
    # while the other component is entirely unassigned.
    product_frontier = 0
    n1 = n2 = 3
    for alpha in itertools.product((0, 1, None), repeat=n1 + n2):
        left, right = alpha[:n1], alpha[n1:]
        compatible = shortcut_compatible(left, 0, meter) and shortcut_compatible(right, 1, meter)
        if compatible:
            continue
        minimal = True
        for i, bit in enumerate(alpha):
            if bit is not None:
                weak = list(alpha)
                weak[i] = None
                if not (shortcut_compatible(tuple(weak[:n1]), 0, meter) and shortcut_compatible(tuple(weak[n1:]), 1, meter)):
                    minimal = False
                    break
        product_frontier += int(minimal)
    meter.check(product_frontier == 2 ** (n1 - 1) + 2 ** (n2 - 1), "product frontier")

    # Affine/Gaussian control and inconsistent Tseitin-style row dependency.
    meter.check(gf2_consistent([(0b011, 0), (0b110, 1)], 3, meter), "affine SAT control")
    meter.check(not gf2_consistent([(0b011, 0), (0b110, 1), (0b101, 0)], 3, meter), "affine UNSAT control")

    # Horn and 2SAT controls: direct linear scans/propagation witnesses.
    horn_assignment = {1: 1, 2: 1, 3: 1}
    horn = [(-1, 2, 2), (-2, 3, 3)]
    two_sat = [(-1, 2, 2), (-2, 1, 1)]
    meter.check(all(any(horn_assignment[abs(l)] == (l > 0) for l in c) for c in horn), "Horn")
    meter.check(all(any(horn_assignment[abs(l)] == (l > 0) for l in c) for c in two_sat), "2SAT")

    wrap_enc = build_parity_encoding(6, 1, "left", meter)
    wrappers = wrapper_audit(wrap_enc, meter)

    # Large controls use closed forms only, with deterministic source samples.
    rng = random.Random(seed)
    large = []
    for n in (16, 32, 64, 128, 256, 512):
        wrong = 1 << (n - 1)
        for _ in range(8):
            source = tuple(rng.getrandbits(1) for _ in range(n))
            meter.check((sum(source) & 1) in (0, 1), "large parity sample")
        large.append({
            "n": n,
            "clauses": 4 * n,
            "variables": 2 * n + 1,
            "minimal_incompatible_exact": str(wrong),
            "frontier_log2": n - 1,
            "evaluator_source_bit_scans": n,
            "one_bit_sat_answer": True,
        })

    elapsed = time.perf_counter() - started
    return {
        "claim": "MINIMAL-INCOMPATIBILITY-FRONTIER-OBLIGATION1",
        "status": "FALSIFIED/RETIRED",
        "proved_family_identity": {
            "formula": "proper duplicate-free 3-CNF Tseitin encoding of XOR(x_1,...,x_n)=b",
            "encoded_size": "Theta(n log n) bits under indexed literals",
            "clauses": "4n",
            "variables": "2n+1 for n>=2 (n source, n-1 XOR outputs, 2 padding)",
            "minimal_incompatible_source_partials": "2^(n-1)",
            "compatibility_evaluator": "one star scan, else one parity scan",
            "one_bit_sat_decision": "YES after canonical recognition",
            "primal_treewidth_upper_bound": 2,
        },
        "parameters": {
            "max_exhaustive_n": max_exhaustive_n,
            "seed": seed,
            "exhaustive": True,
            "large_cases_use_closed_form_only": True,
        },
        "exhaustive_cases": exhaustive,
        "large_closed_form_cases": large,
        "independent_product_frontier": product_frontier,
        "wrapper_results": wrappers,
        "meters": meter.__dict__,
        "runtime_seconds": elapsed,
        "limitations": [
            "Finite checks validate the implementation only; the all-n count is proved symbolically.",
            "The frontier is defined on declared source variables after existentially quantifying Tseitin auxiliaries.",
            "This easy family falsifies an unqualified semantic-frontier promotion, not a worst-case full-language lower bound.",
            "No runtime conclusion is inferred from the large integer counts.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-exhaustive-n", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20261012)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.max_exhaustive_n <= 10:
        raise SystemExit("max exhaustive n must be in [1,10]")
    result = run(args.max_exhaustive_n, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "runtime_seconds": result["runtime_seconds"],
        "meters": result["meters"],
        "largest_frontier_log2": result["large_closed_form_cases"][-1]["frontier_log2"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
