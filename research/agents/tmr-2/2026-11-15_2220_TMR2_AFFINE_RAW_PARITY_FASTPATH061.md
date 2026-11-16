# TMR-2/061: a source-authenticated affine-raw fast path beyond pinned-bit enumeration

Date: 2026-11-15 22:20 PST, America/Los_Angeles. Track A. Ownership: TMR-2 / PNP Information Necessity. **PROVED/EXACT for the declared typed source class; external independent mathematical review OPEN.** Finite checks COMPUTATIONAL. **P versus NP OPEN.**

## Dependency and falsification contract

The selected stable chain is **D2-COUNT-PIPELINE**: authentic source bytes -> typed shared-DAG authentication -> actual bilinear gate matrices -> GF(2) span discovery -> authentic Boolean post-DAG evaluation -> exact integer Walsh/affine character sums -> exact accepting ORIGINAL-input count and decision bit. This run closes **D2-AFFINE-RAW-FASTPATH** in that chain. It is a stronger algorithmic option than the general `p nraw` pinned-probe extension independently proved by TMR-5/059 in draft PR #199, which costs O(2^(d+k) poly(N)). Our new `p naff` grammar is different, and never silently reinterprets a general raw-Boolean post DAG as affine.

**Precise candidate:** For every authenticated `p naff` source with n=a+b original input bits, a,b>=1, original source bit length N and discovered bilinear interface rank d, the exact accepting count is constructible deterministically in O(2^d N^12) bit time and simultaneous O(N^3+2^d N) writable bits, regardless of the number k of distinct original raw bits read by the authenticated final affine-parity DAG. **Falsifiers considered:** (1) signed-character sign or normalization discrepancy for h(w) XOR affine raw; (2) singular matrices or incompatible affine right-hand sides yielding falsely nonzero sums; (3) repeated XOR operands/shared fan-out counted as fresh independent wires; (4) accepting an arbitrary nonlinear mixing of post and raw gates through untyped source edges.

## Exact authentic grammar, not an oracle

Canonical ASCII `p naff n a b g root` with precisely g records `T id ...`, unique IDs 0..g-1 in arbitrary order. Types `E id i j` are x_i AND y_j, `X id r s` are early XORs of E/X gates. Post `O/A/P id r s` are OR/AND/XOR and `N id r` is NOT, accepting only early/post predecessors. Raw `R id i` reads one actual original x/y input bit; raw `L id r s` XORs raw predecessors and `U id r` NOTs one raw predecessor. The single final `Z id post raw` XORs a Boolean post result with a raw-affine result. The declared root is Z. Every gate must be source-reachable and the DAG acyclic; all n original inputs must appear in E or R; every ID, shore, type and input bound is authenticated, with n<=2g before n-indexed allocation. There is no variable/order/matrix oracle or exponential tree unrolling. Malformed inputs are rejected, not counted as UNSAT. All records, including repeated operands, are counted once by identity and re-read as required. This is a restricted model, not general Circuit-SAT.

Write all actual early-to-post interface bits as x^T A_i y over GF(2). Discover a genuine matrix basis B_1,...,B_d and coordinate masks, so all post logic is a source-derived Boolean function h(w), w_j=x^T B_j y. Separately propagate the raw DAG as an exact linear mask and constant, ell(x,y)=u^T x+v^T y+c. Then the original root computes C(x,y)=h(w(x,y)) XOR ell(x,y) on EVERY original assignment. The raw source can use k=n bits and contain polynomially many gates; its entire effect is the CONSTRUCTED affine vector, not a 2^k truth table.

## Theorem: twisted bilinear Fourier identity and proof

For lambda in GF(2)^d, set M_lambda=XOR_j(lambda_j B_j) and H_lambda=SUM_(w in GF(2)^d) (-1)^(h(w)+lambda dot w), computed as an INTEGER Walsh transform. For any a-by-b binary M and vectors u in GF(2)^a, v in GF(2)^b define

    G(M,u,v) = SUM_(x in GF(2)^a,y in GF(2)^b)
                      (-1)^(x^T M y + u^T x + v^T y).

Let r=rank_GF2(M). If u is NOT in image(M) OR v is NOT in image(M^T), then G=0. Otherwise choose ANY x0 with M^T x0=v and

    G(M,u,v) = (-1)^(u^T x0) 2^(a+b-r).

