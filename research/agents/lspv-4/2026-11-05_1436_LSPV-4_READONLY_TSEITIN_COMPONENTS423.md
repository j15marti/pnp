# LSPV-4/423: logspace decision of authenticated Tseitin residuals with a read-only branch context

**2026-11-05 14:36 PST | Route A primary | PROVED/RESTRICTED (standard graph-algebra and Reingold) + COMPUTATIONAL controls | P versus NP OPEN.** Full expanded proof, producer, independent verifier and SHA256 manifest: `LSPV4_423_TSEITIN_READONLY_CONTEXT_REPRO.zip` in the contemporaneous automation attachment.

## IDEA first: exact hypothesis and adversaries

Hypothesis: for a source-authenticated cubic Tseitin 3-CNF and a *separately read-only* ternary assignment to its edges, residual SAT is decidable in deterministic logspace without a materialized graph or exponential cofactor cache. Tests: (F1) partial assignment destroys affine constraints; (F2) global even charge guarantees every cofactor SAT; (F3) implicit graph connectivity forces a full adjacency matrix; (F4) such a helper automatically yields the all-input FLMV contraction. F2 is falsified by the even cube four-edge cut (8 SAT/8 UNSAT), F1/F3 are addressed under the stated read-only model, and F4 remains an OPEN transfer and fails for an unchanged guest fallback (LSPV-4/417).

## Theorem: RESTRICTED deterministic L upper bound

Let G=(V,E) be a connected simple cubic graph with H vertices and 3H/2 edges. The canonical original source consists of *four distinct proper 3-literal CNF clauses* per vertex forbidding the wrong parity for its incident three edge variables: XOR_{e incident v} x_e = chi_v. The clause groups, edge occurrences, and dense variable IDs must be verified against the **original bytes**, not assumed from a model name. A separate read-only ternary tape provides alpha in {*,0,1}^E.

Set S={e:alpha_e != *}, G0=(V,E\S) and chi'_v=chi_v XOR (XOR_{e in S incident v} alpha_e). Then F_G|alpha is exactly the affine system B_{G0}x=chi'. For every component C of G0, the column space of its GF(2) incidence matrix is precisely the even-total-charge vectors (rank |C|-1). Hence

$$
F_G|\alpha\in\mathrm{SAT}\quad\Longleftrightarrow\quad
\forall C\in\operatorname{components}(G_0),\ 
\bigoplus_{v\in C}\chi'_v=0.
$$

Every adjacency query, residual-charge bit and canonical-clause check can be generated from repeated indexed original-source/context scans using O(log N) writable/index/head bits. By Reingold's 2008 deterministic logspace undirected connectivity algorithm, determine component membership without storing G0. Scan each vertex to find minimum representatives; then scan vertices again to XOR residual charges for each component. At most O(H^2) USTCON calls and polynomial source/index work; O(log(N+2)) all-phase writable space; one output label. This proves a **uniform special-family logspace decider**, not a logspace implementation of arbitrary SAT or an n^1.1-time algorithm. Reingold's theorem is the external dependency. SHA256 test hashes are evidence fingerprints, not a proof-soundness oracle.

## Sharing, branch contexts and full physical ledger

For a fixed assigned edge set S, the branch-label function is an affine component-boundary equation M alpha_S=u (previous LSPV-2/424). A shared binary branch tree can cache M and u once, but a dense c-by-|S| cache uses Theta(c|S|) live bits; a sparse list has O((c+|S|)log N) bits on bounded-degree graphs. If instead we recompute the component relation from **read-only** source+context, writable scratch remains logarithmic but may require polynomially many rescans. If alpha is constructed and retained as an arbitrary k-bit writable vector inside a compiler, that particular materialization costs k peak bits; no blanket lower bound on compact or readonly alternatives is claimed.

The ideal logical shared-DAG counts distinct legal inference nodes only once, but executed SAT machines pay source acquisition, index/head operations, policy discovery, false branches, guest reads, semantic comparisons, cache references, retention, recomputation, output and simultaneous ancestor contexts. UNSAT via explicit split is an AND of both assumed branches; cross-context reuse requires scope verification. No new case-split rule is granted to historical R_mix341. The one-label L-space helper does not create N^1/2-sized ordinary CNF guests, and its time exponent is unspecified. Therefore it supplies neither the all-input recursively iterable A -> Phi(A) nor rho,eta,lambda<=1/2 and no FLMV contradiction.

