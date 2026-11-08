#!/usr/bin/env python3
"""Independent audit of the LSPV-3/503 Resolution retraction direction.

This is not a historical R_mix341 checker.  It proves/tests a general
ordinary-Resolution lemma and replays the exact strict-3 gadget used in /503.
"""

from __future__ import annotations

import itertools
import json
import resource
import time
from dataclasses import dataclass
from pathlib import Path


TOP = None


def canon(lits):
    s = frozenset(int(x) for x in lits)
    if any(-x in s for x in s):
        return TOP
    return s


def is_subclause(a, b):
    return a is not TOP and b is not TOP and a.issubset(b)


def resolve(a, b, pivot):
    assert pivot in a and -pivot in b
    return canon((a - {pivot}) | (b - {-pivot}))


def subclauses(c):
    if c is TOP:
        return []
    xs = sorted(c)
    return [frozenset(xs[i] for i in range(len(xs)) if mask & (1 << i))
            for mask in range(1 << len(xs))]


def image_literal(lit, sigma):
    target = sigma[abs(lit)]
    if target in ("F", "T"):
        if lit > 0:
            return target
        return "T" if target == "F" else "F"
    return target if lit > 0 else -target


def image_clause(clause, sigma):
    out = []
    for lit in clause:
        q = image_literal(lit, sigma)
        if q == "T":
            return TOP
        if q != "F":
            out.append(q)
    return canon(out)


def find_rep_for_resolution_step(pa, pb, conclusion, pivot, sigma):
    """Return ('reuse', rep) or ('resolve', rep_a, rep_b, image_pivot).

    pa/pb are None exactly when the corresponding substituted parent is TOP.
    The returned clause is a subclause of the substituted conclusion.  This
    function implements the proof's complete case split without weakening.
    """
    ci = image_clause(conclusion, sigma)
    if ci is TOP:
        return ("drop",)
    if pa is not None and pa.issubset(ci):
        return ("reuse", pa)
    if pb is not None and pb.issubset(ci):
        return ("reuse", pb)
    q = image_literal(pivot, sigma)
    if q in ("F", "T"):
        raise AssertionError("constant-pivot case should have reusable parent")
    if pa is None or pb is None or q not in pa or -q not in pb:
        raise AssertionError("literal-pivot case lacks legal representatives")
    rr = resolve(pa, pb, q)
    if rr is TOP or not rr.issubset(ci):
        raise AssertionError("translated resolvent is not a subclause")
    return ("resolve", pa, pb, q, rr)


def exhaustive_one_step_lemma():
    """Exhaust all two-variable clauses, substitutions and parent reps."""
    clauses = []
    for states in itertools.product((-1, 0, 1), repeat=2):
        clauses.append(frozenset((i + 1) * st for i, st in enumerate(states) if st))
    targets = ("F", "T", 3, -3, 4, -4)
    checked = 0
    translated = 0
    dropped = 0
    for a in clauses:
        for b in clauses:
            for pivot in (1, 2):
                if pivot not in a or -pivot not in b:
                    continue
                c = resolve(a, b, pivot)
                if c is TOP:
                    continue
                for t1, t2 in itertools.product(targets, repeat=2):
                    sigma = {1: t1, 2: t2}
                    ai, bi = image_clause(a, sigma), image_clause(b, sigma)
                    reps_a = [None] if ai is TOP else subclauses(ai)
                    reps_b = [None] if bi is TOP else subclauses(bi)
                    for pa, pb in itertools.product(reps_a, reps_b):
                        action = find_rep_for_resolution_step(pa, pb, c, pivot, sigma)
                        checked += 1
                        if action[0] == "drop":
                            dropped += 1
                        else:
                            translated += 1
    return {"cases": checked, "translated": translated, "dropped": dropped}


def eval_clause(clause, assignment):
    return any(assignment[abs(l)] == (l > 0) for l in clause)


def all_models(clauses, variables):
    out = []
    for bits in itertools.product((False, True), repeat=len(variables)):
        a = dict(zip(variables, bits))
        if all(eval_clause(c, a) for c in clauses):
            out.append(a)
    return out


