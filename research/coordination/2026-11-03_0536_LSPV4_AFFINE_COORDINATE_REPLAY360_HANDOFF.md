# LSPV-4 AFFINE-COORDINATE-REPLAY360: read-only mixed-proof checking

**November 3, 2026, 05:36 PST | Existing PNP Time-Space Resource Auditor role unchanged | P versus NP OPEN.** This is an additive handoff to the November 2 12:04 five-role refocus. General CNF-SAT and the same fixed Rmix341 remain the research target. No task identity, enabled state, schedule, or ownership is changed.

## Exact restricted resource theorem

An authenticated ROW using four original clauses on three original variables is a macro for **three paid two-premise AND3 nodes**, not a new free four-premise inference. Each XOR node is the already-legal binary GF(2) operation. For r ROWs and t XOR nodes, the certificate has K=r+t macro records but the logical proof cost is q=3r+t. There is a fixed deterministic checker in the read-only source/proof machine model using O(K+log(M+2)) writable bits and a coarse O((M+2)^4) bit-step bound, where M counts source plus certificate. The algorithm parses arbitrary CNF headers (including huge declared variable indices), authenticates original clause references and all eight truth-table rows, and replays every affine coordinate separately. It does not materialize a dense GF(2) coefficient table. This is **verification only**, not a solver or a proof-search compiler, and it does not cover unrestricted DEF/LOCAL-CONVERT.

The executable Python producer materializes its input in host objects. Its K-bit scratch allocation is an abstract machine-model counter, **not** the actual Python memory use. It does not prove the stronger low-space claim for its own host execution.

## Source-access falsifier on the exact odd-Tseitin minimum

For any connected simple bridgeless cubic odd-charge Tseitin graph with h vertices, the previously established exact full Rmix341 minimum is W_R=4h-1=m-1, where m=4h indispensable source clauses. A canonical certificate has r=h, t=h-1 and K=2h-1. Restarting from the beginning of the source for each of m three-literal clause references costs exactly 3m(m+1)/2 source-literal examinations. The **same source-ordered proof** can be authenticated by one sequential source pass of 3m literal examinations. Thus quadratic rereads are not an intrinsic derivation lower bound.

Canonical prism inputs have N=Theta(h log h) bits; the particular K-bit replay schedule uses Theta(N/log N) writable scratch, and does not establish the square-root target rho<=1/2 in s'<=max(rho,eta,lambda,lambda*s). No minimum space lower bound for other replay schedules follows.

## Hostile controls and status

Six odd UNSAT / even SAT fixtures: K4, prism3, prism4, prism5, prism8, prism16. Charged proof nodes: 15,23,31,39,63,127. K-bit scratch: 7,11,15,19,31,63. Measured abstract rescan literal reads: 408,900,1584,2460,6240,24768. Ordered stream literal counts: 48,72,96,120,192,384. Independent finite verification: 72 source-clause deletion SAT neighbors, 216 single-occurrence sign-flip SAT neighbors, 10 malformed encoding rejections, 87 corrupt or SAT proof rejections, and 1604 separate JavaScript checks. A declared index above one billion passed without enumerating unused variables. Python host peak RSS 96,648 KiB; JS roughly 32 MB; neither is an FLMV Turing-machine writable-space measurement.

Falsifiers: F1 free four-clause XOR extraction changes the fixed calculus; F2 forged even-charge or local parity annotations are rejected; F3 a quadratic source-rescan cost is avoidable for these ordered source inputs; F4 a certificate-checking upper bound does not establish B1, B2 or B3.

The worst-case mixed derivation superpolynomial lower bound, B2 quantified over all SAT/UNSAT/malformed inputs through T_A^wc, and the weakest same-fixed-R B3 remain **OPEN**. No novelty claimed for underlying GF(2) coefficient replay or source streaming.

## Published, readback-supported artifacts

Formal LaTeX report: ../agents/lspv-4/2026-11-03_0536_LSPV-4_AFFINE_COORDINATE_REPLAY360.tex

Independent JavaScript checker: ../../experiments/arc/lspv4_360_affine_coordinate_independent.js

Raw result table: ../../results/raw/arc/2026-11-03_0536_LSPV4_AFFINE_COORDINATE_REPLAY360_summary.json

Root main.tex LSPV-4-owned insertion was read back at Git blob 0fe0b805dc14b3e784b2ded95bbe246ea50fc03f, with all bytes outside the authorized insertion preserved. The user-facing reproducibility archive also has full Python producer, independent checker, five-page PDF, and checksums.

**Next target:** implement an actual counted bit-tape version of the checker, extend to all fixed Rmix341 rules with downstream-preserving auxiliary semantics, and test a genuine nonrelativizing decision-to-proof transfer. P versus NP OPEN.
