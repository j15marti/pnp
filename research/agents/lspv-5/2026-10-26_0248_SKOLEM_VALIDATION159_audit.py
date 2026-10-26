#!/usr/bin/env python3
"""Finite audit for SKOLEM-VALIDATION159.

The symbolic theorem in the companion report is a coNP-completeness result.
This program checks the explicit exact-(2,2) source, proper-3CNF circuit
encoding, supplied Skolem circuits, one-bad-boundary family, and a genuine
second proper-3CNF level for q=1,...,7.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

OUT = Path(__file__).with_name(
    "2026-10-26_0248_SKOLEM_VALIDATION159_results.json"
)


class Builder:
    def __init__(self, q: int):
        self.next_var = 3 * q + 1
        self.clauses: list[tuple[int, int, int]] = []
        self.witness_rules: dict[int, tuple] = {}

    def fresh(self) -> int:
        v = self.next_var
        self.next_var += 1
        return v

    def widen_binary(self, a: int, b: int) -> None:
        r = self.fresh()
        self.clauses += [(a, b, r), (a, b, -r)]
        self.witness_rules[r] = ("const", False)

    def add_or(self, a: int, b: int) -> int:
        y = self.fresh()
        self.clauses.append((a, b, -y))
        self.widen_binary(-a, y)
        self.widen_binary(-b, y)
        self.witness_rules[y] = ("or", a, b)
        return y

    def add_not(self, a: int) -> int:
        # y <-> not a, with both binary clauses widened independently.
        y = self.fresh()
        self.widen_binary(a, y)
        self.widen_binary(-a, -y)
        self.witness_rules[y] = ("not", a)
        return y

    def add_force_true(self, lit: int) -> None:
        a, b = self.fresh(), self.fresh()
        self.witness_rules[a] = ("const", False)
        self.witness_rules[b] = ("const", False)
        for sa in (a, -a):
            for sb in (b, -b):
                self.clauses.append((lit, sa, sb))

    def add_neutral_name(self, x: int) -> None:
        p, r = self.fresh(), self.fresh()
        self.witness_rules[p] = ("const", True)
        self.witness_rules[r] = ("const", False)
        self.clauses += [(x, p, r), (-x, p, r)]


def source_gadgets(q: int) -> list[tuple[int, int, int]]:
    clauses = []
    for i in range(q):
        y, a, b = i + 1, q + i + 1, 2 * q + i + 1
        clauses += [(y, a, b), (y, -a, -b), (-y, a, -b), (-y, -a, b)]
    return clauses


def lit_value(lit: int, assignment: dict[int, bool]) -> bool:
    value = assignment[abs(lit)]
    return value if lit > 0 else not value


def sat_clauses(clauses, assignment) -> bool:
    return all(any(lit_value(l, assignment) for l in c) for c in clauses)


def proper(clauses) -> bool:
    return all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in clauses)


def eval_rules(base: dict[int, bool], rules: dict[int, tuple]) -> dict[int, bool]:
    a = dict(base)
    pending = dict(rules)
    while pending:
        progressed = False
        for v, rule in list(pending.items()):
            op = rule[0]
            args = rule[1:]
            if op == "const":
                a[v] = bool(args[0])
            elif all(abs(x) in a for x in args):
                vals = [lit_value(x, a) for x in args]
                if op == "or":
                    a[v] = vals[0] or vals[1]
                elif op == "not":
                    a[v] = not vals[0]
                else:
                    raise AssertionError(op)
            else:
                continue
            del pending[v]
            progressed = True
        if not progressed:
            raise AssertionError(f"cyclic or missing witness rules: {pending}")
    return a


def build_child(q: int, good: bool):
    b = Builder(q)
    u = list(range(1, q + 1))
    if good:
        neg = b.add_not(u[0])
        out = b.add_or(u[0], neg)
    else:
        out = u[0]
        for x in u[1:]:
            out = b.add_or(out, x)
    b.add_force_true(out)
    for x in range(1, 3 * q + 1):
        b.add_neutral_name(x)
    return b


def gadget_models(q: int):
    per = []
    for i in range(q):
        y, a, b = i + 1, q + i + 1, 2 * q + i + 1
        block = []
        for vals in itertools.product((False, True), repeat=3):
            assn = {y: vals[0], a: vals[1], b: vals[2]}
            if sat_clauses(source_gadgets(1), {1: vals[0], 2: vals[1], 3: vals[2]}):
                block.append(assn)
        assert len(block) == 4
        per.append(block)
    for choice in itertools.product(*per):
        merged = {}
        for part in choice:
            merged.update(part)
        yield merged


def main() -> None:
    assertions = 0
    failures: list[str] = []
    rows = []
    for q in range(1, 8):
        src = source_gadgets(q)
        bad = build_child(q, False)
        good = build_child(q, True)
        assertions += 4
        if not proper(src):
            failures.append(f"q={q}: source not proper")
        if not proper(bad.clauses):
            failures.append(f"q={q}: bad child not proper")
        if not proper(good.clauses):
            failures.append(f"q={q}: good child not proper")
        if any(sum(1 for c in src for l in c if l == v) != 2 or
               sum(1 for c in src for l in c if l == -v) != 2
               for v in range(1, 3 * q + 1)):
            failures.append(f"q={q}: source is not exact-(2,2)")

        fail_models = 0
        total_models = 0
        seen_u = set()
        for alpha in gadget_models(q):
            total_models += 1
            uword = tuple(alpha[i] for i in range(1, q + 1))
            seen_u.add(uword)
            assertions += 1
            if not sat_clauses(src, alpha):
                failures.append(f"q={q}: enumerated nonmodel")

            bad_a = eval_rules(alpha, bad.witness_rules)
            bad_ok = sat_clauses(bad.clauses, bad_a)
            expected_bad = any(uword)
            assertions += 1
            if bad_ok != expected_bad:
                failures.append(f"q={q}: bad child mismatch at {uword}")
            if not bad_ok:
                fail_models += 1

            good_a = eval_rules(alpha, good.witness_rules)
            assertions += 1
            if not sat_clauses(good.clauses, good_a):
                failures.append(f"q={q}: tautology child failed at {uword}")

            # A genuine second level: add one new proper clause and extend by 1,0,0.
            r, s, t = bad.next_var, bad.next_var + 1, bad.next_var + 2
            level2 = bad.clauses + [(r, s, t)]
            bad_a2 = dict(bad_a)
            bad_a2.update({r: True, s: False, t: False})
            assertions += 1
            if sat_clauses(level2, bad_a2) != expected_bad:
                failures.append(f"q={q}: level-two mismatch at {uword}")

        assertions += 4
        if len(seen_u) != 2 ** q:
            failures.append(f"q={q}: source does not realize all universal words")
        if total_models != 4 ** q:
            failures.append(f"q={q}: source model count mismatch")
        if fail_models != 2 ** q:
            failures.append(f"q={q}: one-bad-word multiplicity mismatch")
        source_names = set(range(1, 3 * q + 1))
        child_names = {abs(l) for c in bad.clauses for l in c}
        if not source_names <= child_names:
            failures.append(f"q={q}: source name missing in child")

        rows.append({
            "q": q,
            "source_variables": 3 * q,
            "source_clauses": len(src),
            "source_models": total_models,
            "universal_words": len(seen_u),
            "bad_universal_words": 1,
            "bad_source_models": fail_models,
            "bad_fraction_of_source_models": f"1/{2 ** q}",
            "bad_child_variables": bad.next_var - 1,
            "bad_child_clauses": len(bad.clauses),
            "good_child_variables": good.next_var - 1,
            "good_child_clauses": len(good.clauses),
            "second_level_extra_variables": 3,
            "second_level_extra_clauses": 1,
        })

    result = {
        "marker": "SKOLEM_VALIDATION159",
        "status": "COMPUTATIONAL finite verification of separately proved theorem",
        "parameters": {"q_min": 1, "q_max": 7, "random_seed": None},
        "assertions": assertions,
        "failures": len(failures),
        "failure_messages": failures[:20],
        "rows": rows,
        "limits": [
            "Finite enumeration is not an asymptotic lower bound.",
            "The coNP-completeness theorem is symbolic and applies to general supplied circuits.",
            "The source is an easy disconnected exact-(2,2) control, not a hard SAT family.",
            "A syntactically checkable derivation can avoid generic semantic validation.",
        ],
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
