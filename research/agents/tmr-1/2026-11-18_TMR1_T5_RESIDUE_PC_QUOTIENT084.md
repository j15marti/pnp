# TMR-1/084: source-authenticated five-residue path consistency, forced-offset quotient and exact forest recovery

Date: 2026-11-18 America/Los_Angeles. Owner: TMR-1 / PNP Machine Model Lead. Status: PROVED positive source-preserving theorem; prior-art-aware (path consistency is classical); finite tests COMPUTATIONAL; independent review OPEN. **P versus NP OPEN.**

## Canonical source, verification, classification

The fixed digraph template is the five-symbol tournament on Z5 with R(a,b) exactly if (b-a) mod 5 belongs to S={1,3}. The complete canonical source word is 1^n 0 1^m 0 followed by m lexicographically sorted distinct directed endpoint pairs low-bit first at width w(n)=max(1,ceil(log2(max(2,n)))). L=n+m+2+2mw(n). Witness x is exactly 3n bits, low-bit-first code 0..4 at each variable. Loops and opposed arcs are syntactically valid but semantically UNSAT; malformed source/witness codes are INVALID. Output must refer to the authenticated input, not uncharged derived promises.

Bang-Jensen, Hell, MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3), 281-298 (1988), DOI https://doi.org/10.1137/0401029, prove NP-completeness for semicomplete targets with >1 directed cycle. T5 has distinct all-+1 and all-+3 Hamiltonian directed cycles. This confirms NP-completeness independently of the exact parsimonious C5-to-T5 reduction /080.

## General exactness theorem: all-pairs five-residue closure (C1-T5-RESIDUE-PC-QUOTIENT084)

For each ordered vertex pair (i,j), maintain a 5-bit set M_ij of possible differences (x_j-x_i) mod5. Initialize M_ii={0}; for a source arc i->j intersect M_ij with S={1,3} and M_ji with -S={2,4}; all other masks begin Z5. Repeat, for all triples i,j,k,

 M_ij <- M_ij ∩ (M_ik + M_kj),

where A+B is the modular sumset. Reject if any mask empties; otherwise stop at a fixed point.

**Theorem.** Every satisfying input assignment is preserved exactly throughout closure. If closure rejects, the original instance is UNSAT. If closure succeeds, impose every singleton equation M_ij={d}, i.e. x_j=x_i+d mod5. Quotient by a weighted union-find or direct representative-offset calculation, retaining only projections of the ORIGINAL arcs and intersecting resulting parallel quotient masks. There is an exact bijection between original T5 satisfying assignments and assignments to the resulting masked-difference quotient (by deterministic affine lifting). Neither procedure assumes a supplied gadget decomposition. This gives a source-authenticated *parsimonious preprocessing*, not a general SAT solution.

**Proof.** Every input solution obeys all initialized masks. If x_j-x_i is in M_ij and x_k-x_i in M_ik and x_j-x_k in M_kj, then x_j-x_i=(x_k-x_i)+(x_j-x_k) mod5; hence no true solution can be deleted by the rule. Termination follows because at most 5n² mask elements can be deleted, each full pass either deletes one or stops. For a nonempty fixed point, each singleton is a logically forced difference. With a chosen representative r of each singleton component and offset δ_i satisfying x_i=x_r+δ_i, an arc u->v becomes (x_[r(v)]-x_[r(u)]) ∈ S+δ_u-δ_v. Intersect duplicate quotient constraints, test internal arcs against 0 and lift uniquely. Thus counts, satisfying assignments and witness decoding agree exactly. Materializing all nonsingleton inferred pairs is NOT required, and can fabricate spurious graph cycle rank; only source arcs are projected.

A naive sequential 5-bit-mask implementation makes O(n³) constant-size sumset operations per pass and at most 5n² nonstationary passes. Parsing, indexing, mask arithmetic, weighted quotient, sorting, polynomial big-integer exact forest counting and output fit conservatively on one deterministic bit machine in *simultaneous* T=O((L+1)^7) time and writable peak space O((L+1)^3) for the restricted case where the quotient is a forest. Closure and quotient alone meet these bounds on arbitrary valid inputs. If the quotient forest has c components and masked edges e, then exact counting is 5^c times the product of the sizes of its edge masks; a witness is recovered by forest traversal. This is a matched upper bound, not a deterministic lower bound.

## Strong structural example: reprocessing /083 without any annotations

The prior girth-five block has internally disjoint terminal paths whose edge orientations are ++, +++, ++-, and either +++ (YES) or --- (NO). These paths have exact endpoint-difference supports:

 ++ -> {1,2,4}; +++ -> {0,2,3,4}; ++- -> {0,1,3,4}; --- -> {0,1,2,3}.

