# Strict-C witness run 3: fully pinned common-anchor CSP is exactly reducible to 2-SAT

**2026-11-19 Pacific. Status: PROVED restricted, COMPUTATIONALLY VERIFIED 16,307 executions, OPEN general strict C / P vs NP.** No claim of a new P4 link graph: the user's November 18 strict research PDF already records the four-vertex path.

## Canonical predicate
Colors Z5, R(a,b) iff (b-a) mod5 in {1,3}, C(a,b,c) iff either directed 3-cycle orientation. Three different variable **names** per physical clause, repeated colors permitted. 30 of 125 value triples accepted. Independent GF5 check: C(a,b,c) iff (a-b)^2+(b-c)^2+(c-a)^2 = 1 mod5, on all 125 triples.

## Theorem A: common-anchor criterion (PROVED)
For every unpinned source F = AND_e C(a,u_e,v_e) with one named variable a occurring in EVERY physical clause, form a graph G on remaining variables with undirected edges u_e v_e. Then F is SAT iff G is bipartite. Necessity: for an anchor color t, C(t,u,v) forces R(t,u) XOR R(t,v)=1, hence a graph 2-coloring. Sufficiency: choose a=0 and give the two sides colors 1,2; C(0,1,2) is true. A sourced odd follower cycle is an original-C UNSAT certificate. Unused variables are unrestricted.

For odd L>=3, H_L = AND_{i mod L} C(a,v_i,v_(i+1)) is physically clause-minimal UNSAT. Its L deleted-clause sources are SAT with a fully constructed witness necessarily falsifying the missing original clause. H_L has L+1 named variables, L clauses, incidence cycle rank L, and incidence girth 4. Thus large feedback rank alone is no hardness witness.

## Theorem B: arbitrary pinned source (PROVED)
For every original-C common-anchor source with n indexed variables, m clauses, and every arbitrary partial assignment p:V'->Z5, there is one **deterministic complete two-polarity** source-uniform algorithm that outputs either a full pin-respecting SAT witness verified against ALL original C clauses or a verifiable UNSAT certificate. All source parsing, all failed phases, full output and certificate paths/replay are charged. Complexity O(n+m) indexed RAM word time, O(n+m) writable words; O((n+m)log(n+m)) bits including pointers/indices. On non-anchored sources return UNKNOWN rather than a possibly incorrect polarity. Arbitrary string labels can require O(L log L) canonicalization, depending on input model.

**Proof and construction.** Find anchor by intersecting the three candidate names of the first clause with all others. Build follower graph; odd cycle => UNSAT. Otherwise enumerate every permitted anchor value t in Z5 (one if pinned, else five). The anchored link is a path P4 on colors t+2--t+1--t+4--t+3. For each connected bipartite follower component, try its two parity phases. A vertex on one side has Boolean choice from {t+2,t+4}, the opposite side {t+1,t+3}, or swapped. Every follower edge permits precisely THREE of the FOUR endpoint Boolean choices. Its single forbidden pair is one binary 2-CNF clause. A pinned variable gives a Boolean unit clause or outright domain exclusion. SCC-based 2SAT then solves each phase exactly. Components are conditionally independent after t, so no exponential product of their phases is needed. If all components can be solved, lift letters and verify original C. If for every t one component rejects both phases, output at most ten branch-failure certificates: a physical pin-domain exclusion or two source-tagged contradictory implication paths x=0=>x=1 and x=1=>x=0. The independent checker reconstructs every forbidden Boolean choice from the original quadratic GF5 predicate and validates all paths and color coverage.

This is NOT the historical Q exact-one XOR pinned-2SAT theorem. No S/C gadget substitutions are performed.

## Falsification controls
Pinned bare bipartiteness is insufficient: C(a,u,v) with pins (a,u,v)=(0,2,3) is UNSAT despite the one-edge follower graph being bipartite. The 2SAT phases certify this.

