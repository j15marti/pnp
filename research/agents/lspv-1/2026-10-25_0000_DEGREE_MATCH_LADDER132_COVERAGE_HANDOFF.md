# LSPV-1 DEGREE-MATCH-LADDER132: role-owned cumulative gap, source and rejection ledger

**Date:** 2026-10-25 00:00 Asia/Seoul. **P versus NP OPEN. ARC-EDGE-90 OPEN.** The shared five-agent target and pre-existing schedules are unchanged.

## Verified source objects and the exact improvement

**FILLED / PROVED/EXACT in restricted source language, independent peer review pending:** For positive EXACT-ONE ternary constraints with three distinct source variables per triple, let `k` count variables occurring at least three times. Source degree <=2 reduces to **maximum-weight graph matching**. The clause-graph has one node per exact-one constraint; each occurrence-degree2 variable is a node-node edge, occurrence-degree1 variable is a node-leaf edge; the matching must saturate every clause node. Complete exact solving and optional witness extraction have a uniform `2^k poly(N)` algorithm by branching on high-occurrence source variables and matching the residual. The parameter is source-defined before executing the solver and independent of runtime.

**KNOWN THEOREM transfer:** Moore--Robson (Discrete Comput. Geom. 2001, arXiv:math/0003039) prove planar cubic monotone 1-in-3-SAT NP-complete, so exact source degree 3 admits NP-complete instances. Edmonds (Canad. J. Math. 1965) gives polynomial general matching. The local 3-signature affine/binary identity and linear proper-CNF copies were already present in Role 3 EXACTONE-JOIN-CYCLE95 and Role 5 THREE-STATE-JOIN-FIREWALL130, not novel here. Degree-three source NP-completeness alone is not a lower bound on general decision machines.

**FILLED semantic encoder:** Each positive exact-one triple compiles to four proper ternaries encoding odd parity and two proper ternaries encoding NAND with a fresh auxiliary. Every source assignment extends iff exact-one. Total n'=n+m, m'=6m. Private auxiliary variables alter degree, so do not incorrectly transfer degree-source structural claims to ordinary post-compilation CNF.

**FALSIFIED/RETIRED candidate:** “local size-three feasible relation + nonlinear cyclic gluing forces hard decisions in every solver” because the degree-two class has arbitrary cycles yet polynomial matching. Likewise the same 16-vertex cubic clause degree/cycle rank graph can be SAT or UNSAT; these source parameters do not decide labels or impose exponential time.

**COMPUTATIONAL:** Full Python source `research/agents/lspv-1/2026-10-25_0000_DEGREE_MATCH_LADDER132_repro.py`, SHA-256 `fb7802a2e07613656de2c0c0886ec368ac997791f21979c72fd26a945c927439`. Finite seeded controls `202610240800`, NetworkX 3.6.1: 296 sources (265 SAT, 31 UNSAT), 134 degree<=2, 162 degree>=3, 1,618 assertions, no failures; independent DPLL and exhaustive validation, gadget eight-assignment check and a matched 16-clause-degree graph pair. Raw aggregate at `research/agents/lspv-1/2026-10-25_0000_DEGREE_MATCH_LADDER132_results.json`. Python counters are **not** FLMV indexed-machine bit steps/flips/peak space and finite checks don't prove asymptotic lower bounds.

## Exact ranking and canonical proof dependency map

1. **ARC/FLMV lead**: published matched random-access TM forbidden box with `t<241/200, s<11642479/23232400` = KNOWN THEOREM, subject to strict bounds; cofinal finite-hit logical implication = PROVED/EXACT conditional reasoning; existential all-input charged successor/finite route = **OPEN ARC-EDGE-90**. A code compiler, exponent discovery and invariant witnesses across implementations are not logically required for all possible existential proof routes, but each achieved pair needs one total fixed uniform all-input machine jointly meeting time and space bounds.
2. **UWI-1 / universal selector alternative**: corrected witness cost and abstract characterization, but no independent general all-decider lower bound, so no complete proof. Preserve as separate possible endpoint only after exact source-to-machine transport.
3. **CP/PCR, semantic rectangle, DNNF bridge**: genuine restricted proof-size and representation lower bounds, but universal decider-to-proof/repr transfer missing. No requirement that a one-bit decider output a DNNF or refutation.
4. **WRAPPER, clocks, hashes, provenance**: conditional causal/replay audits; no unconditional source-observable all-input static decision cost. Retired `2*cos(pi/7)` universal product criterion remains retired.

## Current peer concrete integrations

- Role 2 `OPTIMAL-WINDOW-CUT126`: exact O(L(W+1)) minimization of scoped source-dependent boundary-enumeration cost proxy; a restricted upper bound, not necessary all-solver calls.
- Role 3 `EXACTONE-JOIN-CYCLE95`: 3-element local supports and source-named equality gluing NP-complete; extends prior affine intersection, avoids false independent-child SAT inference.
- Role 4 `INTERVAL-PIN-COVER90`: exact special implication-chain splitting into ordinary power-short children and r+KQ>=q field acquisition; all-input fallback recovers original exponent.
- Role 5 `THREE-STATE-JOIN-FIREWALL130`: independent peer audit of Role3 semantics and arc-consistency SAT/UNSAT matched pair; NP-complete joins do not force arbitrary runtime.
- Role 1 older `CUBICCOVER75`: cited pre-existing cubic three-bridge no-perfect-matching construction, repurposed rather than rediscovered; earlier signed exact-(2,2) branch-and-matching parameter is distinct from this source-positive exact-one occurrence threshold.
- Role 1 `NONAFFINE-WINDOW131`: nonaffine chain four-state DP as an unrelated easy cyclic countercontrol.

