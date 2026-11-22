#!/usr/bin/env python3
"""Audit the strict-3CNF final-pin compiler and independent optimized levels."""
import hashlib
import itertools
import json
from pathlib import Path
from time import perf_counter


def compile_formula(h, n):
    p, x, a, b = range(n + 1, n + 5)
    f = [(p, x, a), (p, x, -a), (p, -x, b), (p, -x, -b)]
    for j, (l1, l2, l3) in enumerate(h):
        s = n + 5 + j
        f.extend([(-p, l1, s), (-s, l2, l3)])
    assert all(len(c) == len({abs(l) for l in c}) == 3 for c in f)
    return f, n + len(h) + 4, dict(p=p, x=x, a=a, b=b)


def masks(clauses):
    return [(sum(1 << (v - 1) for v in c if v > 0),
             sum(1 << (-v - 1) for v in c if v < 0)) for c in clauses]


def satisfies(a, cs):
    return all(a & positive or (~a) & negative for positive, negative in cs)


def find_model(clauses, n):
    cs = masks(clauses)
    for assignment in range(1 << n):
        if satisfies(assignment, cs):
            return assignment, assignment + 1
    return None, 1 << n


def residual(clauses, pins):
    output = []
    for c in clauses:
        if any(abs(l) in pins and pins[abs(l)] == (l > 0) for l in c):
            continue
        output.append(tuple(l for l in c if abs(l) not in pins))
    return output


def guard_core_size(guards, pins):
    cs = residual(guards, pins)
    var_ids = sorted({abs(l) for c in cs for l in c})
    remap = {v: j + 1 for j, v in enumerate(var_ids)}
    cs = [tuple(remap[abs(l)] if l > 0 else -remap[abs(l)] for l in c) for c in cs]
    for k in range(1, len(cs) + 1):
        for chosen in itertools.combinations(cs, k):
            if find_model(chosen, len(var_ids))[0] is None:
                return k
    return None


def main():
    started = perf_counter()
    universe = [tuple(sign * v for sign, v in zip(signs, (1, 2, 3)))
                for signs in itertools.product((-1, 1), repeat=3)]
    cases = []
    examined = 0
    for selection in range(1 << len(universe)):
        h = [c for i, c in enumerate(universe) if selection & (1 << i)]
        f, n_f, named = compile_formula(h, 3)
        hm, hc = find_model(h, 3)
        fm, fc = find_model(f, n_f)
        examined += hc + fc
        assert (hm is None) == (fm is None)
        failed_at_zero = [i for i, c in enumerate(masks(f)) if not satisfies(0, [c])]
        assert failed_at_zero == [0]
        cases.append({"h_mask": selection, "h_sat": hm is not None,
                      "f_sat": fm is not None, "n_f": n_f, "m_f": len(f)})
    h = universe
    f, n_f, named = compile_formula(h, 3)
    assert n_f == 15 and len(f) == 20
    model, count = find_model(f, n_f)
    examined += count
    assert model is None
    deletion_models = []
    for removed in range(len(f)):
        witness, work = find_model(f[:removed] + f[removed + 1:], n_f)
        examined += work
        assert witness is not None
        assert not satisfies(witness, masks([f[removed]]))
        deletion_models.append({"removed_row": removed,
                                "assignment_bits_v1_first": [(witness >> v) & 1 for v in range(n_f)]})
    release_order = [named['a']] + [v for v in range(1, n_f + 1)
                                    if v not in {named['a'], named['p'], named['x']}]
    release_order += [named['x'], named['p']]
    assert len(set(release_order)) == n_f
    levels = []
    for r in range(n_f + 1):
        pins = {v: 0 for v in range(1, n_f + 1) if v not in release_order[:r]}
        gmu = guard_core_size(f[:4], pins)
        if r == 0:
            assert gmu == 1
            mu = 1
        elif r <= 13:
            assert gmu == 2
            assert all(c for c in residual(f, pins))
            mu = 2
        elif r == 14:
            assert gmu == 4
            assert min(map(len, residual(f, pins))) >= 2
            mu = 4
        else:
            assert gmu is None
            mu = 20
        levels.append({"unknown_count": r, "erased": release_order[:r],
                       "remaining_pins": pins, "minimum_core_size": mu})
    data = {"status": "PASS", "scope": "complete finite compiler/control audit",
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "all_source_subsets_tested": len(cases),
            "sat_cases": sum(c['h_sat'] for c in cases),
            "unsat_cases": sum(not c['h_sat'] for c in cases),
            "assignments_examined_by_direct_search": examined,
            "cube_h": h, "compiled_formula": f, "variables": n_f,
            "clauses": len(f), "special_ids": named,
            "all_zero_violations": [0], "all_32768_assignments_rejected": True,
            "all_20_single_deletions_satisfiable": True,
            "deletion_models": deletion_models, "optimized_release_order": release_order,
            "independent_levels": levels, "source_subset_cases": cases,
            "seconds": perf_counter() - started}
    print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
