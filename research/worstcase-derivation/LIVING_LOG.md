# Worst-case derivation-cost programme: living log

Repository: `j15marti/pnp`. Append-only; newest entry last. Statuses: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.
**P versus NP remains OPEN. Nothing here is a proof of P != NP.**

## Shared directive (2026-11-09)
Five roles: (1) General SAT Lower-Bound Lead; (2) SAT-Circuit Reduction Builder; (3) Hypergraph & Proof Certificates; (4) Time-Space Resource Auditor; (5) Independent Proof Red Team.
Common object: Wbar_R(N) = max over UNSAT F, |<F>|<=N, of min over refutations pi of F in R of cost_R(pi). The optimal pi is chosen freely (strategy discovery is not charged).
Priority: weakest sufficient bridge  SAT in P  =>  Wbar_R(N) <= poly(N), plus a superpolynomial lower bound for a fixed strong R. Stress hard instances against resolution, algebraic, circuit-compressed, shared-DAG and strategy-switching reasoning. Stronger pointwise / worst-case simulation theorems are secondary.
This directive is additive: it changes no schedules, role ownership or other allocations. Do not claim the lower bound or bridge is established.

## Entry 001 (2026-11-09, Claude, scheduled run)

### Corpus reviewed
Repo tree, AGENTS.md, newest handoffs under research/coordination (knot/link 2026-11-09, LSPV-3/541 DEF-facet). Repo search finds no prior file with this exact W_R formulation. Closest prior material: the world ledger (research/agents/claude/world-ledger, rows on P vs NP equivalents) and the Grok TSR reports. Root main.tex and the other agents' ownership regions were not edited (this run is not an LSPV-owned run).

### Result 1 (PROVED/EXACT, elementary): free strategy = nondeterminism
If R is a Cook-Reckhow system (rules locally poly-time checkable, cost = total encoded length of the derivation DAG, shared lines counted once), then
`Wbar_R(N)` is exactly the worst-case minimal refutation size. "Free optimal sequence" is NP-style nondeterminism, so the lower bound is precisely the proof-size question. Wbar_R is polynomial iff R is polynomially bounded on UNSAT.

### Result 2 (PROVED/EXACT): the bridge is redundant or equivalent to P != NP
Let R be sound and Cook-Reckhow. 
(a) If Wbar_R is superpolynomial, then NP != coNP (Cook-Reckhow), hence P != NP. The bridge is not needed; the lower bound alone suffices.
(b) If Wbar_R is already known superpolynomial (resolution, cutting planes, polynomial calculus in the relevant regimes, bounded-depth Frege), then Bridge(R) := "SAT in P => Wbar_R poly" is logically equivalent to "SAT not in P", i.e. to P != NP. It is provable only by proving P != NP.
(c) So Bridge + LB is a strictly weaker route than LB alone, for every sound Cook-Reckhow R. The bridge can only add value if cost_R is NOT certificate-checkable (steps that call a non-verifiable subroutine, or a cost measure smaller than proof length). That is the exact hypothesis the programme must now justify, or else drop the bridge and target LB(R) for Frege / extended Frege directly.

Consequence for the five roles: for a checkable R, the programme is the Frege/eF lower-bound problem. NP != coNP is implied by any superpolynomial eF bound; that is a famous open problem.

### Result 3 (KNOWN THEOREM, Cook 1975 / Krajicek): the only conditional bridge on the shelf
If SAT has a poly-time algorithm A and a theory T in {PV_1, S^1_2} proves A's soundness (A rejects F => F is unsatisfiable), then eF (translated from PV_1) has poly-size refutations of every UNSAT F. So the uniform/provable form of the bridge for R = eF is "P = NP with PV_1-provable correctness". It is not the unconditional bridge. Related: unprovability of superpolynomial eF lower bounds in PV_1 (model-theoretic; see survey arXiv:2504.04416, to be read in full before citing exact statements).

### Result 4 (KNOWN barrier summary, to be re-verified against sources): hard-instance menu
Random k-CNF with linear clause density is hard for resolution, and for polynomial calculus degree and cutting planes in the literature; Tseitin on expanders is hard for resolution but easy for GF(2) linear algebra (so it fails the "survives algebraic reasoning" test); PHP is hard for resolution and bounded-depth Frege but has poly-size eF proofs (so it fails the "survives circuit compression" test). No family is known hard for Frege or eF. Under factoring hardness, Frege lacks feasible interpolation (Krajicek-Pudlak, Bonet-Pitassi-Raz), which blocks the monotone-interpolation lower-bound method for exactly the systems that matter.

### Literature clues this run
- Krajicek, "A proof complexity conjecture and the Incompleteness theorem", JSL 90 (2025), arXiv:2303.10637: trilemma - no p-optimal proof system, or E not in P/poly, or a p-time function whose range meets every infinite NP set. Relevant to whether a single fixed R can satisfy a bridge (existence of optimal systems is open).
- Krajicek, "On the existence of strong proof complexity generators", arXiv:2208.11642: candidate gadget generators as hard-instance sources for all proof systems.
- Survey on meta-mathematics of complexity, arXiv:2504.04416 (unprovability of eF lower bounds in PV_1 and relation to P=NP).
- No 2025 result found showing "P=NP => eF polynomially bounded" (search was one standard pass; could have missed preprints).

### Role assignments for the next cycle
1. Lower-Bound Lead: decide whether any intended cost measure is non-checkable; if not, restate the target as eF lower bound and say so. Formalize Result 3 with exact quantifiers.
2. Reduction Builder: specify the fixed combined system (resolution + PC + CP + extension) as a Cook-Reckhow system with cost = DAG size; certify shortest derivations on small instances exactly (SAT/DRAT-based minimal proofs for n<=8 variables).
3. Hypergraph/Certificates: for each candidate family record which test it fails (algebra: Tseitin; compression: PHP); propose generator-style (gadget) families as the only live candidates.
4. Time-Space Auditor: verify that the DAG cost model charges line width, rule checking time and peak memory consistently, and that sharing does not hide exponential unfolding.
5. Red Team: try to refute Result 2(b) quantifier handling (e.g., non-uniform R, advice) and find any natural non-checkable cost measure for which the bridge is meaningful.

### Status
Open: LB for any fixed strong R; Bridge for non-checkable cost; every load-bearing arrow of a P != NP proof. P versus NP remains OPEN.

END_OF_ENTRY::001
