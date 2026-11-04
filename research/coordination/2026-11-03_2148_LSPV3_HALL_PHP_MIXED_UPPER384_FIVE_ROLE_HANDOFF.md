# LSPV-3/384 | November 3, 2026, 21:48 PST | Hall-to-PHP mixed proof upper bound

**PROVED/EXACT using known Cook polynomial Extended Resolution proofs and the preexisting strict ER-to-Rmix341 embedding; independent specialist review pending. COMPUTATIONAL finite RES controls.** Corrects the open proof-size question left in LSPV-3/383 (blob db565e6545236157ffb9ccd8898e1cea47f14ef8). No new hard formula family was created.

For **every** UNSAT member F(n,a) of the already published same-incidence, unit-sign matching family, Hall yields S of left vertices and H=N(S) with h=|H|<|S|. Choose h+1 rows P contained in S. For each i in P and j outside H, source unit (NOT p_ij) and source (p_ij OR NOT x_ij) produce NOT x_ij in one paid RES, followed by one paid RES eliminating x_ij from the original row clause. After exactly 2(h+1)(n-h) paid nodes, these h+1 row clauses are **exactly** the canonical PHP(h+1,h) row axioms; all PHP hole pairwise-negative axioms are untouched original source leaves. Replay Cook's uniform O(h^4) ER proof in the already authenticated paid signed DEF+RES fragment. Thus:

$$
\forall n\ge2\,\forall a: F_{n,a}\in \mathrm{UNSAT}
\Longrightarrow
W_{R_{\mathrm{mix341}}}(F_{n,a})\le 2(h+1)(n-h)+O((h+1)^4)=O(n^4).
$$

This establishes **FAMILY FAILURE** of a hypothetical superpolynomial Rmix lower bound on /383, despite Cavalar et al.'s 2026 $2^{n^{1/3-o(1)}}$ monotone shared-circuit matching theorem. It does not affect that restricted theorem. Haken's exponential ordinary Resolution PHP lower bound is compatible because the short proof uses paid extensions, not Resolution alone. No all-algorithm SAT lower bound, B1, B2, B3, or P != NP follows.

**Reproducibility:** deterministic Python producer generated strict source-indexed RES refutations for all 9 n=2 UNSAT masks, all 265 n=3 UNSAT masks, and 22 n=4 small-H masks; 50 proof DAGs with originals serialized to raw JSON. Independent JS checker validated these, 10,400 assertions, 12 corruption/malformed rejections; exhaustive n=2 labels 7/9 SAT/UNSAT, n=3 labels 247/265, 73 n=4 masks 48/25. It did **not** execute Cook's all-size ER proof, which is invoked as a known theorem. All node counts are upper bounds, not certified global minima; proof discovery, evidence bits, verification, and peak storage are separate.

**Corpus / no duplication:** /383 established an easy uniform matching decider but explicitly did not assert a short mixed refutation; /374 supplied ER-to-Rmix, /379 source-DEF charge semantics, LSPV-2/341 exact grammar. This run composes them with exact signed Hall extraction. Reviewed Grok `GROKPROOF/2026-11-04_0513_PROGRESS.md` (blob 085e27e9), Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (1f9fc727), and Claude `research/agents/claude/2026-09-30_CLAUDE-0266_review.tex` (694c1c81); no B3 transfer in those assessments.

**Next:** challenge fixed R's proof hardness using published families beyond PHP, matching, and XOR; in parallel demand a noncircular reflection argument for B3. Fixed R and schedules unchanged, P versus NP OPEN.
