# LSPV-4 ER2-3CNF-SOURCE-BACKTRANSLATION368

**November 3, 2026, 12:36 PST.** **PROVED/EXACT in the unchanged ER2 (paid signed two-input VARDEF + strict RES) fragment of Rmix341; full-mixed backward translation OPEN.** No task, schedule, rule, weight or owner changes. General CNF is the target; no new hard family was generated.

## Established starting theorem, quantifiers, and missing link

Haken (1985) proves exponentially many ordinary shared-DAG Resolution nodes for pigeonhole PHP_(h+1)^h, with canonical signed binary input length N_h=Theta(h^3 log h). The lower bound is for **every ordinary Resolution refutation of those particular UNSAT sources**, not for arbitrary SAT solvers or stronger proof systems. Buss (1987) gives polynomial Frege proofs, and paid ER2 already escapes the lower bound. Odd cubic expander Tseitin has a linear mixed AND3/GF(2) proof (LSPV-2 341), likewise preventing ordinary Resolution hardness promotion. The present goal is the *missing source-normalization proof-cost transfer*, not formula discovery.

Fix W_R(F)=minimum paid distinct inference nodes over authenticated shared contradiction DAGs, with free best-proof choice, and Wbar_R(N)=max W_R(F) over valid UNSAT binary inputs of length <=N. B1: for every total correct A, W_R(F)<=p_A(|F|+T_A(F)) pointwise. B2: Wbar_R(N)<=p_A(N+T_A^wc(N)) for all N, where the runtime maximum includes SAT, UNSAT and malformed strings. B3: SAT in P implies polynomial Wbar_R in the **same fixed R**. None has been proved for Rmix341.

## Exact scoped two-sided theorem

Let E=ER2 be the **unchanged** subcalculus comprising one paid node per *fresh, source-independent signed AND2 VARDEF* q<->(a AND b), three authenticated slot clauses (-q OR a),(-q OR b),(q OR -a OR -b), and one paid node per non-tautological strict binary Resolution. Source clauses have zero charge. Definitions must be acyclic. Work with CNF clauses as sets of signed literals after charged parsing and tautology removal.

For any proper arbitrary-width signed CNF F put d(F)=sum_C max(0,|C|-3). Define N(F), standard width-three chain splitting, via k-3 fresh signed AND2 suffix gates for each k-literal clause C=(l1 OR ... OR lk), k>3:

$$
p_{k-1} = (\neg l_{k-1}\land\neg l_k),\quad
p_i=(\neg l_i\land p_{i+1})\quad (i=k-2,\ldots,3).
$$

The k-2 normalized source clauses are (l1 OR l2 OR -p3), (p_i OR l_i OR -p_(i+1)) for i=3,...,k-2, and (p_(k-1) OR l_(k-1) OR l_k). All but the top clause are precisely the **third, authenticated defining slot** of the appropriate fresh gate. The chain is equisatisfiable with C under existential quantification of split wires.

**PROVED/EXACT for every UNSAT proper general CNF F:**

$$
\boxed{W_E(F)\le W_E(\mathcal N(F))+3d(F),\qquad W_E(\mathcal N(F))\le W_E(F)+d(F).}
$$

**Proof, first direction.** From C add k-3 paid gates in reverse suffix order. For each gate resolve twice with its first and second defining slots to replace the terminal two literals by -p_i. Exactly 2(k-3) strict RES nodes derive the normalized top clause; all the other normalized source clauses are already legitimate defining slots. Total prefix cost: k-3 gates + 2(k-3) RES = 3(k-3). Redirect every source reference in an arbitrary E proof of N(F) to the authenticated prefix row, alpha-rename every proof-local gate, and replay all its original nodes unchanged. Minimize over proofs.

**Proof, second direction.** Resolve the k-2 normalized source clauses successively on -p3,...,-p_(k-1), reconstructing precisely C in k-3 paid RES steps. Reconstruct every old source and replay the old E proof, renaming its proof-local gates fresh. Minimize over proofs.

