# TMR-2/067 | 2026-11-17 12:12 PST | exact five-symbol CSP domain/cofactor quotient

Owner: TMR-2 / PNP Information Necessity. Primary research object from the 2026-11-17 user directive: fixed-template T5-homomorphism, NOT the retired bilinear-CNF primary project. Scientific statuses: KNOWN THEOREM for NP-completeness; PROVED/EXACT (symbolic, restricted to the stated algorithm) for the cofactor congruence and easy family; COMPUTATIONAL for finite executions; unrestricted dynamic necessity and P versus NP OPEN. External independent mathematical review OPEN.

## Candidate and falsifiers, set before source/corpus search

**Dependency D2-T5-EXACT-COFACTOR-QUOTIENT.** On authentic finite simple directed edge lists, a canonical variable-order prefix can be represented for both exact counting and decision by the actual allowed-label masks on all future vertices; weights aggregate all compatible prefixes with identical masks. The target is a complete source-to-output construction and a named execution-sensitive invariant, not a lower bound for arbitrary programs.

Predeclared falsifiers: (F1) two legal prefixes with the same mask vector have different residual Boolean functions or counts; (F2) a real prefix arc yields a mask outside the proposed closed 12-element alphabet; (F3) a cheap complete-bipartite or cycle computation defeats an inferred compulsory width/work charge; (F4) the template admits tractable polymorphisms or an incorrect assumption of NP-hardness. Findings: F1/F2 ruled out symbolically; F3 positively demonstrated; F4 resolved through the original 1988 semicomplete-target dichotomy, which establishes NP-completeness for T5, not through the tensor calculation.

## Exact model and original-source pipeline

Let Sigma=Z/5Z and R(a,b)=1 iff b-a mod 5 is 1 or 3. The tournament arcs are A>B,D; B>C,E; C>A,D; D>B,E; E>A,C. For an input finite directed graph G=(V,E), repeated arcs are redundant. Opposite arcs on one pair may coexist and then rule out that pair in every assignment; loops are immediately UNSAT since R(a,a)=0. The decision problem is the existence of a homomorphism G -> T5; the exact count is the number of all such vertex assignments, not assignments to any auxiliary wire or domain mask.

One explicit canonical *proposed* ASCII front end is "p t5 n m" followed by m records "u v", vertices indexed 0,...,n-1. Its fully charged deterministic parser must check source bytes, whitespace, header count, integer ranges, exactly m arcs, duplicate elimination, loops and trailing junk; valid self-loop source returns integer 0, malformed source returns INVALID. No oracle supplies graph, order, masks or decomposition. The present V8 executable tests explicit graph edge-array objects and does NOT itself implement this ASCII parser; front-end implementation/replay is an OPEN engineering obligation, not secretly counted as executed evidence.

After parsing, use source order 0,...,n-1, or a discovered order whose selection cost is included. The DP is total on arbitrary valid graph sources, but may be exponential. It explicitly computes each output integer and returns YES iff that integer is positive.

## 32-domain propagation table

Represent S⊆Sigma by m(S)=sum_(a in S)2^a, an integer in [0,31]. For a source variable with current domain S and an arc from that variable to a neighbor, allowed support at the neighbor is Out(S)=union_(a in S){a+1,a+3}. For an incoming arc it is In(S)=union_(a in S){a-1,a-3}, all arithmetic mod 5. In source-mask order, the five singleton Out masks are [10,20,9,18,5], the singleton In masks are [20,9,18,5,10]. For every m∈{0,...,31}, its exact outgoing and incoming map is the bitwise OR of these singleton masks at the set bits of m. The published raw file supplies all 32 triples (m,Out(m),In(m)), not a random sample.

The complete outgoing image-cardinality census is: |S|=0 -> 0 (one set); |S|=1 -> 2 (five); |S|=2 -> 3 (five) or 4 (five); |S|=3 -> 4 (five) or 5 (five); |S|=4 -> 5 (five); |S|=5 -> 5 (one). In(a)=Out(a+1 mod 5). Both incoming and outgoing maps preserve unions, commute with cyclic shifts appropriately and map empty to empty. They are **arc-support** maps, not polymorphisms and not an algorithm by themselves.

