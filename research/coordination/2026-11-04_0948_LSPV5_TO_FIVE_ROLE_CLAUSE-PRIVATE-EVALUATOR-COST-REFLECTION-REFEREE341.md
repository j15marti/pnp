# REFEREE341 five-role handoff: clause-private evaluator cost reflection

**Task:** PNP Independent Proof Red Team `6ad42a2a9a088191ab9042245f3b4393`  
**Time:** November 4, 2026, 09:48 PST  
**Fixed calculus:** unchanged `R_mix341`; no task/schedule/state/rule changes.

## Proved restricted theorem

For a normalized nonempty CNF `F` with no empty clause and total literal count `L`, let `T(F)` be the private binary-OR-per-clause / binary-AND-over-clauses evaluator, with all complete gate definition clauses and positive root unit. Under the documented charged DEF-facet semantics,

\[
W_{R_{\mathrm{mix341}}}(F)
\le W_{R_{\mathrm{mix341}}}(T(F))+3(L-1).
\]

The source-to-root macro has `L-1` paid DEF nodes and `2(L-1)` paid RES nodes. It is a construction upper bound, not a minimum. For any full mixed proof of exact `T(F)`, replace its free gate-clause leaves by the corresponding charged DEF slots and its root source by the derived root; alpha-rename proof-owned gates; replay all downstream typed nodes unchanged.

This is a representation-specific D4/cost-reflection result, not representation independence. It does not specialize a universal indexed evaluator to `T(F)` and does not prove reflection shortness, B1/B2/B3 or P != NP.

## Duplicate/new audit

- Duplicate components: REFEREE284 `L-1` private gate count; LSPV-4/376 `L-1` DEF plus `2(L-1)` RES root forcing; LSPV-1/354, /356, /361 conditional replay framework.
- Surviving increment: explicit arbitrary-downstream `R_mix341` cost-reflection inequality for exact `T(F)` and charged source-leaf substitution.
- Physical correction: a width-`k` clause emits `k^2-1` explicit replay-conclusion literal occurrences. Linear nodes can serialize quadratically. Instruction-only encoding shifts work to checker reconstruction.

## Verification

- Python: 262 signed polarity/AND-chain records, one complete 34-node UNSAT splice, SAT control, five malformed rejects.
- Independent JavaScript: 94 record checks PASS.
- Raw SHA-256: `d72bd34cbfec0bb347ad3b100b4b34564bf5ead9a19f79a30fec8d1b16f6e730`.

Artifacts:

- `research/main/2026-11-04_0948_MAIN_CLAUSE-PRIVATE-EVALUATOR-COST-REFLECTION-REFEREE341.md`
- `experiments/arc/lspv5_341/evaluator_cost_reflection_referee341.py`
- `experiments/arc/lspv5_341/verify_evaluator_cost_reflection_referee341.js`
- `results/raw/arc/lspv5_341/evaluator_cost_reflection_referee341.json`

## Role allocation

- **LSPV-1:** formulate the weakest uniform normalization premise from the all-length indexed evaluator to exact `T(F)`; keep B1/B2/B3 quantifiers distinct.
- **LSPV-2:** type constants/aliases/multiplexers under the unchanged DEF grammar; retain GF(2) and compact-circuit counterexamples.
- **LSPV-3:** audit whether every universal-evaluator source leaf has a polynomial authenticated replacement; distinguish exact facet identity from semantic equivalence.
- **LSPV-4:** charge the `sum k_i^2` explicit clause payload, lazy reconstruction, proof-ID maps, checking, output and peak space.
- **LSPV-5:** seek a uniform indexed evaluator whose specialization defeats polynomial normalization without smuggling an answer oracle; attack any claimed all-rule source retraction.

Latest reviewed external assessments: `GROKPROOF/2026-11-04_1518_PROGRESS.md` blob `4e2bb9d...`; Claude WORLD-LEDGER `79e4d4e7...`, DIRECTPRODUCT `95c2649b...`, TPORT `1f9fc727...`, ONETAPE `9a5b05d6...`. None closes normalization, reflection shortness or B3.
