# CC09: Best constructive proof formulation and circulation closure audit

2026-11-24, America/Los_Angeles. Prepared in the 19:44 PST iteration. **PROVED/EXACT in stated domains; COMPUTATIONAL controls; CONDITIONAL universal theorem. P versus NP remains unresolved by this work. Independent review pending.**

## Main document

[Best Current Proof Attempt (PDF)](PNP_Best_Proof_Attempt_CC09_2026-11-24.pdf) is the complete mathematical formulation. [Editable LaTeX](PNP_Best_Proof_Attempt_CC09_2026-11-24.tex) and [BibTeX references](references.bib) accompany it. This is an additive synthesis, not an edit to a peer-owned manuscript.

## Substantive result of this iteration

For any two partitions of n variables into monotone NAE triples, the source is a cubic bipartite incidence graph. It has two disjoint perfect matchings A,B. For every source edge e, one matching M avoids e; both M and M+e are NAE-feasible. Their difference is the unit vector e. Therefore the exact affine hull of every unpinned two-partition feasible set is the full F2^n.

Consequently, splitting a four-partition source into two pairs and comparing the two complete affine hulls supplies no root distinction at all, regardless of the pairing. This falsifies affine synchronization as a sufficient universal completion rule. It does not exclude exact nonlinear compatibility, a different representation, or P=NP.

The nine-variable affine-plane source makes the failure explicit: each half has 102 models and affine rank 9, but the full source has none. A short independent proof uses the fact that every five points in the affine plane of order three contain a line. Every two-coordinate projection of each half is also full.

## Positive constructive component

Each pair compiles exactly to a single-hub integral circulation with arc intervals [1,2], [0,1], [1,2]. Source pins become fixed bounds. Every feasible difference from a baseline decomposes into arc-disjoint residual cycles. A two-sheet parity lift finds an odd labeled cycle, or certifies its absence, in polynomial time.

M07 already proved the one-bit oracle and primal/dual affine-hull mechanism. CC09 credits that dependency and implements the complete loop in the explicit width-one source: each query either adds an actual feasible difference or an independent true identity. At most n queries acquire the exact affine hull. This is complete linear information about the pinned flow support, not its nonlinear support and not an arbitrary simultaneous-parity flow oracle.

## Best remaining constructive route

The PDF proves the one-third phase-chart theorem through every supplied model, exact guarded cycle composition, the explicit Fibonacci cycle-catalogue obstruction, and a direct 3SAT reduction to negative binary conflicts plus disjoint ternary XOR equations. It restates and proves the BD13 actual-witness span terminal on exact affine observation trees, with the paid job count

    J = 1 + sum_leaf 2^w (D+1)(d+1) max(1,L)^2
          + sum_join 2^(w_left+w_right) D_left D_right.

The terminal preserves all shared observations in cut keys and retains actual witnesses. T <= acquisition + poly(N) J. Polynomial acquisition and a polynomial aggregate J, or a different authenticated terminal/reduction with a conserved global reserve, would give a uniform polynomial decider for the NP-complete four-partition source. That universal bound remains OPEN.

Small exponential kernels are allowed: 2^(O(k)) poly(N) is polynomial at k=O(log N), for fixed constants and paid discovery. N^(O(k)), an unspecified FPT parameter function, or polynomial work per branch does not yield that conclusion.

## Executed CC09 evidence

Run `python3 CC09_check.py --stage controls --output CC09_results.json` and `python3 CC09_check.py --stage scaling --output CC09_scaling.json`. Standard library only; seed 2091124; Python 3.12.14. Final checker SHA-256: `3bd9557ef05490064d05e32a98d0a820f3b92a998edc537dbfea5a044a2aafe0`.

* 120 pinned flow contexts, 110 SAT and 10 UNSAT, compared with exhaustive source models; acquired hulls and every returned witness checked.
* Exact AP3 UNSAT and 12-variable 90-model SAT controls; halves have 102/102 and 450/450 models, respectively.
* 192 supplied anchors and 2,256 forest-chart words directly verified.
* Three explicit catalogues of 29,29,46 cycles; all 654 source models reconstructed; 436 legal and 1,411 forbidden cycle-pair choices checked against original capacities, including hub arcs.
* One UNSAT 22-clause residual and all 22 one-clause-deletion SAT neighbors; four have six models and eighteen have one. Also 66 two-NAE-deletion SAT controls. The 12 single-NAE deletions and 36 one-sign flips of the full AP3 source were all UNSAT, and are recorded as unsuccessful neighboring attempts.
* 41 mixed-guard source comparisons, 40 SAT and one UNSAT, with witness lifting.
* Fibonacci cycle counts checked at seven sizes through k=12 (144 required cycles, n=36); polynomial hull acquisition at n=9,18,36,72 with n queries and actual witness generators.
* 48,770 controls assertions plus 27,386 scaling assertions, zero discrepancies in the completed runs. Approximate stage times 0.47s and 0.03s. No measured physical peak memory or cumulative memory.

## Evidence and publication discipline

`prior_CC02_CC08.zip` preserves the recovered report/code/results from the earlier CC02, CC03, CC04, CC05, CC06 and CC08 iterations. Their saved results are historical and were not rerun here. The PDF includes the prior bipartite small-port proof and explains the exact domains of wheel factorization, flow/count hybrids, Fourier acquisition, probe-stable ranks, and integer-lattice closure.

GitHub connector reads recovered AGENTS.md, CODEX.md, the PNP research skill, issue #327, recent comments, original DO01/DP01/S06, M07/MS08, and recent BD13/DY13/DP13/MS19 reports. No local checkout was available, so repository preflight was not executed. A bounded branch inventory was inspected; not every draft or historical chat was audited. No other agents or schedules were changed.

All discovery, failed attempts, closure, source compilation, arithmetic bits, DAG keys and edge attempts, sharing, branch aggregation, memory, and reconstruction remain charged. CM <= (T+1) S is an analytic same-execution bound, not a measurement. No formal proof assistant, universal portfolio, native strict tetrahedral compiler, or all-channel semantic closure was executed.

## Specific peer feedback

M07/I06: independent explicit circulation implementation confirms the one-parity mechanism and n-query outer hull loop; no new general theorem of parity-flow tractability is claimed. BD13: consumer-specific witnessed spans and actual cut words are the sound route; independent affine hulls are insufficient. DY13: binary conflicts plus XOR remain a substantive language, and small global rank is distinct from bounded cut width. DP01/DP13: preserve additive job reserves and bound their magnitude on the original input, with no free adapter or guard-dependent rank reuse. DO01: the full-hull result is an unconditional summary-level limitation across the two-partition source domain, not an unrestricted lower bound. MS19: actual anchors remain essential; an affine or integer-lattice point is not a feasible source witness.

**Next named dependency:** acquire a source-equivalent nonaffine joint interface or compatible exchange decomposition on arbitrary residual cores with a proved polynomial aggregate reserve. The universal proof cannot currently be closed.
