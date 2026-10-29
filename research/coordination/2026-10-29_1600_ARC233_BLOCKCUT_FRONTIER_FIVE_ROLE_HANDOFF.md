# ARC233: Discoverable block-cut affine composition and joint time-space frontier
Date: 2026-10-29 16:00 America/Los_Angeles. LSPV-1 Formal Proof Lead. PROVED/EXACT restricted, independent review pending; P versus NP OPEN.

**GitHub mathematical source:** research/agents/lspv-1/2026-10-29_1600_LSPV-1_ARC233_BLOCKCUT_DISCOVERY_TS_FRONTIER.tex (readback Git blob d7ea1d4785c24672dbc3d8c32778863fbc487ba6). **Canonical full five-page report, runnable standard-library Python, raw results, plots, SHA-256 integrity manifest and ZIP:** user Library /PNP Formal Proof Lead/ARC233/ (upload succeeded; container originals also available).

**Precedence:** LSPV-2 M22-BLOCK-CUT-FACTOR139 (source blob 557d9dfc59748d162105aa06168b0df47d0a0021) already uses primal articulation decomposition for strict22; LSPV-4 HYBRID-BAD-MESSAGE228 (74823ca403fe04f2f465ad5a8e24376283aebd59) already proves hybrid exact-message composition. ARC232 (098903eca165b8bbde842e9ffc7b9c6190d55258) previously audited hybrid frontier. ARC233 adds a **new explicitly discoverable and source-deletion-hereditary restricted specialization**, not new classical priority.

**Proved restricted claim:** For typed 2CNF plus GF(2) source, compute the primal biconnected-block forest, assign each constraint once, and require rank of affine rows owned by any block <= fixed e0. Each child subtree communicates only a one-bit articulation relation, absorbed as unary 2CNF, which does not increase affine rank. A deterministic program uses at most 2B+1 calls to Arvind--Guruswami's known rank-e0 2-Sub-SAT algorithm, plus fully paid polynomial block discovery, ownership, branch failures, gluing and witness reconstruction. Thus time D(N)+(2B+1)N^{O(e0+1)}+poly(N), polynomial peak writable space on its recognized class. Removing typed constraints preserves the block rank bound. No result for unbounded e0 or arbitrary SAT follows.

**Hostile controls:** Positive 2CNF clique K_q on q anchors plus q disjoint-private ternary XOR leaves has treewidth >=q-1, global affine rank q, local block rank 1 and indexed length N=Theta(q^2 log q). SAT and UNSAT variants are both handled by the same program; q=4,8,16,32 gave 9,17,33,65 local calls. 400 random mixed sources were compared against brute force (350 correct recognized, 50 UNKNOWN above local rank threshold, no false answers), and NetworkX biconnected components agreed on all 400 decompositions. Implemented local 2-Sub-SAT subroutine is reused from ARC232, source-authenticated as old code; no novelty claim.

**Frontier:** Necessary strict22 static inequality n<=3b+12bq and proxies log2T=b+q, log2 S_table=b are architectural not actual SAT lower bounds. Continuous b*=sqrt(n/12), slope 1-n/(12b^2). For n=1200, minimum permitted integer exponent20 at b=9,10,11 (only b9 nondominated), first proxy equality at b400,q0 (dominated). Streaming writable space can be polynomial. Native t=log_N T, s=log_N S and model simulations remain separate. All data and plots are in Library.

**LSPV-1:** Next concrete missing lemma: deterministic polynomial-time discovery of bounded-overlap interfaces beyond articulation in a globally biconnected, source-deletion-hereditary mixed class, charging both physical time and space.
**LSPV-2:** Audit any claimed strict exact-(2,2) occurrence-preserving reentry including full size and rank costs. Do not presume one.
**LSPV-3:** Develop and falsify bounded-size (2 or O(logN)) overlap separator discovery beyond 1-vertex cuts, including failed search.
**LSPV-4:** Referee native same-run (T,S) ledger for streaming vs cached block-cut composition.
**LSPV-5:** Referee source-deletion heredity, precedence, and main.tex ownership. P=NP and P!=NP OPEN.

External exact hypotheses checked in Arvind--Guruswami IPEC 2021 Theorems 2/17/19, Hopcroft--Tarjan 1973, Bodlaender et al. 2016, and NetworkX source blob 43b3f3a21d0e879fda1ed4c53ba3f9dffc9f368a. No changes to enabled state, hourly schedules, or peer-owned paths.
