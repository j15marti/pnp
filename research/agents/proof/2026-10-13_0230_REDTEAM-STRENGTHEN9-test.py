#!/usr/bin/env python3
"""Exact ordered-image decoder audit. Each stage has a 24-second alarm.

From repository root:
  python research/agents/proof/2026-10-13_0230_REDTEAM-STRENGTHEN9-test.py --stage 0 --out results.json
Requires the existing experiments/review/universal22.py compiler. No SAT
oracle is used for image recognition. Small source truth tables only check
the recovered source; they do not decide arbitrary compiled inputs.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import signal
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'experiments/review'))
import universal22 as u


def encode(cnf):
    return json.dumps(cnf, separators=(',', ':'), ensure_ascii=True).encode('ascii')


def decode_image(raw, ledger=None):
    """Return one source preimage, or None. Exact, order-preserving bytes.

    The bit-time implementation has polynomial cost. This Python prototype
    materializes arrays and regenerated outputs, so it is NOT a half-space
    implementation. It does not recognize the renaming/permutation orbit.
    """
    if ledger is None:
        ledger = Counter()
    ledger['input_bytes'] += len(raw)
    try:
        y = json.loads(raw)
    except (ValueError, UnicodeError, RecursionError):
        return None
    if not isinstance(y, list) or not y or any(
        not isinstance(c, list) or len(c) != 3 or any(
            type(l) is not int or l == 0 or abs(l) > 3 * len(y) for l in c
        ) for c in y
    ):
        return None
    if encode(y) != raw or len(y) % 12:
        return None
    b = len(y) // 12
    if b % 2:
        return None
    R = 3 * b // 2
    clone_map = {}
    start = 1
    group = 1
    for j in range(R):
        a, v, port = y[b+j]
        z = j+1
        ledger['cycle_records'] += 1
        if a != -z or port != R + 15*(j//3) + u.PORTS[j%3]:
            return None
        clone_map[z] = group
        if v == start:
            if z-start+1 < 2:
                return None
            start = z+1
            group += 1
        elif v != z+1 or z == R:
            return None
    if start != R+1:
        return None
    if any(abs(l) > R for c in y[:b] for l in c):
        return None
    bal = [tuple((1 if l > 0 else -1)*clone_map[abs(l)] for l in c) for c in y[:b]]
    # The original source is a prefix. Enumerate all possible boundaries;
    # no uniqueness assumption and no omitted failed candidates.
    for m in range(1, b+1):
        ledger['prefix_attempts'] += 1
        source = bal[:m]
        try:
            u.check_proper(source)
            comp = u.compile22(source)
        except (ValueError, AssertionError):
            continue
        rebuilt = encode(comp.clauses)
        ledger['regenerations'] += 1
        ledger['regenerated_bytes'] += len(rebuilt)
        ledger['comparison_byte_upper_bound'] += max(len(rebuilt), len(raw))
        if rebuilt == raw:
            return source
    return None


def source_sat(source):
    n = u.check_proper(source)
    return any(u.eval_cnf(source, dict(enumerate(bits, 1)))
               for bits in itertools.product((0,1), repeat=n))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', type=int, choices=range(5), required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('24-second stage budget')))
    signal.alarm(24)
    started = time.monotonic()
    checks = Counter()
    ledger = Counter()
    rows = []

    def check(ok, label):
        checks[label] += 1
        if not ok:
            raise AssertionError(label)

    pool = [tuple((i+1)*s for i,s in enumerate(signs)) for signs in itertools.product((-1,1), repeat=3)]
    if args.stage < 4:
        lo, hi = 1+64*args.stage, min(256, 1+64*(args.stage+1))
        cases = [(f'cube_subset_{mask}', [c for i,c in enumerate(pool) if mask & (1<<i)]) for mask in range(lo,hi)]
    else:
        cases = [('Horn', [(1,-2,-3),(-1,2,-3),(-1,-2,3)]),
                 ('dual_Horn', [(-1,2,3),(1,-2,3),(1,2,-3)]),
                 ('Krom', u.properize23([(1,2),(-1,2),(-1,-2)])[0]),
                 ('independent', [(1,2,3),(4,5,6)]),
                 ('affine_sat', [pool[i] for i in (0,3,5,6)]),
                 ('affine_unsat', pool)]
        base = [(1,2,3),(-1,2,-3)]
        cases += [('source_reordered', list(reversed(base))),
                  ('source_renamed', [tuple((4-abs(l))*(1 if l>0 else -1) for l in c) for c in base]),
                  ('source_complemented', [tuple(-l for l in c) for c in base])]
    for name, source in cases:
        comp = u.compile22(source)
        raw = encode(comp.clauses)
        got = decode_image(raw, ledger)
        check(got is not None, 'image_accepted')
        check(encode(u.compile22(got).clauses) == raw, 'exact_roundtrip')
        check(source_sat(got) == source_sat(source), 'source_truth')
        if name.startswith('cube_subset_') or name == 'affine_unsat':
            check(decode_image(encode(got), ledger) is None, 'decoded_child_leaves_image')
        check(len(encode(got)) <= len(raw), 'preimage_size')
        for bits in itertools.product((0,1), repeat=comp.source_n):
            vals = dict(enumerate(bits, 1))
            check(u.eval_cnf(comp.clauses, u.lift(comp, vals)) == u.eval_cnf(source, vals), 'zero_lift')
        check(decode_image(raw+b' ', ledger) is None, 'noncanonical_bytes_rejected')
        bad = [list(c) for c in comp.clauses]
        b = len(bad)//12
        bad[b][0] *= -1
        check(decode_image(encode(bad), ledger) is None, 'broken_cycle_rejected')
        # Reversing literal order of one implication preserves the CNF
        # semantics, but destroys this canonical ordered image.
        bad = [list(c) for c in comp.clauses]
        bad[b].reverse()
        check(decode_image(encode(bad), ledger) is None, 'semantic_same_off_image')
        rows.append(dict(case=name, source_clauses=len(source), target_clauses=len(comp.clauses),
                         source_bits=8*len(encode(source)), target_bits=8*len(raw),
                         decoded_clauses=len(got), sat=source_sat(source)))
    if args.stage == 4:
        for raw in (b'[]', b'null', b'[[true,2,3]]', b'[[1.0,2,3]]', b'[[0,2,3]]',
                    b'[[999999999999999999999999,2,3]]', b'[[1,1,2]]', b'[[1,2]]', b'garbage'):
            check(decode_image(raw, ledger) is None, 'malformed_rejected')
        # Infinite off-image YES family: disjoint clauses; counts never match
        # the image, yet all-ones satisfies it for every k.
        for k in range(1,11):
            source = [tuple(range(3*j+1,3*j+4)) for j in range(k)]
            check(decode_image(encode(source), ledger) is None and
                  u.eval_cnf(source, {i:1 for i in range(1,3*k+1)}), 'SAT_is_not_total_image_language')
        for a in range(1,5):
            for q in range(1,5):
                for d in range(1,17):
                    check(max(a,q*d) >= d, 'exponent_retained')
        c = Fraction(6,5)
        dc = ((c+2)/(c*c)-c)/2
        check(dc == Fraction(23,45) and dc-Fraction(1,2)==Fraction(1,90), 'endpoint_slack')
    result = dict(run_id='REDTEAM-STRENGTHEN9', status='COMPUTATIONAL', stage=args.stage,
                  all_checks_passed=True, checks=dict(checks), assertions=sum(checks.values()),
                  ledger=dict(ledger), cases=rows, elapsed_seconds=time.monotonic()-started,
                  seed=None, compiler_sha256=hashlib.sha256(Path(u.__file__).read_bytes()).hexdigest(),
                  code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  limitations=['Ordered compiler image only; no orbit recognizer.',
                    'Materialized polynomial space; no FLMV-space or PRE-A bound.',
                    'Ledger is structural work, not complete Python bit-time accounting.',
                    'Finite target truth checked via lift, not exhaustive target SAT.'])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    signal.alarm(0)
    print(json.dumps({k:result[k] for k in ('stage','assertions','elapsed_seconds','all_checks_passed')}))


if __name__ == '__main__':
    main()
