# Localized witnessing: a witness-free, length-tolerant form of the Pich–Santhanam bridge to B(EF)

Run: 2026-11-16, third pass (scheduled Claude routine). Branch `ccr-1695bd63-vp7fgl`, base `f9f4d90c` (origin/main).
Status: Lemma 1 and Theorem 3 are PROVED/EXACT at sketch level, unreviewed. Lemma 4 is PROVED (sketch), unreviewed. The finite check is COMPUTATIONAL. The hypothesis H_sound is OPEN. **P versus NP remains OPEN.** No lower bound and no unconditional bridge is proved.

Dependency advanced: **BRIDGE-B(EF)**, the arrow SAT ∈ P ⟹ W̄_EF(N) ≤ poly(N). By the previous run (`2026-11-16_RMIX341_EF_COLLAPSE.md`) this is the same as the bridge for the repository's fixed mixed calculus R_mix341. The log's open next lemma was "reproduce the Pich–Santhanam conditional bridge in project notation". This report does that from the paper body and then weakens the hypothesis.

## 0. Source actually read

J. Pich and R. Santhanam, *Towards P ≠ NP from Extended Frege lower bounds*, arXiv:2312.08163v1 (13 Dec 2023), ECCC TR23-199. I read §1.1.1 (pp. 2–4) in full from the PDF text: the formula w^k_n(f), Theorem 1, Corollary 1, Proposition 1 and Corollary 2. Later sections were not read.

- **Theorem 1.2 (KNOWN THEOREM).** Suppose there is a p-time f with S^1_2 ⊢ W^k_{n0}(f). Then if EF is not p-bounded, SAT_n ∉ Circuit[n^{εk}] for infinitely many n.
- **What w^k_n(f) says.** For every circuit C of size n^k, either C solves search-SAT at length n, or f(C) = (φ, a) where φ has length n, a satisfies φ, and C(φ) does not.
- **Corollary 2 (KNOWN THEOREM).** This is the uniform version for n^k-time algorithms with ≤ log n description bits and u(n) advice bits. Its conclusion is SAT ∉ Time[n^{Ω(k)}]/u(n).
- **The authors' emphasis.** f must find an error *at the same length n* and must output a satisfying assignment. They note that diagonal "refuters" [Gutfreund–Shaltiel–Ta-Shma 2007; Bogdanov–Talwar–Wan ICS 2010] do not supply this.

Follow-up literature checked: Arteche–Khaniki–Pich–Santhanam, ICALP 2024 (arXiv 2405.02232). This conditional iEF ⟹ #P ⊄ FP/poly result was read at abstract level only. It records the PS observation that an *unconditional* "EF lower bound ⟹ circuit lower bound" connection would already imply NEXP ⊄ P/poly.

The project notation is: B(R) := [SAT ∈ P ⟹ W̄_R(N) ≤ poly(N)], with free choice of the optimal derivation.

## 1. Candidate and falsifiers (stated before the proofs)

Candidate: the uniform B(EF) follows from a witnessing hypothesis that needs neither (i) a satisfying assignment in the output nor (ii) an error at exactly length n. The certificate is a *local inconsistency* of the decider in the restriction (self-reduction) DAG.

Falsifiers:
- **F1.** A decider that is wrong at length n but locally consistent on every formula of length n. This would kill Lemma 1(a). **Not possible:** see the proof.
- **F2.** The EF derivation from local consistency to soundness needs exponentially many instances of LocCons. This would kill Lemma 1(b). **Handled:** the derivation uses one walk of length ≤ n, driven by the free assignment variables y.
- **F3.** Length tolerance breaks the concrete-evaluation step. **Handled:** evaluating a fixed poly-time A on a fixed string of length n^c has poly(n) EF proofs.
- **F4.** The weakened hypothesis is strictly stronger than PS's, or is false outright. **Partly handled:** Lemma 4 shows it is implied by the PS uniform hypothesis applied to self-reduction search algorithms. Its truth under P ≠ NP is OPEN. Under SAT ∈ P its *truth* holds trivially, and only its S^1_2-*provability* has content.

## 2. Definitions

