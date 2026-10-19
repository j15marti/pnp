# SAT5X8-HITTING-CIRCUITS1 | 19 October 2026 (Asia/Seoul)

**Status:** EXACT proper-clause structural theorem and finite exact-cover count; COMPUTATIONAL, independently checked gate-level circuit UPPER bounds. Minimum for raw 56- or 96-bit inputs is OPEN. P versus NP OPEN.

## 1. Eight-clause hitting theorem

Let F consist of precisely eight proper 3-clauses on n>=3 variables. Each excludes 2^(n-3) assignments. Their sizes add to 2^n. Thus F is UNSAT iff the eight excluded-assignment subcubes are pairwise disjoint, equivalently **every one of the 28 distinct pairs of clauses contains some common variable with complementary polarity**. SAT is therefore detectable by a nonclashing clause pair. This does not hold as stated for effective width less than three or tautological clauses.

For n=5 there are 80 possible signed proper clauses; each excludes one four-vertex square in Q5. An exact least-uncovered-vertex covering recursion counted **4,380** unordered eight-square tilings: ten use three active variables, 1,340 use four, and 3,030 use all five. Each unordered tiling has 8! orders. Thus **176,601,600** ordered UNSAT lists occur among **80^8 = 1,677,721,600,000,000** ordered proper lists. The 272 prior Q4 perfect matchings embed exactly in Q5.

## 2. Actual primitive gate-level circuits

Conventional nominal unsized complementary CMOS library: INV=2 devices; BUF2=4; NANDk/NORk=2k; OR2=6. Input to one SAT output; P is gate input-terminal count, W logical driven nets, B explicit two-load fanout buffers. All circuits are combinational. Long NAND/NOR16/32 stacks are not characterized for delay or placement.

| Input encoding / netlist | Input bits | G gates | P input-pin incidence | W driven nets | Logic depth | B added | Core nominal MOS | Buffered nominal MOS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 56-bit proper, primitive fan-in <=4 | 56 | 1,023 | 2,246 | 1,079 | 18 | 808 | 4,492 | 7,724 |
| 56-bit proper, primitive fan-in <=16 | 56 | 757 | 2,012 | 813 | 12 | 856 | 4,024 | 7,448 |
| 56-bit proper, alternative presence decoder | 56 | 1,114 | 3,081 | 1,170 | 12 | 1,496 | 6,162 | 12,146 |
| 96-bit arbitrary literals, shared-complement implementation | 96 | 1,381 | 4,548 | 1,477 | 11 | 2,304 | 9,096 | 18,312 |
| 96-bit arbitrary literals, direct implementation | 96 | 1,429 | 6,228 | 1,525 | 10 | 4,272 | 12,456 | 29,544 |
| PRECOMPUTED 80-bit clause presence | 80 | 38 | 357 | 118 | 5 | 160 | 714 | 1,354 |
| PRECOMPUTED 80-bit falsifying rails | 80 | 313 | 872 | 393 | 5 | 400 | 1,744 | 3,344 |
| PRECOMPUTED 256-bit independent falsification table, fan-in 2 | 256 | 255 | 510 | 511 | 8 | 0 | 1,022 | 1,022 |
| PRECOMPUTED 256-bit table, giant gates | 256 | 34 | 289 | 290 | 3 | 0 | 578 | 578 |

56-bit proper encoding = eight seven-bit symbols: 4-bit triple ID (0..9) and 3-bit sign mask. 96-bit arbitrary encoding = 24 signed-literal symbols of four bits (0..9), including repetitions/tautologies. Invalid codes reject. **Precomputed** masks/rails/tables omit all input conversion and are NOT comparable with full raw-input circuit costs.

## 3. True minimum and lower bounds

All 56 proper, 96 general-literal, 80 presence and 256 table input bits have independently constructed single-bit sensitivity witnesses on valid complete formulas. Thus any fan-in-two circuit requires at least 55, 95, 79, 255 binary gates, respectively. The **256-bit independently supplied falsification-table** implementation attains its 255-gate lower bound (74 NAND2, 180 NOR2 and 1 OR2; 1,022 nominal MOS). Its transistor count is within two nominal MOS of the trivial 4*255=1,020 lower bound; no transistor minimum is independently proved. For raw proper56/general96 the lower bounds are FAR below current constructions. No global minimal circuit is claimed.

## 4. Constructed three/four/five-variable comparison

| Input class | n | Input bits | Core gates | Core MOS | Buffered MOS |
|---|---:|---:|---:|---:|---:|
| Proper | 3 | 24 | 156 | 630 | 854 |
| Proper | 4 | 40 | 445 | 2,296 | 4,120 |
| Proper | 5 | 56 | 757 | 4,024 | 7,448 |
| Arbitrary signed literals | 3 | 72 | 517 | 2,760 | 4,776 |
| Arbitrary signed literals | 4 | 72 | 745 | 4,032 | 7,008 |
| Arbitrary signed literals | 5 | 96 | 1,381 | 9,096 | 18,312 |

All are specific implementation UPPER BOUNDS with different input lengths and different chosen gate decomposition. These three data points cannot prove the asymptotic minimum circuit size.

## 5. Computational and reproducibility audit

Complete local user conversation artifact: 3SAT_8clauses_5variables_reproducible_circuits.zip, containing all 20 five-variable core/buffered primitive Verilog netlists, a bundled four-variable comparator netlist, Python standard-library generator, independent Verilog interpreter, Boolean input-dependency witness checker, 300-input logical-toggle ledger, CSV/JSON pin/wire/cell censuses, schematic PNG and DOT, exact test outputs and SHA256 checksums. Built with seed 2026101905; independent verifier seed 60108191019.

Tests: 6,400 clause-pair conflict cases, all 4,380 Q5 UNSAT tilings through the raw netlist, independent complete Verilog replay for all 4,380 tilings, 272 previous Q4 embeddings, 8,192 independent falsification-table column masks, invalid-code rejection and randomized proper/tautological/repeated-literal formulas. Zero detected errors. No full 80^8 brute-force scan is claimed. Static MOS devices are not actual measured transistor switching, area, routing or energy; these quantities remain NULL. P versus NP remains OPEN.

<!-- FINAL_VERIFICATION_SENTINEL::MAIN::SAT5X8-HITTING-CIRCUITS1::P_VS_NP_OPEN -->