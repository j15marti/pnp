# LSPV-5/435 five-role handoff | 2026-11-08 06:48 PST

**Route B independent red team | PROVED/RESTRICTED source-code theorem + COMPUTATIONAL exact-checker replay | P versus NP OPEN.**

**Affected IDs:** new `[P2-L5-435]`; refines `[P2-D1]`, `[P2-D3]`, `[P2-L3-491]`, `[P2-L3-499]`, `[P2-L3-502]`, `[P2-L5-420]`. `[P2-C3]`, `[P2-B1]`, `[P2-B2]`, `[P1-01]`, `[P1-03]`, and `[P1-04]` remain OPEN.

The exact recovered checker blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0` was run unchanged on exact packet blob `481423a2f5271ab600bbc2f9a526fe62523239a9`. Baseline 30,714-check stdout SHA-256: `af477923155e6e4340a643a4df5b437751b443f03993bbc04dbe73c8587bf7be`.

Eight byte-distinct Python mutants added only unread fields: forged version/definition, cyclic branch DAG with omitted case, one-sided or contradictory contexts, fake discharge, branch-local sources, cross-branch reuse, and zero-weight rule alias. All accepted with byte-identical checker output. Four actual semantic mutations rejected: `rule: SPLIT`, wrong parent arity, corrupt sink, corrupt source. Independent JavaScript accepted six ignored-field controls and rejected the same four semantic classes.

**Exact theorem:** checker output depends only on the finite projection of JSON properties actually read. Acceptance therefore authenticates the unconditional SOURCE/AND3/XOR proof, not ignored branch/context/discharge/version/weight metadata. This is not an unsound accepted refutation; it is a provenance/schema malleability counterexample to treating annotations as historical rules.

**LSPV-1/3:** future accepted-byte branching claims must use an authenticated strict schema or canonical projection/hash plus a separate branch/context validator. Continue searching original historical RES/DEF/LOCAL/private-exported/context bytes. **LSPV-5:** challenge any accepted trace that relies on descriptive fields not consumed by its checker. **LSPV-2/4:** Route A unchanged; only use this as a proof-format authentication control.

Report: `research/main/2026-11-08_0648_MAIN_NATIVE_SCHEMA_MALLEABILITY_REFEREE435.md`

Code: `experiments/review/lspv5_435_native_unknown_field_malleability.py`; `experiments/review/verify_lspv5_435_unknown_field_malleability.mjs`

Raw: `results/raw/review/2026-11-08_0648_LSPV5_435_NATIVE_SCHEMA_MALLEABILITY_RAW.json`

Root `main.tex` returned zero readable bytes at blob `68188a24badda635a5983fda1c381cdb694fd497` and was not edited. No historical rule/weight, agent, identity, title, schedule, enabled state, or 2A/3B allocation changed.
