#!/usr/bin/env python3
"""Exact restricted single-facet retention/peak firewall, LSPV-4/589.
An interval is live at every integer paid-step epoch between first and last use.
The background counts only OTHER retained values, never the tested facet.
"""
from itertools import combinations, product
import json


def intervals(uses, cuts):
    starts = [0] + [i + 1 for i in cuts]
    ends = list(cuts) + [len(uses) - 1]
    return [(uses[i], uses[j]) for i, j in zip(starts, ends)]


def score(uses, cuts, background):
    iv = intervals(uses, cuts)
    area = sum(b - a + 1 for a, b in iv)
    peak = max(background[t] + sum(a <= t <= b for a, b in iv)
               for t in range(len(background)))
    return peak, area, iv


def brute(uses, k, background):
    return min((score(uses, c, background)[0], c)
               for c in combinations(range(len(uses) - 1), k - 1))


def threshold_min_views(uses, background, H):
    if any(background[t] >= H for t in uses):
        return None
    forced = tuple(i for i, (a, b) in enumerate(zip(uses, uses[1:]))
                   if any(background[t] >= H for t in range(a + 1, b)))
    return 1 + len(forced), forced


def formula(uses, k, background):
    for H in range(max(background), max(background) + 2):
        z = threshold_min_views(uses, background, H)
        if z is not None and z[0] <= k:
            cuts = z[1] + tuple(i for i in range(len(uses) - 1)
                                 if i not in z[1])[:k - z[0]]
            return H, tuple(sorted(cuts))
    raise AssertionError('unreachable')


def two_facet_example():
    A, B = (1, 4, 10), (7, 12)
    bg = [0] * 13
    bg[10] = 5
    opts = []
    for a in ((), (0,), (1,)):
        for b in ((), (0,)):
            if 2 + len(a) + len(b) != 3:
                continue
            ivA, ivB = intervals(A, a), intervals(B, b)
            p = max(bg[t] + sum(lo <= t <= hi for lo, hi in ivA + ivB)
                    for t in range(13))
            area = sum(hi-lo+1 for lo, hi in ivA+ivB)
            opts.append(dict(cuts_A=list(a), cuts_B=list(b), peak=p,
                             area=area, A=ivA, B=ivB))
    assert len(opts) == 3
    amin = min(opts, key=lambda x: x['area'])
    pmin = min(opts, key=lambda x: x['peak'])
    assert (amin['area'], amin['peak']) == (11, 7)
    assert (pmin['area'], pmin['peak']) == (12, 6)
    return {'background_at_10':5,'views_K':3,'choices':opts,
            'area_minimum':amin, 'peak_minimum':pmin}


def main():
    cases = 0
    for T in range(2, 8):
        for m in range(1, min(T, 4) + 1):
            for uses in combinations(range(T), m):
                for bg in product(range(3), repeat=T):
                    for k in range(1, m + 1):
                        H, cuts = formula(uses, k, bg)
                        opt, _ = brute(uses, k, bg)
                        assert H == opt, (uses, k, bg, H, opt)
                        assert score(uses, cuts, bg)[0] == H
                        cases += 1
    out={'status':'PASS', 'exhaustive_cases':cases, 'T_range':[2,7],
         'background_alphabet':[0,1,2], 'max_uses':4,
         'two_facet_counterexample':two_facet_example(),
         'model':'read-only sources; fixed paid epochs; free independently reemittable typed facet; fixed background; no physical scratch or raw evidence bytes'}
    print(json.dumps(out,indent=2))

if __name__ == '__main__':
    main()
