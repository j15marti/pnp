# T5-QBF LOCALITY36 | PNP Sigma2 Circuit Agent | 2026-11-18

Status: PROVED source-backed infinite-family existence and quantified private-head projection; VERIFIED K6 QBF controls; OPEN all-input lower bound, constructive growing-girth criticality and P vs NP.

## Source control and proposed mechanism
Loaded user-owned `T5_Exact_One_Experiments_2026-11-18.zip` (library ID `libfile_00b4599c2cfc8191a859b757dad101a0`). Executed its root verifier successfully: Q=60/125, P=20/125, 5-clause deletion counts 10/40/10/30/25, 236 Mycielski clause-deletion witnesses, 55,696 direct relation checks. Did not redo the completed 2,320-job matched grid or classify the exploratory UNKNOWN as UNSAT. Reviewed Sigma2 ADVICE-FIREWALL35. Proposed to remove private heads *existentially*, then test global 5-letter compatibility, quantified selector advice, and unbounded-girth critical obstructions.

## Theorem 36A (PROVED, existential infinite family)
For every integer g, a connected, intrinsically clause-minimal UNSAT T5 exact-one formula exists, with a different private head h_e in each clause Q(h_e,u,v), incidence girth >2g, and every subformula of at most g clauses satisfiable.

Proof: For the five-symbol tournament R(a,b) iff (b-a) mod 5 in {1,3}, Q(h,a,b)=R(h,a) XOR R(h,b). For a!=b, take h equal to the winning endpoint; for a=b, Q is always false. Therefore exists h Q(h,a,b) iff a!=b. Fresh distinct heads allow exact projection from Q-SAT to graph 5-coloring. Erdős (1959) proves for arbitrary g a graph G of girth >g and chromatic number >=6 exists. Choose an edge-inclusion-minimal H with chi(H)>5. Deleting every edge makes it 5-colorable; since one edge raises chromatic number at most one, chi(H)=6. Remove isolates; H is connected. Edge deletion preserves girth. Replace each edge with one private-head Q clause. Full formula is UNSAT, every clause deletion has a witness, and all head-parity tests pass. Its variable/clause incidence graph subdivides each H-edge and adds one private-head leaf, so incidence girth =2 girth(H)>2g. All <=g-clause subinstances are forests and SAT.

This is **not** an efficient construction or an asymptotic SAT-witness machine lower bound. The supplied 283-variable/236-clause Mycielski example has fixed incidence girth 8, not growing girth. The theorem rules out any *fixed finite* clause-subformula obstruction basis and per-head parity alone.

## Theorem 36B (PROVED, quantified advice firewall)
For a private-head graph K=(V,E), NON-5-COLORABILITY is equivalent to
`forall c in {0..4}^V exists i in [|E|]: c[u_i]=c[v_i]`.
Neither a 4-bit edge index nor an accepted individual response proves universal coverage. `exists i forall c` is false for every simple graph containing an edge (a candidate can color that edge differently). On one edge, `forall a!=b exists h Q(h,a,b)` holds while `exists h forall a!=b Q(h,a,b)` fails. The private-head elimination cannot hoist h ahead of the endpoint colors.

For K6 with 6 vertices and 15 edges, a uniform first-equal-edge selector scans <=15 original edges per candidate. Nevertheless every edge is essential to a **static** obstruction menu, because for each edge one 5-coloring of K6 gives that edge the only equality. Such a response program is easy; proving universal coverage is a separate claim.

To encode the QBF with 3 bits per universal vertex, guard invalid words 5,6,7: matrix `!AllValid(c) OR (i<15 AND Eq(c[u_i],c[v_i]))`. Valid prefix: `forall c_bits (18) exists i_bits (4), functional trace T (167)`. T depends on both c and i and stays after them.

## Executed finite controls (VERIFIED)
- K6: 6 graph vertices, 15 Q clauses, 15 private heads, 21 total T5 variables. Examined all 5^6=15,625 base assignments with 234,375 edge comparison positions; original Q is UNSAT. Each of 15 clause deletions has exactly 120 proper 5-coloring base assignments, and an explicit full 21-variable Q witness was checked. All original 15 edges are statically necessary. The count of full Q witnesses differs due to 2/4 head-extension multiplicity.
- Matched old P scopes: trivially SAT for arbitrary base graphs; assign every follower 0 and every private head 2, which beats 0 twice. Thus private-head P is an invalid hardness control for Q.
- Generated correct functional selector QDIMACS: 189 variables, 547 clauses, 7,022 bytes. Direct gate verifier tested 854 pinned choices and 467,138 gate-clause evaluations, including invalid color words. Separate QDIMACS parser/unit propagator tested 1,014 pinned cases (424 SAT, 590 UNSAT), with zero failures.
- Reproducibility bundle: `PNP_SIGMA2_T5_QBF_LOCALITY36_20261118.zip` contains full report, primary and independent scripts, QDIMACS, raw JSON with full deletion witnesses, technical handoff, source archive hash, SHA256 manifest. Source bundle remains available as original user-owned Library archive.

## Charged resource audit and limitation
For rows <=n^.195, blocks <=n^.65 per row and child size <=n^.35, full child scan under a hypothetical O(L^d) SAT seed costs n^(.845+.35d+o(1)) just in guest calls; the n^1.33 guest-only threshold requires d<=1.385714.... Source access, failures, materialization, replay, output and peak live workspace are extra. If all private children actually contain disjoint explicit n^.35 variables, the nominal source already has Omega(n^1.195) private variables; normalize all exponents to actual encoded input length N before interpreting bounds. N^.65 simultaneous offsets exceed N^.5 workspace; streaming needs explicit source-address and stack accounting.

FLMV (JACM 2005) random-access SAT deterministic rectangle excludes b<((c+2)/c^2-c)/2 =0.27626... when c=1.33, not b=.5; co-nondeterministic bounds concern the other polarity. McKay-Williams (ITCS 2019) TS near-quadratic witness-printing bounds do not transfer to critical T5 without a fine-grained resource-preserving source/witness reduction. A k-bit correct path is not a full strategy: deterministic enumeration charges 2^k replay, while the universal branching of a quantified proof must be covered or compactly proven correct. Wrong-path acceptance must be independently source checked. No P-versus-NP conclusion.

## Next handoff
Seek uniformly constructible connected edge-critical six-chromatic increasing-girth sources, with a verifiable source-preserving reduction and resource-charged criticalization, and test shared-head T5 compatibility after parity/small-core filters. Audit all proposed universal selector services using a correctness miter; charge any UNSAT call used to validate it. Retain sigma-primary ownership, schedule and independent red-team duties.

## Primary literature
[1] Erdős (1959), Graph Theory and Probability, https://doi.org/10.4153/CJM-1959-003-9 .
[2] Osthus, Prömel & Taraz (2001), Almost All Graphs with High Girth and Suitable Density Have High Chromatic Number, https://doi.org/10.1002/jgt.1017 .
[3] Fortnow, Lipton, van Melkebeek & Viglas (2005), Time-Space Lower Bounds for Satisfiability, https://doi.org/10.1145/1101821.1101822 .
[4] McKay & Williams (2019), Quadratic Time-Space Lower Bounds for Computing Natural Functions with a Random Oracle, https://doi.org/10.4230/LIPIcs.ITCS.2019.56 .
[5] Buss & Williams (2015), Limits on Alternation Trading Proofs for Time-Space Lower Bounds, https://doi.org/10.1007/s00037-015-0104-9 .
