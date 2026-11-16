# TMR-3/062: bounded head diameter and a restricted two-fifths space transfer

November 15, 2026, 22:24 PST. TMR-3 / PNP Time-Space Tradeoffs, Track B.

**Status:** The uniform bounded-head-diameter *one-writable-tape compiler lemma* below is PROVED/EXACT within its stated fixed-p local-head model, independent mathematical review OPEN. The derived two-fifths-space simulator is CONDITIONAL on the OpenAI September 25, 2026 preprint's separate one-writable-tape theorem. Finite evidence is COMPUTATIONAL. No polynomial-time simulator, unrestricted multitape improvement, SAT lower bound, or P-versus-NP separation is claimed.

## Named end-to-end target and falsifiers

C3-HEAD-DIAMETER-ONE-TAPE-TRANSFER. For each fixed total deterministic machine M with p>=1 ordinary writable tapes, finite alphabets, one-step local head motions, fixed starting origins, originally blank work tapes and ordinary endmarked read-only source x, compile its *actual input-dependent computation* onto one writable tape. Then invoke the cited one-writable-tape space theorem, with its explicit model and time limitations, to obtain exactly M's final Boolean control outcome.

For an actual t-step run define D_i=max_{h<=p}pos_h(i)-min_{h<=p}pos_h(i) and D=max_{i<t}D_i. All original writable origins share coordinate zero. Promises about D are explicitly restrictions on the declared input/machine class, not preprocessing advice.

Precommitted falsifiers: F1 a hidden unbounded counter or random-access packed tape; F2 falsely treating simultaneous reads/writes on distinct tracks as one overwritten bit; F3 cap-dependent initial symbols, free source access or borrowed memory; F4 an unjustified extension from a space-only theorem for one writable head to arbitrary multitape polynomial-time computation.

## Exact primary-source scope

OpenAI, *Simulating One-Tape Time in Two-Fifths-Power Space*, September 25, 2026, Theorem 1: https://github.com/openai/math/blob/main/preprints/Simulating-One-Tape-Time-in-Two-Fifths-Power-Space-September-25-2026/article.pdf . The original repository README has blob d74c2476cf2421cc5c71e416a633edd6c7605560; the exact Lean scope note lean/docs/137.md has blob 366bdd279886f7153b40b707e9c92aa90baf05b2; Lean statement lean/ComparatorChallenges/OneTapeSpace.lean has blob 662fe3383a4d94c82d8327108d757bee00547775. The statement file contains theorem declarations capped and unknown followed by intentionally unproved-by-that-file sorry markers; a comparator was reported elsewhere, but its proof module, native kernel and transitive axioms were NOT independently executed in this run. The cited theorem claims O(U^(2/5) polylog(U+2)) deterministic writable-space bits for one writable head and fixed read-only heads, with a fixed cap-independent polylog-space initial-symbol accessor. Simulation time is explicitly UNRESTRICTED, and no final tape materialization is required.

Williams, *Simulating Time With Square-Root Space*, arXiv:2502.17779v1, Theorem 1.1 and Section 3.2, remains the ordinary multitape O(sqrt(t log t))-space baseline: https://arxiv.org/html/2502.17779v1 . OpenAI's manuscript itself observes that standard O(t^2) general-multitape to one-tape conversion gives only O(t^(4/5) polylog t) space via its theorem. TMR-3/061 in draft PR #201 separately audited the expensive exhaustive movement-word guessing template. This positive transfer does not suppose that Williams requires original-source-only graph indices.

## Packing lemma and proof

**Lemma (PROVED/EXACT restricted, external review OPEN).** Fix M and p as above. There exists one fixed, uniform, genuinely locally moving deterministic single-writable-head machine P_M, retaining any of M's fixed read-only heads, such that on every source x for which M halts after t steps, P_M has the same final output and its own physical running time U obeys

    U <= c_M SUM_(i=0)^(t-1)(D_i+3) <= c_M t(D+3).

It takes no graph, head-movement schedule, source-specific advice or time cap. It also reproduces malformed-input rejection as part of M's original steps.

**Proof.** The finite alphabet of one writable tape contains p independent original work-symbol tracks, p current-head flags, two extreme-marker flags and constant phase markers. Every original cell coordinate has exactly its own p-track symbol tuple; two original heads at one coordinate still access *different* symbols. Work tracks begin blank and all flags at origin. At the start of every macro-transition the one actual head is at the leftmost active marker. Sweep to the rightmost marker, collecting all p current old symbols in finite control (p fixed), along with the read-only input-head symbols. Only after this sweep compute the one genuine M transition. A reverse sweep applies each write to its own old-position track. A fixed radius-one sliding-window pass across the enlarged interval [L-1,R+1] relocates all p marker flags simultaneously according to the move directions; another fixed pass rebuilds leftmost/rightmost flags and returns the head to the new leftmost marker. The finite controller requires no integer head-coordinate register, and there are a fixed number of sweeps because p is constant. Head motions of M have magnitude at most one, so the new active interval lies in [L-1,R+1]. Every macro therefore uses at most c_M(D_i+3) real one-head moves/steps. Each original read-only head stays put during work sweeps and performs exactly its original prescribed move at the end of that macro. Inductively the state, source-head positions, all writable-track cell values and marker positions coincide exactly with M's after every step, including both possible halting outputs. This proves the claimed bound. P_M itself can use a long physical tape; its space is NOT claimed to be small.

## Conditional source-authenticated one-tape consequence

