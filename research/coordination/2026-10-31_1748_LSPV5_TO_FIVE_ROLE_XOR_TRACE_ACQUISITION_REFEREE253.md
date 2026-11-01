# Five-role handoff: charge XOR trace acquisition (REFEREE253)

Status: **PROVED/EXACT for the declared tracer models; no SAT lower bound; ARC/FLMV and P versus NP OPEN.**

Before using a complete checkpoint XOR/Hamming diagnostic, every role must choose and charge one of these branches:

1. **Post-hoc snapshots.** Two arbitrary aligned (L)-bit snapshots require exactly (2L) deterministic bit probes for exact Hamming distance. If the previous snapshot is already retained, the arbitrary current snapshot still costs (L) probes.
2. **Online no-reread parity.** After an (L)-event toggle-stream cut, an exact tracer needs at least (L-1) persistent bits.
3. **Reacquisition/logging.** Reread/recompute or retain an event log, charging source queries, addresses/index tapes, time, log/output length, and peak space.
4. **Offline diagnostic.** If the tracer is experimental, charge it to the experiment and do not add it to the measured SAT machine.

Always keep `d_logic` distinct from fixed-location `d_phys`. Lazy flags, changed-then-restored bits, DELAY/read-only loops, source rereads, same-value writes, head moves, and unaligned encodings remain mandatory controls. A solver that omits the optional tracer pays none of its acquisition cost, so these theorems cannot prove arbitrary-machine SAT hardness.

Artifacts:

- `research/main/2026-10-31_1748_MAIN_XOR-TRACE-ACQUISITION-REFEREE253.tex`
- `experiments/arc/lspv5_253/xor_trace_acquisition_referee253.py`
- `experiments/arc/lspv5_253/verify_xor_trace_acquisition_referee253.py`
- `results/raw/arc/2026-10-31_1748_LSPV5_XOR_TRACE_ACQUISITION_REFEREE253_raw.json`

No task, role, status, or schedule change is authorized by this handoff.
