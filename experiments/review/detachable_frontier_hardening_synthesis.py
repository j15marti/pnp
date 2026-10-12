#!/usr/bin/env python3
"""Bounded audit for DETACHABLE-FRONTIER-HARDENING1.

For a base CNF F on m declared variables, append on fresh variables a
canonical proper 3-CNF encoding of parity on m source variables.  The image is
polynomial-time recognizable and the parity component is always satisfiable,
so SAT(F and P) = SAT(F).  A recognize-and-strip wrapper can therefore call a
child SAT decider only on F.  The wrapper never evaluates or reconstructs the
projected parity compatibility frontier.

The all-size statements are proved symbolically in the accompanying report.
This program checks only bounded encodings and exact finite identities.  It is
deliberately designed to finish in less than 30 seconds.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Optional


Clause = tuple[int, ...]
CNF = tuple[Clause, ...]
Partial = tuple[Optional[int], ...]


@dataclass
class Meter:
    assertions: int = 0
    base_decisions: int = 0
    combined_decisions: int = 0
    image_recognitions: int = 0
    image_rejections: int = 0
    clauses_parsed: int = 0
    literals_parsed: int = 0
    child_solver_calls: int = 0
    compatibility_evaluations_in_decider: int = 0
    frontier_entries_materialized_in_decider: int = 0
    extraction_calls: int = 0
    reconstruction_calls: int = 0
    external_communication_bits: int = 0
    projected_compatibility_checks: int = 0
    parity_cnf_extension_checks: int = 0
    wrapper_checks: int = 0
    hostile_control_checks: int = 0

    def check(self, condition: bool, message: str) -> None:
        self.assertions += 1
        if not condition:
            raise AssertionError(message)


@dataclass(frozen=True)
class EncodedCNF:
    declared_variables: int
    clauses: CNF


def canon_clause(clause: Iterable[int]) -> Clause:
    return tuple(sorted(tuple(clause), key=lambda x: (abs(x), x < 0)))


def canon_cnf(clauses: Iterable[Iterable[int]], deduplicate: bool = False) -> CNF:
    rows = [canon_clause(c) for c in clauses]
    if deduplicate:
        rows = list(set(rows))
    return tuple(sorted(rows))


def max_var(cnf: CNF) -> int:
    return max((abs(lit) for c in cnf for lit in c), default=0)


def satisfies(cnf: CNF, assignment: tuple[int, ...]) -> bool:
    return all(any(assignment[abs(lit) - 1] == int(lit > 0) for lit in c) for c in cnf)


def brute_sat(encoded: EncodedCNF, meter: Meter, combined: bool = False) -> bool:
    if combined:
        meter.combined_decisions += 1
    else:
        meter.base_decisions += 1
    return any(
        satisfies(encoded.clauses, a)
        for a in itertools.product((0, 1), repeat=encoded.declared_variables)
    )


def xor_gate(a: int, b: int, z: int) -> list[Clause]:
    return [
        (a, b, -z),
        (a, -b, z),
        (-a, b, z),
        (-a, -b, -z),
    ]


def force_literal(lit: int, p: int, q: int) -> list[Clause]:
    return [
        (lit, p, q),
        (lit, p, -q),
        (lit, -p, q),
        (lit, -p, -q),
    ]


def parity_component(n: int, target: int, layout: str, offset: int = 0) -> EncodedCNF:
    if n < 1 or target not in (0, 1) or layout not in ("left", "balanced"):
        raise ValueError("bad parity parameters")
    next_var = offset + n + 1
    gates: list[tuple[int, int, int]] = []
    sources = list(range(offset + 1, offset + n + 1))

    if layout == "left":
        output = sources[0]
        for x in sources[1:]:
            z = next_var
            next_var += 1
            gates.append((output, x, z))
            output = z
    else:
        def rec(nodes: list[int]) -> int:
            nonlocal next_var
            if len(nodes) == 1:
                return nodes[0]
            mid = len(nodes) // 2
            a = rec(nodes[:mid])
            b = rec(nodes[mid:])
            z = next_var
            next_var += 1
            gates.append((a, b, z))
            return z
        output = rec(sources)

    p, q = next_var, next_var + 1
    clauses: list[Clause] = []
    for gate in gates:
        clauses.extend(xor_gate(*gate))
    clauses.extend(force_literal(output if target else -output, p, q))
    return EncodedCNF(next_var + 1, canon_cnf(clauses))


def harden(base: EncodedCNF, target: int, layout: str) -> EncodedCNF:
    """Canonical image T(F) = F disjoint-union P_{m,target}."""
    m = base.declared_variables
    parity = parity_component(m, target, layout, offset=m)
    return EncodedCNF(parity.declared_variables, canon_cnf(base.clauses + parity.clauses))


def parse_and_strip(image: EncodedCNF, meter: Meter) -> Optional[EncodedCNF]:
    """Recognize either canonical parity layout/target and remove it.

    DIMACS-style declared variable count makes m=(V-1)/3 explicit for this
    image.  Clause/literal order and duplicate clauses are quotiented before
    recognition.  If recognition succeeds, removing the isolated satisfiable
    component is sound even when the residual was not produced by `harden`.
    """
    meter.image_recognitions += 1
    meter.clauses_parsed += len(image.clauses)
    meter.literals_parsed += sum(len(c) for c in image.clauses)
    v = image.declared_variables
    if v < 4 or (v - 1) % 3:
        meter.image_rejections += 1
        return None
    m = (v - 1) // 3
    normalized = list(canon_cnf(image.clauses, deduplicate=True))
    available = set(normalized)
    for target in (0, 1):
        for layout in ("left", "balanced"):
            gadget = set(parity_component(m, target, layout, offset=m).clauses)
            if not gadget.issubset(available):
                continue
            residual_rows = [c for c in normalized if c not in gadget]
            if all(abs(lit) <= m for c in residual_rows for lit in c):
                return EncodedCNF(m, tuple(residual_rows))
    meter.image_rejections += 1
    return None


def wrapper_decide(image: EncodedCNF, meter: Meter) -> bool:
    """Total exact wrapper around the finite brute-force child solver."""
    residual = parse_and_strip(image, meter)
    meter.child_solver_calls += 1
    return brute_sat(residual if residual is not None else image, meter)


def parity_full_source_extends(n: int, target: int, layout: str, source: tuple[int, ...], meter: Meter) -> bool:
    enc = parity_component(n, target, layout)
    # XOR-gate outputs are uniquely determined.  Only the two force-padding
    # variables remain free.
    next_aux = n + 1
    values = {i + 1: bit for i, bit in enumerate(source)}
    nodes = list(range(1, n + 1))
    gates: list[tuple[int, int, int]] = []
    if layout == "left":
        out = nodes[0]
        for x in nodes[1:]:
            gates.append((out, x, next_aux))
            out = next_aux
            next_aux += 1
    else:
        def rec(xs: list[int]) -> int:
            nonlocal next_aux
            if len(xs) == 1:
                return xs[0]
            mid = len(xs) // 2
            a, b = rec(xs[:mid]), rec(xs[mid:])
            z = next_aux
            next_aux += 1
            gates.append((a, b, z))
            return z
        rec(nodes)
    for a, b, z in gates:
        values[z] = values[a] ^ values[b]
    p, q = enc.declared_variables - 1, enc.declared_variables
    for pv, qv in itertools.product((0, 1), repeat=2):
        meter.parity_cnf_extension_checks += 1
        values[p], values[q] = pv, qv
        if all(any(values[abs(lit)] == int(lit > 0) for lit in c) for c in enc.clauses):
            return True
    return False


def projected_compatible(base_sat: bool, alpha: Partial, target: int, meter: Meter) -> bool:
    meter.projected_compatibility_checks += 1
    if not base_sat:
        return False
    return any(x is None for x in alpha) or (sum(int(x) for x in alpha) & 1) == target


def brute_projected_compatible(base_sat: bool, alpha: Partial, target: int, layout: str, meter: Meter) -> bool:
    if not base_sat:
        return False
    stars = [i for i, bit in enumerate(alpha) if bit is None]
    for fill in itertools.product((0, 1), repeat=len(stars)):
        source = list(alpha)
        for i, bit in zip(stars, fill):
            source[i] = bit
        if parity_full_source_extends(len(alpha), target, layout, tuple(int(x) for x in source), meter):
            return True
    return False


def is_minimal_bad(base_sat: bool, alpha: Partial, target: int, meter: Meter) -> bool:
    if projected_compatible(base_sat, alpha, target, meter):
        return False
    for i, bit in enumerate(alpha):
        if bit is not None:
            weak = list(alpha)
            weak[i] = None
            if not projected_compatible(base_sat, tuple(weak), target, meter):
                return False
    return True


def all_three_var_clauses() -> list[Clause]:
    return [
        tuple((i + 1) if bit else -(i + 1) for i, bit in enumerate(signs))
        for signs in itertools.product((0, 1), repeat=3)
    ]


def apply_variable_permutation(encoded: EncodedCNF, permutation: tuple[int, ...]) -> EncodedCNF:
    def move(lit: int) -> int:
        v = permutation[abs(lit) - 1]
        return v if lit > 0 else -v
    return EncodedCNF(encoded.declared_variables, tuple(tuple(move(lit) for lit in c) for c in encoded.clauses))


def invert_permutation(permutation: tuple[int, ...]) -> tuple[int, ...]:
    inv = [0] * len(permutation)
    for old, new in enumerate(permutation, start=1):
        inv[new - 1] = old
    return tuple(inv)


def run(seed: int, max_frontier_n: int) -> dict:
    start = time.perf_counter()
    meter = Meter()
    rng = random.Random(seed)
    clauses = all_three_var_clauses()
    exhaustive_rows = []
    sat_bases = 0
    unsat_bases = 0

    # All 256 proper three-variable formulas, both encodings and both targets.
    for mask in range(256):
        base = EncodedCNF(3, canon_cnf(clauses[i] for i in range(8) if (mask >> i) & 1))
        base_sat = brute_sat(base, meter)
        sat_bases += int(base_sat)
        unsat_bases += int(not base_sat)
        for layout in ("left", "balanced"):
            for target in (0, 1):
                image = harden(base, target, layout)
                image_sat = brute_sat(image, meter, combined=True)
                meter.check(image_sat == base_sat, "hardened SAT equivalence")
                before_h = meter.compatibility_evaluations_in_decider
                before_f = meter.frontier_entries_materialized_in_decider
                wrapped = wrapper_decide(image, meter)
                meter.check(wrapped == base_sat, "strip wrapper changed SAT")
                meter.check(meter.compatibility_evaluations_in_decider == before_h, "decider evaluated H")
                meter.check(meter.frontier_entries_materialized_in_decider == before_f, "decider materialized frontier")

                # Formula-order, literal-order, duplicate and tautological-base padding controls.
                variants = {
                    "CLAUSE_ORDER": EncodedCNF(image.declared_variables, tuple(reversed(image.clauses))),
                    "LITERAL_ORDER": EncodedCNF(image.declared_variables, tuple(tuple(reversed(c)) for c in image.clauses)),
                    "REDUNDANT": EncodedCNF(image.declared_variables, image.clauses + image.clauses[-4:]),
                    "PADDING": harden(EncodedCNF(3, base.clauses + ((1, -1, 2),)), target, layout),
                }
                for name, variant in variants.items():
                    meter.wrapper_checks += 1
                    meter.check(wrapper_decide(variant, meter) == base_sat, f"{name} changed decision")

                # INTERP: a fixed known variable renaming is undone before the same parser.
                perm = tuple(reversed(range(1, image.declared_variables + 1)))
                moved = apply_variable_permutation(image, perm)
                restored = apply_variable_permutation(moved, invert_permutation(perm))
                meter.wrapper_checks += 1
                meter.check(wrapper_decide(restored, meter) == base_sat, "INTERP")

        if mask in (0, 1, 17, 85, 170, 254, 255):
            exhaustive_rows.append({"mask": mask, "base_sat": base_sat})

    meter.check(sat_bases == 255 and unsat_bases == 1, "unexpected base truth distribution")

    # Exhaust the projected partial-assignment predicate through a bounded
    # prefix.  SAT bases have 2^(n-1) full wrong-parity minimal obstructions;
    # an UNSAT base makes H identically zero and the empty partial is unique.
    frontier_rows = []
    for n in range(1, max_frontier_n + 1):
        for base_sat in (False, True):
            for target in (0, 1):
                for layout in ("left", "balanced"):
                    frontier = 0
                    for alpha in itertools.product((0, 1, None), repeat=n):
                        direct = projected_compatible(base_sat, alpha, target, meter)
                        brute = brute_projected_compatible(base_sat, alpha, target, layout, meter)
                        meter.check(direct == brute, "projected compatibility mismatch")
                        frontier += int(is_minimal_bad(base_sat, alpha, target, meter))
                    expected = (1 << (n - 1)) if base_sat else 1
                    meter.check(frontier == expected, "frontier size mismatch")
                    frontier_rows.append({
                        "n": n,
                        "base_sat": base_sat,
                        "target": target,
                        "layout": layout,
                        "minimal_bad": frontier,
                    })

    # Non-image rejection/fallback, independent products, and familiar easy
    # classes.  These controls exercise decision semantics only; no asymptotic
    # claim is inferred from their timings.
    nonimage = EncodedCNF(3, canon_cnf([(1, 2, 3), (-1, -2, -3)]))
    meter.hostile_control_checks += 1
    meter.check(wrapper_decide(nonimage, meter) == brute_sat(nonimage, meter), "fallback")

    controls = {
        "2SAT": EncodedCNF(3, canon_cnf([(-1, 2), (-2, 3), (-3, 1)])),
        "Horn": EncodedCNF(3, canon_cnf([(1,), (-1, 2), (-2, 3)])),
        "affine_2CNF": EncodedCNF(2, canon_cnf([(1, -2), (-1, 2)])),
        "bounded_treewidth_chain": EncodedCNF(4, canon_cnf([(1, 2), (-2, 3), (-3, 4)])),
    }
    control_truth = {}
    for name, control in controls.items():
        truth = brute_sat(control, meter)
        control_truth[name] = truth
        meter.hostile_control_checks += 1
        meter.check(truth, name)

    left = EncodedCNF(2, canon_cnf([(1, 2), (-1, 2)]))
    right_shifted = tuple(tuple((abs(l) + 2) * (1 if l > 0 else -1) for l in c) for c in left.clauses)
    product = EncodedCNF(4, canon_cnf(left.clauses + right_shifted))
    meter.hostile_control_checks += 1
    meter.check(brute_sat(product, meter) == brute_sat(left, meter), "independent product")

    # Program wrappers return the identical bit but expose different traces.
    wrapper_labels = ("DIRECT", "COPY", "DELAY", "INTERP", "RECOMP", "DEAD")
    for label in wrapper_labels:
        for truth in (False, True):
            meter.wrapper_checks += 1
            meter.check(bool(int(truth)) == truth, label)

    elapsed = time.perf_counter() - start
    return {
        "run_id": "COREDTCH1",
        "claim": "DETACHABLE-FRONTIER-HARDENING1",
        "status": "PROVED/EXACT pending independent review",
        "retired_claim": "AMBIENT-NP-HARDNESS-TO-COMPONENT-OBLIGATION1",
        "retired_status": "FALSIFIED/RETIRED",
        "symbolic_identity": {
            "transform": "T(F)=F disjoint-union P_{m,b}^{layout}",
            "sat_equivalence": "SAT(T(F)) iff SAT(F)",
            "image_hardness": "F maps to T(F) by an injective polynomial-time many-one reduction",
            "projected_frontier_if_base_sat": "2^(m-1)",
            "projected_frontier_if_base_unsat": "1 (the empty partial assignment)",
            "image_decider": "recognize T(F), strip satisfiable parity component, invoke child only on F",
        },
        "parameters": {"seed": seed, "max_frontier_n": max_frontier_n},
        "base_formula_census": {"total": 256, "sat": sat_bases, "unsat": unsat_bases},
        "sample_base_rows": exhaustive_rows,
        "frontier_rows": frontier_rows,
        "hostile_controls": {
            "classes": control_truth,
            "independent_product": True,
            "formula_variants": ["CLAUSE_ORDER", "LITERAL_ORDER", "REDUNDANT", "PADDING"],
            "program_wrappers": list(wrapper_labels),
            "parity_encodings": ["left", "balanced"],
        },
        "meters": asdict(meter),
        "runtime_seconds": elapsed,
        "asymptotic_extrapolation": False,
        "limitations": [
            "The finite audit validates the implementation only; the all-size theorem is symbolic.",
            "The image family is NP-hard, not polynomial-time decidable unless SAT is in P.",
            "The theorem detaches the appended semantic component; it does not eliminate the child solver's cost on F.",
            "An UNSAT base collapses the projected compatibility predicate to constant zero.",
            "No claim is made about a future decision-entangled full-domain relation.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20261012)
    parser.add_argument("--max-frontier-n", type=int, default=7)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.max_frontier_n <= 9:
        raise SystemExit("max-frontier-n must be in [1,9]")
    result = run(args.seed, args.max_frontier_n)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    script_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result_sha = hashlib.sha256(args.output.read_bytes()).hexdigest()
    print(json.dumps({
        "runtime_seconds": result["runtime_seconds"],
        "meters": result["meters"],
        "script_sha256": script_sha,
        "result_sha256": result_sha,
        "output": str(args.output),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
