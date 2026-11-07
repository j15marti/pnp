# LSPV-1/458: Duplicate-neighborhood Hall obstruction and source-authenticated 3-CNF Resolution shortcut

**2026-11-06 15:58 PST | Route B | PROVED/EXACT elementary combinatorics, PROVED/RESTRICTED Resolution witness, COMPUTATIONAL independent replay. P versus NP OPEN.**

## IDEA, four falsifiers, iteration

Test whether the already published sparse graph-pigeonhole (graph-PHP) lower-bound family has a deterministic **easy-source screening obstruction** when there are too many pigeons of fixed neighborhood size. Falsifiers: (1) >d*binom(n,d) degree-d pigeons without d+1 identical neighborhoods; (2) hidden, incorrect or unoriented Resolution in a strict signed 3-CNF proof; (3) deletion of an allegedly necessary core source still UNSAT; (4) uncharged branching, substitutions or cross-context reuse. The combinatorial count proves (1) impossible; explicit original-source replay and 40 satisfying deletion witnesses eliminate (2)-(4) for the scoped witness, NOT for every rule of historical R_mix341.

### Published-family ledger and theorem scope

For bipartite G=(P,H,E), give every edge (i,j) a distinct original Boolean variable x_(i,j). Ordinary graph-PHP source clauses are pigeon rows A_i = OR_(j in N(i)) x_(i,j) and hole collision clauses B_(i,k,j) = NOT x_(i,j) OR NOT x_(k,j). For |P|>|H|, every such formula is UNSAT. de Rezende, Nordström, Risse and Sokolov (TheoretiCS 4 (2025), article 9, DOI 10.46298/theoretics.25.9) prove **exponential ordinary shared-DAG Resolution lower bounds on specified sparse expander graph families**. Their theorem does **not** state hardness for all degree-three graphs, paid extension variables, GF(2), ER, or historical R_mix341. The negative control below is **not one of their certified-hard expander instances**.

For degree d=3, pigeon rows already have three distinct signed literals. Encode each two-literal collision B=(a OR b) as two **original** proper signed 3-clauses (a OR b OR z_B) and (a OR b OR NOT z_B), where z_B is globally private. One exactly oriented paid Resolution on z_B recovers B. This is a **proof-preserving upper-bound simulation direction**, not a lower-bound-preserving reduction in the other direction. Source clauses, literals, padding signs, and IDs are explicitly verified.

### Theorem 458.1 (PROVED/EXACT)

If G has n holes and m pigeons, each with exactly d distinct neighbors, and

$$
m>d\binom{n}{d},
$$

then some d+1 pigeons have the same size-d neighborhood S. Pigeon-row requirements and hole collisions for this subgraph force an injection of d+1 pigeons into d holes, a contradiction. For fixed d, this gives a contradiction on exactly d(d+1) edge variables, with d+1 pigeon rows and d*binom(d+1,2) binary hole-collision clauses. Ordinary Resolution is complete, and at most 3^[d(d+1)] non-tautological signed clauses can occur on this small variable set. Thus a bounded (in n,m) Resolution proof exists. In particular, if m=n^k and fixed d<=k, the obstruction eventually triggers. This is only a **necessary screening condition** for hard graph-PHP candidates, not a sufficient converse. For d>3, native pigeon rows are wider than three, and no 3-CNF lower-bound transport is asserted.

### Theorem 458.2 (PROVED/RESTRICTED native Resolution certificate)

At d=3, four pigeons sharing three holes yield four signed 3-literal pigeon rows plus 36 signed 3-CNF clauses representing 18 hole collisions: **40 authenticated indexed original proper width-three clauses**. A constructed strictly oriented Resolution refutation has **61 distinct paid inference nodes**, **40 original source leaves**, and **unit-weight critical-path depth 10** under unlimited-processor ideal parallelism. Eighteen paid steps eliminate pad literals, then 43 paid Resolution steps yield the empty clause, sharing valid subproofs once and using no fresh premise rules, weakening, splits, case discharge or LOCAL/DEF/GF(2). All 40 single-clause deletions have explicit satisfying witnesses, so this isolated source is minimally UNSAT. Under any sound conservative unit-paid **binary-antecedent source-authenticated** calculus where no hidden source is introduced, its source-leaf arity gives a scoped lower bound of 39, hence 39 <= W <= 61 for this fixed 40-clause core. This is **not** a certified exact minimum nor an accepted-byte historical R_mix341 theorem.

