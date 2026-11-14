# TMR-1/012: additive-linear copy simulation and an exact unrestricted-head quantifier bridge

**Date:** 2026-11-13 22:04 PST (America/Los_Angeles). **Role:** TMR-1 Machine Model Lead. **Repository:** j15marti/pnp, main.

**Scientific status:** New lemma TMR1-CH12 **CANDIDATE**, pending independent TMR-5/TMR-4 review. The finite replication audit is **COMPUTATIONAL**. This is a standard-type machine simulation with a self-contained constructive proof, not an unconditional SAT time lower bound. P versus NP **OPEN**.

## 1. Scope and concrete model

For each integer h >= 1, define M_h as the class of fixed, finite, total, deterministic multitape decision machines with exactly h independent *read-only input heads* and an arbitrary but fixed finite number r >= 0 of standard read/write work tapes. The input source is the unchanged binary word x of exact encoded length L, presented between left and right endmarkers at cells 0 and L+1. All h input heads initially rest on the left endmarker. At each counted transition, all input heads read their current pre-move symbols and may stay or move by one adjacent cell, without crossing the endmarkers. All original work tapes are initially blank; work-head visits, work writes, preprocessing, output and input rereads count. The alphabet and control are finite and independent of L. Invalid encoded 3-CNF strings must be handled by the same total decision procedure. The model accommodates both SAT and UNSAT terminal labels, not a one-sided recognizer.

This is a *model of original source access*, not the class of arbitrary unit-cost indexed reads. It is also not a one-way streaming restriction, a fixed-space promise or a bound on the number of times an input bit may be read.

The integer h is a fixed machine-description parameter, not h(L). L denotes **all encoded source bits**, not variable count, clause count, number of constraints or bit complexity of a witness.

## 2. New substantive lemma TMR1-CH12: linear-cost multihead elimination

**Claim (CANDIDATE pending peer review).** For every A in M_h there exists one **fixed** total deterministic machine B_A in M_1, with h additional writable work tapes, such that for every binary input x of length L:

$$
\operatorname{out}_{B_A}(x)=\operatorname{out}_A(x),\qquad
T_{B_A}(x)=T_A(x)+2L+3
$$

under the explicit copy/rewind convention below, and

$$
S_{B_A}(x)\leq S_A(x)+h(L+2)+c_A .
$$

Here S counts the total number of visited writable cells on all tapes; c_A covers any fixed auxiliary control/output convention. If terminal bookkeeping is implemented within the terminal transition, one step of A is precisely one step of B and no per-step overhead appears. The construction is uniform in all source lengths. In less rigid tape conventions the conclusion is the same with $T_B\leq c_A(T_A+L+1)$ and $S_B\leq S_A+c_A(L+1)$.

**Construction.** B_A has one original read-only input head, copies A's h read-only heads onto h *writable but subsequently unchanged* work tapes, and preserves A's r ordinary work tapes. Initially these h work heads and the physical source head are at cell 0. During L+2 counted transitions B reads, then simultaneously writes, one original source/endmarker symbol into each of h copy tapes. It moves to the next cell except after reading the right endmarker. Because all h writes happen in one multitape transition, the charge is L+2, not h(L+2) time. Next it moves the h copy heads in parallel leftward for exactly L+1 transitions until all are at their stored left markers. This does not move or change A's original work tapes. Thus initialization costs (L+2)+(L+1)=2L+3 transitions and touches exactly h(L+2) copy cells.

B now uses A's original finite transition function on the h copy-tape symbols and r original work-tape symbols. Every simulated step leaves the copy symbols unchanged, moves their heads as A moves its input heads, writes and moves the r original work tapes exactly as A does, and advances A's finite control. One B step realizes one A step because there is one work-tape head corresponding to each original input head. The original physical read-only head stays parked at the right endmarker. By induction on simulated transitions, A and B share the exact control, all h virtual source-head coordinates, all r original work-tape head coordinates and symbols, and the terminal output. Since A is total, B is total. No oracle, advice, lookups, per-length programs or uncharged memory occurs.

The construction does not need A to be correct on malformed inputs in any particular way except that it halts and obeys its declared specification there; it copies and simulates malformed binary inputs as well. The original 3-CNF encoding and both valid label classes are unmodified.

**Space caveat.** B's copy tapes consume h(L+2) visited writable cells even if A used O(1) work cells or read just one original bit. Consequently this theorem preserves all-polynomial time lower-bound questions but **does not preserve small-space hypotheses**. Applying a one-input-head T*S inequality to B after copying may yield no useful constraint on T_A, because S_B includes the full source copies.

## 3. Exact quantifier-preserving transfer

Define the correct-uniform-target Q_h:

$$
\forall A\in M_h\text{ correct total},\
\forall k\in\mathbb{Z}_{\geq1},\
\forall C>0,\
\forall L_0,\
\exists\text{ valid }F:
|F|\geq L_0,\quad T_A(F)>C(|F|+1)^k.
$$

**Consequence of TMR1-CH12:** Q_1 implies Q_h, for every fixed h, with the **same exponent k**. Fix any A,k,C,L_0 and construct its one-head simulator B_A. Apply Q_1 to B_A at k, L_0 and C_B=C+3, obtaining a valid F with

$$
T_{B_A}(F)>(C+3)(L+1)^k.
$$

The exact simulation bound gives $2L+3\leq3(L+1)^k$ for every L >= 0 and integer k >= 1. Therefore

$$
T_A(F)=T_{B_A}(F)-(2L+3)>C(L+1)^k.
$$

The hard formula is allowed to depend on A,k,C,L_0, exactly as required. Conversely Q_h implies Q_1 because any one-head decider may be represented as a h-head decider with h-1 unused stationary heads. Thus Q_h and Q_1 are equivalent as **unrestricted all-polynomial-exponent time objectives** in this bounded local-head family. This does not prove either assertion. A finite bound on the resource cost of source copying is the actual transfer arrow; restating Q_1 without it would be circular.

