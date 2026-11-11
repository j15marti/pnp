# P vs NP world ledger (CLAUDE WORLD-LEDGER-0001)

Added 2026-10-28 at the user's request. **Reference resource only**: it changes no task schedules, agent count, role ownership or scientific allocation, and it is not a proof of anything. **P versus NP remains OPEN.**

## What it is

A table of statements S about complexity, each marked `True`, `False` or `Open` in the five Impagliazzo worlds:

| World | Definition used |
|---|---|
| Algorithmica | P = NP |
| Heuristica | P ≠ NP, but NP is easy on average |
| Pessiland | NP is hard on average, but one-way functions do not exist |
| Minicrypt | One-way functions exist, but public-key encryption does not |
| Cryptomania | Public-key encryption exists |

The pattern of the five values sorts S into a category automatically:

| Category | Meaning | Use |
|---|---|---|
| Theorem (win-win) | True in every world | Unconditional (if the world entries are right) |
| Refuted in every world | False in every world | Excluded |
| Equivalent to P = NP / P ≠ NP | Decided exactly by P vs NP | A reformulation, not progress |
| Half-win (true if P = NP / P ≠ NP) | Forced in one camp, open in the other | Proving S in the open camp proves S outright; refuting S settles P vs NP |
| Implies P = NP / P ≠ NP (open) | Proving S settles P vs NP | Same difficulty as the target, at least |
| World separator | Mixed True/False values that split the worlds | Separates worlds, does not decide P vs NP |

Exact rules (all twelve cases) are in the report's category table and in `classify()` in `build_ledger.py`.

A **Consistency** column flags `CONFLICT` when a world contradicts a known theorem. A genuine conflict would eliminate that world; in practice it almost always means an entry is wrong. With a world marked False on a Theorem row, the flag fires (tested).

Each world cell is a CONDITIONAL claim ("if world W, then S"), justified in the Source column. Technique tags (relativizes / naturalizes / algebrizes) marked `Unverified` have not been checked against the primary paper.

## Files

| File | Purpose |
|---|---|
| `build_ledger.py` | Source of truth. Seeded rows live in its `rows` list. Regenerates both outputs. |
| `P_vs_NP_World_Ledger.xlsx` | Spreadsheet with live Category / Consistency formulas, dropdowns, Read me, Worlds and Summary sheets. |
| `world_ledger.csv` | Plain-text copy for agents; Category and Consistency computed in Python with the same rules (cross-checked: 40/40 rows match the recalculated spreadsheet as of 2026-10-28; 49 rows as of 2026-11-11). |
| `../2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` | Report: category semantics, proofs of the results the ledger cites (rows L20–L24, L28), nested-SAT classification (L09–L12, L27), and relevance to the ARC/FLMV spine (L13). |

## How to add a statement

1. Add a tuple to `rows` in `build_ledger.py`: ID, statement, the five world values, known status (`Theorem` / `Refuted` / `Open`), three technique tags, source, notes.
2. Run `python research/agents/claude/world-ledger/build_ledger.py` (needs `openpyxl`).
3. Check the new row's Category and Consistency in `world_ledger.csv`. Investigate any `CONFLICT` before committing.

Status labels in the repo's vocabulary: `Theorem` corresponds to KNOWN THEOREM or PROVED/EXACT, `Open` to OPEN, `Refuted` to FALSIFIED/RETIRED.

## Rows most relevant to current work

- **L13** — SAT time-space bounds: 2cos(π/7) is the proven ceiling of alternation-trading proofs (Buss–Williams 2015). Relevant to any FLMV-box route built from the standard speedup/slowdown rules.
- **L06, L03–L05** — half-wins on the P = NP side; the best targets are those whose open side would need a non-relativizing step.
- **L28** — P = NP iff every satisfiable formula A has a solution x with Kt(x | A) = O(log n).
- **L29–L33** — from the audit of the direct-product route to the UWI common-input statement (`research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`). L32 (portfolio collapse) shows that route is dominated; **L33 (T-PORT)** is the proposed next target linking UWI to the ARC/FLMV time–space spine.
- **L34–L36** — from `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex`. **L34**: alternation trading with the portfolio rules provably cannot beat linear time at the UWI portfolio size (d = 1). **L35**: every sublinear portfolio (d < 1) has a nontrivial bound. **L36**: whether Skolemization changes L34 is open (computationally, it does not).
- **L37** — from `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`: the provable exponent is 1 + Θ(1 − d), between 1 + 0.58(1 − d) and 1 + (1 − d) as the portfolio size approaches N.
- **L38–L40** — from `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`: one-tape and sequential-access crossing-sequence bounds for SAT, their nondeterministic and portfolio forms, and the quadratic wall.
- **L41–L49** — from `research/agents/claude/2026-11-11_0955_CLAUDE_DERIVBRIDGE-0001.tex`: the worst-case minimum-derivation program (W̄_R, bridges B1/B2/B3). B3 for Resolution is equivalent to P ≠ NP; B3(EF), which matches B3(R_mix341) under the corpus simulation, is a half-win; B2(Res) is ETH-type; Pich–Santhanam is a conditional B3(EF).
