# TASK-008: TWOSATDEC-WIDTH1 — the exact-layer depth-r series is degenerate at t=3.5q and falsified at every constant UNSAT density

P versus NP remains OPEN. No monotone-circuit or general SAT lower bound is claimed. This note concerns only the restricted procedure "depth-r decision + unit propagation + free exact 2-SAT" tested by TWOSATDEC6..96.

## Preflight

HEAD at start `cc43d05a` (TWOSATDEC96, q=101 empty draw). TWOSATDEC86..96 are eleven consecutive empty draws (`SAT 16 / UNSAT 0`). `research/explorations/monotone-slice/2026-10-05_1011_DIRECTIONALTELESCOPE1.tex` and `tasks/TASK-008_SLICE-UNSAT.md` are absent from every ref (`git log --all` finds no commit touching them), so the exact text of SAT-LOCAL-ERROR1 is NOT recoverable here. This note therefore targets the claim the series itself names in every Box: that "decision depth stays bounded on the exact layer", i.e.

**Candidate B-DEPTH (tested here).** There are fixed r and constant density Delta such that, for uniform exact-layer formulas with t = floor(Delta q) clauses, depth-r free-2-SAT certificates capture a fraction of UNSAT formulas bounded away from 0 as q -> infinity.

Falsifiers stated before work: (F1) at the protocol density Delta=3.5 the UNSAT conditioning event has probability -> 0, so the residual is undefined asymptotically; (F2) a depth-r certificate yields a bounded-width resolution refutation, so a known random-3-CNF width lower bound forces r = Omega(q); (F3) finite minimal certifying depth r* grows with q at a fixed density above threshold.

Also reviewed per the routine prompt: the linked Google Doc "P vs. NP Proof Attempts" (read completely, 62.6k chars; six trajectories IA–IIC: holographic/matchgate, tensor-network contraction, IPS synthesis, GCT occurrence obstructions, IPS functional lower bounds, hardness magnification/locality barrier). Its Reciprocal Barrier theme — each failed algorithm is a restricted lower bound — applies directly: the depth-r procedure is a sub-system of bounded-width resolution, and its failure is the Ben-Sasson–Wigderson width bound. GitHub search of `org:openai` and `org:google-deepmind`/`org:google` (repository search, default branch) surfaced only `openai/ten-proofs` (Lean certificates) and `google-deepmind/formal-conjectures` (Lean conjecture statements); neither contains a SAT-slice, 2-SAT decision-depth or resolution-width result relevant here. Not read beyond descriptions.

## Lemma W (PROVED/EXACT, elementary; not independently reviewed)

If a set S of r variables certifies an unsatisfiable 3-CNF F in the TWOSATDEC sense, then F has a resolution refutation of width at most r+3.

Proof. Fix rho in {0,1}^S. Unit propagation on F|rho is a sequence of resolutions of a unit with a clause of width <= 3, so every derived clause has width <= 3. If it derives the empty clause, F|rho has a width-3 refutation. Otherwise the residual width-<=2 skeleton is unsatisfiable; resolution restricted to width-<=2 clauses is closed (two 2-clauses resolve to width <= 2) and complete for 2-CNF, so F|rho again has a width-3 refutation (input clauses of width 3 included). By the standard restriction lemma (Ben-Sasson–Wigderson 2001, Lemma 3.2 style: a width-w refutation of F|_{x=a} lifts to a width-(w+1) derivation from F of the literal falsified by x=a, applied r times), F derives the clause C_rho falsified exactly by rho in width <= r+3. The 2^r clauses C_rho resolve along the complete decision tree on S in width <= r. QED.

## Consequences

**(F1) Delta = 3.5 is vacuous. KNOWN THEOREM.** Random 3-SAT with m = Delta n clauses is satisfiable w.h.p. for Delta < 3.52 (Kaporis–Kirousis–Lalas 2006; Hajiaghayi–Sorkin 2003). The exact-layer sampler (t distinct proper clauses) is the standard without-replacement model; transfer of this monotone w.h.p. statement between with/without-replacement models at linear density is standard but is not re-proved here. Hence Pr[UNSAT] -> 0 and TWOSATDEC's residual is undefined for all large q at t = floor(3.5q); the empty draws since q≈43 are the predicted outcome, not evidence about depth.