For any individually certified bound $T_{B_A}(F)\geq g(L)$ on the constructed simulator, the only direct consequence is

$$
T_A(F)\geq g(L)-(2L+3).
$$

Therefore an Omega(L) one-head observation bound can be entirely paid by copying before A begins, and does **not** automatically lower-bound the multiple-head A. By contrast, a certified superlinear lower bound on B_A survives the additive O(L) correction in the same realization.

## 4. Precise dependency DAG and research implications

- **Input model specification** and finite fixed h, finite tapes, endmarkers, both-label totality [this report].
- **Copy/rewind simulation** for every concrete A transition [constructive argument above].
- **Uniform bound and Q_1 to Q_h** [algebra above, conditional on the simulation lemma].
- **Actual one-head all-exponent SAT lower bound Q_1** [OPEN].
- **Representation-independent 3-SAT bottleneck / P != NP** [OPEN].

The result directly narrows TMR-1's multiple-source-head model bridge. It does not remove the obstacles to extending source-observation potentials (TMR-4/012) into post-acquisition computational potentials or to proving physical TMR-3/008 crossing/splice premises. In particular, the O(L) source-copy overhead leaves complete source summaries on writable tapes. A proposed restricted input-interleaving lower bound must apply to this copied representation and charge its full S_B before inferring anything about A. TMR-2's mask certificate count and TMR-4's source-transport lower bounds remain correctly restricted and cannot be promoted to processing lower bounds from this lemma.

## 5. Reproducible finite test and hostile controls

**Executed in hosted JavaScript/V8:** experiments/tmr/tmr1_input_head_copy012.cjs. Every binary source x with lengths 0 through 8 was used. For h in {1,2,3} and 12 fixed synthetic deterministic transition programs each executing 23 simulated steps on two mutable work tapes, compare the original h-head trace against the frozen-clone replay on h work tapes. Each mode and head-count pair denotes a fixed bounded finite-control total machine across all lengths (the fixed step budget can be encoded into its control); these synthetic machines **do not decide 3-SAT**. The harness verifies every step's observed symbols, control, simulated head positions and original work-tape visits, plus the copy/rewind charge.

Result: **18,396 complete source/program/head-count executions, 423,108 simulated transitions, 8,371 accepting and 10,025 rejecting outputs, zero trace mismatches, zero accounting failures.** Maximum tested initialization charge 19 at L=8. Empty source, both labels and head boundaries were included. Failure on a cloned source read or charge inequality aborts the harness. The raw JSON is separately stored at results/raw/tmr/2026-11-13_2204_TMR1_INPUT_HEAD_COPY012_RAW.json. There was no native-Node replay, physical general 3-SAT decider, arbitrary-bit RAM simulation, or full LaTeX compile. The theorem is symbolic and all-length; the finite tests remain COMPUTATIONAL.

**Hostile interpretations checked:** (i) An extra input head is not free computation because it needs a charged source copy in B. (ii) A small-space restriction is not preserved by source copying. (iii) A one-head Omega(L) lower bound cannot force an h-head Omega(L) time bound via this construction. (iv) Gaussian elimination, Horn, 2-SAT, bounded-treewidth, direct products, sharing, source padding, renaming, auxiliary variables and caching/recomputation are all permitted inside A and simulated unchanged, though no specialized family classifier was executed in this run. (v) An h growing with L or genuinely unit-cost random access is outside the theorem. (vi) Nonuniform h(L) input tapes or prefilled work tapes are outside the initially blank fixed-machine contract.

## 6. Source verification and corpus

Primary classical context, **not** a claim of originality for general model invariance:
1. Hartmanis and Stearns, "On the computational complexity of algorithms", *Transactions AMS* 117 (1965), 285-306, DOI https://doi.org/10.1090/S0002-9947-1965-0170805-7.
2. Hennie and Stearns, "Two-tape simulation of multitape Turing machines", *JACM* 13(4) (1966), 533-546, DOI https://doi.org/10.1145/321356.321362. Its published abstract describes a different multi-*work*-tape simulation theorem; it is not being misquoted as the proof of the explicit multi-*input*-head additive-linear result here.

Read first: research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md. Also read complete proof1.txt (28,714 chars, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343) and authentic recovered proof2.txt via Git blob (1,051,196 chars, SHA 930c5eeddafce656717f28055a7a9a755f44737c); recovered authentic main.tex via Git blob (2,511,782 chars, SHA c04a02a97492f88938791f363ff91d99b67cd78b); issue #3 through TMR-5/009; AGENTS.md, CODEX.md, pnp-research skill, all five current TMR handoffs, original TMR-1/011, TMR-2/011, TMR-3/010, TMR-4/012, TMR-5/009, and historical original LSPV-4/149 multihead firewall. Superseded LSPV ownership instructions are not active. Both trackers were fully recovered and reviewed with **NO MATERIAL CHANGE**. Canonical main.tex is TMR-5's whole-document synthesis responsibility; this result is handed off rather than replacing or rewriting any historical section.

## 7. Next target

Have TMR-5 independently check the exact finite-control copy/rewind simulation and quantifier preservation. Then isolate whether TMR-3's physical crossing-sequence/splice hypothesis remains valid for the special one-head machine B_A that carries h fully copied writable source tapes. If the restricted bound is absorbed by S_B = Omega(L), record the exact exhausted proof arrow and seek a processing invariant whose strength persists when the entire source is explicitly materialized. Do not infer P != NP from Q_h equivalence.

END_OF_REPORT::TMR1::2026-11-13_2204_PST
