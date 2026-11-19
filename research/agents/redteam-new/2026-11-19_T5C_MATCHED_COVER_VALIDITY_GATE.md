# Strict-C red-team: coNP-complete symbolic-cover validation and a one-clause SAT/UNSAT pair
2026-11-19 Pacific | Independent adversarial audit | PROVED structural theorems, COMPUTATIONALLY VERIFIED finite controls; P vs NP OPEN.

## Theorem A: universal bare equality cover is coNP-complete
Canonical Z5: R(a,b) iff (b-a) mod 5 belongs to {1,3}; C(x,y,z) is a cyclic directed triangle in either orientation. C accepts 30 of 125 triples. All source clauses have 3 distinct variable NAMES; equal VALUES are allowed elsewhere.

For every u,v in Z5, exists a fresh head h with C(h,u,v) iff u!=v. For arbitrary simple graph G=(V,E), write the strict-C source F_G = AND_{uv in E} C(h_e,z_u,z_v), with independent h_e. Then:
F_G UNSAT iff forall z in Z5^V exists uv in E: z_u=z_v.
The natural source-indexed formula Phi_G(z)=OR_{uv in E}[z_u=z_v] can be printed in O(|E|) on SAT *and* UNSAT sources; it is not a certificate until its universal validity is proved. Deciding whether Phi_G is a tautology is coNP-complete: its complement is witnessed by a proper 5-coloring, and for arbitrary 3-COLOR source H, the join H with a new K2 is 5-colorable iff H is 3-colorable. This uses the classical NP-completeness of 3-COLOR. A polynomial-size, polynomial-time verifiable certificate for every such universal Phi_G would imply NP=coNP. No assumption that NP!=coNP is being made.

## Theorem B: matched original-C sources, exponentially rare SAT z
For k>=2, form k consecutive K6-minus-terminal-edge segments. Terminals t0..tk; each segment has four unique inner vertices, all 14 K6 edges except the terminal pair. This gives 14k common graph edges and 5k+1 shared graph variables.
Add ONE final edge, with a single fresh private C head:
- CLOSED = t0-tk. UNSAT and physically C-clause-minimal.
- OPEN = t0-a_last, where a_last is an inner vertex of the last segment. SAT, since this edge is implied by the common clauses and adds no new restriction.

With an indexed common-edge prefix, the sources share IDENTICAL FIRST 14k PHYSICAL C CLAUSES AND VARIABLE NAMES. Only final C clause differs. Both have exactly 19k+2 C variables and 14k+1 C clauses. Each segment's K4 interior uses four distinct colors, forcing both terminals to the same fifth; interior permutations are independent. Hence OPEN has exactly 5*(4!)^k = 5*24^k proper shared colorings out of 5^(5k+1), fraction (24/3125)^k. CLOSED has none. Every original C private head has a constructive completion from distinct endpoints. Each CLOSED physical clause deletion is SAT: deleting a segment edge permits a change of terminal color at that segment; removing closing edge directly permits all terminals equal. This is a restricted, recognizable family with incidence girth 6, NOT a growing-girth or general complexity lower bound.

## Executed independent controls
Two independently implemented strict C predicates: original R-based directed triangle and GF(5) quadratic identity, checked on all 125 triples. Original-C head projection tested on all 25 endpoint pairs. Complete/pruned graph coloring DFS:
 k=1: OPEN 120, CLOSED 0; 15 CLOSED deletion witnesses.
 k=2: OPEN 2880, CLOSED 0; 29 CLOSED deletion witnesses.
 k=3: OPEN 69120, CLOSED 0; 43 CLOSED deletion witnesses.
 k=4: mathematical counts OPEN 1,658,880, CLOSED 0 (not exhaustively enumerated).
In total 87 physical C deletion witnesses and 4 complete OPEN SAT witnesses were materialized and independently replayed: 91 full witness vectors, 3,058 original strict C predicate checks, every one of 87 deleted clauses false. Six incidence graphs for k<=3 have girth 6. All 15,625 z assignments of K6-e control checked, 120 proper.
Independent uniform random z sample seed 2026111909 (per-k seed +k): k=2 0 SAT rows /10,000; k=3 0/10,000; k=4 0/100,000. Exact probability of no hits in 100,000 k=4 rows is 0.99965216816. 1,000 sampled local blockers for each k verified false under all 5 head values.

Complete executable scripts + complete source/witness JSONL and raw results in locally created T5C_Matched_Cover_Validity_Redteam_20261119.zip. SHA256 audit_cover.py 9dc71053bfc369bde901e23623a571808f9d1fee7152d8880b420b98f7ec3d58; sources.jsonl 94870a107d27bf48dc2522d5cc0bb41c88eb6ca83f4d26ae0a5b4dd7528f503f; witnesses.jsonl 15277cf89d380c9de0872370f01ceb9ea314360ea007ff85eaadff652a1c13ec; results.json e3be54ebe09e911b24e371812fe574760921a51cdf9553add5068c02b74b9dff.

## Resource firewall
Per-row bad-edge selection is O(E) on read-only source + supplied z, but printing a symbolic equality disjunction is NOT checking forall z; random row coverage is not exact. One can group private heads asymptotically into O(N^.65) blocks of O(N^.35) size, but q=5k+1 shared variables require 5^q explicit rows, far beyond R<=N^.195. Full acquisition, source reads, both-polarity calls, failed branches, replay, proof checking, output and peak writable memory remain charged. Nothing shows an unrestricted n^1.33 time, sqrt(n) space solver or P!=NP.
Next blocker: source-verifiable proof objects for all-z covers on nonrecognizable growing-girth critical strict-C sources. New simple DNF certificates without a validity proof fail the gate.

Prior checked: existing repo equality-wire cover, S-to-C criticality counterexample, source-transfer lead, and Mycielski witness reports. User Library t5_strict_research.pdf pages 1-3 read; strict ZIP not recovered. Literature: Garey/Johnson/Stockmeyer TCS 1976 DOI 10.1016/0304-3975(76)90059-1; Buss/Williams Comput Complexity 2015 DOI 10.1007/s00037-015-0104-9, Fig 8.2 gives (epsilon,c)=(.5,1.34070) for model-specific SAT lower bound. No claim extends the lower bound to the restricted family.
