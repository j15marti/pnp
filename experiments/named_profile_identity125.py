#!/usr/bin/env python3
"""Deterministic audit for LSPV-5 NAMED-PROFILE-IDENTITY125.

No external SAT package is used.  Clauses are tuples of signed integers.
The audit distinguishes source-anonymized 8-bit clause profiles from named
profiles (ordered variable-ID triples plus the same 8 bits).
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from typing import Dict, Iterable, List, Sequence, Tuple

Clause = Tuple[int, ...]
Formula = List[Clause]


def lit_value(lit: int, assignment: Dict[int, bool]) -> bool:
    v = assignment[abs(lit)]
    return v if lit > 0 else not v


def clause_value(clause: Clause, assignment: Dict[int, bool]) -> bool:
    return any(lit_value(lit, assignment) for lit in clause)


def formula_value(formula: Formula, assignment: Dict[int, bool]) -> bool:
    return all(clause_value(c, assignment) for c in formula)


def simplify(formula: Formula, var: int, val: bool) -> Formula | None:
    out: Formula = []
    for clause in formula:
        if (var if val else -var) in clause:
            continue
        reduced = tuple(l for l in clause if l != (-var if val else var))
        if not reduced:
            return None
        out.append(reduced)
    return out


def dpll(formula: Formula) -> Dict[int, bool] | None:
    formula = [tuple(dict.fromkeys(c)) for c in formula]
    assignment: Dict[int, bool] = {}

    def rec(cur: Formula, a: Dict[int, bool]) -> Dict[int, bool] | None:
        while True:
            unit = next((c[0] for c in cur if len(c) == 1), None)
            if unit is None:
                break
            var, val = abs(unit), unit > 0
            if var in a and a[var] != val:
                return None
            a = dict(a)
            a[var] = val
            nxt = simplify(cur, var, val)
            if nxt is None:
                return None
            cur = nxt
        if not cur:
            return a
        lit = cur[0][0]
        var = abs(lit)
        for val in (True, False):
            nxt = simplify(cur, var, val)
            if nxt is not None:
                b = dict(a)
                b[var] = val
                ans = rec(nxt, b)
                if ans is not None:
                    return ans
        return None

    return rec(formula, assignment)


def assignments3() -> Iterable[Tuple[int, int, int]]:
    return itertools.product((0, 1), repeat=3)


def profile(clause: Clause) -> str:
    assert len(clause) == 3 and len({abs(x) for x in clause}) == 3
    scope = tuple(abs(x) for x in clause)
    bits = []
    for row in assignments3():
        a = {scope[i]: bool(row[i]) for i in range(3)}
        bits.append("1" if clause_value(clause, a) else "0")
    return "".join(bits)


def named_profile(clause: Clause) -> Tuple[Tuple[int, int, int], str]:
    return tuple(abs(x) for x in clause), profile(clause)


def reconstruct(named: Tuple[Tuple[int, int, int], str]) -> Clause:
    scope, bits = named
    assert len(bits) == 8 and bits.count("0") == 1
    false_row = list(assignments3())[bits.index("0")]
    return tuple(-v if false_row[i] else v for i, v in enumerate(scope))


def transcript(formula: Formula, named: bool) -> list:
    if named:
        return [(list(scope), bits) for scope, bits in map(named_profile, formula)]
    return [profile(c) for c in formula]


def reconstruct_formula(named_transcript: list) -> Formula:
    return [reconstruct((tuple(scope), bits)) for scope, bits in named_transcript]


def unit_gadget(lit: int, a: int, b: int) -> Formula:
    return [
        (lit, a, b), (lit, a, -b),
        (lit, -a, b), (lit, -a, -b),
    ]


def canonical_clause(sign_mask: int) -> Clause:
    return tuple(-(i + 1) if (sign_mask >> i) & 1 else i + 1 for i in range(3))


def pin_child(clause: Clause, row: Tuple[int, int, int]) -> Formula:
    # Canonicalize source positions to 1,2,3, preserving signs.
    c = tuple(-(i + 1) if lit < 0 else i + 1 for i, lit in enumerate(clause))
    out: Formula = [c]
    for i, bit in enumerate(row):
        target = i + 1 if bit else -(i + 1)
        out.extend(unit_gadget(target, 4 + 2 * i, 5 + 2 * i))
    return out


def brute_sat_n(formula: Formula, n: int) -> bool:
    for row in itertools.product((False, True), repeat=n):
        a = {i + 1: row[i] for i in range(n)}
        if formula_value(formula, a):
            return True
    return False


def connected_collision() -> Tuple[Formula, Formula]:
    f = [tuple((-(i + 1) if (mask >> i) & 1 else i + 1) for i in range(3))
         for mask in range(8)]
    g: Formula = []
    for mask in range(8):
        base = 3 * mask + 1
        g.append(tuple((-(base + i) if (mask >> i) & 1 else base + i)
                       for i in range(3)))
    common = [(25, i, 27 + i) for i in range(1, 25)]
    common += unit_gadget(25, 26, 27)
    return f + common, g + common


def periodic_pair(m: int = 64) -> Tuple[Formula, Formula]:
    assert m % 16 == 0
    filler = (4, 5, 6)
    u, v = [filler for _ in range(m)], [filler for _ in range(m)]
    gap = m // 8
    for mask in range(8):
        u[mask * gap] = canonical_clause(mask)
        v[mask * gap] = canonical_clause(6 if mask == 7 else mask)
    return u, v


def minimal_pair(m: int = 5) -> Tuple[Formula, Formula, Dict[str, int]]:
    xs = list(range(1, m + 1))
    cs = list(range(m + 1, 2 * m))
    a0, b0, am, bm = 2 * m, 2 * m + 1, 2 * m + 2, 2 * m + 3
    f = unit_gadget(xs[0], a0, b0)
    for i in range(m - 1):
        f.extend([(-xs[i], xs[i + 1], cs[i]),
                  (-xs[i], xs[i + 1], -cs[i])])
    f.extend(unit_gadget(-xs[-1], am, bm))
    g = list(f)
    g[-4] = (-xs[-1], am, xs[0])
    return f, g, {"xm": xs[-1], "am": am, "bm": bm, "n": 2 * m + 3}


def gf2_consistent(equations: Sequence[Tuple[int, int]], n: int) -> bool:
    # Each row is (coefficient bitmask, rhs).
    rows = [[mask, rhs] for mask, rhs in equations]
    pivot = 0
    for col in range(n):
        q = next((r for r in range(pivot, len(rows)) if (rows[r][0] >> col) & 1), None)
        if q is None:
            continue
        rows[pivot], rows[q] = rows[q], rows[pivot]
        for r in range(len(rows)):
            if r != pivot and ((rows[r][0] >> col) & 1):
                rows[r][0] ^= rows[pivot][0]
                rows[r][1] ^= rows[pivot][1]
        pivot += 1
    return all(mask != 0 or rhs == 0 for mask, rhs in rows)


def main() -> None:
    checks = 0
    two_level_children = 0
    grandchild_statuses = 0

    # All signed proper clauses: named profiles are exactly invertible.
    for mask in range(8):
        c = canonical_clause(mask)
        assert reconstruct(named_profile(c)) == c
        checks += 1
        for row in assignments3():
            child = pin_child(c, row)
            expected = profile(c)[list(assignments3()).index(row)] == "1"
            assert brute_sat_n(child, 9) == expected
            checks += 1
            # A complete second-level named transcript reconstructs this child.
            t2 = transcript(child, named=True)
            assert reconstruct_formula(t2) == child
            checks += len(child)
            two_level_children += 1
            # Independently test every grandchild status, not merely clause eval.
            for cc in child:
                for r2 in assignments3():
                    gc = pin_child(cc, r2)
                    exp2 = profile(cc)[list(assignments3()).index(r2)] == "1"
                    assert brute_sat_n(gc, 9) == exp2
                    grandchild_statuses += 1

    # Role-3 connected same-anonymous-profile collision.
    cf, cg = connected_collision()
    assert len(cf) == len(cg) == 36
    assert transcript(cf, named=False) == transcript(cg, named=False)
    assert transcript(cf, named=True) != transcript(cg, named=True)
    assert reconstruct_formula(transcript(cf, True)) == cf
    assert reconstruct_formula(transcript(cg, True)) == cg
    for row in assignments3():
        assert not all(clause_value(c, {1: bool(row[0]), 2: bool(row[1]), 3: bool(row[2])})
                       for c in cf[:8])
    witness_g: Dict[int, bool] = {i: False for i in range(1, 52)}
    for mask, c in enumerate(cg[:8]):
        first = c[0]
        witness_g[abs(first)] = first > 0
    witness_g[25] = True
    assert formula_value(cg, witness_g)
    checks += 6 + 8

    # Role-4 periodic pair: isolated counts collide, named profiles do not.
    pu, pv = periodic_pair()
    assert dpll(pu) is None and dpll(pv) is not None
    assert transcript(pu, True) != transcript(pv, True)
    assert reconstruct_formula(transcript(pu, True)) == pu
    assert reconstruct_formula(transcript(pv, True)) == pv
    count_vectors = []
    for parent in (pu, pv):
        counts = []
        for j in range(64):
            window = [parent[(3 * j + i) % 64] for i in range(3)]
            cnt = sum(formula_value(window, {i + 1: row[i] for i in range(6)})
                      for row in itertools.product((False, True), repeat=6))
            counts.append(cnt)
        count_vectors.append(counts)
    assert count_vectors[0] == count_vectors[1]
    checks += 5 + 128 * 64

    # Minimal-UNSAT pair: named transcript identifies the altered scope/profile.
    mf, mg, ids = minimal_pair()
    assert len(mf) == len(mg) == 16
    assert dpll(mf) is None and dpll(mg) is not None
    mtf, mtg = transcript(mf, True), transcript(mg, True)
    diffs = [i for i, (a, b) in enumerate(zip(mtf, mtg)) if a != b]
    assert diffs == [12]
    assert reconstruct_formula(mtf) == mf and reconstruct_formula(mtg) == mg
    fresh = ids["n"] + 1
    pins = (unit_gadget(ids["xm"], fresh, fresh + 1) +
            unit_gadget(-ids["am"], fresh + 2, fresh + 3) +
            unit_gadget(-ids["bm"], fresh + 4, fresh + 5))
    assert dpll(mf + pins) is None and dpll(mg + pins) is not None
    checks += 8

    # Adaptive easy controls: no label oracle chooses the representation.
    controls = {
        "horn_sat": dpll([(-1, -2, 3), (-3, 4), (1,)]) is not None,
        "horn_unsat": dpll([(1,), (-1,)]) is None,
        "two_sat_sat": dpll([(1, 2), (-1, 2), (1, -2)]) is not None,
        "two_sat_unsat": dpll([(1, 2), (-1, 2), (1, -2), (-1, -2)]) is None,
        "affine_sat": gf2_consistent([(0b011, 1), (0b110, 0)], 3),
        "affine_unsat": not gf2_consistent([(0b001, 0), (0b001, 1)], 1),
        "decide_first_sat_token": int(dpll(mg) is not None) == 1,
        "decide_first_unsat_token": int(dpll(mf) is not None) == 0,
    }
    assert all(controls.values())
    checks += len(controls)

    # Exact payload accounting for the connected example, excluding headers.
    id_width = math.ceil(math.log2(51 + 1))
    named_payload_bits = 36 * (3 * id_width + 8)
    anonymous_payload_bits = 36 * 8

    result = {
        "claim": "NAMED-PROFILE-IDENTITY125",
        "status": "COMPUTATIONAL corroboration of symbolic restricted theorem",
        "checks": checks,
        "first_level_pin_children": 64,
        "two_level_reconstructions": two_level_children,
        "grandchild_sat_statuses": grandchild_statuses,
        "connected_pair": {
            "n": 51, "m": 36, "anonymous_profiles_equal": True,
            "named_profiles_equal": False, "labels": ["UNSAT", "SAT"],
            "anonymous_payload_bits": anonymous_payload_bits,
            "named_payload_bits_excluding_headers": named_payload_bits,
        },
        "periodic_pair": {
            "M": 64, "K": 3, "isolated_count_vectors_equal": True,
            "named_profiles_equal": False, "labels": ["UNSAT", "SAT"],
        },
        "minimal_pair": {
            "M": 16, "changed_named_profile_indices": diffs,
            "three_pin_labels": ["UNSAT", "SAT"],
        },
        "adaptive_controls": controls,
        "limitations": [
            "finite deterministic audit only",
            "named transcript is source-equivalent and does not give an ARC edge",
            "no unrestricted deterministic SAT lower bound",
        ],
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["canonical_sha256_without_hash_field"] = hashlib.sha256(canonical.encode()).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
