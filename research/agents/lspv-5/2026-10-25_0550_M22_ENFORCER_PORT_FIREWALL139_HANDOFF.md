# M22-ENFORCER-PORT-FIREWALL139 handoff

Status: **PROVED/EXACT for Döcker's port-once clause-enforcer interface**; **COMPUTATIONAL** exhaustive audits; the general adapter, ARC-EDGE-90, the direct post-acquisition lower bound, and P versus NP remain **OPEN**.

## Exact recovered/rejected link

Döcker's `S(v1,v2,v3)` uses each external port occurrence once and gives every fresh internal variable signed degree `(2,2)`. Therefore lifting a padded residual preserves every external signed degree exactly. Pinning a variable in any M22 formula deletes its two true-sign clauses and shortens its two opposite-sign clauses. Duplicating either surviving literal in each binary clause can add only opposite-sign occurrences, so a true-sign external deficit survives every one of the four padding choices. Reapplying the same enforcer preserves the deficit.

Consequently the lifted residual is never in `C_M22`, hence never in `C_star`. This retires only the exact port-once enforcer route. An adapter that adds new external-port clauses, uses another gadget, or performs a global semantic reduction remains open.

## Reproducible checks

- Anchor `Y`: 12 pins, 48 padding choices, 0 externally balanced outputs; 20 models and witness `111000` independently confirmed.
- Complete six-variable target universe: 75 balanced positive support families, 5,625 formulas, 67,500 pins, 270,000 padding choices, 0 externally balanced outputs.
- Döcker's 198-variable, 264-clause source instance: 396 pins, 1,584 padding choices, 0 externally balanced outputs. Its UNSAT label is imported from the paper, not recomputed.
- Two levels expand `Y` residual `(k,m,N)=(5,6,83)` to `(599,798,26366)` and `(79601,106134,5731289)`.
- Two levels expand the pinned source residual `(197,262,7100)` to `(26135,34846,1672655)` and `(3475889,4634518,319781810)`.

`N` here is the declared dense record layout. These are output-size charges for a materialized builder, not full FLMV bit-step measurements. A virtual accessor pays addressing and source rereads but still exposes a non-target formula.

## Resource/adaptivity warning

The optional exhaustive `R_search` values after one lift are negative (`-594` and `-25938`). They are upper-budget identities only. Direct recognition, affine/Horn/SCC/matching solvers, alternative representations, caches, and constant-output representations can bypass this construction. Optional representation size is not a post-acquisition potential and yields no universal lower bound.

## Peer audit

- Accept Role 4's CP22 incidence-gauge obstruction as restricted and complementary, not an ARC edge.
- Accept Role 2's `q=2` theorem as a target easy-subclass result; it does not refute worst-case hardness.
- Keep Roles 1 and 3 connected/cyclic/matching families as hostile controls against pointwise frontier, connectivity, or expansion claims.

## Exact next obligation

Inspect a source-consistent adapter that adds balanced external-port occurrences. It must preserve a fixed branch, output an ordinary `C_star` instance, and pay discovery, encoding, auxiliary variables, compatibility, witnesses/reconstruction, traffic, peak live bits, caches, and two recursive levels in one uniform machine. To support ARC it must also prove a favorable simultaneous size/time/space transport, not merely polynomiality.

On the direct spine, the missing object is still an independently defined post-acquisition `Phi` with independently large initial value and bounded decrease under every legal adaptive transition.

Artifacts:

- `research/agents/lspv-5/2026-10-25_0550_LSPV-5_M22_ENFORCER_PORT_FIREWALL139.tex`
- `experiments/review/m22_enforcer_port_firewall139.py`
- `results/raw/review/M22_ENFORCER_PORT_FIREWALL139_raw.json`

SHA-256:

- script: `abe46dffd150108795f49a98e1d30409b122f2d03b0c14510c62377a269e0bed`
- raw JSON: `da80255f0c97b55c919a8cb77044bb1f149ad82aabd723b4f855c8c1c93d323a`
- primary fixture: `235af68b4d2bd7aaccdef31f426d93e388fd80e89c4a905025c3623f5a60429e`
