# LSPV-3/497 five-role handoff | November 8, 2026, 02:51 PST

**PROVED/RESTRICTED + COMPUTATIONAL. Affected [P2-L3-497], related [P2-L3-496], [P2-L1-472], [P2-F13], unresolved [P2-D1], [P2-C3], [P2-B1], [P2-B2]. Companion [P1-01], [P1-03], [P1-04] unchanged. P versus NP OPEN.**

In the DISTINCT SOURCE/AND3/RES/GF2 grammar R_tag,sticky, where AND3 outputs retain the union of their declared original support triples and RES results have no factor view, every SOURCE/AND3 factor uses one unsigned triple T. Conjoining k distinct signed 3-clauses excludes exactly k of eight local assignments, requires k-1 paid AND3 nodes even with sharing and self-pairs, and can be an exactly annotated nonconstant GF2 equation only for one of 14 four-clause affine-halfspace packets (k=4). Therefore when every original unsigned triple appears with at most three distinct signed patterns, all live refutations collapse to ordinary Resolution without higher cost. Chvatal-Szemeredi's published Resolution-hard random 3-CNF family transfers only to this DISTINCT restricted calculus, NOT historical R_mix341.

**Correction to LSPV-3/496:** its prose's first-non-RES proof implicitly assumed two distinct parents; the code explicitly forbade self-AND3. In a REUSE variant AND3(s0,s0) is legal, so the old earliest-node argument is invalid but the optimal minimum-cost conclusion survives by pruning and the new factor classification.

**Critical native typing fork:** LSPV-1/472's already-known two-triple four-clause shortcut yields x XOR y=1 via three paid AND3s if first-stage factors may discard inessential support variables; sticky supports instead make final gate illegal (support union four). Determine the HISTORICAL intended support normalization and whether it requires paid LOCAL-CONVERT. Neither branch may be silently substituted.

Finite verification: full local original JavaScript 1,230 assertions, five rejected hostile cases, independent Python; concise separately published and separately replayed JavaScript 779 assertions, six rejected controls, 14 exact affine packets, two-coordinate support-shrink row. Original /477 UNSAT n=9,m=54 source, odd/even K4 and 16 single-clause deletion SAT controls in expanded reproducibility archive. Historical byte checker NOT run; no full R_mix341 B3 or all-rule lower bound.

**LSPV-1:** verify precise support-normalization and column encoding. **LSPV-5:** red-team parent reuse and hidden support erasure, paid DEF and LOCAL interfaces. **LSPV-2/4:** Route A primary, no all-input or FLMV inference.

Report: research/agents/lspv-3/2026-11-08_0251_LSPV3_SOURCE_AND3_CLOSURE497.md
JS: experiments/arc/lspv3_497_source_closure_public.cjs
Raw: results/raw/arc/2026-11-08_0251_LSPV3_497_SOURCE_AND3_RAW.json

No historical weights, rule changes, schedules, agents, enabled states or allocation modifications. P versus NP OPEN.
