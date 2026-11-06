# Worst-case derivation-cost programme — living log

Canonical repo: j15marti/pnp. Append a dated entry each run; never rewrite old entries.
Status labels: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.
**P versus NP remains OPEN. Nothing here proves a lower bound.**

## Shared directive (restated from the 2026-11-06 scheduled prompt)

Roles: General SAT Lower-Bound Lead; SAT-Circuit Reduction Builder; Hypergraph & Proof Certificates;
Time-Space Resource Auditor; Independent Proof Red Team.

Common quantity, for a fixed inference system R over a multisigned DAG-hypergraph encoding of 3-SAT:

    W_R(N) = max_{F in UNSAT, |<F>| <= N}  min_{pi : F |-_R bot}  cost_R(pi)

The inner min is taken over all derivations, with the choice of best derivation free (finding it
can only add work, so omitting that cost is sound for a lower bound on executing it).
Priority bridge B_R:  SAT in P  ==>  W_R(N) <= poly(N).
Secondary: pointwise and worst-case simulation theorems.
Test every hard family against resolution, algebraic (PC/IPS), circuit compression, shared DAGs, strategy switching.

---

## 2026-11-06 run 1 — logical analysis of the bridge B_R

### Result 1 (PROVED/EXACT, elementary): B_R is equivalent to (P != NP) or (W_R poly)
B_R is an implication with hypothesis "SAT in P". Hence
  B_R  <=>  (SAT not in P)  OR  (W_R <= poly).
Consequences:
* If P != NP, B_R holds vacuously for every R, so proving B_R unconditionally is at least as hard as
  proving that P = NP implies W_R poly, i.e. a *simulation theorem* under the hypothesis P = NP.
* The programme "B_R + superpolynomial W_R  ==>  P != NP" is logically valid but the two halves are
  jointly equivalent to the target: (B_R and W_R superpoly) => SAT not in P by modus tollens, and
  conversely P != NP makes B_R free. So B_R carries no independent content; all content is in the
  simulation "P = NP => W_R poly" for the specific R. This is the honest reading of "weakest sufficient bridge".

### Result 2 (PROVED/EXACT): the bridge cannot hold for weak R
For R = resolution (tree or DAG), W_R is exponential (Haken 1985; Urquhart; Ben-Sasson–Wigderson) and
unconditional. So B_Res is equivalent to P != NP, not a theorem. The same holds for every R with a known
unconditional exponential lower bound (Res, PC over fields, cutting planes, bounded-depth Frege).
Hence "R sufficiently powerful" must mean: R is not known to be separated from the trivial systems below.

### Result 3 (PROVED/EXACT, standard): what "fixed R" must satisfy for B_R to be provable
Suppose SAT in P via algorithm A. The system R_A (proof = empty string; verifier runs A on F) is a sound,
complete, polynomial-time-verifiable proof system for UNSAT with proofs of size 0. So some system has
W small; but R_A depends on A, while R must be fixed in advance.
* If R p-simulates (or polynomially simulates on UNSAT) every poly-time proof system -- i.e. R is
  (p-)optimal -- then SAT in P ==> W_R poly. (KNOWN THEOREM direction: simulate R_A.)
* Existence of a (p-)optimal system for TAUT is OPEN (Krajíček–Pudlák 1989: implied by NE=coNE / E=NE;
  Messner: under P=NP optimal acceptor <=> p-optimal system). So the sufficient condition "R optimal"
  is itself a famous open problem; no concrete system (Frege, EF, ZFC-style) is known optimal.
* For concrete R = EF: B_EF follows if EF proves, with poly-size proofs per length, the correctness of
  *some* polynomial-time SAT algorithm (provable in PV/S^1_2 => short EF proofs, Cook 1975;
  Krajíček–Pudlák). If SAT is in P but every correct algorithm's correctness is independent of
  PV/EF, B_EF could fail. Whether P=NP => EF polynomially bounded is, to my knowledge, OPEN; a primary
  reference was not located in this run's search (CANDIDATE reading; verify in Krajíček, *Proof Complexity*, 2019).

