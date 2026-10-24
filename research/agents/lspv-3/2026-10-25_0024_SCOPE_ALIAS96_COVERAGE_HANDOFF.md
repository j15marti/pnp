# SCOPE-ALIAS-COMPLETENESS96: Role 3 cumulative delta and gap-to-evidence ledger
Date: 2026-10-25 00:24 Asia/Seoul (2026-10-24 08:24 America/Los_Angeles). P versus NP OPEN; ARC-EDGE-90 OPEN. No automation schedule, agent routing or other role file changed.

## Verified role artifacts
- Mathematical report: `research/agents/lspv-3/2026-10-25_0024_LSPV-3_SCOPE_ALIAS_COMPLETENESS96.tex`; create commit `f3ee44bf81e4353f9d6027197720d4b8c044e3b4`. Proof model: exact 7-event clause-local stream, source-name semantics, proper 3CNF equality repairs, forbidden-region conditional.
- Peer independently runnable stdlib checker: `research/agents/lspv-3/2026-10-25_0024_SCOPE_ALIAS96_peer_repro.py`; create commit `c328a3b4f38497582432bf29eb3520fefb7749f4`. Tested on 375 proper-3CNF sources, 314 SAT and 61 UNSAT, plus 24 occurrence releases, zero discrepancies. Local peer-code SHA256 `cac7ecd9b3da4a811dbe5d874838abe101a03c43dca14867982218342ab6b28b`.
- Public expanded raw summary: `research/agents/lspv-3/2026-10-25_0024_SCOPE_ALIAS96_results_summary.json`; create commit `0e4a4dd7e4b77ff925e57b7f066f3dd2dea990ee`. Extended local full audit 585 sources, 7,196 checks, zero discrepancies. Source SHA256 `f0d3f804c6955c468d66c0a7d993bdbb54a3ae27b4c21ea0e6434918f91b7da7`, raw local JSON SHA256 `f5ccb80ac5fb5330101e125b2c2b60103d2cb0242798e68deee8eb940a99a937`.
- Full extended Python and raw machine-readable JSON are also local conversation artifacts. Their local paths are *not* assumed shared across future scheduled runtimes.

## Exact theorem, quantifiers and receiving obligation
For every ordinary proper three-CNF F with m clauses, build a seven-event OPEN,OPEN,OPEN,CLAUSE,CLOSE,CLOSE,CLOSE block per clause using original global IDs. Locally well-formed stream width is exactly three; original signed CNF after erasing events remains F; local-width-three *reopening* stream SAT is therefore NP-complete by a linear-size map. A frontend DP that silently regards reopened IDs as fresh returns SAT on every source, including UNSAT F. This is a type error: the source is **not a globally valid named scope**.

For every F, freshen each occurrence to its own globally unique name. The resulting globally valid width-three stream is always SAT. Restoring the original SAT semantics requires r=3m-n_+ global equality links between copies of the same original name. A spanning-tree equality representation suffices. Each link has an exact four-proper-ternary, two-auxiliary compiler, so the resulting independent 3CNF has n'=3m+2r variables and m'=m+4r clauses. This is an ordinary linear-size semantic repair, not a power-small child.

For all 24 variable occurrences in the complete eight-clause three-variable UNSAT core, freeing any one source occurrence from global name identification makes the formula SAT. This is not a statement about deleting one arbitrary edge from a selected equality spanning tree.

Receiving ARC obligation remains ONE FIXED uniform all-input exact ordinary-SAT machine for each attainable joint (time,space) point, or a finite cofinal route of such points. The above elementary transformations neither produce a lower bound on unrestricted decision time nor a favorable all-input successor.

## Conditional matched FLMV firewall
Suppose an all-input uniform converter from the reopening language to **globally valid** width-three scoped streams preserves the original SAT label and has simultaneously time exponent r<=1.1, writable space sigma<=.5, output length exponent mu<=1, with every bit/grammar/child/access/switch charge included. Online scoped DP would solve unrestricted SAT in joint exponents (1.1,.5), forbidden by FLMV using c=241/200 and beta(c)=11642479/23232400>.5. Thus no converter can meet all those promises. This applies to the stated full normalizer contract only, not all SAT solvers or arbitrary renaming.

