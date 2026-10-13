#!/usr/bin/env python3
"""IMAGE22DECODE1: exact ordered-image decoder and bounded falsification audit.

Uses the *unchanged* universal22.py compiler. Canonical encoding is the
ordered compact JSON byte encoding in image22_language_audit.py, not a
clause-sorted or isomorphism-canonical representation. No SAT oracle or
claimed lower bound is used by the decoder. Every invocation has a 25-second
cooperative deadline. Run --batch exhaustive or --batch controls separately.
"""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import itertools
import json
from pathlib import Path
import time
import universal22 as u

RUN_ID = 'IMAGE22DECODE1'
EXPECTED_COMPILER_BLOB = 'f985a13f237f2322f988ec82af132625acf3912c'


def encode(cnf: u.CNF) -> bytes:
    return json.dumps(cnf, separators=(',', ':'), ensure_ascii=True).encode('ascii')


def bounded_proper(cnf: object) -> int | None:
    """Validate before any allocation indexed by an untrusted variable ID."""
    if not isinstance(cnf, list) or not cnf:
        return None
    cap = 3 * len(cnf)
    for c in cnf:
        if not isinstance(c, (list, tuple)) or len(c) != 3:
            return None
        if any(type(x) is not int or x == 0 or abs(x) > cap for x in c):
            return None
    try:
        return u.check_proper(cnf)
    except (ValueError, TypeError):
        return None


@dataclass
class Decoded:
    balanced: u.CNF
    clone_map: list[int]
    clause_count: int
    R: int


