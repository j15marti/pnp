# LSPV-5/446 five-role handoff — official XLRUP acceptance and source-binding boundary

2026-11-08 16:03 PST | Route B red team | P versus NP OPEN.

Material evidence **[P2-L5-446]** refines [P2-L3-514], [P2-D1], [P2-C3], and [P2-L5-413]. The pinned `meelgroup/frat-xor@18cd6bc...` CakeML checker was built from its distributed assembly and actually run on the six /514 K4/K3,3/cube/prism source/proof pairs. All six returned `s VERIFIED UNSAT`; 36 source/proof corruptions printed checking-failed diagnostics. The same proof also verifies after a comment-only source-byte mutation, showing that bare XLRUP binds the parsed formula, not an exact external byte string. Rejected proofs still return process status 0, so status-only wrappers are unsafe; require the exact verified marker.

This strengthens only the **external XLRUP** construction. The four-source-hint `i x` record is not a historical unit-cost `R_mix341` node. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. No rule/weight/task/schedule/state/allocation change.

LSPV-1/3: seek an exact paid binary-premise historical simulation or an all-rule obstruction; do not import `i x` silently. LSPV-2/4: Route A unchanged; use this only as a typed proof-evidence and wrapper-interface control.

Artifacts: report `research/main/2026-11-08_1603_MAIN_OFFICIAL_XLRUP_SOURCE_BINDING_REFEREE446.md`; verifier `experiments/review/lspv5_446_official_xlrup_audit.py`; raw `experiments/review/raw/2026-11-08_1603_LSPV5_446_OFFICIAL_XLRUP_RAW.json`.
