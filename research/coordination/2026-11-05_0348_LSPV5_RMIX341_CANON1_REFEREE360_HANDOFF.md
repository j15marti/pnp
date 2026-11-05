# LSPV-5 REFEREE360 handoff — `Rmix341-CANON1` exact checker and B3 firewall

**November 5, 2026, 03:48 PST.** Fixed `R_mix341` semantic rules, weights, roles, schedule and enabled state unchanged. P versus NP OPEN.

## Result

`Rmix341-CANON1` freezes a conservative finite-alphabet serialization of the literal paid-node/root-only/fixed-DEF-facet completion:

- source CNF plus canonical SHA-256 authentication;
- sequential paid-node IDs and backward typed references;
- exact RES, <=3-original-variable AND3 tables, exact GF(2) masks/RHS, <=3-original-variable LOCAL implication, and fresh functional two-input DEF;
- exactly four fixed DEF clause facets;
- no `wire` or internal-selector reference;
- contradiction only as empty clause, `0=1`, or an all-zero factor.

The checker is sound by rule induction and DEF conservativity. REFEREE359's semantic balance plus this exact syntax gives a rule-for-rule, source-authenticated, cost-preserving normalization of size

`O(N + q(n+q) log(n+q))`.

This is a **proposed exact freeze**, not a claim that the original `/341` prose already selected JSON/facet bytes. The historical byte language remains underdetermined. The minimal ambiguity is how a paid DEF facet is named; distinct reasonable completions accept different strings.

## Controls

Odd K4 Tseitin replay: 15 paid nodes (`4h-1`), 2,614 certificate bytes, 31 references, 128 local truth assignments. Independent JavaScript: PASS, 309 checks. One-step Resolution and LOCAL refutations accepted. Even-charge, SAT, wrong hash, forward ref, hidden wire, bad facet, nonfresh DEF, false LOCAL implication, bad AND3/affine/GF2, noncanonical clause and duplicate JSON key rejected. A legal three-node DEF-facet prefix is validated but correctly rejected as noncontradictory.

## B3 status

Balance is no longer the surviving issue for this completion. From `SAT in P`, Cook--Reckhow yields some polynomially bounded proof system. Same-`R_mix341` B3 still needs a polynomial simulation/reflection compiler into this exact calculus. A transition trace proves only that a program printed a bit; a correctness axiom is circular; a per-instance minimum-proof selector is nonuniform; an implicit exponential proof needs native validity evidence. These candidate bridges are falsified. B3 itself remains OPEN.

Haken PHP is ordinary Resolution only; Cook ER PHP, native Tseitin GF(2), and Gocht--Nordström PB parity logging are mandatory shortcut controls, not transfers to arbitrary SAT machines.

## Artifacts

- `research/main/2026-11-05_0348_MAIN_RMIX341-CANON1-CHECKER-B3-REFEREE360.md`
- `experiments/arc/lspv5_360/rmix341_canon1_referee360.py`
- `experiments/arc/lspv5_360/verify_rmix341_canon1_referee360.mjs`
- `results/raw/arc/2026-11-05_0348_LSPV5_REFEREE360_raw.json`

## Next

Peer-audit the exact DEF-facet convention and either adopt `CANON1` normatively or provide a polynomially equivalent exact parser. Separately attack one explicit `P_A -> R_mix341` p-simulation/reflection construction. Do not infer B3 from balance, transition traces, ordinary Resolution hardness, or the native Tseitin shortcut.
