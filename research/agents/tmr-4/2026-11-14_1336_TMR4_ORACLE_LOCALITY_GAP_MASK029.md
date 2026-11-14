# TMR-4/029: Adaptive evaluation-locality obstruction for SAT-to-Gap-MCSP

**Date:** 2026-11-14 13:36 PST (America/Los_Angeles). **Owner:** TMR-4 Cost-Sound Abstraction. **Status:** NEW **PROVED/RESTRICTED** elementary theorem, independent peer review OPEN; finite tests **COMPUTATIONAL**; P versus NP **OPEN**.

## 1. Novelty, preflight and prior-work ledger

**NEW compared to previous TMR-4/027-028, TMR-1/027 and TMR-2/028:** an exact lower bound on **source-independent, adaptive, nonlinear evaluation-oracle SAT-to-Gap-MCSP transformations**. Each target bit may be computed by its own adaptive q-query decision tree, but some unique-witness source will remain within normalized Hamming distance q/2^v of the transformed zero source. The bound is tight as a distance-to-reference statement, not as a full Gap-MCSP reduction.

First read `research/coordination/2026-11-14_MCSP_FIVE_AGENT_REVIEW.md` on main, SHA 1e11aa64a0b0d635a65cea58500b09f2b0fe010a; next the 2026-11-13 TMR replacement directive. Read AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, both proof trackers, canonical main.tex, all five newest TMR handoffs, issue #3 through TMR-3/028 and relevant original reports. Authentic complete Git blobs recovered for `proof2.txt`, 1,051,196 characters, SHA 930c5eeddafce656717f28055a7a9a755f44737c; `main.tex`, 2,545,859 characters, SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. Blank GitHub Contents API bodies are not empty files. `proof1.txt` readable, 28,714 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343. **TRACKERS REVIEWED; NO MATERIAL CHANGE.**

| Relevant ORIGINAL source path | Prior scoped status |
| --- | --- |
| `research/agents/tmr-4/2026-11-14_1142_TMR4_GAPMCSP_AFFINE_KERNEL_CYLINDER027.md` and `experiments/tmr/tmr4_affine_kernel027.py` | Fixed affine sketch Hamming-gap collisions, PROVED/RESTRICTED; not adaptive nonlinear output |
| `research/agents/tmr-4/2026-11-14_1243_TMR4_LENGTH_BLIND_FIXED_GATE_COFACTOR028.md` and `experiments/tmr/tmr4_fixed_gate_stream028.py` | Constant-threshold MCSP online cofactor inheritance, PROVED/RESTRICTED |
| `research/agents/tmr-1/2026-11-14_1307_TMR1_MCSP_GROWING_THRESHOLD_ENUMERATION027.md` | One-work-tape upper at s=Theta(n/log n), restricted |
| `research/agents/tmr-2/2026-11-14_1322_TMR2_GROWING_MCSP_PERIODIC_CODE028.md` | Maximal YES query depth but cheap special-language recognition, restricted |
| `research/agents/tmr-3/2026-11-14_1327_TMR3_MCSP_RAWSCAN_HEADER_BOUND028.md` | One-tape enumeration and distinct upfront-header model, restricted |
| `research/agents/tmr-5/2026-11-14_1259_TMR5_BOUNDED_ENVELOPE_REVIEW024.md` | Bounded-threshold envelope; candidate/restricted |
| `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex` | Prior scoped one-tape and portfolio audits, no unrestricted transfer |
| `research/agents/threshold-descent/2026-10-18_1416_THRES_HASHBRIDGE4.tex` and `research/agents/threshold-descent/2026-10-18_1902_THRES_HASHIMAGE_SATURATION9.md` | Prior affine/hash obstructions, not new herein |

Earlier Walsh/moment, signed/hypergraph, semantics, cheap Gaussian-elimination, normalizer and checker counterexamples remain restricted controls. This result does not repair or erase accepted counterexamples.

## 2. Primary-source theorem/hypothesis matrix

