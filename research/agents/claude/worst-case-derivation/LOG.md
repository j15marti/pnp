# Living log: worst-case derivation complexity routine

Objective: Wbar_R(N) = max_{F UNSAT, |<F>|<=N} min_{pi: F |-_R bot} cost_R(pi);
weakest sufficient bridge B(R): SAT in P => Wbar_R(N) <= poly(N).
P versus NP remains OPEN.

## 2026-11-15 12:50 PST — WCD-0001
- Report: `research/agents/claude/2026-11-15_1250_CLAUDE_WCD-0001.tex`
- Code / raw: `experiments/claude_worstcase/rt_reflection_collapse.py`,
  `results/raw/claude_worstcase/2026-11-15_1250_CLAUDE_WCD-0001_raw.json`
- PROVED/EXACT (repackaged KNOWN THEOREM, Cook 1975 / Krajicek-Pudlak 1989):
  fixed reflection system R_T (resolution + "T-proof of one-sided UNSAT soundness
  of M + clocked run"). Pointwise: w_{R_T}(F) <= K_M + O(t_M(F)) for every
  T-provably-sound M. Hence B(R_T) follows from the provable-soundness gap
  B^|-(T): SAT in P => some poly SAT decider has T-provable UNSAT-soundness.
- Unconditional consequence of a superpoly Wbar_{R_T} bound: no poly SAT decider
  is T-provably sound; also an Extended Frege lower bound (T >= PV).
- OPEN: B^|-(T); superpoly Wbar_{R_T}. For weak R (Res, CP, AC0-Frege) B(R) is
  equivalent to P != NP (corpus codex 2026-11-11 eq. 12, adopted).
- COMPUTATIONAL: Tseitin width vs Gauss cost, tiny sizes; 2 timeouts recorded.
- Gates: DISJ PASS; relativization OPEN; DTISP N/A; config counting PASS.
- Next: PV + feasible-witnessing version of B^|-(PV), or an oracle world with
  P = NP and no PV-provably-sound poly SAT decider.