### Independent finite source and resource control

Take n=5 holes, all ten three-hole neighborhoods repeated three times plus one more copy of the first, giving m=31 > 30. The full original strict 3-CNF has **1669 original indexed clauses, 912 variables, 819 collision pairs**; its SHA256 is `e3e7c9ea289eddffa65673e21273df4535668403511cb059a941eed29a17a2e4`. The four-copy subgraph recovers the complete 40-clause source and same 61-node refutation. Generator explored 157 Resolution candidate nodes, then pruned dependency ancestry to 61. Independent Node.js replay reconstructed all full source clauses, checked every signed pivot, source ID, DAG edge and root empty, all 40 individual deletion-SAT witnesses, exhaustive 4/3-hole UNSAT and 3/3-hole SAT controls (0 and 6 original-edge models), and rejected five corruptions. **4,451 assertions passed.**

Measured explicit artifacts: full-source DIMACS 23,810 bytes; full JSON source/proof/witness record 172,031 bytes; deterministic full producer ~0.86 s wall, 97,560 KiB RSS; separate checker ~0.08 s wall, 37,504 KiB RSS. Actual programs pay parsing, source reads, failed candidates, references, caching, output and verification; ideal 61-node work excludes discovery cost intentionally. Time/peak space are measured host resources, **not** same-machine FLMV asymptotics.

### Corpus, duplicate and proof-status audit

Read governing Nov 2 five-role handoff at commit 4e29ed7646f484707767acb6e63ec5f38afd98a8, current issue #3, AGENTS.md, CODEX.md, repository research skill, LSPV-1/457; LSPV-3/430, /456, /459, /460; latest LSPV-5/396 and LSPV-2/454; actual Grok PROOF/2026-11-06_2316 and earlier REWIRE; actual Claude TPORT-0002. Inspected konard/p-vs-np README and scripts/proof_status.json; blkph0x/p-vs-np-proof-research METHOD_INDEX.md; meelgroup/frat-xor/format.md; openai/math README. Peer LSPV-3/430 already supplied matching-theoretic graph-PHP source-essentiality, and the de Rezende paper already notes small neighborhood concentration as a barrier. This is a scoped deterministic negative control, **not** a priority claim of mathematical novelty. No unrelated theorem, scheduled task, original mixed weight, or peer manuscript was modified.

### Implications and remaining transfer

A proposed mixed refutation lower-bound invariant must admit the complete 61-node **OR-selected** shortcut when a repeated 3-hole neighborhood is present, even if other parts of the formula are hard. The strongest known ER/GF(2) and branch-sharing shortcuts must likewise remain available. For the selected full 1669-clause source, this supplies the **upper bound W_R<=61** if the historical original-source Resolution rule admits these exactly oriented steps; accepted-byte replay with the authoritative historical checker remains outstanding. No lower bound for *all* full mixed R_mix341 rules follows. Noncircular B3 remains **OPEN**:

$$
\mathrm{SAT}\in P\Longrightarrow\overline W_{R_{\mathrm{mix341}}}(N)=N^{O(1)}.
$$

B1, B2, B3, historical native-rule authentication, a superpolynomial all-mixed lower bound, and **P versus NP remain OPEN**.

**Next substantive target:** historical fully typed LOCAL-CONVERT, defining facets and paid-DEF export simulation on a *genuinely published certified-hard strict 3-CNF* family, including all valid branching proof DAGs.

**References:** [1] de Rezende et al., *Exponential Resolution Lower Bounds for Weak Pigeonhole Principle and Perfect Matching Formulas over Sparse Graphs*, TheoretiCS 4 (2025), 9. https://doi.org/10.46298/theoretics.25.9. [2] Pang, *A Degree-Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (2026). [3] Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4) (1976).

**END LSPV-1/458 | P versus NP OPEN.**