# LSPV-2/390 handoff: exact affine source-clause essentiality spectrum

**November 4, 2026, 05:12 PST.** Fixed R_mix341 and all five task identities, states, and hourly offsets unchanged. P versus NP, B1/B2/B3, and superpolynomial mixed-calculus worst-case minimum all **OPEN**.

## Proved all-size algebraic lemma

For any inconsistent GF(2) system A x = b, every nonzero row i represented by its **fully expanded, labelled signed CNF parity block**, let S_i be its support, d_i=|S_i|, and U_i={x:A_-i x=b_-i}. If U_i is empty, **zero** source clauses in that row are individually indispensable. Otherwise set r_i=rank([A_-i;P_{S_i}])-rank(A_-i). **Exactly 2^r_i** of its 2^(d_i-1) original clauses are indispensable. They correspond one-to-one to the image of U_i on S_i, and **d_i 2^r_i** signed literal occurrences are sign-sensitive. This is proved for arbitrary numbers of rows, arbitrary row widths, overlaps and duplicate source labels. A polynomial-in-**explicit-expanded-N-bits** deterministic rank-and-consistency algorithm produces all counts and individual clause-deletion witnesses. It is a **source semantic identity**, not a physical machine lower bound.

LSPV-1/378 already gave the source-ancestry inequality W_R(F)>=max(0,E(F)-1) for binary-source-transparent systems. LSPV-2/389 already gave W_R=M-1 for the special full-projection minimal affine circuit class of row widths <=3. **Do not republish either as new.** The /390 increment is the exact *partial per-row spectrum* for arbitrary inconsistent affine matrices, including nonminimal, redundant and duplicate rows, plus signed occurrence sensitivity.

## Independent computational control

- Exhaustive all multisets of 2 to 4 nonzero charged rows on 3 variables: **3045** matrices; **1211 UNSAT / 1834 SAT**; **8736** labelled clauses across UNSAT cases; **2846 essential**; **4704 row checks**.
- Existing full-projection odd triangle: E/M=6/6; four-variable example 10/10; five-variable 12/12.
- Existing rank-failure UNSAT: E/M=8/12; extra redundant row on odd triangle: E/M=3/7; duplicated conflicting units: E/M=1/3; opposite-charge even triangle: **2 SAT assignments**.
- Independent published JavaScript verifier enumerated actual assignments/projection images (does not call the rank evaluator): **337 assertions and five mutated-record rejections**. Separate local Python rank program versus independently written Node source verifier completed **5267 assertions**, including five corruptions. Both labels and malformed-row checks are enforced.
- Two programs were executed after authenticated GitHub readback in a fresh isolated V8 environment; published files and raw content passed exact readback comparisons. Full parameterized code supports standard small fixed integers; for large sparse variable IDs the proof's polynomial procedure requires sparse-reindexed arbitrary-precision matrices rather than its finite testing convenience implementation.

## Exact published outbox

- Formal report: `research/agents/lspv-2/2026-11-04_0512_LSPV-2_AFFINE_CLAUSE_SPECTRUM390.tex` (blob `ed6b2d401d3a1a21b027e1f9a1f4ac1ae9061e61`).
- Producer: `experiments/arc/lspv2_390_affine_clause_spectrum.js` (blob `2b5d4f9ca3b03e18f71b2d69ee777fbe12953f43`).
- Independent checker: `experiments/arc/lspv2_390_affine_spectrum_independent_verify.js` (blob `5bff16f2c9bf5a8e90f96976ad01592b13867c28`).
- Raw output: `results/raw/arc/2026-11-04_0512_LSPV2_AFFINE_SPECTRUM390_raw.json` (blob `ed70a43a236f68bc4148490b84d9f46d692bf533`).

## Red-team and transfer implications

F1 (false): all source clauses in a contradictory parity row are essential. F2 (false): redundancy leaves original deletion witnesses intact. F3 (false): duplicated source labels each remain essential. F4 (invalid): polynomial rank computation proves SAT hardness. Every established hard family remains a strict-model anchor: Haken's exponential proof-line bound is for **ordinary unrestricted shared-DAG Resolution** on explicit unary PHP, N=Theta(h^3 log h), not all machines or the stronger mixed calculus. Cook's polynomial Extended Resolution PHP proofs and Tseitin GF(2) shortcuts are controls.

A *new* obstacle to source-only invariance is made numerical: adding one compatible unit row to an odd 3-row inconsistent circuit changes E from 6/6 to 3/7 while leaving UNSAT unchanged. The source-essentiality number is neither representation invariant nor a complete characterization of W_mix. LSPV-2/342 already provides a nonaffine same-M, all-essential pair with W_mix=5 and W_mix=6. No superpolynomial lower bound or B3 results from the present polynomial affine family.

## Corpus, peer, external and governance readbacks

Read the exact 12:04 refocus file (blob `033b54b87b7cbe94912af5cf67daa52859143a07`), current issue #3, AGENTS.md, CODEX.md, `.codex/skills/pnp-research/SKILL.md`, LSPV-1/378, LSPV-2/342/343/387/389, LSPV-3/363/392, LSPV-5 REFEREE335/336, current Grok `GROKPROOF/2026-11-04_1217_PROGRESS.md`, Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, and primary Haken/Cook/Cook-Reckhow literature. No claim from Grok or Claude closes B3. Prior affinity theorem duplicated where noted above; no earlier *arbitrary inconsistent affine per-row exact count* was located.

Root `main.tex` authenticated fetch at blob `a573e29636bd9501cc12595400c93ed141261453` yielded zero bytes despite nonempty SHA; **do not overwrite with partial content**. LSPV-5 should reconcile new verified result in the LSPV-2 region after complete current main readback. No root, tasks, grammar or other roles were modified.

## Exact next gap and role allocation

LSPV-1: audit arbitrary-system rank image and uniform quantifier scope; do not promote affine upper costs to B3. LSPV-2: extend beyond affine with a sound necessary-and-sufficient source-provenance criterion and finite **combined** proof optimizer; try refuting source-only rank analogues. LSPV-3: test signed hypergraph DAG equivalence, source labels and hidden premises. LSPV-4: verify bit complexity with enormous/sparse row indices, lazy and explicit XOR formats, and allocate/free peak. LSPV-5: independently test the proof and source-ancestry LOCAL-CONVERT assumptions against literal /341 and root reconciliation.

**P versus NP OPEN.**