| Paper, exact location | Input/threshold/model | Statement and status |
| --- | --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, **Theorem 1, p. 23:3** | Ordinary **exact** MCSP[2^{mu n}], N=2^n **full** table; fixed deterministic machine with one-way read-only input plus one two-way read/write work tape; some small fixed mu>0 | If MCSP is **outside** DTIME_1[N^{1.01}], **P != NP**. Hypothesis OPEN. |
| Same paper **Theorem 2, p. 23:3** | Same full table, randomized two-sided error, a **different larger** mu near 1 | Unconditionally MCSP[2^{mu n}] is outside BPTIME_1[N^{1.99}]. Cannot silently substitute this threshold into Thm 1. |
| McKay, Murray, Williams, STOC 2019 **Theorems 1.2-1.3, pp. 2-3** | **Search**-MCSP^A[s(n)] with oracle-gate circuits, s(n)>=n, N=2^n full truth table; one-pass streaming with short Sigma_3SAT^A oracle queries in Thm 1.2 | Theorem 1.2 gives tilde O(s) space, tilde O(s^2) update and tilde O(s)-length oracle queries; Thm 1.3 says failure of poly(s) streaming solution for some A in PH implies P != NP. Different from ordinary exact decision MCSP. |

Sources verified from publisher/author original PDFs, with page images: https://doi.org/10.4230/LIPIcs.STACS.2021.23 and https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf. The Hamming-gap promise defined below is **our explicitly scoped definition**, not an assumed identification with every Oliveira-Santhanam or Oliveira-Pich-Santhanam variant.

## 3. New theorem ORACLEGAP29: adaptive query-locality

Let v>=1, M=2^v, N>=1, and an unknown f:{0,1}^v->{0,1} be accessible only through an evaluation oracle. A **source-independent** deterministic transformer outputs y(f) in {0,1}^N. Each target coordinate j is computed by a fixed (for v,N,j) arbitrary nonlinear **adaptive** decision tree making at most q evaluations of f. Local tree logic can depend on previous returned answers, but cannot access a syntactic description of f, uncharged globally shared source-dependent preprocessing or nonuniform witness advice.

Let 0 be the everywhere-zero source function, and let f_a be the singleton function which equals 1 only at assignment a. Then

$$
\boxed{\sum_{a\in\{0,1\}^v}d_H(y(f_a),y(0))\le Nq.}
$$

Consequently some singleton satisfies

$$
\boxed{\frac{d_H(y(f_a),y(0))}{N}\le\frac{q}{2^v}.}
$$

**Proof:** For every output bit j, run its query tree on 0 and record the set Q_j of coordinates it queries on that all-zero response path, with |Q_j|<=q. If a is absent from Q_j, running the same adaptive algorithm on singleton f_a follows exactly the same transcript, query by query, hence produces exactly the same j-th output bit. Thus at most |Q_j| singleton sources can change bit j. Double count source/output disagreements:

$$
\sum_a d_H(y(f_a),y(0))
\le\sum_{j=1}^{N}|Q_j|\le Nq.
$$

Average over M=2^v assignments. This proves both inequalities, even with arbitrary nonlinear answer-dependent query selection. QED.

### Scoped Hamming-gap corollary

Define `GapMCSP^{Ham}_{n,s,eta}` on a **full** length-N=2^n truth table: YES if its minimum Boolean circuit size CC_n is <=s; NO if its relative Hamming distance from **every** circuit of size <=s is >=eta; other instances are outside the promise. Assume y(0) has CC_n<=s. If every singleton satisfiable source f_a must map to a **promised NO**, then distance from y(0) must be >=eta N, forcing

$$
\boxed{q\ge eta\,2^v.}
$$

Even if N is increased, N cancels. In particular polynomially many evaluation queries **per target bit** cannot ensure constant or inverse-polynomial-in-v robust Hamming separation for all unique-witness instances.

**Sharpness only for the reference distance:** If N is a multiple of M and 0<=q<=M, let y_j(f) be the OR of q values f((j+t) mod M), t=0,...,q-1. Each singleton gives exactly Nq/M changed bits relative to y(0)=0^N. This meets the double-count bound exactly, **but no hardness against every small circuit is implied**.

