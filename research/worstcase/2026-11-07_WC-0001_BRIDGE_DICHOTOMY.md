<!-- WC REPORT::WC-0001::2026-11-07 -->
# WC-0001: What the bridge B(R) can be (worst-case derivation programme)

Status: P vs NP **OPEN**. All items labelled; nothing here is a lower bound for a strong system.

## 0. Corpus reviewed / duplication audit
Surveyed repo tree, AGENTS.md, world ledger (rows on NP vs coNP, proof systems), LSPV-1 RUP/resolution bridge reports (Nov 2026), LSPV-5 proof-system fallback 163, charged-SAT-shrinker literature audit. grep finds no earlier report defining W_R as above with a bridge B(R); the dichotomy below is new to the corpus as a formulation, but its ingredients (Cook-Reckhow; known resolution lower bounds) are standard. No existing claim is strengthened.

## 1. Setup (EXACT definitions)
R = Cook-Reckhow system: poly-time verifier V(F,pi), sound and complete for UNSAT. Hypergraph/multisign DAG derivations are one concrete encoding (nodes = signed clause-hyperedges, arcs = rule applications, cost = DAG size; space = peak simultaneously-held nodes). W_R as in the directive. L(R) := "W_R is superpolynomial". B(R) := "SAT in P => W_R polynomial".

## 2. Free search is exactly Cook-Reckhow  (PROVED/EXACT, standard)
Charging nothing for finding the best pi is the NP-guess. Hence: (a) some R has W_R polynomial iff NP = coNP; (b) L(R) for a single R does not imply NP != coNP, since R may be weak. So granting free search loses nothing, but also gains nothing beyond proof complexity.

## 3. Bridge dichotomy  (PROVED/EXACT; elementary)
**Lemma 3.** (i) L(R) and B(R) together imply P != NP (contrapositive of B). (ii) If L(R) is a known theorem (e.g. R = resolution, tree resolution, Nullstellensatz/PC at bounded degree, cutting planes on monotone-interpolation families), then B(R) is classically equivalent to SAT not in P, so proving B(R) is exactly as hard as the target. (iii) If L(R) is not known (Frege, Extended Frege, strong systems), B(R) is a statement that no one has proved either way.
Consequence: a "weakest sufficient bridge" cannot be proved by a soft/semantic argument for any R whose lower bound is already known; it must be a *constructive simulation* of algorithms by derivations, valid only for systems where L(R) is itself open. This is the structural reason the programme cannot be decomposed into "easy bridge + known lower bound".

## 4. What a real bridge must look like
**Lemma 4 (CONDITIONAL; standard Cook translation, not re-proved here).** If M is a polynomial-time SAT decider and the theory PV proves its correctness Corr_M, then Extended Frege has polynomial-size derivations of every UNSAT F (use the poly-size propositional translation of Corr_M plus M's poly-size trace on F). So B_PV(EF): "SAT in P via an algorithm with PV-provable correctness => EF polynomially bounded" holds.
Gap (OPEN, load-bearing): B(EF) needs this for *every* possible fast algorithm, including ones whose correctness is not feasibly provable. If P=NP held only via an algorithm whose correctness PV cannot prove, Lemma 4 gives nothing. World-dependent systems R_M (verifier := run M) make B trivial but are not fixed R (they are sound only if M is correct, and encode the answer). Any fixed Cook-Reckhow R satisfying B in all worlds must therefore simulate all correct algorithms' traces without proving them correct - no known route, and no sound recursive system can add "all true correctness axioms" (that would be a complete decision of Pi_1 truths about machines).
Hence the realistic sufficient bridge is B*(R): "P=NP is provable-feasibly (PV/EF) if true". This is a *meta-mathematical* statement about independence of P=NP from bounded arithmetic, not a complexity lower bound; I label it CANDIDATE/OPEN and flag it as a likely failure point for the entire W_R route.

## 5. Direction of search charging (consistency check)
The bridge runs algorithm -> derivation (simulation), so no search cost enters. The reverse direction (short derivation -> algorithm) needs automatizability and would charge search; Krajicek-Pudlak show EF is not weakly automatable unless RSA is insecure against P/poly, so the reverse (pointwise-converse) theorem is unavailable for EF; consistent with the directive that only the conditional bridge is needed.

## 6. Survival of hard instances (role 3/5 tasks, no new claims)
Known: PHP, Tseitin on expanders, random 3-CNF are exponentially hard for resolution; PHP/BVP remain hard for PC/CP variants (Alekseev, Theory of Computing 22, 2026: exponential bit-size lower bounds for PC-with-extension on the binary value principle, a system simulating EF - but the result is for an *algebraic* proof size notion, not Boolean EF). No exponential lower bound for Frege/EF is known (Filmus-Pitassi-Santhanam; Pich-Santhanam link EF bounds to circuit lower bounds). Therefore "survives resolution, algebra, circuits, shared DAGs, strategy switching" currently holds only for restricted systems, which by Lemma 3(ii) cannot carry the bridge.

## 7. Literature clues (this run)
- Cook-Reckhow 1979: poly-bounded system iff NP=coNP. Krajicek-Pudlak 1989: NE=coNE gives optimal, E=NE p-optimal systems.
- Krajicek-Pudlak 1998: EF not weakly automatable unless RSA insecure vs P/poly.
- Alekseev (ToC 22, 2026): PC with extension, BVP lower bound. Pich-Santhanam (ECCC 2023): EF lower bounds vs circuit lower bounds. Filmus-Pitassi-Santhanam: bounded-depth Frege lower bounds imply Frege lower bounds in a restricted regime.
Classification: Cook translation = directly transferable (Lemma 4, needs PV-provable correctness); automatability = analogy, failed transfer for this direction; Pich-Santhanam = useful analogy needing a transfer theorem.

## 8. Roles, next steps
1 Lower-Bound Lead: state B* precisely (PV/EF-provable correctness) and test independence literature (Razborov, Krajicek on feasible provability of P=NP).
2 Circuit Builder: encode the multisign hypergraph DAG as an R and prove it p-simulates (or is p-equivalent to) resolution/PC, so it is not stronger than a system with known L.
3 Certificates: families surviving PC+CP simultaneously; record size and space.
4 Resource Auditor: define space as peak live nodes; verify DAG size/space tradeoff vs Ben-Sasson-Nordstrom.
5 Red Team: attack Lemma 3(ii) quantifier handling and Lemma 4's uniformity.

## Stale / overstated claims found
None in the files consulted; note: any corpus text suggesting a soft bridge plus a known lower bound would contradict Lemma 3(ii).

Sources: https://arxiv.org/pdf/2304.14702 ; https://theoryofcomputing.org/articles/v022a004/ ; https://www.cs.toronto.edu/~toni/Papers/frege.pdf ; https://eccc.weizmann.ac.il/report/2023/199/download

<!-- END_OF_VERIFIED_REPORT::WC::WC-0001 -->
