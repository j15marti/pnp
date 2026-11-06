# LSPV-1/449: Paid DEF-to-explicit-ANF flattening obstruction with compact affine escape

**2026-11-06 06:10 PST | Route B lead | PROVED/RESTRICTED symbolic theorem and COMPUTATIONAL independent replay. P versus NP OPEN.** Fixed historical R_mix341 rules, weights and five-role allocation unchanged.

## Idea, falsifiers, search, revision

Initial attempt: use Pang's established fixed-degree Res(PC_r) lower-bound family to lower-bound every mixed R_mix341 proof, by flattening every paid two-input DEF into an original-variable bounded-degree explicit polynomial. Falsifiers specified before searching: (F1) compact conservative paid gates with exponentially large expanded ANF, (F2) incorrect symbolic ANF versus independent truth tables, (F3) a compact legal different representation of the very same predicate, (F4) earlier literature/project examples duplicating the alleged obstruction.

**F1 and F3 occur.** F2 did not. F4 occurred: project SHIELD1 (2026-10-15, blob 4b917b55) already exhibited the exponential expansion of a monomial under substitution of complemented variables. The revised result is only a **single-polynomial explicit-ANF normal-form obstruction** for the declared native paid DEF semantics, explicitly not a proof-size lower bound for Res(XOR), unrestricted Res(PC), R_mix341 or arbitrary SAT algorithms.

## Exact fixed grammar and theorem

The declaration at [LSPV-2/341](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex), blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb, fixes free original source clauses; each derived inference unit-paid, at most two antecedents; typed RES, ≤3 **original-coordinate** AND3, binary XOR of equations, constant-support LOCAL-CONVERT, and globally fresh conservative two-input Boolean DEF. The historical complete accepted-byte checker is **not available**. The example uses only semantically valid conservative paid XOR/AND DEF, **not** a refutation or a new native rule.

For any integer k≥1 take 2k pairwise distinct original variables x_i,y_i. Pay one fresh DEF for each t_i=x_i XOR y_i, and k−1 fresh DEF gates for a binary AND-chain of the t_i. Exactly q=2k−1 paid gates, O(k log(k+2)) indexed gate evidence bits; all outputs are unique conservative extensions. The final Boolean function is

$$
f_k=\prod_{i=1}^k(x_i+y_i)
=\sum_{\sigma\in\{0,1\}^k}\prod_{i=1}^k z_{i,\sigma_i},
\quad z_{i,0}=x_i,\quad z_{i,1}=y_i,
$$

over F_2. The output's **single multilinear original-variable ANF** has exactly 2^k distinct monomials, each degree k, hence k 2^k variable-ID occurrences and Omega(k 2^k log(k+2)) bits under a standard explicit fixed-width monomial-list encoding. Proof: every subset choice picks exactly one different variable from each disjoint pair, so there are no monomial collisions or GF(2) cancellations. Boolean multilinear ANF is unique via Möbius inversion. Any **single GF(2) polynomial equation** g=0 having exactly the same Boolean zero set must have g=f_k on Boolean assignments, because GF(2) has only one nonzero value; after Boolean multilinear reduction its ANF is the displayed one. Fixed-degree r<k cannot represent that same zero set in one polynomial equation.

**Crucial escape that defeats the overly strong transfer proposal:**

$$
f_k=0\ \Longleftrightarrow\ \bigvee_{i=1}^k(x_i+y_i=0),\qquad
f_k=1\ \Longleftrightarrow\ \bigwedge_{i=1}^k(x_i+y_i=1).
$$

Thus each predicate has **O(k) affine atoms** in the indicated representations. No lower bound for affine-disjunction proof systems or mixed R_mix341 follows from the exponential ANF. A compact semantic representation is not by itself an original-source-authenticated legal proof. No B3 implication is established.

## Established 3-CNF hardness-family, encoding, shortcut ledger

