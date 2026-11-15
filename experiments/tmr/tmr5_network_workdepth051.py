#!/usr/bin/env python3
"""TMR-5/030: independently check a charged OR-oracle network coupling.
Finite oracle/event interpreter only; not a physical TM or SAT lower bound.
"""
import json
import random
from fractions import Fraction

rng = random.Random(202611141850)
checks = 0

def check(b, label):
    global checks
    checks += 1
    if not b:
        raise AssertionError(label)

def sharp_run(M, K, coin, support):
    # Four equiprobable branches. At most K distinct oracle probes per tick.
    if coin == 0:
        return 1, 0, 0, frozenset()
    if coin == 1:
        return 0, 0, 0, frozenset()
    seen = set()
    ticks = 0
    for pos in range(0, M, K):
        ticks += 1
        seen.update(range(pos, min(M, pos + K)))
    return int(bool(seen.intersection(support))), len(seen), ticks, frozenset(seen)

def adaptive_run(M, K, salt, support):
    # Globally shared deterministic adaptive policy; multiple lanes per tick.
    seen, log = set(), []
    ticks = 0
    for _ in range(1 + (salt % 7)):
        ticks += 1
        batch = []
        for lane in range(K):
            addr = (salt * 11 + ticks * 13 + lane * 7 + sum(log) * 5) % M
            batch.append(addr)
        replies = [int(a in support) for a in batch]
        seen.update(batch)
        log.extend(replies)
        if any(replies) and salt % 3 == 0:
            break
    # Message/postprocessing output is charged as another event if needed;
    # omission only weakens the lower bound under audit.
    return tuple(log), frozenset(seen), ticks

for M in range(1, 45):
    for K in range(1, 9):
        zero = [sharp_run(M, K, coin, frozenset()) for coin in range(4)]
        expected_queries = sum(Fraction(z[1], 4) for z in zero)
        expected_ticks = sum(Fraction(z[2], 4) for z in zero)
        check(expected_queries == Fraction(M, 2), 'sharp work equality')
        check(K * expected_ticks >= Fraction(M, 2), 'parallel work depth')
        check(sum(z[0] == 1 for z in zero) == 1, 'zero-error fraction')
        for a in range(M):
            one = [sharp_run(M, K, coin, frozenset([a])) for coin in range(4)]
            check(sum(z[0] == 0 for z in one) == 1, 'singleton-error fraction')
            for coin in range(4):
                z, q = zero[coin], one[coin]
                if a not in z[3]:
                    check(z == q, 'unqueried coupling')

adaptive_pairs = 0
for i in range(1200):
    M = rng.randint(2, 23)
    K = rng.randint(1, 7)
    salt = rng.randint(0, 100000)
    zero = adaptive_run(M, K, salt, frozenset())
    check(len(zero[1]) <= K * zero[2], 'adaptive work bound')
    for a in range(M):
        one = adaptive_run(M, K, salt, frozenset([a]))
        if a not in zero[1]:
            check(one == zero, 'adaptive zero-singleton trace coupling')
        adaptive_pairs += 1

print(json.dumps({'claim':'TMR5_NETWORK051', 'timestamp_pst':'2026-11-14 18:50 PST',
                  'model':'finite shared-oracle network event proxy',
                  'source_sizes_tested':'M=1..44', 'processors_tested':'K=1..8',
                  'random_adaptive_policies':1200, 'paired_adaptive_traces':adaptive_pairs,
                  'exact_checks':checks,'failures':0,'status':'COMPUTATIONAL',
                  'note':'Symbolic proof separate; syntax-aware SAT unrestricted transfer OPEN'},
                 indent=2, sort_keys=True))
