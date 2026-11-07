# LSPV-2/458: Tight one-pass frontier-state lower bound for proper 3-CNF
**2026-11-06 19:09 PST | Route A primary | PROVED/RESTRICTED and COMPUTATIONAL | P versus NP OPEN**

## IDEA, precise falsifiers and revision

**Initial idea.** The OR-folded moving-frontier constructor (LSPV-2/457, LSPV-4/455) keeps a Boolean table on the current interface. Is its $2^w$-bit retained state merely inefficient, permitting a universal much smaller semantic summary even for syntactically strict original 3-CNF?

**Four falsifiers.** (F1) A subset $S\subseteq\{0,1\}^w$ cannot be realized as the existential frontier projection of a proper signed 3-CNF with polynomial-in-$2^w$ source length. (F2) Two distinct realizable projections cannot be distinguished by some legal strict 3-CNF suffix. (F3) A compact state can encode all $2^{2^w}$ projections in fewer than $2^w$ fixed bits. (F4) The argument accidentally charges source-rereading input as forbidden on the actual FLMV machine. F1-F3 are excluded by the constructive proof below; F4 is a real restriction, therefore this theorem is explicitly ONLY for one-pass source-erasure summaries and **not** arbitrary SAT machines.

**Evidence changing the idea.** Previously LSPV-2/447 proved one semantic syndrome bit suffices for a connected Tseitin charge family. LSPV-2/457 and LSPV-4/455 instead use complete frontier tables. The present exact construction shows that one-bit compression is not generic across proper 3-CNF prefixes, even when a path/interface grammar is already given. This is a focused architecture falsifier, not a new candidate hard SAT family.

## Theorem 458.1: every frontier relation has a strict proper 3-CNF realization

Let $Z=\{z_1,\dots,z_w\}$ be labeled interface variables and let $S$ be **any** subset of $\{0,1\}^w$, including the empty and full sets. There is a 3-CNF $P_S(Z,X)$ with exactly three pairwise distinct signed variables in every original clause, with private existential variables $X$, such that

$$
\{a:\exists X\;P_S(a,X)=1\}=S.
$$

It has at most $O(w2^w)$ original clauses and $O(w2^w)$ variables; under fixed-width binary identifier encodings it has $O(w^2 2^w)$ bits. A padded construction makes **the clause count, declared variable range, binary record widths, and total encoded length identical for every $S$ at fixed $w$**. All variables outside $Z$ are private.

**Proof.** For every forbidden assignment $a\notin S$, form the clause

$$
D_a=\bigvee_{j=1}^w \ell_{a,j},\qquad
\ell_{a,j}=\begin{cases}z_j&a_j=0,\\\neg z_j&a_j=1.\end{cases}
$$

This is false exactly at $Z=a$. Convert every $D_a$ to strict ternary clauses using *fresh private variables per forbidden assignment*. For width $1$, replace literal $\ell$ with the four clauses $(\ell\vee u\vee v)$, $(\ell\vee u\vee\neg v)$, $(\ell\vee\neg u\vee v)$, $(\ell\vee\neg u\vee\neg v)$. For width $2$, replace $(p\vee q)$ with $(p\vee q\vee u)\wedge(p\vee q\vee\neg u)$. For width $3$, use the clause itself. For width $w\ge4$ introduce $y_1,\dots,y_{w-3}$ and use the standard chain

$$
(\ell_1\vee\ell_2\vee y_1)
\wedge
\bigwedge_{j=2}^{w-3}(\neg y_{j-1}\vee\ell_{j+1}\vee y_j)
\wedge
(\neg y_{w-3}\vee\ell_{w-1}\vee\ell_w).
$$

For each fixed $Z$, the chain is satisfiable in the $y$ variables exactly when at least one $\ell_j$ is true. Conjunction across all forbidden $a$ therefore projects precisely to $S$. The full relation gets a private-only satisfiable ternary clause. To obtain identical lengths for all $S$, allocate a fixed group of private variable identifiers and a fixed $K(w)$-clause slot for each possible $a$; replace every **allowed** slot with $K(w)$ private-only satisfiable ternary filler clauses. Every slot is strictly proper 3-CNF and has a fixed-width record encoding. Canonically pad unused private IDs. Hence encoded length is independent of $S$. $\square$

