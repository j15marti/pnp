# LSPV-3 CERTIFIED-RACE-SPACE-GATE275 (2026-10-31 06:28 PDT)

Status: restricted exact symbolic counterexample (peer review pending) and independently verified finite experiment. P versus NP remains OPEN.

Run with Python 3.11+ standard library:

```bash
python experiment275.py
python verify275.py
python space275.py
```

The original fixture `fixtures271.json` is copied unchanged from the verified 2026-10-31 LSPV-3 HORN-AFFINE-MIXED-GATE274 archive. `experiment275.py` is the producer. `verify275.py` independently checks every stored original signed clause, its local S/U and complement inversions, all pairwise extremes against complete enumeration of shared variables, the actual 0/1/Gray status records, the complete source SAT/UNSAT labels for 19 formulas, the winner's original-source certificate, the from-scratch dyadic restart clock, and five deliberately corrupted certificates. `space275.py` is an abstract losing-tape demonstration, not a native FLMV simulation.

Outputs: `raw275.json` (full ~764KB machine-readable record), `summary275.json`, `verification275.json`, `space275.json` and `manifest275.json`. The original full source remains immutable; no solver receives a separate Boolean value for any signed occurrence. All solver counts are selected Python semantic events, not native Turing machine instruction counts. Python materializes source and proof objects. No true power-short ordinary SAT children or guest arbitrary-A calls are produced.

Corpus and novelty audit: the dyadic finite-portfolio lemma already appears in LSPV-3 ADAPTIVE-SELECTOR-GATE255 and LSPV-1 ARC-SPACE-CAPPED-DOVETAIL262; it is not claimed new. The new restriction-level observation is a paired SAT/UNSAT source example of the space-competition failure, supported by an explicit synthetic tape accounting trace and verified six-policy finite benchmark.
