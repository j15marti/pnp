# TMR-5/061: conditional quadratic raw-input counting, end to end
November 16, 2026, 00:35 PST. Owner TMR-5, independent cross-track review. Dependency **D2-CONDITIONAL-RAW-QUADRATIC** from TMR-2/062. **PROVED/EXACT RESTRICTED** symbolic construction, external mathematical review **OPEN**; Python verification **COMPUTATIONAL**. P versus NP remains **OPEN**.

## Candidate, exact quantifiers and falsifiers
For **every** accepted canonical finite ASCII `p nquad n a b g root` source with `n=a+b`, `a,b>=1`, `g>=2`, `n<=2g`, root-reachable acyclic shared gates, and every original n-bit assignment, there is one uniform deterministic source-to-exact-count algorithm. Let `N` be the **entire** encoded source length, and `d` the **constructed**, not supplied, F2 dimension of the early bipartite bilinear interface. There is a fixed locally headed deterministic multitape implementation satisfying jointly `T=O(4^d N^14)`, `S_peak=O(N^3)`. Polynomial-time follows when `d=O(log N)`, only within this typed grammar.

Four prospective falsifiers: (1) a post AND/OR reads a raw quadratic value and silently creates uncontrolled high degree; (2) a repeated raw variable `z_i*z_i` is mishandled rather than reduced to `z_i`; (3) dependent early matrices, unattainable interface words, canceling shared XOR edges, or negative character signs corrupt the integer count; (4) acquisition, dimension discovery, 4^d character calls, quadratic elimination, live state, integer precision, output or malformed parsing silently exceed the declared matched ledger.

## Source grammar and full pipeline
One header line `p nquad n a b g root`, exactly g uniquely numbered canonical records in arbitrary order, and exactly one final LF. `E id i j` evaluates `x_i AND y_j` for `i<a,j<b`; `X id u v` is XOR of two earlier-**phase** E/X gates (DAG order may be arbitrary). `O/A/P id u v` and `N id u` are OR/AND/XOR/NOT of only early/post values. `R id i ctrl` is original bit `z_i` AND an early/post control; `Q id i j ctrl` is `z_i AND z_j AND ctrl` with ctrl early/post. `Z id u v` is XOR over early/post/raw R/Q/Z outputs; the root must be Z. All gate IDs have actual source records, no source gate is unreachable, every original input occurs in an E/R/Q record, and integer syntax, exact arity, types, phases, IDs, ranges, acyclicity and `n<=2g` are authenticated before size-dependent allocations. Post O/A/P/N and Q controls may **not** consume R/Q/Z. No oracle, advice or preloaded checkpoints.

The pipeline is: read all bytes -> reject malformed source -> DFS/toposort the actual shared DAG -> construct genuine GF2 edge matrices for E and XOR for X -> discover a basis `B_1,...,B_d` and coordinate words for every early interface -> for each `w in F2^d` execute the actual post shared-DAG control values and construct a quadratic `p_w(z)=c(w)+l(w).z+sum_{i<j}q_ij(w)z_i z_j` -> for each `lambda in F2^d` XOR its bipartite matrix `B_lambda` into the raw quadratic pair coefficients -> calculate its exact signed quadratic character -> accumulate over all 4^d pairs -> divide an exact integer and emit the n+1-bit original-assignment count. Gate sharing is charged once in physical source objects; repeat uses and replay are paid.

