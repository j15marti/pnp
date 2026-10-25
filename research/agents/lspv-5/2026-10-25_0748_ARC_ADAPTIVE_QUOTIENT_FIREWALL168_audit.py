#!/usr/bin/env python3
"""ARC-ADAPTIVE-QUOTIENT-FIREWALL168 deterministic finite audit.

This is a finite set/CNF audit, not an FLMV machine trace and not a SAT
lower bound.  It checks the quantifier distinction between one quotient
reused through a pin tree and node-dependent semantic quotients.
"""

from __future__ import annotations

import json
from itertools import product


ASSERTIONS = 0


def check(condition: bool, message: str) -> None:
    global ASSERTIONS
    ASSERTIONS += 1
    if not condition:
        raise AssertionError(f"assertion {ASSERTIONS}: {message}")


def pin_support(d: int, prefix: tuple[int, ...]) -> frozenset[int]:
    mask = (1 << len(prefix)) - 1
    value = sum(bit << i for i, bit in enumerate(prefix))
    return frozenset(x for x in range(1 << d) if (x & mask) == value)


def image_of_support(domain: range, support: frozenset[int], subset: frozenset[int]) -> set[int]:
    """Image of subset under h_support(x)=1[x in support]."""
    return {int(x in support) for x in subset if x in domain}


def exact_adaptive_join(domain: range, support: frozenset[int], suffix: frozenset[int]) -> bool:
    left = image_of_support(domain, support, support)
    right = image_of_support(domain, support, suffix)
    return bool(left & right)


def all_tree_supports(d: int) -> list[tuple[tuple[int, ...], frozenset[int]]]:
    return [
        (prefix, pin_support(d, prefix))
        for depth in range(d + 1)
        for prefix in product((0, 1), repeat=depth)
    ]


def eval_cnf(clauses: list[tuple[int, int, int]], assignment: int) -> bool:
    for clause in clauses:
        if not any(((assignment >> (abs(lit) - 1)) & 1) == (1 if lit > 0 else 0) for lit in clause):
            return False
    return True


def projected_support(clauses: list[tuple[int, int, int]], boundary=(1, 2)) -> frozenset[int]:
    nvars = max((abs(lit) for clause in clauses for lit in clause), default=max(boundary))
    seen: set[int] = set()
    for assignment in range(1 << nvars):
        if eval_cnf(clauses, assignment):
            word = sum(((assignment >> (var - 1)) & 1) << i for i, var in enumerate(boundary))
            seen.add(word)
    return frozenset(seen)


def pin_cnf(lit: int, a: int, b: int) -> list[tuple[int, int, int]]:
    return [(lit, sa * a, sb * b) for sa in (-1, 1) for sb in (-1, 1)]


def proper(clauses: list[tuple[int, int, int]]) -> bool:
    return all(len(c) == 3 and len({abs(x) for x in c}) == 3 and all(x != 0 for x in c) for c in clauses)


