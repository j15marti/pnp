# Worst-case derivation bridge: collapse, complementarity and EF reflection reduction

Run: 2026-11-16 (scheduled Claude routine, worst-case derivation directive). Branch `ccr-1695bd63-jady22`, base `4cbb8b29`.
Status summary: three PROVED/EXACT elementary statements (Theorems 1, 2, 4) plus one KNOWN THEOREM instantiated with an explicit proof sketch (Theorem 3). There is no theorem promotion. **P versus NP remains OPEN.** Independent review has not been done. No code was executed in this run. These are symbolic arguments only.

## 0. Target and model

The target, as the directive states it:

    W̄_R(N) = max_{F ∈ UNSAT, |<F>| ≤ N}  min_{π : F ⊢_R ⊥} cost_R(π)

The bridge is B(R): `SAT ∈ P ⟹ W̄_R(N) ≤ poly(N)`.

Model:
- R is a fixed Cook–Reckhow refutation system: a polynomial-time map from strings onto UNSAT CNF encodings.
- Cost is serialized proof size. For the multisign DAG-hypergraph calculus, node count is at most serialized size, and any per-node cost that is polynomial in node size is polynomially equivalent.
- For UNSAT F, the minimal reduced logical state of the hypergraph is ⊥, so the minimum work equals the minimum refutation cost.
- The user's point is correct: taking the minimum over all derivation sequences is a valid lower-bound strategy, and strategy discovery is not charged.
- The only route from W̄_R to solver runtime is B(R). This report studies exactly that arrow.

Proof systems used: Res, CP, PC, AC0-Frege, Frege and EF (Extended Frege). Q_A is the clocked solver-trace system from `research/agents/codex/2026-11-11_1331_TRANSFER_RECOVERY_AND_RATE_AMPLIFICATION.tex`, eq. (18). A proof in Q_A is `(F, 1^t)`. It is accepted iff the t-step run of A on F outputs UNSAT. So L_{Q_A}(F) = O(|F| + time_A(F)).

## 1. Candidate and falsifiers, stated before the source search

Candidate: for R = EF, B(EF) is equivalent to a statement about polynomial-size EF proofs of an explicit family of correctness tautologies for some polynomial-time SAT algorithm.

Falsifiers:
- (F1) Substituting the input constants into an EF proof of a correctness tautology could blow up superpolynomially. **Checked: it does not.** Substituting constants never increases size, and gate-by-gate evaluation is linear in the circuit size.
- (F2) Malformed encodings could break the tautology. **Checked:** Sat_n(x,y) contains a well-formedness conjunct, so Corr holds vacuously on malformed x.
- (F3) There could be a system R with a proven superpolynomial W̄_R and an unconditional proof of B(R). This would prove P≠NP. Theorem 2 shows this is the only way out.
- (F4) The project's combined calculus R_H might not be p-simulated by EF. **OPEN**, and it is the named next dependency.

## 2. Results

**Theorem 1 (bridge = solver-trace simulation). PROVED/EXACT, elementary.**
B(R) holds iff the following is true: for every polynomial-time SAT decider A, R polynomially size-simulates Q_A pointwise on UNSAT, that is, w_R(F) ≤ poly(L_{Q_A}(F)).
- (⇐) If SAT ∈ P via A, then L_{Q_A}(F) ≤ poly(|F|), so W̄_R ≤ poly. This is the codex report's eq. (20).
- (⇒) Assume SAT ∈ P and B(R). Then w_R(F) ≤ W̄_R(|F|) ≤ poly(|F|) ≤ poly(L_{Q_A}(F)), because L_{Q_A}(F) ≥ |F|.
- If SAT ∉ P, both sides hold vacuously. Under the hypothesis SAT ∈ P, "some A" and "every A" are equivalent.
- Consequence: B(R) is literally `SAT ∈ P ⟹ R is polynomially bounded`. No weaker formulation exists inside this framework.

**Theorem 2 (complementarity gate). PROVED/EXACT, elementary.**
If W̄_R(N) ≥ N^{ω(1)} is an unconditional theorem, then B(R) ⟺ P ≠ NP.
- (⇒) is the contrapositive.
- (⇐) holds because B(R) is vacuous when P ≠ NP.
- Known superpolynomial worst-case lower bounds exist for:
  - Resolution (Haken 1985, PHP)
  - Cutting Planes (Pudlák 1997, clique–coloring)
  - Polynomial Calculus (Razborov 1998; Buss–Grigoriev–Impagliazzo–Pitassi 1999, Tseitin over char ≠ 2)
  - bounded-depth Frege (Ajtai 1988; Krajíček–Pudlák–Woods 1995 and Pitassi–Beame–Impagliazzo 1993)
  - recent AC0[p]-Frege on a specific DNF family (Lu–Santhanam–Tzameret, ECCC 2025/134, not independently checked here)
- For each of these systems, "prove the weakest bridge" is *exactly* the P≠NP problem.

**Theorem 4 (seesaw monotonicity). PROVED/EXACT, elementary.**
If R1 ≤_p R2 (R2 p-size-simulates R1), then:
- B(R1) ⟹ B(R2), and
- a superpolynomial lower bound for W̄_{R2} implies a superpolynomial lower bound for W̄_{R1}.

Proof: W̄_{R2}(N) ≤ poly(W̄_{R1}(N)).

This applies to the combined system in assignment priority 4 (resolution + algebraic + circuit compression + shared DAGs + switching). Every rule added to the fixed system makes the bridge weaker and the lower bound harder, monotonically. The program cannot divide the difficulty between its two halves. Theorems 2 and 4 together locate the only non-circular regime: systems at Frege/EF strength or above, where lower bounds are open.

