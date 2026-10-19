# HOURLY-QUERY7-SANITY | 2026-10-20 (scheduled hourly check)

**Status: P versus NP remains OPEN.** No root `main.tex` edit.

Independent finite sanity check of the CONDITIONED-HARD-SPARSE-QUERY7 inequality
`Pr_F[hit] <= h_q + eta`, `h_q = 1 - C(N-k,q)/C(N,q)`, with `F` uniform on an arbitrary
subset `H` of the weight-`k` strings of density `1-eta`. Exhaustive over all weight-`k` strings,
random `H` (eta ~ 0.2, 200 trials each) and random zero-path probe sets `Q`, for
(N,k,q) = (8,2,3), (10,3,4), (12,2,5): no violation. Status: COMPUTATIONAL (finite, restricted
bit-query model only; not a machine lower bound, no CHMY transport, no SAT-to-MKTP reduction).
Chunking: three parameter triples, each well under 1 s.

Observation: the bound only uses that conditioning on a subset of density `1-eta` inflates any
event probability by at most `eta` additive in the TV sense; it is model-restricted and does not
touch the load-bearing open arrows.

% END_OF_VERIFIED_NOTE::HOURLY-QUERY7-SANITY
