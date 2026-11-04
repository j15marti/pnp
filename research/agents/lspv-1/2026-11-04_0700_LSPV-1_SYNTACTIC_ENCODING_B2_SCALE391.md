# LSPV-1/391: Syntactic encoding invariance and worst-case time-rescaling firewall

November 4, 2026, 07:00 PST. **PROVED/EXACT** elementary metatheorems, external mathematical review pending. **COMPUTATIONAL** finite two-language controls. The original $R_{\mathrm{mix341}}$ is unchanged. B1/B2/B3 for this calculus, its superpolynomial worst-case minimum, and P versus NP remain **OPEN**.

## Published hard-family anchor and exact model

Haken (1985) proves that for the standard unary pigeonhole CNF $P_h=\mathrm{PHP}_{h+1}^{h}$, there are constants $c>0,h_0$ such that **for every** $h\ge h_0$ and **every** ordinary shared-DAG Resolution refutation $\pi$ of that same CNF, $|\pi|_{\rm lines}\ge 2^{ch}$. The source has $h(h+1)$ variables $x_{p,j}$, $h+1$ clauses $\bigvee_{j=1}^h x_{p,j}$, and $h\binom{h+1}{2}$ pairwise negative collision clauses $(\neg x_{p,j}\vee\neg x_{q,j})$. Conventional explicit signed-literal binary-index encoding length is $N_h=\Theta(h^3\log(h+2))$. Free original axioms give derived-node lower bound at least $2^{ch}-[(h+1)+h\binom{h+1}{2}]$. The theorem allows unrestricted ordinary Resolution width, pivots, and DAG reuse but NO extension-variable definitions, XOR equations, or arbitrary algorithms. Cook (1976) established polynomial Extended Resolution pigeonhole proofs. Braun (2026, arXiv:2609.23015) reports an extension-free DAG Res$(\oplus)$ bit-PHP bound $>\exp(n/(32768\ell^2))$ for $n=2^\ell$, $\ell\ge32$; it has no implication for Extended Resolution or general SAT machines, and independent specialist review remains pending.

Fix the **same preselected** $R_{\mathrm{mix341}}$ of LSPV-2/341, blob c87acd11: source-labelled DIMACS original clauses free; distinct shared-DAG inference nodes charged 1; binary RES, constant-3-original-variable AND3, binary GF(2) XOR, justified bounded-support LOCAL-CONVERT, and paid conservative two-input DEF. Its LOCAL-CONVERT exported-wire grammar remains incompletely specified. This run does not alter any rule.

## Theorem 391A: genuinely syntactic encodings preserve B1 and B3

Fix a set $\mathcal F$ of **the same abstract source-labelled CNFs**, and a sound complete fixed calculus $R$ operating on those unchanged objects with fixed node charges. Let $e_0,e_1:\mathcal F\to\{0,1\}^*$ be injective canonical encodings with polynomial-time recognizable images, polynomial-time converters $e_0(F)\leftrightarrow e_1(F)$, and fixed polynomial length bounds both ways. Malformed binary strings are rejected. Do not substitute an equisatisfiable formula for $F$.

Define

$$
W_R(F)=\min_{\pi:F\vdash_R\bot}\sum_{\text{distinct paid }v\in\pi}1,\qquad
\overline W_{R,e}(N)=\max_{\substack{F\text{ UNSAT}\\|e(F)|\le N}}W_R(F),
$$

with empty maximum zero. For polynomials $g_{01},g_{10}$ bounding the output lengths,

$$
\overline W_{R,e_1}(N)\le\overline W_{R,e_0}(g_{10}(N)),\qquad
\overline W_{R,e_0}(N)\le\overline W_{R,e_1}(g_{01}(N)).
$$

**PROVED:** Polynomial boundedness of $\overline W_R$ is equivalent between the two encodings. Consequently its failure to be polynomially bounded is equivalent. SAT being in P is also encoding-independent since canonical parsing and conversion are polynomial time. Therefore the *truth value* of

