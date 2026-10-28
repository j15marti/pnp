#!/usr/bin/env python3
"""Exhaustive annotation search for CLAUDE TPORT-0001.

Enumerates every valid op string over {S,T,D,B} (see atp.py) up to a length
and block-depth bound, and records the best exponent c for a given portfolio
width coefficient d.  Strings are processed in chunks so that each invocation
stays short; results append to a JSON-lines file.

Usage:
  python search.py --d 1 --maxlen 14 --ops STDB --chunk 0 --nchunks 1 \
                   --out results.jsonl
"""

import argparse
import json
import time

from atp import best_c, build, feasible, ProofError

EXISTS = 1


def enumerate_strings(maxlen, ops, maxdepth):
    """Yield complete op strings (ending at a single E-residual)."""
    out = []

    def rec(s, line, speedups):
        # line: list of (q, kind)
        if len(line) == 1 and line[0][1] == 'res' and speedups > 0:
            out.append(s)
            return
        if len(s) >= maxlen:
            return
        last = line[-1]
        q, kind = last
        if 'S' in ops and len(line) + 1 <= maxdepth:
            rec(s + 'S', line[:-1] + [(q, 'big'), (-q, 'log')], speedups + 1)
        if 'T' in ops and len(line) + 2 <= maxdepth:
            rec(s + 'T', line + [(-q, 'big'), (q, 'log')], speedups + 1)
        if 'K' in ops:
            pos = None
            for i in range(len(line) - 2, 0, -1):
                if line[i][1] == 'res':
                    pos = i
                    break
            if pos is not None:
                A, R = line[pos - 1], line[pos]
                if pos + 2 < len(line):
                    Y = line[pos + 2]
                    new = line[:pos - 1] + [(A[0], 'big'), Y] + line[pos + 3:]
                else:
                    new = line[:pos - 1] + [(A[0], 'big'), (R[0], 'res')]
                rec(s + 'K', new, speedups)
        if kind != 'res' and 'D' in ops:
            rec(s + 'D', line[:-1] + [(q, 'res')], speedups)
        if kind == 'res' and len(line) > 1 and 'B' in ops:
            rec(s + 'B', line[:-1], speedups)

    rec('', [(EXISTS, 'res')], 0)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--d', type=float, required=True)
    ap.add_argument('--maxlen', type=int, required=True)
    ap.add_argument('--maxdepth', type=int, default=8)
    ap.add_argument('--ops', default='SDB')
    ap.add_argument('--chunk', type=int, default=0)
    ap.add_argument('--nchunks', type=int, default=1)
    ap.add_argument('--threshold', type=float, default=1.0)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    strings = enumerate_strings(args.maxlen, args.ops, args.maxdepth)
    mine = strings[args.chunk::args.nchunks]
    t0 = time.time()
    best, best_s, n_above = args.threshold, None, 0
    for s in mine:
        L = build(s, args.d)
        if not feasible(L, best + 1e-6):
            continue
        n_above += 1
        c = best_c(s, args.d, lo=best)
        if c is not None and c > best + 1e-9:
            best, best_s = c, s
    rec = {'d': args.d, 'maxlen': args.maxlen, 'maxdepth': args.maxdepth,
           'ops': args.ops, 'chunk': args.chunk, 'nchunks': args.nchunks,
           'n_strings_total': len(strings), 'n_checked': len(mine),
           'threshold': args.threshold, 'n_strictly_above_threshold': n_above,
           'best_c': best if best_s else None, 'best_string': best_s,
           'seconds': round(time.time() - t0, 2)}
    with open(args.out, 'a') as fh:
        fh.write(json.dumps(rec) + '\n')
    print(json.dumps(rec))


if __name__ == '__main__':
    main()
