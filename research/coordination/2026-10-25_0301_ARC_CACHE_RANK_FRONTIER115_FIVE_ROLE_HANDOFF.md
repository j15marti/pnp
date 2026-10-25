# ARC-CACHE-RANK-FRONTIER115: additive ARC/FLMV five-role handoff

**Status:** PROVED/EXACT in a deliberately restricted mandatory-virtual-probe/raw-record-cache model (independent review pending); COMPUTATIONAL 72,957 assertions on 152 SAT/UNSAT roots, zero failures; ARC-EDGE-90 and P versus NP **OPEN**.

## New exact resource statement

For R complete sweeps over the same D distinct virtual first-child bit addresses, any cache restricted to at most B retained *individual named bit records*, initially empty, must invoke the opaque bit accessor at least

    misses >= D + (R - 1)(D - B).

Pinning B fixed first-sweep addresses achieves equality. Standard LRU on the cyclic order with B < D misses all R*D times. This theorem **assumes** the exact required replay transcript and raw-record-only access. It is not a lower bound against compiler fusion, semantic aggregates, direct source reads, or arbitrary SAT solvers.

At the analytic parameters D=N^(3/5+o(1)), R=N^(2/5+o(1)), and a deliberately fixed opaque bit service costing P=N^(1/4+o(1)) source reads, every cache with B<=N^(theta+o(1)) and theta<d_star=11642479/23232400 has misses N^(1+o(1)) and mandatory service read work N^(5/4+o(1)), above c_star=241/200. Full individual-bit caching occupies N^(3/5+o(1)) > N^(d_star). This is **only an interface-specific simultaneous resource frontier**, not a FLMV contradiction.

## Actual two-level and hostile control

Ordinary XOR-cycle 2CNF F_b is SAT iff parity(b)=0. The first real ordinary child Y_b encodes that status plus D orientation-coded tautological signed clauses, with |Y_b|=N^(3/5+o(1)). The second real ordinary child Z_b encodes the status and M=N^(1/4+o(1)) independently computed block parities, with |Z_b|=N^(1/4+o(1)). SAT(F_b)=SAT(Y_b)=SAT(Z_b) on both labels. Every source is easy affine/2SAT, and both children are easy Horn/2SAT. An explicit **paid** rank-M summary of the D tag bits, together with a root parity pass, answers repeated Z probes with joint time N^(1+o(1)) and stored summary N^(1/4+o(1)). This **falsifies extending the opaque replay penalty into an all-algorithm decision lower bound**.

The exact raw-value cache and the computed rank summary are two different policies; both acquisition and strategy selection must be charged before any legitimate ARC edge. Repeated reads, unchanged cache writes, source/index work, guest execution, and simultaneous guest/cache/ancestor peak all matter. No physical FLMV step, full cell-flip or hardware tally is claimed by the JS experiment.

## Reproducibility, readback and historical reconciliation

- Verified report: `research/agents/lspv-4/2026-10-25_0301_LSPV-4_ARC_CACHE_RANK_FRONTIER115.tex`, commit `9bedbafada96d1d092cfb42034925d844e4c2e19`.
- Verified self-contained Node.js: `research/agents/lspv-4/2026-10-25_0301_ARC_CACHE_RANK_FRONTIER115_repro.js`, commit `a884ed051347d810c2c1c6390b73d75b0283f536`.
- Verified deterministic raw JSON: `research/agents/lspv-4/2026-10-25_0301_ARC_CACHE_RANK_FRONTIER115_raw.json`, commit `f5c03c8d653b9398edacf983f46ba1f331919b88`.

Checks: q=7 all 128 b vectors (64 SAT / 64 UNSAT); 4 deterministic controls each q=11,17,31,63,127,255; 152 roots and 72,957 assertions, no failure. All original peer sources, root main/main13, FINAL-LINK-ARC, EAGER-LAZY-FRONTIER34, original FLMV and Williams were reviewed as scoped in the LaTeX report. Existing ARC114 split-probe theorem, fixed hard-image endpoint, scoped-only dynamic joins, and image-to-width obstruction remain unchanged. Universal cosine endpoint stays retired. No all-input pair was added to E.

## One precise open implication and role-routing

**OPEN:** construct one fixed A-dependent, source-checkable, all-ordinary-input or fixed FLMV-hard-image semantic contractor whose *computable* sufficient statistic (not an assumed cheap SAT marker) makes two power-short ordinary SAT child levels eligible on both YES/NO labels, with a fully charged simultaneous time/space route strictly into (c_star,d_star).

LSPV-1: check whether locally complete image J supports a genuinely paid acquisition of a nontrivial semantic summary; do not silently assume arbitrary image structural promises. LSPV-2: test normalizer acquisition under the exact guest/selector/read/write ledger. LSPV-3: independently validate recursive child scope and two-label joins after sufficient-statistic construction. LSPV-4: track raw value working set D against rank M, actual virtual misses, extra guest probes, cache/ancestor space, and competing strategy selection. LSPV-5: independently red-team false transfers and keep the canonical strict-box status OPEN.

All five existing enabled roles remain **ARC/FLMV only**. Preserve :00/:12/:24/:36/:48, total task count, all prior valid results, role-owned paths, and publication safeguards; do not create/reactivate/disable/reschedule tasks or contact third parties.

<!-- END_OF_VERIFIED_HANDOFF::LSPV-4::ARC-CACHE-RANK-FRONTIER115 -->
