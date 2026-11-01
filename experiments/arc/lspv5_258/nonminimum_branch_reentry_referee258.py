#!/usr/bin/env python3
"""REFEREE258: q=4 nonminimum critical-port branch re-entry.

Constructs a target-valid formula equisatisfiable with one raw Shannon
cofactor of any valid canonical target.  The construction grows by 201
variables and 268 clauses, so it is not an ARC contraction.
"""
from __future__ import annotations

import ast
import base64
import gzip
import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "tmp/doecker61_source.txt"
SUMMARY = ROOT / "results/raw/arc/2026-10-31_2248_LSPV5_NONMINIMUM_BRANCH_REENTRY_REFEREE258_raw.json"
FULL = ROOT / "results/raw/arc/2026-10-31_2248_LSPV5_NONMINIMUM_BRANCH_REENTRY_REFEREE258_raw.full.json"
ARCHIVE = ROOT / "results/raw/arc/2026-10-31_2248_LSPV5_NONMINIMUM_BRANCH_REENTRY_REFEREE258_raw.json.gz.b64"
V_WITNESS = "001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101"


def load_u():
    return ast.literal_eval("\n".join(x for x in SOURCE.read_text().splitlines() if not x.startswith("#")))


def y6():
    pos = [(1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6)]
    neg = [(1, 2, 4), (1, 3, 6), (2, 3, 5), (4, 5, 6)]
    return [list(c) for c in pos] + [[-x for x in c] for c in neg]


def valid_target(formula):
    if not formula:
        return False
    keys, occ = [], Counter()
    for clause in formula:
        if len(clause) != 3 or len({abs(x) for x in clause}) != 3:
            return False
        if not (all(x > 0 for x in clause) or all(x < 0 for x in clause)):
            return False
        keys.append(tuple(sorted(clause)))
        for lit in clause:
            occ[abs(lit), lit > 0] += 1
    variables = {abs(x) for clause in formula for x in clause}
    return len(keys) == len(set(keys)) and variables == set(range(1, max(variables) + 1)) and all(occ[v, s] == 2 for v in variables for s in (False, True))


def satisfies(formula, bits):
    return all(any((bits[abs(x) - 1] == "1") == (x > 0) for x in clause) for clause in formula)


def simplify(clauses, assignment, counter=None):
    out = []
    for clause in clauses:
        row, done = [], False
        for lit in clause:
            if counter is not None:
                counter["literal_tests"] += 1
            if abs(lit) in assignment:
                if assignment[abs(lit)] == (lit > 0):
                    done = True
                    break
            else:
                row.append(lit)
        if done:
            continue
        if not row:
            return None
        out.append(row)
    return out


def dpll_witness(clauses, assignment=None):
    assignment = {} if assignment is None else dict(assignment)
    clauses = simplify(clauses, assignment)
    if clauses is None:
        return None
    while True:
        unit = next((c[0] for c in clauses if len(c) == 1), None)
        if unit is None:
            break
        v, val = abs(unit), unit > 0
        if v in assignment and assignment[v] != val:
            return None
        assignment[v] = val
        clauses = simplify(clauses, {v: val})
        if clauses is None:
            return None
        if not clauses:
            return assignment
    if not clauses:
        return assignment
    pivot = abs(min(clauses, key=len)[0])
    for value in (False, True):
        w = dpll_witness(clauses, {**assignment, pivot: value})
        if w is not None:
            return w
    return None


def complete_witness(formula, partial, n):
    bits = "".join("1" if partial.get(v, False) else "0" for v in range(1, n + 1))
    assert satisfies(formula, bits)
    return bits


