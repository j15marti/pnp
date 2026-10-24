# WRITE-SHADOW-ENDPOINT118 coverage and gap handoff

**Status:** P versus NP remains OPEN. The exact all-input ARC route is still missing.

## New exact link

For one fixed uniform total exact SAT decider on a blank-memory log-word RAM, count every mutable work-memory write, including caches and auxiliary tables. If time is `N^(t+o(1))` and writes plus one are `N^(u+o(1))`, a balanced sparse dictionary yields one fixed all-input FLMV random-access Turing machine with simultaneous time `N^(t+o(1))` and space `N^(u+o(1))`. Therefore the log-word-RAM time/write pair is forbidden whenever there is a `c > max(1,t)` with `u < beta(c)`, where `beta(c)=((c+2)/c^2-c)/2`.

This is **PROVED/EXACT in the declared restricted model, independent review pending**. It is a pullback of FLMV, not a new endpoint or a new ARC successor. It fails if polynomial mutable storage is omitted from the write count, words/addresses are unbounded, or the machine model is changed without a simulation.

## Rejection ledger

- **FALSIFIED/RETIRED:** `q` necessary source reads imply `q` work-memory writes. A fixed-template parity-chain CNF has all `q` orientation fields label-sensitive, but a streaming finite-control policy uses `q` input reads and zero work-memory writes, on both SAT and UNSAT instances.
- **PARTIAL/RESTRICTED:** `H(Y|K) <= S+qw` is exact when a specified `Y` must be reconstructed. An ordinary one-bit SAT decider need not reconstruct a witness, proof, DNNF, context table or history.
- **PARTIAL/RESTRICTED:** circuit size/depth/fan-in/fan-out/sharing/layout bounds transfer only under a stated circuit-model embedding. They do not directly bound arbitrary sequential SAT time.
- **FALSIFIED/RETIRED:** the historical universal `t+s<2 cos(pi/7)` SAT endpoint remains invalid.

## Peer compatibility

- Role 4 SENSITIVITY-SATURATION80 is accepted exactly for explicit source reads. Its source floor does not produce a positive target-work remainder or a write floor.
- Role 1 ARC-STREAM-FENCE117 is another conditional FLMV pullback, not an all-input successor.
- Role 2 TORUS-EXACT22-FRONTIER116 and Role 3 SPARSE-BOUNDARY-SUPPORT83 remain restricted structural results with direct-decision/representation escapes.
- CACHE-MISS-FRONTIER18 and VIRTUAL-CHILD-COMPOSITION61 remain correct conditional ledgers. Every cache update must be counted in the time/write model; neither source supplies the missing all-input hereditary both-label constructor.

## Adaptive resource ledger

The solver may switch among virtual evaluation, one-child materialization, partial caching, recomputation, SCC/Horn/affine solving, direct decision and fallback. The write-shadow theorem applies only after all mutable channels, failed policies, source rereads, representation changes, gluing, ancestors and peak buffers are included. SAT and UNSAT need not use the same success certificate; no label oracle is allowed.

## Reproducibility

- `2026-10-24_1448_WRITE_SHADOW_ENDPOINT118_audit.py`
- `2026-10-24_1448_WRITE_SHADOW_ENDPOINT118_results.json`
- 417,023 assertion-accounted checks, zero failures.
- Script SHA-256 `daf908e0e9088dcb3458d1f8fc9efad17dcfa0aec46bc550a5ad89ee2e38081d`.
- Raw JSON SHA-256 `fd5c87f59c0146abbbd3411d3bb80e1a265248e9d2d95fac0478df284c39cb21`.

## First missing implication

Produce a fixed uniform all-input exact SAT route from cofinally many achievable polynomial seeds to the curved FLMV forbidden region, or equivalently (for the declared charged log-word RAM implementation) into its time/write shadow, while charging every source read, child bit, write, cache, switch, gluing step and peak live bit. No reviewed source proves this.

## Next artifact tranche

Instrument the original CACHE-MISS-FRONTIER18 audit and selector/virtual-child constructor bodies so every mutable write, free-register assumption, cache update, regeneration, and source dereference is reported. Test both SAT and UNSAT parents and compare virtual, materialized, partial-cache and direct-decision policies.

<!-- END_OF_VERIFIED_HANDOFF::LSPV-5::WRITE-SHADOW-ENDPOINT118 -->
