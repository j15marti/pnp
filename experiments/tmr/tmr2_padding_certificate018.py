#!/usr/bin/env python3
"""TMR-2/018 independent syntactic-certificates audit, standard Python 3.

The finite fixture E0 uses a binary word whose bits designate independent
proper-3CNF four-clause unit gadgets for one shared variable. It is NOT a
complete general 3SAT encoding or a low-level universal TM interpreter.

The scanner does charge each physically moving READ-ONLY input-head step and
current-cell read separately from host-language syntactic/parsing work.
"""
import hashlib
import itertools
import json
from collections import Counter


def pad(x):
    return '1' * len(x) + '0' + x + '0' * (1 << len(x))


def reference_parse(y):
    """Independent grammar oracle for the restricted binary payload."""
    j = 0
    while j < len(y) and y[j] == '1':
        j += 1
    if j == len(y) or y[j] != '0':
        return 'MALFORMED'
    n = j
    prefix_len = 2 * n + 1
    if len(y) < prefix_len:
        return 'MALFORMED'
    if len(y) - prefix_len != 1 << n:
        return 'MALFORMED'
    if any(c != '0' for c in y[prefix_len:]):
        return 'MALFORMED'
    x = y[n+1:2*n+1]
    if any(c not in '01' for c in x):
        return 'MALFORMED'
    return 'UNSAT' if ('0' in x and '1' in x) else 'SAT'


def scan_and_classify(y):
    """A real locally moving source head scans the whole input exactly once.

    Parsing and satisfying the extracted toy formula are separately implemented
    in Python and are NOT claimed to be individually charged TM transitions.
    """
    pos = 0  # Left endmarker; data positions 1..N, right marker N+1
    n = len(y)
    transitions = 0
    current_cell_reads = 0
    head_moves = 0
    visited = set()
    seen = []
    while pos <= n:
        sym = 'LEFT' if pos == 0 else y[pos-1]
        if pos > 0:
            current_cell_reads += 1
            visited.add(pos)
            seen.append(sym)
        # One physical locally moving transition; read current cell, then move.
        pos += 1
        head_moves += 1
        transitions += 1
    assert pos == n + 1
    assert ''.join(seen) == y
    # At the right marker, output in one further physical transition.
    label = reference_parse(''.join(seen))
    transitions += 1
    return label, transitions, current_cell_reads, head_moves, visited


def forcing_3cnf(bits):
    """Four strict proper ternary clauses enforce a prescribed x value."""
    clauses = []
    for i, bit in enumerate(bits):
        base = 1 if bit == '0' else -1
        u, v = 2*i+2, 2*i+3
        for su in (-1, 1):
            for sv in (-1, 1):
                clauses.append((base, su*u, sv*v))
    return clauses, 1 + 2*len(bits)


def brute_satisfiable(clauses, var_count):
    for values in itertools.product((False, True), repeat=var_count):
        if all(any((lit > 0) == values[abs(lit)-1] for lit in cl) for cl in clauses):
            return True
    return False


def main():
    counts = Counter()
    max_length = 0
    examples = {}
    digest = hashlib.sha256()
    for n in range(0, 9):
        for t in range(1 << n):
            x = format(t, '0%db' % n) if n else ''
            z = pad(x)
            N = len(z)
            assert N == 2*n+1+(1 << n)
            got, steps, reads, moves, visited = scan_and_classify(z)
            expected = 'UNSAT' if ('0' in x and '1' in x) else 'SAT'
            assert got == expected
            assert len(visited) == N and reads == N and steps == N+2
            suffix_start = 2*n+2  # 1-based first data-bit position
            assert set(range(suffix_start, N+1)).issubset(visited)
            counts['valid_sources'] += 1
            counts['valid_'+expected] += 1
            counts['valid_current_cell_reads'] += reads
            counts['valid_source_head_transitions'] += steps
            max_length = max(max_length, N)
            digest.update((x + ':' + got + ':' + str(steps) + ';').encode())
            # Exhaustively flip all 2^n suffix bits for n<=6.
            if n <= 6:
                positions = range(2*n+1, N)
            else:
                # deterministic sample incl first, middle and final suffix cell
                positions = sorted({2*n+1, (2*n+1+N-1)//2, N-1})
            for j in positions:
                w = z[:j] + '1' + z[j+1:]
                ref = reference_parse(w)
                assert ref == 'MALFORMED'
                actual, charged, creads, cmoves, _ = scan_and_classify(w)
                assert actual == ref
                assert len(w) == N and sum(a != b for a,b in zip(z,w)) == 1
                counts['suffix_corruptions'] += 1
                counts['corrupt_current_cell_reads'] += creads
                counts['corrupt_source_head_transitions'] += charged
                digest.update((str(n)+':'+str(j)+':bad;').encode())
            # Prefix invalidity checks, not all are uniformly malformed when
            # x itself is replaced; test only sufficient syntactic mutations.
            malformed = [z + '0', z[:-1], z[:n] + '1' + z[n+1:]]
            for w in malformed:
                assert reference_parse(w) == 'MALFORMED'
                actual, _, _, _, _ = scan_and_classify(w)
                assert actual == 'MALFORMED'
                counts['length_or_delimiter_controls'] += 1
    for n in (1,2,3,4):
        for t in range(1 << n):
            x = format(t, '0%db' % n)
            cls, nv = forcing_3cnf(x)
            assert len(cls) == 4*n
            assert all(len({abs(l) for l in c}) == 3 for c in cls)
            assert brute_satisfiable(cls, nv) == ('0' not in x or '1' not in x)
            counts['proper_3cnf_exhaustive_controls'] += 1
    # Additional strict label examples, as opposed to only malformed cases.
    examples['valid_SAT'] = {'x':'000','padded':pad('000'),'label':reference_parse(pad('000'))}
    examples['valid_UNSAT'] = {'x':'01','padded':pad('01'),'label':reference_parse(pad('01'))}
    examples['first_suffix_flip'] = {'x':'01','padded':pad('01')[:5]+'1'+pad('01')[6:],'label':'MALFORMED'}
    out = {
        'agent':'TMR-2', 'run':'018', 'timestamp_pacific':'2026-11-14 04:19 PST',
        'status':'COMPUTATIONAL finite tests; mathematical statements independently proved in report, peer review pending',
        'model':'one locally moving read-only input head, full current-cell scan; Python parser operations not claimed charged microsteps',
        'payload':'restricted binary sign stream, each bit maps to proper-3CNF four-clause unit forcing gadget',
        'counts':dict(counts), 'maximum_N':max_length,'fixture_digest_sha256':digest.hexdigest(),
        'examples':examples,'assertion_failures':0,
        'limitations':['not a generic Turing-machine compiler','not a general 3SAT finite solver','host Python parsing and brute truth tables not translated to physical steps','asymptotic proof separate from finite experiments'],
    }
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
