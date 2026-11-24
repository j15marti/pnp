#!/usr/bin/env python3
"""QC01: reproducible finite controls for exact activation/repair guards.

Python 3.10+, standard library only. No SAT/NP complexity conclusion follows
from these finite tests. See the accompanying report for the symbolic proofs.

Run stages separately (each is designed to take less than about 30 seconds):
  python3 QC01_check.py --stage generic --output QC01_generic.json
  python3 QC01_check.py --stage cuts --output QC01_cuts.json
  python3 QC01_check.py --stage compiler --output QC01_compiler.json

Integers encode GF(2) column vectors, least significant bit = coordinate 0.
All Boolean witnesses and all rejection separators are explicitly verified.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import platform
import random
import resource
import sys
import time
from collections import Counter
from pathlib import Path


class Audit:
    def __init__(self):
        self.counts = Counter()

    def check(self, name, statement):
        self.counts[name] += 1
        if not statement:
            raise AssertionError(name)


def parity(x):
    return x.bit_count() & 1


def xors(values):
    out = 0
    for v in values:
        out ^= v
    return out


def bit_indices(mask):
    while mask:
        b = mask & -mask
        yield b.bit_length() - 1
        mask ^= b


def row_basis(rows):
    """Echelon basis for mask.dot(x)=rhs, or None on inconsistency."""
    basis = {}
    for mask, rhs in rows:
        while mask:
            p = mask.bit_length() - 1
            if p not in basis:
                basis[p] = (mask, rhs)
                break
            bm, br = basis[p]
            mask ^= bm
            rhs ^= br
        else:
            if rhs:
                return None
    return basis


def reduce_row(mask, rhs, basis):
    for p in sorted(basis, reverse=True):
        if (mask >> p) & 1:
            bm, br = basis[p]
            mask ^= bm
            rhs ^= br
    return mask, rhs


def row_solutions(rows, n):
    basis = row_basis(rows)
    if basis is None:
        return None
    free = [i for i in range(n) if i not in basis]

    def lift(free_word, homogeneous):
        word = free_word
        for p in sorted(basis):
            mask, rhs = basis[p]
            value = parity(mask & word) ^ (0 if homogeneous else rhs)
            word |= value << p
        return word

    return lift(0, False), [lift(1 << i, True) for i in free]


def rank(columns):
    return len(row_basis((x, 0) for x in columns))


def annihilator(columns, q):
    return row_solutions(((x, 0) for x in columns), q)[1]


def column_solve(columns, target):
    """Return a coefficient bit word, or None; no enumeration."""
    basis = {}
    for i, v in enumerate(columns):
        coefficient = 1 << i
        while v:
            p = v.bit_length() - 1
            if p not in basis:
                basis[p] = (v, coefficient)
                break
            bv, bc = basis[p]
            v ^= bv
            coefficient ^= bc
    coefficient = 0
    while target:
        p = target.bit_length() - 1
        if p not in basis:
            return None
        bv, bc = basis[p]
        target ^= bv
        coefficient ^= bc
    return coefficient


def repair(c, d, target, activation):
    rhs = target ^ xors(c[i] for i in bit_indices(activation))
    columns = [di if (activation >> i) & 1 else 0
               for i, di in enumerate(d)]
    return column_solve(columns, rhs)


def brute_repair(c, d, target, activation):
    """Independent exhaustive control over active repair bits."""
    rhs = target ^ xors(c[i] for i in bit_indices(activation))
    sub = activation
    while True:
        if xors(d[i] for i in bit_indices(sub)) == rhs:
            return sub
        if not sub:
            return None
        sub = (sub - 1) & activation


def separator(c, d, target, activation, q):
    rhs = target ^ xors(c[i] for i in bit_indices(activation))
    equations = [(d[i], 0) for i in bit_indices(activation)] + [(rhs, 1)]
    sol = row_solutions(equations, q)
    return None if sol is None else sol[0]


def guard(c, d, target, lam):
    support = sum(parity(lam & di) << i for i, di in enumerate(d))
    mask = sum(parity(lam & ci) << i for i, ci in enumerate(c))
    return support, mask, parity(lam & target)


def guard_holds(g, activation):
    support, mask, rhs = g
    return bool(support & activation) or parity(mask & activation) == rhs


def guarded_closure(c, d, target, q, pins=(), extra_lambdas=()):
    """Certified, incomplete polynomial closure for a supplied guard registry.

    Unconditional affine consequences: project away all not-forced-zero repair
    columns. Also propagate coordinate dual guards and supplied learned guards.
    A conditional parity equation is added only when its entire repair guard is
    certified off. Every deduction restarts the pass; stagnation is UNKNOWN.
    Pins are protected external conditions, never exported without the pins.
    """
    m = len(c)
    rows = [(1 << i, value) for i, value in pins]
    lambdas = sorted(set([1 << j for j in range(q)] + list(extra_lambdas)))
    passes = 0
    while True:
        passes += 1
        basis = row_basis(rows)
        if basis is None:
            return {"status": "UNSAT", "passes": passes, "rank": None,
                    "rows": rows, "pins": {}}
        known = {}
        for i in range(m):
            rem, value = reduce_row(1 << i, 0, basis)
            if not rem:
                known[i] = value
        allowed = [di for i, di in enumerate(d) if known.get(i) != 0]
        candidate_rows = []
        for lam in annihilator(allowed, q):
            _, mask, rhs = guard(c, d, target, lam)
            candidate_rows.append((mask, rhs))
        for lam in lambdas:
            support, mask, rhs = guard(c, d, target, lam)
            indices = list(bit_indices(support))
            if any(known.get(i) == 1 for i in indices):
                continue
            unknown = [i for i in indices if i not in known]
            rem, value = reduce_row(mask, rhs, basis)
            if not unknown:
                candidate_rows.append((mask, rhs))
            elif not rem and value == 1 and len(unknown) == 1:
                candidate_rows.append((1 << unknown[0], 1))
        added = False
        for mask, rhs in candidate_rows:
            rem, value = reduce_row(mask, rhs, basis)
            if not rem and not value:
                continue
            rows.append((mask, rhs))
            added = True
            break  # certified deduction, then restart closure immediately
        if not added:
            return {"status": "UNKNOWN", "passes": passes, "rank": len(basis),
                    "rows": list(basis.values()), "pins": known}
        if passes > m + 2:
            raise AssertionError("closure must add rank or derive contradiction")


def verify_lift(c, d, target, activation, repairs):
    m = len(c)
    # Recover the original punctured two-bit coordinates.
    u = activation
    v = ((1 << m) - 1) ^ activation ^ (activation & repairs)
    if any(not (((u >> i) & 1) or ((v >> i) & 1)) for i in range(m)):
        return False
    p = [ci ^ di for ci, di in zip(c, d)]
    source_target = target ^ xors(d)
    lhs = xors(p[i] for i in bit_indices(u)) ^ xors(d[i] for i in bit_indices(v))
    return lhs == source_target


def independent_basis_terminal(c, d, target):
    """Exact XP reference terminal from the preceding repair-basis lemma."""
    m = len(c)
    for size in range(rank(d) + 1):
        for inds in itertools.combinations(range(m), size):
            ds = [d[i] for i in inds]
            if rank(ds) != size:
                continue
            chosen = set(inds)
            free = [i for i in range(m) if i not in chosen
                    and column_solve(ds, d[i]) is not None]
            rhs = target ^ xors(c[i] for i in inds)
            coeff = column_solve([c[i] for i in free] + ds, rhs)
            if coeff is None:
                continue
            a = sum(1 << i for i in inds)
            a |= sum(((coeff >> j) & 1) << i for j, i in enumerate(free))
            b = repair(c, d, target, a)
            if b is None:
                raise AssertionError("basis terminal lift failed")
            return a, b
    return None


def generic_stage(audit):
    rng = random.Random(202611241515)
    cases = []
    # Complete one-bit syndrome systems with 1..3 factors.
    for m in range(1, 4):
        for word in itertools.product(range(4), repeat=m):
            c = [w & 1 for w in word]
            d = [(w >> 1) & 1 for w in word]
            for target in range(2):
                cases.append((c, d, target, 1, "exhaustive_q1"))
    for _ in range(240):
        m, q = rng.randint(1, 7), rng.randint(1, 6)
        c = [rng.randrange(1 << q) for _ in range(m)]
        d = [rng.randrange(1 << q) for _ in range(m)]
        cases.append((c, d, rng.randrange(1 << q), q, "seeded"))
    records = []
    counts = Counter()
    for ci, (c, d, target, q, mode) in enumerate(cases):
        m = len(c)
        closure = guarded_closure(c, d, target, q)
        all_guards = [guard(c, d, target, lam) for lam in range(1 << q)]
        gauges = rng.randrange(1 << m)
        shifted_c = [v ^ (d[i] if (gauges >> i) & 1 else 0)
                     for i, v in enumerate(c)]
        shifted_guards = [guard(shifted_c, d, target, lam) for lam in range(1 << q)]
        good = []
        for act in range(1 << m):
            b = repair(c, d, target, act)
            b0 = brute_repair(c, d, target, act)
            good_here = b is not None
            audit.check("linear_vs_exhaustive_repair", good_here == (b0 is not None))
            audit.check("all_dual_guards_exact", good_here == all(guard_holds(g, act) for g in all_guards))
            for g, sg in zip(all_guards, shifted_guards):
                audit.check("each_track_flip_guard_invariant", guard_holds(g, act) == guard_holds(sg, act))
            counts["activation_checks"] += 1
            if good_here:
                good.append(act)
                audit.check("source_lift", verify_lift(c, d, target, act, b))
                audit.check("closure_preserves_every_model", closure["status"] != "UNSAT" and all(parity(mask & act) == rhs for mask, rhs in closure["rows"]))
                counts["repairable_activations"] += 1
            else:
                lam = separator(c, d, target, act, q)
                audit.check("separation_exists", lam is not None)
                audit.check("separator_rejects_current", not guard_holds(guard(c, d, target, lam), act))
                audit.check("separator_annihilates_active_columns", all(not parity(lam & d[i]) for i in bit_indices(act)))
                counts["nonrepairable_activations"] += 1
        basis_result = independent_basis_terminal(c, d, target)
        audit.check("repair_basis_terminal", bool(good) == (basis_result is not None))
        if basis_result is not None:
            audit.check("basis_terminal_original_lift", verify_lift(c, d, target, *basis_result))
        # Each fully pinned query first invokes and saturates certified closure.
        chosen_act = rng.randrange(1 << m)
        pc = guarded_closure(c, d, target, q,
                             pins=[(i, (chosen_act >> i) & 1) for i in range(m)])
        audit.check("fully_pinned_closure_exact", (pc["status"] != "UNSAT") == (chosen_act in good))
        counts["SAT" if good else "UNSAT"] += 1
        records.append({"case": ci, "mode": mode, "c": c, "d": d,
                        "target": target, "q": q, "repairable_activations": len(good),
                        "closure": {k: closure[k] for k in ("status", "rank", "passes")}})
    return {"seed": 202611241515, "counts": dict(counts), "cases": records}


def parallel_paths(k):
    # Graph s-w_i-t. Coordinates 0=s, 1..k=w_i, k+1=t.
    d = []
    for i in range(k):
        d += [(1 << 0) ^ (1 << (i + 1)), (1 << (i + 1)) ^ (1 << (k + 1))]
    return [0] * (2 * k), d, (1 << 0) ^ (1 << (k + 1)), k + 2


def path_formula(activation, k):
    return any(((activation >> (2 * i)) & 3) == 3 for i in range(k))


def polynomial_eval_rank(points, n, degree):
    monomials = [mask for mask in range(1 << n) if mask.bit_count() <= degree]
    rows = [sum(int((x & mon) == mon) << j for j, mon in enumerate(monomials))
            for x in points]
    return len(monomials), rank(rows)


def cuts_stage(audit):
    records = []
    counts = Counter()
    for k in range(1, 9):
        c, d, target, q = parallel_paths(k)
        m = len(c)
        closures = guarded_closure(c, d, target, q)
        audit.check("path_closure_consistent", closures["status"] != "UNSAT")
        audit.check("no_unconditional_pin_k_ge_2", len(closures["pins"]) == (2 if k == 1 else 0))
        lambdas = [1 | (word << 1) for word in range(1 << k)]
        guards = [guard(c, d, target, lam) for lam in lambdas]
        cut_masks = [g[0] for g in guards]
        audit.check("distinct_minimal_cuts", len(set(cut_masks)) == (1 << k))
        audit.check("linear_dual_rank", rank(lambdas) == k + 1)
        audit.check("all_guard_degrees_k", all(x.bit_count() == k for x in cut_masks))
        # Each guard has a distinct degree-k leading monomial. This verifies
        # the finite leading-coefficient matrix is the identity.
        audit.check("independent_leading_monomials", len(set(cut_masks)) == len(guards))
        for j, cut in enumerate(cut_masks):
            act = ((1 << m) - 1) ^ cut
            violations = [h for h, g in enumerate(guards) if not guard_holds(g, act)]
            audit.check("exactly_one_cut_needed", violations == [j])
            audit.check("bad_neighbor_linear_unsat", repair(c, d, target, act) is None)
            pins = [(i, (act >> i) & 1) for i in range(m)]
            bc = guarded_closure(c, d, target, q, pins=pins)
            audit.check("bad_neighbor_closure_unsat", bc["status"] == "UNSAT")
            changed = act | (cut & -cut)
            good_pins = [(i, (changed >> i) & 1) for i in range(m)]
            gc = guarded_closure(c, d, target, q, pins=good_pins)
            b = repair(c, d, target, changed)
            audit.check("one_bit_sat_neighbor", b is not None and gc["status"] != "UNSAT")
            audit.check("one_bit_neighbor_source_lift", verify_lift(c, d, target, changed, b))
            counts["UNSAT_pinned_neighbors"] += 1
            counts["SAT_pinned_neighbors"] += 1
        point_checks = 0
        if k <= 6:
            for act in range(1 << m):
                expected = path_formula(act, k)
                audit.check("path_all_words_linear", (repair(c, d, target, act) is not None) == expected)
                audit.check("path_all_words_guard_cnf", all(guard_holds(g, act) for g in guards) == expected)
                point_checks += 1
        degrees = []
        if k <= 4:
            points = [a for a in range(1 << m) if path_formula(a, k)]
            for degree in (k - 1, k):
                dim, r = polynomial_eval_rank(points, m, degree)
                nullity = dim - r
                audit.check("exact_low_degree_consequence_dimension", nullity == (0 if degree < k else (1 << k)))
                degrees.append({"degree": degree, "monomials": dim,
                                "evaluation_rank": r, "vanishing_dimension": nullity})
        counts["all_activation_checks"] += point_checks
        records.append({"k": k, "vertices": q, "activation_variables": m,
                        "repair_rank": rank(d), "dual_guard_count": len(guards),
                        "dual_direction_span_rank": rank(lambdas),
                        "necessary_guard_leading_rank": len(set(cut_masks)),
                        "binary_gates_in_compact_relation": 2 * k - 1,
                        "all_activation_checks": point_checks,
                        "low_degree_controls": degrees,
                        "closure_pins": len(closures["pins"])})
    return {"counts": dict(counts), "families": records}


def compile_cnf(clauses):
    """Exact affine activation gluing + one rank-one repair block per clause.

    For every occurrence l of signed variable x use a_l=x XOR negative(l).
    Consecutive occurrences of each source variable are equated with phases.
    A clause j requires XOR_l a_l*b_l=1.
    """
    occurrences = [(j, lit) for j, clause in enumerate(clauses) for lit in clause]
    m_clauses = len(clauses)
    c = [0] * len(occurrences)
    d = [1 << j for j, _ in occurrences]
    target = (1 << m_clauses) - 1
    last = {}
    rows = []
    row_id = m_clauses
    for i, (_, lit) in enumerate(occurrences):
        var, neg = abs(lit), int(lit < 0)
        if var in last:
            previous, pneg = last[var]
            c[previous] ^= 1 << row_id
            c[i] ^= 1 << row_id
            target ^= (neg ^ pneg) << row_id
            rows.append(((1 << previous) | (1 << i), neg ^ pneg))
            row_id += 1
        last[var] = (i, neg)
    return c, d, target, row_id, occurrences, rows


def source_satisfies(clauses, x):
    return all(any(((x >> (abs(lit) - 1)) & 1) ^ (lit < 0) for lit in clause)
               for clause in clauses)


def source_activation(occurrences, x):
    return sum((((x >> (abs(lit) - 1)) & 1) ^ (lit < 0)) << i
               for i, (_, lit) in enumerate(occurrences))


def compiler_stage(audit):
    cube = [tuple(-(i + 1) if (word >> i) & 1 else (i + 1) for i in range(3))
            for word in range(8)]
    cases = [("cube_subset", 3, [cube[j] for j in range(8) if (mask >> j) & 1])
             for mask in range(256)]
    fano_edges = [(1, 2, 3), (1, 4, 5), (1, 6, 7), (2, 4, 6),
                  (2, 5, 7), (3, 4, 7), (3, 5, 6)]
    fano = [cl for edge in fano_edges for cl in (edge, tuple(-v for v in edge))]
    cases.append(("fano_root", 7, fano))
    cases += [("fano_one_clause_neighbor", 7, fano[:j] + fano[j+1:]) for j in range(14)]
    cases += [("fano_one_nae_neighbor", 7, fano[:2*j] + fano[2*j+2:]) for j in range(7)]
    rng = random.Random(202611241516)
    for _ in range(120):
        n = rng.randint(3, 6)
        clauses = [tuple(v if rng.randrange(2) else -v for v in rng.sample(range(1, n+1), 3))
                   for _ in range(rng.randint(0, 32))]
        cases.append(("seeded_cnf", n, clauses))
    counts, records = Counter(), []
    for ci, (mode, n, clauses) in enumerate(cases):
        c, d, target, q, occs, copy_rows = compile_cnf(clauses)
        closure = guarded_closure(c, d, target, q)
        # Confirm that the affine copy chart contains exactly the source
        # degrees of freedom on variables that occur, without free copy bits.
        used = len({abs(lit) for _, lit in occs})
        audit.check("copy_chart_exact_rank", len(row_basis(copy_rows)) == len(occs) - used)
        model_count = 0
        for x in range(1 << n):
            act = source_activation(occs, x)
            expected = source_satisfies(clauses, x)
            b = repair(c, d, target, act)
            audit.check("cnf_per_assignment_equivalence", (b is not None) == expected)
            audit.check("source_copy_chart", all(parity(mask & act) == rhs for mask, rhs in copy_rows))
            counts["source_assignments"] += 1
            if b is not None:
                model_count += 1
                audit.check("compiled_punctured_source_lift", verify_lift(c, d, target, act, b))
                audit.check("compiler_closure_preserves_models", closure["status"] != "UNSAT" and all(parity(mask & act) == rhs for mask, rhs in closure["rows"]))
                # Explicit reverse map from the first occurrence of each var.
                reconstructed, seen = 0, set()
                for i, (_, lit) in enumerate(occs):
                    v = abs(lit)
                    val = ((act >> i) & 1) ^ (lit < 0)
                    if v not in seen:
                        reconstructed |= val << (v - 1)
                        seen.add(v)
                audit.check("reverse_original_cnf_witness", source_satisfies(clauses, reconstructed))
                counts["verified_source_lifts"] += 1
        if mode == "fano_root":
            audit.check("fano_root_unsat", model_count == 0)
        if mode == "fano_one_clause_neighbor":
            audit.check("fano_owner_neighbor_five", model_count == 5)
        if mode == "fano_one_nae_neighbor":
            audit.check("fano_nae_neighbor_ten", model_count == 10)
        # Before finite reference enumeration, the root closure above ran to
        # stagnation. Re-run to verify an idempotent fixed point, not completion.
        again = guarded_closure(c, d, target, q)
        audit.check("closure_fixed_point_replay", closure == again)
        counts["SAT" if model_count else "UNSAT"] += 1
        counts["closure_" + closure["status"]] += 1
        records.append({"case": ci, "family": mode, "source_variables": n,
                        "clauses": clauses, "source_model_count": model_count,
                        "activation_variables": len(occs), "syndrome_dimension": q,
                        "repair_rank": rank(d), "local_repair_rank": int(bool(clauses)),
                        "closure_status": closure["status"], "closure_rank": closure["rank"],
                        "closure_pins": len(closure["pins"])})
    return {"seed": 202611241516, "counts": dict(counts), "cases": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("generic", "cuts", "compiler"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    audit = Audit()
    start = time.perf_counter()
    data = {"generic": generic_stage, "cuts": cuts_stage, "compiler": compiler_stage}[args.stage](audit)
    elapsed = time.perf_counter() - start
    result = {"status": "PASS", "stage": args.stage,
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "python": sys.version, "platform": platform.platform(),
              "elapsed_seconds": elapsed,
              "process_max_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              "cumulative_memory_measured": False,
              "assertions": dict(audit.counts), "assertion_total": sum(audit.counts.values()),
              "data": data,
              "limitations": ["Finite controls do not prove asymptotics.",
                "Reference enumeration is charged experimental work, not a polynomial solver.",
                "Certified closure is an explicit incomplete repertoire; UNKNOWN is not UNSAT.",
                "No strict E4/B4 physical compiler or full cooperative portfolio executed.",
                "No Lean/formal proof kernel or external solver used."]}
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"stage": args.stage, "status": "PASS", "assertions": result["assertion_total"],
                      "counts": data["counts"], "elapsed_seconds": elapsed,
                      "rss_kib": result["process_max_rss_kib_linux"], "output": str(args.output)}))


if __name__ == "__main__":
    main()
