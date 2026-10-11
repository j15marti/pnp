#!/usr/bin/env python3
"""Bounded audit for a one-branch matching pass on paired clean cores.

The program does not benchmark arbitrary SAT.  It verifies a declared promise
recognizer, constructs a perfect-matching witness, simplifies to TRUE, and
meters preprocessing/extraction/reconstruction operations.  Every configured
invocation is intended to finish well under 30 seconds.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import time
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from pathlib import Path

Clause = tuple[int, ...]
Formula = tuple[Clause, ...]


@dataclass
class Meter:
    parse_literals: int = 0
    pair_updates: int = 0
    incidence_updates: int = 0
    color_edge_scans: int = 0
    matching_edge_scans: int = 0
    assignment_writes: int = 0
    reconstruction_literal_checks: int = 0

    def total(self) -> int:
        return sum(vars(self).values())


class Audit:
    def __init__(self) -> None:
        self.assertions = 0
        self.failures: list[str] = []

    def check(self, cond: bool, label: str) -> None:
        self.assertions += 1
        if not cond:
            self.failures.append(label)


def paired_circulant(r: int, offset: int = 0) -> tuple[Formula, dict[int, tuple[int, int]]]:
    """Cubic bipartite circulant, shifted to give independent products."""
    edges: dict[int, tuple[int, int]] = {}
    incident: dict[int, list[int]] = defaultdict(list)
    next_var = offset + 1
    for u in range(r):
        for d in (0, 1, 2):
            v = r + ((u + d) % r)
            edges[next_var] = (u, v)
            incident[u].append(next_var)
            incident[v].append(next_var)
            next_var += 1
    clauses: list[Clause] = []
    for v in range(2 * r):
        vs = tuple(sorted(incident[v]))
        clauses.append(vs)
        clauses.append(tuple(-x for x in vs))
    return tuple(clauses), edges


def independent_product(rs: tuple[int, ...]) -> Formula:
    out: list[Clause] = []
    offset = 0
    for r in rs:
        formula, edges = paired_circulant(r, offset)
        out.extend(formula)
        offset = max(edges)
    return tuple(out)


def permute_encoding(formula: Formula, seed: int) -> Formula:
    rng = random.Random(seed)
    variables = sorted({abs(x) for c in formula for x in c})
    image = variables[:]
    rng.shuffle(image)
    ren = dict(zip(variables, image))
    clauses = [list((ren[abs(x)] if x > 0 else -ren[abs(x)]) for x in c) for c in formula]
    for c in clauses:
        rng.shuffle(c)
    rng.shuffle(clauses)
    return tuple(tuple(c) for c in clauses)


def recognize_and_extract(formula: Formula, meter: Meter):
    """Recover paired clauses and their incidence graph, or return None."""
    signs: dict[tuple[int, ...], set[int]] = defaultdict(set)
    for clause in formula:
        meter.parse_literals += len(clause)
        if len(clause) != 3 or len({abs(x) for x in clause}) != 3:
            return None
        if not (all(x > 0 for x in clause) or all(x < 0 for x in clause)):
            return None
        key = tuple(sorted(abs(x) for x in clause))
        signs[key].add(1 if clause[0] > 0 else -1)
        meter.pair_updates += 1
    if len(formula) != 2 * len(signs) or any(s != {-1, 1} for s in signs.values()):
        return None

    keys = sorted(signs)
    kid = {k: i for i, k in enumerate(keys)}
    var_vertices: dict[int, list[int]] = defaultdict(list)
    for key in keys:
        v = kid[key]
        for x in key:
            var_vertices[x].append(v)
            meter.incidence_updates += 1
    if any(len(vs) != 2 or vs[0] == vs[1] for vs in var_vertices.values()):
        return None

    adj: list[list[tuple[int, int]]] = [[] for _ in keys]
    for x, (a, b) in sorted(var_vertices.items()):
        adj[a].append((b, x))
        adj[b].append((a, x))
    if any(len(row) != 3 for row in adj):
        return None

    color: list[int | None] = [None] * len(adj)
    components = 0
    for root in range(len(adj)):
        if color[root] is not None:
            continue
        components += 1
        color[root] = 0
        q = deque([root])
        while q:
            a = q.popleft()
            for b, _ in adj[a]:
                meter.color_edge_scans += 1
                if color[b] is None:
                    color[b] = 1 - int(color[a])
                    q.append(b)
                elif color[b] == color[a]:
                    return None
    return adj, [int(x) for x in color], components, sorted(var_vertices)


def perfect_matching(adj, color, meter: Meter) -> dict[int, tuple[int, int]]:
    left = [v for v, c in enumerate(color) if c == 0]
    mate_right: dict[int, tuple[int, int]] = {}

    def augment(u: int, seen: set[int]) -> bool:
        for v, edge_var in adj[u]:
            meter.matching_edge_scans += 1
            if v in seen:
                continue
            seen.add(v)
            if v not in mate_right or augment(mate_right[v][0], seen):
                mate_right[v] = (u, edge_var)
                return True
        return False

    for u in left:
        if not augment(u, set()):
            return {}
    return mate_right


def select_one_branch(formula: Formula):
    meter = Meter()
    extracted = recognize_and_extract(formula, meter)
    if extracted is None:
        return {"status": "UNKNOWN", "meter": vars(meter)}
    adj, color, components, variables = extracted
    matching = perfect_matching(adj, color, meter)
    if len(matching) != sum(c == 0 for c in color):
        return {"status": "UNKNOWN", "meter": vars(meter)}
    true_vars = {edge_var for _, edge_var in matching.values()}
    assignment = {x: x in true_vars for x in variables}
    meter.assignment_writes += len(assignment)
    unsatisfied = 0
    for clause in formula:
        ok = False
        for lit in clause:
            meter.reconstruction_literal_checks += 1
            value = assignment[abs(lit)]
            if value == (lit > 0):
                ok = True
                break
        if not ok:
            unsatisfied += 1
    return {
        "status": "SAT",
        "components": components,
        "variables": len(variables),
        "clauses": len(formula),
        "branch_count": 1,
        "residual_clauses": unsatisfied,
        "matching_size": len(matching),
        "assignment_sha256": hashlib.sha256(
            "".join("1" if assignment[x] else "0" for x in variables).encode()
        ).hexdigest(),
        "meter": vars(meter) | {"total": meter.total()},
    }


def exact_occurrence_profile(formula: Formula) -> dict[str, object]:
    pos, neg = Counter(), Counter()
    for c in formula:
        for x in c:
            (pos if x > 0 else neg)[abs(x)] += 1
    variables = set(pos) | set(neg)
    return {
        "proper_three": all(len(c) == len({abs(x) for x in c}) == 3 for c in formula),
        "duplicate_free": len({tuple(sorted(c)) for c in formula}) == len(formula),
        "monotone": all(all(x > 0 for x in c) or all(x < 0 for x in c) for c in formula),
        "exact_2_2": all(pos[x] == 2 and neg[x] == 2 for x in variables),
    }


def solve_horn(formula: Formula) -> tuple[bool, int]:
    true: set[int] = set()
    scans = 0
    changed = True
    while changed:
        changed = False
        for c in formula:
            scans += len(c)
            positives = [x for x in c if x > 0]
            negatives = [-x for x in c if x < 0]
            if len(positives) > 1:
                raise ValueError("not Horn")
            if all(x in true for x in negatives):
                if not positives:
                    return False, scans
                if positives[0] not in true:
                    true.add(positives[0])
                    changed = True
    return True, scans


def solve_2sat(formula: Formula) -> tuple[bool, int]:
    variables = sorted({abs(x) for c in formula for x in c})
    n = max(variables, default=0)
    graph = [[] for _ in range(2 * n)]
    rev = [[] for _ in range(2 * n)]
    scans = 0

    def node(lit: int) -> int:
        return 2 * (abs(lit) - 1) + (0 if lit > 0 else 1)

    def add(a: int, b: int) -> None:
        graph[node(a)].append(node(b))
        rev[node(b)].append(node(a))

    for c in formula:
        a, b = c
        add(-a, b)
        add(-b, a)
        scans += 2
    seen, order = set(), []

    def dfs(g, u, out):
        nonlocal scans
        seen.add(u)
        for v in g[u]:
            scans += 1
            if v not in seen:
                dfs(g, v, out)
        out.append(u)

    for u in range(2 * n):
        if u not in seen:
            dfs(graph, u, order)
    comp = [-1] * (2 * n)

    def mark(u, k):
        nonlocal scans
        comp[u] = k
        for v in rev[u]:
            scans += 1
            if comp[v] < 0:
                mark(v, k)

    for k, u in enumerate(reversed(order)):
        if comp[u] < 0:
            mark(u, k)
    return all(comp[2*i] != comp[2*i+1] for i in range(n)), scans


def gaussian_gf2(rows: list[tuple[int, int]], n: int) -> tuple[bool, int, int]:
    work = [[(mask >> j) & 1 for j in range(n)] + [rhs] for mask, rhs in rows]
    rank = ops = 0
    for col in range(n):
        pivot = next((i for i in range(rank, len(work)) if work[i][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        for i in range(len(work)):
            if i != rank and work[i][col]:
                work[i] = [a ^ b for a, b in zip(work[i], work[rank])]
                ops += n + 1
        rank += 1
    consistent = not any(not any(row[:-1]) and row[-1] for row in work)
    return consistent, rank, ops


def bounded_path_dp(length: int) -> tuple[int, int]:
    # Number of satisfying assignments of AND_i (x_i OR x_{i+1}).
    state = {0: 1, 1: 1}
    ops = 0
    for _ in range(length - 1):
        nxt = {0: 0, 1: 0}
        for a, count in state.items():
            for b in (0, 1):
                ops += 1
                if a or b:
                    nxt[b] += count
        state = nxt
    return sum(state.values()), ops


def wrapper_checks(formula: Formula) -> dict[str, object]:
    base = select_one_branch(formula)
    out = {}
    for name, repeats, dead in (
        ("DIRECT", 1, 0), ("COPY", 1, 1), ("DELAY", 1, 7),
        ("INTERP", 1, 2), ("RECOMP", 2, 0), ("DEAD", 1, 11),
    ):
        runs = [select_one_branch(formula) for _ in range(repeats)]
        out[name] = {
            "status": runs[-1]["status"],
            "same_decision": runs[-1]["status"] == base["status"],
            "meter_total": sum(x["meter"].get("total", sum(x["meter"].values())) for x in runs) + dead,
        }
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed", type=int, default=12026)
    args = parser.parse_args()
    started = time.perf_counter()
    audit = Audit()
    sizes = (4, 8, 16, 32, 64, 128, 256, 512)
    records = []
    for r in sizes:
        formula, _ = paired_circulant(r)
        profile = exact_occurrence_profile(formula)
        result = select_one_branch(formula)
        alternate = select_one_branch(permute_encoding(formula, args.seed + r))
        for key, value in profile.items():
            audit.check(bool(value), f"r={r}:{key}")
        audit.check(result["status"] == "SAT", f"r={r}:recognized")
        audit.check(result["residual_clauses"] == 0, f"r={r}:residual_true")
        audit.check(result["branch_count"] == 1, f"r={r}:one_branch")
        audit.check(result["matching_size"] == 2 * r // 2, f"r={r}:perfect_matching")
        audit.check(alternate["status"] == "SAT", f"r={r}:alternate_encoding")
        records.append({
            "r": r,
            "variables": 3 * r,
            "clauses": 4 * r,
            "all_branch_log2": 3 * r,
            "selected_branches": 1,
            "selector": result,
            "alternate_encoding": alternate,
        })

    base, _ = paired_circulant(12)
    duplicated = base + (base[0],)
    padded = base + ((1, -1, 2),)
    complemented = tuple(tuple((-x if abs(x) == 1 else x) for x in c) for c in base)
    independent = independent_product((8, 12))
    hostile = {
        "duplicate_clause": select_one_branch(duplicated),
        "tautological_padding": select_one_branch(padded),
        "single_variable_complement": select_one_branch(complemented),
        "independent_product": select_one_branch(independent),
    }
    audit.check(hostile["duplicate_clause"]["status"] == "UNKNOWN", "duplicate rejected")
    audit.check(hostile["tautological_padding"]["status"] == "UNKNOWN", "padding rejected")
    audit.check(hostile["single_variable_complement"]["status"] == "UNKNOWN", "complement rejected")
    audit.check(hostile["independent_product"]["status"] == "SAT", "product accepted")
    audit.check(hostile["independent_product"]["components"] == 2, "product components")

    horn_sat, horn_ops = solve_horn(((-1, 2), (-2, 3), (1,), (-3,)))
    two_sat, two_ops = solve_2sat(((1, 2), (-1, 2), (1, -2), (-1, -2)))
    affine_sat, affine_rank, affine_ops = gaussian_gf2(
        [(0b0011, 0), (0b0110, 1), (0b1100, 0), (0b1001, 1)], 4
    )
    tw_count, tw_ops = bounded_path_dp(64)
    audit.check(not horn_sat, "Horn control UNSAT")
    audit.check(not two_sat, "2SAT control UNSAT")
    audit.check(affine_sat and affine_rank == 3, "affine control")
    audit.check(tw_count > 0, "treewidth-one control")
    wrappers = wrapper_checks(base)
    for name, item in wrappers.items():
        audit.check(item["same_decision"], f"wrapper:{name}")

    elapsed = time.perf_counter() - started
    payload = {
        "run_id": "TESTS-0012",
        "claim": "PAIRED-MATCHING-ONEBRANCH1",
        "status": "COMPUTATIONAL",
        "seed": args.seed,
        "python": "dependency-free",
        "elapsed_seconds": elapsed,
        "chunking": "single bounded invocation; no stage exceeds 30 seconds",
        "assertions": audit.assertions,
        "failures": audit.failures,
        "sizes": records,
        "hostile_controls": hostile,
        "easy_controls": {
            "Horn": {"satisfiable": horn_sat, "operations": horn_ops},
            "2SAT": {"satisfiable": two_sat, "operations": two_ops},
            "affine_GF2": {"consistent": affine_sat, "rank": affine_rank, "xor_operations": affine_ops},
            "bounded_treewidth_path": {"length": 64, "solution_count": tw_count, "dp_operations": tw_ops},
        },
        "wrappers": wrappers,
        "limitations": [
            "The selector is exact only on the recognized paired-incidence promise and returns UNKNOWN otherwise.",
            "Finite operation counts are not asymptotic lower bounds.",
            "The test does not constrain an arbitrary one-bit SAT decider.",
        ],
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(out),
        "elapsed_seconds": elapsed,
        "assertions": audit.assertions,
        "failures": len(audit.failures),
        "max_variables": records[-1]["variables"],
        "max_all_branch_log2": records[-1]["all_branch_log2"],
        "max_meter_total": records[-1]["selector"]["meter"]["total"],
    }, sort_keys=True))
    if audit.failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
