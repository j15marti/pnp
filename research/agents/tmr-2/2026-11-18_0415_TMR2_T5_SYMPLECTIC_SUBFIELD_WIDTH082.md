# TMR-2/082: Explicit unbounded gauge-conditioned width with a seven-node T5 NO certificate

Status: **PROVED/EXACT restricted** for the algebraic family and refutation certificate, **COMPUTATIONAL** for the finite Node.js PC/SAC audit, independent external mathematics review **OPEN**. Date: 2026-11-18 04:15 America/Los_Angeles. **P versus NP OPEN.**

## Load-bearing dependency, input and falsifiers

Advance **D2-T5-UNBOUNDED-GAUGE-CONDITIONED-WIDTH-MIXED-FAMILY** by building an infinite, polynomially constructible YES/NO pair with identical undirected source skeleton, undirected girth eight, increasing *minimum* (not merely heuristic) elimination width even after any single-color root gauge, and full path-consistency/singleton-AC survival. The aim is a rigorous hostile **counterexample** to interpreting growing width as unavoidable computation, not a general-purpose lower bound.

Model: Σ=Z5; (R(a,b)=1) iff ((b-a)\bmod 5\in\{1,3\}). Genuine encoded directed arcs are source constraints, with no guessed auxiliary variables. Source grammar is canonical `p t5 n m`, `v i`, `a u v` lines; orient every undirected edge exactly once.

Predeclared falsifiers: (F1) the finite W(3,4) generated graph is not a simple 5-regular bipartite girth-eight graph; (F2) the anchored seven-node refutation omits an available branch or invalidly removes a T5 value; (F3) singleton AC or full binary PC refutes either member; (F4) the same-skeleton YES witness violates an arc; (F5) the subfield embedding or the minimum-width lower bound fails. Finite checks F1-F4 passed; F5 is proved algebraically below, external review OPEN.

## Finite model and exact certified comparison

Take (F_4=F_2[\alpha]/(\alpha^2+\alpha+1)). The projective points are nonzero vectors in (F_4^4), normalized so the first nonzero coordinate equals 1. Totally isotropic projective lines arise from distinct points (p,q) satisfying the nondegenerate alternating form
[
\langle p,q\rangle=p_0q_1+p_1q_0+p_2q_3+p_3q_2=0.
]
The incidence graph (H_4=W(3,4)) has (85) point vertices, (85) line vertices, (425) edges, degree five and undirected girth eight. Points and lines are sorted lexicographically over canonical field element encodings (0,1,\alpha,\alpha+1); incidences are ordered by point index and line index. The original NO orientation is defined by the complete 425-bit hexadecimal word

`64d078efa08476fb30ed79caa29d504b82420b2eb6a3003cac558620466a0034b0b6353ae12fae42b36bc5576b1d41f68aee542a09`

where bit (i=1) reverses the (i)-th canonical incidence (line to point), otherwise point to line. Exactly 195 edges are reversed. The canonical NO source SHA256 is `cf27ebb991e8a1f105a862857eb0b8ff96cc5931682a5a332c5035fce1220715`. The all-point-to-line YES comparator has exactly the same undirected skeleton and canonical source SHA256 `ab09996653ffc670018ed66450144e1212ee26094e563c5b524dc8377b9a070c`.

**Exact NO certificate.** By the free simultaneous (Z_5)-rotation action, fixing original variable (x_0=0) preserves satisfiability. Global binary arc consistency on the authentic 425 arcs leaves (x_{85}\in\{2,4\}). For (x_{85}=2), it leaves (x_5\in\{0,3\}), both contradictory under full AC. For (x_{85}=4), it leaves (x_5\in\{0,2\}), both contradictory. Thus the complete tree contains **7 nodes, 3 exhaustive splits, 4 independently checked AC conflict leaves**, proving (Z_{NO}=0) for all five values of (x_0). The program checks every split's entire supported color set, recomputes AC independently at each node from the original arcs, and rejects invalid branches.

**YES comparator.** Assign zero to each point and one to each line. Every arc is satisfied since (R(0,1)=1). Consequently (Z_{YES}>0); in fact (Z_{YES}\ge 5\cdot2^{85}), since all points may have any common color (c) and each of 85 line variables may independently choose (c+1) or (c+3). This is a certified bound, **not a claimed exact full YES count**.

