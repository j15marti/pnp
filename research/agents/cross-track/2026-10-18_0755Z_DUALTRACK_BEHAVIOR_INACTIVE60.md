# DUAL-TRACK BEHAVIOR-INACTIVE60
Date: 2026-10-18
Status: Track B scoped exact theorems and counterexample, independent review pending. P versus NP OPEN. Track A unchanged/open.

## PROPOSE

1. Test the prior inactive-chain normalization hope: inactive -> separable/product, local pruning, or rank<=4 resolved relation.
2. If false, identify the exact residual object hidden from rank<=4 closure.
3. Replace syntactic inactivity by a chain-behavior quotient: two local chain states are equivalent when every residual predicate on that chain has the same truth value.
4. Charge low-cardinality behavior quotients directly as exact branches that eliminate the entire 3-variable chain.
5. Reframe the remaining hard case by combining MIXEDRANK-CLOSE59 with behavior-quotient density.

## PROJECT / LITERATURE CHECK

Project source used:
- the maximal selected-clause interaction catalogue: every nonselected 3-clause has pattern 3, 2+O, 1+O+O, 2+1, 1+1+O, or 1+1+1; O+O+O is excluded by maximality;
- after the first separator, binary clauses have patterns 2, 1+O, or 1+1;
- main2 MED-ELIM1 / WIDTHCLOSE1 / CLAUSECHAR1 / ACTIVE-DENSITY1;
- RANK2-CLOSE57, RANK34-CLOSE58, MIXEDRANK-CLOSE59.

Primary context:
- Williams, Gomes, Selman, IJCAI 2003, strong backdoors to tractable subsolvers.
- Abbasizanjani and Kullmann, 2020, classification of minimally unsatisfiable 2-CNFs via weak double cycles. This confirms that Krom obstructions can have arbitrarily long implication structure; it is contextual, not needed for the elementary counterexample below.

## THEOREM 1: SELECTED CHAINS FORM A STRONG KROM BACKDOOR

At the maximal variable-disjoint selected-clause stage, every remaining residual clause contains at least one selected-chain variable; otherwise an all-outside 3-clause could be added to the selected family.

Therefore, after assigning all selected-chain variables, every remaining clause has width at most two on outside variables.

So the selected chain variables form a strong backdoor into Krom/2-CNF.

Equivalently SAT can be written as:
choose one satisfying local state for every selected chain, then test the induced outside formula by polynomial-time 2-SAT.

This does not make the search over chain states polynomial; it identifies the exact tractable residual class.

## COUNTEREXAMPLE 2: LONGPATH-INACTIVE

For r>=2 selected chains T_0,...,T_{r-1}, choose one designated local literal a_i on each chain and introduce private outside variables y_1,...,y_{r-1}. Define

P_r =
(a_0 OR y_1)
AND product_{i=1}^{r-2}(a_i OR NOT y_i OR y_{i+1})
AND (a_{r-1} OR NOT y_{r-1}).

Then

exists y_1,...,y_{r-1} P_r
iff
a_0 OR a_1 OR ... OR a_{r-1}.

Proof:
- if all a_i=0, the first clause forces y_1=1, each middle clause propagates y_i=1 -> y_{i+1}=1, and the last clause forces y_{r-1}=0, contradiction;
- if a_j=1, set y_1,...,y_j=1 and y_{j+1},...,y_{r-1}=0, with the obvious endpoint conventions. Every clause is satisfied.

Every proper-subset projection of the a_i relation is full: for any assignment on a proper subset, choose an omitted a_j=1. Thus the exact projected relation has no nontrivial constraint on any proper subset of the r chains.

Consequences for r>=5:
- no rank<=4 chain-only relation exists;
- every individual chain retains all seven local type-1 states, so there is no local pruning;
- nevertheless the chains are globally non-product, because the all-false tuple is forbidden.

Hence the hoped-for implication
inactive -> separable OR locally pruned OR rank<=4 relation
is FALSE.

The obstruction is an unbounded-rank implication-path relation.

