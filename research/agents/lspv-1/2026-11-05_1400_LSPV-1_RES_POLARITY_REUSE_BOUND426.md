# LSPV-1/426: Positive-literal fanout budget in shared Resolution over established graph-PHP sources

**November 5, 2026, 14:00 PST | Route B | PROVED/RESTRICTED (symbolic, pending specialist review), COMPUTATIONAL finite replay.** Full historical \`R_mix341\`, B1, B2, B3, superpolynomial mixed \`Wbar_R\`, and P versus NP remain **OPEN**. This is a new project-level quantitative *ordinary Resolution* refinement of the existing binary source-arity floor, not a general-machine lower bound.

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis.** For an original-source-essential graph-pigeonhole 3-CNF, the $m-1$ fan-in-two lower bound might be attained by a source-disjoint Resolution tree, so source-minimum work would require no derived-lemma sharing. Exact falsifiers: (F1) an oriented RES pivot can increase positive-literal mass; (F2) a source-deletion SAT witness fails, so a source is not essential; (F3) a source-disjoint RES proof does derive empty despite an apparent sign deficit; (F4) AND3/GF(2)/DEF in the full native calculus invalidates promotion of a Resolution-only bound.

**Search.** Read the November 2 governing refocus, current issue #3 through LSPV-5 REFEREE370, AGENTS.md, CODEX.md, the repo research skill, historical native LSPV-2/341, LSPV-1/424-/425, LSPV-3/427-/430, and real Grok \`GROKPROOF/2026-11-05_1913_PROGRESS.md\` and Claude \`research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex\`. Existing LSPV-3/430 *already establishes* the graph-PHP source-essentiality matching criterion. LSPV-3/428 and LSPV-5 REFEREE367 *already establish* scope-safe branch-Resolution lifting. Neither is re-claimed here. Queried repository for "positive occurrence budget pigeonhole read once", "polarity token conservation resolution", "signed polarity fanout lower bound", and affine/branch lifts. Read primary Haken (ordinary Resolution), Ben-Sasson--Galesi (graph-PHP Resolution space), Cook (ER), and Kleine Büning--Wojciechowski--Subramani (read-once 2CNF) results. Indexed web searches included "read once resolution pigeonhole principle", "read once resolution minimally unsatisfiable deficiency", and "graph pigeonhole Resolution lower bound". Direct Google-branded interactive search was unavailable: indexed web and authenticated GitHub search were used, without claiming a Google session.

Required external current repository files inspected: \`konard/p-vs-np/README.md\` and \`DETAILED_SOLUTION_PLAN.md\` (model-scoped educational claims, not an arbitrary-machine theorem); \`blkph0x/p-vs-np-proof-research/METHOD_INDEX.md\` and \`README.md\` (explicitly scoped certificates/obstructions); \`meelgroup/frat-xor/format.md\` (typed XOR evidence format, **not** the historical R grammar); \`openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean\` (a concrete costed model, **not** a proof-size transfer). No relevant same-R B3 result was identified.

**ITERATION.** The corrected idea charges *weighted reuse of already-derived positive literals* rather than assuming source-disjoint trees can be optimal. Source-arity and polarity conservation together imply an exact all-size necessary fanout budget. A finite independent read-once closure on the smallest complete graph-PHP validates the obstruction. Its full-native extension is explicitly **not** asserted.

## Lemma 426.1: exact signed fanout conservation for shared strict Resolution

Let $F$ be any tautology-free source CNF, and let $\pi$ be a finite *ordinary exact binary Resolution* DAG refutation whose root $r$ is the empty clause. Require every retained node to be an ancestor of $r$, source clauses to have authenticated IDs, and every non-source node to be a genuine, oriented non-tautological RES inference. Distinct inference nodes cost one; sharing is allowed without unfolding. Define $P(v)$ as the number of positive literals in the clause at node $v$, and $\deg^+(v)$ as the number of *premise references* leaving $v$, counted with multiplicity when a node is cited twice. Let $q$ count paid RES nodes, and $P_0=\sum_{s\in {\rm src}(\pi)}P(s)$.

**PROVED/RESTRICTED:**
$$
\boxed{q\ \le\ P_0+\mathcal R_+(\pi),\qquad
\mathcal R_+(\pi)=\sum_{\substack{v\in\pi\\v\ne r}}(\deg^+(v)-1)P(v).}
$$

**Proof.** In a strict RES inference $u,v\to w$, exactly one positive pivot literal is removed, no positive literal is created, and nonpivot duplicate-positive elimination only decreases positive count. Hence
$$
P(u)+P(v)-P(w)\ge1.
$$
Sum over the $q$ paid inferences. Each source $s$ appears in the positive parent sum $\deg^+(s)$ times and has no negative child term; each paid node $v$ appears as a child once and as a parent $\deg^+(v)$ times. The root has $P(r)=0$. Every other retained node has $\deg^+(v)\ge1$, so the right side is exactly
$$
\sum_{s\in{\rm src}(\pi)}P(s)+
\sum_{v\ne r}(\deg^+(v)-1)P(v).
$$
This is the claimed inequality. QED.

If $F$ is *clause-minimally UNSAT*, all $m$ source clauses must appear in any sound source-authenticated refutation, and the established binary-fan-in ancestry edge bound gives $q\ge m-1$. Therefore
$$
\boxed{\mathcal R_+(\pi)\ge m-1-\sum_{C\in F}P(C).}
$$
If the right side is positive, *every* Resolution refutation must reuse some source or derived node carrying a positive literal. This remains true even when the proof can reconverge and freely select its best legal derivation. It does **not** imply an additional lower bound on $q$ when reuse is permitted; $\mathcal R_+$ is an explicit graph/reference property, not another native node weight.

## Corollary 426.2: complete and sparse graph-pigeonhole CNFs

For a bipartite graph $G=(P,H,E)$ with $|P|=|H|+1$, introduce original variable $x_{p,j}$ for each edge. Include one source row clause $A_p=\bigvee_{j\in N(p)}x_{p,j}$ per pigeon, and every collision source $B_{p,q,j}=(\neg x_{p,j}\lor\neg x_{q,j})$ for distinct pigeons sharing hole $j$. This is *direct* width-at-most-three CNF whenever all pigeon degrees are $\le3$: no clause-width reduction or lower-bound-preservation claim is needed. The source statistics are
$$
m=|P|+\sum_{j\in H}\binom{\deg(j)}2,\qquad
P_0=|E|.
$$
When every source is individually indispensable, as can be established by the **existing** LSPV-3/430 matching criteria, all strict source-authenticated ordinary-Resolution refutations obey
$$
\boxed{\mathcal R_+\ge |P|+\sum_j\binom{\deg(j)}2-1-|E|.}
$$
This holds for any such graph, but it does *not* assert that every published hard expander graph satisfies the antecedent. Exact matching verification is required for a chosen published family.

For the standard *complete* graph $\mathrm{PHP}_{h+1}^h$ we can prove essentiality directly: after removing one pigeon row, match the other $h$ pigeons bijectively to the holes; after deleting one collision $(p,q,j)$, map both $p,q$ to $j$ and all remaining $h-1$ pigeons injectively to the other holes. In each case exactly the deleted source clause is violated. Thus
$$
m=h+1+h\binom{h+1}{2},\quad P_0=h(h+1),\qquad
\boxed{\mathcal R_+\ge \frac{h^2(h-1)}2\quad(h\ge2).}
$$
For $h=2$, source clauses $m=9$, variables $6$, minimum ordinary-RES fan-in bound $q\ge8$, and $\mathcal R_+\ge2$. For $h=3$, *original signed 3-CNF without auxiliaries*: $m=22$, variables $12$, row width $3$, and $\mathcal R_+\ge9$. For $h>3$ the standard complete-PHP row clauses are wider than three; **this argument does not transport Haken's infinite unary-PHP lower bound to 3-CNF**.

If all premise-positive fanout excesses vanish, source-disjoint read-once Resolution is impossible for these $h\ge2$ formulas. Even sharing negative-only clauses cannot remove the positive mass deficit. This is a uniform *necessary reuse theorem*, not a size or time lower bound for general shared Resolution, because the legal reuse can be cheap.

## Family, proof system, and shortcut ledger

| Source | Exact encoding / size | Established hardness model | Available shortcuts and transfer boundary |
| --- | --- | --- | --- |
| Haken $\mathrm{PHP}_{h+1}^h$ | $h(h+1)$ edge variables; $m=h+1+h\binom{h+1}{2}$ clauses; explicit signed indexed size $N=\Theta(h^3\log h)$; row width $h$ | Haken 1985: $2^{\Omega(h)}$ **ordinary shared-DAG Resolution** lines for $h\to\infty$ | Cook 1976 gives polynomial **Extended Resolution** proofs. Not direct 3-CNF for $h>3$, not a mixed-system or machine-time lower bound. |
| Graph-PHP $G$ | Pigeon rows of width $\deg(p)\le3$, binary collisions; $N=O((m+|E|)\log(|E|+2))$ | Ben-Sasson--Galesi 2003 studies lower bounds in **Resolution clause space** for specified expanding graphs; actual graph/hypotheses must be verified before any family-wide transfer. | LSPV-3/430 source matching test; this report gives a conditional strict-Resolution fanout bound, no full-mixed bound. |
| Odd cubic expander Tseitin | $h$ cubic vertices, $3h/2$ edge variables, $4h$ width-three original clauses, $N=\Theta(h\log h)$ | Urquhart 1987, Ben-Sasson--Wigderson 2001: exponential **ordinary DAG Resolution** for suitable cubic expanders | Historical full mixed AND3/GF(2) has the **legal** $4h-1$ refutation; therefore no Resolution-to-mixed size transfer on this family. |

The 3-CNF $K_{4,3}$ control certifies *UNSAT and source-minimality*, and only the displayed restricted positive-reuse lower bound. Its small size is not a published asymptotic proof-hardness certificate. Likewise, solver runtime observations are not substituted for a published hardness theorem.

## COMPUTATIONAL evidence and independently executable replay

Files:
- \`experiments/arc/lspv1_426_php_polarity_reuse.js\`, source generator, exhaustive small Resolution polarity validation and source-disjoint DP.
- \`experiments/arc/lspv1_426_independent_verify.js\`, no-import independent algorithm and negative-control verifier.
- \`results/raw/arc/2026-11-05_1400_LSPV1_GRAPH_PHP_POLARITY_REUSE426_raw.json\`, exact source arrays, source-deletion models, all counters and independent replay.

The producer checked every oriented strict RES step among the $3^4=81$ non-tautological clauses on four variables: **2,744** valid oriented inferences, zero polarity-budget failures. It built full original-source complete-PHP controls: $h=2$ (9 clauses, 6 variables) and $h=3$ (22 clauses, 12 variables), checked all $2^6$ and $2^{12}$ assignments respectively, and obtained all **31** independent deletion witnesses. A strict source-disjoint proof-tree dynamic program over all subsets of the nine sources at $h=2$ reached **120** (subset, derived-clause) pairs and no empty clause at full support. The separately implemented verifier independently reconstructed both original sources, replayed every deletion model, checked all 2,744 valid oriented RES steps, and independently reran a recursive read-once closure: **3,352 assertions passed**. It rejected a forged source-deletion witness and deliberately invalid pivot/tautological rules.

This is finite regression plus an explicit all-size algebraic proof. The finite closure is an **exact proof of no 8-node read-once strict RES refutation** for the specified nine-clause source; it is *not* an optimum over all mixed proof DAGs and does not establish any nonconstant-size asymptotics.

## Quantifiers, resources and remaining barriers

The *fixed* $R_{\rm mix341}$ charges one unit per distinct shared paid inference/definition node and includes strict RES, AND3, GF(2), local conversion and globally fresh paid conservative DEF. Our lemma's positive-polarity potential applies **only when every charged step is ordinary RES**: AND3 factors, GF(2) rows and paid gate facets are not such clauses, and a cross-representation step can invalidate the token accounting. Treating this as a full-native lower bound would be an illegal transfer. Proposed branch ASSUME/MERGE/discharge rules are not silently added.

The DP optimizer explicitly explores source-subsets and consumes time/space beyond the ideal logical $q$; its exploration cannot be counted as a free physical SAT algorithm. Authenticated DIMACS bits, parsing, row/collision construction, source-index reads, proof references, hash/indexing, malformed inputs, search failures, certificate verification, output, storage and recomputation, and all-phase simultaneously live memory are separate. The present scripts are host JS finite computations, not exact Turing-machine/FLMV traces; no unmeasured RSS or runtime is asserted. The raw witness/reference payload is larger than the mathematical node minimum. A parallel proof critical-path depth is also not determined by this lemma.

For every fixed uniform total, SAT/UNSAT/malformed-correct algorithm $A$, project B1 asks pointwise $W_R(F)\le p_A(|F|+T_A(F))$, B2 asks worst-case $\overline W_R(N)\le p_A(N+T_A^{wc}(N))$, and weakest B3 asks whether $\mathrm{SAT}\in P\Rightarrow\overline W_{R_{\rm mix341}}(N)=(N+1)^{O(1)}$ for this **same preselected calculus**. These are **OPEN**. This restricted polarity result supplies neither a lower bound surviving all native mixed shortcuts nor a noncircular B3 reflection/certificate compiler.

**Next test:** apply the new positive-fanout accounting as a *diagnostic* to an independently authenticated published bounded-left-degree graph-PHP Resolution proof, and explicitly test the first native AND3, XOR, LOCAL-CONVERT or paid-DEF consumer that breaks it. Coordinate exact typed source IDs with LSPV-3 and adversarial mixed-rule/branch sharing with LSPV-5, without altering ownership or rules.

## References

[1] Haken, A. (1985). The Intractability of Resolution. *Theoretical Computer Science* 39:297-308.

[2] Cook, S. (1976). A Short Proof of the Pigeon Hole Principle Using Extended Resolution. *SIGACT News* 8(4):28-32.

[3] Ben-Sasson, E. and Galesi, N. (2003). Space complexity of random formulae in resolution. *Random Structures and Algorithms* 23:92-109. DOI 10.1002/rsa.10089.

[4] Urquhart, A. (1987). Hard Examples for Resolution. *JACM* 34:209-219.

[5] Ben-Sasson, E. and Wigderson, A. (2001). Short Proofs Are Narrow: Resolution Made Simple. *JACM* 48:149-169.

[6] Kleine Büning, H., Wojciechowski, P., and Subramani, K. (2016). On the Computational Complexity of Read Once Resolution Decidability in 2CNF Formulas. arXiv:1610.04523.

## Execution environment and control coverage

The no-import producer and independent verifier were executed directly in the connected JavaScript research runtime. They operate on indexed, canonical signed-clause arrays, **not** arbitrary DIMACS byte strings. Corrupted Resolution pivots, tautological resolvents and a forged source-deletion witness were rejected; **malformed DIMACS parsing was not rerun in LSPV-1/426**, although it is a control in historical Rmix341/341. No historical authoritative Rmix341 checker was executed for this restricted result. The container/Python environment returned `redis.exceptions.ResponseError` to both attempted execution tools, so the repository `preflight.py` and `scripts/check_research_reports.py` could not be run in this environment; this must not be reported as a passing check. The committed JS and raw records allow independent replay in a normal Node.js environment. Root `main.tex` was later reconciled inside the exact LSPV-1 ownership range in commit `4494ab7edd48fdd0083991f7d7127cc0bf8f96b2`; full GitHub-content readback showed byte-exact preservation outside the inserted 1,456-character note.
