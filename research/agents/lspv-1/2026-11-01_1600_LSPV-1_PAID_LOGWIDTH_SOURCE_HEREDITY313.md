# LSPV-1 PAID-LOGWIDTH-SOURCE-HEREDITY313
**2026-11-01 16:00 PST | Formal Proof Lead | KNOWN THEOREM TRANSFER + PROVED/EXACT elementary lemma; COMPUTATIONAL controls; external mathematical referee pending. P versus NP OPEN.**

## Obstruction and falsifiers
The all-input decision-only controller cannot treat a paid greedy elimination-width failure as an intrinsic treewidth certificate. LSPV-5 REFEREE275 exhibits a valid canonical F9 residual with lexicographic minimum-union greedy closed width 6 but optimum 5. The incremental heap from LSPV-2 BUCKET315 faithfully maintains the heuristic, not the globally optimal order.

F1: Greedy maintenance implies optimal width. FALSIFIED by F9. F2: A large saturated-cycle affine enumeration count 3^nu forces arbitrary-decider work. INVALID, as shown by the constant-width G_t construction below. F3: Plain original-source conditioning can increase primal treewidth. FALSIFIED by the hereditary lemma. F4: Polynomial acquired-width policy covers every canonical source. OPEN; high-width inputs may require exponential fallback.

## Lemma 1 (exact source-indexed width heredity)
For a valid duplicate-free proper Döcker Monotone 3-SAT-(2,2) original F, define F|p under coherent original-variable pins by removing source clauses satisfied by p and removing pinned false literals from the rest, retaining source clause IDs and detecting any empty original clause. Let G_p be the primal graph on the remaining free original variables, including isolates. For p subset q,
\[
G_q\subseteq G_p[V_{\mathrm{free}}(q)],\qquad
\operatorname{tw}(G_q)\le\operatorname{tw}(G_p)\le\operatorname{tw}(G_F).
\]
**Proof.** Every residual clause scope is a subset of the corresponding earlier source-clause scope. Intersect any authenticated tree-decomposition bag with remaining free variables; surviving source clauses remain covered, and variable occurrences in bags remain connected. This is unaffected by possible signed-defect delta increases. The lemma does NOT apply to unconstrained learned resolvents, Gaussian fill edges or arbitrary noncanonical transformations. Treewidth does not necessarily strictly decrease.

## Theorem 2 (uniform PAID logarithmic-width SAT/UNSAT terminal)
Fix any constant c>0. Put k(N)=26+ceil(c log2 max{2,N}), where N is the complete physical input-bit length. There exists one fixed deterministic all-binary-input controller D_c which fully checks the canonical grammar and rejects malformed strings; constructs the true source primal graph; runs the known **constructive** Korhonen 2023 single-exponential 2-approximation for treewidth at parameter k; verifies its output decomposition; then performs Boolean-semiring exact factor elimination and an original-source SAT witness check or a replayable complete zero-table UNSAT proof. If no decomposition is found, it reports UNRESOLVED internally and uses exact exhaustive fallback. On every valid input F with tw(G_F)≤k(N), this whole process, including discovery, source/index/head access, proof output/checks, failed trials, optional SAT witness construction and simultaneous live workspace, takes N^{O_c(1)} deterministic bit work and N^{O_c(1)} writable peak space. On arbitrary valid originals it remains correct but can take exponential work.

**Proof.** Korhonen's published algorithm either certifies tw>k or outputs a decomposition of width at most 2k+1; on tw≤k it succeeds. Its 2^{O(k)}n executable work is fully charged as a subroutine, not treated as an oracle. Clause-variable triples form cliques in the primal graph and therefore occur in certified bags. Exact Boolean variable elimination uses tables with at most 2^{2k+2} rows and polynomially many bag transitions; zero-table replay checks UNSAT, and paid backtracking followed by source-clause evaluation checks SAT. Converting standard graph-algorithm word operations into indexed bit-machine instructions costs polynomial overhead. Since k=26+O_c(log N), total work and peak live space are polynomial for fixed c. The fallback is correct by induction on the strictly decreasing number f of unpinned source variables, even if delta rises. The complete work recurrence charges EVERY evaluated OR/AND child, trial, cache and guest. This is a RESTRICTED polynomial island and says nothing about N^{6/5} time with N^{1/2} simultaneous peak space.

ARC219 ALREADY used Bodlaender et al.'s paid 5-approximate treewidth algorithm; the present transfer uses the later verified 2-approximation and connects it to the newly exposed greedy-width counterexample. No new general treewidth algorithm is claimed.

