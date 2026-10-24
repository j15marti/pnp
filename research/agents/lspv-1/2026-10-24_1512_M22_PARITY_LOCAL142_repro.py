#!/usr/bin/env python3
"""Exact finite checker for M22-PARITY-LOCAL142.

Run from repository root: python research/agents/lspv-1/<script-name>.py
Run outside repository: python M22_PARITY_LOCAL142_repro.py

Uses only Python standard library. An imported published UNSAT claim is never
presented as computationally re-proved; the validator checks grammar,
explicit pairwise-marginal identities and the separate SAT witness.
"""
import ast
import json
from collections import Counter
from pathlib import Path

Y = ((1,2,3),(1,4,5),(2,4,6),(3,5,6),
     (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
U_PATH = Path('research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt')
W_PATH = Path('research/agents/lspv-2/2026-10-24_1112_M22_DEFECT_ADAPTER131_monotone_sat_witness.json')


def target_stats(clauses):
    p, q, seen = set(), set(), set()
    pos, neg = Counter(), Counter()
    for clause in clauses:
        assert len(clause) == 3 and len(set(map(abs, clause))) == 3
        assert all(z > 0 for z in clause) or all(z < 0 for z in clause)
        key = tuple(sorted(map(abs, clause)))
        signed_key = (1 if clause[0] > 0 else -1, key)
        assert signed_key not in seen
        seen.add(signed_key)
        support = p if clause[0] > 0 else q
        counts = pos if clause[0] > 0 else neg
        support.add(key)
        for z in clause:
            counts[abs(z)] += 1
    assert set(pos) == set(neg)
    assert all(pos[z] == neg[z] == 2 for z in pos)
    return dict(k=len(pos), m=len(clauses), q=len(p-q), paired=len(p&q),
                target=(p != q), pairfree=(not p&q))


def parity_row(clause):
    # For all-positive OR, the parity-odd four rows are all satisfying.
    # For all-negative OR, parity-even rows are all satisfying.
    want = 1 if clause[0] > 0 else 0
    return [bits for bits in range(8) if bits.bit_count() % 2 == want]


def parity_consistency(clauses):
    rows = [parity_row(c) for c in clauses]
    hist = Counter()
    tested = 0
    conflicts = 0
    for i, a in enumerate(clauses):
        names_a = tuple(map(abs, a))
        for j in range(i+1, len(clauses)):
            names_b = tuple(map(abs, clauses[j]))
            shared = tuple(sorted(set(names_a) & set(names_b)))
            hist[len(shared)] += 1
            tested += 1
            ma, mb = Counter(), Counter()
            for word in rows[i]:
                projected = tuple((word >> names_a.index(x)) & 1 for x in shared)
                ma[projected] += 1
            for word in rows[j]:
                projected = tuple((word >> names_b.index(x)) & 1 for x in shared)
                mb[projected] += 1
            if ma != mb:
                conflicts += 1
    for c, rows4 in zip(clauses, rows):
        for word in rows4:
            assert any(((word >> z) & 1) == (1 if c[z] > 0 else 0) for z in range(3))
    return {'tested_clause_pairs': tested,
            'intersection_histogram': {str(z): hist[z] for z in (0,1,2,3)},
            'marginal_conflicts': conflicts}


def xor_consistency(clauses):
    """Gauss-Jordan-style incremental GF(2) elimination of stronger XOR clauses."""
    basis = {}
    contradiction = False
    for clause in clauses:
        mask = sum(1 << (abs(z)-1) for z in clause)
        rhs = int(clause[0] > 0)
        for pivot, (oldmask, oldrhs) in sorted(basis.items()):
            if (mask >> pivot) & 1:
                mask ^= oldmask
                rhs ^= oldrhs
        if mask == 0:
            contradiction |= bool(rhs)
        else:
            pivot = (mask & -mask).bit_length() - 1
            basis[pivot] = (mask, rhs)
    return {'rank': len(basis), 'inconsistent': contradiction}


def witness_check(clauses, bits):
    return len(bits) == max(abs(z) for c in clauses for z in c) and all(
        any((bits[abs(z)-1] == '1') if z > 0 else (bits[abs(z)-1] == '0')
            for z in clause)
        for clause in clauses
    )


def count_models(clauses, k):
    return sum(witness_check(clauses, ''.join('1' if (mask >> j) & 1 else '0'
                                               for j in range(k)))
               for mask in range(1 << k))


def stats(clauses):
    return {**target_stats(clauses), **parity_consistency(clauses),
            'stronger_xor': xor_consistency(clauses)}


def main():
    out = {'name': 'M22-PARITY-LOCAL142', 'status': 'COMPUTATIONAL finite audit'}
    h = Y[:4] + tuple(tuple(-z for z in clause) for clause in Y[:4])
    out['Y'] = {**stats(Y), 'model_count': count_models(Y, 6)}
    out['fully_paired_H_outside_target'] = {**stats(h), 'model_count': count_models(h, 6)}
    assert out['Y']['q'] == 4 and out['Y']['marginal_conflicts'] == 0
    assert out['Y']['model_count'] == 20
    assert out['fully_paired_H_outside_target']['q'] == 0
    assert out['fully_paired_H_outside_target']['model_count'] == 18
    assert out['fully_paired_H_outside_target']['marginal_conflicts'] == 4
    if U_PATH.is_file() and W_PATH.is_file():
        raw = U_PATH.read_text(encoding='utf-8')
        u = ast.literal_eval(raw[raw.index('['):])
        metadata = json.loads(W_PATH.read_text(encoding='utf-8'))
        v = [list(c) for c in u]
        for index, replacement in metadata['source_replacements'].items():
            v[int(index)] = replacement
        out['published_U_unsat_imported'] = stats(u)
        out['U_mutant_V_sat_witness_replayed'] = {
            **stats(v), 'valid_sat_witness': witness_check(v, metadata['witness_bits'])}
        assert out['published_U_unsat_imported']['q'] == 132
        assert out['U_mutant_V_sat_witness_replayed']['q'] == 132
        assert out['published_U_unsat_imported']['marginal_conflicts'] == 0
        assert out['U_mutant_V_sat_witness_replayed']['marginal_conflicts'] == 0
        assert out['published_U_unsat_imported']['stronger_xor']['inconsistent']
        assert out['U_mutant_V_sat_witness_replayed']['stronger_xor']['inconsistent']
        assert out['U_mutant_V_sat_witness_replayed']['valid_sat_witness']
        assert out['published_U_unsat_imported']['intersection_histogram'] == \
               out['U_mutant_V_sat_witness_replayed']['intersection_histogram']
        out['original_U_status_note'] = 'UNSAT imported from published D\u00f6cker proof, not re-proved here'
    else:
        out['U_validation'] = 'SKIPPED: source and witness paths not available; run from repo root'
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
