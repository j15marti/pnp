# TMR-2/063: end-to-end quadratic symbolic compiler for authentic shared AND/OR DAGs

**2026-11-16 01:05 PST**, America/Los_Angeles. Owner TMR-2 / PNP Information Necessity, Track A. Governing coordination: research/coordination/2026-11-15_END_TO_END_AGENT_MANUSCRIPTS.md. Status **PROVED/EXACT for the precisely authenticated degree-two-relative circuit class**, with actual finite verification **COMPUTATIONAL**, external mathematical review **OPEN**. P versus NP **OPEN**.

## Predecessor reconciliation and precise candidate

The TMR-2/062 main-merged result handles conditional raw affine expressions with source gate R and costs O(4^d N^12) time, O(N^3) space. Independently, TMR-5/061 on **draft PR #199, not main**, establishes a separate *typed pair-monomial gate* Q whose coefficient depends on a bilinear interface w, and proves O(4^d N^14) counting. That result **already closed the original D2-CONDITIONAL-RAW-QUADRATIC dependency in its restricted grammar**; the present work does not claim to be first to derive its character identity.

**New dependency D2-RELATIVE-DEGREE-TWO-COMPILER:** For every authenticated source in the new canonical p d2poly grammar, compile unrestrictedly shared XOR/AND/OR/NOT gates including genuine **raw-to-raw AND/OR of affine expressions**, provided the source-derived *syntactic relative-degree certificate* stays <=2. Construct the polynomial for every genuine source gate for each interface word, carry a bilinear GF(2) basis, and calculate exact original-input #accept in O(4^d poly(N)) time without truth-table expansion or preloaded coefficients. The grammar is a **strict source-level extension** beyond pair-monomial Q gates; it makes no semantic claim beyond a sound sufficient certificate.

Potential falsifiers established before corpus/source review: (1) an AND/OR of raw-dependent gates is accidentally treated as merely affine; (2) z_i^2=z_i, repeated references, shared cancellations or inaccessible interface vectors alter count; (3) malformed syntax, undischarged reachability and nonuniform basis advice avoid real input costs; (4) an alleged polynomial-workspace implementation actually retains a 2^d table or O(g n^3) bits of unpacked monomial indices.

## Authentic encoded source and uniform algorithm

A source is one canonical ASCII string ending in exactly one LF with header p d2poly n a b g root, where n=a+b, a,b>=1, n<=2g and g>=1. There are exactly g gate records with distinct IDs 0,...,g-1 in any physical order, each root-reachable, acyclic and with valid references. Every original input appears in an E or I leaf. E id i j computes the bipartite original-input AND x_i AND y_j; X id u v is XOR of two E/X early gates, with no mixed child; I id i reads one actual original input; N id u negates any gate; A/O/P id u v are ordinary binary AND/OR/XOR of arbitrary shared predecessor gates. A source with any gate exceeding the certified degree bound is outside the accepted promise and is rejected by this recognizer. No input is an uncharged oracle, auxiliary guess or preloaded tensor.

The **relative-degree** grammar gives E/X degree 0, I degree 1, N degree of its input, P the maximum of child degrees and A/O the **sum** of child degrees. It rejects a calculated value above 2. The degree is a sufficient syntactic bound, not a purported computation of minimal ANF degree. Notably, A and O may consume outputs of earlier raw-dependent A/O gates provided the degree rule passes, so the source includes actual reconvergent sharing and raw-to-raw products.

Pipeline: authenticate all N input bytes, delimiters, canonical numeric addresses and gate records; DFS/toposort root, reject disconnected records/cycles, check coverage and relative degree; build one ab-bit matrix for every early E and X; Gaussian-eliminate the actual early matrices into residual basis B_1,...,B_d and compute each gate's exact coordinate mask; stream w in GF(2)^d; evaluate the actual shared source in the Boolean quotient ring GF(2)[z_1,...,z_n]/(z_i^2-z_i), with early values replaced by their mask dot w; emit the root's degree<=2 ANF polynomial p_w; stream lambda in GF(2)^d; XOR the bilinear character sum_j lambda_j B_j into p_w; calculate its exact signed quadratic character by pair elimination; accumulate an integer, normalize exactly, output the original-input count, and decide by comparison to zero. Source order and repeated gate references are authenticated and shared source identities retained, not expanded into trees.

## Theorem 13: exact count and proof

