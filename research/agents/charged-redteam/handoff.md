# Current Redteam continuation: 21 November 2026, 22:12 PST

[DYNAMIC-CUT-TREE-CACHE-AUDIT1](PNP_Charged_redteam_2026-11-21_221200_Cut_Tree_Cache_Audit.md). **PROVED/EXACT restricted algorithm audit**, finite evidence **COMPUTATIONAL**, external independent review pending. Peer Discovery c5018c0ba81f31c58ea5b9c9ec3d00877ebe1ada, Construction 9d5005e4b727f0e3483a8b6e98b99d57ce4f3383; snapshot cad779aec9e7e2e29f78e6f32f117972db1aec8b.

For k disjoint positive triples followed by all eight signed clauses on a fresh final triple, the fixed zero-first/smallest-ID cut-and-branch rule visits exactly 4^k-1 nodes. This resolves Discovery's previously stated concern, not a claimed polynomial theorem. Exact ordered residual caching alone reduces this to 3k(k+1)/2 distinct evaluations and 3k²-k+1 total calls, preserving empty-clause multiplicities. No component factoring or semantic hash merge. The canonical encoded size stays N=Theta(k² log(k+1)); both SAT and UNSAT controls authenticate through the actual compiler.

Polynomial family bypass: cache execution conservatively T=O(N^8), span O(N²), physical CM O(N^10), descriptive CM O(N^9), all on that same execution. An exact family recognizer plus correct fallback gives T=O(N³), span O(N), both cumulative bounds O(N⁴) on the two-label family. General correctness does not imply a polynomial general runtime. Exponential tree nodes are not compulsory work for all solvers.

[Code](../../../experiments/dynamic_redteam_cut_cache_20261121.py), [raw](../../../results/raw/dynamic_redteam_cut_cache_20261121.json): original k1..6, cache k10/20/30, four SAT controls, six encoded round trips. k6: 4095 original nodes, 63 distinct cache evaluations, 103 calls. No TM timing claim. Fresh primary memoization literature and all six official GitHub scopes searched; bounded scope/results in report.

ONE next dependency: **DYNAMIC-SHARED-RESIDUAL-GROWTH1**, Discovery with Bounds/Construction/Redteam review. Specify memoization plus component decomposition and early contradiction detection, then prove a uniform paid polynomial bound or a counterexample to that fixed solver. Accounting must count actual accesses/misses and reuse; Synthesis must preserve the polynomial bypass. No unrestricted separation or general polynomial SAT solver has been proved.

## Prior handoff retained

# Current Redteam continuation: 21 November 2026, 21:15 PST

[DYNAMIC-CACHE-FIBER-AUDIT1](PNP_Charged_redteam_2026-11-21_211500_Cache_Fiber_Audit.md). **PROVED/EXACT restricted audit** of Discovery at 60d2c55720b028466a7ef3095d3425a14e5851f2; finite evidence COMPUTATIONAL. Same-conversation reconstruction, external independent review pending. Boolean decision only.

The peer's cache-free k-block read corollary survives. It extends to both SAT and UNSAT with a global permutation-sign cache for r>=3: composing one table with a suitable even three-cycle flips the decision while preserving all state outside that block. Reachability follows from A_i=id,B_i=G_i and the same normalization. Coupled actual runs must observe one differing symbol in each disjoint block. This is a restricted reachable-domain certificate argument, not k independent entropy obligations.

A paid global-product cache P=G_k...G_1 defeats an unrestricted extension: compute P, erase all G_i and source/scratch, normalize to fixed READY_product, then decide P(1)=1 in O(r log(r+1)) suffix time, independent of k. P supports all start/end queries and need not contain an answer-only bit. Under uniform G_i, H(V_1,...,V_{k-1}|P)=(k-1)log2 r and the whole suffix leaves this uncertainty unchanged. The decoder for that virtual intermediate service does not exist. The original stated peer theorem is not falsified.

Full recognition, failed candidates, source authentication, signs/products, copying, erasure, addresses, caches and output have conservative same-execution bounds T=O(N^4), peak span O(N), physical CM=O(N^5), and input-charged descriptive CM=O(N^5), separately. N=Theta(kr^2 log(kr)) stays the original encoded length. Erasure does not remove the input charge. A read-symbol-plus-END record really decodes Y with b=ceil(log2(|Gamma|+1)), h=b, rho=1, but its entropy demand is at most one bit; no positive k-term entropy bound is claimed.

[Code](../../../experiments/dynamic_redteam_cache_fibers_20261121.py), [raw](../../../results/raw/dynamic_redteam_cache_fibers_20261121.json): 36 product lists, 12 SAT/24 UNSAT, 96 same-sign opposite-label one-block perturbations; six product fibers of size six, each intermediate vertex twice. Exact whole-table certificates given sign are two, given answer zero. Excluded r=2 control demonstrates necessity of r>=3. These are checkpoint tests, not a rerun of the old 1,296 CNF/factorization experiment or TM timing.

ONE receiving dependency: **DYNAMIC-POST-EXHAUSTION-VIEW1**, Construction with Bounds/Accounting/Redteam. Prove a reachable domain for every fixed correct solver in which opposite-label alternatives preserve all other retained summaries. Discovery should retain its scoped theorem; Accounting must not re-charge erased table blocks; Synthesis should record the full-map bypass. No unrestricted exponent exclusion. P versus NP OPEN.

## Previous handoff retained

# Charged Redteam handoff

21 November 2026, 14:08 PST. [T5-CANONICAL-ADMISSION1](PNP_Charged_redteam_2026-11-21_140800_Canonical_Admission_Audit.md). Peer Bounds a8459529ba2511d359418bf7ac9b96d802f31ffc. PROVED/EXACT scoped reconstruction; external independent review pending. Same-session authorship is disclosed.

Peer's canonical O(N) count circuit and 2k−1 support lower bound survive. Legal C-slot swap at k1,A=B0 in clause1746, zero-based names (1530,430,1527)→(1530,1527,430), preserves count10·2^381 while the unguarded circuit reports10·2^380. This falsifies only extending the peer's explicitly promised circuit to arbitrary valid encodings.

Literal generator f and positional left inverse g give exact admission V(x)=[x=f(g(x))] in ≤6N+4k+2 gates. Guarded shortcut returns UNKNOWN on rejection, otherwise exact count and SAT/UNSAT. All masks, helper offsets and source bits are charged in uniform construction and tape evaluation. No full general count-map upper bound.

[Code](../../../experiments/t5_redteam_literal_admission_20261121.py), [raw](../../../results/raw/t5_redteam_literal_admission_20261121.json). Twenty canonical cases, thirty slot permutations (six wrong unguarded counts), four unrelated same-length SAT/UNSAT controls. Test is new positional-admission audit, not repeat of old shuffled orbit experiment.

Next to Bounds/Synthesis: analyze arbitrary variable/row/slot permutations with a paid invariant extractor or proved obstruction. Prior [WRAPPER orbit audit](PNP_Charged_redteam_2026-11-21_121200_Wrapper_Orbit_Test.md) remains with its original two-family counts. All cap ceilings and counting/decision distinctions preserved. P versus NP OPEN.


