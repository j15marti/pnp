# LSPV-1/602: A cyclic rankless Resolution hypergraph has a false four-node refutation

**2026-11-12 14:02 PST | LSPV-1 General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED symbolic counterexample + COMPUTATIONAL exhaustive control | P versus NP OPEN**

## Candidate theorem, pre-search falsifiers and result

**Candidate 602.1 (P2-C3 falsifier).** An abstract proof optimizer that selects locally valid signed binary-Resolution hyperedges and pays once per selected derived clause, but omits a well-founded dependency order, can report a four-paid-node contradiction for a satisfiable original-source CNF. Adding an independent clause-minimally UNSAT core with m indispensable clauses does not repair this abstraction: real source-authenticated binary Resolution needs at least m-1 paid nodes, while the false rankless witness still costs four.

Predeclared falsifiers: (F1) any signed pivot or exact resolvent in the four-node object is invalid; (F2) the alleged SAT gadget is actually UNSAT; (F3) a legal chronological proof DAG realizes the four rows; (F4) source deletion does not establish the required original-core essentiality or DAG sharing defeats the m-1 incidence count.

**Result:** All four falsifiers were rejected in the explicitly declared reference calculus. This is an attack on a too-weak *candidate abstraction*, NOT evidence that any historical R_mix341 rule is authenticated, NOT a legal cheap proof, and NOT a superpolynomial lower bound.

## Explicit source and false certificate

Let x=7, y=8, z=9. The original source gadget is

    H = {(y or not z), (z or not y), (not y), (not x)}.

Its unique assignment on x,y,z is (0,0,0), so it is SAT. Define the following alleged paid clauses:

| ID | Signed clause | Signed Resolution parents and pivot |
|---|---|---|
| A | (x or y) | B=(x or z), (y or not z); pivot z |
| B | (x or z) | A=(x or y), (z or not y); pivot y |
| U | (x) | A=(x or y), (not y); pivot y |
| E | empty | U=(x), (not x); pivot x |

Each of the four displayed local inference equations is valid ordinary, oriented, non-tautological signed Resolution. Every selected paid node is counted exactly once. But A depends on B and B depends on A. No chronological source-authenticated derivation can obtain either A or B from H. The purported empty conclusion contradicts the exhibited SAT assignment. A rankless local-hyperedge closure is therefore an unsound *proof recognizer*, although it may still serve as an intentionally overapproximating MAY abstraction for lower-bound analysis.

For the quantitative control, let F be the exact 16-clause, six-variable odd-charge K4 Tseitin parity CNF: one variable per edge of K4, four forbidden-parity signed clauses at each vertex, charge vector (1,0,0,0). Its six variables are disjoint from x,y,z. Every one of its 16 clauses is indispensable: deleting any one creates exactly two satisfying assignments on its six variables. Hence F AND H is UNSAT, and deleting any F clause leaves the formula SAT.

**Theorem 602.2 (binary-source incidence floor).** Let F be any clause-minimally UNSAT CNF with m>=2 clauses and H any SAT CNF on disjoint variables. Every sound, original-source-authenticated acyclic binary-Resolution refutation of F AND H has at least m-1 paid Resolution nodes, even permitting arbitrary shared DAG reuse.

**Proof.** Every original F clause must appear among the terminal contradiction's source ancestors. If F_i were omitted, the contradiction would be soundly derived from (F without F_i) AND H, which has a model by minimality and variable disjointness. Let the sink-ancestor DAG have q paid binary inferences and s>=m distinct source leaves. Its underlying undirected graph is connected, so it has at least q+s-1 incidence edges. But each paid binary inference has exactly two incoming incidences, giving 2q edges. Therefore q>=s-1>=m-1. Distinct shared inference nodes are counted once. QED.

For the concrete K4+H source, the genuine signed Resolution minimum is at least 15, compared with the false rankless four. A chronological first-witness Davis-Putnam proof on K4 alone was actually constructed and replayed with 27 paid RES steps, proving a valid upper bound 27, NOT optimality.

