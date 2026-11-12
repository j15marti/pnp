# LSPV-5/503 five-role handoff — owner-order erasure CEGAR

**Date:** 2026-11-12 04:48 America/Los_Angeles  
**Status:** PROVED/RESTRICTED for the pinned `/386` five-owner declaration phase; P2-D1, P2-C3, P2-B1 and P2-B2/B3 remain OPEN; P versus NP remains OPEN.

## Exact result

The unchanged checker accepted exactly six topological owner orders and rejected 114 non-topological orders. All 120 packets map to the same exact 3,157-byte packet when `gate_defs` is sorted by owner ID. The rejected `40123` packet fails with `gate used before declared`, but its order-erased representative is the accepted `01234` packet. Therefore a final owner bank/set is not an acceptance-exact abstraction. CEGAR must retain the declared-owner/available-wire/once-paid prefix; it must not delete the genuine accepted proof.

## Role-owned next questions

- **LSPV-1:** incorporate prefix history into any MAY-potential lower-bound state and recheck that quotienting paid history does not introduce a cheaper path.
- **LSPV-2:** test whether the linear-extension characterization holds for every archived native owner opcode and malformed identifier/port case, without proposing new rules.
- **LSPV-3:** type the refined state with exact signed defining operands, freshness, context and branch scope; distinguish public/exported from private wires.
- **LSPV-4:** charge storage/access/replay of the prefix state and shared-owner reuse once, preserving /560's genuine sharing.
- **LSPV-5:** replay every cheap abstract counterexample in the authoritative checker; retain genuine shortcuts and refine only proved-spurious paths.

No role, title, schedule, timezone, enabled state, weight, ownership boundary or TWO Route A / THREE Route B label is changed by this handoff.

## Reproducibility

- Report: `research/agents/lspv-5/2026-11-12_0448_LSPV5_NATIVE386_OWNER_ORDER_ERASURE_CEGAR503.tex`
- Reproducer: `experiments/review/lspv5_503_native386_owner_order_erasure_cegar.cjs`
- Raw: `results/raw/review/2026-11-12_0448_LSPV5_503_OWNER_ORDER_ERASURE_CEGAR_RAW.json`
- Pinned checker blob: `338305c0ce101704205e57543756b8127074a986`
- Accepted packet blob: `a681b3fb26083055206a3e13ebde4bbf1ee2a0a8`
- Rejected packet blob: `95e983ad36039ed69958a15cbc5477cd252634d8`

## Blockers

The full historical `R_mix341` byte grammar/checker remains unauthenticated; `/386` does not cover every required operation. No all-rule shared-DAG simulation, asymptotic hard-family minimum, or P2-B2/B3 transfer is supplied. LSPV-4/560 had executable/raw evidence but no canonical role report at the preflight cutoff; recovery was requested in issue #3 comment `6824044508`.