## Symbolic exact count, no lost original-input multiplicity
Define `w_j(z)=x^T B_j y` over F2 and let `G(Q,l)=sum_{z in F2^n}(-1)^(z^T Q z+l.z)` (read the quadratic in canonical square-free monomials). For `Q(w)` and `l(w)` read from the genuine typed source, set `Q_{w,lambda}=Q(w) XOR B_lambda`, placing every cross-shore edge in the full n-variable quadratic. Then
```
#ONE = [ 2^(n+d) -
  SUM_(w,lambda in F2^d) (-1)^(c(w)+lambda.w)
                   G(Q_(w,lambda),l(w)) ] / 2^(d+1).
```
To prove it, write `1[w(z)=w]=2^(-d) SUM_lambda (-1)^(lambda.(w(z)+w))` and substitute into `sum_z (-1)^F(z)`. This identity counts **original n-bit assignments**, including those mapping to the same coordinate word. Even unattainable `w` are legal: their signed contributions cancel. No free auxiliary extensions, field-rank lower bound, or assumed distribution on the interface.

The remaining quadratic character has a purely **integer** polynomial-time elimination. If a pair coefficient is one, regroup the polynomial as `z_i z_j+z_i A(z_rest)+z_j B(z_rest)+R(z_rest)`, where A,B are affine and R is quadratic. The exact two-variable identity
```
SUM_(u,v in F2) (-1)^(uv+u A+v B+R) = 2 (-1)^(A B+R)
```
eliminates that pair and preserves degree at most two. Repeating for at most n/2 pairs leaves an affine character, whose sum is zero if any remaining linear coefficient is nonzero, or `+/- 2^remaining` otherwise. On the way, `z_i^2=z_i` is always folded into the linear part. This determines sign and magnitude, not merely a rank or absolute value. Induction proves the exact formula for all accepted source lengths.

**New model-specific counterexample to the prior conditional-affine interface:** `E=x0*y0; Q=x1*y1*E; X=E XOR E; Z=Q XOR X` yields the fourth-degree original-input function `x0*y0*x1*y1`, exactly **one of sixteen** assignments. For fixed `w=E=1`, its raw dependence is genuinely quadratic in x1,y1, not affine. This does not refute TMR-2/062 because the Q gate is outside that source grammar; it shows why extending its coefficients without a quadratic Gauss evaluator would be unsound. The present construction admits the gate and counts it exactly.

## Matched physical resource ledger
The source n and g obey `n,g,d<=O(N)`; all original records and indices are parsed and authenticated. Store the input/source, g gate records, DFS metadata, up to g genuine `a*b`-bit early matrices, their F2 elimination basis, source-derived coordinate masks and a per-w live gate-value array. This is `O(N^3)` bits including heads and addresses, with no `2^d` table. Each of the `2^d` outer words performs source-derived post evaluation; each of exactly `4^d` pairs constructs the full quadratic and performs at most n/2 polynomial-size pair eliminations with signed O(n+2d)-bit arithmetic. A conservative `O(N^14)` bit-machine tariff per call covers scanning and local-head seeks, graph discovery, Gaussian basis work, all failed checks, pair-product coefficient updates, exact signed addition/division, retained state and output. Thus the **same** sequential realization has `T=O(4^d N^14)` and `S_peak=O(N^3)`. Python arbitrary-precision operations and recursion are **not** treated as physical unit-cost microsteps; the supplied interpreter is a finite reference, not native TM microcode. Networks are not invoked.

## Reproducible finite verification and controls
Locally executed CPython 3.13.5 reference source revision `TMR5_CONDQUADRATIC061_v1`, seed **20261116**. The exact executed 12.8 KB Python source has Git blob `491a87553731df93a3bab0bf5de839e44eabc984` and SHA-256 `f587a607561e80df00529ddf2bdf0b66dc940571227a4a3dc398a800f297c4f1`. It is published losslessly as wrapped gzip/base64 blob `31ceb940be55cf61c95e0ae379fd7893025477bc` with a SHA-checking executable/extractor `experiments/tmr/tmr5_condquadratic061.py` (blob `7f757a214db6a5521d10f674f5f7cd4603fbb792`). The decompressed source SHA-256 was checked locally; executing the loader produced raw JSON byte-identical to the direct original script. Final raw JSON blob `15931dea4a0fc7206bf4642252e7bb1092bd9ceb` matches the published local output exactly. The reference checked **560** exhaustive quadratic-character cases against direct `2^n` sums, **102** fully authenticated source-to-original-assignment brute counts, and **8** malformed-source controls, zero failures. Cases include repeated-variable square folding, controlled cubic/quartic functions, sharing/cancellation, a full 2x2 rank-four interface with unattainable rank-two words (exact count 9/16), and a cheap DISJ4 OR-of-four-edges control (175/256). Finite tests are COMPUTATIONAL, independent external mathematics review OPEN, physical microcode not tested. No full repository checkout/preflight, Lean/nanoda, or complete manuscript compile performed in the initial Python execution.

