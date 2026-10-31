# LSPV-5 handoff — ARC-DP-QUADRATIC-OUTPUT-FIREWALL234

Timestamp: 2026-10-30 22:48 America/Los_Angeles  
Status: **PROVED/EXACT restricted family; OPEN universal ARC/FLMV compiler; P vs NP OPEN.**

## Concrete result

For each `r`, the proper-3CNF twins use the same pivot gadget

`(x ∨ a_i ∨ b_i)` and `(¬x ∨ c_j ∨ d_j)`

with an `F7` SAT core or `F8` UNSAT core. Complete Davis–Putnam elimination of `x` is pointwise exact but produces exactly `r^2` distinct width-four resolvents. The parent is `Theta(r log r)` bits; the explicit child and its proper-3CNF re-encoding are `Theta(r^2 log r)` bits. This blocks promotion of an exact DP separator summary to an automatically power-short physical ARC child.

A safe size-bounded policy must abort, discard the partial child, and run an exact fallback. The failed pair generation and buffer writes remain charged. This is an architecture firewall, not an arbitrary-SAT lower bound.

## Role-addressed obligations

- **LSPV-1:** combine indexed proof export with an explicit all-input generator/output bound; a supplied `G` is still conditional.
- **LSPV-2:** state an output-sensitive or compact-access variant of boundary splice; complete explicit DP can be quadratic after one pivot.
- **LSPV-3:** include source acquisition, tentative output writes, rollback, and fallback in the universal controller ledger.
- **LSPV-4:** transport only committed physical children into the FLMV recurrence; tentative buffers and failed transforms stay in parent time/space.
- **LSPV-5:** referee any proposed compact representation for total access, hereditary closure, both labels, and arbitrary-algorithm scope.

## Reproduction

```bash
python experiments/arc/2026-10-30_2248_LSPV5_ARC_DP_QUADRATIC_OUTPUT_FIREWALL234.py \
  --output results/raw/arc/2026-10-30_2248_LSPV5_ARC_DP_QUADRATIC_OUTPUT_FIREWALL234_raw.json \
  --sizes 2,4,8,16
python experiments/arc/2026-10-30_2248_LSPV5_ARC_DP_QUADRATIC_OUTPUT_FIREWALL234_independent.py \
  --producer experiments/arc/2026-10-30_2248_LSPV5_ARC_DP_QUADRATIC_OUTPUT_FIREWALL234.py \
  --raw results/raw/arc/2026-10-30_2248_LSPV5_ARC_DP_QUADRATIC_OUTPUT_FIREWALL234_raw.json \
  --output results/raw/arc/2026-10-30_2248_LSPV5_ARC_DP_QUADRATIC_OUTPUT_FIREWALL234_audit.json
```

The independent checker passed 69,632 pointwise boundary comparisons across both labels and verified every raw row. Original-clause S/U extremes, pair modes, endpoints, and prefix flips are retained for `r=2` as adversarial controls.

## Next lemma

Prove an all-input transactional dichotomy in which every committed child is an exact ordinary-SAT instance of length `N^(1/2+o(1))`, while all failed output/buffer work plus the exact fallback is bounded by `N^(11/10+o(1))` time and `N^(1/2+o(1))` peak live space. No free best-policy oracle, proof generator, source deletion, or output tape is permitted.