def sat_module(clauses, assignment):
    clauses = simplify(clauses, assignment)
    if clauses is None:
        return False
    while True:
        unit = next((c[0] for c in clauses if len(c) == 1), None)
        if unit is None:
            break
        v, val = abs(unit), unit > 0
        assignment = dict(assignment)
        assignment[v] = val
        clauses = simplify(clauses, {v: val})
        if clauses is None:
            return False
        if not clauses:
            return True
    if not clauses:
        return True
    p = abs(min(clauses, key=len)[0])
    return sat_module(clauses, {**assignment, p: False}) or sat_module(clauses, {**assignment, p: True})


def unsat_boundary_certificate(U, pin=None):
    boundary = list(range(193, 199))
    allowed = []
    for module in [U[2 + 42 * i:2 + 42 * (i + 1)] for i in range(6)]:
        rows = set()
        for mask in range(64):
            a = {v: bool((mask >> (v - 193)) & 1) for v in boundary}
            if pin:
                a[pin[0]] = pin[1]
            if sat_module(module, a):
                rows.add(mask)
        allowed.append(rows)
    globals_ok = set()
    for mask in range(64):
        a = {v: bool((mask >> (v - 193)) & 1) for v in boundary}
        if pin:
            a[pin[0]] = pin[1]
        if all(any(a.get(abs(x), None) == (x > 0) for x in c if abs(x) in a) for c in U[:2]):
            globals_ok.add(mask)
    return sorted(globals_ok.intersection(*allowed))


def raw_cofactor(formula, pivot, value):
    out, removed, binaries = [], [], []
    for idx, clause in enumerate(formula):
        if (pivot if value else -pivot) in clause:
            removed.append((idx, clause[:]))
            continue
        if (-pivot if value else pivot) in clause:
            row = [x for x in clause if abs(x) != pivot]
            binaries.append((len(out), idx, row[:]))
            out.append(row)
        else:
            out.append(clause[:])
    assert len(removed) == 2 and len(binaries) == 2
    return out, removed, binaries


def choose_pairing(slots):
    for pairs in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
        if all(abs(slots[a]) != abs(slots[b]) for a, b in pairs):
            return [[slots[a], slots[b]] for a, b in pairs]
    raise AssertionError("no proper pairing")


def build_child(formula, pivot, value, base_D, base_D_witness):
    n = max(abs(x) for c in formula for x in c)
    old_map = {v: v if v < pivot else v - 1 for v in range(1, n + 1) if v != pivot}
    raw, removed, binaries = raw_cofactor(formula, pivot, value)
    mapped = []
    binary_positions = []
    for clause in raw:
        row = [(1 if x > 0 else -1) * old_map[abs(x)] for x in clause]
        if len(row) == 2:
            binary_positions.append(len(mapped))
        mapped.append(row)
    assert len(binary_positions) == 2

    # D has a missing positive clause.  Orient it to the binary polarity.
    selected_sign = 1 if value else -1
    opposite_sign = -selected_sign
    d_offset = n - 1
    dmap = {v: d_offset + v for v in range(1, 199)}
    oriented_D = [[opposite_sign * (1 if x > 0 else -1) * dmap[abs(x)] for x in c] for c in base_D]
    base_ports = (194, 196, 197)
    ports = [opposite_sign * dmap[v] for v in base_ports]
    for pos, port in zip(binary_positions, ports[:2]):
        mapped[pos].append(port)

    selected_slots = []
    for _, clause in removed:
        selected_slots.extend(selected_sign * old_map[abs(x)] for x in clause if abs(x) != pivot)
    pairs = choose_pairing(selected_slots)
    z = [d_offset + 198 + i for i in range(1, 5)]
    sz = [selected_sign * x for x in z]
    oz = [opposite_sign * x for x in z]
    closure = [
        pairs[0] + [sz[0]],
        pairs[1] + [sz[2]],
        [sz[0], sz[1], sz[3]],
        [sz[1], sz[2], sz[3]],
        [oz[0], oz[1], ports[2]],
        [oz[0], oz[2], oz[3]],
        [oz[1], oz[2], oz[3]],
    ]
    child = mapped + oriented_D + closure
    assert valid_target(child)

    def extend(parent_bits):
        assert parent_bits[pivot - 1] == ("1" if value else "0")
        old_bits = "".join(parent_bits[v - 1] for v in range(1, n + 1) if v != pivot)
        d_bits = base_D_witness if opposite_sign == 1 else "".join("1" if b == "0" else "0" for b in base_D_witness)
        selected_truth = (1, 0, 1, 0)
        z_bits = "".join(str(t if selected_sign == 1 else 1 - t) for t in selected_truth)
        bits = old_bits + d_bits + z_bits
        assert satisfies(child, bits)
        return bits

    return {
        "child": child,
        "raw": raw,
        "removed": removed,
        "binary_source_indices": [x[1] for x in binaries],
        "selected_slots": selected_slots,
        "pairing": pairs,
        "ports": ports,
        "fresh": z,
        "closure": closure,
        "extend": extend,
    }


