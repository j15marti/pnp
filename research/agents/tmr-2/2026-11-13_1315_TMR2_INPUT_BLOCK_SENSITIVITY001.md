# TMR-2 INPUT-BLOCK-SENSITIVITY-001: all-machine source-acquisition lemma and failed streaming-space transfer

**TMR-2 REPORT::INPUT-BLOCK-SENSITIVITY-001::2026-11-13T13:15:00-08:00**  
**Research scope:** j15marti/pnp, main, TMR-2 Information Necessity.  
**Scientific status:** CANDIDATE (complete elementary symbolic proofs below, independent TMR-5 review pending); COMPUTATIONAL (executed bounded controls); unrestricted superpolynomial SAT-time bound OPEN. P versus NP OPEN.

## 1. Candidate and predeclared falsifiers

Candidate D2: Identify a genuinely necessary, input-aware operation in **every fixed correct total uniform deterministic multitape 3-SAT decider**, regardless of compact representations, arbitrary work tapes, algebraic computation, or rereading the read-only input.

Three possible falsifiers: (F1) an opposite-label perturbation is not a valid same-length proper-3CNF source; (F2) a correct machine can distinguish opposite labels without reading any changed input coordinate; (F3) a one-pass retained-state lower bound also constrains a machine that can revisit original input. F1 and F2 fail for the precise lemma below; F3 succeeds as a counterexample to a proposed unrestricted-space transfer.

**Duplication audit:** The project already proved the underlying equality-family construction and single-tape crossing-sequence phenomena in research/agents/claude/onetape/SOURCE_note1_onetape_lower_bound.txt, SOURCE_note2_tightness_and_limits.txt, and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex. The present incremental contribution fixes TMR-1's exact **proper 3-CNF binary source encoding**, proves **2n disjoint sensitive sign-blocks on every single satisfiable equality instance**, and formalizes its exact unrestricted-machine first-access scope. We claim no conceptual priority for equality or communication lower bounds.

## 2. Exact machine and source model

Use TMR-1's fixed binary input grammar: a header of N ones, 0, M ones, 0, then M ordered triples. Each literal is one sign bit (0 positive, 1 negative) plus a zero-based variable index of width

$$w=\max(1,\lceil\log_2 N\rceil).$$

There must be exactly three **distinct** variables in every clause and no trailing bits. Let L be the full bit length, not the number of variables or clauses. The decider is a single finite total uniform deterministic multitape machine, with one two-way read-only input tape, a fixed number of writable work tapes and a finite alphabet. A transition observes at most one input symbol. Both SAT and UNSAT are classified correctly on every valid source; malformed inputs reject. All input head motions, work and rereads cost actual transitions.

### Lemma TMR2-1: disjoint opposite-label perturbations force physical input acquisition

Let x be any binary input of length L, and let nonempty sets B_1,...,B_r of input coordinates be pairwise disjoint. Suppose each x^(i), made by complementing precisely B_i, is valid and has the *opposite* language label from x. On the computation of x, every correct deterministic machine must read at least one original input coordinate in each B_i, hence at least r distinct input positions and at least r input-observing transitions.

**Proof.** Suppose B_i is never read on x. Run the same deterministic program on x^(i). Every cell observed along the original execution has identical symbols on the two inputs. By induction on transitions, controller, work-tape contents, all head positions and the eventual halting label coincide. This violates the required opposite language labels. Disjointness implies at least r distinct physically observed positions. QED.

This argument includes arbitrary algebraic summaries, additional writable work tapes, adaptive rereads, cache/recomputation, and source copying. It does **not** establish a memory-space bound. Since r<=L, this entire kind of first-input-acquisition argument has a **linear ceiling** in encoded bits.

### Lemma TMR2-2: 2n disjoint essential sign-blocks on one strict-3CNF SAT input

For each n>=1, take five disjoint n-variable banks: x_i; prefix auxiliary p_i,q_i; suffix auxiliary r_i,s_i. For a literal ell on x_i and fresh u,v, define the exact four-clause proper-width-three gadget

$$
U(\ell;u,v)=(\ell\lor u\lor v)\land(\ell\lor u\lor\neg v)
\land(\ell\lor\neg u\lor v)\land(\ell\lor\neg u\lor\neg v).
$$

When ell is true all clauses hold. When false, exactly one of the four choices of signs on u,v is violated, whatever u,v are. Thus U is equivalent to the unit constraint ell.

