# PHYSICAL MASKED-PARITY-SHEAR8 | 2026-10-19 12:36 KST
**Status:** Exact canonical-family counterexample, independent review pending; finite controls passed; P versus NP OPEN.

## REVIEW
Originals fetched: WIRE_LEDGER1, WIRE-SWITCH-ACCOUNTING1 and verified JSON, current FANOUT-CAPACITY-CONSERVATION6, TSEITIN-BISECTION-GAUSS7 handoff and raw JSON, WIRE-EQUIV-ELIM3, COMBINED-REPLAY1, RECURCLOSE1, main4/main5. The :24 role remains paused. Restricted fanout-tree B2(f)=max(0,f-2) is not placed hardware. CNF literal incidence is not transistor wiring.

## IDEAS PROPOSED BEFORE PRIMARY LITERATURE
1. Nonlinear bijective triangular masking of hypercube edge parities, to test inference from high ANF degree to SAT difficulty.
2. Explicit separation of raw full-assignment CNF evaluation, existential projection, and SAT decision circuits, with different input domains clearly labeled.
3. Complete named-net fanout/buffer accounting; output driver, routing and transistor nets unknown.
4. Full-source canonical template validation and malformed single-literal rejection, no uncharged externally supplied labels.

## PRIMARY LITERATURE CHECK
Toffoli, Reversible Computing, MIT-LCS-TM-151 (1980), provides invertible Boolean primitives. Soos, Nohl and Castelluccia, Extending SAT Solvers to Cryptographic Problems, SAT 2009, motivate extraction/elimination of XOR relations. Thompson, Area-Time Complexity for VLSI, STOC 1979, requires a specified physical model. None implies unrestricted SAT hardness from transistor counts.

## EXACT THEOREM
For integer d>=3 let Q_d be the d-dimensional hypercube with V=2^d vertices and M=d*2^(d-1) edges indexed 0,...,M-1. Introduce source x_e and nonlinear triangular map:

    y_0=x_0; y_1=x_1;
    y_i=x_i XOR (y_(i-1) AND x_(i-2)) for 2<=i<M.

The inverse is x_i=y_i XOR (y_(i-1) AND x_(i-2)), sequentially. For i>=4, the ANF monomial x_0*x_1*...*x_(i-2) occurs with degree i-1; hence the last degree is M-2.

At every vertex v impose XOR_{e incident(v)} y_e=b_v. Encode each mask AND by five proper signed 3CNF clauses using two freely padded bits; each mask XOR by four proper signed 3CNF clauses; each vertex parity by d-2 ternary XOR relations of four proper clauses each, with d-3 intermediary variables. The resulting single 3CNF F_d(b) has distinct, proper three-literal clauses:

    N = 5M-8+V(d-3) variables
    C = 9(M-2)+4V(d-2) clauses
    I = 3C literal incidences.

For ALL d>=3 and ALL b in {0,1}^V:
    SAT(F_d(b)) <=> XOR_{v=0}^{V-1} b_v=0.

Each edge occurs in precisely two parity checks, proving necessity. For even charges a spanning-tree assignment yields y, invertible masking yields x and all gate auxiliary bits have explicit lifts, proving sufficiency. Exact complete assignment count is zero when odd; when even it is 2^(M-V+1+2(M-2)), including the two unconstrained AND-padding bits at each of the M-2 masks. SAT is therefore polynomial-time decidable for this canonical subclass, not for arbitrary SAT.

## WIRE/SWITCH LEDGER
Declared static CMOS proxy library: INV=2, OR2=6, AND2=6, XOR2=16 (four NAND2 equivalent), BUF2=4 nominal MOS. A logical XOR2 has two MACRO input terminals; internal NAND/transistor nets are unspecified. Named-net RAW full-assignment CNF evaluator uses INV=N, OR2=2C, AND2=C-1 and balanced AND outputs. Therefore:
    G=N+3C-1; P_in=N+6C-2; P_out=G;
    E=N+6C-1 (including output sink); W=2N+3C-1;
    static nominal MOS=2N+18C-6.
Exact abstract fanout-two buffer completion is sum over named nets max(0,fanout-2). No placed wirelength, routed area, actual transistor nets, capacitance, measured delay/energy or output-driver MOS was obtained; keep these fields NULL.

