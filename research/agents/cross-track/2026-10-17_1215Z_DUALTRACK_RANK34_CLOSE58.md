# DUAL-TRACK RANK34-CLOSE58
Date: 2026-10-17
Status: P versus NP OPEN. Track B scoped exact theorem, independent review pending. Track A unchanged/open.

## PROPOSE COMBINATIONS

Track B:
1. Extend RANK2-CLOSE57 to rank-3 and rank-4 resolved support hypergraphs using repeated center concentration.
2. At each concentration level branch on the common center predicate and charge the false branch by the already-proved rank-(r-1) resolved-clause DLS factor.
3. Use simple-support representatives so that after fixing r-1 center chains, distinct residual hyperedges have distinct final leaf chains.
4. Pair the high-degree branch with a maximal hypermatching gain in the bounded-degree case.

Track A:
Treat the current Sigma2/Sigma3 circuit work only as a red-team source unless it yields genuinely smaller encoded SAT calls. Parent-size calls retain coefficient >=1 on the unknown solver exponent and do not instantiate the fractional contractor.

## SEARCH / DUPLICATION CHECK

Project sources checked: main2.tex CLAUSECHAR1, HYPERMATCH-DENSITY1, LINK-DICHOTOMY1, LOCALPATTERN-BRANCH1; MINCOVER-DLS56; RANK2-CLOSE57; HUBBRANCH54; current Sigma red-team reports.
No project artifact was found containing the explicit thresholds D3=1001089 or D4=38686455361.

Primary literature checked:
- Sixue Liu, ICALP 2018, DOI 10.4230/LIPIcs.ICALP.2018.88, for BR/DLS and chain covering characteristics.
- Thomas Eiter and Georg Gottlob, SIAM J. Comput. 24(6), 1995, DOI 10.1137/S0097539793250299, for hypergraph minimal transversals and bounded-rank output-polynomial subcases. The present proof does not require a generic transversal enumerator; it uses explicit bounded-rank link concentration.

## DECLARED RESOLVED MODEL

For r=3 or 4, let H_r be the simple r-uniform support hypergraph of active resolved clauses on disjoint positive type-1 chains. Keep one representative non-tautological resolved clause per support. All original clauses remain checked by the terminal SAT search.

For rank 3, every representative has one signed literal on each of its three support chains.
For rank 4, every representative has one signed literal on each of its four support chains.

Use the existing exact worst resolved-clause DLS factors:
    g2 = 440/441
    g3 = 9236/9261
    g4 = 193856/194481.

For forcing one signed literal on one type-1 chain true, use the worst local ratio
    alpha = 16/21.
For a negative literal the ratio 5/7 is smaller.

The branch calculations below are conservative: any extra gain from fixing a center predicate false is omitted.

## LEMMA 1: STAR-COMPOSITION

For one common center predicate Q and pairwise chain-disjoint petal predicates R_i,

    AND_i (Q OR R_i) = Q OR AND_i R_i.

If requiring Q true has DLS ratio a and each R_i true has DLS ratio at most b on disjoint petal chain sets, then the two-branch DLS ratio is at most

    a + b^p.

This is exact Boolean factorization plus a conservative DLS upper bound.

## RANK-3 THRESHOLDS

Fix a center chain T. A rank-3 clause through T has one signed literal Q(T) and a rank-2 petal clause on two other chains.

There are six exact one-literal center predicates. If p petal supports are pairwise chain-disjoint:

positive center:
    16/21 + (440/441)^p < 1 first at p=633;
negative center:
    5/7 + (440/441)^p < 1 first at p=552.

Use the uniform first-level threshold p31=633.

If a fixed-Q link graph has no matching of size 633, endpoints of a maximal matching form a vertex cover of size at most
    c31 = 2(633-1)=1264.

Concentrate on one cover chain U and one of its six literal predicates. Clauses sharing fixed literals on T and U have a one-chain leaf. Branch on the rank-2 center clause Q_T OR Q_U. Its true-branch ratio is at most g2. The leaf false-side obligations are single literals of ratio at most alpha.

    g2 + alpha^p < 1

first at
    p32=23.

To force 23 equal U-predicate clauses, U must see at least
    6(23-1)+1 = 133
clauses in the fixed-T-predicate link class.

Thus a fixed T-predicate class of size at least
    1264(133-1)+1 = 166849
forces either the first-level matching branch or the second-level center branch.

Pigeonholing the six T literals gives the rank-3 high-degree threshold

    D3 = 6(166849-1)+1 = 1001089.

### RANK3-CLOSE58

If Delta(H_3) >= 1001089, a strict favorable branch exists by the preceding concentration.

If Delta(H_3) <= 1001088, let nu be the number of active chains and M the number of support hyperedges. Since every active chain has positive degree,
    M >= nu/3.
A greedy maximal matching in a 3-uniform hypergraph of maximum degree Delta has size at least
    M/(3Delta-2),
