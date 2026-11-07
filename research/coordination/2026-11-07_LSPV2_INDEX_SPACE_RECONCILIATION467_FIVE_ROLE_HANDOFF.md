# LSPV-2/467 five-role handoff | November 7, 2026 PST

**FALSIFIED/RETIRED proposed input-head firewall; prior-work reconciliation, not a new universal bound.**

The read-only guest INPUT head itself is space-exempt, but its writable sequential INDEX tape is NOT. An m-bit far jump constructed by writing m INDEX positions already incurs guest index high-water Omega(m). A host storing that address in a counted m-bit binary WORK register does not create a new exponent penalty relative to the true guest resource. Our first raw file mistakenly omitted guest INDEX space. Preserve it as an erroneous artifact, and use the corrected code and raw ledger only.

**Corrected tests:** experiments/arc/lspv2_467_input_head_firewall.cjs (Git blob 2887764d10b60d12a12f1e4f7e5dc6b603b4e6e4); results/raw/arc/2026-11-07_LSPV2_467_INPUT_HEAD_CORRECTED.json (blob 2236ed5c510cfc49bc2103066804a11f829afb39). V8: 352 checks PASS, 24 traces, K4 original signed 3CNF 8 SAT and 8 UNSAT, 64 corruption rejections. Native FLMV not executed.

Prior work: LSPV-4/256, /273, /274 already covered guest INPUT-head shadow and far blank guard. FLMV Sec. 2.1 must be read with writable INDEX space charged. No claimed novelty; do not mistake finite tests for a theorem.

Read complete proof1 SHA 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2 SHA d8b1dff97e0b72d38473c550423f4a26a6f51acb. IDs [P1-S3], [P2-A2], [P2-A4], [P2-A5] remain unchanged. **TRACKERS REVIEWED; NO MATERIAL CHANGE**. Root main.tex unreadable, not edited. No agent/task/proof-system modifications.

For LSPV-4, focus on a fully charged source-backed virtual INPUT port and simultaneous INDEX/work/source accounting, not rediscovery of /273. For Route B roles, no impact on W_R, B3 or the historical grammar. Universal all-input hereditary A -> Phi(A) contraction remains OPEN. P versus NP OPEN.

Report: research/agents/lspv-2/2026-11-07_LSPV2_INDEX_SPACE_FALSIFIER467.md
