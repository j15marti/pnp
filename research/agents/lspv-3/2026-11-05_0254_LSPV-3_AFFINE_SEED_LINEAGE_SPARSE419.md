# LSPV-3/419: Affine seed-lineage certificate and sparse original-coordinate bounds

**2026-11-05 02:54 PST | PNP Hypergraph & Proof Certificates (LSPV-3).**
**Status: PROVED/EXACT for an explicitly typed affine sub-DAG; independent specialist review pending. COMPUTATIONAL finite controls. Full native R_mix341 exported-wire/DEF-facet/LOCAL bytes, all-rule compiler, B1/B2/B3, superpolynomial mixed W and P versus NP: OPEN.**

## IDEA (registered before searching) and falsifiers

Hypothesis: every **typed** GF(2) row obtained using binary XOR from paid constant-support, original-coordinate AND3 row seeds has a compact, source-authenticated *seed-lineage mask*, even when the original DIMACS header names exponentially many coordinates, and even with a shared/reconvergent XOR DAG. This may produce a narrow polynomial-bit result without requiring a general LOCAL port compiler.

Falsifiers: (1) an authenticated non-XOR affine seed referring to a hidden auxiliary output or arbitrary-width LOCAL private export; (2) a derived XOR row introducing an identifier absent from every seed; (3) a row whose evidence requires a dense array of length equal to the declared DIMACS variable bound; (4) a typed proof where duplicate XOR paths invalidate the seed-lineage mask. Cases (1) and the exact DEF/LOCAL selector bytes are NOT settled by the original prose, so no unconditional claim about every native row is made.

## SEARCH, original grammar, duplication audit

Read first `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` (commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, blob `033b54b8`); current issue #3 through LSPV-5 REFEREE359 and LSPV-4/409; AGENTS.md, CODEX.md, `.codex/skills/pnp-research/SKILL.md`. Read original `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`) and `research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md` (blob `bbcdad9a`). Reviewed recent /418 polarity gauge, LSPV-2/413 nonlinear DEF affine failure, REFEREE358 GF2-erasure impossibility, REFEREE359 semantic canonical balance, and LSPV-4/409 sparse XOR schedule. No duplication claim: those already prove generic restricted canonical balance and schedule sensitivity; this report isolates **exact seed-lineage coefficient vectors and a sharp 3a support invariant**.

Actual Grok: `GROKPROOF/2026-11-05_1218_PROGRESS.md` (blob `d3183283`), white-box FLMV residual OPEN. Actual Claude: `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (blob `1f9fc727`) and `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (blob `9a5b05d6`); their sequential-access/portfolio restrictions do not provide a same-R B3 compiler. Authenticated github.com/openai queries `ExecCNFNodeSearchCosts`, `CookLevin`, `LRAT proof checker`; read FULL `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` (blob `1ced21f4`), which proves charged same-execution bounds but supplies no native R_mix341 proof translation.

Actual web queries: `Haken 1985 intractability of resolution pigeonhole principle exponential lower bound original paper`; `Gocht Nordstrom certifying parity reasoning pseudo boolean 2022 xor clauses certificates paper`; `Raz Tzameret resolution over linear equations 2008 proof system original paper`; `propositional proof systems p optimal proof system P NP coNP Cook Reckhow polynomial bounded`; `Cook Reckhow relative efficiency of propositional proof systems theorem NP coNP 1979 original`. Read publisher/institutional pages: Haken 1985, https://doi.org/10.1016/0304-3975(85)90144-6 ; Cook/Reckhow 1979 https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/abs/relative-efficiency-of-propositional-proof-systems/218048250981F835B4B2A4080205A0BA ; Raz/Tzameret 2008 https://weizmann.elsevierpure.com/en/publications/resolution-over-linear-equations-and-multilinear-proofs/ ; Gocht/Nordström AAAI 2021 https://ojs.aaai.org/index.php/AAAI/article/view/16494 . Direct Google-branded search unavailable; indexed general web used instead. Nothing there authenticates the missing LOCAL/DEF selector bytes or B3.

Haken's established result concerns explicit unary PHP source CNFs and **every ordinary shared-DAG Resolution** proof, with exponentially many lines in the pigeonhole parameter; it is not a lower bound for GF(2)/ER or arbitrary SAT machines. Cook's ER PHP shortcuts and native odd cubic Tseitin's 4h-1 optimum remain controls.

## ITERATE: corrected scope and exact theorem

The literature/peer check forced a narrower scope. LSPV-5 REFEREE359 already isolates the **literal paid-node closure** and notes that original /341 does not authorize free private LOCAL wire antecedents; /341 does not provide an exact parser for individual DEF facets, GF2 source selectors or LOCAL internal gates. Therefore the present theorem concerns the following actual **unambiguous typed sub-DAG**: a bank of a paid AND3 annotations, each a GF(2) row using at most three *original* DIMACS coordinates authenticated by an eight-row local truth table; all further affine rows are binary XOR outputs of previously authenticated rows. No hidden DEF-to-GF2 export is silently included. All original source clauses are retained and named, node weights remain one and proof fan-in at most two.

**Theorem (seed-lineage).** Let `a` authenticated original-coordinate affine seeds `r_1,...,r_a` each have support size at most three. For every node `v` in any acyclic shared binary-XOR sub-DAG above these seeds there is a deterministically computed lineage vector `lambda_v in GF(2)^a`, with unit vectors at seeds and `lambda_v=lambda_u XOR lambda_w` at XOR children, such that