For a,b in {0,1}^n let ell_i(a)=x_i for a_i=1 and negated x_i otherwise. Construct ordered

$$
E_{a,b}=\bigwedge_{i=1}^n U(\ell_i(a);p_i,q_i)
\land\bigwedge_{i=1}^n U(\ell_i(b);r_i,s_i).
$$

There are N=5n variables, M=8n actual proper three-literal clauses, with the 4n prefix clauses before the 4n suffix clauses. The complete encoding is

$$
L(n)=13n+2+24n\bigl(1+\max(1,\lceil\log_2(5n)\rceil)\bigr)
=\Theta(n\log(n+1)).
$$

**Exact semantic claim:** E_(a,b) is SAT iff a=b: prefix units force x_i=a_i and suffix units force x_i=b_i for every i. This is **not** a general algorithmic hardness result.

For each satisfiable E_(a,a), flip the sign bit on x_i in all four prefix clauses for one i. No other input bit, including variable indices, changes, and the resulting same-length proper source is E_(a xor e_i,a), UNSAT. The analogous four suffix sign bits produce E_(a,a xor e_i), UNSAT. All 2n sets of four sign-bit positions are pairwise disjoint. By Lemma TMR2-1,

$$
\forall A\in\mathcal D_{\rm 3SAT}\ \forall n\ge1\
\forall a\in\{0,1\}^n:\quad
T_A(E_{a,a})\ge 2n.
$$

The quantified machine A is one fixed total deterministic decider correct on **all** binary inputs and lengths. This theorem holds for each individual SAT input E_(a,a), not for a collection of distinct worst-case witnesses. It proves only Omega(L/log L) time against the declared bit representation and no superpolynomial claim.

### Lemma TMR2-3: one-way memory lower bound is a model restriction, not unrestricted 3-SAT space

Consider a deterministic one-pass source-stream machine whose head cannot move left and whose prefix information after the 4n initial clauses must reside entirely in its finite control and writable state. Different a require different post-prefix configurations: if a != a' produced the same, the common suffix b=a would make E_(a,a) SAT and E_(a',a) UNSAT, but the same post-prefix state plus the same suffix would yield identical output. So at least 2^n post-prefix configurations are needed. With a fixed alphabet and fixed tape count, S writable cells offer at most

$$
|Q|\,(S+1)^{O(1)}\,|\Gamma|^{O(S)}
$$

configurations, whence S=Omega(n) on that single-pass model. This is the familiar deterministic one-way equality argument.

**Exact failed transfer.** An ordinary two-way-read-only-input machine can recognize the rigid E-family with O(log L) writable cells (check the constant-size clause pattern, fixed indices and repeated signs using binary counters), then compare for each i one prefix and one suffix sign by re-scanning the immutable source. Repeated scans cost at most O(L^2 log L) transitions with counters and O(log L) writable cells. It can make an initial pass over every prefix **without retaining any prefix sign**, arriving at the same control/work state and input-head boundary across all a, before revisiting input. Equal workspace states therefore do **not** imply indistinguishable continuations for offline machines. Their complete configurations include the different read-only input tapes.

To make this a fixed total *all-input correct 3-SAT decider*, take any fixed exhaustive total 3-SAT decider D; first recognize the special E-family with the cheap rigid parser, solve it by repeated scans when recognized, otherwise run D. This is a single uniform correct program on every length. Its fast path uses O(log L) space on E, but **no polynomial worst-case upper bound** is claimed for non-E inputs. One-pass streaming memory cannot be imported as an unrestricted machine-space lower bound.

## 3. Executed finite evidence

Published executable Node.js runner:
experiments/tmr/tmr2_strict3_input_block_audit.cjs

Published immutable raw:
results/raw/tmr/2026-11-13_1315_TMR2_STRICT3_INPUT_BLOCK_RAW.json

The exact runner was executed in a fresh V8 module with no packages and no randomness. It constructed **all 1,364 ordered pairs (a,b) for n=1,2,3,4,5**; validated strict proper three-variable clauses and bit lengths (111,268,401,630,787); checked **101,952** exhaustive local signed-gadget truth-table assertions; independently brute-forced **20 full formulas** for n<=2 (including SAT and UNSAT); and verified **516** four-sign-bit, same-length perturbations that turn equal-pair SAT instances into different-pair UNSAT instances. All assertions passed. Exact logged counts and reproducible Node source are in the two linked repository files. A separate local Python implementation independently matched the 1,364/20/516 counts but its local-only file is **not claimed** to be published evidence.

