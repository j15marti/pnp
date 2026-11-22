#!/usr/bin/env python3
"""Exact finite audit of DYNAMIC-CACHE-FIBER-AUDIT1; no timing claims.

Run from repository root. Enumerates product-table READY configurations,
not the previously tested source factorizations or the 3-CNF compiler.
"""
import hashlib
import itertools
import json
from pathlib import Path


def compose(left, right):
    return tuple(left[v - 1] for v in right)


def sign_bit(p):
    return sum(p[i] > p[j] for i in range(len(p))
               for j in range(i + 1, len(p))) % 2


def endpoint(gs):
    v = 1
    for g in gs:
        v = g[v - 1]
    return v


def label(gs):
    return int(endpoint(gs) == 1)


def full_product(gs):
    p = tuple(range(1, len(gs[0]) + 1))
    for g in gs:
        p = compose(g, p)
    return p


def cache(gs, kind):
    return sum(map(sign_bit, gs)) % 2 if kind == 'sign' else label(gs)


def cert_size(gs, domain, kind, free_cache):
    """Minimum number of whole-table/cache coordinates fixing this label.

    Whole-table queries are stronger than a single-tape cell read.
    free_cache=True conditions on the cache and counts table queries only.
    """
    row = gs + (cache(gs, kind),)
    opposite = [h + (cache(h, kind),) for h in domain
                if label(h) != label(gs)
                and (not free_cache or cache(h, kind) == cache(gs, kind))]
    indices = range(len(gs) if free_cache else len(gs) + 1)
    for size in range(len(gs) + 2):
        for chosen in itertools.combinations(indices, size):
            if all(any(row[j] != other[j] for j in chosen) for other in opposite):
                return size
    raise AssertionError('No certificate')


def cycles3(r):
    for a, b, c in itertools.combinations(range(1, r + 1), 3):
        for order in [(a, b, c), (a, c, b)]:
            p = list(range(1, r + 1))
            for x, y in zip(order, order[1:] + order[:1]):
                p[x - 1] = y
            yield tuple(p)


def encoding_ledger(r, k):
    layers = 2 * k
    n0 = (layers + 1) * (2 * r - 3) + 2
    m0 = (layers + 1) * (r * r - 2) + 2 * layers * r + 8
    n, m = n0 + m0 + 3, 2 * m0 + 4
    w = n.bit_length()
    nbits = 3 * n + 2 + 2 * ((m + 1).bit_length() - 1) + 3 * m * (w + 1) + w
    return dict(r=r, k=k, L=layers, n0=n0, m0=m0, n=n, m=m, w=w, N=nbits)


def run():
    r, k = 3, 2
    domain = list(itertools.product(itertools.permutations(range(1, r + 1)), repeat=k))
    rows, witnesses = [], []
    for gs in domain:
        entry = dict(tables=gs, endpoint=endpoint(gs), decision=label(gs), sign=cache(gs, 'sign'))
        for kind in ['sign', 'answer']:
            entry[kind + '_table_certificate_given_cache'] = cert_size(gs, domain, kind, True)
            entry[kind + '_total_coordinate_certificate'] = cert_size(gs, domain, kind, False)
        assert entry['sign_table_certificate_given_cache'] == k
        assert entry['sign_total_coordinate_certificate'] == k
        assert entry['answer_table_certificate_given_cache'] == 0
        assert entry['answer_total_coordinate_certificate'] == 1
        for i in range(k):
            found = 0
            for cyc in cycles3(r):
                h = gs[:i] + (compose(cyc, gs[i]),) + gs[i + 1:]
                assert sign_bit(cyc) == 0 and cache(h, 'sign') == cache(gs, 'sign')
                if label(h) != label(gs):
                    found += 1
                    assert all(h[j] == gs[j] for j in range(k) if j != i)
                    witnesses.append(dict(source=gs, block=i, cycle=cyc, target=h,
                                          source_decision=label(gs), target_decision=label(h)))
            assert found > 0
        rows.append(entry)
    small = list(itertools.product(itertools.permutations((1, 2)), repeat=1))
    r2_control = [dict(tables=gs, sign=cache(gs, 'sign'), decision=label(gs),
                       table_certificate_given_sign=cert_size(gs, small, 'sign', True))
                  for gs in small]
    assert all(x['table_certificate_given_sign'] == 0 for x in r2_control)
    fibers = {}
    for gs in domain:
        p = full_product(gs)
        assert p[0] == endpoint(gs)
        fibers.setdefault(p, []).append(gs)
    fiber_rows = []
    for p, members in sorted(fibers.items()):
        counts = {v: sum(g[0][0] == v for g in members) for v in range(1, r + 1)}
        assert len(members) == 6 and set(counts.values()) == {2}
        assert len({label(gs) for gs in members}) == 1
        fiber_rows.append(dict(product=p, decision=int(p[0] == 1),
                               members=members, intermediate_vertex_counts=counts))
    result = dict(lemma='DYNAMIC-CACHE-FIBER-AUDIT1', status='COMPUTATIONAL',
                  scope='Exhaustive READY product-table/cached-sign finite audit; not a TM simulator or CNF certification',
                  source_revision='60d2c55720b028466a7ef3095d3425a14e5851f2',
                  code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  encoding=encoding_ledger(r, k), configurations=len(rows),
                  SAT=sum(x['decision'] for x in rows), UNSAT=sum(1-x['decision'] for x in rows),
                  same_sign_opposite_label_witnesses=len(witnesses),
                  rows=rows, witnesses=witnesses, full_product_fibers=fiber_rows,
                  excluded_r2_control=r2_control)
    out = Path('results/raw/dynamic_redteam_cache_fibers_20261121.json')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: result[key] for key in ['configurations', 'SAT', 'UNSAT',
          'same_sign_opposite_label_witnesses', 'encoding', 'code_sha256']}))
    print('raw_sha256=' + hashlib.sha256(out.read_bytes()).hexdigest())


if __name__ == '__main__':
    run()
