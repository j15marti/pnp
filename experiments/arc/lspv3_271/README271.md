# LSPV-3 STRICT22-BACKDOOR-SELECTOR-GATE271

Time label: 2026-10-31 02:19 America/Los_Angeles (PDT).
Role: LSPV-3 Adaptive Certificate Theorems. Primary integrated target: fully charged universal residual-SAT/ARC to actual FLMV forbidden region. **Not proved. P versus NP remains OPEN.**

## Replicate

Python 3.10+; requires SciPy and NumPy for separate off-policy exact 0/1 static-backdoor integer optimization. No random nondeterminism; fixed seed 2711031.

    python run271.py
    python verify271.py
    python corrupt271.py

`run271.py` generates raw271.json and summary271.json, and `verify271.py` independently validates the original-source outputs without importing the producer; `corrupt271.py` rejects three deliberately perturbed source/diagnostic records. Please run from within this directory. A fresh run rewrites results deterministically. All files in manifest271.json are checksummed.

## Contents

- `...GATE271.tex`: mathematical report, exact quantifiers, proofs, original corpus/literature and limitations.
- `run271.py`: deterministic producer for 19 source CNFs with source-indexed occurrence/extreme controls, 2SAT/Horn/GF2 recognition and UP-first DPLL baseline.
- `verify271.py`: independent full-label, all-pair extrema, Gray flip and proof-tree verification.
- `corrupt271.py`: three rejection tests.
- `fixtures271.json`: original-source control clauses from preceding LSPV-3 experiments.
- `raw271.json`: complete reproducible outputs and authenticated source clauses.
- `summary271.json`: compact table of all source outcomes and host-event proxies.
- `verified271.json`: independent check counts.
- `console271.txt`: producer output.
- `manifest271.json`: SHA256 manifest; the manifest itself is not self-checksummed.

## Computational status

Reported operations are deliberately selected Python-level events, NOT physical indexed random-access FLMV Turing machine time or joint writable space. Search-policy failure and source recognition work are included in controller events, but the off-policy MILP optimization to discover minimum strong syntactic backdoors is **NOT** included as a controller stage or an efficient selector. The full original-clause S/U matrix stored in the raw results is an *offline adverse diagnostic* and not a proposed FLMV low-space state. The produced strict22 easy-family witness and the signed-graph orbit escape prevent transfer of any claimed local static-backdoor barrier to arbitrary algorithms. The 2026-10-30 affine MCSP theorem only applies to its restricted source-independent affine transformation model.

## Deterministic falsification controls

Pair SS/SU/US/UU modes, full source-indexed signed occurrences with both S and U and their inversions, global 0^n and 1^n, per-clause true-count status 0/1/2/3, intermediate Gray flips, exact non-tautological resolution and prohibited cube, witness/UNSAT tree, multiple independent strict22 sources, polarity renamings, affine and easy controls. Unsatisfiability is NEVER inferred from two failed endpoints or exhausted bounded repair.

Repo project governance: https://github.com/j15marti/pnp/issues/3 ; main proof contract: research/review/spines/2026-10-30_UNIVERSAL_PARAMETERIZED_FLMV_CONTRACT1.md.

## GitHub portable rehydration

GitHub also contains the full original-source record as `raw271.json.gz.b64` and the self-checking `restore271.py`. Run `python restore271.py` before `python verify271.py` to check the archived raw record without recomputing it. The restored raw JSON SHA-256 must be `79bfb830e3a18f99bbaf6d5489b7924882e7aaa244f50726db23f0cf837783bd`. Then run `python run271.py` to independently regenerate the record from original source fixtures. The complete raw JSON, baseline UNSAT proof trees, original-clause S/U modes, Gray trails and exact certificate statistics are included. This file documents an experiment, not a native FLMV simulation or universal complexity separation.
