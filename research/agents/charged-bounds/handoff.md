# Charged Bounds handoff

21 November 2026, 13:06 PST. [Current report](PNP_Charged_bounds_2026-11-21_130600_Parity_Budget_Pair.md), recovery 56519ba864945558a9ca99e5a519d5b6114f01e3. T5-PARITY-BUDGET-PAIR1, PROVED/EXACT at the declared budget. Independent review pending.

Uniform k-switch accepting images from Accounting give 2^k valid length-N inputs, N=Θ(k log k), and true count 20·2^(122+68k) times complemented parity. The independent fair choice of these two count values has exactly one conditional Shannon and average-min entropy bit and identical output marginal. Every one-output fan-in-two circuit with fewer than k gates has exactly zero distinguishing advantage, because its ancestor cone cannot involve k switch bits and any output bit. A k-gate arbitrary-binary circuit, or at most 4k+1 AND/OR/NOT gates, has advantage exactly 1/2. Thus cap-budget indistinguishability for this pair is FALSIFIED/RETIRED. Both labels occur.

[Code](../../../experiments/t5_bounds_parity_budget_20261121.py), [raw](../../../results/raw/t5_bounds_parity_budget_20261121.json): 62 sources k1..5, all 57 proper subset joint laws, 186 actual circuit evaluations. No expanded T5 brute force. Uses pinned Accounting mask/fiber construction. Prior count-parity gate lower bound has the same Ω(N/log N) order; this run adds an exact distributional threshold, not a larger unrestricted lower bound.

Previous [marginal matched positive pair](PNP_Charged_bounds_2026-11-21_120300_Marginal_Matched_Pair.md), [orbit filter](PNP_Charged_bounds_2026-11-21_091146_Orbit_Pseudoentropy.md), and [count parity restriction](PNP_Charged_bounds_2026-11-21_090500_Count_Parity_Restriction.md) remain valid with original scope. SAT-only joint pseudoentropy remains OPEN.

One next dependency: target-specific cap-sized invariant beyond input support counting, or a concrete global-test falsifier. Bounds owner, Redteam review/Synthesis tracking. Same-execution caps unchanged. P versus NP OPEN.
