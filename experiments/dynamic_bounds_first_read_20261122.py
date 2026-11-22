"""Exact finite checks for DYNAMIC-FIRST-READ-DEBIT1.

Standalone projected-source/encoding audit, not a native tape implementation.
No random choices or third-party packages. Run with Python 3.
"""
from itertools import product
from collections import defaultdict
from pathlib import Path
import hashlib
import json


def source(bits):
    q = len(bits)
    z, one = 0, 1
    xs = list(range(2, q + 3))
    ws = list(range(q + 3, 2 * q + 3))
    clauses = [(z, z, one), (xs[0], xs[0], one),
               (xs[-1], xs[-1], one)]
    for j, bit in enumerate(bits):
        clauses.append((xs[j], ws[j], z))
        clauses.append((xs[j+1], xs[j] if bit else ws[j], z))
    return 2*q + 3, clauses


def cycle(v, clauses):
    # Independent reconstruction of Discovery's pinned block map.
    top, bottom, starts = [], [], []
    for length in [2]*v + [3]*len(clauses):
        starts.append(len(top))
        top.extend('A'*length + 'CAC')
        bottom.extend('A'*length + 'CCC')
    rows = [(5*var + 1, starts[v+k] + e, starts[v+k] + e + 1)
            for k, clause in enumerate(clauses)
            for e, var in enumerate(clause)]
    return ''.join(top), ''.join(bottom), rows


def gamma(n):
    assert n > 0
    s = bin(n)[2:]
    return '0'*(len(s)-1) + s


def pack(top, bottom, rows):
    t = len(top)
    w = (t-1).bit_length()
    header = gamma(t) + top.replace('A','0').replace('C','1')
    header += bottom.replace('A','0').replace('C','1') + gamma(len(rows)+1)
    return header + ''.join(format(x, f'0{w}b') for row in rows for x in row)


def direct(v, clauses):
    return any(all(sum(x[i] for i in row) == 1 for row in clauses)
               for x in product((0,1), repeat=v))


def extension(bits, v, clauses):
    x = [0,1,0]
    for bit in bits:
        x.append(x[-1] ^ bit)
    x.extend(1-x[2+j] for j in range(len(bits)))
    assert len(x) == v
    assert all(sum(x[i] for i in row) == 1 for row in clauses)
    zz = []
    for val in x:
        zz.extend([1,val,0,1,0])
    for row in clauses:
        a,b,c = [x[i] for i in row]
        zz.extend([1,1-a,c,0,1,0])
    return zz


def check_path(top, bottom, rows, z):
    assert len(z) == len(top)
    for i, (a,b) in enumerate(zip(top,bottom)):
        pair = z[i], z[(i+1) % len(z)]
        allowed = {(0,0),(1,0),(1,1)} if a+b == 'AA' else (
            {(0,1),(1,0)} if a+b == 'CC' else {(1,0)})
        assert pair in allowed
    assert all(z[a] ^ z[b] ^ z[c] == 0 for a,b,c in rows)


def main():
    results = []
    total_images = direct_cases = fibers_checked = 0
    for q in range(1,9):
        allbits = list(product((0,1), repeat=q))
        images, labels = {}, {}
        for bits in allbits:
            v, clauses = source(bits)
            top,bottom,rows = cycle(v,clauses)
            assert len(top) == 22*q+33 and len(rows) == 6*q+9
            assert all(len(set(r)) == 3 for r in rows)
            expected = sum(bits) % 2 == 0
            if q <= 4:
                assert direct(v,clauses) == expected
                direct_cases += 1
            if expected:
                check_path(top,bottom,rows,extension(bits,v,clauses))
            images[bits] = pack(top,bottom,rows)
            labels[bits] = expected
        zero = (0,)*q
        base = images[zero]
        supports = []
        for j in range(q):
            flip = tuple(int(i == j) for i in range(q))
            support = {k for k,(a,b) in enumerate(zip(base,images[flip])) if a != b}
            assert support
            assert not any(support & other for other in supports)
            supports.append(support)
        for bits in allbits:
            for j in range(q):
                flip = tuple(b ^ (i == j) for i,b in enumerate(bits))
                assert labels[flip] != labels[bits]
                actual = {k for k,(a,b) in enumerate(zip(images[bits],images[flip])) if a != b}
                assert actual == supports[j]
        # Adaptive, read-only probe proxy. The next index depends on earlier
        # answers; physical motion is not measured. Verify conditional fibers,
        # prefix-free lengths, and no event reuse at every query checkpoint.
        if q <= 6:
            traces = {}
            for bits in allbits:
                remaining, history = set(range(q)), []
                choose_high = False
                while remaining:
                    j = max(remaining) if choose_high else min(remaining)
                    p = min(supports[j])
                    symbol = images[bits][p]
                    history.append((j,p,symbol))
                    choose_high = symbol == '1'
                    remaining.remove(j)
                traces[bits] = history
            for cutoff in range(q+1):
                for j in range(q):
                    groups = defaultdict(list)
                    for bits in allbits:
                        side = (bits[:j]+bits[j+1:], tuple(traces[bits][:cutoff]))
                        groups[side].append(bits)
                    for side, members in groups.items():
                        seen = any(event[0] == j for event in side[1])
                        assert len(members) == (1 if seen else 2)
                        assert len({b[j] for b in members}) == (1 if seen else 2)
                        codes = []
                        for bits in members:
                            event = next(e for e in traces[bits] if e[0] == j)
                            code = '' if seen else event[2]
                            codes.append(code)
                            # Reconstruct event position from other coordinates
                            # and the common transcript; it is equal in the pair.
                        if not seen:
                            assert {c for c in codes} == {'0','1'}
                            assert len({next(e for e in traces[b] if e[0] == j)[1]
                                        for b in members}) == 1
                        fibers_checked += 1
        total_images += len(allbits)
        results.append(dict(q=q, images=len(allbits), SAT=len(allbits)//2,
                            UNSAT=len(allbits)//2, packed_length=len(base),
                            sensitive_regions=[sorted(s) for s in supports]))
    data = dict(status='COMPUTATIONAL', images=total_images,
                direct_source_cases=direct_cases, conditional_fibers=fibers_checked,
                native_tape=False, adjacent_compiler=False, seed=None,
                code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                cases=results)
    print(json.dumps(data,indent=2))


if __name__ == '__main__':
    main()
