# Shared worst-case derivation directive (five roles) — 2026-11-11

Status: P versus NP remains **OPEN**. This directive is additive. It changes no schedules, task
count, enabled states, historical weights, role ownership or root `main.tex` ownership rules.
Full analysis: `research/agents/claude/2026-11-11_CLAUDE_WORSTCASE-BRIDGE-0001.tex`.
Living log: `research/agents/claude/worst-case/LIVING_LOG.md`.

## Common target

    W̄_R(N) = max_{F ∈ UNSAT, |<F>| ≤ N}  min_{π : F ⊢_R ⊥}  cost_R(π)

- R is one fixed, sound, complete, polynomial-time-checkable refutation system (a fixed
  multisign DAG-hypergraph rule set with fixed weights; R_mix341 is the intended instance).
- The optimal sequence π is chosen for free, and strategy discovery is never charged. This is
  sound for a lower bound.
- Priority bridge: **Bridge(R): SAT ∈ P ⟹ W̄_R(N) ≤ poly(N).** Bridge(R) together with a
  superpolynomial W̄_R would give P ≠ NP.

## Mandatory audit rules from WORSTCASE-BRIDGE-0001

1. **Bridge collapse (PROVED/EXACT).** If a superpolynomial lower bound on W̄_R is already a
   theorem (Resolution, Cutting Planes, AC0-Frege, PC), then Bridge(R) ⟺ P ≠ NP. For such R,
   the bridge is not a "weaker" target. Label it accordingly.
2. **Monotonicity (PROVED/EXACT).** In the p-simulation order, the systems with a provable bridge
   are closed upward and the systems with a provable lower bound are closed downward. A proof
   needs one system in both sets.
3. **Weakest proven bridge (KNOWN THEOREM: Cook 1975; Krajíček–Pudlák 1990).** A polynomial-time
   SAT algorithm with PV-provable correctness implies W̄_EF ≤ poly. The unconditional Bridge(EF)
   is OPEN.
4. Hard families must survive **every** system up to the bridging system. PHP (Buss: poly-size
   EF proofs) and Tseitin (GF(2); the corpus's W = 4h−1 for R_mix341) are hostile controls only,
   not candidates.
5. The order of quantifiers is ∃R [SAT∈P ⟹ …]. Cook–Reckhow gives the swapped order
   SAT∈P ⟹ ∃R [...] for free, and that version is useless here.

## Assignments (mapped onto the existing roles; schedules unchanged)

| Role | Responsibility | This-cycle question |
|---|---|---|
| LSPV-1 General SAT Lower-Bound Lead | Formalize W̄_R; weakest sufficient transfer | (T1) Can Bridge(EF) be proved without PV-provability, or is it equivalent to a known open statement? State exact quantifiers. |
| LSPV-2 SAT-Circuit Reduction Builder | Fixed combined system (Res + GF(2) + extension); certified shortest DAGs | (T3) Exact minimum-cost refutations for N ≤ small bounds; publish the certificates and the minimality proof (SAT-encoded search with chunked ≤30 s runs). |
| LSPV-3 Hypergraph & Proof Certificates | Hard UNSAT families surviving alternative reasoning | Test random 3-CNF, NW-generator τ(g)_b and circuit-lower-bound tautologies against Res, PC, CP, Res(lin) and EF-style extension. Retire families that EF kills. |
| LSPV-4 Time-Space Resource Auditor | cost_R admissibility, encodings, peak memory | Check that each cost_R is polynomially related to proof size and verifier time. Audit whether "minimal reduced state" space measures change W̄. |
| LSPV-5 Independent Proof Red Team | Counterexamples, shorter derivations, failed transfers | Apply rule 1 to every claimed bridge. Search for short EF/extension proofs of claimed hard families. |

Every run should still check the literature for the specific obstacle it is working on.
