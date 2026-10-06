# LEAD-0022 — SAT-native reconvergent wrapper with delayed restriction re-separation

Timestamp: 2026-10-06 12:44 PT  
Agent: LEAD  
Global status: **P versus NP remains OPEN.**

## 1. Goal

Instantiate the reconvergent-diamond wrapper using only SAT-native branch bits and SAT-native delayed re-separation.

The experiment tests the proposed architecture:

1. a node asks an actual restricted-SAT question;
2. answer A/B chooses a different branch-dependent transformation;
3. the branches return to the same nominal control node;
4. later SAT restrictions can distinguish histories that appeared to reconverge;
5. all terminal routes retain the same external SAT semantics.

## 2. SAT-native diamond

Let the current CNF be \(F_i\). At diamond \(i\), choose a legal restriction \(\rho_i\) and compute

\[
\beta_i
=
\operatorname{SAT}(F_i\upharpoonright\rho_i).
\]

The bit \(\beta_i\in\{0,1\}\) is the A/B branch bit.

Choose one of two fixed satisfiability-preserving signed variable renamings

\[
T_{i,0},\qquad T_{i,1},
\]

and set

\[
F_{i+1}
=
T_{i,\beta_i}(F_i).
\]

Both branches then return to the same nominal control node \(D_{i+1}\).

Since signed renaming preserves satisfiability,

\[
\operatorname{SAT}(F_{i+1})
=
\operatorname{SAT}(F_i).
\]

Thus all paths preserve the same external semantic endpoint.

## 3. Full state versus nominal node

At the nominal merge node, the true state is

\[
S_i=(D_i,F_i,g_i,H_i),
\]

where \(g_i\) is the composed signed renaming and \(H_i\) is the realized A/B history.

Two paths that reach the same \(D_i\) but have different \(F_i\) or \(g_i\) have not truly merged computationally.

The experiment therefore measures delayed behavioral equivalence rather than treating nominal node identity as state identity.

## 4. Delayed SAT-native re-separation

For a state \(S_i\), define restriction-service signatures

\[
\Sigma_k(S_i)
=
\left(
\operatorname{SAT}(F_i\upharpoonright\rho)
\right)_{\rho\in\mathcal R_k},
\]

where \(\mathcal R_k\) is the set of all restrictions fixing exactly \(k\) current variables.

Two nominally merged histories re-separate at level \(k\) if their \(\Sigma_k\) values differ.

No provenance/hash query is used in this test. Re-separation occurs only through ordinary SAT restrictions.

## 5. SINGLE-REALIZATION1 — PROVED/EXACT guard

For fixed deterministic \(A\), fixed deterministic wrapper \(W\), and fixed input \(F\), there is exactly one realized control history.

Therefore an exponential family of reconvergent histories cannot be charged to one ordinary run merely because those histories are possible on other inputs or other external seeds.

A many-history merge lower bound must either:

1. range over an input family and establish a genuine branching-program/state lower bound in a declared model; or
2. prove that one state must service multiple future counterfactual restrictions.

The second alternative requires an independently SAT-forced consumer; the wrapper may not invent it for free.

## 6. COMPACT-RENAMING1 — PROVED/EXACT

A signed permutation of \(n\) variables can be represented using

\[
\lceil\log_2(n!)\rceil+n
=
O(n\log n)
\]

bits.

Composition and inversion are polynomial time.

Moreover, signed variable renaming preserves CNF clause count and width.

Hence even if many nominal histories reach pairwise different current formulas, the wrapper-created transformation state has a polynomial-size exact representation.

For \(n=8\), the experiment's simple upper encoding is 24 bits.

## 7. SAT-REPLAY-CLOSE1 — PROVED/EXACT

Assume the hypothetical exact SAT decider \(A\) runs in polynomial time.

For a polynomial-depth reconvergent wrapper, the full realized branch/renaming state at depth \(d\) can be reacquired from the input by replay:

1. recompute the stage-1 restricted-SAT bit with \(A\);
2. apply the corresponding known transition;
3. continue for \(d\) stages.

If \(d=\operatorname{poly}(n)\), this replay is polynomial time.

Thus delayed re-separation does not by itself turn discarded wrapper history into an expensive ordinary-source object.

The same statement is SAT-oracle shadowable.

## 8. WRAPPER-TRANSITION-CLOSE1 — PROVED/EXACT

More generally, let \(W[A]\) have polynomially many stages. At every stage:

- it makes polynomially many calls to \(A\) on polynomial-size instances;
- it applies a polynomial-time branch-dependent transition;
- its explicit state has polynomial length.

If \(A\in P\), then the entire realized wrapper is in \(P\).

Therefore a superpolynomial contradiction cannot come from the wrapper's own polynomial-depth hash/renaming/recursive-looking transition system. It must come from an independently proved lower bound on a SAT-required service that no polynomial representation/replay can supply.

## 9. Exact finite experiment

Configuration:

- \(n=8\);
- 512 input formulas obtained as signed-renaming samples from each base family;
- 10 nominal diamonds;
- each branch bit is an actual SAT answer to a three-variable restriction;
- branch action is one of two signed variable renamings;
- delayed re-separation uses all 1-, 2-, and 3-variable SAT restriction queries.