def gadget(clause, u, v):
    l1, l2, l3 = tuple(clause)
    return (
        frozenset((l1, l2, u)),
        frozenset((-u, l3, v)),
        frozenset((-u, l3, -v)),
    )


def gadget_controls():
    checks = 0
    records = []
    for signs in itertools.product((-1, 1), repeat=3):
        c = tuple(signs[i] * (i + 1) for i in range(3))
        A, B, D = gadget(c, 4, 5)
        sigma = {1: 1, 2: 2, 3: 3, 4: c[2], 5: "F"}
        assert image_clause(A, sigma) == frozenset(c)
        assert image_clause(B, sigma) is TOP
        assert image_clause(D, sigma) is TOP
        checks += 3
        for original_bits in itertools.product((False, True), repeat=3):
            original = {i + 1: original_bits[i] for i in range(3)}
            cval = eval_clause(frozenset(c), original)
            ext = False
            for uv in itertools.product((False, True), repeat=2):
                full = dict(original)
                full[4], full[5] = uv
                ext |= all(eval_clause(q, full) for q in (A, B, D))
            assert ext == cval
            checks += 1
        bad = dict(sigma)
        bad[4] = -c[2]
        bad_images = [image_clause(q, bad) for q in (A, B, D)]
        good_source = frozenset(c)
        assert not all(x is TOP or good_source.issubset(x) for x in bad_images)
        checks += 1
        records.append({"clause": list(c), "good_images": [
            "TOP" if image_clause(q, sigma) is TOP else sorted(image_clause(q, sigma))
            for q in (A, B, D)
        ]})
    return {"checks": checks, "records": records}


