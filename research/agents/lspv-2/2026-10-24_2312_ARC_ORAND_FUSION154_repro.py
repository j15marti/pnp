#!/usr/bin/env python3
"""ARC-ORAND-FUSION154: two real ordinary-SAT recursion levels.
Finite structural/semantic audit only. Python materializes full formula lists:
NOT a physical FLMV random-access machine space, flip, or bit-time trace.
Seed-free, Python 3 standard library.
"""
import itertools
import json
import math
from collections import Counter
from pathlib import Path


class Builder:
    def __init__(self):
        self.n = 0

    def var(self):
        self.n += 1
        return self.n

    def clause(self, *ls):
        assert len(ls) == 3
        assert len({abs(v) for v in ls}) == 3
        return tuple(ls)


def leaves_for(b, labels, builder):
    out = []
    for label in labels:
        x, y, z = [builder.var() for _ in range(3)]
        all8 = [
            builder.clause(sign[0]*x, sign[1]*y, sign[2]*z)
            for sign in itertools.product((1, -1), repeat=3)
        ]
        # Ordinary 3CNF permits duplicate records. The all-eight core is
        # UNSAT; removing one distinct pattern leaves a SAT core.
        clauses = list(all8 if label == 0 else all8[:-1] + [all8[0]])
        for _ in range(b):
            clauses.append(builder.clause(builder.var(),
                                          builder.var(),
                                          builder.var()))
        assert len(clauses) == b + 8
        out.append(clauses)
    return out


def at_least_one(selectors, builder):
    if len(selectors) == 2:
        aux = builder.var()
        return [builder.clause(selectors[0], selectors[1], aux),
                builder.clause(selectors[0], selectors[1], -aux)]
    if len(selectors) == 3:
        return [builder.clause(*selectors)]
    aux = [builder.var() for _ in range(len(selectors) - 3)]
    out = [builder.clause(selectors[0], selectors[1], aux[0])]
    for j in range(2, len(selectors) - 2):
        out.append(builder.clause(-aux[j-2], selectors[j], aux[j-1]))
    out.append(builder.clause(-aux[-1], selectors[-2], selectors[-1]))
    return out


def compose(b, labels):
    assert len(labels) == b*b
    builder = Builder()
    leaves = leaves_for(b, labels, builder)
    groups = [
        sum(leaves[i*b:(i+1)*b], []) for i in range(b)
    ]
    selectors = [builder.var() for _ in range(b)]
    root = at_least_one(selectors, builder)
    for i, group in enumerate(groups):
        for u, v, w in group:
            a = builder.var()
            root += [
                builder.clause(-selectors[i], u, a),
                builder.clause(-a, v, w)
            ]
    return builder.n, root, groups, leaves, selectors


def cnf_sat(clauses, limit=100000):
    """Independent exact DPLL, with unit and pure literal propagation."""
    steps = 0

    def recurse(cls):
        nonlocal steps
        steps += 1
        if steps > limit:
            raise RuntimeError("DPLL node limit exceeded")
        cls = list(cls)
        while True:
            if not cls:
                return True
            if any(len(c) == 0 for c in cls):
                return False
            unit = next((c[0] for c in cls if len(c) == 1), None)
            if unit is None:
                counts = Counter(v for clause in cls for v in clause)
                ids = {abs(v) for v in counts}
                unit = next(
                    (v if v in counts else -v for v in sorted(ids)
                     if not (v in counts and -v in counts)),
                    None)
                if unit is None:
                    break
            cls = [
                tuple(v for v in c if v != -unit)
                for c in cls if unit not in c
            ]
        frequencies = Counter(abs(v) for clause in cls for v in clause)
        pivot = max(frequencies, key=lambda v: (frequencies[v], -v))
        for literal in (pivot, -pivot):
            child = [
                tuple(v for v in c if v != -literal)
                for c in cls if literal not in c
            ]
            if recurse(child):
                return True
        return False

    answer = recurse(tuple(clauses))
    return answer, steps


def indexed_bits(n, m):
    width = math.ceil(math.log2(64*(n+m+1)))
    return (4*m+2)*width


def structural_check(root, groups, leaves, b, n):
    assert len(groups) == b and len(leaves) == b*b
    seen = set()
    for i, group in enumerate(groups):
        assert len(group) == b*(b+8)
        assert group == sum(leaves[i*b:(i+1)*b], [])
        assert all(len(c) == 3 and len({abs(x) for x in c}) == 3
                   for c in group)
    for leaf in leaves:
        names = {abs(v) for clause in leaf for v in clause}
        assert not (names & seen), "global source-name collision"
        seen.update(names)
    assert all(1 <= abs(v) <= n for c in root for v in c)
    return True


