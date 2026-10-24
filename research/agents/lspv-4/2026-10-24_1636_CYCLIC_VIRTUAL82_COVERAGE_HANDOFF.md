# LSPV-4: CYCLIC-VIRTUAL-SELECTOR82 coverage and ARC gap handoff

Date: 2026-10-24, 16:36 Asia/Seoul. **P versus NP remains OPEN.** This is a source-addressing and bit-resource result, not an all-input SAT contraction theorem. Independent review is pending.

## Peer-accessible artifacts, verified by GitHub readback

Report: research/agents/lspv-4/2026-10-24_1636_LSPV-4_CYCLIC_VIRTUAL_SELECTOR82.tex, blob 265eba9c5b2e80be7f9405e39f13da6e49818acd.
Independent runnable mini-auditor: research/agents/lspv-4/2026-10-24_1636_CYCLIC_VIRTUAL_SELECTOR82_MINI.py, blob 8862025e2faccab2965488565b8cdde1a3ef20ce.
Full-audit summary and local executable/raw SHA-256 provenance: research/agents/lspv-4/2026-10-24_1636_CYCLIC_VIRTUAL82_RESULTS_SUMMARY.json, blob a7b4fee0493eb822e64a1953582b58ee4437d397.
The complete local Python audit and raw JSON are separate user attachments, not shared persistent files. Do not assume a transient container path is accessible to another scheduled runtime.

## Exact new link, restricted model

For a canonical proper 3CNF with M=2^h ordered clauses, n=M-3 and encoded length N=(4M+2)ceil(log2(64(n+M+1))), set odd K=Theta(sqrt(N)/log N), 2K<=M, and Q=min(M,floor(N^(3/5))). The ordered child j has original clause indices

    s(j,i)=(j*K+i) mod M, 0<=i<K.

The full ordinary child retains the variable header n, records clause count K, recomputes its fixed word width from n,K, and has exact length L=(4K+2)ceil(log2(64(n+K+1)))=Theta(sqrt(N)). A fixed uniform arithmetic controller using O(log N) writable bits outputs any requested ordinary child bit in polylog(N) bit work by charged addressing and source reads. M is a power of two and K odd, hence all Q<=M children are distinct. Consecutive child index sets are disjoint when 2K<=M.

**PROVED/EXACT restricted:** A canonical flat materialized child array at fixed addresses incurs at least K changed literal-code fields per transition, hence Omega(QK) actual changed bits/field writes across this schedule. An exact arithmetic virtual service avoids those child-buffer writes and stores only the O(log N)-bit controller state. It must still pay on every requested solver input bit. This does not contradict the prior ceil(log2 binom(M,K)) all-subsets full-service capacity bound: the latter covers every K-subset, whereas this construction services just Q arithmetically generated selectors.

## Same-machine conditional accounting

Given ONE fixed all-ordinary-input total uniform exact SAT decider A with simultaneous T_A(L), S_A(L), each virtual child call costs tilde-O(T_A(L)+1) time and tilde-O(S_A(L)+log N) space in a random-access read-only-input machine simulation. Charge all original source access. Let R(N), H(N) be additional parent-local semantic gluing, selection, failed attempts, cache and ancestor costs. **Only if** a separately proved all-input exact parent-label reconstruction exists for this portfolio can one write

    T_parent <= tilde-O(N+R(N)+Q*T_A(L)+Q)
    S_parent <= tilde-O(log N+H(N)+S_A(L)).

For R=N^(r+o(1)), H=N^(sigma+o(1)) this would yield

    t' <= max(1,r,3/5+t/2),
    s' <= max(0,sigma,s/2).

The required semantic gluing rule is OPEN. These inequalities do not assert a new achievable SAT pair.

## Opposite-label hostile controls and adaptive state switching

Reuse the original MINIMAL-UNSAT-PROJECTION20 formulas F_m (minimal UNSAT) and G_m (SAT) with M=2m+6, n=2m+3=M-3 and identical encoded length. Every strict clause subset of both is SAT. Since K<M, all Q cyclic deletion children of both sources return SAT, while parent labels differ. This source-pair lemma is **already known** and is used only as a stringent falsifier. A direct source-aware recognizer can decide this restricted family after a paid grammar scan; an arbitrary solver is not forced to follow the children.

The tested total uniform adaptive policy first recognizes the family using input-derived clauses, then makes an exact direct decision if recognition succeeds, otherwise switching to DPLL on unsupported formulas. The true SAT/UNSAT label is never supplied. Canonical SAT and UNSAT, a mutated-grammar fallback, a generic Horn-like SAT instance and an eight-clause UNSAT triple are controls. The experimental menu is not all-decider coverage.

## Computational / BIT-RESOURCE1 ledger