Two anchors are not enough for the same implication: C(0,1,2), C(0,2,3), C(0,2,4), C(1,3,4) is a physically clause-minimal UNSAT source (every one-clause deletion SAT). The four full witnesses after deleting clauses 0..3 respectively are (0,2,4,1,3), (0,1,4,2,3), (0,1,4,3,2), (0,1,2,1,1). This is a relabeling of the native Type-1 control already described in the user's 2026-11-18 strict research PDF, NOT a claim of novel counterexample. The common-anchor specialist correctly returns UNKNOWN.

For each t>=2, encode K_(t,t) with a common anchor a and physical clauses C(a,u,v). Treewidth of primal graph >=t, yet the solver is O(t^2). Adding one same-side follower edge yields an easy UNSAT control with the same unbounded treewidth. These are low-incidence-girth noncritical controls; no lower bound follows.

## Executed and independently replayed results
- 16,307 full solver/certificate executions: 6,531 SAT, 9,774 UNSAT, 2 UNKNOWN, zero mismatches.
- All 1,098 distinct simple unpinned anchored sources for n=3..6 cross-checked by exact 5^n brute force: n3 SAT/UNSAT 2/0; n4 7/1; n5 41/23; n6 376/648.
- All 10,368 pin patterns for all eight n4 simple anchored formulas, independently exhaustive (4,182 SAT, 6,186 UNSAT).
- 4,700 seeded pinned sources under random variable relabeling and clause shuffling, n4:600, n5:1800, n6:2300. Seed 202611190540; all original C replay and independent status agreement.
- 125 H-e witnesses on L=3,5,11,101 (all deletions) and L=1001 (5 selected). Each removed clause checked false and retained clauses true. Every H itself checked UNSAT by source odd-cycle certificate.
- Matched SAT/UNSAT K_(t,t) controls for t=5,20,50,80, max 161 variables and 6401 original C clauses, arbitrary randomized labels.
- Prior native strict C critical source, 25 variables / 25 clauses / incidence girth8 (earlier research archive): unsupported status UNKNOWN, and 25 full deletion witnesses independently replayed against 625 original C truth evaluations. All designated false, all 600 retained true.

**Reproducibility:** Complete working Python 3 source anchored_solver.py, independently coded original-GF5 independent_audit.py, 16,307-test results.json, original physical samples/complete witnesses, mathematical REPORT.md, HANDOFF.md and SHA-256 manifest are included in conversation file T5C_Anchored_Pinned_Exact2SAT_Witness_20261119.zip; archive SHA-256 9f8fc59a1e00eb89bba765aa2b539031e7bdc922b09a8177914d0e9b488ee07d. Run python3 independent_audit.py, standard library only. Python runtime is empirical, not a model-independent space theorem.

## Exact resource and completeness firewall
On authenticated literal shared rows R<=N^.195 and B<=N^.65 blocks with *encoded length* <=N^.35, each local child remaining common-anchored after pins, and a fully charged O(N) per-row stream/index access, exact two-polarity children run in O(N^.35) words, so a conditional full row/block scan costs O(N^1.195) word time and O(N^.35 polylog N) live bits for local materialization. This DOES NOT establish those promises for arbitrary strict C, source indexing for general layouts, a compressed global cover, or unrestricted P-vs-NP lower bound. Prior hard resolution and alternation-trading results are separate proof-system/model statements.

**Next falsifiable blocker:** classify the two-anchor strict-C pinned fragment and obtain a sound exact source-uniform solver or a certified incompatible obstruction. Avoid conflating shared-name anchors with S designated-head or Q XOR heads.

**Research context:** user strict research PDF (2026-11-18), p2 and p5-7; j15marti/pnp prior witness 2026-11-19 cycle-rank/TW30 report; Hell-Nešetřil 1990 H-coloring, Schaefer 1978 STOC 10.1145/800133.804350, Bodlaender 1996 SIAM J Comput 10.1137/S0097539793251219. P vs NP remains OPEN.