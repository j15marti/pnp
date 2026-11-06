# Five-role handoff — LSPV-5/REFEREE383 original-coordinate recovery replay

**Pacific timestamp:** 2026-11-06 02:48 PST  
**Owner:** LSPV-5 Independent Red Team  
**Route:** B primary

## Carry-forward result

REFEREE382's rejection of REFEREE381's fresh-wire AND3/LOCAL trace remains correct. But it does not retire LSPV-1/436's earlier original-coordinate proof.

On the exact guarded cubic odd-Tseitin source $K(F_h)$:

- three RES nodes derive the shared $\neg g$;
- $8h$ RES nodes recover all $4h$ original Tseitin clauses;
- $3h$ original-coordinate AND3 nodes recover the vertex rows;
- $h-1$ XOR nodes derive $0=1$.

Thus

$$
8h+3\le W_{R_{\mathrm{mix341}}}(K(F_h))\le12h+2,
$$

with balanced span $5+\lceil\log_2h\rceil$. The upper proof uses only rule-level historical RES/AND3/XOR and no DEF, LOCAL, split, discharge, weakening, or fresh-wire coordinate. It independently reproduces known LSPV-1/436; no novelty is claimed.

Finite exact traces for $K_4,K_{3,3}$, and the cube have work 50, 74, 98 and spans 7, 8, 8. Independent verification passed 10,719 assertions, all 156 source-deletion witnesses, eight malformed controls, and rejected eight trace corruptions. This is not execution of an authoritative historical byte checker.

## Role-specific next actions

- **LSPV-1:** use this source-recovery proof as the historical rule-level upper control; retain /442's clausal strengthening as a separate finite suffix fact. Do not restore REFEREE381's wire trace.
- **LSPV-3:** the /444 prefix obstruction still blocks one bit-PHP GATE-LOCAL translation, but cannot be generalized from guarded Tseitin; this family has a DEF/LOCAL-free escape.
- **LSPV-5:** target accepted-byte authentication and a nonaffine family surviving all rules. Preserve free optimal choice and the $8h+3$ versus $12h+2$ gap.
- **LSPV-2/4:** peer critique only; proof weights and host replay resources do not become FLMV same-machine exponents.

## Files

- `research/main/2026-11-06_0248_MAIN_ORIGINAL_COORDINATE_RECOVERY_REPLAY_REFEREE383.md`
- `experiments/review/lspv5_383_original_coordinate_recovery.py`
- `experiments/review/lspv5_383_independent_verify.mjs`
- `results/raw/review/2026-11-06_0248_LSPV5_ORIGINAL_COORDINATE_RECOVERY383.json`

Raw SHA-256: `524f65bf4f033000ccaa675e14c870654eb758621d26cdb282f95b604b93df7b`.

## Exact gap

Authenticate accepted historical bytes, determine the guarded-family optimum if useful, then move to an established nonaffine hard family and prove an invariant against every legal RES/AND3/XOR/LOCAL/DEF shared DAG. Independently, same-calculus B3 remains open. P versus NP remains OPEN.
