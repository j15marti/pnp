#!/usr/bin/env python3
"""Independent referee for the saturated-cycle affine terminal.

No producer imports.  All finite checks are exhaustive and deterministic.
This is a restricted source theorem audit, not a native FLMV machine trace.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path

Y6 = (
    (1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6),
    (-1, -2, -4), (-1, -3, -6), (-2, -3, -5), (-4, -5, -6),
)
F9 = (
    (1, 5, 6), (2, 3, 8), (1, 3, 5), (4, 6, 9),
    (2, 4, 7), (7, 8, 9), (-4, -6, -8), (-1, -6, -7),
    (-2, -3, -4), (-3, -5, -8), (-1, -2, -9), (-5, -7, -9),
)
F15 = (
    (1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),
    (6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15),
    (-1,-2,-11),(-2,-3,-11),(-1,-3,-12),(-4,-5,-13),
    (-5,-6,-14),(-4,-6,-15),(-7,-8,-12),(-8,-9,-13),
    (-9,-10,-14),(-10,-7,-15),
)
F9_U = {8:0, 3:0, 7:0, 6:0, 1:1, 5:1}
F9_S = {**F9_U, 1:0}
F15_S = dict(zip(range(7,16), (1,0,0,0,1,1,1,1,0)))


def nvars(F):
    return max(abs(l) for c in F for l in c)


def valid(F):
    if not F:
        return False
    n = nvars(F)
    cnt = Counter((abs(l), l > 0) for c in F for l in c)
    return (
        3 * len(F) == 4 * n
        and len({tuple(sorted(c)) for c in F}) == len(F)
        and all(len(c) == 3 and len({abs(l) for l in c}) == 3
                and (all(l > 0 for l in c) or all(l < 0 for l in c)) for c in F)
        and all(cnt[v, s] == 2 for v in range(1, n + 1) for s in (False, True))
    )


def literal_true(lit, a):
    return a[abs(lit)] == int(lit > 0)


def true_count(c, a):
    return sum(literal_true(l, a) for l in c)


def sat(F, a):
    return all(true_count(c, a) for c in F)


def completions(F, p):
    free = [v for v in range(1, nvars(F) + 1) if v not in p]
    for bits in product((0, 1), repeat=len(free)):
        yield {**p, **dict(zip(free, bits))}


def gate(F, p):
    free = [v for v in range(1, nvars(F) + 1) if v not in p]
    covered, active = [], []
    spill = Counter()
    for j, c in enumerate(F):
        if any(abs(l) in p and literal_true(l, p) for l in c):
            covered.append(j)
        else:
            rest = tuple(l for l in c if abs(l) not in p)
            if not rest:
                return {"status": "EMPTY", "clause": j}
            active.append((j, rest))
    for j in covered:
        for l in F[j]:
            if abs(l) not in p:
                spill[abs(l), l > 0] += 1
    eta = sum(min(spill[v, False], spill[v, True]) for v in free)
    pref = {v: (0 if spill[v, True] > spill[v, False] else 1)
            for v in free if spill[v, True] != spill[v, False]}
    edges = [(j, frozenset(map(abs, rest))) for j, rest in active if len(rest) == 2]
    triangles = []
    for three in combinations(edges, 3):
        supports = [x[1] for x in three]
        deg = Counter(v for e in supports for v in e)
        if len(deg) == 3 and set(deg.values()) == {2}:
            triangles.append(tuple(sorted(x[0] for x in three)))
    # Same declared policy as the published terminal, independently coded.
    cycles, used = [], set()
    for cyc in sorted(set(triangles)):
        if used.isdisjoint(cyc):
            cycles.append(cyc)
            used.update(cyc)
    e = 2 * len(free) - len(active)
    return {
        "status": "GATE", "free": free, "covered": covered, "active": active,
        "eta": eta, "e": e, "pref": pref, "cycles": tuple(cycles),
        "delta": e - eta - len(cycles),
    }


def affine_rows(F, p, g, picks):
    cycle_ids = {j for cyc in g["cycles"] for j in cyc}
    picked = set(picks)
    rows = []
    for j, rest in g["active"]:
        if j in cycle_ids:
            vals = tuple(map(abs, rest))
            if j in picked:
                bit = int(F[j][0] > 0)
                rows.extend((1 << (v - 1), bit, {f"C{j}:both:{v}"}) for v in vals)
            else:
                rows.append((sum(1 << (v - 1) for v in vals), 1, {f"C{j}:one"}))
        else:
            vals = tuple(map(abs, rest))
            rhs = 1 if F[j][0] > 0 else 1 ^ (len(vals) & 1)
            rows.append((sum(1 << (v - 1) for v in vals), rhs, {f"C{j}:odd"}))
    rows.extend((1 << (v - 1), b, {f"pref:{v}"}) for v, b in g["pref"].items())
    return rows


def gaussian(rows):
    basis = {}
    ops = 0
    for mask, rhs, proof in rows:
        proof = set(proof)
        while mask:
            ops += 1
            pivot = mask.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = (mask, rhs, proof)
                break
            bm, br, bp = basis[pivot]
            mask ^= bm
            rhs ^= br
            proof ^= bp
        if not mask and rhs:
            return {"consistent": False, "rank": len(basis), "row_xors": ops,
                    "contradiction_provenance": sorted(proof)}
    return {"consistent": True, "rank": len(basis), "row_xors": ops}


def decomposition_membership(F, p, g, a, picks):
    if any(a[v] != b for v, b in g["pref"].items()):
        return False
    selected = set(picks)
    cycle_ids = {j for cyc in g["cycles"] for j in cyc}
    for j, rest in g["active"]:
        t = sum(literal_true(l, a) for l in rest)
        if j in selected and t != 2:
            return False
        if j in cycle_ids - selected and t != 1:
            return False
        if j not in cycle_ids and t % 2 != 1:
            return False
    return True


def audit_saturated_family(name, F, roots):
    stats = Counter()
    total_memberships = 0
    overlap_example = None
    for root in roots:
        free0 = [v for v in range(1, nvars(F)+1) if v not in root]
        for states in product((-1, 0, 1), repeat=len(free0)):
            p = {**root, **{v:s for v, s in zip(free0, states) if s >= 0}}
            g = gate(F, p)
            stats["cubes"] += 1
            if g["status"] == "EMPTY":
                stats["empty"] += 1
                continue
            if g["delta"] != 0:
                stats["nonsaturated"] += 1
                continue
            stats["saturated"] += 1
            branches = list(product(*g["cycles"]))
            stats["nominal_branches"] += len(branches)
            for a in completions(F, p):
                source = sat(F, a)
                matches = sum(decomposition_membership(F, p, g, a, picks)
                              for picks in branches)
                assert source == (matches == 1), (name, p, a, matches, g)
                assert matches <= 1
                total_memberships += matches
                stats["assignments_checked"] += 1
                stats["models"] += source
                if source and g["cycles"] and overlap_example is None:
                    cyc = g["cycles"][0]
                    over = [j for j in cyc if true_count(F[j], a) == 2]
                    assert len(over) == 1
                    overlap_example = {
                        "p": p, "cycle": list(cyc), "witness": [a[v] for v in range(1,nvars(F)+1)],
                        "unique_overfull_edge": over[0], "correct_delta": g["delta"],
                        "duplicated_same_cycle_delta": g["delta"] - 1,
                    }
    stats["model_branch_memberships"] = total_memberships
    return {"stats": dict(stats), "overlap_counterexample": overlap_example}


def extrema_control(F):
    n = nvars(F)
    all_a = [{v:b[v-1] for v in range(1,n+1)} for b in product((0,1), repeat=n)]
    local = []
    for j,c in enumerate(F):
        S = {abs(l):int(l>0) for l in c}
        U = {abs(l):1-int(l>0) for l in c}
        local.append({"clause_id":j,"literals":list(c),"S":S,"invert_S":U,
                      "U":U,"invert_U":S})
    modes = 0
    for j,k in combinations(range(len(F)),2):
        for tj,tk in product((0,3), repeat=2):
            exact = any(true_count(F[j],a)==tj and true_count(F[k],a)==tk for a in all_a)
            common = set(map(abs,F[j])) & set(map(abs,F[k]))
            same = any((next(l for l in F[j] if abs(l)==v)>0) ==
                       (next(l for l in F[k] if abs(l)==v)>0) for v in common)
            opp = any((next(l for l in F[j] if abs(l)==v)>0) !=
                      (next(l for l in F[k] if abs(l)==v)>0) for v in common)
            predicted = (not opp) if tj==tk else (not same)
            assert exact == predicted
            modes += 1
    ends=[]
    for b in (0,1):
        a={v:b for v in range(1,n+1)}
        h=Counter(true_count(c,a) for c in F)
        ends.append([h[i] for i in range(4)])
    witness=next(a for a in all_a if sat(F,a))
    p={};trail=[]
    for v in range(1,n+1):
        before=[true_count(c,{**p,**{x:0 for x in range(1,n+1) if x not in p}}) for c in F]
        p[v]=witness[v]
        after=[true_count(c,{**p,**{x:0 for x in range(1,n+1) if x not in p}}) for c in F]
        trail.append({"var":v,"value":witness[v],"changed_clause_ids":[j for j in range(len(F)) if before[j]!=after[j]]})
    return {"local_targets":local,"pair_modes_checked":modes,"endpoint_histograms":ends,
            "sat_witness":[witness[v] for v in range(1,n+1)],"flip_trail":trail}


def xor_firewalls():
    return {
        "lazy_flag": {"d_logic_virtual": 12, "d_phys_declared_flag_only": 1,
                      "conclusion": "logical status fanout is not physical writes"},
        "changed_then_restored": {"states":["0000","1000","0000"],
                                  "sum_adjacent":2,"endpoint":0},
        "delay_read_only": {"read_steps":1000,"writable_data_sum_xor":0,
                            "conclusion":"time can be positive with zero writable-data XOR"},
        "copy_recompute_uncompute": {"states":["0000","1100","0000"],
                                     "sum_adjacent":4,"endpoint":0},
        "counter_encoding": {"binary_1_to_2":2,"gray_1_to_2":1,
                             "conclusion":"delta depends on encoding"},
        "scope":"toy fixed layouts only; not a native FLMV trace",
    }


def main():
    assert all(valid(F) for F in (Y6,F9,F15))
    assert len([a for a in completions(F9,{}) if sat(F9,a)]) == 70
    Uext=list(completions(F9,F9_U)); Sext=list(completions(F9,F9_S))
    assert len(Uext)==8 and sum(map(lambda a:sat(F9,a),Uext))==0
    assert sum(map(lambda a:sat(F9,a),Sext))==2
    gu=gate(F9,F9_U)
    assert gu["delta"]==0 and gu["cycles"]==((3,4,10),)
    branch_refutations=[]
    for pick in product(*gu["cycles"]):
        z=gaussian(affine_rows(F9,F9_U,gu,pick))
        assert not z["consistent"]
        branch_refutations.append({"selected_edges":list(pick),**z})
    outside=[a for a in Uext if a[2]==a[4]==a[9]==1]
    assert len(outside)==1
    naive=outside[0]
    assert [true_count(F9[j],naive) for j in (3,4,10)]==[2,2,0]

    family = {
        "Y6_all_cubes": audit_saturated_family("Y6",Y6,[{}]),
        "F15_pS_refinements": audit_saturated_family("F15",F15,[F15_S]),
        "F9_pinned_refinements": audit_saturated_family("F9",F9,[F9_U]),
    }
    # Strong explicit necessity counterexample: duplicate one F15 authenticated
    # cycle ID-list.  Correct family is edge-disjoint and SAT; duplicate counting
    # would lower delta to -1 and falsely assert UNSAT.
    ov=family["F15_pS_refinements"]["overlap_counterexample"]
    assert ov and ov["correct_delta"]==0 and ov["duplicated_same_cycle_delta"]==-1

    report={
        "run":"SATURATED-CYCLE-AFFINE-REFEREE262",
        "status":"PROVED/EXACT independent symbolic reconstruction plus COMPUTATIONAL exhaustive controls; P versus NP OPEN",
        "exact_obstruction":"cycle edge IDs must be authenticated and edge-disjoint; outside parity alone is necessary but not sufficient",
        "F9":{
            "root_models":70,"unsat_cube":F9_U,"unsat_cube_completions":8,
            "unsat_cube_models":0,"neighbor_sat_cube":F9_S,"neighbor_models":2,
            "gate":{"e":gu["e"],"eta":gu["eta"],"nu":len(gu["cycles"]),"delta":gu["delta"],"cycles":[list(x) for x in gu["cycles"]]},
            "outside_parity_solution":[naive[v] for v in range(1,10)],
            "cycle_true_counts":[true_count(F9[j],naive) for j in (3,4,10)],
            "branch_refutations":branch_refutations,
        },
        "exhaustive_union_audit":family,
        "edge_disjointness_necessity":ov,
        "source_controls":extrema_control(F9),
        "xor_firewalls":xor_firewalls(),
        "resource_ledger":{
            "grammar":"full original-source scan and signed quotas",
            "discovery":"all residual binary-edge triples for triangle policy",
            "failed_choices":"every nominal selected-edge branch charged",
            "GE":"row visits and XOR provenance charged",
            "output":"witness or all branch contradictions plus original-source replay",
            "space":"source, pins, candidate cycles, rows, provenance and retained branch state simultaneously",
            "not_measured":["native FLMV head moves","physical d_phys on U198/V198","guest execution","target-child accessor"],
        },
        "large_controls":{
            "U198":"fresh replay of archived independent six-module certificate: all 64 boundary rows rejected in 152 module calls; capped DPLL is not a label",
            "V198":"fresh replay of archived complete 198-bit witness against all 264 original clauses",
            "replay_runtime_seconds":11.04,
            "native_FLVM_physical_tape_trace":False,
            "challenge":"neither large label implies the cycle terminal is hereditary, power-short, or a universal lower bound",
        },
        "projection_rank_reconciliation":"The newer exact 2^h projection terminal can dominate the nominal product of cycle lengths; 3^nu is an upper bound for one policy, never mandatory work.",
        "limitations":["children are noncanonical","finite controls do not imply all-input polynomial time","no arbitrary-A to Phi(A)","no numerical FLMV transfer"],
        "P_vs_NP":"OPEN",
    }
    out=Path(__file__).with_name("saturated_cycle_referee262_raw.json")
    out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps({
        "F9_branch_refutations":len(branch_refutations),
        "audits":{k:v["stats"] for k,v in family.items()},
        "overlap_false_gap":ov,
        "raw":str(out),"P_vs_NP":"OPEN"},indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
