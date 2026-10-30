#!/usr/bin/env python3
"""Clause-indexed S/U inversion and globally coherent-search red-team audit.

Every benchmark is a proper signed 3-CNF.  Exact enumeration is used only as
an external oracle on small instances.  The instrumented solver is ordinary
fixed-order DPLL with saturated unit propagation; it is not industrial CDCL.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import random
import statistics
import time
from dataclasses import dataclass, asdict
from pathlib import Path

SEED = 202610292248
OUT = Path(__file__).with_name("2026-10-29_2248_EXTREME-COMPATIBILITY-FIREWALL214_raw.json")


def vars_of(clauses):
    return sorted({abs(l) for c in clauses for l in c})


def lit_true(lit, assignment):
    v = assignment[abs(lit)]
    return bool(v) if lit > 0 else not bool(v)


def clause_vector(clause, assignment):
    return tuple(int(lit_true(l, assignment)) for l in clause)


def status(clauses, assignment):
    vectors = [clause_vector(c, assignment) for c in clauses]
    counts = [sum(v) for v in vectors]
    nr = [counts.count(r) for r in range(4)]
    return {"vectors": ["".join(map(str, v)) for v in vectors],
            "true_literal_counts": counts, "N0_N1_N2_N3": nr,
            "formula_sat": nr[0] == 0}


def local_clause_record(j, clause):
    occ = []
    for p, lit in enumerate(clause):
        sign = "+" if lit > 0 else "-"
        s_value = 1 if lit > 0 else 0
        u_value = 1 - s_value
        occ.append({"occurrence": f"x_{{{abs(lit)},{j}}}", "position": p,
                    "variable": abs(lit), "explicit_sign": sign,
                    "literal": lit, "preferred_S_value": s_value,
                    "S_target": s_value, "invert_S_to_U": u_value,
                    "preferred_U_value": u_value, "U_target": u_value,
                    "invert_U_to_S": s_value})
    return {"source_clause_index": j, "clause": list(clause),
            "S_all_literals_true_target": {str(o["variable"]): o["S_target"] for o in occ},
            "inverted_S_is_U_target": {str(o["variable"]): o["invert_S_to_U"] for o in occ},
            "U_all_literals_false_target": {str(o["variable"]): o["U_target"] for o in occ},
            "inverted_U_is_S_target": {str(o["variable"]): o["invert_U_to_S"] for o in occ},
            "occurrences": occ}


def demands(clause, mode):
    # mode S means literal truth 1, U means literal truth 0.
    truth = 1 if mode == "S" else 0
    return {abs(l): truth ^ int(l < 0) for l in clause}


def merge_demands(items):
    merged, conflicts = {}, []
    for source, ds in items:
        for v, val in ds.items():
            if v in merged and merged[v][0] != val:
                conflicts.append({"variable": v, "first": merged[v], "second": [val, source]})
            else:
                merged[v] = [val, source]
    return ({v: val_src[0] for v, val_src in merged.items()}, conflicts)


def pair_matrix(j, cj, k, ck):
    shared = sorted(set(map(abs, cj)) & set(map(abs, ck)))
    same, opposite = [], []
    sj = {abs(l): l > 0 for l in cj}
    sk = {abs(l): l > 0 for l in ck}
    for v in shared:
        (same if sj[v] == sk[v] else opposite).append(v)
    matrix = {}
    for a, b in ("SS", "SU", "US", "UU"):
        merged, conflicts = merge_demands([(f"C{j}:{a}", demands(cj, a)),
                                            (f"C{k}:{b}", demands(ck, b))])
        matrix[a+b] = {"feasible": not conflicts, "witness_partial": merged if not conflicts else None,
                       "conflicts": conflicts}
    return {"source_clause_indices": [j, k], "shared_variables": shared,
            "same_polarity_shared": same, "opposite_polarity_shared": opposite,
            "matrix": matrix,
            "all_four_incompatible": all(not x["feasible"] for x in matrix.values())}


def enumerate_assignments(vs):
    for bits in itertools.product((0, 1), repeat=len(vs)):
        yield dict(zip(vs, bits))


def exact_pair_verify(cj, ck, matrix, vs):
    checks = 0
    for modes, cell in matrix.items():
        found = False
        for a in enumerate_assignments(vs):
            checks += 1
            vj, vk = clause_vector(cj, a), clause_vector(ck, a)
            if (vj == ((1,)*3 if modes[0] == "S" else (0,)*3)
                    and vk == ((1,)*3 if modes[1] == "S" else (0,)*3)):
                found = True
                break
        assert found == cell["feasible"]
    return checks


def multi_extreme_audit(clauses, vs, limit=8):
    """Exact check of simultaneous S/U targets on a bounded source subset."""
    idx = list(range(min(limit, len(clauses))))
    records, checks = [], 0
    for modes in itertools.product("SU", repeat=len(idx)):
        items = [(f"C{j}:{m}", demands(clauses[j], m)) for j, m in zip(idx, modes)]
        merged, conflicts = merge_demands(items)
        found = None
        for a in enumerate_assignments(vs):
            checks += 1
            ok = True
            for j, mode in zip(idx, modes):
                target = (1,1,1) if mode == "S" else (0,0,0)
                if clause_vector(clauses[j], a) != target:
                    ok = False; break
            if ok:
                found = a; break
        assert (found is not None) == (not conflicts)
        records.append({"modes": "".join(modes), "feasible": not conflicts,
                        "witness": found, "merged_demands": merged if not conflicts else None,
                        "conflicts": conflicts})
    return {"source_clause_subset": idx,
            "realizable_count": sum(r["feasible"] for r in records),
            "inconsistent_count": sum(not r["feasible"] for r in records),
            "mode_records": records}, checks


def all_resolvents(clauses, max_width=None):
    unique, records = {}, []
    pair_tests = literal_ops = 0
    for j, cj in enumerate(clauses):
        for k in range(j + 1, len(clauses)):
            ck = clauses[k]
            for lj in cj:
                for lk in ck:
                    pair_tests += 1
                    if lj != -lk:
                        continue
                    tail = [x for x in cj if x != lj] + [x for x in ck if x != lk]
                    literal_ops += len(tail)
                    if any(-x in tail for x in tail):
                        records.append({"parents": [j, k], "pivot": abs(lj),
                                        "status": "tautological", "raw_tail": tail})
                        continue
                    res = tuple(sorted(set(tail), key=lambda x: (abs(x), x < 0)))
                    if max_width is not None and len(res) > max_width:
                        records.append({"parents": [j, k], "pivot": abs(lj),
                                        "status": "over_width", "resolvent": list(res)})
                        continue
                    cube = {str(abs(l)): int(l < 0) for l in res}  # falsify each literal
                    rec = {"parents": [j, k], "pivot": abs(lj), "status": "kept",
                           "resolvent": list(res), "prohibited_cube": cube,
                           "proof": f"C{j},C{k}; resolve on x{abs(lj)}"}
                    records.append(rec)
                    unique.setdefault(res, rec)
    return list(unique), records, {"opposite_pair_tests": pair_tests, "literal_ops": literal_ops}


def extends_cube(a, cube):
    return all(a[int(v)] == val for v, val in cube.items())


@dataclass
class Counters:
    nodes: int = 0
    branches: int = 0
    clause_scans: int = 0
    literal_reads: int = 0
    propagations: int = 0
    conflicts: int = 0
    extreme_guard_pair_checks: int = 0
    extreme_guard_rejections: int = 0
    peak_assigned: int = 0


def unit_propagate(clauses, a, c):
    while True:
        changed = False
        for clause in clauses:
            c.clause_scans += 1
            sat, unassigned = False, []
            for lit in clause:
                c.literal_reads += 1
                v = abs(lit)
                if v not in a:
                    unassigned.append(lit)
                elif lit_true(lit, a):
                    sat = True
                    break
            if sat:
                continue
            if not unassigned:
                c.conflicts += 1
                return False
            if len(unassigned) == 1:
                lit = unassigned[0]
                v, val = abs(lit), int(lit > 0)
                if v in a and a[v] != val:
                    c.conflicts += 1
                    return False
                if v not in a:
                    a[v] = val
                    c.propagations += 1
                    c.peak_assigned = max(c.peak_assigned, len(a))
                    changed = True
                    break
        if not changed:
            return True


def extreme_guard(clauses, a, c):
    realized = []
    for j, clause in enumerate(clauses):
        if all(abs(l) in a for l in clause):
            vec = clause_vector(clause, a)
            if vec == (1, 1, 1): realized.append((j, "S"))
            if vec == (0, 0, 0): realized.append((j, "U"))
    for (j, mj), (k, mk) in itertools.combinations(realized, 2):
        c.extreme_guard_pair_checks += 1
        _, conflicts = merge_demands([(str(j), demands(clauses[j], mj)),
                                       (str(k), demands(clauses[k], mk))])
        if conflicts:
            c.extreme_guard_rejections += 1
            return False
    return True


def dpll(clauses, use_guard=False):
    vs = vars_of(clauses)
    c = Counters()
    def rec(a):
        c.nodes += 1
        c.peak_assigned = max(c.peak_assigned, len(a))
        a = dict(a)
        if not unit_propagate(clauses, a, c): return None
        if use_guard and not extreme_guard(clauses, a, c): return None
        if all(any(abs(l) in a and lit_true(l, a) for l in cl) for cl in clauses):
            return {v: a.get(v, 0) for v in vs}
        v = next(v for v in vs if v not in a)
        for val in (0, 1):
            c.branches += 1
            child = dict(a); child[v] = val
            ans = rec(child)
            if ans is not None: return ans
        return None
    model = rec({})
    return model, c


def work(c, preprocess=None):
    p = preprocess or {"opposite_pair_tests": 0, "literal_ops": 0}
    return (c.nodes + c.branches + c.clause_scans + c.literal_reads + c.propagations
            + c.conflicts + c.extreme_guard_pair_checks
            + p["opposite_pair_tests"] + p["literal_ops"])


def timed_solver(clauses, guard=False, repeat=7):
    samples = []; last = None
    for _ in range(repeat):
        t0 = time.perf_counter_ns(); last = dpll(clauses, guard)
        samples.append((time.perf_counter_ns() - t0) / 1000)
    return last, statistics.median(samples)


def strict22(n=6):
    assert n % 3 == 0
    cs = []
    for i in range(1, n + 1):
        nxt = i % n + 1; nxt2 = (i + 1) % n + 1
        cs.append((i, nxt, -nxt2))
    for i in range(1, n + 1, 3): cs.append((-i, -(i+1), -(i+2)))
    return cs


def parity3(rhs):
    # Forbid assignments whose parity differs from rhs.
    out = []
    for bits in itertools.product((0,1), repeat=3):
        if (sum(bits) & 1) != rhs:
            out.append(tuple((i+1) if bits[i] == 0 else -(i+1) for i in range(3)))
    return out


def dense_overlapping_xor(n=6):
    # Even parity on every triple.  The primal graph is K_n, hence treewidth n-1.
    out=[]
    for supp in itertools.combinations(range(1,n+1),3):
        for bits in itertools.product((0,1),repeat=3):
            if sum(bits)&1:
                out.append(tuple(supp[i] if bits[i]==0 else -supp[i] for i in range(3)))
    return out


def padded_unit(x, a, b):
    return [(x, a, b), (x, a, -b), (x, -a, b), (x, -a, -b)]


def planted_dense():
    rng = random.Random(SEED); vs = list(range(1,8)); planted = {v: (v % 2) for v in vs}
    pool = []
    for supp in itertools.combinations(vs,3):
        for signs in itertools.product((1,-1),repeat=3):
            c=tuple(v*s for v,s in zip(supp,signs))
            if any(lit_true(l,planted) for l in c): pool.append(c)
    rng.shuffle(pool); return pool[:28]


BENCH = {
 "mixed_both_endpoints_fail_sat": [(1,2,3),(1,2,-3),(-1,-2,-3)],
 "duplicate_support_dense_conflict_sat": [(1,2,3)]*4 + [(1,2,-3)]*4,
 "contradictory_padded_units_unsat": padded_unit(1,2,3)+padded_unit(-1,4,5),
 "xor3_even_sat": parity3(0),
 "xor3_even_odd_unsat": parity3(0)+parity3(1),
 "dense_overlapping_xor_K6_sat": dense_overlapping_xor(6),
 "horn_sat": [(-1,-2,3),(-3,-4,5),(-5,-1,-4),(-2,-4,-6)],
 "padded_2sat_sat": [(1,2,5),(1,2,-5),(-2,3,6),(-2,3,-6),(-3,4,7),(-3,4,-7)],
 "strict22_connected_sat": strict22(6),
 "all_signs_three_vars_unsat": [tuple((i+1) if bits[i]==0 else -(i+1) for i in range(3))
                                  for bits in itertools.product((0,1),repeat=3)],
 "planted_dense_sat": planted_dense(),
 "adversarial_polarity_renaming_sat": [tuple((-l if abs(l) in {1,3} else l) for l in c)
                                         for c in [(1,2,3),(1,2,-3),(-1,-2,-3)]],
}


def audit_formula(name, clauses):
    clauses = [tuple(c) for c in clauses]
    assert all(len(c)==3 and len({abs(l) for l in c})==3 for c in clauses)
    vs=vars_of(clauses); assigns=list(enumerate_assignments(vs))
    models=[a for a in assigns if status(clauses,a)["formula_sat"]]
    local=[local_clause_record(j,c) for j,c in enumerate(clauses)]
    multi, multi_checks = multi_extreme_audit(clauses,vs)
    pairs=[]; pair_checks=0
    for j,k in itertools.combinations(range(len(clauses)),2):
        p=pair_matrix(j,clauses[j],k,clauses[k])
        pair_checks += exact_pair_verify(clauses[j],clauses[k],p["matrix"],vs)
        pairs.append(p)
    # Every coherent full assignment realizes only compatible extreme pairs.
    coherent_extreme_checks=0
    for a in assigns:
        ext=[]
        for j,c in enumerate(clauses):
            v=clause_vector(c,a)
            if v==(1,1,1): ext.append((j,"S"))
            elif v==(0,0,0): ext.append((j,"U"))
        for (j,mj),(k,mk) in itertools.combinations(ext,2):
            coherent_extreme_checks += 1
            cell=next(p for p in pairs if p["source_clause_indices"]==[j,k])["matrix"][mj+mk]
            assert cell["feasible"]
    # Complement and flip identities.
    complement_checks=flip_checks=0
    for a in assigns:
        comp={v:1-a[v] for v in vs}
        sa=status(clauses,a); sb=status(clauses,comp)
        assert sb["true_literal_counts"] == [3-x for x in sa["true_literal_counts"]]
        assert sb["N0_N1_N2_N3"] == list(reversed(sa["N0_N1_N2_N3"]))
        complement_checks += len(clauses)
        for v in vs:
            b=dict(a); b[v]=1-b[v]
            before=sa["true_literal_counts"]
            after=status(clauses,b)["true_literal_counts"]
            for j,c in enumerate(clauses):
                if v not in map(abs,c): assert after[j]==before[j]
                else: assert abs(after[j]-before[j])==1
                flip_checks += 1
    # Endpoints and deterministic intermediate trails.
    zero={v:0 for v in vs}; one={v:1 for v in vs}
    trails=[]
    for label,start,order in [("0_to_1",zero,vs),("1_to_0",one,list(reversed(vs)))]:
        a=dict(start); steps=[]
        for step,v in enumerate([None]+order):
            if v is not None: a[v]=1-a[v]
            steps.append({"step":step,"flipped_variable":v,"assignment":"".join(str(a[x]) for x in vs),
                          **status(clauses,a)})
        trails.append({"trail":label,"steps":steps})
    # Resolutions and external exact cube certification.
    derived, recs, prep=all_resolvents(clauses,max_width=3)
    cube_checks=0
    for rec in recs:
        if rec["status"] != "kept": continue
        for a in assigns:
            if extends_cube(a,rec["prohibited_cube"]):
                cube_checks += 1
                j,k=rec["parents"]
                assert not (sum(clause_vector(clauses[j],a))>0 and sum(clause_vector(clauses[k],a))>0)
                assert not status(clauses,a)["formula_sat"]
    # Solver comparisons: conventional baseline, same search plus guard, bounded resolution.
    (m0,c0),t0=timed_solver(clauses,False)
    (mg,cg),tg=timed_solver(clauses,True)
    augmented=clauses+[tuple(r) for r in derived if tuple(r) not in clauses]
    (mr,cr),tr=timed_solver(augmented,False)
    truth=bool(models)
    assert (m0 is not None)==truth==(mg is not None)==(mr is not None)
    assert cg.extreme_guard_rejections==0 and cg.nodes==c0.nodes
    comp={
      "standard_fixed_order_UP_DPLL":{"model":m0,"counters":asdict(c0),"work_units":work(c0),"median_us_7":t0},
      "same_DPLL_plus_extreme_compatibility_guard":{"model":mg,"counters":asdict(cg),"work_units":work(cg),"median_us_7":tg,
         "pruned_nodes_relative_to_standard":c0.nodes-cg.nodes},
      "same_DPLL_plus_source_bounded_resolvents":{"model":mr,"counters":asdict(cr),
         "derived_clause_count":len(augmented)-len(clauses),"preprocess":prep,
         "work_units_including_preprocess":work(cr,prep),"median_us_7_excludes_preprocess":tr},
    }
    return {"name":name,"variables":vs,"source_clauses":[list(c) for c in clauses],
            "is_sat":truth,"model_count":len(models),"first_model":models[0] if models else None,
            "local_clause_extremes":local,"pair_extreme_compatibility":pairs,
            "multi_clause_extreme_compatibility":multi,
            "global_endpoints":{"0^n":status(clauses,zero),"1^n":status(clauses,one)},
            "intermediate_flip_trails":trails,"resolution_records":recs,
            "distinct_kept_bounded_resolvents":[list(x) for x in derived],
            "solver_comparison":comp,
            "checks":{"pair_exact_enumeration":pair_checks,"multi_extreme_exact_enumeration":multi_checks,
                      "coherent_extreme_pairs":coherent_extreme_checks,
                      "complement":complement_checks,"single_flip":flip_checks,"prohibited_cube_extensions":cube_checks}}


def main():
    t0=time.perf_counter(); reports=[audit_formula(n,c) for n,c in BENCH.items()]
    by_name={r["name"]:r for r in reports}
    total={k:sum(r["checks"][k] for r in reports) for k in reports[0]["checks"]}
    assertions={
      "all_guard_rejections_zero":all(r["solver_comparison"]["same_DPLL_plus_extreme_compatibility_guard"]["counters"]["extreme_guard_rejections"]==0 for r in reports),
      "all_guard_node_counts_equal_baseline":all(r["solver_comparison"]["same_DPLL_plus_extreme_compatibility_guard"]["counters"]["nodes"]==r["solver_comparison"]["standard_fixed_order_UP_DPLL"]["counters"]["nodes"] for r in reports),
      "both_endpoints_fail_but_sat": (not by_name["mixed_both_endpoints_fail_sat"]["global_endpoints"]["0^n"]["formula_sat"] and not by_name["mixed_both_endpoints_fail_sat"]["global_endpoints"]["1^n"]["formula_sat"] and by_name["mixed_both_endpoints_fail_sat"]["is_sat"]),
      "duplicate_conflict_family_easy_sat":by_name["duplicate_support_dense_conflict_sat"]["is_sat"] and by_name["duplicate_support_dense_conflict_sat"]["model_count"]==6,
      "xor_control_present":by_name["xor3_even_sat"]["is_sat"] and not by_name["xor3_even_odd_unsat"]["is_sat"],
      "dense_high_treewidth_xor_control_present":by_name["dense_overlapping_xor_K6_sat"]["is_sat"],
      "strict22_control_sat":by_name["strict22_connected_sat"]["is_sat"],
    }
    out={"run_id":"EXTREME-COMPATIBILITY-FIREWALL214","timestamp":"2026-10-29T22:48:00-07:00",
         "seed":SEED,"scope":"proper signed 3-CNF, exact enumeration only for small controls",
         "theorem_under_test":"An S/U compatibility guard cannot reject a globally coherent source-variable assignment; it only filters independently posited occurrence-level targets.",
         "total_checks":total,"assertions":assertions,"benchmark_count":len(reports),
         "elapsed_seconds":time.perf_counter()-t0,"benchmarks":reports,
         "limitations":["finite controls do not prove a general runtime bound",
                        "fixed-order UP+DPLL is conventional but not industrial CDCL",
                        "work units are instrumented logical operations, not tape crossings",
                        "resolution comparison retains only non-tautological width-at-most-3 resolvents"]}
    assert all(assertions.values())
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    digest=hashlib.sha256(OUT.read_bytes()).hexdigest()
    print(json.dumps({"output":str(OUT),"sha256":digest,"elapsed_seconds":out["elapsed_seconds"],
                      "total_checks":total,"assertions":assertions},indent=2))


if __name__=="__main__": main()
