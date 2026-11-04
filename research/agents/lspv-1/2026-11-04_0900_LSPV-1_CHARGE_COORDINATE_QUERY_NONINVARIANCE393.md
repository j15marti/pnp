# LSPV-1/393: Reversible charge coordinates collapse a source-query invariant without changing the SAT source

**November 4, 2026, 09:00 PST.** **PROVED/EXACT:** elementary model-specific theorem below, independent specialist mathematical review pending. **COMPUTATIONAL:** independent finite checks, detailed in raw and scripts. **OPEN:** B1, B2, B3 for the unchanged R_mix341, superpolynomial full-mixed minimum, and P versus NP. Original roles, schedules, identities, proof rules and unit charges unchanged.

## IDEA, before search

Proposed falsifier: source-sign SAT-neighbor hypergraphs, particularly the 12h pivotal sign bits of a connected bridgeless cubic odd-Tseitin formula, might impose a representation-independent input-acquisition cost across every uniform polynomial-time invertible canonical source encoding. The test prediction was that even an alternative canonical source syntax would require h^{Omega(1)} original-bit probes from **every** uniform total correct all-binary SAT decider on the same abstract UNSAT family. Hypotheses: authentic source, source-preserving invertible encodings, explicitly indexed binary random-access input, full SAT/UNSAT/MALFORMED correctness. No new hard family.

## SEARCH and prior-work audit

**Published hardness, with exact scope.** Haken (1985) proves that for constants c>0,h0 and each h>=h0, **every ordinary unrestricted shared-DAG Resolution refutation** of the standard unary PHP(h+1,h) source has at least 2^(c h) lines, or at least 2^(c h)-O(h^3) paid derived nodes when original clauses are free. Its explicit signed indexed source has h(h+1) variables, h+1+h*binom(h+1,2) clauses and N_h=Theta(h^3 log(h+2)) bits. Neither arbitrary SAT machines nor Extended Resolution or our mixed system is included. Cook (1976) gives polynomial Extended Resolution PHP proofs. Urquhart (1987) proves exponential ordinary unrestricted Resolution lower bounds for specific odd Tseitin expander-graph CNFs. A bounded-degree cubic source on h vertices has 3h/2 variables, 4h ternary clauses, and Theta(h log(h+2)) signed indexed bits. No Resolution-hardness claim is made about the finite prism graphs used in tests. Neither published theorem bounds arbitrary SAT algorithms. GF(2) and charged conservative DEF create allowed compact escapes in R_mix341.

**Fixed calculus** is exactly original LSPV-2/341, blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb: free authenticated source-labelled original clauses; unit-paid shared DAG nodes with at most two ancestors; RES; support-at-most-three-original-variable AND3; binary GF(2) row XOR; constant-support justified LOCAL-CONVERT; and charged conservative two-input DEF. LSPV-2/341 proves that for every connected simple bridgeless cubic graph G of h vertices, every odd-charge Tseitin source F has W_Rmix341(F)=4h-1 via indispensable source leaves and matching AND3/XOR derivation. The original LOCAL-CONVERT wire grammar remains an independent open audit, not changed here.

**Project corpus actually read:** November 2 refocus (pinned commit 4e29ed7, current blob c3889a3), coordination issue #3 (through 2026-11-04 ~08:40 PST), AGENTS.md blob 19656af1, CODEX.md blob 754999f5, repo skill blob b8df83a7, LSPV-1/387/390/391/392, LSPV-2/341, LSPV-3/394/397, LSPV-4/389 and LSPV-5/REFEREE339. LSPV-1/387 uses a redundant triple-majority encoding to erase single-bit pivotality, but not the present full all-SAT-neighbor transversal collapse; LSPV-3/394 uses reversible *semantic source alteration* that adds an empty clause to recognizable PHP, unlike the exact SAME source here. REFEREE339 requires exact prefix alignment for its B2 encoding-transfer theorem, and polynomial length balancing alone does not establish that stronger transfer.

**External primary searches:** web-engine queries "Urquhart 1987 hard examples for resolution Tseitin graph expanders lower bound source theorem", "Tseitin expander graph resolution size exponential over variables", "Haken 1985 intractability of resolution pigeonhole principle exponential bound", "Cook 1976 short proof pigeonhole principle using extended resolution", "decision tree complexity change under invertible linear transformation parity encoding sensitivity is not invariant", "Boolean function parity is one bit after invertible GF2 transformation decision tree complexity linear". Results included Urquhart, JACM 34(1), DOI 10.1145/7531.8928; Haken, TCS 39, DOI 10.1016/0304-3975(85)90144-6; Cook, SIGACT News 8(4); Zhang and Shi, arXiv:1004.0436; Nisan, "CREW PRAMs and Decision Trees", SICOMP 1991. No claim that classical parity-query/decision-tree sensitivity is novel. Direct Google-site querying was unavailable; a general web search engine and authenticated GitHub searches were used, and direct Google use is NOT claimed.