## Established family and theorem ledger

Cubic odd-charge Tseitin: H vertices, 4H original width-three clauses, 3H/2 edge variables, Θ(H log H) direct binary/ASCII length. Odd total charge proves source UNSAT, even proves SAT. On **suitable growing constant-degree expanders** Urquhart 1987 and Ben-Sasson/Wigderson 2001 give 2^{Omega(H)} lower bounds for **ordinary shared-DAG Resolution only**. This run's finite K4, cube, Petersen are source-format controls, not a certified infinite expander sequence. The existing historical R_mix341 mixed AND3+GF(2) shortcut gives 4H-1 paid inference nodes on bridgeless odd cubic sources, so Resolution hardness does not transfer to the full mixed calculus or arbitrary SAT machines. Haken PHP/ordinary Resolution and Cook Extended Resolution are distinct controls. Standard parity coding follows the actual CNFgen `cnfgen/families/tseitin.py` source.

## COMPUTATIONAL reproduction

The separately executable Python producer checked **2,310** partial contexts: 2,310 component-parity versus independent Gaussian-elimination agreements; 1,458 exhaustive K4 ternary-context versus brute-force Boolean comparisons; 479 original-clause-verified SAT witnesses; 1,155 odd-charge UNSAT residuals and 676 even-charge UNSAT residuals; 24 malformed source rejections. Cube cut: eight SAT and eight UNSAT branches on the even original; sixteen UNSAT branches on the odd original. Seed 4232105. Source sizes: K4 16 clauses/163 bytes, cube 32/340, Petersen 40/440 (per charge label). Independent Node code reconstructed all six original source SHA256s, exhaustively checked 1,458 K4 partial contexts, and verified all 16 cube-cut branches, rejecting forged branch-label records: **1,645 independent assertions**. Host Python/Node memory is materialized; these executions DO NOT measure an FLMV logspace machine.

## SEARCH and independent critique

Governing handoff: `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` blob c3889a3e; current issue #3; AGENTS.md, CODEX.md and pnp-research skill; LSPV-2/424 blob 95ed3931, /426 c7e4563e, /427 4694e28e. Actual external files: `GROKPROOF/2026-11-05_1913_PROGRESS.md` blob 8a004bf4 and `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob 1f9fc727. Neither supplies universal contraction.

Actual repository checks: `konard/p-vs-np/proofs/complexity/README.md` blob 7ee9a11e (finite one-tape rather than FLMV); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob 18d693ea and `PROJECTION_DISCOVERY_BARRIER_REPORT.md` blob a24f4fd (projection does not become a free tool); `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` blob 1ced21f4 (particular program's costs, not arbitrary callbacks); `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` blob 4bb5fd1 (established source generator). Indexed web searches included 'FLMV SAT indexed time space theorem', 'Reingold undirected connectivity logspace', 'Urquhart Tseitin resolution expander', 'branch caching SAT shared subcomputations', and both required new repos. Direct Google-branded search unavailable; indexed web substituted without claiming Google access.

Primary theorems: Reingold, JACM 55(4), 2008, DOI 10.1145/1391289.1391291; Fortnow--Lipton--van Melkebeek--Viglas, JACM 52(6), 2005, DOI 10.1145/1101821.1101822; Urquhart JACM 34(1), 1987 DOI 10.1145/7531.8928; Ben-Sasson--Wigderson JACM 48(2), 2001 DOI 10.1145/375827.375835.

## ITERATE and exact open arrow

Initial materialized graph/cached-branch view was replaced, using Reingold, by implicit adjacency plus repeated indexed scans on a *readonly context*. The even cube cut falsifies global-parity-only merging, while the odd charge demonstrates a legal algebraic shortcut bypassing the whole branch tree. **OPEN:** construct a both-label malformed-aware *all-input* uniform recursively iterable contractor, valid for every polynomial SAT decider on exactly the FLMV indexed machine, satisfying t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2) and strict finite FLMV entry. Route B B3 and P versus NP remain OPEN. No task, rule, weight, schedule, ownership or root manuscript changed.
