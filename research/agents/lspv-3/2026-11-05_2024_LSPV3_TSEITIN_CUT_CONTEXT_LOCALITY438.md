# LSPV-3/438: Cut-context locality firewall on established cubic Tseitin 3-CNFs

**2026-11-05 20:24 PST | Route B primary | PROVED/RESTRICTED and COMPUTATIONAL.** Fixed historical R_mix341 grammar unchanged; P versus NP OPEN.

## IDEA -> SEARCH -> ITERATE

Hypothesis: although a source-authenticated, high-width cut-parity row can be carried cheaply as an existing GF(2) inference, forcing a three-wire LOCAL port through branch contexts has a precise locality threshold. Falsifiers tested: (F1) hidden additional boundary constraints for a connected induced subgraph; (F2) nontrivial three-wire implicates with four or more free boundary bits; (F3) failure of source-authenticated AND3/XOR construction; (F4) an actual native free split or wide-local conversion rule. F1-F3 rejected by theorem and finite replay; F4 not a legal historical premise.

Read governing Nov 2 five-role handoff, issue #3 through LSPV-1/433 and REFEREE376, original native specification at `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob `c87acd11`), AGENTS.md/CODEX.md/research skill, peer LSPV-2/422 (blob `67386065`), LSPV-1/428 (`89cbfe50`), LSPV-3/425 and /437, actual Grok `GROKPROOF/2026-11-06_0215_PROGRESS.md` and Claude `research/agents/claude/tport/README.md`. Searched both mandatory repositories `konard/p-vs-np` (complexity README `7ee9a11e`, experiments README `4c8752aa`) and `blkph0x/p-vs-np-proof-research` (method index `18d693ea`, residual barrier `46413596`), and FRAT-XOR `format.md` (`986a21aa`), `cake_xlrup/README.md` (`c71de809`), cake_lpr `README.md` (`e94f45e9`), openai/math `README.md` (`cc5b0a03`). Queried primary research on Tseitin/expander Resolution hardness, bounded-depth Frege, and CNF/XOR checking. Google-branded search and container git DNS unavailable; indexed web and authenticated GitHub file reads were available. FRAT-XOR and CakeML code were read, not executed.

**Duplication audit:** LSPV-2/422 already proves the exact affine cut projection, LSPV-1/428 the strict-Resolution canonical opposite-row join lower bound, and LSPV-3/425 a conditional paid gate reifier. None is claimed new. This run isolates the *branch-context / three-wire-locality* consequence and certifies its scoped application at original source level.

## Exact established family and model

Let G=(V,E) be connected simple cubic with h vertices, n=3h/2 edges, and odd total charge chi. Each vertex has the four proper width-3 signed clauses falsified by the four incident-bit triples of wrong parity. Thus `F_G` has exactly 4h original 3-clauses, and binary-index encoded size N=Theta(h log(h+2)). Summing all h equations gives 0=1, so the formula is certified UNSAT. For suitable cubic expander families, Urquhart (JACM 1987) and Ben-Sasson--Wigderson (JACM 2001) establish 2^{Omega(h)} ordinary shared-DAG **Resolution** length; Ben-Sasson (Computational Complexity 2002) separately proves bounded-depth Frege hardness. These theorems do not concern the full mixed calculus or arbitrary SAT algorithms. Existing native semantic AND3/GF(2) certificates from /341 attain W_R(F_G)=4h-1 on bridgeless cubic graphs.

## Exact context-locality theorem

Take nonempty proper S subset V, with induced connected G[S] and cut delta(S) of k>=4 edges. Let F_S consist of precisely the 4|S| original clauses at S, and b=XOR_{v in S} chi_v. Let y denote the public cut bits and w the internal edges. Then

$$
\exists w\,F_S(w,y) \equiv \Pi_b(y):=
\left(\bigoplus_{e\in\delta(S)}y_e=b\right).
$$

Necessity follows by adding equations; sufficiency is the connected internal incidence matrix having rank |S|-1 and even-syndrome image. Crucially, this is the **satisfiable subsource F_S**, not global logical consequence of the full UNSAT F_G.

Let Gamma fix any r<k distinct public boundary bits consistently, leaving m=k-r free wires. The restricted parity is still exactly one parity constraint on those m wires, and every projection to fewer than m wires is the full Boolean cube. Therefore any non-tautological clause or asserted factor on <=3 **unfixed cut wires**, justified solely by Gamma and Pi_b, requires r>=k-3. Conversely for 1<=m<=3 there exists a nontrivial width-m clause blocking one parity-violating assignment. This threshold holds for any fixed-variable choices and values.

