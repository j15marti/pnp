# LSPV-3/521: Pair-defect group deletion and strengthened source-ancestry bound for published-hard strict-3CNF modulo-three Tseitin

**2026-11-08 20:36 PST | Route B, LSPV-3 | PROVED/RESTRICTED analytic source lemma; COMPUTATIONAL exhaustive/constructive controls. Historical R_mix341, B3, and P versus NP OPEN.**

**Proof-chain IDs:** new **[P2-L3-521]** refines [P2-L3-520], [P2-L1-523], [P2-D3], [P2-F6], and the qualifications on [P2-D1], [P2-C3], [P2-B1], [P2-B2]. [P1-X1] unchanged. This is an improved *linear* source lower bound, not superpolynomial mixed-system hardness.

## IDEA, pre-search falsifiers, and revision

Hypothesis: although LSPV-1/523 correctly identifies nine individually redundant wrong-defect forbidden triples at each vertex of the original-source signed mod-3 strict-3CNF, those clauses cannot be removed simultaneously at two vertices without making the formula SAT. The **precise falsifiers** were (F1) a connected graph where the prescribed two-residue defect vector has no edge flow; (F2) an assignment satisfying the original or a single wrong-defect group deletion; (F3) a pair-flow assignment that falsifies an ALO, an essential-class clause or a clause at a third vertex; (F4) a claim that the group's clauses are not literal original-source clauses of the published-hard strict3 CORE. None was observed; algebra and the original-source checks establish the stated result for all connected simple cubic graphs.

Search found the prior **one-clause** charge classification in LSPV-1/523, but no prior general *two-vertex group-deletion/source-cover* result in the inspected project. The revised target is a theorem about **which original sources must occur in any sound proof ancestry**, not a claimed new proof rule or an all-rule superpolynomial minimum.

## Original-source family and published hardness ledger

Let $G=(V,E)$ be connected, simple, cubic; $h=|V|$ is even, $m=|E|=3h/2$. Orient edges arbitrarily. Give every edge $e$ Boolean atoms $x_{e,t}$, $t\in\mathbb F_3$. Fix charges $b_v\in\mathbb F_3$ with $\sigma=\sum_v b_v\in\{1,2\}$.

The exact proper strict-3CNF CORE of LSPV-3/520 consists of one **original** $A_e=x_{e,0}\vee x_{e,1}\vee x_{e,2}$ per edge, and 18 **original** signed negative triples
$$
D_{v,(t_1,t_2,t_3)}=\neg x_{e_1,t_1}\vee\neg x_{e_2,t_2}\vee\neg x_{e_3,t_3}
$$
per vertex whenever $\sum_{i=1}^3s_{v,e_i}t_i\ne b_v$ in $\mathbb F_3$, with $s_{v,e}\in\{+1,-1\}$ the incidence sign. There are $39h/2$ distinct original clauses, $9h/2$ original Boolean atoms, all clauses properly of width three. The unexpanded DIMACS length is $N=\Theta(h\log h)$ with sequential decimal IDs.

**Published model-specific hardness:** Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (October 24, 2026), §7.1 and Theorem 7.2(b), gives $\exp(\Omega_{p,r}(h))$ refutation-size lower bounds for the *standard* mod-$q$ Tseitin CNF on fixed-degree regular edge expanders in $\operatorname{Res}(\mathrm{PC}_r/\mathbb F_p)$, $p\ne q$, fixed $r$. With $p=2,q=3$, our strict3 CORE is a literal subformula of its standard one-hot input, after deletion of edge-AMO sources. The prior /520 proof establishes exact semantic one-hot recovery and 12-RES source-authenticated AMO macros; monotonic source-axiom containment transfers the lower bound **in the correct direction** to the strict3 CORE for that same Res(PC) calculus. No hardness against Extended Resolution, the unrestricted historical mixed calculus or arbitrary algorithms is claimed.

Relevant controls: ordinary-Resolution exponential Tseitin lower bounds (Urquhart 1987; Ben-Sasson and Wigderson 2001), opposite-field algebraic proof lower bounds (Pang), existing LSPV-1/520 signed-AND DEF/RES polynomial upper controls, and LSPV-5/450 historical DEF facet-owner objection.

