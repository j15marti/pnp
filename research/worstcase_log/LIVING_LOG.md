# Living log: worst-case minimum-derivation programme

Quantity: Wbar_R(N) = max over UNSAT F with |<F>|<=N of min over R-refutations pi of cost_R(pi).
Optimal derivation is granted free (search cost only adds work, so it is dropped from a lower bound).
Weakest sufficient bridge B3: SAT in P  =>  Wbar_R(N) <= poly(N).
**P versus NP remains OPEN.** Nothing below is a proof of any separation.

Entries are append-only; newest last. Detailed reports live in research/agents/*, research/main/*, research/coordination/*.

## 2026-11-03 scheduled run
**Corpus state found (not re-derived).** Fixed calculus R_mix341 (RES, AND3, XOR, CONVERT, VARDEF; source axioms cost 0, derived nodes cost 1, shared nodes once).
Closed negatives: pointwise simulation TR(Res) false (Tseitin/expander, LSPV-1 334); disjoint-copy amplification false, Wbar monotone under adding axioms (REFEREE305); selector-guarded Peitl composition has 7k-1 <= W <= 10k-1, so it is not a superpolynomial family (LSPV-4 352). Open: B1/B2/B3 for R_mix341, and any superpolynomial family against it.
Sufficient bridge on record (LSPV-1 336): if R is size-optimal (p-simulates every Cook-Reckhow system) then B3 holds. Existence of optimal systems is OPEN (Krajicek-Pudlak 1989).

**Literature check.** Egidy, "Recursive Jump Operators and Optimal Proof Systems", ICALP 2026: builds an oracle with infinite PH, no optimal proof system for TAUT and no recursive jump operators. Consequences, stated as OBSERVATIONS (my reading, not claims of the paper):
1. Optimality of a fixed R cannot be established by a relativizing argument; so the "optimal R => B3" route needs non-relativizing input.
2. This does NOT bar B3 itself: in a world with P != NP the hypothesis of B3 is false and B3 is vacuous. B3 is only informative where P=NP, and there it needs Wbar_R polynomial, so a superpolynomial lower bound for R must fail relative to oracles with P^A=NP^A. This matches the black-box firewall already in REFEREE296.
Also noted: Messner (via Egidy): every NP set has an optimal proof system; for NP=coNP, complex sets with optimal systems exist. No result found that P=NP makes a specific natural system such as Extended Frege polynomially bounded; that implication is not known to me and is not assumed anywhere.

**Status.** No new theorem this run. No change to any status label. Next gap (unchanged): an interacting-component hard family against R_mix341 that defeats selector decomposition, with a certified excess over the 7k-1 style source-count lower bound; independently, the weakest direct proof of B3 for a fixed R.
