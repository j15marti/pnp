# Living log: worst-case derivation cost (DAG / multisigned hypergraph route)

Status of P vs NP: **OPEN**. Nothing below proves a lower bound. Append-only; newest entry last.

## Entry 1 — 2026-11-05 12:50 UTC (Claude, scheduled run)

### Setup (CANDIDATE formalization)
W(N) = max over UNSAT F, |F|<=N, of min over derivations pi: F |-_R bot of cost_R(pi).
Strategy discovery is not charged (min is a pure combinatorial quantity). cost_R >= |pi| (size), so
a bound on cost needs a bound on size.

### Lemma A (PROVED/EXACT, elementary): the bridge cannot be weaker than P != NP for a system with a known lower bound
Let B(R) denote: SAT in P => W_R(N) <= poly(N).
(i) If W_R is already known superpolynomial (e.g. R = resolution, Haken; cutting planes for some families),
    then B(R) is logically equivalent to "SAT not in P". Proving B(R) = proving P != NP. No progress.
(ii) If W_R's growth is unknown (Frege, Extended Frege), B(R) is equivalent to
    "P = NP => R is polynomially bounded". Since P = NP => NP = coNP => *some* system is poly bounded,
    B(R) is a statement that R is "optimal under P = NP". That is a Krajicek-Pudlak-type optimality
    claim; it is not known for any natural R.
(iii) Natural sufficient route: if the correctness of a given poly-time SAT algorithm is provable in the
    theory associated with R (e.g. PV/ S^1_2 for EF) then R is p-bounded by reflection. But the algorithm is
    unknown, so a fixed R must prove correctness of ALL candidate algorithms uniformly; that is not available
    (it would be an optimality/ reflection property, cf. the open conjecture that no optimal system exists
    unless e.g. NE = coNE).
Consequence: the "weakest sufficient bridge" is exactly an R-optimality statement under P = NP. The
research load therefore splits into (L) an unconditional lower bound for R and (B) the conditional
bridge; (B) is as hard as proving R is optimal-under-P=NP, and (L) for EF/Frege is open (best known: quadratic).
Hybrid note: both together imply P != NP, so each is individually at least as hard as an open problem
except possibly one of them; no free lunch via choice of R.

### Lemma B (PROVED/EXACT): free strategy choice cannot help the upper-bound side
Charging nothing for the search only lowers W; so a lower bound on W (the target) is the strongest version
and the bridge's consequent W <= poly is the weakest requirement on the algorithm side. No loss in generality.

### Literature check (this run)
- Krajicek survey: optimal proof system existence still open; Frege lower bound only Omega(n^2).
- arXiv 2506.16956 (rev. May 2026): Proof Analysis Problem for EF is NP-complete; P=NP gives automatability of
  any proof system. Relevant: under P=NP, EF is *automatable* from a short proof, but this does not bound
  proof size, so it does not give B(EF).
- arXiv 2506.20221 (rev. Mar 2026): bounded-arithmetic route to NP != coNP, conditional on a model-theoretic assumption.
Classification: analogy/CANDIDATE, no transfer theorem found.

### Open arrows
1. Any unconditional superpolynomial lower bound for a system R for which B(R) is plausible (EF/Frege): OPEN.
2. B(R) for such R: OPEN, equivalent to optimality-under-P=NP.
3. Hostile-control tests (resolution, algebraic, shared DAGs, adaptive switching) have not been run this entry.

### Next
- Formalize "multisigned hypergraph DAG" as a concrete R and check whether it p-simulates, or is p-simulated by, Res/PC/EF
  (needed to place it relative to Lemma A).
- Time-space audit: define cost = (time, peak space) for derivation execution; state cost vs size separation.

END_OF_LOG_ENTRY::1
