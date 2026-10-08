#!/usr/bin/env python3
"""Exact partial cover builders for the remaining WRAPPER link.

This is a bounded experiment, not a general SAT shrinker.  Every successful
plan is a forward AND/OR circuit whose recursive leaves are explicit CNFs no
larger than floor(M^(2/3)).  Construction uses only source-checkable rules:

* unit propagation, tautology deletion, and clause subsumption;
* exact AND decomposition into variable-disjoint components;
* direct Horn, 2-CNF, and bounded ordered-frontier solvers;
* fixed-size strong backdoors and clause-induced backdoor DNFs;
* a disjoint first-satisfied-literal cover of a source clause;
* exact equality and oriented clause-set dominance inside OR frontiers.

The program separately charges construction reads, exact plan replay, output
fanout, maximum child encoding, and a conservative logical-workspace ledger.
It has a 25-second internal alarm.  Run under a roughly 30-second hard cap:

    timeout 30s python3 final_link_hybrid_builder.py OUTPUT.json
"""

from __future__ import annotations

import hashlib
import itertools as it
import json
import math
import random
import signal
import sys
import time
from collections import Counter, deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

Clause = Tuple[int, ...]
Formula = Tuple[Clause, ...]
Assignment = Dict[int, bool]


def deadline(*_args: object) -> None:
    raise TimeoutError("25-second internal budget reached; split the batch")


def clause_key(c: Clause) -> Tuple[int, Tuple[int, ...]]:
    return len(c), c


def canonical(raw: Iterable[Iterable[int]], met: Optional[Counter] = None) -> Formula:
    """Remove tautologies/duplicates and perform exact clause subsumption."""
    rows = []
    for raw_clause in raw:
        if met is not None:
            met["construction_clause_reads"] += 1
        seen = set()
        tautology = False
        for lit in raw_clause:
            if met is not None:
                met["construction_literal_reads"] += 1
            if -lit in seen:
                tautology = True
            seen.add(lit)
        if tautology:
            if met is not None:
                met["tautologies_deleted"] += 1
            continue
        rows.append(tuple(sorted(seen, key=lambda x: (abs(x), x < 0))))
    rows = sorted(set(rows), key=clause_key)
    keep: List[Clause] = []
    keep_sets: List[frozenset[int]] = []
    for c in rows:
        cs = frozenset(c)
        dominated = False
        for old in keep_sets:
            if met is not None:
                met["subsumption_comparisons"] += 1
            if old <= cs:
                dominated = True
                break
        if dominated:
            if met is not None:
                met["subsumed_clauses_deleted"] += 1
            continue
        keep.append(c)
        keep_sets.append(cs)
    return tuple(keep)


def variables(f: Formula) -> Tuple[int, ...]:
    return tuple(sorted({abs(x) for c in f for x in c}))


def encoding_bits(f: Formula) -> int:
    nlabel = max((abs(x) for c in f for x in c), default=0)
    width = max(1, (nlabel + 1).bit_length())
    return width + sum(width + (width + 1) * len(c) for c in f)


def satisfies(f: Formula, a: Assignment) -> bool:
    return all(any(a.get(abs(x), False) == (x > 0) for x in c) for c in f)


def restrict_formula(f: Formula, a: Assignment, met: Counter) -> Formula:
    out: List[Clause] = []
    met["restriction_calls"] += 1
    met["parent_restriction_passes"] += 1
    met["parent_restriction_literal_reads"] += sum(map(len, f))
    for c in f:
        met["construction_clause_reads"] += 1
        residual: List[int] = []
        hit = False
        for lit in c:
            met["construction_literal_reads"] += 1
            v = abs(lit)
            if v in a:
                if a[v] == (lit > 0):
                    hit = True
                    break
            else:
                residual.append(lit)
        if not hit:
            out.append(tuple(residual))
    return canonical(out, met)


def simplify_units(f: Formula, met: Counter) -> Tuple[Formula, Assignment, bool]:
    f = canonical(f, met)
    forced: Assignment = {}
    while True:
        if () in f:
            return ((),), forced, False
        units = [c[0] for c in f if len(c) == 1]
        if not units:
            return f, forced, True
        step: Assignment = {}
        for lit in units:
            v, value = abs(lit), lit > 0
            if v in forced and forced[v] != value:
                return ((),), forced, False
            if v in step and step[v] != value:
                return ((),), forced, False
            step[v] = value
        fresh = {v: b for v, b in step.items() if v not in forced}
        if not fresh:
            return f, forced, True
        forced.update(fresh)
        met["unit_assignments"] += len(fresh)
        f = restrict_formula(f, fresh, met)


def component_formulas(f: Formula, met: Counter) -> List[Formula]:
    vs = set(variables(f))
    if not vs:
        return [f]
    adj = {v: set() for v in vs}
    for c in f:
        met["construction_clause_reads"] += 1
        cv = [abs(x) for x in c]
        met["construction_literal_reads"] += len(c)
        for v in cv[1:]:
            adj[cv[0]].add(v)
            adj[v].add(cv[0])
    groups: List[set[int]] = []
    while vs:
        root = min(vs)
        q = [root]
        group: set[int] = set()
        while q:
            v = q.pop()
            if v in group:
                continue
            group.add(v)
            vs.discard(v)
            q.extend(adj[v] - group)
        groups.append(group)
    if len(groups) == 1:
        return [f]
    out = []
    for group in groups:
        clauses = []
        for c in f:
            met["construction_clause_reads"] += 1
            met["construction_literal_reads"] += len(c)
            if any(abs(x) in group for x in c):
                clauses.append(c)
        out.append(tuple(clauses))
    met["component_splits"] += 1
    met["components_generated"] += len(out)
    return out


