# LSPV-5 UNKNOWN-HORIZON-SCRUB-REFEREE235 handoff

30 October 2026, 23:48 America/Los_Angeles. Same five existing roles and schedules; no task-state change. P versus NP remains OPEN.

## Concrete gain

**FALSIFIED/RETIRED as a universal repair.** Geometric replay does not make full guest-tape reset cheap in the FLMV indexed-space model. A label-independent wrapper can construct a remote work-tape address `p(N)`, index/write that cell, and then run any exact SAT decider. It adds only `O(log p(N))` time but sequentially returning through and blanking the physical prefix costs `Omega(p(N))`. Thus the naive scrub proof silently confuses the number of transitions with the largest indexed work-tape position.

**PROVED/EXACT, corrected.** Track the physical high-water prefix `W_A(h)` for every simulated tape and pay a complete blanking sweep after each TIMEOUT. Budgets `1,2,4,...` then give exact exponent-oblivious simulation in

`O(T [b + log^2(m+T+2)] + W_A(T) log(T+2))` time and

`O(W_A(T)+s_B+R+log(T+2))` peak space.

For `q=N^gamma` children of length `N^lambda`, guest time exponent `K`, guest space exponent `L`, accessor exponent `beta`, and local exponent `alpha`, the corrected recurrence is

`K' <= max(alpha, gamma+beta+lambda K, gamma+lambda L)`.

On the project diagonal `K>=L`, the new scrub term is absorbed, so `K*=6/5+2 beta` and the fixed FLMV test still requires `beta<1/400`. Off diagonal the `gamma+lambda L` term may not be dropped. The child/accessor, source descriptor and parent join remain OPEN.

## Affine referee verdict

AFFINE-SMALLBIAS-DESCENT-GATE2 is certified under its pointwise all-input, source-independent randomized affine hypotheses. Fourier fiber comparison gives `B epsilon`; circuit counting and the explicit easy small-bias source yield error at least `1/2-o(1)`. It is only a restricted MCSP semantic no-go. Nonlinear/source-dependent preprocessing and arbitrary SAT runtime are outside its quantifiers.

## Controls

The producer and independent checker passed 472/474 checks on a one-model SAT formula and a matched zero-model UNSAT formula across six DELAY depths plus 15 far-index controls. Maximum replayed guest-step ratio was `2.822<4`; the wrapper increased the transparent work proxy in every run. Far-index sequential scrub ratios reached `4.382e12` in the finite controls while preserving the same source-computed label. Original-occurrence S/U inversions, pair SS/SU/US/UU matrices, endpoints and flip trails are retained as source-integrity controls.

Artifacts:

- `research/main/2026-10-30_2348_MAIN_ARC-UNKNOWN-HORIZON-SCRUB-REFEREE235.tex`
- `experiments/arc/2026-10-30_2348_unknown_horizon_scrub_referee235.py`
- `experiments/arc/2026-10-30_2348_unknown_horizon_scrub_referee235_check.py`
- `results/raw/arc/2026-10-30_2348_LSPV5_UNKNOWN_HORIZON_SCRUB_REFEREE235_raw.json`

## Next single arrow

Construct or falsify the main OPEN child/accessor theorem: an all-input exact ordinary-SAT child of length `N^(1/2+o(1))` with total reentrant accessor exponent `beta<1/400`, all discovery/failures/output within `N^(11/10+o(1))`, simultaneous space `N^(1/2+o(1))`, exact both-label join and hereditary closure. Every off-diagonal use must also carry the new `gamma+lambda L` scrub term.
