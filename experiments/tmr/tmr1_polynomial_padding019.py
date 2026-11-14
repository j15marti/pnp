#!/usr/bin/env python3
"""TMR-1/019 finite hostile audit of honest polynomial padding.

Standalone CPython 3. No external dependencies or oracle.
The toy payload models a restricted proper 3-CNF sign-gadget language;
it is NOT a general 3-CNF solver. Host Python string operations and tests
are NOT a charged generic physical Turing-machine implementation.
"""
import argparse
import hashlib
import itertools
import json
import time
from collections import Counter


def pad(x: str, degree: int) -> str:
    assert degree >= 2 and len(x) >= 1
    return '1' * len(x) + '0' + x + '0' * (len(x) ** degree)


def toy_label(x: str) -> str:
    if not x or any(c not in '01' for c in x):
        return 'MALFORMED'
    return 'SAT' if len(set(x)) == 1 else 'UNSAT'


def trivalid(y: str, d: int) -> str:
    """Independent full string reference recognizer; not physical TM time."""
    i = 0
    while i < len(y) and y[i] == '1':
        i += 1
    if i == 0 or i == len(y) or y[i] != '0':
        return 'MALFORMED'
    end = 2*i + 1
    if end > len(y) or len(y) != end + i**d:
        return 'MALFORMED'
    x = y[i+1:end]
    if len(x) != i or any(b != '0' for b in y[end:]):
        return 'MALFORMED'
    return toy_label(x)


def membership(y: str, d: int) -> bool:
    return trivalid(y, d) == 'SAT'


def physical_full_scan(y: str):
    """Only physical source head trajectory and its current-cell reads charged."""
    p = 0  # left endmarker; data positions 1 ... N
    seen = []
    visited = []
    moves = 0
    while p <= len(y):
        sym = 'LEFT' if p == 0 else y[p-1]
        if p > 0:
            seen.append(sym)
            visited.append(p)
        p += 1
        moves += 1
    assert ''.join(seen) == y and p == len(y)+1
    return moves, visited


def physically_prefix_decide(y: str, d: int):
    """Fixed binary membership algorithm: early NO on every UNSAT payload.

    Counts actual read-only current-cell observations and moves ONLY.
    Semantic toy decision/host arithmetic are not claimed to be TM-level charged.
    """
    p = 0
    visited = []
    def read():
        nonlocal p
        if p > len(y):
            return 'RIGHT'
        sym = 'LEFT' if p == 0 else y[p-1]
        if p > 0:
            visited.append(p)
        return sym
    assert read() == 'LEFT'
    p += 1
    n = 0
    while True:
        sym = read()
        if sym == 'RIGHT':
            return False, visited
        if sym == '0':
            p += 1
            break
        n += 1
        p += 1
    if n < 1:
        return False, visited
    data = []
    for _ in range(n):
        sym = read()
        if sym == 'RIGHT':
            return False, visited
        data.append(sym)
        p += 1
    x = ''.join(data)
    lab = toy_label(x)
    if lab != 'SAT':
        return False, visited  # NO without reading ANY suffix bit
    # SAT inner payload: verify every padded zero and the right endmarker
    for _ in range(n**d):
        sym = read()
        if sym != '0':
            return False, visited
        p += 1
    return read() == 'RIGHT', visited


def force_gadget(x):
    """Four proper 3-CNF clauses per bit force same shared variable."""
    clauses = []
    for i, bit in enumerate(x):
        primary = 1 if bit == '1' else -1
        u, v = 2*i+2, 2*i+3
        for su, sv in itertools.product((-1, 1), repeat=2):
            clauses.append((primary, su*u, sv*v))
    return clauses, 2*len(x)+1


def independent_dpll(clauses, n):
    """Independent small truth-table verifier; limited to n<=11."""
    for z in range(1 << n):
        ok = True
        for cl in clauses:
            if not any((((z >> (abs(t)-1)) & 1) == 1) == (t > 0) for t in cl):
                ok = False
                break
        if ok:
            return True
    return False