def decode_image(target: bytes) -> Decoded | None:
    """Total exact recognizer/inverse for the declared ordered compiler image.

    Return its unique balanced preimage, or None. Full deterministic
    recompilation/equality is essential: local format alone is insufficient.
    Python's hash-table implementation is not a sublinear-space or unit-bit
    machine claim; the accompanying proof gives conservative polynomial costs.
    """
    try:
        parsed = json.loads(target)
        n = bounded_proper(parsed)
        if n is None:
            return None
        cnf = [tuple(c) for c in parsed]
        if encode(cnf) != target:
            return None
        M = len(cnf)
        if M % 24 or n != 3 * M // 4:
            return None
        mb, R = M // 12, M // 8
        clone_map = [0] * (R + 1)
        first, group = 1, 1
        for index in range(R):
            source_id = index + 1
            left, right, port = cnf[mb + index]
            expected_port = R + 15 * (index // 3) + u.PORTS[index % 3]
            if left != -source_id or port != expected_port:
                return None
            clone_map[source_id] = group
            if right == source_id + 1 and source_id < R:
                continue
            if right != first or source_id < first + 1:
                return None
            group += 1
            first = source_id + 1
        if first != R + 1:
            return None
        if any(abs(l) > R for c in cnf[:mb] for l in c):
            return None
        bal = [tuple((1 if l > 0 else -1) * clone_map[abs(l)] for l in c)
               for c in cnf[:mb]]
        nb = bounded_proper(bal)
        if nb is None or nb != group - 1:
            return None
        counts = Counter(l for c in bal for l in c)
        if any(counts[x] != counts[-x] or counts[x] < 2 for x in range(1, nb + 1)):
            return None
        rebuilt = u.compile22(bal)
        if rebuilt.padding_gadgets != 0 or rebuilt.clauses != cnf:
            return None
        return Decoded(bal, clone_map, M, R)
    except (ValueError, TypeError, OverflowError, RecursionError, UnicodeError):
        return None


def preimages(decoded: Decoded, deadline: float | None = None) -> list[u.CNF]:
    """Enumerate the entire ordered source fiber, not only one guessed source.

    F must be a prefix of B(F). For g padding gadgets its counts necessarily
    satisfy m=m_B-7g and n=n_B-5g. These O(M) candidates are checked exactly.
    """
    B = decoded.balanced
    nb = u.check_proper(B)
    maximum = min((len(B) - 1) // 7, (nb - 3) // 5)
    found = []
    for g in range(maximum + 1):
        if deadline is not None and time.monotonic() > deadline:
            raise TimeoutError('25-second cooperative budget exceeded')
        F = B[:len(B) - 7 * g]
        if bounded_proper(F) != nb - 5 * g:
            continue
        candidate, candidate_n, candidate_g = u.balance(F)
        if candidate_g == g and candidate_n == nb and candidate == B:
            found.append(F)
    return found


def blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def run(batch: str) -> dict:
    start = time.monotonic()
    deadline = start + 25
    counts: Counter[str] = Counter()
    rows = []
    def check(condition: bool, group: str) -> None:
        if time.monotonic() > deadline:
            raise TimeoutError('25-second cooperative budget exceeded')
        counts[group] += 1
        if not condition:
            raise AssertionError((group, counts[group]))
    check(blob_sha(Path(u.__file__)) == EXPECTED_COMPILER_BLOB, 'exact_compiler_revision')
    cube = [tuple((j + 1) * (1 if b[j] == 0 else -1) for j in range(3))
            for b in itertools.product((0, 1), repeat=3)]
    if batch == 'exhaustive':
        cases = [(f'cube_subset_{mask:03d}', [cube[j] for j in range(8) if mask >> j & 1])
                 for mask in range(1, 256)]
    else:
        two, _ = u.properize23([(1, 2), (-1, 2)])
        graph3, _ = u.properize23(u.colouring_cnf(3, itertools.combinations(range(3), 2)))
        graph4, _ = u.properize23(u.colouring_cnf(4, itertools.combinations(range(4), 2)))
        # Three pigeons, two holes. Native count/flow detects UNSAT.
        php = [(2*i+1, 2*i+2) for i in range(3)]
        php += [(-(2*i+h+1), -(2*j+h+1)) for h in range(2) for i in range(3) for j in range(i+1, 3)]
        php3, _ = u.properize23(php)
        parity = [tuple((j+1)*(1 if b[j] == 0 else -1) for j in range(3))
                  for b in itertools.product((0, 1), repeat=3) if sum(b) % 2]
        cases = [
            ('horn', [(1,-2,-3),(-1,2,-3),(-1,-2,3)]),
            ('dual_horn', [(-1,2,3),(1,-2,3),(1,2,-3)]),
            ('two_sat', two), ('affine_parity', parity), ('tseitin_W1', u.W1),
            ('bounded_treewidth_chain', [(1,2,3),(-2,3,4),(-3,4,5)]),
            ('independent_product', [(1,2,3),(4,5,6)]),
            ('transparent_padding', [(1,2,3)] + u.pad7(1,4)),
            ('counting_flow_PHP_3_2', php3),
            ('colouring_K3_YES', graph3), ('colouring_K4_NO', graph4)]
        for raw in [b'', b'[]', b'null', b'[[true,2,3]]', b'[[0,2,3]]',
                    b'[[1,1,2]]', b'[[1,2,999999999999999999999999999999999]]',
                    b'[[1,2,3]] ', b'[[1,2,3],[1,2,3]]', b'[[1,2,3]]\x00']:
            check(decode_image(raw) is None, 'malformed_or_off_image')
        qmodels = 0
        for b in itertools.product((0, 1), repeat=15):
            values = dict(enumerate(b, 1))
            if u.eval_cnf(u.Q, values):
                qmodels += 1
                check(all(values[p] == 0 for p in u.PORTS), 'Q_forced_ports')
        check(qmodels == 244, 'Q_model_count')
    for name, F in cases:
        comp = u.compile22(F)
        y = encode(comp.clauses)
        D = decode_image(y)
        check(D is not None, 'image_acceptance')
        assert D is not None
        check(D.balanced == comp.balanced, 'balanced_inverse')
        check(u.balance(D.balanced)[0] == D.balanced, 'balance_idempotence')
        check(encode(u.compile22(D.balanced).clauses) == y, 'recompile_identity')
        check(len(comp.clauses) == 12 * len(D.balanced), 'clause_count_ratio')
        check(D.clone_map[1:] == [comp.clone_to_balanced[z] for z in range(1, comp.R + 1)],
              'clone_map_recovery')
        fiber = preimages(D, deadline)
        check(F in fiber and D.balanced in fiber, 'entire_fiber_contains_sources')
        for P in fiber:
            check(u.balance(P)[0] == D.balanced, 'preimage_recheck')
        check(len(fiber) <= 1 + min((len(D.balanced)-1)//7, (comp.balanced_n-3)//5),
              'fiber_size_bound')
        check(comp.padding_gadgets == 0 or (F != D.balanced and len(fiber) >= 2),
              'noninjectivity_control')
        # Target reorderings/renamings preserve SAT and exact-(2,2), but not ordered image membership.
        mb = len(D.balanced)
        swapped = list(comp.clauses)
        swapped[mb], swapped[mb+1] = swapped[mb+1], swapped[mb]
        check(decode_image(encode(swapped)) is None, 'clause_order_scope')
        rename = [tuple((1 if l>0 else -1)*(2 if abs(l)==1 else 1 if abs(l)==2 else abs(l))
                        for l in c) for c in comp.clauses]
        check(decode_image(encode(rename)) is None, 'variable_rename_scope')
        complement = [tuple(-l if abs(l)==1 else l for l in c) for c in comp.clauses]
        check(decode_image(encode(complement)) is None, 'variable_complement_scope')
        literals = list(comp.clauses)
        literals[mb] = tuple(reversed(literals[mb]))
        check(decode_image(encode(literals)) is None, 'literal_order_scope')
        corrupted = list(comp.clauses)
        corrupted[-1] = tuple(-l for l in corrupted[-1])
        check(decode_image(encode(corrupted)) is None, 'full_recompile_guard')
        check(decode_image(y+b' ') is None, 'noncanonical_byte_padding')
        check(decode_image(bytes(bytearray(y))).balanced == D.balanced, 'COPY_wrapper')
        check(decode_image(encode(json.loads(y))).balanced == D.balanced, 'INTERP_wrapper')
        if comp.source_n <= 6:
            for bits in itertools.product((0, 1), repeat=comp.source_n):
                values = dict(enumerate(bits, 1))
                check(u.eval_cnf(F, values) == u.eval_cnf(comp.clauses, u.lift(comp, values)),
                      'all_source_assignments_section')
        rows.append({'case': name, 'm_source': len(F), 'n_source': comp.source_n,
                     'm_balanced': len(D.balanced), 'n_balanced': comp.balanced_n,
                     'm_target': len(comp.clauses), 'n_target': comp.n,
                     'target_bytes': len(y), 'balanced_bytes': len(encode(D.balanced)),
                     'fiber_source_clause_counts': [len(P) for P in fiber]})
    return {'run_id': RUN_ID, 'batch': batch, 'status': 'COMPUTATIONAL', 'seed': None,
            'method': 'exhaustive three-variable clause subsets' if batch=='exhaustive' else 'deterministic hostile controls',
            'assertions': sum(counts.values()), 'checks_by_group': dict(counts),
            'elapsed_seconds': time.monotonic()-start, 'rows': rows,
            'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'compiler_git_blob': blob_sha(Path(u.__file__)),
            'compiler_sha256': hashlib.sha256(Path(u.__file__).read_bytes()).hexdigest(),
            'limitations': ['Ordered byte encoding only; not anonymized/isomorphism image recognition.',
                           'A decoder is preprocessing, not a SAT decider or an arbitrary-execution lower bound.',
                           'Finite checks do not establish asymptotic complexity; independent proof review pending.',
                           'Input/output/clone maps are materialized; no subpolynomial-space claim.']}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', choices=('exhaustive', 'controls'), required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.batch), indent=2, sort_keys=True))
