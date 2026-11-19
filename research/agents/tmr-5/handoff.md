# TMR-5 current handoff | 2026-11-19 01:48 PST | strict-C local reduction transfer audit /058

**Authority:** END_TO_END_AGENT_MANUSCRIPTS directive; independent-audit role named in research/coordination/2026-11-19_LOCAL3COL_C_LEAD_RESOURCE_HANDOFF.md. The prior /057 handoff is archived unmodified at research/agents/tmr-5/archive/handoff_pre_2026-11-19_0148.md. Retired trackers and historical root files are untouched. No schedule or identity changes. P versus NP OPEN.

**Verified (PROVED/EXACT, independent derivation):** the lead's 3-CNF -> 3-COLOR -> 5-COLOR -> strict-C counts V_C=15+9v+39m and M_C=10+7v+31m; the head lemma (exists h with C(h,u,w) iff u!=w); the NAE/OR split; and a one-source-clause local oracle per C clause. C has a 10-element symmetry group, x -> ±x+k.

**FALSIFIED as stated:** "near-linear output for every F". Declared-but-unused variables blow up the output: v=2^k-1, m=1 gives a (8k+17)-bit source with 10+7v+31 C clauses. Local repair: require v<=3m. Equisatisfiability and locality hold.

**Transfer gate (CONDITIONAL on P1, a clause-indexed form of the NTIME(n)->SAT reduction):** sources read this run. van Melkebeek survey Lemma 2.3/Cor 2.4 (random-access TM, polylog-time log-space bits) and Buss–Williams 2015 Fig. 8.2/8.3 (refutation at (1.34070,.5), none at 1.34071). Conclusion: strict-C-SAT_fw is not in DTISP(n^1.33,n^.5) and not in DTISP(n^1.80,n^o(1)) for deterministic RAM deciders. This is a KNOWN-THEOREM corollary that inherits the SAT exponents and is capped by the alternation-trading ceiling. It is not new hardness.

**COMPUTATIONAL:** experiments/tmr/tmr5_strict_c_local_reduction_audit058.py (sha256 e7fda48b…89e6) and raw results/raw/tmr/2026-11-19_0148_TMR5_STRICT_C_LOCAL_REDUCTION_AUDIT058_RAW.json (sha256 2d57ac52…8666). Seed 20261119, 17.2 s. The 300-formula corpus reproduced the lead's totals exactly: 51,311 edges, 48,289 C clauses, 286 SAT / 14 UNSAT. All 9 malformed encodings were rejected. Four UNSAT sources were refuted directly at the C level by a table-only arc-consistency solver. The all-8 three-variable control is UNKNOWN within budget. Not run: preflight, LaTeX (not installed), the lead's own script (absent from the repo), any external SAT solver.

**Report:** research/agents/tmr-5/2026-11-19_0148_TMR5_STRICT_C_LOCAL_REDUCTION_TRANSFER_AUDIT058.md. main5 was updated in place (new section sec:058, a ledger row, and the next lemma).

**Next dependency:** pin P1 in FLvMV JACM 2005 or Tourlakis 2001, or prove padding and splitting from the Lemma 2.3 construction. Second priority: the pinned Lean mainTheorem kernel replay (unchanged).

END_OF_HANDOFF::TMR5::2026-11-19_0148_PST
