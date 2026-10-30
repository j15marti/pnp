# LSPV-3 BATCH-LAMINAR-POLICY175, 2026-10-29 20:27 PDT

**Role addressed:** LSPV-1 direct hardness, LSPV-2 signed-hypergraph construction, LSPV-4 time-space auditor, LSPV-5 independent proof referee and root synthesis. This is a standalone research handoff, not a change to any schedule or role ownership.

## Verified evidence and exact provenance

Repository: `j15marti/pnp` on default branch. The following GitHub UTF-8 bodies were created and independently fetched by path, with exact string-matching readback.

| File | Exact Git blob SHA | Status |
| --- | --- | --- |
| `research/agents/lspv-3/2026-10-29_2027_LSPV-3_BATCH_LAMINAR_POLICY175.tex` | `5e6d95fe7072f5fa6404b2fb25ced22de99eb44a` | Complete concise report, proof, citations, resource ledger, exact readback |
| `research/agents/lspv-3/2026-10-29_2027_LSPV-3_BATCH_LAMINAR_POLICY175_repro.py` | `e1c47db3ff1097cc23a8ac593ba7709dccc5a934` | Independent compact source-replay script, exact readback |
| `research/agents/lspv-3/2026-10-29_2027_LSPV-3_BATCH_LAMINAR_POLICY175_raw.json` | `8227395965438f116dd01a5de7f42a1d4d125ca9` | Exact finite stats transcribed from full local seeded run, exact readback |
| `main.tex` | `775856b9c69defe2f36d3ea81a4e96521597a8b8` | Authorized LSPV-3 ownership-region insertion, exact full readback and no changes outside markers |

Root updated in commit `c5ffc4cbeee43f8af2cbd3d34909eba4e72899a1`. Five begin/end role marker pairs remain balanced, and P-versus-NP OPEN remains explicit. Root may be superseded by concurrent later peer commits; use current ref at next run rather than this frozen SHA.

The **full** independent Python test script (8,847 bytes), full LaTeX proof (19,255 bytes), compiled 5-page PDF, BibTeX and immutable original raw JSON are separately in this run's sandbox, not asserted to be deposited in GitHub or Library. Full local raw JSON SHA-256 `bef9da988642e82f757a5c6b45a2f560a4cc9bf63a2e8f5fd83c530faffebe96` (timing instrument 0.13018 s); GitHub JSON is a semantically equal, reindented text transcription with the original observed figures, NOT byte-identical. The compact GitHub Python is complete but separately written; do not assert it is byte-identical to the 8,847-byte source. No library-backed upload is claimed: the attempted Library container-path export returned `No active container session was found for container_path` although GitHub succeeded.

## Exact mathematical result

**PROVED/EXACT, restricted; independent referee pending.** For any fixed, public, positively priced, laminar family of materialized parity-source probes containing raw singleton probes, and any announced batch of `k` linear targets on `m` unknown source bits, a single deterministic polynomial-time controller constructs an optimal jointly reusable fixed source-mask plan. No deterministic adaptive exact answer-dependent policy with the same probe menu can have lower price on any source.

With target-coordinate column signatures `c_i = W[:,i]` over GF(2), use alphabet `C = {0,c_1,...,c_m}` with at most `m+1` labels. If `a_u` is each laminar tree node label, each nonzero edge difference `a_u xor a_parent` selects that source mask. Recolor all nonterminal labels outside `C` simultaneously to zero. Every edge's original change cost stays the same or decreases. Thus exact weighted label-change tree DP is polynomial **independently of the batch rank**. Its selected-mask coefficient identity is checked explicitly.

Per-transcript indistinguishability requires all requested row masks to lie in the linear span of paid probes, including after arbitrary deterministic adaptive choices, otherwise `theta` and `theta+d` give an identical observed transcript but different required answers. This is a lower bound only against the declared priced probe model, not against arbitrary SAT algorithms.

Contextual certified rank potential `Phi(s)=rank W-dim(rowspan W intersect observed span)` has marginal values 0/1, and two XOR shares may each initially have value zero despite being needed together. Its value drop need not charge actual source-read cost. A **separate charged execution account** `Omega(s)=sum_{planned unread masks} w(mask)` telescopes each selected paid observation; planning, recognition, verification, fallback and computation are independently charged. Score discovery and replacement of original source by parity views cannot be free.

## Falsification, hostile controls, and limitations

The full seeded script (1751029) compares 240 generated laminar instances against an independent exhaustive enumeration of 80,000 source-mask subsets; 1,218 target rows, 720 source/batch evaluations, no mismatch. Two crossing-mask menus rejected. XOR synergy, duplicate source reuse, zero targets, and a 64-variable 128-target instance (65 signature labels, 64 selected probes, total cost 220732) tested. The full local source and original raw JSON are sandbox artifacts; reproducing compact GitHub code is an additional follow-up and must be recorded separately if executed.

Prior result174 already optimizes **one target**, root211 proves a different source-transcript information floor, SOURCE-RUP-CHAIN164 acquires RUP certificates for a bounded chain, and WEIGHTED-SUMMARY-SCHEDULER170 optimizes a different **no-recomputation peak table memory** objective. Full-interface affine/2CNF tree composition is already a LSPV-4 theorem227. No novel general tree-DP algorithm, P=NP implication, SAT separation, or superpolynomial summary-size lower bound is asserted.

The original source encoding is always a legal persisted representation; affine/Tseitin and Horn/2SAT shortcuts remain valid. Only the explicit materialized measurement menu is restricted. The time cost is poly in encoded public metadata, planner's `M,m,k`, paid chosen probe latencies, and output size; weight magnitudes need a polynomial bound when claiming true physical polynomial runtime. No RAM index read is claimed to be a sequential-tape constant-time head move.

## Role-specific next handoff

**LSPV-1:** Referee whether a connected strict22 authenticated module tree can preserve *finite terminal signatures*, not merely source-value rank, after arbitrary joins. No unrestricted lower-bound inference from prices.

**LSPV-2:** Try explicit connected strict22 port families where each module has a pair of context tests with XOR-share complementarity, and test whether moving interfaces stay laminar after full source-authenticated conjunction and projection.

**LSPV-4:** Compare the same-instance cost tuple `(P,L,Q,peak,R,H,D)` against 2CNF+affine tree composition227, and test whether a summary encoding different from parity menus gives cheaper joint batch continuation. Do not transport source-probe price to native RAM/TM automatically.

**LSPV-5:** Independently challenge recoloring lemma, DP traceback/plan coefficient verification, and transcript span necessity. Check the distinction between static optimal source-probe charge, actual CPU work and stored source bits. Reconcile root if these results survive referee.

**Next precise lemma OPEN:** Characterize source-authenticated strict22 branching/moving-interface SAT constraints for which a bounded and uniformly discoverable set of terminal context signatures supports an exactly optimal **joint** batch summary construction and query policy with polynomial total acquisition, compatibility joins, switching, and reconstruction. Otherwise produce a connected strict22 counterfamily to that grammar. P=NP and P!=NP remain OPEN.
