# STRICT22-MINIMUM-REFEREE218 raw manifest

Run timestamp: 2026-10-30 02:48 America/Los_Angeles  
Seed: `202610300248`  
Status: `COMPUTATIONAL` for finite checks; the lower bound `mu(3,2,2)=20` is a cited `KNOWN THEOREM`.

## Files

- Producer: `experiments/clause_extremes/2026-10-30_0248_STRICT22-MINIMUM-REFEREE218_repro.py`
  - SHA-256: `59e09403b458cbb7b60efe1ea1daa9718008f17c992d0cd99915a115d05a849d`
- Independent checker: `experiments/clause_extremes/2026-10-30_0248_STRICT22-MINIMUM-REFEREE218_check.py`
  - SHA-256: `c1fb2c8eba5ec0b4860a6332a3fac983920859b9f8ec664b65e51cacb5a0d7b3`
- Compact result: `results/raw/clause_extremes/2026-10-30_0248_STRICT22-MINIMUM-REFEREE218_summary.json`
- Full expanded raw trace: `2026-10-30_0248_STRICT22-MINIMUM-REFEREE218_raw.json`
  - bytes: `1,856,054`
  - final SHA-256: `9441acd55d6574cbb9f2b54af240edc82adbd2513d01e25e71368aa6945d1f7f`
- Independent checker output: `2026-10-30_0248_STRICT22-MINIMUM-REFEREE218_check.json`
  - status: `PASS`
  - checks: `2,407`

The full raw trace contains every source clause and occurrence target/inversion, every indexed pair matrix, bounded triple modes, global endpoints, complement checks, flip trails, source resolvents, prohibited cubes, models, and solver ledgers for all eight controls. It exceeds the preferred GitHub contents-API payload, so GitHub carries this checksum manifest and the compact summary; the complete bytes are in the durable reproducibility bundle recorded by the run handoff.

Durable reproducibility bundle: `libfile_c2d28aaa9db88191b04a8365cd5229f1`.

## Scope

The program independently validates the 20-clause W1 upper-bound witness and finite controls. It does **not** reproduce the SAT Modulo Symmetries lower-bound computation of Zhang--Peitl--Szeider. P versus NP remains OPEN.