## EXACT CHARACTERISTIC OF THE LONG CLAUSE

For a positive designated literal on a positive type-1 chain, the local falsifying-set Schur quantity in CLAUSECHAR1 is a=5/9 and t=7/3.

For the r-chain projected clause OR_i a_i,

lambda_r = [ (7/3)^r - (5/9)^r ]^(-1).

Relative to r independent type-1 chains,

g_r = (3/7)^r / lambda_r
    = 1 - (5/21)^r.

Thus every fixed r gives strict DLS credit, but the gain tends exponentially to zero as r grows. One long path of rank r=Theta(n) cannot provide a fixed exponential-base improvement by characteristic credit alone.

This is a hostile control, not a hardness theorem; P_r itself is structurally simple.

## THEOREM 3: CHAIN BEHAVIOR QUOTIENT

Let D_T be the seven satisfying states of selected type-1 chain T.
Let P_T be the finite set of all local Boolean predicates on T that occur in residual clauses after ordinary cleanup (literal predicates and any explicitly retained local multi-literal predicates).

Define s ~_T s' iff
P(s)=P(s') for every P in P_T.

Let q_T be the number of equivalence classes.

For any set S of selected chains, branch only on one behavior class for each T in S. This costs exactly product_{T in S} q_T branches.

Once a behavior class is chosen:
- every occurrence of T in every residual clause has a fixed truth value;
- the base type-1 clause is satisfiable by definition of the class;
- all three private variables of T can be existentially removed without selecting an exact local state.

Therefore each branch eliminates all 3|S| chain variables exactly and leaves a CNF of width at most three on the remaining variables. No branch duplicates semantic possibilities because the classes partition D_T.

Hence, if an exact 3-SAT algorithm runs in O*(c^n), quotienting S first gives

T(n) <= [product_{T in S} q_T] c^(n-3|S|).

## COROLLARY 4: TWO-BEHAVIOR CHAINS ARE STRICTLY FAVORABLE

For q_T<=2, one chain contributes relative factor

2/c^3.

At Liu's reference c_L = 1.3279235672158634...,

2/c_L^3 = 0.8541040081... < 1.

Thus any linear number of two-behavior chains yields a strict exponential improvement over the Liu reference recurrence.

The LONGPATH-INACTIVE gadget is exactly such a case when each chain is used only through its designated literal a_i: q_T=2. So the long-path counterexample kills the naive low-rank normalization, but it is not a surviving worst-case obstruction after behavior quotienting.

## SHARPENED REMAINING TRACK B CORE

Combine MIXEDRANK-CLOSE59 with the behavior quotient.

Any asymptotic worst-case family that avoids a strict improvement must simultaneously satisfy:

1. active resolved-chain density nu_act/nu -> 0, otherwise MIXEDRANK-CLOSE59 gives exp(-Omega(nu)) gain;
2. two-behavior-chain density -> 0, otherwise BEHAVIOR-INACTIVE60 gives factor (2/c_L^3)^(Omega(nu));
3. therefore almost all selected chains are inactive with respect to the rank<=4 resolved hypergraph AND have at least three distinct behavior classes under their residual predicate signatures.

This is a substantially narrower target than "inactive-dominant".

NEXT TARGET: DIVERSE-INACTIVE61.
Classify type-1 chains with q_T>=3. Determine whether positive density of such behavior-diverse inactive chains forces:
- a bounded-rank relation after cheap constant-width closure,
- a favorable branching recurrence using their multiple local predicates,
- or a bounded-depth/backdoor-depth decomposition of the conditional Krom residual.

The Krom implication graph and minimally-unsatisfiable 2-CNF weak-double-cycle structure are natural tools for this next step.

## TRACK A

No load-bearing Track A implication changes. Recent Partial-MCSP and Sigma/QBF work remains diagnostic. The missing theorem is still an A-relative hereditary fractional contractor with genuinely smaller encoded SAT calls and full same-machine accounting.

END_BEHAVIOR_INACTIVE60_READBACK
