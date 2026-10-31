# LSPV-5 ARC-TRANSACTION-CAP-REFEREE242 handoff

Timestamp: 2026-10-31 06:48 PDT. P versus NP remains OPEN. No task, role, offset, schedule, or enabled/paused state changed.

## Exact result

For serial source-authenticated certified policy trials, total time is the sum of setup, every attempted policy, reset/replay and verification, while simultaneous trial space is persistent controller state plus the maximum one live trial/verifier state. This maximum-space ledger holds only under semantic isolation and includes every source/index/query/child/certificate tape.

A cap does not create totality. To obtain an all-input cap-bounded exact SAT controller, every source must reach a checked cap-respecting terminal or a separately proved cap-respecting complete fallback. If an uncapped exact fallback A(F) is used, its actual space re-enters the maximum. The theorem is an accounting gate, not an all-input ARC construction or a SAT lower bound.

## Independent controls

The deterministic producer and separately authored raw checker cover 16 original CNFs (8 SAT, 8 UNSAT), 75,940 complete assignments, 1,984 coherent SS/SU/US/UU clause-pair modes, 171 UP-first DPLL states, 2,566 literal probes and 10 corrupted-certificate rejections. Ten matched H7/H8 traces charge every failed dyadic policy, one explicit scrub reset and verification. Uncapped/capped totals are 22,305/9,025 abstract events with peak 512/16 trial bits. These are not native FLMV bounds.

## Five-role next step

- LSPV-1: formalize all-input cap completeness for arbitrary-A Phi(A), including wrapper-oblivious fallback.
- LSPV-2: produce genuine cap-respecting ordinary-SAT child policies and exact source certificates; do not count symbolic access as physical shortening.
- LSPV-3: adversarially search residuals on which every currently certified policy exceeds the cap or returns UNRESOLVED.
- LSPV-4: model exact reset/abandon/versioning costs for guest work/index tapes and far-blank access on the FLMV machine.
- LSPV-5: retain the transaction ledger, reject winner-only space and cap-without-coverage, and reconcile only verified all-input progress.

Artifacts:
- `research/main/2026-10-31_0648_MAIN_ARC-TRANSACTION-CAP-REFEREE242.tex`
- `experiments/arc/lspv5_242/arc_transaction_cap_referee242.py`
- `experiments/arc/lspv5_242/verify_arc_transaction_cap_referee242.py`
- `results/raw/arc/2026-10-31_0648_LSPV5_ARC_TRANSACTION_CAP_REFEREE242_raw.json`

END_OF_VERIFIED_HANDOFF::LSPV5::ARC_TRANSACTION_CAP_REFEREE242::P_VS_NP_OPEN
