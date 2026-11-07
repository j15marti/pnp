# LSPV-1/480 | Stronger bit-PHP original-source backtranslation bound

**2026-11-07 09:12 PST | Route B lead | KNOWN THEOREM application / PROVED-RESTRICTED deduction / COMPUTATIONAL controls. P versus NP OPEN.**

**Affected node [P2-F3]**, extending LSPV-1/454. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. All historical R_mix341 rules/weights, roles, schedules and the two Route A / three Route B allocation unchanged.

## IDEA -> SEARCH -> ITERATE

Hypothesis: the original bit-PHP lower bound used in LSPV-1/454 can be strengthened from Braun's exp(Omega(n/log^2 n)) to exp(Omega(n)) without changing source or proof system. Four predeclared falsifiers: F1, Pang lacks the exact original width-2ell collision source; F2, he excludes arbitrary DAG sharing or changes prime/degree; F3, the separate FACET-A strict-3CNF proof is superpolynomial; F4, semantic vs syntactic Res(XOR) weakens the theorem.

Read BOTH complete root proof trackers, issue #3 and latest comments, November 2 five-role handoff, AGENTS.md, CODEX.md, repo research SKILL, prior LSPV-1/454, /478, /479, LSPV-3/456, LSPV-5/412 and /413, Grok progress GROKPROOF/2026-11-07_0819_PROGRESS.md and Claude report research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex. Required change-aware reads: konard/p-vs-np/scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and REVIEW_ADDENDUM.md blob 6a7cc2f8962d3fcfcfc1778b1d3d8f5dc8d56d70; meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f; openai/math/README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae. GitHub queries included R_mix341, Pang bit PHP, bit pigeonhole, AND3, Grok, Claude and P2-B20; indexed general web search was used, no separate Google-branded interface.

Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, 2026-10-24, Section 7.1 and Theorem 7.2(e), https://arxiv.org/html/2610.00837v2, applies to the **original collision-clause bit-PHP** with n=2^ell holes and m=O(n) pigeons, fixed prime p and fixed r>=1, every DAG-like Res(PC_r/F_p). It proves exp(Omega_{p,r}(n)) lines. Taking p=2,r=1 is Res(XOR) on the same original source, improving Braun's exp(Omega(n/ell^2)) theorem. Pang Remark 1.2 states semantic weakening has a polynomial syntactic simulation. No initial falsifier fires at this restricted scope. This is a 2026 preprint, not independently formalized here.

## Exact family/theorem/encoding/known method ledger

The original bit pigeonhole family B_ell has n=2^ell holes, m=n+1 pigeons, m*ell original address bits. One original width-2ell collision clause C_(i,j,z) forbids pigeons i<j simultaneously choosing address z in {0,1}^ell. There are

$$
A=n\binom{n+1}{2}=\frac{n^2(n+1)}2
$$

original clauses. UNSAT follows by pigeonhole. This source is not strict 3-CNF. The distinct equisatisfiable strict proper 3-CNF C_ell is the standard private-chain split of each original clause into 2ell-2 ternary source clauses with 2ell-3 private auxiliary variables. Hence

$$
S=A(2\ell-2),\quad V=(n+1)\ell+A(2\ell-3),\quad N_\ell=\Theta(n^3\ell^2)
$$

for signed-indexed binary source length N_ell. Equisatisfiability alone NEVER transports Pang proof-size hardness to C_ell.

The **mandatory short-proof upper-bound control** is the Cook-style Extended Resolution proof in separately declared FACET-A, REFEREE379 and LSPV-1/454. Its strict-source C_ell paid node count is

$$
Q=A(4\ell-3)+(n+1)(2n\ell-9)+\frac{n(n+1)(27n^2+11n-14)}{24}.
$$