$$
\mathrm{B3}_e:\quad \mathrm{SAT}\in P\Longrightarrow \overline W_{R,e}(N)=N^{O(1)}
$$

is encoding-independent. This does **not** prove B3 itself.

**PROVED:** The stronger pointwise B1 condition is likewise equivalent. To prove one direction, choose an arbitrary fixed uniform total correct $e_1$-decider $A_1$. Construct the **one fixed** $e_0$-decider $A_0$ that parses, rejects malformed inputs, converts valid $e_0(F)$ to $e_1(F)$, and simulates $A_1$. There is a fixed polynomial $h$ with

$$
T_{A_0}(e_0(F))\le h\bigl(|e_0(F)|+T_{A_1}(e_1(F))\bigr).
$$

If B1 holds for $e_0$, substitute this inequality and the polynomial length bounds in $W_R(F)\le p_{A_0}(|e_0(F)|+T_{A_0}(e_0(F)))$. This gives $W_R(F)\le p'_{A_1}(|e_1(F)|+T_{A_1}(e_1(F)))$ for a polynomial depending on $A_1$ but not on $F$. Reverse converters prove the converse. There is no per-input machine or nonuniform per-size advice.

## Theorem 391B: B2 survives length-preserving code isomorphisms

If additionally $|e_0(F)|=|e_1(F)|$ for **every** abstract $F$, the two worst-case $\overline W$ functions agree exactly. The simulation of any one fixed total correct decider gives

$$
T_{A_0}^{wc}(N)\le h(N+T_{A_1}^{wc}(N)),
\quad T_A^{wc}(N)=\max_{\text{all binary }x,\ |x|\le N}T_A(x).
$$

Malformed codes are rejected at polynomial cost; valid conversions preserve input length. Thus B2 is true for $e_0$ iff it is true for $e_1$. **This does not establish B2 for the actual mixed calculus.** The argument does not promote B2 to all polynomial-length-changing encodings.

## Theorem 391C: a fixed correct uniform decider defeats naive worst-case time rescaling

**PROVED/EXACT:** There is a single fixed, total, uniform, correct SAT/UNSAT/malformed classifier $A$, and a computable unbounded sequence $n_k=2^{10^k}$, for which, **for every polynomial $p$**, eventually

$$
T_A^{wc}(n_k^2)>p\bigl(n_k+T_A^{wc}(n_k)\bigr).
$$

**Construction and proof:** On input $x$ of bit length $m$, detect in polynomial $m$-time whether $m=n_k^2$ by repeated tenth powers with integer values capped above $m$. At such lengths execute a genuine $2^{m^2}$-step counter delay, using $m^2$ writable bits. Afterwards use one fixed exact exhaustive CNF-SAT decider with strict malformed rejection. This algorithm is total and correct on **every binary input**, with no embedded answers. Its baseline time is at most $2^{2m}$ for sufficiently large $m$. Since $n_k=n_{k-1}^{10}$, the largest prior delayed length below $n_k$ has delay exponent $n_{k-1}^4<n_k$. Therefore for sufficiently large $k$

$$
T_A^{wc}(n_k)\le 2^{3n_k},\qquad
T_A^{wc}(n_k^2)\ge 2^{n_k^4}.
$$

Every polynomial in $n_k+2^{3n_k}$ is $2^{O(n_k)}$, proving the claim. The high delay has a real bit-operation and all-phase space cost. This **falsifies the unjustified runtime scaling inequality** $T_A^{wc}(N^2)\le\operatorname{poly}(N+T_A^{wc}(N))$ for arbitrary total correct $A$. It does NOT falsify B2 or prove failure of B2 encoding invariance. It explains why the one-line polynomial-size rescaling used for B3 cannot simply be reused for B2's worst-case runtime term.

## Three falsifiers

