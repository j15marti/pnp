# Five-role handoff: LSPV-4/462 FLMV index-tape reset firewall
**2026-11-07 00:36 PST | Route A | P versus NP OPEN.**

**PROVED/RESTRICTED direct-physical-index reset counterexample.** FLMV Section 2.1 expressly erases an index tape when its associated work head performs an indexed jump; such a jump changes the counted work high-water. A guest may leave L consecutive nonblank 1 bits on its work-index tape after touching only M=1 work cell. A direct physical reset with work high-water at most L^k requires at least L-floor(k log2 L)-1 separately cleared index bits; an immediate erasing jump instead incurs high-water 2^L-1. Therefore LSPV-4/461's M-cell DATA/MARK clear count is valid **only for those two tapes**, not an O(M polylog N) COMPLETE raw guest reset.

**Corrected time envelope:** include actual INDEX tapes and head normalization. L_j<=O(T_j) index writes means direct guest+reset O(T_j polylog N+M_j polylog N+L_j) may still be O(T_j polylog N) under separately unproved work-address recovery; previous conditional exponent recurrences are not falsified. Do not claim an unconditional native interpreter. Source control: original odd-charge cubic-expander Tseitin is Resolution-hard, polynomial GF(2) shortcut, no unrestricted machine hardness. Native R_mix341 grammar/weights unchanged.

**LSPV-2 Route A:** check all guest work-index tape cleanup in POSTORDER TREE3 and virtual-input simulation; address this counterexample before claiming actual native resource bounds. [P2-A2] and recursive closure [P2-A5] remain OPEN.

**LSPV-1/3/5 Route B:** note work vs logical shared-DAG cost distinction, but do not migrate this guest-index result to R_mix341 proof-size claims. [P2-D1],[P2-B1],[P2-B2] OPEN.

**Trackers:** both proof1/proof2 reviewed, material resource evidence applies to [P2-A4]. [P1-04] and [P1-S3] reviewed with no status change. Existing five-agent allocation and schedules unmodified.

**Artifacts:** research/agents/lspv-4/2026-11-07_0036_LSPV4_RAW_INDEX_RESET_FIREWALL462.md; experiments/arc/lspv4_462_index_reset_falsifier.cjs; results/raw/arc/2026-11-07_0036_LSPV4_462_INDEX_RESET.json. Exact published JS reexecuted in V8, 72 assertions PASS, matching published raw JSON. These tests are finite host-level controls, not native FLMV performance or asymptotic computation lower bounds.
