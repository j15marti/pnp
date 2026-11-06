# Shared worst-case derivation-cost directive (created 2026-11-06)

Status: P versus NP remains OPEN. This directive is a research target, not a claim.

## Object
Multisign DAG hypergraph H_F for a CNF F: vertices = signed clauses/formulas (sign in {+,-,0,...}),
hyperedges = inference steps of a FIXED rule set R (multi-premise -> conclusion). A derivation of bottom is a
sub-hypergraph (hyper-DAG, shared nodes) rooted at bottom. cost_R(pi) = (work = total bit-size of nodes+edges,
space = peak pebbles / live width). "Minimal reduced logical state" = irredundant (no removable edge) derivation.

  W_R(N) = max_{F in UNSAT, |F|<=N}  min_{pi : F |-_R bottom} cost_R(pi)     (strategy search is NOT charged)

## Agent roles
1. General SAT Lower-Bound Lead; 2. SAT-Circuit Reduction Builder; 3. Hypergraph & Proof Certificates;
4. Time-Space Resource Auditor; 5. Independent Proof Red Team.

## Fixed facts (see research/worstcase/2026-11-06_WCDC-0001.tex)
- Free strategy choice = nondeterminism: W_R is a coNP-side proof-size measure (Cook-Reckhow).
- Bridge B(R): SAT in P => W_R <= poly. For any R with an unconditional superpoly W_R, B(R) <=> P != NP (tautological).
  So the bridge is informative only for R with no known lower bound (Frege, EF, ...), and there it needs a *structural* simulation theorem.
- Weakest non-tautological sufficient hypothesis currently known: a poly-time SAT algorithm whose correctness is
  provable in PV/S^1_2 gives poly EF refutations (Cook 1975; Krajicek). Provability, not truth, is the gap.
Read the log: research/worstcase/LIVING_LOG.md. Append, never rewrite.
