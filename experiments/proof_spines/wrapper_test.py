#!/usr/bin/env python3
"""Bounded accounting and SAT semantic controls, not a general shrinker proof."""
import itertools
import json
import math
import random
import time
from fractions import Fraction
from pathlib import Path

START = time.monotonic()
DEADLINE = START + 25.0
SEED = 20261007
rng = random.Random(SEED)

def check_time():
    if time.monotonic() > DEADLINE:
        raise TimeoutError('25-second batch deadline; split workload before retry')

def sat(formula, n):
    for bits in itertools.product((False, True), repeat=n):
        check_time()
        if all(any(bits[abs(v)-1] == (v > 0) for v in clause) for clause in formula):
            return True
    return False

def restrict(formula, variable, value):
    true_literal = variable if value else -variable
    return tuple(tuple(v for v in clause if v != -true_literal)
                 for clause in formula if true_literal not in clause)

def main():
    semantic_cases = 0
    for n in range(1, 8):
        for _ in range(30):
            check_time()
            formula = tuple(tuple((v if rng.randrange(2) else -v)
                                  for v in rng.sample(range(1, n+1), min(n, 3)))
                            for _ in range(rng.randrange(1, 15)))
            variable = rng.randrange(1, n+1)
            answer = sat(formula, n)
            child_answers = [sat(restrict(formula, variable, value), n)
                             for value in (False, True)]
            assert answer == any(child_answers)
            semantic_cases += 1
    # Equal SAT answers do not ensure equivalence under a common future restriction.
    f, g = ((1,),), ((-1,),)
    assert sat(f, 1) == sat(g, 1)
    assert sat(restrict(f, 1, True), 1) != sat(restrict(g, 1, True), 1)
    recurrence_cases = 0
    for a in (Fraction(0), Fraction(1, 3), Fraction(1, 2)):
        for b in (Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)):
            for c in (Fraction(1), Fraction(2)):
                for k in (2, 20, 100):
                    exponent = Fraction(k)
                    for depth in range(1, 21):
                        exponent = max(c, a + b * exponent)
                        geometric = a*(1-b**depth)/(1-b)
                        locals_ = [a*(1-b**j)/(1-b)+c*b**j for j in range(depth)]
                        closed = max(locals_ + [geometric+k*b**depth])
                        assert exponent == closed
                        assert closed <= max(c, a/(1-b)) + k*b**depth
                        recurrence_cases += 1
                        check_time()
    gamma = 2*math.cos(math.pi/7)
    a, b, c, s, k, ell = 1/3, 2/3, 1.0, 0.0, 100.0, 100.0
    target = max(c,a/(1-b))+max(s,b)
    depth = 1
    while (k+ell)*b**depth >= (gamma-target)/2:
        depth += 1
    finite_time = max([a*(1-b**j)/(1-b)+c*b**j for j in range(depth)]
                      + [a*(1-b**depth)/(1-b)+k*b**depth])
    finite_space = max(s,b,ell*b**depth)
    assert finite_time+finite_space < gamma
    cover_cases = []
    for n in range(1, 11):
        for live in range(n+1):
            # Exact partition formed by fixing the first n-live coordinates.
            q = 2**(n-live)
            assert q*2**live == 2**n
            cover_cases.append((n, live, q))
    result = dict(status='PASS', scope='Finite accounting and semantic controls only; no general SAT shrinker established',
                  seed=SEED, semantic_cases=semantic_cases, recurrence_cases=recurrence_cases,
                  invalid_merge_counterexamples=1, coverage_cases=len(cover_cases),
                  hypothetical_fixed_depth=dict(depth=depth, K=k, L=ell, time_exponent=finite_time,
                                               space_exponent=finite_space, gamma=gamma),
                  elapsed_seconds=time.monotonic()-START, deadline_seconds=25)
    Path(__file__).with_name('wrapper_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
