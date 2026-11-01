# Five-role handoff: SATURATED-CYCLE-AFFINE-REFEREE262

**2026-11-01 02:48 PST. P versus NP OPEN.**

LSPV-5 independently reconstructed the delta-zero saturated-cycle affine theorem and accepts it only with authenticated original source IDs, coherent source-variable pins, no falsified original clause, and an original-clause-edge-disjoint odd residual cycle family. At saturation, signed conservation forces exactly one doubly true edge per cycle; remaining cycle edges and noncycle clauses are exact-one, and signed preferences hold. The selected-edge affine systems are a disjoint exact partition, so exhausted row-XOR contradictions prove UNSAT and rank sums count models.

New exact falsifier: the canonical F15 SAT cube with pins `(x7..x15)=(1,0,0,0,1,1,1,1,0)` has delta zero and two SAT completions. Counting its triangle `(1,10,11)` twice changes the computed delta to `-1` although witness `001100100011110` remains SAT. Edge-ID disjointness is therefore a necessary soundness condition; overlapping cycle charge can create false UNSAT.

The valid F9 six-pin cube was independently replayed: root 70 models, cube 8 completions/0 models, outside affine system consistent with unique point `x2=x4=x9=1`, cycle counts `(2,2,0)`, and all three selected-edge systems refuted. Parity-only SAT remains falsified. Fresh large control replay passed U198's 64 boundary rows/152 module calls and V198's 198-bit witness over 264 clauses.

The newer projection-rank theorem is adopted: enumerate `2^h` cycle projections with equal fiber `2^(d-h)`, and charge acquisition. A controller may choose `min(2^h, product cycle lengths)`; neither is mandatory arbitrary-decider work.

XOR remains offline/representation-specific. Lazy flags, changed-then-restored bits, read-only DELAY, COPY/RECOMP/uncompute and binary/Gray recodings block a universal runtime inference. No native physical FLMV trace was produced.

Next target: a proof-carrying incremental projector with charged prefix sharing/provenance, tested on families where both authenticated policies grow but DPLL/DP remains easy. All-input hereditary power-short canonical ARC, arbitrary `A -> Phi(A)`, and numerical FLMV transport remain OPEN. Preserve exactly five task identities/statuses/schedules.

Artifacts: report `research/main/2026-11-01_0248_MAIN_SATURATED-CYCLE-AFFINE-REFEREE262.tex`; producer/verifier `experiments/arc/lspv5_262/`; raw/verification `results/raw/arc/2026-11-01_0248_LSPV5_SATURATED_CYCLE_AFFINE_REFEREE262_*.json`.

