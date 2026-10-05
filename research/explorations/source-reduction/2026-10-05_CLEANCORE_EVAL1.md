# CLEANCORE-EVAL1 — Universal Response Evaluators for the Low-Degree Externally Mediated Clean Core

**Date:** 2026-10-05  
**Repository:** `j15marti/pnp`  
**Global status:** **OPEN. P versus NP remains open.**

This note tests the SRAS-RANDOM-REPLAY1 proposal on the current low-degree externally mediated clean-core model from the Liu/type-1-chain branch.

The experiment asks whether a post-commitment challenge family on the clean core admits a compact reusable **universal response evaluator**, which would defeat a replay/freshness lower-bound attempt.

---

## 1. Clean-core mediator model

Let \(X\) denote the variables belonging to bare type-1 chains. Each chain has seven locally satisfying states.

Let \(Y\) be outside mediator variables. For a mediator \(y\in Y\), suppose all clauses containing \(y\) have the form

\[
A_{y,i}(X)\vee y,
\qquad i\in P_y,
\]

or

\[
B_{y,j}(X)\vee \neg y,
\qquad j\in N_y,
\]

where each \(A_{y,i}\) and \(B_{y,j}\) is a disjunction of two chain literals from distinct clean chains.

This is the pure external-mediator pattern used by the current branch rule.

Let

\[
F(X,Y)
=
F_{\rm chain}(X)
\wedge
\bigwedge_{y\in Y}
\left[
\bigwedge_{i\in P_y}(A_{y,i}\vee y)
\wedge
\bigwedge_{j\in N_y}(B_{y,j}\vee\neg y)
\right].
\]

A natural random/replay challenge commits \(F\), later presents a complete assignment \(x\) of one of the seven satisfying local states to every chain, and asks whether \(x\) is compatible with some assignment to all mediators.

---

# 2. MED-ELIM1 — exact mediator elimination theorem

**Status: PROVED/EXACT for the displayed mediator model.**

For one mediator \(y\),

\[
G_y(X,y)
=
\bigwedge_{i\in P_y}(A_i(X)\vee y)
\wedge
\bigwedge_{j\in N_y}(B_j(X)\vee\neg y).
\]

Then

\[
\boxed{
\exists y\,G_y(X,y)
\iff
\left(\bigwedge_{i\in P_y}A_i(X)\right)
\vee
\left(\bigwedge_{j\in N_y}B_j(X)\right).
}
\]

Equivalently, by distributivity / Davis-Putnam resolution,

\[
\boxed{
\exists y\,G_y(X,y)
\iff
\bigwedge_{i\in P_y}
\bigwedge_{j\in N_y}
\left(A_i(X)\vee B_j(X)\right).
}
\]

### Proof

If \(y=0\), every positive-\(y\) clause requires \(A_i=1\), while every negative-\(y\) clause is automatically satisfied.

If \(y=1\), every negative-\(y\) clause requires \(B_j=1\), while every positive-\(y\) clause is automatically satisfied.

Therefore some value of \(y\) works exactly when all \(A_i\)'s are true or all \(B_j\)'s are true.

The pairwise-CNF form follows from

\[
\left(\bigwedge_i A_i\right)\vee\left(\bigwedge_j B_j\right)
\equiv
\bigwedge_{i,j}(A_i\vee B_j).
\]

\(\square\)

---

## 3. Size consequence

Let

\[
d_y=|P_y|+|N_y|
\]

be mediator degree and suppose \(d_y\le\Delta\).

Eliminating \(y\) creates at most

\[
|P_y||N_y|
\le
\frac{d_y^2}{4}
\le
\frac{\Delta d_y}{4}
\]

width-at-most-4 resolvents.

If \(M\) is the total number of mediator-clause occurrences, then all mediators can be eliminated using at most

\[
\boxed{
\frac{\Delta M}{4}
}
\]

raw resolvents.

Thus for constant low mediator degree \(\Delta\), the complete chain-assignment compatibility function has a linear-size CNF evaluator after mediator elimination.

More strongly, the direct evaluator does not need to materialize the resolvents: for each \(y\), test

