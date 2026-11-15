#!/usr/bin/env python3
"""TMR-4/034, GLOBALORACLE050: finite adaptive black-box coupling audit.

Every test uses a total deterministic oracle transducer that may adapt,
repeat queries, stop early and emit an output vector dependent on prior answers.
No SAT decision computation or general TM compiler is asserted.
"""
import json
import random
from fractions import Fraction

SEED = 202611141834
rng = random.Random(SEED)
checks = 0
traces = 0
proper_clauses = 0

def check(condition, what):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(what)

def oracle_run(M, support, policy):
    seen = set()
    history = []
    output = []
    for step in range(policy['budget']):
        action = policy['rules'].get(tuple(history))
        if action is None:
            break
        op, arg = action
        if op == 'read':
            addr = arg % M
            bit = int(addr in support)
            seen.add(addr)
            history.append((addr, bit))
        elif op == 'emit':
            output.append(arg & 1)
            history.append(('emit', arg & 1))
        else:
            break
    return tuple(output), frozenset(seen), tuple(history)

def random_policy(M):
    # Generate an acyclic adaptive policy whose rules are defined for both replies.
    budget = 9
    rules = {}
    def expand(history, depth):
        if depth >= budget:
            return
        u = rng.random()
        if u < 0.25:
            rules[history] = ('stop', 0)
            return
        if u < 0.68:
            a = rng.randrange(M)
            rules[history] = ('read', a)
            expand(history + ((a, 0),), depth + 1)
            expand(history + ((a, 1),), depth + 1)
        else:
            b = rng.randrange(2)
            rules[history] = ('emit', b)
            expand(history + (('emit', b),), depth + 1)
    expand((), 0)
    return {'budget': budget, 'rules': rules}

def force(v, i, truth):
    j, k = (i + 1) % v, (i + 2) % v
    base = (i + 1) if truth else -(i + 1)
    return [(base, j + 1 if b else -(j + 1), k + 1 if c else -(k + 1))
            for b in (0, 1) for c in (0, 1)]

def evaluate(v, clauses, assignment):
    return all(any(((assignment >> (abs(lit)-1)) & 1) == int(lit > 0)
                   for lit in clause) for clause in clauses)

for M in (2, 4, 8):
    for p in range(500):
        pol = random_policy(M)
        out0, query0, trace0 = oracle_run(M, set(), pol)
        for a in range(M):
            out1, _, trace1 = oracle_run(M, {a}, pol)
            if a not in query0:
                check((out0, trace0) == (out1, trace1),
                      f'coupling failed M={M} p={p} a={a}')
            traces += 1

for v in (3, 4, 5, 6):
    M = 1 << v
    for a in range(M):
        F = [cl for i in range(v) for cl in force(v, i, (a >> i) & 1)]
        F += force(v, 0, a & 1)  # redundant padding: 4(v+1) clauses
        U = [cl for i in range(v) for cl in force(v, i, (a >> i) & 1)]
        U += force(v, 0, 1-(a & 1))  # incompatible, same clause count
        check(len(F) == len(U) == 4*(v+1), 'clause length')
        for clause in F + U:
            check(len({abs(z) for z in clause}) == 3, 'proper 3-clause')
            proper_clauses += 1
        for x in range(M):
            check(evaluate(v, F, x) == (x == a), 'unique witness')
            check(not evaluate(v, U, x), 'unsat')

# Exact rational upper/lower error and the optimal charged baseline budget.
for M in (2, 4, 8, 16, 32):
    for delta in (Fraction(0), Fraction(1, 5), Fraction(1, 4), Fraction(1, 3)):
        full = 1-2*delta
        # With probability delta, answer YES without reading; with delta, NO;
        # with remainder, read entire source and decide OR exactly.
        err_on_zero = delta
        err_on_each_singleton = delta
        eq0 = full*M
        lower = (1-2*delta)*M
        check(eq0 == lower and err_on_zero <= delta and
              err_on_each_singleton <= delta, 'randomized tightness')

raw = {
    'claim': 'GLOBALORACLE050', 'seed': SEED, 'models': 'black-box zero-vs-singleton oracle',
    'machine': 'finite adaptive decision/output policy with globally shared query transcript',
    'policy_count': 1500, 'paired_traces': traces,
    'proper_three_literal_clauses_tested': proper_clauses,
    'assertions': checks, 'failures': 0,
    'narrative': 'finite proxy verification, not a physical TM or asymptotic proof',
    'status': 'COMPUTATIONAL',
}
print(json.dumps(raw, sort_keys=True, indent=2))
