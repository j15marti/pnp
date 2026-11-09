## LSPV-5/446 | 2026-11-08 16:03 PST | Route B red team | official XLRUP replay + provenance/interface audit | P versus NP OPEN

**Affected proof-chain ID:** add **[P2-L5-446]**, refining **[P2-L3-514]**, **[P2-D1]**, **[P2-C3]**, **[P2-L5-413]**. **[P2-B1]**, **[P2-B2]** remain OPEN. `proof1.txt` unchanged.

**IDEA -> SEARCH -> ITERATE:** Built the actual pinned `meelgroup/frat-xor@18cd6bc...` CakeML `cake_xlrup` from its distributed assembly (binary SHA-256 `56e2bc4a...`) and independently generated the six /514 strict cubic odd-Tseitin source/proof pairs. All K4/K3,3/cube/Prism8/16/64 baselines returned exact `s VERIFIED UNSAT`; 36 missing/foreign-hint, bad-parent, flipped-XOR, nonempty-export and source-literal corruptions printed checking-failed diagnostics. This closes only /514's external official-execution gap.

**Two red-team boundaries:** (1) adding an ignored comment changes complete source bytes/SHA while the identical proof still verifies, so bare XLRUP authenticates parsed constraints, not a separately named exact byte string; (2) every rejected corruption returned process status `0`, so status-only wrappers are unsafe—automation must require the exact verified marker. Neither is a failure of the HOL logical soundness theorem. The external four-hint `i x` remains non-native to historical paid at-most-binary-premise `R_mix341`; no all-rule lower bound or B3 follows.

Report: `research/main/2026-11-08_1603_MAIN_OFFICIAL_XLRUP_SOURCE_BINDING_REFEREE446.md`; verifier: `experiments/review/lspv5_446_official_xlrup_audit.py`; raw: `experiments/review/raw/2026-11-08_1603_LSPV5_446_OFFICIAL_XLRUP_RAW.json`; handoff: `research/coordination/2026-11-08_1603_LSPV5_OFFICIAL_XLRUP_446_HANDOFF.md`.

Historical grammar/weights, five roles/IDs/titles/schedules/enabled states and 2A/3B allocation unchanged. P versus NP OPEN.
