# TMR-4/097: Row-local cost-sound abstraction and polarity-routing firewall

**Owner:** TMR-4 / PNP Cost-Sound Abstraction. **Primary object:** original five-symbol T5-CSP graph, R(a,b) iff (b-a) mod 5 belongs to {1,3}. Also considers general CNFs only under the explicitly stated separated-private-variable layout. **Status:** PROVED/EXACT for factorization, time-accounting algebra, and four logical falsifiers; COMPUTATIONAL for the finite native/CNF/domain tests; CONDITIONAL for a polynomial SAT seed; OPEN for unrestricted machine lower bounds, independent review, and TM microstep auditing. This is a continuation of /096, not a replacement of earlier research.

## Candidate, quantifiers, and the complete chain

Candidate D4-T5-ROW-ABSTRACT-SOURCE-097: authenticate an explicit encoded source graph G; verify that, after a supplied shared interface Z of q vertices has been fixed, all other vertices are partitioned into disjoint local sets Y_{rb}, indexed by at most R rows and B_r blocks per row; compile a source-faithful per-block evaluator, then a three-valued one-sided row summary; charge all child calls, source reads, validation, materialization, proof checks, recomputation, cache/switch costs, and peak live workspace. The layout certificate and every cross-block arc are checked, not assumed. If a partition is *discovered* instead, discovery time and workspace must be paid.

For a value z in Sigma^q, let N_{rb}(z) count satisfying extensions on Y_{rb}. The verified factorization is

    Z(G) = sum_{z in Sigma^q} product_r product_b N_{rb}(z).

This is an identity over **original assignments** and counts, not an algorithm for computing N in polynomial time. Define h_{rb}(z) = [N_{rb}(z)>0], row H_r(z)=AND_b h_{rb}(z), and global H(z)=AND_r H_r(z). Then

    G SAT iff exists z: H(z)=1.
    G UNSAT iff for all z: exists (r,b): N_{rb}(z)=0.

The UNSAT witness for a *fixed* z may be a different block for every z. The quantifier swap to "there exists one globally UNSAT block" is invalid.

**Three-valued verifier**: given z, an untrusted block index and candidate refutation pi, output REFUTED(z,r,b,pi) only after checking a sound proof of the actual residual block's UNSAT. If all local witness strings are independently verified and concatenate consistently on the same z, output EXTENSION(z,w); otherwise return UNKNOWN. Wrong supplied branches never lead to a false accepting certificate. A complete deterministic local decision seed can make the fixed-z Boolean decision total, but an UNSAT decision bit alone is not an independently checkable refutation. If the seed is only a decision procedure, SAT-witness reconstruction requires an additional paid search reduction.

## Exact four-vertex counterexample, independent of complexity assumptions

Let shared z=(u,v), and private variables a,b. Row 0 has arcs u->v,u->a. Row 1 has v->u,v->b. No private variable is shared between blocks. Each row separately has ten z-values with two private extensions, and is satisfiable. Their supports on z are disjoint because T5 has no reciprocal directed pairs. Among the 25 z-values, 10 make only row 0 feasible, 10 make only row 1 feasible and five make neither feasible. **No fixed row/block is refutable for every z, yet their conjunction is UNSAT.**

Removing v->u produces a SAT paired control with exactly 40 satisfying full assignments. These facts hold at the level of actual authenticated source arcs, not hand-selected truth-table labels. Direct 3-bit-per-symbol CNF uses 3N+15M clauses, 9N+90M signed occurrences, forbids codes 5,6,7, and agrees pointwise on all valid codes.

## Resource-exponent falsifiers for the proposed n^1.33 + o(1) / sqrt(n) polylog layout

Use n strictly as the **base layout parameter**. Assume R<=n^.195, B_r<=n^.65 per row, and each block's actually materialized local encoding has length <=n^.35. There are at most n^.845 local calls, with a worst-case materialization envelope n^1.195. The exponents are caps, not a claim that this is an n-bit input. If n denotes true input length L, disjoint explicitly serialized local data sum to O(L), and these three caps cannot all represent separate additional source content beyond L.

A hypothesized deterministic complete local SAT seed with time O(s^d polylog s) gives per-fixed-z **Boolean decision** upper envelope

    T_z <= T_parse+T_discover + O(n^(.845+.35*max{d,1}) polylog n),

provided there is a streamable, authenticated block index and each child sees only the shared z-coordinates *actually occurring* in that local source. The bound n^1.33 requires d <= (1.33-.845)/.35 = 97/70 ~=1.385714; "polynomial seed" without a degree is not enough. A degree-two seed yields n^1.545, not n^1.33. An essentially linear seed yields n^1.195 per fixed z, **not** all-z decision.

Four costs can independently invalidate an alleged n^1.33 conclusion:

