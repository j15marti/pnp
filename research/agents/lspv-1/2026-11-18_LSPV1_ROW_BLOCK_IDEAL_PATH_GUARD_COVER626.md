# LSPV-1/626 | One-sided row/block selection versus verifiable correct paths

Date: 2026-11-18 America/Los_Angeles. Role: General SAT Lower-Bound Lead (unchanged). **P versus NP OPEN.** Status: PROVED/RESTRICTED mathematical results; COMPUTATIONAL original-source controls; CONDITIONAL resource contraction; OPEN arbitrary-CNF/physical-model transfer. Independent peer audit pending.

## Pre-search candidate and falsifiers

Candidate: on a source-authenticated supplied decomposition (F(z,y)=\bigwedge_{j=1}^B F_j(z,y_j)) with pairwise disjoint private (y_j), every UNSAT shared row (z) has a bad block and a total deterministic exact child SAT decider can find it with no advice, while a separately verifiable correct path may not have the same interpretation or cost.

F1: a private variable appears in different blocks and gluing fails. F2: a purported global fixed bad-block index substitutes for the necessary row-dependent index. F3: a guessed NO label or supplied correct-path bit is mistaken for a sound UNSAT certificate. F4: only favorable guesses/children are costed or a read-only proof is silently counted as ordinary low writable space.

## Theorem A: exact quantifiers and the actual deterministic specialist

For every binary (z), disjointness yields
[
\operatorname{SAT}(F)\iff\exists z\ \forall j\ \exists y_j\ F_j(z,y_j),
\qquad
\operatorname{UNSAT}(F)\iff\forall z\ \exists j\ \forall y_j\ \neg F_j(z,y_j).
]
The selected bad index is (j=j(z)), not necessarily independent of (z). Given one fixed total exact deterministic SAT decider (A) on ordinary residual CNFs, scan every (z) and block, stop on the first child NO, or combine independently obtained child witnesses when all children are YES. Both label correctness and original-clause verification follow from the input disjointness, not an advice bit. A *partial* one-sided specialist may certify NO on a recognized tractable subclass and abstain elsewhere; it does not by itself supply a guaranteed selector on arbitrary UNSAT rows. The negative answer from a correct decider is semantic and need not be a short Resolution proof.

For the explicitly validated layout (R\le N^{.195+o(1)}), (B\le N^{.65+o(1)}), each residual encoded length (\le N^{.35+o(1)}), and a fully charged (N^{1.195+o(1)}) local materialization/validation budget, the old cross-track /72 bound is
[
T(N)\le N^{1.195+o(1)}+N^{.845+o(1)}T_A(N^{.35+o(1)}),\quad
S(N)\le N^{.35+o(1)}+S_A(N^{.35+o(1)})
]
*only under the indexed read-only source/one-live-child implementation assumptions*. For seed (T_A(M)=M^{t+o(1)}), (S_A(M)=M^{s+o(1)}), time (N^{1.33+o(1)}) requires (t\le97/70) and space (N^{.5+o(1)}) requires (s\le10/7). Merely assuming (SAT\in P) does not give these exponents. Recursive fixed-point (t=1.30, s=.35) is CONDITIONAL on a fully hereditary, solver-dependent ALL-INPUT split, which remains OPEN; a seed-independent all-input source-only contraction would conflict with the deterministic Buss-Williams bound.

## NEW Theorem B: arbitrary row selectors on a connected, clause-critical family are source-easy

For every (r\ge1), set (Z=\{0,1\}^r), (R=2^r), and for (s\in Z) define one full-sign original clause
[
C_s=\bigvee_{i=1}^r \ell_i(s),\quad
\ell_i(s)=\begin{cases}x_i&s_i=0,\\ \neg x_i&s_i=1.\end{cases}
]
This clause is false at exactly the assignment (s). For ANY block map (f:Z\to\{1,\ldots,B\}), group (C_s) into (F_{f(s)}) and set (H_f=\bigwedge_s C_s). Private variable sets are all empty, hence disjoint. Every (H_f) is UNSAT and removing any original clause (C_t) yields a SAT formula with the UNIQUE witness (t). For each shared row (s), precisely the block (f(s)) is UNSAT under that row. Thus the row-to-bad-block strategy can be any of (B^{2^r}) functions, including ones for which no single block is UNSAT independent of (z). For (r\ge2) the primal graph is connected and every original clause is indispensable. This is not T5 edge-criticality.

