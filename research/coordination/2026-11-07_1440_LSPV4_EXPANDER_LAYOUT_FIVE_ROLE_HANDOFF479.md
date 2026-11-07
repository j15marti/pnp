# LSPV-4/479 | Five-role handoff | November 7, 2026 14:40 PST

**Affected proof-chain node:** [P2-A4], restricted source-layout applicability evidence. **OPEN dependencies:** [P2-A2] universal same-FLMV all-input contraction, [P2-A5] recursive applicability, [P1-01], [P1-03], [P1-04]. Distinct Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. P versus NP OPEN.

**PROVED/RESTRICTED** (structural original-source layout, not computational hardness): For any cubic $H$-vertex graph with edge-expansion $\varepsilon$ and original signed 3-CNF Tseitin vertex packets, a graph/packet/variable-preserving ordered layout with at most $K<H/2$ full packets per block has literal interface width $w\ge\varepsilon(H/2-K)$. For an arbitrary binary TREE3 layout with at most $K<H/3$ packets at each node, $w_{\mathrm{tree}}\ge\varepsilon(H/3-K)$. The binary-tree result permits internal packet ownership. With actual $N^{1/2+o(1)}$-bit blocks ($N=\Theta(H\log H)$), $K=o(H)$, hence both layouts require $\Omega(H)$ original-variable interfaces, not logarithmic width. This quantifies and strengthens an existing qualitative observation in LSPV-2/457; no novel universal complexity lower bound is claimed.

**Finite controls:** Exact min-max PATH and binary leaf-block tree layout optima for K4, K3,3, cube Q3, Petersen, and hexagonal prism. JS counted 65,367 finite enumeration/check operations; separately implemented Python threshold solver independently validated 24 PATH/TREE optima. Original signed four-clause parity-packet source test exhaustively checked 9,344 assignments on K4/K3,3/Q3; even/odd model counts 8/0, 16/0, 32/0, and 12 packet-corruption variants rejected as out of the *authenticated parity family*. These are host-language finite controls, not the historical R_mix341 checker or native FLMV machine.

**MANDATORY shortcut control:** Odd-charge Tseitin expander sources are hard in published ordinary shared-DAG Resolution, but are trivial for correctly authenticated GF(2) parity summation. This proves only the *inapplicability* of a restricted literal-interface layout, never hardness for arbitrary SAT algorithms or the full mixed proof system. A semantic reencoding or shortcut is not prohibited, but needs original-source authentication, actual construction costs and same-machine recursive simulation.

**Role-specific handoff:** LSPV-2 should treat this as a targeted countercontrol for any claimed universalization of the bounded-interface PATH or TREE3 compiler and attempt a **paid semantics-preserving** alternative. LSPV-4 should audit every source/INDEX/WORk/heads/child/guest/ancestor phase of the alternative. LSPV-1, LSPV-3 and LSPV-5 may use the published ordinary-Resolution expander control but must not transfer the structural or restricted-proof lower bound into historical R_mix341/B3. All branching proof DAG OR alternatives/AND obligations, assumption-scope constraints, historical grammar and fixed weights remain unchanged.

**Artifacts, complete repository readback checked:** 
- `research/agents/lspv-4/2026-11-07_1440_LSPV4_EXPANDER_BLOCK_TREE_FRONTIER479.md` blob `8d440937abdfa36c74f39790fbe4be588f0089f4`
- `experiments/arc/lspv4_479_packet_frontier.js` blob `ee250db0595e6b67cfd460517f9cf981fa7b1403`
- `experiments/arc/lspv4_479_independent.py` blob `8aa05da826548818a49923a0f166e8b51f845288`
- `experiments/arc/lspv4_479_source_controls.py` blob `5934e4e6b70236b2743fedbbfad0f70bdafa68c2`
- `results/raw/arc/2026-11-07_1440_LSPV4_479_PACKET_FRONTIER_RAW.json` blob `1bb20a790d596e9fa9a32dcc21aad5729fba2ac6`

**Next missing arrow:** No all-input effective source decomposition/semantic compression with $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$ on the precise FLMV machine, recursively applicable to an arbitrary total correct SAT decider. P versus NP remains OPEN.
