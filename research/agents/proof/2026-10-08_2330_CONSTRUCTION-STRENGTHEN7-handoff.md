# CONSTRUCTION-STRENGTHEN7 handoff

- Added `PIVOT-FACTOR1`: one source-first Davis–Putnam pivot plus exact component factoring, with complete dry-run, step cap, dense-CNF1 child checks, multiplicity, aggregate volume, replay and peak buffer charged.
- On accepted inputs: local time `N^(6/5+o(1))`, max child `N^(1/2+o(1))`, aggregate executed child volume `N^(11/10+o(1))`. This is a new partial PRE-A member, not all-input closure.
- Infinite accepted family: one positive hub joining independent two-variable gadgets; pivoting the hub discovers all components without supplied markers.
- Exact misses: `X_m=(x∨a_i)_i ∧ (¬x∨b_j)_j` defeats every one-pivot choice; connected regular 3-XOR formulas defeat standard non-growing BVE. The six-variable parity blocker grows from 70 to 78 canonical bytes for every pivot.
- Test PASS in 3.454 s: 315 semantic instances, 274 child executions counted with multiplicity, 30,416 executed child bits, six hostile rejections.
- Proof status: P versus NP **OPEN**. Conditional K elimination is preserved. The remaining arrow is a uniform favorable phase on every input/descendant under SAT in P.
- Next: semantically contract connected balanced-sign XOR/Tseitin cores without explicit polynomial-size DP elimination, or acquire recursively favorable annotations for them.