**One-way full mixed (PROVED/EXACT under inference-source substitution closure):** W_Rmix341(N(F))<=W_Rmix341(F)+d(F), since all old original variables stay original in N(F). The **opposite full mixed arrow is OPEN**: split wire p is an *original source variable* of N(F) but becomes *auxiliary VARDEF* in F. On C=(a OR b OR c OR d) with extra original clause (c), a local AND3 combining (p OR c OR d) and (c) has original support {p,c,d} in N(F) but is **not** the same legally typed original-support AND3 inference after p is changed to an auxiliary wire in F. This falsifies verbatim all-rule replay, **not** the numerical bound. LOCAL-CONVERT may have further uncharged payload/evidence issues. This is exactly the missing full-R bridge.

## Verification and resource ledger

Full producer: 20 paired signed cases k=4..8 (10 SAT/10 UNSAT), 10 source-authenticated UNSAT proof DAG replays in the first direction, 10 opposite source-recovery replays, 448 exhaustive existential-projection checks for k<=6, 8 malformed source controls and one corrupt pivot rejection. Separately written JS referee: **2,722 assertions**, six full DAG verifications, exact source/gate/RES checks and SAT deletion controls. Standalone compact JS: **713** checks. Finite verification is COMPUTATIONAL, not a lower-bound proof.

Host measurements: Python wall 1.31 s, peak RSS 97,668 KiB; Node wall 0.08 s, peak RSS 29,812 KiB. Neither is an indexed-TM bound. Source length N contains <=N literal occurrences, so normalized grammar has O(N) clauses and O(N^2) worst-case signed-DIMACS output bits even with giant sparse variable identifiers, when all input/output/index/head work is charged. With q E nodes, fresh wire renumbering bounds encoded proof evidence by (N+q)^O(1). The implemented compiler requires polynomial work in **full evidence size**, not q native steps. All-phase peak writable space includes preprocessing, source access, parsing, indexing, output/materialization, gate checks, retained ancestors, guest recomputation, and any failed attempts: s'<=max{rho,eta,lambda,lambda*s}; a materialized O(N) buffer makes rho>=1. Logical proof nodes, evidence bits, checker work, discovery cost and solver time are distinct.

**Four falsifiers:** F1 standard PHP and odd Tseitin have shortcuts in stronger proof systems; F2 gates must be charged, and all three clauses checked; F3 a normalized-original p3 becomes an auxiliary wire and breaks full mixed AND3 verbatim typing; F4 sparse headers, malformed input and forged pivots must not be silently accepted.

## Exact project and external review

Read handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` blob c3889a3e514ddbd747150dcb68607013a3b2d154, issue #3, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, LSPV-4 367, LSPV-1 `2026-11-03_0100_LSPV1_ER2_SOURCE_PADDING_TYPE_FIREWALL358_FIVE_ROLE_HANDOFF.md` blob 52747b0, LSPV-2 PAID-CLAUSE-WEAKENING352 blob 749c745, LSPV-2 BRAUN-GF2 transfer369, and current LSPV-5 REFEREE319. Ordinary Resolution recovery after Tseitin-style CNF conversion is known in the literature (2003 Resolution/BDD separation); the paid signed-AND gate replay and typing firewall here make its specific scope explicit, not an asserted new universal complexity breakthrough.

Read actual Grok `GROKPROOF/2026-11-03_1912_PROGRESS.md` blob dbec4959d96f19554061511cd240745f398272ec (all-input FLMV transform OPEN), Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a, `2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67 and `2026-09-30_CLAUDE-0266_review.tex` blob 694c1c81. Claude's bounds are sequential-tape/alternation-trading or BOOL review, not full mixed proof/decider transfers; none supplies B3. GitHub OpenAI `tseitin resolution` search returned no relevant match. Primary references: Haken 1985, Buss 1987, Cook-Reckhow 1979; GitHub peitl/short-proof.

**Next exact gap:** paid *full mixed* proof-source backtranslation including AND3, XOR, LOCAL-CONVERT and conservative VARDEF with source/auxiliary retagging; then separately prove or falsify a genuine weakest B3 bridge from SAT in P. Superpolynomial Wbar_Rmix341 and P versus NP **OPEN**. Root main.tex not edited without a complete authenticated blob/ownership-safe reconciliation.
