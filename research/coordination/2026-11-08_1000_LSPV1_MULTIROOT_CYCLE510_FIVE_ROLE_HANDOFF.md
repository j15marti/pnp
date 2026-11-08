# LSPV-1/510 five-role handoff: exact multi-root cycle-excess accounting
**2026-11-08 10:00 PST | Route B lead | PROVED/RESTRICTED | P versus NP OPEN**

**Affected tracker:** proposed new [P2-L1-510], refining [P2-L1-509], [P2-F13], older single-root [P2-B12]. **Unchanged OPEN:** [P2-D1] native R_mix341 grammar, [P2-C3] full mixed transfer, [P2-B1] superpolynomial all-rule proof minimum, [P2-B2] noncircular same-R B3; [P1-01], [P1-03], [P1-04] Route A.

A pruned source-explicit context-free proof DAG with m source vertices, q binary-or-smaller paid inference vertices, e premise incidences and c weak components has exact nonnegative decomposition
$$
q=m-c+\mu+\delta,\quad \mu=e-(m+q)+c,\quad \delta=2q-e.
$$
This extends the previously known one-root accounting of LSPV-1/469 to the **three-goal** /509 structure. For the 16 indispensable source facets, c=1, and strict binary Resolution delta=0. Every legal proof must satisfy q=15+mu. The known /507 Resolution proof has q=19, mu=4 and weighted-unit span 4. The /509 NONLEGAL abstract merge graph has q=15, mu=0, span 8. Thus a hypothetical <=18-node Resolution proof must have mu<=3, but none has been ruled out. Exact ordinary Resolution minimum remains 15..19.

**LSPV-3:** verify typed/source-authenticated history before borrowing the identity into R_mix341; extra zero-cost premises/definitions or multi-premise rules invalidate blind binary counting. **LSPV-5:** search actual *legal* Resolution DAGs of cycle rank <=3, respecting all three goals, or prove a syntactic obstruction. Avoid calling the abstract graph a proof. **LSPV-2/4:** consider work-versus-span and source-reference costs solely as restricted controls, not all-input FLMV evidence.

Artifacts: research/agents/lspv-1/2026-11-08_1000_LSPV1_MULTIROOT_CYCLE_BUDGET510.md; experiments/arc/lspv1_510_multiroot_cycle_budget.cjs (SHA-guarded GitHub readback and V8 replay PASS); results/raw/arc/2026-11-08_1000_LSPV1_510_MULTIGOAL_CYCLE_RAW.json. Independent local Python checks also pass. Do not change historical rules/weights, task IDs, titles, schedules, enabled states, role ownership or two Route A/three Route B allocation.

Already established B3 clocked-system countermodel [P2-B6]/LSPV-1/462 was rediscovered during exploratory checking and deliberately NOT republished as a new result. The essential remaining transfer for B3 has not advanced. **P versus NP remains OPEN.**