def main(d):
    start = time.monotonic()
    tally = Counter()
    digest = hashlib.sha256()
    sample = {}
    for n in range(1, 7):
        for tup in itertools.product('01', repeat=n):
            x = ''.join(tup)
            y = pad(x, d)
            N = len(y)
            assert N == 2*n+1+n**d
            lab = trivalid(y, d)
            assert lab == toy_label(x) != 'MALFORMED'
            tally['valid_sources'] += 1
            tally['valid_'+lab] += 1
            # Physical source scanning: every position 1..N is actually observed.
            moved, observed = physical_full_scan(y)
            assert moved == N+1 and observed[-1] == N
            tally['full_scan_head_moves'] += moved
            # Binary decider (potentially expensive) can reject UNSAT BEFORE suffix.
            yes, inspected = physically_prefix_decide(y, d)
            assert yes == (lab == 'SAT')
            if lab == 'UNSAT':
                assert len(inspected) <= 2*n+1
                assert all(q <= 2*n+1 for q in inspected)
                tally['unsat_valid_early_binary_rejections'] += 1
                tally['unsat_early_visited_bits'] += len(inspected)
            else:
                assert inspected[-1] == N
                tally['sat_valid_suffix_visited_bits'] += N-(2*n+1)
            suffix_start = 2*n+1  # zero-based substring begins at this index
            # Exhaustive one-bit changes of required syntax to MALFORMED.
            for j in range(suffix_start, N):
                alternate = y[:j]+'1'+y[j+1:]
                assert len(alternate)==N and trivalid(alternate, d)=='MALFORMED'
                yes_alt, seen_alt = physically_prefix_decide(alternate, d)
                assert not yes_alt
                if lab == 'UNSAT':
                    assert not any(k > 2*n+1 for k in seen_alt)
                tally['opposite_tri_label_suffix_neighbors'] += 1
                if lab == 'SAT':
                    tally['sat_to_no_binary_neighbors'] += 1
                digest.update(f'{d}|{x}|{j}|{lab}\n'.encode())
            # Exhaustive changes in syntax header / embedded data.
            if n <= 5:
                for j in range(suffix_start):
                    alt = y[:j]+('0' if y[j]=='1' else '1')+y[j+1:]
                    assert physically_prefix_decide(alt, d)[0] == membership(alt,d)
                    tally['header_payload_mutations_checked'] += 1
            if n <= 5:
                clauses, v = force_gadget(x)
                assert independent_dpll(clauses, v) == (lab=='SAT')
                tally['proper_three_distinct_variable_3cnf_controls'] += 1
            if x == '01':
                sample = {'d':d,'x':x,'N':N,'valid_label':lab,
                          'forced_reads':n**d,'full_scan_source_movements':moved,
                          'binary_no_reads':len(inspected),
                          'binary_no_max_position':max(inspected)}
    return {'agent':'TMR-1','run':'019', 'degree':d,
            'model':'1 locally moving source head, tri-label source read certificate and binary early-reject witness',
            'timestamp_pacific':'2026-11-14 05:00 PST',
            'code':'experiments/tmr/tmr1_polynomial_padding019.py',
            'raw_status':'COMPUTATIONAL finite fixtures',
            'counts':dict(tally), 'fixture_sha256':digest.hexdigest(),
            'sample':sample, 'max_payload_bits':6,
            'assertion_failures':0,
            'elapsed_seconds_rounded':round(time.monotonic()-start,3),
            'limitations':['Toy proper-3CNF force-gadget payload, not a general NP-complete E parser',
                           'Host Python toy semantics and integer arithmetic not compiled into low-level TM',
                           'Only source head movement and current-cell access explicitly charged',
                           'Asymptotic proof is separate from this finite experiment']}

if __name__ == '__main__':
    a=argparse.ArgumentParser();a.add_argument('--degree',type=int,required=True);a.add_argument('--output',required=True)
    o=a.parse_args()
    assert o.degree in (2,3,4)
    result=main(o.degree)
    with open(o.output,'w',encoding='utf-8') as f:
        json.dump(result,f,sort_keys=True,indent=2);f.write('\n')
    print(json.dumps({'degree':o.degree,'seconds':result['elapsed_seconds_rounded'],
                      'counts':result['counts'],'failures':result['assertion_failures']},sort_keys=True))
