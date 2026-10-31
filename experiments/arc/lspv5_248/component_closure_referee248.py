#!/usr/bin/env python3
"""Exact component-closure controls for COMPONENT-CLOSURE-REFEREE248.

The program checks the source-faithful hereditary theorem independently:
a subset of unchanged clauses of a valid duplicate-free proper Monotone
3-SAT-(2,2) formula is again valid iff it is a union of incidence components.
It also replays the canonical connected SAT/UNSAT controls and all signed
clause-extreme bookkeeping used as adversarial controls.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import itertools
import json
import sys
import time
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt"
SOURCE = CANONICAL if CANONICAL.exists() else ROOT / "tmp/doecker61_source.txt"
OUT = ROOT / "results/raw/arc/2026-10-31_1248_LSPV5_COMPONENT_CLOSURE_REFEREE248_raw.json"
BASE = ROOT / "experiments/arc/lspv5_247/target_scope_flmv_referee247.py"


def load_base():
    spec = importlib.util.spec_from_file_location("ref247", BASE)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def load_source() -> list[list[int]]:
    text = "\n".join(x for x in SOURCE.read_text().splitlines() if not x.startswith("#"))
    return ast.literal_eval(text)


def y6() -> list[list[int]]:
    pos = [(1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6)]
    neg = [(1, 2, 4), (1, 3, 6), (2, 3, 5), (4, 5, 6)]
    return [list(c) for c in pos] + [[-x for x in c] for c in neg]


def shifted(clauses: list[list[int]], delta: int) -> list[list[int]]:
    return [[(1 if x > 0 else -1) * (abs(x) + delta) for x in c] for c in clauses]


def incidence_components(clauses: list[list[int]]) -> list[list[int]]:
    """Return clause-index components of the bipartite incidence graph."""
    by_var: dict[int, list[int]] = {}
    for j, clause in enumerate(clauses):
        for lit in clause:
            by_var.setdefault(abs(lit), []).append(j)
    seen: set[int] = set()
    out: list[list[int]] = []
    for start in range(len(clauses)):
        if start in seen:
            continue
        q = deque([start])
        seen.add(start)
        component = []
        while q:
            j = q.popleft()
            component.append(j)
            for lit in clauses[j]:
                for k in by_var[abs(lit)]:
                    if k not in seen:
                        seen.add(k)
                        q.append(k)
        out.append(sorted(component))
    return sorted(out, key=lambda x: x[0])


def valid_target(clauses: list[list[int]]) -> bool:
    if not clauses or any(len(c) != 3 for c in clauses):
        return False
    if any(len({abs(x) for x in c}) != 3 for c in clauses):
        return False
    if any(not (all(x > 0 for x in c) or all(x < 0 for x in c)) for c in clauses):
        return False
    norm = [tuple(sorted(c)) for c in clauses]
    if len(norm) != len(set(norm)):
        return False
    occ: Counter[tuple[int, int]] = Counter()
    for c in clauses:
        for lit in c:
            occ[(abs(lit), 1 if lit > 0 else -1)] += 1
    variables = {v for v, _ in occ}
    return all(occ[v, 1] == occ[v, -1] == 2 for v in variables)


def is_component_union(mask: int, components: list[list[int]]) -> bool:
    for component in components:
        selected = [(mask >> j) & 1 for j in component]
        if any(selected) and not all(selected):
            return False
    return mask != 0


def exhaustive_subset_audit(clauses: list[list[int]]) -> dict:
    components = incidence_components(clauses)
    tested = valid_count = union_count = mismatches = 0
    examples = []
    for mask in range(1, 1 << len(clauses)):
        tested += 1
        sub = [c for j, c in enumerate(clauses) if (mask >> j) & 1]
        valid = valid_target(sub)
        union = is_component_union(mask, components)
        valid_count += valid
        union_count += union
        if valid != union:
            mismatches += 1
            if len(examples) < 5:
                examples.append(mask)
    return {
        "clauses": len(clauses),
        "components": components,
        "subsets_tested": tested,
        "valid_subsets": valid_count,
        "component_unions": union_count,
        "mismatches": mismatches,
        "mismatch_examples": examples,
    }


def brute_models(clauses: list[list[int]]) -> int:
    n = max(abs(x) for c in clauses for x in c)
    count = 0
    for bits in itertools.product((False, True), repeat=n):
        if all(any(bits[abs(l) - 1] == (l > 0) for l in c) for c in clauses):
            count += 1
    return count


def formula_digest(clauses: list[list[int]]) -> str:
    return hashlib.sha256(json.dumps(clauses, separators=(",", ":")).encode()).hexdigest()


def main() -> int:
    started = time.perf_counter()
    base = load_base()
    u = load_source()
    v = [c[:] for c in u]
    v[2][-1], v[44][-1] = v[44][-1], v[2][-1]
    y = y6()
    yy = y + shifted(y, 6)

    # Exhaustive, independent reconstruction of the closure theorem.
    subset_audits = {
        "Y6_connected": exhaustive_subset_audit(y),
        "Y6_disjoint_union_Y6": exhaustive_subset_audit(yy),
    }
    assert subset_audits["Y6_connected"]["mismatches"] == 0
    assert subset_audits["Y6_disjoint_union_Y6"]["mismatches"] == 0
    assert subset_audits["Y6_connected"]["valid_subsets"] == 1
    assert subset_audits["Y6_disjoint_union_Y6"]["valid_subsets"] == 3

    controls = {}
    for name, clauses in (("U198", u), ("V198", v), ("Y6", y), ("Y6_union_Y6", yy)):
        components = incidence_components(clauses)
        controls[name] = {
            "valid": valid_target(clauses),
            "variables": len({abs(x) for c in clauses for x in c}),
            "clauses": len(clauses),
            "component_clause_sizes": [len(c) for c in components],
            "connected": len(components) == 1,
            "clause_sha256": formula_digest(clauses),
        }
        assert controls[name]["valid"]

    # Same-source both-label exact controls.
    controls["Y6"]["model_count"] = brute_models(y)
    controls["Y6_union_Y6"]["model_count"] = brute_models(yy)
    cert = base.module_certificate(u)
    assert cert["proved_unsat_254_clause_subformula"]
    controls["U198"]["exact_status"] = "UNSAT"
    controls["U198"]["certificate"] = cert
    witness = base.replay(v, base.SAT_WITNESS)
    assert witness["satisfied"]
    controls["V198"]["exact_status"] = "SAT"
    controls["V198"]["witness_sha256"] = hashlib.sha256(base.SAT_WITNESS.encode()).hexdigest()
    controls["V198"]["witness_replay"] = witness

    # Source-faithful one-clause deletion must fail on connected valid inputs.
    deletion_audit = {}
    for name, clauses in (("U198", u), ("V198", v), ("Y6", y)):
        surviving = [j for j in range(len(clauses)) if valid_target(clauses[:j] + clauses[j + 1 :])]
        deletion_audit[name] = {"deletions_tested": len(clauses), "valid_children": surviving}
        assert not surviving

    # Mandatory signed S/U controls; full rows are reproducible and hashed.
    extremes = {
        "U198": base.clause_extreme_control(u),
        "V198": base.clause_extreme_control(v),
    }

    # Quantitative obstruction: connected instances have no nonempty proper
    # source-faithful target child, so their largest available child is parent.
    contraction = {}
    for name in ("U198", "V198", "Y6"):
        m = controls[name]["clauses"]
        contraction[name] = {
            "parent_clauses": m,
            "proper_source_faithful_target_children": 0,
            "largest_nonempty_source_faithful_child_clauses": m,
            "ratio": 1.0,
        }

    raw = {
        "run_id": "COMPONENT-CLOSURE-REFEREE248",
        "source": str(SOURCE.relative_to(ROOT)),
        "theorem_tested": "unchanged-clause target child iff nonempty union of incidence components",
        "subset_audits": subset_audits,
        "controls": controls,
        "one_clause_deletion_audit": deletion_audit,
        "contraction_obstruction": contraction,
        "signed_clause_extremes": extremes,
        "resource_ledger": {
            "explicit_BFS_DSU_discovery": "linear input scan/time; Theta(parent vertices) writable words",
            "Reingold_transfer": "KNOWN THEOREM: deterministic O(log N) space and polynomial time for each undirected connectivity query",
            "indexed_child_accessor": "requires component membership plus clause/variable rank and output addressing; strict t<241/200 and s<11642479/23232400 simultaneously not established",
            "failed_trials_charged": ["all proper clause subsets on Y6", "all proper clause subsets on Y6 disjoint union Y6", "all one-clause deletions on U198/V198/Y6"],
            "retained_space": "raw experiment uses explicit parent-scale adjacency; this is an implementation cost, not an arbitrary-algorithm lower bound",
        },
        "elapsed_seconds": time.perf_counter() - started,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "subset_audits": subset_audits,
        "control_summary": {k: {x: v[x] for x in ("valid", "variables", "clauses", "component_clause_sizes", "connected")} for k, v in controls.items()},
        "status": {"U198": controls["U198"]["exact_status"], "V198": controls["V198"]["exact_status"]},
        "elapsed_seconds": raw["elapsed_seconds"],
        "output": str(OUT.relative_to(ROOT)),
    }, indent=2))
    print("VERIFIED::COMPONENT-CLOSURE-REFEREE248")
    return 0


if __name__ == "__main__":
    sys.exit(main())