def horn_solve(f: Formula, met: Counter) -> Tuple[bool, Assignment]:
    true: set[int] = set()
    rules: List[Tuple[Tuple[int, ...], Optional[int]]] = []
    all_vars = variables(f)
    for c in f:
        pos = [x for x in c if x > 0]
        if len(pos) > 1:
            raise ValueError("not Horn")
        body = tuple(-x for x in c if x < 0)
        rules.append((body, pos[0] if pos else None))
    changed = True
    while changed:
        changed = False
        for body, head in rules:
            met["base_rule_checks"] += 1
            if all(v in true for v in body):
                if head is None:
                    return False, {v: v in true for v in all_vars}
                if head not in true:
                    true.add(head)
                    changed = True
    a = {v: v in true for v in all_vars}
    assert satisfies(f, a)
    return True, a


def two_sat_solve(f: Formula, met: Counter) -> Tuple[bool, Assignment]:
    vs = variables(f)
    index = {v: i for i, v in enumerate(vs)}
    nn = 2 * len(vs)
    g = [[] for _ in range(nn)]
    rg = [[] for _ in range(nn)]

    def node(lit: int) -> int:
        return 2 * index[abs(lit)] + (0 if lit > 0 else 1)

    def neg(k: int) -> int:
        return k ^ 1

    for c in f:
        if len(c) == 0:
            return False, {}
        if len(c) == 1:
            pairs = [(-c[0], c[0])]
        elif len(c) == 2:
            a, b = c
            pairs = [(-a, b), (-b, a)]
        else:
            raise ValueError("not 2-CNF")
        for a, b in pairs:
            u, v = node(a), node(b)
            g[u].append(v)
            rg[v].append(u)
            met["base_graph_edges"] += 1

    seen = [False] * nn
    order: List[int] = []
    sys.setrecursionlimit(max(1000, 8 * nn + 100))

    def dfs1(v: int) -> None:
        seen[v] = True
        for w in g[v]:
            met["base_graph_steps"] += 1
            if not seen[w]:
                dfs1(w)
        order.append(v)

    for v in range(nn):
        if not seen[v]:
            dfs1(v)
    comp = [-1] * nn

    def dfs2(v: int, k: int) -> None:
        comp[v] = k
        for w in rg[v]:
            met["base_graph_steps"] += 1
            if comp[w] < 0:
                dfs2(w, k)

    k = 0
    for v in reversed(order):
        if comp[v] < 0:
            dfs2(v, k)
            k += 1
    for v in vs:
        if comp[node(v)] == comp[node(-v)]:
            return False, {}
    a = {v: comp[node(v)] > comp[node(-v)] for v in vs}
    if not satisfies(f, a):
        a = {v: not b for v, b in a.items()}
    assert satisfies(f, a)
    return True, a


def frontier_solve(f: Formula, cap: int, met: Counter) -> Tuple[bool, Optional[bool], Assignment]:
    """Return (recognized, SAT, witness) for the supplied clause order."""
    vs = variables(f)
    last = {v: -1 for v in vs}
    for i, c in enumerate(f):
        for lit in c:
            last[abs(lit)] = i
            met["frontier_source_reads"] += 1
    boundary: List[int] = []
    table: Dict[int, int] = {0: 0}  # boundary assignment -> full true-variable mask
    bitpos = {v: i for i, v in enumerate(vs)}
    for i, c in enumerate(f):
        u = list(boundary)
        for lit in c:
            if abs(lit) not in u:
                u.append(abs(lit))
        after = [v for v in u if last[v] > i]
        if len(after) > cap:
            met["frontier_cap_exits"] += 1
            return False, None, {}
        bpos = {v: j for j, v in enumerate(boundary)}
        upos = {v: j for j, v in enumerate(u)}
        apos = {v: j for j, v in enumerate(after)}
        out: Dict[int, int] = {}
        for x in range(1 << len(u)):
            met["frontier_transitions"] += 1
            old = sum(((x >> upos[v]) & 1) << bpos[v] for v in boundary)
            if old not in table:
                continue
            if not any(bool((x >> upos[abs(lit)]) & 1) == (lit > 0) for lit in c):
                continue
            new = sum(((x >> upos[v]) & 1) << apos[v] for v in after)
            full = table[old]
            for v in u:
                if (x >> upos[v]) & 1:
                    full |= 1 << bitpos[v]
                else:
                    full &= ~(1 << bitpos[v])
            out.setdefault(new, full)
        table = out
        boundary = after
        met["frontier_max_width"] = max(met["frontier_max_width"], len(boundary))
        met["frontier_max_table_records"] = max(met["frontier_max_table_records"], len(table))
        if not table:
            return True, False, {}
    if not table:
        return True, False, {}
    full = next(iter(table.values()))
    witness = {v: bool((full >> bitpos[v]) & 1) for v in vs}
    assert satisfies(f, witness)
    return True, True, witness