- **Fixed CNF encoding.** Restriction ψ|_{x_i=b} is re-padded to the same length n. A is a deterministic algorithm with output 1 = SAT, a description of ≤ log n bits, and clock n^k.
- **i(ψ)** is the least free variable of ψ. "Closed" means ψ has no free variable or contains the empty clause.
- **Local consistency.**

      LocCons_A(ψ) :=  [ψ closed ∧ A(ψ) = eval(ψ)]  ∨  [ψ open ∧ A(ψ) = A(ψ|_{i=0}) ∨ A(ψ|_{i=1})].

  This is a three-point hyperedge (parent, child0, child1) in the restriction DAG of ψ. That DAG is the precise form of the "multisign DAG hypergraph" in the routine prompt.
- **Loc_{A,n}** := ∀ψ ∈ {0,1}^n LocCons_A(ψ). As a propositional family it has poly(n^k) size: three copies of A's length-n circuit plus the restriction circuit.
- **Sound_{A,n}** := ∀ψ, y [A(ψ) = 0 → ¬Sat(ψ, y)].

## 3. Lemma 1 (localization). PROVED/EXACT, sketch, unreviewed; likely folklore

**(a)** A decides SAT correctly on all formulas of length n ⟺ Loc_{A,n} is true.

**(b)** EF has proofs of Loc_{A,n} → Sound_{A,n} of size poly(n, n^k).

*Proof of (a).* (⟹) The exact SAT predicate satisfies the recurrence. (⟸) Use induction on the number of free variables. Closed formulas are correct by the first disjunct. An open ψ inherits correctness because SAT(ψ) = SAT(ψ0) ∨ SAT(ψ1).

*Proof of (b).* Work with free variables ψ, y. Define a walk ψ_0 = ψ, ψ_{t+1} = ψ_t|_{i(ψ_t) = y_{i(ψ_t)}} (identity when ψ_t is closed), for t < n, using extension variables. Each restriction is a fixed poly-size circuit.

1. EF proves Sat(ψ_t, y) → Sat(ψ_{t+1}, y). The restriction agrees with y.
2. EF proves LocCons_A(ψ_t) → [A(ψ_t) = 0 → A(ψ_{t+1}) = 0]. This is the substitution instance of the hypothesis at the circuit ψ_t. EF p-simulates substitution Frege, so the instance costs poly.
3. At t = n, ψ_n is closed. LocCons gives A(ψ_n) = eval(ψ_n), and Sat(ψ_n, y) gives eval(ψ_n) = 1.

Chaining yields Sat(ψ, y) → A(ψ) = 1. That is n rounds of poly(n^k) lines. ∎

This is the same walk as check C4 in §7.

**Corollary 2.** B(EF) ⟺ [SAT ∈ P ⟹ ∃ correct p-time A such that Loc_{A,n} has poly(n)-size EF proofs].

*Proof.* (⟸) Let F be UNSAT with |F| = n. From Lemma 1(b) get a proof of Sound_{A,n}. Substitute ψ := F. EF-evaluate A(F) = 0, a fixed computation of size poly(n^k). Conclude ¬Sat(F, y) and refute F. (⟹) A p-bounded EF proves the true poly-size tautologies Loc_{A,n}. ∎

This sharpens the earlier Theorem B (TMR-5/057 on branch dh8nvl; LSPV-1/361). The tautology the bridge needs is the *local* labelling constraint on the restriction hypergraph, not the global soundness statement.

## 4. Theorem 3 (localized witnessing ⟹ B(EF)). PROVED/EXACT, sketch, unreviewed

**Hypothesis H_sound.** For every k there are a constant c and a p-time f_k such that S^1_2 proves the ∀Π^b_1 (indeed open-PV) sentence

    ∀n ∀A (|A| ≤ log n, clock n^k) ∀ψ ∀y :  [Sat(ψ, y) ∧ A(ψ) = 0 ∧ |ψ| = n]  →  [ |f_k(A, 1^n)| ≤ n^c ∧ ¬LocCons_A(f_k(A, 1^n)) ].

In words: whenever A gives a false UNSAT answer at length n, f_k outputs a concrete local inconsistency of A at some length ≤ n^c. The output carries no satisfying assignment and need not be at length n.

**Theorem.** H_sound ⟹ B(EF). Equivalently, H_sound ∧ (EF not p-bounded) ⟹ SAT ∉ P.

*Proof.* Assume SAT ∈ P via a correct A_0 with clock n^{k_0}. Take k = k_0 and n large enough that |A_0| ≤ log n.

