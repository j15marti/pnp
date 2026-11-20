# LOCALDEPTHWIDTH1: bounded free-2-SAT decision depth is bounded-width resolution; the q-sweep at density 3.5 is retired

P versus NP remains OPEN. No circuit lower bound and no unrestricted runtime lower bound is claimed. Independent review: NONE yet.

## Why this run differs from TWOSATDEC57 to TWOSATDEC90

This routine has run the same test hourly for 85 runs, raising q by one each time at t = floor(3.5q) with N = 16. The last nine draws (q = 87 to 95) were all empty. AGENTS.md (2026-11-15) says repeated easy draws and parameter steps don't count as progress, and that each run must advance or falsify a named dependency. The named dependency is SAT-LOCAL-ERROR1: does free exact 2-SAT plus a bounded-depth decision capture exact-layer UNSAT formulas? This run answers it analytically where it is answerable and retires the sweep.

Model. Exact layer: F is a uniform t-subset of the M = 8 binom(q,3) proper 3-clauses on q variables. Depth-r certificate: a set S of r variables such that every assignment rho of S, after unit propagation (UP), yields an empty clause or an unsatisfiable width-at-most-2 skeleton. This is the protocol of TWOSATDEC6 to TWOSATDEC90.

Falsifiers stated before the work: (F1) a certificate step that isn't simulable by width-bounded resolution; (F2) a failure of the with-replacement to exact-layer transfer; (F3) small-q data where the minimal depth doesn't grow at a density where UNSAT is typical. None fired. F3 is only a finite probe.

## Lemma LDW-1 (PROVED/EXACT, short proof; not independently reviewed)

If a 3-CNF F has a depth-r certificate, then F has a resolution refutation of width at most r + 3 and size at most 2^r poly(|F|).

Proof. Fix rho. Each UP step resolves a clause of F|rho (width at most 3) against derived unit clauses. Every intermediate clause is a subclause of a width-3 clause, so its width is at most 3. That derives every unit, every reduced clause, and the empty clause if there is a conflict. If the width-at-most-2 skeleton is unsatisfiable, resolution closure restricted to width 2 is complete for 2-CNF, because a resolvent of two clauses of width at most 2 has width at most 2. So F|rho has a refutation of width at most 3. Next, use the standard restriction lemma (Ben-Sasson and Wigderson 2001). If F|x=0 and F|x=1 both have refutations of width at most w, then adding the literal back to every clause gives derivations of x and of not-x of width at most w + 1, and one resolution step refutes F. Inducting over the r variables of S gives width at most r + 3. There are 2^r branches, each of polynomial size. QED.

## Consequence LDW-2 (KNOWN THEOREMS + LDW-1; scoped)

These sources were cited from memory. They weren't re-fetched in this run, and their exact constants need checking before promotion.

- Ben-Sasson and Wigderson (J. ACM 2001), building on Chvátal and Szemerédi (1988): for random 3-CNF with Delta n clauses and constant Delta, every resolution refutation has width Omega(n / Delta^{1+epsilon}) with high probability. That model samples with replacement.
- Díaz, Kirousis, Mitsche and Pérez-Giménez (2009): density 4.4898 or more is UNSAT with high probability.

Transfer to the exact layer (PROVED, elementary). With t = Theta(q) and M = Theta(q^3), the with-replacement sample has all clauses distinct with probability 1 - O(t^2/M) = 1 - O(1/q). Conditioned on that event, it is exactly the exact-layer law. An event with probability 1 - o(1) keeps probability 1 - o(1) under this conditioning.

Therefore, at any constant density above 4.4898 (for example 5), with high probability an exact-layer formula is UNSAT and has minimal certificate depth r at least Omega(q) - 3. Bounded depth captures a vanishing fraction, and any certificate has at least 2^{Omega(q)} branches. So SAT-LOCAL-ERROR1 is FALSIFIED in the typical-UNSAT regime for every fixed r, and also for r = o(q).

## Consequence LDW-3: the density-3.5 sweep can't inform SAT-LOCAL-ERROR1 (KNOWN THEOREM)

