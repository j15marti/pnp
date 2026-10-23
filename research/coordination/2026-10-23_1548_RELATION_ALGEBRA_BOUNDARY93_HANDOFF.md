# RELATION-ALGEBRA-BOUNDARY93 handoff

**Status:** P versus NP remains **OPEN**.

## New exact results

1. **Affine/permutation holonomy:** For arbitrary graphs with constraints `x_v=x_u+b (mod 3)`, a spanning-forest potential calculation decides satisfiability in `O(V+E)` word time and linear peak space. If consistent, the model count is exactly `3^components`. The one-hot CNF encoding is parsimonious.
2. **Feedback-vertex continuation:** For arbitrary explicit 3-by-3 binary relations and a supplied, verified feedback vertex set of size `c`, exact SAT takes `O(3^c * 9(V+E))` word time and linear peak space.
3. **Chord repair:** A cycle plus `h` chords has an explicit feedback vertex set of size at most `h+1`; the certified fallback improves from Role 4's `3^(2h) poly(N)` to `3^(h+1) poly(N)`.
4. **Endpoint:** Replacing functional permutation relations by inequality gives exactly graph 3-coloring and its one-hot CNF, an NP-complete language.

## Transport result

The cycle has an exact `q`-field lower bound on the all-zero input, but its CNF construction/recognition costs `Theta(q)`. Therefore the positive-remainder transport numerator is not proved positive. Direct inclusion preserves only `Omega(N/log N)` aligned-word acquisition. Enlarging the allowed relation language does not amplify the easy subfamily's lower bound.

## Cross-role reconciliation

- Independently proves Role 4 PERMUTATION-CYCLE54's modulo-three semantics and linear shortcut.
- Extends Role 2 COLOR-JOIN51 from forest quotients to supplied feedback vertex sets.
- Integrates Role 1 ONEPASS66: its one-pass state lower bound collapses under two charged passes, paralleling the failure of representation-specific obligations to cover arbitrary random-access deciders.

## Audit

- Seed `20261023`
- 7,831 assertions, zero failures
- 560 affine systems
- 1,380 arbitrary-relation/FVS instances
- 1,020 cycle orientations
- 152 cycle-plus-chord checks
- 970 one-hot CNF model-count checks
- 10.28 seconds

## Artifacts

- `research/main/2026-10-23_1548_MAIN_RELATION_ALGEBRA_BOUNDARY93.tex`
- `experiments/review/relation_algebra_boundary93_audit.py`
- `results/raw/review/RELATION_ALGEBRA_BOUNDARY93_raw.json`
- `research/coordination/2026-10-23_1548_RELATION_ALGEBRA_BOUNDARY93_HANDOFF.md`

## Highest-value next lemma

For one fixed NP-complete three-valued relation language and a succinct source-complete cyclic family, prove an all-decider algebraic-compression-or-continuation dichotomy that survives affine holonomy, cutset/treewidth DP, repeated passes, caching, alternate encodings, and decide-first normalization. No such unrestricted theorem is currently established.
