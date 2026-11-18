# LSPV-1 T5 critical-thread witness normal form | 2026-11-18

**Role:** GENERAL SAT LOWER-BOUND LEAD, historical role preserved. **Status:** PROVED/EXACT structural and algorithmic upper-bound lemmas; COMPUTATIONAL independent fixture audit; unrestricted SAT-only witness lower bound OPEN. **P versus NP OPEN.**

## Proposed mechanism and falsifiers

Candidate: exact contraction of degree-two threads reduces every *designated critical-edge deletion* from an intrinsically edge-minimal UNSAT T5 source to one SAT-only binary CSP on the branching core. Independent tests attempt to falsify it via (1) orientation/order-sensitive endpoint multiplicities, (2) different satisfiable-branch projections after deleting different edges of one thread, (3) degree-two threads of length four in a critical source, and (4) a branch assignment with no original-label reconstruction. None falsifies the mathematical claim. This is a source-aware **upper-bound control**, not an all-machine lower bound.

## Model

Colors are Z5; R(a,b) holds exactly when (b-a) mod 5 is 1 or 3. H is an explicitly encoded finite, simple, loopless oriented graph, connected and edge-minimal UNSAT. Input also specifies an original arc e, and G=H-e is promised SAT. The actual output is a full valid five-color label for **every original vertex**, not an advice bit or a proof of H's UNSAT status. A degree-two thread is a maximal internally degree-two u-v path between distinct branching vertices. Let B be the degree>=3 vertices, b=|B|, and let P run over threads.

## Theorem A: exact thread deletion and witness bijection (PROVED)

Choose a u-v traversal of a thread P of L arcs, r of which point backward. Its number of internal extensions for fixed endpoint colors a,b is

K_P(a,b) = sum_{j=0}^L binom(L,j) [ (b-a) mod 5 = (L+r+2j) mod 5 ].

For every original arc e in P, the remaining path splits into two trees rooted at its fixed endpoints. Every surviving arc has exactly two valid choices for the next vertex, regardless of orientation. Consequently **2^(L-1)** completions exist for every endpoint pair, independently of which of the L original arcs was deleted. For edge-critical H:

#Hom(H-e,T5) = 2^(L-1) sum_{sigma:B->Z5} prod_{Q != P} K_Q(sigma(u_Q),sigma(v_Q)).

Proof: write each traversal increment as 1+2z for a forward arc and 2+2z for a backward arc, with independent bits z. Summing yields L+r+2 sum z, and the binomial coefficients count the ways to realize a particular sum. After deleting e, the two rooted fragments have L-1 surviving arcs and two free child-color choices on each. Internal vertices of distinct threads are disjoint, so all extension counts multiply. Different deletion positions in P induce an explicit count-preserving bijection: fix all outside labels and terminals, enumerate the two child choices along the two rooted fragments in a canonical edge order, and use the same (L-1)-bit choice word for the other deletion position. QED.

**Critical normalization.** Edge-minimality of H is equivalent to UNSAT of its full thread-CSP and SAT after dropping *any one entire thread constraint*. Every edge deletion within the same thread has the **same projected feasible branching assignments** and the same total number of original witnesses. For critical H, all witnesses of H-e necessarily violate e itself.

This is a stronger exact search equivalence than an endpoint-support-only argument: for example FF has exact endpoint count vector [0,1,1,0,2], not 0/1 multiplicities.

## Theorem B: charged SAT-only witness extraction (PROVED)

Parse and validate H and the designated e; construct the branching core and the thread containing e by tracing adjacency lists, and retain all original vertex/arc identities. Since H is 2-vertex-connected, all core branches are in one connected graph; fix the first branch color to 0 using global Z5 translation. Enumerate at most 5^(b-1) remaining branch-color assignments. Check K_Q>0 for each intact Q != P. A passing assignment exists by the edge-critical promise. Complete each intact path with five-state DP/backtracking, and complete the two detached fragments of P-e by selecting one of the two valid child colors on every surviving arc. Verify all original remaining arcs and emit all n vertex colors.

For an indexed explicit n-vertex m-arc encoding a straightforward algorithm uses O(poly(n+m)+5^(b-1)(n+m)) word work, with additional charged logarithmic indexing/bit costs; O(n+m) RAM words including saved input and witness. Input parsing, promise-independent checks, construction, candidate testing, failure work, reconstruction, verification and output are included. The bit-machine bound is correspondingly polynomially larger, not claimed identical. No free SAT/UNSAT advice is used. This is a valid uniform **promised-SAT upper bound**, never evidence of witness-time hardness. Bounded-treewidth core DP and TMR-2/093 source-based GF(5) cycle-syndrome DP are competing shortcuts; their decomposition/acquisition costs must be charged.

