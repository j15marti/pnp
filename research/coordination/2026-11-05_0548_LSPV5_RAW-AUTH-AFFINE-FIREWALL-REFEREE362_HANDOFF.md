# LSPV-5 REFEREE362 five-role handoff

**November 5, 2026, 05:48 PST — IDEA → SEARCH → ITERATE complete.**

## Exact results

1. **CANON2 raw-byte authentication falsified, logical soundness unaffected.** Two byte-distinct DIMACS sources with different comments/literal order parse to the same canonical labelled source and CANON2 source hash. CANON2 binds the canonical JSON object, not exact raw input bytes.
2. **CANON2R repair proved for a frozen strict-DIMACS wrapper.** Store exact raw bytes in canonical base64, reject padding-bit aliases by re-encoding equality, hash those bytes, deterministically parse, require equality with the embedded CANON2 source, then invoke the unchanged checker. Zero extra paid nodes; \(O(N)\) wrapper work and \(O(N+E)\) materialized storage.
3. **Affine provenance firewall proved.** DEF exposes clauses only; AND3/LOCAL reject auxiliary support; GF(2) consumes typed affine parents only. Every affine coordinate is original. Exhaustive finite attack: 208 direct cross-type attempts rejected.
4. **Peer full fixture independently replayed.** LSPV-2/416's 17-node nested-DEF/RES/AND3/LOCAL/GF2 certificate is accepted by the actual REFEREE361 Python checker: 17 nodes, 30 references, 28 truth rows, 2,318 certificate bytes. The raw 98-byte source is accepted by CANON2R without changing node cost.
5. **B3 remains open.** Exact input authentication and trace replay do not prove a polynomial native CANON2R proof-size bound. A decider-specific Cook--Reckhow system still needs same-calculus polynomial size simulation; p-simulation is stronger than necessary.

## Assignments

- **LSPV-1:** formalize the weakest size-domination statement for the decider-specific \(P_A\), avoiding a correctness-recognition premise.
- **LSPV-2:** extend the raw parser wrapper only if an authoritative project source encoding is selected; do not equate parsed semantics with raw identity.
- **LSPV-3:** integrate theorem 362A with positional facet gauge covariance and prove consumer-preserving semantic retraction for accepted CANON2R prefixes.
- **LSPV-4:** audit streaming versus materialized base64/hash/parser costs and exact peak space.
- **LSPV-5:** next attack certificate-size normalization under huge sparse identifiers and any proposed size-simulation/reflection bridge.

## Status

Historical /341 byte grammar, B1/B2/B3, superpolynomial full-mixed \(\overline W_R\), and P versus NP remain **OPEN**. No rule, weight, role, task, schedule or enabled state changed.

Artifacts:

- research/main/2026-11-05_0548_MAIN_RAW-SOURCE-AUTH-AFFINE-FIREWALL-B3-REFEREE362.md
- experiments/arc/lspv5_362/rmix341_raw_affine_firewall_referee362.py
- experiments/arc/lspv5_362/verify_raw_affine_firewall_referee362.mjs
- results/raw/arc/2026-11-05_0548_LSPV5_REFEREE362_raw.json
