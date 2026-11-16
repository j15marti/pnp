# TMR-5/057 | 2026-11-15 20:50 PST | Independent end-to-end OR-of-bilinear-layers extension

**Governing protocol:** END_TO_END_AGENT_MANUSCRIPTS main blob 8451d955f6cd5397de0895f8ebb46e30818842c3. Owner: TMR-5 / PNP Machine Bottleneck Redteam. Scientific status: PROVED/EXACT RESTRICTED for the mathematical source-to-count construction, COMPUTATIONAL for executable finite checks, and independent mathematical peer review OPEN. P versus NP OPEN.

## Candidate fixed before inspecting source and primary references

**D2-OR-OF-BILINEAR-LAYERS:** For all authentic finite original-source DAGs in the following grammar, uniformly compile a complete source-to-exact-original-input-count (and optional strict proper-3CNF) chain with T(N,q)=O(2^q N^8) bit-machine steps and S_peak(N,q)=O(N^3) writable bits in the same single deterministic locally headed execution, where N is source bit length and q is the number of distinct root-reachable non-OR layer gates. The bound is polynomial for q=O(log N), but may be exponential for general q. It is an upper algorithm for a restricted circuit class, not a lower bound on SAT.

**Falsifiers:** F1 shared XOR children might be multiplied rather than canceled mod 2; F2 an OR DAG O(h,h) might cause exponential layer extraction or double count; F3 the vector of ranks of individual layers might fail to determine the OR count; F4 malformed numeric declarations, cycles and OR gates underneath XOR might bypass authentic-source checks; F5 functional CNF wiring might create multiple auxiliary assignments or lose duplicate operands. All were directly addressed.

## Entire authenticated model and source-to-output chain

Canonical ASCII source header: p norxor n a b g root. The following exactly g records are g id E u v, g id X j k, or g id O j k. E is the real AND of left original input u in 1..a and right original input v in a+1..n; X is XOR of two gate outputs; O is OR. Every original input appears in an E, and every gate is reachable from root. All gate IDs are unique and the dependency graph is acyclic, but records can be in arbitrary order. XOR gates may reference only E or XOR gates, never an O gate, so every maximal non-OR descendant is an XOR-of-bilinear-AND DAG. OR subgraphs may share arbitrarily, and repeated operands are legal. Authenticating the n<=2g necessary arity bound before any n-sized allocation prevents enormous invalid headers from causing disproportionate space usage. Canonical decimal, ASCII, bounds, source records, all-use, reachability, cycles and opcode restrictions are checked; invalid strings are rejected, not declared UNSAT.

After authenticating the graph, traverse the OR-reachable source subDAG once by ORIGINAL gate ID, yielding q distinct maximal non-OR layer roots. Duplicate OR references to the same source layer remain a single Boolean disjunct, which is justified by OR idempotence. For each layer i, reverse-propagate its GF(2) coefficient weight through the actual XOR shared DAG. Perform both child toggles even for X(h,h), and toggle an a-by-b GF(2) matrix A_i at each E leaf. This realizes the exact original function

F(x,y) = OR_{i=1}^q [ x^T A_i y (mod 2) ].

No unfolded formula tree, layer-evaluation oracle, choice of basis or duplicate-gate advice is supplied. Original identifiers and all parsing costs are paid.

## Rank-sum exact counting lemma and proof

For each subset J of {1,...,q}, let A_J be the XOR of the authentic matrices A_i for i in J, and r_J its GF(2) rank. Define n=a+b. Then the exact integer count of accepting original assignments is

    #F = 2^n - (1/2^q) * SUM_{J subset [q]} 2^(n-r_J).

**Proof.** For Boolean b_i(x,y)=x^T A_i y, the zero-indicator is (1+(-1)^b_i)/2. Multiplying all q zero-indicators and expanding gives 2^-q sum_J (-1)^(x^T A_J y). For fixed x, the inner sum over all y is 2^b when A_J^T x=0 and zero otherwise. There are exactly 2^(a-r_J) such x, giving character sum 2^(n-r_J). Summing and dividing yields exactly the number of assignments on which every b_i is zero. Subtracting from 2^n yields #F. The numerator is necessarily divisible by 2^q; this is an exact integer identity, not a numerical approximation. For q=1 it reduces to the earlier TMR-2/059 rank formula, including rank zero.

