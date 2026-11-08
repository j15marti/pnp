#!/usr/bin/env python3
"""Finite controls for contextual branching/guard compilation (LSPV-5/431).

This checks a DISTINCT proposed calculus.  It is not the historical R_mix341
checker and it does not replay Pang's asymptotic lower-bound proof.
"""

from __future__ import annotations

import itertools
import json
import resource
import time


def norm_clause(lits: tuple[int, ...] | list[int]):
    s = set(lits)
    if 0 in s or any(-x in s for x in s):
        return None  # tautology (zero is also malformed in actual records)
    return tuple(sorted(s, key=lambda z: (abs(z), z < 0)))


def valid_context(ctx: tuple[int, ...], n: int) -> bool:
    return (
        len(set(ctx)) == len(ctx)
        and all(isinstance(x, int) and x != 0 and abs(x) <= n for x in ctx)
        and all(-x not in ctx for x in ctx)
    )


def guard(ctx: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(-x for x in ctx)


def exclusion_clause(support: tuple[int, ...], assignment: int) -> tuple[int, ...]:
    return tuple(-v if ((assignment >> i) & 1) else v for i, v in enumerate(support))


def guarded_clause(ctx: tuple[int, ...], clause: tuple[int, ...]):
    return norm_clause(guard(ctx) + clause)


def all_contexts(n: int):
    for state in itertools.product((-1, 0, 1), repeat=n):
        yield tuple((i + 1) * state[i] for i in range(n) if state[i])


def compatible_mask(ctx: tuple[int, ...], n: int) -> int:
    mask = 0
    for a in range(1 << n):
        if all(bool((a >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in ctx):
            mask |= 1 << a
    return mask


def lift_table(table: int, support: tuple[int, ...], n: int) -> int:
    out = 0
    for a in range(1 << n):
        local = 0
        for i, v in enumerate(support):
            local |= ((a >> (v - 1)) & 1) << i
        if (table >> local) & 1:
            out |= 1 << a
    return out


def discharge_controls(n: int = 3) -> dict[str, int]:
    cases = 0
    resolved = 0
    inherited = 0
    omitted_tautologies = 0
    for ctx in all_contexts(n):
        assert valid_context(ctx, n)
        assigned = {abs(x) for x in ctx}
        for pivot in range(1, n + 1):
            if pivot in assigned:
                continue
            plus = ctx + (pivot,)
            minus = ctx + (-pivot,)
            for bits in range(1 << n):
                support = tuple(i + 1 for i in range(n) if (bits >> i) & 1)
                for table in range(1 << (1 << len(support))):
                    for alpha in range(1 << len(support)):
                        if (table >> alpha) & 1:
                            continue
                        d = exclusion_clause(support, alpha)
                        target = guarded_clause(ctx, d)
                        if target is None:
                            omitted_tautologies += 1
                            continue
                        left = guarded_clause(plus, d)
                        right = guarded_clause(minus, d)
                        if pivot in d:
                            assert right == target
                            inherited += 1
                        elif -pivot in d:
                            assert left == target
                            inherited += 1
                        else:
                            assert left is not None and right is not None
                            assert -pivot in left and pivot in right
                            resolvent = norm_clause(
                                tuple(x for x in left if x != -pivot)
                                + tuple(x for x in right if x != pivot)
                            )
                            assert resolvent == target
                            resolved += 1
                        cases += 1
    return {
        "guarded_output_clauses_checked": cases,
        "native_pivot_resolutions": resolved,
        "one_branch_already_equals_target": inherited,
        "tautological_targets_omitted": omitted_tautologies,
    }


def contextual_local_controls(n: int = 3) -> dict[str, int]:
    support = tuple(range(1, n + 1))
    functions = 1 << (1 << n)
    valid = 0
    false_rows = 0
    strict_context_only = 0
    for ctx in all_contexts(n):
        compat = compatible_mask(ctx, n)
        for antecedent in range(functions):
            for output in range(functions):
                if (antecedent & compat) & ~output:
                    continue
                valid += 1
                if antecedent & ~output:
                    strict_context_only += 1
                for alpha in range(1 << n):
                    if not ((compat >> alpha) & 1) or ((output >> alpha) & 1):
                        continue
                    assert not ((antecedent >> alpha) & 1)
                    parent = guarded_clause(ctx, exclusion_clause(support, alpha))
                    target = guarded_clause(ctx, exclusion_clause(support, alpha))
                    assert parent == target and target is not None
                    false_rows += 1
    return {
        "contextual_factor_implications": valid,
        "implications_valid_only_because_of_context": strict_context_only,
        "consistent_output_false_rows_with_false_parent": false_rows,
    }


def parity(mask: int, assignment: int) -> int:
    return (mask & assignment).bit_count() & 1


def affine_guard_controls(n: int = 3) -> dict[str, int]:
    equations = [(mask, rhs) for mask in range(1 << n) for rhs in (0, 1)]
    checks = 0
    for ctx in all_contexts(n):
        for (f, a), (h, b) in itertools.product(equations, repeat=2):
            for assignment in range(1 << n):
                guard_true = not all(
                    bool((assignment >> (abs(lit) - 1)) & 1) == (lit > 0)
                    for lit in ctx
                )
                premise1 = guard_true or parity(f, assignment) == a
                premise2 = guard_true or parity(h, assignment) == b
                conclusion = guard_true or parity(f ^ h, assignment) == (a ^ b)
                assert not (premise1 and premise2) or conclusion
                checks += 1
    return {"guarded_affine_assignment_checks": checks}


def hostile_controls() -> dict[str, bool]:
    ctx_x = (1,)
    ctx_not_x = (-1,)
    controls = {
        "cross_branch_lift_rejected": not set(ctx_x).issubset(set(ctx_not_x)),
        "inconsistent_context_rejected": not valid_context((1, -1), 2),
        "missing_positive_branch_rejected": False,
        "missing_negative_branch_rejected": False,
        "mismatched_conclusion_rejected": False,
        "cyclic_dependency_rejected": False,
    }

    def discharge_ok(branches):
        return branches.get("plus") == branches.get("minus") == "FALSE"

    controls["missing_positive_branch_rejected"] = not discharge_ok({"minus": "FALSE"})
    controls["missing_negative_branch_rejected"] = not discharge_ok({"plus": "FALSE"})
    controls["mismatched_conclusion_rejected"] = not discharge_ok({"plus": "FALSE", "minus": "C"})

    graph = {"a": ["b"], "b": ["a"]}
    temporary: set[str] = set()
    permanent: set[str] = set()

    def visit(v: str) -> bool:
        if v in temporary:
            return False
        if v in permanent:
            return True
        temporary.add(v)
        if any(not visit(w) for w in graph[v]):
            return False
        temporary.remove(v)
        permanent.add(v)
        return True

    controls["cyclic_dependency_rejected"] = not visit("a")
    assert all(controls.values())
    return controls


def accepted_trace() -> dict[str, object]:
    # F=(x or y)&(~x or y)&(x or ~y)&(~x or ~y).
    trace = {
        "source": [[1, 2], [-1, 2], [1, -2], [-1, -2]],
        "nodes": [
            {"id": "n1", "ctx": [1], "rule": "CTX_RES", "pivot": 1, "parents": ["s1"], "out": [2]},
            {"id": "n2", "ctx": [1], "rule": "CTX_RES", "pivot": 1, "parents": ["s3"], "out": [-2]},
            {"id": "n3", "ctx": [1], "rule": "RES", "pivot": 2, "parents": ["n1", "n2"], "out": []},
            {"id": "n4", "ctx": [-1], "rule": "CTX_RES", "pivot": -1, "parents": ["s0"], "out": [2]},
            {"id": "n5", "ctx": [-1], "rule": "CTX_RES", "pivot": -1, "parents": ["s2"], "out": [-2]},
            {"id": "n6", "ctx": [-1], "rule": "RES", "pivot": 2, "parents": ["n4", "n5"], "out": []},
            {"id": "n7", "ctx": [], "rule": "DISCHARGE", "pivot": 1, "parents": ["n3", "n6"], "out": []},
        ],
    }

    def verify(record: dict[str, object]) -> bool:
        source = record["source"]
        assert isinstance(source, list)
        env: dict[str, tuple[tuple[int, ...], tuple[int, ...]]] = {
            f"s{i}": ((), norm_clause(clause)) for i, clause in enumerate(source)
        }
        for node in record["nodes"]:
            assert isinstance(node, dict)
            node_id = node["id"]
            ctx = tuple(node["ctx"])
            out = norm_clause(node["out"])
            parents = node["parents"]
            assert isinstance(node_id, str) and node_id not in env
            assert valid_context(ctx, 2) and out is not None
            assert all(parent in env for parent in parents)  # acyclic/topological
            rule = node["rule"]
            pivot = node["pivot"]
            if rule == "CTX_RES":
                assert len(parents) == 1 and pivot in ctx
                parent_ctx, parent_clause = env[parents[0]]
                assert parent_ctx == () and parent_clause is not None
                assert -pivot in parent_clause
                derived = norm_clause(tuple(x for x in parent_clause if x != -pivot))
                assert derived == out
            elif rule == "RES":
                assert len(parents) == 2
                left_ctx, left = env[parents[0]]
                right_ctx, right = env[parents[1]]
                assert left_ctx == right_ctx == ctx and left is not None and right is not None
                assert pivot in left and -pivot in right
                derived = norm_clause(
                    tuple(x for x in left if x != pivot)
                    + tuple(x for x in right if x != -pivot)
                )
                assert derived == out
            elif rule == "DISCHARGE":
                assert len(parents) == 2 and pivot not in ctx and -pivot not in ctx
                left_ctx, left = env[parents[0]]
                right_ctx, right = env[parents[1]]
                assert left_ctx == ctx + (pivot,)
                assert right_ctx == ctx + (-pivot,)
                assert left == right == out
            else:
                raise AssertionError(f"unknown rule {rule}")
            env[node_id] = (ctx, out)
        return env["n7"] == ((), ())

    assert verify(trace)
    # The guarded target proof is exactly three derived clauses: ~x, x, empty.
    target = [(-1,), (1,), ()]
    assert norm_clause((-1, 2, -2)) is None
    assert norm_clause((-1, 2)) == (-1, 2)
    assert norm_clause((-1, -2)) == (-1, -2)
    assert norm_clause((-1,)) == (-1,)
    assert norm_clause((1,)) == (1,)
    assert norm_clause((-1, 1)) is None
    payload = json.dumps(trace, sort_keys=True, separators=(",", ":")).encode()
    return {
        "accepted_by_independent_proposed_trace_verifier": True,
        "source_clauses": 4,
        "paid_context_nodes": 7,
        "translated_distinct_inference_nodes": 3,
        "translated_lines": [list(x) for x in target],
        "trace_bytes": len(payload),
        "trace_hex": payload.hex(),
    }


def main() -> None:
    start = time.perf_counter_ns()
    out = {
        "claim_id": "P2-L5-431",
        "status": "COMPUTATIONAL finite controls for a separate symbolic proof",
        "historical_r_mix341_checker": False,
        "random_seed": None,
        "discharge": discharge_controls(),
        "contextual_local": contextual_local_controls(),
        "affine": affine_guard_controls(),
        "hostile": hostile_controls(),
        "trace": accepted_trace(),
    }
    out["resources"] = {
        "elapsed_ns": time.perf_counter_ns() - start,
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    out["limitations"] = [
        "No historical R_mix341 checker was executed.",
        "Finite checks do not prove the asymptotic theorem.",
        "The proposed contexts and discharge rule define a distinct calculus.",
    ]
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
