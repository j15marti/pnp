# LSPV-1/406: Feasible-Antichecker Conditional B3 Through Native RES+DEF

**November 4, 2026, 19:05 PST.** LSPV-1. Original fixed R_mix341 from research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11) unchanged: free original CNF clauses, unit-cost binary RES, bounded-support AND3/LOCAL-CONVERT, binary GF(2) row XOR, and one paid conservative fresh two-input DEF. **CONDITIONAL derived corollary; independent mathematical review pending.** B1/B2/B3, superpolynomial native Wbar, and P vs NP OPEN.

## IDEA before search and falsifiers
Candidate route: formal, uniform *antichecker generation* might suffice for B3 without a formal soundness proof for a hypothetical SAT decider. Predict a published theorem may yield polynomial Extended Frege bounds, which source-preserving EF→ER→paid native RES+DEF can carry to the **unchanged** system, independent of disputed LOCAL-CONVERT exports.
F1: theorem only gives SOME proof system. F2: generator hypothesis presupposes rejecting-decider reflection. F3: ER-native step secretly needs LOCAL export or changed sources. F4: a bounded-size-circuit antichecker is mistakenly replaced by a subset distinguishing all possible Boolean functions.

## SEARCH: exact source record
Read the complete shared 2026-11-02_1204 five-role directive (blob c3889a3e), current coordination issue #3 through REFEREE351, AGENTS.md 19656af1, CODEX.md 754999f5, .codex/skills/pnp-research/SKILL.md b8df83a7, native /341 c87acd11 and peers LSPV-1/405, LSPV-2/405, LSPV-3/406-407, LSPV-4/400, REFEREE350-351. Existing LSPV-1/357 one-sided provability firewall, /360 oracle firewall, /364 proof search, /405 checkpoint sampling, REFEREE318/344/350/351 cover adjacent arguments and are credited. REF350 proves source-exact ER mutual simulation for an **explicit root-only completion**, but original native LOCAL-CONVERT leaves payload/export/charge grammar under-specified; no completion is asserted here.

Primary: J. Pich and R. Santhanam, *Towards P != NP from Extended Frege Lower Bounds*, ECCC TR23-199 (2023), Theorem 10 and its proof (PDF pp. 25–26), https://eccc.weizmann.ac.il/report/2023/199/ and arXiv 2312.08163. The exact published theorem requires a polynomial-time f and a fixed S^1_2 proof of a universal circuit-or-antichecker correctness assertion for fixed k≥3. Under it, EF not polynomially bounded implies SAT has no size-n^k circuits infinitely often. Cook–Reckhow (1979), Cook (1976), Haken (1985) and EF/ER proof translations checked as model background.
Actual web search strings: "P equals NP implies Extended Frege polynomial bounded open question proof complexity"; "if P=NP then Frege proofs polynomial size all tautologies bounded arithmetic"; "Towards P!=NP from Extended Frege lower bounds feasible anticheckers theorem 10"; "S2^1 bounded arithmetic Pich Santhanam antichecker". Direct Google-branded interface unavailable; general web research performed, no claim of direct Google session.
Authenticated github.com/openai query "ExecCNFNodeSearchCosts": full-read openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean blob 1ced21f4. This is real SAT execution-cost accounting, NOT an antichecker correctness proof or B3 compiler.
Grok actually read: GROKPROOF/2026-11-04_2315_PROGRESS.md blob f5b8ef62, universal all-input FLMV extraction OPEN. Claude actually read: research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex blob 1f9fc727, and 2026-10-28_1521_CLAUDE_ONETAPE-0001.tex blob 9a5b05d6. Their restricted portfolio/sequential models do not establish B3.

## ITERATE: exact derived conditional statement
For each fixed integer k≥3, write AC_k for the **entire** unproved Pich–Santhanam Theorem 10 hypothesis: a single polynomial-time generator f_k with a fixed S^1_2 derivation of its universally quantified output guarantee. At each unary 1^n, either its output is a small search circuit B producing witnesses for every SAT instance of length n, or a small authenticated antichecker with consistent SAT witnesses and a counterexample for **every** Boolean circuit of size ≤n^k. Neither f_k nor its formal correctness proof has been constructed. AC_k is not implied by bare SAT in P here.

**Theorem 406A (CONDITIONAL):** For every fixed k≥3,
$$
AC_k \land \mathrm{SAT}\in\mathrm{SIZE}(n^k)
\quad\Longrightarrow\quad
\exists C,d>0\;\forall N:\quad \overline W_{R_{\mathrm{mix341}}}(N)\le C(N+1)^d.
$$
The nonuniform circuit family on the left decides every binary string at each length, including malformed signed-CNF encodings; for sufficiently large n its size is ≤n^k. N is the total signed encoded input bit length, not variable count.

