# TWOSATDEC-DENSITY-AUDIT1: the TWOSATDEC series cannot test SAT-LOCAL-ERROR1

P versus NP remains OPEN. No monotone-circuit or SAT lower bound is claimed.
HEAD at start: `f3e7eaaef888e1c265d0ed1550d1d5fc3b490ca1` (TWOSATDEC92).

## Why this run does not do TWOSATDEC93

TWOSATDEC88 through TWOSATDEC92 (q=93..97) all drew `0/16` UNSAT formulas. Under AGENTS.md (2026-11-15) that is a repeated easy result with one parameter moved each run, which does not count as progress. This run checks whether the protocol can say anything about its target at all.

## Candidate and falsifiers

Candidate (the series' implicit hypothesis): for UNSAT formulas on the exact 3-CNF layer, decision depth r = O(1) plus free exact 2-SAT closure after unit propagation certifies UNSAT.
Falsifiers: (F1) the sampling density makes UNSAT draws vanish as q grows, so the sample says nothing; (F2) a KNOWN THEOREM forces r to grow with q at any density where UNSAT is typical; (F3) UNSAT draws below the threshold are dominated by small dense cores, so a bounded r measures a local artifact.

## Results

**Lemma (PROVED, elementary, not independently reviewed).** If a depth-r certificate in the TWOSATDEC sense exists for F, then F has a resolution refutation of width at most r+3.
Proof. Take a leaf ρ, which assigns the r chosen variables. Unit propagation on F|ρ is a sequence of resolutions of a clause of width ≤3 with a unit, so width stays ≤3. An UNSAT width-≤2 skeleton has a resolution refutation using only clauses of width ≤2 (follow the implication-graph paths x→¬x→x). So F|ρ has a width-3 refutation. Undoing the restriction one decision variable at a time adds at most one literal per level (Ben-Sasson–Wigderson 2001, restriction lemma). The total is ≤ r+3. ∎

**F1 holds (KNOWN THEOREM, plus an unchecked model transfer).** TWOSATDEC uses t = ⌊3.5q⌋, i.e. density 3.5. Random 3-CNF is satisfiable w.h.p. at every density below 3.52 (Kaporis–Kirousis–Lalas 2006; Hajiaghayi–Sorkin 2003). Going from the i.i.d.-clause model to sampling distinct clauses without replacement is standard at this density but was not re-checked here. So the series is expected to draw only SAT formulas from now on. Every further run is uninformative by design.

**F2 holds (KNOWN THEOREM via the Lemma).** For any constant density Δ above the threshold, a random 3-CNF needs resolution width Ω(n) w.h.p. (Chvátal–Szemerédi 1988 expansion; Ben-Sasson–Wigderson 2001). With the Lemma this gives a minimum certificate depth of Ω(q) w.h.p. on the layer where UNSAT is typical. So the bounded-depth hypothesis is FALSIFIED asymptotically wherever it could be tested. The transfer to sampling without replacement is the same caveat as in F1.

**F3 is consistent with the data (COMPUTATIONAL).** Code: `experiments/monotone_slice/twosatdec_density_audit.py` (seed 20261120) and `_stage2.py` (seed 20261121). The certificate semantics match TWOSATDEC. Each stage finishes in under 5 s.

- Density 6.0, minimum depth: q=12 → all 2; q=16 → all 2; q=20 → 2–3; q=24 → mostly 3; q=28 → 3; q=32 → 3,3,3,4. The depth grows with q, as F2 predicts. These sizes are finite and say nothing asymptotic on their own.
- Density 3.5, conditioned on UNSAT: at q=16, 4 UNSAT in 179 draws, depths 3,3,3,3; at q=20, 4 in 160 draws, depths 4,3,3,3. UNSAT draws are rare, and when they occur they are refuted at small depth. This is consistent with small dense cores and does not distinguish the hypothesis.

Raw output: `results/raw/monotone_slice/TWOSATDEC_DENSITY_AUDIT1_stage{1,2}.txt`. Both stages were re-executed and reproduced byte-identically.

## Gates

- DISJ: NOT APPLICABLE. This is a statement about one proof system, not about computation.
- Relativization: NOT APPLICABLE, same reason.
- Simultaneous DTISP: NOT APPLICABLE, same reason.
- Deterministic configuration counting: NOT APPLICABLE, same reason.

Under the AGENTS.md rule against unrestricted runtime claims from restricted proof complexity, the Lemma and F2 bound decision depth and resolution width only. They say nothing about monotone circuit size or about SAT algorithms in general.

## Recommendation

RETIRE the TWOSATDEC empty-draw series (q-increment runs) as FALSIFIED/RETIRED for SAT-LOCAL-ERROR1. If the depth question matters, it is settled at density Δ > 4.27 by the Lemma plus Ben-Sasson–Wigderson: depth is Ω(q). It cannot carry a circuit lower bound. The next load-bearing step should be chosen inside one of the five TMR end-to-end pipelines (see main5_PNP_MACHINE_BOTTLENECK_REDTEAM.tex), not here.

## Sources consulted this run

- Google Doc "P vs. NP Proof Attempts" (id 1b2SYjJJ…, content sha256 `eff485d7…`). I read keyword-matched excerpts only, not the full document. Its tensor-network section also attributes the collapse to expander/treewidth Ω(n), which is consistent with F2.
- GitHub code search (`org:openai`, `org:google`, `org:google-deepmind`). It surfaced openai/math preprint paths, including "Linear Variance of the Random 3-SAT Hitting Time" and "The Exponential Time Hypothesis is False". These are outside this session's repository scope. They were NOT read and are not evidence.
- Ben-Sasson, Wigderson, "Short proofs are narrow — resolution made simple", J. ACM 48 (2001). Chvátal, Szemerédi, J. ACM 35 (1988). Kaporis, Kirousis, Lalas, Random Struct. Alg. 28 (2006). Cited from knowledge; the PDFs were not re-fetched this run.
