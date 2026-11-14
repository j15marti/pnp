#!/usr/bin/env python3
"""TMR-4/027. Finite exact audit of affine-sketch kernel MCSP/Gap-MCSP collisions.
No network/API calls. Standard Python 3.12, no dependencies. Outputs JSON on stdout.
All arithmetic uses actual N=2**n truth-table bits, not succinct formulas.
"""
import json
import itertools
import random
from math import comb, log2


def parity(x): return x.bit_count() & 1

def coordinate_truth(n, j):
    return sum(((v >> j) & 1) << v for v in range(1 << n))


def circuits_up_to(n, s):
    N = 1 << n
    allbits = (1 << N) - 1
    wires = [0, allbits] + [coordinate_truth(n, j) for j in range(n)]
    found = set(wires)
    frontier = [tuple()]
    for _ in range(s):
        nxt = set()
        for added in frontier:
            available = wires + list(added)
            for a in available:
                nxt.add(added + (allbits ^ a,))
                for b in available:
                    nxt.add(added + (a & b,))
                    nxt.add(added + (a | b,))
        frontier = list(nxt)
        for gates in frontier: found.add(gates[-1])
    return found


def rank(rows):
    basis = {}
    for row in rows:
        z = row
        while z:
            j = z.bit_length() - 1
            if j in basis: z ^= basis[j]
            else:
                basis[j] = z
                break
    return len(basis)


def linear_image(x, rows):
    return sum(parity(x & mask) << j for j, mask in enumerate(rows))


def exact_min_distance(x, yes):
    return min((x ^ g).bit_count() for g in yes)


def hamming_volume(N, radius):
    return sum(comb(N, j) for j in range(radius + 1))


def description_bound(n, s):
    return (s + 1) * (n + s + 2) * (3 * (n + s + 2)**2)**s


def main():
    results = {'title': 'TMR4-AFFKERNEL27', 'status': 'COMPUTATIONAL', 'failures': 0,
               'basis': 'fanin-two AND OR; unary NOT; free 0 and 1 input wires; projections',
               'scope': 'fixed GF2-linear maps of complete source truth-table bits; no adaptive source-dependent matrices'}
    tests = 0
    small = []
    for n, max_s in [(2, 2), (3, 2), (4, 1)]:
        N = 1 << n
        allbits = 1 << N
        previous = set()
        for s in range(max_s + 1):
            C = circuits_up_to(n, s)
            assert previous.issubset(C)
            previous = C
            D = description_bound(n, s)
            assert len(C) <= D
            # Entire truth-table language with both YES and NO labels.
            num_yes = sum(x in C for x in range(allbits))
            assert num_yes == len(C)
            assert 0 in C and (allbits - 1) in C
            tests += allbits
            small.append(dict(n=n, N=N, s=s, yes=len(C), no=allbits-len(C),
                              description_bound=D))
    results['small_full_classifications'] = small

    n = 4; N = 1 << n
    C0, C1 = circuits_up_to(n, 0), circuits_up_to(n, 1)
    rng = random.Random(202611141136)
    # Every listed map is full row rank, maps 16-bit source table to 8-bit output table.
    rows_list = [list(1 << j for j in range(8))]
    for _ in range(5):
        rows = []
        while len(rows) < 8:
            z = rng.randrange(1, 1 << N)
            if rank(rows + [z]) == len(rows)+1: rows.append(z)
        rows_list.append(rows)
    kernel_cases = []
    for idx, rows in enumerate(rows_list):
        assert rank(rows) == 8
        ker = [x for x in range(1 << N) if linear_image(x, rows) == 0]
        assert len(ker) == 1 << (N - 8)
        for s, yes in [(0,C0), (1,C1)]:
            hard = [x for x in ker if x not in yes]
            assert hard, (idx,s)
            witness = hard[0]
            assert linear_image(witness, rows) == linear_image(0, rows) == 0
            # even after a deterministic nonlinear decoder the two sources collide.
            for rot in (0,1,3):
                def post(z): return (((z ^ 0b10110110) << rot) | ((z ^ 0b10110110) >> (8-rot))) & 255 if rot else z ^ 0b10110110
                assert post(linear_image(witness, rows)) == post(linear_image(0, rows))
                tests += 1
            far = [x for x in ker if exact_min_distance(x, yes) >= 4]
            kernel_cases.append(dict(map_id=idx, s=s, rank=8, kernel_size=len(ker),
                                     yes_count=len(yes), hard_count=len(hard),
                                     hard_witness=f'{witness:04x}', far_eta_quarter_count=len(far),
                                     far_witness=f'{far[0]:04x}' if far else None))
            tests += len(ker)
    results['n4_rank8_kernel_cases'] = kernel_cases

    # All-length certified exact collision count bound: kernel cardinality > D.
    # Robust promise collision: |kernel| > D * V(N,ceil(eta*N)-1).
    bounds = []
    for n, s, r, eta_num, eta_den in [(4,0,8,1,4), (6,0,8,1,4),
                                       (8,2,16,1,8), (8,8,64,1,8),
                                       (8,8,32,1,4)]:
        N = 1 << n
        D = description_bound(n,s)
        radius = (N * eta_num + eta_den - 1)//eta_den - 1
        V = hamming_volume(N, radius)
        exact = (1 << (N-r)) > D
        robust = (1 << (N-r)) > D * V
        bounds.append(dict(n=n,N=N,s=s,r=r,eta=f'{eta_num}/{eta_den}',
                           log2_kernel=N-r, log2_D_approx=round(log2(D),6),
                           radius=radius,log2_DV_approx=round(log2(D)+log2(V),6),
                           certified_exact=exact,certified_robust=robust))
        assert exact == (N-r > log2(D)+1e-9)
        assert robust == (N-r > log2(D)+log2(V)+1e-9)
        tests += 2
    results['asymptotic_fixture_bounds'] = bounds
    # One 64-bit direct independent witness under an eight-bit coordinate sketch.
    n = 6; N = 64; yes = circuits_up_to(n,0)
    assert len(yes) == n+2
    assert (1 << (N-8)) > description_bound(n,0)*hamming_volume(N,15)
    rng = random.Random(6042026)
    trials = 0
    while True:
        trials += 1
        x = rng.getrandbits(N) & ~255
        if exact_min_distance(x,yes) >= 16:
            break
        assert trials < 100000
    assert x & 255 == 0
    results['n6_eta_quarter_witness'] = {'hex':f'{x:016x}', 'min_distance':exact_min_distance(x,yes),
                                         'trials':trials, 'rank':8,
                                         'query': 'first 8 table bits',
                                         'source_zero_and_witness_same_sketch':True}
    tests += len(yes) + trials
    results['checks'] = tests
    print(json.dumps(results,sort_keys=True,indent=2))

if __name__ == '__main__': main()