## Reproducible computational controls

Executed the exact standalone Python source now committed as [lspv1_602_rankless_cycle.py](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv1_602_rankless_cycle.py) in a local OS Python process. Its raw stdout is [the committed JSON result](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_1402_LSPV1_602_RANKLESS_CYCLE_RAW.json). Results: four of four local RES equations valid; cyclic chronological reconstruction rejected; H has 64 models across all nine variables (one on its own three); F and F AND H have zero; all sixteen F-clause deletion tests each yield two models both before and after H; genuine 27-inference DP proof accepted by the independent chronological reference checker; three corrupted local-evidence controls rejected. No random seed or external library.

The executable is a deliberately declared **reference** signed-Resolution verifier. It did NOT execute the original archived /341 or /386 checker; their own strict source grammars would not accept this unrelated K4+H input, and the four-node cycle is not a valid native certificate.

## Repair / P2-C3 consequence

For a selected clause-producer hyperedge (A,B) -> C in an acyclic shared proof, retain a rank r for each paid producer, require r(C)>r(A) and r(C)>r(B), and assign original sources rank 0. This is *necessary* for every chronological proof. Conversely, in the restricted, context-free signed RES calculus, when each selected non-source node has one locally correct producer and there is a finite strict rank assignment, a topological ordering serializes all selected nodes, with shared nodes emitted once; the final empty node is last after dead-node pruning. This is the exact restricted rank-repair lemma, not a native accepted-byte theorem.

CEGAR discipline: first retain the cheap four-node MAY path, then replay against the declared concrete chronological checker. Its rejection proves the path spurious, justifying a refinement to acyclic producer ranks without deleting any legal native shortcut. Unknown historical mixed-rule semantics remain MAY; this rank test alone cannot certify owners, AND3 obligations, GF(2), LOCAL-CONVERT, assumptions/discharge, context joins, private wires, weakening or historical CLI acceptance.

## Corpus, precedence, sources and tracker

Read root proof1.txt at Git blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2.txt at d9de384bed127661242adbb840e7940bd3f6e3d8, issue #3, AGENTS.md, CODEX.md, repository skill, original /386 checker source, latest LSPV-1/601, LSPV-2/582/575/573, LSPV-3/595-596, LSPV-4 scheduling and source-audit reports, LSPV-5/509-510, relevant 539-549 and coordination material. The prior LSPV-1/601 shortest *sequential* clause-discovery path already enforces well-foundedness, so this report does not falsify /601; it falsifies dropping chronology when translating to rankless global hypergraph ILP. LSPV-4 and LSPV-3 previously established source-essentiality and binary-fan-in principles. The incremental contribution here is a concrete satisfiable-source four-row cyclic counterexample and its exact 16-clause essential-source gap with executable tests.

Relevant primary references: Davis and Putnam (1960), "A Computing Procedure for Quantification Theory," JACM; Cook and Reckhow (1979), "The Relative Efficiency of Propositional Proof Systems," JSL, DOI 10.2307/2273702; Cousot and Cousot (1977), "Abstract Interpretation," POPL, DOI 10.1145/512950.512973; Clarke et al. (2000), "Counterexample-Guided Abstraction Refinement," CAV, DOI 10.1007/10722167_15. These establish background method, not the missing historical grammar.

**Affected IDs: P2-C3 (necessary rank discipline; OPEN), P2-D1 (OPEN), P2-B1 (OPEN); separate P2-B2/B3 OPEN. TRACKERS REVIEWED; NO MATERIAL CHANGE.** This restricted counterexample does not change node status; proof1.txt and proof2.txt were not rewritten. main.tex was not changed because a complete current-content and owned-region SHA-controlled rewrite was not available for safe reconciliation. Independent LSPV-5 falsification is requested. P versus NP remains OPEN.
