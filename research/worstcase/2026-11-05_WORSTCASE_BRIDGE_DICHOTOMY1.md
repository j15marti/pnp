<!-- WORSTCASE REPORT::WC-0001::2026-11-05 -->
# WC-0001: Worst-case derivation cost, and a dichotomy for the bridge SAT∈P ⇒ W̄_R(N) ≤ poly(N)

Status of P vs NP: **OPEN**. Nothing here proves a lower bound. This run shows which version of the bridge can be non-circular.

## 0. Setup (matches the shared directive)
W̄_R(N) = max over UNSAT F with |⟨F⟩| ≤ N of min over refutations π of F in R of cost_R(π). Strategy search is free, so the min is the existential witness.
Bridge: **B_R : SAT∈P ⇒ W̄_R(N) ≤ poly(N).** R is a fixed inference system on the multisign DAG hypergraph. It is fixed *before* the decider is chosen. cost_R is size, work, or (time, peak space).

## 1. Results (labels strict)
**T1 (PROVED/EXACT, standard).** Suppose R is poly-time verifiable (π checkable in time poly(|π|+|F|)) and complete. Then W̄_R ≤ poly ⇒ UNSAT∈NP ⇒ NP=coNP. This is Cook–Reckhow. The free-search clarification is exactly NP-style nondeterminism: min over π is the coNP witness size. So superpolynomial W̄_R for strong R is at least as hard as NP≠coNP, which implies P≠NP. The program is a sufficient route, strictly harder than P≠NP.

**T2 (PROVED/EXACT, dichotomy).** Let R be any poly-time-verifiable system.
- (a) *Weak R* — superpolynomial lower bound already known (resolution, cutting planes, bounded-depth Frege, etc.). Then B_R is *equivalent* to SAT∉P, i.e. to P≠NP, because its conclusion is known false. Proving B_R for such R is proving P≠NP. **The bridge is circular for every system with a known lower bound.**
- (b) *Strong R* — no lower bound known (Frege, extended Frege). B_R is not circular, but it is not known unconditionally. It needs: "a poly-time SAT algorithm M yields poly-size R-proofs". The standard route is that M's correctness is *provable inside R* (PV / S¹₂-style). The hypothesis SAT∈P gives no such provability. Not established.

Proof of (a): B_R ∧ (W̄_R superpoly) ⇒ ¬(SAT∈P). Conversely P≠NP does not follow vacuously, so "B_R" is in effect "SAT∉P" restated. ∎

**T3 (KNOWN THEOREM, literature).** Obtaining R with B_R from the weakest hypothesis amounts to an *optimal/p-optimal proof system*: a system that simulates all others. Krajíček–Pudlák (1989): TAUT has p-optimal proof systems iff an almost-optimal algorithm for TAUT exists. Existence of an optimal system is open. Cook–Krajíček: with advice, optimal systems exist (and match extended-Frege-style extensions). Messner: under P=NP, optimal acceptor ⇔ p-optimal system. Sources: [Wikipedia: Propositional proof system](https://en.wikipedia.org/wiki/Propositional_proof_system), [Cook slides](https://www.cs.utoronto.ca/~sacook/slidesPrint.pdf), [arXiv 2506.16956](https://arxiv.org/pdf/2506.16956). Implication for us: B_R for a fixed explicit R is a statement of the same strength as a conditional optimality claim, not an easy transfer lemma.

**T4 (CANDIDATE, weakest non-circular bridge to pursue).**
B*_R : "SAT decided by M in time T(N), with R-provable correctness of M ⇒ W̄_R(N) ≤ poly(T(N))." This is the standard simulation (Cook, Krajíček) for R = EF. For R = hypergraph-DAG system R_H the missing piece is **R_H p-simulates EF** (or the trace of a RAM computation with extension variables). Then B*_{R_H} reduces to a provable-correctness hypothesis. Unconditional proof of the premise from SAT∈P alone is *not* available — that is the open arrow.

**T5 (COMPUTATIONAL, sanity check).** `experiments/worstcase/min_res_dag.py` computes exact minimum DAG-resolution refutation steps for the complete CNF on n variables: n=1,2,3 give 1, 3, 7 = 2ⁿ−1 (runtime <1 s). Matches the known tree/DAG bound for the complete formula. This is a harness check; the complete formulas are not hard instances (size ~ n·2ⁿ, proof linear in N).

## 2. Consequences for the five roles
1. *Lower-Bound Lead:* abandon proving B_R for any system with a known lower bound (circular, T2a). Target B*_{R_H} with R_H ⊇ EF-simulation, or state a transfer theorem whose hypothesis includes provable correctness.
2. *Reduction Builder:* prove R_H p-simulates EF (extension / definitional hyperedges on the multisign DAG), with cost accounted as size and peak width.
3. *Certificates:* hard UNSAT families for R_H *without* extension (analogue of Haken/Ben-Sasson–Wigderson) are useful only as evidence about weak fragments; flag as non-bridge.
4. *Resource Auditor:* check cost_R includes verification time (poly), encoding length, and peak space; confirm T1 applies (poly-time verifier).
5. *Red Team:* attack T2a/T4: find an R where B_R holds non-circularly with no lower bound known, or a flaw in treating "free search" as coNP witness.

## 3. Literature clues checked this run
Cook–Reckhow equivalence; Krajíček–Pudlák optimal systems; Cook–Krajíček advice; Messner under P=NP; recent proof-analysis paper arXiv 2506.16956. No source gives an unconditional bridge. Barrier transfer: this is proof-complexity ⇔ NP vs coNP; natural proofs/relativization not yet audited for this route (OPEN audit).

## 4. Open load-bearing arrows
(i) superpoly W̄_R for strong R; (ii) B*_R premise from SAT∈P; (iii) R_H ⊇ EF simulation. P≠NP not proved.

Duplication note: root main.tex and LSPV ARC/FLMV spine were not re-read this run; this report does not modify main.tex or any ownership region.
<!-- END_OF_VERIFIED_REPORT::WC::WC-0001 -->