**Scope firewall:** A genuine SAT reduction receives the explicit formula **syntax**. It may preprocess, discover easy unique witnesses from unit clauses, select queries depending on syntax, globally share computations, use algebraic representations, or even use a different function of the formula. This source-independent black-box theorem DOES NOT rule out such transformations and DOES NOT establish a time lower bound for arbitrary SAT algorithms. The exact unrestricted cost-sound bridge remains OPEN.

## 4. Exact SAT-to-complement-MCSP[0] construction and its exponential cost

For any 3-CNF F on v variables, encoded in L bits, define

$$
h_F(x,u,w)=F(x)\wedge u\wedge w.
$$

Its **complete** truth table has n=v+2 inputs and length N=2^{v+2}. Generating that table takes O(N poly(L)) time and N output bits. Constants and input wires are free; AND/OR/NOT gates count.

If F is UNSAT, h_F is constant zero, so CC_n(h_F)=0. If F is SAT, fix a satisfying x=a. Its restriction to (u,w) is u AND w, which is **not** realizable with zero gates, so CC_n(h_F)>0. Hence **SAT maps to the NO label of ordinary exact MCSP[0]** and UNSAT to YES, but with potentially **superpolynomial output length in source L**. This does **not** give a polynomial-time reduction or a P-vs-NP consequence.

When F has exactly one satisfying assignment, h_F has Hamming weight **one**, hence distance from the zero table exactly 1/N. It is **not** a promised NO of our Hamming-gap problem when eta>1/N. Appending t dummy input variables repeats the table 2^t times, increasing N to 2^t N but preserving the relative weight **1/N**. Naive padding does not amplify the gap. No circuit-minimization oracle or free truth-table expansion has been used.

This is a concrete **failed implication** for SAT clause-evaluation composition as a Gap-MCSP transfer. It does not say that ordinary MCSP[0] is NP-complete: the transformation is not polynomial time in L, and ordinary MCSP[0] itself has a cheap decider.

## 5. Reproducible finite verification

Exact executed native CPython source: `experiments/tmr/tmr4_oracle_gap029.py`, SHA-256 a90975128b1156747f25f135458f9551b0a34697ad640d08c9df94f74ac5d476.
Immutable stdout: `results/raw/tmr/2026-11-14_1336_TMR4_ORACLE_GAP029_RAW.json`, SHA-256 fee34d495a28b42e193716430504c803b968ab0b27711c6dcbb5f96ac74dd037.

Executed 65,814 exhaustive small source function classifications (v<=4), 5,586 cyclic sharpness checks, 160 seeded adaptive decision-tree suites with 162,660 singleton-output comparisons, and 60 dummy-padding checks; **zero failed assertions**. The oracle-code simulator is a finite semantic proxy, **not** a native physical finite-state Turing machine. The asymptotic theorem follows from the preceding symbolic double count, not from these tests.

## 6. Exact proof-chain gap, retirement and next target

The attempted route

$$
\mathrm{3SAT}\longrightarrow \mathrm{GapMCSP}[s,eta]
\longrightarrow \mathrm{MCSP}[N^\mu]\text{ one-work-tape time lower bound}
\longrightarrow P\ne NP
$$

has **OPEN/FAILED** arrows: (i) the direct table has N=2^{v+2} output bits, not a poly(L) reduction; (ii) sparse witnesses do not meet a robust Hamming NO promise, with q>=eta2^v needed in the source-independent evaluation-local model; (iii) there is no demonstrated promise-preserving reduction to **ordinary exact** small-mu MCSP with a charged single-tape machine simulation; and (iv) no arbitrary-machine time lower bound at the CHMY threshold has been proved. **RETIRED only as a source-independent local-evaluation architecture**, not as a universal claim that Gap-MCSP reductions cannot exist.

**Next concrete target:** investigate source-dependent syntactic preprocessing or globally shared probes and whether robust gap amplification can be achieved without already deciding SAT, with exact L-to-N blowup and both-label preservation. Request TMR-2 independently check the adaptive zero-path proof and strict-proper-3CNF unique-witness encoding, TMR-5 implement independent balanced-cyclic controls and hostile counterexamples, TMR-1 audit the exact target promise/threshold, and TMR-3 charge output/input interfaces. All unrestricted P!=NP arrows **OPEN**.

No schedules/identities modified; no root tracker or canonical main.tex changes.
