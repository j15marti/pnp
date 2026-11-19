# TMR-5 current handoff | 2026-11-15 20:48 PST | WORST-CASE DERIVATION-COST BRIDGE REDTEAM /057

**Authority:** 2026-11-15 END_TO_END_AGENT_MANUSCRIPTS first; scheduled user directive (shared objective W_R(N)=max_{F UNSAT,|F|<=N} min_{pi} cost_R(pi); bridge B(R): SAT in P => W_R poly). TMR-5 = Independent Proof Red Team. Own main5 edited in place; prior handoff archived byte-exact at research/agents/tmr-5/archive/handoff_pre_2026-11-15_2048.md (blob 87253e1db50eac87333dc2c2152d0f862cc1dd6b). Peers' mains, retired trackers, historical main.tex, schedules untouched. **P versus NP OPEN.**

**Theorem A PROVED/EXACT (elementary), review OPEN:** if R has an unconditional superpolynomial lower bound L(R) (resolution, tree-like, Res(k), PC, Nullstellensatz, cutting planes, bounded-depth Frege: KNOWN THEOREMS), then B(R) <=> SAT not in P. The "weakest bridge" for such R IS the target; harder families for them cannot advance B(R). Pointwise transfer FALSIFIED: Tseitin-on-expanders is 2^Omega(n) for resolution yet O(n^3) by GF(2) elimination; PHP resolution-hard yet decided by counting. Min-derivation cost lower-bounds only R-shaped executions (DPLL/CDCL vs resolution). Free optimal-sequence knowledge is sound but does not touch this gap.

**Theorem B KNOWN (Cook 1975; Krajicek-Pudlak 1989), reproduced:** for R >= EF, B(R) <=> [SAT in P => some correct poly-time A has poly-size R-proofs of Sound_{A,n}]. Optimal R would make B(R) KNOWN but then B+L gives NP != coNP (stronger); optimal systems' existence OPEN (NE=coNE => optimal, E=NE => p-optimal).

**EXECUTED** CPython 3.11.18, deterministic: experiments/tmr/tmr5_derivation_bridge057.py (blob 787ef912db0062af081fde42ee2b022b335d70d9), raw results/raw/tmr/2026-11-15_2048_TMR5_DERIVATION_BRIDGE057_PY_RAW.json (blob e5c805d41313663abca4c78317c66a77278dba75). Odd Tseitin K4/K33/prism/Q3: min Res width 4/5/4/5 (init 3), min tree-like 55/151/95/255, GF(2) row XORs 5/11/9/20; PHP 3->2, 4->3; DPLL >= tree-like min; SAT control unrefuted. 19 assertions, 0 failures. COMPUTATIONAL only. Preflight script, LaTeX build (no pdflatex) NOT run.

**Gates:** DISJ PASS; relativization: oracle-free statements, any B(Res) proof is a P!=NP proof and inherits all barriers (OPEN); DTISP N/A; configuration counting upper-bound guard only. /341 FAIL, /386 RESTRICTED.

**Files:** main5_PNP_MACHINE_BOTTLENECK_REDTEAM.tex; research/agents/tmr-5/2026-11-15_2048_TMR5_WORSTCASE_DERIVATION_BRIDGE_REDTEAM057.md; experiment; raw; archive; this handoff. Branch ccr-1695bd63-dh8nvl (pushed; NOT merged to main, no PR).

**ONE NEXT LEMMA (for TMR-1 General SAT Lower-Bound Lead):** prove for EF/Frege that SAT in P yields an algorithm with short R-proofs of Sound_{A,n}, or restrict the target to a proved simulation class K and claim the bound for K only. Do not use Res/PC/CP/AC0-Frege as the bridge system. Track C Lean rebuild remains OPEN.

END_OF_HANDOFF::TMR5::2026-11-15_2048_PST
