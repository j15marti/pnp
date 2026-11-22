"""Deterministic finite audit of acquisition on original, labelled support groups."""
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json
from dynamic_construction_dihedral_choice_20261121 import build, codec


def cycle(k, p, q):
    if k < 6 or k % 2 or not (0 < p < k and 0 < q < k):
        raise ValueError("requires even k >= 6 and interior marks")
    clauses = []
    for i in range(k):
        scope = (k + 1, i + 1, (i + 1) % k + 1)
        for gate, x, y in product(range(2), repeat=3):
            demand = int(i not in (0, (p, q)[gate]))
            if x + y != demand:
                clauses.append(tuple(-v if bit else v for v, bit in zip(scope, (gate, x, y))))
    return clauses


def groups(clauses):
    tables = {}
    for row in clauses:
        scope = tuple(sorted(map(abs, row)))
        if len(scope) != 3 or len(set(scope)) != 3 or 0 in scope:
            raise ValueError("expected proper ternary row")
        forbidden = tuple(int(-v in row) for v in scope)
        tables.setdefault(scope, set(product(range(2), repeat=3))).discard(forbidden)
    return tables


def locally_admitted(scope, table, pins):
    fixed = [i for i, v in enumerate(scope) if v in pins]
    free = [i for i, v in enumerate(scope) if v not in pins]
    domain = set(product(range(2), repeat=len(free)))
    layers = [{x for x in domain if sum(x) == b} for b in range(len(free) + 1)]
    for values in product(range(2), repeat=len(fixed)):
        section = {tuple(x[i] for i in free) for x in table
                   if tuple(x[i] for i in fixed) == values}
        if section and section != domain and section not in layers:
            return False
    return True


def acquire(tables):
    degree = Counter(v for scope in tables for v in scope)
    forced = {v for v, d in degree.items() if d > 2}
    visited = 0

    def find(pins, left):
        nonlocal visited
        visited += 1
        for scope, table in tables.items():
            if locally_admitted(scope, table, pins):
                continue
            if left:
                for v in scope:
                    if v not in pins:
                        answer = find(pins | {v}, left - 1)
                        if answer is not None:
                            return answer
            return None
        return pins

    for left in range(len(degree) - len(forced) + 1):
        result = find(forced, left)
        if result is not None:
            return sorted(result), visited
    raise AssertionError("full pinning must succeed")


def audit():
    scope = (1, 2, 3)
    domain = list(product(range(2), repeat=3))
    table_audit = []
    for mask in range(256):
        table = {bits for i, bits in enumerate(domain) if (mask >> i) & 1}
        valid = [pins for n in range(4) for pins in combinations(scope, n)
                 if locally_admitted(scope, table, pins)]
        picked, visits = acquire({scope: table})
        assert tuple(picked) in valid and len(picked) == min(map(len, valid))
        table_audit.append([mask, picked, visits])
    control = []
    for t in range(1, 4):
        picked, visits = acquire(groups([(3*i+1, 3*i+2, 3*i+3) for i in range(t)]))
        assert len(picked) == 2*t
        control.append([t, picked, visits])
    cases = []
    images = []
    for k in (6, 8):
        for p, q in product(range(1, k), repeat=2):
            rows = cycle(k, p, q)
            pins, visits = acquire(groups(rows))
            branches = []
            for gate in (0, 1):
                branches.append(any(all(any(bits[abs(v)-1] == (v > 0) for v in row)
                                        for row in rows)
                                    for xs in product(range(2), repeat=k)
                                    for bits in [xs + (gate,)]))
            assert len(rows) == 4*k+4 and pins == [k+1]
            assert branches == [bool(p % 2), bool(q % 2)]
            cases.append([k, p, q, pins, visits, branches])
            if k == 6 and (p, q) in ((1, 2), (2, 4)):
                bits, program, r = build(codec.load_generator(), rows)
                n, target, alpha, beta, release = codec.parse(bits)
                c = len(rows)
                n0 = k+1 + (10*c+1)*r + 2
                m0 = (20*c+4)*r
                m = 2*m0+4
                w = n.bit_length()
                assert (r, n, len(target), release) == (c+1, n0+m0+3, m, n0+1)
                assert len(bits) == 3*n+2+2*((m+1).bit_length()-1)+3*m*(w+1)+w
                assert sum(a != b for a, b in zip(alpha, beta)) == 1
                for row in target:
                    a = alpha if sum(v > 0 for v in row) <= 1 else beta
                    assert any((a[abs(v)-1] == '1') == (v > 0) for v in row)
                images.append(dict(k=k,p=p,q=q,n=n,m=m,N=len(bits),r=r,
                                   sha256_ascii_bits=sha256(bits.encode()).hexdigest()))
    return dict(code_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                mode="exhaustive finite; no seed; no tape timing", table_tests=table_audit,
                disjoint_OR=control, cycle_cases=cases, images=images)


if __name__ == "__main__":
    print(json.dumps(audit(), separators=(",", ":")))
