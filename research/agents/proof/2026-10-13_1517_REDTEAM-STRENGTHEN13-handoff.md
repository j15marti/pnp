# REDTEAM-STRENGTHEN13 handoff

- **Result:** Berger et al.'s zero-cost subsumption invalidates naive one-line-per-proof-node semantic-CP accounting. A redundant split over `{empty clause}` is the smallest counterexample.
- **Repair:** Maintain a subclause at every node; resolve only when both pivot literals survive, otherwise return the pivot-free stronger parent. This yields at most `n` strict Resolution inferences and at most `|H|+n` semantic-CP lines.
- **Exact scope:** PROVED/EXACT only for explicit tree-encoded DPLL certificates with one record per expanded rule occurrence. Pointer, macro, DAG-compressed, CDCL, and arbitrary one-bit-decider cases require separate simulation/extraction theorems.
- **Validation:** PASS in 0.676629 s under a 24 s alarm; 26,244 exhaustive local checks, 1,200 random valid derivation trees, 66,255 free resolutions, and explicit redundant-split/macro firewalls. Semantic digest `993d295cad0c280269a27747b4907b9930e3579383299ce3ab6a7adde5527ffe`.
- **Global status:** Conditional K elimination is unchanged. P versus NP remains OPEN.
- **Repository incident:** current GitHub root `main.tex` at head prefix `3be89e9...` is a 28-byte placeholder despite the commit message claiming restoration. Root was not edited. `main4.tex` and `main5.tex` were reconciled only through new manuscript inputs.
- **Next target:** fix a proof-logging CDCL/DRAT-like machine class and source-check exact proof-size, replay, deletion, restart, encoding, and no-weakening costs. Do not infer an arbitrary-decider bridge.
