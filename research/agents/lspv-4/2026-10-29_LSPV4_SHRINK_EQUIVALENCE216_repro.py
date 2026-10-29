#!/usr/bin/env python3
"""Independent audit of strict length descent, closed moving guards, and horizon classes.
No packages, oracle calls, SAT solver or Internet are used.
"""
import itertools
import json
import hashlib
import random
from collections import Counter

rng = random.Random(202610290136)
counts = Counter()

# Explicit single-child length decrement for the PARITY language.
# Input: one parity accumulator bit, followed by arbitrary data bits.
# Acceptance: accumulator XOR parity(data) == 1.
def parity_decide(x):
    return sum(x) & 1

def parity_step(x):
    assert len(x) > 1
    return (x[0] ^ x[1],) + x[2:]

for n in range(1, 14):
    for data in itertools.product((0, 1), repeat=n):
        x = (0,) + data
        answer = parity_decide(x)
        while len(x) > 1:
            y = parity_step(x)
            assert len(y) == len(x) - 1
            assert parity_decide(y) == parity_decide(x)
            x = y
            counts['length_descent_steps'] += 1
        assert x[0] == answer
        counts['parity_full_instances'] += 1

# Canonical proper 3CNF fixed YES/NO instances: 1 clause and all eight clauses.
TRIPLES = tuple(tuple(sign * (i + 1) for i, sign in enumerate(signs))
                for signs in itertools.product((-1, 1), repeat=3))
def sat(clauses, n=3):
    return any(all(any(((assignment >> (abs(lit)-1)) & 1) == (lit > 0)
                       for lit in clause) for clause in clauses)
               for assignment in range(1 << n))
assert sat((TRIPLES[0],)) and not sat(TRIPLES)
for mask in range(1 << len(TRIPLES)):
    clauses = tuple(TRIPLES[j] for j in range(8) if (mask >> j) & 1)
    original = sat(clauses)
    child = (TRIPLES[0],) if original else TRIPLES
    assert sat(child) == original
    counts['fixed_cnf_yes_no_controls'] += 1

# Moving guard: arbitrary truth table over the four end variables,
# and arbitrary signed consecutive-triple clauses.
def guard_eval(mask, endpoints, assignment):
    idx = sum(((assignment >> v) & 1) << j for j, v in enumerate(endpoints))
    return bool(mask & (1 << idx))

def clause_eval(clause, assignment):
    return any(bool(assignment & (1 << (abs(lit)-1))) == (lit > 0)
               for lit in clause)

def formula_eval(clauses, guardmask, endpoints, assignment):
    return guard_eval(guardmask, endpoints, assignment) and all(
        clause_eval(clause, assignment) for clause in clauses)

def signed_consecutive(r):
    return [tuple((i + j + 1) * rng.choice((-1, 1)) for j in range(3))
            for i in range(r-2)]

def exact_project(clauses, guardmask, r, h):
    c = r-h
    assert r >= 5 and 4 <= h < r
    endpoints = (0,1,r-2,r-1)
    new_ends = (c,c+1,r-2,r-1)
    dropped = [cl for cl in clauses if min(abs(l)-1 for l in cl) < c]
    kept = [cl for cl in clauses if min(abs(l)-1 for l in cl) >= c]
    proj = 0
    for index in range(16):
        end_values = {v: (index >> j) & 1 for j,v in enumerate(new_ends)}
        exists = False
        for bits in range(1 << c):
            assignment = bits
            for v,value in end_values.items():
                if value: assignment |= 1 << v
            # Other retained variables do not appear in dropped clauses or old guard.
            if guard_eval(guardmask,endpoints,assignment) and all(
                    clause_eval(cl,assignment) for cl in dropped):
                exists=True;break
        if exists: proj |= (1 << index)
    return proj,kept,new_ends

for r in range(5,10):
    h=max(4,r//2)
    c=r-h
    endpoints=(0,1,r-2,r-1)
    for trial in range(75):
        clauses = signed_consecutive(r)
        # Include both all-yes, all-no and randomly chosen boundary functions.
        guardmask = (0 if trial % 13 == 0 else (65535 if trial % 13 == 1 else rng.getrandbits(16)))
        newmask,kept,new_ends = exact_project(clauses,guardmask,r,h)
        good_old = False
        good_new = False
        for suffix in range(1 << h):
            whole_suffix = suffix << c
            projected = any(formula_eval(clauses,guardmask,endpoints,whole_suffix | prefix)
                            for prefix in range(1 << c))
            child = guard_eval(newmask,new_ends,whole_suffix) and all(
                clause_eval(cl,whole_suffix) for cl in kept)
            assert projected == child, (r,h,trial,suffix)
            counts['projected_full_function_assignments'] += 1
            good_old |= projected
            good_new |= child
        assert good_old == good_new
        counts['moving_guard_cases'] += 1
        counts['moving_guard_SAT' if good_old else 'moving_guard_UNSAT'] += 1

# Full future-answer equivalence classes of the bounded update model.
# The only potentially useful continuation overwrites a subset of cells with 1.
for m in range(1,8):
    for h in range(m+1):
        continuation_sets = [mask for mask in range(1 << m) if mask.bit_count() <= h]
        signatures = {}
        for zeros in range(1 << m):
            signature = tuple((zeros & ~mask)==0 for mask in continuation_sets)
            predicted = (('source',zeros) if zeros.bit_count() <= h else ('overflow',))
            signatures.setdefault(signature,set()).add(predicted)
        # A signature cannot represent two distinct predicted equivalence classes.
        assert all(len(classes)==1 for classes in signatures.values())
        num_classes = (1+sum(__import__('math').comb(m,j) for j in range(h+1))
                       if h<m else 2**m)
        assert len(signatures)==num_classes
        counts['horizon_parameter_cases'] += 1
        counts['horizon_source_cases'] += 1 << m
        counts['horizon_continuation_evaluations'] += (1 << m)*len(continuation_sets)

# Exponential-value rank counterexample: N-bit counter takes 2^N-1 transitions.
for n in range(1,18):
    z=(1<<n)-1
    ticks=0
    while z:
        z-=1; ticks+=1
    assert ticks == (1<<n)-1
    counts['rank_counter_steps']+=ticks
    counts['rank_bits_checked']+=1

print(json.dumps({'status':'PASS','seed':202610290136,'counts':dict(counts),
 'claims':{'power_shrinker_equivalence':'mathematical proof in report, not experimentally proved',
           'moving_guard':'exact full-function comparisons',
           'rank_counter':'binary encoded rank admits exponential number of decrements'},
 'limitations':['No unrestricted SAT shrinker was constructed.',
                'These are finite controls, not native TM transition measurements.',
                'No formal proof assistant kernel checking was performed.']},indent=2,sort_keys=True))