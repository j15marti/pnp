# LSPV-1/472 | Sharp source-local GF(2) barrier in a published Resolution-hard 3-CNF family

**2026-11-07 03:55 PST | Route B | PROVED/RESTRICTED symbolic, COMPUTATIONAL finite.** The historical accepted-byte \(R_{\mathrm{mix341}}\) checker was NOT executed. P versus NP OPEN. Relevant nodes: [P2-B1], [P2-B2], [P2-B13] (new restricted evidence), [P2-D1], [P2-D2], [P2-C3], [P2-F8].

## IDEA and falsifiers

Hypothesis: A fixed-linear-density Chvátal–Szemerédi random proper 3-CNF, already proved hard for ordinary shared-DAG Resolution in its published model, has with high probability **no direct affine equation implied by any subset of at most four original source clauses**. This is not a statement about arbitrary derived clauses.

Predeclared falsifiers: F1, three proper 3-clauses force a nontrivial affine equation; F2, four proper 3-clauses with four distinct unsigned support triples force one; F3, a proposed checker requires all four affine-source clauses to use exactly one triple and wrongly excludes legal mixed-support shortcuts; F4, duplicate source triple probability fails to tend to zero for m=Theta(n). Theorem 472.1 refutes F1; Theorem 472.2 refutes F2; explicit legal mixed-support parity refutes the overly strong F3; exact union bound refutes F4. No universal mixed-system hardness is inferred.

## SEARCH and precedence controls

Read BOTH complete root proof trackers (at start proof1 blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, proof2 blob 9809e0302c00c009cd50db3d6e2ab300de192751), governing five-role handoff, issue #3 with its current comments, AGENTS.md, CODEX.md, and .codex/skills/pnp-research/SKILL.md. Read actual original LSPV-2/341 report at \`research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex\` (blob c87acd11), LSPV-1/471, LSPV-3/471, Grok \`GROKPROOF/2026-11-07_1119_PROGRESS.md\` (d87fcb3a) and Claude \`research/agents/claude/world-ledger/README.md\` (de75a371). The historical /341 *declared semantic* rules are unit-paid RES, at-most-three-original-variable AND3, binary XOR of GF(2) rows, LOCAL-CONVERT of one derived local factor, and conservative charged fresh two-input DEF. Historical accepted-byte syntax, exported/private-wire scope and faceted source binding remain unauthenticated under [P2-D1]; CANON variants are not silently substituted.

