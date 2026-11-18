# PNP CROSS-TRACK SYNTHESIS 65: HIGH-GIRTH ALWAYS-YES T5 WITH #P-HARD EXACT COUNT

2026-11-18 08:26 PST. P versus NP OPEN. New restricted theorem, independently reviewed mathematics OPEN. Earlier 4 candidate proposals were frozen before literature/project search; selected integration is TMR-2/086 four-edge saturation + TMR-1/092 exact counting + TMR-3/086 charged path cofactors + TMR-4/089 proof-transport safeguards.

## Four tracks read
Resource Contraction: TMR-1/092 full Fourier-flow exact time poly(L)min(5^rho,2^(n-c)); TMR-3/086 full source-derived weighted path quotient and affine DSU. Nonrelativizing Simulation: LSPV-5 FACTOREDGATE1 full main manuscript; exponential ANF closure can coexist with polynomial source-certified endpoint, WRAPPER necessity OPEN. Universal Obstruction: TMR-2/086 full four-subdivision SAT-collapse report; all four-edge path words have positive but nonconstant cofactor. Proof Transport: TMR-4/089 full nonaffine crown OBDD report, arbitrary decider-to-Resolution transfer OPEN. Also checked issue #3, current GitHub, prior project chats/Library, Google Drive (no newer replacement), and primary #CSP dichotomy literature.

## Theorem: one-query exact-count reduction to a guaranteed-SAT bipartite girth-8 source class
Let R(a,b) iff (b-a)%5 is 1 or 3. Let A be the cyclic T5 adjacency matrix, S the +1 shift matrix, so A^T=AS. The endpoint completion first row for a directed all-forward length-4 path is K0=(4,4,1,6,1). For a length-4 path with three backward edges, K3=(1,6,1,4,4). Two internally disjoint length-4 paths with these orientation words between the same terminals give exact cofactor

    W(d)=K0(d)K3(d)=(4,24,1,24,4).

It is strictly positive at every endpoint difference d, and W(d)=24 iff d in {1,3}, precisely the original beat relation. Given any loopless directed graph G with n>=1 vertices and m arcs, choose k=n+1 and replace every original arc by k copies of the two-path gadget, with all 6km new internal vertices private. The expanded H has N=n+6km vertices and M=8km arcs, is bipartite and has underlying girth >=8 if cyclic. Every original core labeling extends, including the all-zero coloring, so H is always SAT.

Let C=#Hom(H,T5) and Z=#Hom(G,T5). Conditional on original coloring x, the number of interior completions is product_over_arcs W(x_v-x_u)^k. Every original satisfying assignment contributes exactly 24^(km). Every original UNSAT assignment contributes at most 24^(km)/6^k, so

    0 <= C / 24^(km) - Z <= 5^n / 6^(n+1) < 1.

Hence the exact polynomial-time ONE-QUERY METRIC REDUCTION

    Z = floor(C / 24^(km)).

All graph generation, parsing, full interior witness construction, binary integer computation and source costs are polynomial; C uses O(N) bits. Loop-containing G are trivially counted as zero before reduction. By Dyer-Richerby/Bulatov #CSP dichotomy, #Hom(-,T5) is #P-hard because R is not rectangular: R(0,1),R(0,3),R(2,3) hold but R(2,1) fails. Thus exact counting on the high-girth, bipartite, always-satisfiable target class is #P-complete under polynomial-time metric reductions, not claimed parsimoniously. By contrast the T5 decision problem restricted to the target promise class is constantly YES, with a cheap explicitly constructible witness.

This refutes the implication that difficult exact counting, large transfer rank, or exponential state-summation on a source family entails hard SAT decision there. The new construction is NOT five-regular. It does not establish any superpolynomial runtime lower bound.

## Independent hostile finite audit
- 16 four-edge orientation words x 25 endpoints, 400 checks comparing matrix and direct path enumeration.
- Two-path gadget all 390,625 possible 8-vertex colorings audited by endpoint-conditioned enumeration, cofactor W exactly; internal enumeration pruned on invalid prefixes.
- 127 directed sources n<=5, including antiparallel and local triangle-star UNSAT, original 5^n exhaustive count matched floor of transformed exact integer count. 829 total code assertions, zero final failures, seed 202611180818.
- Controls: 3-edge all-forward path has forbidden endpoint difference 1; sharing private vertices breaks multiplicative factorization; loops are excluded or preprocessed; transformed #count reduction cannot transport to arbitrary SAT proof/time lower bounds.
- Executed standard-library Python script: audit_counting_fork65.py; full report and SHA256 file manifest in locally preserved 2026-11-18_0826_T5_GIRTH8_COUNT_DECISION65_BUNDLE.zip. External review pending.

## Proof DAG
ESTABLISHED: decision T5 NP-complete; counting T5 #P-complete under #CSP dichotomy because R nonrectangular.
PROVED RESTRICTED: K0/K3 exact cofactor -> W maximum precisely on legal differences -> H_k always SAT, bipartite, girth>=8 -> integer-floor single-query count decoding -> counting hardness on an always-YES class.
CONDITIONAL: polynomial exact counter on H_k yields polynomial exact counter on unrestricted T5 after fully charged metric reduction.
OPEN: girth8/five-regular relative-pin enforcement, truly universal resource lower bound, necessary nonrelativizing WRAPPER hinge, correct same-input/common-clock UWI, arbitrary-decider-to-Resolution transport, unrestricted T5 superpolynomial decision lower bound, P!=NP.

## Next specialist assignments
Resource Contraction: source-recognize/count H_k, pay full graph and bigint costs; test any unexpected exact-count quotient versus Fourier. 
Nonrelativizing Simulation: test whether WRAPPER contributes any logically necessary nonrelativizing step once easy decision and hard counting coexist.
Universal Obstruction: add H_k as explicit SAT-positive control to NO-instance high-girth tests; same-input UWI must include all valid source-aware witness algorithms.
Proof Transport: distinguish one-query metric #count reduction from unproved algorithm-to-Resolution transport; formalize counting proof maps before discussing proof complexity.

Sources: Dyer & Richerby, SIAM J Comput 42 (2013), DOI 10.1137/100811258, https://arxiv.org/abs/1003.3879 ; Bulatov, J ACM 60 (2013), #CSP dichotomy; Bang-Jensen/Hell/MacGillivray SIDMA (1988), DOI 10.1137/0401029. Independent math review OPEN. P vs NP OPEN.
