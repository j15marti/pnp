# DUAL-TRACK RANK2-CLOSE57
Date: 2026-10-17
Status: P versus NP OPEN. Track B scoped exact theorem; Track A unchanged/open.

## PROPOSE COMBINATIONS

Track B:
1. Combine MINCOVER-DLS56 with the existing five local center-predicate costs from LOCALPATTERN-BRANCH1.
2. Exploit the proper width-3 constraint: if a rank-2 clause uses two literals on the center chain, its leaf side has only one literal, so the leaf true-branch DLS ratio is at most 16/21 rather than 20/21.
3. Use the resulting star thresholds to replace the astronomical generic rank<=4 high-incidence threshold by a small explicit threshold for the rank-2 active core.
4. Pair the high-degree star branch with the standard maximal-matching gain in the bounded-degree case.

Track A:
No new separation implication is claimed here. The current Sigma/QBF work is treated only as a red-team reminder that local challenge responses and parent-size SAT calls do not yield fractional contraction.

## SEARCH / DUPLICATION CHECK

Project sources checked: main2.tex RESOLVE-HYPERMATCH, LINK-DICHOTOMY1, LOCALPATTERN-BRANCH1, CLAUSECHAR1; MINCOVER-DLS56; HUBBRANCH54; BICLIQUE-LEDGER55.
No existing project report was found with the 274-neighbor rank-2 closure or the threshold table below.

Primary literature checked:
- Sixue Liu, ICALP 2018, DOI 10.4230/LIPIcs.ICALP.2018.88, for the BR/DLS chain framework.
- Tsukiyama, Ide, Ariyoshi, Shirakawa, SIAM J. Comput. 1977, DOI 10.1137/0206036, for output-polynomial maximal-independent-set enumeration, hence minimal-vertex-cover enumeration.

## DECLARED MODEL

Let G be the simple support graph of the active rank-2 resolved core. Vertices are disjoint positive type-1 chains. For each unordered pair of chains with at least one non-tautological rank-2 resolved clause, retain one representative clause. All other original clauses remain in the final SAT check.

Every representative edge e=TU has the form

    Q_e(T) OR R_e(U),

where Q_e and R_e are nonempty disjunctions of one or two signed literals on their respective 3-variable type-1 chains. Proper width <=3 implies that if |Q_e|=2 then |R_e|=1, and conversely.

From the existing exact local table, the DLS ratio for requiring a local predicate true is:
    1+   : 16/21
    1-   : 5/7
    2++  : 20/21
    2+-  : 19/21
    2--  : 33/35.

For an arbitrary one-literal predicate the worst ratio is 16/21.
For an arbitrary one-or-two-literal predicate the worst ratio is 20/21.

The existing worst rank-2 resolved-clause characteristic is lambda=81/440 versus independent 9/49, hence one disjoint resolved edge has relative DLS factor 440/441.

## THEOREM 1: EXACT STAR FACTORIZATION

Suppose p representative edges incident to one center chain T have the same exact center predicate Q(T) and distinct leaf chains U_1,...,U_p:

    AND_i ( Q(T) OR R_i(U_i) ).

Then exactly

    AND_i (Q OR R_i) = Q OR AND_i R_i.

This is the K_{1,p} instance of MINCOVER-DLS56. Search the two branches:
(A) require Q true;
(B) require every R_i true.

All original clauses remain checked in each terminal search, so arbitrary additional constraints do not invalidate the upper bound.

Let a(Q) be the true-branch DLS ratio for Q. Let beta be an upper bound on every leaf true-branch ratio. The star contributes at most

    S_Q(p) = a(Q) + beta^p

times the independent-chain baseline.

For a one-literal center, beta <= 20/21.
For a two-literal center, proper width <=3 forces one-literal leaves, so beta <=16/21.

Exact threshold table:

    center Q     beta       least p with S_Q(p)<1
    1+           20/21      30
    1-           20/21      26
    2++          16/21      12
    2+-          16/21       9
    2--          16/21      11

