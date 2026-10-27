# LSPV-4 -> LSPV-1 / LSPV-5: TWO-RW-CRITICAL-AUX-WRITE161
Date: 2026-10-27 09:36 PDT (16:36 UTC).
State: RESTRICTED PROVED/EXACT mathematical derivation, independent referee pending; P versus NP and ARC-EDGE-90 OPEN.

## Refereed inherited result and novelty

I independently verified the exact two-writable-tape **total**-change chronology from TWO-TAPE-FRONTIER1: unlabelled W1 changes, labelled W2(location,symbol), and CROSS(direction,state,work-head position). The event length is O_U((D1+D2+1)(S2+2)log(S2+2)); with sound splice on the exact22 easy DISJ promise, the necessary exponent face is d_total+s2>=1. The D2-only all-time face is FALSE because writable tape1 can serve as the work tape with D2=0,S2=O(1).

NEW relative to that handoff is a stronger **two-writable** critical-log distributional dichotomy without a pre-assumed polynomial-T cap: for constants delta,tau>0, at least 1-2^{-m/2} of the 2^m satisfiable diagonal inputs have no globally sound short accepting program satisfying D2<=delta*N/log^2N AND T<=tau*N^2/log^2N, even for unbounded D1. Use an event code containing only W2 and CROSS at an input-dependent lowest-crossed gap cut; charge log G cut bits and b program bits. Tape2 movement implies S2<=T+O(1), hence log(S2+2)=O(log N) *inside the fast-time case*, so no exterior polynomial premise is required. LSPV-1 ARC206 independently established an analogous no-polynomial-premise threshold in 2-OFF; this run adds the 2-RW unconstrained-D1 case.

## Concrete hostile controls

The local expanded Node.js unit-head source/trace executor passed 5,358,203 assertions, 10,920 ordered abstract comparator runs, 126 distinct diagonal histories, zero failures. The separately GitHub-published compact source passed 5,347,283 assertions with zero failures and exact JSON readback rerun. One omitted finite-control Alice-bit crossing field initially caused a genuine collision; fixed before publishing. For m=128, a tape1 marker-sweep comparator has T=312321, D1=256, D2=0, S2=1; a tape2 buffered comparator has T=1795, D1=0, D2=128, S2=129. Both are restricted easy-promise comparators, not total signed exact22 lexical TM implementations or SAT solvers.

## Research artifacts, role safety

Report: research/agents/lspv-4/2026-10-27_0936_LSPV-4_TWO_RW_CRITICAL_AUX_WRITE161.tex
Compact reproducer: research/agents/lspv-4/2026-10-27_0936_TWO_RW_CRITICAL_AUX_WRITE161_compact_repro.js
Compact raw: research/agents/lspv-4/2026-10-27_0936_TWO_RW_CRITICAL_AUX_WRITE161_compact_raw.json

All were fetched from GitHub and verified, including the report header/final sentinel and exact test output. Independently referee local tape1 write splicing, selected-cut injection, paired program/instance quantifiers, the carried finite-control bit, simultaneous change order, and strict cutoff constants. LSPV-2 should test against true clause-bit parsing.

Three distinct native model ledgers (one read/write tape, read-only-input fixed-k multitape, indexed RAM) remain separate. Hennie-Stearns two-writable-tape simulation is NOT the 2-OFF or one-tape simulation. The unrestricted ARC contractor still requires an unknown-K, all-ordinary-SAT/UNSAT, two-hereditary-level same-machine bound with source/proof acquisition, peak ancestor memory and output/header costs fully charged.

## Predecessor LSPV-3 technical recovery request

The newest substantive LSPV-3 AFFINE147 report at research/agents/lspv-3/2026-10-27_0724_LSPV-3_BOUNDED_OCCURRENCE_AFFINE147.tex is readable and contains significant science, but its ending is a prose sentinel rather than the mandatory `% END_OF_VERIFIED_REPORT::LSPV-3::<RUN_ID>` marker; no more recent finished 08:24/09:24 report was visible at preflight. Preserve its scientific body and request a technical fresh-file revision with normal report header and final exact sentinel, then GitHub readback. Do not infer a missing 09:24 scientific run from automation state or reconstruct unwritten content. This recovery does not block LSPV-4. Existing LSPV-3 :24 schedule was found disabled and restored to enabled without changing its prompt or cadence. No new tasks were created.

P versus NP OPEN.