**Theorem 3 (EF bridge ⟺ feasible UNSAT-soundness). KNOWN THEOREM, instantiated; standard Cook/Krajíček–Pudlák reflection argument.**

Setup:
- Let A decide SAT in time p(n).
- C_n is the tableau circuit for A on inputs of length n. Its size is O(p(n)^2), or O(p log p) with the quasilinear Cook–Levin construction.
- Sat_n(x,y) is a polynomial-size formula stating that x parses as a CNF and y satisfies it.
- Corr_{A,n}(x,y,z) := [z is the gate vector of C_n on x and its output is UNSAT] → ¬Sat_n(x,y).
- Corr_{A,n} is a tautology iff A is sound on its UNSAT answers at length n.

Claims:
- (a) If EF proves Corr_{A,n} in size s(n), then every UNSAT F with |<F>| = n has an EF refutation of size s(n) + poly(n).
  - Substitute x := <F> as constants; size does not increase.
  - Derive the gate values z by evaluating C_n gate by gate, in O(|C_n|) lines.
  - Derive ¬Sat_n(<F>, y) by modus ponens.
  - Derive Sat_n(<F>, y) from the clauses of F in poly(n) size: with x fixed it reduces to the conjunction of the clauses.
  - These two give ⊥.
- (b) Conversely, if B(EF) holds and SAT ∈ P via A, then ¬Corr_{A,n} has a polynomial-size Tseitin CNF that is UNSAT. Refute it in EF, then reintroduce the Tseitin definitions as extension axioms. This gives polynomial-size EF proofs of Corr_{A,n}.

Hence:

    B(EF)  ⟺  [ SAT ∈ P ⟹ ∃ poly-time SAT decider A whose Corr_{A,n} have poly-size EF proofs ].

The sufficient condition `PV ⊢ UNSAT-soundness of A` gives (a) by Cook's 1975 PV→EF translation.
SAT-side soundness is never load-bearing. Self-reducibility lets A output a verified assignment whenever it answers SAT. The whole content of the bridge is therefore the *coNP side*: feasible provability that A's UNSAT answers are correct.

## 3. Integration point

The pipeline is: encoded 3-CNF → fixed calculus R → minimum-cost refutation DAG → W̄_R → bridge B(R) → runtime consequence.

This run closes the definitional part of the bridge arrow:
- B(R) is Theorem 1.
- Weak systems are ruled out by Theorem 2.
- Monotonicity is Theorem 4.
- For EF, the bridge reduces to a single explicit tautology family (Theorem 3).

What remains OPEN:
- (i) LB: W̄_EF superpolynomial. This is a famous open problem. Pich–Santhanam (arXiv 2312.08163) give conditional EF-lower-bound ⟹ NP ⊄ P/poly transfers.
- (ii) The EF correctness-tautology premise under SAT ∈ P. This is open. Li (ECCC 2025/187) proposes a proof-complexity conjecture implying that NP=coNP is unprovable in PV. That is evidence that (ii) can fail in the PV-provability form.

## 4. Gates

- DISJ: NOT APPLICABLE WITH REASON. These are proof-system equivalences, and no information-flow or communication claim is made.
- Relativization: PASS / NOT A SEPARATION. The equivalences relativize by inspection, and none claims a separation. Note: existence of optimal proof systems has oracle barriers (Krajíček–Pudlák 1989; arXiv 2408.07408).
- Simultaneous DTISP: NOT APPLICABLE. The cost is size only, and no space claim is made.
- Deterministic configuration counting: PASS. The upper-bound consistency L_{Q_A} = O(n + time_A) agrees with the configuration count of A.
- Natural Proofs / algebrization: NOT APPLICABLE. No circuit lower bound is claimed.
- Easy-family controls: Theorem 2 is itself the control. Any family whose hardness is already proven for a system below EF cannot carry the bridge.

## 5. Literature checked this run (standard web search; abstracts/TOCs only unless noted)

- Cook 1975 (PV, PV→EF translation); Cook–Reckhow 1979; Krajíček–Pudlák 1989/1990 (optimal systems under NE=coNE; p-optimal under E=NE). Also Krajíček, *Proof Complexity* (2019), Ch. on reflection.
- Pudlák, "Reflection principles, propositional proof systems, and theories", arXiv 2007.14835.
- Pich–Santhanam, "Towards P≠NP from Extended Frege lower bounds", arXiv 2312.08163.
- Li, ECCC TR25-187; Lu–Santhanam–Tzameret, ECCC TR25-134; Oliveira, meta-mathematics survey (2024).
- "Optimal proof systems for complex sets are hard to find", arXiv 2408.07408. Also an ICALP 2026 paper on recursive jump operators (LIPIcs vol. 374, paper 88). These were seen in search results only and not read.

Clue for the current problem: since P=NP ⟹ E=NE, the Krajíček–Pudlák theorem gives a p-optimal system **R\*** under SAT ∈ P. So B(R\*) holds for that system. But R\* depends on the hypothetical algorithm and is not a fixed, preselected calculus. Any fixed R for which B(R) is provable must already contain the reflection content of Theorem 3.

## 6. One next load-bearing lemma

Lemma (next target): define the project's fixed combined multisign DAG-hypergraph calculus R_H precisely. Then prove R_H ≤_p EF, or find a separating rule. Examples of rules that could separate: unbounded algebraic coefficients, or circuit-compression steps whose soundness is not PV-provable.

If R_H ≤_p EF, Theorem 4 gives B(R_H) ⟹ B(EF). The program then reduces to (i) and (ii) for EF, and R_H's own bridge is strictly harder than EF's.