1. Cook's translation of the S^1_2 proof gives poly(n)-size EF proofs of the length-n propositional translation. Substitute the constant description A_0.
2. A_0 is correct at every length, so LocCons_{A_0}(f_k(A_0, 1^n)) is a true closed statement about a fixed poly-time computation on a fixed input. EF proves it in poly(n^{c·k}) size by evaluation.
3. Modus ponens on the contrapositive gives Sound_{A_0, n}.
4. Corollary 2 (⟸) then refutes every UNSAT F of length n in poly(n) size. So W̄_EF(N) ≤ poly(N). ∎

**Resource ledger** (per refuted F, |F| = n; "size" means EF symbols):

| component | size |
|---|---|
| translated S^1_2 proof | p_W(n), a polynomial fixed by the S^1_2 proof |
| substitution of A_0 | O(log n) constants |
| evaluation of f_k(A_0, 1^n) | poly(n) |
| evaluation of A_0 at three points of length ≤ n^c | O(n^{c·k_0}) per point, times poly |
| evaluation of A_0(F) | O(n^{k_0}) |
| final modus ponens | O(1) lines |

Total size is poly(n). The free choice of derivation is used: nothing charges the discovery of A_0 or of the S^1_2 proof. The minimum over derivations is only bounded above. This matches the routine's convention.

## 5. Lemma 4 (H_sound is no stronger than the PS uniform hypothesis). PROVED, sketch, unreviewed

Let S_A be the standard A-guided self-reduction search algorithm. It follows a child where A says 1 and outputs the leaf assignment.

**Claim.** If f witnesses PS-errors of S_A at length n, S^1_2-provably, then f' := walk ∘ f witnesses H_sound for A, S^1_2-provably. Here f outputs (φ, a) with a ⊨ φ and S_A(φ) ⊭ φ, for every A with false-UNSAT at n (Corollary 2-type hypothesis with u = 0).

*Proof.* A false-UNSAT (ψ, y) for A means S_A fails at ψ, so the PS antecedent holds. Given (φ, a), there are two cases:

- If A(φ) = 0, walk along a. Lemma 1(b)'s walk must meet a node violating LocCons within n steps, because the closed leaf is satisfied while A keeps answering 0.
- If A(φ) = 1, follow S_A's path. It must hit a node with A = 1 and both children 0, or a closed false leaf with A = 1. Either one is a local inconsistency.

Both walks are p-time with ≤ n steps. Their correctness is a bounded (Π^b_1-LIND) induction available in S^1_2. ∎

The converse is not known. A local inconsistency is not a satisfiable-with-witness error. So H_sound is a candidate *strict* weakening, with two relaxations: no witness and polynomial length tolerance. The second matters only uniformly. In the nonuniform Theorem 1 the circuit C exists only at length n, so length tolerance is meaningless there.

## 6. Exact residual obstruction (OPEN; the named next lemma)

Try to build f_k for H_sound by the Gutfreund–Shaltiel–Ta-Shma idea. Let

    Φ_n(A) := "∃ψ ∃y : |ψ| = n ∧ Sat(ψ, y) ∧ A(ψ) = 0",

which has length m = poly(n^k). The function f runs A and its self-reduction on Φ_n(A):

- **A(Φ_n) = 1.** The A-guided walk either reaches a satisfying assignment (ψ, y), or reaches a local inconsistency at length ≤ m. In the first case f walks along y on ψ and finds a local inconsistency at length ≤ n. **f succeeds.**
- **A(Φ_n) = 0 and Φ_n is UNSAT.** Then A has no false-UNSAT at n, the antecedent is false, and any output is acceptable.
- **A(Φ_n) = 0 and Φ_n is SAT.** This is the **self-referential false-UNSAT** case. A errs on the very formula asserting that it errs. No certificate is obtained, and iterating to Φ_m(A) regresses.

So the open dependency is:

**OPEN lemma SR.** For every p-time A, either A(Φ_n(A)) = 0 implies a p-time-findable local inconsistency of A at length ≤ n^c, or such A can be S^1_2-provably detected. For example, f could also query A on a polynomial family of "diagonal" formulas built from A's code.

In addition, the whole case analysis must be S^1_2-provable. That is automatic for the first two bullets, since their conclusions are p-time checkable, and it is exactly what fails for the third.