**OpenAI-owned GitHub:** authenticated searches restricted to org=openai for "Tseitin", "GF2", "SubexponentialSAT"; read openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNF.lean blob e60f4d986b and Incidence.lean blob 70394893f1. The former distinguishes list-operation counts from charged bit costs; neither file establishes B3 or this encoding theorem. **Grok directly read:** GROKPROOF/2026-11-04_1518_PROGRESS.md blob 4e2bb9d941, still OPEN on an all-input fully charged FLMV compiler. **Claude directly read:** research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex blob 9a5b05d6ec and 2026-10-28_1452_CLAUDE_TPORT-0002.tex blob 1f9fc727d3. Their sequential-access and alternation-trading limitations do not imply the Rmix341 B3 bridge.

## ITERATE: full-code repair and two proved claims

For any uniformly polynomial-time constructible sequence of connected simple bridgeless cubic labelled graphs G_h on h vertices, let F_(h,b) be the canonical signed 3-CNF of the h vertex parity equations (one clause for each of the four forbidden triples per vertex), charge b in GF(2)^h. The connected graph incidence matrix has rank h-1, so

$$
F_{h,b}\in\mathrm{UNSAT}\quad\Longleftrightarrow\quad \bigoplus_{i=1}^{h} b_i=1.
$$

For an *explicit indexed source encoding* e0 with source-label-ordered three-literal clauses and independently readable polarity bits, any odd F_h has 12h disjoint singleton SAT neighbor difference sets: deleting any original clause makes the source satisfiable, and flipping any of that clause's three sign bits permits the deletion witness to satisfy the flipped source. The full same-length valid-SAT-neighbor fractional and integral hitting numbers therefore obey

$$
\tau_{e_0}(F_h),\ \tau^*_{e_0}(F_h)\ge 12h.
$$

Now define **one canonical whole-CNF language** e1. A source exactly equal to one of the uniformly generated graph-template F_(h,b) is represented by tag bit 1, a self-delimiting binary header encoding h, and an h-bit charge-coordinate payload

$$
y=(b_1\oplus\cdots\oplus b_h,\ b_2,\ldots,b_h).
$$

This is invertible: b_1=y_1\oplus y_2\oplus\cdots\oplus y_h and b_i=y_i for i>=2. Every h-bit payload is a valid source code; its SAT label is determined by the single first payload bit y_1. All other source-labelled valid CNFs use tag bit 0 followed by their complete e0 code; the tag-0 parser rejects a graph template to enforce canonical uniqueness. Malformed codes are rejected. Both full-language conversion directions are one fixed uniform polynomial-time algorithm, with polynomially balanced encoded lengths (on templates |e0|=Theta(h log h), |e1|=h+O(log h); on other sources |e1|=|e0|+1). This is an EXACT SOURCE serialization, not the LSPV-3/394 altered CNF.

**Theorem 393A (PROVED/EXACT, model-relative).** For every odd template source F_h and the complete same-length SAT-neighbor difference hypergraph in the respective full canonical languages,

$$
\boxed{\tau_{e_0}(F_h),\tau^*_{e_0}(F_h)\ge12h,\qquad
\tau_{e_1}(F_h),\tau^*_{e_1}(F_h)\le2.}
$$

The first inequalities follow from disjoint singleton SAT sign flips. For the second, any same-length valid SAT e1 neighbor with tag 0 differs at the tag bit. Any one with tag 1 must have the same h, because the length 1+|gamma(h+1)|+h is strictly increasing, and its parity coordinate y1=0 differs from the original UNSAT y1=1. Thus the two positions (tag, parity) hit **every** valid SAT neighbor, not just a sampled or promised subset. In the tag-1 template sublanguage, the exact hitting number is 1.

**Theorem 393B (PROVED/EXACT, algorithm quantifiers).** For **every** fixed uniform total exact SAT/UNSAT/MALFORMED decider A0 in the length-aware random-access single-bit probe model, on e0(F_h) it reads all 12h pivotal sign positions. For any randomized total decider with error <=epsilon<1/2 on every input, expected distinct sign reads on that same input are at least (1-2epsilon)12h, by identical-random-tape coupling of each opposite-label one-bit neighbor.

But there **exists one fixed uniform total correct all-binary decider A1 for e1** which on *every odd* template e1(F_h) reads just tag, O(log h) self-delimiting header bits, and one parity bit y1. The random-access input's total length is given and compared against 1+header length+h. No other payload bits are needed because every charge payload is syntactically valid. All tag-0 sources are parsed and solved by exhaustive search, with malformed/corrupt/noncanonical inputs rejected. Hence A1 requires O(log h) distinct input probes on the SAME abstract odd formula family, despite every A0 requiring Omega(h) sign-bit probes under e0. The algorithm is fixed across all lengths; it uses no nonuniform advice or SAT oracle.