For every accepted source, let z=(x,y) be its n **original** input bits, let w_j(z)=x^T B_j y, and let p_u(z) be the actually constructed formal root polynomial at supplied interface coordinates u. The source induction proves pointwise C(z)=p_{w(z)}(z), despite possible unrealizable u. For quadratic Q, write H(Q)=sum_{z in GF(2)^n}(-1)^{Q(z)} as a signed integer. Exact Fourier character orthogonality gives

    #C = [2^(n+d) - sum_(u,lambda in GF(2)^d)
          (-1)^(lambda dot u) H(p_u + sum_j lambda_j w_j)] / 2^(d+1).

The proof substitutes 1[w(z)=u] = 2^(-d) sum_lambda(-1)^(lambda dot (w(z)+u)) into sum_z(-1)^{C(z)}, then applies #1=(2^n-signed_gap)/2. The denominator divides the numerator exactly for all accepted sources. It counts the n original variables once each; there is no overlooked Tseitin multiplicity or promise that u is reachable.

For a nonzero pair monomial z_i z_j, write Q=z_i z_j+z_i A(t)+z_j B(t)+R(t), with t the remaining variables, affine A/B, quadratic R. The **exact** integer identity

    sum_(z_i,z_j in GF(2)) (-1)^Q = 2(-1)^(R(t)+A(t) B(t))

removes the pair and reduces the remaining quadratic degree without increasing it. Repeated reductions leave an affine character, with sum 0 if any residual linear coefficient is 1, else +/-2^remaining. Every original repeated-variable product is folded using z_i^2=z_i. This computes signs as well as magnitudes. All computations take integer place, not an erroneously invertible Walsh basis over GF(2).

## Simultaneous source-to-output resource ledger

N is the entire actual byte length, g,n,d<=O(N). One fixed, deterministic, locally headed multitape realization can use **dense, packed square-free coefficient vectors of 1+n+binomial(n,2) bits per gate**, rather than the prototype's bigint-key Set objects. The g live per-word gate vectors and up to g early ab-bit matrices each occupy O(g n^2)=O(N^3) physical writable bits. A streamed d-bit u, d-bit lambda, one quadratic polynomial, a polynomial number of addresses/heads, source buffers, topological metadata and an O(n+2d)-bit exact signed accumulator fit in O(N^3) **simultaneous** bits. Re-reading, cache eviction, failures and sharing are included; no 2^d entries or duplicated gate trees reside in memory.

Parse/validate/DFS/degree certification, discovery of the early matrices and basis, and all source seeks take polynomial bit work. For each of 2^d streamed u, replay every actual shared gate using dense XOR and degree-<=2 multiplication/OR, with explicit coefficient and index costs. For each of the resulting 4^d ordered (u,lambda) pairs, construct the character quadratic, perform at most n/2 coupled-pair reductions, process signed O(n+2d)-bit integers and add to the exact accumulator. The full locally headed source, address and scratch sweeps fit a deliberately conservative O(N^14) bit-operation envelope **per pair**, including startup and output overhead. For this one implementation,

    T(N)=O(4^d N^14),      S_peak(N)=O(N^3).

The exact-count and decision algorithm is polynomial-time when the *constructed* d=O(log N), on this accepted family. An arbitrary circuit may have d=Theta(N) or fail the relative-degree certificate, so no universal polynomial-time Circuit-SAT claim is implied. The reference Node/V8 implementation uses BigInt Set objects and a finite d<=8 test cap; it is a semantic test harness, **not** the claimed packed-bit physical machine or a Turing-machine microtrace.

## New test and countercontrol evidence

Actual hosted V8 execution of revision TMR2_D2POLY063_v1, deterministic 32-bit xorshift seed 20261116: **100 authenticated cases, 99 exhaustive original-input comparisons, 105 counted assertions, 3 negative-source controls, 1,840 exact character calls, 0 failures**. All 96 seeded cases include authentic mixed raw AND/OR, repeated source operands and shared fan-out; small-case outputs are checked against an independent direct gate-by-gate evaluation over all original assignments. The actual published source was fetched and re-executed in hosted V8; raw JSON reproduced **byte for byte**.

DISJ_4 is built by four authentic E edge gates followed by source NOT and AND; it counts **3^4=81** accepting assignments out of 256, not a hard general circuit. A repeated raw gate A(I_i,I_i) tests Boolean square folding. A degree-three raw product is correctly rejected. In an authenticated 64-original-variable, 197-gate source with raw-to-raw products, shared zero-cancellation references and discovered d=1, the count is exactly 2^60=1,152,921,504,606,846,976, with **four** streamed character evaluations, not 2^64 assignments. Exact source bytes N=2151. This count also follows analytically because x_0 y_0 must be 1 and each of two disjoint raw parity pairs must be 1, a combined fraction 1/16. Tests are COMPUTATIONAL, not asymptotic theorem verification.

