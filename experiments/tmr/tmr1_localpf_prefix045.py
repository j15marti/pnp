#!/usr/bin/env python3
"""TMR-1 LOCAL-PF045 finite machine locality checks, not PF circuit compiler.
Execute: python3 tmr1_localpf_prefix045.py [out.json]
"""
import itertools
import json
import random
import sys
from pathlib import Path

SEED = 202611141704
rng = random.Random(SEED)
counts = {'full_vs_clipped_traces': 0, 'matched_steps': 0,
          'index_prefix_pairs': 0, 'numeric_windows': 0, 'errors': 0}

def read_original(bits, pos):
    if pos < 0: return '^'
    if pos == len(bits): return '#'
    if pos > len(bits): return '_'
    return bits[pos]

def trace(source, index, horizon, truncated=False):
    if truncated:
        # If the word is longer than the step horizon, omit its far suffix.
        # Model this suffix as inaccessible filler, not as an early endmarker.
        src_cut = source[:horizon+1]
        idx_cut = index[:horizon+1]
    else:
        src_cut, idx_cut = source, index
    head_s = head_i = 0
    state = 0
    cell = 0
    history = []
    for _ in range(horizon):
        def symbol(word, original, pos):
            if pos < 0: return '^'
            if pos < len(word): return word[pos]
            if pos < len(original): return '?' # Unreachable if head starts at 0 and moves locally.
            return '#' if pos == len(original) else '_'
        a = symbol(src_cut, source, head_s)
        b = symbol(idx_cut, index, head_i)
        assert a != '?' and b != '?', 'a supposedly inaccessible cell was accessed'
        history.append([head_s, head_i, state, cell, a, b])
        h = (state*17+cell*11+ord(a)*7+ord(b)*13) % 101
        state = (state + h + (a == '1') + 2*(b == '1')) % 7
        cell = (cell ^ (h & 1) ^ ((h >> 3) & 1)) & 1
        head_s = max(0, head_s + ((h % 3)-1))
        head_i = max(0, head_i + (((h // 3) % 3)-1))
    return history, (state ^ cell) & 1

for horizon in range(0, 16):
    for _ in range(360):
        L = rng.randrange(0, 90)
        n = rng.randrange(0, 90)
        source = ''.join(rng.choices('01', k=L))
        index = ''.join(rng.choices('01', k=n))
        full = trace(source, index, horizon)
        clipped = trace(source, index, horizon, True)
        if full != clipped:
            counts['errors'] += 1
            raise AssertionError((horizon, source, index, full, clipped))
        counts['full_vs_clipped_traces'] += 1
        counts['matched_steps'] += horizon

# Index bits strictly beyond the first t+1 positions cannot affect t-step output.
for horizon in range(0, 6):
    for _ in range(28):
        n = 8
        src = ''.join(rng.choices('01', k=rng.randrange(0, 45)))
        buckets = {}
        for seq in itertools.product('01', repeat=n):
            index = ''.join(seq)
            output = trace(src, index, horizon)[1]
            prefix = index[:horizon+1]
            if prefix in buckets and output != buckets[prefix]:
                counts['errors'] += 1
                raise AssertionError((src, horizon, index, prefix, output, buckets[prefix]))
            buckets[prefix] = output
            counts['index_prefix_pairs'] += 1

# An asymptotic strict-exponent window where localized PF is informative but
# the older full-input-copy PF H=L+n+t+2 bound cannot establish MCSP-YES.
for m in range(20, 65, 5):
    L = 2**m
    t = 2**((3*m)//10)
    # a=2, mu=2/5, so s=2^(4m/5)
    s = 2**((4*m)//5)
    if not (t.bit_length() < s.bit_length() and L > s):
        counts['errors'] += 1
        raise AssertionError((m, L, t, s))
    counts['numeric_windows'] += 1

out = {'experiment': 'TMR1-LOCALPF045', 'seed': SEED, 'counts': counts,
       'status': 'COMPUTATIONAL finite local-head prefix and exponent tests only; PF theorem not implemented',
       'source': 'tmr1_localpf_prefix045.py'}
path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/mnt/data/tmr1_1704/tmr1_localpf_prefix045_raw.json')
path.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
print(json.dumps(out, sort_keys=True))
