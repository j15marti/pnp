#!/usr/bin/env python3
"""FINAL-LINK2: one-scan residual-family compilation over a shared route trie.

The compiler receives an ordinary CNF and an exact disjunctive restriction
cover.  It scans the source once (twice when source-matched clauses must first
be selected), propagates each source clause symbolically through the route
trie, and stores every stable residual fragment at the highest trie node where
it applies.  A child is recovered from payloads on one root-to-leaf path.  No
child recovery rereads the source.

This tests a genuine shared BatchAcquire object, but does not claim that an
arbitrary SAT algorithm can consume the parent-aware representation at the
smaller-child complexity scale.  Standalone child emission, recovery work,
the shared object, and source-dependent verification are all charged.

Run under a hard 30-second cap.  The program installs a 25-second alarm:

    timeout 30s python3 final_link2_batch_acquire.py OUTPUT.json
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
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

import final_link_hybrid_builder as base

Clause = Tuple[int, ...]
Formula = Tuple[Clause, ...]
Assignment = Dict[int, bool]


def deadline(*_args: object) -> None:
    raise TimeoutError("25-second internal budget reached; split the batch")


def clean_clause(raw: Iterable[int]) -> Optional[Clause]:
    seen: Set[int] = set()
    for lit in raw:
        if -lit in seen:
            return None
        seen.add(lit)
    return tuple(sorted(seen, key=lambda x: (abs(x), x < 0)))


def raw_encoding_bits(f: Sequence[Clause]) -> int:
    largest = max((abs(x) for c in f for x in c), default=0)
    width = max(1, (largest + 1).bit_length())
    return width + sum(width + (width + 1) * len(c) for c in f)


def source_variables(f: Sequence[Clause]) -> Tuple[int, ...]:
    return tuple(sorted({abs(x) for c in f for x in c}))


def source_satisfied(f: Sequence[Clause], assignment: Assignment) -> bool:
    return all(any(assignment.get(abs(lit), False) == (lit > 0) for lit in c) for c in f)


@dataclass
class TrieNode:
    ident: int
    parent: Optional[int]
    edge: Assignment
    assignment: Assignment
    depth: int
    children: List[int] = field(default_factory=list)
    descendant_variables: Set[int] = field(default_factory=set)
    leaf_mask: int = 0
    leaf_index: Optional[int] = None
    payload: Set[int] = field(default_factory=set)


class RouteTrie:
    def __init__(self) -> None:
        self.nodes = [TrieNode(0, None, {}, {}, 0)]
        self.leaves: List[int] = []
        self.selected_clauses: List[Clause] = []
        self.metrics: Counter = Counter()

    def child(self, parent: int, edge: Assignment) -> int:
        p = self.nodes[parent]
        merged = dict(p.assignment)
        for v, value in edge.items():
            if v in merged and merged[v] != value:
                raise AssertionError("inconsistent route edge")
            merged[v] = value
        ident = len(self.nodes)
        self.nodes.append(TrieNode(ident, parent, dict(edge), merged, p.depth + 1))
        p.children.append(ident)
        self.metrics["route_edges"] += 1
        self.metrics["route_assignment_records"] += len(edge)
        return ident

    @staticmethod
    def residual_clause(clause: Clause, assignment: Assignment) -> Tuple[bool, Clause]:
        residual = []
        for lit in clause:
            v = abs(lit)
            if v in assignment:
                if assignment[v] == (lit > 0):
                    return True, ()
            else:
                residual.append(lit)
        return False, tuple(residual)

    @staticmethod
    def first_true_terms(clause: Clause) -> List[Assignment]:
        prefix: Assignment = {}
        terms = []
        for lit in clause:
            term = dict(prefix)
            term[abs(lit)] = lit > 0
            terms.append(term)
            prefix[abs(lit)] = lit < 0
        return terms

    def finalize(self, frontier: Sequence[int]) -> None:
        self.leaves = list(dict.fromkeys(frontier))
        for j, ident in enumerate(self.leaves):
            self.nodes[ident].leaf_index = j

        def post(v: int) -> Tuple[Set[int], int]:
            node = self.nodes[v]
            desc: Set[int] = set()
            mask = 0
            if node.leaf_index is not None:
                mask |= 1 << node.leaf_index
            for child_id in node.children:
                child = self.nodes[child_id]
                child_desc, child_mask = post(child_id)
                self.metrics["trie_finalize_set_work"] += len(child.edge) + len(child_desc) + 1
                desc.update(child.edge)
                desc.update(child_desc)
                mask |= child_mask
            node.descendant_variables = desc
            node.leaf_mask = mask
            return desc, mask

        post(0)
        full = (1 << len(self.leaves)) - 1
        assert self.nodes[0].leaf_mask == full
        # All route cubes must be pairwise disjoint.  The source-matched cover
        # only needs to cover source models, not all assignments.
        for left, right in it.combinations(self.leaves, 2):
            a = self.nodes[left].assignment
            b = self.nodes[right].assignment
            assert any(v in b and b[v] != value for v, value in a.items())


def choose_source_clauses(source: Sequence[Clause], depth: int, metrics: Counter) -> List[Clause]:
    candidates = []
    seen = set()
    for raw in source:
        metrics["cover_selection_source_literal_reads"] += len(raw)
        metrics["cover_selection_normalization_work_upper"] += len(raw) * (
            2 + max(1, math.ceil(math.log2(len(raw) + 1)))
        )
        c = clean_clause(raw)
        if c is None or not c or c in seen or len(c) > 8:
            continue
        metrics["cover_candidate_hash_literal_probes"] += len(c)
        seen.add(c)
        candidates.append(c)
        metrics["cover_candidate_clauses"] += 1
        metrics["cover_candidate_literals"] += len(c)
        metrics["cover_candidate_max_variable"] = max(
            metrics["cover_candidate_max_variable"], max(map(abs, c), default=0)
        )
    used: Set[int] = set()
    chosen: List[Clause] = []
    for _ in range(min(depth, len(candidates))):
        best: Optional[Clause] = None
        best_key: Optional[Tuple[object, ...]] = None
        for c in candidates:
            metrics["cover_greedy_candidate_tests"] += 1
            if c in chosen:
                continue
            metrics["cover_greedy_literal_probes"] += len(c)
            key: Tuple[object, ...] = (len({abs(x) for x in c} - used), -len(c), c)
            if best_key is None or key > best_key:
                best, best_key = c, key
        assert best is not None
        chosen.append(best)
        used.update(abs(x) for x in best)
    return chosen


def build_clause_trie(source: Sequence[Clause], depth: int) -> RouteTrie:
    trie = RouteTrie()
    selected = choose_source_clauses(source, depth, trie.metrics)
    trie.selected_clauses = selected
    frontier = [0]
    for clause in selected:
        next_frontier = []
        for ident in frontier:
            node = trie.nodes[ident]
            trie.metrics["cover_trie_residual_literal_probes_upper"] += len(clause)
            sat, residual = trie.residual_clause(clause, node.assignment)
            if sat:
                next_frontier.append(ident)
                continue
            if not residual:
                trie.metrics["infeasible_routes_pruned"] += 1
                continue
            trie.metrics["cover_trie_term_literal_probes"] += len(residual)
            for term in trie.first_true_terms(residual):
                next_frontier.append(trie.child(ident, term))
        frontier = next_frontier
    trie.finalize(frontier or [0])
    trie.metrics["selected_clause_count"] = len(selected)
    trie.metrics["trie_nodes"] = len(trie.nodes)
    trie.metrics["leaves"] = len(trie.leaves)
    return trie


def build_shannon_trie(selected_variables: Sequence[int]) -> RouteTrie:
    trie = RouteTrie()
    frontier = [0]
    for v in selected_variables:
        next_frontier = []
        for ident in frontier:
            next_frontier.append(trie.child(ident, {v: False}))
            next_frontier.append(trie.child(ident, {v: True}))
        frontier = next_frontier
    trie.finalize(frontier)
    trie.metrics["selected_clause_count"] = 0
    trie.metrics["trie_nodes"] = len(trie.nodes)
    trie.metrics["leaves"] = len(trie.leaves)
    return trie


class BatchAcquire:
    def __init__(self, source: Sequence[Clause], trie: RouteTrie) -> None:
        # The caller supplies an immutable tuple.  Retain a read-only reference
        # instead of silently making an uncharged literal-for-literal copy.
        self.source: Formula = source if isinstance(source, tuple) else tuple(source)
        self.trie = trie
        self.metrics: Counter = Counter(trie.metrics)
        self.fragments: List[Clause] = []
        self.fragment_ids: Dict[Clause, int] = {}
        self.entries: Set[Tuple[int, int]] = set()

    def intern(self, clause: Clause) -> int:
        if clause in self.fragment_ids:
            self.metrics["fragment_pool_hits"] += 1
            return self.fragment_ids[clause]
        ident = len(self.fragments)
        self.fragment_ids[clause] = ident
        self.fragments.append(clause)
        return ident

    def add_entry(self, node_id: int, residual: Clause) -> None:
        frag = self.intern(residual)
        item = (node_id, frag)
        if item in self.entries:
            self.metrics["duplicate_entries_eliminated"] += 1
            return
        self.entries.add(item)
        self.trie.nodes[node_id].payload.add(frag)
        self.metrics["payload_entries"] += 1

    def apply_edge(self, residual: Clause, edge: Assignment) -> Tuple[bool, Clause]:
        by_var = {abs(lit): lit for lit in residual}
        removed: Set[int] = set()
        for v, value in edge.items():
            self.metrics["delta_assignment_probes"] += 1
            lit = by_var.get(v)
            if lit is None:
                continue
            if value == (lit > 0):
                return True, ()
            removed.add(v)
        if not removed:
            return False, residual
        return False, tuple(lit for lit in residual if abs(lit) not in removed)

    def propagate(self, node_id: int, residual: Clause) -> None:
        node = self.trie.nodes[node_id]
        self.metrics["symbolic_trie_visits"] += 1
        live = {abs(lit) for lit in residual}
        if not node.children or live.isdisjoint(node.descendant_variables):
            self.metrics["stable_subtrees"] += 1
            self.add_entry(node_id, residual)
            return
        for child_id in node.children:
            child = self.trie.nodes[child_id]
            sat, child_residual = self.apply_edge(residual, child.edge)
            if sat:
                self.metrics["satisfied_subtrees_pruned"] += 1
                continue
            self.propagate(child_id, child_residual)

    def compile(self) -> None:
        for raw in self.source:
            self.metrics["batch_source_literal_reads"] += len(raw)
            self.metrics["source_clause_count"] += 1
            self.metrics["source_literal_count"] += len(raw)
            self.metrics["source_max_clause_length"] = max(
                self.metrics["source_max_clause_length"], len(raw)
            )
            self.metrics["batch_source_normalization_work_upper"] += len(raw) * (
                2 + max(1, math.ceil(math.log2(len(raw) + 1)))
            )
            for lit in raw:
                self.metrics["source_max_variable"] = max(
                    self.metrics["source_max_variable"], abs(lit)
                )
            clause = clean_clause(raw)
            if clause is None:
                self.metrics["source_tautologies_deleted"] += 1
                continue
            self.propagate(0, clause)
        self.metrics["total_source_literal_reads"] = (
            self.metrics["cover_selection_source_literal_reads"]
            + self.metrics["batch_source_literal_reads"]
        )
        self.compute_storage()

    def compute_storage(self) -> None:
        largest = max(1, self.metrics["source_max_variable"])
        var_bits = max(1, (largest + 1).bit_length())
        node_bits = max(1, len(self.trie.nodes).bit_length())
        frag_bits = max(1, (len(self.fragments) + 1).bit_length())
        entry_bits = max(1, (len(self.entries) + 1).bit_length())
        pool = sum(var_bits + (var_bits + 1) * len(c) for c in self.fragments)
        trie_bits = 0
        for node in self.trie.nodes[1:]:
            trie_bits += node_bits + max(1, len(node.edge).bit_length())
            trie_bits += len(node.edge) * (var_bits + 1)
        references = len(self.entries) * (node_bits + frag_bits)
        payload_offsets = (len(self.trie.nodes) + 1) * entry_bits
        leaf_descriptors = len(self.trie.leaves) * node_bits
        source_bits = (
            var_bits
            + self.metrics["source_clause_count"] * var_bits
            + self.metrics["source_literal_count"] * (var_bits + 1)
        )
        candidate_pool_bits = (
            self.metrics["cover_candidate_clauses"] * var_bits
            + self.metrics["cover_candidate_literals"] * (var_bits + 1)
        )
        max_clause_buffer_bits = var_bits + (var_bits + 1) * self.metrics["source_max_clause_length"]
        max_depth = max((node.depth for node in self.trie.nodes), default=0)
        compile_stack_bits = (max_depth + 1) * max_clause_buffer_bits
        intern_index_bits = len(self.fragments) * frag_bits
        compile_peak = (
            pool
            + trie_bits
            + 2 * references
            + payload_offsets
            + intern_index_bits
            + compile_stack_bits
        )
        selection_peak = candidate_pool_bits + trie_bits + max_clause_buffer_bits
        storage_accounting_work = (
            len(self.trie.nodes) + len(self.fragments) + len(self.entries) + self.metrics["source_clause_count"]
        )
        self.metrics.update(
            source_encoding_bits=source_bits,
            fragment_pool_bits=pool,
            unique_payload_fragments=len(self.fragments),
            trie_bits=trie_bits,
            entry_reference_bits=references,
            payload_offset_bits=payload_offsets,
            leaf_descriptor_bits=leaf_descriptors,
            batch_object_bits=pool + trie_bits + references + payload_offsets,
            shared_H_plus_source_bits=source_bits + pool + trie_bits + references + payload_offsets,
            cover_candidate_pool_bits=candidate_pool_bits,
            cover_selection_peak_workspace_bits=selection_peak,
            compile_stack_buffer_bits=compile_stack_bits,
            compile_peak_logical_workspace_bits=compile_peak,
            storage_accounting_work=storage_accounting_work,
            max_route_depth=max_depth,
        )

    def ancestors(self, leaf_node: int) -> List[int]:
        out = []
        at: Optional[int] = leaf_node
        while at is not None:
            out.append(at)
            at = self.trie.nodes[at].parent
        return list(reversed(out))

    def recover(self, leaf_node: int) -> Formula:
        clauses = []
        for node_id in self.ancestors(leaf_node):
            payload = self.trie.nodes[node_id].payload
            self.metrics["recovery_payload_reference_reads"] += len(payload)
            for frag in payload:
                clause = self.fragments[frag]
                self.metrics["recovery_literal_emits"] += len(clause)
                clauses.append(clause)
        # Canonicalization is part of child recovery and is charged by the
        # emitted-fragment counters plus this comparison ledger.
        canon_metrics = Counter()
        result = base.canonical(clauses, canon_metrics)
        self.metrics["recovery_canonical_work"] += sum(canon_metrics.values())
        return result


def independent_restrict(source: Sequence[Clause], assignment: Assignment) -> Tuple[Formula, Counter]:
    metrics = Counter()
    result = base.restrict_formula(tuple(tuple(c) for c in source), assignment, metrics)
    return result, metrics


def primal_components(f: Formula) -> int:
    vs = set(base.variables(f))
    if not vs:
        return 0
    adj = {v: set() for v in vs}
    for c in f:
        cv = [abs(x) for x in c]
        for v in cv[1:]:
            adj[cv[0]].add(v)
            adj[v].add(cv[0])
    count = 0
    while vs:
        count += 1
        todo = [next(iter(vs))]
        seen = set()
        while todo:
            v = todo.pop()
            if v in seen:
                continue
            seen.add(v)
            vs.discard(v)
            todo.extend(adj[v] - seen)
    return count


def family_stats(residuals: Sequence[Formula]) -> Dict[str, int]:
    clause_sets = [set(f) for f in residuals]
    comparable = 0
    for i, j in it.combinations(range(len(residuals)), 2):
        if clause_sets[i] <= clause_sets[j] or clause_sets[j] <= clause_sets[i]:
            comparable += 1
    horn = [all(sum(lit > 0 for lit in c) <= 1 for c in f) for f in residuals]
    two_cnf = [all(len(c) <= 2 for c in f) for f in residuals]
    return dict(
        unique_residuals=len(set(residuals)),
        equality_merges=len(residuals) - len(set(residuals)),
        clause_dominance_comparable_pairs=comparable,
        horn_children=sum(horn),
        two_cnf_children=sum(two_cnf),
        polynomial_portfolio_children=sum(a or b for a, b in zip(horn, two_cnf)),
        zero_clause_children=sum(not f for f in residuals),
        explicit_empty_clause_children=sum(() in f for f in residuals),
        decomposable_children=sum(primal_components(f) > 1 for f in residuals),
    )


def php(pigeons: int, holes: int) -> Formula:
    var = lambda p, h: p * holes + h + 1
    out: List[Clause] = [tuple(var(p, h) for h in range(holes)) for p in range(pigeons)]
    for h in range(holes):
        for p, q in it.combinations(range(pigeons), 2):
            out.append((-var(p, h), -var(q, h)))
    return tuple(out)


def xor_constraint(literals: Sequence[int], parity: int) -> List[Clause]:
    out = []
    for values in it.product((False, True), repeat=len(literals)):
        if sum(values) % 2 != parity:
            # Exclude this falsifying assignment.
            out.append(tuple(v if not value else -v for v, value in zip(literals, values)))
    return out


def prism_tseitin(m: int, odd_charge: bool) -> Tuple[Formula, Assignment]:
    # Circular ladder with 2m vertices and 3m edges; every vertex has degree 3.
    edges = []
    for row in (0, 1):
        for i in range(m):
            edges.append(((row, i), (row, (i + 1) % m)))
    for i in range(m):
        edges.append(((0, i), (1, i)))
    incidence: Dict[Tuple[int, int], List[int]] = {(r, i): [] for r in (0, 1) for i in range(m)}
    for j, (u, v) in enumerate(edges, 1):
        incidence[u].append(j)
        incidence[v].append(j)
    clauses: List[Clause] = []
    for index, vertex in enumerate(sorted(incidence)):
        charge = int(odd_charge and index == 0)
        clauses.extend(xor_constraint(incidence[vertex], charge))
    return tuple(clauses), {j: False for j in range(1, len(edges) + 1)}


def random_3cnf(n: int, m: int, seed: int, planted: bool) -> Tuple[Formula, Assignment]:
    rng = random.Random(seed)
    witness = {v: True for v in range(1, n + 1)}
    clauses = []
    for _ in range(m):
        vs = rng.sample(range(1, n + 1), 3)
        signs = [rng.choice((-1, 1)) for _ in range(3)]
        if planted and all(s < 0 for s in signs):
            signs[rng.randrange(3)] = 1
        clauses.append(tuple(v * s for v, s in zip(vs, signs)))
    return tuple(clauses), witness


def repeated_source() -> Tuple[Formula, Assignment]:
    core, witness = random_3cnf(16, 24, 22001, True)
    return tuple(c for c in core for _ in range(20)), witness


def disjoint_components(blocks: int = 5) -> Tuple[Formula, Assignment]:
    clauses: List[Clause] = []
    witness: Assignment = {}
    for b in range(blocks):
        offset = 6 * b
        local, _ = random_3cnf(6, 12, 23000 + b, True)
        clauses.extend(tuple((abs(x) + offset) * (1 if x > 0 else -1) for x in c) for c in local)
        witness.update({offset + v: True for v in range(1, 7)})
    return tuple(clauses), witness


def backdoor_dnf_source(s: int = 4) -> Tuple[Formula, Assignment]:
    p = 1
    aa = list(range(2, s + 2))
    qq = list(range(s + 2, s + 2 + (2 ** s - s)))
    rows: List[Clause] = [(a, p) for a in aa]
    rows.extend(tuple(aa + [q, -p]) for q in qq)
    largest = max(x for c in rows for x in map(abs, c))
    return tuple(rows), {v: True for v in range(1, largest + 1)}


def semantic_antichain(d: int = 6) -> Tuple[Formula, Assignment, Tuple[int, ...]]:
    selectors = tuple(range(1, d + 1))
    clauses: List[Clause] = []
    next_var = d + 1
    for bits in it.product((False, True), repeat=d):
        guard = [(-v if bit else v) for v, bit in zip(selectors, bits)]
        payload = [next_var, next_var + 1, next_var + 2]
        next_var += 3
        clauses.append(tuple(guard + payload))
    witness = {v: True for v in range(1, next_var)}
    return tuple(clauses), witness, selectors


def semantic_antichain_common_core(
    d: int = 6, core_variables: int = 256
) -> Tuple[Formula, Assignment, Tuple[int, ...]]:
    """Guarded private residuals plus a large route-independent 2-CNF core.

    Each residual contains the same near-parent-size core and one private
    positive clause.  Thus equality and clause-subset dominance cannot merge
    the residuals, while explicit ordinary-CNF emission repeats the core q
    times.  The all-true assignment witnesses satisfiability.
    """
    guarded, _, selectors = semantic_antichain(d)
    first_core = max((abs(x) for c in guarded for x in c), default=d) + 1
    core = tuple(
        (-(first_core + i), first_core + i + 1)
        for i in range(core_variables - 1)
    ) + ((first_core, first_core + 1),)
    source = guarded + core
    largest = max(abs(x) for c in source for x in c)
    return source, {v: True for v in range(1, largest + 1)}, selectors


def two_cnf_chain(n: int = 80) -> Tuple[Formula, Assignment]:
    clauses = tuple((-i, i + 1) for i in range(1, n)) + ((1, 2),)
    return clauses, {v: True for v in range(1, n + 1)}


def case_manifest() -> List[Dict[str, object]]:
    sparse, sparse_w = random_3cnf(30, 45, 21001, True)
    dense, dense_w = random_3cnf(24, 144, 21002, True)
    repeat, repeat_w = repeated_source()
    components, components_w = disjoint_components()
    bdnf, bdnf_w = backdoor_dnf_source()
    ts, ts_w = prism_tseitin(5, False)
    tu, _ = prism_tseitin(5, True)
    antichain, antichain_w, selectors = semantic_antichain()
    anti_core, anti_core_w, anti_core_selectors = semantic_antichain_common_core()
    chain, chain_w = two_cnf_chain()
    return [
        dict(name="random_sparse_planted", source=sparse, witness=sparse_w, cover="clause", depth=3),
        dict(name="random_dense_planted", source=dense, witness=dense_w, cover="clause", depth=3),
        dict(name="repeated_clause_positive", source=repeat, witness=repeat_w, cover="clause", depth=3),
        dict(name="disjoint_components", source=components, witness=components_w, cover="clause", depth=3),
        dict(name="backdoor_DNF", source=bdnf, witness=bdnf_w, cover="clause", depth=3),
        dict(name="Tseitin_prism_SAT", source=ts, witness=ts_w, cover="clause", depth=3),
        dict(name="Tseitin_prism_odd_UNSAT", source=tu, witness=None, cover="clause", depth=3),
        dict(name="PHP_5_4", source=php(5, 4), witness=None, cover="clause", depth=3),
        dict(name="PHP_6_5", source=php(6, 5), witness=None, cover="clause", depth=3),
        dict(name="PHP_7_6", source=php(7, 6), witness=None, cover="clause", depth=3),
        dict(name="two_CNF_chain", source=chain, witness=chain_w, cover="clause", depth=3),
        dict(name="semantic_antichain", source=antichain, witness=antichain_w, cover="shannon", variables=selectors),
        dict(
            name="semantic_antichain_common_core",
            source=anti_core,
            witness=anti_core_w,
            cover="shannon",
            variables=anti_core_selectors,
            semantic_antichain=True,
        ),
    ]


def verify_small_model_cover(source: Formula, trie: RouteTrie) -> int:
    vs = source_variables(source)
    if len(vs) > 15:
        return 0
    checks = 0
    for values in it.product((False, True), repeat=len(vs)):
        assignment = dict(zip(vs, values))
        if not source_satisfied(source, assignment):
            continue
        matches = [leaf for leaf in trie.leaves if all(assignment[v] == b for v, b in trie.nodes[leaf].assignment.items())]
        assert len(matches) == 1
        checks += 1
    return checks


def semantic_antichain_checks(residuals: Sequence[Formula]) -> int:
    # The constructed controls have one private positive clause per residual,
    # optionally beside a common all-true-satisfied core.  Exhibit both
    # implication counterdirections for every pair.
    checks = 0
    for left, right in it.combinations(residuals, 2):
        left_only = set(left) - set(right)
        right_only = set(right) - set(left)
        assert len(left_only) == len(right_only) == 1
        lc, rc = next(iter(left_only)), next(iter(right_only))
        assert len(lc) == len(rc) == 3 and all(x > 0 for x in lc + rc)
        assert set(map(abs, lc)).isdisjoint(map(abs, rc))
        all_variables = {abs(x) for f in (left, right) for c in f for x in c}
        a = {v: True for v in all_variables}
        for x in rc:
            a[abs(x)] = False
        a[abs(lc[0])] = True
        assert source_satisfied(left, a) and not source_satisfied(right, a)
        b = {v: True for v in all_variables}
        for x in lc:
            b[abs(x)] = False
        b[abs(rc[0])] = True
        assert source_satisfied(right, b) and not source_satisfied(left, b)
        checks += 2
    return checks


def run_case(spec: Dict[str, object]) -> Dict[str, object]:
    source = tuple(spec["source"])  # type: ignore[arg-type]
    if spec["cover"] == "clause":
        trie = build_clause_trie(source, int(spec["depth"]))
    else:
        trie = build_shannon_trie(tuple(spec["variables"]))  # type: ignore[arg-type]
    batch = BatchAcquire(source, trie)
    batch.compile()
    residuals = []
    verification_source_reads = 0
    verification_work = 0
    for leaf in trie.leaves:
        recovered = batch.recover(leaf)
        expected, vm = independent_restrict(source, trie.nodes[leaf].assignment)
        assert recovered == expected, (spec["name"], leaf, recovered, expected)
        verification_source_reads += sum(map(len, source))
        verification_work += sum(vm.values())
        residuals.append(recovered)
    witness = spec.get("witness")
    witness_route_checks = 0
    if witness is not None:
        assert source_satisfied(source, witness)  # type: ignore[arg-type]
        matching = [leaf for leaf in trie.leaves if all(witness[v] == b for v, b in trie.nodes[leaf].assignment.items())]  # type: ignore[index]
        assert len(matching) == 1
        chosen = residuals[trie.leaves.index(matching[0])]
        assert source_satisfied(chosen, witness)  # type: ignore[arg-type]
        witness_route_checks = 1
    model_cover_checks = verify_small_model_cover(source, trie)
    anti_checks = semantic_antichain_checks(residuals) if (
        spec["name"] == "semantic_antichain" or spec.get("semantic_antichain")
    ) else 0
    child_bits = [base.encoding_bits(f) for f in residuals]
    q = len(residuals)
    source_literals = sum(map(len, source))
    naive_reads = q * source_literals
    emitted = sum(child_bits)
    batch.metrics["total_child_explicit_bits"] = emitted
    batch.metrics["emitted_standalone_child_bits"] = emitted
    batch.metrics["max_child_explicit_bits"] = max(child_bits, default=0)
    batch.metrics["recursive_size_bits"] = max(child_bits, default=0)
    batch.metrics["naive_per_child_source_literal_reads"] = naive_reads
    batch.metrics["verification_source_literal_reads"] = verification_source_reads
    batch.metrics["verification_work_excluded"] = verification_work
    batch.metrics["source_read_savings_factor"] = naive_reads / max(1, batch.metrics["total_source_literal_reads"])
    batch.metrics["total_recovery_work"] = (
        batch.metrics["recovery_payload_reference_reads"]
        + batch.metrics["recovery_literal_emits"]
        + batch.metrics["recovery_canonical_work"]
    )
    construction_components = (
        "total_source_literal_reads",
        "cover_selection_normalization_work_upper",
        "cover_candidate_hash_literal_probes",
        "cover_greedy_candidate_tests",
        "cover_greedy_literal_probes",
        "cover_trie_residual_literal_probes_upper",
        "cover_trie_term_literal_probes",
        "route_edges",
        "route_assignment_records",
        "trie_finalize_set_work",
        "batch_source_normalization_work_upper",
        "delta_assignment_probes",
        "symbolic_trie_visits",
        "payload_entries",
        "storage_accounting_work",
    )
    batch.metrics["construction_work"] = sum(batch.metrics[k] for k in construction_components)
    frag_bits = max(1, (batch.metrics["unique_payload_fragments"] + 1).bit_length())
    max_path_refs = max(
        (
            sum(len(trie.nodes[node_id].payload) for node_id in batch.ancestors(leaf))
            for leaf in trie.leaves
        ),
        default=0,
    )
    batch.metrics["max_recovery_path_payload_references"] = max_path_refs
    recovery_peak = batch.metrics["batch_object_bits"] + 2 * max(child_bits, default=0) + max_path_refs * frag_bits
    batch.metrics["recovery_peak_logical_workspace_bits"] = recovery_peak
    batch.metrics["peak_logical_workspace_bits"] = max(
        batch.metrics["cover_selection_peak_workspace_bits"],
        batch.metrics["compile_peak_logical_workspace_bits"],
        recovery_peak,
    )
    batch.metrics["peak_logical_memory_including_readonly_source_bits"] = (
        batch.metrics["peak_logical_workspace_bits"] + batch.metrics["source_encoding_bits"]
    )
    M = max(2, batch.metrics["source_encoding_bits"])
    max_child = max(1, batch.metrics["max_child_explicit_bits"])
    a = math.log(max(1, q), M)
    lam = math.log(max_child, M)
    beta = math.log(max(1, batch.metrics["construction_work"]), M)
    recovery_exp = math.log(max(1, batch.metrics["total_recovery_work"]), M)
    # Counter.update adds counts and therefore rejects non-numeric metadata.
    # These are computed measurements, not increments, so assign them directly.
    batch.metrics["finite_fanout_exponent"] = a
    batch.metrics["finite_child_exponent"] = lam
    batch.metrics["finite_batch_construction_exponent"] = beta
    batch.metrics["finite_recovery_exponent"] = recovery_exp
    batch.metrics["finite_shared_object_exponent"] = math.log(
        max(1, batch.metrics["batch_object_bits"]), M
    )
    batch.metrics["finite_workspace_exponent"] = math.log(
        max(1, batch.metrics["peak_logical_workspace_bits"]), M
    )
    batch.metrics["finite_standalone_emission_exponent"] = math.log(max(1, emitted), M)
    batch.metrics["ordinary_all_block_k2_exponent"] = a + beta + 2 * lam
    batch.metrics["optimistic_global_batch_k2_exponent"] = max(beta, recovery_exp, a + 2 * lam)
    batch.metrics["descriptor_only_warning"] = (
        "Leaf ID is small only with current-scale shared H retained and a modified consumer interface."
    )
    return dict(
        name=spec["name"],
        cover=spec["cover"],
        variables=len(source_variables(source)),
        clauses=len(source),
        source_literals=source_literals,
        q=q,
        selected_clauses=[list(c) for c in trie.selected_clauses],
        witness_route_checks=witness_route_checks,
        model_cover_checks=model_cover_checks,
        semantic_antichain_checks=anti_checks,
        family=family_stats(residuals),
        metrics=dict(batch.metrics),
    )


def main() -> None:
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(25)
    started = time.perf_counter()
    rows = [run_case(spec) for spec in case_manifest()]
    result = dict(
        status="COMPUTATIONAL",
        scientific_status="OPEN",
        run_id="FINAL-LINK2-BATCHACQUIRE1",
        cases=len(rows),
        residual_recovery_checks=sum(r["q"] for r in rows),
        witness_route_checks=sum(r["witness_route_checks"] for r in rows),
        exhaustive_model_cover_checks=sum(r["model_cover_checks"] for r in rows),
        semantic_antichain_checks=sum(r["semantic_antichain_checks"] for r in rows),
        errors=0,
        seconds=time.perf_counter() - started,
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        rows=rows,
        conclusions=[
            "The compiled trie object uses one batch source scan after cover selection and recovers every child without a source reread.",
            "Construction work still includes symbolic trie probes; standalone recovery still emits every child bit.",
            "A leaf descriptor is not a smaller ordinary SAT instance because it retains a current-scale shared H and requires a parent-aware consumer.",
            "The semantic-antichain control forces distinct residual payloads and blocks equality or clause-dominance collapse.",
            "No general bound proves that the shared object, recovery, emitted bits, recursive size, and arbitrary-solver interface jointly enter any cited SAT time-space endpoint.",
        ],
    )
    Path(sys.argv[1]).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}, indent=2))
    for row in rows:
        m = row["metrics"]
        print(
            row["name"], "q", row["q"], "reads", m["total_source_literal_reads"],
            "naive", m["naive_per_child_source_literal_reads"], "object", m["batch_object_bits"],
            "emit", m["total_child_explicit_bits"], "maxchild", m["max_child_explicit_bits"],
            "sharedE", round(m["optimistic_global_batch_k2_exponent"], 4),
        )


if __name__ == "__main__":
    main()