because one selected edge intersects at most 3Delta-2 hyperedges.
Therefore at Delta<=1001088,
    |matching| >= nu/9009786,
and at least a 1/3003262 fraction of active chains is covered by disjoint rank-3 resolved blocks.
Their terminal DLS ratio is at most
    (9236/9261)^(nu/9009786)
relative to independent type-1 chains.

Hence there is no local spread-versus-concentration escape in the declared rank-3 support-hypergraph model.

## RANK-4 THRESHOLDS

Fix center chain T. A rank-4 representative through T has one center literal and a rank-3 petal clause.

First level, with pairwise disjoint rank-3 petals:
positive center:
    16/21 + (9236/9261)^p < 1 first at p=531;
negative center:
    5/7 + (9236/9261)^p < 1 first at p=464.
Use p41=531.

If the fixed-T-predicate 3-uniform link hypergraph has no matching of size 531, endpoints of a maximal matching give a cover of size at most
    c41=3(531-1)=1590.
Concentrate on one cover chain U and one of its six literal predicates.

Now the common center is a rank-2 clause on T,U, and petals are rank-2 clauses on disjoint chain pairs. A matching of petal pairs of size p gives ratio
    g2 + g2^p.
This first becomes <1 at
    p42=2683.

If no such matching exists, a maximal matching in that link graph gives a cover of size at most
    c42=2(2683-1)=5364.
Concentrate on one further center chain V and one of its six literal predicates.

Now the common center is a rank-3 clause with ratio at most g3, and the leaves are single-chain literals. The branch ratio
    g3 + alpha^p
first becomes <1 at
    p43=22.

Exact reverse pigeonhole accounting:
- to get 22 equal V-predicate clauses requires at least 6(22-1)+1=127 clauses through V;
- to force such a V under a 5364-cover requires at least 5364(127-1)+1=675865 clauses in the fixed T,U-predicate class;
- to force that U-predicate class requires at least 6(675865-1)+1=4055185 clauses through U;
- to force such a U under a 1590-cover requires at least 1590(4055185-1)+1=6447742561 clauses in the fixed-T-predicate class;
- pigeonholing the six T literals yields

    D4 = 6(6447742561-1)+1 = 38686455361.

### RANK4-CLOSE58

If Delta(H_4) >= 38686455361, one of the three center-concentration levels gives a strict favorable branch.

If Delta(H_4) <= 38686455360, then M>=nu/4 and a greedy maximal matching has size at least
    M/(4Delta-3)
    >= nu/618983285748.
Thus at least a 1/154745821437 fraction of active chains is covered by disjoint rank-4 blocks, and the terminal DLS ratio is at most
    (193856/194481)^(nu/618983285748).

Hence there is no local spread-versus-concentration escape in the declared rank-4 support-hypergraph model.

## EXACT ARITHMETIC CHECK

Exact Fraction calculations verify:
rank-3:
- 16/21+(440/441)^633 <1, while p=632 is >=1;
- 5/7 +(440/441)^552 <1, while p=551 is >=1;
- 440/441+(16/21)^23 <1, while p=22 is >=1.

rank-4:
- 16/21+(9236/9261)^531 <1, while p=530 is >=1;
- 5/7 +(9236/9261)^464 <1, while p=463 is >=1;
- 440/441+(440/441)^2683 <1, while p=2682 is >=1;
- 9236/9261+(16/21)^22 <1, while p=21 is >=1.

All displayed degree thresholds follow by exact ceiling/pigeonhole inversion.

## TRACK B CONSEQUENCE

Together with RANK2-CLOSE57, all simple active rank-2, rank-3, and rank-4 resolved support layers now have scoped local closure:
- bounded maximum incidence => positive-density disjoint Hamming-block credit;
- sufficiently high incidence => finite center-concentration branch with strict DLS decrease.

This is a stronger and more structured replacement for the generic enormous LINK-DICHOTOMY threshold, but only inside the declared simple representative support layers.

The principal remaining Track B theorem is now GLOBAL PIPELINE INTEGRATION:
1. prove every residual produced by Liu Algorithm 4 can be normalized into the declared layers or another already-handled form without losing correctness or hidden exponential cost;
2. handle inactive chains and mixtures of ranks without double counting;
3. combine the local gains with the corrected chain catalogue and BR stopping/overshoot;
4. derive and independently verify one strict global base below Liu's published 1.32793-level bound.

The earlier numerical candidate bases remain OPEN until this integration is complete.

## TRACK A STATUS

No separation arrow is promoted.
Current quantified-circuit reports continue to show the same obstruction: straightforward candidate/witness services use parent-size SAT calls or global commitments, giving time exponents such as d+1 or d^2 rather than a coefficient lambda<1 on the unknown SAT exponent.
The required A-relative hereditary fractional contractor remains OPEN.

END_RANK34_CLOSE58_READBACK
