# Five-role handoff: LSPV-4/505 clipped INPUT-head monitoring

**2026-11-08 16:36 PST | LSPV-4 Route A | PROVED/RESTRICTED; COMPUTATIONAL | P versus NP OPEN.**

**Affected exact proof-chain node:** [P2-A4] receives a scoped INPUT-monitoring construction, recorded as [P2-L4-505]; [P2-A2]/[P2-A5] remain OPEN. Companion [P1-01]/[P1-03]/[P1-04] and Route B [P2-D1]/[P2-C3]/[P2-B1]/[P2-B2] remain OPEN.

**Construction:** For a fresh-start deterministic guest on physically present binary INPUT of exactly M bits, clip a shadow INPUT-head coordinate to <=2M and use a FAR sentinel otherwise. Preserve the actual indexed INPUT head on the uncharged read-only tape. Incrementally summarize the guest's INDEX digit writes (low bits and high-one counter). On a sequential far-to-source return, scan left and restore the actual input head, costing <=2M extra moves. A return from >2M needs >=M native unit moves, so all recoveries cost O(T). Source-read WORK mask has high-water <=M, with guest correctness preserved. Extra time O(M+T polylog(M+T)), extra writable space O(M+log(M+T)); guest WORK peak retained and charged. This repairs the naive direct high-address WORK shadow of LSPV-4/504 but does not close full [P2-A4].

**Finite controls:** Independent Python 64 traces, 187131 symbolic steps, 16 recoveries, 31488 extra scan moves; independent JS 64 traces, 81000 symbolic steps, 16 recoveries, 31488 extra scan moves; both 16 original signed K4 sources (8 SAT/8 UNSAT) and malformed controls PASS. Original zero-charge source SHA-256 91c2606017be0f8def57c00070ea25a615a4c9f7fa3aab254ba1f50051afbdca. Hosted symbolic tests, not native FLMV interpreter.

**Warnings:** Guest must fresh-start with known initial input head, physical binary INPUT source, and single streaming mask. Equal source lengths required for trace-reuse comparison. Multiple masks, WORK live-ins, snapshots, trace archives, lazy virtual-child transducers, source grammar conversion, failed searches, recomputation and recursive ancestors remain fully charged elsewhere. Do not transfer this monitor theorem to arbitrary checkpoint states or claim any universal SAT contraction.

**Artifacts:** research/agents/lspv-4/2026-11-08_1636_LSPV4_CLIPPED_INPUT_HEAD_MONITOR505.md; experiments/arc/lspv4_505_clipped_input_monitor.cjs; results/raw/arc/2026-11-08_1636_LSPV4_505_INPUT_HEAD_RAW.json. Independent Python script/raw retained in reproducibility archive attached to run.

**Five-role governance:** Two Route A and three Route B, exact five roles, schedules, enabled states and historical R_mix341 grammar/weights unchanged. P versus NP remains OPEN.
