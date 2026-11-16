# TMR-2/066: source-constructible live spectral projection

Date: 2026-11-16 07:12 PST. Owner: TMR-2 / PNP Information Necessity, Track A. Governing directive: research/coordination/2026-11-15_END_TO_END_AGENT_MANUSCRIPTS.md. Status: **PROVED/EXACT for the declared restricted mathematical source grammar; independent external mathematical review OPEN**. Actual finite evidence **COMPUTATIONAL**. P versus NP **OPEN**.

## Named dependency, pre-search candidate and falsifiers

**D2-LIVE-SPECTRAL-PROJECTION: CLOSED for the accepted /065 cancellation-certified source class.** The input is a genuine canonical `p d2poly n a b g root` circuit with early bipartite E/X bilinear gates and late shared I/N/A/O/P Boolean gates, all original inputs and source gates authenticated, unique gate IDs, arcs, coverage, root reachability and acyclicity. The source parser, original Gaussian basis B_1,...,B_d, source IDs, parity bitmap and canonical AND atom normalization are exactly those in /065; no semantic oracles or uncharged virtual coordinates are added. For certified relative raw-degree at most two, construct the smaller span of bilinear *linear masks actually present in the surviving root's parity words and its retained AND operands*, and count by exact integer quadratic characters using that effective dimension r.

Falsifiers specified before primary-source/corpus verification: (F1) a linear mask used in a shared, nontrivial retained AND operand is missed by scanning only the output; (F2) GF(2) basis selection or re-expression is incorrect when source or retained masks are dependent or pivot order varies; (F3) treating formal features as free original assignments corrupts counts, especially unreachable formal words and a zero-dimensional projection; (F4) preprocessing, canceled branches, exact coefficient bit lengths or retained shared state force exponential work in the original source dimension d. The theorem addresses all four for the declared implementation and certificate. Its sound-but-incomplete mask extraction can overestimate the *semantic* minimal dimension.

## Exact pipeline and newly closed dependency

**Source and semantic domain.** Given the original ASCII source of full length N, authenticate bytes, g gate records, n=a+b original input identities, unique integer IDs, stage types, all genuine edges, all arcs, full reachability and a discovered topological order. Reject malformed inputs INVALID. Compute each actual early bilinear matrix A_t and a GF(2) independent basis B_j with coordinate masks for every early gate. Source-normalize to the /065 shared parity-and-interned-AND atom DAG. If its genuinely normalized root has certified relative raw-degree above two, report OUTSIDE, never UNSAT. Preserve all actual original gates, repeated child references, normalization lookups and canceled high-degree work in the charged construction.

**Mask discovery.** Each parity bitmap V denotes constant XOR original raw-input atoms XOR already constructed AND atoms XOR formal coordinates W_j. Let m(V) in GF(2)^d denote the mask of its W_j atoms. Traverse the exact normalized root V_root and, for each AND atom reachable from it, its two stored parity operands V_left, V_right. Form the list M of their masks. At most 2g+1 words occur (repeated occurrences are charged), and every live W dependency enters at least one such word. Perform *fully charged high-pivot Gaussian elimination* on these masks to form independent row masks h_1,...,h_r, with r=rank(M)<=d, and explicitly reconstruct the coordinate of every encountered mask in that row basis. No minimization of arbitrary Boolean semantic dependence is assumed.

Define the actually computed bilinear matrices D_i=sum_j h_ij B_j over GF(2), and true features v_i(z)=z_L^T D_i z_R. The original B_j are independent, so the D_i are independent matrices too. At each source normalized parity word, its formal part m(V).w is **exactly** the XOR of coordinate-selected v_i values. Rewriting only these formally linear masks, retaining original raw and shared-AND identities, yields a source-constructed G(z,v) with the pointwise identity for every real original assignment z,

    C(z)=G(z,v_1(z),...,v_r(z)).

This is a structural induction through shared AND semantics, not a claim that every formal w in GF(2)^d is independently realizable. It accounts for arbitrary source fan-out, duplicate operands, internal cancellations and nonlinear AND/OR between the masks. The sound previous degree certificate is unchanged since v replaces formal raw-degree-zero linear masks; for fixed formal v=u, G(z,u) specializes to an exact quadratic square-free polynomial p_u(z).