**Exhaustive local-consistency audit.** For each of the 170 original vertices and five pins, full AC survives: **850/850 NO** and **850/850 YES**. Complete 25-bit binary path consistency converges in two sweeps on both, removes exactly 102,000 ordered-color supports from the initialized pair matrices, retains **604,350** ordered pair-color supports across all (170^2) ordered vertex pairs, and never empties a pair relation. The equality of cardinality profiles is exact; the surviving masks need not be equal. The count is also checked against the girth-eight distance profile: 170 diagonal pairs with five supports, and 850/3400/13600/10880 ordered pairs at distances 1/2/3/4 with 10/15/20/25 supports respectively.

Executed, unmodified Node.js stdlib source revision `tmr2-t5-symplectic-width082.v1`, decoded source SHA256 `7762b18fa9a6054a7271353c4f07af897e9d9c3af42eec79442b400c9e90a940`. Invoked `node experiments/tmr/tmr2_t5_symplectic082.js --pc` using the hash-checking launcher and lossless compressed source. **20,058 assertions, zero failures**, independently cross-checked by a separate CPython GF(4) geometry builder, arc-consistency/backtracker (seven rooted nodes), and all 850 singleton pins per orientation. The exact finite test is COMPUTATIONAL; the fully checkable finite refutation is a PROVED/EXACT restricted certificate under the checker semantics. Complete JSON raw SHA256 `9abc095a19cee906d92b551cd54a3514c2a9b7a04f27e39942b9e95aea6b958b`.

## Infinite growing family, proof of minimum conditioned-width growth

For every integer (t\ge1), put (q=4^t) and form the symplectic generalized quadrangle (W(3,q)) on projective points and totally isotropic lines in (F_q^4) with the same alternating form. Its incidence graph has
[
n_q=2(q+1)(q^2+1),\qquad m_q=(q+1)^2(q^2+1),
]
undirected girth eight and exactly (q+1) neighbors per vertex. Its size is (\Theta(q^3)) vertices and (\Theta(q^4)) edges.

The subfield (F_4\subseteq F_{4^t}) induces a literal copy of the 85 point and 85 line vertices of (W(3,4)), with all 425 canonical incidences preserved. Fix the subfield embedding by choosing a root of (X^2+X+1), map the normalized (F_4) projective vectors into (F_q^4), and inherit the corresponding ambient isotropic lines. Define the **NO** orientation to equal the above fixed 425-bit rule on this finite subgeometry; orient every other ambient edge from point to line. The entire source is UNSAT because its restriction to the 170 subgeometry vertices includes the certified NO gadget. The **YES** source orients *every* edge point to line and has the explicit (0/1) witness. Both share the identical (W(3,q)) undirected skeleton. These sources are uniform: standard finite-field arithmetic and enumeration of normalized projective vectors and isotropic lines run in time polynomial in the written source length (even a deterministic search over polynomially many (F_2) polynomial representations suffices when measured in (q)).

The primal graph of either source has minimum degree (q+1). Fixing any single root label deletes at most one neighboring vertex from the primal graph; every remaining vertex still has degree at least (q). In every elimination ordering, the *first* eliminated vertex therefore has at least (q) live neighbors. Thus the minimum induced width after any choice of a single gauge root satisfies
[
\boxed{w_{\mathrm{rooted}}(H_q)\ge q=4^t
      =\Omega(n_q^{1/3}).}
]
There is no degree-one or degree-two original variable to suppress, even after one root gauge for (q\ge4). The minimum width is a rigorous graph invariant, not a heuristic order statistic. Both inputs have undirected girth eight, and the previously established girth-eight local-consistency lemma applies to **any** orientation, so full PC and every singleton-AC test survive for all (t).

**Crucial source-aware shortcut:** the NO member contains the same *constant-size* 170-variable obstruction with the seven-node proof; the YES member has a direct two-color witness. In the promised, canonically generated family, checking the subfield gadget and the orientation mode and verifying its original arcs can be performed in polynomial source time. Even on unrestricted source graphs, enumerating copies of a fixed 170-vertex forbidden directed graph costs at most (n^{170}\operatorname{poly}(m)), a polynomial but not practical finite exponent. Therefore no growing-width-to-general-work necessity theorem follows. A naive dense bucket table for width (q) has (5^{\Omega(q)}) candidate tuples, whereas a source-aware decision certificate remains constant-size relative to the family parameter. This is an exact counterexample to **width-alone** or **PC/SAC-plus-width-alone** necessity assertions, including after degree-two and gauge reductions. It is not a refutation of a lower bound with additional explicit hypotheses ruling out short subcertificates and cheap family recognition.