**F1, FALSE:** Every polynomial-time invertible equisatisfiable *semantic recoding* preserves paid proof-node cost. LSPV-3/394 already exhibited a reversible recognized-PHP encoder introducing an active empty clause and tag clauses. This changes the underlying formula and is not a legal source-preserving $R_{\mathrm{mix341}}$ deduction. The positive 391A theorem is deliberately restricted to the **same source-labelled CNF**.

**F2, FALSE:** Merely reserializing the identical CNF and fixed calculus with efficiently invertible polynomially balanced codes can change whether $\overline W_R$ is polynomially bounded. The explicit two-sided inequalities in 391A rule this out.

**F3, FALSE AS A TRANSFER STEP:** A polynomial expansion of code length automatically yields a polynomial expansion of an **arbitrary fixed correct** decider's worst-case runtime profile from $N$ to $N^2$. The charged uniform DELAY witness in 391C disproves this. It is not a counterexample to B2 as stated.

## Reproduction and limits

**COMPUTATIONAL:** Python and independent Node programs evaluate all 256 subsets of eight non-tautological width-1/2 clauses over two variables: 95 SAT, 161 UNSAT. A finite BFS over source-augmented ordinary Resolution clause sets establishes toy optima with maximum three paid nodes. Two concrete encodings have lengths $|b(F)|=3+2|a(F)|$ and identical abstract sources. Their finite worst-case profiles agree after this exact dilation at every tested threshold. Python: 823 assertions including eleven malformed rejections; independent Node: 768 checks. Finite results do not establish the all-size theorems, and these are ordinary Resolution toy optima, not mixed-calculus optima. The enormous DELAY witness is proved symbolically, not executed.

Charge input parsing and bit/index/source reads, conversion, serialized proof evidence, proof-discovery/search, failed policies, gate access/update, output, checking, caches, and simultaneous peak memory separately from logical $W_R$. Arbitrarily large intermediate representations are allowed and charged if materialized. FLMV same-machine and all-phase $\rho$ constraints remain separate; a polynomial proof cost is not an implemented algorithm.

## Corpus and publication provenance

Recovered controlling November 2 directive at commit 4e29ed7, blob 033b54b8; current issue #3 through November 4 06:36 PST; AGENTS.md blob 19656af1, CODEX.md 754999f5, pnp skill b8df83a7, original R_mix341/341 blob c87acd11, LSPV-1/390, LSPV-3/394 with its 06:46 full-main readback addendum, LSPV-5/REFEREE337, LSPV-4/386 issue handoff. Project search for encoding-rescaling and semantic recoding found LSPV-3/394 but not the exact 391A/B/C combination. Primary literature queried Haken 1985, Cook 1976, Cook-Reckhow 1979, Braun 2026. GitHub openai searches for CNF proof verifier and p-optimal proof systems yielded no applicable B3 compiler. Actual Grok assessment GROKPROOF/2026-11-04_1217_PROGRESS.md blob cae0560d proposes an unproved fully charged circuit-cut compiler; Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex blob 1f9fc727 treats an alternation-trading small-space calculus, not unrestricted B3. Neither is accepted as a computation-to-proof transfer.

**Next precise gap:** settle the unchanged LOCAL-CONVERT public-wire/auxiliary semantics and full $b(N,q)$ certificate normalization; independently prove or refute the weakest B3 and a superpolynomial minimum for **the very same** $R_{\mathrm{mix341}}$. P versus NP remains OPEN.

References: [1] A. Haken, The Intractability of Resolution, TCS 39 (1985), 297-308. [2] S. Cook, A Short Proof of the Pigeon Hole Principle Using Extended Resolution, SIGACT News 8(4) (1976), 28-32. [3] S. Cook and R. Reckhow, The Relative Efficiency of Propositional Proof Systems, JSL 44 (1979), 36-50. [4] K. Braun, arXiv:2609.23015 (September 19, 2026, preprint).