**Exact count.** For u,lambda in GF(2)^r, put

    Q_(u,lambda)(z) = p_u(z) + sum_i lambda_i z_L^T D_i z_R.
    H(Q) = sum_(z in GF(2)^n) (-1)^Q(z).

The same explicit integer coupled-pair Gaussian character reduction as /063-/065 computes H(Q) in polynomial bit-time. Orthogonality on the **actually computed** features gives

    #C = ( 2^(n+r) - sum_(u,lambda) (-1)^(lambda.u) H(Q_(u,lambda)) ) / 2^(r+1).

Proof: for each original assignment z, 1[v(z)=u] = 2^(-r) sum_lambda (-1)^(lambda.(v(z)+u)). Substitute G(z,v(z)), expand the signed acceptance gap, exchange finite sums and divide by exactly 2^(r+1). Every original z is counted once. The expression is integral. No early feature, internal circuit wire or parsimonious 3CNF auxiliary bit becomes an independently counted assignment. SAT for the accepted class is YES iff #C>0.

**Cost and model.** On the same fixed locally headed deterministic multitape realization, the complete original source parser/authenticator, all g actual E/X matrix operations, original d-basis and coordinates, AND intern/cache lookups and misses, cancellations and full live-ancestor scan are paid. Form at most 2g+1 masks of at most d<=N bits, run polynomial Gaussian elimination with exact coordinate checks and construct r<=d matrices of ab<=N^2 bits. Retain at most O(N) shared atoms and O(N)-bit parity vectors, O(N) actual early matrices, live scratch for O(N) packed quadratic monomials, head/address/index buffers, signed O(N+r)-bit character sums and an O(N)-bit exact-count accumulator. Stream 4^r terms without materializing a 4^r table; unsuccessful accesses, output, conversion and recomputation are charged. One conservative uniform bit-machine ledger is

    T(N) = O(N^14 * 4^r),   S_peak(N)=O(N^3).

The polynomial preprocessing is included since 4^r>=1; source d may be linear in N even when r=0. The host V8 reference has a test-only r<=8 cap and safe-JS-number source address bounds; the asymptotic theorem is for the defined bit-machine implementation, not for an executed native physical TM.

**TMR-4 transition invariant D2-LIVE-PROJECTION-TRACE.** An execution state contains authenticated original gate IDs/arcs and source cursor; all genuine early matrices, d-basis and coordinate masks; canonical normalized source-gate parity bitmaps and AND lookup hit/miss records; retained live AND-atom DAG and degree certificate; the complete root-plus-retained-operand mask stream M; row-echelon projected basis h_i and checked coordinates; newly constructed bilinear D_i; streamed projected u and lambda; the exact quadratic coefficient vector p_u and Q; pair-elimination state; signed accumulated character and exact final division/output. Allowed paid transitions READ/PARSE/DFS, EARLY_MATRIX/BASIS/COORD, NORMALIZE_AND_LOOKUP/CREATE/PRUNE, LIVE_WORD_SCAN, PROJECTION_INSERT/REDUCE/COORD_VERIFY, FORM_D, STREAM_U/SUBSTITUTE, STREAM_LAMBDA/QUADRATIC_CHARACTER, BIGINT_ACCUM/DIV, CACHE/DROP/RECOMPUTE/SWITCH and OUTPUT. It is a sound upper-algorithm invariant, not necessary materialization for every SAT algorithm. TMR-4's alternative compact representations remain legal.

## Reproducible evidence, executed tests and smallest controls

Actually executed a self-contained V8 JavaScript revision **TMR2_LIVE_SPECTRAL_PROJECTION066_v1**, deterministic xorshift seed **20261116**, by evaluating the *complete generated source body*. Its console-printing source was published and read back byte-exactly from the branch. The original /065 parser, normalizer and quadratic-character kernel are retained; the new projection and specialization are executed on every accepted source, including formal dimension r=0. **93 authenticated counted cases, 92 independently exhaustive original-input comparisons, 741 exact integer quadratic characters, 3 negative/malformed-source controls, zero failed checks**. No cryptographic randomness or unexecuted test is claimed.

Source: experiments/tmr/tmr2_live_spectral_projection066.js (blob SHA 563e7c3451ef793269fd32222eba079827b117a1). Immutable raw: results/raw/tmr/2026-11-16_0712_TMR2_LIVE_SPECTRAL066_V8_RAW.json (blob SHA 34ce9a7ccbf01e44492216e5a604ea5adace44cd).