\[
\left(\bigwedge_i A_i(x)\right)
\vee
\left(\bigwedge_j B_j(x)\right).
\]

Hence the complete challenge can be answered in

\[
\boxed{O(M)}
\]

time after reading the challenged chain states.

This is a source-transparent compact universal evaluator.

---

# 4. Canonical mediator witness

The same calculation gives a canonical mediator assignment.

For each \(y\):

- if all \(A_i(x)\) are true, choose \(y=0\);
- otherwise compatibility implies all \(B_j(x)\) are true, so choose \(y=1\).

Thus on every compatible complete chain challenge, an exact canonical mediator witness is computable in \(O(M)\) time.

Therefore SAME_REALIZATION-style challenge/response binding to the formula does not make the natural full-state response expensive in this mediator model.

---

# 5. Consequence for fresh random challenges

Let the clean-core formula be committed before a fresh challenge \(x\) is revealed.

Stopping-time freshness can ensure that the particular \(x\) was not predictable from the prior computation.

Nevertheless MED-ELIM1 supplies a single reusable evaluator

\[
E(F,x)
\]

of linear size/time in the explicit mediator incidence description.

Therefore:

\[
\boxed{
\text{fresh unpredictable complete chain-state challenge}
+
\text{exact mediator compatibility response}
}
\]

does **not** yield a replay or acquisition lower bound on the low-degree mediator core.

This is an exact negative result for this natural challenge family.

---

# 6. Partial-restriction challenges

A stronger challenge can reveal only some chain states and ask whether the partial assignment extends to a complete satisfying clean-core state.

After MED-ELIM1 this is exactly satisfiability of the residual bounded-width chain formula.

That can remain computationally nontrivial.

However this does not by itself create a P-vs-NP contradiction:

- under the counterfactual \(P=NP\), each such residual SAT query is polynomial-time;
- polynomially many adaptive fresh challenges remain polynomial under the earlier PCLOSE/RANDCLOSE/ROUNDABSORB closures;
- demanding a canonical completion is likewise selectable under \(P=NP\) by ordinary SAT self-reduction / fixed-PH search.

Therefore the partial-challenge route simply moves the original SAT difficulty into the response evaluator rather than producing a new independent lower-bound resource.

---

# 7. Finite decision-diagram experiment

A reproducible experiment was added at

`experiments/source_reduction/clean_core_universal_evaluator.py`.

For each \(k=3,\ldots,8\):

- use \(k\) type-1 chains;
- generate \(2k\) outside mediators;
- mediator degree is uniformly sampled from \(2,\ldots,4\), always with both polarities;
- each mediator clause couples literals from two distinct chains;
- use five deterministic seeds;
- eliminate mediators exactly;
- simplify duplicate/subsumed resolvents;
- build a reduced ordered 7-ary decision diagram for the complete compatibility function;
- sample up to 40 chain orders and record the best node count.

For \(k=3,4\), the script also exhaustively verifies equality between direct existential mediator evaluation and eliminated-CNF evaluation over all \(7^k\) complete chain states.

All 20 exhaustive theorem checks passed.

Raw results:

`results/source_reduction/2026-10-05_clean_core_universal_evaluator.csv`

---

## 8. Aggregate finite results

| chains \(k\) | response table \(7^k\) | mean simplified CNF clauses | mean best sampled MDD nodes | max best sampled MDD |
|---:|---:|---:|---:|---:|
| 3 | 343 | 8.8 | 13.4 | 15 |
| 4 | 2,401 | 14.2 | 34.4 | 38 |
| 5 | 16,807 | 16.8 | 86.0 | 118 |
| 6 | 117,649 | 22.8 | 213.6 | 305 |
| 7 | 823,543 | 27.0 | 420.4 | 474 |
| 8 | 5,764,801 | 33.4 | 938.8 | 1,168 |

The sampled best-MDD means over these six sizes fit approximately

\[
1.16\,(2.33)^k,
\]

with an excellent finite log-linear fit.

This is **not** an asymptotic theorem.

The important point is the mismatch:

\[
\boxed{
\text{sampled MDD size appears to grow rapidly}
}
\]

while simultaneously

