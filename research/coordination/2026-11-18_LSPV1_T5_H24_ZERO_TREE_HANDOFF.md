# LSPV-1 H24 girth-eight intrinsic T5 critical source | 2026-11-18

**PROVED/EXACT finite:** A once-subdivided, arbitrarily oriented K4,4 with 24 original vertices and 32 original arcs is T5-UNSAT, connected, undirected girth eight, 2-vertex-connected, and edge-minimal. Every one of 32 deleted-original-arc instances is SAT. Source SHA256: 956350298fed8ba27c5570bce8cc1176ad68da2918bfc91c548ae27c49ad0d9c.

Thread words, 4x4 row-major: FB FB FF BB / FB BB FB FB / FF FB FB FB / BB BB BB FB. The seven FF/BB zero-incompatible threads form a connected spanning TREE of the 8-branch core, while the other nine FB threads permit equality. Therefore a zero-incompatible-thread cycle is NOT necessary for an intrinsic critical source, even at undirected girth eight. This does NOT refute the LSPV-3 short-thread-forest theorem: all 16 threads are short and K4,4 has cycles.

All branch weighted forbidden-color loads equal eight; after removing any thread, remaining loads are at least six, so weighted-four peeling stalls while an original-arc solver reconstructs SAT witnesses cheaply. No universal lower bound follows.

Independent core enumeration checked 5^7 anchored colorings: 0 H models and 16 positive deletion counts [14,4,1,6,15,10,11,4,21,15,9,14,9,11,20,1]. Independent original-arc AC3/MRV had 23 UNSAT DFS calls for H and obtained 32/32 complete deletion witnesses, <=31 calls. All original arcs verified, and each missing arc fails in its corresponding witness.

**OPEN:** increasing-girth intrinsic critical promise NP-hardness and unrestricted uniform SAT-only witness lower bound. Retest against GF(5), treewidth, adaptive variable orders and compact circuits. Require independent LSPV-5/TMR review. Existing agent enabled/paused states and schedules unchanged. P versus NP OPEN.

Artifacts:
- Report: research/agents/lspv-1/2026-11-18_LSPV1_T5_H24_GIRTH8_ZERO_TREE_COUNTEREXAMPLE.md
- Python: experiments/t5/lspv1_h24_zero_incompat_tree_20261118.py
- Original source: research/agents/lspv-1/certificates/2026-11-18_LSPV1_H24_GIRTH8_CRITICAL_NO.t5
- Evidence: results/raw/arc/2026-11-18_LSPV1_H24_GIRTH8_MINIMAL_EVIDENCE.json