**Published artifacts** on branch tmr2-20261116-0105-degree2-symbolic063, until separately confirmed merged:

- experiments/tmr/tmr2_degree2_symbolic_e2e063.js; Git blob 7c6f830087e4fb237b5d293957f6fda80d0ff655
- results/raw/tmr/2026-11-16_0105_TMR2_D2POLY063_NODE_RAW.json; Git blob 040bf834a6fc1a6c8e60eaadf493a87229fd9d4a
- current report and living manuscript, SHA and branch revision verified separately on publication.

No local git checkout/preflight, physical TM microcode, repository-wide tests or full LaTeX compilation were executed. Independent external mathematics review is OPEN.

## Four mandatory gates and hostile controls

| Gate | Verdict and precise reason |
|---|---|
| DISJ sanity | **PASS restricted**. Exact DISJ4 accepts 81/256, has a cheap 2-CNF circuit, and no general circuit lower bound is drawn from static rank. |
| Relativization | **PASS for intermediate algebraic upper theorem only**. A general NP separation would require an explicit nonrelativizing step and separate algebrization/Natural Proofs audits; that bridge is **OPEN**. |
| Simultaneous DTISP | **PASS for one restricted time/peak-space upper realization**. No strict forbidden time-space pair, transfer to arbitrary machines or lower bound is asserted; those are **OPEN**. |
| Configuration counting | **PASS as an upper-only consistency guard**, T<=2^O(S+log N) for fixed deterministic total read-only-input machines. Not a compulsory-work lower bound or a randomized/quantum claim. |

Horn expanders, 2-SAT, affine/Gaussian, bounded treewidth, equality, autarky, independent products, padding and auxiliary gates, unique-selector projections, unique-solution rank-one tensors, local-basis rank invariance, characteristic-two Walsh singularity and genuine compact sharing remain legal shortcuts. Most were **not** exhaustively executed in /063; no transfer is claimed on them beyond source semantics. Direct source logic and exact count are distinct from fixed-formula assignment matrices and SAT on encodings. Historical /341 is FAIL as a general UNSAT authority and /386 is RESTRICTED.

## Dynamic interface for TMR-4 and one next dependency

**D2-RELATIVE-D2-TRACE** is an execution-sensitive *correctness* invariant: canonical source IDs, real arc multiplicities and actual topological order; certified degree for every gate; actual early matrices and derived pivot/coordinate masks; the streamed u; the actual dense quadratic gate coefficients and idempotent product transitions; streamed lambda and combined character quadratic; signed pair-elimination records; exact accumulator, division and output. Required transitions are SOURCE_READ, PARSE, DFS, DEGREE_CHECK, MATRIX_XOR, PIVOT_INSERT, MASK_DECODE, GATE_READ, POLY_XOR, POLY_AND, POLY_OR, NOT, FOLD_SQUARE, BUILD_CHARACTER, PAIR_ELIM, AFFINE_TAIL, BIGINT_ACCUM, DIV_EXACT, CACHE/DROP/RECOMPUTE/SWITCH and OUTPUT. All physical accesses, sharing and attempts must be charged; no solver is forced to follow this trace.

**ONE NEXT LEMMA, D2-CERTIFIED-DEGREE-COMPRESSION (OPEN):** Build or falsify a uniform *source-certified* cancellation-aware representation that admits genuine mixed gates whose naive relative degree exceeds two but whose square-free polynomial degree remains <=2, without using exhaustive truth-table equivalence or an uncharged semantic-minimization oracle. State the exact construction cost and prove that source-selected graph sharing does not cause exponential polynomial expansion. A mere low actual ANF degree without a paid certificate is not sufficient.

References: (1) O'Donnell, Analysis of Boolean Functions (2014, corrected arXiv:2105.10386, Ch. 1); (2) TMR-2/062 original report on main; (3) TMR-5/061 original report on draft PR #199, research/agents/tmr-5/2026-11-16_0035_TMR5_CONDITIONAL_QUADRATIC_E2E061.md, blob f88132e2b8fac173d0e78d96577fd03b67e5b282. The Fourier and pair-elimination identities are proved here and are not claimed as new independent mathematical discoveries.
