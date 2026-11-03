# Living log: worst-case derivation cost W_R(N) and the SAT∈P ⇒ W_R ≤ poly bridge

Target: W_R(N) = max over UNSAT F (|F|≤N) of min over derivations π of F in R of cost_R(π).
Status of P vs NP: **OPEN**. Nothing below proves a lower bound.

## Entry 2026-11-03 (scheduled run, Claude)

### Literature check (one standard search; no full-text reading of the items below)
- Cook–Reckhow 1979 (KNOWN THEOREM): a polynomially bounded propositional proof system exists iff NP = coNP.
- arXiv 2506.16956 (2025): deciding whether a proof is optimal for Extended Frege is NP-complete; it notes P = NP makes every proof system automatable. Automatable means a proof can be found in time poly(shortest proof size). It does not mean short proofs exist.
- Papamakarios (2024): depth-d Frege is NP-hard to automate.
- ECCC TR26-055 (Davis–Robere, Apr 2026), "Res(log) Proves Bounded-Depth Frege Lower Bounds": only the title and part of the abstract were seen. It concerns bounded-depth Frege, not general Frege.
- No source found claims a superpolynomial lower bound for general Frege or Extended Frege.

### Observation (PROVED/EXACT, elementary)
Fix a proof system R with a polynomial-time verifier and cost = proof size.
Write B_R for the bridge "SAT ∈ P ⇒ W_R(N) ≤ poly(N)".

1. W_R is a nondeterministic certificate measure: the optimal sequence is chosen for free. So "W_R ≤ poly" says R is polynomially bounded. By Cook–Reckhow this implies NP = coNP.
2. If R has an unconditional superpolynomial lower bound (Resolution, bounded-depth Frege, cutting planes on known families), then B_R is *equivalent to* SAT ∉ P. The antecedent would have to be refuted. So B_R is not a weaker bridge for these R. It is P ≠ NP in disguise.
3. If R is strong enough that B_R has a *simulation* proof, B_R can be proved by formalizing "algorithm M decides SAT correctly" inside R. That needs R to carry the correctness proof of M, so a superpolynomial lower bound on W_R would again imply SAT ∉ P. The lower bound is then at least as hard as P vs NP. Known cases:
   - Extended Frege. EF plus the claim that M is a correct SAT solver is not a fixed poly-time-verifiable system. The correctness statement is itself a Π₁ claim.
   - Time-based cost. If cost_R is the time of the best deterministic computation, B_R is tautological and W_R = SAT time.
4. Consequence (CONDITIONAL on the structure above): the "weakest sufficient bridge" is informative only for an R that satisfies two conditions at once.
   - (i) R has no known unconditional lower bound, so it is plausible that W_R is superpolynomial.
   - (ii) P = NP gives poly-size R-proofs without assuming the conclusion.

   No such R is known. The natural candidates are EF and Frege, and proving B_EF is the "does P = NP imply EF proves its own algorithm correct" question from bounded arithmetic. That question is OPEN. Krajíček's work on feasible/uniform proof size is the relevant literature.

### Task allocation for next runs (additive; no schedule change)
- General lower-bound lead: write B_R precisely for EF and decide whether it follows from a bounded-arithmetic hypothesis (e.g. "P = NP is provable in S¹₂/PV"). Record this as a CONDITIONAL bridge.
- Circuit/inference builder: build a combined system whose lower bounds do not collapse to Resolution. Check each family against item 2.
- Hypergraph/certificates: for each hard family, tag which systems already give an unconditional exponential bound (so B_R for them equals P ≠ NP).
- Resource auditor: check that cost accounting (size vs. time vs. space) matches the quantifier in W_R.
- Red team: attack item 3 and look for an R satisfying both (i) and (ii).

### Not claimed
No superpolynomial lower bound on W_R for any strong R. No proof of B_R for any R without a lower bound. P vs NP remains OPEN.
