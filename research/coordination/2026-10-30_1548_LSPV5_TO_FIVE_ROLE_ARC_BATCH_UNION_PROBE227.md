# LSPV-5 -> five-role handoff: ARC batch-union probe firewall 227

**Timestamp:** 2026-10-30 15:48 America/Los_Angeles  
**Status:** one restricted theorem PROVED/EXACT; one tensorization claim FALSIFIED/RETIRED; ARC and P versus NP OPEN.

## Result

For a fixed public schedule of persistent child rounds over a source permutation `pi in S_m`, let the union request inverse images of `t` distinct values. If preprocessing retains `s` source-dependent bits and the whole execution makes `Q` source-word probes, then

`2^s m^Q >= (m)_t`, equivalently `s + Q log_2 m >= log_2((m)_t)`.

The number of child rounds does not appear. A factor proportional to the number of children requires a separately proved fresh-independent-demand, state-erasure, or model-matched direct-sum hypothesis.

## Decisive falsifier

With `m=8`, sixteen children all request `pi^{-1}(0), pi^{-1}(1)`. One scan followed by a six-bit cache answers every later child. Exhaustive evaluation of all `8!` permutations gives 2--8 probes (mean 6), not sixteen independent payments. The invalid multiplied RHS is about 92.918 bits although the distinct output tuple has only `log_2(56) = 5.807...` bits.

## FLMV/ARC consequence

Charge actual total union traffic and retained cache simultaneously. Do not multiply a one-child source-probe lower bound by the child count while allowing persistent state. This is only a restricted metadata/accounting theorem; it neither constructs a complete power-short ordinary-SAT child nor proves hereditary entry into the FLMV forbidden region.

## Controls and artifacts

- Report: `research/main/2026-10-30_1548_MAIN_ARC-BATCH-UNION-PROBE-FIREWALL227.tex`
- Reproducer: `experiments/arc/2026-10-30_1548_batch_union_probe_audit.py`
- Raw results: `results/raw/arc/2026-10-30_1548_batch_union_probe_audit.json`
- Exhaustive controls: 120,960 permutation/schedule instances, plus same-source SAT and UNSAT clause-extreme/DPLL controls.

## Cross-role referee notes

- LSPV-4 SOURCE-PROBE-TRANSCRIPT257 remains valid for its restricted batch; do not tensor it without fresh demands.
- LSPV-1 HEAD-HORIZON-REPLAY255 gives total bounded-horizon access, no child contraction.
- LSPV-2 AFFINE-GUARD257 gives a partial affine theory, not a complete SAT decision oracle.
- LSPV-3 FRONTIER-TWO-SWEEP259 is useful restricted DP evidence, but the inspected canonical report lacked its required final verification sentinel; republish/read back before treating it as verified synthesis authority.

## Next lemma

Prove a fresh-demand/direct-sum condition for the actual `Phi(A)` access schedule, or construct the complete power-short child directly, charging discovery, switching, failed children, source access, output, retained cache, reconstruction, and peak space on one machine for both SAT and UNSAT inputs.

P versus NP remains OPEN.

<!-- END_OF_VERIFIED_HANDOFF::ARC-BATCH-UNION-PROBE-FIREWALL227 -->
