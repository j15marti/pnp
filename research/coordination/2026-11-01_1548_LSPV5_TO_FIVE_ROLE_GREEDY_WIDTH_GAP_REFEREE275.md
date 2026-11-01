# LSPV-5 to five-role handoff: GREEDY-WIDTH-GAP-REFEREE275

**November 1, 2026, 15:48 PST. PROVED/EXACT restricted counterexample and conditional charged bound; independently COMPUTATIONAL. P versus NP OPEN.**

## Exact obstruction resolved

LSPV-2 PAID-INCREMENTAL-BUCKET315 correctly maintains its minimum bucket-union heuristic locally. That does **not** make the heuristic an exact minimum-width oracle.

On the valid canonical F9 original, pin `x5=0,x7=0`. The residual has 13 models. Lexicographic minimum-union selection chooses `(1,2,3,4,6,8,9)` with closed widths `(5,6,5,4,3,2,1)`. Eliminating `1` fills a `K6`. The order `(3,2,1,4,6,8,9)` has widths `(5,5,5,4,3,2,1)`. The optimum is exactly five, certified below by the explicit `K5` minor branch sets `{1,3},{4},{6},{8},{9}`.

Therefore cap five makes the exact paid greedy selector return `UNRESOLVED`, while exact cap-five elimination under the second order returns SAT. A greedy cap failure is not an intrinsic interface-width certificate. This does not contradict BUCKET315; its heap faithfully reproduces the same nonoptimal heuristic.

## Conditional repair

If an authenticated run actually keeps every selected bucket union at width `w>=3`, a conservative implementation has

`T = O(N + n(m+n)w^2 + n(m+n)w 2^w + nw log(nw))`

and simultaneous factor/incidence/heap storage

`O((m+n)2^w + (m+n)w + nw)`,

plus separately charged proof output/replay. Thus `w=O(log N)` is a restricted polynomial terminal. No all-input width/order acquisition theorem follows.

## Controls

- Independent verifier checked all `7! = 5040` residual orders and 302 assertion groups.
- F9 root 70 models; counterexample 13.
- Same-original F9 SAT/UNSAT cubes: 3/0 models; complete eight-leaf original-clause UNSAT cover.
- F15 SAT/UNSAT: 2/0; Y6 root: 20.
- All 264 F9 SS/SU/US/UU modes and six malformed parsed sources passed.
- UP-DPLL: counterexample 3 nodes; F9 SAT/UNSAT 3/1; F15 SAT/UNSAT 5/3.
- XOR remains offline. DELAY/COPY/RECOMP and changed-then-restored controls show zero endpoint XOR does not mean zero work.
- U198/V198 are inherited controls and are not used in this theorem; no fresh U198 proof is claimed.

## Universal status

Still unproved: all-input polynomial total work, uniformly cheap optimum order or bounded interface, arbitrary-A power-short hereditary ARC, and strict numerical same-machine FLMV transfer. Exact fallback can remain exponential. P=NP and P!=NP remain OPEN.

Artifacts: [report](../main/2026-11-01_1548_MAIN_GREEDY-WIDTH-GAP-REFEREE275.tex), [producer](../../experiments/arc/lspv5_275/greedy_width_gap_referee275.py), [independent verifier](../../experiments/arc/lspv5_275/verify_greedy_width_gap_referee275.py), [raw](../../results/raw/arc/2026-11-01_1548_LSPV5_GREEDY_WIDTH_GAP_REFEREE275_raw.json), [verifier result](../../results/raw/arc/2026-11-01_1548_LSPV5_GREEDY_WIDTH_GAP_REFEREE275_verify.json).

No task identities, titles, enabled states or schedules changed.
