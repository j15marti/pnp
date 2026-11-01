# Five-role handoff: action-aware XOR delta replay (REFEREE254)

Status: **PROVED/EXACT in the declared logical event-replay model; no SAT lower bound; ARC/FLMV and P versus NP OPEN.**

For every valid duplicate-free proper Monotone 3-SAT-(2,2) source, if the current assignment/count/status state and authenticated four-occurrence index are already materialized, a variable-flip event reconstructs the complete next logical state and all changed record IDs. A fixed-length exact event code needs and suffices with `ceil(log2 n)` bits. Therefore a known online action does **not** require rescanning all `L=5n` logical state bits.

Charge one of four branches:

1. retain the `5n`-bit logical state and explicit incidence index, including construction/authentication/address/update/peak space;
2. reacquire or recompute them from the source, charging all source/index/head time;
3. compare arbitrary snapshots post-hoc, using REFEREE253's scan cost;
4. omit the diagnostic, paying no tracer-specific cost.

This does not emit a target child, prove hereditary re-entry, select a best policy, or transfer to the FLMV forbidden region. Logical event replay is not native `d_phys`; keep eager/lazy, Gray/binary, restored-bit, source-reread, unaligned, index-erasure and DELAY controls.

Artifacts:

- `research/main/2026-10-31_1848_MAIN_XOR-DELTA-EVENT-REFEREE254.tex`
- `experiments/arc/lspv5_254/xor_delta_event_referee254.py`
- `experiments/arc/lspv5_254/verify_xor_delta_event_referee254.py`
- `results/raw/arc/2026-10-31_1848_LSPV5_XOR_DELTA_EVENT_REFEREE254_raw.json`

No task, role, status, or schedule change is authorized.
