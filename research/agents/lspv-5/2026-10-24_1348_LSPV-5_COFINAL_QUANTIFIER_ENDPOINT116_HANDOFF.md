# LSPV-5 handoff — COFINAL-QUANTIFIER-ENDPOINT116

Timestamp: 2026-10-24 13:48 KST. P versus NP remains **OPEN**.

## Exact result

Let `E` be the simultaneous time/space exponent pairs achieved by one fixed uniform total all-input exact SAT decider in the matched FLMV random-access model. Let

`B_FLMV = {(t,s): exists c > max(1,t) with s < beta(c)}`,

where `beta(c)=((c+2)/c^2-c)/2`. Primary FLMV implies `E ∩ B_FLMV = ∅`; the region is coordinatewise downward closed.

For any **fixed unbounded** `U ⊆ N`, define the conditional route assertion

`H_U: for every K in U, if (K,K) in E, then a finite sequence of points of E starts at (K,K) and ends in B_FLMV`.

**PROVED/EXACT:** `H_U ⇔ E=∅ ⇔ P≠NP`. If `E` is empty, `H_U` is vacuous. If `E` is nonempty, upward closure puts every sufficiently large diagonal in `E`; unbounded `U` contains one, and its route would end in `E ∩ B_FLMV`.

This independently verifies Role 3’s logical-strength theorem. The new sharpening is the quantifier split:

- A fixed-unbounded-set **conditional** `H_U` is separation-equivalent.
- The literal claim “there exists an unbounded `U` of already-achievable diagonals and each has a route” is false both when `E` is empty (no such `U`) and when it is nonempty (endpoint disjointness forbids every route). Retire that literal wording.

Existential/cofinal routes are constructionally more modular than a universal source-code compiler, but the abstract assertion is not logically weaker than P≠NP.

## Endpoint correction

- **KNOWN THEOREM:** FLMV Cor. 5.8 plus Thm. 3.1/Cor. 3.2 yields the curved forbidden region above with strict slack.
- At `c=241/200`, `beta(c)=11642479/23232400 > 1/2`; the standard box remains valid.
- The curve is larger: `(1.21,.45)` is forbidden using `c=1.22`; `(1.3,.3)` using `c=1.31`.
- **FALSIFIED/RETIRED:** `t+s < 2 cos(pi/7)` as a universal random-access SAT endpoint. The Williams primary statement is for `n^{o(1)}` space, not arbitrary polynomial-space exponent.

## Peer audit

- Role 1 ARCARCHIVECURVE90 and Role 2 FLMV-CURVE-FRONTIER115: endpoint repair independently verified.
- Role 3 ARCHIVE-ARC-SEMANTIC82: separation-equivalence independently rederived.
- Role 3 BOUNDARY-TREEWIDTH81: restricted constructive upper bound only.
- Role 4 BALANCE-HEADER-ORACLE79: exact restricted metadata-field sensitivity with both labels; source-aware/small-cache escape prevents all-input transport.

No proposed FILLED item supplies an all-input same-realization achievable-pair edge. Constant-false UNSAT representations, polynomial decision self-reduction for SAT witnesses, direct source rereads, decide-first compression, representation switching, affine/Horn/SCC solvers, caches and restricted-family fallback remain valid bypasses.

## Adaptive resource ledger

Each route point must be one uniform all-input machine with joint time and peak work-space bounds. An edge may use a different finite rule, but a concrete construction must charge recognition, parameter discovery, policy evaluation, switching, failed candidates, source access, ordinary child headers/bits, transformations, gluing, reconstruction, replay, caches, buffers and live ancestors. Exponents and route index may be analysis-only. No label oracle; SAT and UNSAT may use different success evidence.

## Coverage increment

Full current texts read: root `main.tex` blob `da6cc8a...`, `main13.tex` blob `87dbaad5...`, MAIN WEIGHTED-TRANSCRIPT-COVER108, newest substantive Role 1–4 reports named above, pinned FINAL-LINK-ARC, Drive ARC origin, task files, primary FLMV and Williams statements. The supplied 3,532-file pinned crawl and count of thirteen stale cosine scripts are inherited, not re-certified. Drive pagination and earlier-chat archives remain unexhausted.

## Exact remaining implication

**OPEN:** prove one nontrivial all-input, uniform, same-realization joint time/space successor edge for arbitrary adaptive exact SAT, or directly prove `H_U` with every finite edge fully charged. This is separation-strength.

Next inspect the complete original HEREDITARY-SCOPED10 proof body, especially its arbitrary-input fallback and source-address contract, then PCLOSE1-R1, MULTICHANNEL1, KDAG2, EXTENSIONAL-COLLAPSE1 and STATIC-DYNAMIC-TRANSPORT-DICHOTOMY1.

Artifacts: standalone LaTeX report, exact-rational Python auditor, raw JSON. All 11 executable assertions pass; finite checks prove no asymptotic lower bound.
