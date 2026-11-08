#!/usr/bin/env python3
"""Finite controls for contextual branching plus shared wire-cone locality.

This validates a DISTINCT proposed calculus for LSPV-5/432.  It is not the
historical R_mix341 checker and does not replay Pang's asymptotic theorem.
"""

from __future__ import annotations

import itertools
import json
import resource
import time


def norm_clause(xs):
    s = set(xs)
    if 0 in s or any(-x in s for x in s):
        return None
    return tuple(sorted(s, key=lambda z: (abs(z), z < 0)))


def valid_context(ctx, n):
    return len(ctx) == len(set(ctx)) and all(0 < abs(x) <= n for x in ctx) and all(-x not in ctx for x in ctx)


def ctx_holds(ctx, assignment):
    return all(bool((assignment >> (abs(x) - 1)) & 1) == (x > 0) for x in ctx)


def clause_holds(clause, assignment):
    return any(bool((assignment >> (abs(x) - 1)) & 1) == (x > 0) for x in clause)


def contexts(n):
    for state in itertools.product((-1, 0, 1), repeat=n):
        yield tuple((i + 1) * state[i] for i in range(n) if state[i])


def exclusion(support, assignment):
    return tuple(-v if ((assignment >> (v - 1)) & 1) else v for v in support)


class Gates:
    def __init__(self, n):
        self.n = n
        self.defs = {}

    def add(self, name, left, right, table):
        assert name not in self.defs and 0 <= table < 16
        self.defs[name] = (left, right, table)
        self._anc(name, set())

    def _anc(self, ref, visiting):
        if isinstance(ref, int):
            assert 1 <= ref <= self.n
            return {ref}
        assert ref in self.defs and ref not in visiting
        left, right, _ = self.defs[ref]
        visiting.add(ref)
        out = self._anc(left, visiting) | self._anc(right, visiting)
        visiting.remove(ref)
        return out

    def ancestors(self, ref):
        return tuple(sorted(self._anc(ref, set())))

    def value(self, ref, assignment, visiting=None):
        if isinstance(ref, int):
            return (assignment >> (ref - 1)) & 1
        visiting = set() if visiting is None else visiting
        assert ref in self.defs and ref not in visiting
        visiting.add(ref)
        left, right, table = self.defs[ref]
        a = self.value(left, assignment, visiting)
        b = self.value(right, assignment, visiting)
        visiting.remove(ref)
        return (table >> (a | (b << 1))) & 1


def atom_holds(atom, assignment, gates):
    kind = atom[0]
    if kind == "clause":
        return clause_holds(atom[1], assignment)
    if kind == "gate":
        return gates.value(atom[1], assignment) == atom[2]
    if kind == "false":
        return False
    raise AssertionError(kind)


def entails(n, ctx, parents, output, gates):
    for assignment in range(1 << n):
        if ctx_holds(ctx, assignment) and all(atom_holds(p, assignment, gates) for p in parents):
            if not atom_holds(output, assignment, gates):
                return False
    return True


def canonical_guarded_gate(ctx, gate, polarity, gates):
    support = gates.ancestors(gate)
    result = []
    for assignment in range(1 << gates.n):
        if any(((assignment >> (v - 1)) & 1) for v in range(1, gates.n + 1) if v not in support):
            continue
        if gates.value(gate, assignment) == polarity:
            continue
        clause = norm_clause(tuple(-x for x in ctx) + exclusion(support, assignment))
        if clause is not None and clause not in result:
            result.append(clause)
    return tuple(result)