def base_solve(f: Formula, met: Counter, frontier_cap: int = 4) -> Tuple[bool, Optional[bool], Assignment, str]:
    met["base_recognition_scans"] += sum(len(c) for c in f)
    if all(sum(lit > 0 for lit in c) <= 1 for c in f):
        sat, w = horn_solve(f, met)
        return True, sat, w, "Horn"
    if all(len(c) <= 2 for c in f):
        sat, w = two_sat_solve(f, met)
        return True, sat, w, "2CNF"
    recognized, sat, w = frontier_solve(f, frontier_cap, met)
    if recognized:
        return True, sat, w, "frontier"
    return False, None, {}, "none"


def merge_assignments(*parts: Assignment) -> Assignment:
    out: Assignment = {}
    for part in parts:
        for v, b in part.items():
            if v in out and out[v] != b:
                raise AssertionError((v, out[v], b))
            out[v] = b
    return out


@dataclass
class Node:
    kind: str
    formula: Formula = ()
    lift: Assignment = field(default_factory=dict)
    value: Optional[bool] = None
    witness: Assignment = field(default_factory=dict)
    children: List["Node"] = field(default_factory=list)
    edge_assignments: List[Assignment] = field(default_factory=list)
    base_kind: str = ""


class Overflow(Exception):
    pass


