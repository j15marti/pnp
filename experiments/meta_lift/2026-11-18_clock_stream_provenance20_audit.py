#!/usr/bin/env python3
"""CLOCKSTREAMPROVENANCE20 finite audit; Python 3.12; stdlib only.

Validates concrete QBF stack semantics and short source-fiber representatives,
not PSPACE-hardness or an actual one-tape simulation.
"""
import itertools
import json
import random
from dataclasses import dataclass
from pathlib import Path

SEED = 202611180612
OUT = Path(__file__).with_name("2026-11-18_CLOCKSTREAMPROVENANCE20_raw.json")

@dataclass(frozen=True)
class Formula:
    quantifiers: tuple[str, ...]
    clauses: tuple[tuple[int, ...], ...]

    @property
    def k(self):
        return len(self.quantifiers)

    def leaf(self, mask):
        for clause in self.clauses:
            if not any((((mask >> (self.k - abs(lit))) & 1) == 1) if lit > 0
                       else (((mask >> (self.k - abs(lit))) & 1) == 0)
                       for lit in clause):
                return 0
        return 1

    def desc(self):
        return ''.join(self.quantifiers) + ':' + ','.join('/'.join(map(str, c)) for c in self.clauses)


def reference_qbf(formula):
    def rec(level, prefix):
        if level == formula.k:
            return formula.leaf(prefix)
        left = rec(level + 1, prefix * 2)
        right = rec(level + 1, prefix * 2 + 1)
        if formula.quantifiers[level] == 'A':
            return left & right
        return left | right
    return rec(0, 0)


def streamed_qbf(formula):
    """One leaf per sequential source tick; at most k+1 pending bits."""
    stack = [None] * (formula.k + 1)
    for mask in range(1 << formula.k):
        v = formula.leaf(mask)
        level = formula.k
        while level > 0 and stack[level] is not None:
            left = stack[level]
            stack[level] = None
            v = (left & v) if formula.quantifiers[level - 1] == 'A' else (left | v)
            level -= 1
        assert stack[level] is None
        stack[level] = v
    assert stack[0] is not None
    assert all(x is None for x in stack[1:])
    return stack[0]


def features(tail):
    adj = int(any(tail[i] and tail[i+1] for i in range(len(tail)-1)))
    parity = sum(tail) & 1
    exactly_one = int(sum(tail) == 1)
    return adj, parity, exactly_one


def canonical(triple, L):
    assert L >= 5
    a, p, e = triple
    if e:
        assert (a, p, e) == (0, 1, 1)
        support = (0,)
    elif a == 0 and p == 0:
        support = ()
    elif a == 0 and p == 1:
        support = (0, 2, 4)
    elif a == 1 and p == 0:
        support = (0, 1)
    elif a == 1 and p == 1:
        support = (0, 1, 3)
    else:
        raise AssertionError(triple)
    return tuple(int(i in support) for i in range(L))


def label(formula, tail):
    a, p, e = features(tail)
    return (formula.desc(), reference_qbf(formula) ^ a, a, p, e)


def sample_formula(rng, k):
    quantifiers = tuple(rng.choice('AE') for _ in range(k))
    clauses = []
    for _ in range(rng.randrange(1, 7)):
        width = rng.randrange(1, min(k, 3) + 1)
        vars_ = rng.sample(range(1, k+1), width)
        clauses.append(tuple(v * rng.choice([-1, 1]) for v in vars_))
    return Formula(quantifiers, tuple(clauses))


def audit():
    rng = random.Random(SEED)
    assertions = 0
    formulas = []
    exhaustive_tails = 0
    canonical_cases = 0
    mixed_fiber_controls = 0
    order_controls = 0
    for k in (1, 2, 3):
        for j in range(12):
            form = sample_formula(rng, k)
            formulas.append(form)
            assert reference_qbf(form) == streamed_qbf(form)
            assertions += 1
            L = 8
            for number in range(1 << L):
                tail = tuple((number >> (L-1-i)) & 1 for i in range(L))
                a, p, e = features(tail)
                g = canonical((a, p, e), L)
                assert features(g) == (a, p, e)
                assert sum(g) <= 3
                assert label(form, g) == label(form, tail)
                assertions += 3
                canonical_cases += 1
                exhaustive_tails += 1
            fiber = [tuple((num >> (L-1-i)) & 1 for i in range(L))
                     for num in range(1 << L)
                     if ((num >> (L-1)) & 1) and ((num >> (L-2)) & 1)
                     and ((num.bit_count() & 1) == 0)]
            assert len(fiber) == 1 << (L-3)
            assert all(features(x) == (1, 0, 0) for x in fiber)
            assert all(label(form, x) == label(form, canonical((1,0,0), L)) for x in fiber)
            assertions += 3
            mixed_fiber_controls += 1
    h1 = (1,0,1,0,0,0,0,0)
    h2 = (1,1,0,0,0,0,0,0)
    assert sum(h1) == sum(h2) == 2
    assert features(h1) != features(h2)
    assertions += 2
    order_controls += 1
    t = Formula(('E',), ((1,),))
    f = Formula(('A',), ((1,),))
    assert streamed_qbf(t) == 1 and streamed_qbf(f) == 0
    assert label(t, (0,)*8)[1:] == (1,0,0,0)
    assert label(f, (0,)*8)[1:] == (0,0,0,0)
    assertions += 4
    payload = {
        'name': 'CLOCKSTREAMPROVENANCE20',
        'status': 'COMPUTATIONAL (finite tests); restricted symbolic theorem separately',
        'date_local': '2026-11-18 06:12 Asia/Seoul',
        'seed': SEED,
        'input_model': 'QBF CNF description + explicit 8-bit tail, small test variant',
        'quantifier_widths': [1,2,3],
        'formula_count': len(formulas),
        'exhaustive_source_tail_cases': exhaustive_tails,
        'canonical_representative_cases': canonical_cases,
        'mixed_fiber_controls': mixed_fiber_controls,
        'order_sensitive_controls': order_controls,
        'assertions': assertions,
        'failures': 0,
        'limitations': [
            'This code is not a universal QBF parser or actual one-work-tape TM.',
            'Finite audit does not establish PSPACE-hardness, circuit lower bounds, or P != NP.',
            'PSPACE result follows from a separate formal TQBF reduction and full-source compiler proof.'
        ],
    }
    OUT.write_text(json.dumps(payload, indent=2) + '\n')
    print(json.dumps(payload, indent=2))


if __name__ == '__main__':
    audit()
