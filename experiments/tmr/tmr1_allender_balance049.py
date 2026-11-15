#!/usr/bin/env python3
"""TMR-1/049. Exhaustive double-majority balanced unique-witness gadget.
Finite evidence only; symbolic proof is in accompanying report.
No random numbers, no external packages. Python 3.12+ compatible.
"""
import json
from collections import Counter


def truth_bit(mask, a, b, k):
    return (mask >> ((a << k) | b)) & 1


def witness(a, b, m):
    return (7 * a + 3 * b + 1) % (1 << m)


def gadget(mask, a, b, z, v, k, m, unique=True, background=True):
    f = truth_bit(mask, a, b, k)
    phi = f and ((z == witness(a, b, m)) if unique else True)
    return bool((v and phi) or ((not v) and background and ((b & 1) or (z != 0))))


def direct_count(mask, a, k, m, unique=True, background=True):
    return sum(gadget(mask, a, b, z, v, k, m, unique, background)
               for b in range(1 << k) for z in range(1 << m) for v in (0, 1))


def run():
    cases = 0
    inner_checks = 0
    outer_checks = 0
    ties = 0
    yes_cases = 0
    by_param = []
    for outer_bits in (1, 2):
        for inner_bits in (1, 2, 3):
            if outer_bits + inner_bits > 4:
                continue
            f_table_size = 1 << (outer_bits + inner_bits)
            masks = range(1 << f_table_size)
            for aux_bits in (1, 2, 3):
                local = 0
                for mask in masks:
                    outer_before = 0
                    outer_after = 0
                    for a in range(1 << outer_bits):
                        count = sum(truth_bit(mask, a, b, inner_bits) for b in range(1 << inner_bits))
                        expected = (1 << (aux_bits + inner_bits)) - (1 << (inner_bits - 1)) + count
                        got = direct_count(mask, a, inner_bits, aux_bits)
                        assert got == expected, (outer_bits, inner_bits, aux_bits, mask, a, got, expected)
                        original_majority = count >= (1 << (inner_bits - 1))
                        new_majority = got >= (1 << (inner_bits + aux_bits))
                        assert original_majority == new_majority
                        inner_checks += 1
                        ties += count == (1 << (inner_bits - 1))
                        outer_before += original_majority
                        outer_after += new_majority
                    assert outer_before == outer_after
                    assert ((outer_before >= (1 << (outer_bits - 1))) ==
                            (outer_after >= (1 << (outer_bits - 1))))
                    outer_checks += 1
                    yes_cases += outer_before >= (1 << (outer_bits - 1))
                    cases += 1
                    local += 1
                by_param.append({'outer': outer_bits, 'inner': inner_bits,
                                 'aux': aux_bits, 'truth_tables': local})
    # Nonunique auxiliary extensions CAN change the nested decision.
    # Outer a is irrelevant. One of four b assignments is TRUE, but all four z values
    # extend this b. Original inner majority is NO (1 < 2); gadget yields 18 >= 16.
    k, m = 2, 2
    mask = 1 << 0  # b=0 is the sole accepting b for a=0
    count_bad = direct_count(mask, 0, k, m, unique=False)
    assert count_bad == 18 and count_bad >= (1 << (k + m))
    count_good = direct_count(mask, 0, k, m, unique=True)
    assert count_good == 15 and count_good < (1 << (k + m))
    # Removing the v=0 balancing clause destroys even an easy YES witness.
    mask_all = (1 << (1 << k)) - 1
    no_background = direct_count(mask_all, 0, k, m, background=False)
    assert no_background == (1 << k) and no_background < (1 << (k + m))
    # Exact inclusive-tie control: f(b)=b_0 gives two of four YES.
    mask_tie = sum(1 << b for b in range(1 << k) if (b & 1))
    tie_gadget = direct_count(mask_tie, 0, k, m)
    assert tie_gadget == (1 << (k + m))
    return {
        'experiment': 'TMR1_ALLENDER_BALANCE049',
        'method': 'exhaustive deterministic truth-table enumeration and direct (b,z,v) evaluation',
        'parameters': by_param,
        'nested_truth_tables': cases,
        'inner_count_and_threshold_checks': inner_checks,
        'outer_majority_checks': outer_checks,
        'inner_exact_ties': ties,
        'outer_yes_cases': yes_cases,
        'negative_controls': {
            'nonunique_all_extensions_no_to_yes': {'correct': count_good, 'nonunique': count_bad, 'threshold': 16},
            'without_balancing_even_all_true_fails': {'count': no_background, 'threshold': 16},
            'inclusive_tie': {'count': tie_gadget, 'threshold': 16},
        },
        'failures': 0,
        'scope': 'COMPUTATIONAL finite check; not SAT or MajMajSAT time-space lower bound',
    }

if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
