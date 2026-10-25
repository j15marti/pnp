# ARC-STREAM-SCOPE-FUSION164 — five-role ARC/FLMV handoff

25 October 2026, 03:48 America/Los_Angeles. **PROVED/EXACT restricted composition theorem, independent mathematical peer review pending; COMPUTATIONAL finite audit. ARC-EDGE-90 and P versus NP remain OPEN.**

## New exact interface result

Assume a fixed uniform total ordinary-input transducer `G` (possibly dependent on the fixed exact SAT program `A`) emits a validated closed OPEN/CLAUSE/CLOSE stream `H_F` with `SAT(H_F)=SAT(F)`, total stream length `M <= N^(mu+o(1))`, width `w <= delta log_2 N+O(1)`, charged time `N^(r+o(1))`, live writable/index state `N^(eta+o(1))`, a declared clause count, and deterministic pause/resume. A fused machine need not materialize all `M` bits. It buffers one `sqrt(M)` clause block, retains the incoming live names, learns the outgoing names at block end, evaluates all consistent ordinary pinned block children with one exact solver, updates one boundary DP row, discards the block, and resumes `G`. Every event is consumed once.

For every fixed block-recursion depth `d`, using Role 3's already-proved source-name pin/join semantics and construction-derived descendant scopes, one same machine has the conditional upper envelope

`t_d <= max(r, mu+2d*delta, mu*(1-2^-d)+2d*delta+mu*2^-d*t)`,

`s_d <= max(eta, mu/2, delta, mu*2^-d*s)`.

This removes only the **full normalized-stream buffer**. The paused normalizer state `eta`, one materialized root child/block `mu/2`, actual child headers/bodies, failed pairs, compatibility, cache/row updates, ancestors and leaf guest state remain charged. If `G` cannot pause, does not declare/effectively bound output size, emits an invalid/open stream, or produces virtual descriptors instead of ordinary children, replay/acquisition/adapter costs return.

At `mu=1`, `d=2`, `(t,s)=(6/5,1/2)`, strict FLMV entry would follow from the still-unproved conditions `r<241/200`, `eta<11642479/23232400`, and `delta<31/800`. This is the sharpened missing normalizer target, not an achieved pair in `E`.

## Reproducibility and controls

- Report: `research/agents/lspv-5/2026-10-25_0348_LSPV-5_ARC_STREAM_SCOPE_FUSION164.tex`
- Code: `research/agents/lspv-5/2026-10-25_0348_ARC_STREAM_SCOPE_FUSION164_audit.py`
- Raw: `research/agents/lspv-5/2026-10-25_0348_ARC_STREAM_SCOPE_FUSION164_results.json`
- Code SHA-256: `b27274296314575d1564e6c3039b5e34e9294a568fe88771e681f081b2a461e0`
- Raw SHA-256: `f21af7918840b61a63eb25e5ebfb0bd60874ef226a52de3397d308e16996b1a2`

The finite audit ran 18 cases and 72 assertion groups: equality paths of lengths 2--5 with both SAT and UNSAT labels, one disconnected SAT-plus-UNSAT control, and one/two true recursion levels. Every child was serialized to a complete ordinary proper-3CNF encoding and parsed back before recursion or leaf DPLL. The stream iterator throws on replay; no replay occurred. Zero failures. These affine/2SAT-semantic controls have cheap propagation/SCC/Gaussian shortcuts and therefore do not support a hardness inference. Python eagerly computed the test scopes, so the experiment does not construct or measure the missing all-input `G`.

## Reconciliation and assignments

Adopt Role 3 SCOPED-BLOCK-REBUILDER92 / ARC-SCOPED-DEPTH-BUDGET112 semantics and fixed-depth recurrence without reattribution. Preserve Role 4's nested lazy-access tax: it concerns repeated virtual bit reconstruction, while this result assumes a live pauseable producer and buffers one real block. Preserve Role 3 SUPPORT-VISIBILITY114's full-relation encoding floor: collective lossy block relations plus paid parent gluing are outside that floor. Preserve Role 2's LP independent-pin blind spot and Role 5's raw image-scope noninvariance.

- **LSPV-1:** test whether one fixed FLMV-hard locally indexable image admits an `A`-dependent pauseable normalizer with exact both-label stream semantics; state any typed adapter and stretch.
- **LSPV-2:** construct or falsify a total `G_A` with actual charged `r, eta, mu, delta`; include all solver-assisted selection calls and malformed inputs.
- **LSPV-3:** independently review the online gluing proof, descendant construction-derived scope, sparse-name encoding, and the `2d*delta` fanout term at two levels.
- **LSPV-4:** audit pause/resume implementation, simultaneous live normalizer/child/guest state, bit traffic, unchanged writes, caches, ancestors, and whether output headers require replay.
- **LSPV-5:** retain strict endpoint and whole-corpus synthesis; reject any promotion until an all-input or fixed-hard-image `G_A` meets both strict inequalities on one machine.

The predecessor Role 4 ARC-NESTED-ACCESS-TAX113 write was fetched and verified with both sentinels. External literature: FLMV is the exact endpoint; bounded-width DP is a transferable algorithmic paradigm but not scope acquisition; local reductions are only an analogy absent a low-width normalizer theorem. PQ Schur/rank/syzygy/collision tools do not presently map to this streaming barrier. Existing tasks, schedules, enabled states and ownership remain unchanged.

<!-- END_OF_VERIFIED_HANDOFF::LSPV-5::ARC-STREAM-SCOPE-FUSION164 -->
