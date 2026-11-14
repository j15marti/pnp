#!/usr/bin/env python3
"""TMR-3/028 independent physical-head micro-rotation and MCSP finite controls.
This executes single-head tape rotations, NOT a compiled full TM MCSP decider.
"""
import json
from itertools import product

passes = rotations = operations = comparisons = 0

def rotate_right(tape, start, width):
    """One physical head, one carried alphabet symbol, shift [scratch,bit] -> [bit,scratch]."""
    global rotations, operations
    carry = tape[start]
    for j in range(start + 1, start + width + 1):
        next_carry = tape[j]
        tape[j] = carry
        carry = next_carry
        operations += 2  # a local move and rewrite, with one-symbol finite-control buffer
    tape[start] = carry
    operations += width + 1  # return sweep and terminal rewrite
    rotations += 1

def rotate_left(tape, start, width):
    """One physical head, one carried symbol, shift [bit,scratch] -> [scratch,bit]."""
    global rotations, operations
    carry = tape[start + width]
    operations += width  # move from boundary to right endpoint
    for j in range(start + width - 1, start - 1, -1):
        next_carry = tape[j]
        tape[j] = carry
        carry = next_carry
        operations += 2
    tape[start + width] = carry
    operations += width + 1
    rotations += 1

def physical_sweep(bits, target_mask, width):
    """Symbolic candidate test, but every data/scratch crossing is a literal tape rewrite."""
    global passes, comparisons
    N = len(bits)
    scratch = list('S' + ('u' * (width - 2)) + 'E')
    tape = scratch + [str(b) for b in bits]
    matched = True
    for i, b in enumerate(bits):
        matched &= ((target_mask >> i) & 1) == b
        comparisons += 1
        rotate_right(tape, i, width)
        assert tape == [str(v) for v in bits[:i+1]] + scratch + [str(v) for v in bits[i+1:]]
    for i in range(N - 1, -1, -1):
        rotate_left(tape, i, width)
        assert tape == [str(v) for v in bits[:i]] + scratch + [str(v) for v in bits[i:]]
    assert tape == scratch + [str(v) for v in bits]
    passes += 1
    return bool(matched)

def gate_vals(n, s):
    """Independent complete straight-line gate-list semantics up to s gates."""
    N = 1 << n
    full = (1 << N) - 1
    vars_ = [sum(((i >> j) & 1) << i for i in range(N)) for j in range(n)]
    sources = tuple([0, full] + vars_)
    outs = set(sources)
    states = [sources]
    for _ in range(s):
        nxt = []
        for wires in states:
            choices = {full ^ a for a in wires}
            choices |= {a & b for a in wires for b in wires}
            choices |= {a | b for a in wires for b in wires}
            for v in choices:
                nxt.append(wires + (v,))
                outs.add(v)
        states = nxt
    return sorted(outs)

checks = 0
class_count = {}
for n in (1, 2, 3):
    N = 1 << n
    for s in (0, 1, 2):
        candidates = gate_vals(n, s)
        class_count[f'{n}:{s}'] = len(candidates)
        assert len(candidates) == {(1,0):3,(1,1):4,(1,2):4,(2,0):4,(2,1):8,(2,2):14,(3,0):5,(3,1):14,(3,2):40}[(n,s)]
        checks += 1
        for truth in range(1 << N):
            bits = [(truth >> i) & 1 for i in range(N)]
            width = 3 + n + 2 * s
            found = any(physical_sweep(bits, candidate, width) for candidate in candidates)
            expected = truth in candidates
            assert found == expected, (n, s, truth)
            checks += 1

# Direct independent one-head finite rotations over all 4-bit source strings and scratch widths 2..9.
for width in range(2, 10):
    for raw in product('01', repeat=4):
        scratch = list('S' + 'z' * (width-2) + 'E')
        tape = scratch + list(raw)
        for i in range(4):
            rotate_right(tape, i, width)
            assert tape == list(raw[:i+1]) + scratch + list(raw[i+1:])
            checks += 1
        for i in range(3, -1, -1):
            rotate_left(tape, i, width)
            assert tape == list(raw[:i]) + scratch + list(raw[i:])
            checks += 1

print(json.dumps({'label':'RAWSCAN31','status':'COMPUTATIONAL','single_head_rotate_primitives':rotations,'charged_symbol_moves_and_rewrites_proxy':operations,'full_candidate_sweeps':passes,'candidate_bit_comparisons':comparisons,'assertions_passed':checks,'failures':0,'gate_class_counts':class_count,'limitations':'literal finite-alphabet head-rotation rewrites executed; candidate truth bits evaluated by Python integer semantics, not a compiled all-transition TM; analytic header-known streaming variant not executed'},indent=2,sort_keys=True))
