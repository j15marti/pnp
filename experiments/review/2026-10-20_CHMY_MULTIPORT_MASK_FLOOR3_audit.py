#!/usr/bin/env python3
"""Exact multiport-mask exhaustive audit and affine-history control."""
import json
from random import Random
from pathlib import Path

RUN_ID = 'CHMY_MULTIPORT_MASK_FLOOR3'
SEED = 202610200320

def effective_source_bit(h, ports_mask, mask_bits):
    """D_j XOR f at each j in ports, G_{i+1}=D_i XOR (T_i AND G_i)."""
    out = 0
    for j in range(1, h + 1):
        if (ports_mask >> (j - 1)) & 1:
            term = 1
            for i in range(j + 1, h + 1):
                term &= (mask_bits >> (i - 1)) & 1
            out ^= term
    return out

def trajectory_recurrence_bit(h, ports_mask, mask_bits, g1, d_mask, f):
    g = g1
    for i in range(1, h + 1):
        d = (d_mask >> (i - 1)) & 1
        t = (mask_bits >> (i - 1)) & 1
        g = d ^ ((t & g)) ^ (f if (ports_mask >> (i - 1)) & 1 else 0)
    return g

def matvec(rows, v):
    return sum(((r & v).bit_count() & 1) << i for i, r in enumerate(rows))

def apply_affine(a, b, x):
    return matvec(a, x) ^ b

def compose(f, g):
    """Return f after g, each affine map (matrix rows, shift)."""
    a, b = f
    c, d = g
    aa = [__import__("functools").reduce(int.__xor__, (c[j] for j in range(len(c)) if (row >> j) & 1), 0) for row in a]
    return aa, apply_affine(a, b, d)

def fastforward(f, x, t):
    d = len(f[0])
    res = ([1 << i for i in range(d)], 0)
    power = f
    while t:
        if t & 1:
            res = compose(power, res)
        power = compose(power, power)
        t >>= 1
    return apply_affine(*res, x)

def main():
    stats = {'run_id': RUN_ID, 'seed': SEED,
             'scope': 'bitwise masks iid across layers with fair marginal; fixed port set',
             'by_h': [], 'counterexamples': {}, 'affine_control': {}}
    total_portsets = total_mask_states = total_checks = 0
    for h in range(1, 10):
        observed_min_ratio = 2
        observed_max_ratio = -1
        for ports in range(1, 1 << h):
            latest = ports.bit_length()
            t = h - latest
            hits = 0
            for mask in range(1 << h):
                val = effective_source_bit(h, ports, mask)
                hits += val
                base = trajectory_recurrence_bit(h, 0, mask, 1, 0, 0)
                transformed = trajectory_recurrence_bit(h, ports, mask, 1, 0, 1)
                assert (base ^ transformed) == val
                total_checks += 1
                if latest < h:
                    suffix_on = all((mask >> (i - 1)) & 1 for i in range(latest + 1, h + 1))
                    if suffix_on and ((mask >> (latest - 1)) & 1) == 0:
                        assert val == 1
                        total_checks += 1
            numerator = hits << t
            denominator = 1 << h
            assert 2 * numerator >= denominator and numerator <= denominator
            if ports.bit_count() == 1:
                assert numerator == denominator
            observed_min_ratio = min(observed_min_ratio, numerator / denominator)
            observed_max_ratio = max(observed_max_ratio, numerator / denominator)
            total_portsets += 1
            total_mask_states += 1 << h
        stats['by_h'].append({'h': h, 'port_sets': (1 << h) - 1,
                              'exposure_ratio_min': observed_min_ratio,
                              'exposure_ratio_max': observed_max_ratio})
    correlation_hits = [effective_source_bit(3, 3, (tt << 1) | (tt << 2)) for tt in (0, 1)]
    assert correlation_hits == [0, 0]
    stats['counterexamples']['reused_layers_h3_ports_1_2'] = correlation_hits
    rng = Random(SEED)
    affine_checks = 0
    for d in range(2, 9):
        mask = (1 << d) - 1
        for _ in range(30):
            a = [rng.randrange(mask + 1) for _ in range(d)]
            b = rng.randrange(mask + 1)
            x = rng.randrange(mask + 1)
            for t in (0, 1, 2, 3, 5, 8, 13, 31, 64, 127):
                z = x
                for _ in range(t):
                    z = apply_affine(a, b, z)
                assert fastforward((a, b), x, t) == z
                affine_checks += 1
    stats['affine_control'] = {'dimensions': [2, 3, 4, 5, 6, 7, 8],
                               'maps_per_dimension': 30, 'time_indices': 10,
                               'passed': affine_checks}
    stats['checks'] = {'port_sets': total_portsets, 'mask_state_evaluations': total_mask_states,
                        'recurrence_and_frontier_assertions': total_checks,
                        'affine_fastforward_assertions': affine_checks, 'failures': 0}
    print(json.dumps(stats, indent=2, sort_keys=True))
    Path(__file__).with_suffix('.json').write_text(json.dumps(stats, indent=2, sort_keys=True)+'\n')

if __name__ == '__main__':
    main()
