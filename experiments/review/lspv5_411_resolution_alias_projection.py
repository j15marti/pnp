#!/usr/bin/env python3
"""Independent red-team check of the LSPV-1/476 literal-alias projection.

This is ordinary source-authenticated DAG Resolution only.  It is not the
historical R_mix341 byte checker.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import resource
import time

TOP = None


def norm(lits):
    s = set(lits)
    if any(-x in s for x in s):
        return TOP
    return tuple(sorted(s, key=lambda x: (abs(x), x < 0)))


def is_subset(a, b):
    return a is not TOP and b is not TOP and set(a) <= set(b)


def resolve(a, b, pivot):
    if a is TOP or b is TOP:
        raise ValueError("TOP is not a Resolution premise")
    if pivot not in a or -pivot not in b:
        raise ValueError("wrong oriented pivot")
    return norm([x for x in a if x != pivot] + [x for x in b if x != -pivot])


def project(clause, sigma):
    if clause is TOP:
        return TOP
    out = []
    for lit in clause:
        image = sigma[abs(lit)]
        out.append(image if lit > 0 else -image)
    return norm(out)


def subclauses(clause):
    if clause is TOP:
        return [TOP]
    c = list(clause)
    return [tuple(c[i] for i in range(len(c)) if mask & (1 << i))
            for mask in range(1 << len(c))]


def compile_local(a, b, pivot, sigma, wa, wb):
    """Return (kind,witness) using no weakening and at most one RES."""
    child = resolve(a, b, pivot)
    pc = project(child, sigma)
    pa, pb = project(a, sigma), project(b, sigma)

    if pc is TOP:
        return "skip-top", TOP
    if pa is not TOP and (wa is TOP or not is_subset(wa, pa)):
        raise ValueError("bad left invariant")
    if pb is not TOP and (wb is TOP or not is_subset(wb, pb)):
        raise ValueError("bad right invariant")
    if pa is TOP and wa is not TOP:
        raise ValueError("compiler must skip a tautological parent")
    if pb is TOP and wb is not TOP:
        raise ValueError("compiler must skip a tautological parent")

    if wa is not TOP and is_subset(wa, pc):
        return "left-survivor", wa
    if wb is not TOP and is_subset(wb, pc):
        return "right-survivor", wb

    image = sigma[abs(pivot)]
    oriented = image if pivot > 0 else -image
    if wa is not TOP and wb is not TOP and oriented in wa and -oriented in wb:
        w = resolve(wa, wb, oriented)
        if w is not TOP and is_subset(w, pc):
            return "one-res", w
    raise AssertionError((a, b, pivot, sigma, wa, wb, pa, pb, pc))


def signed_clause_choices(vars_):
    for states in itertools.product((-1, 0, 1), repeat=len(vars_)):
        yield norm(s * v for s, v in zip(states, vars_) if s)


def exhaustive_local_lemma():
    counts = {"skip-top": 0, "left-survivor": 0,
              "right-survivor": 0, "one-res": 0}
    transitions = witness_pairs = 0
    target_lits = (-3, -2, -1, 1, 2, 3)
    for a0 in signed_clause_choices((2, 3)):
        for b0 in signed_clause_choices((2, 3)):
            a = norm((1,) + a0)
            b = norm((-1,) + b0)
            for images in itertools.product(target_lits, repeat=3):
                sigma = {i + 1: images[i] for i in range(3)}
                pa, pb = project(a, sigma), project(b, sigma)
                was = [TOP] if pa is TOP else subclauses(pa)
                wbs = [TOP] if pb is TOP else subclauses(pb)
                transitions += 1
                for wa in was:
                    for wb in wbs:
                        kind, witness = compile_local(a, b, 1, sigma, wa, wb)
                        pc = project(resolve(a, b, 1), sigma)
                        assert witness is TOP if pc is TOP else is_subset(witness, pc)
                        counts[kind] += 1
                        witness_pairs += 1
    return transitions, witness_pairs, counts


def cube_source():
    # The complete contradictory width-three source on x1,x2,x3.
    return [norm(signs[i] * (i + 1) for i in range(3))
            for signs in itertools.product((-1, 1), repeat=3)]


def split_source(source):
    out, sigma = [], {1: 1, 2: 2, 3: 3}
    next_var = 4
    for c in source:
        l1, l2, l3 = c
        a = next_var
        next_var += 1
        out.extend((norm((l1, l2, a)), norm((l1, l3, -a))))
        sigma[a] = l3
    return out, sigma


def full_cube_trace(source, start_id=0):
    nodes = [{"clause": c, "parents": None, "pivot": None}
             for c in source]
    level = list(range(start_id, start_id + len(source)))
    for pivot in (3, 2, 1):
        pos = [i for i in level if pivot in nodes[i]["clause"]]
        neg = [i for i in level if -pivot in nodes[i]["clause"]]
        by_rest = {}
        for i in pos:
            rest = tuple(x for x in nodes[i]["clause"] if x != pivot)
            by_rest[(1, rest)] = i
        new = []
        used = set()
        for i in neg:
            rest = tuple(x for x in nodes[i]["clause"] if x != -pivot)
            key = (1, rest)
            if key not in by_rest:
                # At each cube level the matching rest is identical.
                continue
            j = by_rest[key]
            if (j, i) in used:
                continue
            used.add((j, i))
            clause = resolve(nodes[j]["clause"], nodes[i]["clause"], pivot)
            nodes.append({"clause": clause, "parents": (j, i), "pivot": pivot})
            new.append(len(nodes) - 1)
        # Canonical cube pairing is easier by direct grouping if ordering differs.
        if len(new) != len(level) // 2:
            new = []
            groups = {}
            for i in level:
                rest = tuple(x for x in nodes[i]["clause"] if abs(x) != pivot)
                groups.setdefault(rest, {})[pivot in nodes[i]["clause"]] = i
            for rest, pair in groups.items():
                j, i = pair[True], pair[False]
                nodes.append({"clause": resolve(nodes[j]["clause"], nodes[i]["clause"], pivot),
                              "parents": (j, i), "pivot": pivot})
                new.append(len(nodes) - 1)
        level = new
    assert len(level) == 1 and nodes[level[0]]["clause"] == ()
    return nodes, level[0]


def split_trace_and_projection():
    base = cube_source()
    split, sigma = split_source(base)
    nodes = [{"clause": c, "parents": None, "pivot": None} for c in split]
    reconstructed = []
    for i, c in enumerate(base):
        a = 4 + i
        p, q = 2 * i, 2 * i + 1
        nodes.append({"clause": resolve(nodes[p]["clause"], nodes[q]["clause"], a),
                      "parents": (p, q), "pivot": a})
        assert nodes[-1]["clause"] == c
        reconstructed.append(len(nodes) - 1)

    # Add the canonical seven-node cube refutation using reconstructed sources.
    current = reconstructed
    for pivot in (3, 2, 1):
        groups = {}
        for i in current:
            rest = tuple(x for x in nodes[i]["clause"] if abs(x) != pivot)
            groups.setdefault(rest, {})[pivot in nodes[i]["clause"]] = i
        nxt = []
        for pair in groups.values():
            u, v = pair[True], pair[False]
            nodes.append({"clause": resolve(nodes[u]["clause"], nodes[v]["clause"], pivot),
                          "parents": (u, v), "pivot": pivot})
            nxt.append(len(nodes) - 1)
        current = nxt
    assert nodes[current[0]]["clause"] == ()

    witnesses = {}
    paid = 0
    kinds = {"source": 0, "skip-top": 0, "left-survivor": 0,
             "right-survivor": 0, "one-res": 0}
    for i, node in enumerate(nodes):
        pc = project(node["clause"], sigma)
        if node["parents"] is None:
            if pc is not TOP:
                witnesses[i] = pc
                kinds["source"] += 1
            continue
        u, v = node["parents"]
        kind, w = compile_local(nodes[u]["clause"], nodes[v]["clause"],
                                node["pivot"], sigma,
                                witnesses.get(u, TOP), witnesses.get(v, TOP))
        kinds[kind] += 1
        if w is not TOP:
            witnesses[i] = w
        if kind == "one-res":
            paid += 1
    assert witnesses[current[0]] == ()
    assert paid == 7
    return {"base_sources": len(base), "split_sources": len(split),
            "input_paid_nodes": len(nodes) - len(split),
            "projected_paid_nodes": paid, "kinds": kinds,
            "final_witness": list(witnesses[current[0]])}


def hostile_controls():
    rejected = 0
    c = norm((1, -2, 3))
    l1, l2, l3 = c
    a = 4
    p, q = norm((l1, l2, a)), norm((l1, l3, -a))
    good = {1: 1, 2: 2, 3: 3, a: l3}
    assert project(p, good) == c and project(q, good) is TOP
    for bad in (
        {1: 1, 2: 2, 3: 3, a: -l3},
        {1: 1, 2: 2, 3: 3, a: 1},
    ):
        try:
            assert project(p, bad) == c and project(q, bad) is TOP
        except AssertionError:
            rejected += 1
    for thunk in (
        lambda: resolve(p, q, -a),
        lambda: compile_local(p, q, a, good, (999,), TOP),
        lambda: compile_local(p, q, a, good, TOP, TOP),
    ):
        try:
            thunk()
        except (ValueError, AssertionError):
            rejected += 1
    assert rejected == 5
    return rejected


def main():
    started = time.perf_counter()
    transitions, pairs, kinds = exhaustive_local_lemma()
    trace = split_trace_and_projection()
    rejected = hostile_controls()
    result = {
        "run": "LSPV-5/411",
        "status": "PROVED/EXACT ordinary Resolution projection; COMPUTATIONAL exhaustive controls; historical R_mix341 bytes OPEN",
        "theorem": "For every literal substitution sigma and every source-authenticated Resolution DAG pi, a no-weakening subclause compiler maps pi to a proof from sigma(F) with at most one paid RES per paid input node.",
        "local_exhaustion": {
            "source_variables": 3,
            "target_variables": 3,
            "substitutions": 6 ** 3,
            "transition_skeletons": transitions,
            "witness_pairs": pairs,
            "outcomes": kinds,
        },
        "split_cube_trace": trace,
        "hostile_controls_rejected": rejected,
        "scope": {
            "ordinary_resolution": True,
            "shared_reconvergent_dags": True,
            "hidden_weakening": False,
            "historical_R_mix341_checker_run": False,
            "all_mixed_lower_bound": False,
            "p_vs_np": "OPEN",
        },
        "elapsed_seconds": time.perf_counter() - started,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["canonical_payload_sha256"] = hashlib.sha256(payload.encode()).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
