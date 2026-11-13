# CLAUDE living log: worst-case derivation functional W̄_R(N)

Shared target (scheduled-routine directive): W̄_R(N) = max over UNSAT F with |F| ≤ N of min over R-derivations π of cost_R(π),
plus the bridge B_R: SAT ∈ P ⇒ W̄_R(N) ≤ poly(N). Statuses use the project vocabulary. **P versus NP remains OPEN.**
This log is additive. It changes no schedules, roles, allocations, or root `main.tex` ownership regions.

## 2026-11-13 09:00 PST — WR-BRIDGE-0001
Report: `research/agents/claude/2026-11-13_0900_CLAUDE_WR-BRIDGE-0001.tex`
- PROVED/EXACT: if a superpolynomial W̄_R is already a theorem (resolution, cutting planes, polynomial calculus, bounded-depth Frege), then B_R is equivalent to SAT ∉ P. For those systems, proving the "weakest bridge" is the same as proving P ≠ NP.
- KNOWN THEOREM (Cook 1975; Krajíček–Pudlák 1989): B_EF holds whenever SAT ∈ P is witnessed by an algorithm whose soundness is PV-provable. This duplicates LSPV-1/357. The open residue is true but unprovable soundness.
- Trichotomy of fixed systems R: (i) lower bound known, so the bridge is a reformulation; (ii) R is EF or stronger, so the bridge holds for provably sound algorithms and the lower bound is open; (iii) R lies in between, so both are open.
- FAILED TRANSFER: the Krajíček–Pudlák route (E = NE gives a p-optimal system) produces a system that depends on the hypothesis. It does not give a fixed R.
- COMPUTATIONAL: exact minimum tree-like resolution sizes, with the derivation sequence chosen freely: PHP 21/85; Tseitin K4/K3,3/Petersen 55/151/639; random 3-CNF with n ≤ 12 at most 45. Raw data: `results/raw/claude_wr/`.
- NEXT: class (iii). Is there a polynomial-time SAT algorithm whose soundness is provable in VTC^0 or VNC^1? If so, the Cook–Nguyen correspondence gives a polynomial TC^0-Frege or Frege bridge.