At depth 10:

| family | branch histories | 1-literal classes | 2-literal classes | 3-literal classes | full function classes | median/max fixed-order OBDD |
|---|---:|---:|---:|---:|---:|---:|
| planted 3-SAT | 217 | 1 | **512** | 512 | 512 | 30 / 37 |
| 2-SAT | 229 | 298 | **507** | 507 | 507 | 10 / 17 |
| Horn | 39 | 1 | 97 | **512** | 512 | **38 / 54** |
| path 3-CNF | 157 | 1 | 511 | **512** | 512 | 25 / 38 |
| 3-XOR CNF | 192 | 16 | 305 | 305 | 305 | 7 / 7 |

Status: **COMPUTATIONAL EXACT for the stated finite instances.**

## 10. SAT-NATIVE-RESEP-CONTROL1 — computational conclusion

The desired phenomenon is real.

For the planted 3-SAT sample at depth 10:

\[
|\{\Sigma_1\}|=1,
\qquad
|\{\Sigma_2\}|=512.
\]

Thus states that are completely indistinguishable by all one-variable SAT restrictions can re-separate maximally when two-variable restrictions are permitted.

However the effect is not hardness-specific.

The Horn control reaches

\[
|\{\Sigma_3\}|=512,
\]

and the 2-SAT control reaches

\[
|\{\Sigma_2\}|=507.
\]

Both are polynomial-time decidable families.

Therefore

\[
\boxed{
\text{large delayed SAT-native re-separation}
\not\Rightarrow
\text{computational hardness}.
}
\]

## 11. OBDD hostile control

The fixed-order reduced OBDD count also fails to track hardness in this experiment.

At depth 10:

\[
\operatorname{medianOBDD}(\text{Horn})=38
>
30
=
\operatorname{medianOBDD}(\text{planted 3-SAT}),
\]

and the Horn maximum is 54 versus 37 for the planted 3-SAT sample.

This is consistent with the literature: residual-subfunction/width arguments yield strong lower bounds only after the computation has been transferred into the corresponding restricted branching-program model.

## 12. Literature alignment

Relevant precedents:

1. Barrington (JCSS 1989): width-5 polynomial-size branching programs capture nonuniform \(NC^1\). Branch-dependent noncommuting function composition can therefore be computationally rich while visible width remains constant.

2. Komarath and Sarma, *Pebbling, Entropy and Branching Program Size Lower Bounds* (TOCT / arXiv:1301.1425): pebbling/entropy lower bounds become strong for explicitly restricted branching-program models such as read-once, thrifty, or bitwise-independent programs.

3. Cook, Edmonds, Medabalimi, Pitassi, ICALP 2016, DOI 10.4230/LIPIcs.ICALP.2016.36: exponential lower bounds are proved for semantic read-once nondeterministic branching programs. The read-once restriction is load-bearing.

These results support the continuation-equivalence viewpoint but also emphasize the missing arbitrary-algorithm transfer.

## 13. Revised load-bearing target

The reconvergent wrapper is useful only if a future SAT service is independently forced and cannot be compactly represented/replayed.

Define a SAT-native continuation service

\[
g_S(\rho)
=
\operatorname{SAT}(F_S\upharpoonright\rho).
\]

A representation \(Q_S\) with evaluator \(E\) is sufficient for query family \(\mathcal R\) when

\[
E(Q_S,\rho)=g_S(\rho)
\qquad
\forall \rho\in\mathcal R.
\]

The required theorem would have to establish both:

### SAT-MERGE-FORCING1 — OPEN
SAT correctness forces one ordinary state/object to support the declared multi-restriction continuation service.

### MERGE-SERVICE-LB1 — OPEN
Every ordinary representation/evaluator for that forced service has superpolynomial acquisition/use cost, even allowing:

- source reread;
- replay;
- arbitrary circuits;
- BDD/DAG sharing;
- algebraic/Gaussian representations;
- memoization;
- alternate coordinate systems.

Without SAT-MERGE-FORCING1, the wrapper has invented a counterfactual service.

Without MERGE-SERVICE-LB1, the service may have a compact evaluator despite many behavioral classes.

## 14. Consequence for the wrapper program

The useful content of the reconvergent construction is now sharply separated:

**PROVED/EXACT**
- SAT-native branching and nominal reconvergence are well-defined;
- delayed SAT-restriction re-separation can occur;
- SINGLE-REALIZATION1;
- COMPACT-RENAMING1;
- SAT-REPLAY-CLOSE1;
- WRAPPER-TRANSITION-CLOSE1.

**COMPUTATIONAL EXACT**
- large delayed re-separation in the stated finite tests.

**FALSIFIED as generic hardness indicators**
- number of nominal paths;
- number of delayed restriction classes;
- fixed-order OBDD size by itself.

**OPEN / LOAD-BEARING**
- SAT-MERGE-FORCING1;
- MERGE-SERVICE-LB1;
- arbitrary-algorithm/model-preserving transfer;
- nonrelativizing ordinary-source lower bound.

P versus NP remains OPEN.
