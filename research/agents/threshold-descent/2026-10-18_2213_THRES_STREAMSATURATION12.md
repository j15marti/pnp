# THRES-STREAMSATURATION12 | 2026-10-18 22:13 KST

**Status:** Exact restricted finite-state image-saturation theorem, pending independent review. The full MCSP threshold descent and P versus NP remain OPEN.

## PROPOSE 4 -> SEARCH -> BUILD

Proposals: (A) high-algebraic-degree streamable semantic syndrome, (B) small-state source-adaptive online image quotient, (C) clock-charged position-aware selector, (D) distributional CHMY local-PRG vs uniform pushforward. Chose A/B for an explicit falsification theorem. Reviewed main ASYMPTOTIC_CONE5, LOSSY_PROMISE_CASCADE6, PARTIAL_SAMPLE_WEDGE7, PROMISE_CASCADE_FIXEDPOINT8, SOURCEQUERY_SYNTHESIS10; threshold-descent HASHIMAGE_SATURATION9/POLYFIBER10; MAGRED_DISTANCE_OVERLAP9/STREAM_NO10; CLOCKPARITY12; local THRES_STREAMFUSION11. Searched repository for prior time-homogeneous automaton-image sections; no direct project duplicate found.

Primary sources: CHMY STACS 2021, Theorem 16 and Lemma 15; Oliveira-Pich-Santhanam ToC 2021 Section 4 anti-checkers; Potechin-Shallit Information Processing Letters 2020 on fixed-length finite-automaton paths and matrix powers; Hirahara FOCS 2022 on Partial-MCSP.

## Theorem STREAM-STATE-SECTION12 (restricted, exact)

Let N=2^n and R be a deterministic **time-homogeneous** Q-state transducer on length-N input words. On consuming each source bit it updates its state and emits either no bit or one output bit; it may append O(1) final-state-dependent output bits after end of input. R has NO external step-index input, uncharged source-position-specific transition tables, or free side tape. Let B bound its output length. Interpret input f in {0,1}^N as an n-variable truth table and define

IMAGE_R[t] = { y : exists g in {0,1}^N, CC(g)<=t and R(g)=y }.

For every attainable y in R({0,1}^N) there exists g with R(g)=y and

    CC(g) <= poly(n, ceil(log2(Q+1))) (Q^2+B+1).

More explicitly the bound is O(n Q^2 poly(log(Q+1))+(B+1)n^2 poly(log(Q+1))) in the fan-in-two AND/OR/NOT model (nonuniform circuit advice allowed). Thus IMAGE_R[t] is identically YES on legitimately produced outputs whenever t exceeds this bound.

**Proof.** Fix source f producing y. Mark at most B input positions whose transitions emit bits. Preserve those emitting transitions, their input bits, and their start/end states. Partition each intervening no-output run into at most n blocks of power-of-two lengths; record start/end states for each block. For the directed graph consisting only of silent transitions, let A_k(p,q) say that some silent path of length 2^k connects states p,q. A_0 is adjacency; A_{k+1}=A_k o A_k over the Boolean semiring. A recorded block's endpoints satisfy A_k(p,q)=1. Replace it by the canonical such block: at each division choose the least midpoint m satisfying A_{k-1}(p,m)=A_{k-1}(m,q)=1, recurse left/right, and at length 1 choose a valid silent source bit. All block endpoints, emission positions, and terminal state are preserved, so the new input g has R(g)=y.

To compute g(i) for n-bit address i, hardwire O((B+1)n) interval/event records containing binary endpoints and endpoint states. Comparators select the containing block, then n unrolled midpoint rounds using precomputed A_0,...,A_{n-1} (nQ^2 constants) decode its bit. Each round requires at most O(Q^2 polylog Q) fan-in-two gates to find a feasible midpoint from the state pair; interval selection costs O((B+1)n(n+log Q)) up to fixed polylogarithmic factors. The proposed circuit computes the entire truth table of g with the asserted gate bound. QED.

For B=N^{a+o(1)}, Q=N^{sigma+o(1)}, any t=N^{tau+o(1)} with

    tau > max(a, 2 sigma)

trivializes this image-membership target. Unlike POLYFIBER10 this includes high-degree streamable features: full-input AND has algebraic degree N, yet only two states.

## Falsifiers and genuine scope

A position-dependent two-control-state machine could compare f_i against a separately hardwired arbitrary word h_i at each position and emit 1 only on f=h. The output-1 image fiber is then {h}, and counting gives h with CC(h)>N^{1-o(1)}. This shows why a free index-specific transition oracle would destroy the conclusion. An n-bit binary address counter generally contributes N distinguishable states to Q, making the stated bound vacuous at threshold N^tau for tau<1. Seed generation or provenance performed by the *same* homogeneous transducer and included in its emitted output is reproduced; external seeds, separate provenance constraints, random coin tapes, arbitrary index access and general one-tape algorithms are not covered.

The theorem constructs a NONUNIFORM source circuit witness and does NOT give a fast algorithm to find it, a uniformly NP/PH-low verification method for IMAGE_R, a CHMY one-work-tape lower bound, an actual two-sided MCSP/Gap-MCSP reduction, or a repeatable (beta,g)->(beta',g') map. In particular it does not automatically apply to THRES_STREAMFUSION11's arbitrary O(log N)-space online reducers: Q may be N^c for large c.

## Reproducible finite audit

Local standard-library Python audit of 1,296 exhaustive 2-state transition tables, 250 random 3/4-state machines and explicit parity/AND terminal-bit controls: 1,548 transducer families; 22,372 source inputs; 311,072 decoded input bits; 25,203 exact reachability checks; 22,372 matching-output/final-state checks; zero failures. A time-dependent two-state matcher for the 64-bit six-variable parity truth table rejected seven one-bit perturbations, illustrating the excluded position-specific transition model. Random seed 202610182212. These are finite identities, NOT experiments proving machine-time lower bounds.

## Next arrow

CLOCK-CHARGED-SELECTIVE-YES13: allow a source-address counter whose cost is explicitly charged, and either prove an analogous section theorem under highly uniform position-dependent transitions or construct an explicit counterexample; separately pursue a genuine YES-preserving selective anti-checker with robust NO, streaming tape composition, a jointly low verifier and positive slope gain. CHMY high-beta oracle one-work-tape lower bound remains the source, with query lengths N^{o(1)}. No rho>lambda established. **P versus NP OPEN.**

Sources:
1. CHMY, STACS 2021. https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2021.23
2. OPS, Theory of Computing 2021. https://theoryofcomputing.org/articles/v017a011/
3. Potechin-Shallit, Information Processing Letters 2020. https://arxiv.org/abs/1802.04708
4. Hirahara, FOCS 2022. https://eccc.weizmann.ac.il/report/2022/119/

FINAL_VERIFICATION_SENTINEL::THRES_STREAMSATURATION12::P_VS_NP_OPEN
