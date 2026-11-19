# TMR-5/059: charged raw-input probes in the bilinear-span exact-count pipeline

November 15, 2026, 21:58 PST. Identity TMR-5 / PNP Machine Bottleneck Redteam. Named dependency: **D2-RAW-INPUT-POST-READ** from TMR-2/060. Status: **PROVED/EXACT RESTRICTED** for the mathematical and algorithmic construction; external mathematical review OPEN. Finite executions are **COMPUTATIONAL**. P versus NP OPEN.

## Exact candidate, quantifiers and falsifiers

For every positive integers a,b, let n=a+b. For every canonical ASCII source of length N in the *new, explicitly distinguished* typed grammar `p nraw n a b g root`, with E gates `x_i AND y_j`, early X gates over E/X, post O/A/P/N gates, and post R gates that read individual original source input bits, authenticate all IDs, reachability, acyclicity, input coverage, gate types, and n<=2g *before* n-sized allocation. Gate records may be permuted, repeated children and arbitrary shared fan-out are allowed; root is post-type. Let k be the number of distinct raw input indices actually referenced through R and d the GF(2) rank of the span of the q true early interface coefficient matrices. Then a fixed uniform locally headed deterministic bit machine can output the exact number of accepting assignments to the n *original* input bits in time O(2^(d+k) N^12) and simultaneous peak writable space O(N^3+2^d N). This is an extension to a **different declared model**, not a retroactive claim about the unextended TMR-2/060 grammar.

Named falsifiers: (1) a legal mixed raw/early source with a count disagreement; (2) missing affine terms after conditioning on raw coordinates; (3) a wrong sign or nonintegral Walsh denominator for a rank-deficient matrix; (4) hiding graph authentication, source rereads, raw-pin pattern selection, rank solving, retained spectra, big-integer arithmetic or output cost.

## Algebraic lemma and complete proof

Authenticate the early subgraph once, propagate GF(2) edge coefficients without unfolding gate identities, and compute a basis B_1,...,B_d of all original a-by-b bilinear interface matrices, together with each true interface's coordinate mask. Consequently, for every actual input (x,y), each early interface value is a linear combination of w_j=x^T B_j y (mod 2). Every post node reads either an interface value, an actual raw input bit, or an earlier post node. The source thus induces one well-defined Boolean function h(w,r), where r is the vector of the k *distinct* raw input bits.

For each raw pattern p in {0,1}^k, write h_p(w)=h(w,p), and its **integer** Walsh coefficients
```
H_p(lambda) = SUM_(w in {0,1}^d) h_p(w) (-1)^(lambda dot w).
```
For each lambda, let A_lambda=XOR_(j:lambda_j=1) B_j. Partition x and y into pinned (P_x,P_y) and free (U_x,U_y) coordinates. With the bits specified by p, the quadratic exponent is
```
x^T A_lambda y = u^T M v + alpha^T u + beta^T v + c (mod 2),
```
where M is the U_x-by-U_y submatrix, alpha=A_(U_x,P_y) y_P, beta=A_(P_x,U_y)^T x_P, and c=x_P^T A_(P_x,P_y)y_P. Put a0=|U_x|, b0=|U_y| and r=rank_F2(M). The signed character sum over *unpinned* originals is exactly
```
G(lambda,p) = 0
    if alpha not in columnspace(M) OR beta not in rowspace(M);
otherwise G(lambda,p) = (-1)^(c + alpha^T u0) 2^(a0+b0-r)
    for ANY solution M^T u0 = beta.
```
This statement also covers empty free-variable sets and rank zero. Proof: sum over v first. Orthogonality makes the inner sum 2^b0 if M^T u=beta and zero otherwise. This affine solution set is empty unless beta lies in rowspace(M). On a nonempty coset, the remaining signed sum vanishes unless alpha annihilates ker(M^T), equivalently alpha in columnspace(M); otherwise its value is (-1)^(alpha dot u0) 2^(a0-r), multiplied by (-1)^c 2^b0. No independence, uniformity of reachable w, field-2 Walsh basis, or unit-cost matrix oracle is assumed.

The exact ORIGINAL-input count is therefore
```
#YES = (1/2^d) SUM_(p in {0,1}^k) SUM_(lambda in {0,1}^d)
             H_p(lambda) G(lambda,p).
```
Pointwise character orthogonality on the *actual* w(x,y) proves it. In particular the numerator is an integer multiple of 2^d. For k=0, all affine parts vanish and G(lambda,empty)=2^(n-rank(A_lambda)), exactly recovering TMR-2/060. This is a source-to-output algorithm, not an information-theoretic necessity or a general SAT lower bound.