Despite arbitrary choices of (f), a uniform solver reads the actual full-sign source clauses, detects their unique falsifying bit masks, and tests at most (min(2^r,m+1)) candidate rows for membership among the (m) source masks, re-scanning input to keep (O(r+\log m)) writable bits and (O(m(m+1)\operatorname{poly}(r,\log m))) time. On full-cover instances the same process produces a source-indexed complete-cover NO certificate, with all (2^r\le m) rows explicitly checked. On the exact one-clause-deletion promise, compute (t=(\bigoplus_{s\in Z}s)\oplus (\bigoplus_{C\in G}\operatorname{falsemask}(C))), output (t), then verify against every original clause. This takes (O(m\operatorname{poly}(r,\log m))) bit time and (O(r+\log m)) writable bits, including all parsing, source scans, output and verification. Thus clause-criticality, arbitrary selector-table entropy and a unique SAT witness do not force an intrinsic computational lower bound.

**Interpretation caveat:** representing an arbitrary *extensional* table (f\) takes (R\log_2 B) bits in the worst case, but the source itself may encode (f), and an algorithm may read/compute it. This is NOT an advice lower bound or a runtime lower bound. These full-sign guards are original r-CNFs (proper 3-CNF for r=3), not evidence that the tight ((.195,.65,.35)) layout or the T5 critical promise has such a structure. Artificial padding does not prove intrinsic hardness.

## Theorem C: correct-path polarity and clock firewall

Let (V(F,a)\) be a uniform, TOTAL deterministic verifier on every bit string (a\in\{0,1\}^{k(N)}). Its time/space maxima must include malformed, accepting, rejecting and timeout branches, source reads, certificate access and output. If (V\) accepts SOME advice exactly for UNSAT inputs, then (UNSAT\in NTIME(T_V)) with (k\) guessed bits, and its bitwise complemented branch machine recognizes SAT **conondeterministically** (universal acceptance on SAT). It is *not* a nondeterministic SAT witness checker. Conversely a sound SAT witness verifier is existential for SAT and conondeterministic for UNSAT after complementation.

If both SAT and UNSAT have independently sound, complete polynomial-length, polynomial-verifiable existential correct paths on all CNFs, then (NP=coNP). This is an implication, not a construction. If *wrong* paths may output false labels, an externally supplied correct label bit solves the decision problem by advice and has no uniform computational content. An alternating (\forall z\exists j\) NO strategy must either contain a verified global Skolem policy, or pay to visit all universal branches and check each leaf; one selected favorable path does not discharge (\forall z\). Enumerating (k\) guessed bits deterministically costs at most (2^k T_V\) time and (O(k+S_V+\log N)\) writable bits in a standard simple implementation. A read-only external certificate is not a physically stored NTM guess with zero machine space.

A polynomial-time sound/complete UNSAT verifier with existential certificates yields (UNSAT\in NP); on ALL ordinary CNFs this would imply (NP=coNP). The construction here applies only to the easily recognizable guard family, avoiding any general inference.

## Source-checked simultaneous time-space regions and polarity

