# Living log — worst-case minimum derivation cost  \(\overline W_R(N)\)

Shared objective (scheduled Claude routine):
`W̄_R(N) = max_{F ∈ UNSAT, |F| ≤ N} min_{π : F ⊢_R ⊥} cost_R(π)`, with the weakest sufficient bridge
`SAT ∈ P ⟹ W̄_R(N) ≤ poly(N)`. Append-only. Status labels follow AGENTS.md. **P versus NP remains OPEN.**

| Item | Status | Source |
|---|---|---|
| Min over derivations is a valid lower-bound strategy; it makes W̄_R a nondeterministic (proof-complexity) measure | KNOWN THEOREM (Cook–Reckhow) | WCDERIV-0001 |
| Fixed explicit system R_T (Resolution + T-certified clocked verifiers) is sound assuming only Con(T) | PROVED/EXACT | WCDERIV-0001 Lemma "R_T is Cook–Reckhow" |
| Bridge(R_T) holds for every poly-time SAT algorithm with T-provable soundness | PROVED/EXACT | WCDERIV-0001 Thm "fixed-system bridge" |
| R_T p-simulates Res, CP, PC, Frege, EF ⇒ lower bound on W̄_{R_T} ⊇ EF lower bound | PROVED/EXACT (packaging of Krajíček–Pudlák) | WCDERIV-0001 Thm "price of the bridge" |
| If W̄_R superpoly is already known (Resolution), Bridge(R) ⟺ P ≠ NP — no reduction in difficulty | PROVED/EXACT | WCDERIV-0001 Thm "bridge collapse" |
| Signed-parity / Tseitin hypergraph families as sole hardness carrier | FALSIFIED/RETIRED (easy for PC/F2, Frege; quasipoly CP) | WCDERIV-0001 §2 |
| Provability gap: SAT∈P ⟹ some poly SAT algorithm with T-provable soundness | OPEN (best bridge target) | WCDERIV-0001 |
| Superpolynomial lower bound on W̄_{R_T} | OPEN (≥ EF lower bounds) | WCDERIV-0001 |

## Entries

### 2026-11-14 23:51 PST — WCDERIV-0001
Report: `research/agents/claude/2026-11-14_2351_CLAUDE_WCDERIV-0001.tex`.
Result: exact three-regime classification of the bridge (known-hard weak R ⇒ bridge ≡ P≠NP;
R ⊇ R_T ⇒ bridge free for T-provably sound algorithms but lower bound ⊇ EF; intermediate ⇒ no mechanism).
Literature check: no new Frege/EF superpolynomial lower bound in 2025–2026 (checked AC0[p]-Frege ITCS'26,
EF proof-analysis NP-completeness arXiv 2506.16956, ⟨EF,R⟩ ECCC 2026/109).
Next: relate the provability gap to known statements (Krajíček, *Proof Complexity* 2019); relativized
oracle with P=NP but every R_T^O superpolynomial; test hard 3-CNF candidates against F2/CP/Frege controls.
