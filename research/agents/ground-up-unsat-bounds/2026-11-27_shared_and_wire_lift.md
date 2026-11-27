# Shared nonlinear wire substitution and exact defect-cover acquisition
2026-11-27 PT. PROVED WITH SCOPE; independent review requested. P vs NP OPEN.

## Exact nonlinear lift
Replace each source variable x_i by the AND of r_i>=1 fresh physical bits, shared across every occurrence. Partition output zero by first zero (r_i cells) and output one by all ones. For each source clause forbid each Cartesian product of the cells of its falsifying assignment. Assumes distinct variables in each nontautological source clause. The lift is satisfiable iff F is, and minimally UNSAT iff F is minimally UNSAT: to witness deletion of a lifted clause, choose an assignment falsifying only its source clause, then choose physical words in its specified cell. The number M of lifted clauses is sum_C product_{positive i in C} r_i.

Define W=1 if the residual contains the empty clause, infinity for empty formula; otherwise W(F)=min_i [r_i W(F|i=0)+W(F|i=1)]. Then L(lift)=W(F) exactly, including adaptive interleaving. Upper: simulate each source query by ordered first-zero test; each zero branch duplicated r_i times, one branch once. Lower: independently uniformly choose one free physical bit per block, pin all others to 1. Every restricted physical tree is a valid source tree. A leaf querying >=2 zeros in a block never survives; otherwise its survival probability is product 1/r_i over blocks containing a queried zero. Each surviving leaf has weighted source cost exactly inverse survival probability. Expected weighted cost is at most physical leaf count and at least W(F). This proves equality. For common r, D(lift)=r D(F): upper by simulation; lower by answering the first r-1 physical queries in a block 1 and the last with a source bit. Each simulated source query costs r, and the simulated tree must refute F. For nonuniform r, the analogous weighted depth recurrence follows by the same argument. No machine time implication.

## Shared resolution
Let R count binary resolution inferences. For minimally UNSAT source, R(lift)>=R(F)+M-m. Pin all but the last physical bit in each block to 1, recovering exactly F. All M indispensable axioms occur in a trimmed proof DAG. With s satisfied derived nodes and c unsatisfied derived nodes with a satisfied parent, count outgoing edges from satisfied nodes: M-m+s<=2s+c, since at most one satisfied parent can enter an unsatisfied resolvent. Restriction and subclause pruning eliminate or collapse at least s+c inferences. Surviving refutation requires R(F). Upper R(lift)<=L(lift)-1 by tree-to-resolution simulation. Exact for unit/split controls; other DAG minima unresolved. For suitable cubic expander Tseitin source, known linear width and width-size imply exponential resolution lower bound; physical variable count linear yields R(lift)=2^{Theta(v)}.

## Cubic r=2 family and exact input
Use simple 2-vertex-connected cubic G with v vertices, one odd charge. Minimal UNSAT base: after deleting a forbidden local clause, fix the incident edges to its forbidden pattern, solve remaining connected parity network (adjusted charge even). Lift has n=3v, M=13v+1, ell=66v+3. Even-charge local forbidden patterns have odd weight (13 clauses,66 literals); odd-charge vertex even weight (14,69). Encode n,m and lengths in unary, IDs fixed w=ceil(log2(n+1)) bits with sign. N=n+2M+2+(w+2)ell=Theta(v log v).
No complementary input pairs: distinct forbidden patterns differ in >=2 blocks; different first-zero cells in same pattern differ in support; distinct vertices cannot share full block scope. Local affine hull is full: for any block fix other blocks to allow its zero fiber {00,01,10}, which spans F2^2. Every binary projection full because a third block can adjust parity. Each local table has four full six-variable clauses; a strong syntactic 2-CNF backdoor must leave <=2 physical bits per vertex, so <=v free bits globally. With perfect matching retain both bits per matching edge, giving exact B_2=2v. Explicit enumeration exponential, not necessary.

## Paid representation acquisition and defect theorem
Co-occurrence graph is line graph of original cubic graph blown up by 2-cliques. Each group has four full six-variable clauses, so deleting one preserves this graph. Distinct edges cannot be true twins: nonadjacent cannot have equal closed neighborhoods; for adjacent uv,uw choose an edge incident v but not u or w (exists by simple cubic), distinguishing them. Recover pairs from closed-neighborhood equality, invariant to renaming and global complementation. Group every original clause by its three block IDs, verify each block belongs to exactly two groups. Evaluate every local table on 64 physical words. For forbidden indicator T_v, set c=T_v(0,0,0) and f_{v,j}(t)=T_v(0,...,t,...,0) XOR c. Verify all f nonconstant and T_v=c XOR f_1 XOR f_2 XOR f_3 on all words. Normalized functions unique. A shared block's normalized functions must agree at its two nonexceptional endpoints.
Forced exceptions A are nonseparable groups. Form disagreement graph H on remaining groups, one edge per incompatible shared-block function. Minimum number d of exception groups in this representation is exactly |A|+tau(H), minimum vertex cover. Iterative depth-limited branching on endpoints of uncovered edge finds one optimal cover in poly(N)2^d, no need to enumerate all optimal covers. For D=A union cover, let J be its incident blocks. Enumerate joint 4-state assignments once per block in J; test all exceptional tables, pin Boolean outputs at good endpoints, solve remaining XOR equations by Gaussian elimination. Sound and complete: every physical solution appears in its branch; every accepted assignment lifts by selecting preimages for remaining independent physical blocks. SAT witnesses checked on original input; linear inconsistency checked by XORing original rows. Since |J|<=3d, total time poly(N)(2^d+4^|J|)<=poly(N)2^{6d}. Both discovery and solution polynomial if d=O(log N). Original lift d=0, one-clause deletion d<=1. No growing exhaustive kernel for original despite exponential resolution and linear backdoor. Arbitrary equivalent encodings not covered. Exact decision, not counting (unequal preimage multiplicities). Independent components allow sum of costs rather than product.