def partitions(tokens):
    tokens = tuple(tokens)
    if not tokens:
        yield ()
        return
    for inds in itertools.combinations(range(1, len(tokens)), 2):
        idx = (0,) + inds
        block = tuple(tokens[i] for i in idx)
        if len({x[1] for x in block}) != 3:
            continue
        rem = tuple(x for i, x in enumerate(tokens) if i not in idx)
        for tail in partitions(rem):
            yield (tuple(sorted(block)),) + tail


def positive_forms():
    toks = [(f"o{i}", f"o{i}") for i in range(4)] + [(f"z{i}{j}", f"z{i}") for i in range(4) for j in range(2)]
    forms = set()
    for p in partitions(toks):
        blocks = tuple(sorted(tuple(sorted(x[1] for x in b)) for b in p))
        if len(set(blocks)) == 4:
            forms.add(blocks)
    return sorted(forms)


def negative_forms():
    subs = [tuple(i for i in range(4) if mask >> i & 1) for mask in range(1, 16) if mask.bit_count() <= 3]
    out = []
    for form in itertools.combinations_with_replacement(subs, 3):
        if any(form.count(s) > 1 and len(s) == 3 for s in form):
            continue
        if sum(map(len, form)) == 8 and all(sum(z in s for s in form) == 2 for z in range(4)):
            out.append(form)
    return out


def core_full_projection(pos, neg):
    for om in range(16):
        ok = False
        for zm in range(16):
            p_ok = all(any(((om >> int(v[1])) & 1) if v[0] == "o" else ((zm >> int(v[1])) & 1) for v in c) for c in pos)
            n_ok = all(any(not ((zm >> z) & 1) for z in c) for c in neg)
            if p_ok and n_ok:
                ok = True
                break
        if not ok:
            return False
    return True


def relation_mask(pos, neg):
    raw_mask = closure_mask = 0
    for mask in range(256):
        om, bm = mask & 15, (mask >> 4) & 15
        raw = bool((bm & 1) or (bm & 2)) and bool((bm & 4) or (bm & 8))
        if raw:
            raw_mask |= 1 << mask
        close = raw and core_full_projection_for_o(pos, neg, om)
        if close:
            closure_mask |= 1 << mask
    return raw_mask, closure_mask


def core_full_projection_for_o(pos, neg, om):
    for zm in range(16):
        if all(any(((om >> int(v[1])) & 1) if v[0] == "o" else ((zm >> int(v[1])) & 1) for v in c) for c in pos) and all(any(not ((zm >> z) & 1) for z in c) for c in neg):
            return True
    return False