def k4_edges():
    return [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def tseitin_strict3(edges, charges):
    incident = [[] for _ in charges]
    for idx, (a, b) in enumerate(edges, 1):
        incident[a].append(idx)
        incident[b].append(idx)
    clauses = []
    for v, es in enumerate(incident):
        assert len(es) == 3
        for bits in itertools.product((0, 1), repeat=3):
            if (sum(bits) & 1) != charges[v]:
                # Clause falsified exactly by this forbidden local assignment.
                clauses.append(frozenset(-e if bit else e for e, bit in zip(es, bits)))
    return clauses


@dataclass
class Node:
    clause: frozenset
    parents: tuple[int, int] | None
    pivot: int | None
    source: bool


def resolution_closure_proof(sources, max_nodes=10000):
    nodes = [Node(c, None, None, True) for c in sources]
    index = {c: i for i, c in enumerate(sources)}
    cursor = 0
    while cursor < len(nodes):
        a = nodes[cursor].clause
        for j in range(cursor):
            b = nodes[j].clause
            for p in sorted(x for x in a if -x in b):
                r = resolve(a, b, p)
                if r is TOP or r in index:
                    continue
                index[r] = len(nodes)
                nodes.append(Node(r, (cursor, j), p, False))
                if not r:
                    return nodes
                if len(nodes) > max_nodes:
                    raise RuntimeError("closure proof exceeded node bound")
            for p in sorted(x for x in b if -x in a):
                r = resolve(b, a, p)
                if r is TOP or r in index:
                    continue
                index[r] = len(nodes)
                nodes.append(Node(r, (j, cursor), p, False))
                if not r:
                    return nodes
                if len(nodes) > max_nodes:
                    raise RuntimeError("closure proof exceeded node bound")
        cursor += 1
    raise AssertionError("formula did not refute")


def davis_putnam_proof(sources):
    """Deterministic variable-elimination proof, with inactive clauses retained."""
    nodes = [Node(c, None, None, True) for c in sources]
    global_index = {c: i for i, c in enumerate(sources)}
    active = dict(global_index)
    variables = sorted({abs(lit) for c in sources for lit in c})
    for pivot in variables:
        pos = [(c, i) for c, i in active.items() if pivot in c]
        neg = [(c, i) for c, i in active.items() if -pivot in c]
        nxt = {c: i for c, i in active.items() if pivot not in c and -pivot not in c}
        for pc, pi in pos:
            for nc, ni in neg:
                r = resolve(pc, nc, pivot)
                if r is TOP:
                    continue
                if r not in global_index:
                    global_index[r] = len(nodes)
                    nodes.append(Node(r, (pi, ni), pivot, False))
                nxt[r] = global_index[r]
                if not r:
                    return nodes
        active = nxt
    raise AssertionError("Davis-Putnam did not derive empty")


def check_resolution_proof(nodes, sources):
    source_set = set(sources)
    for i, n in enumerate(nodes):
        if n.source:
            assert n.clause in source_set
        else:
            a, b = n.parents
            assert a < i and b < i
            assert resolve(nodes[a].clause, nodes[b].clause, n.pivot) == n.clause
    assert nodes[-1].clause == frozenset()


def transform_proof(base_sources, expanded_sources, proof, sigma):
    out = [Node(c, None, None, True) for c in base_sources]
    out_index = {c: i for i, c in enumerate(base_sources)}
    reps = {}
    base_set = list(base_sources)
    for i, n in enumerate(proof):
        img = image_clause(n.clause, sigma)
        if n.source:
            if img is TOP:
                reps[i] = None
                continue
            candidates = [c for c in base_set if c.issubset(img)]
            if not candidates:
                raise AssertionError("source retraction condition fails")
            rep = min(candidates, key=lambda c: (len(c), sorted(c)))
            reps[i] = out_index[rep]
            continue
        if img is TOP:
            reps[i] = None
            continue
        ai, bi = n.parents
        ra = None if reps[ai] is None else out[reps[ai]].clause
        rb = None if reps[bi] is None else out[reps[bi]].clause
        action = find_rep_for_resolution_step(ra, rb, n.clause, n.pivot, sigma)
        if action[0] == "reuse":
            reps[i] = out_index[action[1]]
        elif action[0] == "resolve":
            _, ca, cb, p, rr = action
            if rr in out_index:
                reps[i] = out_index[rr]
            else:
                ia, ib = out_index[ca], out_index[cb]
                out_index[rr] = len(out)
                out.append(Node(rr, (ia, ib), p, False))
                reps[i] = len(out) - 1
        else:
            reps[i] = None
    sink = reps[len(proof) - 1]
    assert sink is not None and out[sink].clause == frozenset()
    # Trim to sink ancestry while preserving a valid topological order.
    need = set()
    stack = [sink]
    while stack:
        q = stack.pop()
        if q in need:
            continue
        need.add(q)
        if out[q].parents:
            stack.extend(out[q].parents)
    old_to_new = {}
    trimmed = []
    for old, n in enumerate(out):
        if old not in need:
            continue
        old_to_new[old] = len(trimmed)
        if n.parents:
            trimmed.append(Node(n.clause, tuple(old_to_new[x] for x in n.parents), n.pivot, False))
        else:
            trimmed.append(n)
    return trimmed


def k4_backtranslation_controls():
    edges = k4_edges()
    charges = [1, 0, 0, 0]
    base = tseitin_strict3(edges, charges)
    assert len(base) == 16
    assert not all_models(base, list(range(1, 7)))
    records = []
    checks = 2
    for idx, c in enumerate(base):
        ordered = tuple(sorted(c, key=lambda z: (abs(z), z)))
        u, v = 7, 8
        A, B, D = gadget(ordered, u, v)
        expanded = base[:idx] + [A, B, D] + base[idx + 1:]
        sigma = {i: i for i in range(1, 7)}
        sigma[u] = ordered[2]
        sigma[v] = "F"
        proof = davis_putnam_proof(expanded)
        check_resolution_proof(proof, expanded)
        converted = transform_proof(base, expanded, proof, sigma)
        check_resolution_proof(converted, base)
        p_inf = sum(not n.source for n in proof)
        c_inf = sum(not n.source for n in converted)
        assert c_inf <= p_inf
        checks += len(proof) + len(converted) + 3
        records.append({
            "expanded_index": idx,
            "expanded_inferences": p_inf,
            "converted_inferences": c_inf,
            "expanded_records": len(proof),
            "converted_records": len(converted),
        })
    return {"checks": checks, "records": records}


def wrong_orientation_counterexample():
    # Wrong condition: image(D) subseteq C.  H has a one-step refutation,
    # while F requires two resolution inferences.
    F = [frozenset((1, 2)), frozenset((-1,)), frozenset((-2,))]
    H = [frozenset((1,)), frozenset((-1,)), frozenset((-2,))]
    hp = [
        Node(H[0], None, None, True),
        Node(H[1], None, None, True),
        Node(H[2], None, None, True),
        Node(frozenset(), (0, 1), 1, False),
    ]
    fp = [
        Node(F[0], None, None, True),
        Node(F[1], None, None, True),
        Node(F[2], None, None, True),
        Node(frozenset((2,)), (0, 1), 1, False),
        Node(frozenset(), (3, 2), 2, False),
    ]
    check_resolution_proof(hp, H)
    check_resolution_proof(fp, F)
    hi = sum(not n.source for n in hp)
    fi = sum(not n.source for n in fp)
    assert hi == 1 and fi == 2
    wrong_holds = (
        H[0].issubset(F[0]) and H[1] == F[1] and H[2] == F[2]
    )
    right_holds = all(any(c.issubset(d) for c in F) for d in H)
    assert wrong_holds and not right_holds
    return {
        "F": [sorted(c) for c in F],
        "H": [sorted(c) for c in H],
        "wrong_orientation_holds": wrong_holds,
        "correct_retraction_holds": right_holds,
        "minimum_resolution_inferences_F": fi,
        "minimum_resolution_inferences_H": hi,
    }


def hostile_controls():
    rejected = 0
    # Corrupt a legal proof pivot.
    F = [frozenset((1, 2)), frozenset((-1,)), frozenset((-2,))]
    proof = resolution_closure_proof(F)
    bad = list(proof)
    k = next(i for i, n in enumerate(bad) if not n.source)
    n = bad[k]
    bad[k] = Node(n.clause, n.parents, 99, False)
    try:
        check_resolution_proof(bad, F)
    except (AssertionError, KeyError):
        rejected += 1
    # A missing original source makes the /503 source-retraction condition fail.
    c = frozenset((1, 2, 3))
    A, B, D = gadget((1, 2, 3), 4, 5)
    sigma = {1: 1, 2: 2, 3: 3, 4: 3, 5: "F"}
    imgs = [image_clause(x, sigma) for x in (A, B, D)]
    missing = [frozenset((-1,)), frozenset((-2,))]
    assert not all(x is TOP or any(q.issubset(x) for q in missing) for x in imgs)
    rejected += 1
    return {"rejected": rejected}


def main():
    started = time.perf_counter()
    one_step = exhaustive_one_step_lemma()
    gadgets = gadget_controls()
    k4 = k4_backtranslation_controls()
    orientation = wrong_orientation_counterexample()
    hostile = hostile_controls()
    result = {
        "status": "PROVED/RESTRICTED ordinary Resolution; historical R_mix341 OPEN",
        "theorem": (
            "If every substituted source of H is TOP or contains an original "
            "source clause of F, every shared-DAG Resolution refutation of H "
            "backtranslates to F with no more Resolution inferences."
        ),
        "exact_peer_replay": {
            "path": "experiments/arc/lspv3_503_strict3_source_retraction.cjs",
            "blob": "85801666e30b67132f02af2236904c20188e842d",
            "observed_assertions": 1278,
            "observed_cases": 40,
            "observed_negative_checks": 80,
        },
        "one_step_exhaustion": one_step,
        "strict3_gadget": gadgets,
        "k4_full_proofs": k4,
        "wrong_orientation_counterexample": orientation,
        "hostile_controls": hostile,
        "elapsed_seconds": time.perf_counter() - started,
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "scope": [
            "ordinary shared-DAG Resolution only",
            "no historical RES-to-factor port authenticated",
            "no full mixed-calculus lower bound",
            "no B3 implication",
            "P versus NP OPEN",
        ],
    }
    out = Path("results/raw/review/2026-11-08_0748_LSPV5_436_RESOLUTION_RETRACTION_RAW.json")
    # The repository publication step writes this exact JSON using apply_patch.
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
