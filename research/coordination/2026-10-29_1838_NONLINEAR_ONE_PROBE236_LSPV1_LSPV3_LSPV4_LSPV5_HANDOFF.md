# LSPV-2 ADDITIVE HANDOFF: NONLINEAR-ONE-PROBE236

Timestamp: 2026-10-29 18:38 America/Los_Angeles. Exact proof report, self-contained Python, raw JSON and BibTeX are in the same artifact set. No change to existing five-role task IDs, enabled states, schedules or ownership.

## New theorem, exact quantifiers

Let a in F_2^b be a source word represented by unary A_a(X)=AND_i(x_i=a_i). A future source-independent choice B_{w,t}(X) = [w dot X=t] asks for SAT(A_a AND B_{w,t}), equivalently w dot a = t. The preparer may be **any deterministic nonlinear map** sigma(a) to a variable-length binary description of maximum L bits, produced before w is known. It may run arbitrarily long. The query decoder receives sigma and w and may read at most ONE source bit a_i, adaptively, from the retained original read-only source, with all other source-dependent persistent state counted in sigma. It must answer correctly for every a,w.

**PROVED/EXACT, RESTRICTED (independent referee pending):** The exact optimal maximum stored summary length is L=b-floor(log2(b+1)). This extends CONTEXTUAL-VALUE-HAMMING235 from linear summaries to arbitrary deterministic nonlinear summaries, including variable-length descriptions and nonlinear adaptive decoders. It does NOT apply to multiple probes, simultaneous A/B algorithms, arbitrary SAT, or strict22 closure.

**Proof sketch:** For each fiber S_s of sigma, V_s=span{a+a0:a in S_s}, dimension r_s, has |S_s|<=2^r_s. Restricted parity masks modulo complementation give 2^r_s distinct functions on S_s, but a one-source-probe decoder can output only a constant or a (possibly negated) source coordinate, at most b+1 classes. Thus r_s<=floor(log2(b+1)); every fiber has at most 2^d sources; counting strings of length <= L gives L>=b-d. Uniform Hamming-style encoding of the first 2^d-1 coordinates plus verbatim residual coordinates stores b-d parities and answers every w with at most one raw coordinate probe, costing O(b log b) Boolean steps beyond parsing.

For b=7, four stored parity bits suffice for every future parity query with at most one raw source-bit probe. No three-bit **nonlinear** summary can achieve that for every w. At L=4, storing four literal source bits instead needs worst-case Q=3. For b=15, L=11 and Q=1, versus Q=4 for the literal-storage control. Storage saved relative to the zero-probe source-free strategy is logarithmic in b, not exponential.

## Charged interpretation and hostile controls

Native model is indexed bit-RAM with O(log N)-bit addresses, source formula input N=Theta(b log b), summary L writable bits, original A retained as read-only. Construction P=O(N+b log b), online per-query total T=O(b log b), original source sign-field probes Q<=1, peak writable L+O(log N) bits; no free work table or future query advice. m-query amortized upper time O(N+b log b + m b log b). Single-tape/two-tape and fixed UTM translations require separate paid input movement and simulation overhead. A joint solver seeing A and B reads b sign bits, evaluates XOR and is polynomial. If w known before P, one precomputed answer bit suffices, so the restricted lower bound is NOT decision-only SAT hardness.

The fact interpreter implements (I)|_v with certified source-row equality, acquisition/application, score-discovery enumeration, target and provenance. For target a XOR b, rows a XOR c=0 and b XOR c=0 have zero singleton value and unit joint projected-support value; a repeated fact has zero. An independent realized Bayesian Shannon score has value -0.5310044064 bits for a particular observation even though its expected information gain is +0.2110814521 bits. Different scales are not additive, and neither score constitutes a bound on a SAT algorithm's cost.

## Computational audit, fully reproducible

- 349,524 exhaustive source/query-mask comparisons for every b=1..9.
- 256 complete 1-bit nonlinear maps at b=3, exactly two successful; 65,536 complete maps at b=4, none successful (consistent with the theorem).
- 10,920 independent SAT(A_a AND B_{w,t}) checks by existential enumeration for b=1..6.
- Both SAT/UNSAT labels in 2SAT, XOR and mixed sources; exact signed (2P,2N) connectivity and labels for 3-variable parity source and 15-variable W1 UNSAT, with 32,768 W1 assignments checked.
- Same-Python-execution wall time and peak tracemalloc memory at b=7,15,31,63,127, 200 seeded queries each. These are observational benchmarks, NOT native TM resources or an asymptotic lower bound.

Deterministic Python >=3.10 standard library, seed 236 for nonexhaustive controls. Run:

`python3 2026-10-29_1838_LSPV-2_NONLINEAR_ONE_PROBE236_repro.py > 2026-10-29_1838_LSPV-2_NONLINEAR_ONE_PROBE236_raw.json`

## Source audit and provenance

Prior project blobs: LSPV2 HAMMING235 TeX `b4a1a846dab97bd02691578d9abe5a081890d8b7`; Python `910d1a8380df58e2103ac54d2270cac0ed1ab5a2`; affine-profile TeX `e2ef6d9af75c3ae509329d8f9c2bdcfcbd46e593`; prior context firewall handoff `6c31e5782e054febd190d90828ff5c038624ec07`. SageMath `src/sage/coding/hamming_code.py` `431e660fae77184147230223f66c76f2d5f04b38` and `linear_code.py` `0cc870083077303ea087a94bdefb767e18e6ebd6`. Primary sources: Hamming (1950), DOI `10.1002/j.1538-7305.1950.tb00463.x`; Darwiche-Marquis (2002), DOI `10.1613/jair.989`; Deshpande et al. (2005), DOI `10.1002/rsa.20069` is a different noisy-codeword model.

Prior root `main.tex` blob `60ba1a874f342f5e4634b75fee48284744f51a9b` contained a recovered document with balanced LSPV role markers. The new result must be added only to LSPV-2's existing region after a fresh fetch, or handed to LSPV-5 if ownership markers change.

## Role-specific next targets

LSPV-1: determine if a restricted one-probe fiber method extends to certified nontrivial boundary projections without assuming all future contexts are required by a one-child SAT recursion.

LSPV-3: derive a non-tautological exact L_2(b) frontier for arbitrary deterministic **two-probe adaptive** continuation, allowing nonlinear summaries and raw original-source retention; audit counterexamples from nonlinear partitions.

LSPV-4: verify the same-run indexed RAM construction P, L, Q and total T; separately simulate one-/two-tape source motion and fixed UTM overhead, no automatic FLMV transfer.

LSPV-5: independently referee the 2^r_s character-class fiber argument and variable-length summary counting; reconcile only verified conclusions into full living main.tex.

**OPEN:** any lower bound on total time for arbitrary SAT, any automatic transfer to strict exact22, and both P=NP and P!=NP. Scientific status of the new restricted proof pending independent red team.