class Builder:
    def __init__(self, source: Formula, strategy: str, node_cap: int = 4096) -> None:
        self.source = canonical(source)
        self.strategy = strategy
        self.M = encoding_bits(self.source)
        self.target = max(2, math.floor(self.M ** (2 / 3)))
        self.q_budget = max(1, math.floor(self.M ** (1 / 3)))
        self.node_cap = node_cap
        self.nodes: List[Node] = []
        self.met: Counter = Counter()
        self.active_bits = 0
        self.stored_bits = 0
        self.complete = True

    def charge_node(self, node: Node) -> None:
        self.nodes.append(node)
        self.stored_bits += encoding_bits(node.formula)
        descriptor = 1 + len(node.lift) * max(2, max(variables(self.source), default=1).bit_length() + 1)
        self.met["peak_logical_workspace_bits"] = max(
            self.met["peak_logical_workspace_bits"], self.stored_bits + self.active_bits + descriptor
        )
        if len(self.nodes) > self.node_cap:
            raise Overflow

    def clause_terms(self, clause: Clause) -> List[Assignment]:
        terms: List[Assignment] = []
        prefix: Assignment = {}
        for lit in clause:
            term = dict(prefix)
            term[abs(lit)] = lit > 0
            terms.append(term)
            prefix[abs(lit)] = lit < 0
        return terms

    def branch_candidates(self, f: Formula, mode: str) -> Tuple[List[Assignment], str]:
        occ = Counter(abs(x) for c in f for x in c)
        if mode == "shannon":
            v = min(occ, key=lambda x: (-occ[x], x))
            return [{v: False}, {v: True}], f"x{v}"
        clauses = list(f)
        if mode == "short":
            c = min(clauses, key=lambda z: (len(z), -sum(occ[abs(x)] for x in z), z))
            return self.clause_terms(c), repr(c)
        if mode == "hub":
            c = min(clauses, key=lambda z: (-sum(occ[abs(x)] for x in z) / max(1, len(z)), len(z), z))
            return self.clause_terms(c), repr(c)
        if mode in ("minimax", "hybrid"):
            ranked = sorted(clauses, key=lambda z: (-sum(occ[abs(x)] for x in z), len(z), z))[:12]
            best = None
            for c in ranked:
                sizes = []
                for term in self.clause_terms(c):
                    child = restrict_formula(f, term, self.met)
                    sizes.append(encoding_bits(child))
                score = (max(sizes, default=0), sum(sizes), len(c), c)
                if best is None or score < best[0]:
                    best = (score, c)
            assert best is not None
            clause = best[1]
            clause_terms = self.clause_terms(clause)
            if mode == "hybrid":
                v = min(occ, key=lambda x: (-occ[x], x))
                shannon_terms = [{v: False}, {v: True}]
                shannon_sizes = [encoding_bits(restrict_formula(f, t, self.met)) for t in shannon_terms]
                clause_sizes = [encoding_bits(restrict_formula(f, t, self.met)) for t in clause_terms]
                if (max(shannon_sizes), sum(shannon_sizes), 2) < (max(clause_sizes), sum(clause_sizes), len(clause_terms)):
                    return shannon_terms, f"x{v}"
            return clause_terms, repr(clause)
        raise ValueError(mode)

    def try_backdoor_value(self, f: Formula) -> Optional[Tuple[bool, Assignment, str]]:
        if "backdoor" not in self.strategy and "dnf" not in self.strategy:
            return None
        vs = variables(f)
        # Fixed-size strong backdoors.  Empty set is handled by base_solve.
        if "backdoor" in self.strategy:
            for k in (1, 2):
                for chosen in it.combinations(vs, k):
                    self.met["backdoor_candidates"] += 1
                    outcomes = []
                    all_base = True
                    for bits in it.product((False, True), repeat=k):
                        a = dict(zip(chosen, bits))
                        child = restrict_formula(f, a, self.met)
                        child, forced, consistent = simplify_units(child, self.met)
                        if not consistent:
                            outcomes.append((False, {}, a, forced, "conflict"))
                            continue
                        known, sat, w, kind = base_solve(child, self.met)
                        if not known:
                            all_base = False
                            break
                        outcomes.append((bool(sat), w, a, forced, kind))
                    if all_base:
                        self.met["strong_backdoors_found"] += 1
                        for sat, w, a, forced, _kind in outcomes:
                            if sat:
                                return True, merge_assignments(a, forced, w), f"strong-{k}"
                        return False, {}, f"strong-{k}"
        # Clause-induced disjoint DNF.  This can be smaller than a strong
        # backdoor enumeration and is exact because every model satisfies c.
        for c in sorted(f, key=lambda z: (len(z), z))[:16]:
            outcomes = []
            all_base = True
            self.met["clause_dnf_candidates"] += 1
            for term in self.clause_terms(c):
                child = restrict_formula(f, term, self.met)
                child, forced, consistent = simplify_units(child, self.met)
                if not consistent:
                    outcomes.append((False, {}, term, forced, "conflict"))
                    continue
                known, sat, w, kind = base_solve(child, self.met)
                if not known:
                    all_base = False
                    break
                outcomes.append((bool(sat), w, term, forced, kind))
            if all_base:
                self.met["clause_backdoor_dnfs_found"] += 1
                for sat, w, term, forced, _kind in outcomes:
                    if sat:
                        return True, merge_assignments(term, forced, w), "clause-DNF"
                return False, {}, "clause-DNF"
        if "dnf" in self.strategy and len(vs) >= 3:
            # Fixed four-variable, six-term DNF acquisition.  Tautology is
            # checked exactly over the 16 assignments to the chosen variables;
            # every retained term must put the residual in a directly solved
            # base class.  This is a bounded partial rule, not a scalable DNF
            # detector.
            occ = Counter(abs(x) for c in f for x in c)
            chosen = tuple(sorted(vs, key=lambda v: (-occ[v], v))[:4])
            covered_occurrences = sum(occ[v] for v in chosen)
            if covered_occurrences * 3 >= sum(occ.values()):
                valid = []
                universe_assignments = list(it.product((False, True), repeat=len(chosen)))
                for pattern in it.product((-1, 0, 1), repeat=len(chosen)):
                    if all(x == -1 for x in pattern):
                        continue
                    term = {v: bool(x) for v, x in zip(chosen, pattern) if x != -1}
                    child = restrict_formula(f, term, self.met)
                    child, forced, consistent = simplify_units(child, self.met)
                    if not consistent:
                        sat, witness, kind, known = False, {}, "conflict", True
                    else:
                        known, sat0, witness, kind = base_solve(child, self.met)
                        sat = bool(sat0)
                    self.met["bounded_dnf_terms_tested"] += 1
                    if not known:
                        continue
                    mask = 0
                    for j, bits in enumerate(universe_assignments):
                        full = dict(zip(chosen, bits))
                        if all(full[v] == b for v, b in term.items()):
                            mask |= 1 << j
                    valid.append((mask, term, sat, witness, forced, kind))
                full_mask = (1 << len(universe_assignments)) - 1
                paths: Dict[int, Tuple[int, ...]] = {0: ()}
                frontier = deque([0])
                expansions = 0
                found: Optional[Tuple[int, ...]] = None
                while frontier and expansions < 20000:
                    mask = frontier.popleft()
                    path = paths[mask]
                    if len(path) >= 6:
                        continue
                    for j, item in enumerate(valid):
                        new = mask | item[0]
                        expansions += 1
                        if new in paths:
                            continue
                        paths[new] = path + (j,)
                        if new == full_mask:
                            found = paths[new]
                            frontier.clear()
                            break
                        frontier.append(new)
                self.met["bounded_dnf_cover_expansions"] += expansions
                if found is not None:
                    self.met["bounded_backdoor_dnfs_found"] += 1
                    self.met["bounded_backdoor_dnf_terms"] += len(found)
                    for j in found:
                        _mask, term, sat, witness, forced, _kind = valid[j]
                        if sat:
                            return True, merge_assignments(term, forced, witness), "bounded-DNF"
                    return False, {}, "bounded-DNF"
        return None

    def dominance_prune(self, items: List[Tuple[Formula, Assignment]]) -> List[Tuple[Formula, Assignment]]:
        # Exact equality first.  Keep the first route because it carries a
        # valid source witness lift for the shared residual.
        unique: List[Tuple[Formula, Assignment]] = []
        seen = set()
        for f, a in items:
            if f in seen:
                self.met["equal_residuals_deleted"] += 1
                continue
            seen.add(f)
            unique.append((f, a))
        drop = set()
        clause_sets = [set(f) for f, _ in unique]
        live_sets = [set(variables(f)) for f, _ in unique]
        for i in range(len(unique)):
            for j in range(len(unique)):
                if i == j or i in drop:
                    continue
                self.met["dominance_comparisons"] += 1
                # If Fi contains every clause of Fj, then Fi => Fj and Fi may
                # be deleted from an OR frontier.  Same-live-variable guard is
                # retained exactly as in CLAUSE-DOM-SELECT1.
                if live_sets[i] == live_sets[j] and clause_sets[i] > clause_sets[j]:
                    drop.add(i)
                    self.met["dominance_residuals_deleted"] += 1
        return [x for i, x in enumerate(unique) if i not in drop]

    def build(self, raw: Formula, depth: int = 0) -> Node:
        self.met["max_depth"] = max(self.met["max_depth"], depth)
        self.active_bits += encoding_bits(raw)
        self.met["peak_logical_workspace_bits"] = max(
            self.met["peak_logical_workspace_bits"], self.stored_bits + self.active_bits
        )
        f, forced, consistent = simplify_units(raw, self.met)
        if not consistent:
            node = Node("CONST", formula=f, lift=forced, value=False)
            self.charge_node(node)
            self.active_bits -= encoding_bits(raw)
            return node
        if not f:
            node = Node("CONST", formula=f, lift=forced, value=True, witness={})
            self.charge_node(node)
            self.active_bits -= encoding_bits(raw)
            return node
        # The inner contract asks for small recursive children, not for those
        # children to be solved during acquisition.  Emit a leaf as soon as it
        # crosses the target.  This prevents a later easy-class recognition
        # from making fanout look vacuously zero after the builder already did
        # all recursive work.
        if encoding_bits(f) <= self.target:
            node = Node("LEAF", formula=f, lift=forced)
            self.charge_node(node)
            self.active_bits -= encoding_bits(raw)
            return node
        # The DNF diagnostic deliberately tries its certified cover before a
        # bounded-frontier shortcut so the mechanism receives a positive
        # control.  Ordinary strategies use the cheaper direct recognizer first.
        bd = self.try_backdoor_value(f) if "dnf" in self.strategy else None
        if bd is not None:
            value, witness, kind = bd
            node = Node("VALUE", formula=f, lift=forced, value=value, witness=witness, base_kind=kind)
            self.charge_node(node)
            self.active_bits -= encoding_bits(raw)
            return node
        known, sat, witness, kind = base_solve(f, self.met)
        if known:
            self.met[f"direct_{kind}_values"] += 1
            node = Node("VALUE", formula=f, lift=forced, value=sat, witness=witness, base_kind=kind)
            self.charge_node(node)
            self.active_bits -= encoding_bits(raw)
            return node
        bd = self.try_backdoor_value(f) if "dnf" not in self.strategy else None
        if bd is not None:
            value, witness, kind = bd
            node = Node("VALUE", formula=f, lift=forced, value=value, witness=witness, base_kind=kind)
            self.charge_node(node)
            self.active_bits -= encoding_bits(raw)
            return node
        comps = component_formulas(f, self.met)
        if len(comps) > 1:
            node = Node("AND", formula=f, lift=forced)
            self.charge_node(node)
            node.children = [self.build(c, depth + 1) for c in comps]
            self.active_bits -= encoding_bits(raw)
            return node
        mode = self.strategy.split("+")[0]
        terms, _label = self.branch_candidates(f, mode)
        items = [(restrict_formula(f, a, self.met), a) for a in terms]
        items = self.dominance_prune(items)
        if not items:
            raise AssertionError("exact cover lost every branch")
        node = Node("OR", formula=f, lift=forced)
        self.charge_node(node)
        for child, edge in items:
            node.edge_assignments.append(edge)
            node.children.append(self.build(child, depth + 1))
        self.active_bits -= encoding_bits(raw)
        return node

    def run(self) -> Tuple[Optional[Node], Dict[str, object]]:
        start = time.perf_counter()
        try:
            root = self.build(self.source)
        except Overflow:
            root = None
            self.complete = False
            self.met["node_cap_exits"] += 1
        leaves = [n for n in self.nodes if n.kind == "LEAF"]
        self.met["construction_work_proxy"] = (
            self.met["construction_literal_reads"]
            + self.met["construction_clause_reads"]
            + self.met["subsumption_comparisons"]
            + self.met["dominance_comparisons"]
            + self.met["base_rule_checks"]
            + self.met["base_graph_steps"]
            + self.met["frontier_transitions"]
        )
        work = max(1, int(self.met["construction_work_proxy"]))
        peak = max(1, int(self.met["peak_logical_workspace_bits"]))
        work_exp = math.log(work) / math.log(max(2, self.M))
        space_exp = math.log(peak) / math.log(max(2, self.M))
        shape_success = self.complete and len(leaves) <= self.q_budget
        summary: Dict[str, object] = dict(
            strategy=self.strategy,
            complete=self.complete,
            input_bits=self.M,
            target_child_bits=self.target,
            q_budget=self.q_budget,
            q=len(leaves),
            max_child_bits=max((encoding_bits(n.formula) for n in leaves), default=0),
            plan_nodes=len(self.nodes),
            stored_formula_bits=self.stored_bits,
            target_success=shape_success,
            empirical_work_exponent=work_exp,
            empirical_workspace_exponent=space_exp,
            unit_coefficient_M43_work_pass=shape_success and work <= self.M ** (4 / 3),
            unit_coefficient_M23_space_pass=shape_success and peak <= self.M ** (2 / 3),
            build_seconds=time.perf_counter() - start,
            metrics=dict(self.met),
        )
        return root, summary


