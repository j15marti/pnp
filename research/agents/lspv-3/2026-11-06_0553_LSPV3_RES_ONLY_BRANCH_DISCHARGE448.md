# LSPV-3/448: Native-Resolution discharge of shared branching assumptions

**2026-11-06 05:53 PST | Route B | PROVED/RESTRICTED (Resolution-only), COMPUTATIONAL finite controls.** Historical R_mix341 accepted-byte grammar, full mixed lower bound, B3 and P versus NP OPEN.

## Hypothesis and falsifiers

Given two ordinary Resolution refutations of $F\cup\{x\}$ and $F\cup\{\neg x\}$, compile each into a proof from **F alone** of the opposite literal and join by one paid native Resolution step. No added split, discharge or weakening rule. Falsifiers: (F1) weakening/wrong-pivot requirement, (F2) assumption leakage across contexts, (F3) omitted AND branch, (F4) double charging shared nodes or corrupted source IDs. The repair uses copy/pruning of existing proved lines in place of weakening, and an explicit paid RES join. Ten hostile mutations test F1-F4. This is an explicit variant of a familiar Resolution deduction principle, not claimed as new scholarship.

## Theorem 448.1 (constructive Resolution discharge)

Let $F$ be non-tautological CNF and let $\pi$ be any source-indexed DAG **ordinary oriented binary Resolution** refutation **with no tautological source or derived clauses** of $F\cup\{\ell\}$ with one separately marked unit assumption $\ell$. There exists a pure Resolution DAG from source clauses $F$ deriving either $\square$ or $\neg\ell$, with **at most** the number $r(\pi)$ of distinct paid original RES nodes in $\pi$'s goal ancestry. This does not assume a native SPLIT/DISCHARGE/WEAKEN rule, a semantic oracle, a fresh auxiliary variable, or any discovery-cost lower bound.

**Proof.** Process the input DAG topologically. For each original line $C$, store either an actually derived source-authenticated clause $D\subseteq C\cup\{\neg\ell\}$, or an unmaterialized tautology marker $\top$ permitted only if $\ell\in C$. Copy original source $C$ exactly; mark the assumption unit $\ell$ by $\top$. At a Resolution node, if actual translated parents contain both complementary pivot literals, resolve them, and check $D\subseteq C\cup\{\neg\ell\}$. A tautological transformed result can only arise with $\ell\in C$, so mark it by $\top$ instead. If a pivot literal disappears from either stronger translated parent, **copy its already derived reference**: that clause is contained in the desired new target. If a parent is $\top$, a pivot other than the assumption literal leaves $\ell\in C$, so output $\top$; a pivot on $\ell$ allows copying the other actual parent. Two $\top$ premises cannot eliminate $\ell$ because **all input proof clauses are required to be non-tautological**. This theorem does not silently claim the same compiler for arbitrary proof streams containing tautological intermediate lines; such lines require separate pruning or normalization. Thus the invariant holds with at most one emitted paid RES per original paid RES, preserving source indices and acyclic sharing. At the empty-clause root the marker is impossible and $D\subseteq\{\neg\ell\}$, yielding $\square$ or $\neg\ell$. QED.

**Two-arm corollary.** Given refutations $\pi_+$ of $F,x$ and $\pi_-$ of $F,\neg x$ with $R_+,R_-$ paid RES ancestors, discharge both to derive $\neg x$ and $x$, respectively, unless one already derives the empty clause. If two units arise, one paid oriented native RES concludes $\square$. Therefore an exhibited proof gives

$$
W_{\rm RES}(F)\le R_+ + R_- + 1.
$$

Both arms are AND obligations unless another unconditional refutation succeeds. Free after-the-fact choice of a legal proof is respected. Shared unconditional subderivations are charged once in the union, not once per branch. The theorem concerns **pure RES** input proofs, NOT conditional AND3/GF(2)/DEF/LOCAL-CONVERT proofs. The generated proof uses only the already-declared historical native RES rule in LSPV-2/341, not an extension of R_mix341.

## Established hard-family / exact encoding / theorem / shortcut ledger

| Family | Lower-bound model, size and exact source encoding | Strongest allowed shortcut and transfer gap |
| --- | --- | --- |
| Urquhart 1987 cubic odd Tseitin | Growing suitable cubic expanders with $h$ vertices, $3h/2$ edge variables and $4h$ original proper signed ternary clauses encoding three-input parity at each vertex: $\Theta(h\log h)$ source bits. Exponential **ordinary shared Resolution** lower bound (also Ben-Sasson–Wigderson 2001). | Already established LSPV-2/341 *semantic mixed* AND3/GF(2) proof exactly $4h-1$ paid nodes on bridgeless instances. The finite K4 example below is only a validity control, not a certified hard expander. |
| Chvátal–Szemerédi 1988 random strict 3-CNF, Pang 2026 | $8n$ independently sampled signed proper ternary clauses on $n$ variables (sampling with replacement). A.a.s. exponential ordinary Resolution hardness. Pang's recent preprint reports $\exp(\Omega_{p,r}(n))$ DAG Res(PC$_r/\mathbb F_p$) lower bounds for fixed prime $p$, fixed $r$. | No transfer to complete paid DEF/AND3/GF(2)/LOCAL mixed calculus from these restricted models. |
| Braun bit-PHP, Pang 2026 | $N=2^\ell$ holes, $N+1$ pigeons, $N\binom{N+1}{2}$ width-$2\ell$ clauses; Braun $>\exp(N/(32768\ell^2))$ DAG Res(XOR) for $\ell\ge32$. A standard private-chain strict-3 form contains $N\binom{N+1}{2}(2\ell-2)$ clauses. | Cook ER and LSPV-3/441,/446 give *conditional polynomial upper* witnesses in separately declared stronger grammars. Equisatisfiability alone does not preserve any lower bound under strict-3 reduction. |

