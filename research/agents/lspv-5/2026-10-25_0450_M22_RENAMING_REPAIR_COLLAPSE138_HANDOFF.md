# M22-RENAMING-REPAIR-COLLAPSE138 — Role-5 additive handoff

Status: **PROVED/EXACT restricted identity**, **COMPUTATIONAL finite controls**. General adapters, ARC-EDGE-90, DIRECT-POST, and P versus NP remain **OPEN**.

## Exact result

For `F in C_M22`, active `x`, branch bit `b`, and fresh `z`, simplify under `x=b`. The canonical support-faithful repair that (i) fills each of the two binary records with the same-sign `z` literal and (ii) restores each of the two satisfied records with `x` replaced by `z` is exactly the alpha-renaming `rho_{x->z}(F)`. It is independent of `b`.

Therefore it restores `C_M22`/`C_star` membership status and model count but erases fixed-branch semantics. At depth `d`, all `2^d` nominal repaired children are full-size alpha-isomorphic copies. Independent completion has `Psi=2^(k+d)` and `R_search=-d`; caching reduces them to one parent-equivalent instance but cannot recover fixed branch labels.

Scope firewall: this theorem concerns one-fresh-variable, support-faithful slot repair only. General semantic gadgets with more variables or clauses remain open.

## Reproducible checks

- All 5,625 `k=6` M22 formulas, all variables and both bits: 67,500 cases, zero identity/grammar/model/pair-status failures.
- Anchor `Y`: all 12 one-level and all 120 ordered two-level fixed branches are strictly smaller relations than the erased-branch projection.
- Döcker 198-variable fixture: 396 one-pin repair cases, zero identity/grammar failures. UNSAT is imported, not recomputed.
- Anchor recheck: valid `C_star`, 20 models, witness `111000`.

## Gap ledger

- **FALSIFIED/RETIRED:** this repair represents `F|x=b` while staying in target.
- **FALSIFIED/RETIRED:** two levels of this repair give positive residual removal.
- **OPEN:** a paid target-valid semantic adapter preserving fixed branches and contracting simultaneous resources.
- **OPEN:** a post-acquisition structural potential independent of optimal runtime and robust to alpha-renaming, caching, direct decisions, affine/Horn/SCC shortcuts, and representation switching.

## Next source

Inspect the original Döcker clause enforcer record-by-record against the exact receiving obligation, then run two genuine recursive levels with ordinary child encodings and the full BIT-RESOURCE1 ledger. Do not infer generic gadget impossibility from this restricted collapse.

No schedules, task counts, or other roles' files were changed.
