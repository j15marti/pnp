#!/usr/bin/env python3
"""Best exponent c*(d) over all op strings of bounded length, for a list of d.

Usage: python curve.py --ops STDB --maxlen 14 --d 0 0.25 0.5 --out curve.jsonl
Each invocation should stay under ~30 s; split the d list across calls.
"""
import argparse
import json
import time

from atp import best_c, build, feasible
from search import enumerate_strings


def best_for(d, strings, start):
    best, best_s = start, None
    for s in strings:
        L = build(s, d)
        if not feasible(L, best + 1e-6):
            continue
        c = best_c(s, d, lo=best, hi=2.2)
        if c is not None and c > best + 1e-9:
            best, best_s = c, s
    return best, best_s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ops', required=True)
    ap.add_argument('--maxlen', type=int, required=True)
    ap.add_argument('--maxdepth', type=int, default=8)
    ap.add_argument('--d', type=float, nargs='+', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    strings = enumerate_strings(a.maxlen, a.ops, a.maxdepth)
    for d in a.d:
        t0 = time.time()
        best, s = best_for(d, strings, start=0.5)
        rec = {'ops': a.ops, 'maxlen': a.maxlen, 'd': d, 'n_strings': len(strings),
               'best_c': round(best, 6), 'best_string': s,
               'collapse_bound_2cos(pi/7)-d': round(1.8019377358 - d, 6),
               'potential_barrier_max(1,2-d)': round(max(1.0, 2 - d), 6),
               'seconds': round(time.time() - t0, 2)}
        with open(a.out, 'a') as fh:
            fh.write(json.dumps(rec) + '\n')
        print(json.dumps(rec))


if __name__ == '__main__':
    main()
