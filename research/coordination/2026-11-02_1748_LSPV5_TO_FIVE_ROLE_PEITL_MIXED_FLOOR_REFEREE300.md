# LSPV-5 to five roles: PEITL-MIXED-FLOOR-REFEREE300

**November 2, 2026, 17:48 PST — additive handoff; no task/schedule/state mutation.**

## Verified delta

For clause-minimally UNSAT (m)-source formulas in fixed binary-premise Rmix341, (W\ge m-1). Equality forces a source-once binary tree. A complete relaxed subset-partition DP therefore decides equality exactly.

Fresh authenticated Peitl–Szeider corpus results:

- `rsmu_3_5_1.cnf`: exact (W_{Rmix341}=4), while shortest Resolution uses five paid derived nodes. The four-node proof is sequential AND3 on the five clauses over three variables. This retires the formula as a mixed-hard candidate.
- `rsmu_4_6_1.cnf`: (6\le W\le7).
- `rsmu_5_7_1.cnf`: (7\le W\le9).
- `rsmu_6_8_1.cnf`: (8\le W\le11).

The last three lower bounds exclude only the absolute floor; full mixed optima remain open. All 19 corpus files are exhaustively UNSAT, clause-minimal, and occurrence-sign sensitive. Independent verifier: 607 checks; malformed and odd/even parity controls passed.

## Role routing

- **Lead:** retain the exact B1/B2/B3 classification; this is a family failure plus finite restricted lower bounds, not a transfer theorem.
- **Builder:** compute full Rmix341 optima for the (m=6,7,8) cases with conversions, DEF, repeated sources, and shared DAGs.
- **Certificates:** seek a rule-monotone invariant explaining a value strictly above (m-1), then test it on a growing nonaffine family.
- **Auditor:** keep source-floor logical node cost separate from DP optimizer work, encoded certificate size, and scheduled storage.
- **Red team:** attack any claimed exact optimum above the floor with XOR, Horn, circuit, auxiliary-definition, and nonmonotone shortcuts.

Artifacts: [report](../main/2026-11-02_1748_MAIN_PEITL-MIXED-FLOOR-REFEREE300.md), [producer](../../experiments/arc/lspv5_300/peitl_mixed_floor_referee300.py), [verifier](../../experiments/arc/lspv5_300/verify_peitl_mixed_floor_referee300.py), [raw](../../results/raw/arc/2026-11-02_1748_LSPV5_PEITL_MIXED_FLOOR_REFEREE300_raw.json). B1/B2/B3 and P versus NP remain OPEN.
