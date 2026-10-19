# SAT5X9-PARALLEL-OVERLAP-OPT1

Date: 2026-10-20 (Asia/Seoul). Status: exact mathematical equivalence; computationally checked real primitive Verilog netlists and construction UPPER BOUNDS. Neither raw circuit is proved globally minimum. P versus NP remains OPEN.

## Exact source function

Inputs: nine seven-bit proper 3-clause codes, each giving three distinct signed literals chosen from five source variables (10 legal triple IDs, three sign bits). Repetitions allowed; malformed code rejects. One SAT output. For nine clauses, each falsification set is a size-four square in {0,1}^5. If W is the sum of all 36 pairwise intersection cardinalities then SAT iff W>=5 (and UNSAT iff W=4). Nonzero pair weights are 1,2,4.

A pairwise compiler uses C = nonconflicting shared signs; D = C AND supports share at least two underlying variables; E = C AND supports are identical. Then intersection size is exactly C+D+2E. The new weighted-overlap circuit uses two weight-one input bits C,D and one weight-two bit E per pair. Its compressor tree uses 3:2 full adders and a final at-least-five comparison. It improves logic depth and gate count but does not beat direct coverage.

A distinct De Morgan decoder is better. For each source clause, decode negative one-hot support (10 options) and polarity (8 options). NOR2 of the two negative minterms is the positive indicator for one of 80 possible proper clauses. NOR9 computes absence of that type across the nine source records. Each of 32 possible truth assignments is covered iff NAND10 of the 10 relevant absence bits is 1. NAND reduction of all coverage bits, with valid-support-code checks, yields SAT exactly. No precomputed presence mask or other uncharged input work is supplied: all decoding gates are inside the 63-bit circuit.

## Model-matched implementation results

Ideal static CMOS proxy: INV=2, NANDk/NORk=2k, AND2/OR2=6, XOR2=16 and BUF2=4 nominal devices. Maximum *primitive logic gate fan-in* is 16 except for the explicit older fan-in-four comparator. Buffers are separately emitted noninverting cap-two signal trees, with each input terminal treated as a load. Unknown routed wire lengths, layout, power, actual transistor nets and delay are NULL, not zero.

| Actual 63-bit raw-input Verilog design | Functional gates G | Gate input pins P | Distinct logic nets W | Depth | Core nominal MOS | Added BUF2 | Buffered nominal MOS |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original serial overlap | 2885 | 6666 | 2948 | 91 | 18320 | 2569 | 28596 |
| New parallel Wallace weighted-overlap | 2083 | 4838 | 2146 | 49 | 15536 | 1802 | 22744 |
| Earlier direct assignment coverage, fan-in 16 | 1145 | 3367 | 1208 | 15 | 6734 | 1773 | 13826 |
| Earlier direct assignment coverage, fan-in 4 | 1671 | 3425 | 1734 | 23 | 6850 | 1143 | **11422** |
| New factored presence, direct OR2 matcher | 1076 | 3259 | 1139 | 11 | 7958 | 1753 | 14970 |
| **New factored presence, De Morgan NOR2 matcher** | **1075** | **3258** | **1138** | **10** | **6516** | **1753** | **13528** |

The winning new De Morgan core contains 67 INV, 720 NOR2, 80 NOR9, 72 NAND3, 90 NAND4, 41 NAND10, 2 NAND16, 1 NAND9 and 2 NAND2 cells: 1075 functional gates, 6516 nominal MOS. Its 1753 explicit BUF2 cells yield 2828 cells, 2891 distinct driven nets, 5012 directed logical connections, 13528 nominal CMOS devices and buffered depth 17. Maximum raw pin fanout is 10. All raw 63-bit source bits are included; no input preprocessing has been left outside the design.

The new Wallace overlap versus serial overlap decreases gates 2885 -> 2083 (27.8%) and core depth 91 -> 49 (46.2%) but still does not beat direct coverage. The new De Morgan decoder versus previous 1145-gate direct coverage decreases G by 6.1%, core MOS by 3.2%, buffered MOS by 2.2%, and depth by one third. However, the fan-in-four older circuit retains the lowest measured **buffered** nominal MOS among these options, 11422. Gate-count, circuit depth, buffered-device cost and minimum transistor size are separate optimization objectives. No transistor or gate lower bound matching 1075 has been proved.

## Tests, falsifiers and scope

The builder-side test code independently generated all 4380 prior eight-clause UNSAT tilings with a ninth clause and additional 4000 seeded formula tests for each new Wallace design, and all 4380 tilings plus 6000 further seeded tests for each factored-presence variant; zero unexpected mismatches.

A separate parser/evaluator reads actual primitive-gate Verilog without invoking the builder's circuit evaluator. It checked all 4380 tilings against the new De Morgan and old coverage designs, checked the first 160 tilings against all six compared designs, checked nine minimally-UNSAT deletion-witness controls, 1100 randomized/adversarial formulas and malformed codes against all six, verified the full emitted raw/buffered gate-pin-net-MOS and fanout-two ledgers for six designs, and executed 60 more buffered controls. No discrepancies. Original sampling seeds: Wallace 202610191951; presence 202610192050; independent parser 202610201104.

On the same declared deterministic 300-input trace (seed 202610201357), core logical gate-output toggles were 155347 (serial overlap), 133052 (parallel Wallace), 70709 (older 1145-gate coverage) and 22769 (new 1075-gate De Morgan). These are *logical gate-output toggles*, not transistor switching events, measured power or energy. The trace contains deliberately structured cases; it is not a representative operating distribution.

Complete reproducibility with source builders, Verilog cores and BUF2 netlists, independent verification scripts, component comparison CSV/JSON, SHA256 manifest, and full results is packaged in the originating conversation at 3SAT5_9clauses_parallel_overlap_optimization_2026-10-20.zip; the zip itself is not assumed to be published to GitHub. The previous canonical starting point is research/main/2026-10-19_1935_MAIN_SAT5X9_OVERLAP_CIRCUITS1.md.

## Scientific conclusion

The mathematically simpler weighted-overlap identity did **not** give the smallest hardware realization. Direct SAT coverage, especially the factored 80-type decoder, is significantly cheaper on this finite problem. This is evidence against treating a proof identity as a compulsory computation. Even the new best 1075-gate raw-input design is a constructive upper bound, not a minimum-circuit theorem. Fixed n=5,m=9 supplies no asymptotic P versus NP lower bound.

<!-- FINAL_VERIFICATION_SENTINEL::MAIN::SAT5X9_PARALLEL_OVERLAP_OPT1::P_VS_NP_OPEN -->