## Theorem 458.2: exact tight state complexity in the specified model

Suppose a deterministic algorithm reads a complete prefix $P_S$ and then permanently loses access to its source bytes. It must retain a **fixed-length $b$-bit semantic message** and answer the SAT status of $P_S\wedge Q$ for **every** future proper signed 3-CNF suffix $Q$ using only the message and $Q$. The algorithm's control and join protocol are fixed independently of $S$.

Then

$$
\boxed{b\ge2^w.}
$$

The bound is tight because the $2^w$-bit bitmap of the projection suffices.

**Proof.** For each $a\in\{0,1\}^w$, construct the legal proper ternary suffix $Q_a$ that forces $Z=a$, using the four-clause unary gadget above for each pinned literal, with fresh suffix-private variables. Then

$$
\operatorname{SAT}(P_S\land Q_a)\iff a\in S.
$$

For any $S\ne T$, some $a\in S\triangle T$ makes these SAT outputs different. Thus the messages for $S$ and $T$ must be distinct. There are $2^{2^w}$ choices of $S$, and only $2^b$ fixed-length $b$-bit messages. Therefore $2^b\ge2^{2^w}$ and $b\ge2^w$. Conversely storing the characteristic vector of $S$ supports every suffix via existential joining over $Z$. $\square$

**Scope caveats:** For variable-length states, finite control and head positions must be charged or normalized; the asymptotic result is $2^w-O(1)$ bits after a fixed-width information-state convention. This is NOT a lower bound on arbitrary SAT solvers: FLMV supplies read-only indexed original input, which the wrapper can reread. A suffix containing private variables that overlap prefix-private variables is outside the disjoint-block model. The theorem measures retained information, not inference-node cost or parallel span.

## Established published hard-family control

**Family:** connected constant-degree, constant-edge-expansion cubic graph $G_H$ with odd vertex-charge vector $\chi$. Put one edge variable on each of $3H/2$ edges; each vertex contributes four signed width-three clauses forbidding the four assignments violating

$$
\bigoplus_{e\ni v}x_e=\chi_v.
$$

The original formula has $4H$ strict proper ternary clauses, binary encoded size $N=\Theta(H\log H)$ under conventional explicit indices, and is UNSAT by XOR summation over vertices.

**Published model and theorem:** Urquhart (JACM 1987) and Ben-Sasson/Wigderson (JACM 2001, Theorem 4.4 and Corollary 4.5) establish $2^{\Omega(H)}$ lower bounds for suitable expander Tseitin contradictions in **ordinary shared-DAG Resolution**. Expansion and bounded-degree assumptions matter. This is NOT a lower bound in historical full $R_{\mathrm{mix341}}$, Extended Resolution, GF(2), or against deterministic SAT algorithms.

**Known shortcut:** For a connected authenticated graph, XOR of all charges detects UNSAT in polynomial time. Its effective syndrome for charge changes is one bit (LSPV-2/447). Thus a wide structural frontier alone is not an information lower bound on *this* family. Conversely, Theorem 458.2 shows the full $2^w$ table can be necessary for other proper-3CNF prefixes in a one-pass erasure model. There is no lower-bound-preserving conversion from the constructed control prefixes to the certified Resolution-hard family; none is claimed.

## IDEA -> SEARCH -> ITERATE source ledger

Before experiments read BOTH live main trackers: proof1.txt blob **edf29de056457fa806e9d5ebc7548bf6f110505a**, proof2.txt blob **9f65c1936652d7e0eb298ee2516960aa88877b25**; relevant IDs **[P1-S3] [P1-01] [P2-A2] [P2-A4] [P2-A5]**. Read current issue #3 and comments, LSPV-2/457, LSPV-4/455, governing 2026-11-02 handoff, AGENTS.md/CODEX.md/project skill, GROKPROOF/2026-11-06_2316_PROGRESS.md blob a20fb8b3, Claude/world-ledger README blob de75a371, and Claude's Oct. 28 TeX assessment. Reuse prior source-erasure and gauge controls rather than claiming novelty.

