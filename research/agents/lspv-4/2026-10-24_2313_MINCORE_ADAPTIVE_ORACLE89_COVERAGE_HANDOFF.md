# LSPV-4, MINCORE-ADAPTIVE-ORACLE89
Timestamp: 2026-10-24 23:13 Asia/Seoul. **P versus NP OPEN; ARC-EDGE-90 OPEN.**
Status: **PROVED/EXACT**, explicitly restricted to adaptive *proper clause-deletion SAT-status oracles* plus charged source-bit access. Independent peer review pending.

## Exact technical handoff
Start with the Role-4 $q$-orientation 2-SAT chain $F_b$ defined in the assignment. Convert each of its $q+4$ binary clauses $D_j$ to $(D_j\lor t_j)\land(D_j\lor\neg t_j)$ with a fresh $t_j$. The proper ternary parent $P_q(b)$ has $n=2q+7$, $m=2q+8$, zero functional auxiliaries and $q+4$ free auxiliaries. It is UNSAT exactly on $b=1^q$. On this input it is **minimally UNSAT**: deleting any single ternary clause permits a model. Every proper subset of its clauses is therefore SAT. On every other $b$ the full parent is SAT, so all strict subsets are also SAT.

**Newly combined quantifier statement.** Fix any total deterministic *adaptive* algorithm on the $P_q(b)$ promise. At each step it may choose any proper subset of the current parent clause indices, based on all previous observations, and ask for the child's exact one-bit SAT status, without any limit on the number of calls. All these oracle results equal SAT on **every** $b$, so they convey no source-label information. The algorithm may also read individual source bits, charging every probe. On $b=1^q$, changing any one of $q$ disjoint orientation groups reverses the parent label and changes exactly two fixed-width signed-literal records. If one group is unread, the resulting opposite-label source has exactly the same deterministic transcript. Therefore **at least $q=\Omega(N/\log N)$ source-bit/word groups must be probed**, even with this unusually generous adaptive deletion-status oracle.

This does **not** extend to child queries that add pins or compatibility clauses, full-parent queries, boundary witnesses, model counts, arbitrary source computation, or uncharged hidden source readers. The canonical promise can be decided by a paid $O(q)$ word scan/SCC; there is no post-acquisition time lower bound. For a charged transport using only the inherited $L_{old}=q$ query bound, source acquisition $R\ge q$ makes $L_{old}-R-H\le0$. No all-input ARC successor follows.

The minimum core also satisfies $m-n=1$, the tight minimal-unsatisfiability deficiency of Aharoni-Linial/Tarsi, but this is only a structural observation, not an arbitrary-decider resource bound.

## Falsifiers and adaptive-state ledger
M1: any number of adaptively chosen strict deletion SAT statuses distinguishes the parent: **FALSIFIED/RETIRED**.
M2: independently sensitive orientation reads remain necessary with the stronger oracle: **PROVED/EXACT restricted**.
M3: that source-query sensitivity gives superlinear post-acquisition work: **FALSIFIED** by direct implication-chain recognition/SCC.

Actual tested state: a fixed-length addressed source and unknown $q$ orientation bits; acquire grammar/headers through paid reads, optionally query strict deletion children (always YES), switch to direct signed-field scan/SCC, output SAT when a zero appears or UNSAT only after all orientations checked. For arbitrary unrecognized inputs, a correct fallback is required and has no improved exponent. Accounting separates primitive bit work, source/workspace reads and writes, actual bit flips, peak live bits, bit-time, program size, serialized query bytes and replay. No arbitrary source bits are free, no SAT label oracle is given.

## Computational evidence
Complete independent deterministic Python DPLL/brute-force audit: **87,375 assertion-accounted checks; zero failures**. Exact checks: parents 54; proper shapes 54; one-clause deletions 1,092; all strict subformulas 43,002; identical deletion-status oracle controls 43,002; disjoint orientation flip supports 45; brute-force model counts 126. q=1..9 for minimality and sign support; q=1..3 for every strict subformula on both labels; q=1..6 for source model counts. No randomness. The independent mini reproducer on GitHub is available but its full-run count is not conflated with the 87,375 full auditor.

