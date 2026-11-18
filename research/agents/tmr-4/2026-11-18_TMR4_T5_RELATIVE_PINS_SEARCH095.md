# TMR-4/095: exact T5 relative pins give a costed decision-to-witness reduction

**Status:** PROVED/EXACT within a named model, computational verification of finite instances; not an unconditional lower bound. Existing TMR-4/094 source-bit certificate, /093 mixed-input counterexample, and earlier research remain intact. P versus NP remains OPEN.

## Candidate and four falsifiers

Candidate: use the original five-symbol beat relation itself to impose *relative* colors, and quantify a uniform T5-CSP decision-to-search reduction over newly encoded graph sources. The theorem must account for source parsing, all decision queries, fresh vertices, fan-out, propagation, and output. Do **not** transfer a large full-assignment OBDD into a source-level decision lower bound.

1. Absolute color pinning is impossible in the unaugmented T5 language. Every instance is invariant under global Z5 translations. Pin differences to a distinguished original root, never an absolute palette element inside a queried graph.
2. An ordinary R-path admits two edge differences, so it does **not** force a successor. Use the three-arc triangle with an internally unique extension.
3. Decision-preserving auxiliary gadgets need not preserve counts. The precise theorem below proves exactly one accepting auxiliary extension per compatible original assignment, zero otherwise; rejected expanded assignments must be counted separately.
4. An input consisting of a binary integer vertex-count header and zero arcs can describe a billion isolated vertices with only 26 canonical JSON bytes, while any explicit witness has one billion symbols. State complexity in n plus the source length L, or require an explicit vertex list guaranteeing n ≤ poly(L).

## Local gadget and exact theorem

Let Σ=Z5 with R(a,b) iff (b-a) mod 5 lies in {1,3}. Define S(u,v;z) = R(u,v)∧R(u,z)∧R(z,v). For every u=a, there is exactly one choice (v,z), namely v=a+1 and z=a+3. Proof: each of v-a and z-a is either 1 or 3. Equal choices give a forbidden loop, while choices (3,1) yield difference 2 on z→v; only choices (1,3) yield the permitted difference 3.

A directed chain of ℓ such triangles, with fresh auxiliary endpoints and side vertices, forces output-start difference ℓ mod 5. To pin x_v−x_r=d, use ℓ=d for 1≤d≤4 and ℓ=5 for d=0. At most 2ℓ−1≤9 vertices and 3ℓ≤15 arcs are added; overlapping source arcs may be deduplicated. Every compatible assignment of the original endpoints has **exactly one** accepting extension to the new variables, every incompatible assignment has none.

**Theorem (restricted uniform decision-to-witness transfer).** For an authenticated source graph G on n≥1 original vertices and m arcs, and a *total uniform* algorithm D deciding T5-CSP on every encoded T5 graph, one can decide G and, if SAT, return a valid original five-symbol assignment after at most 1+5(n−1) calls to D. Every queried source has at most 10n−9 vertices and m+15(n−1) arcs. The additional work for canonical serialization, parsing, source authentication, graph construction, and witness checking is polynomial in n and original encoded length L. If the maximum query has B=O((n+m) log(n+1)+L) source bits and D runs in time T(B), the overall running time is O(n T(B)+poly(n+L)), including polynomial output work. A polynomial decision algorithm therefore yields polynomial witness search when n≤poly(L), for example under conventional explicitly listed vertex encodings.

Proof: query D(G). On YES, fix the *output representative* x_r=0 by the global translation automorphism; no queried graph pins any absolute color. For each remaining vertex v, try d=0,1,2,3,4 in order by submitting an actual expanded source with all previous chosen relative pins plus the candidate pin for v. One d must preserve satisfiability, because the previously feasible assignment has some relative difference to the root and each candidate gadget has the proved unique-extension property. Induction gives a compatible full assignment. Rotate the final assignment to root zero; it satisfies all original arcs. The oracle-query and source-size bounds follow by summing the gadget sizes. For n=0, the empty assignment is a witness without oracle queries.

For a set Q of relative pins and its expanded graph H_Q, an **exact count identity** is:

Z(H_Q) = Σ_{x∈Σ^n} [x satisfies G] ∏_{(v,d)∈Q}[x_v−x_r=d].

No arbitrary expanded assignment is identified pointwise with an original assignment. The exact rejecting-assignment count of H_Q is 5^N−Z(H_Q), where N is its expanded vertex count. This is a count-preserving *existential projection*, not an unrestricted complete-assignment FBDD equivalence.

