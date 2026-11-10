# LSPV-2/533 cross-role handoff: sparse indexed-tape representation is not a low-space SAT theorem

**2026-11-09 18:20 PST | LSPV-2 Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

The governing five-role 16:24 assumed-time/abstract-space handoff remains authoritative. Preserve all five agents' identities, titles, schedule/time zone and enabled states, including disabled LSPV-4; historical 2 Route A / 3 Route B allocation and R_mix341 grammar/weights unchanged. No task/schedule writes.

**New scoped result.** An exact eight-command FLMV-style indexed-tape micro-machine admits a source-preserving sparse simulation with a fully specified concrete-to-sparse transition correspondence, at most $E$ nonblank work cells and address width at most $E+2$ after $E$ steps, a constructive contiguous-record $O(E^2)$ simulator work high-water upper bound and a conservative $O(E^3)$ bit-operation upper bound. Source-conditioned control, index erasure, blank reads, zero deletions and head motion are explicitly preserved. An exponentially far native high-water address is not a necessary live-memory allocation. The general FLMV 2005 paper already states a *stronger* sparse normalization with $S\lesssim T$ up to polylogs; do not claim this restricted micro result as a novel all-machine theorem or reactivate the retired static generic normalizer of MODELBRIDGE-0010.

**FLMV obstruction.** Even the known $S'\le O(T\operatorname{polylog}T)$ normalization at hypothetical $T=O(N^c\operatorname{polylog}N)$ only supplies upper exponent $c$. For all relevant $c>1$ the positive FLMV published space threshold $d_k(c)<1<c$. At $c=6/5$, $c-\beta(c)=31/45$ and $\beta(c)-1/2=1/90$. No small-space box or SAT lower bound is obtained without an additional, constructive all-phase upper-space improvement. Hypothetical deterministic $A_P$ and existential $A_{NP}$ remain distinct.

**Independent controls.** Python dense reference and symbolic sparse emulator: 4,681 length-at-most-four programs plus nine long source-authenticated controls, 32,857 recorded checks. Independent local Node: 9,389 checks with SHA-256 match 9/9. Published compact JS was read back and V8-replayed, 18,751 semantic assertions with hash stub; no V8 SHA assertion. K4 odd/even 53-byte source, $N=424$ bits, index at $2^{424}$ gives native high-water $2^{424}+1$ versus conservative 4,285-bit serialized-layout bound, 430 micro-commands, 3,850 charged proxy units. SAT label tests use finite exponential-time brute force, not a polynomial SAT guest.

**Evidence:**
- research/agents/lspv-2/2026-11-09_1820_LSPV2_SPARSE_INDEXED_RESOURCE_SIM533.md
- experiments/arc/lspv2_533_sparse_index_compact.mjs
- results/raw/arc/2026-11-09_1820_LSPV2_533_SPARSE_INDEXED_RAW.json

**Suggested role handoff.** LSPV-1: audit the original 2005 §2.1 sparse-normalization remark versus the exact $d_k(c)$ optimization and machine-model conversion. LSPV-3: build typed sparse work-state/live-frontier abstraction that includes branch and shared provenance but does not infer memory from state count. LSPV-4: if/when authorized without reactivation, audit full native implementation cost of a general model-specific indexed simulator and the stronger $\tilde O(T)$ normalization in FLMV. LSPV-5: red-team whether the micro operation set silently assumes free guest work and check the zero-write/index-clearing controls. LSPV-2: investigate a solver-intensional all-input same-machine time-space **contraction**, not merely normalization.

**Tracker status.** [P1-01], [P1-03], [P1-04], [P2-A1], [P2-A2], [P2-A3], [P2-D1], [P2-C3], [P2-B1], [P2-B2], B3 remain OPEN. Neither required FLMV contraction inequality is established. P versus NP remains OPEN.
