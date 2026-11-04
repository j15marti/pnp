#!/usr/bin/env python3
"""LSPV-1/391 finite encoding and Resolution controls, dependency-free, Python >=3.10."""
import itertools
import json
from collections import deque

LITERALS = (-2, -1, 1, 2)
CLAUSES = tuple(sorted(((x,) for x in LITERALS), key=str)) + tuple(
    (a, b) for a, b in itertools.combinations(LITERALS, 2) if a != -b
)
assert len(CLAUSES) == 8

def canonical(formula):
    return tuple(sorted((tuple(sorted(c)) for c in formula)))

def enc_a(formula):
    cs = canonical(formula)
    return 'CNF2|' + ';'.join(','.join(str(a) for a in c) for c in cs) + '|'

def parse_a(text):
    if not isinstance(text, str) or not text.startswith('CNF2|') or not text.endswith('|'):
        raise ValueError('invalid wrapper')
    middle = text[5:-1]
    clauses = [] if middle == '' else [tuple(int(t) for t in c.split(',')) for c in middle.split(';')]
    for c in clauses:
        if not c or len(c) > 2 or any(v not in LITERALS for v in c):
            raise ValueError('invalid clause')
        if any(v == -w for v in c for w in c):
            raise ValueError('tautological clause')
    cs = canonical(clauses)
    if text != enc_a(cs) or len(set(cs)) != len(cs):
        raise ValueError('noncanonical/duplicate source')
    return cs

def enc_b(formula):
    return 'H2:' + enc_a(formula).encode('ascii').hex()

def parse_b(text):
    if not isinstance(text, str) or not text.startswith('H2:'):
        raise ValueError('invalid tagged encoding')
    try:
        decoded = bytes.fromhex(text[3:]).decode('ascii')
    except (ValueError, UnicodeError) as e:
        raise ValueError('invalid hex') from e
    cs = parse_a(decoded)
    if enc_b(cs) != text:
        raise ValueError('noncanonical hex')
    return cs

def sat(formula):
    return any(all(any((assignment[abs(v) - 1] if v > 0 else not assignment[abs(v) - 1]) for v in c)
                   for c in formula) for assignment in itertools.product((False, True), repeat=2))

def resolve(a, b):
    for v in a:
        if -v in b:
            r = set(a) - {v}
            r.update(set(b) - {-v})
            if any(-v in r for v in r):
                continue
            yield tuple(sorted(r))

def min_resolution_nodes(formula):
    start = frozenset(formula)
    if () in start:
        return 0
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        state, depth = queue.popleft()
        for a, b in itertools.combinations(state, 2):
            for c in resolve(a, b):
                if c in state:
                    continue
                if c == ():
                    return depth + 1
                nxt = state | {c}
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, depth + 1))
    raise ValueError('no resolution proof, as expected only on SAT')

def run():
    records = []
    checks = 0
    for mask in range(256):
        f = canonical(c for i, c in enumerate(CLAUSES) if mask & (1 << i))
        a, b = enc_a(f), enc_b(f)
        assert parse_a(a) == parse_b(b) == f
        assert len(b) == 3 + 2 * len(a)
        checks += 3
        satisfiable = sat(f)
        w = None if satisfiable else min_resolution_nodes(f)
        records.append({'mask': mask, 'a': len(a), 'b': len(b), 'sat': satisfiable, 'w': w})
    for n in range(max(r['a'] for r in records) + 1):
        u = max((r['w'] for r in records if r['w'] is not None and r['a'] <= n), default=0)
        v = max((r['w'] for r in records if r['w'] is not None and r['b'] <= 3 + 2*n), default=0)
        assert u == v
        checks += 1
    malformed_a = ('', 'CNF2|1,3|', 'CNF2|1;1|', 'CNF2|1,-1|', 'CNF2|1;|', 'cnf2||')
    malformed_b = ('', 'H2:garbage', 'H2:0', 'H2:' + enc_a(()).encode().hex().upper(), 'H2:ff')
    for x in malformed_a:
        try:
            parse_a(x)
            raise AssertionError('accepted malformed source')
        except ValueError:
            checks += 1
    for x in malformed_b:
        try:
            parse_b(x)
            raise AssertionError('accepted malformed recoding')
        except ValueError:
            checks += 1
    for f in [(), ((1,),), ((-1,), (1,)), ((1,), (-1,), (2,))]:
        assert sat(parse_a(enc_a(f))) == sat(parse_b(enc_b(f)))
        checks += 1
    for k in range(4):
        nk = 2 ** (10 ** k)
        mk = nk * nk
        prev_delay_exp = (2 ** (10 ** (k - 1))) ** 4 if k else 0
        assert prev_delay_exp < nk < nk**4 == mk * mk
        checks += 1
    return {'name': 'LSPV1-391-syntactic-encoding-finite-controls',
            'domain': 'all 256 source subsets of eight width<=2 non-tautological clauses on two variables',
            'counts': {'sources': len(records), 'sat': sum(r['sat'] for r in records),
                       'unsat': sum(not r['sat'] for r in records),
                       'max_resolution_paid_nodes': max((r['w'] for r in records if r['w'] is not None), default=0),
                       'checks': checks, 'malformed_rejected': len(malformed_a) + len(malformed_b)},
            'records': records,
            'note': 'Resolution node optima are for finite toy source grammar only; B1/B2/B3 asymptotics not tested.'}

if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, separators=(',', ':')))