**Proof.** Pich–Santhanam Theorem 10 says under AC_k, if EF is not polynomially bounded then SAT has no n^k-size circuits for infinitely many n. Contrapose against the assumed circuits for all sufficiently large n. Therefore EF is polynomially bounded. Every original UNSAT F of encoded size N gives a tautology expressing unsatisfiability of size poly(N), and the EF assumption gives a single polynomial upper bound on EF proof bits uniformly across F. Standard EF→fan-in-two Extended Resolution simulates a supplied EF proof with polynomial encoded output size and uniform construction. The already established **exact-source** ER→R_mix341 translation uses solely the unambiguous paid two-input conservative DEF and strict binary RES rules. Every derived node contributes output bits, so native distinct paid node count q≤poly(N). Maximize over valid UNSAT F of length ≤N. This proves proof **existence**, not computationally free discovery. Crucially, no native LOCAL-CONVERT, exported wire, source-retraction oracle, or new inference rule is used. The logical implication depends on the published theorem and already-known simulation; its premise AC_k is OPEN.

**Theorem 406B (CONDITIONAL B3 criterion):**
$$
\left(\forall k\ge3\ AC_k\right)\Longrightarrow
\left(\mathrm{SAT}\in P\;\Rightarrow\; \overline W_{R_{\mathrm{mix341}}}(N)=N^{O(1)}\right).
$$
**Proof.** One fixed hypothetical P-time uniform total SAT decider with some finite exponent t can be compiled into nonuniform circuits of size O(n^e) for a fixed e. Choose **one fixed** k≥max(3,e+1), apply AC_k and Theorem 406A. Constants depend on that one algorithm and fixed k, not on N or F. The universal AC_k premise is not proved. Thus B3 remains OPEN, and this is a narrower conditional **alternative route**, not a solution.

**Conditional hard-family consequence:** If full-mixed Wbar is proved superpolynomial and AC_k independently holds, then SAT ∉SIZE(n^k) infinitely often. If AC_k holds for each k and full-mixed superpolynomial Wbar is proved, then SAT∉P/poly and P≠NP. Neither ingredient is established.

## Exact certified hard anchor and escape controls
Haken (1985) establishes that for explicit unary PHP(h+1,h), with h(h+1) variables, h+1+h·binom(h+1,2) clauses, and signed binary-index N_h=Theta(h^3 log(h+2)), there are c>0,h0 such that for every h≥h0 every ordinary unrestricted shared-DAG Resolution refutation has at least 2^(ch) lines. This is **only ordinary Resolution**, not ER/EF, R_mix341, Res(XOR), or arbitrary SAT machines. Cook's polynomial Extended Resolution proofs of PHP and odd Tseitin's short mixed GF(2) proofs are mandatory opposite controls.

## Computational checks and falsifiers
Eight explicit signed two-variable CNFs with truth labels [1,1,0,1,1,1,0,1], plus malformed sources. In the *unrestricted* class of all 2^8 classifiers of eight inputs, every 255 proper subdomains fail to distinguish the true SAT truth table from a single-bit-flip classifier on a missing input. This is an exact elementary finite quantifier lemma and is **NOT** a counterexample to Theorem 10, which limits circuit sizes and includes an alternative search-circuit branch.
The full standard-library Python producer exhaustively checked all 256 classifiers and all 256 subdomains, with 301 assertions and nine malformed rejections; independent Node JS verified 347 assertions, both labels and all signed mutations. Code experiments/arc/lspv1_406_antichecker_firewall.py and experiments/arc/lspv1_406_independent_verify.js. Raw results/raw/arc/2026-11-04_1905_LSPV1_FEASIBLE_ANTICHECKER_B3_406.json. Independent check pending remote GitHub readback; raw SHA-256 local 509693798bb6a5dfb26c63a2932375eb52b0c837cf63e6c92914750f440db62f. Finite checks DO NOT test B3 or theorem 10.

## Physical work, failure classification, next obligation
Native Wbar counts unit paid shared-DAG inference nodes only. Given an explicit EF proof, the translator pays separately for source parsing, source/index/header reads, local construction, gate indices, pivot checks, every encoded intermediate/certificate bit, checker work, output and all-phase peak space. Existence of short proofs is distinct from optimizer discovery and actual machine SAT runtime. No exponential backtranslation is assumed. A later FLMV child contraction must respect s'≤max{rho,eta,lambda,lambda*s}, with rho charging all local phases. AC_k is formal self-provability of a generator, a substantial additional hypothesis, not a free inference from circuit upper bounds. F1-F3 avoided by conditional theorem and native RES+DEF upper simulator; F4 confirmed by finite class countercontrol.
**Next decisive step:** propose one explicit uniform generator f_k, and prove or refute its full S^1_2 correctness under every length/circuit and signed/malformed input, without assuming B3. Independent specialists must check whether AC_k is genuinely weaker than the desired transfer; do not promote it. In parallel LSPV-2/3/4/5 must complete native LOCAL-CONVERT export grammar and adversarial resource audit. No task, schedule, weight, grammar, or owner changed. B1/B2/B3, full-mixed superpolynomial Wbar and P vs NP OPEN.

### References
[1] Pich and Santhanam, Towards P != NP from Extended Frege Lower Bounds, ECCC TR23-199 (2023), Theorem 10. https://eccc.weizmann.ac.il/report/2023/199/
[2] Cook and Reckhow, Relative Efficiency of Propositional Proof Systems, JSL 44(1), 1979, 36–50.
[3] Cook, A Short Proof of the Pigeon Hole Principle Using Extended Resolution, SIGACT News 8(4), 1976.
[4] Haken, The Intractability of Resolution, TCS 39, 1985, 297–308.
[5] Krajicek, A Note on SAT Algorithms and Proof Complexity, IPL 2012.
