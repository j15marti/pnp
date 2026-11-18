# TMR-4/094: Exact source-decision certificate, not an assignment-OBDD lower bound

**Date:** 2026-11-18, America/Los_Angeles. **Role:** TMR-4 / PNP Cost-Sound Abstraction. **Status:** PROVED/EXACT in two specified deterministic bit-probe models, independent mathematical review OPEN; finite checks COMPUTATIONAL. P versus NP OPEN.

## T5 template, uniform source model, and named dependency

Let \(\Sigma=\mathbb Z_5\), \(R(a,b)\iff(b-a)\bmod5\in\{1,3\}\). For n labeled vertices, an authenticated loopless directed graph has one independent input bit \(e_{ij}\) for every ordered pair \(i\ne j\). Antiparallel arcs are allowed. Its exact decision function is \(F_n(e)=1\) iff there is an original-vertex coloring satisfying every present directed arc. The source interface exposes only individual graph bits, at one query per address, after n and the fixed input format are known. A correct deterministic decision tree must work on **all** \(2^{n(n-1)}\) source graphs.

**D4-T5-DECISION-SPECIFIC-SOURCE-MACHINE-TRANSFER-094:** Replace the unsound /092-/093 proxy of minimum complete-assignment OBDD width with an actual *source decision certificate*, and determine precisely what lower bound transfers.

## Theorem 094A: full directed-source certificate (PROVED/EXACT, scoped)

The minimum number of source bit probes on the all-zero graph, over all deterministic decision trees computing \(F_n\) correctly on every input, is

\[
C_{\mathrm{SAT}}(0^{n(n-1)})=n(n-1)-\lfloor2n^2/5\rfloor.
\]

**Proof.** Follow a correct algorithm's all-zero query transcript and let H contain every *unqueried* possible arc. If H is UNSAT, that H input produces the identical observed transcript and the algorithm incorrectly returns YES. Thus H has a T5 homomorphism h. With h color class sizes \(n_0,\dots,n_4\), at most one directed arc is permitted across any differently colored vertex pair and no arc is permitted within a class, hence \(|E(H)|\le\sum_{a<b}n_an_b=(n^2-\sum n_a^2)/2\le\lfloor2n^2/5\rfloor\). For equality, choose the balanced coloring \(h(i)=i\bmod5\), query exactly its forbidden arc positions, and return YES with h if all those bits are zero. If any queried bit is 1, query the remainder and perform exhaustive five-color search. This is one uniform, total, all-input-correct algorithm. QED.

At n=100 the matrix has 9,900 original source bits and the tight certificate reads 5,900 of them, *not* an exponential number.

**Reverse mismatch.** The very same empty G has an identically-TRUE original-assignment predicate, with exactly \(5^n\) accepting and zero rejecting assignments; a complete native five-way OBDD has width one and n internal nodes. Thus even a trivial assignment OBDD does not imply no source decision work. In the other direction, /092-/093 already showed that huge exact-assignment OBDD width can accompany cheap source decisions. Neither proves a machine lower bound.

## Theorem 094C: forward-only source promise (PROVED/EXACT, separate model)

