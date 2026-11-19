# Proof lead RUN3: Growing-boundary projection diversity and unrestricted-SAT firewall
2026-11-19. **P vs NP OPEN**. Independent finite audit and mathematical proof.

## Theorem A (PROVED, exact quantifiers)
For every integer q>=2, there exist **at least 7^(q-1) pairwise distinct nonempty D5-invariant projected relations** on q shared names z_0,...,z_(q-1), each definable as an existential conjunction of at most 7(q-1) original strict-C clauses on O(q) names with private names disjoint across factors.

Canonical predicate: R(a,b) iff (b-a) mod 5 in {1,3}; C(a,b,c) iff the three colors form either directed cycle. Exactly 30 of 125 color triples accepted, and every clause has three distinct VARIABLE NAMES.

Proof: For shared pair (z0,zi), there are three orbit classes E (equal), A (difference +/-1), B (difference +/-2). The native original-C gadgets:
- G_EA = C(z0,u,v)&C(z0,u,w)&C(zi,u,s)&C(zi,s,t)&C(v,w,t), 5 clauses, projects E union A;
- G_EB = C(z0,p,r)&C(zi,p,r), 2 clauses, projects E union B;
- G_AB = C(z0,zi,h), 1 clause, projects A union B.
Independent private copies and intersections produce E (7 clauses), A (6), B (3). The universal EAB projection is C(z0,u,v)&C(zi,w,t), 2 clauses. Hence all seven nonempty subsets of {E,A,B} have <=7-clause native realizations. Choose a mask independently at each i=1,...,q-1 and existentially conjoin its gadget with entirely fresh private names. The resulting relation accepts precisely those shared colorings whose pair orbit at every coordinate i belongs to its chosen mask. Two different mask selections yield distinct relations by selecting a pair orbit in their symmetric difference at one coordinate and satisfying choices at all other coordinates. Therefore 7^(q-1) distinct nonempty relations, all with <=7(q-1) clauses.

**Scope:** Every constructed relation has an O(q)-size product description, so this theorem proves neither superpolynomial certificate size nor machine-time complexity. It refutes only a constant-size three-orbit-type extrapolation to arbitrarily growing q. No girth or criticality claim.

## Theorem B (PROVED)
The number of orbits of q shared-color assignments under simultaneous D5 is (5^q+5)/10 for every q>=1. Burnside: 5^q identity fixed points, none for nonidentity rotations, one for each of five reflections. If an algorithm **explicitly enumerates one row per orbit** subject to R<=N^0.195, then q<=log_5(10 N^0.195 - 5). Larger q needs authentically source-verifiable *symbolic* row coverage, not just a row index.

## Experiment (COMPUTATIONALLY VERIFIED)
Deterministic Python, no random seeds. Original C and an independent unordered-consecutive-pentagon implementation agree on 125/125 tuples; 30 true. Original C invariant under all ten D5 transformations. All seven native pair gadgets' exact private extension counts and positive witnesses were exhaustively replayed independently. The full projected relation counts for q=2,3,4,5 were **7,49,343,2401**; D5 orbit counts for q=1,...,5 were **1,3,13,63,313**. Head projection exists h C(h,a,b) iff a!=b for all 25 pairs, NAE triangle gadget for all eight Boolean terminal tuples, and the two-NAE 3-OR decomposition for all eight Boolean truth tuples.

The original ten-name eight-clause critical UNSAT source was independently replayed with original-C physical deletion witnesses and counts **340,340,80,120,460,240,240,600**. An initially naive count for deletion of the last clause returned 120 rather than 600 because its unique variable h becomes isolated; the independent count must multiply by 5 for each such source variable. This **FALSIFIES** isolated-variable-ignorant model-counting, not the SAT status.

## SINGLE unrestricted SAT bridge; conditional resource transfer
Previously verified local indexed 3-CNF->native C reduction generates exactly 15+9v+39m variables and 10+7v+31m original C clauses. This run independently verifies its two semantic core primitives (3-OR through two NAE triangles, and graph edge inequality through one fresh-head C), not its entire indexed source compiler. Exact bit-level composition from the SAT model used in the lower bound into fixed-width indexed 3-CNF is the missing audit.

Buss-Williams (2015) Figure 8.3 explicitly confirms a 44-round, 406-triple alternation-trading refutation for SAT not in DTISP(n^1.34070,n^0.5). Williams (2006), Theorem 2.1 and Corollary 2.3, explicitly discuss near-linear polylog-workspace and bit-locally-computable reductions for SAT and 3-SAT. Therefore a uniform unrestricted, *same-machine-model* strict-C decider with n^1.33 time and n^0.5 space is incompatible with this known lower bound **if** the locally indexed reduction chain is fully certified. This simultaneous time-space exclusion is not P!=NP and does not automatically transfer to high-girth or clause-critical promise inputs.

For R<=N^0.195 rows, complete encoded child bit lengths L_j with sum_j L_j<=N^(1+o(1)) and maximum <=N^(gamma+o(1)), child complete time L_j^(a+o(1)), sequential child cost <=N^(1.195+gamma(a-1)+o(1)). At gamma=.35 the 1.33 endpoint needs a<=97/70, *plus* source access, row generation, both child polarities, failures, certificate acquisition/replay, output and peak-live writable space. A private-variable cap does not bound encoded length. Correctness requires SAT: EXISTS z FORALL j EXISTS x_j F_j(z,x_j), UNSAT: FORALL z EXISTS j FORALL x_j NOT F_j(z,x_j). A block index is not its refutation.

## Reproducible artifacts / next blocker
Independent Python scripts: lead_audit.py SHA256 6e25256250d6b9ab1c36e175f78cc219314dc4d2699a440905cf60276b198dba; independent_replay.py SHA256 f21590276eb3814d7ed5f803fbc24000419a620c68c3f762f482be2fdabac29c; audit_results.json SHA256 4563b2d545e742f4d38ba7427891c89f6551fb62a34ffafd27fb035a5303ab39. User-facing archive T5C_ProofLead_GrowingBoundary_Run3_20261119.zip SHA256 6a8aa0c49f0cffe9147804793d633bd24c27ce35d72ee48be2f5c4a379593637.

Reviewed actual repository LOCAL3COL_C_SOURCE_ACCESS_RESOURCE_FIREWALL and compact core/orbit cover reports, user's t5_strict_research.pdf pp. 1-3, and primary papers. ZIP package not retrieved in this run.

**Next blocker OPEN:** certify machine-model and source-bit adapter, then pursue full source-uniform all-z UNSAT obstruction acquisition beyond these easily factorized product controls. Independent static certificate for high-girth 149/168 control still missing.

References: Buss & Williams (2015), https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf ; Williams (2006), https://people.csail.mit.edu/rrw/sat-journal-final.pdf .
