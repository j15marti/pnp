#!/usr/bin/env python3
"""LSPV-4/592: independent signed Davis-Putnam guard-erasure cost audit.
Standard-library Python; deterministic, no network, no historical checker replacement.
Run: python lspv4_592_guard_projection.py > lspv4_592_raw.json
"""
import itertools
import json


def norm(lits):
    s = set(lits)
    if any(-x in s for x in s):
        return None
    return tuple(sorted(s, key=lambda x: (abs(x), x < 0)))


def dp(clauses, order):
    records = [('SOURCE', c, None, None, None) for c in clauses]
    active = {c: i for i, c in enumerate(clauses)}
    steps = []
    for x in order:
        p = [(c, i) for c, i in active.items() if x in c]
        n = [(c, i) for c, i in active.items() if -x in c]
        nxt = {c: i for c, i in active.items() if x not in c and -x not in c}
        created = []
        for a, ai in p:
            for b, bi in n:
                c = norm([z for z in a if z != x] + [z for z in b if z != -x])
                if c is None or c in nxt:
                    continue
                records.append(('RES', c, ai, bi, x))
                nxt[c] = len(records) - 1
                created.append((c, a, b))
        active = nxt
        steps.append(created)
    for i, (kind, c, a, b, x) in enumerate(records):
        if kind != 'RES':
            continue
        assert 0 <= a < i and 0 <= b < i
        assert x in records[a][1] and -x in records[b][1]
        assert norm([z for z in records[a][1] if z != x] +
                    [z for z in records[b][1] if z != -x]) == c
    return {'records': records, 'active': active, 'steps': steps,
            'res': sum(kind == 'RES' for kind, *_ in records)}


def guard_test(source, order, guard, expect_unsat):
    assert all(abs(z) != guard for c in source for z in c)
    base = dp(source, order)
    guarded = dp([norm(list(c) + [-guard]) for c in source] + [(guard,)], order + [guard])
    # The whole shared RES DAG (not just counts) is transported before g elimination.
    assert len(base['steps']) + 1 == len(guarded['steps'])
    for a, b in zip(base['steps'], guarded['steps'][:-1]):
        stripped = [(norm(z for z in c if z != -guard),
                     norm(z for z in x if z != -guard),
                     norm(z for z in y if z != -guard)) for c, x, y in b]
        assert a == stripped
    # Check the shared parent identity mapping, not just the clause values.
    n = len(source)
    for i in range(n+1, len(guarded['records']) - int(expect_unsat)):
        kind,c,p,q,x = guarded['records'][i]
        bk,bc,bp,bq,bx = base['records'][i-1]
        def rebase(z):
            assert z != n  # guard SOURCE must never occur in an x-step
            return z if z < n else z-1
        assert (kind,bp,bq,bx) == ('RES',rebase(p),rebase(q),x)
        assert norm(v for v in c if v != -guard) == bc
    assert (() in base['active']) == expect_unsat
    assert guarded['res'] == base['res'] + (1 if expect_unsat else 0)
    assert len(guarded['steps'][-1]) == (1 if expect_unsat else 0)
    if expect_unsat:
        assert guarded['steps'][-1][0][0] == ()
        assert norm((-guard,)) in guarded['active'] or () in guarded['active']
    return base, guarded


def prism(m, odd):
    edges = []
    for i in range(m):
        edges.extend([(f'T{i}', f'T{(i+1)%m}'),
                      (f'B{i}', f'B{(i+1)%m}'), (f'T{i}', f'B{i}')])
    source = []
    for i in range(m):
        for side in 'TB':
            v = f'{side}{i}'
            inc = [j + 1 for j, (a, b) in enumerate(edges) if v in (a, b)]
            assert len(inc) == 3
            charge = int(odd and i == 0 and side == 'T')
            for bits in itertools.product((0, 1), repeat=3):
                if sum(bits) % 2 == charge:
                    continue
                source.append(norm((-e if bit else e) for e, bit in zip(inc, bits)))
    return source, list(range(1, 3*m + 1))


def satisfiable(clauses, n):
    for bits in itertools.product((0, 1), repeat=n):
        if all(any((bits[abs(x)-1] == int(x > 0)) for x in c) for c in clauses):
            return True
    return False


def main():
    rows = []
    for m in list(range(3, 16)) + [20, 30, 40]:
        src, order = prism(m, True)
        a, b = guard_test(src, order, 3*m+1, True)
        rows.append({'m':m, 'strict_source':len(src),
                     'strict_res':a['res'], 'guarded_source':len(src)+1,
                     'guarded_res':b['res'], 'guarded_paid_including_one_cli_gate':b['res']+1,
                     'strict_per_pivot':[len(x) for x in a['steps']] if m <= 5 else None})
    assert all(x['strict_res'] == 80*x['m']-161 for x in rows)
    # Exhaustive *formula* controls: all 256 subsets of the eight proper 3-clauses
    # on three variables; all six variable orders; plus contradictory units.
    all3 = [norm(-i-1 if bit else i+1 for i, bit in enumerate(bits))
            for bits in itertools.product((0, 1), repeat=3)]
    tested = 0
    sat_count = unsat_count = 0
    for mask in range(1 << len(all3)):
        formula = [c for i,c in enumerate(all3) if mask & (1 << i)]
        unsat = not satisfiable(formula, 3)
        for perm in itertools.permutations((1,2,3)):
            guard_test(formula, list(perm), 4, unsat)
            tested += 1
            sat_count += not unsat
            unsat_count += unsat
    even_controls = []
    for m in (3, 4, 5):
        src, order = prism(m, False)
        assert satisfiable(src, 3*m)
        a,b = guard_test(src, order, 3*m+1, False)
        even_controls.append({'m':m, 'strict_res':a['res'], 'guarded_res':b['res'],
                              'final_guard_resolution':len(b['steps'][-1])})
    for formula, unsat in [([(1,),(-1,)],True), ([(1,2),(-1,2)],False), ([()],True)]:
        for perm in itertools.permutations((1,2,3)):
            guard_test(formula, list(perm), 4, unsat)
            tested += 1
            sat_count += not unsat
            unsat_count += unsat
    print(json.dumps({'report':'LSPV-4/592', 'classification':'PROVED/RESTRICTED plus computational',
                      'prism_odd_charges':rows, 'exhaustive_small_formula_order_cases':tested,
                      'sat_controls':sat_count,'unsat_controls':unsat_count,
                      'even_charge_prism_controls':even_controls,
                      'hostile_even_charge_label_control':'satisfiable; no final g pivot',
                      'native_original_checker_executed':False,
                      'historical_mixed_R_mix341_recovered':False,
                      'guarantee':'DP strict/guarded record-pair bijection except final g-RES on UNSAT'},
                     indent=2))

if __name__ == '__main__':
    main()
