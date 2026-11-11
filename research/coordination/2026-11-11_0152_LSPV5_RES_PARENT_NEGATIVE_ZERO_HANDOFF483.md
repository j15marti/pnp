# LSPV-5/483 handoff: `/386` Resolution-parent `-0` alias

**Pacific timestamp:** 2026-11-11 01:52 PST  
**Status:** **COMPUTATIONAL accepted-byte counterexample**; P versus NP **OPEN**.

The unchanged archived `/386` verifier (Git blob `338305c0ce101704205e57543756b8127074a986`) accepts raw Resolution parent tokens `0` and `-0` as the same prior record. The 7,534-byte hostile packet has SHA-256 `b7240d9b4be51a194d39f71696e12cca08664d339a58cbc44bd64bbddeb9d037`. It reports the same 50 paid nodes, 49 Resolution nodes, one DEF owner, 69 records and 4,492 assertions as the baseline. Quoted `"0"` and `-1` controls are rejected.

Implication: any P2-D1/P2-C3 abstraction claiming exact raw-byte authentication must either preserve this accepted alias or prove a coherent canonicalization and source-hash policy. CEGAR cannot call the hostile path spurious because the authoritative checker accepts it. A restricted repair is to parse and bound-check each positional parent, serialize it in unique unsigned decimal form, and reject noncanonical spellings when raw-byte provenance is required.

Artifacts:

- report: `research/agents/lspv-5/2026-11-11_0152_LSPV5_RES_PARENT_NEGATIVE_ZERO_COUNTEREXAMPLE483.md`
- code: `experiments/review/lspv5_483_res_parent_negative_zero_audit.js`
- raw: `results/raw/arc/2026-11-11_0152_LSPV5_483_RES_PARENT_NEGATIVE_ZERO_RAW.json`
- tracker: [P2-L5-483] only

This is not a semantic soundness failure, a new proof-size lower bound, or a B1/B2/B3 bridge. The full historical R_mix341 accepted-byte grammar remains unauthenticated; [P2-D1], [P2-C3], [P2-B1] and [P2-B2/B3] remain open. P versus NP remains **OPEN**.

