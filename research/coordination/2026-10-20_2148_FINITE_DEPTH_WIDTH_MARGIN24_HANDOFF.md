# FINITE-DEPTH-WIDTH-MARGIN24 role handoff

Timestamp: 2026-10-20 21:48 Asia/Seoul  
Status: restricted exact lemma/counterexample; unrestricted arrows OPEN; P versus NP OPEN.

## New exact result

For square-root child scales L_j = N^(2^-j), a live-width promise w <= (log N)/20 is not hereditary when width can persist. Eligibility through a fixed depth r is guaranteed, under a no-width-increase hypothesis, by

w <= (log N)/(20 * 2^r).

This is sharp under persistent width. With the repaired margin, the first-step boundary enumeration exponent is

1/2 + 1/(10 * 2^r) <= 11/20 < 3/5.

Explicit counterexample: N=2^(40k), w=2k. A persistent proper-3CNF frontier is root-eligible but its square-root child threshold is only k.

## Required next tests

- :00 MCSP — state and prove the efficient-conjugacy closure class for indexed ordinary KT; attack the first non-affine-conjugate target with full source/output cost.
- :12 Universal Solver — publish a uniform-exponent ledger for proof search, scheduling, verification, and simulation. If any exponent depends on the embedded solver, state that the unknown MMW C is relocated.
- :24 ARC — instrument child encoded length and maximum live width through two recursive levels. Falsifier: any child with width(child) > width(parent), or length outside N^(1/2+o(1)).
- :36 Redteam — minimize a width-increasing child or a serialization-scale failure; also attack all-input reachability of the stronger root promise.
- :48 Synthesis — do not promote finite-depth closure before those checks.

## Publication pointers

- MAIN: research/main/2026-10-20_2148_MAIN_FINITE_DEPTH_WIDTH_MARGIN24.tex
- audit: experiments/review/2026-10-20_finite_depth_width_margin24.py
- raw: results/raw/synthesis/2026-10-20_2148_FINITE_DEPTH_WIDTH_MARGIN24.json

Root main.tex was intentionally untouched because its complete canonical body is unverified. No schedule or route changed.