$$
r_v = \bigoplus_{i=1}^{a} (\lambda_v)_i r_i,
\qquad
|\operatorname{supp}(r_v)|\le 3a.
$$

The mask is **unique relative to the displayed DAG**, not necessarily the unique algebraic representation of the same row when the seed bank is dependent. Every identifier belongs to the union of authenticated seed identifiers, independent of reconvergence, cancellation and intermediate row lengths.

**Proof.** Induct on the topological order. The statement is tautological for a seed. A binary XOR node computes the symmetric difference of parent coefficient sets and the XOR of their RHS bits. Substituting the inductive identities gives the claimed lineage and coordinate union. Duplicate appearances cancel modulo two, which handles reconvergence. No new identifier can arise because symmetric difference is contained in union. The induction uses only displayed, already-authenticated seeds and legal binary XOR. QED.

**Corollary (sparse bits).** With `q >= a` charged nodes and original ASCII DIMACS input length `N` bits, each original identifier requires `O(N)` bits even when declared coordinate bound `K=10^t` is exponentially large in N. An explicit normalized sparse row takes `O(a(N+log(q+2)))` bits, all at most q affine rows take `O(q*a*(N+log(q+2)))=O(q^2(N+log(q+2)))` bits, and all lineage vectors use `O(a*q)` bits. This excludes the **unnecessary** dense K-coordinate array but NOT arbitrary other supplied E-bit LOCAL payloads. Given explicit seed rows, all masks/rows can be recomputed and checked in polynomial bit time/space in N+E+q; evidence acquisition is at least Omega(E). Intermediate outputs, scans, failed checks, output, and peak memory remain charged independently of node W.

**Terminal-XOR compression.** If a final contradiction `0=1` is produced by binary XOR from the authenticated bank, its lineage mask is nonzero (the empty XOR is `0=0`). Let `s` be its Hamming weight. A fresh left-to-right chain of `s-1 <= a-1` legal paid XOR nodes, reusing the same authenticated seed nodes, reproduces the contradiction. This is a single-terminal suffix replacement, **not** a consumer-preserving rewrite for all intermediate named rows. If seeds have an internal XOR ancestry, that ancestry must be retained and charged too. The emitted explicit chain has polynomial bits; finding and validating it from an E-bit supplied proof costs additional time and memory. Existence of a short minimum and acquisition cost are different.

**Grammar firewall.** Original /341 calls AND3 an eight-bit original-support factor with optional *exact* affine annotation, but does not serialize GF(2) output coefficients or state whether an XOR-defining DEF relation is independently exposed as a row. If such extra rows are authorized by a later concrete selector, add them as separately authenticated seeds and reprove the width bound for that seed grammar. An invented DEF/LOCAL port export cannot be used to claim this theorem for all R_mix341 derivations. No original-source retraction into Resolution alone is attempted, consistent with REFEREE358.

## COMPUTATIONAL evidence and hostile controls

Python (seed 419): 55 three-original-coordinate seed rows, 550 reconvergent XOR operations, **605 exactly recomputed lineage vectors**, exponential declared DIMACS coordinate bound `K=10^80`, 20,353 assertions. A separate 120-group **source-authenticated SAT** CNF with 480 original parity clauses has 360 paid AND3 and 119 XOR nodes producing a valid row of **360** original variables; literal source is 947,328 bits and sparse final row is 233,456 bits. All 480 source clauses are satisfied by an explicit witness. This tests that the bound is **3a**, not an invalid universal three-coordinate bound. Independently written JavaScript/BigInt checker: 2,175 assertions, same 120 groups, correct 360-coordinate row, and eight rejected corrupted affine RHS tests. Negative checks reject auxiliary/undeclared coordinates, duplicate row entries, nonaffine majority masks and malformed gates. This is only a constructive upper trace, not an optimizer-certified minimum or a hard family.

Exact working copies: `/mnt/data/lspv3_419_native_affine_confinement.py`, `/mnt/data/lspv3_419_independent_sparse_affine.js`, and `/mnt/data/lspv3_419_native_affine_confinement_raw.json`. GitHub role-owned compact verifier and summary are published separately. Full program-resource interpretation not claimed: the high-ID case does not allocate dense K bits. Host runtime RSS was not measured.

## B3 and the next exact missing obligation

For the SAME fixed calculus, the primary bridge is

$$
\mathrm{SAT}\in\mathrm{P}\Longrightarrow
\exists C,k\ \forall N:\
\overline W_{R_{\mathrm{mix341}}}(N)\le C(N+1)^k.
$$

Neither row-lineage compression, polynomial canonical **bytes conditional on q**, nor SAT decider answer bits proves the implication. The missing arrow is a noncircular same-calculus polynomial refutation existence theorem under SAT in P, with native proof-consumer legality. B1/B2/B3 remain OPEN; no new computational-hardness invariant was proved.

**Next task:** Obtain exact authoritative row/DEF-facet/LOCAL-export selector semantics, then try to extend seed-lineage propagation through **every legal native affine consumer**, giving a typed legal counterexample immediately if some rule introduces unchecked hidden row coordinates. Defer root `main.tex` mutation if its current entire content cannot be retrieved safely; preserve all five task settings and historical reports.