def reference_witness(f: Formula, met: Counter) -> Tuple[bool, Assignment]:
    """Independent validation solver.  Its cost is excluded from construction."""
    f = canonical(f)
    f, forced, consistent = simplify_units(f, met)
    if not consistent:
        return False, {}
    if not f:
        return True, forced
    v = min(variables(f), key=lambda x: (-sum(x == abs(l) for c in f for l in c), x))
    for b in (False, True):
        child = restrict_formula(f, {v: b}, met)
        sat, w = reference_witness(child, met)
        if sat:
            return True, merge_assignments(forced, {v: b}, w)
    return False, {}


def evaluate(node: Node, replay: Counter) -> Tuple[bool, Assignment]:
    replay["nodes_replayed"] += 1
    replay["formula_bits_replayed"] += encoding_bits(node.formula)
    replay["literal_reads"] += sum(map(len, node.formula))
    if node.kind == "CONST":
        return bool(node.value), dict(node.lift)
    if node.kind == "VALUE":
        if not node.value:
            return False, {}
        return True, merge_assignments(node.lift, node.witness)
    if node.kind == "LEAF":
        oracle_met = Counter()
        sat, w = reference_witness(node.formula, oracle_met)
        replay["leaf_oracle_calls"] += 1
        replay["validation_solver_work"] += sum(oracle_met.values())
        if not sat:
            return False, {}
        return True, merge_assignments(node.lift, w)
    if node.kind == "AND":
        witness = dict(node.lift)
        for child in node.children:
            sat, w = evaluate(child, replay)
            if not sat:
                return False, {}
            witness = merge_assignments(witness, w)
        return True, witness
    if node.kind == "OR":
        for edge, child in zip(node.edge_assignments, node.children):
            replay["edge_assignments_replayed"] += len(edge)
            sat, w = evaluate(child, replay)
            if sat:
                return True, merge_assignments(node.lift, edge, w)
        return False, {}
    raise ValueError(node.kind)


