#!/usr/bin/env python3
"""Checkpoint reachability audit, not an end-to-end TM timing experiment.

Uses the pinned transport generator, independently parses its bytes, authenticates
by exact regeneration, then simulates the three actual output transitions.
Run at repository root: python experiments/dynamic_synthesis_reachable_splice_20261121.py
"""
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import importlib.util
import json

DEP = Path(__file__).parent / 'charged_unsat_transport_20261121/charged_unsat_transport_audit.py'
EXPECTED = '98b46a013cabc3f969bcf58c08da2b1fd6937a26e1b46e75a06318e03d34d4f4'


def load_generator():
    assert sha256(DEP.read_bytes()).hexdigest() == EXPECTED
    spec = importlib.util.spec_from_file_location('transport', DEP)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build(mod, f, g):
    source, sn, _ = mod.source_formula(f, g)
    cs, n, y, _, _, alpha, beta = mod.compile_compatibility(source, sn)
    return mod.encode(cs, n, y, alpha, beta, len(f))


def parse(bits):
    if not bits or set(bits) - {'0', '1'}:
        raise ValueError('binary syntax')
    n = bits.find('0')
    if n < 1:
        raise ValueError('unary declaration')
    pos = n + 1
    start = pos
    while pos < len(bits) and bits[pos] == '0':
        pos += 1
    z = pos - start
    if pos + z + 1 > len(bits):
        raise ValueError('gamma truncation')
    m = int(bits[pos:pos + z + 1], 2) - 1
    pos += z + 1
    w = n.bit_length()
    if m < 0 or len(bits) != pos + 3*m*(w+1) + 2*n + w:
        raise ValueError('full encoded length')
    cs = []
    for _ in range(m):
        row = []
        for _ in range(3):
            sign = bits[pos]
            name = int(bits[pos+1:pos+1+w], 2)
            pos += w+1
            if not 1 <= name <= n:
                raise ValueError('identifier')
            row.append(name if sign == '0' else -name)
        if len(set(map(abs, row))) != 3:
            raise ValueError('proper clause')
        cs.append(tuple(row))
    alpha = bits[pos:pos+n]
    beta = bits[pos+n:pos+2*n]
    y = int(bits[pos+2*n:], 2)
    if not 1 <= y <= n:
        raise ValueError('release identifier')
    return n, cs, alpha, beta, y


def admit(mod, bits):
    try:
        n, cs, _, _, _ = parse(bits)
        if (n+1) % 8:
            return None
        r = (n+1)//8
        if r < 3 or len(cs) != 10*r:
            return None
        f = tuple(cs[5+4*i][1]-r for i in range(r))
        g = tuple(-cs[6*r+4*i+1][1]-r for i in range(r))
        regenerated = build(mod, f, g)[0]
        if regenerated != bits:
            return None
        return f, g, int(f != g)
    except (ValueError, IndexError):
        return None


def checkpoint(bits, answer):
    # Three-tuple symbols are one fixed finite tape alphabet, not RAM cells.
    return tuple((v, answer if i == 0 else None) for i, v in enumerate(bits))


def suffix(tape):
    tape = list(tape)
    head, state, trace = 0, 'READY', []
    while state != 'HALT':
        oldhead, read = head, tape[head]
        if state == 'READY':
            assert read[1] in (0, 1)
            tape[head] = (str(read[1]), None)
            head, state = 1, 'TERM'
        elif state == 'TERM':
            tape[head] = ('#', None)
            head, state = 0, 'RETURNED'
        else:
            state = 'HALT'
        trace.append((oldhead, read, tape[oldhead], head, state))
    return ''.join(x[0] for x in tape[:2]), trace, 3*(len(tape)+1)


def main():
    mod = load_generator()
    groups = []
    for r in (3, 4):
        ps = list(permutations(range(1, r+1)))
        diagonals = {p: build(mod, p, p) for p in ps}
        detail = []
        for f, g in product(ps, repeat=2):
            bits, left, middle, right = build(mod, f, g)
            assert admit(mod, bits) == (f, g, int(f != g))
            cut = len(left) + len(middle)//2
            left_state = checkpoint(diagonals[f][0], 0)
            right_state = checkpoint(diagonals[g][0], 0)
            mixed = left_state[:cut] + right_state[cut:]
            assert ''.join(s[0] for s in mixed) == bits
            genuine = checkpoint(bits, int(f != g))
            differing = [i for i, (x, y) in enumerate(zip(mixed, genuine)) if x != y]
            assert differing == ([] if f == g else [0])
            out, trace, cm = suffix(genuine)
            assert out == str(int(f != g)) + '#'
            assert len(trace) == 3
            assert all(max(t[0], t[3]) < cut for t in trace)
            stale_out, stale_trace, _ = suffix(mixed)
            assert stale_out == '0#'
            detail.append(dict(f=f, g=g, N=len(bits), cut=cut,
                               sat=bool(f != g), mixed_equals_actual=not differing,
                               differing_cells=differing, output=out,
                               mixed_output=stale_out, suffix_steps=len(trace),
                               suffix_span_cell_CM=cm, selected_cut_crossings=0,
                               input_sha256=sha256(bits.encode()).hexdigest()))
        groups.append(dict(r=r, diagonal_count=len(ps), pair_count=len(detail),
                           invalid_offdiagonal_splices=sum(x['sat'] for x in detail),
                           records=detail))
    # Nonpermutation map and malformed/admission controls. No UNKNOWN -> UNSAT.
    bits = build(mod, (1,1,1), (1,1,2))[0]
    assert admit(mod, bits) == ((1,1,1), (1,1,2), 1)
    base = build(mod, (1,2,3), (1,2,3))[0]
    # Valid syntax, changed witness metadata: rejected by exact authentication.
    n, _, _, _, _ = parse(base)
    w = n.bit_length()
    q = len(base)-w-2*n
    forged = base[:q] + str(1-int(base[q])) + base[q+1:]
    parse(forged)
    controls = [forged, base[:-1], base+'0', 'x'+base[1:]]
    assert all(admit(mod, c) is None for c in controls)
    return dict(lemma='DYNAMIC-REACHABLE-SPLICE1', status='COMPUTATIONAL',
                mode='exhaustive permutation pairs r=3,4; no random seed',
                scope='Exact encoded checkpoint states and three-step suffix only; prefix TM bound proved in report',
                generator_sha256=EXPECTED,
                script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                groups=groups, rejection_controls=len(controls), nonpermutation_controls=1)


if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
