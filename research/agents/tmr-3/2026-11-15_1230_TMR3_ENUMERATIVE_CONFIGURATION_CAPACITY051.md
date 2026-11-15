# TMR-3/051: Configuration-Capacity Barrier to Lazy Exhaustive Graph Enumeration

**2026-11-15 12:30 PST | TMR-3, Track B | PROVED/RESTRICTED (peer review OPEN), COMPUTATIONAL audit | P versus NP OPEN**

## Candidate and falsifiers (before substantive research)

Candidate: even if the Tree Evaluation routine is improved to space \(\widetilde O(b+B^\alpha)\) with \(\alpha<1\), a deterministic **end-to-end** simulator on a short original input cannot both use \(o(B)\) total writable cells and actually examine \(2^{\Omega(B)}\) distinct computation-graph candidates in sequence. The argument is an application of fixed-machine configuration counting, not a claim about all possible graph generators.

Falsifiers: (F1) computing the true graph directly rather than enumerating guesses defeats any unconditional extension; (F2) an uncharged output tape, message buffer, external clock, or growing number of heads defeats the proposed model; (F3) an explicitly materialized exponential-size read-only Tree Evaluation input can store an exponential head-position counter, so the **original input must have length polynomial in B**; (F4) the number of possible candidate graphs does not prove the chosen algorithm actually processes them all.

## Primary source and duplication audit

Williams, *Simulating Time With Square-Root Space*, arXiv:2502.17779v1 (STOC 2025), Section 3.2, pp. 10-13, constructs block-respecting computations with B=Theta(T/b) time blocks. For a constant number of tapes p, candidate graph motion labels m(h,i) belong to {-1,0,+1}, with O(pB) symbols. Each guessed graph yields an implicitly defined Tree Evaluation instance; inconsistent head motions produce FAIL. The proof enumerates graph guesses and retains O(B) space for this graph and node navigation. It restates the Cook-Mertz Tree Evaluation space O(db+B log(db)) and achieves O(b+(T/b)log b) overall. Williams Section 3.3 already observes that even LOGSPACE Tree Evaluation leaves O(b+T/b) in that construction. Neither source promises polynomial sequential simulation time. Primary: https://arxiv.org/pdf/2502.17779 (Section 3.2, Corollary 3.6); Cook-Mertz STOC 2024 https://doi.org/10.1145/3618260.3649664.

Project precedent: TMR-3/050 draft PR #142 establishes the exact explicit-materialization barrier min_b max(b,ceil(T/b))=ceil(sqrt T), and includes a streamed source control; it does NOT establish a lower bound against graph-free enumeration. TMR-3/015 already proves a fixed-head configuration-capacity envelope. The present result applies this **known** envelope to the new exhaustive-enumeration bottleneck: no explicit record is necessary to force Omega(B) writable space when the actual deterministic run is exponentially long. This is a new scoped application, not a new general counting theorem. The current TMR-1/051 and TMR-5/047 handoffs were checked for related class-target and compression controls.

## Theorem and proof

**Theorem (same-execution enumerative capacity).** Fix a total deterministic uniform machine A with H locally moving read-only source heads, w locally moving writable tapes, finite control Q and finite writable alphabet Gamma, all independent of B. Let the original input x_B have N(B)<=B^c symbols for a fixed c. Suppose A, on that **one halting execution**, actually processes K_B>=2^(kappa B) distinct candidate records sequentially, one or more genuine transitions per record. Count ALL visited writable cells S_B, including storage for messages, work, output, indices and scheduling. Then S_B=Omega(B).

Proof: with total writable footprint S, there are at most (N+2)^H source-head positions. The allocation of visited cells among w tapes and their head positions has at most (S+2)^(2w) possibilities, and their symbol contents at most |Gamma|^(S+w). Therefore a generous complete-configuration upper bound is

\[
C_A(N,S)\le |Q|(N+2)^H(S+2)^{2w}|\Gamma|^{S+w}.
\]

A fixed-input halting deterministic run never revisits a complete configuration, so T+1<=C_A(N,S). Since each candidate is actually processed in sequence, T>=K_B-1 and K_B<=C_A(N,S_B). Thus

\[
\kappa B \le O_A(S_B+\log(N+2)+\log(S_B+2)).
\]

If S_B=o(B) and N(B)<=B^c, the right side is o(B), a contradiction. QED.

**Explicit one-binary-work-tape necessary inequality:** with one read-only source head, q finite-control states and binary writable alphabet, a generous bound is

\[
C(N,S)\le q(N+2)(S+2)2^S.
\]

A full sequential scan of all 3^B ternary words therefore requires

\[
S+\log_2(S+2)\ge B\log_2 3-\log_2(q(N+2)).
\]

This lower bound is on writable space **conditional on the witnessed long run**, not on the correctness cost of any SAT decider. A larger fixed alphabet or fixed number of heads changes constants, not Omega(B).

## New quantitative Track B implication