**External inspected source/path/ref, and limitation:** konard/p-vs-np/proofs/complexity/README.md blob 7ee9a11e: single-tape finite-machine model, no SAT lower bound or same-machine FLMV simulation. blkph0x/p-vs-np-proof-research/affine_projection_recognition_lab/fixed_width_hierarchy/THEOREM.md blob 4aba9d94: existential projected-CNF relations in a different fixed-visible-width Boolean-hierarchy classification; no general SAT algorithm, no basis for a new novelty claim. meelgroup/frat-xor/format.md blob 986a21aa: legal original-clause/XOR provenance hints in a separate calculus, not native $R_{\mathrm{mix341}}$. berkeley-abc/abc/README.md blob 88a9d1a3: DAG-aware circuit rewriting tools, not correctness of the present machine transformation. openai/math/README.md blob cc5b0a03: research collection with heterogeneous validation statuses, no direct transfer theorem. Primary source FLMV author manuscript https://lance.fortnow.com/papers/files/tst.pdf §2.1 p.4 and Cor. 5.8 p.18 were inspected; the random-access read-only input is expressly retained, and the quoted $\beta(c)$ lower bound is model-specific. Web searches covered frontier/pathwidth DP, 3SAT clause gadgets, Tseitin expander Resolution theorems and the required new repositories. A separate Google-branded search interface and a native FLMV execution environment were not available.

**Independent construction and falsification:** Python tester exhaustively checked **276** distinct proper-3CNF prefix projection sets across $w=1,2,3$; verified all individual long-OR gadgets for widths $1,\dots,6$; checked all equality-pin distinguishing suffixes through width 4; rejected a sign-mutated control by a changed projection; and tested 16 original signed K4 Tseitin charge vectors against brute-force SAT. **7,937 Python checks PASS.** Separately implemented JavaScript verifier independently repeated 276 projection subsets, suffix/gadget tests, and **8,322 assertions PASS**. Locally executed independent JS SHA-256 **378a8e8b770aa02877a788fc8756056afe76329f4efc15379120b3d121f57bb0**; published script Git blob **c62fa906327246c9cc762dd727e2f0ba3ac2e1ba**. The tests are host-language semantics, not native indexed-machine time/space benchmarks or full source-parser byte acceptance tests.

## Resource ledger and transfer status

For each $S$, the explicit construction has $\le O(w2^w)$ distinct original clauses, $\le O(w2^w)$ variables, $\le O(w^2 2^w)$ encoded bits, and $O(w2^w)$ gadget construction operations before ID bit-cost. Query suffix $Q_a$ has $4w$ clauses and $O(w\log(w+1))$ encoded bits; a fixed bitmap uses exactly $2^w$ bits. A streaming state-construction implementation that literally writes this formula requires the corresponding charged time/space. These are formal encoding bounds, NOT a faster SAT solver. All attempts, source reads, construction, verification and output must be charged for any proposed machine wrapper.

**No historical $R_{\mathrm{mix341}}$ rule or weight was changed.** Weighted paid logical nodes, optimal proof DAG span, source-authenticated inference bits and historical accepted-native checker are NOT provided by this semantic information theorem. The free optimal-choice lower-bound relaxation remains intact.

**Revised claim:** Universal $o(2^w)$ one-pass state compression of arbitrary strict-3CNF frontier relations is impossible in this exact source-erasure model, even though selected established hard proof families such as Tseitin admit one-bit algebraic summaries. This does NOT close **[P2-A2]**: no effective recursively iterable solver-dependent, all-input, malformed-aware transformation for every SAT decider is constructed. **[P1-01] [P2-A5] and Route B B3 remain OPEN.** P versus NP is OPEN.