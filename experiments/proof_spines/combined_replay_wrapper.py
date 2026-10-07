#!/usr/bin/env python3
"""One-realization source-replay SAT wrapper.

The read-only CNF is never replaced by retained residual CNFs or a retained
formula DAG.  A subproblem is a tuple (clause scope, assignment mask, values).
Residual clauses are regenerated from the source.  The solver combines:

* streaming unit propagation;
* a block-batched clause-frontier dynamic program;
* exact AND decomposition over residual primal-graph components;
* exact Shannon OR branching; and
* a bounded answer cache.  Hashes only select cache candidates.  A streaming
  normalized-residual comparison is required before reuse, so collisions do
  not affect correctness.

Run: python combined_replay_wrapper.py OUTPUT.json
The batch has an internal 25-second alarm.  Finite tests are not an asymptotic
SAT theorem.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
import signal
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

Clause = Tuple[int, ...]
Formula = Tuple[Clause, ...]
Scope = Optional[Tuple[int, ...]]  # None denotes every source clause.
State = Tuple[Scope, int, int]


def popcount(x: int) -> int:
    return x.bit_count()


def truth(source: Formula, n: int) -> bool:
    return any(
        all(
            any(bool((assignment >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause)
            for clause in source
        )
        for assignment in range(1 << n)
    )


def formula_bits(source: Formula, n: int) -> int:
    width = max(1, n.bit_length())
    return width + sum(width + (width + 1) * len(clause) for clause in source)


@dataclass
class CacheEntry:
    signature: bytes
    state: State
    answer: bool
    descriptor_bits: int


class ReplaySolver:
    def __init__(
        self,
        source: Formula,
        n: int,
        *,
        frontier_cap: int = 5,
        frontier_block: int = 4,
        cache_budget_bits: int = 8192,
        digest_bytes: int = 8,
    ) -> None:
        self.source = source
        self.n = n
        self.m = len(source)
        self.frontier_cap = frontier_cap
        self.frontier_block = frontier_block
        self.cache_budget_bits = cache_budget_bits
        self.digest_bytes = digest_bytes
        self.variable_width = max(1, (n + 1).bit_length())
        self.clause_index_width = max(1, (self.m + 1).bit_length())
        self.source_encoding_bits = formula_bits(source, n)
        self.source_literal_slots = sum(map(len, source))
        # A RAM parser normally retains clause boundaries.  A strict sequential
        # tape can avoid this index but then pays the replay counter below.
        self.source_random_access_index_bits = self.m * max(
            1, (self.source_literal_slots + self.m + 1).bit_length()
        )
        self.cache: List[CacheEntry] = []
        self.cache_bits = 0
        self.metrics: Dict[str, int] = {
            "source_passes": 0,
            "source_clause_accesses": 0,
            "source_literal_reads": 0,
            "sequential_replay_clause_steps": 0,
            "recursive_calls": 0,
            "recursive_children_generated": 0,
            "max_recursion_depth": 0,
            "unit_propagations": 0,
            "branch_nodes": 0,
            "and_nodes": 0,
            "components_generated": 0,
            "frontier_attempts": 0,
            "frontier_completed": 0,
            "frontier_cap_exits": 0,
            "frontier_transitions": 0,
            "frontier_blocks": 0,
            "max_frontier_width": 0,
            "max_frontier_union_width": 0,
            "max_frontier_table_bytes": 1,
            "max_frontier_last_records": 0,
            "max_frontier_block_literal_slots": 0,
            "cache_lookups": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "cache_insertions": 0,
            "cache_evictions": 0,
            "cache_candidate_comparisons": 0,
            "cache_hash_collisions_rejected": 0,
            "max_cache_entries": 0,
            "max_cache_descriptor_bits": 0,
            "max_normalization_records": 0,
            "max_component_records": 0,
            "max_component_scope_ids": 0,
            "max_live_descriptor_bits": 0,
            "max_frontier_aux_bits": 0,
            "max_component_aux_bits": 0,
            "max_normalization_aux_bits": 0,
            "max_charged_workspace_bits_random_access": 0,
            "max_charged_workspace_bits_sequential": 0,
            "max_semantic_residual_bits": 0,
            "recursive_size_reductions": 0,
            "recursive_nonreductions": 0,
            "max_recursive_child_semantic_bits": 0,
            "sat_oracle_calls": 0,
            "retained_residual_formulas": 0,
            "retained_formula_dag_nodes": 0,
            "source_encoding_bits": self.source_encoding_bits,
            "source_literal_slots": self.source_literal_slots,
            "source_random_access_index_bits": self.source_random_access_index_bits,
        }

    def scope_ids(self, scope: Scope) -> Iterable[int]:
        return range(self.m) if scope is None else scope

    def descriptor_bits(self, state: State) -> int:
        scope, mask, values = state
        index_width = max(1, (self.m + 1).bit_length())
        scope_bits = 1 if scope is None else 1 + len(scope) * index_width
        # This charges the actual dense integer representation used here.
        return scope_bits + max(1, mask.bit_length()) + max(1, values.bit_length())

    def update_live(self, live_bits: int, ephemeral_bits: int = 0) -> None:
        total = live_bits + ephemeral_bits + self.cache_bits
        self.metrics["max_live_descriptor_bits"] = max(
            self.metrics["max_live_descriptor_bits"], total
        )
        self.metrics["max_charged_workspace_bits_sequential"] = max(
            self.metrics["max_charged_workspace_bits_sequential"], total
        )
        self.metrics["max_charged_workspace_bits_random_access"] = max(
            self.metrics["max_charged_workspace_bits_random_access"],
            total + self.source_random_access_index_bits,
        )

    def residual_clauses(self, state: State) -> Iterator[Tuple[int, Clause]]:
        """Regenerate a residual stream.  No residual clause survives the pass."""
        scope, mask, values = state
        self.metrics["source_passes"] += 1
        # A strict sequential-source implementation may need one whole-source
        # replay to locate a sparse scope.  Record that model separately from
        # direct read-only random access.
        self.metrics["sequential_replay_clause_steps"] += self.m
        for clause_id in self.scope_ids(scope):
            clause = self.source[clause_id]
            self.metrics["source_clause_accesses"] += 1
            residual: List[int] = []
            satisfied = False
            for literal in clause:
                self.metrics["source_literal_reads"] += 1
                bit = 1 << (abs(literal) - 1)
                if mask & bit:
                    if bool(values & bit) == (literal > 0):
                        satisfied = True
                        break
                else:
                    residual.append(literal)
            if not satisfied:
                yield clause_id, tuple(residual)

    def inspect_state(
        self, state: State
    ) -> Tuple[str, int, int, Optional[int], Optional[int]]:
        """One source pass: status, residual bits/count, first var, first unit."""
        width = max(1, self.n.bit_length())
        unit: Optional[int] = None
        first: Optional[int] = None
        clauses = 0
        bits = width
        conflict = False
        for _, residual in self.residual_clauses(state):
            clauses += 1
            bits += width + (width + 1) * len(residual)
            if not residual:
                conflict = True
                break
            if first is None:
                first = abs(residual[0])
            if len(residual) == 1 and unit is None:
                unit = residual[0]
        self.metrics["max_semantic_residual_bits"] = max(
            self.metrics["max_semantic_residual_bits"], bits
        )
        if conflict:
            return "UNSAT", bits, clauses, first, unit
        if clauses == 0:
            return "SAT", bits, clauses, first, unit
        return "OPEN", bits, clauses, first, unit

    def normalized_residual(self, state: State, live_bits: int = 0) -> Iterator[Clause]:
        """First-occurrence variable renaming; equal streams are isomorphic CNFs."""
        mapping: Dict[int, int] = {}
        for _, clause in self.residual_clauses(state):
            normalized: List[int] = []
            for literal in clause:
                variable = abs(literal)
                if variable not in mapping:
                    mapping[variable] = len(mapping) + 1
                    self.metrics["max_normalization_records"] = max(
                        self.metrics["max_normalization_records"], len(mapping)
                    )
                    aux = 2 * len(mapping) * self.variable_width
                    self.metrics["max_normalization_aux_bits"] = max(
                        self.metrics["max_normalization_aux_bits"], aux
                    )
                    self.update_live(live_bits, aux)
                label = mapping[variable]
                normalized.append(label if literal > 0 else -label)
            yield tuple(normalized)

    def signature(self, state: State, live_bits: int = 0) -> bytes:
        digest = hashlib.sha256()
        for clause in self.normalized_residual(state, live_bits):
            digest.update(len(clause).to_bytes(4, "big"))
            for literal in clause:
                digest.update(int(literal).to_bytes(8, "big", signed=True))
        return digest.digest()[: self.digest_bytes]

    def residual_equal(self, left: State, right: State, live_bits: int = 0) -> bool:
        sentinel = object()
        # Both generators and both renaming dictionaries can be live together.
        dual_aux = 4 * self.n * self.variable_width
        self.metrics["max_normalization_aux_bits"] = max(
            self.metrics["max_normalization_aux_bits"], dual_aux
        )
        self.update_live(live_bits, dual_aux)
        for a, b in itertools.zip_longest(
            self.normalized_residual(left, live_bits),
            self.normalized_residual(right, live_bits),
            fillvalue=sentinel,
        ):
            if a != b:
                return False
        return True

    def cache_lookup(self, state: State, live_bits: int = 0) -> Optional[bool]:
        if self.cache_budget_bits <= 0:
            return None
        self.metrics["cache_lookups"] += 1
        signature = self.signature(state, live_bits)
        compared = False
        for entry in reversed(self.cache):
            if entry.signature != signature:
                continue
            compared = True
            self.metrics["cache_candidate_comparisons"] += 1
            if self.residual_equal(state, entry.state, live_bits):
                self.metrics["cache_hits"] += 1
                return entry.answer
            self.metrics["cache_hash_collisions_rejected"] += 1
        self.metrics["cache_misses"] += 1
        # "compared" is intentionally unused except to document that a miss can
        # be a clean bucket miss or a rejected collision.
        _ = compared
        return None

    def cache_insert(self, state: State, answer: bool, live_bits: int = 0) -> None:
        if self.cache_budget_bits <= 0:
            return
        descriptor = self.descriptor_bits(state) + 8 * self.digest_bytes + 1
        if descriptor > self.cache_budget_bits:
            return
        signature = self.signature(state, live_bits)
        while self.cache and self.cache_bits + descriptor > self.cache_budget_bits:
            old = self.cache.pop(0)
            self.cache_bits -= old.descriptor_bits
            self.metrics["cache_evictions"] += 1
        self.cache.append(CacheEntry(signature, state, answer, descriptor))
        self.cache_bits += descriptor
        self.metrics["cache_insertions"] += 1
        self.metrics["max_cache_entries"] = max(
            self.metrics["max_cache_entries"], len(self.cache)
        )
        self.metrics["max_cache_descriptor_bits"] = max(
            self.metrics["max_cache_descriptor_bits"], self.cache_bits
        )
        self.update_live(live_bits)

    def frontier(self, state: State, live_bits: int = 0) -> Optional[bool]:
        """Block-batched frontier DP over regenerated residual streams."""
        self.metrics["frontier_attempts"] += 1
        boundary: List[int] = []
        table = bytearray([1])
        start = 0
        while True:
            block: List[Clause] = []
            last: Dict[int, int] = {variable: -1 for variable in boundary}
            total = 0
            for _, clause in self.residual_clauses(state):
                position = total
                total += 1
                if start <= position < start + self.frontier_block:
                    block.append(clause)
                    for literal in clause:
                        last[abs(literal)] = position
                elif position >= start + self.frontier_block:
                    for literal in clause:
                        variable = abs(literal)
                        if variable in last:
                            last[variable] = position
            if not block:
                self.metrics["frontier_completed"] += 1
                return bool(table[0])
            self.metrics["frontier_blocks"] += 1
            self.metrics["max_frontier_last_records"] = max(
                self.metrics["max_frontier_last_records"], len(last)
            )
            self.metrics["max_frontier_block_literal_slots"] = max(
                self.metrics["max_frontier_block_literal_slots"], sum(map(len, block))
            )
            block_slots = sum(map(len, block))
            frontier_aux = (
                block_slots * (self.variable_width + 1)
                + len(last) * (self.variable_width + self.clause_index_width)
                + (len(boundary) + 3 * self.frontier_cap) * self.variable_width
                + 8 * len(table)
            )
            self.metrics["max_frontier_aux_bits"] = max(
                self.metrics["max_frontier_aux_bits"], frontier_aux
            )
            self.update_live(live_bits, frontier_aux)
            for offset, clause in enumerate(block):
                position = start + offset
                union = list(boundary)
                for literal in clause:
                    if abs(literal) not in union:
                        union.append(abs(literal))
                after = [variable for variable in union if last[variable] > position]
                if len(after) > self.frontier_cap:
                    self.metrics["frontier_cap_exits"] += 1
                    return None
                boundary_positions = [union.index(variable) for variable in after]
                literal_positions = [
                    (union.index(abs(literal)), literal > 0) for literal in clause
                ]
                output = bytearray(1 << len(after))
                old_mask = (1 << len(boundary)) - 1
                self.metrics["max_frontier_union_width"] = max(
                    self.metrics["max_frontier_union_width"], len(union)
                )
                self.metrics["max_frontier_width"] = max(
                    self.metrics["max_frontier_width"], len(boundary), len(after)
                )
                self.metrics["max_frontier_table_bytes"] = max(
                    self.metrics["max_frontier_table_bytes"], len(table) + len(output)
                )
                transition_aux = (
                    frontier_aux
                    + 8 * len(output)
                    + (
                        len(union)
                        + len(after)
                        + len(boundary_positions)
                        + 2 * len(literal_positions)
                    )
                    * self.variable_width
                )
                self.metrics["max_frontier_aux_bits"] = max(
                    self.metrics["max_frontier_aux_bits"], transition_aux
                )
                self.update_live(live_bits, transition_aux)
                for assignment in range(1 << len(union)):
                    self.metrics["frontier_transitions"] += 1
                    if not table[assignment & old_mask]:
                        continue
                    if not any(
                        bool((assignment >> index) & 1) == positive
                        for index, positive in literal_positions
                    ):
                        continue
                    projected = sum(
                        ((assignment >> old_index) & 1) << new_index
                        for new_index, old_index in enumerate(boundary_positions)
                    )
                    output[projected] = 1
                boundary = after
                table = output
                if not any(table):
                    self.metrics["frontier_completed"] += 1
                    return False
            start += len(block)
            if start >= total:
                self.metrics["frontier_completed"] += 1
                return bool(table[0])

    def components(self, state: State, live_bits: int = 0) -> List[Tuple[int, ...]]:
        """Materialize clause identifiers and union-find records, not clauses."""
        parent: Dict[int, int] = {}
        rank: Dict[int, int] = {}
        residual_ids: List[Tuple[int, int]] = []

        def find(variable: int) -> int:
            root = variable
            while parent[root] != root:
                root = parent[root]
            while parent[variable] != variable:
                nxt = parent[variable]
                parent[variable] = root
                variable = nxt
            return root

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1

        pending: List[Tuple[int, int]] = []
        for clause_id, clause in self.residual_clauses(state):
            variables = [abs(literal) for literal in clause]
            for variable in variables:
                if variable not in parent:
                    parent[variable] = variable
                    rank[variable] = 0
            for variable in variables[1:]:
                union(variables[0], variable)
            pending.append((clause_id, variables[0]))
        groups: Dict[int, List[int]] = {}
        for clause_id, variable in pending:
            groups.setdefault(find(variable), []).append(clause_id)
        self.metrics["max_component_records"] = max(
            self.metrics["max_component_records"], len(parent) + len(pending)
        )
        scopes = [tuple(ids) for _, ids in sorted(groups.items(), key=lambda pair: pair[1][0])]
        self.metrics["max_component_scope_ids"] = max(
            self.metrics["max_component_scope_ids"], sum(map(len, scopes))
        )
        # Conservative simultaneous logical payload: parent/rank maps, pending
        # pairs, grouping lists, and returned immutable scopes.
        component_aux = (
            4 * len(parent) * self.variable_width
            + len(pending) * (self.clause_index_width + self.variable_width)
            + 2 * sum(map(len, scopes)) * self.clause_index_width
            + len(scopes) * self.variable_width
        )
        self.metrics["max_component_aux_bits"] = max(
            self.metrics["max_component_aux_bits"], component_aux
        )
        self.update_live(live_bits, component_aux)
        return scopes

    def solve(self) -> Tuple[bool, Dict[str, int]]:
        answer = self._solve((None, 0, 0), depth=0, live_bits=0, parent_bits=None)
        return answer, self.metrics

    def _solve(
        self,
        state: State,
        *,
        depth: int,
        live_bits: int,
        parent_bits: Optional[int],
    ) -> bool:
        self.metrics["recursive_calls"] += 1
        self.metrics["max_recursion_depth"] = max(
            self.metrics["max_recursion_depth"], depth
        )
        status, semantic_bits, _, first, unit = self.inspect_state(state)
        descriptor = self.descriptor_bits(state)
        local_live = live_bits + descriptor
        self.update_live(local_live)
        if parent_bits is not None:
            self.metrics["max_recursive_child_semantic_bits"] = max(
                self.metrics["max_recursive_child_semantic_bits"], semantic_bits
            )
            if semantic_bits < parent_bits:
                self.metrics["recursive_size_reductions"] += 1
            else:
                self.metrics["recursive_nonreductions"] += 1

        cached = self.cache_lookup(state, local_live)
        if cached is not None:
            return cached

        if status == "SAT":
            self.cache_insert(state, True, local_live)
            return True
        if status == "UNSAT":
            self.cache_insert(state, False, local_live)
            return False

        frontier_answer = self.frontier(state, local_live)
        frontier_bits = 8 * self.metrics["max_frontier_table_bytes"]
        self.update_live(local_live, frontier_bits)
        if frontier_answer is not None:
            self.cache_insert(state, frontier_answer, local_live)
            return frontier_answer

        # A unit is used only after the bounded frontier attempt exits.  This
        # ordering lets narrow implication chains use the batched acquisition
        # path instead of forcing one whole-source rescan per implication.
        if unit is not None:
            bit = 1 << (abs(unit) - 1)
            child_mask = state[1] | bit
            child_values = state[2] | bit if unit > 0 else state[2] & ~bit
            self.metrics["unit_propagations"] += 1
            self.metrics["recursive_children_generated"] += 1
            answer = self._solve(
                (state[0], child_mask, child_values),
                depth=depth + 1,
                live_bits=local_live,
                parent_bits=semantic_bits,
            )
            self.cache_insert(state, answer, local_live)
            return answer

        scopes = self.components(state, local_live)
        if len(scopes) > 1:
            self.metrics["and_nodes"] += 1
            self.metrics["components_generated"] += len(scopes)
            index_width = max(1, (self.m + 1).bit_length())
            grouping_bits = sum(len(scope) for scope in scopes) * index_width
            self.update_live(local_live, grouping_bits)
            answer = True
            for scope in scopes:
                self.metrics["recursive_children_generated"] += 1
                if not self._solve(
                    (scope, state[1], state[2]),
                    depth=depth + 1,
                    live_bits=local_live + grouping_bits,
                    parent_bits=semantic_bits,
                ):
                    answer = False
                    break
            self.cache_insert(state, answer, local_live)
            return answer

        # The one-component scope list is only a discovery artifact.  Drop it
        # before branching so it is not silently retained in the parent frame.
        del scopes
        assert first is not None
        self.metrics["branch_nodes"] += 1
        bit = 1 << (first - 1)
        self.metrics["recursive_children_generated"] += 1
        if self._solve(
            (state[0], state[1] | bit, state[2] & ~bit),
            depth=depth + 1,
            live_bits=local_live,
            parent_bits=semantic_bits,
        ):
            self.cache_insert(state, True, local_live)
            return True
        self.metrics["recursive_children_generated"] += 1
        answer = self._solve(
            (state[0], state[1] | bit, state[2] | bit),
            depth=depth + 1,
            live_bits=local_live,
            parent_bits=semantic_bits,
        )
        self.cache_insert(state, answer, local_live)
        return answer


def repeated_triangle(blocks: int, interleave: bool = True) -> Tuple[int, Formula]:
    components: List[List[Clause]] = []
    for block in range(blocks):
        a = 3 * block + 1
        components.append([(a, a + 1), (-a, a + 2), (-(a + 1), a + 2)])
    if interleave:
        formula = tuple(components[b][row] for row in range(3) for b in range(blocks))
    else:
        formula = tuple(clause for component in components for clause in component)
    return 3 * blocks, formula


def repeated_dense_sat(blocks: int, width: int = 5) -> Tuple[int, Formula]:
    """Interleaved isomorphic components, each with one satisfying assignment."""
    components: List[List[Clause]] = []
    all_true = (1 << width) - 1
    for block in range(blocks):
        base = width * block
        component: List[Clause] = []
        for assignment in range(1 << width):
            if assignment == all_true:
                continue
            component.append(
                tuple(
                    -(base + index + 1) if (assignment >> index) & 1 else base + index + 1
                    for index in range(width)
                )
            )
        components.append(component)
    formula = tuple(
        components[block][row]
        for row in range(len(components[0]))
        for block in range(blocks)
    )
    return blocks * width, formula


def pigeonhole(pigeons: int, holes: int) -> Tuple[int, Formula]:
    variable = lambda pigeon, hole: pigeon * holes + hole + 1
    clauses: List[Clause] = [
        tuple(variable(pigeon, hole) for hole in range(holes)) for pigeon in range(pigeons)
    ]
    clauses += [
        (-variable(left, hole), -variable(right, hole))
        for hole in range(holes)
        for left in range(pigeons)
        for right in range(left + 1, pigeons)
    ]
    return pigeons * holes, tuple(clauses)


def cases() -> List[Tuple[str, int, Formula, Optional[bool]]]:
    rows: List[Tuple[str, int, Formula, Optional[bool]]] = []
    signed3 = list(itertools.product(*[(i, -i) for i in range(1, 4)]))
    for subset in range(256):
        rows.append(
            (
                f"exhaustive3_{subset}",
                3,
                tuple(clause for index, clause in enumerate(signed3) if (subset >> index) & 1),
                None,
            )
        )
    rng = random.Random(20261007)
    for n in (6, 8, 10):
        for seed in range(4):
            formula = tuple(
                tuple(variable * rng.choice((-1, 1)) for variable in rng.sample(range(1, n + 1), 3))
                for _ in range(4 * n)
            )
            rows.append((f"random_{n}_{seed}", n, formula, None))
    for n in (16, 32, 64):
        rows.append((f"chain_{n}", n, tuple([(-v, v + 1) for v in range(1, n)] + [(1,)]), True))
    for blocks in (2, 4, 8):
        n, formula = repeated_triangle(blocks, interleave=True)
        rows.append((f"interleaved_components_{blocks}", n, formula, True))
    for blocks in (2, 4):
        n, formula = repeated_dense_sat(blocks)
        rows.append((f"dense_isomorphic_components_{blocks}", n, formula, True))
    for n in (8, 10):
        formula = tuple((v, -v) for v in range(1, n)) + ((n,), (-n,))
        rows.append((f"late_contradiction_{n}", n, formula, False))
    n, formula = pigeonhole(4, 3)
    rows.append(("php_4_3", n, formula, False))
    for pigeons, holes in ((5, 4), (6, 5), (7, 6)):
        n, formula = pigeonhole(pigeons, holes)
        rows.append((f"php_{pigeons}_{holes}", n, formula, False))
    n = 5
    full_width = tuple(
        tuple((i + 1) if ((assignment >> i) & 1) == 0 else -(i + 1) for i in range(n))
        for assignment in range(1 << n)
    )
    rows.append(("all_assignments_forbidden_5", n, full_width, False))
    rows += [
        ("empty", 0, (), True),
        ("empty_clause", 0, ((),), False),
        ("unit_conflict", 1, ((1,), (-1,)), False),
    ]
    return rows


def deadline(*_: object) -> None:
    raise TimeoutError("25-second combined replay batch limit reached")


def main() -> None:
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(25)
    started = time.perf_counter()
    details = []
    checks = 0
    cache_answer_matches = 0
    for name, n, source, expected in cases():
        if expected is None:
            expected = truth(source, n)
        configured = ReplaySolver(
            source,
            n,
            frontier_cap=5,
            frontier_block=4,
            cache_budget_bits=8192,
            digest_bytes=8,
        )
        answer, metrics = configured.solve()
        assert answer == expected, (name, answer, expected)
        checks += 1
        # For bounded controls, compare against the identical realization with
        # sharing disabled.  This tests that cache reuse changes cost, not truth.
        no_cache_metrics = None
        if (
            name.startswith("exhaustive3_")
            or name.startswith("interleaved_components_")
            or name.startswith("dense_isomorphic_components_")
        ):
            uncached = ReplaySolver(
                source,
                n,
                frontier_cap=5,
                frontier_block=4,
                cache_budget_bits=0,
                digest_bytes=8,
            )
            uncached_answer, no_cache_metrics = uncached.solve()
            assert uncached_answer == answer
            cache_answer_matches += 1
        details.append(
            {
                "name": name,
                "n": n,
                "clauses": len(source),
                "literals": sum(map(len, source)),
                "input_bits": formula_bits(source, n),
                "answer": answer,
                "metrics": metrics,
                "no_cache_metrics": no_cache_metrics,
            }
        )

    # Adversarial hash-bucket control: a zero-byte signature sends every entry
    # to one bucket.  Exact residual replay must reject unequal formulas.
    collision_checks = 0
    collision_rejections = 0
    for name, n, source, expected in cases():
        if name not in {"random_8_0", "all_assignments_forbidden_5", "interleaved_components_4"}:
            continue
        if expected is None:
            expected = truth(source, n)
        solver = ReplaySolver(
            source,
            n,
            frontier_cap=3,
            frontier_block=3,
            cache_budget_bits=4096,
            digest_bytes=0,
        )
        answer, metrics = solver.solve()
        assert answer == expected
        collision_checks += 1
        collision_rejections += metrics["cache_hash_collisions_rejected"]
    assert collision_rejections > 0

    aggregate = {
        key: sum(row["metrics"][key] for row in details)
        for key in (
            "source_passes",
            "source_clause_accesses",
            "source_literal_reads",
            "sequential_replay_clause_steps",
            "recursive_calls",
            "recursive_children_generated",
            "frontier_attempts",
            "frontier_completed",
            "frontier_cap_exits",
            "frontier_transitions",
            "and_nodes",
            "branch_nodes",
            "cache_hits",
            "cache_hash_collisions_rejected",
            "unit_propagations",
            "recursive_size_reductions",
            "recursive_nonreductions",
        )
    }
    maxima = {
        key: max(row["metrics"][key] for row in details)
        for key in (
            "max_recursion_depth",
            "max_cache_descriptor_bits",
            "max_frontier_aux_bits",
            "max_component_aux_bits",
            "max_normalization_aux_bits",
            "max_charged_workspace_bits_sequential",
            "max_charged_workspace_bits_random_access",
        )
    }
    block_tradeoff = []
    chain_n = 256
    chain = tuple([(-v, v + 1) for v in range(1, chain_n)] + [(1,)])
    for block in (1, 4, 16, 32):
        solver = ReplaySolver(
            chain,
            chain_n,
            frontier_cap=5,
            frontier_block=block,
            cache_budget_bits=0,
            digest_bytes=8,
        )
        answer, metrics = solver.solve()
        assert answer is True
        block_tradeoff.append(
            {
                "block": block,
                "source_passes": metrics["source_passes"],
                "source_literal_reads": metrics["source_literal_reads"],
                "sequential_replay_clause_steps": metrics["sequential_replay_clause_steps"],
                "frontier_transitions": metrics["frontier_transitions"],
                "max_frontier_table_bytes": metrics["max_frontier_table_bytes"],
                "max_frontier_last_records": metrics["max_frontier_last_records"],
                "max_frontier_block_literal_slots": metrics["max_frontier_block_literal_slots"],
            }
        )
    result = {
        "status": "COMPUTATIONAL",
        "cases": len(details),
        "answer_checks": checks,
        "cache_disabled_answer_matches": cache_answer_matches,
        "forced_collision_answer_checks": collision_checks,
        "forced_collision_rejections": collision_rejections,
        "errors": 0,
        "seconds": time.perf_counter() - started,
        "seed": 20261007,
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "aggregate": aggregate,
        "maxima": maxima,
        "chain_256_block_tradeoff": block_tradeoff,
        "details": details,
        "scope": (
            "One exact realization using source replay, streaming frontier DP, "
            "component AND, Shannon OR, and collision-safe bounded sharing."
        ),
        "limitations": [
            "Finite correctness and accounting tests do not prove favorable general-SAT exponents.",
            "Component discovery materializes union-find records and clause-ID scopes, though never residual clauses.",
            "Python recursion retains ancestor descriptors; max_live_descriptor_bits charges their logical payload.",
            "Random clause access and strict sequential replay are both counted; the relevant endpoint model must be fixed.",
            "A frontier cap exit falls back to exact branching, whose general total can be exponential.",
            "Cache equality uses full normalized residual replay; the hash is not a correctness premise.",
        ],
    }
    destination = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_suffix(".json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    signal.alarm(0)
    print(json.dumps({key: value for key, value in result.items() if key != "details"}, indent=2))
    for row in details:
        if row["name"] in {
            "random_10_0",
            "chain_64",
            "interleaved_components_8",
            "dense_isomorphic_components_4",
            "all_assignments_forbidden_5",
            "php_4_3",
            "php_6_5",
        }:
            print(json.dumps(row))


if __name__ == "__main__":
    main()
