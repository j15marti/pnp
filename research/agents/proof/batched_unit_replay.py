#!/usr/bin/env python3
"""BATCHED-UNIT-REPLAY1: dynamic source-major forced-assignment sweeps.

Frontier is attempted before entering unit propagation. Once a unit is known,
sweeps apply newly forced literals immediately, until a no-change pass or
conflict. No intermediate state cache insertion, occurrence index, residual
CNF, or unit queue. Inherited AND/OR and bounded exact cache are unchanged.
Counters describe logical payloads, not Python heap/RSS or full machine bounds.
Selected-clause reads use source random access; inherited index charge remains.
The separate sequential replay counter charges locating scopes, not a complete
sequential literal-read simulation. Proper clauses are the intended domain.
Inherited recursive-size counters compare batch endpoints, not every forced
assignment; unit_tail_steps counts the individual assignments inside a sweep.
"""
from __future__ import annotations
import itertools
import json
import random
import signal
import sys
import time
from pathlib import Path
from typing import Optional
from unit_tail_replay import UnitTailReplaySolver, State, _base

class BatchedUnitReplaySolver(UnitTailReplaySolver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("unit_sweep_passes", "unit_sweep_literal_reads",
                     "unit_sweep_clause_accesses", "unit_sweep_assignments",
                     "unit_sweep_conflicts", "unit_sweep_mask_scratch_peak_bits",
                     "unit_sweep_clause_scratch_peak_bits"):
            self.metrics[name] = 0

    def propagate_sweeps(self, state, ancestor_live_bits):
        scope, mask, values = state
        # Caller retains its old state while this routine runs. Charge that
        # descriptor plus new masks and intermediate bitwise values. Scope is
        # shared, not copied. Scratch allowances are conservative logical bits.
        old_descriptor = self.descriptor_bits(state)
        mask_scratch = 8 * max(1, self.n)
        clause_scratch = 4 * self.variable_width + 2 * self.clause_index_width + 8
        self.metrics["unit_sweep_mask_scratch_peak_bits"] = max(
            self.metrics["unit_sweep_mask_scratch_peak_bits"], mask_scratch)
        self.metrics["unit_sweep_clause_scratch_peak_bits"] = max(
            self.metrics["unit_sweep_clause_scratch_peak_bits"], clause_scratch)
        self.update_live(ancestor_live_bits + old_descriptor,
                         mask_scratch + clause_scratch)
        while True:
            changed = False
            self.metrics["unit_sweep_passes"] += 1
            self.metrics["source_passes"] += 1
            self.metrics["sequential_replay_clause_steps"] += self.m
            for clause_id in self.scope_ids(scope):
                clause = self.source[clause_id]
                self.metrics["source_clause_accesses"] += 1
                self.metrics["unit_sweep_clause_accesses"] += 1
                remaining = 0
                last = 0
                satisfied = False
                for literal in clause:
                    self.metrics["source_literal_reads"] += 1
                    self.metrics["unit_sweep_literal_reads"] += 1
                    bit = 1 << (abs(literal) - 1)
                    if mask & bit:
                        if bool(values & bit) == (literal > 0):
                            satisfied = True
                            break
                    else:
                        remaining = min(2, remaining + 1)
                        last = literal
                if satisfied:
                    continue
                if remaining == 0:
                    self.metrics["unit_sweep_conflicts"] += 1
                    return (scope, mask, values), True
                if remaining == 1:
                    bit = 1 << (abs(last) - 1)
                    mask |= bit
                    values = values | bit if last > 0 else values & ~bit
                    changed = True
                    self.metrics["unit_propagations"] += 1
                    self.metrics["unit_tail_steps"] += 1
                    self.metrics["unit_sweep_assignments"] += 1
            if not changed:
                return (scope, mask, values), False

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
                self.update_live(local_live, self.descriptor_bits(state) + 2 * self.n)
                state, conflict = self.propagate_sweeps(state, live_bits)
                parent_bits = semantic_bits
                if conflict:
                    self.cache_insert(state, False, live_bits + self.descriptor_bits(state))
                    return False
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
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('25-second limit')))
    signal.alarm(25)
    start = time.monotonic()
    rng = random.Random(20261008)
    checks = 0
    rows = []
    collisions = 0
    keys = ('source_passes', 'source_literal_reads', 'source_clause_accesses',
            'sequential_replay_clause_steps', 'max_recursion_depth', 'recursive_calls',
            'unit_propagations', 'branch_nodes', 'and_nodes', 'cache_hits',
            'cache_hash_collisions_rejected', 'max_cache_descriptor_bits',
            'logical_active_descriptor_and_cache_peak', 'max_live_descriptor_bits')
    def check(label, source, n, cap, budget, expected, record=False):
        nonlocal checks, collisions
        old = UnitTailReplaySolver(source, n, frontier_cap=cap, cache_budget_bits=budget, digest_bytes=0)
        new = BatchedUnitReplaySolver(source, n, frontier_cap=cap, cache_budget_bits=budget, digest_bytes=0)
        a, am = old.solve(); b, bm = new.solve()
        assert a == b == expected, (label, a, b, expected)
        assert old.cache_bits <= budget and new.cache_bits <= budget
        assert bm['sat_oracle_calls'] == 0
        assert bm['retained_residual_formulas'] == bm['retained_formula_dag_nodes'] == 0
        collisions += bm['cache_hash_collisions_rejected']
        checks += 1
        if record:
            rows.append(dict(label=label, n=n, clauses=len(source), cap=cap, budget=budget,
                             answer=b, unit_tail={k:am[k] for k in keys},
                             batched={k:bm[k] for k in keys},
                             sweep={k:v for k,v in bm.items() if k.startswith('unit_sweep')}))
    # All subsets of <=3 proper clauses on three variables.
    clauses = []
    for width in range(1,4):
        for variables in itertools.combinations(range(1,4),width):
            for signs in itertools.product((-1,1),repeat=width):
                clauses.append(tuple(v*s for v,s in zip(variables,signs)))
    for k in range(4):
        for source in itertools.combinations(clauses,k):
            check('exhaustive',source,3,0,0,_base.truth(source,3))
    exhaustive = checks
    for i in range(240):
        n=rng.randint(1,7)
        source=tuple(tuple(rng.choice((-1,1))*v for v in rng.sample(range(1,n+1),rng.randint(1,min(n,3)))) for _ in range(rng.randint(0,22)))
        answer=_base.truth(source,n)
        for budget in (0,256): check('random',source,n,i%3,budget,answer)
    for n in (16,32,64,128,256):
        chain=((1,),)+tuple((-i,i+1) for i in range(1,n))
        shuffled=list(chain); rng.shuffle(shuffled)
        for name,source in (('forward',chain),('reverse',tuple(reversed(chain))),('shuffled',tuple(shuffled))):
            for budget in (0,512): check('chain_'+name,source,n,0,budget,True,True)
        check('chain_conflict',chain+((-n,),),n,0,0,False,True)
    for generator in (_base.repeated_triangle,_base.repeated_dense_sat):
        n,source=generator(3)
        for budget in (0,1024): check(generator.__name__,source,n,0,budget,True,True)
    # Explicit scope test excludes a contradictory source clause.
    scoped=BatchedUnitReplaySolver(((1,),(-1,),(-1,2),(-2,3)),3,frontier_cap=0,cache_budget_bits=0)
    st,bad=scoped.propagate_sweeps(((0,2,3),0,0),0)
    assert not bad and st[1]==st[2]==7
    assert scoped.metrics['unit_sweep_clause_accesses']==6
    # Conflict reached only on a subsequent source pass.
    scoped2=BatchedUnitReplaySolver(((-2,),(-1,2),(1,)),2,frontier_cap=0,cache_budget_bits=0)
    _,bad=scoped2.propagate_sweeps((None,0,0),0)
    assert bad
    signal.alarm(0)
    return dict(status='PASS',seed=20261008,formula_comparisons=checks,
                exhaustive_formulas=exhaustive,scope_and_conflict_checks=2,
                rejected_collision_candidates=collisions,
                elapsed_seconds=time.monotonic()-start,rows=rows,
                note='Logical payloads, not RSS or complete machine bounds. Dynamic sweep reads counted; random-access source index remains separately charged. No favorable all-input time-space theorem. Source clause order may require linearly many sweeps. Frontier-first ordering is retained before entering propagation; frontier is not retried between individual forced literals.')

if __name__=='__main__':
    result=run_tests()
    output=Path(__file__).with_name('batched_unit_replay_results.json')
    if '--output' in sys.argv: output=Path(sys.argv[sys.argv.index('--output')+1])
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