def solve_group_ordinary(group, b, group_index):
    """Layer 1 receives an ordinary group CNF, calls ordinary leaf DPLL."""
    assert len(group) == b*(b+8)
    calls = []
    for j in range(b):
        child = list(group[j*(b+8):(j+1)*(b+8)])
        answer, nodes = cnf_sat(child)
        calls.append({"group": group_index, "leaf": j,
                      "sat": answer, "dpll_nodes": nodes})
        if not answer:
            return False, calls
    return True, calls


def nested_solver(b, groups):
    """Layer 0 root OR -> layer 1 group AND -> layer 2 leaf SAT."""
    calls = []
    for i, group in enumerate(groups):
        answer, child_calls = solve_group_ordinary(group, b, i)
        calls.extend(child_calls)
        if answer:
            return True, calls
    return False, calls


def label_only_tree(labels, b):
    seen = []
    for i in range(b):
        group_yes = True
        for j in range(b):
            index = i*b + j
            seen.append(index)
            if not labels[index]:
                group_yes = False
                break
        if group_yes:
            return True, seen
    return False, seen


def adversarial_profile(b, yes):
    # b-1 preceding groups each have their last leaf UNSAT;
    # the last group is all SAT if yes, otherwise its last leaf is UNSAT.
    labels = [1]*(b*b)
    for i in range(b-1):
        labels[i*b+b-1] = 0
    if not yes:
        labels[-1] = 0
    return labels


def main():
    cases = []
    for b in (2, 3, 4):
        for root_yes in (False, True):
            labels = adversarial_profile(b, root_yes)
            n, root, groups, leaves, selectors = compose(b, labels)
            assert structural_check(root, groups, leaves, b, n)
            correct = any(all(labels[i*b:(i+1)*b]) for i in range(b))
            assert correct == root_yes
            label_answer, label_indices = label_only_tree(labels, b)
            real_answer, actual_calls = nested_solver(b, groups)
            assert real_answer == label_answer == correct
            assert len(actual_calls) == len(label_indices) == b*b
            assert [x["group"]*b+x["leaf"] for x in actual_calls] == label_indices
            leaf_nodes = 0
            for j, leaf in enumerate(leaves):
                value, nodes = cnf_sat(leaf)
                assert value == bool(labels[j])
                leaf_nodes += nodes
            group_nodes = 0
            for i, group in enumerate(groups):
                value, nodes = cnf_sat(group)
                assert value == all(labels[i*b:(i+1)*b])
                group_nodes += nodes
            root_value, root_nodes = cnf_sat(root)
            assert root_value == correct
            root_bits = indexed_bits(n, len(root))
            group_bits = indexed_bits(n, len(groups[0]))
            leaf_bits = indexed_bits(n, len(leaves[0]))
            cases.append({
                "b": b, "label": "SAT" if correct else "UNSAT",
                "root_variables": n, "root_clauses": len(root),
                "root_bits": root_bits,
                "group_bits": group_bits, "leaf_bits": leaf_bits,
                "root_to_group_ratio": round(group_bits/root_bits, 6),
                "group_to_leaf_ratio": round(leaf_bits/group_bits, 6),
                "actual_nested_calls": len(actual_calls),
                "actual_nested_nodes": sum(x["dpll_nodes"] for x in actual_calls),
                "group_calls": b, "leaf_calls": b*b,
                "root_dpll_nodes": root_nodes,
                "group_dpll_nodes": group_nodes,
                "leaf_dpll_nodes": leaf_nodes,
                "direct_label_match": True, "all_children_ordinary": True
            })
    # Out-of-promise both-label exact generic DPLL fallback controls.
    B = Builder()
    outside_sat = leaves_for(2, [1], B)[0]
    B = Builder()
    outside_unsat = leaves_for(2, [0], B)[0]
    assert cnf_sat(outside_sat)[0]
    assert not cnf_sat(outside_unsat)[0]
    exhaustive = 0
    for mask in range(16):
        z = [(mask >> i) & 1 for i in range(4)]
        expected = any(all(z[i*2:(i+1)*2]) for i in range(2))
        assert label_only_tree(z, 2)[0] == expected
        exhaustive += 1
    result = {
        "id": "ARC-ORAND-FUSION154", "seed": "none",
        "proof_status": "COMPUTATIONAL finite ordinary-CNF controls; restricted oracle theorem symbolic",
        "cases": cases,
        "exhaustive_two_by_two_profiles": exhaustive,
        "outside_promise_controls": {"sat": True, "unsat": True},
        "note": "Python stores full clauses, not FLMV physical workspace or bit-time."
    }
    out = Path(__file__).with_name(
        "2026-10-24_2312_ARC_ORAND_FUSION154_raw.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "all_pass": True, "cases": len(cases),
        "total_dpll_nodes": sum(row["root_dpll_nodes"] for row in cases),
        "raw": str(out)
    }, sort_keys=True))


if __name__ == "__main__":
    main()
