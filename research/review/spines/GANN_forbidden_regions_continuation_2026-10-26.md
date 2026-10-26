# GANN forbidden regions: strengthened proof-system audit
26 October 2026

## Theorem A: universal polynomial computation defeats any fixed restricted proof lower bound as an automatic execution lower bound
Let P be a Cook-Reckhow refutation system. If P=NP, a deterministic polynomial-time SAT decider D exists. The decision procedure need not produce P-refutations. Therefore an exponential lower bound for P on a formula family cannot, without a separate extraction theorem, exclude D. In fact, for any polynomial-time recognizable family of UNSAT formulas, a uniform algorithm can reject that family in polynomial time and use exhaustive SAT search elsewhere, even if P-refutations of the family are exponentially long.

## Theorem B: polynomially bounded sound and complete certificates are equivalent to NP=coNP
If every UNSAT formula admits a polynomial-length string verifiable in deterministic polynomial time as a proof of unsatisfiability, UNSAT belongs to NP, so NP=coNP. Conversely, NP=coNP yields such a verifier for UNSAT. This does not imply P=NP. Thus an all-proof-systems superpolynomial certificate lower bound would be stronger than a lower bound against any particular PC/CP system and would establish NP != coNP, hence P != NP.

## Theorem C: no communication superpolynomial lower bound under unrestricted centralization
An explicit N-bit input split between two parties can be sent in at most N bits to one party, after which that party computes the function. Therefore any claim that *total* communication must be superpolynomial in N is false in a model with arbitrary local computation. To obtain a meaningful tradeoff restrict rounds, local work, space, or partition, and charge all input movement.

## Theorem D: exact algebraic rank does not force hard computation
The compatibility matrix of equality on m bits is the 2^m by 2^m identity, rank 2^m over any field. Nevertheless equality is decided by m bit comparisons, and the associated XOR equations are handled by GE. Rank must be tied to a representation and a mandatory protocol before it can yield a computational bound.

## Candidate proof spine
1. Take the sparse graph-colouring affine + 2-CNF compatibility family, with one XOR parity-odd constraint per vertex and binary at-most-one and edge-conflict constraints.
2. Use the published all-field PC degree lower bound and a precise polynomial-expansion simulation of any added proof shortcut to inherit exponential explicit-monomial proof size.
3. Add proof capabilities incrementally: counting/CP, polynomial extension variables, compact arithmetic circuits, and eventually arbitrary polynomial-time semantic preprocessing.
4. At every enlargement either prove a cost-preserving simulation into the prior proof system or exhibit a short counterexample proof, and classify the escape mechanism.
5. In parallel, seek a uniform all-input transformation of arbitrary SAT deciders with a *simultaneous* time-space recurrence inside a known forbidden region. This is the separate unproved universal gate.

## Essential warning
Adding all polynomial-time preprocessing, including a hypothetical SAT decider if P=NP, to a proof searcher destroys any direct proof-size-to-runtime implication. There is no demonstrated universal extraction of PC, CP, or other restricted refutations from arbitrary SAT computations. The current result is a restricted proof-complexity theorem, not P != NP.

## Next tests
- Formalize 2-SAT shortcut expansion with explicit antecedent clauses and size accounting.
- Check whether GE shortcut permits only linear combinations of *already derived polynomial rows*, rather than hidden affine consequence extraction.
- Test counting shortcuts on subset-cardinality formulas where PC is exponentially hard but CP is short.
- Track a Pareto vector of time, space, proof length, proof depth, total probes, and access rounds for the same realization.
