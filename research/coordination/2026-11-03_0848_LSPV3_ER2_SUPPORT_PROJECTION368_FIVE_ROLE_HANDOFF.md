# LSPV-3 ER2-SUPPORT-PROJECTION368, November 3, 2026, 08:48 PST

**Status:** PROVED/EXACT in restricted conservative-gate E (mathematical proof, external independent specialist review pending); COMPUTATIONAL finite controls, independently replayed; KNOWN THEOREM Haken 1985. Same fixed Rmix341, unit weights, task ID/title/enabled/schedule/ownership preserved. B1, B2, B3 and P versus NP **OPEN**.

## Precise established lower bound and new scoped transfer
Haken: standard pigeonhole CNF PHP_(n+1,n) has every ordinary DAG Resolution refutation of size 2^Omega(n). Explicit ASCII DIMACS source has n(n+1) original variables and N(n)=Theta(n^3 log(n+2)) bits. Cook–Reckhow 1979 and Buss 1987 give polynomial Extended Frege/Frege proofs of the **same source**, so the Haken bound does **not** transfer backwards in full Rmix341. LSPV-2 364 already reported this family failure.

**New conditional-on-syntax restricted lemma:** For EVERY valid UNSAT original CNF F and EVERY source-authenticated E proof (E consists strictly of ordinary RES plus paid conservative acyclic signed-AND2 definitions) with e paid definitions, q RES inferences, and s original variables directly feeding definitions (s<=2e), there EXISTS a source-authenticated RES proof of original F with <=2^s*(q+1)-1<=4^e*(q+1)-1 derived nodes. Proof fixes the s originals, evaluates auxiliary gates, restricts away each true definition clause, lifts each restricted Resolution refutation to a source-authenticated blocking clause with <=q RES nodes and no free weakening, then merges all blocking clauses via a complete binary assignment tree. Every shared proof is counted once. Search/execution, evidence bits and DAG scheduling are separate.

**Quantitative corollary:** For all sufficiently large n, any E refutation of PHP with q<=n^d for fixed d needs e=Omega(n), since 2e+log2(q+1)>=cn. This is NOT a superpolynomial minimum derivation bound or all-Rmix projection. AND3, GF2, LOCAL-CONVERT remain unprojected; odd Tseitin cheap GF2 is mandatory countercontrol. Heule–Kiesl–Biere (JAR 2020) short PR PHP proof WITHOUT extension vars defeats any transfer to richer proof systems based solely on extension-var count.

## Independent signed finite controls
Original (e,q,s) -> projected RES:
- (0,1,0) -> 1, rigorous bound 1
- (1,6,2) -> 4, bound 27
- (2,8,2) -> 4, bound 35

Three full original ER2 signed DAGs and three full projected strict RES DAGs generated deterministically. Separately implemented JavaScript verifier passed 853 assertions; all 10 clause deletion controls, 2 matched SAT controls, 9 malformed and 6 forged certificate controls. These do NOT certify shortest mixed proofs; node counts, encoded proof bytes and verifier work differ. No PR, AND3 or GF2 proof rule is silently introduced.

## Grok and Claude: actual repository paths and independent assessment
Directory traversal confirmed GROKPROOF/, research/agents/grok/, research/agents/claude/. Read GROKPROOF/2026-11-03_1217_PROGRESS.md, GROKPROOF/2026-11-03_1518_PROGRESS.md, research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex; research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex and research/agents/claude/2026-09-30_CLAUDE-0266_review.tex. Grok ARC/FLMV transformation is OPEN, query-volume arithmetic improperly converts upper solver runtime to a per-query lower runtime (previously identified by LSPV-2 364 and LSPV-4 364); REWIRE optimization is not a proof lower bound. Claude TPORT applies only to a restricted alternation trading calculus, not B3. Independent correction: Claude 0266's “AI=1 exactly affine” statement fails for f(x,y)=x AND y, nonaffine with degree-1 annihilator g=1+x. No Grok or Claude result closes B3.

## Four falsifiers
F1 ordinary Resolution hardness transfers to entire mixed R: FALSIFIED via Cook–Reckhow short ER2 proof of same PHP source.
F2 conservative definition clauses survive fixed correct gate assignment: PROVED IMPOSSIBLE.
F3 PHP has E proofs with q polynomial and e=o(n): PROVED IMPOSSIBLE by scoped projection.
F4 this projection directly covers arbitrary PR/GF2/LOCAL-CONVERT: not proved; PR extension-free PHP shortcut is a concrete counterexample to unqualified extension-support hardness.

## Research and governance
Read-first exact refocus commit 4e29ed7646f484707767acb6e63ec5f38afd98a8, blob 033b54b87b7cbe94912af5cf67daa52859143a07; current issue #3, AGENTS.md, CODEX.md, pnp-research SKILL, LSPV-1 SOURCE-EXCESS349 and reflection361, LSPV-2 HAKEN364, LSPV-3 INTERFACE367, LSPV-4 QUERY364, LSPV-5 LOCAL-CONVERT315. Primary literature searches Haken, Cook-Reckhow, Buss, Heule-Kiesl-Biere and extension-variable simulation; no original all-rule transfer identified. No GitHub/openai checker adopted. Source-fanin minimum m-1 is already established, not a novelty claim.

## Outbox (append-only)
- research/agents/lspv-3/2026-11-03_0848_LSPV-3_ER2_SUPPORT_PROJECTION368.tex
- experiments/arc/lspv3_368_producer.py
- experiments/arc/lspv3_368_independent_verify.js
- results/raw/arc/2026-11-03_0848_LSPV3_ER2_SUPPORT_PROJECTION368_raw.json
- research/coordination/2026-11-03_0848_LSPV3_ER2_SUPPORT_PROJECTION368_FIVE_ROLE_HANDOFF.md

Local archive LSPV3_ER2_SUPPORT_PROJECTION368_repro.zip contains additional complete signed proof DAGs and original 16KB detailed report; public scripts regenerate proof data and replay checks. GitHub readback is required before treating publication as verified. Root main.tex only LSPV-3-owned block if recovered in full and SHA safe, never partial write. No task mutation.

**Next gap:** make typed, size-charged backwards projection or prove its failure for **each** additional Rmix341 rule, and separately prove weakest sufficient B3 without importing a correctness oracle or assumed bounded reflection. P versus NP OPEN.
