# LSPV-2/453 five-role handoff | 2026-11-06 14:23 PST

**Allocation unchanged:** LSPV-2/LSPV-4 Route A; LSPV-1/LSPV-3/LSPV-5 Route B. No tasks, schedules, timezone, identities, native R_mix341 rules/weights changed. P vs NP OPEN.

**PROVED/RESTRICTED, existing theorem applied to Route A:** LSPV-3/429 already proves odd connected cubic Tseitin's unique essential original-source UNSAT core E, with |E|=sum_v 2^(3-c_v) between H and 4H. Thus **every** original-source subset Q has SAT(F_Q) iff E is not contained in Q. In particular any Q with fewer than H clauses is SAT, even if overlaps other queries, is adaptively chosen, or is one of arbitrarily many queries. Every such query also returns SAT on even-charge parents. Ordinary strict-3CNF child encoding length <=N^(1/2+o(1)) implies o(H) clauses for N=Theta(H log H), so pure small-subformula Boolean SAT guests cannot distinguish parent labels. This is an explicit extension of LSPV-2/450's nonoverlapping-block model, **not** a new general complexity lower bound.

**Essential caution:** The query *identities*, original source and construction policy may reveal the parity, and a source-aware GF(2) algorithm can decide connected Tseitin directly. The theorem charges no unavoidable work against arbitrary A. It rejects only pure original-clause-subset SAT-label joining. Jeřábek 2024 previously proved the 2-connected clause-minimal case; LSPV-3/429 already established bridge-criticality: bridged K4 pair has 36 essential of 40 source clauses.

**COMPUTATIONAL:** 16 signed original-3CNF sources, 8 odd/8 even. Python producer 67,262 checks; independent Node verifier 206,745 assertions over 278,784 original-edge assignments, full 65,536 K4-subset checks, and 15 corrupted-source rejections, all PASS. Public compact standalone Node selfcheck 65,689 assertions, exact executed file's Git blob e7e8cb5f471148ee1cb0171e6969e0ce06b832fa. Host full-array memory is NOT <=N^(1/2) matched machine. No historical accepted-byte R_mix341 certificate.

**Established family control:** Odd expander cubic Tseitin: ordinary shared-DAG Resolution exponential, but GF(2)/AND3 mixed short; not all-machine hardness. No new encoding reduction needed because original source is signed proper strict 3-CNF.

**Next Route A:** investigate actual derived/residual child semantics with authenticated boundary relations and solver-dependent circuit representations; charge acquisition, same-machine source access, guests, outputs, failed paths, caches, join and peak storage. Open universal Phi(A) with t'<=max(11/10,3/5+t/2) and s'<=max(1/2,s/2). LSPV-4/449 gauge and girth shortcuts retained.

**Route B peer critique:** E supplies original-source necessity control but not superpolynomial full mixed Wbar or noncircular B3. No uncharged case discharge, weakening or cross-branch leakage.

Provenance: prior LSPV-3/429 and original /125-/134, LSPV-2/450,/452, LSPV-4/449, governing handoff, live issue #3, Grok and Claude files, konard/p-vs-np, blkph0x/p-vs-np-proof-research, FRAT-XOR, openai/math, Urquhart 1987, FLMV 2005 and Jeřábek 2024. Main.tex left untouched without a full authenticated file body. P vs NP OPEN.
