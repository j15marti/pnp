# Living log: worst-case minimum derivation cost and the B3 bridge (Claude routine)

Shared objective: W̄_R(N) = max over UNSAT F with |<F>| ≤ N of min over R-refutations π of cost_R(π).
Weakest sufficient bridge: B3_R : SAT ∈ P ⟹ W̄_R(N) ≤ poly(N).
Status labels follow AGENTS.md. **P versus NP remains OPEN.** This log is append-only; newest entry last.

| When (PT) | Run | Result | Status |
|---|---|---|---|
| 2026-11-13 06:48 | [B3-WRONGPROOF-0001](2026-11-13_0648_CLAUDE_B3-WRONGPROOF-0001.tex) | Rewrote B3 for Extended Frege (EF) as an exact equivalence using Fleming–Grosser–Pitassi–Robere (ECCC TR26-109, 2026), Thm 5.2: B3_EF ⟺ [SAT∈P ⟹ EF p-simulates ⟨EF, WrongProof_{P_A}⟩], where P_A is the proof system "EF or A rejects". It suffices that WrongProof_{P_A} is EF-provably in FP (their Prop 3.8). **Barrier:** any B3 proof that uses only "the search problem is in FP" would prove G1 ≤_p EF, which is open and believed false. A bridge must therefore use provable correctness of the SAT algorithm or structure specific to SAT. | PROVED/EXACT corollary of a known theorem (one encoding convention still needs a peer check); barrier is conditional on G1 ≰_p EF; B3 and lower bound OPEN |

## Open arrows (current)
- B1/lower bound: superpolynomial W̄_R for some R ≥_p EF — OPEN (no superpolynomial EF lower bound is known).
- B3_EF — OPEN; reduced to EF-simulating ⟨EF, WrongProof_{P_A}⟩ (see above).
- For any R with a known lower bound (Resolution, Cutting Planes, bounded-depth Frege), B3_R ⟺ SAT ∉ P (LSPV-1/398), so B3 there just restates P ≠ NP and is not progress.
