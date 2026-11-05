# LSPV-2/410: two-stage behavioral-facet compiler, 88t+r

**2026-11-04, 23:12 PST | IDEA -> SEARCH -> ITERATE.** PNP SAT-Circuit Reduction Builder. **PROVED/EXACT in an expressly assumed readable-DEF-facet, pure-Resolution-consumer fragment; COMPUTATIONAL independent verification.** Native R_mix341 grammar/normalization, B1/B2/B3, superpolynomial mixed minimum and P vs NP remain OPEN. Specialist mathematical review pending.

## IDEA and falsifiers before SEARCH

LSPV-2/409 uses a direct target-implicate translation costing at most 16384t+r paid nodes for t conservative two-input DEF gates and r downstream strict Resolution steps, with all old outputs depending on the same three original source variables. **Falsifiable proposal:** first derive eight canonical *behavior clauses* per old public output, then reconstruct every old defining facet using the behavior clauses, reducing the upper bound to 88t+r. Falsifiers: (F1) a 3-input function needs >4 paid binary gates, (F2) the new definitions do not entail a claimed behavior clause, (F3) actual derived behavior subclauses do not entail old facets, (F4) the unchanged native rule lacks a free facet-selector or permits consumers not covered by the compiler. F1 was addressed by the known Seidler catalog and LSPV-3/411. F2/F3 passed symbolic analysis and independent constructive tests. **F4 remains unresolved and prevents a full-native claim.**

## SEARCH: original sources and limitations

Read governing five-role directive research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (blob c3889a3e); current issue #3; AGENTS.md; CODEX.md; .codex/skills/pnp-research/SKILL.md; the original R_mix341 rules in research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11); LSPV-2/407 and /409, LSPV-1/409, LSPV-3/411, LSPV-4/403 and REFEREE354. The original rule says paid DEF has all its defining relations *attributed to the same node* and later uses refer to that node, but does not explicitly settle individual CNF-facet selectors, direct GF(2) equation exports, or LOCAL-CONVERT circuit wire exports. No new rule is declared.

Read actual GROKPROOF/2026-11-05_0515_PROGRESS.md (blob f348f7bb), research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727) and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (blob 9a5b05d6). None proves native exports or B3. The previously identified grammar addendum was not independently fetched at a verified path this run.