1. **Cubic odd expander Tseitin**: for h cubic vertices and 3h/2 edge variables, four proper signed width-three clauses at each vertex forbid precisely the wrong parity triples; 4h clauses, Theta(h log(h+2)) indexed bits; odd total charge is UNSAT. Known 2^{Omega(h)} ordinary unrestricted shared-DAG Resolution size for suitable expanders (Urquhart 1987; Ben-Sasson/Wigderson 2001), **not** all-algorithm hardness. Existing declared mixed AND3/GF(2) shortcut is **4h−1 paid nodes** (LSPV-2/341), so Resolution hardness fails to transfer to mixed R.
2. **Random F(n,3,8n)**: n variables, 8n independent proper signed three-clauses sampled uniformly with replacement from 8 binom(n,3), indexed bits Theta(n log n). Pang, arXiv:2610.00837v2 (2026-10-24), Theorem 7.2(a): asymptotically almost surely exp(Omega_{p,r}(n)) DAG size in Res(PC_r/F_p), **fixed** prime p and degree r, and a preprint not independently refereed here. Not hardness against dynamic paid extension variables; sampling a finite member does not certify its proof-size hardness.
3. **Bit PHP**, Braun arXiv:2609.23015: n=2^ell holes, n+1 pigeons, (n+1)ell Boolean variables, n binom(n+1,2) original clauses width 2ell, published >exp(n/(32768 ell^2)) DAG Res(XOR_2) length for ell≥32 in its stated system. Cook's polynomial Extended Resolution shortcut is a mandatory control. Exact lower-bound-preserving strict-three conversion is **not established** by equisatisfiability.

The present 2k-input circuit is a focused **normalization falsifier**, not an invented hard SAT family. The established families remain the actual transfer targets.

## Reproduction and full resource qualifications

Python symbolic producer generated k=1,...,12, exact ANF support through 4096 monomials, verified **21,844** original-variable evaluations up through k=7, checked **24** independent individual monomial-deletion witnesses and rejected two forged gate records. k=12 has q=23 paid definitions, 4096 ANF monomials and 49,152 explicit variable occurrences. A separately implemented Node verifier computed the truth table and independent Boolean Möbius ANF coefficients for k≤8, checking **87,380** valuations and passing **91,509** assertions. Full raw producer JSON is preserved in the downloadable reproducer; SHA256 **a421ad3ae123e584aaccd1eb7cbbd1e43c677bcabf21cc8431300eafdfe6828e**. The repository compact verifier and raw summary have a smaller publication footprint than the complete local archive. No historical R_mix341 accepted-byte checker executed.

Observed Python producer peak RSS **103,460 KiB**; independent Node RSS and all-phase simultaneous machine peak were not measured. A physically executable compiler must charge gate parsing, source reads and authenticating IDs, source/index/head reads, construction, failed choices, explicit ANF writes, references, retention/recomputation, checker and output. The explicit ANF alone forces exponential output bits, but the alternate compact affine representation has polynomial bits. Logical paid work, ideal span and realizable machine time/space are different accounting objects. This is not an all-input FLMV contraction; Route A's full-space envelope s'≤max(rho,eta,lambda,lambda*s) remains applicable.

## Corpus and publication safeguards

Reviewed five-role handoff pinned 4e29ed7646f484707767acb6e63ec5f38afd98a8, issue #3 (1,066 comments at initial read), AGENTS.md, CODEX.md, research SKILL, native /341, LSPV-1/448, LSPV-3/429 and /447, LSPV-5/REFEREE385, actual GROKPROOF/2026-11-06_1220_PROGRESS.md and Claude ONETAPE-0001.tex. Required external files reviewed: konard/p-vs-np/scripts/proof_status.json SHA 93b77ed3; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md SHA 18d693ea; meelgroup/frat-xor/format.md SHA 986a21aa. github.com/openai/math code search did not produce the needed native bridge. Indexed web primary-paper search was used; Google-branded interface unavailable. The previous SHIELD1 expansion result is acknowledged, not claimed original.

Root main.tex remains **unmodified** because complete body could not be safely retrieved for an ownership-preserving edit. No task creation/disable/rescheduling or historical rule/weight changes.

**Next OPEN obligations:** authenticate the exact historical native DEF/LOCAL evidence grammar; find a superpolynomial lower-bound invariant valid under every mixed legal RES/AND3/XOR/LOCAL/DEF shortcut; prove a **noncircular same-R B3** SAT∈P ⇒ Wbar_R(N)=N^{O(1)}. B1, B2, B3, full mixed lower bound and P versus NP are OPEN.