The different-domain existential projection circuit takes only M source x bits and synthesizes forward shears plus vertex checks; it existentially removes gate auxiliary bits. The different-task SAT decision circuit takes V extracted charge bits after FULL canonical source validation and computes inverted charge parity. Its core counts: G=V; E=2V; W=2V; buffers=0; static nominal MOS=16(V-1)+2; depth=ceil(log2(V))+1. It excludes source decoding and validation, and is NOT a smaller circuit for the same all-N-input Boolean function computed by the raw CNF evaluator.

| d | C | B source bits | ANF degree | raw G | raw E | raw W | BUF2 | raw MOS | buffered MOS | projected MOS | SAT-core MOS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 122 | 2592 | 10 | 417 | 783 | 469 | 230 | 2294 | 3214 | 526 | 114 |
| 4 | 398 | 10780 | 30 | 1361 | 2555 | 1529 | 750 | 7494 | 10494 | 1538 | 242 |
| 5 | 1086 | 32618 | 78 | 3713 | 6971 | 4169 | 2046 | 20454 | 28638 | 3982 | 498 |
| 6 | 2734 | 98464 | 190 | 9345 | 17547 | 10489 | 5150 | 51494 | 72094 | 9734 | 1010 |
| 7 | 6574 | 256428 | 446 | 22465 | 42187 | 25209 | 12382 | 123814 | 173342 | 22982 | 2034 |

B=2h+16+3C(w+1) for declared ordered encoding with h=bit_length(max(N,C)+1), w=bit_length(N+1), 16-bit format marker. A complete one-pass canonical template verifier reads B bits / 3C literal records, generates each expected clause from O(log B) counters, extracts charge from each final vertex XOR triple and accumulates parity. Template edge index is computed from each binary endpoint via a closed-form cumulative bit-count rank. O(B polylog B) bit time and O(log B) work bits suffice abstractly. A conservative uninstrumented live-control bound is 16*bit_length(B)+128 bits. The Python reference recognizer materializes the input and regenerated template, so its heap is NOT evidence of the streaming bound. Source replay/cache can be zero for the *proposed* one-pass decision algorithm but all B bit traversals remain charged. Full witness finding uses O(V+M) RAM descriptors and a larger output, charged separately.

For d=7, on 24 seeded primary x assignments lifted to consistent gate auxiliary values, raw full-CNF and existential-projection outputs agreed. Raw internal gate-output toggles=71132; projection toggles=19086. A separate 24-charge stimulus had SAT-core toggles=1452. These are not physical energy or fair same-input-domain circuit-minimum comparisons. Buffer output toggles and full parser switching are NULL.

## BUILD AND BOUNDED TESTS
The complete locally archived Python generator constructs every CNF clause, forward/inverse mask, spanning-tree witness, primitive circuit, per-net fanout histogram and 5-scale JSON ledger. Seed 202610191236. Tested: all 4096 primary assignments for Q3, all 256 Q3 charge vectors (128 constructive YES witnesses), 4352 forward/inverse checks, 240 named netlist controls, 764 index-rank checks, 60 near-image one-literal mutation rejections, and proper/distinct clauses for all five sizes. Unexpected assertion failures 0. Finite tests support but do not replace the algebraic theorem.

## STATUS AND NEXT FALSIFIER
ESTABLISHED, review pending: exact parity decision after nonlinear invertible masking, degree and clause/model-count identities.
COMPUTATIONAL: named-net, pin/edge, buffer and dynamic trace censuses.
CONDITIONAL: logspace one-tape recognizer actual head-motion and physical hardware realization uninstrumented.
RETIRED: inferring hard SAT from high nonlinear ANF degree, many unique clauses, high nominal MOS/net/fanout counts or gate toggles.
OPEN: arbitrary scrambled encodings, routed physical minima, genuine all-input reduction, unrestricted SAT-time lower bounds, P versus NP.

Next: randomly rename/reorder literals and clauses, compose overlapping nonlinear shears, and attempt source-independent detection with construction costs charged. Do not equate existential SAT decision and complete CNF evaluation.

Primary sources:
[1] Toffoli 1980: https://dspace.mit.edu/entities/publication/06a8b271-428a-4379-955c-8c7334aa0288
[2] Soos et al 2009: https://www.msoos.org/wordpress/wp-content/uploads/2011/03/Extending_SAT_2009.pdf
[3] Thompson 1979: https://doi.org/10.1145/800135.804401

<!-- FINAL_VERIFICATION_SENTINEL::MASKED-PARITY-SHEAR8::P_VS_NP_OPEN -->