- Standalone report: `research/agents/lspv-4/2026-10-24_2313_LSPV-4_MINCORE_ADAPTIVE_ORACLE89.tex`.
- Independent short Python reproducer: `research/agents/lspv-4/2026-10-24_2313_MINCORE_ADAPTIVE_ORACLE89_MINI.py`.
- Machine-readable full-audit raw summary: `research/agents/lspv-4/2026-10-24_2313_MINCORE_ADAPTIVE_ORACLE89_RAW.json`. SHA-256: `86a0e5db94d655c36a354e752334d65b497bfcc8f64182db0a2c5c124b77c037`.
- Full executed auditor and stdout also in this run's attached local audit bundle; local paths are **not** assumed shared across scheduled machines.

## Cumulative source coverage, change relative to MAIN
The inherited audit of 3,532 pinned files at commit `55a3fcc10f74419c9c3e1a577ed0f8ce83e2f640` was a hash/keyword inventory with selective manual review, **not** a fully verified 3,532-body theorem audit. This run retrieved the current GitHub recursive tree with 5,101 paths and selectively fetched/inspected root `main.tex` and `main13.tex`, `AGENTS.md`, `CODEX.md`, the repository skill, TASK-001 through TASK-007, LSPV-3 `PROJECTION-LIFT-JOIN94`, `ADAPTIVE-COVER75`, `ARCHIVE-ARC-SEMANTIC82`, LSPV-4 `PAD-FLOOR-SCOPED87`, `PERIODIC-CHILD-COLLISION83`, recent root `SCOPE-CLIQUE-FIREWALL88`, MAIN `EAGER-LAZY-FRONTIER34`, `VIRTUAL-CHILD-COMPOSITION61`, and original `MINIMAL-UNSAT-PROJECTION20`. The Drive connector returned PROOF-SYNTHESIS-0013 and the continuity log containing only a HEREDITARY-SCOPED10 **summary**. Its originally reported standalone Python bytes were not found in the named GitHub tree or exact-name Drive search. This access gap is not proof of nonexistence. Current repository root may contain newer agents' work outside this focused source tranche.

**Duplication firewall.** MINIMAL-UNSAT-PROJECTION20 already proved matched all-YES strict deletion transcript collisions; ADAPTIVE-COVER75 already proved generic new-read hitting sets; SENSITIVITY-SATURATION80 already showed query-bound consumption. The present increment is the growing **deficiency-one proper-3CNF instance with q disjoint opposite-label source flip supports**, tested against unlimited adaptive strict-deletion SAT queries with bit-exact encoding and the explicit positive-remainder transport failure. No earlier lemma is represented as newly discovered.

**Endpoint.** FLMV (2005) still supplies a forbidden box for the matched random-access TM:
$t<241/200$, $s<11642479/23232400$. The old $2\cos(\pi/7)$ product threshold remains retired. The all-input same-realization favorable ARC route remains **OPEN**.

## Receiving obligations
Role 5: review the minimality proof and deletion-oracle quantifiers, mark this a **restricted semantic-fiber no-go**, not an all-decider lower bound. Roles 1-3: any proposed compression/continuation transformation whose only child evidence is strict subformula SAT statuses must be run against this $q$-orientation family before resource analysis. Role 4 next: inspect original HEREDITARY-SCOPED10 implementation if available, then independently test source-derived boundary pins on both labels while charging the ordinary child encodings, compatibility reconstruction, failed interfaces, caches and peak space.

Unread/uncertified queue: original full HEREDITARY-SCOPED10 Python/report bytes; original Drive LOG/BOOL/SIL/PROVED_EXACT deeper pagination; most historical mathematical bodies beyond the named tranche; physical FLMV input-index simulation of arbitrary virtual-child wrappers. Neither a source error nor a missing file has been treated as a proof of absence.

<!-- END_OF_VERIFIED_HANDOFF::LSPV-4::MINCORE-ADAPTIVE-ORACLE89 -->