def enumerate_q4_relations():
    pos = positive_forms()
    neg = negative_forms()
    exact = [(p, n) for n in neg for p in pos if core_full_projection(p, n)]
    payload = json.dumps(exact, separators=(",", ":"), sort_keys=True).encode()
    chosen_p = (("o0", "o1", "z0"), ("o2", "o3", "z2"), ("z0", "z1", "z3"), ("z1", "z2", "z3"))
    chosen_n = ((0, 1), (0, 2, 3), (1, 2, 3))
    assert (chosen_p, chosen_n) in exact
    raw, close = relation_mask(chosen_p, chosen_n)
    assert raw == close and raw.bit_count() == 144
    return {
        "positive_forms": len(pos),
        "negative_forms": len(neg),
        "pairs_tested": len(pos) * len(neg),
        "exact_relations": len(exact),
        "exact_forms_sha256": hashlib.sha256(payload).hexdigest(),
        "chosen_positive": chosen_p,
        "chosen_negative": chosen_n,
        "fixed_selected_literal_truths_z0_z1_z2_z3": [1, 0, 1, 0],
        "raw_models": raw.bit_count(),
        "closure_models": close.bit_count(),
        "raw_only": (raw & ~close).bit_count(),
        "closure_only": (close & ~raw).bit_count(),
    }


def dpll_cap(formula, cap=400):
    counter = {"nodes": 0, "literal_tests": 0, "cap": cap}

    def rec(clauses, assignment):
        if counter["nodes"] >= cap:
            return "UNRESOLVED"
        counter["nodes"] += 1
        clauses = simplify(clauses, assignment, counter)
        if clauses is None:
            return "UNSAT"
        while True:
            unit = next((c[0] for c in clauses if len(c) == 1), None)
            if unit is None:
                break
            v, val = abs(unit), unit > 0
            assignment = {**assignment, v: val}
            clauses = simplify(clauses, {v: val}, counter)
            if clauses is None:
                return "UNSAT"
            if not clauses:
                return "SAT"
        if not clauses:
            return "SAT"
        p = abs(min(clauses, key=len)[0])
        unresolved = False
        for value in (False, True):
            ans = rec(clauses, {**assignment, p: value})
            if ans == "SAT":
                return "SAT"
            unresolved |= ans == "UNRESOLVED"
        return "UNRESOLVED" if unresolved else "UNSAT"

    counter["status"] = rec(formula, {})
    return counter


def gamma_len(x):
    return 2 * x.bit_length() - 1


def encoding_length(n, m):
    return gamma_len(n) + gamma_len(m) + m * (1 + 3 * n.bit_length())


def clause_extremes(formula):
    rows = []
    for i, c in enumerate(formula):
        S = [[abs(x), int(x > 0)] for x in c]
        U = [[v, 1 - b] for v, b in S]
        rows.append({"clause_index": i, "clause": c, "S": S, "invert_S": U, "U": U, "invert_U": S})
    return rows


def pair_matrix(formula):
    rows, sig = [], Counter()
    for i, j in itertools.combinations(range(len(formula)), 2):
        same = any(x in formula[j] for x in formula[i])
        opposite = any(-x in formula[j] for x in formula[i])
        row = {"i": i, "j": j, "SS": not opposite, "SU": not same, "US": not same, "UU": not opposite}
        rows.append(row)
        sig["".join("1" if row[x] else "0" for x in ("SS", "SU", "US", "UU"))] += 1
        # exact enumeration on the local union
        variables = sorted({abs(x) for x in formula[i] + formula[j]})
        observed = set()
        for bits in itertools.product((False, True), repeat=len(variables)):
            a = dict(zip(variables, bits))
            t = [sum(a[abs(x)] == (x > 0) for x in formula[k]) for k in (i, j)]
            if t[0] in (0, 3) and t[1] in (0, 3):
                observed.add(("S" if t[0] == 3 else "U") + ("S" if t[1] == 3 else "U"))
        assert observed == {x for x in ("SS", "SU", "US", "UU") if row[x]}
    return {"rows": rows, "signature_counts": dict(sig)}


def truth_count(c, a):
    return sum(a[abs(x) - 1] == int(x > 0) for x in c)


def logical_state(formula, a, gray):
    out = list(a)
    for c in formula:
        t = truth_count(c, a)
        code = t ^ (t >> 1) if gray else t
        out.extend((code & 1, (code >> 1) & 1, int(t > 0)))
    return out