Outside-project actual files: \`konard/p-vs-np/scripts/proof_status.json\` (blob 93b77ed3) and \`proofs/complexity/README.md\` (7ee9a11e); \`blkph0x/p-vs-np-proof-research/METHOD_INDEX.md\` (18d693ea) and \`REVIEW_ADDENDUM.md\` (6a7cc2f8); \`meelgroup/frat-xor/format.md\` (986a21aa); \`tanyongkiam/cake_lpr/README.md\` (e94f45e9); \`openai/math/README.md\` (cc5b0a03). These define other proof/model interfaces, NOT the historical checker.

Primary published-family sources: Chvátal and Szemerédi, *Many Hard Examples for Resolution*, JACM 35(4), 759–768 (1988), DOI 10.1145/48014.48016, with exact random-density/length assertion checked against a historical technical report (ACM publisher PDF returned 403), and Gryaznov–Talebanfard, *Bounded-Depth Frege Lower Bounds for Random 3-CNFs via Deterministic Restrictions* (2024), arXiv:2403.02275, a **different restricted** superlinear result. Google-branded search was not independently available. GitHub connector was used for real source reads, not search snippets alone. Prior LSPV-2/341 had already established efficient GF(2) refutations for odd-Tseitin, and LSPV-1/357 plus LSPV-5/376 had already recorded Gödel/reflection firewalls. Neither is rebranded as new. Root \`main.tex\` range returned SHA but empty content, so no unsafe root-manuscript write occurred.

## ITERATE, proved mathematical lemmas

**Theorem 472.1 (sharp width-w source budget).** For a conjunction F of m proper width-w clauses on n>=w original variables, if m<2^(w-1), F cannot entail ANY nonconstant GF(2) affine equation. At equality m=2^(w-1), if F entails one such equation, F is semantically exactly that equation.

**Proof.** A proper width-w clause falsifies precisely 2^(n-w) assignments. The union of m falsifying cubes has at most m*2^(n-w) assignments. A nontrivial affine equation over GF(2) is false on exactly 2^(n-1) assignments. Therefore implication requires m>=2^(w-1). At equality the union of excluded assignments has exactly the same cardinality as the bad affine halfspace and contains that halfspace, hence the sets are equal. This is sharp: the conventional parity packet consists of exactly 2^(w-1) width-w clauses. QED.

**Theorem 472.2 (sharp 3-CNF duplicate-unsigned-support necessity).** Suppose four proper signed width-three clauses entail a nontrivial affine equation. Then at least two of the four original clauses use the **same unordered triple of variable names**. Accordingly, any proper 3-CNF whose source clauses all have distinct unsigned triples has no nontrivial affine equation implied by ANY subset of at most four original clauses.

**Proof.** At equality the four disjoint falsifying 3-cubes exactly partition the affine row's bad halfcube. Each source cube must include every variable appearing with nonzero coefficient in the affine row, since changing a missing variable within a source cube reverses parity. Thus the row has support size d=1,2 or 3. If d=3, all four triples are the same. If d=2, there are two forbidden assignments on the row's two variables. Each must be partitioned by exactly two of the four codimension-three cubes. For a pair of such cubes to cover all residual assignments, their third variable must be the same and their specified signs opposite, giving a repeated triple. If d=1, fix the row variable to its forbidden value. Four disjoint codimension-two subcubes partition all remaining Boolean assignments. In sign coordinates z_i in {-1,+1}, the indicator for each is (1+alpha*z_i)(1+beta*z_j)/4. Since the four indicators sum identically to 1, every quadratic Fourier coefficient z_i*z_j cancels. If all four pairs {i,j} were distinct, each such coefficient appears exactly once with nonzero value +/-1/4. Impossible. Therefore a pair and hence an original triple repeats. QED.

**Mandatory legal shortcut control.** The four proper source clauses

$$
(x\lor y\lor a)\land(x\lor y\lor\neg a)\land
(\neg x\lor\neg y\lor b)\land(\neg x\lor\neg y\lor\neg b)
$$

are exactly equivalent to $x\oplus y=1$, despite using TWO different unsigned triple supports. Two paid ordinary Resolution steps yield $(x\lor y)$ and $(\neg x\lor\neg y)$, after which a sound, *properly authenticated* conversion might express the row. A same-triple-QUARTET-only shortcut finder is therefore incomplete. Historical native conversion legality/weights remain [P2-D1] OPEN. This legitimate upper control must not be excluded to manufacture a lower bound.

**Theorem 472.3 (published random family, source-local lower control).** Sample m=cn distinct signed proper 3-clauses uniformly from the 8*binom(n,3) available, with fixed c>5.6 (e.g., c=6). For two different selected signed clauses the probability of identical unsigned support is exactly 7/(8*binom(n,3)-1). Therefore by union bound

$$
\Pr[\text{repeated unsigned triple}]
\le {m\choose 2}{7\over 8{n\choose3}-1}=O_c(1/n).
$$

With probability tending to one the source has no four-clause direct affine extraction. Chvátal–Szemerédi also established, for compatible standard random proper 3-CNF with c/8>0.7, that with high probability the formula is UNSAT yet *ordinary Resolution* needs at least (1+epsilon)^n generated clauses. The intersection of these high-probability events is high probability. The binary literal-index source has N=Theta(n log n) bits, so the scoped Resolution lower bound is 2^Omega(N/log N). **No corresponding lower bound is proved for R_mix341 or arbitrary SAT algorithms.**

**Native-AND3 first-step implication.** Under /341's *declared* AND3 combined-support<=3 condition, two distinct original proper width-three clauses can be its two antecedents only when they have identical unsigned triple support. Thus the same random source w.h.p. has no AND3 combining two different ORIGINAL clauses at initialization. Paid Resolution-derived narrower clauses and auxiliary definitions can still permit later AND3/XOR/LOCAL-CONVERT, so this is not even a claim about the whole first computational phase.

## Finite original-source controls and full resources

Standalone, GitHub-readback executed V8 verifier \`experiments/arc/lspv1_472_source_local_affine.js\` (blob 8200efd9) enumerated **all** 32 signed proper clauses on n=4 and 80 on n=5. It checked **4,960 / 82,160** clause triples and **35,960 / 1,581,580** clause quartets. Of those quartets **128 / 500** encode a nontrivial affine equation exactly; **72 / 360** use more than one unsigned triple; **zero** have all four support triples distinct. It checked the non-packet two-support XOR exactly on all sixteen assignments, plus K4 signed original odd/even Tseitin (16 clauses, 6 variables): odd 0 SAT assignments, even 8 SAT assignments, deleting each of sixteen odd-charge source clauses restores SAT. It passed **87,784** checks. An independent Python implementation locally reran ALL n=4/5 triples and quartets with independent masks, passing **87,750** checks and reproducing the exact category counts. Separate earlier locally executed JS producer included 90,815 checks, malformed-source fixtures, vertex parity packet truth tables, and peak-RSS/time instrumentation. See published raw ledger.

Resource and method accounting: ideal source-local premise count is **not** the project's paid inference work; it has no algorithmic discovery cost by definition. The standalone exhaustive checker explicitly enumerates 1.58 million quartets at n=5, caches truth masks and candidate sets, and is not an efficient all-input SAT decider. Reading/validating the original source, building signed support indices, hashing/sorting unsigned triples, later inference search, GF(2) row bits, source IDs, shared references, output validation, rejected policies and simultaneous peak memory would all be charged by a realizable native solver. Standard sorting/hashing can detect duplicate supports in polynomial time, but it does not decide UNSAT. No FLMV computation/time-space inequality follows.

## Status, exact family ledger and missing transfer

**Family:** Chvátal–Szemerédi ordinary random signed proper 3-CNF, m=cn (fixed c=6 suitable), n original variables, N=Theta(n log n) bits; **published theorem:** UNSAT and exponential ordinary Resolution refutations w.h.p.; **new source-local result:** no four-source affine equation and no two-original-clause AND3 in /341-declared semantics w.h.p.; **known methods:** arbitrary RES, shared DAGs, AND3 after derived binaries, paid DEF and LOCAL-CONVERT remain legal, and odd-Tseitin demonstrates very short mixed GF(2) refutations; **missing transfer:** a superpolynomial invariant surviving the FULL FIXED all-rule R_mix341 with source authentication, branching and sharing. Theorem 472.3 is not a lower bound on Wbar_Rmix341. Independent finite formulas are SAT/UNSAT *controls*, not certified hard individual instances.

**Affected tracker:** new strictly restricted evidence node [P2-B13] under open [P2-B1]; proof1.txt reviewed with NO MATERIAL CHANGE. Keep [P2-D1], [P2-B1], [P2-B2], [P2-C3] OPEN, B1/B2/B3 unresolved, no P-vs-NP resolution. No changes to historical rules/weights, agent identities, titles, schedules, enabled states, two Route A/three Route B allocation, or main.tex.

References: [Chvátal–Szemerédi 1988, DOI](https://doi.org/10.1145/48014.48016); [Gryaznov–Talebanfard 2024](https://arxiv.org/abs/2403.02275); [historical LSPV-2/341](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex). P versus NP **OPEN**.
