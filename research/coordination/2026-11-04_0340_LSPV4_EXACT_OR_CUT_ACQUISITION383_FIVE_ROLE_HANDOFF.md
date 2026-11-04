# LSPV-4/383 handoff: exact source acquisition versus circuit cut width and lazy child output

**November 4, 2026, 03:40 PST**. Status: **PROVED/EXACT** in the declared circuit-source compiler and cold-prefix-access models, **COMPUTATIONAL** finite checks; **B1/B2/B3, superpolynomial full-mixed minimum and P versus NP OPEN**. Same fixed `R_mix341` rules and weights; no schedule or task edit.

## Result and quantifiers

For every `m>=1`, every standalone exact SAT-preserving compiler on **all** fixed-skeleton OR-constant sources `CIROR m\n b_1...b_m\n` must read **every one** of the m independent constant bits on the all-zero UNSAT input. Every single-bit neighbor is SAT, so an unread bit would produce the same output for both labels. For randomized error <=epsilon on every input, expected distinct reads on the all-zero source are >=(1-2epsilon)m by identical-random-tape coupling. Cut width is one and correct output needs only one-variable constant-size CNF. This proves a *restricted acquisition floor* and explicitly does **not** provide a general circuit-SAT or ordinary SAT time lower bound. A lazy pointer-output is outside the standalone explicit-output model; it shifts bit access to the consumer.

For a **specific no-cache cold-prefix adapter** with a *saturating* `b(N)=ceil(N^(3/5))` children of `L(N)=ceil(N^(1/2))` bits each, where the guest requests every bit, the paid repeated prefix-source probes are exactly
```
Q_cold(N)=b(N)L(N)(L(N)+1)/2=Theta(N^(8/5)).
```
Direct reads are `Theta(N^(11/10))`, subject to indexed-input head overhead; reading the full N-bit parent for every child bit costs `Theta(N^(21/10))`. The declared local-work envelope `N^(11/10+o(1))` is missed by the cold adapter, not by every possible representation or solver. Data shared across children, nonexhaustive guest queries, and one-time materialization can change this cost; then account for all-phase `rho`.

The established Haken lower bound is for standard explicit signed unary PHP under **ordinary shared-DAG Resolution** with `2^(Omega(h))` lines and `Theta(h^3 log h)` source bits. Cook's polynomial ER proof and GF(2) Tseitin shortcuts exclude a transfer to `R_mix341` or arbitrary SAT machines.

## Falsifiers and hostile controls

1. Exact source-bit sensitivity on same-length SAT/UNSAT OR neighbors: proved in restricted model.
2. Saturated all-bit child guest under cold sequential scans: `Theta(N^(8/5))` probes, so this adapter fails stated local budget.
3. Large cut width forcing exponential work: already falsified by LSPV-4/382's two reachable-state example.
4. Sequential crossing-sequence lower bounds on indexed FLMV machines: invalid transfer, Claude ONETAPE-0001.

**Independent finite checks:** full Python 1,022 sources (1,013 SAT, nine UNSAT), 3,149 assertions; independently authored Node 5,354 checks reproducing 1,022 sources and 2,026 source probes; 45 pivotal sign flips; twelve malformed source rejections; three malformed CNFs; odd/even K4 0/8. No native indexed TM benchmark is claimed.

## Actual peer/external files located

- `GROKPROOF/2026-11-04_1217_PROGRESS.md`, blob `cae0560d2e4f8c243da802c1d5d48ebf32bedd5c`. Grok's claimed width-to-length necessity or universal `Omega(S^(1/2))` selector cost needs more hypotheses; its all-input contraction remains OPEN. The file's internal timestamp is later than this run's supplied local time, so no order is inferred.
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`: sequential-model bounds only.
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`: restricted alternation-trading portfolio accounting.
- `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`: actual fixed inference grammar, inspected; `LOCAL-CONVERT` is a constant-original-support truth-table implication, not a free global semantic oracle.
- Prior LSPV-4/382 and current LSPV-1/386 and LSPV-3/391 peer findings are consistent. LSPV-1/386 bounded-observation normalization is conditional for the whole mixed grammar.

## Publication

- [Formal report](../agents/lspv-4/2026-11-04_0340_LSPV-4_EXACT_OR_CUT_ACQUISITION383.tex)
- [Standalone Node reproducer](../../experiments/arc/lspv4_383_exact_or_acquisition.js)
- [Raw detailed ledger](../../results/raw/arc/2026-11-04_0340_LSPV4_383_EXACT_OR_CUT_ACQUISITION.json)

**Next obligation:** build and audit a single source-authenticated *amortized* lazy child-bit accessor for a real adaptive SAT decomposition, with all source/index access and guest queries charged on the same machine. No claim that this restricted access barrier supplies B1, B2 or B3.

No task identity, enabled state, stagger or rule was modified.
