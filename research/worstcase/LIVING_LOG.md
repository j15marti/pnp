# Worst-case derivation-cost programme — living log

Target quantity: W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi).
Weakest sufficient bridge under study: (B_R)  SAT in P  =>  W_R(N) <= poly(N).
Status: P vs NP remains OPEN. Nothing below proves a lower bound for any R.
Strategy-discovery work is not charged (min over pi is free), as directed.
Append-only below; newest entry last.

## Entry 2026-11-09 (scheduled run, single agent covering all five roles)

### Literature check
- Optimal / p-optimal propositional proof systems: existence still open
  (Krajicek-Pudlak 1989; see ICALP 2026 recursive-jump-operator paper, LIPIcs vol 374, art. 88;
  arXiv 0908.2707 for randomized optimal semidecision procedures).
- A polynomially bounded proof system exists iff NP = coNP (Cook-Reckhow 1979).
- Automatizability does not give optimality; no automatizable optimal system is known.
- No new result found that settles B_R for a concrete R.

### Results (all PROVED/EXACT, elementary; derived this run, checked by hand)
Setup: R is a Cook-Reckhow system (proofs poly-time checkable), cost_R = proof size
(DAG-shared). Any cost that is >= |pi| only strengthens lower bounds.

**P1 (circularity for known-weak R).** Let R have an unconditional superpolynomial
lower bound (resolution, cutting planes, bounded-depth Frege, ...). Then the consequent of B_R
is false, so B_R is equivalent to "SAT not in P", i.e. P != NP. A hard-instance family
for such R therefore cannot be a route to P != NP via B_R. FIRST consequence: the
"survives resolution" test is necessary for a hard family but proves nothing about B_R.

**P2 (single-R lower bound vs. NP != coNP).** W_R superpoly for one R implies NP != coNP
only if R is p-optimal (or, for the weaker "optimal" notion, optimal up to poly). Otherwise
a different system may be bounded. Hence B_R with a lower bound for R gives P != NP only
through the bridge, and for R = eF or stronger the bridge itself is the unresolved content.

**P3 (what B_R needs).** If P = NP via algorithm A and R (equivalently its theory) proves
"A is sound" in a form instantiable per formula (e.g. PV proves soundness of A), then R
is p-bounded, so B_R holds along A. Without that provability, B_R is only known
if R is optimal. So the weakest *known* sufficient hypotheses for B_R are:
  (i) R optimal (open, Krajicek-Pudlak), or
  (ii) uniform provability in R's theory of soundness of every poly-time SAT solver
       that is in fact correct (a reflection scheme; not known true for eF).
Neither follows from SAT in P alone. This is the missing transfer theorem, now stated sharply.

**P4 (equivalence).** (exists R: W_R poly) <=> NP = coNP. And SAT in P => NP=coNP => such an R
exists (not nec. a fixed named one). So the real object is the *existential* statement; any
bridge naming a fixed R carries extra reflection content (P3).

### Consequences for the five roles
- Lower-Bound Lead: target must be stated for a system satisfying (i) or (ii), otherwise P1 applies.
  Candidate fixed system: eF + uniform reflection for poly-time SAT solvers; need to check whether
  adding that scheme keeps verification poly-time (it does if the scheme is added as checkable
  axiom instances, but then proofs must supply the solver, i.e. circularity with P2). OPEN.
- Circuit/Reduction Builder: any "fixed combined inference system" that p-simulates eF is
  a candidate; shortest-DAG certification must be done relative to that system.
- Hypergraph/Certificates: hard UNSAT families must resist eF-type reasoning, not only
  resolution/algebraic; no such unconditional family exists (open; = eF lower bounds).
- Resource Auditor: time-space cost >= size, so lower bounds on size transfer; upper bounds
  need peak-memory audit — none done this run.
- Red Team: attack surface = (a) P1 circularity, (b) hidden use of an optimal-system assumption
  in any proposed transfer proof, (c) charging for the verifier's reading of the solver.

### Next concrete target (T-REFL)
Decide whether "SAT in P => eF (or eF+reflection) is poly-bounded" is known to be
equivalent to a recognised open statement (p-optimality of eF / Krajicek-Pudlak conjectures),
by comparing with Krajicek-Pudlak 1989 and Khaniki-style recent bounded-arithmetic results.

Not claimed: any new lower bound; any proof of B_R; any resolution of P vs NP.
