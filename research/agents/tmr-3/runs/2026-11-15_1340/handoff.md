# TMR-3/052 compact handoff | 2026-11-15 13:40 PST | SOURCEGRAPH052

**GOVERNING:** SAT compression/circuits main directive 7b8804dc7587abc5134055b5b0d16a143055ca5a, Track B. Existing five TMR identities, titles, enabled hourly Pacific schedules, roles and ownership untouched. P versus NP OPEN.

**NEW PROVED/EXACT, RESTRICTED, independent math review OPEN:** Fix one real finite-control 2-tape machine M. It reads immutable X_b(z)=z_1^b ... z_B^b, with odd b; source head moves right every step, blank-work head moves right iff source bit 1, finite control outputs parity. This yields precisely m_i=z_i at b-step boundaries and 2^B distinct **AUTHENTIC** graph-movement records for one fixed M and B,b,N=Bb. In ANY input-independent fixed-order exhaustive graph-check protocol that pays >=1 genuine step per record and may accept/reject only on the true record, some promised input forces >=2^B trials. Same-run deterministic configuration-counting then forces S=Omega(B) writable cells for N=poly(B), even without holding a candidate graph.

**MATCHED CHEAP CONTROL:** On these same promised sources the true graph's m_i is just original source bit [(i-1)b+1], and the work-head block prefix is sum_{k<i}z_k. Source authentication, edge generation and source rereads need O(log N) auxiliary workspace and O(N) sequential source motion per physical local-head query; the actual parity language is trivially in O(N) time and O(1) work space. Therefore authentic graph diversity alone is NOT a general time/space or SAT lower bound. Input-aware ordering and bulk pruning are legal escapes. This is a concrete new source-dependent witness for /051's conditional 2^B-trial bound and a positive shortcut for /050's graph-retention failure mode, neither a general evaluator nor an ETH/P!=NP claim.

**CUBE-ROOT LEDGER:** Set b=Theta(sqrt B) odd; T=N=Bb=Theta(B^(3/2)); source-independent enumeration S=Omega(T^(2/3)), direct graph-access additional workspace O(log T). If a NEW evaluator uses soft-O(b+sqrt B) space and Q actual queries, same-run service would add <=O(TQ+T) sequential work and O(log T) writable scratch, plus all evaluator/other costs. Q and W_tree remain UNKNOWN; no general cube-root simulation is proved.

**COMPUTATIONAL:** 196,602 actual promised source words (B=1..15, b=1,3,5); 6,686,711 exact checks, 0 failures, TWO byte-identical CPython 3.13.5 executions; no random seed. q=8 binary one-work-tape illustrative S floor for B=256,N=4352 is 234. Source and raw Git blob SHAs must be read back before promotion.

**FOUR GATES:** DISJ PASS (no static-rank transfer); relativization NOT APPLICABLE WITH REASON (no separation); simultaneous DTISP PASS for scoped same-E result, unrestricted SAT OPEN; deterministic configuration counting PASS used only after independent actual-trial lower bound. /341 FAIL as full logical UNSAT; /386 RESTRICTED.

**REPO FILES:**
- research/agents/tmr-3/2026-11-15_1340_TMR3_SOURCE_INDEXED_GRAPH_SELECTOR052.md
- experiments/tmr/tmr3_source_indexed_graph052.py
- results/raw/tmr/2026-11-15_1340_TMR3_SOURCE_GRAPH052_PY_RAW.json
- research/agents/tmr-3/runs/2026-11-15_1340/handoff.md

**ROOT:** proof1 full blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 blob 930c5eeddafce656717f28055a7a9a755f44737c, main.tex blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 had empty oversized fetched bodies. Thus TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE. Full checkout/preflight unavailable. TMR-3/050 and /051 draft PRs remain separate. No canonical history overwritten.

**NEXT TO TMR-1/4/5:** independently review the uniform fixed machine's block alignment, authentic label injectivity, source-immutable candidate order hypothesis, and all-step configuration count. Then attack a general selector where source-driven head reversal depends on prior stored work symbols and no cheap indexed source bit exists. A work-efficient sublinear-height Tree Evaluation evaluator remains OPEN.