For random 3-SAT, density 3.52 or less is SAT with high probability (Kaporis, Kirousis and Lalas 2006; Hajiaghayi and Sorkin 2003; cited from memory). Since 3.5 < 3.52, P(UNSAT) tends to 0 on the exact layer, by the transfer above. So empty draws at q of 87 or more are predicted. They carry no information about decision depth.

The limiting threshold alpha_3 exists. Carenini (ECCC TR26-229 / TR26-145) gives it, and so does an independent alternative proof: OpenAI, "A Limiting Satisfiability Threshold for Every Fixed Clause Size" (25 September 2026), openai/math commit 4eaee875, article.pdf sha256 5318fe3d…76365, with Lean files under lean/OAI/Probability/RandomSAT/. Neither the Lean build nor the proof was checked in this run.

Conditioned on UNSAT at density 3.5, the formula is a mixture of two kinds:

- Rare small cores. A core on k variables has probability about q^{-k-2}, which is q^{-9} at best. These are capturable at bounded depth.
- Finite-size large fluctuations. These are what the q = 26 to 42 survivors at depth 4 or 5 look like.

Which kind dominates asymptotically is OPEN and wasn't settled here. That conditional question is the only form of SAT-LOCAL-ERROR1 still open, and an N = 16 sweep can't reach it.

Status. TWOSATDEC sampling at density 3.5: RETIRED as evidence. SAT-LOCAL-ERROR1, typical-UNSAT regime: FALSIFIED (CONDITIONAL on the cited theorems). Conditional-on-rare-UNSAT form at 3.5: OPEN, low value.

## Computation (COMPUTATIONAL, finite only)

Script: `experiments/monotone_slice/local_depth_width_audit.py`. Raw output: `results/raw/monotone_slice/LOCALDEPTHWIDTH1.txt`.

Protocol replay: q = 26, density 3.5, seed 20261005. This reproduced the TWOSATDEC21 fingerprint (SAT 15 / UNSAT 1 at index 0, minimal depth 4). The recorded quadruple (5,20,25,26) certifies, and the lexicographically first certifying set is (5,8,20,26).

Density 5.0, seed 20261120, N = 12, budget about 2 s per instance. The table counts UNSAT instances by their minimal depth.

| q | depth 2 | depth 3 | depth 4 | depth 4 or more, search cut off | SAT |
|---|---|---|---|---|---|
| 10 | 5 | 0 | 0 | 0 | 7 |
| 14 | 3 | 6 | 0 | 0 | 3 |
| 18 | 1 | 4 | 0 | 0 | 7 |
| 22 | 0 | 10 | 0 | 0 | 2 |
| 26 | 0 | 3 | 9 | 0 | 0 |
| 30 | 0 | 3 | 8 | 0 | 1 |
| 34 | 0 | 1 | 3 | 3 | 5 |

The minimal depth grows from 2 to 4 over q = 10 to 34. That fits LDW-2 but is no evidence of an asymptotic rate. Each run took under 12 s.

## Gates

- DISJ sanity: NOT APPLICABLE. This is a proof-system statement about random CNFs, not a communication argument.
- Relativization: NOT APPLICABLE. The result is a resolution-width lower bound, not a machine separation.
- Simultaneous DTISP: NOT APPLICABLE.
- Deterministic configuration counting: NOT APPLICABLE.
- Natural Proofs: the result is restricted proof complexity and claims nothing about circuits.
- AGENTS.md guard: no unrestricted runtime claim follows from a restricted proof-complexity lower bound. LDW-2 rules out the DPLL/2-SAT-leaf local decision family only, not arbitrary algorithms or monotone circuits.

## Integration point and next lemma

This closes the bounded-depth arrow of the SAT-slice local-trimming pipeline. Any continuation must target a model strictly stronger than bounded-width resolution. Next load-bearing lemma: does the "local error" approximator in DIRECTIONALTELESCOPE1 / SAT-SUNFLOWER2-DIRECTIONAL simulate in a proof system with known random-3-CNF lower bounds, such as resolution, Res(k), or polynomial calculus (Ben-Sasson and Impagliazzo; Alekhnovich and Razborov)? If it does, it is falsified the same way. If it doesn't, name the exact step that exceeds those systems. The hourly q-sweep at density 3.5 should not continue.
