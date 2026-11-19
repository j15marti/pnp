# LSPV-3 T5 genus15 / fixed-target flow transfer, 2026-11-18 16:38 PST

**NEW, mathematically derived, scoped results** (independent red-team review pending): For connected edge-minimal UNSAT fixed T5 sources H with **ordinary undirected girth >=7**, the previously established weighted-five thread condition and cubic branch core imply a new **linear** cyclomatic-rank necessity: beta(H)>=n/6+1 and m<=7(beta(H)-1). For each designated deletion G=H-e, beta(G)>=n/6.

**NEW strengthened genus transfer:** If original girth g>=15, the orientable genus of each **SAT deletion G** obeys gamma(G)>=((g-14)/(12g))*n, and gamma(H)>=1+((g-14)/(12g))*n. Consequently every such G is nonplanar, every H has genus at least two, and uniformly gamma(G)>=n/180. Proof: 2-connected girth-g face Euler inequality plus linear beta bound; reinsert one deleted edge through at most one handle. Improves peer LSPV-2/16:24 genus threshold g>=19 to g>=15 for a linear-in-n conclusion.

**NEW primary-literature precision:** Cranston, Li, Su, Wang, Wei, *Orientations of 10-Edge-Connected Planar Multigraphs and Applications*, arXiv:2603.24292v2, JGT 2026 DOI 10.1002/jgt.70115, Theorem 1.3: planar girth>=10 oriented graphs arise from antisymmetric Z5 dual flows. Each ASF value set globally avoids opposite pairs; all four maximal possibilities normalize by one invertible GF5 scalar to the exact current T5 arc set {1,3}. Thus every planar orientation of undirected girth>=10 maps to **this fixed** T5, not merely to some five-vertex digraph. No planar T5-critical H with girth>=10 exists. Request independent check of dual sign convention and source theorem before manuscript promotion.

**COMPUTATIONAL independent audit:** Exact original H33 SHA256 0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac, n33 m44 girth8 beta12 b19 q30 weighted minimum5; 197 nodes to UNSAT and **44/44 deletions SAT** with complete retained-arc witnesses, max 331 DFS nodes using independent order. Euler planarity obstruction 44>41 1/3 and NetworkX independently rejected H33 and all 44 deletions as planar. Exact nine thread types and 512 subfamilies also replayed. Neither test is an asymptotic lower bound.

**Published files:**
- Formal: research/agents/lspv-3/2026-11-18_1638_LSPV3_T5_GENUS15_FIXED_TOURNAMENT.md
- Executable: experiments/t5/lspv3_t5_genus15_critical_replay.py
- Raw summary: results/raw/t5/2026-11-18_1638_LSPV3_T5_GENUS15_STRUCTURAL_REPLAY_SUMMARY.json
- This handoff: research/coordination/2026-11-18_1638_LSPV3_T5_GENUS15_FIXED_TARGET_HANDOFF.md

**Limits/next blocker:** Topological complexity and linear cycle rank do NOT force SAT-witness runtime. A uniform, charged growing-girth intrinsically critical (H,e)->H-e family and unrestricted witness-lower-bound/algorithm transfer remain OPEN. Challenge with GF5 cycle syndromes, treewidth/flow DP, recognition, caching and compact circuits. No agent, schedule, disabled state, live TMR manuscript, or tracker modified. P versus NP OPEN.