1. **Global shared-vector rematerialization:** if each of n^.845 child calls copies all q=n^.5 shared entries, copying alone costs n^1.345, greater than n^1.33. A sparse indexed local interface is required and must be source-verified.
2. **Decision versus witness:** conventional one-variable-at-a-time self-reduction can issue O(s) decision queries per satisfiable block. Its conservative upper envelope is n^(.845+.35*(d+1)); with d=1 this is n^1.545, not n^1.33. A direct witness-producing seed or an improved paid search theorem is a separate premise.
3. **Source index and storage:** a writable n^.845-entry block pointer table exceeds an n^.5 polylog workspace budget. A source-sorted sequential scan, immutable index, or recomputation must be constructed and charged. Repeated arbitrary-source scanning might cost much more.
4. **Universal coverage of z:** deterministic all-z enumeration multiplies T_z by |Sigma|^q=5^q for T5 (2^q for Boolean shared variables), unless a source-proved symbolic compression replaces it. For d=1 and all other ideal costs, n^1.33 requires q<=.135 log_5 n; q=n^.5 gives exponential enumeration. A single freely supplied correct z is an existential path, not this deterministic all-z algorithm.

A plausible conditional per-fixed-z writable space is O(q + max_rb(s_rb+S_seed(s_rb)) + log(number of blocks) + live verification state) **only** with input and certificates genuinely read-only, streaming interfaces, no stored global offset table, and no global exact count retained. Exact total counts can have Theta(number of original vertices) output bits (empty T5 graph: 5^N), which must be charged as output and if materialized as live workspace. SAT decision does not inherit exact counting.

## Three independent path/advice models

**Free polarity routing:** granting the correct global SAT/UNSAT bit as one unverified choice is an answer oracle. A wrong-path accepting result is unsound. Sound branches require checked witnesses for SAT and a valid refutation/total decision procedure for UNSAT. The source promise and all alternative branch costs must be explicit.

**Uniform deterministic specialist:** a program for arbitrary encoded inputs may scan indices, apply a sound proof checker, and return UNKNOWN. A complete polynomial-time source-level decider for general T5 would be a polynomial-time algorithm for an NP-complete CSP, hence P=NP. Barto, Kozik and Niven (2009) apply because T5 is loopless, every two distinct colors are adjacent, so every endomorphism is injective and T5 is a core; each color has in/out degree two and its unique component is not a directed cycle. This is a classification result, not a quantitative reduction-size bound.

**A supplied k-bit nondeterministic correct path:** on SAT, guess a full assignment and check all arcs; on UNSAT, merely guessing a bad-block index is not enough to establish a negative claim. A sound verifier of length-k refutations accepts only actual UNSAT inputs, but arbitrary T5 UNSAT sources are not known to have polynomial-length proofs in a fixed polynomially checkable proof system. An all-UNSAT polynomial proof guarantee would put coT5 in NP and, by NP-completeness, imply NP=coNP. This is not asserted as a theorem about proof length. If all paths are deterministically enumerated, charge up to 2^k paths and replay time; when k bits describe choices at adaptive nodes, a complete alternating strategy may have a universal tree of size up to 2^q and cannot be charged as one path. Read-only random-access certificates are *not* writable workspace, but their addresses, every read, proof verification and the cost of obtaining or deterministically simulating them are mandatory. A read-only given certificate model is not automatically the same as small-space nondeterministic RAM.

A local UNSAT block checker can use a complete (possibly exponential) search tree as a proof; this is sound and complete and incurs the full tree size. The row-level universal obstruction is a sound semantic identity, not a cheap verifier or a total polynomial algorithm.

## Simultaneous RAM time-space literature firewall

The following cited bounds refer to the source-paper **random-access Turing-machine** models and input length L. No quantitative exponent is transported to T5 or the separated layout without a verified length-, time-, and space-preserving reduction.

1. **Nondeterministic SAT:** Fortnow (2000, JCSS 60:337-353) excludes SAT in time L^{1+o(1)} and space L^{1-epsilon}, for every fixed epsilon>0, on general random-access nondeterministic Turing machines. A supplied addressable certificate is a different access model.
2. **Nondeterministic UNSAT / conondeterministic SAT:** Fortnow, Lipton, van Melkebeek and Viglas (2005, JACM 52:835-865) establish, for every c<sqrt(2), a positive d(c) excluding conondeterministic SAT in time L^c and space L^{d(c)}. In particular this excludes L^1.33 and L^{o(1)} simultaneously, but its abstract does not establish exclusion at workspace L^.5.
3. **Deterministic SAT decision:** the small-space benchmark is SAT not in DTISP(L^c,L^{o(1)}) for c<2cos(pi/7) approximately 1.80194 (Williams/Buss-Williams). It does not by itself exclude DTISP(L^1.33,L^.5 polylog L). Buss-Williams (2012 conference; 2015 journal) prove optimality of the 1.801 exponent within the stated alternation-trading proof paradigm at subpolynomial space; this is not a global lower-bound ceiling.
4. **Proof-system-specific negative claims:** Ben-Sasson and Wigderson (JACM 2001) relate resolution width to proof size and give exponential resolution lower bounds for particular families, not for all possible algorithms or all proof systems.