def verify_plan(node: Node, source: Formula, answer: bool, witness: Assignment, replay: Counter) -> None:
    """Replay every edge syntactically, independent of the chosen SAT route."""
    todo = [node]
    while todo:
        current = todo.pop()
        replay["verification_nodes"] += 1
        replay["verification_literal_reads"] += sum(map(len, current.formula))
        if current.kind == "OR":
            assert len(current.children) == len(current.edge_assignments)
            for edge, child in zip(current.edge_assignments, current.children):
                replay["parent_reread_passes"] += 1
                replay["parent_reread_literal_reads"] += sum(map(len, current.formula))
                regenerated = restrict_formula(current.formula, edge, replay)
                simplified, _forced, _consistent = simplify_units(regenerated, replay)
                # The recursive child may have performed the simplification;
                # compare its stored formula after its own lift removal.
                assert simplified == child.formula
            todo.extend(current.children)
        elif current.kind == "AND":
            replay["parent_reread_passes"] += len(current.children)
            replay["parent_reread_literal_reads"] += len(current.children) * sum(map(len, current.formula))
            expected = component_formulas(current.formula, replay)
            assert [c.formula for c in current.children] == expected
            todo.extend(current.children)
        elif current.kind == "VALUE" and current.value:
            assert satisfies(current.formula, current.witness)
    if answer:
        full = {v: witness.get(v, False) for v in variables(source)}
        assert satisfies(source, full)


def php(pigeons: int, holes: int) -> Formula:
    var = lambda p, h: p * holes + h + 1
    clauses: List[Clause] = [tuple(var(p, h) for h in range(holes)) for p in range(pigeons)]
    for h in range(holes):
        for p, q in it.combinations(range(pigeons), 2):
            clauses.append((-var(p, h), -var(q, h)))
    return canonical(clauses)


def xor3(a: int, b: int, c: int, parity: int) -> List[Clause]:
    out = []
    for x, y, z in it.product((0, 1), repeat=3):
        if (x ^ y ^ z) != parity:
            out.append((a if not x else -a, b if not y else -b, c if not z else -c))
    return out


def xor_cycle(n: int, inconsistent: bool = False) -> Formula:
    clauses: List[Clause] = []
    for i in range(n):
        a, b, c = i + 1, (i + 1) % n + 1, (i + 3) % n + 1
        clauses.extend(xor3(a, b, c, int(inconsistent and i == n - 1)))
    return canonical(clauses)


def random_3cnf(n: int, m: int, seed: int, planted: bool = False) -> Formula:
    rng = random.Random(seed)
    out = []
    for _ in range(m):
        vs = rng.sample(range(1, n + 1), 3)
        signs = [rng.choice((-1, 1)) for _ in range(3)]
        if planted and all(s < 0 for s in signs):
            signs[rng.randrange(3)] = 1
        out.append(tuple(v * s for v, s in zip(vs, signs)))
    return canonical(out)


def hub_formula(n: int, seed: int) -> Formula:
    rng = random.Random(seed)
    out = []
    for _ in range(5 * n):
        a, b = rng.sample(range(2, n + 1), 2)
        # All-true planted; x1 appears in every clause.
        signs = [1, rng.choice((-1, 1)), rng.choice((-1, 1))]
        if signs[1] < 0 and signs[2] < 0:
            signs[rng.choice((1, 2))] = 1
        out.append((signs[0], signs[1] * a, signs[2] * b))
    return canonical(out)


def disjoint_blocks(blocks: int, seed: int) -> Formula:
    rng = random.Random(seed)
    out = []
    for j in range(blocks):
        vs = list(range(4 * j + 1, 4 * j + 5))
        for _ in range(8):
            chosen = rng.sample(vs, 3)
            signs = [rng.choice((-1, 1)) for _ in range(3)]
            if all(s < 0 for s in signs):
                signs[0] = 1
            out.append(tuple(v * s for v, s in zip(chosen, signs)))
    return canonical(out)