def xor_trace(formula, flips):
    n = max(abs(x) for c in formula for x in c)
    ans = {}
    for name, gray in (("binary", False), ("gray", True)):
        a = [0] * n
        first = prev = logical_state(formula, a, gray)
        rows = []
        for p in flips:
            before_counts = [truth_count(c, a) for c in formula]
            a[p] ^= 1
            after_counts = [truth_count(c, a) for c in formula]
            cur = logical_state(formula, a, gray)
            changed = [i for i, (x, y) in enumerate(zip(prev, cur)) if x != y]
            rows.append({"pivot_zero_based": p, "changed_clause_ids": [i for i, (x, y) in enumerate(zip(before_counts, after_counts)) if x != y], "changed_cell_ids": changed, "d_logic": len(changed)})
            prev = cur
        ans[name] = {"state_bits": len(first), "rows": rows, "sum_adjacent_d_logic": sum(r["d_logic"] for r in rows), "endpoint_d_logic": sum(x != y for x, y in zip(first, prev)), "actual_d_phys": "NOT MEASURED"}
    return ans


def endpoint_hist(formula):
    n = max(abs(x) for c in formula for x in c)
    out = {}
    for name, a in (("zero", [0] * n), ("one", [1] * n)):
        ts = [truth_count(c, a) for c in formula]
        out[name] = {str(i): ts.count(i) for i in range(4)}
    return out


def full_controls(formula):
    return {"clause_extremes": clause_extremes(formula), "pair_matrix": pair_matrix(formula), "endpoints": endpoint_hist(formula), "xor": xor_trace(formula, [0, 0, 1, 2, 3, 3, 4, 5])}