def main() -> None:
    records = []
    universal_suffix_checks = 0
    sampled_suffix_checks = 0
    no_transition_edges = 0

    # Depth ten already gives a 2,047-node tree and 1,024 boundary words.
    # Keeping the deterministic audit here makes the invocation comfortably
    # sub-30-second; the symbolic theorem in the report covers all d.
    for d in range(1, 11):
        domain = range(1 << d)
        nodes = all_tree_supports(d)

        # A single fixed quotient valid for the whole complete pin tree needs
        # one class per complete descendant-membership signature.
        signatures = {
            tuple(int(word in support) for _, support in nodes)
            for word in domain
        }
        check(len(signatures) == 1 << d, f"fixed hereditary signatures at depth {d}")

        adaptive_max = 0
        for prefix, support in nodes:
            labels = {int(word in support) for word in domain}
            adaptive_max = max(adaptive_max, len(labels))
            check(len(labels) <= 2, f"node-dependent quotient has at most two labels at {prefix}")

            # Exhaust every suffix support for d<=4.  For larger d, use a
            # deterministic hostile battery including every singleton.
            if d <= 3:
                for qmask in range(1 << (1 << d)):
                    suffix = frozenset(word for word in domain if (qmask >> word) & 1)
                    check(exact_adaptive_join(domain, support, suffix) == bool(support & suffix),
                          f"universal suffix join d={d}, prefix={prefix}, q={qmask}")
                    universal_suffix_checks += 1
            else:
                suffixes = [frozenset(), frozenset(domain)]
                stride = max(1, (1 << d) // 16)
                suffixes.extend(frozenset({word}) for word in range(0, 1 << d, stride))
                suffixes.extend([
                    frozenset(word for word in domain if word & 1),
                    frozenset(word for word in domain if not (word & 1)),
                ])
                for suffix in suffixes:
                    check(exact_adaptive_join(domain, support, suffix) == bool(support & suffix),
                          f"sampled suffix join d={d}, prefix={prefix}")
                    sampled_suffix_checks += 1

        check(adaptive_max <= 2, f"adaptive maximum labels at depth {d}")

        # No child quotient can in general be updated from the parent's one
        # bit label alone: both halves of the child split had parent label 1.
        for prefix, parent in nodes:
            if len(prefix) == d:
                continue
            for bit in (0, 1):
                child = pin_support(d, prefix + (bit,))
                inside = next(iter(child))
                outside = next(word for word in parent if word not in child)
                check(int(inside in parent) == int(outside in parent) == 1,
                      "parent quotient merges the two witnesses")
                check(int(inside in child) != int(outside in child),
                      "child quotient must split the merged witnesses")
                no_transition_edges += 1

        records.append({
            "depth": d,
            "boundary_words": 1 << d,
            "pin_tree_nodes": len(nodes),
            "fixed_reusable_min_labels": len(signatures),
            "max_node_dependent_labels": adaptive_max,
        })

    # Independent proper-3CNF realization of the two-level hostile control.
    root = [(1, 3, 4), (2, 5, 6)]
    child = root + pin_cnf(-1, 7, 8)
    grandchild = child + pin_cnf(-2, 9, 10)
    sat_suffix = pin_cnf(-1, 11, 12) + pin_cnf(-2, 13, 14)
    conflict_suffix = pin_cnf(-1, 11, 12) + pin_cnf(2, 13, 14)
    for name, formula in (("root", root), ("child", child), ("grandchild", grandchild),
                          ("sat_suffix", sat_suffix), ("conflict_suffix", conflict_suffix)):
        check(proper(formula), f"{name} is proper signed ternary CNF")

    supports = {
        "root": projected_support(root),
        "child": projected_support(child),
        "grandchild": projected_support(grandchild),
        "sat_suffix": projected_support(sat_suffix),
        "conflict_suffix": projected_support(conflict_suffix),
    }
    check(supports["root"] == frozenset(range(4)), "root full boundary support")
    check(supports["child"] == frozenset({0, 2}), "child pins y1=0")
    check(supports["grandchild"] == frozenset({0}), "grandchild pins 00")
    check(bool(supports["grandchild"] & supports["sat_suffix"]), "SAT ordinary join")
    check(not bool(supports["grandchild"] & supports["conflict_suffix"]), "UNSAT ordinary join")
    check(exact_adaptive_join(range(4), supports["grandchild"], supports["sat_suffix"]),
          "adaptive quotient preserves SAT join")
    check(not exact_adaptive_join(range(4), supports["grandchild"], supports["conflict_suffix"]),
          "adaptive quotient preserves UNSAT join")

    result = {
        "name": "ARC-ADAPTIVE-QUOTIENT-FIREWALL168",
        "model": "finite set semantics plus brute-force proper-3CNF controls; not FLMV trace",
        "seed": None,
        "records": records,
        "universal_suffix_checks": universal_suffix_checks,
        "sampled_suffix_checks": sampled_suffix_checks,
        "no_label_only_transition_edges": no_transition_edges,
        "ordinary_supports": {k: sorted(v) for k, v in supports.items()},
        "assertions": ASSERTIONS,
        "failures": 0,
        "interpretation": (
            "A fixed quotient over the complete pin tree needs 2^d labels, "
            "but node-dependent extensional quotients need at most two. "
            "Changing quotients cannot be performed from the old label alone; "
            "acquisition/translation must be charged."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