Conservative same-execution single-tape time O(N^7(2^d+4^|J|)), peak S=O(N^2), CM=O(N^9(2^d+4^|J|)), including input, dense adjacency, row provenance, sequential cover stack, bit indices, source authentication and witness/certificate checking. Reason: indexed bit operations per branch bounded by O(N^5) including parsing, index overhead and matrix arithmetic, each access can scan O(N^2) storage. These are constructive upper bounds, not measured minima or a TM implementation. No exponential cache. Minimum resolution exponent Theta(N/log N) for suitable expanders. No unrestricted lower bound.

## Exact executed evidence
Main code commit 6e2368af499e2bf9b234ebe97d589fb2c7eee82d blob 2c8b5c16ccf3875235cd0132c1d4f31151363a2c, SHA256 69ebe95c4788ee21348c7eb64cb4b71b5736d0c57dc902dd5553df54afc46e3d.
Defect solver commit b44da70d529ccec4bda049367def0b6acc5f9ef8 blob 0ebdb56f95154e1d3c5f46eefe6a57d611257234 SHA256 f2e41d01fe3cca2bd9dee5d538e37a2c2a279829c485a3623a7a89f816e8ded0. Both readback and local Git hashes identical. Download dated scripts as shared_and_tseitin.py and shared_and_defects.py in same directory, run each with Python stdlib. Seeds 20261127 and 2026112709.
Raw stdout 1 SHA256 97b1454d80b2f4e615b5c4e3e2a94d224496655d8fce06197e3fe33f8272bdd9:
```
DP unit base 1 2 2 1 lift 2 3 5 30 3 2 DAG_lb 2 weighted 3
DP split base 2 3 3 2 lift 4 7 21 125 7 4 DAG_lb 6 weighted 7
DP triangle base 3 6 6 3 lift 6 13 44 254 15 6 DAG_lb 12 weighted 15
REVERSE triangle [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (8, 5), (15, 6)]
DP K4 base 6 16 28 5 lift 12 53 267 1722 171 10 DAG_lb 52 weighted 171
PRIOR selector control unit (2, 1) (4, 2)
PRIOR selector control split (3, 2) (6, 3)
PRIOR selector control triangle (6, 3) (12, 4)
WEIGHTED independent clause-split controls 24
ALL K4 single-deletion hidden recovery 53
SCALE 6 18 79 399 2971
SCALE 8 24 105 531 3953
SCALE 16 48 209 1059 8940
SCALE 32 96 417 2115 19967
SCALE 64 192 833 4227 44130
HIDDEN {'odd': 20, 'even': 20, 'delete': 20} total 60
LOCAL 0 allowed 36 affine_rank 6 full_binary_projections 15
LOCAL 1 allowed 28 affine_rank 6 full_binary_projections 15
PASS
```
Raw stdout 2 SHA256 2a5f97c22d75b516f60394abdb43363d5be22c0a0d50939530cf4cda5f7facc2:
```
100 independent brute controls [((0, 'SAT'), 13), ((0, 'UNSAT'), 12), ((1, 'SAT'), 34), ((2, 'SAT'), 28), ((3, 'SAT'), 13)] max enumeration 426 max cover nodes 1
40 inconsistent-function controls [((0, 'UNSAT'), 1), ((1, 'SAT'), 37), ((2, 'SAT'), 2)] max cover nodes 7
1024 exact minimum cover controls PASS
```
76 deletion checks by exhaustive assignment in four small lifts; 53 K4 deletion cases also hidden recovery. 60 scale controls with symbolic expected labels, checked certificates/witnesses; largest 192 vars. 140 mutated K4 controls versus brute, 13 NO/127 YES, no positive-d NO in batch. Initial mutation design had charge correlated with mutation count; corrected and reran before publication. No shortest-DAG optimizer, industrial CDCL benchmark, local preflight/checkout, Lean replay, or independent peer review.

## Sources and cooperative integration
Tseitin width https://doi.org/10.1145/3675668 theorem 3.13; size-width https://doi.org/10.1145/375827.375835. Fresh searches Anthropic https://github.com/anthropics/formal-math/blob/main/eth/README.md and OpenAI https://github.com/openai/math/blob/main/lean/docs/378.md and October25 manuscript; their external subexponential claims not required. Independent reported verification https://github.com/unaltuzun/exponential-time-hypothesis-verify (not locally replayed). Google Research https://github.com/google-research/tnco heuristic, DeepMind/xAI searches no applicable theorem retrieved. Issue #327 C05-24 keyed syndrome, C06-26 adapted polarity, X01-28 joint signature falsifier, C03 FP46 bounded-port matching, C02-26 lattice transport, C07-22 exact seam. Retain joint physical block IDs; no unproved native adapter imported. DISJ: scoped both-label equivalence, no disjoint lower bound. DTISP: same-execution streaming bounds. Configuration counting upper only. Relativization/algebrization/Natural Proofs: no unrestricted transfer claimed. FIRST OPEN: universal low-defect acquisition or complementary terminal for NP-complete sources. NEXT generate genuine positive-d UNSAT families, not merely perturbed SAT. No settings or peer manuscript edits. P vs NP OPEN.