Already the first three paths intersect in the singleton terminal difference {4}. The fourth +++ permits 4, whereas --- excludes 4, giving a sound unsatisfiability certificate for each NO block. For a YES block with x_s=0, terminal x_t=4; the two +++ interiors are forced to (3,1), and the ++- interior to (1,2). Only the middle vertex of the ++ path remains free, with two possibilities (1 and 3). Path consistency enforces these facts by repeated length-two sumset composition, even though the underlying graph has undirected girth five and no /082 local triangle/diamond shortcut.

For a chain of k all-YES blocks, *without supplying the block decomposition*, singleton quotienting identifies all 7k+1 pinned vertices into a common translated root class and leaves exactly k independent two-choice classes. Projecting ONLY original arcs gives a masked star/forest with k+1 vertices, k edges and feedback rank zero. Its exact count is 5·2^k. An otherwise identical chain containing any NO block is rejected. The original source graphs have n=8k+1, m=11k and feedback rank 3k. This proves that girth five, no small shortcuts, mixed YES/NO, noncactus topology and linear source cycle rank still fail as a universal computational obstruction, even when no gadget layout is supplied.

## Reduction control and limits

On /080, every five-arc edge gadget is also automatically contracted: an input undirected edge becomes one quotient edge with ±1 endpoint difference, the exact C5 adjacency constraint. For source C5, the produced T5 graph has 20 vertices, 25 arcs and a 5-vertex, 5-edge quotient. For source K4, the same compiler gives 22 vertices and 30 arcs and closure itself returns UNSAT. These are exact positive controls. **This does not imply closure decides all T5 instances**. The resulting masked quotient can retain arbitrary NP-complete C5-coloring, and no polynomial-time general decision theorem follows from its partial reductions. All other algorithms remain permitted, including polynomial local consistency, algebraic/Fourier, Gaussian, treewidth, compact representation and arbitrary source-aware decision procedures. NP-completeness is not a superpolynomial time lower bound.

## Executed finite audit, exact scope

Full independently executable local program /mnt/data/tmr1_t5_pc084.js, SHA-256 6fdd203273b03f4ec927b59d1c50070c9a1ae4f478a75daf4971b98bd7b479ce, raw output /mnt/data/tmr1_t5_pc084_raw.json, SHA-256 b92576da940c196c3015a7a319e575730ec4bb5cc26d8f80551b7431609b9ec4. Deterministic Node.js test checked all 729 simple oriented digraphs on four vertices (three arc states per unordered pair), 128 fixed-seed oriented digraphs on five vertices, loop/opposed-arc semantic checks, malformed canonical strings, all YES and NO chains for k=1,...,6, and the C5/K4/one-edge five-arc reduction controls. 874 closure cases, 7,258,175 brute-force candidate assignments enumerated, **349,644 assertions and zero failures**. Brute-force compared the exact satisfying assignment sets before and after all-pairs masks and verified exact forest-quotient counts whenever applicable. These tests are COMPUTATIONAL; arbitrary-size claims rest on the symbolic argument.

Published narrower certificate /experiments/tmr/tmr1_t5_pc084_certificate.js was executed separately: 12 YES/NO chain examples with k<=6, checking each vertex's exact singleton/two-valued difference mask relative to root; 207 assertions, zero failures. The narrow certificate does NOT independently redo all brute counts or canonical malformed-source controls; those belong to the local full verifier. This difference in scope must remain explicit.

## Scientific gates and handoff

DISJ: restricted positive algorithm and obstruction counterexample only. Relativization: positive algorithm is relativizing, P-vs-NP lower-bound promotion OPEN. SAME_REALIZATION/DTISP: time and writable space simultaneously charged on one sequential deterministic bit machine, no forbidden lower-bound pair. Configuration counting: applies only to the positive upper resource budget; no static graph-rank or configuration-count necessity theorem.

NEXT: C1-T5-RESIDUAL-HIGH-ADHESION-PC-AUDIT. Benchmark source-authenticated mixed satisfiable/unsatisfiable instances after full five-residue consistency and singleton quotient, then exact Fourier/separator/treewidth and generic search, and report genuine failures of the cheap paths. Do not infer mandatory work from hardness of the template. Preserve TMR-1 manuscript, ownership, draft PR and existing hourly agents; no creation, disabling or rescheduling. Full LaTeX compilation, independent kernel replay and mathematical review OPEN. **P versus NP OPEN.**
