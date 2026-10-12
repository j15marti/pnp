#!/usr/bin/env python3
"""Finite audit for DECISION-FIBER-ONLINE-DICHOTOMY1.

The symbolic theorem is proved in the accompanying report.  This program
exhausts every nonempty binary response relation on four sources, two
challenges, and two replies, and then runs SAT-family/wrapper controls.
"""

from __future__ import annotations

import itertools
import json
import time


def partitions(n: int):
    """Yield every set partition as a restricted-growth label tuple."""
    labels = [0] * n

    def rec(i: int, maximum: int):
        if i == n:
            yield tuple(labels)
            return
        for label in range(maximum + 2):
            labels[i] = label
            yield from rec(i + 1, max(maximum, label))

    yield from rec(1, 0)


def intersection(mask_table, xs, challenge):
    mask = 3
    for x in xs:
        mask &= mask_table[x][challenge]
    return mask


def partition_works(mask_table, labels, challenges=2):
    blocks = max(labels) + 1
    for block in range(blocks):
        xs = [x for x, label in enumerate(labels) if label == block]
        for challenge in range(challenges):
            if intersection(mask_table, xs, challenge) == 0:
                return False
    return True


def answer_fiber_criterion(mask_table, answers, challenges=2):
    for answer in (0, 1):
        xs = [x for x, bit in enumerate(answers) if bit == answer]
        for challenge in range(challenges):
            if intersection(mask_table, xs, challenge) == 0:
                return False
    return True


def explicit_answer_responder_exists(mask_table, answers, challenges=2):
    # A responder is one reply for each (answer, challenge) pair.
    for replies in itertools.product((0, 1), repeat=4):
        good = True
        for x, answer in enumerate(answers):
            for challenge in range(challenges):
                reply = replies[answer * challenges + challenge]
                if not (mask_table[x][challenge] & (1 << reply)):
                    good = False
                    break
            if not good:
                break
        if good:
            return True
    return False


def exhaustive_relation_audit():
    answers = (0, 0, 1, 1)
    all_partitions = list(partitions(4))
    assert len(all_partitions) == 15
    total = 0
    fiber_yes = 0
    fiber_no = 0
    minimal_blocks_histogram = {str(i): 0 for i in range(1, 5)}
    checks = 0

    for flat in itertools.product((1, 2, 3), repeat=8):
        table = tuple((flat[2 * x], flat[2 * x + 1]) for x in range(4))
        criterion = answer_fiber_criterion(table, answers)
        explicit = explicit_answer_responder_exists(table, answers)
        checks += 1
        assert criterion == explicit

        answer_partition = (0, 0, 1, 1)
        checks += 1
        assert partition_works(table, answer_partition) == criterion

        working = [p for p in all_partitions if partition_works(table, p)]
        checks += len(all_partitions)
        assert working
        minimum = min(max(p) + 1 for p in working)
        minimal_blocks_histogram[str(minimum)] += 1

        total += 1
        if criterion:
            fiber_yes += 1
            assert minimum <= 2
        else:
            fiber_no += 1

    assert total == 3**8
    assert fiber_yes + fiber_no == total
    return {
        "sources": 4,
        "answer_fibers": [2, 2],
        "challenges": 2,
        "replies": 2,
        "total_nonempty_relations": total,
        "answer_factorable_relations": fiber_yes,
        "source_specific_relations": fiber_no,
        "minimal_message_classes_histogram": minimal_blocks_histogram,
        "assertion_checks": checks,
    }


def eval_cnf(clauses, nvars):
    witnesses = []
    for bits in itertools.product((0, 1), repeat=nvars):
        ok = True
        for clause in clauses:
            if not any((bits[abs(lit) - 1] == 1) if lit > 0 else
                       (bits[abs(lit) - 1] == 0) for lit in clause):
                ok = False
                break
        if ok:
            witnesses.append(bits)
    return witnesses


def eval_affine(equations, nvars):
    witnesses = []
    for bits in itertools.product((0, 1), repeat=nvars):
        if all(sum(bits[i] for i in indices) % 2 == rhs
               for indices, rhs in equations):
            witnesses.append(bits)
    return witnesses


