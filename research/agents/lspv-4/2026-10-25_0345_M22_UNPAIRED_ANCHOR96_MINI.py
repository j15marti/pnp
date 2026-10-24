#!/usr/bin/env python3
"""M22-UNPAIRED-ANCHOR96: standard-library exact source/grammar audit.

Run in j15marti/pnp repository root:
python research/agents/lspv-4/2026-10-25_0345_M22_UNPAIRED_ANCHOR96_MINI.py

The 198-variable UNSAT label is imported from Döcker's Proposition 1
and the existing DOECKER-CORE-CERT61 proof audit, not brute forced.
"""
import ast
import itertools
import json
from collections import Counter
from pathlib import Path

P = ((1,2,3), (1,4,5), (2,4,6), (3,5,6))
Q = ((1,2,4), (1,3,6), (2,3,5), (4,5,6))
H = tuple(P) + tuple(tuple(-v for v in e) for e in P)
Y = tuple(P) + tuple(tuple(-v for v in e) for e in Q)
SOURCE = Path('research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt')

def shifted(formula, offset):
    return [tuple(v + offset if v > 0 else v - offset for v in c)
            for c in formula]

def grammar(formula, k):
    seen = set()
    cnt = Counter()
    for c in formula:
        assert len(c) == 3 and len({abs(v) for v in c}) == 3
        assert all((v > 0) == (c[0] > 0) for v in c)
        assert all(1 <= abs(v) <= k for v in c)
        key = (c[0] > 0, tuple(sorted(abs(v) for v in c)))
        assert key not in seen
        seen.add(key)
        cnt.update(c)
    assert 3 * len(formula) == 4 * k
    assert all(cnt[v] == cnt[-v] == 2 for v in range(1, k + 1))
    unpaired = sum(
        ((c[0] < 0, tuple(sorted(abs(v) for v in c))) not in seen)
        for c in formula
    )
    w = k.bit_length()    # equals ceil(log2(k+1))
    N = 3 * w + 2 + 3 * len(formula) * (w + 1)
    return {'k': k, 'm': len(formula), 'N': N, 'w': w,
            'unpaired': unpaired}

def brute_models(formula, k):
    solutions = []
    for a in itertools.product((0,1), repeat=k):
        if all(any(bool(a[abs(x)-1]) == (x > 0) for x in c)
               for c in formula):
            solutions.append(''.join(str(z) for z in a))
    return solutions

def source_U():
    if not SOURCE.exists():
        return None
    lines = [v for v in SOURCE.read_text(encoding='utf-8').splitlines()
             if v.strip() and not v.lstrip().startswith('#')]
    U = tuple(tuple(map(int, c)) for c in ast.literal_eval('\n'.join(lines)))
    assert grammar(U, 198)['unpaired'] == 264
    return U

def matched(p, unsat, U):
    assert p >= 0
    out = []
    offset = 0
    if unsat:
        out.extend(U)
        offset = 198
    for _ in range(p if unsat else p + 33):
        out.extend(shifted(H, offset))
        offset += 6
    out.extend(shifted(Y, offset))
    offset += 6
    return grammar(out, offset)

def main():
    h = grammar(H, 6)
    y = grammar(Y, 6)
    hm = brute_models(H, 6)
    ym = brute_models(Y, 6)
    assert h['unpaired'] == 0 and y['unpaired'] == 8
    assert len(hm) == 18 and len(ym) == 20 and '111000' in ym

    hy = tuple(H) + tuple(shifted(Y, 6))
    assert grammar(hy, 12)['unpaired'] == 8
    assert len(brute_models(hy, 12)) == 360

    U = source_U()
    rows = []
    if U is not None:
        for p in (0, 1, 8, 64, 512):
            yes = matched(p, False, U)
            no = matched(p, True, U)
            assert yes['N'] == no['N'] and yes['k'] == no['k']
            assert yes['unpaired'] == 8 and no['unpaired'] == 272
            assert yes['k'] == 6 * p + 204 and yes['m'] == 8 * p + 272
            rows.append({'p': p, 'k': yes['k'], 'm': yes['m'],
                         'N': yes['N'], 'yes_unpaired': 8,
                         'no_unpaired': 272})

    print(json.dumps({
        'status': 'COMPUTATIONAL: finite exact syntax checks; UNSAT source imported',
        'source_present': U is not None,
        'H_models': len(hm),
        'Y_models': len(ym),
        'H_union_Y_models': 360,
        'Y_witness_111000': True,
        'rows': rows,
        'failed_checks': 0
    }, indent=2))

if __name__ == '__main__':
    main()
