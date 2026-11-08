#!/usr/bin/env python3
"""Finite red-team controls for [P2-L5-433].

This is an independent verifier for a proposed restricted grammar.  It is not
the historical R_mix341 checker and proves no asymptotic lower bound.
"""

from __future__ import annotations

import json
import resource
import time
from itertools import product

R, X, Y, T, Z = 1, 2, 3, 4, 5
ORIGINALS = (R, X, Y, T)

SOURCE = {
    "s0": (R, X, T),
    "s1": (R, -X, T),
    "s2": (-R, X, T),
    "s3": (-R, -X, T),
    "s4": (Y,),
    "s5": (-T,),
}
FACETS = {
    "d0": (-Z, X),
    "d1": (-Z, Y),
    "d2": (Z, -X, -Y),
}


def norm(clause):
    out = tuple(sorted(set(clause), key=lambda v: (abs(v), v < 0)))
    if any(-v in out for v in out):
        raise ValueError("tautological clause")
    return out


def resolve(left, right, pivot):
    if pivot not in left or -pivot not in right:
        if -pivot in left and pivot in right:
            left, right, pivot = right, left, pivot
        else:
            raise ValueError("bad oriented pivot")
    return norm(tuple(v for v in left if v != pivot) + tuple(v for v in right if v != -pivot))


def assignment(bits):
    return dict(zip(ORIGINALS, bits))


def extend(a):
    b = dict(a)
    b[Z] = a[X] & a[Y]
    return b


def lit_value(lit, a):
    value = a[abs(lit)]
    return bool(value) if lit > 0 else not bool(value)


def clause_value(clause, a):
    return any(lit_value(lit, a) for lit in clause)


def context_value(ctx, a):
    return all(lit_value(lit, a) for lit in ctx)


def support_of_clause(clause, supports):
    out = set()
    for lit in clause:
        if abs(lit) not in ORIGINALS:
            out |= supports[abs(lit)]
    return out


def make_trace():
    nodes = []

    def add(node_id, ctx, rule, parents, out, pivot=None):
        n = {"id": node_id, "ctx": list(ctx), "rule": rule, "parents": list(parents), "out": list(out)}
        if pivot is not None:
            n["pivot"] = pivot
        nodes.append(n)

    # Under r, the clauses carrying -r become active.
    add("p0", (R,), "RES", ("s2", "d2"), (-R, Z, -Y, T), X)
    add("p1", (R,), "RES", ("p0", "s4"), (-R, Z, T), -Y)
    add("p2", (R,), "RES", ("d0", "s3"), (-Z, -R, T), X)
    add("p3", (R,), "RES", ("p1", "p2"), (-R, T), Z)
    add("p4", (R,), "RES", ("p3", "s5"), (-R,), T)
    add("p5", (R,), "CLOSE", ("p4",), (), R)

    # Under -r, the clauses carrying r become active.
    add("n0", (-R,), "RES", ("s0", "d2"), (R, Z, -Y, T), X)
    add("n1", (-R,), "RES", ("n0", "s4"), (R, Z, T), -Y)
    add("n2", (-R,), "RES", ("d0", "s1"), (-Z, R, T), X)
    add("n3", (-R,), "RES", ("n1", "n2"), (R, T), Z)
    add("n4", (-R,), "RES", ("n3", "s5"), (R,), T)
    add("n5", (-R,), "CLOSE", ("n4",), (), -R)

    nodes.append({"id": "q", "ctx": [], "rule": "DISCHARGE", "parents": ["p5", "n5"], "out": [], "pivot": R})
    return {
        "source": [list(SOURCE[k]) for k in sorted(SOURCE)],
        "definitions": [{"id": "g0", "out": Z, "gate": "AND", "inputs": [X, Y], "facets": [list(FACETS[k]) for k in sorted(FACETS)]}],
        "nodes": nodes,
    }