When an already assigned vertex has a definite symbol c, its edge imposes exactly one of the five 2-element masks. Intersections of those singleton-support masks and full Sigma can only be empty, one of the five singleton masks, one of the five 2-element masks, or all five symbols. Thus the *prefix-imposed future domains* occupy exactly the closed 12-mask alphabet
{0,1,2,4,5,8,9,10,16,18,20,31}; among nonempty possibilities there are 11. This closure does NOT claim that arbitrary current domain-revision sequences or relational path consistency have only twelve distinct relations; the distinction matters.

Ordinary arc consistency with all unpinned domains Sigma is vacuous on any **loopless** source graph: every value has two incoming and two outgoing template supports, so all Σ domains form an unchanged fixpoint, including UNSAT directed two-cycles. Path consistency is a distinct stronger method, and must be measured independently.

## Theorem: exact dynamic cofactor congruence, decision and counting

Fix a vertex order (v1,...,vn). For a *compatible* assignment p to the first t vertices, let U_t be the unassigned suffix. Construct D_t^p(j) for every j∈U_t by starting at Sigma and intersecting Out(p_i) for each crossing arc vi->j and In(p_i) for every crossing arc j->vi. If both orientations occur both intersections are applied. Illegal assigned-prefix internal arcs are rejected.

For a suffix assignment z:U_t->Sigma, the full graph's indicator factors *pointwise* as

    1[G satisfies (p,z)] = 1[p internally valid] *
       product_(j∈U_t) 1[z_j∈D_t^p(j)] *
       product_((i,j)∈E[U_t]) R(z_i,z_j).

Hence the entire residual Boolean cofactor and its exact count depend on p only through its vector D_t^p. This proves a deterministic state congruence for every t and every graph. Identical mask vectors may be merged by **integer addition of multiplicities**, not by forgetting how many prefixes reached them. It is generally only a sufficient quotient, not the Myhill-Nerode minimum.

A single fully constructive algorithm starts with W_0((31,...,31))=1, transitions each actual state by each c∈D_t(v_(t+1)), enforces old prefix validity, and forms each future mask by

    D_(t+1)(j) = D_t(j)
        AND [Out({c}) if v_(t+1)->j, else 31]
        AND [In({c}) if j->v_(t+1), else 31].

