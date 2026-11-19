# Native strict-C 150/176 girth-10 source: clause-core extraction, partial (checkpointed)

2026-11-19 ~05:50-06:55 PST, scheduled hourly routine (generic SAT-lower-bound prompt; additive report, no peer manuscript edited). **P vs NP remains OPEN.** Independent review: NONE.

## Named dependency advanced

The OPEN blocker from `2026-11-19_UNIVERSAL_3FOLD_SAT_COVER.md` and `research/coordination/2026-11-19_CRITICAL_UNIVERSAL3_COVER_HANDOFF.md`: obtain a clause-minimal UNSAT core of the seed-20 native strict-C 150/176 incidence-girth-10 source, with a replayable static UNSAT certificate and an original-C witness for every single-clause deletion. Integration point: this gives the high-girth critical UNSAT source that any cover/lift or row-block construction has to start from. This run does **not** close the blocker. It measures how expensive the blocker is and publishes a resumable extractor.

Candidate: the source contains a clause-minimal UNSAT core (trivially it does), and that core can be extracted and statically certified within ordinary per-stage budgets. Falsifiers: (i) a SAT assignment of the full source, which would contradict the prior two-solver UNSAT; (ii) single-clause deletions that are UNSAT, showing the source is far from critical; (iii) per-call UNSAT cost far above the 30 s stage budget, which would make deletion-MUS extraction infeasible under this protocol.

## Results

**PROVED (finite, exhaustive over 125 tuples, executed as asserts in the code).** The original predicate C(x,y,z) holds iff {x,y,z} = {a,a+1,a+2} mod 5 for some a. So C is fully symmetric under permuting its positions, and it is invariant under x -> x+t and x -> -x (dihedral D5). As a result, fixing any one variable to 0 preserves satisfiability for **every** subset of clauses. This justifies the symmetry break used in all solver calls below.

**COMPUTATIONAL (source pin).** The regenerator reproduces SHA256 `ecb0b31b1487f8747b582d97de26e2c77e4e1b5e173d89c4c86097e0fcd402a8` exactly. Variable degree histogram: {2:19, 3:64, 4:43, 5:18, 6:6}.

**COMPUTATIONAL, single solver (CaDiCaL 1.5.3 via pysat 1.9.dev24); no proof was emitted or checked.**
- Full source UNSAT. It took 29.9 s with variable 0 pinned (467,398 conflicts). With selector literals and no direct CNF it took 83.4 s, and the failed-assumption core CaDiCaL returned was all 176 clauses, so no core reduction came for free.
- Single deletions of clause 0, 5 and 100 are each still UNSAT, at 36.9 s, 54.5 s and 66.4 s. This agrees with the prior note that clause 0 is redundant, and it suggests the source is far from clause-critical.
- Adaptive chunk-deletion (dichotomic) MUS, 10 calls, state in `results/raw/strict_c_girth10_core/chunk_state.json`:
  - Removing clauses 0..15 gives UNSAT (259.1 s). Removing 0..21 in total gives UNSAT (245.4 s, then 256.4 s). The current UNSAT set has **154** clauses (176 minus {0..21}).
  - Every subset that was also missing a chunk containing 22 and 23 came back SAT in 0.0-8.4 s. The last call removed {22,23} from the 154-set: SAT in 7.9 s. So at least one of clauses 22 and 23 is necessary in the 154-set.
  - Asymmetry: SAT calls take 0-8 s, while each UNSAT call on a 150-160 clause subset takes about 250 s. The roughly 30 s stage guideline was **exceeded**; this is disclosed here. A complete deletion MUS needs one UNSAT call for every redundant clause it removes. At an estimated tens of redundant clauses, that is several hours of single-solver time, before any DRAT proof is emitted or checked.
- Local-search control (seeded tabu/min-conflicts, `experiments/strict_c_girth10_onefalse_search.py`, seed 1, 25 s, 573,007 steps). The best assignment still violated 7 clauses, and no assignment violating exactly one clause was found. Its raw output was not retained because it has no evidential value: local search failing is not a lower bound. Together with the CDCL results above, it suggests the source is heavily over-constrained.

