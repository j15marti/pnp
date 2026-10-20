% CLAUDE HOURLY REPORT::SCHUR_SQUARE_CONTROL1::2026-10-20T21:45Z

# Hourly check, 2026-10-20 21:45 UTC (06:45 KST)

## Repo state
Newest commit is `edb94eb5` (CHMY Bridge 33 handoff, 06:29 KST), about 13 minutes before this check. It follows MAIN
RESTRICTION-SERIALIZATION-BARRIER33 and the Grok 4.7 review annotation in `main.tex`. No new PRs in this window.
MAIN-33 status: two conditional SAT-to-FLMV routes, COMPACT-HISTORY20 as a diagnostic, and no promotion of the restricted barriers to an
unrestricted SAT lower bound. **P versus NP remains OPEN.**

## Own work: matched-random-code control for the Schur-square ledger item (PQ ledger item 1)
Script: `experiments/review/schur_square_control_2026-10-20.py`. Raw output: `results/schur_square_control_2026-10-20.json`.
It runs in seconds and has one invocation. Field is F_97, with 5 random seeds per (n,k).

- COMPUTATIONAL: for Reed-Solomon [n,k] codes, dim C^{*2} = min(2k-1, n) in all 5 tested (n,k).
- COMPUTATIONAL: for uniformly random [n,k] codes, dim C^{*2} = min(k(k+1)/2, n) in all 25 trials.
- Classification: EXACT OBJECT TRANSFER (the Schur square is the same object as in the PQ distinguisher literature, with the dimension
  gap RS vs random known from Cascudo-Cramer-Mirandola-Zemor style results). The experiment is a control only.
- Consequence for the repo: raw square dimension separates structured from matched-random codes only when k(k+1)/2 < n.
  When it saturates at n, as in 4 of the 5 rows, the invariant is blind, so a claim based on "square dimension is large" must
  report the regime. That is a hostile control, not a hardness result.
- Algorithmic caveat (per AGENTS.md): the RS low square dimension is a weakness exploitable by distinguishers, so hidden
  structure is not a hardness source here.

Not claimed: any link to SAT lower bounds, MCSP, or the FLMV/MMW routes. That bridge is missing and stays OPEN.

## Next falsifier
Extend to shortened/punctured codes and Hilbert-function (degree-3 power) saturation to see whether the structured/random gap survives past the
degree-2 saturation point.

% END_OF_VERIFIED_REPORT::CLAUDE::SCHUR_SQUARE_CONTROL1