## One-realization bit-cost ledger and source interfaces

A deterministic locally headed multitape implementation (not a simulated hardware trace) reads and validates all N source bits, guards n<=2g before allocating by n, checks unique IDs, source-alphabet syntax, ordered child references, early-versus-post types, reachability and cycles, and stores the original DAG without unfolding shared children. This takes polynomial bit time and at most O(N^3) live bits conservatively, including decimal index parsing. It constructs q interface matrices and their span basis with at most O(N^3) coefficient bits and pays for every source lookup, branch in the validation DFS and discovered basis pivot.

For each p the same machine evaluates h_p on every 2^d coordinate vector by paid post-DAG traversal and retains one 2^d-entry signed integer array. A staged integer FWHT computes all H_p; it then builds each A_lambda by charged XOR, extracts pinned blocks and affine vectors, and solves two linear systems by exact GF(2) elimination. Each intermediate sum has O(n+2d+1)=O(N) bits, and the final output has n+1 bits. Raw patterns, basis matrices, access addresses, retained spectra, arithmetic, branching and failed/invalid inputs are charged on this same execution. Total upper bounds:
```
T_total <= O(2^(d+k) N^12),   S_peak <= O(N^3+2^d N).
```
This conservative bound includes all stages and is polynomial in N when d+k=O(log N). The concrete CPython checker uses host integer/array abstractions; it is not a native TM microstep test. If a circuit-to-CNF extension is required, enforce one functional gate variable per actual original source gate including R, never unroll shared nodes, and charge all new variables/wires. That compiler was not separately executed in this audit. No complexity claim in the original q source inputs survives an arbitrary live gate count without charging it.

## Smallest interface counterexample and hostile controls

The three-gate valid source `p nraw 2 1 1 3 2; E 0 0 0; R 1 0; O 2 0 1` has output (xy) OR x = x, accepting **2 of 4** inputs. There is no function h(xy) that agrees pointwise: both (x,y)=(0,0) and (1,0) give xy=0 yet different outputs. Thus merely reusing the TMR-2/060 interface after adding raw reads is **FALSE**. Conditioning and the affine character sum repair this named interface for the newly declared grammar, rather than falsifying TMR-2/060.

The (xy) XOR x XOR y control accepts 3/4 and requires the affine-plus-constant case; a repeated-child XOR cancels its bilinear term and gives d=0; a unique-solution conjunctive control accepts 1/4; DISJ_2 accepts 9/16 despite cut rank 4 and a four-gate source; arbitrary shared/repeated gates are legal. Horn, 2-SAT, bounded-treewidth, Gaussian-affine, equality, products, autarkies, selectors, padding, count normalization and direct compact algorithms remain legal. Local invertible bases preserve cut rank, while the integer character transform here is *not* an invertible Walsh transform over GF(2). Unique-solution full indicator tensor has rank one, and Valiant-Vazirani isolation would require paid randomized reduction and promises.

## Independent executable and raw evidence

Actual independently executed local CPython script `/mnt/data/tmr5_059/tmr5_raw_probe_affine059.py` (local evidence attachment, **not** claimed published under experiments/), revision `tmr5-rawprobe-affine059-v2`, fixed seed `20261115`, was executed with `--cases 250`. It checked **257 authenticated sources** including six deterministic controls and 250 seeded randomized sources (each separately brute counted), **1,296 independent quadratic-character sums** across every 2-by-2 matrix and every pin pattern, eight malformed-source rejections, **7,185 counted assertions**, zero unexpected failures. It uses an independent original-DAG evaluator, full input enumeration for n<=6, and a separate GF(2) linear-system solver. Tests finish in approximately two seconds on the local execution host. Finite testing is COMPUTATIONAL and does not prove unbounded-size correctness.

Executed local script Git blob: `7aa38665630496eeb1575de2a904c3262e2c770f`; immutable local raw JSON blob: `7665a12d1e800a61bfd69a26dc8449736805a7c2`. Raw JSON includes the controls, exact check totals and deterministic case checksum `6c3e1481b008cd3534e0305af6baa3c849f241f92966acd798e2ae4f648c14dd`. Check the eventual remote blob readbacks before labeling publication complete. No independent Lean build, nanoda, native TM microcode, full repository preflight or PDF compilation was executed. The separate upstream pinned Anthropic Lean trust check remains OPEN, with the failed executor attempt recorded by TMR-5/058.



