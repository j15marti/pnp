# TMR-3 direct-request speedup follow-up | 2026-11-15 11:10 PST

Additive DRAFT. No schedules, root trackers, main.tex, ownership or canonical historical handoffs changed. The newer SAT-compression directive remains governing; this Allender follow-up answers the user's explicit request and is a supporting checkpoint/time-space investigation. P versus NP OPEN.

## Verified arithmetic
For m=k-1>=1 and b=3/2, replace d=1+1/(4m) by d=1+2/(5m). Binomial/series proof: d^m<97/65<3/2, with strict exponent gap >1/130. This increases d-1 by 60 percent for the same k, not runtime by 60 percent. No numerical k or gamma established.

## Candidate requiring independent review
FK: one fixed K suffices for PrTiSp(n^alpha,n^sigma) subset LCH_K whenever fixed rational alpha>1, 0<sigma<1, alpha+sigma<2. Proposed construction stops at O(n)-time counting leaves, uses exact count-bit predicates in LCH_2, and one multiplicity-preserving checkpoint sum-product layer with O((T/n)(S+log T+log n)) label bits. Remaining gates: compatible source initialization/access; uniformly generated threshold arithmetic; K independent of exponent pair. NOT promoted as a theorem.

## Conditional implication, algebra checked
Assuming FK, set delta=1-sigma, d=1+delta/[8(K-1)], b=1+delta/4. Padding stays inside the one-layer region and d^(K-1)<b. Allender's collapse and time hierarchy then contradict the assumed simultaneous LCH_2 solver. After completeness slack, candidate MajMajSAT exclusion has time n^(1+c*delta), space n^(1-delta), c=1/[32(K-1)]. For the prior one-query virtual compiler, conditional forbidden region simplifies to eta<1 and theta+c*eta<1+c. FK and the exact SAT compiler remain OPEN.

## Evidence and files
71,288 exact finite assertions, zero failures; 3,969 synthetic exponent pairs; 22,363 threshold-count pairs; 120 layered graphs. Seed 20261115. Finite status COMPUTATIONAL. No physical machine compiler or actual circuit depth K tested.

- Report: research/agents/tmr-3/2026-11-15_1110_TMR3_ALLENDER_SPEEDUP_FOLLOWUP.md
- Code: experiments/tmr/tmr3_allender_speedup_followup.py
- Raw: results/raw/tmr/2026-11-15_1110_TMR3_ALLENDER_SPEEDUP_FOLLOWUP.json

Report/code/raw read back with matching full Git blob hashes. Full checkout preflight not executed; oversized main.tex and proof2 bodies unavailable. TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE.

TMR-1/4: independently verify FK's hierarchy-level and circuit-wiring proof, not just exponent arithmetic. TMR-5: attack arbitrary starting configurations, exact threshold ties, local source access, and K uniformity. Preserve exact path multiplicities; weak sampled PP calls are not exact oracle answers. /341 FAIL as full authority; /386 RESTRICTED.
