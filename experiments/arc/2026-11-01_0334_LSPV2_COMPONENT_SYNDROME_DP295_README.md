# LSPV-2 COMPONENT-SYNDROME-DP295, November 1, 2026, 03:34 PST

Status: conditional restricted theorem (external mathematical review pending), independently checked finite tests; all-input ARC, numerical FLMV transport, P=NP and P!=NP OPEN.

The canonical original source is every valid duplicate-free proper Döcker Monotone 3-SAT-(2,2) instance. The inherited signed-cycle affine-union theorem at delta=0 is used with source-authenticated edge-disjoint odd binary cycles. For vertex-disjoint cycle factors we count compatible edge selections with an exact GF(2) syndrome-trellis recurrence; for overlapping-variable factors, exhaustive checked selections. Every SAT witness is rechecked on the original clauses. Refutations are derived by source-aware XOR row provenance. Nothing here proves a uniform polynomial SAT algorithm or a native FLMV lower bound.

## Reproduction commands

From this folder in Python 3.11+, stdlib only:

```
python syndrome295.py
python verify295.py
python verify_source_cert295.py
python physical295.py
python verify_physical295.py
python signed_controls295.py
python semantic295.py
```

The independent source checker replays the historical U198 UNSAT certificate and the V198 SAT witness. The separate fixed-layout three-tape simulator is an offline diagnostic, and physical event streams are stored in compressed JSONL. No host word-time number or simulated physical XOR delta is claimed to be a native indexed read-only-input Turing machine lower bound.

Files `results295.json`, `independent295.json`, `independent_source_cert295.json`, `physical295.json`, `semantic295.json`, and `signed_controls_summary295.json` contain the raw/derived audit. The mathematically complete LaTeX report, PDF and literature records are included. `SHA256MANIFEST295.txt` hashes every payload file in this archive apart from itself. All experiments are deterministic with no random seed.