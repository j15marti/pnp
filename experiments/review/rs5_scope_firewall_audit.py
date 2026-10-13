#!/usr/bin/env python3
"""Independent bounded audit for RS5's same-row and scope firewall.

This does not prove the asymptotic spread theorem.  It checks:
  * the exact quantifier difference between forall z exists x and exists x forall z;
  * the strict-Resolution subclause pruning recursion on all small leaf families;
  * exact-rational feasibility margins for representative (p,beta) pairs.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from fractions import Fraction


def clause_for_assignment(vars_, bits):
    # literal (v, sign); sign True means positive. Clause is falsified by bits.
    return frozenset((v, not bool(bit)) for v, bit in zip(vars_, bits))


def resolve(c0, c1, pivot):
    pos = (pivot, True)
    neg = (pivot, False)
    if pos in c0 and neg in c1:
        a, b = c0, c1
    elif neg in c0 and pos in c1:
        a, b = c1, c0
    else:
        return None
    out = (a - {pos}) | (b - {neg})
    for v, s in out:
        if (v, not s) in out:
            raise AssertionError("tautological resolvent")
    return frozenset(out)


def prune(clauses, free_vars, prefix=()):
    if not free_vars:
        return clauses[prefix], 0, 0
    v = free_vars[0]
    left, dl, sl = prune(clauses, free_vars[1:], prefix + (0,))
    right, dr, sr = prune(clauses, free_vars[1:], prefix + (1,))
    # Complete falsified clauses place positive pivot at bit 0, negative at bit 1.
    if (v, True) not in left:
        return left, dl, sl + sr
    if (v, False) not in right:
        return right, dr, sl + sr
    out = resolve(left, right, v)
    assert out is not None
    return out, max(dl, dr) + 1, sl + sr + 1


def same_row_audit():
    checks = 0
    weak_only = 0
    examples = []
    # Relations R subset rows x outputs, sizes up to 4 x 4.
    for nr in range(1, 5):
        for nz in range(1, 5):
            universe = [(x, z) for x in range(nr) for z in range(nz)]
            for mask in range(1 << len(universe)):
                weak = all(any(mask & (1 << universe.index((x, z))) for x in range(nr))
                           for z in range(nz))
                strong = any(all(mask & (1 << universe.index((x, z))) for z in range(nz))
                             for x in range(nr))
                checks += 2
                assert not strong or weak
                if weak and not strong:
                    weak_only += 1
                    if len(examples) < 3:
                        examples.append({"rows": nr, "outputs": nz,
                                         "edges": [universe[i] for i in range(len(universe))
                                                   if mask & (1 << i)]})
    return checks, weak_only, examples


def subclause_audit():
    checks = 0
    skipped = 0
    # Up to four free variables.  Each leaf may be any subclause of its complete cube clause.
    for q in range(0, 5):
        vars_ = tuple(range(q))
        assignments = list(itertools.product((0, 1), repeat=q))
        full = {a: clause_for_assignment(vars_, a) for a in assignments}
        # Exhaust all families for q<=2; seeded deterministic families beyond.
        families = []
        if q <= 2:
            choices = [[frozenset(s) for r in range(len(full[a]) + 1)
                        for s in itertools.combinations(full[a], r)] for a in assignments]
            for selected in itertools.product(*choices):
                families.append(dict(zip(assignments, selected)))
        else:
            for seed in range(1024):
                fam = {}
                for ai, a in enumerate(assignments):
                    lits = sorted(full[a])
                    fam[a] = frozenset(lit for j, lit in enumerate(lits)
                                       if ((seed * 1103515245 + ai * 12345 + j * 97) >> (j % 13)) & 1)
                families.append(fam)
        for fam in families:
            out, depth, steps = prune(fam, vars_)
            checks += 4
            assert out == frozenset()
            assert depth <= q
            assert steps <= (1 << q) - 1
            for a, c in fam.items():
                assert c <= full[a]
            skipped += ((1 << q) - 1) - steps
    return checks, skipped


def parameter_audit():
    checks = 0
    rows = []
    pairs = [
        (Fraction(6, 5), Fraction(3, 2)),
        (Fraction(6, 5), Fraction(7, 4)),
        (Fraction(2, 1), Fraction(4, 3)),
        (Fraction(3, 1), Fraction(6, 5)),
        (Fraction(10, 1), Fraction(21, 20)),
    ]
    for p, beta in pairs:
        assert beta > 1 and beta < 1 + 1 / p
        rho = (beta - 1 + 1 / p) / 2
        g = 1 + rho - beta
        delta = g / (2 * (1 + rho))
        a = (4 * beta / g).numerator // (4 * beta / g).denominator
        if Fraction(a, 1) < 4 * beta / g:
            a += 1
        # Search an explicit fixed k, then c=floor(rho*k), satisfying strict margins.
        found = None
        for k in range(4, 2_000_000):
            c = (rho * k).numerator // (rho * k).denominator
            if not (3 <= c <= k - 1):
                continue
            q = 4 * a + c + 1
            u = a * (k + 4) + k
            z = Fraction(a, 1) * (1 - delta) * (k + c)
            if Fraction(k, 1) > p * q and z > beta * (u + 1):
                found = (k, c, q, u, z)
                break
        checks += 5
        assert found is not None
        k, c, q, u, z = found
        assert Fraction(k, 1) - p * q > 0
        assert z - beta * (u + 1) > 0
        rows.append({
            "p": str(p), "beta": str(beta), "rho": str(rho),
            "delta": str(delta), "a": a, "k": k, "c": c,
            "depth_margin": str(Fraction(k, 1) - p * q),
            "size_margin": str(z - beta * (u + 1)),
        })
    return checks, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    t0 = time.perf_counter()
    c1, gaps, examples = same_row_audit()
    c2, skipped = subclause_audit()
    c3, params = parameter_audit()
    payload = {
        "status": "pass",
        "candidate_falsified": "FORALL_OUTPUT_EXISTS_ROW_SUFFICES_FOR_ONE_STRIP",
        "candidate_retained": "EXISTS_ONE_ROW_FORALL_OUTPUTS_PLUS_ONE_SAVED_STRIP",
        "same_row_checks": c1,
        "weak_only_relations": gaps,
        "smallest_weak_only_examples": examples,
        "subclause_checks": c2,
        "skipped_resolution_inferences": skipped,
        "parameter_checks": c3,
        "parameter_rows": params,
        "total_checks": c1 + c2 + c3,
        "elapsed_seconds": round(time.perf_counter() - t0, 9),
        "scope": "finite audit; no asymptotic theorem or machine-time claim",
    }
    semantic = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["semantic_sha256"] = hashlib.sha256(semantic.encode()).hexdigest()
    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