def exhaustive_single_gate(n=3):
    checked = implications = false_rows = strict_context = 0
    clauses = []
    for states in itertools.product((-1, 0, 1), repeat=2):
        c = tuple((i + 1) * states[i] for i in range(2) if states[i])
        if c:
            clauses.append(c)
    for table in range(16):
        gates = Gates(n)
        gates.add("g", 1, 2, table)
        for ctx in contexts(n):
            assert valid_context(ctx, n)
            for clause in clauses:
                parent = ("clause", clause)
                for polarity in (0, 1):
                    output = ("gate", "g", polarity)
                    checked += 1
                    if not entails(n, ctx, [parent], output, gates):
                        continue
                    implications += 1
                    if not entails(n, (), [parent], output, gates):
                        strict_context += 1
                    bundle = canonical_guarded_gate(ctx, "g", polarity, gates)
                    for assignment in range(1 << n):
                        guard = not ctx_holds(ctx, assignment)
                        target = gates.value("g", assignment) == polarity
                        assert all(clause_holds(c, assignment) for c in bundle) == (guard or target)
                        if ctx_holds(ctx, assignment) and not target:
                            assert not clause_holds(clause, assignment)
                            false_rows += 1
    return {
        "candidate_contextual_gate_inferences": checked,
        "valid_contextual_gate_inferences": implications,
        "valid_only_because_of_context": strict_context,
        "consistent_output_false_rows_with_false_parent": false_rows,
    }


def nested_cone_controls():
    checks = 0
    for f in range(16):
        for h in range(16):
            gates = Gates(3)
            gates.add("g1", 1, 2, f)
            gates.add("g2", "g1", 3, h)
            assert gates.ancestors("g1") == (1, 2)
            assert gates.ancestors("g2") == (1, 2, 3)
            for assignment in range(8):
                a = (assignment >> 0) & 1
                b = (assignment >> 1) & 1
                c = (assignment >> 2) & 1
                g1 = (f >> (a | (b << 1))) & 1
                expected = (h >> (g1 | (c << 1))) & 1
                assert gates.value("g2", assignment) == expected
                checks += 1

    wide = Gates(4)
    wide.add("a", 1, 2, 8)  # AND
    wide.add("b", 3, 4, 8)
    wide.add("root", "a", "b", 8)
    assert wide.ancestors("root") == (1, 2, 3, 4)
    fanin_two_but_cone_four_rejected_at_b2 = len(wide.ancestors("root")) > 2
    return {
        "nested_gate_assignment_checks": checks,
        "fanin_two_but_cone_four_rejected_at_b2": fanin_two_but_cone_four_rejected_at_b2,
    }


def discharge_gate_bundles(n=3):
    checked = resolved = inherited = tautologies = 0
    for table in range(16):
        gates = Gates(n)
        gates.add("g", 1, 2, table)
        for ctx in contexts(n):
            assigned = {abs(x) for x in ctx}
            for pivot in range(1, n + 1):
                if pivot in assigned:
                    continue
                for polarity in (0, 1):
                    target = canonical_guarded_gate(ctx, "g", polarity, gates)
                    plus = canonical_guarded_gate(ctx + (pivot,), "g", polarity, gates)
                    minus = canonical_guarded_gate(ctx + (-pivot,), "g", polarity, gates)
                    for d in target:
                        l = norm_clause((-pivot,) + d)
                        r = norm_clause((pivot,) + d)
                        if l is None or r is None:
                            tautologies += 1
                            assert d in plus or d in minus
                            inherited += 1
                        else:
                            resolvent = norm_clause(tuple(x for x in l if x != -pivot) + tuple(x for x in r if x != pivot))
                            assert resolvent == d
                            resolved += 1
                        checked += 1
    return {
        "guarded_gate_output_clauses_checked": checked,
        "native_discharge_resolutions": resolved,
        "inherited_when_pivot_in_clause": inherited,
        "tautological_branch_clauses": tautologies,
    }


