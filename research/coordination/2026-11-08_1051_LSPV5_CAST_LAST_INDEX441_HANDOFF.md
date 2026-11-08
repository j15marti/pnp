# LSPV-5/441 handoff: `/507` final-index generator bug and complete repair

**2026-11-08 10:51 PST | Route B independent red team | P versus NP OPEN**

## Result

The published `[P2-L3-507]` generator checks whether an origin index is the final index before checking whether it is the replaced clause. When the replaced clause is final, the vertex factor chain receives source $A$ containing fresh $u$ instead of paid `CAST(C)`, and the generator's own original-variable support guard rejects the certificate.

Exhaustive replay across K4, K3,3, cube, every 72 clause positions and fees 1,2,4 gives 207 accepted and nine rejected valid cases. The failures are exactly the three final indices at three fees. A one-line selector repair accepts all 216 and rejects all 216 corrupt CAST controls. Independent Python reconstruction confirms the support violation and exact repaired parity tables.

This corrects executable coverage only. `[P2-L3-507]`'s separately declared-calculus theorem is not refuted; historical `R_mix341` was not executed or altered.

## Next work

1. Merge the selector repair in LSPV-3 ownership if that role chooses; preserve the original snapshot.
2. Specify and authenticate external accepted trace bytes—`JSON.stringify` size is not a hostile-byte parser.
3. Recover the historical RES-to-factor/LOCAL-CONVERT route or prove its typed obstruction.
4. Keep `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]` OPEN. P versus NP OPEN.
