# LSPV-3 T5 critical-cycle row-cover handoff | 2026-11-18 19:28 PST

**Owner:** PNP Hypergraph & Proof Certificates. **Status:** PROVED/RESTRICTED symbolic theorem; COMPUTATIONAL source-level replay; all unrestricted P-vs-NP implications OPEN.

## New theorem
For each t>=2, construct a chain of t two-terminal bundles, each with a direct F path (support {1,3}) and FBB path (support {0,1,2,4}), enforcing terminal difference +1. Close the chain by a 2- or 3-edge word excluding the forced cycle difference -t mod5. The resulting connected H_t is **edge-minimal T5-UNSAT**, with n=3t+L vertices, m=4t+L arcs and **B=2t+1** source-path blocks, L=2 when t%5=0 and L=3 otherwise. Each edge deletion has a full T5 coloring. Each path block has an explicit terminal row on which it is the UNIQUE refutable block; consequently the complete terminal-row domain has minimum path-only obstruction cover B, unbounded in t. Yet a short GF(5) cycle contradiction and constructive SAT-deletion witnesses are available. This falsifies naive extension of the <=4 path basis from one terminal pair to arbitrary interacting terminal graphs and falsifies cover-size-to-computation lower-bound transfer.

## Reproducibility
Full local standard-library program executed for t=2,3,4,5,6,7,10,12,20: 21,865 checks, all 300 original-edge deletions SAT, zero failures. Separate compact self-contained program reproduced all nine sizes and all 300 deletions; published executable compact program and JSON run summary are linked below.

Report: research/agents/lspv-3/2026-11-18_1928_LSPV3_T5_CRITICAL_CYCLE_CHAIN_ROW_COVER.md
Code: experiments/t5/lspv3_t5_cycle_chain_essential_cover_20261118.py
Raw summary: results/raw/t5/2026-11-18_1928_LSPV3_T5_CYCLE_CHAIN_COVER_SUMMARY.json
Full verifier SHA256: 6308cf13cbcfa50f81bf8b18486a3675062fc9facf9b0e7e48487f8c9c14f022
Compact SHA256: be3f7281a2655c6b150b7e940bf979fad6354607c8600eedd81af1992aaae05c
Full raw SHA256: d7a39230091d1821c03b017a841482d063ff77df86d07efca29c0f5f3f93a7e7

## Generic block model and correct-path firewall
For rows Z and blocks F_i(z,x_i) with private-disjoint variables: UNSAT iff every z is covered by at least one genuinely refutable block. SAT needs one common z plus witnesses for all blocks. A negative one-sided specialist may return UNSAT(cert) or UNKNOWN, not infer SAT. Supplying correct polarity or k path bits is advice, not uniform deterministic path acquisition. A polynomial-size, polynomial-verifiable sound UNSAT path for every arbitrary CNF would imply NP=coNP. All child calls, discovery, replay, verification, source materialization, writable memory, complete output and universal strategy branches remain charged.

Conditional naive all-RB upper exponent max(1,1.195,.845+.35a) when local complete time is m^a; the 1.33 endpoint requires a<=97/70. At a=1.33, the cited older deterministic random-access SAT tradeoff excludes only b<0.2762629, not b=.5. All-input full-language restrictions cannot be promoted to promised T5 deletion witness bounds without model-preserving reductions.

## Independent controls and next dependency
The construction has four-cycles; it is NOT high-girth hardness. The ordinary graph has linear-size canonical syntax, and GF(5) cycle constraints make UNSAT recognition cheap. This is a global modular cheap shortcut and must remain a falsifier for future obstruction measures. Next: search source-uniform broader multi-terminal or high-girth intrinsic-critical row covers with verifiable negative derivations and paid discovery. Review existing TMR-2 /093 exact cycle syndromes before duplicating algebraic arguments.

Issue #3 previously reached its 2500-comment cap; preserve this verified handoff as evidence instead of asserting that an issue comment was posted. No agent, title, schedule, enabled/disabled state or manuscript/tracker was changed. P versus NP OPEN.
