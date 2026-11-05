# LSPV-1/405: Polynomially Dense Checkpoints for Worst-Case Reflection
November 4, 2026, 17:58 PST (America/Los_Angeles). Lead: PNP General SAT Lower-Bound Lead / LSPV-1.
**Status:** PROVED/EXACT elementary abstract sampling theorem, subject to independent specialist review; CONDITIONAL reflection corollary; COMPUTATIONAL finite arithmetic and signed-CNF controls; B1/B2/B3, full mixed lower bound, and P versus NP OPEN. No rule, weight, role, enabled state, or schedule change.

## IDEA (before search)
Try replacing the missing all-length B3 reflection proof obligation by proofs only at a sparse, preselected series of input-length cutoffs, without changing the fixed proof calculus. Initial falsifiable hypothesis: if a reflection family is short at infinitely many unbounded cutoffs, polynomial worst-case mixed proof cost follows. Falsifiers: (F1) enormous gaps may conceal an unbounded worst-case spike; (F2) a reflection-family theorem may silently assume a full-mixed source compiler; (F3) a fresh decider per cutoff could reverse quantifiers; (F4) arithmetic sampling might be misrepresented as a SAT-algorithm simulation.

## SEARCH, duplicate audit, and revision
Read governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (blob c3889a3e), issue #3, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, fixed original Rmix341/341 at research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, recent LSPV-2/403, LSPV-3/405, LSPV-4/398 and REFEREE348. The initial Gödel-incompleteness wrapper idea was **already proved** in LSPV-1/357 and REFEREE294 and was retired without republishing as a new theorem. REFEREE318 and REFEREE343 already establish conditional all-length reflection-family equivalences, so this result is ONLY the sharp checkpoint-density quantifier refinement, not the reflection conversion itself.

Read actual independent assessments GROKPROOF/2026-11-04_2315_PROGRESS.md (blob f5b8ef62) and research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727), research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6). They do not supply B3. The proposed Grok all-input white-box residual extraction remains OPEN; the Claude results concern restricted resource models and do not transfer to unrestricted SAT.

Primary sources read: Cook and Reckhow (1979), *The Relative Efficiency of Propositional Proof Systems*, JSL 44:36-50, https://doi.org/10.2307/2273702 ; Krajicek, *A note on SAT algorithms and proof complexity*, https://www2.karlin.mff.cuni.cz/~krajicek/sat.pdf , particularly Definition 1.1 and Theorem 2.1: the transfer assumes polynomial proofs of reflection formulas; Pudlak (2020), *Reflection principles, propositional proof systems, and theories*, arXiv:2007.14835. Search strings: "Cook Reckhow 1979 relative efficiency propositional proof systems", "Krajicek A Note on SAT Algorithms and Proof Complexity theorem 2.1 reflection formulas", "Pudlak Reflection principles propositional proof systems and theories", "Haken 1985 Intractability of Resolution", and "Gödel second incompleteness polynomial time algorithm soundness". Direct Google-branded UI was not accessible; general web search was used, without claiming a Google-specific search.

Authenticated github.com/openai queries: "ExecCNFNodeSearchCosts", "SAT proof checker", "reflection proof", "Cook Levin"; actual files inspected: openai/math/lean/OAI/Algorithms/SubexponentialSAT/DyadicNodeSearchBounds.lean (blob 24ebc3e2) and ExecCNFNodeSearchCosts.lean (blob 1ced21f4). Their dyadic indexing is an unrelated actual SAT algorithm execution/width-budget proof, not a mixed-reflection lemma and not a B3 implementation.

## ITERATE: sharp theorem
Let $1\le s_0<s_1<\cdots$ be unbounded positive integers. Define checkpoint polynomial density by
$$
\exists d,C,j_0\ \forall j\ge j_0:\quad s_{j+1}\le C(s_j+1)^d .
$$
**Theorem 405.1 (PROVED/EXACT abstract monotone-profile characterization).** The following are equivalent:
(A) the checkpoints have polynomial density;
(B) every nondecreasing function $f:\mathbb N_{\ge1}\to\mathbb N$ with
$$
\forall j:\quad f(s_j)\le s_j+1
$$
is polynomially bounded over **all** integers $N$.
The implication (A)->(B) also holds if the sample bound is any fixed $f(s_j)\le K(s_j+1)^k$ with constants $K,k$ independent of $j$.

**Proof.** For $s_j<N\le s_{j+1}$, monotonicity gives $f(N)\le f(s_{j+1})\le K(s_{j+1}+1)^k\le K'(s_j+1)^{dk}\le K'(N+1)^{dk}$ under (A). Absorb finitely many initial cutoffs into $K'$. Conversely, if (A) fails, define $f(N)=s_0$ for $N\le s_0$ and $f(N)=s_{j+1}$ for $s_j<N\le s_{j+1}$. This is monotone and satisfies $f(s_j)=s_j$ at every checkpoint. But $f(s_j+1)=s_{j+1}$ is not bounded by any fixed polynomial in $s_j+1$, since failure of (A) means the gap ratios are larger than every fixed polynomial infinitely often. Thus (B) fails. QED.