## Adaptive-state/resource audit

Initial solver sees only original ordinary source bits, not SAT label. Charge E-language recognition, occurrence count, graph construction, any high-degree branch discovery, failures, max-weight matching work, alternative fallback, all source/work reads and writes including unchanged writes, addressing/selection, cached values, optional witness, representation conversion, output, peak simultaneously live bits, temporal complete-state flips and cumulative live-bit-time. One-bit exact SAT decision need not materialize a witness or entire relation. Restricted algorithm uses polynomial space per matching branch; no measured physical bit-machine trace. A full-language fallback restores correct outputs but not an all-input ARC favorable bound.

## Archive manifest with precise completeness qualification

**Live metadata survey:** GitHub tree SHA `256a9653f9625b59c7593506f378ce1cd96d5f28`, 5,131 entries (nontruncated), 230 LSPV-1, 189 LSPV-2, 215 LSPV-3, 255 LSPV-4, 65 LSPV-5, 260 research/main and eight tasks. **Prior historical baseline:** pinned `55a3fcc10f74419c9c3e1a577ed0f8ce83e2f640` 3,532 source/prose/config files retrieved, hash/keyword screened in earlier run, **not newly re-performed or fully mathematically read**.

**Full-body current reads:** root main.tex (specialist region and executive), main13.tex, AGENTS.md, CODEX.md, repo pnp-research SKILL.md, October 8 lead FINAL-LINK-ARC ancestor, current Roles 2/3/4/5 original reports named above, prior LSPV-1 NONAFFINE-WINDOW131 handoff, CUBICCOVER75 and PAIRPATH73, Role 2 BOUNDARY-EXCEPTIONS59, Role 3 SCOPED-BLOCK-REBUILDER92 handoff, flat hereditary marker test source, LSPV-5 MAIN WEIGHTED-TRANSCRIPT-COVER108, task4 HEC and task5 CRS. **Other task files** were inventoried but not all full-body read. **Drive:** original 2026-09-27 ARC 21,790-char document full-body via Google Drive; specific HEREDITARY-SCOPED10 search (one continuity record); broad SCOPED search 100 results returned but manual mathematical body screening selective and unrelated; earlier LOG/BOOL/SIL pagination not exhausted. **Web primary literature:** FLMV original JACM 2005 manuscript, Moore--Robson original arXiv:math/0003039, Edmonds original polynomial matching 1965, Freuder bounded-width CSP 1990. **GitHub queries:** 'perfect matching 1-in-3', 'cubic planar 1-in-3', 'Moore Robson', 'exactly twice occurrences exact one', 'occurrence-2 matching', 'degree threshold exact-one', 'HEREDITARY-SCOPED10', 'SAME_REALIZATION'. Absence claims are limited to selected search results, not entire project.

**Current unread queue:** original complete HEREDITARY-SCOPED10 executable (not recovered); exact past versions main2--main12, LSPV corpus manual mathematical body review, historical LOG/PROVED_EXACT/BOOL/SIL Drive folders and pagination, and old code migrations. Do not infer lack of a result from inaccessible archived bytes or transient local paths.

## Three falsifiable links and precise receiving obligation

**M1 FILLED/RESTRICTED:** source occurrence <=2 gives exact polynomial matching despite cycles, proof and public implementation.
**M2 FILLED/KNOWN TRANSFER:** source occurrence exactly3 positive monotone one-in-three gives NP-complete via Moore--Robson, but no unrestricted lower bound.
**M3 OPEN / REJECTED UNJUSTIFIED INFERENCE:** combining degree2 upper and degree3 hardness does **not** produce a cofinal favorable successor for arbitrary ordinary SAT. Source recognition can fail, and an all-input fallback retains the original exponent. The restricted FPT solver cannot establish any jointly achieved pair below FLMV for all source formulas. Any attempt claiming such must exhibit a correctly paid all-input construction, including ordinary child encoding, gluing, source access, failed strategies, peak space and uniformity.

## Next exact source and action

**ARC-EDGE-90** remains the only load-bearing gap. Next inspect the full original HEREDITARY-SCOPED10 if recovered; otherwise test the *newly reconstructed* Role3 SCOPED-BLOCK-REBUILDER92 against Moore--Robson cubic degree-three sources, Role1 nonlinear AND windows, Role4 high-width grids, and Role3 exact-one arc-consistency matched pair. Demand two recursive levels with ordinary serialized children, source-named compatibility, paid failed recognition/fallback and matched-machine bit resources. Treat restricted and full-domain results separately. P versus NP OPEN.

Report: `research/agents/lspv-1/2026-10-25_0000_LSPV-1_DEGREE_MATCH_LADDER132.tex`.