Every known refuter of this kind gives errors only for infinitely many n (GST). That is too weak for B(EF), which needs every large n.

## 7. Finite check (COMPUTATIONAL; proves nothing asymptotic)

- **Code and data.** `research/agents/claude/worst-case-derivation/local_consistency_check.py`, revision `local-consistency-check.v2`, sha256 `39c0dba8883436efcf22ea46f717e8ee2ac49d119a0b00123bc66876f36850a2`. Seed 20261116 (and 20261122 for C6), CPython 3.11.18, 2.1 s. Raw output: `local_consistency_check_raw.json`.
- **C1–C2.** There are 144 random 3-CNFs on 4–7 variables, with 4155 restriction-closure nodes, and 2880 perturbed deciders. The exact decider is consistent everywhere. No perturbed decider was consistent on the whole closure of F yet wrong at F. This is Lemma 1(a) on finite instances.
- **C3–C4.** Each of the 46 false-SAT and 176 false-UNSAT errors converted to a local inconsistency by the walk. Random flips are shallow: the maximum depth was 1.
- **C6 (adversarial path hiding).** These are unique-model 3-CNFs on v = 6, 8, 10, 12 variables, 6 each. Set D := 0 on the whole satisfying path. The only inconsistency is then the closed leaf at depth v, which the assertion verifies exactly. The y-guided walk finds it with 3v + 1 queries (19, 25, 31, 37). Breadth-first search without y queried 31–35, 66–97, 117–199 and 181–429 nodes. That is essentially the whole closure.
- **Reading.** This shows finitely the cost of the missing witness, the gap that H_sound's f must close. It is not evidence for or against H_sound.

## 8. Gates and controls

| gate | status |
|---|---|
| DISJ sanity | NOT APPLICABLE: no communication or rank invariant is used. |
| Relativization | OPEN. Lemma 1 and Theorem 3 relativize (A^O with O-gates in EF^O), so they cannot by themselves separate P from NP. All the content is in H_sound, whose provability is the non-relativizing part. |
| Algebrization, Natural Proofs | NOT APPLICABLE: the statement is not a circuit-lower-bound property. |
| Simultaneous DTISP | NOT APPLICABLE: there is no time-space claim. |
| Deterministic configuration counting | NOT APPLICABLE (upper-bound consistency only). |
| Easy-family controls (PHP, Tseitin, clique–coloring) | Unchanged. All have poly EF refutations, so none can witness W̄_EF superpolynomial. |
| PS Proposition 1 barrier | The circuit form says any concrete R whose non-p-boundedness provably gives NP ⊄ P/poly would already give NP ⊄ SIZE[n^ℓ]. Its uniform analogue is vacuous: NP ⊄ DTIME(n^ℓ) is already known from the time hierarchy, because P ⊆ NP. So this argument puts no barrier on a uniform B(EF). Other barriers are not excluded. |

## 9. Next lemma

Settle OPEN lemma SR in §6. Either give a p-time diagonal family that catches self-referential false-UNSAT deciders, or exhibit a p-time A for which every f_k fails relative to an oracle. The oracle option would show that H_sound is not relativizingly provable, and so pin the non-relativizing content of B(EF).

## References

- J. Pich, R. Santhanam. Towards P ≠ NP from Extended Frege lower bounds. arXiv:2312.08163v1; ECCC TR23-199.
- N. Arteche, E. Khaniki, J. Pich, R. Santhanam. From Proof Complexity to Circuit Complexity via Interactive Protocols. ICALP 2024, LIPIcs 297:12; arXiv:2405.02232.
- D. Gutfreund, R. Shaltiel, A. Ta-Shma. If NP languages are hard on the worst-case then it is easy to find their hard instances. Computational Complexity 16(4):412–441, 2007.
- A. Bogdanov, K. Talwar, A. Wan. Hard instances for satisfiability and quasi-one-way functions. ICS 2010.
- S. Cook. Feasibly constructive proofs and the propositional calculus. STOC 1975.
- J. Krajíček. Proof Complexity. Cambridge University Press, 2019. Covers S^1_2–EF translation and EF ≡ SF.
- Repository: LSPV-1/361, TMR-5/057 (branch ccr-1695bd63-dh8nvl), and `2026-11-16_RMIX341_EF_COLLAPSE.md`.