**Corollary 405.2 (PROVED/EXACT for the unchanged fixed proof-cost function, with a hypothesis).** For ANY fixed sound complete calculus R, including the unchanged Rmix341, its worst-case function $Wbar_R(N)$ is nondecreasing. Consequently:
$$
Wbar_R(N)=N^{O(1)}\quad\Longleftrightarrow\quad
\exists K,k\ \forall j:\ Wbar_R(2^j)\le K(2^j+1)^k.
$$
The right side does **not** hold by assumption; it is simply a sharp equivalent sampling target.

**Conditional reflection corollary, NOT B3.** Fix ONE uniform total correct polynomial-time SAT decider A, conditional on SAT in P, and explicit reflection CNFs $H_{A,s_j}$ whose source lengths and encoded lengths are polynomial in $s_j$. Suppose a sound source-preserving compiler maps every valid mixed proof of $H_{A,s_j}$ to a proof of EVERY UNSAT $F$ with $|enc(F)|\le s_j$, at uniform polynomial total logical overhead in $s_j$ and the input proof cost. If every dyadic $H_{A,2^j}$ has a mixed proof costing at most $K(2^j+1)^k$, then B3 follows. **The two indispensable missing premises are** (i) a fully native, type-correct LOCAL-CONVERT/AND3/GF(2)/DEF retraction for ALL legal operations and exported wires, and (ii) polynomially short reflection proofs derived NONCIRCULARLY from bare SAT in P. The premise (ii) is not supplied by Cook-Reckhow, theorem 2.1 of Krajicek, or prior project reports. This result narrows the cutoff quantifier but solves neither premise. A different A selected per j is NOT permitted.

**Sparse-gap falsifier.** Take $s_0=2$ and $s_{j+1}=2^{s_j}$. The staircase $f$ from the proof has $f(s_j)=s_j$ but $f(s_j+1)=2^{s_j}$, superpolynomial along the growing sequence. This is an *abstract monotone profile*, not a claimed realizable Wbar_Rmix341. At $s_j=65536$, $\log_2 f(s_j+1)=65536$ while $\log_2(s_j+1)<17$; no fabricated exponential output is materialized.

## Established-hard-family anchor and safeguards
For explicit unary PHP with $h+1$ pigeons and $h$ holes there are $h(h+1)$ variables, $(h+1)+h\binom{h+1}{2}$ source clauses and $\Theta(h^3\log(h+2))$ bits in a signed binary-index encoding. Haken (1985), *The Intractability of Resolution*, establishes constants $c>0,h_0$ such that for all $h\ge h_0$ and **every** ordinary source-authenticated shared-DAG Resolution refutation, proof size is at least $2^{ch}$. This does NOT concern Extended Resolution, GF(2), Rmix341 or arbitrary correct uniform machines. Cook's (1976) ER polynomial PHP proof and the fixed mixed odd cubic Tseitin $4h-1$ upper/optimal proof are mandatory shortcuts. No restricted lower bound is transferred.

Rmix341 remains fixed with free genuine CNF leaves, unit-paid shared binary RES, support-three AND3, binary GF(2) XOR, source-justified LOCAL-CONVERT and conservative paid two-input DEF, as originally declared in /341. The unresolved exact LOCAL-CONVERT exported-wire grammar is NOT silently completed here. $Wbar_R$ measures distinct inference nodes, not proof bytes, inference discovery cost, bit accesses, parsing, output or peak machine space. Logical existence at dyadic cutoffs is free to choose an optimum but is not a uniform computational proof extractor; conversion bytes/checking and actual machine costs must be separately polynomial if a machine-time claim is made.

## Computational controls
Python producer (deterministic, no randomness) executed 393,228 assertions: all $N=1..65536$ with dyadic upper-envelope checks, three sparse-gap records (logarithmic not materialized large integers), SAT clause with three models, contradictory units with zero models, consistent parity with two models, and three malformed-clause rejections. Independent Node.js verifier executed 393,234 checks and rejected two corrupted metadata variants. Raw SHA256: cc97e4db727a78b66cf67b5d5fe587ea3e7bcb828161ea5ceb9f49c3f043a75c. This is only FINITE arithmetic/CNF label verification, not a finite Rmix341 optimum or a complexity lower bound.

## Precise status and next step
F1 initial unrestricted sparse-cutoff prediction FALSIFIED. F2 all-mixed reflection retraction OPEN. F3 nonuniform per-j algorithm substitution REJECTED by quantifiers. F4 assigning machine T/S to a noncomputable free minimum REJECTED. B1, B2, B3, $Wbar_{Rmix341}$ superpolynomial lower bound, P versus NP OPEN. Next LSPV-1 task: demand from peers a full native LOCAL-CONVERT exported-port grammar and certified retraction; then attempt a one-decider dyadic reflection proof-construction that does NOT assume short proofs in the premise. This cannot be achieved by the sampling lemma alone.

Published with report/code/raw/five-role handoff; reconcile root main.tex only within LSPV-1 marker after complete fresh blob read, otherwise document safe fallback.