**OPEN.** The MUS itself, a static DRAT/DRUP certificate checked by drat-trim (built locally from commit 2e3b2dc0ecf938addbd779d42877b6ed69d9a985; **not run** on any proof this run), a second-solver confirmation of the 154-clause UNSAT set, and all deletion witnesses.

## Resource ledger (same realization, this machine)

Indexed-RAM costs: source regeneration O(TRIALS) about 4,500 samples. CNF of 750 one-hot variables, 1,650 domain clauses and 95 x m rejected-tuple 3-clauses (16,720 for m = 176). Each UNSAT certificate costs about 0.47-0.5 M conflicts, or about 250 s on 154-160 clause subsets. Total solver time spent this run: about 1,400 s. No caching across calls: each chunk call is a fresh process. Retained learnt clauses between calls are a possible speed-up, but they were not used because they complicate an auditable stage.

## Gates

- DISJ sanity: NOT APPLICABLE (a finite certificate-acquisition audit, not a lower-bound claim).
- Relativization: NOT APPLICABLE, same reason.
- Simultaneous DTISP: NOT APPLICABLE; no asymptotic claim.
- Deterministic-configuration counting: NOT APPLICABLE.
- No unrestricted runtime claim. Measured CDCL cost on one finite instance is COMPUTATIONAL only. It is not a resolution or proof-system lower bound for the family, and it is not a time lower bound for SAT.

## External idea survey (this routine's standing request)

- The user's Google Doc "P vs. NP Proof Attempts" (all 62,596 characters read) surveys holographic/matchgate collapse, tensor-network contraction, IPS synthesis, GCT occurrence obstructions, IPS functional lower bounds and hardness magnification, each with its known barrier. It maps onto existing repository controls (algebrization, Natural Proofs, the locality barrier) and contains no new load-bearing lemma for the strict-C pipeline.
- `openai/ten-proofs` (HEAD 94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6) includes `Permanent.lean`, a Lean formalization of arithmetic circuit and formula lower bounds for the permanent over C (including n^4/log n for formulas). It is an algebraic-model result and does not transfer to Boolean SAT time. It is a possible source-verification target for TMR-1 Track C (formalized-statement audit), but the kernel build was **not** run here.
- `google-deepmind/formal-conjectures` and `google-deepmind/alphaproof-nexus-results`: listed only, not inspected.

## Reproduce / resume

```
python3.13 -I experiments/strict_c_girth10_core_mus.py chunk 16   # repeat; resumes chunk_state.json
python3.13 -I experiments/strict_c_girth10_core_mus.py finalize   # after MUS completes (uses step-state format)
```

Note: `finalize` and `proof` currently read the selector-mode `mus_state.json` format. Before use with chunk mode they need a small adapter (OPEN, trivial). Code SHA256: core_mus `4f0ddedf77fbc31b12d97193de5f3004be1baf383913009072f924a411803cdd`, onefalse `ede015de6493cc1070f5c29f27c5261d3d75bb84dd4a122b3f6a35e27bf3b266`. Raw: chunk_state `5834c79f0c83e3fc8c2500b8494cab16d77ed51025d7eb97ccc3735d0161af3e`, mus_state (first selector solve only) `7336c535fde9e3d46c29d4168f808f7af8cb9be98d1f8fc1db46e40482bdb560`.

## Next load-bearing lemma

Find a cheaper route to criticality than deletion-MUS on the 150/176 source. Either (a) build a girth-10 strict-C source that is critical by construction (for example a near-threshold generator stopped at the first UNSAT clause addition, so the last clause is necessary, then shrink), or (b) emit one CaDiCaL DRAT proof for the 154-clause set and use the clauses its proof actually uses (drat-trim core output) as a much smaller next candidate. Then check deletion witnesses, which come from the fast SAT calls.
