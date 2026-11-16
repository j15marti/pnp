# Lemma SR: the GST dichotomy, the self-referential regress, and one explicit worst-case family for EF

Run: 2026-11-16, fourth pass (scheduled Claude routine). Branch `ccr-1695bd63-o1klgo`, base `a29605c5` (origin/main), with the unmerged third-pass branch `ccr-1695bd63-vp7fgl` merged unchanged first.

Status:
- Theorem 1 is PROVED/EXACT (elementary, sketch), unreviewed.
- Proposition 2 is a KNOWN THEOREM in substance (Krajíček–Pudlák 1989 reflection/simulation). It is restated here in W̄ notation.
- Theorem 3 and Proposition 4 are PROVED/EXACT (elementary, sketch), unreviewed.
- Lemma SR is **RESTATED EXACTLY and partly FALSIFIED**: the naive form is false, and the corrected form is OPEN.
- No code was executed in this run. **P versus NP remains OPEN.**

Dependency advanced: **BRIDGE-B(EF)**, in the form H_sound ⟹ B(EF) from `2026-11-16_LOCALIZED_WITNESSING_BRIDGE.md` (third pass). That pass named "OPEN lemma SR", the self-referential false-UNSAT case, as the next lemma. This report settles how much the Gutfreund–Shaltiel–Ta-Shma (GST) route can contribute: **exactly nothing beyond B(EF) itself at the decisive point.** It also gives the exact remaining statement.

Notation from earlier passes:
- B(R) := [SAT ∈ P ⟹ W̄_R(N) ≤ poly(N)].
- LocCons_A(ψ) is the three-point restriction-hyperedge constraint.
- Sound_{A,n} := ∀ψ∈{0,1}^n ∀y [A(ψ)=0 → ¬Sat(ψ,y)].
- A is deterministic, with a description of ≤ log n bits and clock n^k.

## 1. Candidate and falsifiers (stated before proofs and literature)

Candidate: the GST diagonal formula reduces H_sound for A to a statement only about A's answer on its own error formula. For a correct A_0, the residual is the soundness tautology of A_0 itself, so the GST route gives a regress, not a proof.

Falsifiers:
- **F1.** g fails to produce a certified local inconsistency even when A(Φ_n(A)) = 1. This would kill Theorem 1.
- **F2.** The residual for correct A_0 is strictly weaker than an EF proof of Sound_{A_0,n}. This would make the GST route real progress and kill Theorem 3.
- **F3.** The naive self-trust form of SR is true. This would close H_sound via Theorem 1.
- **F4.** H_sound's *truth* is already known to follow from P ≠ NP at every large length. This would make Proposition 4's lower bar vacuous.

## 2. The self-referential formula

Φ_n(A) is the Tseitin 3-CNF of the circuit "|ψ| = n ∧ Sat(ψ,y) ∧ A(ψ) = 0".
- Variables: ψ, y and Tseitin auxiliaries z.
- Length: m = m_A(n) = poly(n^k), computable in time poly(m) from (A, 1^n).
- Semantics: Φ_n(A) ∈ SAT ⟺ A has a false-UNSAT answer at length n ⟺ ¬Sound_{A,n}.
- Its satisfying assignments are exactly (ψ, y, z) with ψ a certified error of A, together with its witness y.

## 3. Theorem 1 (GST dichotomy, provable). PROVED/EXACT, sketch, unreviewed