## Theorem 521.1 (exact wrong-defect vertex-group deletion threshold)

Partition the forbidden original clauses at each vertex $v$ into two nine-clause sets:
$$
E_v=\{D_{v,t}:\sum_i s_{v,e_i}t_i=b_v-\sigma\},\qquad
R_v=\{D_{v,t}:\sum_i s_{v,e_i}t_i=b_v+\sigma\}.
$$
The $R_v$ clauses are the **individually redundant** ones in LSPV-1/523. For any $U\subseteq V$ set $F_U=F\setminus\bigcup_{v\in U}R_v$. Then, for every connected simple cubic graph with $h\ge2$,
$$
\boxed{F_U\text{ is UNSAT}\iff |U|\le1.}
$$

**Proof, SAT direction:** Choose distinct $u,v\in U$. Modify the requested divergences to $d_u=b_u+\sigma$, $d_v=b_v+\sigma$ and $d_w=b_w$ elsewhere. Since $\sum_wd_w=\sigma+2\sigma=0$ over $\mathbb F_3$, connectedness implies the oriented incidence map $B:\mathbb F_3^E\to\{d:\sum d=0\}$ is surjective. Obtain $z$ constructively on a spanning tree, setting off-tree values zero and each tree edge to the signed charge of its child subtree. Set exactly one indicator $x_{e,z_e}=1$ per edge. All ALOs hold, and all vertices outside $\{u,v\}$ satisfy their charge equation. At each of $u,v$, exactly **one** original forbidden clause is false; its signed sum is $b+\sigma$, hence it belongs to $R_u$ or $R_v$ and is deleted. Every retained source clause is true. Thus $F_U$ is SAT.

**Proof, UNSAT direction:** $U=\emptyset$ is the original inconsistent charged Tseitin system. If $U=\{v\}$, every other vertex's full set of 18 forbidden clauses and edge ALOs enforces one-hot on each incident edge: two true values on one edge and a true value on each other incident edge would activate a forbidden triple. Since the simple graph has no loops, each edge is incident to at least one intact vertex $w\ne v$, so **all edges** are one-hot. Every intact vertex has divergence $b_w$; global incidence cancellation then forces divergence $b_v-\sigma$ at $v$. But $E_v$ is retained and forbids exactly that local tuple, contradiction. This proves the iff statement without a SAT oracle, assuming only the displayed original sources.

An even sharper pair witness follows: for every $\{u,v\}$ there exist original clause IDs $C_u\in R_u$, $C_v\in R_v$ such that $F\setminus\{C_u,C_v\}$ is SAT, while either one-clause deletion is UNSAT by the same charge argument. Thus individual clause redundancy is **not compositional**.

## Theorem 521.2 (new used-source and paid-work lower bounds)

Let $S$ be the distinct original-source clauses in the contradiction ancestry of any sound, conservative, source-authenticated refutation of $F$. A source subset used in a sound refutation must itself be UNSAT. Write $T(S)=\{v:S\cap R_v\ne\emptyset\}$. If $|V\setminus T(S)|\ge2$, choose $u,v$ outside $T(S)$. The two-defect witness above satisfies **every source in $S$** because it falsifies only one clause of $R_u$ and one of $R_v$. This contradicts soundness. Therefore
$$
\boxed{|T(S)|\ge h-1.}
$$
This vertex-group bound is tight **as a group-support threshold**, since deleting all of $R_v$ at one vertex leaves an UNSAT formula, though it is not an exact minimum number of individual clauses.

For $2$-vertex-connected cubic graphs, LSPV-1/523 proved $m_{\mathrm{ess}}=21h/2$ individually indispensable original clauses, disjoint from every $R_v$. All such clauses must occur in $S$ and, by the preceding lemma, at least $h-1$ additional **distinct** source clauses from pairwise distinct $R_v$ must occur. Hence
$$
\boxed{r:=|S|\ge\frac{23h}{2}-1.}
$$
In a sound conservative unit-cost inference DAG with only original free sources, all paid nodes indegree at most two, and no independent contradictory axiom, the undirected contradiction ancestry is connected, and source-count edge accounting yields $q\ge r-1$. Therefore
$$
\boxed{q\ge\frac{23h}{2}-2.}
$$
This improves /523's $q\ge21h/2-1$ by exactly $h-1$ nodes. The counting allows free optimal derivation choice, shared/reconvergent DAGs, conservative paid auxiliaries, and any **legal** shortcuts fitting its premise/provenance conditions. It does **not** cover an uncharged multi-premise oracle, unidentified historical DEF facets as free sources, or unauthorized branch hypothesis leakage. It is linear in $h$ and $\Omega(N/\log N)$ in input bits, far below the required superpolynomial [P2-B1].

