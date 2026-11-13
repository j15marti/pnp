#!/usr/bin/env python3
"""Verify the pinned /620 SAT control. Does not run either native checker."""
import hashlib
import json
import sys
from pathlib import Path

SOURCE = 'results/raw/arc/2026-11-13_1128_LSPV3_620_ACCEPTED_341_SAT_SOURCE.cnf'
EXPECTED = 'c6f8bbf09baf6547de6fea04ac74dd0ecb32f6bd'

def main() -> None:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else SOURCE)
    raw = path.read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    if blob != EXPECTED:
        raise ValueError(f'Unexpected source Git blob: {blob}')
    lines = [x for x in raw.decode('utf-8').splitlines() if x and not x.startswith('c')]
    tag, kind, n, m = lines[0].split()
    n, m = int(n), int(m)
    if (tag, kind, n, m) != ('p', 'cnf', 18, 48):
        raise ValueError('Unexpected source header')
    clauses = [[int(x) for x in line.split()] for line in lines[1:]]
    if len(clauses) != m or any(len(c) != 4 or c[-1] != 0 for c in clauses):
        raise ValueError('Invalid 3-CNF clause ledger')
    if any(abs(x) < 1 or abs(x) > n for c in clauses for x in c[:-1]):
        raise ValueError('Literal out of range')
    masks = [(sum(1 << (x-1) for x in c[:-1] if x > 0),
              sum(1 << (-x-1) for x in c[:-1] if x < 0)) for c in clauses]
    def sat(a: int) -> bool:
        return all((a & p) or ((~a) & q) for p, q in masks)
    count = sum(sat(a) for a in range(1 << n))
    witness = '101001000000100000'
    model = sum(int(b) << i for i, b in enumerate(witness))
    if count != 64 or not sat(model):
        raise AssertionError('Published SAT-source claim not reproduced')
    print(json.dumps({'source_git_blob': blob, 'source_sha256': hashlib.sha256(raw).hexdigest(),
                      'variables': n, 'clauses': m, 'assignments_checked': 1 << n,
                      'models': count, 'verified_witness_x1_to_x18': witness,
                      'native_checker_replayed': False}, indent=2))

if __name__ == '__main__':
    main()