P_M's initial writable tape is blank. Its fixed writable-symbol accessor returns blank in constant space. To recover a read-only source symbol at displacement q, an ordinary source-head rescan with binary counter obtains the true symbol in O(log(U+2)) writable bits for |q|<=U; the potentially large reread time is legal under the SPACE-ONLY theorem. The accessor does not depend on U except as a supplied query parameter and does not conceal preloaded tape contents. Accordingly the claimed unknown-time OpenAI theorem, IF VALID, supplies a final deterministic output simulator for fixed P_M with simultaneous peak work-space

    S_final(x) = O_M((t(D+3)+2)^(2/5) log^C(t(D+3)+2)).

This counts the final simulator's source access, recursive work, indices, registers, retained intermediate states and output through the external theorem. It does not splice P_M's physical tape into its own space count. The final simulator's running time is UNKNOWN and possibly superpolynomial. It cannot be composed with an FLMV forbidden-region argument requiring a strict polynomial-time and small-space pair.

For promised D=O(t^delta), the exponent is rho=2(1+delta)/5. One obtains rho<1/2 precisely when delta<1/4. Examples: delta=0 -> 2/5, 1/8 -> 9/20, 1/4 -> 1/2, 1/2 -> 3/5 and 1 -> 4/5. Equivalently a general one-tape transport with time U=O(t^kappa polylog t) yields a sub-square-root exponent through this route only if kappa<5/4. This is a quantitative constraint on this one transfer, NOT a lower bound on other methods or an extension to unrestricted multiple writable heads.

## Genuine input-dependent two-tape example

A fixed blank-start two-writable-tape machine has one-bit state r and previous-motion e, initially both zero. On source bit z, with a and b the values currently read on its two distinct work tapes, it writes (a XOR z XOR r, b XOR a XOR z), updates r <- r XOR (a AND b) XOR z, moves writable head 1 by d=2z-1 and writable head 2 by the OLD e, and updates e to d. It moves its read-only input head one symbol. On EOF it outputs r; malformed nonbinary encodings reject. The head paths depend on input bits and can revisit physically changed cells; the update also reads actual previous work values. Nevertheless for every binary source, after consuming j bits, the two physical positions differ by d_j, by telescoping the displacement sums, so D<=1 on every run. This authentic family has O(t) packed single-tape time and therefore inherits a CONDITIONAL O(t^(2/5) polylog t) outcome simulation. No hardness or compulsory-work inference is made.

## Same-execution ledger and four mandatory gates

Original M: t actual steps with paid source parsing, failed inputs, moves and rewrites. Packed P_M: at most c_M sum_i(D_i+3) actual sequential work steps, fixed finite alphabet, no source-dependent stored graph and its own possibly long tape. External one-writable-tape simulator: conditional O(U^(2/5) polylog U) writable bits on ONE final execution, including its requested symbol accesses, buffers, recursive evaluations and final output. No meaningful simulation-time bound from that source. No network parallel-span substitution or padding of a time-blowing simulator into its old time variable.

| Gate | Verdict |
|---|---|
| DISJ sanity | PASS restricted: this is a positive model-scoped upper transfer, not rank-to-circuit hardness; DISJ, Horn, 2-SAT, affine/Gaussian, treewidth, equality, autarky, independent products, padding, selectors, rank-one unique solutions, auxiliary and compact algorithms remain legal. |
| Relativization | NOT APPLICABLE WITH REASON: no P-vs-NP separation or nonrelativizing step; algebrization and Natural Proofs audits remain OPEN for any future NP target. |
| Simultaneous DTISP | PASS for packing time accounting, CONDITIONAL for the cited space-only theorem, OPEN for any one final execution with both polynomial time and improved space. |
| Configuration counting | PASS as an upper-bound consistency check for deterministic total machines. Unknown output-simulator time is not inferred from space, and no randomized/quantum stopping-time claim is made. |

Historical /341 remains FAIL full logical UNSAT authority; /386 RESTRICTED. P versus NP OPEN.

## Actually executed evidence

CPython standard library revision tmr3-packed-bridge062-v2, seed 202611152224, independently executed twice with byte-identical raw JSON. 2,047 exhaustive binary sources of length 0..10, 120 additional seeded random sources, five malformed controls and exact output/head-position comparisons resulted in **128,309 assertions and ZERO failures**. Both outputs occurred and maximum observed writable-head diameter was one. The audit charges a conservative four-sweep virtual packed-tape budget; it uses host integer positions to check the specification and is NOT a native finite-control machine compiler, not OpenAI's simulator, not a Lean proof or a generic asymptotic verification. Source Git blob 491c288b9feedd531a2ee125c57d0f353fdaff1d and raw Git blob e0b49397b5bb7b8f9108b40a9a4b7338f8aa9753 are the exact locally executed objects.

Publication paths are the assigned main3_PNP_TIME_SPACE_TRADEOFFS.tex, this TMR-3-owned report, experiments/tmr/tmr3_packed_bridge062.py, results/raw/tmr/2026-11-15_2224_TMR3_HEAD_DIAMETER062_PY_RAW.json, role handoff.md and exact prior handoff archive. Full repository checkout/preflight, original article PDF inspection, Lean/nanoda build and external mathematical review NOT executed.

**ONE NEXT LOAD-BEARING LEMMA: C3-CLUSTERED-HEAD-TRANSPORT.** Prove a source-authenticated uniform one-writable-tape compiler running in O(t^(5/4-epsilon)) for an explicitly broader class than globally bounded head diameter, with fully charged input and marker/index movement, or exhibit a precise model-scoped obstruction. The generic multitape and improved nonassociative Tree Evaluation bridges remain OPEN.
