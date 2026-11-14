"""APPROXPAD25: finite checks for normalized-distance dummy padding.
Circuit basis: AND, OR, NOT; free input wires and constants; max 2 gates.
"""
import json
from pathlib import Path

def cls(n):
    N = 1 << n
    mask = (1 << N) - 1
    wires = tuple(sum(((i >> k) & 1) << i for i in range(N)) for k in range(n)) + (0, mask)
    programs = [wires]
    classes = []
    seen = set(wires)
    for depth in range(3):
        classes.append(set(seen))
        newer = []
        for w in programs:
            for a in w:
                newer.append(w + (mask ^ a,))
                seen.add(mask ^ a)
            for a in w:
                for b in w:
                    for z in (a & b, a | b):
                        newer.append(w + (z,))
                        seen.add(z)
        programs = newer
    return classes

def pad(f, n):
    N = 1 << n
    return sum(((f >> (i % N)) & 1) << i for i in range(2 * N))

def check():
    cases, equations = [], 0
    for n in (2, 3):
        a, b = cls(n), cls(n + 1)
        N = 1 << n
        for s in range(3):
            near = 0
            for f in range(1 << N):
                d = min((f ^ g).bit_count() for g in a[s])
                D = min((pad(f, n) ^ h).bit_count() for h in b[s])
                assert D == 2 * d
                assert (d == 0) == (D == 0)
                near += (0 < d < N / 4)
                equations += 1
            cases.append(dict(n=n, s=s, N=N, M=2*N, YES_old=len(a[s]), YES_new=len(b[s]),
                              strings=1<<N, ordinary_NO_not_quarter_gap=near))
    assert min((1 ^ g).bit_count() for g in cls(3)[0]) == 1
    result = dict(cases=cases, normalized_distance_equations=equations,
                  single_spike_fixture='n=3,s=0,ordinary NO, distance 1/8 < 1/4',
                  failed_assertions=0, status='COMPUTATIONAL only')
    path = Path(__file__).with_name('2026-11-14_1103_TMR1_APPROXPAD025_RAW.json')
    path.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(equations=equations, cases=len(cases), failed=0)))

if __name__ == '__main__':
    check()