**Critical repair after search:** a promise-only parity recognizer was not enough, since the required classifier must handle every binary string. The tag-0 fallback, tag-1 exact-length authentication and full-language canonical decoding make the counterexample genuine. The special parity coordinate is precomputed by a *polynomial-time source encoder*, not by a semantic SAT oracle: the original charge vector must still be parsed. Running A1 on an input originally supplied in e0 coordinates entails this conversion with all bit reads, updates, output and peak-space phases charged, so no uncharged end-to-end speedup follows.

**Logical proof cost is invariant in this example:** e0 and e1 name *the same* source-labelled F, and the preselected Rmix341 proof rules operate on that source. Hence W_Rmix341(F_h)=4h-1 for odd sources under original /341, regardless of serialization. The collapse concerns coordinate-defined query sensitivity, not this paid-node invariant. This is no unrestricted SAT machine-time lower bound and no B1/B2/B3 transfer.

## Falsifiers and controls

F1, polynomial-time invertible source coding preserves the SAT-neighbor hitting number up to a polynomial: **FALSIFIED**, because Omega(h) becomes at most 2. F2, the construction needs a hidden SAT oracle or modifies the source: **FALSIFIED**, exact syntactic graph-template recognition and XOR suffice, and decoding recovers the original CNF. F3, a promise-only one-bit recognizer suffices for all-binary correctness: **FALSIFIED/REPAIRED** by the tag-0 parser/exhaustive fallback and strict tag-1 size validation. F4, input-query collapse refutes a full Rmix341 lower bound, B2 or B3: **FALSE AS A TRANSFER**; expensive e0->e1 preprocessing is not free and the fallback may be exponential.

**Finite verification:** a deterministic Python source producer passed 5,839 checks; an independent no-import Node verifier passed 3,259 checks. K4 (h=4), prism3 (h=6), prism4 (h=8), prism5 (h=10); odd UNSAT and even SAT controls; each of the 2^h charge vectors per size; odd sources zero models, even sources exactly 2^(|E|-h+1) models; all 336 individually flipped e0 sign bits checked SAT; nine malformed/noncanonical strings rejected, and general-CNF SAT and UNSAT fallback controls. Exact raw/input/source hashes and reproducible scripts under experiment/results paths. These tests are finite, not an independent Urquhart lower-bound proof or a mixed-proof global-optimizer run.

**Resource ledger:** e0->e1 canonical conversion scans/authenticates the original source, extracts charges, computes their XOR, and emits an h+O(log h)-bit code. That work is polynomial but not zero; materialized output costs Theta(h) writable bits, whereas streaming output can reduce scratch while paying reads. A1 on already supplied e1 input has a different acquisition cost than a solver that first translates e0. Verification, proof discovery, shared DAG storage and recomputation, every local temporary, and FLMV all-phase peak space remain separate. The logical node minimum never equals physical runtime by declaration.

## B1/B2/B3 firewall and next target

Fix unchanged R=Rmix341, W_R(F)=minimum unit-paid distinct inference DAG nodes, Wbar_R(N)=max valid UNSAT of encoded bit length <=N (empty maximum 0). For fixed total correct uniform A, T_A^wc(N)=max over *all* binary strings of length <=N, including malformed. The three still-unproved obligations are B1: for all A exists polynomial p_A for all UNSAT F, W_R(F)<=p_A(N(F)+T_A(F)); B2: for all A exists polynomial p_A for all N, Wbar_R(N)<=p_A(N+T_A^wc(N)); B3: SAT in P implies Wbar_R(N)=N^O(1) for the SAME preselected R. B1=>B2=>B3. **All OPEN for full Rmix341.** The present theorem concerns source-bit representation and does not prove or refute them.

**Next precise obligation:** prove a model-fixed *post-acquisition* unavoidable-work invariant surviving GF(2), paid auxiliaries, shared DAGs, lazy circuits and arbitrary correct uniform solvers, or prove the still-missing B3 computation-to-proof transfer with native LOCAL-CONVERT/DEF semantics. Do not simply infer machine hardness from certified ordinary-Resolution exponential lower bounds. P versus NP remains OPEN.

## References

[1] A. Haken, "The Intractability of Resolution", Theoretical Computer Science 39 (1985), 297-308. DOI 10.1016/0304-3975(85)90144-6.

[2] S. A. Cook, "A Short Proof of the Pigeon Hole Principle Using Extended Resolution", SIGACT News 8(4) (1976), 28-32.

[3] A. Urquhart, "Hard Examples for Resolution", Journal of the ACM 34(1) (1987), 209-219. DOI 10.1145/7531.8928.

[4] Z. Zhang and Y. Shi, "On the Parity Complexity Measures of Boolean Functions", arXiv:1004.0436 (2010).

[5] N. Nisan, "CREW PRAMs and Decision Trees", SIAM Journal on Computing 20(6) (1991).