## SAME_REALIZATION ledger and encoding comparison

The local executable Python auditor canonicalizes, SHA-256-authenticates and reparses actual encoded graph sources, adds fresh vertices and all gadget arcs, serializes and reparses every queried graph, then executes generic 32-mask unary arc-consistency followed by adaptive DFS branching. It counts actual query-source bytes read, DFS nodes, arc scans, compatibility tests, branch steps, copied domain masks, and maximum source expansion; no gadget identifiers or hidden pin constraints are passed to its decision solver. The independent Node.js auditor rebuilds the gadgets and generic decision solver and checks source SHA-256, exact source counts, literal CNF semantics, and 32-domain transitions. All five values are considered, all rejected original assignments are retained for comparison, and source-special-case recognition is not assumed free. Sorting, hashing, address arithmetic, loop checks, cached state construction, counting precision, and output must be charged for any physical implementation. No Fourier transform or implicit tensor compression is used.

The direct validity-checked 3-bit-per-symbol encoding uses 3N+15M CNF clauses and 9N+90M literal occurrences for an expanded source of N vertices and M arcs. Codes 5,6,7 are rejected. All 2,048 domain-pair/orientation cases agree with the five-valued relation. A grouped Boolean decoder takes at most six binary nodes per native five-branch node, but arbitrary interleaved-bit FBDDs remain outside this restricted reverse implication. A full five-valued complete-query assignment tree has (5^N−1)/4 internal nodes for N≥1 and is not alleged to be an efficient solver or a lower bound on decision.

## Four verification gates, finite COMPUTATIONAL only

**G1 source:** 56 canonical graphs, including directed cycles, paths, random graphs, loops, an explicit 2-cycle contradiction and empty-edge families. All 56 original-source SHA-256 digests match across independently written Python and Node.js. Seven malformed-source controls reject. For n=10^9,m=0 the canonical compact source is 26 bytes, exposing the vertex-header source-cost loophole.

**G2 semantics:** exhaustive checks of all 125 triples of triangle assignments and 125 root/target/offset chain cases; 40 SAT and 16 UNSAT original sources, each exact-counted independently over a total of 43,080 original assignments; 185 actual generic T5 decision calls by each implementation reconstruct root-zero witnesses or correctly reject. The n=0 case also passes separately.

**G3 Boolean/domain:** each implementation checks 43,080 complete valid-code signed-literal CNF assignments, 504 invalid-code samples, and all 2,048 oriented 32-mask pairs; all valid instances preserve original decisions and all malformed codes reject.

**G4 reproducibility/cost:** Python logs 21,903 full query-source bytes, 802 DFS nodes, 28,600 arc scans, 225,139 compatibility tests, 617 branches, 6,846 copied domain masks, maximum 41 query vertices and 465 query bytes. JavaScript independently agrees on all 56 hashes, 40/16 SAT split, 185 oracle queries, all counts, CNFs and masks. Fixed seed 20261118095, repeated output byte-identical, zero unexpected failures. Executable Python and independent JS, source fixtures, complete raw JSON and hashes are in the preserved downloadable evidence package. Formal peer review and physical TM microsteps are **OPEN**.

## Four foundational model checks and next dependency

DISJ sanity **PASS** as a cheap-source obstruction control, not as a source-hardness implication. Relativization: this reduction **relativizes** to any total CSP decision oracle, so no nonrelativizing lower bound is obtained, and oracle separation remains **OPEN**. Simultaneous DTISP **PASS for declared upper-bound accounting only**, not a forbidden region. Deterministic configuration counting **NOT APPLICABLE** as a runtime lower bound; Natural Proofs and algebrization barriers have not been crossed. Unrestricted adaptive FBDD or original-source Turing-machine lower bound remains **OPEN**.

**Next:** D4-T5-ALL-INPUT-UNIFORM-DECISION-ADVERSARY-096, which requires an adversary that survives every allowed source-based preprocessing strategy, witness search and class recognizer, not simply a large exact full-assignment representation.

**Literature:** Barto, Kozik and Niven, *The CSP Dichotomy Holds for Digraphs with No Sources and No Sinks*, SIAM J. Computing 38(5), 2009, DOI 10.1137/070708093. T5 is a loopless tournament and thus a core, but not a directed cycle, so this theorem establishes its CSP is NP-complete. Previous TMR-4/088, /093 and /094 branches establish compatible restricted gadgets, semantic/source transfer barriers and bit-probe controls.