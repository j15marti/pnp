# LSPV-2/391: NP-complete affine source repair distance with a five-node Resolution refutation

**November 4, 2026, 06:10 PST.** **PROVED/EXACT:** explicit all-size reduction, representation scaling and five-step strict RES certificate. **COMPUTATIONAL:** independently checked finite controls. External specialist mathematical review remains pending. **KNOWN:** unweighted Simple Max Cut NP-completeness, Garey, Johnson and Stockmeyer (1976). **OPEN:** B1, B2, B3, superpolynomial worst-case minimum in full R_mix341, and P versus NP.

## Fixed calculus, starting theorem and input models

Keep the unchanged original R_mix341 of LSPV-2/341, Git blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. Signed original source clauses are labelled free leaves; each distinct paid inference costs one; shared-DAG inferences count once. Strict binary Resolution (RES) is a native rule. AND3, GF(2), authenticated LOCAL-CONVERT and conservative charged signed-AND2 definitions remain available; their complete machine grammar has not been finalized. The new upper certificate uses only strict RES, so this grammar gap does not affect it.

Established hard-family anchor: Haken (1985) proves that there exist c>0 and h0 such that for every h>=h0, **every ordinary unrestricted shared-DAG Resolution refutation** of standard unary PHP(h+1,h) requires at least 2^(c h) lines. The input contains h(h+1) variables, (h+1)+h*binom(h+1,2) clauses and Theta(h^3 log(h+2)) explicit signed indexed input bits. This theorem does not cover Extended Resolution, Res(oplus), full R_mix341 or arbitrary uniform SAT machines. Cook's 1976 polynomial Extended Resolution PHP proofs are the mandatory control. Neither hard family is regenerated here.

## Theorem: NP-complete source repair distance on a trivially UNSAT affine promise

For a signed source CNF F with original clause labels, define the deletion-to-SAT distance

$$
\delta(F)=\min\{|D|:F\setminus D\text{ is SAT}\}
          =\min_{a}\#\{\text{original labelled clauses falsified by }a\}.
$$

Both equalities are exact, including with duplicate labels. They define a **source-relative optimization statistic**, not proof cost or machine time.

For any simple graph G=(V,E), introduce Boolean variables x_v. Represent each equation x_u XOR x_v=1 by its complete pair of signed 2CNF clauses (x_u OR x_v), (NOT x_u OR NOT x_v). Append a disjoint three-variable triangle with these same three edge equations; denote the entire formula F_G. This is ordinary signed 2CNF, all rows affine. It has 2(|E|+3) clauses, |V|+3 variables, and O((|V|+|E|+2) log(|V|+|E|+4)) indexed encoding bits. Its source can be constructed uniformly in polynomial bit-time. Every F_G is UNSAT because its triangle is not 2-colorable.

**PROVED/EXACT for every G:**

$$
\boxed{\delta(F_G)=|E|-\operatorname{MaxCut}(G)+1},\qquad
\boxed{W_{R_{\mathrm{mix341}}}(F_G)\le5}.
$$

**Proof of the identity.** For any assignment, an edge whose endpoints differ satisfies both clauses; an equal-ended edge falsifies exactly one clause. The G component therefore falsifies |E|-cut_G(a) clauses, while the independent odd triangle requires exactly one violated edge at its optimum. Minimization over all assignments gives the formula.

**Five-step strict Resolution proof.** Name the six triangle source clauses C0=(a OR b), C1=(NOT a OR NOT b), C2=(b OR c), C3=(NOT b OR NOT c), C4=(a OR c), C5=(NOT a OR NOT c). Derive C6=(a OR NOT c) from C0,C3 pivot b; C7=(NOT c) from C6,C5 pivot a; C8=(NOT b OR c) from C1,C4 pivot a; C9=(c) from C8,C2 pivot b; finally the empty clause from C7,C9 pivot c. Each new statement has exactly two authenticated parents, an explicit pivot and no auxiliary gates. The other source clauses are unused. Five is a proved **upper bound** for F_G, not claimed to be its mixed-system global minimum.

**NP-completeness on the all-UNSAT promise.** From an unweighted Simple Max Cut decision instance (G,k), output the syntactically recognizable pair (F_G, |E|-k+1). It has repair distance at most the threshold iff G admits a cut of size at least k. The output is always an UNSAT affine 2CNF. Membership in NP follows by checking the graph-to-CNF grammar and a proposed assignment with at most the specified number of falsified clauses. Thus the restricted repair decision language is NP-complete. This is a consequence of existing Max Cut hardness; it is not an unconditional superpolynomial time lower bound and does not imply SAT on the promised sources is hard.

## Stronger representation-independence falsifier

For every CNF F and integer r>=1, let F^[r] contain r distinct source labels for every original clause. It has exactly the same satisfying assignments as F, yet

$$
\boxed{\delta(F^{[r]})=r\delta(F)}.
$$

Indeed, for each assignment its count of false labelled clauses is multiplied by r, and taking a minimum commutes with that constant factor. One original triangle copy still yields the same five-step proof of F_G^[r]. Likewise, let G be the disjoint union of s triangles. Then delta(F_G)=s+1 tends to infinity while a five-node Resolution refutation remains available for every s. This falsifies any assertion that an unbounded source repair statistic alone forces long optimal mixed refutations or long arbitrary computation.