## Cross-role duplication and correction
- Role 4 SCOPE-FRESHNESS-VALIDATION91 already proved one-pass global-name validity requires Omega(N/log N) configuration on its fixed-record width-three family, plus a two-pin reopening SAT/UNSAT counterexample. This report adds the full ordinary 3CNF completeness of the weaker syntax and the all-occurrence identity repair. No one-pass validator bound is reattributed.
- Role 3 EXACTONE-JOIN-CYCLE95 and Role 5 THREE-STATE-JOIN-FIREWALL130 already established NP-complete three-state equality-only module joins. That supports rather than duplicates the new scope-language type separation. The 3-state result is not re-proved as novel.
- Role 3 SCOPED-BLOCK-REBUILDER92 supplies exact short children on an **already valid** narrow stream; its all-input source normalizer is still absent.
- Role 3 LAZY-PIN-SOURCE93 supplies source-indexed virtual inputs but does not shorten their ordinary independent encoding.
- Role 1 DEGREE-MATCH-LADDER132 supplies polynomial matching and conditional FPT in a restricted exact-one occurrence regime, not a general SAT contraction.
- Role 5's current synthesis still has no all-input favorable ARC edge. The previous universal product endpoint t+s<2cos(pi/7) remains retired.

## Experimental and BIT-RESOURCE1 ledger
Full stdlib execution seed 202610250024: 585 original sources, 523 SAT, 62 UNSAT, 120 matched connected both-label controls, all 255 nonempty three-variable subset formulas, 24 single occurrence releases, 7,196 assertion-accounted checks and zero failures.
Logical resource counters: 10,140 source-literal records read, 23,660 scoped events, 7,900 spanning-tree equalities. These are not measured FLMV physical bit steps. Charge each emitted field bit; count all input/work reads, unchanged writes, actual complete-state bit flips, peak live writable cells, cumulative bit-time and program/representation size separately. A full writable copy or equality dictionary can cost Theta(m log(m+n)) bits; rereading/recomputation can trade space for time.
Full script and JSON had deterministic identical hashes on rerun only if rerun; do not infer a second local run from one execution. Peer subset was separately executed locally and its result was compared against the expected analytical counts.

## Coverage manifest and unresolved queue
Live selected full-body reads: root main.tex (in root prewrite state), main13.tex; governance AGENTS.md, CODEX.md and repo research skill; Role 4 SCOPE-FRESHNESS91; Role 3 SCOPED92, LAZYPIN93, EXACTONE95; Role 5 THREE-STATE130; Role 1 DEGREE-LADDER132. The current root was fetched again immediately before writing; the 343k-character whole text is available to the write action, but mathematical reading was selective. Parent ARC native Google Doc fetched fully (22,415 characters, title PROOF-SYNTHESIS-0013, date 2026-09-27). Primary literature was checked via FLMV author PDF text, ACM 2005 metadata and Freuder AAAI 1990 source. The web PDF screenshot endpoint returned a cache-miss error; do not claim a successful new visual screenshot.
Bounded GitHub search queries: scope alias, fresh clause, REOPEN, FRESHNESS, NAMED-PROJECTION, exact-one, HEREDITARY-SCOPED10; results not exhaustive. Prior pinned 3,532-file keyword/hash census is inherited, not re-performed or a complete mathematical review. No new full Drive folder pagination was exhausted. Unread: root main2-main12 full proofs, broader LOG/PROVED_EXACT/Manuscript/BOOL/SIL, original HEREDITARY-SCOPED10 full executable and failed-access named originals. GitHub clone/Overleaf local lint preflight unavailable through raw-network DNS; no compilation/validator pass is claimed.

## Gap acceptance
FILLED: primary FLMV endpoint as known theorem and scoped-stream semantics for the declared grammars.
PROVED/EXACT RESTRICTED: reopening full-language reduction, freshening failure, equality repair, 24 incidence-release witnesses.
COMPUTATIONAL: 585-source finite test; no asymptotic promotion.
FALSIFIED/RETIRED: local active width as unrestricted global-name width; treating detached fresh clauses as SAT-equivalent; uncharged alias table or source pointer.
CONDITIONAL: width-three all-input favorable universal repair would collide with FLMV.
OPEN: all-input source-to-ordinary short children with exact globally named two-level joins and complete same-machine time/space improvement, or any cofinal finite route.
Next inspect original full HEREDITARY-SCOPED10 if actually recovered, and exercise SCOPED92 on the eight-clause UNSAT core, connected opposite-label controls and LSPV-1 root-hard pinned family, with source completeness, genuine independent child bit length and two-level costs. Keep all five original schedules unchanged.