**Conditional branch-cover corollary:** In a distinctly **proposed**, split-to-three-wire-localization protocol for two opposite parity rows, every closed leaf must fix at least k-3 cut bits. Each leaf covers at most 2^3 complete boundary assignments, so covering all 2^k assignments under AND obligations requires at least 2^{k-3} leaf contexts, regardless of adaptive split choices or unconditional shared-DAG lemmas. This is **NOT** a native R_mix341 lower bound: /341 has no free case-split/discharge rule, and its already-legal final XOR of opposite wide rows derives false with one node.

A separate, already largely known comparison: any equivalent **original-boundary-only, auxiliary-free CNF** for Pi_b has at least 2^{k-1} clauses, all width k. Every shorter clause is not an implicate, and each width-k clause forbids one of the 2^{k-1} wrong-parity assignments. Canonical blockers attain the bound. For connected BFS prefixes of size Theta(h) in cubic edge expanders, k=Omega(h), hence this restricted export is exponential; sparse GF(2) rows remain legal and compact. No general mixed or SAT-machine hardness follows.

## Independent source-authenticated finite replay

Full proof producer: four original clauses per vertex; three 8-row-checked AND3 inferences per vertex extracting the exact parity row; |V|-1 actual GF(2) XOR joins, with S and V\S summed separately before the final opposite-row XOR. The whole shared DAG has 4h-1 distinct paid nodes and every one of 4h original clauses in source ancestry. Every wide row remains GF(2), never masquerades as a LOCAL factor. This is an independently verified implementation of **the historical semantic /341 rules**, NOT an execution of an authoritative native byte parser.

11 exact cases: K4, cube, Petersen and six-sided prism, with connected S and k=4,5,6,7. Python: **8,876 assertions**, four source/row/reference/rule corruptions rejected. Independent JavaScript: **13,445 assertions**, four further negative controls, SHA-256 bound to original DIMACS bytes, direct exhaustive existential internal-edge projection, all strict boundary subsets and all partial-assignment contexts. A smaller self-contained published JavaScript reproducer reruns parity/context controls (1,356 checks); full typed certificates, Python producer, independent Node checker, raw JSON and exact-byte manifest are in the local run archive. Largest tested cut: prism6 k=7, restricted split-only leaves >=16, canonical boundary CNF 64 clauses, and actual mixed semantic refutation only 47 paid nodes. These are **different specified cost models**.

Actual local Python producer: 0.807 s host elapsed, 1,025,201 bytes traced peak Python allocations, `ru_maxrss` 98,704 in platform units; native TM time/space not measured. Source ASCII size 163..540 bytes, typed certificate JSON approximately 2.5..6.1KB. The free after-the-fact minimum charges distinct inference nodes once. Physical input reads/indexing, construction, policy, output, verification, retention/recomputation and caches are separate; no FLMV contraction inferred.

## Family ledger and open transfer

* Cubic odd-Tseitin: published exp Resolution / bounded-depth Frege hardness under their specified proof models; native mixed GF(2) linear proof is a mandatory shortcut, so NOT a mixed-hard candidate.
* Complete unary PHP: Haken exponential ordinary Resolution (pigeon clauses grow with holes); Cook polynomial ER shortcut. No lower bound preserved by arbitrary 3-CNF equisatisfiable conversion.
* Sparse graph-PHP: de Rezende et al., CCC 2020, exponential ordinary Resolution under specified sparse-expander assumptions; possible ER/Frege upper shortcuts, with native DEF facet transfer still unauthenticated.
* Bit-PHP: Braun 2026 Res(XOR) preprint scope/encoding distinct from full historical R_mix341; direct paid-DEF simulation still required.

**OPEN:** original historical accepted-byte LOCAL-CONVERT / DEF facet / private-exported wire grammar; polynomial original-source normalization of ALL permitted mixed shared derivations or a legal typed counterexample; superpolynomial full mixed Wbar_R; noncircular same-R B3; P versus NP. Root main.tex and all other roles' regions, tasks, weights, schedules unchanged.

Primary references: Urquhart, *Hard examples for resolution*, JACM 34 (1987), DOI 10.1145/7531.8928; Ben-Sasson & Wigderson, *Short proofs are narrow*, JACM 48 (2001), DOI 10.1145/375827.375835; Ben-Sasson, *Hard examples for the bounded depth Frege proof system*, Computational Complexity 11 (2002), DOI 10.1007/s00037-002-0172-5; de Rezende et al., CCC 2020, DOI 10.4230/LIPIcs.CCC.2020.28.
