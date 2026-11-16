# TMR-2/062: authentic conditional-raw affine DAG, exact 4^d counting

2026-11-15 23:22 PST, America/Los_Angeles. Track A. Role TMR-2. Dependency D2-CONDITIONAL-RAW-AFFINE-4D in D2-COUNT-PIPELINE. PROVED/EXACT on the restricted grammar; external independent mathematical review OPEN; finite tests COMPUTATIONAL. P versus NP OPEN.

## Candidate and four falsifiers

For all canonical accepted p ncond source strings of length N, a fixed deterministic locally headed multitape machine outputs the exact accepting ORIGINAL-input count in bit time O(4^d N^12) and same-run peak writable space O(N^3), with d the genuinely constructed F2 bilinear interface dimension. No exponential factor in k raw-bit probe identities. The four falsifiers checked were (1) a hidden post OR/AND reading raw bit values (must reject); (2) pointwise loss when shared XOR operands cancel or matrices are dependent; (3) signs, matrix compatibility, nonuniform coordinate reachability, denominator divisibility; (4) omitted parsing, fan-out, matrix arithmetic, query volume, state retention or output costs. Cheap alternate algorithms are legal.

## End-to-end original-source model

The ASCII source header is p ncond n a b g root, with n=a+b, a,b>=1, g>=2 and n<=2g. Exactly g records, each with unique ID 0,...,g-1 and arbitrary order, are E id i j (one original x_i AND original y_j), X id u v (XOR of early E/X values), O/A/P id u v and N id u (post OR/AND/XOR/NOT of early/post values), R id originalBit control (original raw bit AND one early/post Boolean control), or Z id u v (XOR of early/post/R/Z expressions). Root is Z. Every gate is root-reachable, the dependencies are acyclic, all original inputs appear in E or R, and the source has one terminal LF. Typed phase, source bytes, dimensions, canonical numbers, ranges, coverage, IDs and reachability are explicitly authenticated. Post OR/AND cannot consume R or Z and therefore cannot multiply raw expressions. Source sharing, repeated gate operands, and actual gate/record IDs are retained.

The execution performs parsing and validation, DAG topological traversal, genuine early GF(2) bilinear matrix construction, source-derived basis B_1,...,B_d and coordinate masks, actual Boolean post evaluation for each w in F2^d, collection of exact linear raw coefficients u(w),v(w) and constant c(w), two Gaussian eliminations for each pair (w,lambda), exact signed accumulation/division and output. By gate induction the circuit is POINTWISE equal to C(x,y)=u(w).x XOR v(w).y XOR c(w), w_j=x^T B_j y, for all original assignments. A hypothetical source lacking typed certification is not covered.

## Exact character theorem, proof and quantifiers

For each lambda in F2^d put M_lambda = XOR_{j:lambda_j=1} B_j. Write G(M,u,v)=SUM_{x,y} (-1)^(x^T M y+u.x+v.y), with r=rank_F2(M). Solving M y0=u and M^T x0=v, G is zero if either system is inconsistent. When both are consistent it is (-1)^(u.x0)*2^(a+b-r). Proof: summing over y enforces M^T x=v; the remaining affine coset has 2^(a-r) elements, and its u-character vanishes unless u annihilates ker(M^T), equivalent to u in image(M). In the compatible case its sign is constant. Singular and zero matrices are included.

Character orthogonality supplies the exact delta indicator

    1[w(x,y)=w0] = 2^(-d) SUM_lambda (-1)^(lambda.(w(x,y)+w0)).

Expanding #ZERO-#ONE, then applying the G lemma at each w0 and lambda, yields the **exact integer formula**

    #ONE = (2^(n+d) -
           SUM_{w0,lambda} (-1)^(c(w0)+lambda.w0)
              G(M_lambda,u(w0),v(w0))) / 2^(d+1).

Every intermediate term is an integer, and exact divisibility follows from the original character identity even for unreachable w words. Source semantics give the count of ORIGINAL inputs, not a count of free auxiliary wires or only a decision bit. Any functional Tseitin gadget would need unique wire extensions; no CNF compiler was executed here.

For authenticated sources with d=O(log N), the fully constructed algorithm is polynomial-time. This is a scoped #CircuitSAT UPPER bound, not an unrestricted SAT/circuit lower bound.

## Genuine new interface and contrasting controls

A 4-gate source E=x0 AND y0, X=E XOR E, R=x1 AND E, Z=R XOR X computes x0*x1*y0, exactly **1 of 8** accepting assignments. This does not admit the previous fixed-affine source representation h(w) XOR ell(x,y) with one global raw vector: varying x1 when x0=0 produces derivative zero, while varying x1 when x0=y0=1 gives derivative one. The new conditional coefficient resolves precisely the D2/061 limitation, with d=1 and four (w,lambda) evaluations.

The family a=b=32, 1024 edge predicates XORed to w=(XOR x)(XOR y), includes 64 syntactically reachable raw R gates. The first is controlled by zero, and the remaining 63 by w; root equals w*(XOR of all input bits except x0) = w*x0. Exact count: 2^61 = **2,305,843,009,213,693,952**, n=64, g=2176, d=1, four character calls. This large identity was checked symbolically, not by exhausting 2^64 assignments. DISJ_4 encoded as post OR of four independent cross-shore ANDs has 4^4-3^4=175 accepting inputs and a cheap circuit; rank is not a compulsory-work lower bound. Affine/Gaussian, Horn, 2-SAT, treewidth, equality, autarky, product/padding, unique-selector projection, unique-solution rank-one assignment indicator, compact shared circuits and all legal adaptive paths remain controls.