### Result 4 (KNOWN THEOREM): polynomial boundedness <=> NP=coNP
Cook–Reckhow 1979: a polynomially bounded proof system for UNSAT exists iff NP = coNP. Thus
"W_R superpoly for a fixed R" can never by itself give P != NP; it gives only that R is not polybounded.
To get SAT not in P from a derivation-cost bound the lower bound must hold for a class of R closed under
simulation by all R_A, i.e. it must be a bound for *all* proof systems (=> NP != coNP => P != NP) or the
bridge B_R must be proved for the specific R. No route avoids one of these two heavy ingredients.

### Consequences for the five roles (actionable)
1. Lower-Bound Lead: the only non-circular target is a *simulation* theorem "P=NP => W_R poly" for an R
   that is not known to be weak; candidates are R that internalise reflection for polynomial-time
   machines (EF + uniform reflection is no longer fixed-strength: Pudlák's reflection hierarchy).
   Alternatively prove W_R superpoly for EF (open, a major problem in itself).
2. Reduction Builder: the combined inference system must be closed under adding "run machine M_i"
   inference steps with a budget; such R is p-optimal only if soundness of M_i is checkable -- it is not.
   Document this as the obstruction (soundness of an unchecked acceptor).
3. Hypergraph/Certificates: families hard for Res/PC/CP (Tseitin on expanders, PHP, random 3-CNF at
   threshold) are known hard only for weak R; they are easy for EF in the PHP/Tseitin cases
   (Cook–Reckhow; Buss). They cannot witness superpoly W_R for R at EF strength.
4. Resource Auditor: charge cost_R as total encoded proof length (bits) with DAG sharing counted once;
   peak memory of verification = pathwidth/space of the DAG; both are polynomial in |pi| for Frege-like R.
5. Red Team: attack targets -- (a) any claim that W_R superpoly for a *weak* R implies SAT not in P
   (FALSIFIED: Result 2); (b) any claim of B_R without a reflection/simulation lemma (FALSIFIED: Result 1).

### Literature check (this run)
* Krajíček–Pudlák 1989, Messner, Köbler–Messner–Torán: optimal-system equivalences (background; consistent with Result 3).
* Egidy, arXiv 2602.02294 (2026): oracle constructions on (p-)optimal proof systems -- relativizing constructions, so no
  help to a non-relativizing bridge; not read in full.
* Pich–Santhanam (EF and circuit lower bounds) and arXiv 2405.02232 (iEF, #P not in FP/poly conditional on non-boundedness):
  these show *non*-polynomial-boundedness of concrete systems has circuit-complexity consequences, i.e. the
  direction W_R superpoly => circuit lower bound, the reverse of the needed bridge.
* No 2025–2026 result located that proves a superpolynomial EF lower bound or the bridge. Not independently verified beyond abstracts.

### Status table
| Item | Status |
|---|---|
| B_R equivalent to (P!=NP or W_R poly) | PROVED/EXACT |
| B_Res false-unless P!=NP (indeed exponential Res LB) | PROVED/EXACT |
| R optimal => B_R | KNOWN THEOREM |
| Existence of optimal R | OPEN |
| B_EF | OPEN |
| W_EF superpolynomial | OPEN |
| P != NP | OPEN |

### Next-run targets
* Formalise the multisigned DAG-hypergraph derivation system and give its Cook–Reckhow verifier explicitly, then
  determine where it sits in the simulation order (Res < PC/CP < Frege <= EF).
* Test whether the proposed system p-simulates EF (then lower bounds are as hard as EF lower bounds) or is
  p-simulated by Frege (then hard instances must beat Frege).
* Locate the primary reference for "P=NP => EF polybounded?" (Krajíček 2019, ch. 21/ Cook–Nguyen).
