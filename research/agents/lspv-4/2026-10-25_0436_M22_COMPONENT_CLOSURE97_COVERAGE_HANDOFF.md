# LSPV-4 M22-COMPONENT-CLOSURE97, 2026-10-25 04:36 Asia/Seoul
Status: **PROVED/EXACT restricted original-clause-deletion grammar**. **COMPUTATIONAL** finite audits. **ARC-EDGE-90 OPEN; DIRECT POST-ACQUISITION OPEN; P versus NP OPEN**. Independent peer verification pending.

## Target / exact original-source theorem
For every F in C_M22 (unique proper clausewise-monotone 3-clauses, exactly two positive and two negative occurrences per variable), let c be the number of connected clause-variable incidence components. For ANY subset of the original, unchanged clause records, the resulting CNF remains in C_M22 **if and only if** it is a union of whole source components. Proof: retaining one clause containing x requires retaining all four occurrences of x to keep its exact quotas, then all clauses reached in the incidence graph. Empty CNF is vacuously C_M22, fully paired and outside C_star.

If d components are NOT fully complement paired, the counts of valid clause subsets are 2^c in C_M22 and 2^c - 2^(c-d) in C_star. Complement pairing is component-local. In particular, every connected F in C_star has only **one** C_star source-clause-deletion child: F itself. This is **FALSIFIED/RETIRED as a strict-shrink claim for this named deletion-only constructor**, not a blanket barrier for arbitrary deciders, equivalent rewritings, typed transformations or existential ARC.

## Positive exact link
The source-aware operator Pi(F), for valid F in C_star, removes every fully paired incidence component and retains every nonpaired component. It is idempotent, stays in C_star, and preserves SAT because a fully paired C_M22 component is SAT by Döcker. Full #SAT factors across disjoint components. On connected F in C_star, Pi(F)=F, so this alone gives no power contraction. Parsing, graph traversal, checking partners, source access, reserializing and peak live buffers must be charged. The operator is useful on disconnected instances and admits direct decision without recursive calls.

## Tested both labels
Finite exhaustive 66,048 original-clause subset cases and 66,062 assertion-accounted checks: Y (6 variables/8 clauses/20 models) C_M22 masks 2 and C_star masks 1; fully paired H (6/8/18) C_M22 masks 2 and C_star masks 0; Y disjoint-union H (12/16/360) C_M22 masks 4 and C_star masks 2. Zero failures. Pi(Y union H)=Y.

Original valid connected target UNSAT control U (198 variables/264 clauses) from Döcker Appendix C, Git blob f9dda41a810ad8e02bd553f2711a26a4050861f9, had all 264 single-clause deletions leave C_M22 (separate connector-side programmatic audit). U plus fully paired H has two components and projects to U. **UNSAT imported from published proof, not independently brute forced**. Neither U nor Y test implies every member hard.

## Adaptivity and quantitative gaps
C_A(F,R)+T_finish,A(F,R) is for one fixed uniform total adaptive decider; charge primitive bit work, source/workspace reads and writes even if unchanged, failed recognizers/strategies, cache, variable indices, component discovery, child serialization, exact gluing, peak simultaneous writable/index bits, temporal state flips separately, cumulative bit-time and hardware/program size separately. Psi=sum_j 2^{r_j}; R_search=k-log2(Psi) is only declared independent brute-force completion. There is **no** noncircular post-acquisition Phi here; input-query hitting tau<=N is only input acquisition.

The ARC region E requires one matched exact ordinary-SAT random-access Turing machine for both t,s. The valid FLMV forbidden box is t<241/200, s<11642479/23232400 with beta(c)=((c+2)/c^2-c)/2. Retired t+s<2cos(pi/7) is not a valid universal endpoint. A C_star-only solver cannot inherit that SAT box without an all-input charged reduction. C_star pin children generally exit the grammar; appending Y does NOT repair quotas or ternary width. **The cofinal jointly-charged all-input finite ARC route remains OPEN.**

