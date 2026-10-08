#!/usr/bin/env python3
"""UNIT-TAIL-REPLAY1: iterative forced-assignment transitions.

No saved list of pre-unit states is kept. Consequently those intermediate
states are not inserted into the answer cache on unwind. Exact cache matching,
frontier-first order, component AND, Shannon OR and the original cache budget
are unchanged. Inherited metrics count logical payloads, NOT measured Python
heap or complete machine workspace. Inherited recursive_size_reductions/nonreductions and child-semantic-size
counters describe logical edges, including tail transitions, not stack pushes.
One transition also conservatively charges
old/new descriptor overlap; no favorable general-input time bound is claimed.

Run this file to execute bounded regression tests. The original source is found
at the repository root, or supplied with --original PATH.
"""
from __future__ import annotations
import importlib.util
import itertools
import json
import random
import signal
import sys
import time
from pathlib import Path
from typing import Optional

_root = Path(__file__).resolve().parents[3]
_original = _root / "experiments/proof_spines/combined_replay_wrapper.py"
if not _original.exists():
    _original = _root / "combined_replay_wrapper.py"
if "--original" in sys.argv:
    _original = Path(sys.argv[sys.argv.index("--original") + 1]).resolve()
_spec = importlib.util.spec_from_file_location("combined_replay_original", _original)
_base = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _base
_spec.loader.exec_module(_base)
State = _base.State

class MeasuredOriginal(_base.ReplaySolver):
    def update_live(self, live_bits, ephemeral_bits=0):
        self.metrics["logical_active_descriptor_and_cache_peak"] = max(
            self.metrics.get("logical_active_descriptor_and_cache_peak", 0),
            live_bits + self.cache_bits)
        super().update_live(live_bits, ephemeral_bits)

class UnitTailReplaySolver(MeasuredOriginal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics["unit_tail_steps"] = 0

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
        while True:
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
                # Do not retain pre-propagation state for delayed caching.
                # Existing bounded cache entries remain separately charged.
                self.update_live(local_live, self.descriptor_bits(state) + 2 * self.n)
                state = (state[0], state[1] | bit,
                         state[2] | bit if unit > 0 else state[2] & ~bit)
                self.metrics["unit_propagations"] += 1
                self.metrics["unit_tail_steps"] += 1
                parent_bits = semantic_bits
                continue

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


def run_tests():
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError("25-second test limit")))
    signal.alarm(25)
    started = time.monotonic()
    rng = random.Random(20261008)
    comparisons = 0
    rows = []
    keys = ("source_passes", "source_literal_reads", "source_clause_accesses",
            "sequential_replay_clause_steps", "max_recursion_depth", "recursive_calls",
            "unit_propagations", "branch_nodes", "and_nodes", "cache_hits",
            "cache_hash_collisions_rejected", "max_cache_descriptor_bits",
            "logical_active_descriptor_and_cache_peak", "max_live_descriptor_bits")

    def check(label, source, n, cap, budget, expected, record=False):
        nonlocal comparisons
        old = MeasuredOriginal(source, n, frontier_cap=cap,
                               cache_budget_bits=budget, digest_bytes=0)
        new = UnitTailReplaySolver(source, n, frontier_cap=cap,
                                  cache_budget_bits=budget, digest_bytes=0)
        a, am = old.solve()
        b, bm = new.solve()
        assert a == b == expected, (label, a, b, expected)
        assert old.cache_bits <= budget and new.cache_bits <= budget
        assert am["sat_oracle_calls"] == bm["sat_oracle_calls"] == 0
        comparisons += 1
        if record:
            rows.append(dict(label=label, n=n, clauses=len(source), frontier_cap=cap,
                             cache_budget_bits=budget, answer=b,
                             original={k: am[k] for k in keys},
                             unit_tail={k: bm[k] for k in keys},
                             unit_tail_steps=bm["unit_tail_steps"]))

    for i in range(240):
        n = rng.randint(1, 7)
        source = tuple(tuple(rng.choice((-1, 1)) * v
                            for v in rng.sample(range(1, n+1), rng.randint(1, min(3, n))))
                       for _ in range(rng.randint(0, 22)))
        expected = _base.truth(source, n)
        for budget in (0, 256):
            check("random_%d" % i, source, n, i % 3, budget, expected)
    for n in (16, 32, 64, 128, 256):
        chain = ((1,),) + tuple((-i, i+1) for i in range(1, n))
        permutation = list(range(1, n+1)); rng.shuffle(permutation)
        permuted = tuple(tuple((1 if v > 0 else -1)*permutation[abs(v)-1]
                               for v in clause) for clause in chain)
        for variant, source in (("forward", chain), ("reverse", tuple(reversed(chain))),
                                ("permuted", permuted)):
            for budget in (0, 512):
                check("chain_"+variant, source, n, 0, budget, True, True)
        check("chain_contradiction", chain+((-n,),), n, 0, 0, False, True)
    # Deliberate repeated components exercise AND, cache sharing, and OR.
    for generator in (_base.repeated_triangle, _base.repeated_dense_sat):
        n, source = generator(3)
        for budget in (0, 1024):
            check(generator.__name__, source, n, 0, budget, True, True)
    signal.alarm(0)
    return dict(status="PASS", seed=20261008, comparisons=comparisons,
                elapsed_seconds=time.monotonic()-started, rows=rows,
                model_note="Logical payload counters, not Python heap/RSS or a complete machine space bound. Old/new state overlap charged as ephemeral payload in unit-tail transitions. Unit predecessors are not saved for cache insertion. Forced digest collisions checked exactly. Inherited recursive size counters denote logical edges including unit-tail transitions.")

if __name__ == "__main__":
    result = run_tests()
    output = Path(__file__).with_name("unit_tail_replay_results.json")
    if "--output" in sys.argv:
        output = Path(sys.argv[sys.argv.index("--output")+1])
    output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}, indent=2))
