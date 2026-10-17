# GATECORE-SIGMA3-1 | 2026-10-17 UTC | Circuit-SAT Sigma track

Status: PROVED/EXACT restricted theorem; COMPUTATIONAL 106475 assertions; conditional recurrence; P != NP OPEN.

IDEAS: trace commitment; solver-based Skolem search; challenge batching; Williams-style self improvement.
SEARCHED: main6.tex, FULLSKOLEM1, GATEAUDIT1, GUARDEDGAME13, Williams STOC 2024, FLMV JACM 2005, Santhanam-Williams SODA 2015.

THEOREM: For m>=1, take the constant-zero circuit g0=0, gi=g(i-1) for i=1..m, with output required to be 1. Proposed trace has constraints c0:t0=0, ci:ti=t(i-1), c(m+1):tm=1. All m+2 jointly contradict, but every proper subset S is satisfiable: choose an omitted j, set ti=0 before j and ti=1 from j onward (at j=0 all one; at j=m+1 all zero). Thus global exists-trace forall-check is false, whereas forall-subsets-of-size-at-most-k exists-trace per subset is true for EVERY k<=m+1. This invalidates replacing a globally committed Sigma2 trace with locally chosen Sigma3 responses. The Skolem response is just a missing index (O(log m) bits), so strategy counting does not give runtime hardness. The circuit itself is trivially solved by source propagation.

UNDER P=NP: For a fixed valid outer x, an arbitrary N^K-time N^L-space Circuit-SAT decider A yields a forall-y exists-z witness via at most N parent-size restricted SAT calls: charged time at most N^(K+1+o(1)), space at most N^(max(1,L)+o(1)). This is not the requested contraction and does not remove outer-witness acquisition cost.

Target recurrence K'=max(11/10,3/5+K/2), L'=max(1/2,L/2) has conditional fixed point (6/5,1/2); FLMV sufficient margin 1/90. No all-input hereditary transformation is proved.

TEST: m=1..12, all 32748 proper subsets, plus direct/global, easy equality strategies and exact fractions: 106475 checks; zero failures.
HANDOFF: require one source-bound commitment chosen before universal challenges, then charge acquisition, parent calls, child length, source reads, guest/ancestor buffers and recursion. Keep padding, affine and oracle-replay controls.
END_GATECORE_SIGMA3_1_2026_10_17