def dominance_control() -> Formula:
    # Restricting the first clause by its first-satisfied terms produces
    # deliberately comparable residual clause sets.
    rng = random.Random(17171)
    common: List[Clause] = []
    for _ in range(42):
        chosen = rng.sample(range(3, 15), 3)
        signs = [rng.choice((-1, 1)) for _ in range(3)]
        if all(s < 0 for s in signs):
            signs[0] = 1
        c = tuple(v * s for v, s in zip(chosen, signs))
        if set(c) != {3, 4, 5}:
            common.append(c)
    # For the disjoint cover of (x1 or x2), the x1=1 route retains (x3,x4,x5)
    # while x1=0,x2=1 satisfies the long clause.  The remaining common formula
    # is identical and keeps the same live-variable set, so the first residual
    # is strictly clause-dominated by the second.
    return canonical([(1, 2), (-1, 3, 4, 5)] + common)


def frontier_chain(n: int) -> Formula:
    return canonical((i, i + 1, i + 2) for i in range(1, n - 1))


def backdoor_dnf_family(s: int = 3) -> Formula:
    # Ordyniak--Schidler--Szeider Horn-backdoor-DNF family.  Use p=1,
    # a_i=2..s+1, and q_j thereafter, with r=2^s-s.
    p = 1
    aa = list(range(2, s + 2))
    r = 2 ** s - s
    qq = list(range(s + 2, s + 2 + r))
    rows: List[Clause] = [(a, p) for a in aa]
    rows.extend(tuple(aa + [q, -p]) for q in qq)
    return canonical(rows)


def cases() -> List[Tuple[str, Formula, Optional[bool]]]:
    out: List[Tuple[str, Formula, Optional[bool]]] = []
    # Exhaustive proper 3-variable clause subsets are a small exact regression.
    clauses = list(it.product(*[(i, -i) for i in range(1, 4)]))
    for mask in range(256):
        out.append((f"exhaustive3_{mask}", canonical(c for i, c in enumerate(clauses) if (mask >> i) & 1), None))
    for n in (8, 10, 12):
        for seed in range(4):
            out.append((f"random3_{n}_{seed}", random_3cnf(n, round(4.3 * n), 9000 + 31 * n + seed), None))
    for n in (12, 16, 20):
        out.append((f"planted3_{n}", random_3cnf(n, 5 * n, 12000 + n, planted=True), True))
        out.append((f"hub_{n}", hub_formula(n, 13000 + n), True))
    out.extend([
        ("PHP_4_3", php(4, 3), False),
        ("PHP_5_4", php(5, 4), False),
        ("XOR_cycle_9_SAT", xor_cycle(9, False), True),
        ("XOR_cycle_9_hostile", xor_cycle(9, True), None),
        ("disjoint_3x4", disjoint_blocks(3, 14001), True),
        ("disjoint_5x4", disjoint_blocks(5, 14002), True),
        ("Horn_chain", canonical([(-i, i + 1) for i in range(1, 39)] + [(1,), (-39, 40)]), True),
        ("twoCNF_unsat", canonical([(1, 2), (1, -2), (-1, 2), (-1, -2)]), False),
        ("dominance_control", dominance_control(), True),
        ("frontier_chain_40", frontier_chain(40), True),
        ("backdoor_DNF_s3", backdoor_dnf_family(3), True),
        ("stress_random3_24", random_3cnf(24, 104, 15024), None),
        ("stress_random3_28", random_3cnf(28, 121, 15028), None),
        ("stress_planted3_32", random_3cnf(32, 160, 15032, planted=True), True),
        ("stress_PHP_7_6", php(7, 6), False),
        ("stress_PHP_8_7", php(8, 7), False),
    ])
    return out


def small_truth(f: Formula) -> Tuple[bool, Assignment]:
    vs = variables(f)
    for bits in it.product((False, True), repeat=len(vs)):
        a = dict(zip(vs, bits))
        if satisfies(f, a):
            return True, a
    return False, {}


