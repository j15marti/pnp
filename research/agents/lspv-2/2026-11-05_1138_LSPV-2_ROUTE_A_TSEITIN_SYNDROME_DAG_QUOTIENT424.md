# LSPV-2/424: Source-cofactor shared-DAG cache versus parity quotient

**2026-11-05 11:38 PST | Route A primary | PROVED/EXACT restricted theorem | COMPUTATIONAL finite tests | P versus NP OPEN.**

## IDEA before SEARCH: falsifiers and revision

Hypothesis: exact signed cofactor memoization cannot collapse a complete matching-assignment layer of established cubic Tseitin 3-CNFs, although component-parity algebra can share branch reasoning. Falsifiers: (F1) two distinct matching assignments produce identical signed source cofactors; (F2) cycle-kernel assignments fail to merge; (F3) global even total charge implies every cofactor SAT; (F4) a compact quotient is misused as an all-input FLMV contraction. F1/F2 did not arise, F3 WAS FALSIFIED by cube opposite-component branches; F4 is an unsolved transfer.

## Hard-family ledger and previous work

Choose connected cubic graph G=(V,E), H vertices, 3H/2 original edge variables x_e, charges chi_v. Encode each vertex equation XOR_(e incident v) x_e=chi_v by the **four signed width-three CNF clauses** falsified by wrong local parity. The source has 4H clauses and length N=Theta(H log H) bits under consecutive DIMACS edge IDs. Connectedness implies SAT iff XOR_v chi_v=0. On suitable constant-degree expander sequences, Urquhart (JACM 1987, DOI 10.1145/7531.8928) and Ben-Sasson/Wigderson (JACM 2001, DOI 10.1145/375827.375835) give exp(Omega(H)) lower bounds **for ordinary shared-DAG Resolution**, not all SAT machines. Four finite K4/cube/Petersen/Heawood examples serve as encoding controls, NOT certified growing hard instances. LSPV-2/341 already proves minimum W_Rmix341(F)=4H-1 for bridgeless odd-charge cubic instances via AND3 and GF(2), so restricted Resolution hardness does not transfer to the fixed mixed calculus. LSPV-2/422 identified exponential literal boundary masks and compact affine messages; LSPV-2/423 showed a direct-cofactor TREE mass obstruction. This run addresses shared-DAG state caching.

## THEOREM 424.1: rank and exact cofactor-cache count

Fix an original edge subset S of k variables, an assignment a in GF(2)^k, and incidence matrix B_S over GF(2). Every original vertex-indexed parity cofactor has residual charge

$$
\chi'(a)=\chi+B_S a.
$$

Let c(V,S) count connected components of the graph (V,S), including isolated vertices. Its incidence rank is r=H-c(V,S). Exactly 2^r different charge vectors arise, each reached by 2^(k-r) original branch assignments. Proof: substitute assigned edges into original equations; apply incidence rank and rank-nullity. The kernel is exactly the cycle space.

If source vertex grouping is retained, different charge vectors give distinguishable residual vertex constraints (where the grouping and zero-variable vertices are explicit). Without vertex tags an arbitrary cofactor CNF may merge constraints from distinct vertices. **For S a matching in a simple cubic graph** every affected vertex retains two edge literals and every unaffected vertex retains three, with distinct remaining clause supports; therefore different matching assignments produce different FLATTENED signed residual CNFs, even after deduplication. All 2^k states are distinct for this particular complete matching layer.

Every maximal matching in a simple cubic graph has k>=H/6: there are H-2k unmatched vertices, all adjacent to a matched endpoint; each of the 2k matched endpoints has at most two unmatched neighbors, hence H-2k<=4k. Thus an **exhaustive matching-layer exact-cofactor cache** needs >=2^(H/6) distinct records even granting free optimal perfect memoization. This does NOT constrain a solver that avoids that layer, uses different quotient keys, or directly applies GF(2).

## THEOREM 424.2: exactly correct assumption-typed AND join

Let G-S have components C_1,...,C_c. Each component residual is satisfiable precisely when the XOR of its residual vertex charges is zero. With

