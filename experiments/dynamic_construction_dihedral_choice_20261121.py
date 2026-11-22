#!/usr/bin/env python3
"""Build and audit shared-selector dihedral compatibility CNFs. Run at repo root.

Uses the pinned repository serializer/parser and the Z3 C library for an
independent decision check on the decoded target clauses. No randomness.
"""
import ctypes
import ctypes.util
from collections import Counter
from hashlib import sha256
from itertools import product
import json

import dynamic_synthesis_reachable_splice_20261121 as codec


def word(clause):
    """Execute from left to right. Each pair is (literal, active action)."""
    instructions = [(clause[0], "plus")]
    inverse = {"plus": "minus", "minus": "plus", "reflect": "reflect"}
    for literal in clause[1:]:
        reflection = [(literal, "reflect")]
        undo = [(old, inverse[action]) for old, action in reversed(instructions)]
        instructions = instructions + reflection + undo + reflection
    return instructions


def step(instruction, bit, vertex, width):
    literal, action = instruction
    if bit == (literal > 0):
        return vertex
    if action == "reflect":
        return (-vertex) % width
    return (vertex + (1 if action == "plus" else -1)) % width


def build(mod, clauses):
    if not clauses or any(len(c) != 3 or len({abs(x) for x in c}) != 3 for c in clauses):
        raise ValueError("expected nonempty proper 3-CNF")
    names = {abs(x) for c in clauses for x in c}
    if names != set(range(1, len(names) + 1)):
        raise ValueError("expected dense positive variable identifiers")
    d, c = len(names), len(clauses)
    r = max(3, 2 * ((c + 1) // 2) + 1)
    program = [instruction for clause in clauses for instruction in word(clause)]
    length = len(program)

    def state(j, vertex):
        return d + 1 + j * r + vertex

    pad = state(length, r - 1) + 1
    n0 = pad + 1
    source = []
    pins = [state(0, 0)] + [-state(length, v) for v in range(1, r)]
    for pin in pins:
        source.extend((pin, a * pad, b * n0) for a, b in product((1, -1), repeat=2))
    for j, instruction in enumerate(program):
        selector = abs(instruction[0])
        for vertex in range(r):
            for bit in (0, 1):
                image = step(instruction, bit, vertex, r)
                guard = selector if bit == 0 else -selector
                source.append((-state(j, vertex), guard, state(j + 1, image)))
    assert len(source) == 4 * r + 2 * length * r
    target, n, y, _, _, alpha, beta = mod.compile_compatibility(source, n0)
    bits = mod.encode(target, n, y, alpha, beta, r)[0]
    return bits, program, r


def z3_result(rows, n):
    lib = ctypes.CDLL(ctypes.util.find_library("z3") or "libz3.so.4")
    ptr = ctypes.c_void_p
    signatures = {
        "Z3_mk_config": (ptr, []), "Z3_mk_context": (ptr, [ptr]),
        "Z3_del_context": (None, [ptr]), "Z3_del_config": (None, [ptr]),
        "Z3_eval_smtlib2_string": (ctypes.c_char_p, [ptr, ctypes.c_char_p]),
        "Z3_get_full_version": (ctypes.c_char_p, []),
    }
    for name, (result, args) in signatures.items():
        function = getattr(lib, name)
        function.restype, function.argtypes = result, args
    config = lib.Z3_mk_config()
    ctx = lib.Z3_mk_context(config)
    try:
        commands = [f"(declare-const v{i} Bool)" for i in range(1, n + 1)]
        for row in rows:
            args = " ".join(f"v{x}" if x > 0 else f"(not v{-x})" for x in row)
            commands.append(f"(assert (or {args}))")
        commands.append("(check-sat)")
        result = lib.Z3_eval_smtlib2_string(ctx, "\n".join(commands).encode()).decode().strip()
        return result, lib.Z3_get_full_version().decode()
    finally:
        lib.Z3_del_context(ctx)
        lib.Z3_del_config(config)


def audit(mod, name, clauses, compact=False):
    bits, program, r = build(mod, clauses)
    d = max(abs(x) for c in clauses for x in c)
    n, rows, alpha, beta, release = codec.parse(bits)
    m0 = 4 * r + 2 * len(program) * r
    n0 = d + (len(program) + 1) * r + 2
    assert n == n0 + m0 + 3 and len(rows) == 2 * m0 + 4 and release == n0 + 1
    assert len(bits) == 3*n + 2 + 2*((len(rows)+1).bit_length()-1) + 3*len(rows)*(n.bit_length()+1) + n.bit_length()
    assert sum(a != b for a, b in zip(alpha, beta)) == 1
    for row in rows:
        assignment = alpha if sum(x > 0 for x in row) <= 1 else beta
        assert any((assignment[abs(x)-1] == "1") == (x > 0) for x in row)
    endpoints = []
    for assignment in product((0, 1), repeat=d):
        bad = sum(all(assignment[abs(x)-1] != (x > 0) for x in c) for c in clauses)
        vertex = 0
        for instruction in program:
            vertex = step(instruction, assignment[abs(instruction[0])-1], vertex, r)
        assert vertex == 4 * bad % r and (vertex == 0) == (bad == 0)
        endpoints.append([bad, vertex])
    result, version = z3_result(rows, n)
    assert result == ("sat" if any(bad == 0 for bad, _ in endpoints) else "unsat")
    evidence = (dict(violations_histogram=sorted(Counter(bad for bad, _ in endpoints).items()))
                if compact else dict(violations_endpoint=endpoints))
    return bits, dict(name=name, clauses=clauses, r=r, L=len(program), n=n, m=len(rows),
                      N=len(bits), assignment_order="binary lexicographic", **evidence,
                      sha256_ascii_bits=sha256(bits.encode()).hexdigest(), z3=result, version=version)


def main():
    mod = codec.load_generator()
    signs = list(product((1, -1), repeat=3))
    all_rows = [tuple(i * sign for i, sign in enumerate(pattern, 1)) for pattern in signs]
    records = []
    for i, clause in enumerate(all_rows):
        records.append(audit(mod, f"single-{i}", [clause])[1])
    records.append(audit(mod, "all-eight", all_rows)[1])
    records.append(audit(mod, "four-selectors", [(1, -2, 4), (-4, 3, 2), (-1, -3, -4)])[1])
    base = all_rows[1:] + [(-1, 2, 3)] * 3
    original, record = audit(mod, "star-center", base)
    records.append(record)
    used = set()
    diffs = []
    for j in range(3):
        variant = base.copy()
        variant[7+j] = (1, 2, 3)
        bits, record = audit(mod, f"star-leaf-{j}", variant)
        records.append(record)
        changed = [i for i, (a, b) in enumerate(zip(original, bits)) if a != b]
        assert len(bits) == len(original) and changed and used.isdisjoint(changed)
        used.update(changed)
        diffs.append(changed)
    balanced = []
    for phase, multiplier in enumerate((1, 2, 4, 7)):
        sign = 1 if phase < 2 else -1
        literals = [sign * (1 + (multiplier*i + phase) % 15) for i in range(15)]
        balanced.extend(tuple(literals[i:i+3]) for i in range(0, 15, 3))
    assert len({tuple(sorted(row)) for row in balanced}) == 20
    counts = Counter(x for row in balanced for x in row)
    assert all(counts[i] == counts[-i] == 2 for i in range(1, 16))
    records.append(audit(mod, "balanced-15-20", balanced, compact=True)[1])
    return dict(status="COMPUTATIONAL", records=records, star_difference_offsets_zero_based=diffs)


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
