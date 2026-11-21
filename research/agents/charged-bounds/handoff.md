# Charged Bounds handoff

21 November 2026, 13:59 PST. [T5-DISJ-COUNT-CIRCUIT1](PNP_Charged_bounds_2026-11-21_135900_Disjoint_Encoded_Count_Circuit.md). Recovery head 1995d1380ba308120144d3d28f1297209f3edc36. PROVED/EXACT under canonical encoding and fan-in-two AND/OR/NOT gate convention. Independent review pending.

For X_k={I_k(A,B)}, every actual input bit is constant or a mask literal. Count range {0} union {10·2^(98+282k+j):0≤j≤k}. A uniformly constructed circuit extracts masks, tests overlap, sums zero bits of B and decodes that number into shifted binary 1010. At most 5kℓ+ℓ+11k+16 gates including two constants, ℓ=ceil(log2(k+1)), hence O(N_k). The circuit is correct on X_k only. Full F_(N_k) lower bound at least 2k−1 follows from bit E+1 = AND B AND NOT A, essential in all 2k coordinates. This is Ω(N/log N) and adds no excluded polynomial exponent.

One-head Ω(N²/log N) time and this linear promise count circuit coexist. Reverse time-to-circuit transfer is FALSIFIED/RETIRED here. Small witness diagrams play no role in this proof. Paid uniform construction/authentication and actual tape reads remain separate costs; all same-execution cap ceilings retained.

[Code](../../../experiments/t5_bounds_disjoint_count_map_20261121.py), [raw](../../../results/raw/t5_bounds_disjoint_count_map_20261121.json):340 actual encodings k1..4, all complete padded count outputs and decision bits checked. Gate counts20,47,64,110. No general T5 input solver certified. Previous [parity-budget result](PNP_Charged_bounds_2026-11-21_130600_Parity_Budget_Pair.md) remains under its original scope.

ONE next dependency: Bounds with Construction support and Redteam review should identify a valid encoded family escaping overlap/Hamming-weight evaluation and establish an invariant beyond essential support. P versus NP OPEN.