def main() -> None:
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(25)
    started = time.perf_counter()
    rows = []
    exact_checks = witness_checks = plan_replay_checks = 0
    strategies = ("short", "short+dnf", "hybrid+backdoor", "shannon+backdoor")
    all_cases = cases()
    for index, (name, source, expected) in enumerate(all_cases):
        # Exhaustive n=3 regression needs one strategy; the heterogeneous suite
        # exercises the whole portfolio.
        active = ("hybrid+backdoor",) if name.startswith("exhaustive3_") else strategies
        if name.startswith("stress_"):
            active = ("short",)
        if expected is None:
            if len(variables(source)) <= 14:
                expected, _ = small_truth(source)
            else:
                verify_met = Counter()
                expected, _ = reference_witness(source, verify_met)
        attempts = []
        for strategy in active:
            builder = Builder(source, strategy)
            root, summary = builder.run()
            if root is not None:
                replay = Counter()
                answer, witness = evaluate(root, replay)
                assert answer == expected, (name, strategy, answer, expected)
                exact_checks += 1
                verify_plan(root, builder.source, answer, witness, replay)
                plan_replay_checks += 1
                if answer:
                    witness_checks += 1
                summary["answer"] = answer
                summary["replay"] = dict(replay)
            attempts.append(summary)
        winners = [a for a in attempts if a["target_success"]]
        # A fixed sequential partial portfolio may stop at the first certified
        # success.  Failed attempt work is charged and discarded.
        selected = winners[0]["strategy"] if winners else None
        prefix = attempts[: attempts.index(winners[0]) + 1] if winners else attempts
        portfolio = dict(
            success=bool(winners),
            selected=selected,
            charged_work=sum(int(a["metrics"].get("construction_work_proxy", 0)) for a in prefix),
            peak_logical_workspace_bits=max((int(a["metrics"].get("peak_logical_workspace_bits", 0)) for a in prefix), default=0),
            attempted=[a["strategy"] for a in prefix],
            minimum_empirical_work_exponent=min(float(a["empirical_work_exponent"]) for a in attempts),
            minimum_empirical_workspace_exponent=min(float(a["empirical_workspace_exponent"]) for a in attempts),
            any_unit_M43_work_pass=any(bool(a["unit_coefficient_M43_work_pass"]) for a in attempts),
            any_unit_M23_space_pass=any(bool(a["unit_coefficient_M23_space_pass"]) for a in attempts),
        )
        rows.append(dict(
            family=name,
            variables=len(variables(source)),
            clauses=len(source),
            literals=sum(map(len, source)),
            input_bits=encoding_bits(source),
            expected=expected,
            attempts=attempts,
            portfolio=portfolio,
        ))
    nontrivial = [r for r in rows if not r["family"].startswith("exhaustive3_")]
    # PRF3-0079 all-block correction.  Without an independently proved shared
    # acquisition theorem, normal all-block fanout is a=1-lambda and total
    # exponent is a+beta+lambda*k = 1+beta+lambda for k=2.
    route_b_grid = []
    for lam in (1 / 12, 1 / 6, 1 / 4, 1 / 3, 1 / 2):
        for beta in (0.0, 1 / 12, 1 / 6):
            a = 1 - lam
            exponent = a + beta + 2 * lam
            route_b_grid.append(dict(lambda_=lam, beta=beta, a=a, total_exponent=exponent,
                                     below_four_thirds=exponent < 4 / 3))
    assert not next(x for x in route_b_grid if x["lambda_"] == 0.5 and x["beta"] == 0.0)["below_four_thirds"]
    assert next(x for x in route_b_grid if x["lambda_"] == 1 / 12 and x["beta"] == 1 / 6)["below_four_thirds"]
    result = dict(
        status="COMPUTATIONAL",
        run_id="FINAL-LINK-HYBRID1",
        seed_manifest=[9000, 12000, 13000, 14001, 14002],
        cases=len(rows),
        heterogeneous_cases=len(nontrivial),
        exact_answer_checks=exact_checks,
        lifted_witness_checks=witness_checks,
        full_plan_replay_checks=plan_replay_checks,
        errors=0,
        seconds=time.perf_counter() - started,
        strategies=list(strategies),
        target_portfolio_successes=sum(r["portfolio"]["success"] for r in nontrivial),
        target_portfolio_failures=sum(not r["portfolio"]["success"] for r in nontrivial),
        unit_M43_work_passes=sum(r["portfolio"]["any_unit_M43_work_pass"] for r in nontrivial),
        unit_M23_space_passes=sum(r["portfolio"]["any_unit_M23_space_pass"] for r in nontrivial),
        mechanism_controls=dict(
            dominance_deletions=sum(int(a["metrics"].get("dominance_residuals_deleted", 0)) for r in rows for a in r["attempts"]),
            component_splits=sum(int(a["metrics"].get("component_splits", 0)) for r in rows for a in r["attempts"]),
            direct_zero_child_values=sum(sum(int(v) for k, v in a["metrics"].items() if k.startswith("direct_") and k.endswith("_values")) for r in rows for a in r["attempts"]),
            strong_backdoors=sum(int(a["metrics"].get("strong_backdoors_found", 0)) for r in rows for a in r["attempts"]),
            clause_backdoor_dnfs=sum(int(a["metrics"].get("clause_backdoor_dnfs_found", 0)) for r in rows for a in r["attempts"]),
            bounded_backdoor_dnfs=sum(int(a["metrics"].get("bounded_backdoor_dnfs_found", 0)) for r in rows for a in r["attempts"]),
            frontier_cap_exits=sum(int(a["metrics"].get("frontier_cap_exits", 0)) for r in rows for a in r["attempts"]),
        ),
        route_B_PRF3_0079_grid=route_b_grid,
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        rows=rows,
        limitations=[
            "A success is an exact partial-wrapper certificate for that input, not an all-input asymptotic theorem.",
            "Explicit Python formulas overestimate some logical storage and underestimate interpreter overhead; the logical ledger is reported separately.",
            "Leaf reference solves occur only in validation and are excluded from construction work.",
            "The fixed backdoor search is polynomial only because its size and frontier cap are constants.",
            "Clause-first covers, components, dominance, and base solvers do not prove favorable coverage on unrestricted SAT.",
        ],
    )
    Path(sys.argv[1]).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}, indent=2))
    for row in nontrivial:
        best = min(row["attempts"], key=lambda a: (not a["target_success"], a["q"], a["max_child_bits"]))
        print(row["family"], "portfolio", row["portfolio"]["success"], "best", best["strategy"], "q", best["q"], "max", best["max_child_bits"], "target", best["target_child_bits"])


if __name__ == "__main__":
    main()
