# Shared worst-case derivation-cost directive (WCD-1) — 2026-11-05

**Additive reference.** Changes no schedules, agent count, or role ownership, and does not supersede the 2026-10-24 23:46 ALL-ARC/FLMV allocation; it adds a user-requested exploratory target. **P versus NP remains OPEN.** Nothing here is a proof.

## Object
For a fixed derivation system R (multisigned DAG-hypergraph inference system over 3-CNF; node = derived signed clause/hyperedge), with cost_R(π) = size / verification time / peak state of derivation π:

  W̄_R(N) = max_{F∈UNSAT, |⟨F⟩|≤N}  min_{π : F ⊢_R ⊥}  cost_R(π).

The best derivation is given for free (discovery is not charged; that can only help a lower bound on executing it).

## Priorities (user-stated)
1. Superpolynomial lower bound on W̄_R for a fixed, sufficiently powerful R.
2. Weakest sufficient bridge B(R): SAT ∈ P ⇒ W̄_R(N) ≤ poly(N).
3. Hard instances must survive resolution, algebraic (PC/NS), circuit-compressed, shared-DAG and adaptive strategy-switching reasoning.
4. Every run checks the literature for clues on the current obstacle.

## Roles (same five; no new tasks)
General SAT lower-bound lead; SAT-circuit reduction builder; hypergraph & proof certificates; time-space resource auditor; independent red team.

## Standing audit result (WORSTCASE-0001; `research/agents/claude/worstcase/`)
- "Min over derivations, free strategy" = nondeterminism: W̄_R is the proof-complexity measure of R.
- Bridge dichotomy: if W̄_R is already unconditionally superpolynomial (resolution, bounded-depth Frege, PC), B(R) is *equivalent* to SAT ∉ P (reformulation, not progress). If the lower bound is open (Frege, Extended Frege), B(R) says P = NP ⇒ R p-bounded, with no known route; a fixed-R lower bound alone never gives P ≠ NP.
- Only provable bridge form is reflective (T proves A decides SAT in poly time ⇒ T-proofs poly); unusable unconditionally.
- Living log: `research/agents/claude/worstcase/LOG.md` (append only).
