# Living log: worst-case derivation complexity W_R(N)

Status of P vs NP: **OPEN**. Nothing below is a lower bound; entries are labeled per AGENTS.md.

## Entry 2026-11-10 (scheduled run 1): the bridge is a statement about R, not about SAT

Conventions. R is a Cook-Reckhow system: a poly-time map f_R from strings (proofs) onto TAUT/UNSAT
(a proof contains its formula, so |F| <= poly(|pi|)); cost = bit size of pi (DAG size). W_R as in DIRECTIVE.md.

**Lemma 1 (search for free under P=NP; KNOWN, elementary).** If SAT in P, then for every R and polynomial p, a
refutation of F of size <= p(|F|) can be found in time poly(|F|) whenever one exists
(the set {(F,1^m): F has an R-refutation of size <= m} is in NP; use search-to-decision). PROVED/EXACT.

**Proposition 2 (bridge <=> p-optimality).** Assume SAT in P. For a Cook-Reckhow system R, TFAE:
(a) W_R(N) <= poly(N); (b) R p-simulates every Cook-Reckhow system Q.
(b)=>(a): R_M := {proof = F, accepted iff M(F) rejects}, M a poly-time SAT decider, is a Cook-Reckhow system with
proofs of size |F|; R p-simulates it. (a)=>(b): given a Q-proof pi of F, |F| <= poly(|pi|); by Lemma 1 compute an R-refutation
of size poly(|F|) <= poly(|pi|). PROVED/EXACT (this is Krajicek-Pudlak style folklore; no novelty claimed).

**Corollary 3 (what the weakest bridge actually is).** For fixed R: [SAT in P => W_R <= poly] <=> [P=NP => R is p-optimal].
So the bridge is a property of R alone. Strategy-discovery cost plays no role: it is exactly what Lemma 1 supplies for free
in the hypothesis world, and the min in W_R never charges it in the lower-bound world. PROVED/EXACT.

**Corollary 4 (trap for weak R).** If R has an unconditional superpolynomial lower bound (resolution, bounded-depth Frege,
polynomial calculus, cutting planes, Res(lin), ...), then the bridge for R is *equivalent to* P != NP, hence cannot be a
weaker intermediate step. It is only useful for R with no known superpolynomial lower bound (EF and stronger, e.g. an
extension-augmented R_mix341). PROVED/EXACT (an implication with false consequent is the negation of its hypothesis).

**Tradeoff (CANDIDATE framing).** Cost notions that make the bridge trivial (cost = running time of an arbitrary SAT algorithm, i.e.
derivation = computation) make "W_R superpolynomial" a restatement of SAT not in P (reformulation, cf. world-ledger remark). Cost notions with
poly-time-checkable derivations make the bridge equal to p-optimality of R, whose existence for any R is open (even
relative to oracles, independent of PH collapse: Egidy, arXiv:2602.02294). A genuine proof needs an R strictly between.

**Where the bridge is known (CONDITIONAL).** Cook's translation: if some poly-time M decides SAT and PV (equivalently S^1_2)
proves "M's UNSAT answers are sound" (a Pi^b_1 statement), then EF has poly-size refutations, so Bridge(EF) holds on that branch.
Gap: P=NP gives Levin search, which certifies only the satisfiable side; the unsatisfiable side needs the soundness of M, which is the NP vs coNP asymmetry.
Weakest sufficient transfer theorem, restated: **T\***: P=NP => EF (or a fixed extension R_mix+ext) is p-bounded; sufficient: any
unprovability-free argument that some correct decider's UNSAT answers are EF-verifiable. OPEN.

**Literature check.** Krajicek-Pudlak: p-bounded system exists iff NP=coNP; p-optimal existence open. Egidy 2026 (arXiv:2602.02294):
relativized independence of (p-)optimal systems from PH collapse. arXiv:2506.16956 v2 (2026): Proof Analysis Problem is NP-complete for EF (in P
for resolution); relevant to Lemma 1-type search costs and to red-team checks. Alekseev, Theory of Computing 22 (2026): PC with extension rule needs
exponential size for the binary value principle (a lower bound for a system simulating Res(lin), still below EF). No 2026 result found resolving EF
bounds. Transfer type: Cook translation = directly transferable theorem; Egidy = barrier (relativized) not a proof tool.

**Assignments for next runs.**
1 Lead: decide whether Bridge(EF) follows from P=NP via some non-provability route, or find the relativized/oracle model where it fails (sets expectation: cannot be proved without new ideas).
2 Builder: define the fixed combined system R_mix+ext and certify shortest DAGs for small instances (peitl/short-proof style SAT encoding), reporting exact min sizes.
3 Hypergraph/certificates: candidate hard UNSAT families, tested against R_mix341 mixed clause/XOR evidence and extension; record which known lower bounds they inherit.
4 Auditor: cost model for derivation size vs time-space of the verifier; confirm Lemma 1 overhead is polynomial and peak space bounds.
5 Red team: attack Corollary 4's scope (is every listed system's lower bound unconditional?) and Proposition 2's convention that proofs contain their formula.

No code or data produced this run. Not a P vs NP result.