## Evidence / source coverage
Current GitHub default-branch recursive-tree survey: 4,951 file blobs, untruncated. This is a PATH INVENTORY ONLY. Inherited pinned 55a3fcc audit: 3,532 keyword-searched source/config/prose files, selective manual math, not re-run. Fully/materially read originals this run: AGENTS.md (blob c5265db), CODEX.md (754999f), research skill (b8df83a), root main.tex relevant owner/executive region (before update blob 0af0f39), main13.tex (87dbaad), LSPV-4 M22-UNPAIRED-ANCHOR96 (e912fd3), LSPV-5 M22-ANCHOR-NONADAPTER137 (9956370), LSPV-2 M22-GAUGE-FIREWALL132 (15833a2) and M22-DEFECT-ADAPTER131 (5a8e6af), LSPV-3 PIN-BIT-FLOOR98, LSPV-4 CONNECTED-CRITICAL-BACKDOOR58 (6a61db7), LOCALSHIELD1 STATIC-INCIDENCE-CLOSURE5 (c827e4e), MAIN108 WEIGHTED-TRANSCRIPT-COVER (5cdbf99), Appendix C original U (f9dda41). Eight task file names inventoried, tasks README read; task bodies not exhausted. Bounded default-branch GitHub searches: 'clause deletion', 'occurrence quota', 'component union', 'incidence preservation', exact M22 and hereditary aliases; one broad query failed with 422 search syntax and was replaced with smaller quoted searches; 422 is NOT negative evidence. No independent full Drive LOG/BOOL/SIL/PROVED_EXACT paging, earlier chat, main2-main12 original bodies, all revisions or original HEREDITARY-SCOPED10 executable. Do not infer absence.

Duplicate correction: Generic SAT component decomposition known (Biere/Sinz); prior LSPV-2 DEFECT-ADAPTER131 proves a narrower O(1)-defect two-level restriction floor; peer LSPV-5 ANCHOR-NONADAPTER137 already proves anchor grammar iff source grammar. Current exact **all-original-clause-subsets** closure/count and paired-component projection are a distinct restricted proof, not an NP lower bound. Peer LSPV-2 M22-GAUGE-FIREWALL132 concerns entire-component variable sign gauges, not deletions.

## Primary literature
Janosch Döcker, Monotone 3-Sat-(2,2) is NP-complete, arXiv:1912.08032 (2019).
Armin Biere and Carsten Sinz, Decomposing SAT Problems into Connected Components, JSAT 2 (2006).
Omer Reingold, Undirected Connectivity in Log-Space, JACM 55(4) (2008).
Fortnow et al., Time-Space Lower Bounds for Satisfiability, JACM 52(6) (2005).

## Peer next artifact / required implication
Recover original HEREDITARY-SCOPED10 fully specified generator (not just continuity report), or design a monotone type-restoring all-input source-consistent recursive child compiler. Test **two recursive levels**, connected in-target Y SAT and U UNSAT plus paired products and independent affine/Horn/SCC/easy controls, exact ordinary header and bit access, changed representations, compatibility reconstruction, output work, ancestor/cache peak space. If no favorable jointly achievable ARC route exists, pursue independent post-acquisition Phi with bounded drop under every adaptive operation and independent large initial Phi, avoiding semantic/oracle circularity.

### Published artifacts
Report: research/agents/lspv-4/2026-10-25_0436_LSPV-4_M22_COMPONENT_CLOSURE97.tex
Reproducer: research/agents/lspv-4/2026-10-25_0436_M22_COMPONENT_CLOSURE97_AUDIT.py
Raw summary: research/agents/lspv-4/2026-10-25_0436_M22_COMPONENT_CLOSURE97_RESULTS.json
Additive handoff: research/agents/lspv-4/2026-10-25_0436_M22_COMPONENT_CLOSURE97_COVERAGE_HANDOFF.md