For ell>=32 prior LSPV-1/454 established Q<=2n^4 and S<=n^4, hence Q+S<=3n^4. FACET-A is NOT authenticated historical R_mix341. Peer LSPV-5/413 recovered a byte-exact historical source/AND3/XOR checker and proof packet; it rejects RES, DEF and LOCAL-CONVERT as unknown tags, so cannot authenticate mixed RES->AND3, native DEF facets, or FACET-A. [P2-D1] and [P2-C3] remain OPEN.

## Theorem 480.1 (PROVED-RESTRICTED, conditional on the cited primary theorem)

For some fixed c>0 and sufficiently large powers of two n, any transformation, even nonuniform, noncomputable, with free optimal selection, mapping the exhibited separate-FACET-A proof of C_ell into a valid **original-B_ell-source** Res(XOR) DAG refutation must emit at least exp(cn) lines. Consequently

$$
\frac{\#\mathrm{output\ lines}}{Q+S}\ge\frac{\exp(cn)}{3n^4}=\exp(\Omega(n)).
$$

In the bit length of the **strict 3-CNF input source**,

$$
\boxed{\#\mathrm{original\ source\ output\ records}
\ge\exp\left(\Omega\left(\frac{N_\ell^{1/3}}{(\log N_\ell)^{2/3}}\right)\right).}
$$

This strengthens LSPV-1/454's earlier Braun-based denominator (log N_ell)^(8/3) to (log N_ell)^(2/3). **Proof:** Pang Theorem 7.2(e) lower-bounds all original B_ell Res(XOR) DAG refutations. Every converter output is one of those by hypothesis. Divide the line lower bound by the separate FACET-A input DAG bound Q+S<=3n^4. Use N_ell=Theta(n^3 ell^2), ell=Theta(log N_ell). Explicit line output takes at least one bit and one emission operation per record, but exponential output need not entail exponential *peak* working space. QED. No numerical c is claimed. Pang Remark 1.2 polynomial syntactic simulation preserves the exponential even if semantic weakening is allowed.

**Critical non-transfer:** This proves ONLY an original-source, proof-system-specific **output backtranslation obstruction**, not mixed-R_mix341 minimum hardness for C_ell, not original C_ell Res(XOR) hardness, not SAT-algorithm time, not a noncircular B3 transfer. Every legal shortcut, shared DAG and conservative paid extension is available when minimizing historical native R. We do not suppress Cook ER or affine shortcuts.

## Finite tests and resources

Published independently authored dependency-free Node audit, experiments/arc/lspv1_480_bphp_pang_transfer.cjs, raw results/raw/arc/2026-11-07_0912_LSPV1_480_BPHP_PANG_TRANSFER_RAW.json, reports 8,966 successful assertions. Checks exact A,S,V,Q for n=4,8,16,32,256,1024,4096; original collision-clause source polarity on n=4,8,16; exhaustive existential private-chain gadget projection at widths 4,6,8,10 and private-wire assignments; nine malformed hole counts rejected. Independent Python check replay passed 40 comparisons. Local Node wall time 0.05s and maximum host RSS 32,412 KiB including interpreter startup, construction, output. Finite checks do NOT execute Pang's asymptotic proof, full all-size FACET-A certificate, or an authenticated full historical mixed checker. For any actual compiler count parsing, index/head reads, source authentication, proof construction, failed search, all evidence bits, output, caches, retrieval/recomputation and simultaneous peak storage. No FLMV same-machine exponent follows.

**Precise remaining gaps:** [P2-D1] authoritative complete historical mixed grammar and cross-rule acceptance; [P2-C3] legal native all-rule transfer or counterexample; [P2-B1] superpolynomial minimum across ALL permitted native mixed shortcuts; [P2-B2] noncircular SAT in P => worst-case native-R minimum polynomial. Route A all-input same-machine FLMV contraction also OPEN. P versus NP OPEN.

**References:** Pang (2026) arXiv:2610.00837v2, Theorem 7.2(e); Braun (2026) arXiv:2609.23015v2; project LSPV-1/454 and LSPV-5/REFEREE379, /413. No novelty attributed to this finite audit.