## IDEA -> SEARCH -> ITERATE verification and hostile controls

Executed independently implemented Python and Node.js original-source programs on $K_4$, $K_{3,3}$, cube, Petersen, and prism-16, for $\sigma=1,2$. They constructed and replayed all **428** vertex-pair witness assignments; each failed exactly two source clauses in the prescribed wrong-defect groups. Correct source counts and strict width, signed orientation, spanning-tree flow and source IDs were checked. For both charges on $K_4$, independently exhaustively evaluated all $2^{18}=262{,}144$ Boolean assignments, including multi-hot controls, and all $16$ wrong-class vertex-group deletion combinations. Each subset was SAT exactly when at least two groups were deleted. Python found 567 assignments satisfying the retained ALO and essential-class clauses per charge. Node.js logged 2,720 independent assertion groups, including a corrupted-source negative test. This is finite evidence supporting, not replacing, the algebraic proof.

The Python executable measured approximately 0.10 s on the local host; peak RSS around 100,512 KiB because the exhaustive test materializes NumPy arrays. Host RSS is **not** a TM space bound. A single constructive tree-flow witness uses $O(h)$ algebraic field operations and $O(h\log h)$ explicitly encoded storage; original-source building, incidence indexing, source authentication, checking every retained clause, writing output and bit arithmetic have additional polynomial bit costs. Enumerating all $\binom h2$ pair witnesses costs $O(h^3)$ simple field/verification operations if each witness scans all $\Theta(h)$ clauses. The raw file records one illustrative witness per graph and charge, not the full $O(h^3)$ witness collection. Source reading, parsing, construction, exhaustive-search controls, failed cases, memory allocation and report/write/readback are not treated as free in actual machine upper bounds. Source-plus-certificate bytes and tree index bit costs are separated from the ideal DAG node count.

## Authentication, dependencies, and unresolved work

The historical /341 **prose** is `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`). It specifies unary paid DEF/LOCAL and binary RES/AND3/XOR, but the full original accepted-byte selector grammar remains unverified. This theorem is source-semantic; **no historical R_mix341 checker, no official CakeML checker, no general SAT machine** was executed. The stronger legal shared-circuit shortcuts from LSPV-1/520 and source-owner objections from LSPV-5/450 remain valid upper-bound and adversarial controls. No shortcut is excluded from the true minimum merely to protect the linear lower bound.

Corpus checked: both entire root trackers, issue #3, governing five-role handoff (historical 4e29ed7), AGENTS.md, CODEX.md, the repository skill, actual Grok `GROKPROOF/2026-11-08_1130_PROGRESS.md`, actual Claude `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`, LSPV-3/520, LSPV-1/520-/523 and LSPV-5/450. Primary Pang Theorem 7.2(b) inspected at https://arxiv.org/html/2610.00837v2. External pinned files: `konard/p-vs-np/README.md` (blob `0e0ec77`), `konard/p-vs-np/scripts/proof_status.json` (`93b77ed`), `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` (`18d693e`), `meelgroup/frat-xor/format.md` (`986a21a`), and `openai/math/README.md` (`cc5b0a0`). These are not historical native proof checkers. Web search used; no separate Google-branded backend available, so no Google-specific search asserted. No novelty claim follows from failed search.

**Next explicit gap:** authenticate original-byte RES/AND3/DEF/LOCAL owner and assumption interfaces, then test whether any legal native upper control for this *same original-source formula* satisfies the declared inference weights. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN; P versus NP remains OPEN. Five existing agents, historical weights, task IDs, titles, enabled states, schedules, and 2 Route A / 3 Route B allocation unchanged.