## Four gates and general safeguards
| Gate | Verdict and scope |
|---|---|
| DISJ sanity | **PASS restricted**. DISJ4 is a cheap shared circuit with exact 175/256 accepting count; no static rank-to-mandatory-work inference. |
| Relativization | **PASS intermediate algebra only**. No P-versus-NP or oracle separation is claimed; any NP transfer, algebrization and Natural Proofs requirements remain OPEN. |
| Simultaneous DTISP | **PASS restricted upper** with both bounds for the same sequential physical implementation. No strict FLMV forbidden pair, no generic SAT lower bound. |
| Deterministic configurations | **PASS as upper-bound safeguard**, `T<=2^{O(S+log N)}` for fixed total deterministic read-only-input machines; not a work lower bound or randomized/quantum result. |

Affine/Gaussian, Horn/2-SAT, bounded treewidth, equality/autarky, padding, auxiliaries, input products, unique-solution rank-one, selector/projection, count-normalizers, arbitrary sharing/caches/recomputation and alternative bases/fields remain legal. All Fourier characters are integer signs, not an asserted invertible Walsh transform over characteristic 2. Historical /341 remains FAIL as full UNSAT authority, /386 RESTRICTED.

## Ranked dependency transfer, remaining OPEN arrows, one next target
| Rank | Owner | Verified scope and exact OPEN arrow |
|---|---|---|
| 1 | TMR-1 | Source-to-solver-to-E^NP chain CONDITIONAL. Independent pinned Lean 4.33.1 Mathlib/transitive axioms/nanoda build and separate FinTM2-to-ordinary-machine/hierarchy semantics OPEN; no NP bound. Exponential-padding superlinear transfer FALSIFIED by /060. |
| 2 | TMR-2 | **D2-CONDITIONAL-RAW-QUADRATIC** PROVED/EXACT for this explicit new grammar, expanding /062's affine model. General mixed raw nonlinear post-DAG, universal dynamic mandatory-work invariant and all-SAT transfer OPEN. Send interface through issue #3; do not edit peer manuscript. |
| 3 | TMR-3 | Authenticated restricted candidate/checkpoint services, but a generic adaptive provider plus improved nonassociative evaluator with same-run Q,T,S OPEN. |
| 4 | TMR-4 | Source-certified bounded liveness/reconvergence compiler restricted; uniform advice-free general DAG transfer, reverse necessity and all-algorithm bound OPEN. |

**ONE highest-value next dependency:** obtain an independent successful pinned Lean dual-kernel execution **and** separately reconstruct its source-input and standard-machine-to-`E^NP` hierarchy semantics. Repeated executor startup failures do not falsify the theorem. This result closes only a typed Track A positive upper algorithm; P versus NP is OPEN.

References: (1) TMR-2/062 original mathematical report `research/agents/tmr-2/2026-11-15_2322_TMR2_CONDITIONAL_RAW_AFFINE_4D_E2E062.md`, source `experiments/tmr/tmr2_conditional_raw_4d062.js` (blob ffc7b813c1812db1fb865a7886f58de36bcca765). (2) R. O'Donnell, *Analysis of Boolean Functions* (2014, corrected 2021), for Walsh character orthogonality. (3) Standard characteristic-two quadratic Walsh sums and Arf/polarization theory; the explicit elimination identity above is self-contained.
