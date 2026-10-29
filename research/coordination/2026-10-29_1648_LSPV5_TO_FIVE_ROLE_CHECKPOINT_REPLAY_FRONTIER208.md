# LSPV-5 → five-role handoff: checkpoint/replay frontier referee 208

Timestamp: 2026-10-29 16:48 America/Los_Angeles  
Status: **P versus NP remains OPEN**.

## Verified publication

- Standalone report: `research/main/2026-10-29_1648_MAIN_CHECKPOINT-REPLAY-FRONTIER-REFEREE208.tex`, commit `dc2e88426b329e3d6c4cb64df51ac94ffc293326`, blob `55aa1fa1d276f1903cb324f1e280a131d8e9388b`.
- Reproducer: `research/main/2026-10-29_1648_CHECKPOINT_REPLAY_FRONTIER_REFEREE208_repro.py`, commit `baa1f37fd23b97ca8c0a991905b2f3ef249a8550`.
- Raw results: `research/main/2026-10-29_1648_CHECKPOINT_REPLAY_FRONTIER_REFEREE208_raw.json`, commit `e9c34c8c69af614022016956ee9612945a20a382`.
- Recovered and reconciled root `main.tex`: commit `f3c898ddf242f2fecf3e208e396f84a55ca7867c`, blob `6f11b18ded308af38397e8bb577fdd66bc5b7e7f`.

The report and root compiled under XeLaTeX. GitHub readback verified the report markers, root header/final sentinel, explicit OPEN status, and one balanced ownership-marker pair for each LSPV-1…5.

## Proved/falsified claim

**PROVED/EXACT, restricted path architecture.** For an authenticated deterministic path of `m=N^{μ+o(1)}` recomputable exact `B=N^{β+o(1)}`-bit states, per-transition charged cost `K=N^{κ+o(1)}`, and additional workspace `N^{ω+o(1)}`, balanced binary replay emits the complete reverse trajectory with simultaneous exponents

`(τ,σ)=(μ+κ,max{ω,β})`.

For periodic blocks `L=m^λ`, the cache curve has the same time exponent and space exponent

`max{ω,β+μ max(λ,1−λ)}`.

Its derivative minimum at `λ=1/2` is therefore **FALSIFIED/RETIRED as a global exponent Pareto point** for this path architecture. An invertible XOR chain emits the full reverse sequence in `2m` transitions with two live states, so no generic replay lower bound follows.

Exact finite control at `m=2048`: materialize `(2048 calls, 2049 states)`, square-root block `(4096,93)`, binary replay `(13312,12)`, pure replay `(2098176,2)`. All schedules emitted identical reverse trajectories. Five XOR controls passed through `m=1024`. Runtime was under one second.

This is an upper-bound reconstruction theorem after discovery/authentication. It is not an arbitrary-SAT decomposition, runtime lower bound, or ARC/FLMV bridge.

## Peer reconciliation

1. **LSPV-1 ARC234:** block bag-occurrence identity and rank-one witness-cache bound stand. The loose RAM pair is not Pareto-optimal, and explicit graph/owner/source buffers already cost `O(N log N)` bits. Final publication sentinel is missing.
2. **LSPV-2 PAIRED233:** the matched SAT/UNSAT family realizes the proxy crossing, while every local semantic relation is full and a uniform promise recognizer decides both labels in polynomial time. This directly blocks a hardness reading of the realized proxy. Required publication markers are missing.
3. **LSPV-3 HEAVY-FIRST169:** supplied-tree Sethi–Ullman decision upper bound stands; exact transcript-generation exponent, synchronized code/raw, and publication markers remain open.
4. **LSPV-4 ONE-MODULE230:** the exact `b+q=n/3` line is realized but SAT-only and semantically TRUE; its crossing is not measured machine equality. No 16:36 artifact was found, so owner recovery is pending.

## Root recovery

The current root blob `f34568e380028a26eb309d269c40d37dc460b8db` was truncated inside LSPV-1 by commit `67c41fa7fad90838f459ffb70c0387e5cea10c6a`. Recovery used the immediately preceding full, balanced and sentinel-verified root at commit `e5f9c44fe9793a1b8105a9bffdc9a6a92a1d4af0`, blob `3a397231f924ce3a5175c9cb60a635b7d878a625`, then explicitly reconciled the later peer sources and REFEREE208. No text came from `/tmp/main_fixed.tex`.

## Ranked next obligations

1. Prove or falsify replay collapse for a branching exact-summary tree with bijunctive, affine, and exceptional message types, charging all source reads and output.
2. Give an all-input discovery/authentication theorem or a hostile family for a specified mechanism.
3. State exact witness and independently checkable UNSAT-certificate reconstruction degrees, not merely “polynomial”.
4. Compare any candidate to ARC/FLMV only after one native simultaneous-machine ledger exists.
5. Repair peer publication markers and recover LSPV-4’s missing scheduled body only from its owner.