def main():
    started = time.perf_counter()
    U = load_u()
    V = [c[:] for c in U]
    V[2][-1], V[44][-1] = V[44][-1], V[2][-1]
    Y = y6()
    assert valid_target(U) and valid_target(V) and valid_target(Y)
    assert unsat_boundary_certificate(U) == []
    assert satisfies(V, V_WITNESS)

    D = U[:1] + U[2:]
    d_partial = dpll_witness(D)
    assert d_partial is not None
    d_witness = complete_witness(D, d_partial, 198)
    assert all(d_witness[abs(x) - 1] == "0" for x in U[1])

    pivot, value = 3, True
    uc = build_child(U, pivot, value, D, d_witness)
    vc = build_child(V, pivot, value, D, d_witness)
    assert uc["closure"] == vc["closure"] and uc["selected_slots"] == vc["selected_slots"]
    v_child_witness = vc["extend"](V_WITNESS)
    assert satisfies(vc["child"], v_child_witness)
    assert unsat_boundary_certificate(U, (pivot, value)) == []
    assert len(uc["child"]) == 532 and max(abs(x) for c in uc["child"] for x in c) == 399

    q4 = enumerate_q4_relations()
    malformed = [[], [[1, -2, 3]], [[1, 1, 2]], Y + [Y[0]], [[1, 2, 3]]]
    assert all(not valid_target(x) for x in malformed)
    dpll = {
        "U_raw_cofactor": dpll_cap(uc["raw"]),
        "U_reentry_child": dpll_cap(uc["child"]),
        "V_raw_cofactor": dpll_cap(vc["raw"]),
        "V_reentry_child": dpll_cap(vc["child"]),
    }

    controls = {"U198": full_controls(U), "V198": full_controls(V), "Y6": full_controls(Y)}
    result = {
        "run_id": "NONMINIMUM-BRANCH-REENTRY-REFEREE258",
        "timestamp": "2026-10-31T22:48:00-07:00",
        "claim_status": {"branch_reentry": "PROVED/EXACT", "finite_enumeration": "COMPUTATIONAL", "power_short_contraction": "FALSIFIED/RETIRED for this construction", "arbitrary_A_Phi": "OPEN", "FLMV": "OPEN", "P_vs_NP": "OPEN"},
        "falsifiers": {
            "F1": "every nonminimum q=4 one-copy closure changes the raw boundary relation",
            "F2": "the explicit closure fails target occurrence or duplicate-free properness",
            "F3": "a satisfying raw cofactor assignment cannot always extend through the critical gadget",
            "F4": "valid branch re-entry is automatically a power-short ARC contraction",
        },
        "q4_relation_census": q4,
        "theorem": {
            "quantifiers": "for every valid canonical target F, every variable x, and each b in {0,1}",
            "result": "R(F,x=b) is a valid canonical target and SAT(R(F,x=b)) iff SAT(F restricted by x=b)",
            "sizes": "if F has (n,m), R has exactly (n+201,m+268)",
            "self_reduction": "SAT(F) iff SAT(R(F,x=0)) OR SAT(R(F,x=1))",
            "extension_selected_literal_truths": [1, 0, 1, 0],
            "limitation": "children are larger, not power-short; repeated use grows by 201 variables and 268 clauses per level",
        },
        "actual_controls": {
            "pivot": pivot,
            "value": value,
            "U_child": {"variables": 399, "clauses": len(uc["child"]), "status": "UNSAT by exact equisatisfiability plus pinned U198 certificate", "closure": uc["closure"], "selected_slots": uc["selected_slots"], "pairing": uc["pairing"], "ports": uc["ports"], "binary_source_indices": uc["binary_source_indices"]},
            "V_child": {"variables": 399, "clauses": len(vc["child"]), "status": "SAT", "witness_sha256": hashlib.sha256(v_child_witness.encode()).hexdigest(), "witness": v_child_witness},
            "D": {"status": "SAT", "witness_sha256": hashlib.sha256(d_witness.encode()).hexdigest(), "witness": d_witness, "ports": U[1]},
            "Y6": {"status": "SAT", "models": sum(satisfies(Y, f"{mask:06b}"[::-1]) for mask in range(64))},
            "malformed_rejected": len(malformed),
        },
        "encoding_ledger": {
            "gamma_clause_encoding": "gamma(n)||gamma(m), then one sign bit plus three fixed-width identifiers per clause",
            "U_parent_bits": encoding_length(198, 264),
            "U_child_bits": encoding_length(399, 532),
            "structural_delta_variables": 201,
            "structural_delta_clauses": 268,
            "width_crossover_warning": "away from a name-width boundary the added bit length is O(log n); at a crossover all retained identifiers widen by one bit, adding Theta(m)=Theta(N/log n) bits for the fixed-width clause encoding when m=Theta(n); in every case child length is Theta(N), never N^lambda for lambda<1",
        },
        "dpll_comparison": dpll,
        "same_target_controls": controls,
        "xor_controls": {"delay": {"native_steps": 10000, "data_bit_changes": 0}, "source_reread": {"reads": 1000, "writes": 0}, "unaligned_parent_child": "no XOR comparison claimed without a declared aligned physical encoding", "physical": "all listed U/V/Y XOR traces are offline logical diagnostics; actual d_phys was not measured"},
        "resource_ledger": {
            "discovery": "literature, project search and the 2,628 reduced q=4 relation tests charged",
            "selection_switching": "pivot, branch, pairing, gadget orientation and failed policies are not free",
            "source_access": "grammar validation, two occurrence lists, removed clauses and critical witness/certificate require indexed reads",
            "child_output": "explicit child has 399 variables, 532 clauses and 14,932 gamma-encoding bits on the 198-variable controls",
            "query_guest": "two larger branch queries do not reduce an unknown exponent K and must include accessor/index-tape work",
            "failed_trials": "all nonselected relation forms and unresolved DPLL routes count",
            "proof_checking": "target grammar, boundary truth table, D forcing, U pin certificate and V witness charged",
            "peak_space": "parent, D template or source access, child/output, guest state, indices, witness/certificate and retained branch state count simultaneously",
        },
        "search_record": {
            "web_queries": ["Döcker Monotone 3-SAT (2,2) gadget enforcer clause extension primary paper", "bounded occurrence SAT gadget exact occurrence variable replacement primary paper", "bounded degree CSP gadget relation realization primitive positive definitions primary paper", "SAT faithful gadget boundary relation equisatisfiable extension primary paper"],
            "findings": ["Döcker and Darmann-Döcker use extension-exact monotone gadgets and false-literal enforcers but do not state this q=4 branch repair", "Berman-Karpinski-Scott study bounded-occurrence enforcers but do not supply the FLMV bridge", "pp-definability is the correct abstract boundary-relation language, but exact (2,2) quotas and resource accounting remain extra obligations"],
            "github_queries": ["repo:j15marti/pnp q=4 critical-port", "repo:j15marti/pnp nonminimum closure", "repo:j15marti/pnp 3c-4q", "repo:j15marti/pnp boundary relation critical", "org:openai Monotone 3-SAT 2,2 gadget"],
            "github_findings": "q=4/nonminimum appeared only as an open target in REF257, SLACK292 and GROK 22:15; no explicit repair was found; OpenAI search returned zero hits",
            "access_failures": "none for used searches",
            "novelty": "project-local exact construction only; no external novelty claim",
        },
        "corpus_audit": {
            "reviewed": ["root main/AGENTS/CODEX/pnp-research skill", "REDIRECT1/CONTRACT1 and named affine/construction/ARC gates", "REF255-257", "issue #3", "LSPV-1 ODD-CYCLE293", "LSPV-2 GAMMA-SUFFIX289", "LSPV-3 GATE291", "LSPV-4 INDEX-HEAD291", "GROK 22:15"],
            "duplication": "REF257 leaves q>=4 open; no prior explicit seven-clause relation repair found",
            "stale": "LSPV-3 GATE291 public report still lacks the required opening marker and final sentinel",
        },
        "runtime_seconds": time.perf_counter() - started,
    }

    FULL.parent.mkdir(parents=True, exist_ok=True)
    full_bytes = (json.dumps(result, separators=(",", ":"), sort_keys=True) + "\n").encode()
    FULL.write_bytes(full_bytes)
    archive_bytes = base64.b64encode(gzip.compress(full_bytes, compresslevel=9, mtime=0)) + b"\n"
    ARCHIVE.write_bytes(archive_bytes)
    summary = {k: result[k] for k in ("run_id", "timestamp", "claim_status", "falsifiers", "q4_relation_census", "theorem", "actual_controls", "encoding_ledger", "dpll_comparison", "xor_controls", "resource_ledger", "search_record", "corpus_audit")}
    summary["same_target_control_summary"] = {name: {"clauses": len(form), "pairs": len(result["same_target_controls"][name]["pair_matrix"]["rows"]), "pair_signatures": result["same_target_controls"][name]["pair_matrix"]["signature_counts"], "endpoints": result["same_target_controls"][name]["endpoints"], "xor": {enc: {k: v[k] for k in ("state_bits", "sum_adjacent_d_logic", "endpoint_d_logic", "actual_d_phys")} for enc, v in result["same_target_controls"][name]["xor"].items()}} for name, form in (("U198", U), ("V198", V), ("Y6", Y))}
    summary["full_raw"] = {"archive_path": str(ARCHIVE.relative_to(ROOT)), "full_json_bytes": len(full_bytes), "archive_text_bytes": len(archive_bytes), "full_sha256": hashlib.sha256(full_bytes).hexdigest(), "archive_sha256": hashlib.sha256(archive_bytes).hexdigest()}
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"summary": str(SUMMARY), "summary_bytes": SUMMARY.stat().st_size, "full_bytes": len(full_bytes), "archive_bytes": len(archive_bytes), "runtime_seconds": result["runtime_seconds"], "q4": q4, "dpll": dpll}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