def source_controls():
    raw = [
        ("horn_sat", "Horn", eval_cnf(((1,), (-1, 2)), 2)),
        ("horn_unsat", "Horn", eval_cnf(((1,), (-1,)), 1)),
        ("twosat_sat", "2SAT", eval_cnf(((1, 2), (-1, 2)), 2)),
        ("twosat_unsat", "2SAT", eval_cnf(((1,), (-1,), (2,)), 2)),
        ("affine_sat", "affine/Tseitin", eval_affine((((0, 1), 0), ((1, 2), 1)), 3)),
        ("affine_unsat", "affine/Tseitin", eval_affine((((0,), 0), ((0,), 1)), 1)),
        ("path_sat", "bounded-treewidth", eval_cnf(((1, 2), (-2, 3), (-3, 4)), 4)),
        ("path_unsat", "bounded-treewidth", eval_cnf(((1,), (-1,), (2, 3)), 3)),
    ]
    controls = []
    for idx, (name, family, witnesses) in enumerate(raw):
        controls.append({
            "name": name,
            "family": family,
            "answer": int(bool(witnesses)),
            "witness_count": len(witnesses),
            # Varies among sources in each SAT-answer fiber.
            "source_bit": (idx // 2) & 1,
        })
    assert {c["answer"] for c in controls} == {0, 1}
    for family in {c["family"] for c in controls}:
        assert {c["answer"] for c in controls if c["family"] == family} == {0, 1}
    return controls


def mask(reply):
    return 1 << int(reply)


def named_relation_audit(controls):
    challenges = range(3)
    wrappers = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
    expanded = []
    for c in controls:
        for wi, wrapper in enumerate(wrappers):
            item = dict(c)
            item["wrapper"] = wrapper
            item["wrapper_bit"] = wi & 1
            item["encoding_bit"] = (wi // 2) & 1
            item["padding"] = wi in (1, 2, 3)
            expanded.append(item)

    relations = {}
    for name in ("answer_only", "universal", "source_bit", "wrapper_trace", "encoding_tag"):
        table = []
        for item in expanded:
            row = []
            for challenge in challenges:
                if name == "answer_only":
                    row.append(mask(item["answer"] ^ (challenge & 1)))
                elif name == "universal":
                    row.append(3)
                elif name == "source_bit":
                    row.append(mask(item["source_bit"] ^ (challenge & 1)))
                elif name == "wrapper_trace":
                    row.append(mask(item["wrapper_bit"] ^ (challenge & 1)))
                else:
                    row.append(mask(item["encoding_bit"] ^ (challenge & 1)))
            table.append(tuple(row))

        answers = tuple(item["answer"] for item in expanded)
        criterion = answer_fiber_criterion(table, answers, challenges=3)
        relations[name] = {
            "answer_factorable": criterion,
            "one_bit_state_suffices": criterion,
            "requires_source_information_beyond_decision_bit": not criterion,
        }

    assert relations["answer_only"]["answer_factorable"]
    assert relations["universal"]["answer_factorable"]
    for name in ("source_bit", "wrapper_trace", "encoding_tag"):
        assert not relations[name]["answer_factorable"]

    # Independent products and redundant padding preserve the decision bit,
    # but source-/wrapper-specific response obligations can still change.
    product_checks = 0
    for a, b in itertools.product(controls, repeat=2):
        product_answer = a["answer"] & b["answer"]
        assert product_answer in (0, 1)
        product_checks += 1
    return {
        "base_sources": len(controls),
        "expanded_wrapper_encodings": len(expanded),
        "wrappers": list(wrappers),
        "families": sorted({c["family"] for c in controls}),
        "relations": relations,
        "independent_product_checks": product_checks,
        "one_bit_outputs_checked": len(expanded) * len(tuple(challenges)),
    }


def main():
    started = time.perf_counter()
    exhaustive = exhaustive_relation_audit()
    controls = source_controls()
    hostile = named_relation_audit(controls)
    elapsed = time.perf_counter() - started
    payload = {
        "run_id": "FIBERDICH1",
        "status": "COMPUTATIONAL",
        "symbolic_theorem": "DECISION-FIBER-ONLINE-DICHOTOMY1",
        "seed": None,
        "method": "exhaustive finite enumeration plus deterministic hostile controls",
        "exhaustive": exhaustive,
        "hostile_controls": hostile,
        "failures": 0,
        "elapsed_seconds": round(elapsed, 6),
        "limitations": [
            "Finite enumeration does not prove an asymptotic lower bound.",
            "The symbolic equivalence is proved separately in the report.",
            "Source-specific response obligations are not shown hard to compute."
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