Let g(A, 1^n) be the following p-time procedure:
1. Run the A-guided self-reduction on Φ_n(A).
   - If it meets a node where LocCons_A fails, output that node. It has length m.
   - Otherwise it ends at a closed satisfied leaf, which gives an assignment (ψ', y', z').
2. In that case walk along y' on ψ'. This is the walk of Lemma 1(b) of the third pass. Output the first node of length n where LocCons_A fails.

Then S^1_2, and in fact PV, proves the open statement

    ∀A ∀n :  ¬LocCons_A(g(A,1^n))   ∨   A(Φ_n(A)) = 0.

*Proof.* Suppose A(Φ_n(A)) = 1. The A-guided self-reduction keeps a child answered 1 at every step. Within ≤ |vars(Φ_n)| steps one of two things happens:
- **(a)** It reaches a node answered 1 whose two children are both answered 0, or a closed leaf answered 1 that evaluates to 0. Either one is a LocCons failure.
- **(b)** It reaches a closed leaf that evaluates to 1. That gives (ψ', y') with Sat(ψ', y') and A(ψ') = 0.

In case (b) the y'-walk on ψ' starts at a node answered 0. Each step goes to the child that agrees with y'. That child remains satisfied by y'.
- If LocCons held at every node along the walk, A would answer 0 at every step, by the open-node clause.
- The walk would then end at a closed leaf satisfied by y' and answered 0, which violates LocCons there.

Both case analyses are polynomial-length iterations of a p-time step. The invariant ("A answers 1 at the current node" or "y' satisfies the current node and A answers 0 there") is quantifier-free in PV. So the induction is open induction along a p-time sequence, available in PV ⊆ S^1_2. ∎

F1 does not occur. Note that the antecedent "A errs at n" is not even needed: the dichotomy holds for every A.

## 4. Proposition 2 (one explicit family carries the whole worst case). KNOWN THEOREM in substance

Let s_EF(F) denote the minimum EF refutation size of F. Let A_0 be correct with clock n^{k_0}. Then

    W̄_EF(N) ≤ poly(N)   ⟺   s_EF(Φ_n(A_0)) ≤ poly(n).

Hence

    B(EF)  ⟺  [SAT ∈ P  ⟹  ∃ correct p-time A_0 with  s_EF(Φ_n(A_0)) ≤ poly(n)].

*Proof.*
- (⟹) Φ_n(A_0) is UNSAT, because A_0 is sound, and has length poly(n).
- (⟸) The Tseitin variables of Φ_n(A_0) are extension definitions. So an EF refutation of Φ_n(A_0) converts in poly size to an EF proof of Sound_{A_0,n}.
  - Given UNSAT F with |F| = n, substitute ψ := F in that proof.
  - EF-evaluate the fixed computation A_0(F) = 0 in size O(n^{2k_0}).
  - Modus ponens gives ¬Sat(F, y), that is, a refutation of F.

Total size: poly(n) + O(n^{2k_0}). ∎

In Krajíček–Pudlák language, ¬Φ_n(A_0) is the reflection principle of the p-bounded proof system Q_{A_0}, which accepts the empty proof of F iff A_0(F) = 0. EF p-simulates Q_{A_0} iff EF has short proofs of that reflection principle.

**Reading for the routine's objective.** Under SAT ∈ P the maximum over all UNSAT F in W̄_EF is attained, up to a polynomial, on one explicit, algorithm-dependent self-referential family. It is not attained on any combinatorial family: PHP, Tseitin and clique–coloring are all EF-easy.

Contrapositively, a proof of P ≠ NP through W̄_EF must show the following for **every** p-time A: either A is wrong somewhere, or Φ_n(A) is superpolynomially EF-hard.

This is the precise form of the "Hypergraph & Proof Certificates" assignment, to construct hard UNSAT families surviving all methods, for EF. The hard family **must depend on the algorithm it diagonalizes against**. Here "the algorithm" includes the algorithm's code, not just its I/O behaviour; compare TMR-5/060 Theorem C, under which black-box arguments collapse.

## 5. Theorem 3 (the regress: GST contributes nothing at the decisive point). PROVED/EXACT, sketch, unreviewed

H_sound(A) is H_sound specialized to one A: S^1_2 ⊢ [Sat(ψ,y) ∧ A(ψ)=0 ∧ |ψ|=n] → ¬LocCons_A(f(A,1^n)) at length ≤ n^c.

**(i) Reduction.** Theorem 1 gives H_sound(A), with f := g or h, as soon as S^1_2 proves

    SR(A):   ¬Sound_{A,n} ∧ A(Φ_n(A)) = 0  →  ¬LocCons_A(h(A,1^n))

for some p-time h.

**(ii) The regress for a correct A_0.** Run the third pass's Theorem-3 pipeline using only Theorem 1, that is, without SR. Cook-translating Theorem 1 and evaluating gives EF ⊢ A_0(Φ_n(A_0)) = 0. This is a true closed evaluation, and it says nothing about soundness. To reach Sound_{A_0,n}, EF still needs

    A_0(Φ_n(A_0)) = 0  →  Sound_{A_0,n}.

That is Sound_{A_0,m} instantiated at the single point Φ_n(A_0). Given the true evaluation of A_0 at that point, the implication is literally ¬Φ_n(A_0) = Sound_{A_0,n}. By Proposition 2 it has poly-size EF proofs iff B(EF) holds at length n.

So at the decisive point the GST route reduces B(EF) at length n to **the same** tautology. F2 does not occur. Iterating with Φ_m(A_0) only increases the length, so no length induction closes it.

**(iii) Exact location of the content.** Combining (i) and (ii), the whole non-relativizing content of H_sound for the algorithm that matters is SR(A_0)'s proof in S^1_2. Because A_0 is correct, the hypothesis ¬Sound_{A_0,n} of SR(A_0) is false. So S^1_2 ⊢ SR(A_0) is implied by S^1_2 ⊢ Sound_{A_0,n}. The converse holds for the purposes of B(EF) by (ii). The uniform H_sound demands SR(A) for **all** A in one S^1_2 proof. That is strictly more than needed, and it is where a proof could exploit uniformity.

## 6. Proposition 4 (falsification and placement of SR)

**(a) The naive self-trust form is FALSE.** Here "self-trust" means S^1_2 ⊢ A(Φ_n(A)) = 0 → Sound_{A,n}. The constant decider A ≡ 0 answers 0 on its own Φ_n(A) but is unsound at every n. So F3 is refuted, and the corrected SR(A) must use the inconsistency finder h.

For A ≡ 0, h can output the empty CNF, which is closed, true and answered 0. So SR(A) holds for this A. The counterexample only shows that h is indispensable.

**(b) Truth of H_sound gives a polynomial-window refuter.** If H_sound is true for all A (not merely provable), then the following refuter exists:

> For every p-time decider A and every n at which A gives a false-UNSAT answer, f(A, 1^n) is a certified error of A, namely a LocCons failure, at some length in [1, n^c].

GST (CC 2007) and Bogdanov–Talwar–Wan (ICS 2010, for search algorithms, with satisfying assignments) supply certified or listed errors **only for infinitely many n**, under P ≠ NP or NP ⊄ BPP respectively. No source checked gives every-large-n or polynomial-window refuters from P ≠ NP. So F4 does not occur as far as checked. An unconditional S^1_2 proof of H_sound would in particular make every polynomial-time SAT heuristic constructively refutable within polynomial windows. That is a "constructive separation" property in the sense of Chen–Jin–Santhanam–Williams (FOCS 2021); its definitions were recalled from memory and not re-read this run.

**Status of corrected SR (uniform in A): OPEN.** Its truth under SAT ∈ P is trivial, because h can use the true solver. Its truth under P ≠ NP at every large n is OPEN, and by (b) at least as strong as a window refuter.

## 7. Resource ledger

Sizes for refuting one UNSAT F with |F| = n, under SAT ∈ P via A_0 with clock n^{k_0}.

Route via Proposition 2:

| component | size |
|---|---|
| EF refutation of Φ_n(A_0) | s_EF(Φ_n(A_0)), assumed poly |
| Tseitin-to-extension conversion | O(m), with m = O(n^{2k_0}) |
| substitution ψ := F | O(m·n) |
| EF evaluation of A_0(F) | O(n^{2k_0}) |
| modus ponens and cleanup | O(m) |

Route via Theorem 1:

| component | size |
|---|---|
| Cook translation of the PV proof of Theorem 1 | poly(m) |
| evaluation of g(A_0, 1^n) | poly(m) |

The Theorem 1 route still leaves the residual Sound_{A_0,n} with no bound (Theorem 3(ii)).

As in the routine's convention, discovery of A_0 and of the proofs is not charged: only a minimum is bounded above. Nothing is claimed about bit-machine time or space.

## 8. Gates and controls

| gate | status |
|---|---|
| DISJ sanity | NOT APPLICABLE: no rank or communication invariant. |
| Relativization | Theorem 1 and Proposition 2 relativize, so they carry no separating power. The content sits in SR(A_0)'s provability. Black-box arguments for B(R) collapse (TMR-5/060 Theorem C, branch `ccr-1695bd63-lh9sf9`, unmerged). So OPEN, and necessarily non-relativizing. |
| Algebrization / Natural Proofs | NOT APPLICABLE to these statements. Any proof that Φ_n(A) is EF-hard inherits the known EF-lower-bound barriers (OPEN). |
| Simultaneous DTISP | NOT APPLICABLE. |
| Deterministic configuration counting | NOT APPLICABLE (upper-bound check only). |
| Easy-family controls | PHP, Tseitin, clique–coloring, bit-PHP (TMR-5/WR056) and affine/Gaussian families are EF-easy. None can be the worst-case family for EF. Proposition 2 shows the right family is diagonal. |
| /341 | FAIL as full UNSAT authority. |
| /386 | RESTRICTED. |

## 9. Mapping to the five assignments (this run's contribution only)

- **Lower-Bound Lead.** The weakest sufficient bridge for EF reduces to one explicit family per algorithm (Proposition 2). No weaker GST-based bridge exists (Theorem 3).
- **Reduction Builder.** Fixed system R_mix341 ≡_p EF (second pass). Its shortest-derivation question at the decisive family is s_EF(Φ_n(A_0)).
- **Hypergraph & Certificates.** The certificate structure is the LocCons hyperedge. Theorem 1 gives a provable certificate finder in all but the self-referential case.
- **Resource Auditor.** See the ledger in §7. No bit-model claims.
- **Red Team.** Proposition 4(a) falsifies naive SR. Theorem 3 falsifies "GST closes H_sound".

## 10. Literature checked this run

- Bogdanov–Talwar–Wan ICS 2010: ICS slide deck read in full text. Main theorem: if P ≠ NP, a p-time D outputs, for every p-time search algorithm A and **infinitely many n**, a pair (φ, w) of length n with w ⊨ φ and A failing. The method "uses A to find solutions to instances on which it fails". The full paper was not accessible (archive verification wall).
- GST 2007: via BTW slides and the third pass's notes.
- Carmosino–Dang–Jackman, arXiv:2604.23958 (2026), "Constructive Separations from Gate Elimination": abstract only. Refuters from gate elimination for small circuits. This shows refuter constructions exist for explicit circuit lower bounds, not for uniform SAT algorithms.
- Li–Li–Ren, STOC 2026, "Finding Bugs in Short Proofs": search snippet only. Refuter problems for resolution lower bounds tied to TFNP and relativized bounded arithmetic. This is a relevant clue: proving "Φ_n(A) EF-hard" has a refuter analogue for EF, which is open.
- Krajíček–Pudlák JSL 1989: reflection/p-simulation, as background for Proposition 2.

## 11. Next lemma (one)

Decide SR(A) for a **natural restricted class**: A_0 = a DPLL-style decider with a polynomial-time branching heuristic and unit propagation, clocked at n^k. Either:
- give p-time h with an S^1_2 proof of SR(A) for all A in the class, or
- show the class contains a correct-on-its-domain member for which S^1_2 ⊢ SR(A) would imply a known-open EF upper bound.

This is the first place where white-box structure of A, which TMR-5/060 shows is necessary, can enter.

## References

- D. Gutfreund, R. Shaltiel, A. Ta-Shma. If NP languages are hard on the worst-case then it is easy to find their hard instances. Computational Complexity 16(4), 2007.
- A. Bogdanov, K. Talwar, A. Wan. Hard instances for satisfiability and quasi-one-way functions. ICS 2010, 290–300.
- J. Krajíček, P. Pudlák. Propositional proof systems, the consistency of first order theories and the complexity of computations. JSL 54(3), 1989.
- J. Pich, R. Santhanam. Towards P ≠ NP from Extended Frege lower bounds. arXiv:2312.08163.
- L. Chen, C. Jin, R. Santhanam, R. Williams. Constructive separations and their consequences. FOCS 2021.
- M. Carmosino, N. Dang, T. Jackman. Constructive Separations from Gate Elimination. arXiv:2604.23958.
- J. Li, Y. Li, H. Ren. Finding Bugs in Short Proofs: The Metamathematics of Resolution Lower Bounds. STOC 2026.
- S. Cook. Feasibly constructive proofs and the propositional calculus. STOC 1975.
- Repository: third pass `2026-11-16_LOCALIZED_WITNESSING_BRIDGE.md`; TMR-5/060 on branch `ccr-1695bd63-lh9sf9`; TMR-5/057 on branch `ccr-1695bd63-dh8nvl`.