Haken ordinary Resolution PHP, Cook ER PHP, and Tseitin GF(2) are mandatory contrasting controls. Neither restricted proof complexity nor empirical solver hardness is all-machine hardness.

## Original-source-authenticated finite verification

Original source is $K_4$ odd-charge cubic Tseitin strict 3-CNF with lexicographic six edge variables, charge vector $(1,0,0,0)$ and **16 original ternary clauses**. Exact **163-byte ASCII DIMACS** SHA-256 is:

ea08104837e167b9ebd06d8f50442d828e3ba4d81f79dff8c14a09ba30050096

For **each of the six edge-variable pivots** a Python producer made both complete source/assumption-labelled branch refutations. Every branch has 19 paid RES ancestors, 12 original-source ancestors and one marked assumption. Independent discharge gives 15 paid RES per resulting unit; the native RES join produces an unconditional proof with **31 distinct paid RES nodes, 16 indexed source ancestors, 47 total root-ancestry nodes, and unit-weight critical-path depth 5**. All 64 original assignments were checked: UNSAT. The even-charge all-zero assignment is a SAT control. The established full-mixed exact optimum on this same $K_4$ source is **15 paid nodes** by /341; this run therefore supplies a legal but nonoptimal **upper-bound control**, not a new full-mixed hardness bound.

An independently written Node.js verifier reconstructed the exact original source, authenticated its SHA, checked every branch and compiled proof source reference, signed pivot, exact resolvent, DAG topology, scope and final empty clause. Across six full packets plus ten mutations it passed **55,327 assertions** and rejected **10/10** deliberate corruptions: source SHA, source polarity, missing branch, assumption polarity, forged source index, wrong final pivot, bad root, illegal unconditional assumption, cross-arm substitution and corrupted branch dependency. The verifier is *independent software*, not the authoritative historical native checker.

## Resource and continuity audit

Six complete typed proof packets occupy **6,257,568 JSON bits**. Their verbose encoding is not minimal; compact explicit reference/record evidence has upper bound $O(B+r\log(B+r+2))$ for original input proof bits $B$ and paid RES nodes $r$. Python proof generation ran under 0.3 seconds per pivot, and one recorded run used **96,520 KiB** peak RSS. Independent Node validation including ten hostile controls took approximately **0.65 seconds**, **38,504 KiB** peak RSS. These are host measures, **not** FLMV same-machine exponents. For an implemented upper-bound algorithm one must additionally charge source/index/head reads, full parsing, clause hashing, branch discovery/saturation including failed attempts and non-ancestor lines, mapping, references/retrieval, caching/recomputation, verification, output and *all-phase* peak live memory; minimum logical DAG work excludes discovery cost intentionally.

Reviewed original native semantic grammar in research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb), governing November 2 handoff at 4e29ed7646f484707767acb6e63ec5f38afd98a8, issue #3 including /447 and LSPV-1/448, REFEREE385, AGENTS.md/CODEX.md/skill, actual Grok REWIRE and GROKPROOF progress files, and Claude TPORT-0001. Checked **both required repositories**: konard/p-vs-np README and scripts/proof_status.json (blobs 0e0ec77f..., 93b77ed3...); blkph0x/p-vs-np-proof-research METHOD_INDEX.md and AFFINE_RECOGNITION_LIMITS_REVIEW.md (blobs 18d693ea..., 4e87c1da...). Consulted FRAT-XOR, CakeML/LPR, short-proof and openai/math actual READMEs and indexed primary literature. No independently authenticated historical DEF-owner/LOCAL/private port byte grammar emerged. Google-branded direct search was unavailable; indexed search used. Root main.tex (~1.76 MB) was not edited, because safe full-content retrieval was unavailable; no foreign regions, scheduler tasks, role assignments or weights were mutated.

**Actual advance:** source-authenticated pure-native-RES two-arm branching proof compiler with an explicit no-weakening discharge construction and six fully replayed K4 controls. **OPEN:** historical complete mixed accepted-byte grammar, discharge of conditional **mixed** proof DAGs, superpolynomial $\overline W_{R_{\rm mix341}}$ across all rules, noncircular same-R B3, and P versus NP.

Primary sources: Urquhart (1987) JACM 34:209-219; Ben-Sasson/Wigderson (2001) JACM 48:149-169; Chvátal/Szemerédi (1988) JACM 35:759-768; Braun arXiv:2609.23015v2; Pang arXiv:2610.00837v2.
