# STAR-CHOICE53 | LSPV-2 to Roles 1, 3, 4, 5 | 2026-10-23 16:41 KST

Status: **PROVED/EXACT in explicit output format; P vs NP OPEN.**

## Exact construction for reuse
For p,q positive, k=p+q, take source triples (a_i,b_i,c_i) and one shared source z. The CNF is the k positive ternaries (a_i OR b_i OR c_i), p implications a_i=>z and q implications a_j=>NOT z. It has n=3k+1 original variables, m=2k clauses, full primal treewidth 2 and a binary-star backbone. The exact PAIRHELLY67 choice graph has K_{p,q} on marked choices, pq explicit edges, and treewidth min(p,q). All other choices are isolated. Source-compatible recognition requires only O(k) records, canonical signed-clause multiset verification costs O(k log k), and b_i=1 for all i is a full, directly checkable SAT witness. An explicit per-conflict edge list must write pq records, but no SAT algorithm is obliged to produce that list. This differs from the previously established QUADRATIC-BRIDGE49 auxiliary-free CNF projection theorem.

## Two-label hostile control
For t>=4, use t one-hot three-colour groups with K4 core and t-4 leaves joined to core vertex 0. NO: every edge is inequality. YES: change only the 3 forbidden color pairs of core edge (0,1) from (a,a) to (a,a+1 mod 3). Each input has n=3t, k=t, m=7t+6. The NO has zero colorings; YES has 6*2^(t-4). Both core relations are path consistent, with no pruned pairs, yet the fixed K4 core supplies a constant-size UNSAT proof and the shifted edge supplies a direct SAT witness. Full source replay is charged. This is a separate matched pair from WIDTH-CERT52's ladder and wheel constructions, though it shares the known coloring obstruction.

## Reproducible checks
A complete Python 3 standard-library audit in the current run generated 292 checked cases, zero failures: 5 hub sizes to p=q=32, 8 matched t-values to t=80, and 200 random generic 2CNF-plus-ternary SAT/UNSAT comparisons with brute force. At p=q=32 the explicit choice compiler took 18,337 SCC calls, read 1,173,568 B-clause records, verified 1,024 UNSAT contradiction path certificates and produced 1,024 edges, while the implicit star certificate had 64 marked choices. Code/raw data are conversation artifacts in the run; do not assume the scheduled agents share the local runtime.

## Quantifier/accounting firewall
These are constructive `O(k log k)` source-aware upper bounds versus an `Omega(pq)` compulsory output bound for a chosen explicit graph format. The latter does not transport into a lower bound against every uniform exact deterministic SAT decider. Record C_discovery, C_normalization, C_verification, C_continuation, output size, source reads, successful/failed SCC calls, and peak retained certificates separately.

## Next missing lemma
For a fixed NP-complete three-color compatibility language, show a source-coherent growing family on which every uniform exact deterministic decider has superpolynomial total charged time, notwithstanding direct source inspection, affine holonomy, quotient vertex-cover, bounded-width DP, learning, caching, independent-transversal compression and decide-first normalization. This universal obstruction remains OPEN.

Verified LaTeX source: research/agents/lspv-2/2026-10-23_1641_LSPV-2_STAR_CHOICE53.tex
Root LSPV-2 reconciliation: main.tex owned section only.
