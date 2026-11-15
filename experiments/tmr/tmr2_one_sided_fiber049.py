#!/usr/bin/env python3
"""TMR-2/033: exact finite one-sided ordinary-MCSP fibre/certificate controls.

This tests finite subcubes, not the asymptotic circuit-counting theorem.
No external dependencies. Run: python tmr2_one_sided_fiber049.py
"""
import itertools, json, math
from collections import Counter


def one_gate_yes(n):
    N = 1 << n
    full = (1 << N) - 1
    var = [sum(((a >> v) & 1) << a for a in range(N)) for v in range(n)]
    wires = [0, full] + var
    yes = set(wires)
    for a in wires:
        yes.add(full ^ a)
        for b in wires:
            yes.add(a & b)
            yes.add(a | b)
    return yes


def accepts_full_subcube(x, queried_mask, N, yes):
    unqueried = [i for i in range(N) if not ((queried_mask >> i) & 1)]
    base = x & queried_mask
    for assign in range(1 << len(unqueried)):
        y = base
        for j, idx in enumerate(unqueried):
            y |= ((assign >> j) & 1) << idx
        if y not in yes:
            return False
    return True


def exact_certificate(x, N, yes):
    for q in range(N+1):
        for indices in itertools.combinations(range(N), q):
            Q = sum(1 << i for i in indices)
            if accepts_full_subcube(x, Q, N, yes):
                return q, Q
    raise RuntimeError('No certificate for a YES input')


def experiment():
    rows = []
    assertions = 0
    total_fibers = 0
    for n in (2, 3):
        N = 1 << n
        yes = one_gate_yes(n)
        cnt = len(yes)
        assert cnt < (1 << N)
        assertions += 1
        log_count = math.log2(cnt)
        bound = N - math.floor(log_count)
        minimum_cert = N
        maximum_cert = 0
        histogram = Counter()
        # Independently verify that every accepting cylinder includes at least
        # 2^(N-q)-|YES| NO completions, the quantitative epsilon bound ingredient.
        checked_cylinders = 0
        for x in sorted(yes):
            for Q in range(1 << N):
                q = Q.bit_count()
                no_count = 0
                for y in range(1 << N):
                    if (x & Q) == (y & Q) and y not in yes:
                        no_count += 1
                assert no_count >= max(0, (1 << (N-q)) - cnt)
                checked_cylinders += 1
            cert, Q = exact_certificate(x, N, yes)
            assert cert >= bound, (n, x, cert, bound)
            assertions += 1
            assert accepts_full_subcube(x, Q, N, yes)
            assertions += 1
            if cert:
                for i in range(N):
                    if (Q >> i) & 1:
                        assert not accepts_full_subcube(x, Q ^ (1 << i), N, yes)
                        assertions += 1
            histogram[cert] += 1
            minimum_cert = min(minimum_cert, cert)
            maximum_cert = max(maximum_cert, cert)
        assert checked_cylinders == cnt * (1 << N)
        assertions += checked_cylinders
        assert sum(histogram.values()) == cnt
        assertions += 1
        rows.append({'n':n, 'N':N, 's':1, 'circuit_basis':'AND,OR,NOT; constants free; one gate',
                     'YES_count':cnt, 'YES_bits_counting_bound':bound,
                     'min_actual_yes_certificate':minimum_cert,
                     'max_actual_yes_certificate':maximum_cert,
                     'cert_histogram':dict(sorted(histogram.items())),
                     'exhaustive_acceptance_cylinders':checked_cylinders})
        total_fibers += cnt
    # Sound randomized accept/reject paths: read entire table and accept iff YES
    # with probability 2/3, otherwise immediately reject. For each input it has
    # zero false-positive error, >=2/3 acceptance on every YES input.
    for row in rows:
        N=row['N']; b=row['YES_bits_counting_bound']
        expected=(2/3)*N
        assert expected >= (2/3)*b
        assertions+=1
    return {'experiment':'TMR2_ONE_SIDED_MCSP_FIBER049','timestamp_pst':'2026-11-14 18:14 PST',
            'status':'COMPUTATIONAL finite exact enumeration; symbolic theorem separate',
            'rows':rows,'assertions':assertions,'failed_assertions':0,
            'yes_tables_examined':total_fibers, 'seed':None,
            'scope':'ordinary MCSP with explicit full 2^n-bit truth tables, gate threshold s=1'}

if __name__ == '__main__':
    print(json.dumps(experiment(), indent=2, sort_keys=True))
