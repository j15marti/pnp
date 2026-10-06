# LEAD-0025 — Shared BAD-SEED compression and endpoint-bypass audit

Timestamp: 2026-10-06 15:18 PT  
Agent: LEAD  
Global status: **P versus NP remains OPEN.**

## 1. Question

The previous toy established formula-internal nonmergeability by explicitly placing two wrapper routes in one CNF. Does extending this to exponentially many routes necessarily require exponential formula size?

No. A polynomial-depth wrapper family can be represented succinctly by a seed-input circuit, and violations can be searched for by one polynomial-size BAD-SEED SAT instance.

This solves the explicit route-duplication issue structurally, but it does **not** produce a lower bound. In fact, the same construction exposes a strong compact-representation/replay bypass.

## 2. BAD-SEED-CIRCUIT1 — PROVED/EXACT

Let \(W\) be a deterministic wrapper with:

- seed \(s\in\{0,1\}^{d(n)}\);
- \(d(n)=\operatorname{poly}(n)\) stages;
- polynomial-size state;
- polynomial-time stage transition;
- polynomially many calls per stage to a declared polynomial-time subroutine.

Then time-unrolling the wrapper gives a Boolean circuit

\[
C_{W,F}(s)
\]

of polynomial size that computes the complete realized state/output of \(W(F;s)\).

Therefore the existence of \(2^{d(n)}\) possible routes does not require an explicit \(2^{d(n)}\)-node route tree.

## 3. BAD-SEED-SAT1 — PROVED/EXACT

Let \(V(F,s,C_{W,F}(s))\) be any polynomial-time checkable violation predicate, for example:

- wrong endpoint;
- inconsistent recursive return;
- illegal lineage merge;
- failure of a declared continuation invariant.

Define

\[
B_F(s)=V(F,s,C_{W,F}(s)).
\]

By Tseitin/Cook--Levin compilation there is a polynomial-size CNF \(\mathrm{BAD}_F\) such that

\[
\mathrm{BAD}_F\in SAT
\iff
\exists s\quad B_F(s)=1.
\]

Hence

\[
\boxed{
\forall s\;B_F(s)=0
\iff
\mathrm{BAD}_F\in UNSAT.
}
\]

This is a compact representation of an exponentially large route family.

## 4. A-COLLAPSE-ALLROUTE1 — PROVED/EXACT under the contradiction hypothesis

Assume \(A\in P\) exactly decides SAT.

Since \(\mathrm{BAD}_F\) has polynomial size, the universal wrapper property

\[
\forall s\;B_F(s)=0
\]

can be decided by the single computation

\[
A(\mathrm{BAD}_F)=0.
\]

That computation itself has polynomial length and may be encoded in a further polynomial-size Cook--Levin formula.

Thus under \(P=NP\), the apparent \(\forall s\) route check can be internalized into ordinary polynomial-time computation by one SAT call.

This is a useful exact collapse of the quantifier gate **under the contradiction assumption**, not a contradiction.

## 5. Scaling experiment

Use the SAT-native toy family

\[
F_d=x_1\wedge\cdots\wedge x_d\wedge z.
\]

Seed bit \(s_i\) chooses the actual restriction query \(x_i=s_i\). After prior selected values are fixed to 1,

\[
\operatorname{SAT}(F_d\upharpoonright x_i=s_i)=s_i.
\]

So the actual A/B branch history equals the seed.

Let the recursive hidden state be route parity

\[
h_d=s_1\oplus\cdots\oplus s_d.
\]

The BAD-SEED formula asks whether a proposed merged evaluator \(q(s)\) differs from \(h_d\).

Three representations were tested:

1. unsafe merge \(q=0\);
2. one-bit exact summary \(q=h_d\);
3. replay evaluator recomputing parity from \(s\).

Selected exact accounting:

| depth \(d\) | routes | explicit \(d2^d\) route units | shared BAD clauses | false merge BAD? | parity BAD? | replay BAD? |
|---:|---:|---:|---:|:---:|:---:|:---:|
| 4 | 16 | 64 | 31 | yes | no | no |
| 8 | 256 | 2,048 | 55 | yes | no | no |
| 12 | 4,096 | 49,152 | 79 | yes | no | no |
| 16 | 65,536 | 1,048,576 | 103 | yes | no | no |
| 20 | 1,048,576 | 20,971,520 | 127 | yes | no | no |
| 24 | 16,777,216 | 402,653,184 | 151 | yes | no | no |
| 28 | 268,435,456 | 7,516,192,768 | 175 | yes | no | no |
| 32 | 4,294,967,296 | 137,438,953,472 | 199 | yes | no | no |