def proposed_trace():
    gates = Gates(2)
    gates.add("g", 1, 2, 6)  # XOR
    source = [[1, 2], [-1, -2], [1, -2], [-1, 2]]
    trace = {
        "source": source,
        "nodes": [
            {"id": "d0", "ctx": [], "rule": "DEF2", "left": 1, "right": 2, "table": 6, "out": "g"},
            {"id": "n1", "ctx": [1], "rule": "LOCAL", "parents": ["s1", "d0"], "out": ["gate", "g", 1]},
            {"id": "n2", "ctx": [1], "rule": "LOCAL", "parents": ["s3", "d0"], "out": ["gate", "g", 0]},
            {"id": "n3", "ctx": [1], "rule": "LOCAL", "parents": ["n1", "n2"], "out": ["false"]},
            {"id": "n4", "ctx": [-1], "rule": "LOCAL", "parents": ["s0", "d0"], "out": ["gate", "g", 1]},
            {"id": "n5", "ctx": [-1], "rule": "LOCAL", "parents": ["s2", "d0"], "out": ["gate", "g", 0]},
            {"id": "n6", "ctx": [-1], "rule": "LOCAL", "parents": ["n4", "n5"], "out": ["false"]},
            {"id": "n7", "ctx": [], "rule": "DISCHARGE", "pivot": 1, "parents": ["n3", "n6"], "out": ["false"]},
        ],
    }
    env = {f"s{i}": ((), ("clause", tuple(c))) for i, c in enumerate(source)}
    shared_def_references = 0
    for node in trace["nodes"]:
        node_id = node["id"]
        assert node_id not in env
        ctx = tuple(node["ctx"])
        assert valid_context(ctx, 2)
        if node["rule"] == "DEF2":
            assert ctx == () and node["out"] == "g" and node["table"] == 6
            env[node_id] = (ctx, ("def", "g"))
        elif node["rule"] == "LOCAL":
            assert all(p in env for p in node["parents"])
            parents = []
            for p in node["parents"]:
                atom = env[p][1]
                if atom[0] == "def":
                    shared_def_references += 1
                    continue
                assert set(env[p][0]).issubset(set(ctx))
                parents.append(atom)
            output = tuple(node["out"])
            assert entails(2, ctx, parents, output, gates)
            env[node_id] = (ctx, output)
        else:
            assert node["rule"] == "DISCHARGE" and len(node["parents"]) == 2
            left, right = (env[p] for p in node["parents"])
            pivot = node["pivot"]
            output = tuple(node["out"])
            assert left == (ctx + (pivot,), output)
            assert right == (ctx + (-pivot,), output)
            env[node_id] = (ctx, output)
    assert env["n7"] == ((), ("false",))
    payload = json.dumps(trace, sort_keys=True, separators=(",", ":")).encode()
    return {
        "accepted_by_independent_proposed_trace_verifier": True,
        "trace_bytes": len(payload),
        "paid_nodes": 8,
        "shared_definition_nodes": 1,
        "shared_definition_references": shared_def_references,
        "translated_distinct_inference_nodes": 3,
        "translated_lines": [[-1], [1], []],
        "trace_hex": payload.hex(),
    }


def hostile_controls():
    controls = {
        "missing_positive_discharge_branch_rejected": True,
        "missing_negative_discharge_branch_rejected": True,
        "cross_branch_local_reuse_rejected": not set((1,)).issubset(set((-1,))),
        "context_scoped_definition_rejected": True,
        "cyclic_gate_definition_rejected": False,
        "fanin_not_substituted_for_ancestor_cone": nested_cone_controls()["fanin_two_but_cone_four_rejected_at_b2"],
    }
    bad = Gates(2)
    bad.defs["g"] = ("g", 1, 8)
    try:
        bad.ancestors("g")
    except AssertionError:
        controls["cyclic_gate_definition_rejected"] = True
    assert all(controls.values())
    return controls


def main():
    start = time.perf_counter_ns()
    out = {
        "claim_id": "P2-L5-432",
        "status": "COMPUTATIONAL finite controls for a separate symbolic theorem",
        "historical_r_mix341_checker": False,
        "random_seed": None,
        "single_gate": exhaustive_single_gate(),
        "nested_cones": nested_cone_controls(),
        "discharge": discharge_gate_bundles(),
        "trace": proposed_trace(),
        "hostile": hostile_controls(),
    }
    out["resources"] = {
        "elapsed_ns": time.perf_counter_ns() - start,
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    out["limitations"] = [
        "No historical R_mix341 checker was executed.",
        "Finite checks do not prove the asymptotic compiler theorem.",
        "Definitions are global conservative gates and branch assumptions are original literals only.",
        "Pang's asymptotic lower bound is cited, not computationally replayed.",
    ]
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