- **Deterministic two-label decision (SAT and output-flipped UNSAT):** Buss-Williams, *Computational Complexity* 24 (2015), Fig. 8.2 and 8.3, proves via alternation trading that (SAT\notin DTISP(N^{1.34070},N^{.5})) in its random-access model (with the paper's (o(1)) exponent convention). Hence a fully realized all-input (N^{1.33+o(1)})-time and (N^{.5+o(1)})-space deterministic SAT decider on that model is excluded. In subpolynomial space the (2\cos(\pi/7)\approx1.8019) bound holds; the proof technique cannot pass its own ceiling.
- **Existential NO certificate / conondeterministic SAT:** FLMV, JACM 52(6), 2005, Thms. 1.2/6.4, rules out certain (coNTISP(N^c,N^d)) SAT recognizers for (c<\sqrt2) and sufficiently SMALL (d>0), not arbitrary (d=.5). Project LSPV-1/551 exactly optimizes its published (d_k^{co}(c)\) formula; for (c=1.33), the optimized bound is (d\approx0.08929991\) (level (k=3)). Therefore an (N^{1.33},N^{.5}\) conondeterministic SAT machine is NOT ruled out by this cited region. No existence claim follows.
- **Existential SAT witness / conondeterministic UNSAT:** Standard NP witness verification, with external certificate syntax distinctly costed, supplies no contradictory small-time/small-space deterministic decider. Flipping ALL branch outputs changes the polarity, not nondeterministic SAT into conondeterministic SAT. A nondeterministic SAT path is not covered by the deterministic Fig. 8.2 exclusion.
- **Fixed proof-system refutation:** a short certificate in one system bounds neither unrestricted deterministic SAT time nor the historical /341 system. /341 full logical authority FAIL; /386 RESTRICTED. Physical proof verification and acquisition must be separately charged.

No analogous (c=1.33,s=.5\) exclusion is asserted for nondeterministic SAT, conondeterministic UNSAT, proof-specific NO or external correct advice.

## Executed controls / limitations

Local CPython stdlib audit: all (2^{2^r}\) two-block selector maps for (r=1,2,3\) (4, 16, 256 maps) and every one of their (2^r\) deleted-clause cases (8, 64, 2,048 cases), plus 512 seeded maps at (r=4\) (8,192 deletion cases). Every complete source was UNSAT, each deletion had exactly one original-source witness, and XOR reconstructed it. Of the 256 maps at (r=3\), 254 have NO fixed globally bad block. Original T5 controls independently enumerated: one directed arc 10 SAT assignments, opposite digon zero, directed triangle 15. These do NOT test T5 hard families. Experiment and raw JSON published separately; local SHA256 of full executing script: b3d299db99c8ddbc6de99f7cf2f65d7cc9e56dac0cec4f080d48fe8cceae934d; JSON fa93fe463e0d8f4da5e81a1f17b841eefd5da56c0f619ab481d89ed5a188857b.

Four gates: DISJ PASS on authenticated layout and explicit guard source; arbitrary CNFs OPEN. Relativization PASS as a warning (all guard/XOR arguments relativize and cannot be the nonrelativizing separation). DTISP PASS as a decisive impossibility check on the hypothetical uniform all-input deterministic (1.33,.5\) machine. Deterministic configuration counting NOT APPLICABLE as a lower-bound mechanism; no configuration-count inference made.

**Remaining gap:** construct or falsify a solver-dependent, hereditary, ALL-CNF authenticated source decomposition with physically small children, costed successful and failed selectors of both polarities, bounded peak workspace, and no excluded deterministic resource pair. The guard family refutes shortcut reasoning from clause criticality/selector cardinality, not the possibility of a more sophisticated specialist. Peer independent mathematical and physical-model review pending; no automations or foreign manuscripts modified.

## Primary sources / project corpus

[1] Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, https://doi.org/10.1145/1101821.1101822 .
[2] Buss, Williams, *Limits on Alternation-Trading Proofs for Time-Space Lower Bounds*, Computational Complexity 24 (2015), especially Fig 8.2, https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf .
[3] Project cross-track /72, `research/agents/cross-track/2026-11-18_1825_ROW_BLOCK_SPECIALIST72_STATUS.md`.
[4] LSPV-1/551, `research/agents/lspv-1/2026-11-09_1900_LSPV1_CONONDET_FLMV_WITNESS_FIREWALL551.md`.
[5] LSPV-5/160 polarity and worst-branch clock, `research/agents/lspv-5/2026-10-26_0349_LSPV-5_POLARITY_CLOCK160.tex`.
[6] TMR-2/093 T5 cycle-syndrome DP, `research/agents/tmr-2/2026-11-18_1412_TMR2_T5_CYCLE_SYNDROME093.md`.