A Gray-code pass through 2^q subsets updates the combined matrix by XOR with ONE source-derived layer matrix each time and computes r_J by exact GF(2) Gaussian elimination. No 2^q matrices are retained. One fixed, locally headed deterministic bit machine can scan and validate the N-bit source, construct/store all q matrices and a combined matrix, compute and accumulate the integers with O(n+q) bits, optionally output the functional CNF, and print the n+1-bit exact count. A conservative same-realization cost envelope, charging source reads/seeks, full parser, DFS/topology, every shared edge, q source-to-matrix traversals, subset-Gray counter, matrix bit operations, q-bit divisor, BigInt-sized integer additions, output and reject paths, is

    T_total(N,q) = O(2^q N^8),   S_peak(N,q) = O(N^3),  q<=g<=N.

In particular, q=O(log N) yields polynomial-time exact count on this declared genuine shared circuit grammar. The finite Node source is a test implementation, not an instrumented all-length physical multitape microcode.

## Complete parsimonious gate-CNF interface

Associate one wire variable z_i with each ORIGINAL gate and three distinct pin variables p,r,s, all uniquely forced to 0 by seven proper ternary clauses forbidding all nonzero pin assignments. For every E gate impose (not z or x_u or p), (not z or y_v or p), (z or not x_u or not y_v). For distinct-child XOR impose the four standard 3-literal functional XOR clauses; repeated child XOR forces z=0 with (not z or p or r). For distinct-child OR impose (z or not a or p), (z or not b or p), (not z or a or b); repeated-child OR imposes (not z or a or p) and (z or not a or p). Finally impose (z_root or p or r). All clauses have three distinct variables, including for repeated operand IDs. Topological induction gives EXACTLY ONE extension of every original input vector to all gate and pin variables, and the final unit-equivalent clause accepts iff the authentic source output is 1. Thus

    V=n+g+3, m<=4g+8, #3CNF=#F.

This conversion is linear in original gate records and not an exponential circuit unrolling. The CNF counts all variables, including the uniquely fixed auxiliaries. A different count-normalization shortcut remains legal.

## Minimal full-chain hostile tests

Source A (two rank-one layers sharing the same y):
    p norxor 3 2 1 3 3
    g 1 E 1 3
    g 2 E 2 3
    g 3 O 1 2

Each layer has rank 1; their XOR has rank 1. The subset rank multiset is [0,1,1,1], hence #F=8-(8+4+4+4)/4=3.

Source B (same individual rank vector but algebraic cancellation):
    p norxor 3 2 1 5 5
    g 1 E 1 3
    g 2 E 2 3
    g 3 X 2 2
    g 4 X 1 3
    g 5 O 1 4

Each layer still has rank 1, but A_1 XOR A_2 has rank zero, so subset ranks are [0,1,1,0], #F=8-(8+4+4+8)/4=2. All source gates and all three original inputs are genuinely root-reachable. Therefore **the q individual ranks alone cannot determine exact OR count**; the cross-layer subset-rank profile is necessary for this particular formula. This is a smallest low-dimensional counterexample to that proposed summary, not an unconditional lower bound on every other algorithm.

A 90-deep genuine shared OR(h,h) chain has 91 actual gate records, only one distinct layer, and exact #F=1; naive tree unrolling is not charged as mandatory work. The independent verifier also tests XOR(h,h), an OR layer functionally duplicated with distinct IDs, all small assignments, full auxiliary CNF satisfying assignments on three cases, shuffled source records, 8 malformed input controls, and 63 small generated sources.

## Independent executable evidence and provenance

