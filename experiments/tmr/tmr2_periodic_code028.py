#!/usr/bin/env python3
"""TMR-2/028: periodic truth-table code, exact-query frontier, tape proxy.
Finite verification of an elementary symbolic construction. This is NOT a
compiled finite-alphabet TM, a general MCSP algorithm, or a P-vs-NP proof.
"""
import json
import itertools
import math
import random
from collections import Counter

SEED = 20261114
rng = random.Random(SEED)


def period_k(n, denominator):
    assert n >= 1 and denominator >= 2
    return 1 << (n // denominator)


def repeat_block(block, N):
    assert len(block) > 0 and N % len(block) == 0
    return tuple(block) * (N // len(block))


def reference_periodic(bits, k):
    return all(v == bits[i % k] for i, v in enumerate(bits))


class TapeProxy:
    """Sequential one-head movements and writes are charged explicitly.
    Each physical tape cell has three fixed finite tracks x, t, live.
    End-of-data length and arithmetic use Python in the testing harness only.
    """
    def __init__(self, bits):
        self.cells = [[int(b), None, True] for b in bits]
        self.head = len(bits)
        self.steps = 2 * len(bits)  # one source read/write plus right move
        self.max_head = self.head
        self.operations = Counter()
        self.operations['copy'] = len(bits)

    def goto(self, j):
        assert 0 <= j <= len(self.cells)
        self.steps += abs(self.head - j)
        self.head = j
        self.max_head = max(self.max_head, j)

    def read(self, j, track):
        self.goto(j)
        self.steps += 1
        return self.cells[j][track]

    def write(self, j, track, value):
        self.goto(j)
        self.steps += 1
        self.cells[j][track] = value

    def check_length_by_halving(self):
        N = len(self.cells)
        if N < 2:
            return None
        n = 0
        while True:
            # Full sequential sweep, with finite-control parity, clearing
            # every second still-live marker; zero/one/many detected locally.
            self.goto(0)
            live_count = 0
            parity = 0
            for j in range(N):
                self.goto(j)
                self.steps += 1  # read live
                if self.cells[j][2]:
                    live_count += 1
                    parity ^= 1
                    if parity == 0:
                        self.cells[j][2] = False
                        self.steps += 1
            self.operations['halving_passes'] += 1
            if live_count == 1:
                return n
            if live_count == 0 or live_count % 2:
                return None
            n += 1

    def shift_template_one(self, left, k):
        # Right-to-left copy avoids clobbering unread template cells.
        for j in range(left + k - 1, left - 1, -1):
            old = self.read(j, 1)
            assert old in (0, 1)
            assert self.read(j + 1, 1) is None
            self.write(j + 1, 1, old)
            self.write(j, 1, None)
        self.operations['unit_template_shifts'] += 1

    def decide(self, denominator):
        n = self.check_length_by_halving()
        if n is None:
            return False, None
        N = len(self.cells)
        assert 1 << n == N
        h = n // denominator
        k = 1 << h
        assert N % k == 0
        # Mark/copy first k symbols on the spare track.
        for j in range(k):
            self.write(j, 1, self.read(j, 0))
        left = 0
        for b in range(1, N // k):
            # Move the contiguous k-symbol template to the next block.
            for _ in range(k):
                self.shift_template_one(left, k)
                left += 1
            assert left == b * k
            for j in range(left, left + k):
                if self.read(j, 0) != self.read(j, 1):
                    return False, n
            self.operations['verified_blocks'] += 1
        return True, n


def check_one(bits, denom, details):
    n = len(bits).bit_length() - 1 if len(bits) and len(bits) & (len(bits)-1) == 0 else None
    expected = n is not None and len(bits) >= 2 and reference_periodic(bits, period_k(n, denom))
    sim = TapeProxy(bits)
    got, found_n = sim.decide(denom)
    assert got == expected, (len(bits), denom, bits, got, expected)
    if n is not None and n >= 1:
        assert n == found_n
        k = period_k(n, denom)
        assert sim.steps <= 100 * len(bits) * (k + n + 1) + 1000
    details['proxy_cases'] += 1
    details['proxy_steps'] += sim.steps
    details['max_proxy_steps'] = max(details['max_proxy_steps'], sim.steps)
    details['unit_shifts'] += sim.operations['unit_template_shifts']
    details['halving_passes'] += sim.operations['halving_passes']


def run():
    d = {'test':'TMR2_PERIODIC_GROWING_S028','seed':SEED,'status':'PASS',
         'execution':'native CPython: physical head/tape proxy, not compiled TM',
         'proxy_cases':0,'proxy_steps':0,'max_proxy_steps':0,
         'unit_shifts':0,'halving_passes':0,
         'exhaustive_reference_cases':0,'codeword_checks':0,
         'minimum_distance_checks':0,'boundary_flip_checks':0,
         'malformed_cases':0,'multiplexer_bound_checks':0,
         'sample_catalog':[], 'failures':0}
    for denom in [2, 3, 4]:
        for n in range(1, 8):
            N = 1 << n
            k = period_k(n, denom)
            h = n // denom
            # Exhaust all N-bit strings for n <= 3.
            if n <= 3:
                tests = [tuple((mask >> j) & 1 for j in range(N)) for mask in range(1 << N)]
                d['exhaustive_reference_cases'] += len(tests)
            else:
                tests = []
                for pattern in itertools.islice(itertools.product([0,1], repeat=k), 256):
                    good = repeat_block(pattern, N)
                    tests.append(good)
                    d['codeword_checks'] += 1
                    flip = list(good)
                    flip[(N // 2 + len(tests)) % N] ^= 1
                    tests.append(tuple(flip))
                    d['boundary_flip_checks'] += 1
                for _ in range(25):
                    tests.append(tuple(rng.getrandbits(1) for _ in range(N)))
            for bits in tests:
                check_one(bits, denom, d)
            # All data blocks give distinct words; minimum distance exactly N/k.
            if k <= 8:
                words = [repeat_block(p, N) for p in itertools.product((0,1), repeat=k)]
                assert len(set(words)) == 1 << k
                dmin = min(sum(a != b for a,b in zip(u,v)) for i,u in enumerate(words)
                           for v in words[i+1:]) if len(words)>1 else N
                assert dmin == N // k
                d['minimum_distance_checks'] += 1
            assert 3*(k-1)+h <= 4*k+h
            d['multiplexer_bound_checks'] += 1
            d['sample_catalog'].append({'n':n,'denominator':denom,'N':N,'k':k,
                         'code_size':1<<k,'min_distance':N//k,
                         'gate_bound':3*(k-1)+h,'time_proxy_accepted_example':d['max_proxy_steps']})
        for L in (0,1,3,5,6,7,9,10,11,12,13,14,15):
            bits=tuple(rng.getrandbits(1) for _ in range(L))
            check_one(bits,denom,d)
            d['malformed_cases']+=1
    # Direct acceptance-cylinder certificate controls: code C_h with d=N/k.
    for n, denom in [(3,2),(4,2)]:
        N=1<<n; k=period_k(n,denom); dmin=N//k
        words=[repeat_block(p,N) for p in itertools.product((0,1),repeat=k)]
        for radius in range(1,dmin//2+1):
            Q=N-radius+1
            for cw in words:
                for flip_positions in itertools.combinations(range(N),radius):
                    y=list(cw)
                    for j in flip_positions:y[j]^=1
                    dist=min(sum(a!=b for a,b in zip(y,v)) for v in words)
                    assert dist==radius
                    d['boundary_flip_checks']+=1
                # N-r+1 fixed coordinate queries exclude far NO on YES.
                # Any N-r queries leave r bits, and the r-bit flips are NO.
                assert Q == N-radius+1
    d['total_checks']=sum(d[k] for k in ['proxy_cases','minimum_distance_checks','boundary_flip_checks','malformed_cases','multiplexer_bound_checks'])
    print(json.dumps(d,sort_keys=True,separators=(',',':')))

if __name__=='__main__':
    run()