## One-realization time/space ledger

Source bit length N upper bounds n,g,d and all indices. Charge: N source-byte reads and canonical rejection checks, ID maps, DFS and head seeks; construction and storage of up to g actual ab-bit early matrices (O(N^3) bits); paid basis elimination/masks, degree and phase checks; 2^d streamed post-word DAG evaluations and actual coefficient masks, without 2^d retained truth words; **exactly 4^d** inner character calls, each building M_lambda and doing two GF(2) elimination/consistency/solution computations; signed O(n+2d)-bit accumulator and exact 2^(d+1) division; output and caches/failed work. All shared objects counted once. A conservative locally headed multitape implementation charges O(N^12) bit steps per outer/inner control operation, giving T=O(4^d N^12) and S_peak=O(N^3) for the SAME physical execution. No random-access oracle, uncharged arithmetic, parallel span or free strategy discovery. This is a conservative analytic envelope, not an actual TM microstep trace. Finite JS harness deliberately caps d<=8 but the theorem has no such fixed cutoff.

## Executed evidence and pinned revisions

ACTUALLY EXECUTED in V8 Code Mode: revision TMR2_CONDITIONAL_RAW_4D062_v1, deterministic xorshift seed label 20261116. **222 checks, 104 independently brute-force original-input count comparisons, 13 malformed rejections, zero failures**. The 104 cases include 72 generated mixed conditional post circuits, a cubic counterexample, rank-zero, DISJ, and exact cancellation families. Executable experiments/tmr/tmr2_conditional_raw_4d062.js, Git blob ffc7b813c1812db1fb865a7886f58de36bcca765. Immutable JSON results/raw/tmr/2026-11-15_2318_TMR2_CONDITIONAL_RAW4D062_V8_RAW.json, Git blob b8345f75130439b79cc2264aec791d62b531874f. The published source was fetched from the branch and executed again; its JSON output matched the published raw text byte-for-byte. These finite checks are COMPUTATIONAL, not independent mathematical review. No local repository checkout/preflight, Lean build, manuscript LaTeX compile or physical Turing-machine replay was performed for this hosted V8 run.

Primary mathematical source: Ryan O'Donnell, Analysis of Boolean Functions (Cambridge, 2014; corrected arXiv:2105.10386), Chapter 1, for character orthogonality. Prior actual TMR-2/061 report Git blob 9cac021ba819238962640e2cd88e8a1a99607330, executable e4907b2e535be4dc1357df2280eafd1f22a98fdb. Relativization reference Baker, Gill, Solovay (1975). Valiant-Vazirani randomized isolation is not used. TMR-4/063 draft concerns a different restricted compiler and is not an unrestricted model transfer.

## Four mandatory gates

| Gate | Status and reason |
|---|---|
| DISJ sanity | **PASS restricted**: cheap DISJ and explicit post-OR control retained. Any unrestricted rank-to-work inference FAILS. |
| Relativization | **PASS local upper theorem, OPEN unrestricted lower bridge**: no NP separation; a future proof must identify its exact nonrelativizing step, with algebrization/Natural Proofs audit. |
| Simultaneous DTISP | **PASS restricted upper same-run ledger, OPEN unrestricted lower transfer**: both T and S are bounds for the one source-to-output machine, not a forbidden FLMV pair. |
| Deterministic configuration counting | **PASS upper guard only**: T<=2^{O(S+log N)} for deterministic total read-only-input machines, or 2^{O(S)} when S>=log N; never a necessary-work lower bound or a randomized/quantum assertion. |

Historical /341 remains FAIL as full UNSAT authority and /386 RESTRICTED.

**TMR-4 transition interface:** D2-CONDITIONAL-AFFINE-CHARACTER-TRACE. State contains authenticated source IDs/typed arcs; constructed matrices and GF(2) basis coordinates; current streamed w word; post gate values; actual conditional u(w),v(w),c(w); current lambda and M_lambda; two actual consistency/solution records; signed G, numerator/denominator and exact output. Paid transitions READ/PARSE/GUARD/DFS, MATRIX_XOR, BASIS_ELIM, POST_GATE, RAW_CONTROL_AND, AFFINE_XOR, CHARACTER_BUILD, GF2_SOLVE, SIGNED_ADD, DIV_EXACT, CACHE/DROP, RECOMPUTE, SWITCH and OUTPUT. This correctness invariant is not compulsory for all other SAT machines.

**ONE next load-bearing lemma OPEN:** D2-CONDITIONAL-RAW-QUADRATIC. Authenticate a source grammar that permits coefficients of quadratic terms in original raw bits to depend on constructed bilinear words while forbidding uncontrolled nonlinear raw degree. Implement and charge a true quadratic GF(2) character-sum evaluator; prove or falsify O(4^d poly(N)) exact original-input count without enumerating k raw bits.

**Publication:** additive role-owned draft on tmr2-20261115-2318-conditional-raw4d062; main merge and external review require independent checks.
