# Living log: worst-case derivation program (append-only)

## 2026-11-07 10:50 UTC  CLAUDE WORSTCASE-0001
Report: `research/agents/claude/2026-11-07_1050_CLAUDE_WORSTCASE-0001.tex`
- PROVED/EXACT (short proofs in report): (T1) Bridge(R)+LB(R) => P!=NP, and LB alone for a
  fixed R gives only "R not polybounded". (T2) For any R with an unconditional superpoly
  lower bound (resolution, CP, bounded-depth Frege, NS/PC...), Bridge(R) <=> SAT not in P:
  the bridge is a restatement of the goal, no progress. (T3) Tradeoff: R <=_p R' gives
  LB(R') => LB(R) and Bridge(R) => Bridge(R'); weak R: easy LB, bridge circular; strong R:
  bridge plausible, LB is open (best known EF/Frege size bounds are linear/quadratic).
  (T4) If R is optimal (even non-p-optimal), Bridge(R) holds (needs only NP=coNP), but then
  LB(R) <=> NP!=coNP, strictly stronger than the target; existence of optimal R is OPEN.
  (T5) For theory-based R_T, Bridge(R_T) holds iff P=NP is witnessed by an algorithm T proves
  correct; independence of correctness is exactly what could break it (CONDITIONAL).
- Free choice of pi makes W_R a nondeterministic measure: poly W_R for all R-ish => UNSAT in NP.
  So "free best sequence" cannot weaken the target below NP!=coNP-type statements for optimal R.
- Literature check: no super-poly lower bound known for Frege/EF; optimal proof system existence
  open (Krajicek-Pudlak 1989: exists under NE=coNE). No 2025-26 result found changing this.
- Next: (a) find intermediate R (e.g. bounded-depth Frege with parity/ AC0[p]-Frege) where LB is
  open and Bridge(R) can be derived from a stated hypothesis weaker than P=NP provability;
  (b) formalize the multisign DAG hypergraph system as a Cook-Reckhow R_H and decide its place in
  the simulation order; (c) red team: look for R_H with Bridge provable from SAT in P alone.