The worst star branch is therefore finite and small: 30 spokes for a fixed one-positive-literal center pattern, and at most 12 spokes for any fixed two-literal center pattern.

## THEOREM 2: DEGREE 274 FORCES A FAVORABLE STAR

On one fixed type-1 center chain there are exactly:
- 3 coordinate-specific 1+ predicates,
- 3 coordinate-specific 1- predicates,
- 3 coordinate-pair 2++ predicates,
- 6 coordinate-pair 2+- predicates,
- 3 coordinate-pair 2-- predicates.

If no local center predicate reaches its favorable star threshold, the number of distinct-neighbor representative edges incident to T is at most

    3(30-1)+3(26-1)+3(12-1)+6(9-1)+3(11-1)
    = 87+75+33+48+30
    = 273.

Therefore

    deg_G(T) >= 274

forces a subset of incident edges with one common exact center predicate whose MINCOVER star factor has strict DLS ratio below 1.

This improves the generic rank<=4 incidence threshold only in the declared rank-2 support-graph model; it does not replace the broader LINK-DICHOTOMY theorem.

## THEOREM 3: RANK2-CLOSE57 DICHOTOMY

Let nu be the number of active vertices in the simple rank-2 support graph G.

Case A: Delta(G) <=273.

Every active vertex has degree at least one, so M>=nu/2. A greedy maximal matching in a simple graph of maximum degree Delta contains at least

    M/(2Delta-1)

edges, since selecting one edge deletes at most 2Delta-1 edges. Hence at Delta<=273,

    |matching| >= nu / 1090.

Credit one representative resolved clause on each matched pair. The pairs are chain-disjoint, so the rank-2 characteristic gains multiply. The terminal DLS ratio is at most

    (440/441)^(nu/1090)

relative to treating all nu active chains independently.

Equivalently, at least a 1/545 fraction of active chains is covered by credited rank-2 blocks.

Case B: Delta(G)>=274.

Theorem 2 supplies an exact favorable star branch with strict local DLS ratio below 1.

Thus every nonempty active rank-2 resolved core in the declared model has either:
- an explicit positive-density disjoint matching gain, or
- an explicit favorable high-degree star branch.

There is no remaining local spread-versus-concentration escape inside this rank-2 support-graph model.

## EXACT ARITHMETIC AUDIT

Thresholds were recomputed with exact rational arithmetic:
- 1+: p=30
- 1-: p=26
- 2++: p=12
- 2+-: p=9
- 2--: p=11.

The worst previous values are still >=1 at p-1 and <1 at the listed p.
The total no-favorable-star degree cap is exactly 273.
At Delta=273 the matching lower bound is |M*|>=nu/1090 and covered fraction >=1/545.

No finite experiment is used as evidence for the asymptotic theorem; these are exact identities and counting bounds.

## CONSEQUENCE FOR TRACK B

The rank-2 active residual case is now closed at the local DLS/branching level with far smaller constants than the generic rank<=4 sunflower route.

The highest-value remaining Track B task is no longer rank-2 concentration. It is:
1. propagate rank-2 closure, rank-3/4 hypermatching, HUB/LOCALPATTERN rules, local pruning, and MINCOVER factoring through the exact residual forms produced by Liu Algorithm 4;
2. prove that inactive or broader residual cases are either easy/handled or receive a quantified gain;
3. solve the complete BR/DLS balance with corrected chain types and stop/overshoot accounting.

The current global base candidates remain OPEN until that integration is completed.

## TRACK A STATUS

No load-bearing Track A arrow changes.
P=NP -> polynomial SAT decider is ESTABLISHED.
Arbitrary solver -> fully charged hereditary smaller-instance contraction is OPEN.
Conditional recurrence -> FLMV forbidden endpoint remains conditional/known algebra plus known lower bound.
The current Sigma2/Sigma3 observations add no contraction because their straightforward witness extraction uses parent-size SAT calls and can have coefficient >=1 on the unknown solver exponent.

END_RANK2_CLOSE57_READBACK
