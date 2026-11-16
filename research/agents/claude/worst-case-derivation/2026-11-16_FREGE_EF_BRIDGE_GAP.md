# Bridge(Frege) versus Bridge(EF): the gap is exactly one conditional simulation

Claude scheduled routine, 2026-11-16 (run 3 on the merged log; branch `ccr-1695bd63-bveg4t`).
Base: main `00f8ada1`, plus sibling routine branches `ccr-1695bd63-o6urne` (tex lineage) and
`ccr-1695bd63-o1klgo` (markdown lineage) merged without conflicts. **P versus NP remains OPEN.**
No code was executed this run. Nothing here has been independently reviewed.

## Target and quantifiers

`W̄_R(N) = max_{F ∈ UNSAT, |<F>| ≤ N} min_{π : F ⊢_R ⊥} |π|`.
`Bridge(R)` means `SAT ∈ P ⟹ W̄_R(N) ≤ N^{O(1)}`, i.e. `P=NP ⟹ R` is p-bounded.
`LB(R)` means that `W̄_R` is superpolynomial.
Frege and EF are fixed Cook–Reckhow systems, and Frege ≤_p EF.
`Con_EF` is the family of partial-consistency tautologies of EF (Buss's sense, given polynomial size).
This run's dependency is the open question in the tex lineage: is Bridge(Frege) ⇔ Bridge(EF)?
That question asks whether the choice of fixed `R` above Frege changes the program.

## Falsifiers stated before the literature search

- H1. A published theorem that P=NP implies Frege ≥ EF. If it exists, the two bridges are equivalent.
- H2. A published conditional separation of Frege from EF whose assumption is compatible with P=NP. If it exists, the gap is non-vacuous under the bridge's own hypothesis.
- H3. Buss's characterization "Frege ≥_p EF ⇔ Frege has poly-size proofs of Con_EF" is false or misquoted.

Search outcome:
- H1: not found. A secondary source says Frege vs EF is open, and says P=NP gives only automatability.
- H2: not found. Every known conditional separation tool is cryptographic (see Theorem 3).
- H3: confirmed from two secondary summaries of Buss's abstract. The paper's PDF could not be fetched (HTTP 503), so the exact statement is still unverified.

## Theorem 1 (PROVED/EXACT, elementary; unreviewed)

Let `Q` be the statement: P=NP and EF p-bounded ⟹ Frege has polynomial-size proofs of Con_EF.

Then Bridge(Frege) ⇔ Bridge(EF) ∧ Q. Equivalently, Bridge(EF) ⇒ Bridge(Frege) holds iff Q holds.

Proof.
- (⇒) Bridge(Frege) ⇒ Bridge(EF), because EF ≥_p Frege (seesaw).
- (⇒) Under P=NP, Bridge(Frege) makes Frege p-bounded. Con_EF is a family of polynomial-size tautologies, so it has polynomial-size Frege proofs. Hence Q holds.
- (⇐) Assume P=NP. Bridge(EF) makes EF p-bounded. Q then gives poly-size Frege proofs of Con_EF.
- By Buss 1991, Frege then p-simulates EF, so Frege is p-bounded. ∎

Remark (under P=NP, size simulation and p-simulation coincide for p-bounded targets). A Frege proof of size ≤ p(n) can be found by prefix search with an NP oracle, and that oracle is in P. So "simulates" versus "p-simulates" does not matter here.

Consequence (seesaw tradeoff). The two routes cost:
- (LB(EF), Bridge(EF)) at EF;
- (LB(Frege), Bridge(EF) ∧ Q) at Frege.

LB(Frege) is weaker than LB(EF), but the Frege route pays exactly Q extra on the bridge side. Neither route dominates the other. Moving `R` above or below EF trades lower-bound difficulty for bridge difficulty one-for-one, through a single conditional simulation statement.

## Theorem 2 (PROVED, sketch; unreviewed): the self-certifying witness at Frege

Assume Bridge(Frege) and P=NP. Then there is a complete polynomial-time SAT algorithm `A_Fr` in Alg(Frege), in Krajíček's sense: its reflection formulas `ref^{A_Fr}_{k,n}` have poly-size Frege proofs. `A_Fr` does not depend on any proof about the P=NP decider `B` that it calls.

Construction. `A_Fr` works as follows:
1. Find a Frege refutation π with |π| ≤ p(|F|) by prefix search with `B`.
2. Run a checker `Chk_Fr` that is implemented by a log-depth, poly-size circuit. Frege-proof checking is in NC^1, which suffices for this.
3. Reject (answer UNSAT) iff `Chk_Fr` accepts.

Proof sketch.
- The formula `reject^{A_Fr}(u,v)` carries the full computation trace `v` as free variables.
- The search phase is irrelevant: the implication needs only the wires of the `Chk_Fr` sub-trace, which include π.
- The trace clauses of a log-depth circuit, together with the output bit 1, imply the poly-size formula `Valid_Fr(u,π)`. Frege proves this by gate-by-gate equivalence, and the formula size is polynomial because the depth is O(log).
- Finally, `Valid_Fr(u,π) → ¬sat(u,w)` is the reflection principle of Frege. Frege has polynomial-size proofs of it (Buss 1991; also cited as such in Pudlák arXiv 2007.14835).
- Obligation (not discharged): reflection from partial consistency for Frege. The standard derivation uses substitution instances, which Frege simulates. This should be checked against Krajíček's 1995 book, Ch. 9.

This is the Frege analogue of run 2's Theorem (premise U ⇔ Bridge(EF)). The theory changes from PV to VNC^1, and the checker must be shallow.

## Theorem 3 (KNOWN in substance; elementary observation): known Frege/EF separation evidence is void under P=NP

Under P=NP:
- every disjoint NP pair (U,V) is separated by the P-algorithm deciding U, so every proof system has feasible interpolation trivially, with an interpolant independent of the proof;
- every p-bounded system is automatable.

The known conditional evidence that Frege does not simulate EF is:
- non-feasible-interpolation of Frege or EF under factoring, RSA or Diffie–Hellman hardness (Krajíček–Pudlák 1998; Bonet–Pitassi–Raz 2000);
- non-automatability results.

All of this evidence rests on cryptographic assumptions that are false when P=NP. So no known tool falsifies Q. Q is **OPEN**, and both truth values are consistent with current knowledge to our search. This is not a proof that Q is true.

## Side closure of the markdown lineage's next lemma: SR(A) for a DPLL-style class

Statement (PROVED, elementary; unreviewed). Let `A` be a certifying decider: it answers UNSAT only after it internally checks a resolution refutation it has built (DPLL or CDCL with proof logging). Then:
- Sound_{A,n} has poly-size EF proofs, by EF's proofs of the reflection of resolution. So SR(A) holds for such `A`.
- No such `A` is a complete polynomial-time decider. Resolution has exponential lower bounds (Haken 1985; Chvátal–Szemerédi 1988).

So the DPLL-style restricted class satisfies SR vacuously at the decisive point. It cannot carry the single-family collapse, and the lemma is **uninformative** (RETIRED as a target). The same holds for any certifying class whose certificate system has a known lower bound. This is the bridge-collapse theorem in white-box form.

## Gates

| Gate | Status |
|---|---|
| DISJ | NOT APPLICABLE (no communication invariant) |
| Relativization | Theorems 1–3 are logic plus cited proof-complexity facts. Any proof of Q or of Bridge(EF) must be non-relativizing (Baker–Gill–Solovay) and must avoid the Pich–Santhanam witnessing barrier. |
| Simultaneous DTISP | NOT APPLICABLE (size-only statements) |
| Deterministic configuration counting | PASS as a consistency check; no claim below 2^n·poly |
| Natural Proofs / algebrization | Unchanged. Interpolation-based lower bounds for Frege/EF are blocked under crypto, but the bridge hypothesis P=NP removes the crypto. LB and Bridge are therefore evaluated in incompatible worlds, which is the structural reason the decomposition gives no free leverage. |

## Literature checked this run

- Buss, *Propositional consistency proofs*, APAL 52 (1991). Abstract seen via secondary summaries; PDF fetch failed (503).
- Pudlák, arXiv 2007.14835 (reflection survey). Search snippet only.
- Arteche–Khaniki–Pich–Santhanam, arXiv 2405.02232. Abstract read: iEF lower bounds ⇒ #P ⊄ FP/poly, conditional on iEF proving a hardness hypothesis. This is an iEF-level clue toward an LB-to-circuit transfer, not a Frege/EF equivalence.
- Pich–Santhanam, arXiv 2312.08163. Cited from earlier runs.
- Krajíček, *A note on SAT algorithms and proof complexity*. Cited from run 2.

## Next load-bearing lemma

Find a non-cryptographic consequence of Q. Concretely: decide whether "P=NP and Frege p-bounded" implies a circuit or witnessing collapse, for example a VNC^1-witnessing consequence that P-computable search problems have NC^1 solutions. If such a consequence contradicts a known unconditional result, the Frege route is dead and EF is the canonical choice of `R`. If it does not, Q stays open, and the program's fixed system can be taken as EF without loss.
