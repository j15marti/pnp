# LSPV-5/497 handoff: shared paid Resolution exists natively; band-rigidity criterion

**2026-11-11 15:48 PST | LSPV-5 Independent Proof Red Team | historical Route B | P versus NP OPEN**

- **COMPUTATIONAL:** LSPV-1/575's packet (archived /386, 62 RES, W<=63) has paid-RES fanout histogram {1:57, 2:4}, so four genuinely multi-consumer paid nodes are already natively accepted. An independent DP rebuild reproduces its exact clause multiset. In this run it was accepted again by the unchanged checker running as an OS Node subprocess.
- **The native checker enforces count-once exactly.** It rejected: per-consumer charging, an undercount, a dangling second consumer, a flipped pivot, a weakened shared clause, and zero owners (the known g>=1 floor).
- **Sharing gives no gain on this source.** The shared DAG costs 63; its tree expansion costs 67 and is still accepted. The tree-like W61 (60 RES) is better. That does not make sharing irrelevant in general (BIW 2004).
- **PROVED/EXACT band-rigidity lemma.** With the source prefix fixed, the parent-reference digit total is the same for every topological order whenever each derived node whose legal position range [S+a, n-2-d] straddles a boundary 10^k has fanout 1. LSPV-4/552's tree-like result is the special case. On the /575 DAG the total stays at 236 in all 3,000 sampled orders. The nonnative 9-vs-11 control must violate the hypothesis; it is correctly labelled nonnative.
- **Asks.** LSPV-2: report fanout histograms together with position ranges. LSPV-3: test the 579 shared-owner family against the lemma. LSPV-4: extend the encoding ledger to interleaved source/DEF orders, which the lemma does not cover. LSPV-1: keep W_R distinct from byte cost.

Report: `research/agents/lspv-5/2026-11-11_1548_LSPV5_NATIVE_SHARED_PAID_BAND_RIGIDITY497.tex`. Code: `experiments/review/lspv5_497_native_shared_paid_dp_audit.cjs`. Raw: `results/raw/review/2026-11-11_1548_LSPV5_497_NATIVE_SHARED_PAID_DP_RAW.json`. Status unchanged: P2-D1, P2-C3, P2-B1, P2-B2/B3 OPEN. Roles, schedules and weights unchanged.
