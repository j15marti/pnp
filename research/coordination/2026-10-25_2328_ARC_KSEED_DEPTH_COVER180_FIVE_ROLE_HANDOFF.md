# ARC-KSEED-DEPTH-COVER180 | LSPV-1 formal proof lead handoff
Date: 2026-10-25 23:28 PDT / 2026-10-26 UTC.
All five existing hourly tasks remain enabled at :00/:12/:24/:36/:48; no task/schedule changes. P versus NP and ARC-EDGE-90 OPEN.

## New result: sharp arbitrary-seed fixed-depth accounting frontier
Prerequisites are CONDITIONAL, not established: one fixed uniform all-input SAT guest A of time n^(K+o(1)), a uniform *complete and sound* all-UNSAT adaptive certificate grammar, actual named-compatible joins, per-parent n^(1/2+kappa+o(1)) children of size n^(1/2+o(1)), fixed depth L depending on K but not input length, eager O(polylog n) bit-generation cost and near-linear local work, and all remaining source, proof-description, recursion, failed-route and validation costs charged.

PROVED/EXACT arithmetic:
- Level-i actual node upper envelope exponent P_i=(1+2*kappa)(1-2^-i), encoded child length exponent 2^-i.
- Terminal volume exponent b_L=1+2*kappa*(1-2^-L).
- Terminal guest / whole declared eager ledger exponent c_L=1+2*kappa+(K-1-2*kappa)*2^-L, for K>=2 and zero extra per-bit exponent.
- van Melkebeek 2007 survey Thm 1.3, inspected at primary PDF page 2: coND exponent c and deterministic time d with tiny *same-machine* deterministic space n^e prohibited if (c-1)d<1 OR cd(d-1)-2d+1<0. For K>=2, frontier H(K)=1+1/K.
- A finite L with this ***certified bound*** strictly below H(K) exists iff kappa<1/(2K). Least L satisfies 2^L>(K-1-2*kappa)/(1/K-2*kappa). For kappa=0, 2^L>K(K-1). In particular K=10 requires L>=7 if kappa=0; kappa=.02 requires L>=8; kappa=.05 fails for this accounting. K=100, kappa=0 requires L>=14.
- A fixed positive kappa cannot certify all unknown polynomial K via this scheme. This is only a ledger barrier, NOT a lower bound on other SAT algorithms or a refutation of an alternative adaptive certificate.
- Additional source charge: root eager bit generator exponent 1+kappa+g, so the same strict budget requires kappa+g<1/K. A multiplicative terminal factor n^u yields limiting floor 1+2*kappa+u, so require 2*kappa+u<1/K. Root local work n^r requires r<1+1/K to certify strictness.

TWO INDEPENDENT OPEN GAPS: (1) no all-UNSAT low-volume certificate construction/coverage is proved; (2) the deterministic small-space seed required by Theorem 1.3 is NOT supplied by P=NP, which yields some unknown joint (K,K). Even a perfect coND certificate budget at K does not give an unconditional separation without a small-space transition. ARC/FLMV achievable-pair successor remains a separate all-input SAME-MACHINE obligation. The near-boundary 1.802 assumption is extra.

## Exact semantic control
PROVED/EXACT relation joins record all original-named shared variables. For index-set I, boundary S_I=(union V_i, i in I) intersect (union V_i, i outside I); R_I is the set of extendible assignments. Two successive true compatibility joins (four leaf blocks -> two pairs -> root) exactly reconstruct SAT. Ordinary proper 3CNF with all 8 sign clauses on x,y,z: UNSAT globally though four 2-clause blocks all SAT. Delete one clause: SAT globally and same four local SAT flags. Full relation join differentiates them, local labels do not.

COMPUTATIONAL: standard-library script seeded 202610252328 passed 2,276 exact rational and semantic assertions. 80 SAT and 80 UNSAT independent ordinary 3CNF roots, with four leaf relations and two genuine joins each; zero discrepancies against exhaustive truth tables. Every UNSAT control had 4 locally SAT blocks. These are finite semantics, NOT ordinary SAT-guest two-level recursive M22 reductions. Earlier Gate179 performed actual M22 child restorations independently; no new M22 claims here.

## Literature/scope and duplication
Primary PDF inspected: https://eccc.weizmann.ac.il/report/2007/099/download (page 2, Thm 1.3); Bathie-Williams ITCS 2024 https://doi.org/10.4230/LIPIcs.ITCS.2024.10 (NAND depth, not arbitrary circuits); FLMV JACM 2005. Read root main.tex, main13.tex, previous Gate179, Role 2 QPORT162, Role 3 TSEITIN125, Role 4 VOLUME124, Role 5 COVERAGE155, AGENTS/CODEX/skill. Gate179 already established coND polarity and weighted leaf inequality: no novelty claim for those. PNP_Circuit_Certificate_Continuation.pdf and source bundle remain absent in accessible filename search; no claims imported from them.

## Next concrete falsifiable targets
Role 2 (circuit/compiler): prove end-to-end indexed output bits including source sign -> fixed Cook verifier -> occurrence cloning -> Q15 and signed/monotone adapters; count repeated reads, addresses and actual emitted bits.
Role 3 (coverage): construct or falsify all-UNSAT certificate coverage with *total* certified branching factor kappa(K)<1/(2K), including non-affine hard controls, source-name compatibility and complete leaves; stage internal proof and generator.
Role 4 (FLMV/time-space): independently verify exact recursion and roots g,u,r, retained space, guest small-space premise; test whether all exponent pieces refer to same machine and initial encoding.
Role 5 (independent red team): audit strict depth inequality, exhibit alternate algorithms beyond this ledger, verify theorem premise / arbitrary-K space barrier, and keep executive OPEN.
Role 1: maintain source-exact DAG and investigate an arbitrary-K deterministic small-space transition rather than only near-boundary c=1.8018.

## Verified GitHub paths
- research/agents/lspv-1/2026-10-25_2328_LSPV-1_ARC_KSEED_DEPTH_COVER180.tex
- research/agents/lspv-1/2026-10-25_2328_ARC180_depth_frontier_repro.py
- research/agents/lspv-1/2026-10-25_2328_ARC180_depth_frontier_raw.json

PDF mirror in Library /PNP/ARC180; no peer-owned root edits. Independent peer acceptance pending.

END_HANDOFF::ARC-KSEED-DEPTH-COVER180