Exact general-web searches included: "Haken 1985 Intractability of Resolution pigeonhole original paper full pdf"; "Cook 1976 short proof pigeon hole principle extended resolution pdf"; "Cook Reckhow Relative Efficiency of Propositional Proof Systems 1979 pdf"; "Gocht Nordstrom certifying parity reasoning efficiently pseudo boolean proofs 2021"; "Seidler Minimal Circuits for Boolean Functions of Few Variables 2022 pdf"; "Raz Tzameret Resolution over Linear Equations multilinear proofs pdf"; "OpenAI github SAT formal verification ExecCNFNodeSearchCosts lean proof model". Read publisher/author pages for Cook-Reckhow (JSL 1979, https://doi.org/10.2307/2273702), Seidler (https://sites.math.rutgers.edu/~bas312/Research/slp/slp.html), Raz-Tzameret (APAL 2008, https://doi.org/10.1016/j.apal.2008.04.001), Gocht-Nordstrom (AAAI 2021, https://doi.org/10.1609/aaai.v35i5.16494), and Cook ER (SIGACT News 1976, https://dblp.org/rec/journals/sigact/Cook76). Full AAAI publisher-page open was blocked; bibliographic text available. Direct Google-branded search UI unavailable, so no claim of Google results.

Authenticated github.com/openai searches "ExecCNFNodeSearchCosts", "CookLevin", "LRAT proof" found and read full openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (blob 1ced21f4). Cook-Levin code exists in openai/math; LRAT hits were irrelevant substrings. These code files are not same-R machine-to-proof bridge theorems.

## ITERATE: all-size restricted theorem

Fix any CNF source F. Assume a source-explicit DAG of t paid, acyclic, conservative, arbitrary two-input Boolean DEF gates, with every old public output depending on one common S of at most 3 **original** variables. Downstream uses are original source clauses, **individually selectable defining CNF facets** and r **strict binary Resolution** inferences. Individual selecting of each up-to-four facet of one paid DEF is an **additional, unratified grammar assumption**. No GF(2), AND3 or LOCAL-CIRCUIT private-wire consumers are included. Fresh gate names and output names are correctly typed.

**Theorem 410.1 (restricted, no size/search cutoff):**

$$
\boxed{q_{\mathrm{new}}\le 88t+r.}
$$

**Proof.** First replace *each old gate output name* y, not only final external ports, by a separately synthesized function of S with at most 4 paid two-input gates (Seidler; a paid identity/constant gate retains the old name). Total new DEF gates <=4t. For every assignment s of S, let B(y,s) be the clause falsified precisely when S=s and y differs from its true function f_y(s). Its literals are the blockers of s together with y if f_y(s)=1, otherwise NOT y. At most 8 behavior clauses per old output. The new defining facets for the <=4-gate cone entail B(y,s). Their union involves at most |S|+4 variables, while B(y,s) mentions the |S| originals and y, leaving at most 3 variables outside B(y,s). LSPV-2/403's strict target-implicate lemma derives a **subclause** B'(y,s) of B(y,s) using at most 2^3-1=7 RES nodes. Stage A therefore costs <=56t RES nodes.

For any old gate defining facet C of width c<=3, collect the **actually derived B'(y,s)**, not merely their desired target clauses, for all old named gate wires appearing in C. These clauses mention at most |S|+c variables. As the old public outputs have the correct pointwise functions of S, the behavior clauses imply C; replacing them by stronger derived subclauses preserves entailment. There are at most 3 variables outside C. The same strict-RES implicate lemma derives a subclause C' of C using <=7 RES nodes. There are <=4 facets per old gate, hence <=28t Stage-B RES nodes. Replaying each original downstream RES step from stronger antecedents takes at most one RES inference: if pivot disappears, retain a parent subclause of the target resolvent. Empty final clause remains empty. Total <=4t+56t+28t+r=88t+r. Every produced clause is source-authenticated through explicit new DEF facets. QED.

This improves the previously proved **conditional** 16384t+r coefficient by a factor of >186, without settling the native selector grammar. There is no claim of a global minimum or arbitrary-machine lower bound.

## Experiment, failed attempt, independent audit

Old gate bank: p4=x1 XOR x2; p5=p4 XOR x3; p6=NOT(p4 XOR p5). Replacement: p4=x1 XOR x2; z7=x1 XOR x2; p5=z7 XOR x3; p6=NOT x3 (one paid two-input unary-function gate fed x3 twice). The old and new public vectors coincide for all 8 assignments although internal wiring differs. Original bank: 3 paid DEF gates / 12 facets. Replacement: 4 paid gates / 14 facets. Compiled proof: 24 behavioral targets, **8 paid Stage-A RES, 32 Stage-B RES, 40 total RES, four paid DEF, q=44**. All 36 strict implicate certificates use at most three deficit variables and at most seven RES inferences. Not an optimum claim.

First prototype failed because a target variable absent from its defining cone was not included in the branch universe. It was fixed to use the union of premise and target variables. Second, the prototype improperly fed exact behavior *targets* into Stage B, even when Stage A derived only a **subclause**; the final producer passes only the actual earlier roots. Independent separately implemented JS checks **7,473 assertions**, validates 40 strict parent/pivot/resolvent records and all eight truth-table assignments, SAT/UNSAT controls and rejects five altered records: forged pivot, altered new gate, duplicate literal, forged premise and forged conclusion. Complete JSON certificate SHA-256 4dff0c3104447e7c04a7e3b9b8b563018bda25957422f04afc254596ef209759, 44,242 bytes; deterministic gzip mtime-zero yields 1,933 bytes and 2,580 base64 characters. See owned experiment, independent checker and compressed raw record.

## Physical costs, established hard families, B3

88t+r is logical DAG node cost, **not physical runtime**. A literal compiler must read and parse all N source and E evidence bits; recover and verify supports/definitions, produce and check all gate, clause and proof records; track names and pivots, serialize outputs, manage/recompute/shared DAG nodes and account for peak simultaneous memory. A brute-force buffered implementation is polynomial in N+E+t+r, with a deliberately loose bound O((N+E+t+r+2)^5) bit time and O((N+E+t+r+2)^3) writable peak bits, including input/output staging, and no claim about hardware RSS or FLMV space exponents. A long proof payload cannot be hidden behind short q. Source/statement bits, output and proof-search discovery are separate.

Start from Haken's exponential **ordinary shared-DAG Resolution** lower bound for unary PHP_{h+1}^h, with h(h+1) variables, (h+1)+h*binom(h+1,2) clauses and Θ(h^3 log h) encoded bits. Cook's polynomial Extended Resolution PHP proof (1976), Raz-Tzameret's different Res(lin), and the exact native /341 affine Tseitin optimum 4h-1 prohibit any direct transfer of ordinary Resolution hardness to the combined R or arbitrary SAT algorithms.

The essential open **same preselected calculus** obligation remains

$$
\mathrm{SAT}\in P\Longrightarrow\exists C,k\ \forall N:\quad \overline W_{R_{\mathrm{mix341}}}(N)\le C(N+1)^k.
$$

An existing-proof normalization does not produce a proof from a hypothetical SAT machine. The decider's rejecting trace does not establish universal SAT correctness in the fixed system. Cook-Reckhow gives existence of **some** polynomially bounded system from NP=coNP, not automatically this R. B1/B2/B3, full native polynomial normalization, superpolynomial mixed Wbar and P versus NP remain OPEN.

**Next obligation:** authenticate original byte grammar for DEF-to-facet, DEF-to-GF(2) row, typed AND3 and LOCAL-CONVERT exported/private wires; either extend consumer replay to each permitted kind or give an explicitly **legal native** counterexample. An unratified Splus interpretation cannot substitute for native /341.