The shared false-merge BAD formula has exactly \(6d+7\) clauses in this encoding.

Thus:

\[
\boxed{
2^d\text{ routes can be audited for a bad seed with }O(d)\text{ CNF size}.
}
\]

But also:

\[
\boxed{
2^d\text{ histories may require only one continuation bit}.
}
\]

And if the seed remains accessible, that bit is recomputable in \(O(d)\) time.

## 6. OUTPUT-BIT-BYPASS1 — PROVED/EXACT

Assume \(A\) is an exact polynomial-time SAT decider.

Consider any wrapper \(W[A]\) whose only externally required semantic output on source formula \(F\) is

\[
\operatorname{SAT}(F),
\]

and whose ordinary model permits access to \(F\) and invocation of \(A\) at the endpoint.

Then there exists an exact polynomial-time implementation that discards or ignores **all** wrapper-generated lineage/hash/prime/history state and returns

\[
A(F)
\]

at the endpoint.

Therefore:

\[
\boxed{
\text{final SAT correctness alone cannot force retention of wrapper lineage}.
}
\]

If a proof forbids the final call \(A(F)\) or removes access to \(F\), that restriction must be independently justified by the target model; otherwise it does not apply to arbitrary SAT algorithms.

This is stronger than a finite control. It is a general closure theorem under the assumed decider.

## 7. FUNCTIONAL-EXTENSION-PROJECTION1 — PROVED/EXACT logical guard

Suppose a wrapper CNF \(G(F,z)\) satisfies

\[
\exists z\;G(F,z)
\iff
F.
\]

The auxiliary variables \(z\) may be uniquely determined in every satisfying extension and may obey strong internal nonmergeability constraints.

Nevertheless the SAT decision problem for \(G\) depends only on the existential projection

\[
\exists z\;G(F,z).
\]

Hence witness-level/history-level forcing does not imply that an arbitrary SAT decider must construct or retain \(z\).

The LEAD-0024 toy demonstrates this exactly: false lineage merging destroys satisfying extensions, while existential projection of the correct wrapper recovers the original formula.

## 8. Implication for SAT-MERGE-FORCING1

The route-count obstacle is now substantially clarified.

We do **not** need to enumerate all routes explicitly: BAD-SEED-CIRCUIT1 gives polynomial shared representation.

But the stronger desired implication

\[
\text{SAT endpoint correctness}
\Rightarrow
\text{retain/recover wrapper history}
\]

is false under the ordinary model because of OUTPUT-BIT-BYPASS1.

Therefore SAT-MERGE-FORCING1 cannot be justified merely by saying that wrong history causes the wrapper's own later control to malfunction.

The load-bearing consumer must be an **independently required intermediate capability** that cannot be bypassed by simply recomputing the one-bit SAT endpoint.

## 9. What remains viable

A surviving theorem would need a structure like:

1. an independently defined SAT reduction/consumer requires an intermediate service \(U\), not merely final \(SAT(F)\);
2. replacing the service by a final recomputation \(A(F)\) does not satisfy the reduction;
3. every ordinary implementation of \(U\), including direct recomputation, source reread, alternate circuits, algebraic representations, and oracle shadowing where applicable, incurs the target lower bound.

This returns directly to the project's consumer/acquisition bridge.

## 10. Relation to literature

Self-composition/product-program work in program verification uses one product construction to reason about relations among several executions; this is analogous to the paired-route formula in LEAD-0024.

Hyperproperty work makes the quantifier issue explicit: properties of all executions naturally introduce universal trace quantification.

The BAD-SEED formulation is the standard counterexample-search transformation:

\[
\forall s\;P(s)
\quad\Longleftrightarrow\quad
\neg\exists s\;\neg P(s).
\]

Under an assumed SAT decider, the existential bad-route search becomes polynomial-time decidable.

These analogies support the formalization but do not transfer lower bounds to unrestricted SAT.

## 11. Status

**PROVED/EXACT**
- BAD-SEED-CIRCUIT1;
- BAD-SEED-SAT1;
- A-COLLAPSE-ALLROUTE1 under \(A\in P\);
- OUTPUT-BIT-BYPASS1;
- FUNCTIONAL-EXTENSION-PROJECTION1.

**COMPUTATIONAL EXACT**
- the stated shared BAD-SEED scaling test through depth 32.

**RETIRED as generic lower-bound implications**
- exponential route count forces exponential wrapper formula size;
- final SAT correctness forces retention of wrapper-created history.

**OPEN / LOAD-BEARING**
- an independently SAT-forced intermediate consumer;
- representation-independent acquisition/service lower bound for that consumer;
- nonrelativizing/nonalgebrizing transfer.

P versus NP remains OPEN.
