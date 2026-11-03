# LSPV-1 MASKED-OR-REFLECTION-REPLAY356 | November 3, 2026 00:04 PST

**PROVED/EXACT (RES+source-independent VARDEF theorem), COMPUTATIONAL (finite full certificates), CONDITIONAL (previous one-family reflection comparison), OPEN B1/B2/B3 and P versus NP.**

Research progress beyond LSPV-1 354: An arbitrary-width signed masked OR, using m gate slots and k active distinct literal positions, can be derived from the authentic original proper source clause in at most m*k+5*m+5 paid Rmix341 RES+VARDEF nodes, including all selector pins, inactive positions, exact gate slots and proof pivots. No free weakening or unknown semantic SAT oracle. The theorem assumes at least two declared input variable positions for the existing paid false-wire gadget; fewer-variable UNSAT originals have direct constant-cost refutations. The program handles all widths 2..8, five sparse signed masks including singleton and negative occurrence signs, and the complete 2-label toy.

**New end-to-end finite reflection copy:** The fixed universal toy source has 12 gate-defining clauses plus output pins (e,h), and an authentic 9-RES refutation. From true UNSAT original F-=(w OR z)&(!w)&(!z), a charged source compiler derives the signed gate slots and two pins, then copies every original universal RES pivot *without mixed-rule restriction*. The final original-source certificate costs 8 DEF+20 RES=28. The direct original RES proof costs 2, so 28 is an upper certificate, NOT a minimum. SAT sibling F+=(w OR z)&(!w) derives h but not the rejecting pin; witness (w=0,z=1) prevents a false refutation. The complete universal-9-line signed mapping, all 12 defining slots and two output pins were independently checked.

**Finite reproduction:** Local deterministic Python producer + independent no-import Node checked 15 full source/DAG objects, 22,302 assertions, 90 corrupted certificates, six malformed proof objects. Full signed certificate JSON 241,696 bytes; SHA256 021a037bcafc6ff71e1625353fa5960ad84f5e8f319a4acea8beaf88f8369132. Full host scripts and proof JSON packaged in user-facing archive. GitHub public compact JS builds a distinct, sometimes more expensive masked-OR proof for the all-on cases, so its counts for all-on widths are not claimed equal to the optimized local all-on producer; sparse mask counts agree. The GitHub public JSON is a summary, not a full independent replay.

**Additional malformed original-source controls:** A separately written strict signed-DIMACS checker accepted four valid SAT/UNSAT/empty-CNF test inputs and rejected 16 malformed signed-DIMACS strings, independently of the six malformed proof-object controls. Public checker: experiments/arc/lspv1_356_signed_dimacs_grammar_controls.js. This is grammar validation for a canonical subset, not a complete general-source parser theorem.

**Ownership assignments, no task edits:**
- LSPV-1: maintain Wbar quantifiers and B3 as primary. Next test the full A-circuit reflection family including valid/malformed masks and explicit paid rejecting output, without confusing correct A externally with a formal proof of its soundness.
- LSPV-2: independently reconstruct m-slot signed compiler including inactive slots, source clause width 1, gate freshness and duplicate/tautology normalization. Audit whether declaring unused input variables is accepted by unchanged VARDEF checker; if not, use direct small-support branch.
- LSPV-3: focus nonaffine MUS with no mixed shortcut; attempt superpolynomial source-cycle excess over all legal Rmix nodes and cautious hardness transport.
- LSPV-4: verify proof-node vs evidence-bit polynomial domination and native all-phase costs; reject artificial constant wire as zero-cost machine step.
- LSPV-5: independently test the 9-line signed universal copy, the SAT original, invalid selectors, false-wire soundness, malformed source and corrupted gates; distinguish ER2-only replay from arbitrary mixed proof specialization.

**Exact missing implication:** For some hypothetically correct fixed polynomial general SAT decider A, show the associated uniformly generated universal reflection H_{A,N} admits polynomial ER2 proofs. Neither SAT in P alone nor the finite toy currently establishes this. The prior LSPV-1 354 conditional inequality Wbar_Rmix341(N) <= W_ER2(H_{A,N})+poly(N) is adopted, NOT relabelled a proof of B3.

Paths:
- research/agents/lspv-1/2026-11-03_0004_LSPV-1_MASKED_OR_REFLECTION_REPLAY356.tex
- experiments/arc/lspv1_356_masked_or_compact.js
- results/raw/arc/2026-11-03_0004_LSPV1_MASKED_OR_REFLECTION_REPLAY356_public.json
- local archive contains original full Python producer, independent Node verifier and 15 full proof DAGs.

Keep Rmix341 unchanged, role IDs/titles/states/schedules untouched, preserve all main.tex data outside LSPV-1 ownership markers. P versus NP OPEN.
