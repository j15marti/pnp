# Living log: worst-case minimum derivation cost (W̄_R) program

Target: W̄_R(N) = max over UNSAT F (|F|<=N) of min over refutations π of cost_R(π); weakest bridge B3: SAT∈P ⇒ W̄_R ≤ poly(N). Strategy discovery is not charged. P vs NP remains OPEN. Append newest entries at the top.

## 2026-11-05 — CLAUDE/WORSTCASE-0001
- Report: research/agents/claude/2026-11-05_CLAUDE_WORSTCASE-0001.tex
- B1 ⟺ pointwise simulation of all trace systems R_A; ∃R∀A is the content (optimal-proof-system flavour); ∀A∃R is trivial.
- B3 for an R with known superpoly W̄_R is *equivalent* to P≠NP (a reformulation, not a weaker target).
- Known translation: PV ⊢ Corr(A) ⇒ poly-size EF proofs of size poly(|F|+T_A(F)). Sufficient route: EF superpoly ∧ (SAT∈P ⇒ ∃ PV-provably-correct poly A) ⇒ P≠NP. Both hypotheses OPEN.
- Literature: Krajíček–Pudlák optimal proof systems; Egidy–Glaßer STOC'25 / Egidy arXiv:2602.02294 (relativization limits, abstracts only); Pich–Santhanam arXiv:2312.08163.
- Next: is PV-provable UNSAT-side correctness forced by P=NP for some poly decider?

## Pointers to prior corpus (LSPV)
- LSPV-1/335 explicit-generator barrier; /395 uncomputable node profile; /418 source-branch audits ⇒ Resolution (restricted Haken anchor only).
- Hard-family red-team and time-space audit roles: see latest LSPV-2/3/4/5 reports; nothing here changes their statuses.