Actual local Node v22.16.0 executed source revision TMR5_OR_BILINEAR_E2E057_v1, seed 20261115 (deterministic enumerations), 236 assertions, 68 whole original-input brute comparisons, 3 full auxiliary-extension enumerations, 8 malformed-source rejections and zero failed assertions. Raw includes the two quoted original literal source encodings and rank histograms. All full-CNF tests enumerate entire extended assignments, not merely assume functional mapping. No native all-length TM microcode, Lean, Mathlib or LaTeX build was executed. No local Git checkout existed, so the repository preflight was NOT run. The published source is expected to match local Git blob 3dfc3f783485a8ea2675d926099687961ab6acad, and raw to match 94ce773a04459dcf955fc0fcdd250d480e3384ab; verify on branch and after merge independently.

Primary and original project references: TMR-2/059 original report, source blob d5da510006f68d4eee0089a14a54c9aea271cc9f and raw blob 172a416a702ae1a33ab330edc8b8ef518a401811; TMR-4/061 certified shared-DAG source compiler, report blob e0fffd688b929a4ce4b13a156e5a18890e28eef0; classical finite-field bilinear forms Delsarte, Journal of Combinatorial Theory A 25 (1978), DOI 10.1016/0097-3165(78)90015-8; exact functional Tseitin gate encoding as reproduced in the TMR-2 original and the standard Tseitin transformation. These sources supply background, not a claim of a new general lower bound.

## Ranked peer dependencies and mandatory four gates

| Chain | Verdict | Blocking next arrow |
|---|---|---|
| TMR-1 pinned #SAT theorem, fixed machine, JMV and E^NP transfer | RESTRICTED/CONDITIONAL | Independent Lean 4.33.1 kernel/nanoda, transitive axioms and exact standard-machine translation; NP-class bridge OPEN. TMR-1/060 density guard corrected on draft branch, not mistaken for an upstream proof failure. |
| TMR-2 authenticated XOR-bilinear to exact count | PASS restricted, extension PROVED/EXACT | The named D2-OR-OF-BILINEAR-LAYERS source-to-count dependency is now covered for the declared grammar and q; arbitrary mixed XOR-after-OR and universal dynamic lower-bound transfer OPEN. |
| TMR-3 source-authenticated checkpoint plus evaluator | PASS selected restricted services | Arbitrary work-dependent adaptive provider and genuinely improved general evaluator OPEN. |
| TMR-4 certified shared-core DAG to OBDD | PASS restricted | Many-share low-width discovery and all-equivalent-circuit reverse necessity OPEN. |

| Promotion gate | Verdict | Reason |
|---|---|---|
| DISJ sanity | PASS restricted | High static rank of DISJ is compatible with its linear-size circuit; no static rank-to-general work lower bound is used. |
| Relativization | PASS local intermediate; unrestricted OPEN | This exact algebraic counting algorithm is relativization-neutral. No nonrelativizing NP separation is claimed; BGS, algebrization and Natural Proofs remain barriers to any future separation claim. |
| Simultaneous DTISP | PASS restricted upper, lower transfer OPEN | One source-to-count execution meets the joint T and S ledger above. No strict forbidden resource pair or network-parallel shortcut is inferred. |
| Deterministic configuration counting | PASS upper-only | The fixed total read-only-input deterministic machine obeys T<=2^O(S+log N); this is not a lower bound and gives no quantum/randomized runtime implication. |

Additional controls retained: Horn and 2-SAT, affine/Gaussian, bounded treewidth, equality, autarkies, independent products, padding, auxiliaries, unique-solution rank-one indicator tensors, Valiant-Vazirani random isolation, alternate bases/field characteristics and compact circuits. A Walsh-Hadamard matrix is noninvertible in characteristic 2; our use of integer ±1 character sums is distinct from a claim of invertibility over GF(2). Historical /341 remains FAIL as full logical UNSAT authority and /386 remains RESTRICTED.

**ONE highest-value next target:** Independent clean rebuild of the pinned Anthropic MainResults.mainTheorem with Lean 4.33.1, PrintAxioms and nanoda, followed by the complete physical FinTM2-to-E^NP interface replay. This remains more consequential than this restricted exact-count closure. No P vs NP proof is claimed.