If the grammar permits only the \(M'=\binom n2\) arcs \(i\to j\) for \(i<j\), the exact empty-source certificate becomes

\[
C_{\mathrm{forward}}(0^{M'})=\binom n2-\lfloor n^2/3\rfloor.
\]

**Proof.** A SAT graph in this promise class is \(K_4\)-free after forgetting orientations: a transitive four-tournament needs a top color with three distinct outgoing neighbors, but T5 outdegree is exactly two. Turán's extremal theorem bounds edges by \(\lfloor n^2/3\rfloor\). Conversely partition the vertices into three consecutive, nearly equal intervals colored (0,3,1). These satisfy every forward cross-interval arc, since R(0,3), R(0,1) and R(3,1). Query only the within-interval bits and use the same exhaustive fallback on nonzero answers. QED.

For n=100 this certificate reads 1,617 of 4,950 forward arc bits. **Never import this promise as a bound for the unrestricted loopless directed input model.**

## Four falsifiers

1. The full ordered-pair and forward-only grammars give different exact formulas; including loops adds n compulsory bits.
2. OBDD nodes evaluate assignments after G is fixed. A source algorithm must acquire G, while an OBDD compiler must charge its construction. /092-/093 and /094 establish failures in both informal transfer directions.
3. These are individual source *bit-probe* lower bounds only, \(\Theta(n^2)\), of the same order as matrix input length. Word/batch accesses, preprocessing, authentication, cache, oracle answers and adaptive switching are not free. Full raw-source SHA-256 validation itself reads all matrix bits; experiment hashes are offline provenance, not advice available to a shorter online query transcript.
4. A polynomial empty-source certificate does **not** yield a polynomial all-input SAT decider. The upper construction's nonzero branch uses a valid but exponential-time fallback. No unrestricted deterministic time/space or adaptive FBDD lower bound follows.

## SAME_REALIZATION / conversion

The actual total deterministic algorithm parses the length header and fixed matrix format, builds balanced colors in O(n) work, computes ordered-pair addresses and their R values with O(log n)-bit counters, and probes forbidden bits. The all-zero path has \(\Theta(n^2)\) sequential work and q graph-bit reads; witness output is \(\Omega(n)\). It retains O(n) witness symbols and O(log n)-bit indices. When full syntax authentication or SHA is required, also charge \(\Theta(n^2)\) full-source reads and hashing. On a nonzero queried answer it reads the remaining source, uses \(O(n^2 5^n+n^2)\) upper time and O(n²+n) source/witness workspace, and verifies the decision. Source re-reads, failed paths, fan-out, sharing, storage, cache evictions, propagation and arithmetic must remain charged. No Z5/Fourier, tensor, adaptive switch or external SAT oracle is invoked for free.

For any fixed authenticated source with n variables and m present arcs, the direct 3-bit Boolean encoding uses 3n invalid-code clauses and 15m forbidden-pair clauses, total 3n+15m clauses and 9n+90m literal occurrences. The valid codes bijectively preserve original accepting and rejecting multiplicities. A contiguous three-bit block takes at most six binary decoder nodes per five-way decision node, but arbitrary interleaved Boolean FBDD transfer remains OPEN. All 32 unary mask pairs, both orientations, remain exactly valid-code-equivalent; no smaller asymptotic domain quotient is claimed.

## Four verification gates (finite, COMPUTATIONAL)

**Gate 1, source:** 5 full-matrix and 7 forward-only canonical authenticated zero-source hashes, 7+8 malformed source rejects, independent Python/JavaScript hash agreement.

**Gate 2, assignment semantics:** For full directed sources, every one of 1,052,741 digraph matrices n=1..5 evaluated in an exact original-five-color histogram. Python independently used superset-zeta aggregation; JavaScript independently enumerated every allowed-edge submask of each coloring. Their n-by-n SAT/UNSAT totals, maximum permitted edges, extremizer counts and empty-source assignment multiplicities agree. At n=5: 1,048,576 possible original digraphs; 33,369 SAT and 1,015,207 UNSAT, max 10 arcs attained by 24 graphs, empty-source count 3,125, certificate exactly 10 of 20 source bits. All 1,099 certificate completions n<=5 SAT. For forward-only, both implementations checked all 2,131,019 graph matrices n=1..7; n=7 has 709,097 SAT, 1,388,055 UNSAT and maximum 16 edges, with certificate 5 of 21 bits. All 69,931 forward certificate completions SAT.

**Per-source count-vector SHA-256 parity, stronger than aggregate agreement:** The independently executed Python superset-zeta and JavaScript permitted-submask algorithms produced byte-identical little-endian uint32 arrays containing the **exact satisfying-assignment count for every individual source matrix**. For full directed n=5 (1,048,576 original graphs), both SHA-256 digests were `8c595b6d2f0ec8dcde224da87cc962c4f7dfa38240c84c450accbde6ca0b70db`. For forward-only n=7 (2,097,152 original graphs), both were `f20bfbcf14057c332c2165f270d4b3b785379b13b03eb6105f9e87838e6216ea`. Parity for every smaller n also passed. All 12 exact vectors and digests are recorded at `results/raw/tmr/2026-11-18_TMR4_T5_SOURCE_CERTIFICATE094_PER_GRAPH_PARITY.json`. This proves code-output agreement for the finite tested cases, not the asymptotic theorem.

**Gate 3, binary and domains:** Full directed: 2,000 Python and 3,000 JavaScript actual CNF evaluations, including 1,389 invalid-code Python trials. Forward-only: 1,880 Python and 1,568 JavaScript CNF evaluations. Both languages independently check all 2,048 oriented domain-mask pairs in each model.

**Gate 4, repetition and independent algorithm:** Both implementations returned identical per-n graph statistics, canonical source SHA-256 values, certificate formulas and exact empty-source counts, with zero unexpected assertions. Python used fixed seeds 2026111894 and 20261118094; JavaScript uses deterministic fixed LCG seeds. Full reproducibility package includes all four actual executed source scripts, four raw JSON outputs, SHA256SUMS, standalone TeX theorem proof and successfully compiled 3-page standalone PDF. Local bare-repository preflight, full 4,000-line manuscript compilation, independent formal mathematical review and physical Turing microstep replay were not executed/established.

**Four foundational gates:** DISJ PASS as a cheap-source sanity control, not a rank lower bound; relativization OPEN for oracle-enriched arbitrary machines; simultaneous DTISP PASS only as a matched upper ledger on the declared execution, no forbidden region; deterministic configuration counting NOT APPLICABLE as a lower-bound step. Natural Proofs and algebrization are not crossed. P versus NP OPEN.

## Next dependency

**D4-T5-UNIFORM-DECIDER-ADVERSARY-095:** Seek an original-source, all-input, uniform-machine adversary that survives every legal source-aware shortcut and gives stronger-than-input-length decision cost, with a quantified SAME_REALIZATION conversion. The /094 source certificate does **not** supply that missing theorem.

References: [1] Turán's K4-free extremal theorem, \(\mathrm{ex}(n,K_4)=\lfloor n^2/3\rfloor\), modern supporting discussion C. Reiher, *K4-free graphs have sparse halves*, Bull. LMS (2023), https://doi.org/10.1112/blms.12782. [2] Barto, Kozik and Niven, *The CSP Dichotomy Holds for Digraphs with No Sources and No Sinks*, SIAM J. Comput. 38(5) (2009), https://doi.org/10.1137/070708093.