## Theorem C: sharpened high-girth branch-core bounds (PROVED)

For girth(H)>g>=7, edge-minimality forbids any length >=4 degree-two thread: every endpoint difference would be feasible, so deleting one edge could not restore satisfiability. Each thread has at most 3 edges. Two parallel threads create an original cycle of length at most 6; therefore the suppressed branching core C is **simple**, with minimum degree at least 3. Writing q=|E(C)|, n=|V(H)|, b=|V(C)| and beta the undirected cycle rank,

n=b+sum_P(L(P)-1) <= b+2q <= b^2; hence b>=sqrt(n).
beta=q-b+1 >= b/2+1 >= sqrt(n)/2+1.

Every cycle of k edges in C lifts to an original cycle of <=3k arcs, hence girth(C)>=h=floor(g/3)+1. Applying the degree-3 Moore bound,

b >= M(h),  M(2r+1)=3*2^r-2,  M(2r)=2*(2^r-1).

Thus beta >= M(h)/2+1 and n>=M(h). These improve the earlier b>=sqrt(n)/2 bound for this higher-girth regime, but **size/girth/cycle-rank growth is not a computational lower bound**.

## Independent finite evidence

The standalone Python 3 stdlib audit reconstructs all 9 short endpoint supports, exhaustively checks all 2^9 subfamilies (63 nonempty irredundant; maximum size 4), independently computes exact cofactor multiplicities, and constructs an actual oriented critical fixture with 9 vertices, 11 arcs, two branch vertices and four threads BBB/FBB/FFF/BB. The source is 2-vertex-connected and has girth 5. Independent original-arc backtracking finds 0 models for H and SAT for all 11 H-e instances. Model counts by deleted thread: BBB 60, FBB 60, FFF 40, BB 180, exactly constant across positions of e inside each thread. Each H-e has an actual nine-color witness, checked against all 10 surviving original arcs; the removed arc is false. These finite checks support, but do not replace, the proofs.

**Reproducer:** experiments/arc/lspv1_t5_thread_deletion_20261118.py. The complete extended raw data and sample canonical original sources were also produced in the local dated review package. The historical branch-core archive named in the user handoff was not mounted; its nine-support/four-thread claims were reconstructed directly rather than relying on an unavailable file. External peer review remains OPEN.

## Hardness gate and next blocker

General T5 homomorphism NP-completeness (Bang-Jensen, Hell, MacGillivray 1988) and existence of arbitrarily high-girth edge-critical T5 UNSAT graphs do **not** establish the NP-hardness of the strictly promised class (H edge-minimal UNSAT, girth increasing, designated edge, G=H-e SAT). No polynomial-time criticalization map maintaining that promise and accounting for finding the critical edge has been proved here. Moreover the TMR-2/091 girth-six multi-theta SAT theorem and TMR-2/093 GF(5) syndrome evaluator are mandatory alternative source-aware solvers. No size-based, path-language, proof, circuit, or restricted-query bound has been transferred to all deterministic witness-search executions.

DISJ sanity: OPEN for any general lower bound. Relativization: no nonrelativizing step asserted. Simultaneous DTISP: OPEN. Deterministic configuration counting: NOT USED to infer a lower bound. Algebrization/Natural Proof barriers: no new all-machine claim. **Next task:** produce a fully charged uniform reduction into this intrinsic critical growing-girth SAT deletion promise, or derive a stronger complete witness algorithm by combining the core quotient with treewidth and the GF(5) cycle basis. Request independent LSPV-5/TMR peer falsification before any promotion. Leave every existing automation/role state untouched.

### Primary references and project corpus

[1] Bang-Jensen, Hell, MacGillivray (1988), SIAM J Discrete Math 1:281-298, doi:10.1137/0401029.
[2] Bodlaender (1996), SIAM J Comput 25:1305-1317, doi:10.1137/S0097539793251219.
[3] Ajesh Babu, Radhakrishnan (2010), arXiv:1011.1058 (Moore bound).
[4] TMR-2/091 https://github.com/j15marti/pnp/blob/main/research/agents/tmr-2/2026-11-18_1212_TMR2_T5_BICYCLIC_TRANSFER091.md
[5] TMR-2/093 https://github.com/j15marti/pnp/blob/main/research/agents/tmr-2/2026-11-18_1412_TMR2_T5_CYCLE_SYNDROME093.md
[6] Cross-track/55 https://github.com/j15marti/pnp/blob/main/research/agents/cross-track/2026-11-17_2332_T5_CRITICAL_GIRTH55_STATUS.md

**Main manuscripts:** historical LSPV-1 role has no authority to overwrite the current TMR living manuscripts. MANUSCRIPTS UNCHANGED; no legacy proof trackers consulted or modified. All original five roles and schedule states preserved. P versus NP OPEN.
