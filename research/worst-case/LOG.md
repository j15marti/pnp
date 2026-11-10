# Worst-case derivation-cost living log

Directive: `research/coordination/2026-11-10_WORST_CASE_DERIVATION_COST_DIRECTIVE.md`.
Status vocabulary per AGENTS.md. **P versus NP remains OPEN.** Newest entries at the bottom.

---

## 2026-11-10 entry 1 — triage of the bridge B_R

Notation: Wbar_R as in the directive; "p-bounded" = Wbar_R(N) <= poly(N) (length measure).
B_R := (SAT in P => Wbar_R poly).

### Corpus reviewed
AGENTS.md; GROKPROOF/2026-11-10_0415_PROGRESS.md (restricted results, open arrows
P2-A2/B1/B2/D1); research/coordination knot/link handoff; existing R_mix341 / FLMV references
by title only. Nothing in the repo previously states B_R or the equivalence below in this
form (searched "worst-case", "W_R(N)"). No contradiction with root OPEN status found.

### Results

**L1 (PROVED/EXACT, elementary).** B_R is equivalent to the disjunction
(P != NP) OR (Wbar_R poly).  Proof: SAT in P is equivalent to P = NP; implication A => C is
equivalent to (not A) or C. QED.
Consequences:
- (a) If R has an unconditional superpolynomial bound (Resolution, PC, cutting planes on
  suitable families — Haken, Urquhart, Ben-Sasson–Wigderson, Pudlák, Razborov; KNOWN THEOREMS),
  then B_R is *equivalent to P != NP*. A bridge for such R is not a weaker target; it is the
  goal itself. These R are useless as the "fixed system" for the bridge.
- (b) For R with no known lower bound (Frege, Extended Frege), B_R is implied by P != NP and,
  combined with a lower bound, yields P != NP. The program is therefore exactly the
  Cook–Reckhow program (KNOWN: Wbar_R superpoly for some R iff NP != coNP) with the extra
  requirement of a *specific fixed R*. Free knowledge of the optimal derivation is exactly the
  Cook–Reckhow "exists a short proof" quantifier; no change.
- (c) A superpolynomial lower bound on Wbar_R for R = EF would already give NP != coNP (hence
  P != NP) with no bridge needed. The bridge route is worthwhile only if a lower bound for the
  fixed R is easier than a general NP != coNP argument; no known technique supports that.

**L2 (PROVED/EXACT, standard Cook/Krajíček argument).** Suppose A is a polynomial-time
algorithm that decides SAT and R has the closure properties of Extended Frege (substitution,
modus ponens, poly-size circuit evaluation). If R has polynomial-size proofs of the
propositional soundness statements Sound_A(n) ("A rejects F, |F|<=n  =>  F unsatisfiable"),
then Wbar_R is polynomial. Proof: instantiate Sound_A(n) at F, derive the poly-size evaluation
trace of A(F)=reject, detach. QED. (Equivalent first-order form: PV proves "A is sound".)
So the *weakest sufficient transfer theorem* reduces to a **uniform reflection requirement**:
for the (non-explicit) correct algorithm A, R must prove A's soundness in polynomial size.
CANDIDATE: no known route constructs this for unknown A; a proof that R = EF proves soundness
of every correct polynomial SAT solver would amount to an optimality statement for EF
(Krajíček–Pudlák optimal-proof-system conjecture is believed false in general, so such a
statement is suspicious; it is only needed conditionally on P = NP, which is the loophole).

**L3 (CONDITIONAL/CANDIDATE).** Define R_T = {(e, T-proof of Sound_e)} for a theory T (T = PV
gives EF-level). Under P = NP, R_T is p-bounded iff some correct polynomial solver e has a
T-proof of its soundness. Thus the bridge for this universal fixed system is equivalent to
"P = NP implies PV (or T) proves P = NP via an explicit algorithm". Whether PV proves P = NP
conditional on its truth is open; independence-type results (Cook–Krajíček; Pich–Santhanam;
Chen–Li–Oliveira, LMCS 2025: IS^1_2 cannot prove SAT needs co-nondeterministic n^k circuits)
show provability of *lower bounds* is constrained, but there is no result excluding B_{R_T}.

### Hostile-control ledger (role 3/5)
Known hard families vs. combined system (Res + GF(2) + counting + extension):
- Tseitin on expanders: hard for Res; poly in GF(2)/PC (Gaussian elimination). Dies.
- Pigeonhole: hard for Res/PC; poly Frege (Buss), poly cutting planes. Dies.
- Clique-coloring, random k-CNF: hard for Res/CP/PC; no super-poly bound known for
  Frege/EF. Open — these are the only live candidates and are subject to the same barriers.
No known family survives EF; this is KNOWN-state of the art, not a new claim.

### Time-space auditor note (role 4)
cost_R as length is what L1–L2 use. If cost = (time, peak space), L2 still holds with the
evaluation overhead poly(N) in time; space for substitution/evaluation of A is poly(N) but a
space-bounded cost measure (e.g. clause-space) is not captured by EF length and needs a
separate bridge — OPEN. Do not conflate with FLMV time–space spine without a charged link.

### Red-team note (role 5)
Failure modes to test next: (i) any claimed lower bound that is really a lower bound for a
non-p-simulating sub-system (Res-like) — by L1(a) it cannot feed the bridge; (ii) uses of
"min over sequences" that implicitly bound the *search* — fine for lower bounds, invalid for
upper bounds; (iii) natural-proofs/algebrization/relativization: a combinatorial width/size
argument that works for random 3-CNF against EF would be a strong-circuit-lower-bound-type
statement via feasible interpolation failing under crypto (Krajíček–Pudlák; Bonet–Pitassi–
Raz), so it must not rely on interpolation.

### Literature checked this run
- Pich–Santhanam: it is essentially trivial that some system is non-p-bounded iff NP != coNP;
  EF-unprovability of circuit lower bounds implies P != NP (conditional on EF non-p-bounded).
- Chen–Li–Oliveira, LMCS Sept 2025, unconditional unprovability in IS^1_2 (fixed-poly).
- Proof Analysis Problem, FOCS 2025: PAP for EF is NP-complete; P = NP implies automatability
  of any proof system (relevant to proof *search*, not to the bound on Wbar_R).
- Cook–Krajíček: PV <-> EF translation (PV |- f=g gives poly EF proofs).
Classification: all are ANALOGY/CANDIDATE or KNOWN THEOREM for stated models; none gives B_R.

### Status
No superpolynomial lower bound for any R that is not already below Frege. No proof of B_R for
any R with an open status. The load-bearing arrows (lower bound for a strong fixed R;
uniform reflection of unknown solvers) are OPEN. P versus NP remains OPEN.

### Next target
Role 1/2: formalise L2 with explicit closure axioms for R_mix341 and test whether R_mix341
(extension + GF(2) + counting) meets them, i.e. whether it p-simulates EF. If it does not,
B_{R_mix341} for the "P=NP" side is not even reducible to L2 and the system is too weak to
be the fixed system; if it does, the lower bound is an EF lower bound and Cook–Reckhow-hard.

% END_OF_ENTRY 2026-11-10-1