Suppose an improved constant-arity evaluator promised \(\widetilde O(b+B^\alpha)\) space, alpha<1. Balancing alone would suggest rho=alpha/(1+alpha)<1/2, b=T^rho, B=T^(1-rho). But a simulator that really enumerates 3^(Omega(B)) graph guesses has

\[
S_{\rm sim}=\Omega(B)=\Omega(T^{1-\rho})\gg T^\rho.
\]

At the cube-root target b=T^(1/3), B=T^(2/3), the exhaustive-guess implementation instead needs Omega(T^(2/3)) writable space. This applies **even to a storage-free or recomputation-based enumerator**. It strengthens the scope of /050 beyond explicit graph materialization, without claiming that every simulator must enumerate.

A halting deterministic end-to-end simulator with original N=poly(B) and space O(B^alpha polylog B) has automatically, by configuration counting,

\[
T_{\rm sim}\le2^{O(B^\alpha\operatorname{polylog}B)}.
\]

It cannot perform 2^(Omega(B)) candidate steps. But this remaining upper bound is still generally superpolynomial, so it is not a same-machine FLMV time-space pair.

**Legal escape:** if the genuine movement schedule is a known function of time (e.g. every block moves right), a logarithmic counter can generate the i-th label directly; no graph enumeration is necessary. If a read-only input explicitly contains a candidate schedule, individual labels can be streamed without materializing B writable symbols. Both invalidate any representation-independent graph-storage lower bound. The open task is source-authenticated canonical generation for *non-oblivious adaptive* machines, or a graph-independent joint evaluation that does not iterate exponentially many candidates.

## Full cost ledger

| Resource | Actual accounting |
|---|---|
| Simulated work | T steps, b-bit blocks, B=ceil(T/b); none is automatically actual simulator time |
| Sequential time | Every genuine graph trial and tree evaluation is charged; no free graph choice or zero-cost transition |
| Writable space | All simultaneously live source indices, graph iterators, buffers, output, messages, head state and counters |
| Input size | Original immutable N<=poly(B) with a fixed number of local source heads; cannot import an enormous explicit tree input |
| Sharing/caching/recomputation | Fully allowed; this theorem still applies if the resulting actual trace inspects exponentially many candidates |
| Parallel span | Not a substitute for sequential work; networks require aggregate live workspace and message costs |
| Error or majority | Exact deterministic test only; no probability, interference, oracle or quantum simulation presumed |

**Quantitative finite control:** for B=256, N=512, q=8, the one-binary-tape capacity bound requires S>=386 if the protocol truly examines 3^256 candidate words. At original simulated T=4096 and b=16, this exceeds the proposed cube-root S=16. There is no claim that a correct graph selector needs those trials.

## Four mandatory gates

| Gate | Status |
|---|---|
| DISJ sanity | **PASS.** Rank-to-circuit or rank-to-SAT transfers not invoked. Easy DISJ, Horn and affine families may use a direct selector. |
| Relativization | **NOT APPLICABLE WITH REASON** to a separation, since none is claimed. The fixed-input configuration count is model-relative and not a nonrelativizing P-vs-NP proof. |
| Simultaneous DTISP | **PASS** for one declared machine/execution in the conditional enumeration theorem; **OPEN** for any polynomial-time SAT/FLMV transfer. |
| Configuration counting | **PASS.** Used as an upper bound only after an independent architecture-specific lower bound on actual number of transitions. |

No Natural Proofs, algebrization or static-rank transfer is used. Genuine cheap paths remain legal. Historical /341 FAIL as full UNSAT authority and /386 RESTRICTED.

## Reproduction, publication, next lemma

Self-contained deterministic Python 3 audit, two byte-identical executions: **267,176 exact assertions**, zero failures. Exhaustive ternary words B=1..10; exact binary-one-tape configuration floors B=1..200; cube-root scenarios; 2^B motion-source traces B=1..16; direct indexed read-only schedule controls B=1..255. No randomness. These tests are COMPUTATIONAL, while the asymptotic implication has the short proof above. No native low-level TM, Lean formalization, full checkout preflight, or general SAT machine was executed.

Artifacts: report research/agents/tmr-3/2026-11-15_1230_TMR3_ENUMERATIVE_CONFIGURATION_CAPACITY051.md; code experiments/tmr/tmr3_configuration_enumeration051.py; raw results/raw/tmr/2026-11-15_1230_TMR3_ENUMCAP051_PY_RAW.json; compact handoff research/agents/tmr-3/handoff.md.

**NEXT:** a canonical graph-selector or graph-independent compressed evaluation lemma, explicitly authenticating input-dependent head trajectories with bound on number of source accesses, same-machine sequential work, retained workspace and all interface conversions. A true graph's existence alone does not give such an algorithm.

Root proof1.txt and project protocols were examined; proof2.txt and main.tex gave SHA metadata but empty content via the connector. No root/shared tracker updates without complete source. TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE. All five existing schedules and ownership unchanged. **P versus NP OPEN.**