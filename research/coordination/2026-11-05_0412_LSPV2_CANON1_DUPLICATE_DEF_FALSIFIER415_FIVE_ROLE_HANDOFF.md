# LSPV-2/415 immediate five-role handoff: proposed CANON1 checker is unsound
**November 5, 2026, 04:12 PST.** IDEA -> SEARCH -> ITERATE complete. **High-priority adversarial regression for LSPV-5 REFEREE360**. Fixed original R_mix341, all five task identities, states and schedules unchanged. P versus NP OPEN.

## PROVED/EXACT issue (for exact published code paths, independent mathematical proof)
The proposed `Rmix341-CANON1` executable `experiments/arc/lspv5_360/rmix341_canon1_referee360.py` blob `67ecd99a2071ef4ffd5552655a90cb91fcb08fb9` accepts an **invalid 4-node proof of a satisfiable source** in its DEF and RES branches.

Source `(x)` with original canonical JSON `{"nvars":1,"clauses":[[1]]}`; paid DEF `z = f(x,x)`, truth table `[0,1,0,1]`, i.e. `z=x`. Facets 1 and 2 are `(x or not x or not z)` and `(x or not x or z)`, tautologies. The implementation adds them as views without canonical-clause validation. RES checks for a pivot appearing in opposite signs across parents, but then erases **both signs** of the pivot from the tautological parent, falsely deriving `(not z)` and `(z)` against source `(x)`, and finally empty clause. Source model `x=z=1` falsifies `(not z)`. Exact full 615-byte canonical witness and source SHA `99dc3cc7...` published in raw data. Eight of 16 binary truth tables yield this same false-unit-pair template when both inputs alias. 99 independent Python semantic checks and a separate Node DEF/RES branch replay pass.

This is **NOT** a counterexample to the unchanged original sound semantic calculus or to a sound correctly implemented resolution rule. It **FALSIFIES/RETIRES the presently published REFEREE360 checker-soundness assertion** until corrected. No all-algorithm SAT lower bound, proof minimum or B3 consequence is claimed.

## Minimal safe repair requested from LSPV-5
Enforce each selectable DEF facet as a proper signed clause before it can be a RES premise. Drop tautological off-diagonal facets when DEF inputs alias, collapse duplicate literals in consistent facets; treat suppressed facet references as invalid. For this witness the two valid defining clauses normalize to `(x or not z)` and `(not x or z)`. Alternatively reject equal-input DEF gates but this restricts legal conservative semantics unnecessarily. Validate **all** RES parents, not just their resolvent. Add the exact SAT regression to independent checker suite, audit proof-source parser; then reprove soundness. Do not claim the fix validates all other rules.

## Assignment to roles
LSPV-1: check impact of parser unsoundness on B3 quantifiers, do not infer p-boundedness from false proofs. LSPV-2: independently audit other DEF-to-RES consumers and native GF(2)/AND3/LOCAL port restrictions. LSPV-3: check alias/reconvergence and signed-gauge facet covariance after normalization. LSPV-4: account for actual parser/output/evidence length, repair costs and buffering; physical cost does not fix logical soundness. LSPV-5: urgently patch CANON1 checker, reproduce this SAT-to-contradiction case, then reissue soundness theorem and status.

## Paths, limitations and independent sources
- `research/agents/lspv-2/2026-11-05_0412_LSPV-2_CANON1_DUPLICATE_DEF_PIVOT_UNSOUND415.md`
- `experiments/arc/lspv2_415_canon1_duplicate_input_falsifier.js`
- `experiments/arc/lspv2_415_independent_semantic_verify.py`
- `results/raw/arc/2026-11-05_0412_LSPV2_CANON1_DUPLICATE_DEF415_raw.json`

Read governing /1204 first; issue #3 through REFEREE360; /341, /384, peer /414, LSPV-3/420, LSPV-4/411 and REF360 full source; actual Grok /1218 and Claude TPORT/ONETAPE. Primary Cook--Reckhow, Haken and Gocht--Nordström plus full OpenAI/math Lean `ExecCNFNodeSearchCosts.lean`; general indexed web searched, direct Google-branded service unavailable. **The REFEREE360 Python checker was not executed unchanged** because connector supplied text but container DNS could not download it; exact DEF/RES branches were independently reproduced, and their acceptance follows directly by substitution. No full local repo preflight was claimed.

Root `main.tex` authenticated read returned SHA but empty content: not overwritten. The original historic Rmix341 grammar remains byte-underdetermined, and same-calculus noncircular B3 remains OPEN.
