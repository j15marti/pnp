# Worst-case derivation-cost programme — living log

Shared directive (additive; changes no schedules, agent count, or other allocations).
Status of P vs NP: **OPEN**. Nothing below claims the lower bound or the transfer theorem.

## Objective (all five roles)

W̄_R(N) = max_{F∈UNSAT, |F|≤N}  min_{π : F ⊢_R ⊥}  cost_R(π)

Strategy discovery is not charged (the min is free/nondeterministic). Priority bridge:
**B_R :  SAT ∈ P  ⟹  W̄_R(N) ≤ poly(N).**  Secondary: pointwise / worst-case simulation theorems.
Roles: General SAT Lower-Bound Lead; SAT-Circuit Reduction Builder; Hypergraph & Proof Certificates;
Time-Space Resource Auditor; Independent Proof Red Team.

## Entry 2026-11-09 (first entry)

### Formal observations (status per AGENTS.md labels)

1. **KNOWN THEOREM (Cook–Reckhow 1979).** If R is a propositional proof system (poly-time verifiable,
   sound, complete) and cost = proof length, then "W̄_R(N) ≤ poly for some R" ⇔ NP = coNP.
   So "min over all derivations, strategy free" is exactly proof size; the free-strategy convention
   adds nothing beyond ordinary nondeterminism.
2. **PROVED/EXACT (dichotomy for the bridge B_R).**
   (a) If R has an *unconditional* superpolynomial lower bound (resolution: Haken; cutting planes,
   bounded-depth Frege, PC, …), then B_R is logically equivalent to "SAT ∉ P" (consequent is false).
   So B_R is *true* but *carries the whole of P ≠ NP*; it cannot be a weaker sufficient bridge for such R.
   (b) For B_R to be a genuinely weaker, independently provable statement, R must be strong enough
   to p-simulate traces of every polynomial-time SAT decider that could exist. Then the lower bound
   W̄_R superpoly is itself ≥ as hard as NP ≠ coNP-type statements (for Frege/EF it implies NP ≠ coNP).
   Consequence: **the bridge cannot be the easy half**; effort must go to the lower bound for a strong R,
   or to a *restricted-algorithm* version of B_R (see 4).
3. **CONDITIONAL (Cook translation, Krajíček–Pudlák).** If PV (or S¹₂) proves "M decides SAT in poly time"
   then EF has poly-size refutations of every UNSAT F. So B_EF holds for *feasibly-provably-correct*
   deciders; the gap for B_EF in general is exactly "P = NP via a decider whose correctness is not
   feasibly provable". Closing that gap is the real weakest-bridge question; it is related to optimality of EF.
4. **CANDIDATE restricted bridge (new target T-BR1).** Define B_R^prov: "SAT is decided in poly time by an
   algorithm whose correctness PV proves ⇒ W̄_EF poly". This is a KNOWN THEOREM (item 3). The converse
   direction needed for a lower-bound strategy is therefore: superpoly W̄_EF ⇒ no PV-provable poly SAT algorithm
   (unconditional *unprovability* of P=NP in PV — consistent with known conjectures, still OPEN).
5. **Multisigned DAG hypergraph.** A derivation is a DAG; "minimal reduced logical state" = minimal
   antichain/cut width over the derivation (clause-space / width-like measure), "minimal work" = size
   (or size×width time–space). Known relations: width⇒size (Ben-Sasson–Wigderson), space⇒size trade-offs
   in resolution. For R above resolution these measures are poly-bounded on the known hard families
   (PHP has poly EF/Frege proofs), so a *hard family for Frege* is the real missing object.
6. **Red-team flag.** Any family showing superpoly W̄ for resolution/CP/AC0-Frege does not transfer to
   Frege: circuit compression (extension variables) and shared DAGs break width/space arguments.
   Open hard-instance candidates must be tested against EF-simulation of the instance's natural short proof.

### Literature check (this run)
- Messner: P = NP ⇒ TAUT has a p-optimal proof system iff optimal acceptor exists (reported in the
  recent SPARSE-relativization paper, [arXiv 2602.02294](https://arxiv.org/pdf/2602.02294)); existence of
  optimal systems for TAUT is still open. Krajíček–Pudlák 1989: no optimal system ⇒ NE ≠ coNE.
  Relevance: sharpens item 3 — under P=NP, an optimal system exists, but not necessarily a *natural fixed* one.
- New lower bound (not Frege): superpolynomial size for tree-like semantic Frege with bounded line size
  ([arXiv 2604.28172](https://arxiv.org/pdf/2604.28172), [ECCC TR26-078](https://eccc.weizmann.ac.il/report/2026/078/)).
  Useful as a method (linear pseudo-measure) to test on line-size-bounded DAG versions; does not reach full Frege.
- Filmus–Pitassi–Santhanam: exponential AC0-Frege bounds for CNFs at growing depth ⇒ superpoly Frege
  (conditional route; unverified quantitative threshold from a secondary source).
  Suggested target T-BR2: quantify depth-d bound needed.

### Next targets
- T-BR1: formalise items 2–4 as a short LaTeX note with exact quantifiers (Lead + Red Team).
- T-BR2: FPS depth-threshold route (Hypergraph & Proof Certificates).
- T-BR3: audit whether the "multisigned DAG hypergraph state" measure is poly on PHP/Tseitin/random 3-CNF under EF simulation (Auditor + Red Team).

P versus NP remains OPEN.
