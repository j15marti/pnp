# Shared directive: worst-case minimum derivation cost  W̄_R(N)

Recorded 2026-11-15 04:51 America/Los_Angeles from the stored prompt of a scheduled
Claude routine on this account. **This file is additive. It creates, disables or
reschedules no tasks, and it does not replace the TMR-1..5 allocation in
`research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md`.** It records
the shared target that the routine pursues each run, so TMR agents can consult it.
It does not require them to read it.

## Object

Use a multisign DAG hypergraph encoding of 3-CNF F. Let R be a fixed, sound, complete,
polynomial-time-checkable inference system over that encoding, with cost_R(π) the
fully charged size of a derivation DAG π: F ⊢_R ⊥. Define

    W̄_R(N) = max_{F ∈ UNSAT, |⟨F⟩| ≤ N}  min_{π : F ⊢_R ⊥}  cost_R(π).

The best derivation is given for free (nondeterministic choice). So W̄_R is the
Cook–Reckhow proof-length function of R.

## Priorities

1. A superpolynomial lower bound on W̄_R(N) for a fixed, sufficiently strong R.
2. The weakest sufficient bridge:  **SAT ∈ P ⇒ W̄_R(N) ≤ poly(N).**
3. Hostile controls: resolution, algebraic (PC/Nullstellensatz), parity (Res(⊕)),
   counting (cutting planes), circuit compression / extension variables, shared DAGs,
   and adaptive strategy switching.
4. Pointwise and worst-case simulation theorems are secondary.

## Status discipline (first audit: WCDC-0001)

- Priorities 1 and 2 together imply P ≠ NP. Neither is proved. **P versus NP remains OPEN.**
- If R has a known superpolynomial lower bound (resolution, cutting planes, PC,
  bounded-depth Frege), priority 2 for that R is *equivalent* to P ≠ NP. It is a
  reformulation, not a weaker step (WCDC-0001, Theorem 2).
- If R p-simulates Extended Frege, priority 2 is equivalent to this statement: for every
  correct polynomial-time SAT decider A, the correctness tautologies Corr_A have
  polynomial-size R-proofs (WCDC-0001, Theorem 3). This is the exact open arrow.

Living log: `research/agents/claude/wcdc/LIVING_LOG.md`.
