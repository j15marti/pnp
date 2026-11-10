<!-- CLAUDE WC REPORT::WC-0001::2026-11-10 -->
# WC-0001: Is the bridge SAT in P => Wbar_R poly(N) trivial, circular, or genuine?
Status: reasoning only, nothing computed. P vs NP OPEN. Labels as marked.

## Model of the user's idea
A multisigned DAG hypergraph state S is a set of signed clauses (hyperedges). A move is a sound rewrite S -> S'. The derivation pi is a DAG of states ending in bot. Its cost is total work, with peak state size as the space axis. Special cases are known:
- Resolution: size, width and clause space (Esteban-Toran; Atserias-Dalmau: width <= space) [KNOWN THEOREM].
- Time-space trade-offs at fixed space (Ben-Sasson-Nordstrom; survey: Nordstrom arXiv:1307.3913) [KNOWN THEOREM].
- The free-search convention makes Wbar_R a nondeterministic cost. A lower bound for a poly-time-verifiable R is a proof-complexity bound, not a time bound.

## Lemma 1 (bridge triviality) [PROVED/EXACT]
Let R have a proved superpolynomial lower bound, i.e. Wbar_R(N) is not poly(N). Then (SAT in P ==> Wbar_R poly) is equivalent to SAT not in P, i.e. to P != NP.
Proof: the consequent is false, so the implication is equivalent to the negation of its antecedent.
Examples: Resolution (Haken; Urquhart; Chvatal-Szemeredi), cutting planes (Pudlak), constant-depth Frege (Ajtai; Bellantoni-Pitassi-Urquhart; Krajicek-Pudlak-Woods).
Consequence: proving the bridge for such an R amounts to proving P != NP. A bridge that is only provable for such R must use a hypothesis that already carries SAT-hardness. No progress comes from them.

## Lemma 2 (circular trace system) [PROVED/EXACT]
Let T_M be the system whose derivations are accepting runs of a fixed machine M. If M is a correct SAT decider, then Wbar_{T_M} poly iff M runs in polynomial time on UNSAT inputs. This system makes the bridge trivial for M itself, but the lower bound for T_M is the original problem, so it is a reformulation only.

## Theorem 3 (the genuine non-circular form of the bridge) [KNOWN THEOREM (Cook 1975; Krajicek-Pudlak), applied here as CONDITIONAL]
If SAT is in P by a polynomial-time algorithm A and PV proves "A(F) = reject => F has no satisfying assignment", then Extended Frege has polynomial-size proofs of every UNSAT formula; so Wbar_EF is poly.
So the correct weakest sufficient bridge for R = EF is the provability form:
  (SAT in P with a PV-provable soundness proof) ==> Wbar_EF poly.
Contrapositive: a superpolynomial EF lower bound gives "P != NP OR no poly SAT algorithm has PV-provable soundness".
Two honest consequences:
(a) An EF lower bound alone cannot give P != NP. A second theorem is needed: any poly SAT algorithm is PV-provably sound, or a stronger R that absorbs all algorithms, with no p-optimal-system assumption.
(b) Universal absorption is blocked by known limits: p-optimal proof systems are not known to exist. (Candidate theory-free statement, OPEN.)

## Hard-instance literature clues
- Atserias-Muller-style results (FOCS 2025, "The Proof Analysis Problem", arXiv:2506.16956; I read only a search summary): EF can prove that automating Resolution is NP-hard, and there are Resolution-hard CNFs for which strong theories cannot prove even quadratic lower bounds. Lower bounds on Wbar_R may be unprovable in the ambient theory for the same reason, a self-provability barrier [CANDIDATE relevance; verify at source].
- Automatability: EF and TC0-Frege are not automatable under cryptographic assumptions (Krajicek-Pudlak; Bonet-Pitassi-Raz). Free search, as in the user's convention, deliberately sidesteps automatability, so these do not obstruct Wbar_R lower bounds themselves.
- ECCC TR26-055 (meta-proof-complexity and automatability): not read; follow up.

## Concrete next targets for the five roles
1. Lead: state a hypothesis H on algorithms (e.g. PV-provable soundness) and the weakest R_H for which "SAT in P under H ==> Wbar_{R_H} poly" is a theorem. Lemma 1 shows weakening R is useless; only absorbing R can work.
2. Builder: the combined system "EF + GF(2) + extension + adaptive switching" as the fixed R; certify shortest-DAG sizes on n<=6 3-CNF by exhaustive search (stages <=30 s each).
3. Hypergraph/certificates: families that are hard for Resolution and PC but known EF-easy (Tseitin, pigeonhole). These show where Wbar_R drops as R strengthens.
4. Resource auditor: price each move including extension-variable definitions under both size and peak-state axes.
5. Red team: look for a poly SAT algorithm for a restricted class whose soundness is not PV-provable (known: none natural), and test Lemma 1's use anywhere in the corpus.

Verdict: the bridge is circular for any R with a known lower bound, and genuine only for R rich enough to formalise algorithms (EF, via PV). The lower-bound side for EF is a famous open problem. No new lower bound is claimed. P vs NP OPEN.
<!-- END_OF_VERIFIED_REPORT::WC-0001::2026-11-10 -->