\[
\boxed{
\text{the same exact response function has an }O(k)
\text{-scale CNF/direct evaluator in these experiments.}
}
\]

Therefore even strong MDD growth would not be representation-independent evidence of response hardness.

This is a clean analogue of the earlier ACRTREE1 warning.

---

# 9. SRAS interpretation

For the natural complete challenge, the clean core falls squarely into

\[
\boxed{\mathrm{UNIVERSAL\ EVALUATOR}}
\]

rather than HARD-EVAL.

The evaluator is obtained by bounded-degree mediator elimination or by the direct per-mediator formula

\[
\left(\bigwedge_i A_i\right)
\vee
\left(\bigwedge_j B_j\right).
\]

Thus:

- freshness blocks challenge-specific precomputation;
- provenance ties the challenge to the same committed formula;
- but a compact global authority answers every challenge after it is revealed.

No reacquisition debt accumulates.

---

# 10. New structural lesson

Low mediator degree is algorithmically double-edged.

It defeated the previously certified high-degree branching threshold, but it also makes **single-mediator elimination cheap**.

The remaining difficulty is therefore not the mediator variable itself.

After eliminating all low-degree mediators, the hard object is the induced bounded-arity constraint system among chain states.

In other words,

\[
\boxed{
\text{outside mediator complexity}
\longrightarrow
\text{chain-interaction CSP complexity}.
}
\]

Any successful lower-bound/evaluator experiment should now target the global interaction structure of the eliminated constraints, not mediator replay.

Natural structural parameters include:

- treewidth/pathwidth of the chain interaction hypergraph;
- expansion;
- separator profile;
- communication matrices across balanced cuts;
- circuit/branching-program complexity of the extension predicate;
- whether the induced 7-state CSP falls into a tractable polymorphism/algebraic class.

---

# 11. Revised next target

The next challenge family should not ask only complete compatibility.

Define

\[
\operatorname{EXT}_F(\rho)=1
\]

iff a partial chain-state restriction \(\rho\) extends to a satisfying assignment of the eliminated clean-core CSP.

Then search for compact reusable evaluators of the entire extension map

\[
\rho\mapsto\operatorname{EXT}_F(\rho).
\]

However this must be treated carefully:

- proving a large OBDD/MDD does not rule out circuits or other representations;
- under \(P=NP\), a polynomial SAT algorithm itself is a polynomial evaluator for each extension query;
- therefore an SRAS-strength result must establish a representation-independent source/summary barrier, not merely decision-diagram growth.

A promising finite diagnostic is to correlate extension-evaluator size with interaction-graph treewidth/expansion while simultaneously testing XOR, 2-SAT, bounded-treewidth and independent-product controls.

---

# 12. Strict status

## PROVED/EXACT
- MED-ELIM1.
- linear-time direct evaluator for complete chain-state compatibility in the displayed mediator model.
- canonical mediator witness construction.
- constant-degree linear-size eliminated CNF bound.
- exhaustive equality checks for the tested \(k=3,4\) instances.

## COMPUTATIONAL
- random clean-core MDD measurements for \(k=3,\ldots,8\).
- finite approximate \(2.33^k\) best-sampled-MDD growth.

## FALSIFIED/RETIRED FOR THIS NATURAL CHALLENGE
- fresh complete chain-state challenges force expensive mediator replay.
- mediator response-signature diversity is a lower bound on evaluator size.
- MDD growth alone is representation-independent hardness.

## OPEN
- compact evaluator complexity of the partial-extension map.
- representation-independent no-sharing theorem for eliminated chain CSPs.
- arbitrary-polynomial-SAT-decider to SRAS challenge compiler.
- nonrelativizing/nonalgebrizing hinge.
- final \(P\ne NP\) separation.

---

## Bottom line

For the low-degree externally mediated clean core, the first universal-response-evaluator test finds a **compact escape**, not a lower bound:

\[
\boxed{
\exists Y\,F(X,Y)
\text{ can eliminate each low-degree pure mediator locally.}
}
\]

This sharply redirects the SRAS program. The possible hard resource is not “remembering the mediator history.” It is the global extension problem of the induced chain-state CSP after all cheap mediator elimination has already been credited.
