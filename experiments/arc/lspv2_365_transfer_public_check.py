#!/usr/bin/env python3
"""Replay strict Resolution outputs in the full LSPV2-365 archive dataset.

Usage: python3 public_check.py results.json
This does not validate the input mixed calculus. Use the full independent
JavaScript verifier in the archive for mixed rules and both-label controls.
"""
import argparse
import json
from pathlib import Path


def require(ok, text):
    if not ok:
        raise ValueError(text)


def clause(value, n):
    require(isinstance(value, list), 'clause must be an array')
    require(all(type(x) is int and x and abs(x) <= n for x in value), 'literal range')
    result = set(value)
    require(len(result) == len(value) and all(-x not in result for x in result), 'noncanonical clause')
    return result


def replay(case):
    source, compiled = case['input'], case['compiled']
    n = source['n']
    require(type(n) is int and n >= 0, 'variable count')
    axioms = [clause(c, n) for c in source['cnf']]
    rows, paid = [], 0
    for i, record in enumerate(compiled['strict']):
        c = clause(record['clause'], n)
        if record['op'] == 'src':
            j = record['source']
            require(type(j) is int and 0 <= j < len(axioms), 'source index')
            require(c == axioms[j], 'source authentication')
        else:
            require(record['op'] == 'res', 'strict proof rule')
            parents = record['parents']
            require(len(parents) == 2 and all(type(j) is int and 0 <= j < i for j in parents), 'acyclic parents')
            p = record['pivot']
            require(type(p) is int and 1 <= p <= n, 'pivot range')
            a, b = (rows[j] for j in parents)
            if p not in a:
                a, b = b, a
            require(p in a and -p in b, 'complementary pivot')
            require(c == (a - {p}) | (b - {-p}), 'exact resolvent')
            paid += 1
        rows.append(c)
    require(rows and not rows[-1], 'empty conclusion')
    m, q, b, d = len(axioms), compiled['q'], len(compiled['B']), compiled['d']
    require(all(type(x) is int and x >= 0 for x in (q, b, d)), 'parameter syntax')
    bound = 2**b * (m + q * 2**(d + 1) + 1) - 1
    require(bound == compiled['bound'] and paid == compiled['resolution_cost'] and paid <= bound, 'cost bound')
    return {'name': source['name'], 'strict_resolution_nodes': paid, 'Q': bound}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dataset', type=Path)
    args = parser.parse_args()
    data = json.loads(args.dataset.read_text())
    output = [replay(c) for c in data['results']]
    print(json.dumps({'status': 'PASS', 'fixtures': len(output), 'records': output,
                      'scope': 'strict Resolution outputs only; full mixed verifier is separate'}, indent=2))


if __name__ == '__main__':
    main()