Proof: the inner y sum equals 2^b exactly when M^T x=v and zero otherwise. If that system is solvable, its x-solutions form x0+ker(M^T). The signed sum over this coset vanishes unless u annihilates ker(M^T), equivalently u in image(M). Under that condition the sign is constant (-1)^(u^T x0), giving 2^(a-r) solutions. This includes zero matrices and empty/incompatible affine systems without a supplied inverse.

Integer character inversion on the actual w(x,y) yields

    D := #ZERO - #ONE
       = (-1)^c / 2^d * SUM_lambda H_lambda G(M_lambda,u,v),

    #ONE = (2^n - D)/2.

The exact sum is integral even if many w strings are not reachable. Integer signed arithmetic, NOT a Walsh inverse over GF(2), is used. A fixed typed source is pointwise identical to the extracted h and ell; the produced #ONE counts ORIGINAL inputs once, not auxiliary wire valuations. Optional parsimonious strict proper 3-CNF conversion introduces one uniquely defined wire per source gate, three uniquely zero-pinned variables, at most four ternary clauses per gate plus eight pins/root clauses, V=n+g+3 and C<=4g+8. This optional compiler is a mathematical construction, not executed by the finite test runner.

## Quantitative pipeline and SAME_REALIZATION ledger

On one fixed deterministic locally headed multitape realization, N original source bits bound n,g,q,d, and ab<=N^2. Parse every byte, range-guard indices before allocation, check stages and reachability by DFS, cache each actual early ab-bit matrix, and propagate each raw affine mask (n bits) and constant in the topological order. Exact GF(2) elimination derives the q interface coordinate masks and d basis matrices; no preloaded basis. Actual post Boolean gates are evaluated on all 2^d coordinate strings, sharing true gate identities, followed by one in-place integer FWHT. For each lambda, allocate and XOR the actual M_lambda, solve BOTH M_lambda y=u and M_lambda^T x=v by charged GF(2) elimination, form the signed full-precision integer and accumulate. Finish with exact divisions by 2^d and 2, range-check, output the n+1 bit count and optional decision bit.

The same execution has conservative **T(N)=O(2^d N^12)** bit steps and **S_peak(N)=O(N^3+2^d N)** writable bits. This envelope charges source reads/seeks, invalid checks, gate identity maps, failed pivots, basis construction, access addresses, full-precision integer operations, sharing, retained spectral array, rank/solve scratch, caches, recomputation and output. The JS host cap d<=12 prevents allocation overload; the mathematical algorithm does not assume d<=12. Polynomial time follows only on authenticated instances with d=O(log N). The generic raw-read `p nraw` source is NOT covered by this fast path, and changing the grammar carries a substantive restriction. Networks and parallel-span savings are not used.

**Concrete family:** for every a,b>=1, all ab edge AND gates are XORed into a bilinear parity w=(XOR_i x_i)(XOR_j y_j), duplicated through a genuine post OR(h,h), while all n=a+b original input bits feed a real raw parity chain. The root is w XOR parity_all_inputs. It accepts precisely 3*2^(n-2) assignments; complementing the post h gives 2^(n-2). This has k=n raw reads and d=1, so the generic pinned-probe loop has 2^(n+1) nominal (pattern,character) pairs while this authenticated representation evaluates exactly TWO character terms. These are bounds for the specified representations, not a lower bound against alternative algorithms.

## Executed reproducible evidence and review boundary

V8 Code Mode ACTUALLY EXECUTED exact revision `TMR2_AFFINE_PARITY_FASTPATH061_v1` (deterministic seed label 20261115, no RNG draws): **116 checks**, **53 independently enumerated original-source assignments/count comparisons**, **nine malformed rejection checks**, zero failures. A source with a=b=32 encoded 1,024 distinct edge ANDs and all 64 raw input probes, g=2,176 shared gate identities, discovered d=1, computed 2 character terms and exactly **13,835,058,055,282,163,712** accepting 64-bit inputs; this large case was checked against the proved family formula, not enumerated. Small controls include both post h and NOT h, rank-zero X(E,E), shared repeated-operand OR, two independent bilinear layers, raw NOT, and invalid stage edges. Source `experiments/tmr/tmr2_affine_parity_fastpath061.js`, Git blob `e4907b2e535be4dc1357df2280eafd1f22a98fdb`; immutable raw `results/raw/tmr/2026-11-15_2220_TMR2_AFFINE_PARITY061_V8_RAW.json`, blob `b56418b33ee37bec0003a754a540b8fe22e4fcc3`. Readback matched both executed source and output. A **separate** local CPython reference exhaustively compared 4,360 affine-bilinear Gauss sums against direct sign enumeration for dimensions (1,1), (2,2), (2,3), (3,2); zero failures. This reference test was executed independently and is published separately. Finite tests are COMPUTATIONAL, not a formal proof or native multitape trace. Native repository preflight and LaTeX compilation not executed because no local repository checkout/network DNS exists. External independent mathematics review OPEN.