## Source/input/computation/output and same-realization resources

For the finite result, the completed pipeline is ORIGINAL SOURCE generation and canonical parsing -> incidence and girth certification -> original T5 arc factors -> independently recomputed AC for each of seven refutation nodes -> all five global gauge rotations -> full YES witness scan -> 170 times five singleton AC calls per orientation -> full exact binary PC on both -> output JSON plus hashes. It charges source serialization/authentication, adjacency, 425 edge accesses, 25-bit masks, branch indexing, every AC fixed point and PC composition, all caching/retained matrices, certificate verification, exact integer arithmetic, and output. The primary `--pc` run has (O(n^3\operatorname{poly}(n,m))) bit-time for a fixed five-symbol alphabet, polynomial workspace for the finite verification; structural generation of W(3,q) and checking the fixed gadget for the canonical family are polynomial in the full source length. This is a verifier plus a restricted-family decider, not an all-input polynomial solver. The small constant proof tree does not bound the time needed to *discover* it on arbitrary sources.

**Named TMR-4 handoff:** `D2-T5-SYMPLECTIC-SUBFIELD-7NODE-WIDTH-TRACE`, transitions READ/PARSE/HASH, GENERATE_GF, NORMALIZE_POINT, DISCOVER_ISOTROPIC_LINE, VERIFY_INCIDENCE, GAUGE_ROOT, ASSIGN_DOMAIN, AC_FIXED_POINT, VERIFY_ALL_BRANCHES, CERTIFY_CONFLICT, CHECK_YES_WITNESS, CHECK_PC, CHECK_SAC, VALIDATE_SUBFIELD_EMBEDDING, SOURCE_RECHECK, CACHE/DROP/RECOMPUTE, OUTPUT. The theorem **FALSIFIES** any automatic inference from large source treewidth/minimum induced width plus propagation survival to required time of every equivalent algorithm, by exhibiting a compact source-recognizable NO certificate and YES witness.

**Four mandatory scientific gates.** DISJ: **PASS restricted** (no rank-to-machine complexity inference); a transfer from width to arbitrary work would **FAIL**. Relativization: **NOT APPLICABLE** to explicit finite proof and family recognition; any unrestricted P-vs-NP conclusion **OPEN** under Baker–Gill–Solovay, algebrization and Natural Proofs. Simultaneous DTISP: **PASS** as matched polynomial upper time and workspace for declared verification/family recognition; **OPEN** any forbidden pair lower bound. Deterministic configuration counting: **PASS upper-only** for a total deterministic verifier; no necessary-work inference. No auxiliary witness multiplicity is dropped; the NO count is exact zero, YES bound is expressly partial. Keep Horn/2-SAT/affine, treewidth, modules, separator, products, padding, exact cycle-space, Fourier, compact sharing, adaptive branching, cached extraction and recomputation as legal. /341 FAIL full UNSAT, /386 RESTRICTED.

**Remaining dependency (ONE):** `D2-T5-UNBOUNDED-WIDTH-NONLOCAL-CERTIFICATE-BARRIER` (OPEN). Construct mixed YES/NO high-girth T5 families with growing conditioned minimum width **and** demonstrate that no constant-size NO gadget or polynomial source-authenticated global invariant already settles the pair; audit charged full source-derived cycle-space, exact elimination, OBDD/FBDD and adaptive refutations. Prove any restricted lower bound separately from a cost-sound general algorithm transfer.

## Sources

[1] De Winter S, Lazebnik F, Verstraëte J. An Extremal Characterization of Projective Planes. Electronic Journal of Combinatorics 2008. DOI 10.37236/867 (incidence-graph comparison and finite geometry context).

[2] Bamberg J, Bishnoi A, Royle GF. On regular induced subgraphs of generalized polygons. 2017. https://arxiv.org/abs/1708.01095 (symplectic generalized quadrangle family, regularity/girth).

[3] Standard symplectic quadrangle geometry W(q), projective points and totally isotropic lines: https://www.math.sk/bachraty/docs/stu_thesis.pdf (background, not an independent referee of this construction).

Repository source: `experiments/tmr/tmr2_t5_symplectic082.js.gz.b64`, launcher `experiments/tmr/tmr2_t5_symplectic082.js`, raw `results/raw/tmr/2026-11-18_0415_TMR2_T5_SYMPLECTIC082_JS_RAW.json`.

Native full Git checkout preflight, complete LaTeX build, physical TM microtrace and independent external mathematical review were not executed in this connected-tool environment.
