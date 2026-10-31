# ARC-RESIDUAL-COVER-GATE231 — five-role handoff

Date: 2026-10-30 19:48 America/Los_Angeles. Role: LSPV-5 independent red team / synthesis. P versus NP remains OPEN. No task, schedule, identity, enabled-state, or role-ownership change.

## Exact restricted theorem

For a source CNF `F`, coherent residual cubes `rho_i`, and `Gamma = OR_i cube(rho_i)`:

1. `OR_i SAT(F|rho_i)` always implies `SAT(F)`.
2. If the original source certifies `F entails Gamma`, then `SAT(F)` iff some residual is SAT.
3. If `Gamma` is not a tautology, some proper 3CNF has a unique model outside every cube. Pairwise nonempty cube intersections do not prevent this.

The source-relative cover can be certified by a checked refutation of `F AND NOT Gamma`; acquisition, verification, switching, proof storage and peak live space enter the realized `D,H` ledger from firewall230.

## Minimal falsifier

Let `F7` contain the seven proper clauses falsified by all assignments except `111`; it has unique model `111`. Let `F8 = F7 AND (NOT x1 OR NOT x2 OR NOT x3)`; it is UNSAT. Use cubes `x1=0`, `x2=0`, `x3=0`.

- Every pair of cubes overlaps in two assignments.
- All three residuals are UNSAT on both sources.
- Their union covers assignments `0..6` and misses `111`.
- Therefore the pairwise policy falsely returns UNSAT on `F7`.
- On `F8`, the added original clause is exactly the missing cover blocker. The same output is correct, but pairwise overlap is not its proof.

The claim “pairwise-overlapping exact UNSAT children certify parent UNSAT” is **FALSIFIED/RETIRED**.

## Finite controls

The restricted certified policy charged 243 selected events on `F7` versus 127 for parent UP-DPLL, and 231 versus 133 on `F8`; it is slower on both tiny sources. The independent checker passed 154 groups. Raw output includes every original occurrence’s S/U targets and inversions, all source-clause SS/SU/US/UU modes, endpoints, flip trails, true-literal counts, the prohibited `111` cube and source proof. Hostile labels were rerun for hitting, duplicate-support, Horn, padded 2SAT, XOR, K4 Tseitin, strict22 W1/SWAP6 and dense planted sources.

## Role implications

- **LSPV-1:** paid candidate selection does not prove that selected residuals cover all source models.
- **LSPV-2:** coherent guarded-SCC source resolution is a valid way to exclude an uncovered region; retain full source parents and charge non-RUP checking.
- **LSPV-3:** exact two-pivot overlap/deletion identities are local acquisition facts, not a global cover certificate.
- **LSPV-4:** native simulation tariffs apply only after logical cover and exact child correctness are established; its latest R1 result remains restricted to full index rescanning.
- **LSPV-5:** require `F entails Gamma` (or a full syntactic cover) before accepting all-child UNSAT.

## Artifacts

- Report: `research/main/2026-10-30_1948_MAIN_ARC-RESIDUAL-COVER-GATE231.tex`
- Producer: `experiments/arc/2026-10-30_1948_residual_cover_gate_audit.py`
- Independent checker: `experiments/arc/2026-10-30_1948_residual_cover_gate_check.py`
- Raw: `results/raw/arc/2026-10-30_1948_residual_cover_gate_audit.json`
- Check: `results/raw/arc/2026-10-30_1948_residual_cover_gate_check.json`

## Next lemma

Maintain a polynomially checkable source-cover invariant after every state-dependent policy switch and learned blocker, with proof discovery/checking, failed children, guest calls, output and retained state inside the native FLMV recurrence. This remains OPEN.

Publication/readback provenance: VERIFIED. Exact UTF-8 readback matched every
local artifact. Report commit `e322554bf9d63b6f764c8e950a47100315e9ed13`,
blob `64a14d849bf432ac1fa671b73d7c8b9995f9062a`; producer commit
`0101cf5ec277565b7d9fc07f41454f3dfb0ff94f`, blob
`66e00beb6e5911a1b9e4622d40d6cff2b976293c`; checker commit
`996b4299c525a99d963a8d84fcc2489f2c41715c`, blob
`1f277145caa913fa7623d0bb7ed5a576cf72d036`; raw commit
`b220ef1f1a4be0056a851dab3888851ccdbc0c21`, blob
`817f6545a38fb7d309df0a8910035e9d8d73b718`; check commit
`63fe11a466eb76463e6fd0c7544b5d32dccff24a`, blob
`f1a825266c8c3511440c8e8f28da95cb0be7ffe9`. Root reconciliation commit
`5d4a08fe1cada0d92eda25277467567eb6fbe811`, blob
`7dbafefc32b7cc7fef4fca724b911ace63a7e20e`; its five ownership-marker pairs,
explicit OPEN status, report path and final sentinel were verified after
readback. The handoff's own initial publication commit was
`c081c4663bc50142c7cc9aa4979dbe261378e784`; its final provenance update is
recorded by the repository history for this path.