**(F2) B-DEPTH is FALSIFIED for every constant Delta at which UNSAT has probability bounded below. KNOWN THEOREM + Lemma W.** Ben-Sasson–Wigderson (JACM 2001, Thm on random k-CNF, k=3): w.h.p. every resolution refutation of random 3-CNF with Delta n clauses has width Omega(n / Delta^{1+epsilon}). With Lemma W, r* >= Omega(q/Delta^{1+epsilon}) - 3 w.h.p., so for any fixed r (indeed any r = o(q)) the captured fraction of UNSAT formulas -> 0 and the residual -> 1. For Delta > 4.4898 (Díaz–Kirousis–Mitsche–Pérez-Giménez 2009) UNSAT is w.h.p., so no conditioning issue arises. This kills the bounded-depth version of the series' target in either density regime.

**(F3) COMPUTATIONAL (finite, consistent with F2).** Stage A, t=floor(3.5q), N=200, seed 20261005: UNSAT 3, 4, 0, 0, 0, 0 at q = 20, 30, 40, 60, 80, 100. Stage B, t=6q, N=12, minimal certifying depth r*: q=8: all 2; q=12: all 2; q=18: 2–3; q=26: all 3; q=30: 3 (one 2, one 4); q=34: six 3s and six 4s (mean 3.5); q=40: 3,4 on 7 formulas, 5 undecided within the 25 s budget (NOT computed; recorded as None). Fingerprint replay q=26 reproduced TWOSATDEC21 (SAT 15 / UNSAT idx 0). Finite tests are not asymptotic proofs; F2 carries the asymptotic claim.

## Gates

DISJ sanity: NOT APPLICABLE (no communication/lower-bound transfer claimed). Relativization: NOT APPLICABLE (statement is about a fixed proof sub-system, not a machine class). Simultaneous DTISP: NOT APPLICABLE. Deterministic configuration counting: NOT APPLICABLE. Natural Proofs/algebrization: NOT APPLICABLE — this is a proof-complexity lower bound for a restricted procedure and says nothing about circuits; XOR-SLICE-EASY, LOCALPATTERN-GUARD, the P/poly positive-family barrier, SLICELIFT2 and THRESHOLD-APPROX-GUARD are untouched. Easy-family control: 2-SAT/Horn/affine instances are not in the sampled distribution; the width bound is distribution-specific.

## Recommendation (integration point)

RETIRE the q -> q+1 empty-draw series at t=3.5q: further draws are predetermined by F1 and cannot advance any dependency. The bounded-depth reading of SAT-LOCAL-ERROR1 is FALSIFIED by F2. A non-vacuous successor must (a) work at a density with Pr[UNSAT] bounded below and (b) use a procedure not simulated by width-o(n) resolution — otherwise BSW kills it immediately. Exactly such a procedure must eventually confront the Doc's IIB walls (lower bounds for multiples / commutators) or general resolution size, so the next lemma worth stating is: *which part of SAT-LOCAL-ERROR1, if any, survives once depth is allowed to be Theta(q)?* — recover DIRECTIONALTELESCOPE1's original text before attempting it.

## Status

SAT-LOCAL-ERROR1 (bounded-depth reading): FALSIFIED/RETIRED, by KNOWN THEOREM (BSW 2001) + Lemma W (proved here, unreviewed). Its unrecovered original statement: OPEN, text missing. SAT-SUNFLOWER2-DIRECTIONAL: OPEN, untouched. No living TMR manuscript edited (this routine holds no TMR role). Issue #3 not posted.

Code: `experiments/monotone_slice/twosatdec_width_audit.py`. Raw: `results/raw/monotone_slice/TWOSATDEC_WIDTH1.txt`.
