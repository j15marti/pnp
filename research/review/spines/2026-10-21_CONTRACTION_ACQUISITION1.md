# CONTRACTION-ACQUISITION1: Exact Merge Hardness and Paid Query Budget

Date: 2026-10-21. P vs NP research project.
Status: mathematically proved model-scoped lemmas and finite exact audits. This is **not** a P != NP proof. Independent external review still needed for applications to the project's compiler.

## Connection with previous proof spine

The October 14 resource-contraction target was an iterable transformation of a hypothetical arbitrary polynomial SAT solver A, with time/space recurrence

  t' <= max(11/10,3/5+t/2)
  s' <= max(1/2,s/2).

The limiting pair (6/5,1/2) is forbidden by the Fortnow–Lipton–van Melkebeek–Viglas SAT time-space theorem since beta(6/5)=23/45, giving strict margin 1/90. **No all-input iterable transformation is known**. This research pinpoints an acquisition cost its proposed hash/semantic-state compiler must not omit.

## B1. CoNP-complete exact semantic merging

For 3CNF histories with residual formulas F0(z), F1(z), full continuation equivalence means forall z F0(z)=F1(z). The decision problem is coNP-complete: inequivalence has a witness z, and comparing F against FALSE is equivalent to UNSAT(F).

A particularly simple proper-width-three selector is

S(F)(b,z,u,v) = F(z) AND (b OR u OR v)
               AND (b OR u OR NOT v)
               AND (b OR NOT u OR v)
               AND (b OR NOT u OR NOT v).

At b=0 the residual is always FALSE. At b=1 the residual equals F(z), independent of u,v. Hence merge equality of b=0 and b=1 histories exactly encodes UNSAT(F). This also makes *winning-status equality* coNP-hard when all remaining variables are existentially quantified. The latter is weaker than full Boolean continuation equivalence; two SAT formulas can both be satisfiable but disagree on subsequent restricted assignments.

## B2. Alternation firewall

For arbitrary polynomially alternating QBF games, equality of the *remaining winner bits* of two histories is PSPACE-complete. To reduce TQBF, compare an always-losing branch with a branch containing the input QBF; each outcome can be evaluated in polynomial space. This is a specialization of standard TQBF PSPACE-completeness. P=NP collapses fixed PH levels, **not known to collapse PSPACE**. Thus poly-round WRAPPER strategies cannot be assumed polynomial-time under P=NP merely because SAT becomes polynomial-time.

## B3. Representation-specific positive and negative cases

Exact Boolean-function equivalence for pure 2CNF is polynomial-time, by testing entailment of each other's clauses through 2SAT. Exact equivalence for pure affine equations over GF(2) is polynomial-time using canonical Gaussian row reduction.

Their conjunction has coNP-complete equivalence to FALSE because

ONE3(a,b,c) = (a XOR b XOR c = 1)
 AND (~a OR ~b) AND (~a OR ~c) AND (~b OR ~c),

and Positive One-in-Three SAT is NP-complete. Both components can be individually SAT while the mixed system is UNSAT. The current finite audit independently tests this identity.

## B4. Full charge for merge acquisition

Let A have time exponent t and space exponent s. Let a replacement solver generate at most N^a children of size N^lambda, with N^r local overhead. Suppose it *also* calls A on N^delta merge-validation instances, each of size at most N^gamma. Assuming explicit query buffers and maximum live working-memory exponent h >= max(lambda,gamma), fully charged **upper-bound recurrences** are

  t' <= max(r,a+lambda*t,delta+gamma*t),
  s' <= max(h,lambda*s,gamma*s).

If lambda,gamma<1 and the same bounds apply at each successive transformation, then the certified exponent limits are

  t* = max(r,a/(1-lambda),delta/(1-gamma))
  s* = h.

Only **if** these transformations exist, are all-input correct, closed under iteration, and work on the same RAM model, an eventual t* > 1 with s* < beta(t*) contradicts the published SAT time-space lower bound. With gamma=1, the displayed proof of a contracting upper bound fails, because its paid parent-scale call contributes delta+t. This is not a lower bound against a completely different algorithm that bypasses the call.

For baseline lambda=1/2, a=3/5, r=11/10, h=1/2 and delta=3/5, an additional query size exponent gamma makes the forbidden-region condition fail beyond gamma approximately 0.501912277818. The exact threshold root lies in (0.501912,0.501913) and solves

  250*gamma^3 - 915*gamma^2 + 990*gamma - 298 = 0.

At gamma=0.501 the conditional contradiction still works; gamma=0.502 fails to cross the known forbidden region. Adding N^0.7 queries of N^0.5 size likewise pushes the fixed-point time exponent to 1.4, no longer contradicting beta(1.4).

A stronger candidate numerical contract would use lambda=2/5, a=18/25, r>=28/25, and h=2/5. It still has fixed-point time exponent 6/5 but the space margin becomes 23/45 - 2/5 = 1/9 instead of 1/90. **This is stricter on child size and child count and has not been constructed.**

## Finite audit record

contraction_acquisition_audit.py: 16,384 exhaustive selector assignment checks across all 256 subsets of the eight full-width three-variable clauses; 3 small QBF selector controls; exact Fraction recurrence tests and gamma threshold bracket.

continuation_fragments_audit.py: 450 pairs of arbitrary 2CNFs independently compared with truth tables, 450 affine pairs compared with truth tables, and all 1,024 five-variable 3-uniform hypergraph subfamilies checked for ONE3 correspondence (476 SAT, 548 UNSAT). A four-variable four-triple example is SAT in both separate components, UNSAT jointly.

Local report SHA-256: 7a324f7a0b9d37c1ea4cb77a34df0fc135e02de9ccbf0c3ae6f32878942fc8bf
Archive SHA-256: 7247e59b42f3438166da5ba275e5c5aa8eea50022aaad22383145f214e71a55c

## Next objective

Construct or disprove an all-input *solver-dependent* and recursively closed splitter, with semantic equivalence acquisition, query materialization, response combination, input access and simultaneous working memory all charged. Search only for interfaces that maintain a strict (t*,s*) forbidden-region margin. Do not count exponential histories, hash collisions, or proof-system lower bounds as arbitrary SAT execution lower bounds.

### Sources
- Fortnow, Lipton, van Melkebeek, Viglas (JACM 2005), Time-Space Lower Bounds for Satisfiability, https://lance.fortnow.com/papers/files/tst.pdf
- Arora and Barak, Computational Complexity: A Modern Approach, TQBF PSPACE-completeness, https://theory.cs.princeton.edu/complexity/spacechap.pdf
- Schaefer (STOC 1978), The Complexity of Satisfiability Problems.
- Existing project reports: SUPERLOG-MARKOV1, October 14 resource-contraction report, Saturation and Projection with Charged Access.