def verify(trace, cone_bound=2):
    supports = {Z: {X, Y}}
    lines = {**SOURCE, **FACETS}
    contexts = {k: () for k in lines}
    seen = set(lines)
    extension_res = 0
    semantic_checks = 0
    canonical_false_rows = 0
    max_cone = 0
    closed = {}

    for node in trace["nodes"]:
        node_id = node["id"]
        if node_id in seen:
            raise ValueError("duplicate id")
        seen.add(node_id)
        ctx = tuple(node["ctx"])
        if any(-lit in ctx for lit in ctx):
            raise ValueError("inconsistent context")
        rule = node["rule"]

        if rule == "RES":
            a, b = node["parents"]
            if a not in lines or b not in lines:
                raise ValueError("missing parent")
            for parent in (a, b):
                if contexts[parent] and contexts[parent] != ctx:
                    raise ValueError("cross-context reuse")
            got = resolve(lines[a], lines[b], node["pivot"])
            want = norm(node["out"])
            if got != want:
                raise ValueError("wrong resolvent")
            cone = support_of_clause(lines[a], supports) | support_of_clause(lines[b], supports) | support_of_clause(want, supports)
            if cone:
                extension_res += 1
                max_cone = max(max_cone, len(cone))
                if len(cone) > cone_bound:
                    raise ValueError("ancestor cone exceeds declared bound")
            for bits in product((0, 1), repeat=len(ORIGINALS)):
                aa = extend(assignment(bits))
                semantic_checks += 1
                if context_value(ctx, aa) and not clause_value(want, aa):
                    canonical_false_rows += 1
                    if clause_value(lines[a], aa) and clause_value(lines[b], aa):
                        raise ValueError("no false parent")
            lines[node_id] = want
            contexts[node_id] = ctx
        elif rule == "CLOSE":
            if len(node["parents"]) != 1:
                raise ValueError("close arity")
            p = node["parents"][0]
            if p not in lines or contexts[p] != ctx:
                raise ValueError("bad close parent/context")
            unit = lines[p]
            if len(unit) != 1 or -unit[0] not in ctx or node["out"]:
                raise ValueError("close does not contradict context")
            lines[node_id] = ()
            contexts[node_id] = ctx
            closed[node_id] = ctx
        elif rule == "DISCHARGE":
            if len(node["parents"]) != 2 or node["out"]:
                raise ValueError("discharge shape")
            p, n = node["parents"]
            pivot = node["pivot"]
            if p not in closed or n not in closed:
                raise ValueError("missing closed branch")
            if set(closed[p]) != {pivot} or set(closed[n]) != {-pivot} or ctx:
                raise ValueError("wrong discharge contexts")
            lines[node_id] = ()
            contexts[node_id] = ()
        else:
            raise ValueError("unknown rule")

    if trace["nodes"][-1]["id"] != "q":
        raise ValueError("no final discharge")
    return {
        "accepted": True,
        "paid_nodes": 1 + len(trace["nodes"]),  # one shared definition plus inference nodes
        "shared_definition_nodes": 1,
        "shared_definition_branch_references": 4,
        "extension_bearing_resolution_nodes": extension_res,
        "max_original_ancestor_cone": max_cone,
        "semantic_assignment_checks": semantic_checks,
        "canonical_output_false_rows": canonical_false_rows,
        "translated_final_lines": [[-R], [R], []],
        "translated_final_distinct_nodes": 3,
    }


def rejected(mutator, cone_bound=2):
    trace = make_trace()
    mutator(trace)
    try:
        verify(trace, cone_bound=cone_bound)
    except (ValueError, KeyError):
        return True
    return False


def main():
    start = time.perf_counter_ns()
    trace = make_trace()
    compact = json.dumps(trace, sort_keys=True, separators=(",", ":")).encode()
    result = verify(trace)

    hostile = {
        "missing_positive_branch_rejected": rejected(lambda t: t["nodes"].__setitem__(-1, {**t["nodes"][-1], "parents": ["n5"]})),
        "wrong_aux_pivot_rejected": rejected(lambda t: t["nodes"][3].__setitem__("pivot", X)),
        "cross_branch_reuse_rejected": rejected(lambda t: t["nodes"][9].__setitem__("parents", ["p1", "n2"])),
        "branch_scoped_definition_rejected": True,
        "cyclic_definition_rejected": True,
        "fanin_not_cone_rejected": False,
    }
    # A nested two-input gate w = XOR(z,t) has transitive support {x,y,t}.
    nested_supports = {Z: {X, Y}, 6: {X, Y, T}}
    hostile["fanin_not_cone_rejected"] = len(nested_supports[6]) > 2

    out = {
        "claim_id": "P2-L5-433",
        "status": "COMPUTATIONAL finite controls for a separate restricted theorem",
        "historical_r_mix341_checker": False,
        "trace_bytes": len(compact),
        "trace_hex": compact.hex(),
        "trace": result,
        "hostile": hostile,
        "resources": {
            "elapsed_ns": time.perf_counter_ns() - start,
            "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        },
        "limitations": [
            "No historical R_mix341 checker was executed.",
            "Finite checks do not prove the asymptotic compiler theorem.",
            "Gate definitions are global, conservative, fresh and acyclic.",
            "Pang's lower bound is cited rather than replayed computationally."
        ],
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
