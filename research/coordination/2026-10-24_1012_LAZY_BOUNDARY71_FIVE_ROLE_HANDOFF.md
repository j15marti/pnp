# LAZY-BOUNDARY71: role-2 source-coherent adaptive handoff

**Proof status:** P versus NP remains OPEN. Source-safe lazy-join theorem PROVED/EXACT in the declared decomposition model, independent review pending; numeric improvements COMPUTATIONAL. No schedules or task count changed.

**Fresh verified report:** `research/agents/lspv-2/2026-10-24_1012_LSPV-2_LAZY_BOUNDARY71.tex` (blob `73f175ab8e7872e6e17147cb50f3e8b743927e94`). Executable minimal reproducer and raw summary are in the same existing role directory; Python standard-library full audit, original source and independent list-based checker are packaged as the user-visible `LSPV2_LAZY_BOUNDARY71_2026-10-24.zip`. Local paths are not assumed peer-shared.

## Exact new construction
For certified clause subformula H=G(Y) AND_j H_j(Y_j,U_j), disjoint private U_j and shared original sources Y, ask one local restriction per master candidate. If H_j under alpha|Y_j is UNSAT, record checked local proof and add no-good OR_{y in Y_j}(y != alpha(y)). Every no-good is source-entailed, so an UNSAT master implies UNSAT parent F even when H is only a subformula. If the master has compatible positive witnesses, accept SAT only after replay against **all** original clauses F; otherwise use exact fallback. Source-closed positive-cache keys (block j, assignment to Y_j) plus permanent negative blocking bound distinct local solver calls by sum_j 2^|Y_j|. Root boundary row scanning may still cost 2^|Y| per refinement; no all-decider lower bound follows.

## Two-label strict signed exact-(2,2) control
Benchmark U198/264 versus its two-sign SAT neighbor V: same unsigned supports, source quotas, 15,870 encoded bits and connected incidence. Both defeat initial complementary-pair, tautological-pivot and clause-to-source matching certificate. Use prior DOECKER-CORE-CERT61 six-module layout. Eager U projection: 36 calls, 1,038 nodes, 86,856 clause scans. New cached lazy U: 16 calls, 688 nodes, 62,878 scans. Uncached: 21/764/67,708. Support-first: 15/688/63,190 (fewer calls but more scans). Exactly six certified length-2/3 root clauses refute U; 537 independently checked proof nodes, no enumeration of 30 positive boundary rows. Same total policy probes entire source for 128 nodes: V returns original-source SAT witness after 104 nodes; U switches after the failed probe and proves UNSAT with 128+688+3=819 search nodes plus fully paid other work. A 10,000-node direct-U baseline returns UNKNOWN, not UNSAT.

Generic complete-decomposition test: 140 random six-source instances (58 SAT, 82 UNSAT) independently brute-forced; 145 negative proof trees independently replayed. A missing cross-module clause adversary forces UNKNOWN abstraction, never unjustified SAT. The deterministic suite recorded 335 checks and 0 failures, seed 202610240111.

## Peer-specific next objectives
**Role 1 universal cost:** attempt any all-decider lower-bound potential only after allowing direct decision and this sound compression; a finite policy menu is not all-algorithm coverage.
**Role 2 backward algorithms:** substitute paid affine, SCC and cubic-cover local oracles; use learned/no-good trajectories, try proof-guided assumption-core shrinking on noncanonical interfaces.
**Role 3 exact-(2,2) transport:** seek connected opposite-label controls without the unchanged fixed 254-clause negative subformula; charge discovery of the separator and omitted-clause safety.
**Role 4 independent red-team:** rerun the source replay, no-good entailment, positive-cache soundness and cache-space ledger; vary block order/heuristics, measure clause scans and peak memory as well as search nodes.
**Role 5 synthesis:** reconcile root status, maintain OPEN universal extraction arrow. The CEGAR and DPLL(T) ideas, MAIN64 exact join, and DOECKER-CORE-CERT61 six-module core are prior art. The new item is a fully charged implementation and verified source-specific saving.

**No task created, reactivated, disabled or rescheduled.**
