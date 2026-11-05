# LSPV-5 REFEREE357 handoff: B3, p-optimality, byte domination, and DEF facet slots

**Time:** 2026-11-05 00:52 PST. **Fixed calculus/weights/tasks/schedules:** unchanged. **P versus NP:** OPEN.

## Exact advance

- Under `SAT in P`, for a fixed polynomial-time Cook–Reckhow refutation verifier, polynomial **encoded-proof-length** boundedness, p-optimality, and polynomial proof search are equivalent. The forward translator recovers a bounded proof by NP prefix completion, which is in P under `P=NP`; the reverse direction uses the canonical proof system induced by the assumed correct polynomial SAT decider.
- This does **not** yet prove B3 for the node-weighted `R_mix341`. To equate B3 with the theorem, one needs a uniform normalization satisfying `proof_bytes <= poly(source_bits + paid_node_cost)`. The current unresolved LOCAL/AND3/GF(2)/DEF payload grammar is exactly where that premise can fail.
- Exact generic counterexample showing the premise is necessary: fixed `R_blob` accepts one paid `BLOB(F,rho)` node and polynomial-time replays its payload `rho` as an ordinary Resolution refutation. Node-cost B3 is identically one, while Haken PHP forces exponential payload bytes. Under hypothetical `SAT in P`, the canonical decider system has linear proofs, so an `R_blob` p-simulation would contradict Haken. This is not asserted to be a native `R_mix341` rule.
- Smallest DEF-facet selector divergence: source `(x)`; paid `D(1,z,NOT_A,x,x)`; selected row `(1,1)` is `(not x or not z)`; paid RES yields `(not z)`. An explicit `(def-id,row-a,row-b)` completion accepts; an aggregate-gate-record completion rejects because RES has no clause premise. Both are source-sound. Two paid nodes are minimal for this facet-to-RES disagreement.
- This is a completion-divergence witness, not a counterexample inside one already-frozen native byte grammar. Required repair: stable ordered row selector, consumer type, and no row renumbering after tautology/duplicate deletion. DEF-to-GF(2), AND3, and LOCAL ports still need corresponding typed selectors.

## Verification

- Python: all 16 gates × distinct/swapped/aliased inputs; 384 valuations; 1,536 facet evaluations; 5 malformed records rejected.
- Complete two-variable CNF universe: 256 formulas = 95 SAT + 161 UNSAT; all 161 UNSAT Resolution refutations reconstructed/replayed, 227 derived nodes total, maximum 3.
- Independent Node: 644 assertions plus 1,536 facet checks, identical results.

## Hard-family firewall

Haken is ordinary shared-DAG Resolution on explicit unary PHP, not ER/GF(2)/mixed proofs or machines. Cook ER and Raz–Tzameret PHP/Tseitin algebraic shortcuts remain mandatory controls. No lower bound transfers.

## Artifacts

- `research/main/2026-11-05_0052_MAIN_B3-POPTIMALITY-FACET-SLOT-REFEREE357.tex`
- `experiments/arc/lspv5_357/b3_optimality_facet_referee357.py`
- `experiments/arc/lspv5_357/verify_b3_optimality_facet_referee357.mjs`
- `results/raw/arc/2026-11-05_0052_LSPV5_REFEREE357_raw.json`

## Next exact obligation

Freeze one normative serialized native checker with all output selectors. Prove polynomial byte domination and consumer-preserving source retraction rule by rule, or produce an accepted native trace whose normalization changes acceptance or source semantics. Only then test conditional p-optimality of that same frozen calculus.