## Explicit connected family with primal width at most 26
Let V_i contain the nine original variables in block i of the previously authenticated connected cyclic F9-splice family G_t (t≥2). Replace in each F9 block the positive clause (x1_i OR x5_i OR x6_i) by (x1_i OR x6_i OR x5_(i+1 mod t)). Every source variable still has exactly two positive and two negative occurrences and every original clause remains proper, monotone and duplicate-free. For i=0,...,t−2 choose path bags
\[
B_i=V_0\cup V_i\cup V_{i+1}.
\]
All internal and cross clauses, including the last-to-first wraparound, occur in a bag; bag-occurrence positions of each variable are consecutive. Bags have at most 27 variables, so **tw(G_t)≤26 for all t**, and Lemma 1 applies to every coherent pinned residual. The ONE generic paid FPT selector therefore gives polynomial total decision work for all such sources/residuals with no G_t-specific name recovery or free semantic quotient. This is a concrete counterfamily to any compulsory 3^nu work claim, not evidence against worst-case SAT hardness.

## Full charged recurrence, accounting and finite evidence
For every actually executed residual z,
\[
W(z)=C_{\mathrm{grammar/source/index/head}}(z)
 +\sum_{\pi\in\mathrm{attempts}(z)}C_{\mathrm{acquisition/selection/switch/failure/proof/GE/cache}}(z,\pi)
 +C_{\mathrm{output/guest}}(z)
 +\sum_{y\in\mathrm{evaluatedSucc}(z)}\left(C_{\mathrm{child/bit}}(z,y)+W(y)\right).
\]
Simultaneous peak counts retained ancestors, index/head tapes, graphs, tables, certificates, caching and guest DELAY/COPY/RECOMP; logical XOR is OFFLINE unless paid. f decreases on each recursive pin child but neither f nor source treewidth bounds the NUMBER of OR descendants. For the successful width terminal there are no recursive descendants and total work is polynomial; otherwise exact fallback can be exponential.

Producer: F9 root 70 SAT models (UP-DPLL 5 nodes), F9 pins x5=x7=0: 13 (3 nodes, greedy closed width 6 versus optimum 5 over all 5,040 orders); SAME F9 original SAT pin cube 2 models (1 node), UNSAT pin cube 0 (1 node); Y6 root 20 (4 nodes); SAME canonical connected G2 original A/Z residual 2377 SAT (9 nodes) and B/Q 0 UNSAT (1 node). Explicit path bags checked t=2,3,4,8,16. Independent **NO producer import** verifier replayed every factor elimination table, the output SAT witness and zero-table UNSAT result, and passed **17,765 counted assertion groups**: 376 original-clause SS/SU/US/UU modes, 6,656 complement identities, 5,772 explicit ordering evaluations, malformed parsed-source controls and global sign/name-renaming controls. Source/table operation counters are proxies, NOT native FLMV measurements. Prior U198 UNSAT/V198 SAT certification is inherited, not freshly rerun. The compact published reproducer and raw summary are complemented by a local full producer, independent verifier, raw table JSON and PDF/TeX archive.

## Corpus and literature audit
Project GitHub searches: "treewidth 2 approximation", "Korhonen", "logarithmic selector" in j15marti/pnp; original ARC219/220 confirms prior 5-approx transfer. Separate github.com/openai search: "treewidth SAT" found mathematical material but no source-authenticated general SAT compressor; no novelty claim from search absence. Primary literature web queries: "Korhonen A Single-Exponential Time 2-Approximation Algorithm for Treewidth", "treewidth exact algorithm 2^{O(k)} n", "FLMV time-space lower bounds for satisfiability". Primary citations: [Korhonen 2023](https://doi.org/10.1137/22M147551X); [Bodlaender et al. 2016](https://doi.org/10.1137/130947374); [Döcker 2019](https://arxiv.org/abs/1912.08032); [FLMV 2005](https://doi.org/10.1145/1101821.1101822). Re-read AGENTS/CODEX/pnp-research, the 01:48 integrated handoff, delta-zero theorem, the latest five-agent reports and issue #3. **No novelty is claimed for classical bounded-treewidth DP, the original G_t transfer method, or the FPT graph algorithm.**

## Remaining load-bearing gap
No polynomial aggregate-work selector on ALL canonical target originals; no hereditary unknown-K arbitrary-A→Phi(A) power-short compiler; no strict numerical same-machine FLMV transport. External review pending. Exactly five existing task identities, states, schedules and ownership preserved. **P versus NP OPEN.**

END_OF_VERIFIED_REPORT::LSPV-1::PAID_LOGWIDTH_SOURCE_HEREDITY313::P_VS_NP_OPEN