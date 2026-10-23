# REVERSE-SELECTOR57 Role-2 five-role handoff
Date: 2026-10-23 19:12 Asia/Seoul. P vs NP: OPEN. Evidence: restricted polynomial-time constructive methods, not a separation.

## To Role 1 (universal cost)
For proper exact signed (2 positive, 2 negative) 3-CNF, 4n=3m; the true-literal occurrence graph has 4n vertices, n disjoint K2,2 complementary-variable cycles, 4n conflict edges. Add m triangles for the clauses: 8n edges total, degree 4. Independent set size m iff SAT. Compact graph, degree 4, witness count and gate size do not force enumeration or a rich representation against every decider. Paired supports are solved in O(n^2), disproving mandatory exponential work from these invariants on the paired subfamily.

## To Role 3 (exact 2,2 transport)
Paired monotone proper grammar: pair each positive triple with identical negative triple, support nodes are a 3-regular multigraph and each variable a shared edge. Greedy maximal matching M; unmatched vertices U have all three neighbors among matched vertices W. Each W incident to <=2 U-neighbors, so Hall's 3|Z|<=2|N(Z)| guarantees injecting U into W through an augmenting-path matching D. TRUE variables are the edges of M union D, FALSE others. Every support node sees 1 or 2 TRUE variables, so both signed clauses true. A maximal matching need not be maximum. For t unmatched clauses, |S|<=3t, assign S and check NAE degree intervals on paired supports. Bipartite residual graph yields exact lower-bound feasible circulation; total 2^(3t) poly(N), fully charged. General-factor extension is literature-supported but not implemented. Recover true 198-variable exact(2,2) UNSAT appendix from Docker 2019 for independent audit.

## To Role 4 (red team)
Try to break pair recognition under repeated clauses, malformed supports, sign flips, aliasing and malformed source identifiers. Non-bipartite fully paired prism and K4 are SAT through matching. A naive edge orientation that yields different truth values at its two endpoints is INVALID because the endpoints share one source variable. The adversarial UNSAT clause-cube is proper 3-CNF but NOT regular exact signed(2,2); do not count as that class.

## To Role 5 (synthesis)
New algorithmic positive result is narrow, same-realization charged, and corroborates the literature that paired cases are easy. The known general exact(2,2) monotone class is NP-complete; unrestricted P=NP and P!=NP both OPEN. Main.tex was edited only in LSPV-2 region with verified readback. Existing MAIN85 two-class root quotient and MAIN64 exact source join remain correct.

## Reproduction/source ledger
Full audit locally as REVERSE_SELECTOR57/audit.py in linked user-facing ZIP, seed 202610231912. 353 assertion groups, 0 failures; exhaustive 74752 source-assignment checks through q=5; scalable paired q<=40 (n=120,m=160), 4,289,824 evaluated gates and 8,579,648 wire references; 36 nearpair branches/17 maxflow augmentations; 320 independent randomized 2-SAT brute controls. GitHub includes independently verified concise LaTeX report, minimal matching reproducer, and raw counted summary. Full per-case raw data lives in user-facing ZIP and is not assumed available on peers' local runtimes.
Primary literature: Janosch Docker, Monotone 3-Sat-(2,2) is NP-complete (arXiv:1912.08032); Aspvall-Plass-Tarjan 1979; Hall matching; Gabow/Sankowski 2013.
Original project sources: LSPV-4 PALETTE_SOURCE_CYCLE56, LSPV-1 PAIRHELLY67, TRACEFRONT1, ROOT_LABEL_QUOTIENT85, SMALL_INTERFACE_EXACT_JOIN64.

## First missing research lemma
Prove a useful general algorithm for exact (2,2) misaligned instances or a universally unavoidable symbolic cost, while allowing source rereads, direct decision, arbitrary caching and alternate representations. A forced representation-or-cost dichotomy has not been proved.
LSPV-2::REVERSE-SELECTOR57::HANDOFF-VERIFIED-END
