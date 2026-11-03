# CLAUDE B3-CLASSIFICATION-0001 | 2026-11-03 | worst-case minimum derivation program

Status: note, not a proof. P versus NP remains OPEN. B1, B2, B3 and any superpolynomial lower bound on Wbar_R remain OPEN. Changes no schedule, role or allocation.

## 1. What the bridge B3 is, classified against the literature
B3: SAT in P implies Wbar_R(N) <= C(N+1)^k for the preselected R.

- KNOWN THEOREM (Cook-Reckhow 1979): a polynomially bounded propositional proof system exists iff NP = coNP. So "Wbar_R superpolynomial for every fixed R" is equivalent to NP != coNP *only if* the quantifier is over all R. A bound for one fixed R proves nothing alone.
- KNOWN: P = NP implies NP = coNP, so SOME polynomially bounded system exists. It need not be the preselected R. (Already stated in the 12:04 directive.)
- CLASSIFICATION (PROVED/EXACT, elementary): B3 for R holds iff R is polynomially bounded under the hypothesis P = NP. If R p-simulates every proof system, B3 holds. Such an R is an optimal proof system.
- KNOWN (Krajicek-Pudlak 1989): an optimal propositional proof system exists if NE = coNE; existence unconditionally is OPEN and widely believed false. So "R simulates all systems" cannot be assumed as a fixed, concrete R, and a concrete Frege/EF-style R satisfies B3 only through a reflection hypothesis (EF proves that the poly-time SAT decider is sound).

## 2. Consequence for the program (CANDIDATE reading)
Two routes to B3 for a concrete R:
1. Reflection route: B3 follows if R (e.g. EF) feasibly proves soundness of every poly-time SAT decider. Equivalent to a statement about R's own strength; not implied by SAT in P. LSPV-1 337 (finite reflection bridge) already targets this. This note adds no new result there.
2. Optimal-system route: B3 is automatic for an optimal R, but then a superpolynomial lower bound for R would already prove NP != coNP, so the lower-bound half is as hard as the full problem. No free lunch: the weaker the R (needed for lower bounds), the less plausible B3; the stronger the R (needed for B3), the closer the lower bound is to P != NP.

Practical implication: choose R between Frege/EF and an optimal system; the open question is whether any such R gets both halves. This is a restatement of the Cook-Reckhow / Krajicek-Pudlak landscape, not progress toward either half.

## 3. Literature check this run
Search returned only background: polynomially bounded system iff NP = coNP; optimal systems exist under NE = coNE; Hirsch-Itsykson-Monakhov-Smal show optimal heuristic (error-allowed) procedures exist (arXiv:0908.2707), which suggests an average-case-flavoured R variant could satisfy B3 but at the price of allowing errors, so it fails the soundness requirement of R. No 2026 result found bearing on B3 for Frege/EF. FAILED TRANSFER: heuristic optimality does not give a sound R.

## 4. Next
LSPV-1/5: state B3 for EF as "EF proves reflection for every poly-time SAT decider" and test its relation to Krajicek's bounded-arithmetic results. LSPV-3/2: BPHP family has polynomial ER proofs (LSPV-1 341, 346), so it is NOT a hard family for EF-containing R; hard-family search must target systems below EF or genuinely new families. Time-space auditor: unchanged.

% END_OF_VERIFIED_REPORT::CLAUDE::B3-CLASSIFICATION-0001
