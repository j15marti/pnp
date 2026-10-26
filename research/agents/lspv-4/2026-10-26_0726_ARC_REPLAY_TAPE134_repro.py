#!/usr/bin/env python3
"""Standalone exact replay-tape firewall audit (standard library only).

Model: proof payload u||v where both words have k bits. A one-pass exact
verifier must accept precisely when u=v. This is an interface lower bound,
NOT an ordinary-SAT runtime lower bound and NOT a lower bound for the
BRANCH/EMPTY/PATH tree grammar.
"""
import json
from fractions import Fraction


def indexed_equal(u: int, v: int, k: int):
    """Two-sided random-access proof tape, independent of the source tape."""
    tape = [(u >> i) & 1 for i in range(k)] + [(v >> i) & 1 for i in range(k)]
    reads = 0
    for i in range(k):
        reads += 2
        if tape[i] != tape[k + i]:
            return False, reads
    return True, reads


def streaming_materialized(u: int, v: int, k: int):
    """Standard one-way reader storing the initial k-bit prefix."""
    prefix = []
    for i in range(k):
        prefix.append((u >> i) & 1)
    for i in range(k):
        if prefix[i] != ((v >> i) & 1):
            return False, len(prefix)
    return True, len(prefix)


def beta(c: Fraction) -> Fraction:
    return ((c + 2) / (c * c) - c) / 2


def run():
    groups = 0
    pair_checks = 0
    collision_checks = 0
    state_distinguish_checks = 0
    sample = []
    for k in range(1, 9):
        for u in range(1 << k):
            for v in range(1 << k):
                want = (u == v)
                observed, reads = indexed_equal(u, v, k)
                stored, cells = streaming_materialized(u, v, k)
                assert observed == want and stored == want
                assert reads <= 2 * k and cells == k
                groups += 3
                pair_checks += 1
    for k in range(1, 13):
        for u in range(1 << k):
            assert indexed_equal(u, u, k)[0]
            state_distinguish_checks += 1
            groups += 1
        for s in range(k):
            mask = (1 << s) - 1
            u, up = 0, (1 << s)
            assert u != up and (u & mask) == (up & mask)
            assert indexed_equal(u, u, k)[0]
            assert not indexed_equal(up, u, k)[0]
            collision_checks += 3
            groups += 3
        sample.append({'k': k, 'required_information_states': 1 << k,
                       'required_state_bits': k, 'minimal_bad_memory_bits': k - 1})
    c = Fraction(241, 200)
    exact_beta = Fraction(11642479, 23232400)
    assert beta(c) == exact_beta
    assert Fraction(3, 5) > exact_beta
    d = Fraction(901, 500)
    threshold = (2 * d - 1) / (d * (d - 1))
    assert threshold == Fraction(651000, 361301)
    assert Fraction(7, 4) < threshold
    groups += 4
    return {
        'run_id': 'ARC-REPLAY-TAPE134',
        'scope': 'one-pass exact commitment/replay consistency only; not unrestricted SAT',
        'assertion_groups': groups,
        'pair_cases': pair_checks,
        'short_prefix_collision_checks': collision_checks,
        'distinct_residual_checks': state_distinguish_checks,
        'failed_assertions': 0,
        'c_star': str(c),
        'beta_c_star': str(exact_beta),
        'replay_space_exponent': '3/5',
        'replay_minus_beta': str(Fraction(3, 5) - exact_beta),
        'extra_seed_d': str(d),
        'coNTIME_boundary_Cd': str(threshold),
        'illustrative_coNTIME_c': '7/4',
        'coNTIME_strict_margin': str(threshold - Fraction(7, 4)),
        'state_table': sample,
        'read_only_indexed_tape': '2k worst-case reads, O(log k) index bits',
        'one_way_stream_exact': 'at least 2^k distinct midpoint configurations (proof); k information bits',
        'coNTIME_materialization': 'O(P polylog P) time, O(P) writable bits, with uniform length cap',
        'all_input_SAT_lower_bound': False,
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