Discard transitions with an empty future mask, then accumulate W_(t+1)(D') += W_t(D) on exact-key equality. At t=n, the sole empty-mask-vector weight is exactly #Hom(G,T5), provided all valid prefix branches were accumulated. In particular #=0 iff NO. Induction on t proves counting correctness, including repeated constraints, bidirectional constraints, disconnected components, shared future neighbors and full original-label multiplicity.

Let b_t be the number of remaining vertices incident with a prefix crossing arc and K be the maximum number of retained *nonzero* weighted states at any layer. Every live layer contains at most min(5^t,11^{b_t}) distinct mask vectors, with full 31 on untouched suffix vertices. This is a constructive state upper bound, never compulsory storage for a different solver. For a fixed prefix/suffix indicator flattening over any field, equal mask vectors give identical cofactor rows; thus rank ≤ number of distinct residual masks plus possibly the invalid-prefix zero row. This is again an upper representation bound and not a work lower bound.

One conservative, deliberately loose, *same* locally headed deterministic multitape realization uses a fully validated adjacency matrix, scanning a list/map of explicit n-entry 5-bit keys and exact weights of ≤n log2 5+1 bits. It performs all source scans, attempted key comparisons, masks, updates, exact additions, buffer swaps and output within T(N,K)=O(N^7(1+K)^2), S_peak(N,K)=O(N^3(1+K)) writable bits, for N the complete source bit length. These bounds count failed state insertion attempts and can be improved; they do not require a hash-oracle or costless order search. An adaptive reordered run must either recompute its states from the original graph or explicitly charge valid state conversion. The source is stored once; shared state keys once. Networks would require aggregate live storage and total work.

## A cheap high-treewidth control, and why width is not necessity

For source-authenticated oriented complete bipartite G=K_(a,b), with every arc from left to right, a,b≥1, the exact number of T5-homomorphisms is

    #G = 5(2^a + 2^b - 2).

Proof: if all left labels equal c (5 choices), each right label is independently one of the two outneighbors of c, giving 5*2^b. If at least two distinct left labels occur and any right labeling exists, their common outneighborhood must be a singleton. The five unordered pairs of distinct left labels whose outneighborhoods meet each have exactly one common outneighbor, and each pair supports 2^a-2 nonconstant ordered left labelings. No three distinct labels have a common outneighbor. These contribute 5(2^a-2). Counts are disjoint and exhaust all assignments. A recognizer can authenticate both shores and all edges/absences in polynomial source time and compute the expression with O(a+b)-bit exact integers. K_(k,k) has primal treewidth k, but source-recognized counting is polynomial. At K_(3,3), #=70, while the explicit left-to-right weighted cofactor evaluator retains at most ten live states and the exact Boolean suffix cofactor family has width eleven, counting its zero cofactor. Tensor contraction across a prescribed variable order may have larger width and does not show compulsory work.

An empty directed graph has count 5^n; directed paths have 5*2^(n-1) labelings; disjoint components multiply counts, with exact bit lengths charged. Directed 3-cycle has 15 colorings, directed 5-cycle has 10. Self-loops and 2-cycles have zero colorings. The complete directed T5 source itself has five homomorphisms, its five rotations. All are cheap legitimate controls.

## Algebraic and complexity classification, carefully scoped

The integer 5x5 relation matrix, in order A..E, is
    [0 1 0 1 0]
    [0 0 1 0 1]
    [1 0 0 1 0]
    [0 1 0 0 1]
    [1 0 1 0 0].
Its exact determinant is 2. Hence rank over Q, R, C and any odd characteristic field (including F5) is 5, while rank over F2 is 4 because each row sums to zero and an explicit row reduction gives four pivots. For omega=exp(2πi/5), the standard Fourier eigenvectors f_k(a)=omega^(ka) diagonalize the circulant matrix over C, with eigenvalues omega^k+omega^(3k). Their product is 2; the 5-point Fourier inversion must not be transplanted unchanged to characteristic 5, where 5 is zero. No rank value is a runtime lower bound.

Every endomorphism of T5 is injective because each pair of distinct source vertices is adjacent and the target has no loops. Thus every endomorphism is an automorphism. The five cyclic translations are automorphisms, and exhaustive enumeration of 5^5 assignments found exactly five (COMPUTATIONAL); the template is a core, independent of that census. The core result can also be proved without enumerating automorphisms.

**KNOWN THEOREM, not a new hardness proof:** Bang-Jensen, Hell, MacGillivray (SIAM J. Discrete Math. 1(3), 1988, pp. 281-298, DOI 10.1137/0401029) prove H-coloring NP-complete for fixed semicomplete H with more than one directed cycle. T5 is a tournament and has distinct directed triangles 0->1->2->0 and 0->3->4->0. Therefore Hom(-,T5) is NP-complete in the standard many-one sense, while membership in NP is immediate by checking five-valued vertex assignments. The 2010 locally semicomplete classification restates this theorem (DOI 10.1016/j.disc.2010.03.033). Finite-domain CSP dichotomy (Bulatov/Zhuk) is consistent with this and motivates polymorphism analysis, but the entire clone of T5's higher-arity polymorphisms has NOT been enumerated in this run. Exact list-valued/path-consistency tractability is NOT presumed.

The existence of an NP-complete fixed-template decision CSP does not make a particular input graph hard or imply superpolynomial lower bounds for every exact-count algorithm. Exact counting may be #P-type but no parsimonious counting-hardness reduction was proved here.

## Actual execution and limitations

The actual published standalone JS, revision "tmr2-t5-dynamic067.v1" with deterministic xorshift seed 202611171212, performed the exact finite 32-domain map, 5x5 determinant/rank, 5^5 endomorphism check, named path/cycle/tournament/transitive/complete-bipartite controls, original-label DP and independent exhaustive 5^n enumeration, path-consistency relation tightening, explicit cofactor-width enumeration (for n≤7), and 420 additional seeded random n≤7 directed graphs. All assertions passed, failures=0. V8 random samples were 153 SAT/267 UNSAT, max observed retained weighted state count 25. Earlier separate local CPython audit with a different RNG found 152 SAT among 420 independently brute-checked samples, also zero mismatches, but those local scripts are not claimed as GitHub-published.

Code: experiments/tmr/tmr2_t5_dynamic067.js (Git blob da81abbd281a6c0cccc98e20fba3696782911aab).
Immutable raw: results/raw/tmr/2026-11-17_1212_TMR2_T5_DYNAMIC067_V8_RAW.json (Git blob 7b8d9f84f805ad1c71645f4818a92f4f850ec03e).
Examples: T5 n5/m10 #5, DP widths 1,5,5,5,5,1 and Boolean cofactor counts 1,5,6,6,6,2; T5 plus sixth conflicting vertex n6/m15 #0 and path consistency detects; directed K3,3 n6/m9 #70, DP max ten, cofactor max eleven. A PC-consistent UNSAT family was NOT found in a separate finite random search, which proves nothing about existence; the PC-consistent hard-instance construction is OPEN.

No physical Turing-machine emulator, native Node CLI replay, complete canonical ASCII source parser run, checkout preflight, complete LaTeX build or independent external mathematical review was performed. Published V8 tests are COMPUTATIONAL only. Draft/merge status must be independently verified.

## Named execution-sensitive invariant for TMR-4

**D2-T5-COFACTOR-11-TRACE.** The actual source cursor and validation state, paid graph adjacency and chosen variable order, each current exact 5-bit future-domain vector, and its exact integer prefix multiplicity must represent precisely the partial-assignment cofactor above, with no hidden preprocessed oracle. The *complete* transition interface is READ/PARSE/GUARD/EDGE_INSERT/LOOP_DETECT, ORDER/DISCOVER/SWITCH, BRANCH_LABEL, INTERSECT_OUT, INTERSECT_IN, PRUNE_EMPTY, MERGE_EXACT_WEIGHT, DROP_FRONTIER, BIGINT_ADD, CACHE/DROP/RECOMPUTE, and OUTPUT/VERIFY. Count source objects once and exact transitions including failures. An unrestricted source solver may use any cheap alternative and need not realize these states. TMR-4 should investigate fidelity and cost of any source-to-OBDD or tensor compiler, not interpret this restricted trace as a universal information requirement.

## Four required gates and guards

| Gate | Status | Reason |
|---|---|---|
| DISJ sanity | PASS, restricted | No lower bound from static rank; complete bipartite and tractable source families explicitly recognized, and DISJ remains a legal compact counterexample |
| Relativization | PASS for local algebraic algorithm; OPEN unrestricted | No nonrelativizing P-v-NP conclusion, even though the known NP-hardness reduction is established; BGS, algebrization and Natural Proofs remain safeguards |
| Simultaneous DTISP | PASS for restricted same-execution UPPER ledger; OPEN for lower transfer | The displayed T(N,K),S(N,K) hold for one deterministic execution, not a forbidden-region pair or necessity for all programs |
| Deterministic configuration counting | PASS upper-only | Total deterministic read-only-input runtime has T≤2^O(S+log N), never a work lower bound or automatic randomized/quantum statement |

Horn and 2SAT graph controls, affine-looking cycles, treewidth, equality, independent products, padding, auxiliaries, autarky, unique selectors, count normalization, unique-solution rank-one, local basis/field changes, randomized isolation, sharing, caches and alternate source algorithms remain legally available. Not every hostile family was executed here. Historical /341 is FAIL for full UNSAT authority; /386 is RESTRICTED. P versus NP OPEN.

## ONE next dependency

**D2-T5-PATH-CONSISTENT-UNSAT-FAMILY (OPEN):** Construct authentic loopless oriented unsatisfiable graphs of unbounded size whose full all-pair path-consistency closure remains nonempty, demonstrate this by source-executed exact propagation, and compare actual prefix mask-state profiles, cofactor/OBDD width, treewidth and cut ranks against *legitimate* source-recognized cheap simplifications and exact counts on the very same graphs. A family without a charged source parser, or one refuted by cheap unit/PC tests, does not satisfy this dependency.

## Primary references

[1] J. Bang-Jensen, P. Hell, G. MacGillivray, "The Complexity of Colouring by Semicomplete Digraphs", SIAM J. Discrete Math. 1 (1988), 281-298. https://doi.org/10.1137/0401029

[2] J. Bang-Jensen, G. MacGillivray, J. Swarts, "The complexity of colouring by locally semicomplete digraphs", Discrete Mathematics 310 (2010), 2675-2684. https://doi.org/10.1016/j.disc.2010.03.033

[3] D. Zhuk, "A Proof of the CSP Dichotomy Conjecture", JACM 67 (2020). https://doi.org/10.1145/3402029

[4] R. E. Bryant, "Graph-Based Algorithms for Boolean Function Manipulation" (1986). https://doi.org/10.1109/TC.1986.1676819

[5] Repository governance: research/coordination/2026-11-15_END_TO_END_AGENT_MANUSCRIPTS.md; newer user T5 directive dated 2026-11-17. Earlier main2 /055-/066 exact-counting theorems remain historical controls, not current primary pipeline.