A genuine n=64, g=137, N=1379 source with canceled high-degree raw conjunction has original d=2, projected r=1, five live normalized atoms, **4 rather than 16 character evaluations**, exact #C=2^60=1,152,921,504,606,846,976. The explicit n=8 non-axis parity-mask inside AND has d=2, r=1, 4 characters and #C=24, checked against brute original assignments. A two-independent-mask control returns d=2, r=2, 16 characters and #C=56. The canceled-output control has d=2, r=0, one character and #C=0. DISJ_4 has d=r=4 and counts 81 of 256 original assignments; compression correctly makes no false improvement there. The output counts original assignments, not auxiliary extensions.

## Four gates, mandatory adversaries and barriers

| Gate | Status / reason |
| --- | --- |
| DISJ sanity | **PASS restricted.** DISJ_k controls for k=1..4 count 3^k exactly with r=d=k; high static assignment rank is not converted to mandatory universal work. Any such lower-bound inference remains FAIL. |
| Relativization | **PASS for the restricted algebraic upper construction, OPEN for a nonrelativizing unrestricted lower-bound bridge.** BGS relativization, algebrization and Natural Proofs not overcome. |
| Simultaneous DTISP | **PASS for the same-run restricted upper ledger, OPEN for a universal necessary-work/lower-bound transfer.** This source recognition is not a forbidden time-space pair for arbitrary 3-SAT machines. |
| Deterministic configuration counting | **PASS as an upper-bound consistency guard only**, T<=2^O(S+log N) for a total deterministic read-only-input realization; not a computational lower bound and not automatically quantum/randomized. |

Mandatory hostile family permissions remain explicit: Horn expanders, 2-SAT, affine/Gaussian, bounded treewidth, equality, autarky, independent products, padding, auxiliary variables, unique-selector projection, scalar-count normalization, unique-solution rank one, compact shared circuits and adaptive alternative algorithms. The executed subset is stated above; the rest are **OPEN as exhaustive cross-family tests**, not falsely claimed completed. Invertible local changes of bilinear basis preserve the rank of actual matrices over GF(2); this does not preserve numerical rank across different fields. Integer Walsh orthogonality is not an invertible Walsh basis change in characteristic two. Valiant–Vazirani randomized isolation has charged trials and is not invoked. No majority-tie, quantum error/amplitude or SAT-to-UNSAT reduction is imported. Historical /341 remains FAIL as a full logical UNSAT authority and /386 is RESTRICTED.

Sources/pins: original /065 paper report at research/agents/tmr-2/2026-11-16_0520_TMR2_CANCEL_CERT_SPECTRAL_COMPOSITION065.md; exact source code/blob above; Ryan O'Donnell, *Analysis of Boolean Functions* (Cambridge University Press 2014; corrected author manuscript arXiv:2105.10386, Chapter 1, https://arxiv.org/abs/2105.10386); Bryant (1986), DOI 10.1109/TC.1986.1676819 for shared Boolean manipulation. All new character and rebasing identities are proved directly; external literature is context, not a borrowed black-box theorem. The current peer TMR-4/062 live-core compiler and TMR-5/057 OR-bilinear counter are distinct restricted pipelines, not replacements for this source parser.

No local repository checkout existed, so the updated repository preflight was **not run**. No physical TM microtrace, native Node binary execution, full LaTeX build, independent kernel/formal verification or external mathematical peer review was run. The local branch publication/readback and the V8 evaluation of the full generated JS source **were executed**. A GitHub main merge must be checked separately; a branch commit does not establish main publication.

## ONE next dependency

**D2-PROJECTED-CERTIFICATE-COMPLETENESS (OPEN).** Within the same restricted source family, construct a charged *strictly stronger* sound syntactic quotient that can expose identities such as (W_1 AND x) XOR (W_2 AND x) = (W_1 XOR W_2) AND x before projection, without a semantic-equivalence oracle or exponential ANF. Prove when such factoring is polynomial and whether it reduces the projected dimension on genuine shared circuits. Do not claim an unrestricted semantic minimizer (the /064 coNP-completeness barrier remains).

END_OF_REPORT::TMR2::066