No assertion that the pair (1.33,.5) is already known forbidden follows from these cited statements; likewise a hypothetical seed with linear local workspace has a different resource profile.

## Finite reproducible verification and SAME_REALIZATION

Independent Python and Node.js implementations evaluate original source arcs and the row factorization, with exact original-assignment multiplicities. For two N=4 graphs, each implementation exhaustively tested 625 assignments. The UNSAT graph has 0 accept/625 reject; SAT graph has 40 accept/585 reject. Python checked 625 valid three-bit encodings and all 3,471 invalid codes per graph against actual signed-literal CNF, plus all 320 (fixed color, unary mask, orientation) and all 2,048 (pair of masks, orientation) propagation controls. Native CNF clause counts are 72 (UNSAT, four arcs) and 57 (SAT, three arcs). Python/Node independent original-source SHA-256 values and row histograms agree. There were zero unexpected test failures. No synthetic stress case is an asymptotic proof.

**SAME_REALIZATION ledger:** source bytes, SHA-256 authentication and parsing; partition/discovery verification; original arc enumeration; shared-index fetches; child source materialization and all calls of both answer polarities; candidate proof/witness verification and wrong paths; row-state merging and propagation (full 32 unary masks, not the special ten-mask quotient by assumption); five-way state fan-out; every cache/eviction, branch switch and recomputation; memory retained simultaneously; Boolean/CNF encoding; arbitrary-precision arithmetic and output. No Fourier/Z5 tensor contraction was used, hence no such operation is free. Native finite enumeration visits every original assignment and includes all rejecting paths; unrestricted native FBDD versus interleaved Boolean reverse transfer stays OPEN. Read-only certificate access and storage are explicitly distinct.

**Four gates:** DISJ PASS as a cheap-family falsifier, no lower bound; RELATIVIZATION FAIL for any unqualified P/NP conclusion, this factorization relativizes; SIMULTANEOUS DTISP OPEN for the (1.33,.5) pair and for quantified model transfer; DETERMINISTIC CONFIGURATION PASS as an upper-bound consistency test only, not a runtime lower bound. Algebrization/Natural Proofs are not invoked to promote a result. Hostile 2-SAT, affine, bipartite, local contradiction, compact syntax, T5 translation symmetry, and exact-count controls remain legal shortcuts.

**Evidence:** Python finite runner 'tmr4_097_row_summary.py', independent JavaScript 'tmr4_097_independent.js', raw deterministic JSON with source hashes and exponents, separately materialized in a conversation evidence package. Code is self-contained and uses no random seed. Local Git checkout/preflight, full LaTeX build, and physical-machine microstep replay were not run. Structural proof and source-specialization have not been independently peer-reviewed.

**ONE next dependency:** D4-T5-ROW-PROOF-STRATEGY-INTERFACE-098. Find a genuinely source-derived, independently checked symbolic representation of the entire z -> (bad block, local refutation) strategy with acquisition, proof replay and peak live space bounded on the same all-input execution. If only a row Boolean summary is available, prove a useful bound on computing it *without* assuming a cheap UNSAT oracle or a free correct path. P versus NP remains OPEN.

## Primary references

[1] Barto, Kozik, Niven. The CSP Dichotomy Holds for Digraphs with No Sources and No Sinks. SIAM J Comput 38 (2009), 1782-1802. https://doi.org/10.1137/070708093

[2] Fortnow. Time-Space Tradeoffs for Satisfiability. J Comput Syst Sci 60 (2000), 337-353. https://doi.org/10.1006/jcss.1999.1671

[3] Fortnow, Lipton, van Melkebeek, Viglas. Time-Space Lower Bounds for Satisfiability. J ACM 52 (2005), 835-865. https://doi.org/10.1145/1101821.1101822

[4] Williams. Inductive Time-Space Lower Bounds for SAT and Related Problems. Computational Complexity 15 (2006), 433-470. https://doi.org/10.1007/s00037-007-0221-1

[5] Buss, Williams. Limits on Alternation-Trading Proofs for Time-Space Lower Bounds. Computational Complexity 24 (2015), 533-600. https://doi.org/10.1007/s00037-015-0104-9

[6] Ben-Sasson, Wigderson. Short Proofs Are Narrow: Resolution Made Simple. J ACM 48 (2001), 149-169. https://doi.org/10.1145/375827.375835