The full local standard-library audit completed **53,005 assertion-accounted checks**, zero failures, across M=16,32,64,128,256,1024,4096. There were **302,812 complete ordinary-child bit comparisons** and **39,324 selected bit checks**. At M=4096, N=311334 bits, K=31, Q=1976 and L=2394 bits, the fixed buffer changed 183675 word fields between consecutive children. The binary child-index counter flipped 3941 bits, excluding arithmetic scratch, input scans and solver work. Counter flips are not equated with total primitive work. Count work bit operations, source/workspace reads and writes including unchanged-value writes, complete-state flips, peak live writable bits, cumulative bit-time and representation/program size separately. No random test seed was used.

## Cumulative source coverage and gap-to-evidence ledger

Inherited baseline: pinned commit 55a3fcc10f74419c9c3e1a577ed0f8ce83e2f640 covered 3532 repository prose/source/config files with SHA verification and keyword searching. That broad crawl was **not** repeated or upgraded to exhaustive manual mathematical review.

Full or materially focused reads: root main.tex (head and LSPV-4 region, pre-write blob 9afd01b452578f4e5f1c49a8b1a6e2f612fca551), main13.tex; AGENTS.md; CODEX.md; .codex/skills/pnp-research/SKILL.md; research/main/2026-10-20_1748_MAIN_MINIMAL_UNSAT_PROJECTION20.md (blob 823e1175fe271e8cb3be027d0115d7144b58b8ce); research/coordination/2026-10-22_0948_VIRTUAL_CHILD_COMPOSITION61_HANDOFF.md (cb631fb8cc1bb45af0d0bd6ff8673d2a9eb58b9b); research/coordination/2026-10-22_1048_SELECTOR_VIRTUAL_CHILD62_HANDOFF.md (7dbe309e216bf5eaebfcd0134150ffd7e5bbad19); research/handoffs/2026-10-20_1548_CACHE_MISS_FRONTIER18_HANDOFF.md (57c8f3a042b29ba5888ae94f542a4600ba305a5a); its executable; Role 2 CHILD-SCALE-PREFIX117 (42b08e1a82dff59889a9aa98c4035f4b58a163b2); Role 3 FORBIDDEN-COMPUTATION84 (309a24ef1a503b5463225defa90ee16d9962e55a); Role 5 QUIESCENT-CHILD-REUSE (2c848bc49f05b5651b6843a0d91dfce9889f2530); Role 4 SELECTOR-CAPACITY-BIT-LEDGER81; and previous PC22_ALLFIELD1 (0aa4113f2c36cfaa05d71beb41f38406a88c6).

Bounded repository queries included HEREDITARY-SCOPED10, CACHE-MISS-FRONTIER18, VIRTUAL-CHILD-COMPOSITION61, MINIMAL-UNSAT-PROJECTION20, CP22LIFT1, PC22_ALLFIELD1 and implicit/cyclic selector phrasing. They are not a claim of corpus exhaustion. The native September 27 Google Doc ARC precursor was retrieved. Historical Drive LOG/BOOL/SIL folder pagination and full-body review of main2--main12 remain unread. The complete original HEREDITARY-SCOPED10 executable was not recovered; continuity summaries and missing transient paths are not a verified construction.

Primary literature: FLMV, *Time-Space Lower Bounds for Satisfiability*, JACM 52 (2005), sections 2.1 and 3, Corollary 5.8, including model and endpoint PDF screenshots. Jahanjou--Miles--Viola, *Local Reductions*, Information and Computation 261 (2018), original arXiv HTML. The FLMV box uses t<c and s<beta(c), beta(c)=((c+2)/c^2-c)/2; for c=241/200, beta(c)=11642479/23232400>1/2. The historical universal t+s<2*cos(pi/7) SAT endpoint remains FALSIFIED/RETIRED.

**FILLED restricted:** exact cyclic local ordinary-child bit service, distinct/disjoint schedule, logarithmic controller and flat-buffer update floor. **PARTIAL/RESTRICTED:** virtual input simulation and source-model bridge. **CONDITIONAL:** improved resource recurrence. **FALSIFIED/RETIRED:** mandatory QK writes or K-index array for every selector schedule; strict-child SAT labels alone reconstruct the parent label. **OPEN:** any all-input, both-label favorable SAT achievable-pair successor and final ARC/FLMV contradiction.

## Directed peer review and next inspection

Role 5 should verify indexed bit service, read-only original input, bit-operation overhead and the same-machine peak-space arithmetic, while refusing any all-input closure promotion without semantic gluing. Roles 1--3 should use the same F_m/G_m plus cyclic selectors as common compression and reconstruction falsifiers. The next critical original is the full HEREDITARY-SCOPED10 executable; if recovered, test two recursive levels, paid source discovery, exact ordinary bits and headers, both labels, boundary compatibility, cache resets, mutable writes, live ancestors and peak work bits. Existing schedules are untouched; no emails or third-party messages were sent.
