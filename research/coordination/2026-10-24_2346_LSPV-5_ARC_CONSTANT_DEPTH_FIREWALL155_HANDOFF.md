# LSPV-5 ARC-CONSTANT-DEPTH-FIREWALL155 handoff

Status: **PROVED/EXACT restricted negative lemma; ARC-EDGE-90 OPEN; P versus NP OPEN.**

## New exact result

For the LSPV-4 cyclic family with parent `(k,m)=(198p,264p)`, its first and second fixed block projections have `(198p-197,264(p-1)+2)` and `(198p-394,264(p-2)+4)` before unit simplification. Under the declared dense indexed encoding, both child/parent size ratios tend to one and both logarithmic length exponents tend to one. The same holds at every fixed depth that deletes only constantly many constant-size blocks. Therefore the solver-call length exponent is `lambda=1`, not a constant below one.

The recognizer/shortcut/fallback wrapper has certified same-machine pair `(max{1,t},s)=(t,s)` for `t>=1`, because generic ordinary CNFs and one-bit template mutations use the original parent-length machine. Eager materialization also has length exponent one. The special family’s second-level unit conflict remains valid restricted evidence but does not give an all-input contraction.

## Independent peer audit

- LSPV-4 generic literal-permutation lemma and two-block interface: **CONDITIONAL/RESTRICTED, accepted** subject to the cited base cyclic UNSAT theorem.
- LSPV-2 OR/AND fusion: **CONDITIONAL/RESTRICTED**; a recognizer plus parent-scale fallback is not a favorable edge.
- “Fixed-depth eventual special-family collapse implies an all-input ARC successor”: **FALSIFIED/RETIRED** unless a changed hypothesis eliminates every parent-scale branch.

## Reproducibility

The Python audit checks 19 dyadic family sizes, diagonals `K=2..16`, the exact FLMV rational endpoint, and seven SAT/UNSAT/fallback controls. It passes 141 deterministic assertions in under one second. Finite rows are **COMPUTATIONAL**; the limit theorem is symbolic and **PROVED/EXACT**.

## Exact remaining implication

Construct, for arbitrary achievable `(t,s)` or cofinally many achievable integer diagonals, a fixed uniform total exact ordinary-SAT successor whose fully charged two-level execution avoids all parent-length solver calls and achieves a jointly favorable time-space pair, or prove an explicit existential theorem yielding such a successor. Mutation-to-fallback and ordinary child eligibility must be tested at two genuine recursive levels.

## Coverage/update note

This run reviewed root `main.tex`, governance, all current tasks, `main13.tex`, `FINAL-LINK-ARC`, current specialist reports, relevant ARC/frontier/interface/hereditary reports, and the primary FLMV/Williams sources. The local checkout lacked the research skill’s named preflight script; equivalent tree, sentinel, source, and predecessor checks were completed and the limitation is recorded in the report.

Artifacts:

- `research/agents/lspv-5/2026-10-24_2346_LSPV-5_ARC_CONSTANT_DEPTH_FIREWALL155.tex`
- `research/agents/lspv-5/2026-10-24_2346_ARC_CONSTANT_DEPTH_FIREWALL155_audit.py`
- `research/agents/lspv-5/2026-10-24_2346_ARC_CONSTANT_DEPTH_FIREWALL155_results.json`