## Falsifiers and exact controls

**F1 (FAILED candidate):** NP-hard-to-evaluate repair distance implies large W_R. The five-node certificate refutes this even on the full all-UNSAT promise family. **F2 (FAILED candidate):** deletion distance is invariant under logically identical encodings. Duplicate labels multiply it by r. **F3 (FAILED transfer):** affine feasibility being polynomial-time makes every affine optimization polynomial-time. Feasibility of this promise is trivial, but repair decision is NP-complete. This does not prove P != NP.

Primary Python enumerated **all 1,099 labelled simple graphs with 1 to 5 vertices**. It checked 272,041 assignment-level or consistency conditions. The independent no-import JavaScript checker reconstructed every source, enumerated all 2^(n+3) assignments and graph cuts, and passed **305,923 checks** with six rejected corrupt/malformed payload controls. The exact distance histogram over the 1,099 graphs is: delta 1:427, delta 2:515, delta 3:146, delta 4:10, delta 5:1. Disjoint one-, two- and three-triangle controls were enumerated; the all-s theorem is algebraic, not extrapolated. A separate all-equality parity control is SAT with the all-zero assignment. No exhaustive minimum-proof search is claimed; a five-node legal proof is only an upper certificate.

Publication: primary `experiments/arc/lspv2_391_clause_repair_maxcut.py`; independent `experiments/arc/lspv2_391_independent_verify.js`; raw `results/raw/arc/2026-11-04_0610_LSPV2_MAXCUT_REPAIR391_raw.json`. Command: `python3 experiments/arc/lspv2_391_clause_repair_maxcut.py > out.json && node experiments/arc/lspv2_391_independent_verify.js out.json`. No external packages, random inputs or seeds are used.

**Logical vs physical work:** The five nodes are not five physical machine steps. Input authentication, variable-index parsing, source clause retrieval, proof emission, pivot checking and output consume polynomial bit-time and polynomial peak memory in N on a conventional materializing implementation. Optimizing delta is a separate NP-complete task. The finite exhaustive experiment's work is not solver runtime. Exponentially large intermediate encodings may be legal but must have their real reading, construction and space costs charged. No FLMV transport, B1/B2/B3 implication, or arbitrary SAT lower bound follows.

## Corpus, novelty and external assessment

**CORPUS REVIEWED:** refocus `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` blob `033b54b8`, issue #3, AGENTS.md, CODEX.md, pnp-research skill, original /341, /389, /390, LSPV-3/393 duplicate source-block handoff, LSPV-5/337 dominance firewall, LSPV-1/297, current Grok `GROKPROOF/2026-11-04_1322_PROGRESS.md` blob `0850246c`, and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727`. Root main.tex was recovered as an entire 1.6 MB Git blob for examination.

**DUPLICATION / CONTRADICTION AUDIT:** The graph cut defect |E|-MaxCut already appears in LSPV-1/297. LSPV-2/390 already provides exact singleton affine clause-indispensability spectra; LSPV-3/393 already shows duplicate source labels can destroy singleton criticality. The present contribution is a specific all-UNSAT, exact 2-XOR 2CNF **NP-complete optimization versus five-node refutation** separation with a uniform reduction and certificate. This is a project countercontrol, not a claim of novel Max Cut hardness. Root MAIN's prior exact theorems are not superseded or strengthened.

**GROK/CLAUDE:** Grok's latest FLMV selector conjecture is still unsupported at all-input uniform quantifiers; its self-reduction remarks concern a restricted architecture, not every adaptive SAT solver. Claude TPORT-0002 concerns a restricted alternation-trading rule portfolio. Neither supplies B3. They were independently assessed for applicability rather than treated as proof authorities.

**ADOPTED:** fixed authenticated two-premise proof semantics, Gaussian elimination as an affine SAT shortcut, and the source-deletion notion. **REJECTED:** source repair distance as a lower bound on proof nodes or time across representations. **POTENTIALLY STALE CLAIM:** any free MaxCut distance query or general lower-bound inference from it. **WHAT CHANGED RELATIVE TO ROOT MAIN:** adds a failure mode and a strictly checked five-node countercertificate, without altering the R_mix341 grammar or any earlier proved optimum.

Primary references: [1] Garey, Johnson, Stockmeyer, *Some simplified NP-complete graph problems*, Theor. Comput. Sci. 1 (1976) 237-267, DOI 10.1016/0304-3975(76)90059-1. [2] Haken, *The Intractability of Resolution*, Theor. Comput. Sci. 39 (1985) 297-308. [3] Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4) (1976) 28-32. [4] Berlekamp, McEliece, van Tilborg, *On the Inherent Intractability of Certain Coding Problems*, IEEE IT 24 (1978) 384-386.

**Next:** Test more promising source-restoring *block* invariants against cheapest-proof pruning and conservative extensions in the full combined calculus. B3 and a superpolynomial Wbar_R bound remain OPEN. P versus NP remains OPEN.
