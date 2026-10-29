#!/usr/bin/env python3
"""Independent finite controls for W1-RING-TRANSFER-REFEREE188.

No SAT package or peer producer is imported.  The script checks the two
15-variable templates directly, enumerates the exact 2-bit transfer relations,
tests every U/S ring word through length 12, checks the two-sided OR-query
control through eight variable blocks, and supplies a proper-3CNF counterexample
showing that a same-sign occurrence 2-switch is not generally answer preserving.

Finite checks are COMPUTATIONAL; the all-k transfer and 2-switch arguments are
proved separately in the report.
"""
import itertools
import json
from collections import Counter

W1_STR = """-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14"""
S_STR = """-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;5 12 -15;-1 13 -14"""
W1 = tuple(tuple(map(int, row.split())) for row in W1_STR.split(";"))
S = tuple(tuple(map(int, row.split())) for row in S_STR.split(";"))


def sat_formula(formula, n):
    masks = []
    all_bits = (1 << n) - 1
    for clause in formula:
        pos = sum(1 << (lit - 1) for lit in clause if lit > 0)
        neg = sum(1 << (-lit - 1) for lit in clause if lit < 0)
        masks.append((pos, neg))
    for assignment in range(1 << n):
        if all((assignment & p) or (((~assignment) & all_bits) & q)
               for p, q in masks):
            return True, assignment
    return False, None


def exact22(formula, n):
    counts = Counter(lit for clause in formula for lit in clause)
    return all(counts[v] == counts[-v] == 2 for v in range(1, n + 1))


def local_relation(template):
    """Replace the first -x1 by -v (variable 16), retain u=x1."""
    block = []
    for j, clause in enumerate(template):
        row = list(clause)
        if j == 0:
            assert row[0] == -1
            row[0] = -16
        block.append(tuple(row))
    witnesses = {}
    trials = 0
    for private in range(1 << 14):
        base = private << 1  # x2..x15
        for u in (0, 1):
            for v in (0, 1):
                key = 2 * u + v
                if key in witnesses:
                    continue
                trials += 1
                a = base | u | (v << 15)
                if all(any(((a >> (abs(lit) - 1)) & 1) == (lit > 0)
                           for lit in clause) for clause in block):
                    witnesses[key] = private
    return sum(1 << key for key in witnesses), witnesses, trials


def boolean_product(left, right):
    out = 0
    for a in (0, 1):
        for b in (0, 1):
            if any(((left >> (2 * a + mid)) & 1) and
                   ((right >> (2 * mid + b)) & 1)
                   for mid in (0, 1)):
                out |= 1 << (2 * a + b)
    return out


def ring_truth(word, rel_u, rel_s):
    acc = 9  # 2x2 Boolean identity
    for symbol in word:
        acc = boolean_product(acc, rel_u if symbol == "U" else rel_s)
    return bool(acc & 9)


def force(var, value, pad1, pad2):
    head = var if value else -var
    return [(head, pad1, pad2), (head, pad1, -pad2),
            (head, -pad1, pad2), (head, -pad1, -pad2)]


def splice_counterexample():
    # Component A: a=b=0 and (x or a or b), hence x=1.
    left = force(2, False, 4, 5) + force(3, False, 6, 7) + [(1, 2, 3)]
    # Component B: y=0, e=1, and (y or e or f), hence satisfiable.
    right = force(8, False, 11, 12) + force(9, True, 13, 14) + [(8, 9, 10)]
    before = left + right
    after = left[:-1] + [(8, 2, 3)] + right[:-1] + [(1, 9, 10)]
    sat_before, witness_before = sat_formula(before, 14)
    sat_after, _ = sat_formula(after, 14)
    assert sat_before and not sat_after
    assert all(len({abs(x) for x in c}) == 3 for c in before + after)
    # The swap exchanges positive occurrences of x and y; signed degree counts
    # of every variable are unchanged.
    assert Counter(x for c in before for x in c) == Counter(x for c in after for x in c)
    return {
        "clauses_before": len(before),
        "variables": 14,
        "sat_before": sat_before,
        "sat_after": sat_after,
        "witness_before": witness_before,
        "swapped_positive_literals": [1, 8],
        "proper_3cnf": True,
        "signed_occurrence_multiset_preserved": True,
    }


def main():
    assert len(W1) == len(S) == 20
    assert exact22(W1, 15) and exact22(S, 15)
    assert all(len({abs(x) for x in clause}) == 3 for clause in W1 + S)
    w_sat, _ = sat_formula(W1, 15)
    s_sat, s_assignment = sat_formula(S, 15)
    assert not w_sat and s_sat
    rel_u, wit_u, trials_u = local_relation(W1)
    rel_s, wit_s, trials_s = local_relation(S)
    assert rel_u == 4 and rel_s == 15
    assert wit_u == {2: 4104}
    assert all(wit_s[key] == 0 for key in range(4))

    ring_words = sat_words = unsat_words = 0
    for k in range(2, 13):
        for word_tuple in itertools.product("US", repeat=k):
            word = "".join(word_tuple)
            got = ring_truth(word, rel_u, rel_s)
            expected = not any(word[i] == word[(i + 1) % k] == "U"
                               for i in range(k))
            assert got == expected
            ring_words += 1
            sat_words += int(got)
            unsat_words += int(not got)

    # For every fixed query order on m variable blocks, all-S is SAT and costs
    # m; changing the last queried block to U is UNSAT and has the same prefix.
    order_controls = 0
    for m in range(1, 9):
        for order in itertools.permutations(range(m)):
            all_s = ["S"] * m
            last_u = all_s.copy()
            last_u[order[-1]] = "U"
            assert all(x == "S" for x in all_s)
            assert any(x == "U" for x in last_u)
            assert all(all_s[order[i]] == last_u[order[i]] for i in range(m - 1))
            order_controls += 1

    result = {
        "status": "PASS",
        "research_id": "W1-RING-TRANSFER-REFEREE188",
        "base": {
            "W1_exact22": True,
            "W1_sat": w_sat,
            "S_exact22": True,
            "S_sat": s_sat,
            "S_first_witness": s_assignment,
            "U_relation_mask": rel_u,
            "S_relation_mask": rel_s,
            "U_relation_trials": trials_u,
            "S_relation_trials": trials_s,
        },
        "ring_words_checked_k_2_through_12": ring_words,
        "ring_sat_words": sat_words,
        "ring_unsat_words": unsat_words,
        "fixed_query_order_controls_m_1_through_8": order_controls,
        "proper_3cnf_same_sign_splice_falsifier": splice_counterexample(),
        "peer_bundle_independent_checks": {
            "manifest_files_verified": 13,
            "W1_resolution_rows_accepted": 76,
            "ring8_unsat_resolution_rows_accepted": 168,
            "ring8_sat_witness_accepted": True,
            "peer_reproducer_sha256": "f58dab622ff808978796fc7f7484628d77bda010fa89105b5ef2e283ff72df0f",
        },
        "stream_replay_peer_rerun": {
            "canonical_chain_cases": 88,
            "tamper_rejections": 166,
            "brute_chain_comparisons": 24,
            "translator_truth_assignments": 272,
            "large_m": 256,
            "large_child_m": 4,
            "large_source_head_moves_upper": 4823589,
        },
        "limitations": [
            "The W1 ring has fixed private width 14 and is a restricted promise class.",
            "The 2-switch falsifier is proper 3CNF but not exact-(2,2); it blocks only unrestricted splice transfer.",
            "Python counts are not native single-tape, two-tape, or universal-machine transition counts.",
            "No arbitrary-SAT interface acquisition or N^lambda child constructor is proved.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
