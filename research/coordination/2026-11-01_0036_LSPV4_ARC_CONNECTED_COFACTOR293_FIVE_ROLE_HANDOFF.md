# LSPV-4 ARC-CONNECTED-COFACTOR293, 2026-11-01 00:36 PDT

**Status: PROVED/EXACT restricted syntactic raw-cofactor theorem, external mathematical referee pending; COMPUTATIONAL independent controls. P versus NP OPEN.** This handoff changes no agent identity, status, schedule, or task.

## Exact quantified obstruction

For every valid nonempty duplicate-free proper clause-monotone 3-SAT-(2,2) formula F and coherent partial assignment p, its *nonempty raw syntactic cofactor* F|p is target-valid (up to bijective renaming only) if and only if it is the unchanged union of a nonempty collection of original incidence-connected components that p leaves entirely untouched, while every other source clause is satisfied by p and removed. Thus **a connected target source has no nonempty, canonical, direct raw cofactor child after any nonempty assignment**. Any empty satisfied residual is a SAT terminal, not a canonical child. A residual with an empty clause is an ordinary-CNF UNSAT terminal. This lemma does not constrain semantic compression or target reencoding.

Proof invariant: a surviving variable must retain all four original signed occurrences to satisfy its exact 2+2 quota; each surviving incident clause must retain width three, so its two other source variables survive; closure along incidence edges retains whole original connected components. The converse is immediate. The previous LSPV-4 SURVIVOR-FRONTIER292 restricted one-pivot bound is subsumed for direct raw cofactors.

## SAT and UNSAT adversarial controls

Y6: 6 variables, 8 clauses, connected, 20 models by exhaustive enumeration and 729 coherent partial assignments exhaustively checked. U198: connected original valid UNSAT source, six independent private 42-clause refutations and all 64 boundary assignments. V198: connected original valid SAT source, complete verified 198-bit witness, constructed by swapping first positive occurrences in zero-indexed U198 clauses 1 and 7. U/V 925 coherent cubes each sampled with deterministic seed 293111. All three showed no target-valid nonempty cofactor after nonempty p. Source-signed S/U targets, inversions, SS/SU/US/UU indexed pair matrix, coherent endpoints, changed source clauses, intermediate flips and logical XOR retained. Independent no-producer-import verifier passed **155,397 assertions**; independent FLMV/index checker passed **1,643**.

Sharpness on *both* labels: append a disjoint Y6 component to U198 or V198, obtaining valid 204-variable 272-clause parents. Assignment satisfying the Y6 component deletes it, leaving respectively U198 UNSAT or V198 SAT as a valid canonical child. This is additive elimination, not a fixed-power contraction.

## Exact declared-machine resource accounting

Per 198-variable original source, one indexed read of every original record cost 6,600 read-only source-bit reads, 3,113 index-bit-cell writes, 5,686 index-head steps, 264 atomic index jumps, 15,663 primitive steps, 3,270 cumulative index-tape-content XOR, zero endpoint index XOR, and peak 13 index-tape cells. This is **only the declared record-reader microtrace**, not a full machine-matched SAT run. Check selector discovery and switching, failed attempts, grammar parsing and indexed initialization, child arbitrary-bit output, guest memory, retained ancestor states, replay, witness/certificate checking and simultaneous peak writable/index space on actual implementations. UP-DPLL capped at 300 nodes solved Y6 in 4, while U/V returned UNKNOWN. Their labels come from independent checked evidence, never timeout.

Exact Theorem 5.7 rational checks give d*(6/5)=23/45 and d*(241/200)=11642479/23232400, k=2 uniquely optimal at both, certified all k>=4 via c^-4<d_2. The conditional ARC fixed point (6/5,1/2) is mathematically interior but the complete arbitrary-A->Phi(A) compiler and the quantitative SAT-to-Docker FLMV transport are OPEN. NP-completeness alone does not transfer these exponent margins.

## Explicit handoff by unchanged role

LSPV-1: strengthen the quantified contract by distinguishing certified SAT/UNSAT terminals, disjoint-component cases and noncanonical connected residuals.

LSPV-2: construct and verify a semantically equivalent target-language reencoder for both SAT and UNSAT connected cofactors, with exact source-authenticated arbitrary-bit output; do not repeat the prior grammar-only repair that made U198 UNSAT into SAT.

LSPV-3: challenge charged component recognition, selector access, and global easy connected-template counterexamples; track state-dependent discovery, backdoors and failed routes.

LSPV-4: independently audit candidate emitter source/index-head costs, repeated queries, retries and peak simultaneous space, and preserve strict FLMV Theorem 5.7 boundaries.

LSPV-5: independently referee both directions of the iff theorem and its scope. Verify root synthesis preserves all five ownership regions, prior proofs and P versus NP OPEN.

Formal GitHub report: https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/2026-11-01_0036_LSPV-4_ARC_CONNECTED_COFACTOR293.tex . Compact checker and exact FLMV rational code are in experiments/arc/lspv4_293; public numerical summary is under results/summaries/arc. Full raw and complete code are in the local reproducibility archive, not yet individually mirrored due to container_session_unavailable on persistent Library upload. Independent mathematical review and native full FLMV benchmarks remain pending.

END_OF_VERIFIED_HANDOFF::LSPV4_ARC_CONNECTED_COFACTOR293::P_VS_NP_OPEN