Primary corpus consulted: TMR-2/060 original exact count report/blob b0d80de1ea47c3be8b3b88292dc1c8dce09eb94e, executed /060 source d57dae367427b71927dbcdfb9c3a711c8169d0cf; TMR-5/059 raw-probe independent generalization on **draft** PR #199, source report blob 1bdf30da21c9796cbaff0dc0b182339c2801bf57; TMR-4/062 costed shared-component compiler and issue #3. Literature: Ryan O'Donnell, *Analysis of Boolean Functions*, Cambridge 2014, corrected arXiv:2105.10386, Chapter 1 (finite Boolean Fourier inversion). The twisted rank/affine character sum is proved here rather than attributed as a novel external theorem.

## Four mandatory verification gates

| Gate | Verdict with precise reason |
|---|---|
| DISJ sanity | **PASS restricted.** DISJ_k can have full assignment-cut rank 2^k while a linear-size depth-two circuit decides it; neither this fastpath nor the generic pinned interface infers unrestricted work hardness. All cheap Gaussian, decomposed and shared algorithms remain legal. |
| Relativization | **PASS for the restricted algebraic upper theorem; OPEN for any unrestricted NP transfer.** This proof is oracle-free and has no nonrelativizing separation step. A would-be separation must identify its nonrelativizing operation and face algebrization and Natural Proofs checks. |
| Simultaneous DTISP | **PASS restricted same-run upper ledger; OPEN unrestricted lower-bound bridge.** One ordinary deterministic machine has both displayed resource bounds. No strict FLMV forbidden time/space pair or lower bound is claimed. |
| Deterministic configuration counting | **PASS upper-bound consistency only.** For a total read-only-input deterministic machine T<=2^{O(s+log N)}, or 2^{O(s)} if s>=log N. This is not compulsory work or a randomized/quantum bound. |

Horn/dual-Horn, 2-SAT, affine/Gaussian, bounded treewidth, equality, autarky, independent products, padding/auxiliaries, unique-selector projection, unique-solution indicator rank one, local invertible basis rank invariance, characteristic-two Walsh failure, compact shared circuits and alternate contraction orders remain active hostile controls. Randomized Valiant-Vazirani isolation is neither used nor free. Historical /341 FAIL full UNSAT and /386 RESTRICTED.

**Named execution-sensitive TMR-4 correctness interface:** D2-AFFINE-SPECTRAL-TRACE: authenticated bytes/IDs, typed early/post/raw transitions, actually materialized early matrix coefficients, constructed GF(2) basis and coordinate masks, raw affine mask/constant, post Boolean table, signed integer FWHT values, row-solve compatibility and particular solutions, signed numerator/denominators and emitted count. Charge READ, PARSE, VALIDATE, DFS, MATRIX_XOR, RAW_XOR/NOT, BASIS_ELIM, POST_GATE, FWHT_ADD/SUB, SOLVE_GF2/TRANSPOSE, CHARACTER_SIGN, BIGINT_ACCUM, DIV_EXACT, CACHE/DROP/RECOMPUTE, OUTPUT; all cheap physical alternatives and switches remain legal. This is a restricted preservation invariant, NOT necessary work for arbitrary algorithms.

**ONE next load-bearing lemma:** D2-CONDITIONAL-RAW-AFFINE-4D (OPEN): authenticate a circuit whose post function has the source-derived representation C(x,y)=h_0(w(x,y)) XOR [u(w(x,y))^T x+v(w(x,y))^T y+c(w(x,y))], with all coefficient functions obtainable on each w by actually evaluating a typed shared control DAG. Show a charged 4^d poly(N) exact counter without enumerating k raw input bits, or falsify this transfer with a legal nonlinear raw path. Neither this extension nor the current restricted results resolves P versus NP.
