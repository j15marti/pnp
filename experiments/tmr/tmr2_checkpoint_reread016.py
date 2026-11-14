#!/usr/bin/env python3
"""Independent TMR-2/016 physical input reread and checkpoint test.
Fixed finite-control classifier for unbounded 3-variable proper 3-CNF sign streams.
No imports from peer code. Every locally moving original-input-head step counted.
"""
import itertools
import json
from collections import Counter
from datetime import datetime, timezone


def direct_classify(bits):
    if len(bits) % 3:
        return "MALFORMED"
    masks = [int(bits[i:i + 3], 2) for i in range(0, len(bits), 3)]
    # Explicit eight-assignment semantic evaluation, not the controller mask rule.
    for assignment in range(8):
        if all(assignment != clause_mask for clause_mask in masks):
            return "SAT"
    return "UNSAT"


def physical_run(bits, record=False):
    """Read-only input at cells 1..L; endmarkers at 0 and L+1."""
    assert set(bits) <= {"0", "1"}
    L = len(bits)
    q = L + 1
    p, steps, last = 0, 0, 0
    reads = [0] * L
    checkpoint = None
    crossings = []
    # Wash outward: bits are actually read at physical cell, then immediately discarded.
    while p < q:
        if 1 <= p <= L:
            last = int(bits[p - 1])
            reads[p - 1] += 1
        p += 1
        steps += 1
        if record and 1 <= p <= L:
            crossings.append(("wash_out", p - 1, last))
    # Wash return: retain no source value when returning to marker 0.
    while p > 0:
        p -= 1
        steps += 1
    last = 0
    mask, residue, clause = 0, 0, 0
    phase = "VERIFY_OUT"
    checkpoint = (phase, p, last, mask, residue, clause)
    assert steps == 2 * q and p == 0
    # Second outward scan: finite-state mask over 8 potential assignments.
    while p < q:
        if 1 <= p <= L:
            bit = int(bits[p - 1])
            reads[p - 1] += 1
            clause = 2 * clause + bit
            residue += 1
            if residue == 3:
                assert 0 <= clause < 8
                mask |= (1 << clause)
                residue, clause = 0, 0
        p += 1
        steps += 1
    label = "MALFORMED" if residue else ("UNSAT" if mask == 255 else "SAT")
    while p > 0:
        p -= 1
        steps += 1
    steps += 1  # physical terminal transition
    assert steps == 4 * q + 1
    assert all(r == 2 for r in reads)
    assert label == direct_classify(bits)
    return label, checkpoint, steps, reads, crossings


def two_crossing_parity(bits):
    """Independent audit of TMR-3/014 physically positioned prepass crossing tags."""
    L, pos, parity, last = len(bits), 0, 0, 0
    outward = {}
    backward = {}
    q = L + 1
    while pos < q:
        if 1 <= pos <= L:
            last = int(bits[pos - 1])
            parity ^= last
        pos += 1
        if 1 <= pos - 1 <= L:
            outward[pos - 1] = last
    while pos > 0:
        previous = pos
        pos -= 1
        if 1 <= previous - 1 <= L:
            backward[previous - 1] = parity
    assert len(outward) == L and len(backward) == L
    assert len(outward) + len(backward) == 2 * L
    assert all((outward[i], backward[i]) == (int(bits[i - 1]), parity) for i in range(1, L + 1))
    return parity


def sibling_pair(repetitions):
    # First seven masks 0,..,6, duplicate 0 any number of times,
    # and last mask 110 (SAT) versus 111 (UNSAT). Only the FINAL bit differs.
    base = list(range(7)) + [0] * repetitions
    return ("".join(f"{x:03b}" for x in base) + "110",
            "".join(f"{x:03b}" for x in base) + "111")


def main():
    stats = Counter()
    checkpoints = set()
    labels = Counter()
    # Complete exhaustive binary input sweep for lengths 0..12.
    for L in range(13):
        checkpoints_at_length = set()
        for tup in itertools.product("01", repeat=L):
            bits = "".join(tup)
            label, cp, steps, reads, crossing = physical_run(bits)
            parity = two_crossing_parity(bits)
            assert parity == (bits.count("1") % 2)
            labels[label] += 1
            checkpoints_at_length.add(cp)
            stats["exhaustive_sources"] += 1
            stats["charged_steps"] += steps
            stats["source_cell_reads"] += sum(reads)
            stats["two_crossing_prepass_events"] += 2 * L
        assert checkpoints_at_length == {("VERIFY_OUT", 0, 0, 0, 0, 0)}
        checkpoints.update(checkpoints_at_length)
        stats["exhaustive_lengths"] += 1
    # All 8! UNSAT mask permutations as genuinely valid length-24 sources.
    for masks in itertools.permutations(range(8)):
        bits = "".join(f"{v:03b}" for v in masks)
        label, cp, steps, reads, _ = physical_run(bits)
        assert label == "UNSAT"
        assert cp == ("VERIFY_OUT", 0, 0, 0, 0, 0)
        stats["unsat_permutations"] += 1
        stats["charged_steps"] += steps
        stats["source_cell_reads"] += sum(reads)
    # Length-unbounded opposite-label final-bit sibling series.
    for repeat in range(129):
        sat, unsat = sibling_pair(repeat)
        assert len(sat) == len(unsat)
        assert sat[:-1] == unsat[:-1] and sat[-1] != unsat[-1]
        out1 = physical_run(sat)
        out2 = physical_run(unsat)
        assert (out1[0], out2[0]) == ("SAT", "UNSAT")
        assert out1[1] == out2[1] == ("VERIFY_OUT", 0, 0, 0, 0, 0)
        # First possible different input read after common checkpoint is cell L;
        # traversing from p=0 to p=L takes L moves, then the read needs a step.
        L = len(sat)
        assert out1[2] - 2 * (L + 1) >= L + 1
        stats["opposite_label_pairs"] += 1
        stats["max_sibling_L"] = max(stats["max_sibling_L"], L)
        stats["charged_steps"] += out1[2] + out2[2]
        stats["source_cell_reads"] += sum(out1[3]) + sum(out2[3])
    result = {
      "test_id": "TMR2_CHECKPOINT_REREAD016",
      "model": "one two-way locally-moving read-only input head, finite control only, arbitrary-length 3-variable sign stream",
      "statistics": dict(stats),
      "semantic_labels_exhaustive": dict(labels),
      "common_checkpoint": list(checkpoints.pop()),
      "sibling_examples": {
        "r0": list(sibling_pair(0)),
        "r16_lengths": [len(x) for x in sibling_pair(16)],
        "first_distinguishing_cell": "last physical source data cell L",
      },
      "assertion_failures": 0,
      "verification": "native CPython exhaustive plus sibling family; finite COMPUTATIONAL",
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
