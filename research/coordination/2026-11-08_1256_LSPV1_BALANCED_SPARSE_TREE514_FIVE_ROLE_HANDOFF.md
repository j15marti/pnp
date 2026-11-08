# LSPV-1/514 five-role handoff: sparse original-source XOR tree work bound

**2026-11-08 12:56 PST | Route B | PROVED/RESTRICTED mathematical resource upper bound; COMPUTATIONAL independent tests | P versus NP OPEN.**

**New evidence node [P2-L1-514]**, refining [P2-L3-509], [P2-L1-512], [P2-L4-409] and [P2-D3]. [P2-D1], [P2-C3], [P2-B1], [P2-B2] and Route A [P2-A2]/[P2-A5], [P1-01]/[P1-03]/[P1-04] remain OPEN.

For any connected cubic graph on h vertices with odd charge, the **original** strict signed 3-CNF has 4h clauses and 3h/2 edge variables. The existing restricted paid SOURCE/AND3/binary GF(2) balanced tree gives q=4h-1 inferences and critical-path depth at most 2+ceil(log2 h). Each affine row represents delta(S) of its vertex subset S. At a fixed tree depth the subsets are disjoint and each edge contributes to at most two boundaries, so

$$
\sum_{\text{XOR inference }v}(|M_{v,1}|+|M_{v,2}|)
\le 3h\lceil\log_2 h\rceil.
$$

A sorted sparse two-pointer merge therefore uses O(h log h) mask-entry operations and O(h log^2 h) ID bit operations. Postorder row storage is at most 3h live IDs; allocating the new output before releasing parents raises the peak to at most (9/2)h entries, plus O(h log h) source and certificate bits. Actual deterministic checker/constructor for the canonical grouped cubic sources can be implemented within O(h log^2 h) bit time and O(h log h) peak bits in an appropriately specified multitape model. No transfer to the FLMV reference machine follows. Materializing every row would instead emit O(h log^2 h) mask bits; dense masks require Theta(h^2) writes.

This is an **upper-bound control for an explicitly selected legal fragment**, not a hardness theorem or a native historical R_mix341 accepted-byte certificate. The previous LSPV-4/409 *prism-specific* paired schedule achieves a stronger O(h) mask-entry count and is not superseded. LSPV-3/509 established compact implicit trace bits but reported naive O(h^2) replay; this general worst-case sparse bound refines that resource audit and applies also to expander graph topology. The ordinary Resolution-hard expander Tseitin controls become easy in the specified mixed parity fragment.

Independent source-authenticated Python: 12 cases through h=2048, 12 hostile controls rejected, 8191 paid nodes/30,712 XOR operand entries/3076 peak allocate-before-free row IDs at largest size. Independent published JavaScript: 7 cases through h=1024, 21 hostile controls rejected, 4095 paid nodes/14,328 operand entries/1540 allocated row IDs at largest size. No tested random or prism graph is itself claimed to be a certified hard expander.

**Five-role coordination within unchanged allocation:** LSPV-1 Route B continue original historical Rmix341 full-rule transfer and noncircular B3; LSPV-3 Route B test accepted byte grammar and exact row reconstruction with original source facets, local AND3 and paid GF2; LSPV-5 Route B audit simultaneous peak and short mixed shortcuts, seek failure of this resource bound for malformed or unsupported proof records; LSPV-2/4 Route A reuse the upper-bound control but retain universal same-machine all-input contraction requirement. Do not transform an explicit upper bound into an unrestricted lower bound.

Role-owned report research/agents/lspv-1/2026-11-08_1256_LSPV1_BALANCED_SPARSE_TREE_RESOURCE514.md, Git blob 3d8d60a31d9e98c061bf3212cb03c0b84ade2265; JS verifier experiments/arc/lspv1_514_sparse_tree_cost.cjs, blob 7d7a1899359c85f2cfc042d79214ab4c9f3983bb; raw results results/raw/arc/2026-11-08_1256_LSPV1_514_SPARSE_TREE_RESOURCE_RAW.json, blob 70dca4e030a945aecdac7594a359b19e9def413a. Python independent reproducer provided locally; GitHub historical checker not executed.

No main.tex write, no historical grammar/weights changes, no task/role/identity/title/schedule/enabled-state changes, and no new agents. P versus NP OPEN.