$$
u_j=\bigoplus_{v\in C_j}\chi_v,\quad M_{j,e}=1\quad\hbox{iff the assigned edge }e\hbox{ crosses component }C_j,
$$

a branch a is SAT iff M a=u. The contracted graph is connected because G is, so rank(M)=c-1. For odd original total charge, M a=u has no solutions; for even original total charge it has exactly 2^(k-c+1) solutions. Proof: each residual component incidence matrix has rank |C_j|-1, and consistency requires component charge zero; M is the incidence of connected contracted graph, so rank(M)=c-1.

**Hostile countercontrol:** on the cube, assign the four parallel edges separating two square faces. Their 16 flattened signed cofactors are all different; under even global charge exactly **8 are SAT and 8 UNSAT**. A naive test of global parity wrongly accepts 8 UNSAT branch contexts. One component-cut parity equation repairs this; under odd global charge zero branches are SAT. Heawood matching has 128 distinct cofactors; its six-edge cycle has 64 assignments but 32 distinct syndromes.

## SEARCH sources, iteration and checks

Authenticated source review: governing handoff research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (blob c3889a3e), issue #3 through LSPV-2/423, AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md; preceding /341, /422, /423; LSPV-4/418 and LSPV-3/427. Actual Grok files GROKPROOF/2026-11-05_1014_PROGRESS.md, 1015_PROGRESS.md and 1913_PROGRESS.md; actual Claude research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex. Neither yields universal FLMV contraction.

Required external repository review: konard/p-vs-np README (blob 0e0ec77f), proofs/complexity/README (7ee9a11e), describing finite one-tape P subset NP, not FLMV. blkph0x/p-vs-np-proof-research README (f397a774) and METHOD_INDEX (18d693ea) describe scoped exact results, not P vs NP. MassimoLauria/cnfgen/cnfgen/families/tseitin.py (4bb5fd19) implements established graph parity CNFs. openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (1ced21f4) formalizes costs for its PARTICULAR program, not arbitrary SAT A. Primary FLMV JACM 2005, DOI 10.1145/1101821.1101822, read and checked against the indexed-machine model. Search terms: FLMV random access SAT time space, Urquhart expander Tseitin, cycle-space cofactor caching and the two required repository names. Direct Google-branded search unavailable; indexed web and authenticated GitHub used.

Iteration made two corrections: the global-parity-only join is false for individual even-charge branch contexts; flat CNF injection is proved only for matching S, with arbitrary S retained as vertex-group-indexed data.

The original full Python producer enumerated **18 cases** on four graphs with both source charge labels, 31,944 partial-state checks, checking signed original source, exact original clause reduction, component ranks, and hostile malformed/mutated controls. An independently implemented Node verifier executed **1,535 checks and 4 corrupted-record rejections**. Local Python runtime ~1.33 seconds, tracemalloc peak 391,440 bytes; these are NOT native FLMV time or space measurements. A compact independent replay reconstructs 18 rows and performs 677 counted checks. Complete full producer, independent checker and 36KB original raw data are in the separate user-facing reproducibility archive.

## Physical accounting and remaining OPEN arrow

The algebraic representation is O((H+k)log H) bits, not automatically a <=N^(1/2) ordinary-CNF guest child. An algorithm must charge parsing, authentication, source and index/head reads, policy search and failures, cofactor writes, reference hashing, caches, context typing, AND joins, validation, output, guest-input access, intermediate and simultaneously live memory, and any required recomputation. The required all-phase s'<=max{rho,eta,lambda,lambda*s} remains unproved here.

**OPEN:** for EVERY fixed total uniform polynomial-time SAT decider A with unknown finite t,s, construct a recursively applicable both-label malformed-aware ALL-INPUT same-FLMV-machine Phi(A) satisfying t'<=max(11/10,3/5+t/2) and s'<=max(1/2,s/2). No theorem here asserts that transformation or any unrestricted computational lower bound. Route B B3 and P versus NP remain OPEN. Root main.tex is 1.7MB but its authenticated fetch returns no readable content: not modified. No task/schedule/other-role files changed.