A second, separately executed V8 Code Mode verification used the **exact JavaScript functions** serialized as the published standalone file `experiments/tmr/tmr5_rawprobe_span059.js`, revision `TMR5_RAWPROBE_AFFINE_JS059_V1`, seed `20261115`. It checked 185 authenticated sources (five controls plus 180 seeded instances), 1296 independent signed 2-by-2 quadratic-character cases, five malformed rejections and 195 instrumented top-level checks, zero failures. Its immutable actual raw response is `results/raw/tmr/2026-11-15_2158_TMR5_RAWPROBE059_V8_RAW.json`. Readback Git blobs are executable `7b40ac8f3507b3e55f80dd98ab6326e99521f16c` and raw `d99998275224992dfd878a9d345573033ab627e2`. The in-isolate V8 functions were executed and source-serialized; the standalone Node CLI wrapper was not separately invoked. The separate local Python suite has 7,185 assertions, while the published JS suite has 195 top-level checks; **do not conflate these counts**. The Python executable/raw remain available as local conversation artifacts and have not been uploaded to GitHub.

## Four mandatory gates

| Gate | Verdict and rationale |
|---|---|
| DISJ sanity | **PASS RESTRICTED**. DISJ_2 and general DISJ retain linear source circuits and cheap evaluation; the exponential-rank-to-general-hardness implication remains FAIL. |
| Relativization | **PASS intermediate only** for direct algebra and explicit exact count. No nonrelativizing P-versus-NP step is asserted. An NP step would need a precise nonrelativizing argument, with algebrization/Natural Proofs obstacles audited. |
| Simultaneous DTISP | **PASS restricted UPPER ledger**. Time and peak writable space are upper bounded on the very same source-parsing/counting execution, including input and output. No FLMV forbidden pair, general lower bound or all-machines claim. |
| Deterministic configuration counting | **PASS upper-bound sanity**. A fixed total read-only-input deterministic machine has T<=2^O(S+log N); this does not lower bound work or transfer automatically to random/quantum runs. |

The historical /341 full UNSAT authority is FAIL and /386 remains RESTRICTED.

## Ranked cross-track dependencies and one next target

1. TMR-1: authentic compiler/normalizer/finite-stack theorem to E^NP remains CONDITIONAL. Pinned fresh Lean4.33.1, PrintAxioms, nanoda acceptance and independently charged ordinary-machine/hierarchy bridge OPEN. TMR-5/058 found executor failure before steps, not rejection. TMR-1/061 fixes a density scope error on its draft PR.
2. TMR-2: **D2-RAW-INPUT-POST-READ now PROVED/EXACT RESTRICTED** by the above independent extension. It changes the input grammar and does not claim general mixed arbitrary-depth circuits or necessary time-space lower bounds. The unextended /060 formula remains correct.
3. TMR-3: Williams graph-guess primary-source audit corrects a misleading original-index hardness inference in draft /061; generic paid candidate selection, provider and improved evaluator OPEN.
4. TMR-4: /062 source-recognizable shared in-tree compiler remains PROVED/RESTRICTED; arbitrary reconvergent shared-core schedule/necessity OPEN.

**ONE highest-value next dependency:** independently execute the unchanged pinned Anthropic Lean 4.33.1 + Mathlib proof, its transitive axiom audit and dual-kernel replay in a working executor, then separately audit the `FinTM2` to standard-machine and E^NP transfer. No class-matched NP bridge exists and P versus NP remains OPEN.

## Primary sources and exact integration

TMR-2/060 original report `research/agents/tmr-2/2026-11-15_2117_TMR2_SPAN_COMPRESSED_POST_DAG_E2E060.md`, executable `experiments/tmr/tmr2_post_bilinear_span060.js` at blob `d57dae367427b71927dbcdfb9c3a711c8169d0cf`, TMR-2 living main2 at blob `85c1e3b03b6b4910e5b2bfe9376dd8876e04c6d1`. Standard character orthogonality follows from elementary finite-group Fourier analysis (O'Donnell, *Analysis of Boolean Functions*, revised arXiv:2105.10386, Chapter 1); the affine-bilinear signed sum is proved explicitly above. TMR-3/061 primary-source correction in issue #3 and draft PR #201. Anthropic pinned `MainResults.lean`/`Solution.lean`, commit `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`. Full scope and code revisions are recorded here; independent external mathematical review remains OPEN.
