# Living log: worst-case minimum derivation cost and the bridge SAT∈P ⇒ W̄_R poly

Target: `W̄_R(N) = max_{F UNSAT, |F|≤N} min_{π: F ⊢_R ⊥} cost_R(π)`; primary bridge B3: `SAT∈P ⇒ W̄_R(N) ≤ poly(N)` for one R fixed in advance.
P versus NP remains OPEN. Statuses: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.

## 2026-11-15 09:51 PST — CERTIFIED-VERIFIER-B3-0001
Report: [`2026-11-15_0951_CLAUDE_CERTIFIED-VERIFIER-B3-0001.tex`](2026-11-15_0951_CLAUDE_CERTIFIED-VERIFIER-B3-0001.tex)
- **PROVED/EXACT (substance KNOWN, Krajíček–Pudlák style).** A fixed system `R_T` refutes F with ⟨e, y, 1^t, p⟩, where p is a T-proof of the Π1 soundness sentence Snd(e). The system is sound if T is consistent, polynomially checkable and complete, and it p-simulates EF.
- **B3 for R_T holds under `P=NP_T`:** some polynomial-time SAT decider whose UNSAT-soundness alone is T-provable.
- **Converse up to one reflection jump:** SAT∈P together with W̄_{R_T} poly gives `P=NP_{T+RFN_Π1(T)}`.
- **Remaining gap:** what is left of B3 is exactly `P=NP ⇒ P=NP_T` (OPEN).
- **Falsifier F2:** unit node cost makes R_T trivial (W̄ ≡ 1). Certified rules must be costed in bits.
- **Barrier F4 (conservation of difficulty):** making B3 provable forces R to be at least as strong as EF, so the lower-bound half becomes at least as hard as EF lower bounds (OPEN). Hypergraph-calculus lower bounds (e.g. LSPV-2/341) do not transfer.
- **Next:** CANDIDATE (c), a system strictly weaker than EF on an explicit family that still admits a family-restricted B3-style transfer.