**Controls and limitations:** sign flips leave all variable IDs and clause syntax intact; either side can be flipped; every helper gadget is truth-table verified; no hidden auxiliary setting satisfies a false unit. Noncanonical reorderings and arbitrary variable renamings may leave the rigid syntax and are handled only by the exhaustive fallback, not by an asserted universal cheap algorithm. Horn, 2-SAT, affine/XOR/Tseitin, bounded treewidth, products and padding have easy special-case interpretations and remain mandatory falsifiers of a proposed superlinear distinction cost. This lemma never assumes they are hard. Original-source copying as in TMR-1 N2 cannot avoid **one** necessary read from each sign block, but it invalidates uncharged repeated original-head movement arguments.

**Not executed:** native OS Node replay of the published runner, full repository preflight and report-validator scripts, formal TM state-by-state implementation, independent TMR-5 proof review, or any unconditional 3-SAT time-bound experiment. The V8 controls are finite COMPUTATIONAL evidence, not an asymptotic proof.

## 4. Corpus and primary literature

[1] H. T. Vu, *Revisiting maximum satisfiability and related problems in data streams*, Theoretical Computer Science 982 (2024), 114271, https://doi.org/10.1016/j.tcs.2023.114271. Its Theorem 2 establishes stronger single-pass k-SAT memory bounds in its own streaming model, not bounds on a conventional two-way-input machine.

[2] C.-N. Chou, A. Golovnev, M. Sudan, S. Velusamy, *Sketching Approximability of All Finite CSPs*, Journal of the ACM (2024), https://doi.org/10.1145/3649435. Relevant restricted streaming/CSP research; no unrestricted Turing-machine time inference.

[3] Earlier project notes: research/agents/claude/onetape/SOURCE_note1_onetape_lower_bound.txt; SOURCE_note2_tightness_and_limits.txt; research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex. Existing equality-family and crossing-sequence facts have priority over the present special-case formalization.

[4] TMR-1 report research/agents/tmr-1/2026-11-13_1307_TMR1_MACHINE_SLICE_FIREWALL001.md and its handoff.md, especially N1/N2 (uniform program, source-copy firewall).

Reading completed: authoritative five-agent replacement directive first; root proof1.txt blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343; root proof2.txt blob 930c5eeddafce656717f28055a7a9a755f44737c; root main.tex blob 600f00f4bfaf05d09c136c40edc6e22f1cce9d96; AGENTS.md, CODEX.md, repository research skill, current issue #3, TMR-1 original report/handoff, and relevant previous Claude/LSPV artifact. The large proof2 and main content was fully recovered via Git blob API after ordinary file fetch gave blank content despite a valid SHA. No destructive rewrite.

## 5. Dependency/transfer verdict and next target

For every correct deterministic machine, **some information acquisition is necessary**, as a physical read from every disjoint label-sensitive sign block, but its maximum possible count is at most encoded input length L. Exponentially many possible semantic assignments do not force the machine to retain exponentially many bits. A one-way cut gives Omega(n) streaming space only because returning to the prefix is forbidden. It provides no repeat-processing necessity for unrestricted multitape 3-SAT.

The new lemma fills a **restricted, low-strength instance** of TMR-1's D2 information-acquisition obligation and explicitly **fails** to close D4, the all-polynomial-exponent bottleneck. Proof1 P1-01, P1-03, P1-04 remain OPEN. Proof2 P2-D1, P2-C3, P2-B1, P2-B2/B3 remain OPEN. P versus NP remains OPEN.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Neither root proof tracker was edited. Root main.tex not edited: no TMR-2-authorized section exists and TMR-5 owns whole-document synthesis.

**Next specific research target:** define and falsify a **charged repeated-distinction** invariant that can establish computation after first source acquisition, survives arbitrary rereading, input copying, Gaussian elimination, compact algebraic global invariants, and the trivial rigid equality family. Ask TMR-5 to review the exact bit positions, TMR-3 to audit any claimed repeat/crossing charge, TMR-4 to include such events in every concrete machine transition.

**END_OF_VERIFIED_REPORT::TMR-2::INPUT-BLOCK-SENSITIVITY-001**
