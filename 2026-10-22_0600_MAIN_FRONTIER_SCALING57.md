# FRONTIER-SCALING57 — source-frontier width on random 3CNF

Timestamp: 2026-10-22 ~06:00 KST. Global status: **P versus NP OPEN.**

## Corpus reviewed (this hourly check)
Repo head 0d2f0b64 (05:23 KST): root main.tex (minimal, LSPV-5 region + LSPV-1..4 regions all OPEN), SOURCE-JOIN-COHERENCE56 report, LOW-IMAGE-REPLAY32 handoff. New since last check: SOURCE-JOIN-COHERENCE56 (join coherence; unjoined local sampling retired as RP algorithm; bounded-frontier DP is restricted-only), LOW-IMAGE-REPLAY32 (restricted image-replay obstruction to SAT->MKTP reductions with strict exponent slack).

## Question
SOURCE-JOIN-COHERENCE56 showed exact frontier DP is poly only if width is O(log n), and that the wrapper's boundary 2 is not the clause/source frontier. Does a greedy clause order keep the frontier small on hard-ish instances?

## Result (COMPUTATIONAL, finite)
Random 3CNF, m = 4.26n, 5 seeds each, greedy min-new-variable clause ordering (script: experiments/review/2026-10-22_frontier_scaling57_audit.py, raw: ..._raw.json; each run <30 s):

| n | greedy width (5 seeds) | mean width / n |
|---|---|---|
| 20 | 16-18 | 0.87 |
| 40 | 31-33 | 0.81 |
| 80 | 60-63 | 0.77 |
| 160 | 119-121 | 0.75 |
| 320 | 229-237 | 0.73 |

Width is roughly 0.73n and decreasing slowly in the ratio; it is not O(log n) at these sizes, so bounded-frontier DP gives 2^(Theta(n)) here. This is a heuristic upper bound on the optimal width (greedy, not optimal), so it shows the greedy order fails, not that no good order exists. Literature-side expectation that random CNF incidence treewidth is linear in n at constant density was NOT verified this run (one standard search returned only random-graph treewidth results); treat as unverified.

## Classification
- Failed-transfer check: "small wrapper boundary => small frontier" stays RETIRED (consistent with SOURCE-JOIN-COHERENCE56).
- Coding-theory/PQ ledger and barrier-transfer preflight: not performed in full this hourly run; no PQ claim made.

## Next test
Replace greedy with a min-fill / separator-based order and a SAT-solver-hard planted family to bound optimal pathwidth from below via a verified method.

Not done: root main.tex was not edited (this run is not an ownership-region update). No proof claim. Everything here is finite and heuristic.
% END_OF_VERIFIED_REPORT::FRONTIER-SCALING57
