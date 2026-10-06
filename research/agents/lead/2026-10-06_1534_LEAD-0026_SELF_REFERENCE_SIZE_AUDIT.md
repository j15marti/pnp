# LEAD-0026 — Self-referential wrapper tableau size audit

Timestamp: 2026-10-06 15:34 PT  
Agent: LEAD  
Global status: **P versus NP remains OPEN.**

## 1. Motivation

After BAD-SEED-CIRCUIT1, a natural strengthening is to let the wrapper-CNF contain the claim

\[
A(\mathrm{BAD}_F)=0
\]

and make later recursive control depend on that result.

An even stronger diagonal attempt would seek a formula \(\Phi\) satisfying

\[
\Phi\in SAT
\quad\Longleftrightarrow\quad
A(\Phi)=0.
\]

If such an ordinary polynomial-size CNF could contain a faithful computation of \(A\) on itself for long enough to cover \(A\)'s running time, exactness of \(A\) would yield a contradiction.

The present audit checks the size accounting for the standard time-unrolled Cook--Levin/Tseitin route.

## 2. Declared model

Assume

\[
T_A(m)\le m^K
\]

for fixed \(K\ge1\).

Let \(T\) be the number of steps of \(A(\Phi)\) that the formula attempts to encode, and let \(m=|\Phi|\).

For an ordinary time-unrolled tableau, assume only the very weak lower accounting

\[
m\ge T+b
\]

for some positive base overhead \(b>0\): at least one encoding unit per simulated time step plus nonempty surrounding formula.

To make the tableau long enough to contain the completed computation, require

\[
T\ge m^K.
\]

Combining,

\[
m\ge m^K+b.
\]

## 3. TABLEAU-SELF-CONTAINMENT-GAP1 — PROVED/EXACT in the declared model

For \(K=1\),

\[
m\ge m+b
\]

is impossible for \(b>0\).

For \(K>1\) and \(m\ge1\),

\[
m^K\ge m,
\]

so

\[
m^K+b>m.
\]

Hence no positive \(m\) satisfies the necessary inequality.

Therefore:

\[
\boxed{
\text{a standard time-unrolled CNF cannot contain a completed }m^K
\text{-step computation of }A\text{ on that same CNF}.
}
\]

This blocks the naive self-containing liar tableau.

## 4. Numerical diagnostic

Representative ratios using the minimal proxy

\[
m_{\rm tableau}=m^K+1
\]

are:

| \(K\) | \(m\) | tableau/formula ratio | closes? |
|---:|---:|---:|:---:|
| 1 | 16 | 1.0625 | no |
| 1 | 64 | 1.015625 | no |
| 2 | 16 | 16.0625 | no |
| 2 | 64 | 64.015625 | no |
| 3 | 16 | 256.0625 | no |
| 3 | 64 | 4096.015625 | no |
| 5 | 16 | 65,536.0625 | no |
| 5 | 64 | 16,777,216.015625 | no |

For \(K>1\), fixed-point iteration of the size map \(m\mapsto m^K+1\) explodes rather than closes.

## 5. Scope guard

This is **not** a theorem that every possible succinct representation of a long computation must have size \(\Omega(T)\).

It is exact only for the declared time-unrolled computation-tableau route.

A proposed escape must therefore supply a separate theorem giving a generic succinct representation of an arbitrary \(T\)-step deterministic computation while preserving ordinary SAT semantics and the required exactness.

That theorem cannot be assumed for free.

Known easy controls show why this matters: affine or small-group transition systems can admit very compact composition summaries, while arbitrary computation does not inherit those summaries automatically.

## 6. Relation to current-scale exponent problem

The failed self-containment is another form of the project's current-scale issue.

To know that the encoded tableau covers the hypothetical algorithm's run, one must dominate its unknown polynomial exponent \(K\).

But enlarging the tableau enlarges the formula, which enlarges the running-time budget \(m^K\) that must be encoded.

The attempted diagonal therefore chases its own input scale upward.

This is structurally analogous to the earlier SELECTCHARGE/current-scale obstruction.

## 7. Combined lesson from LEAD-0024--0026

The wrapper-as-SAT program now has three exact facts:

1. **Formula-internal merge forcing is possible** on explicitly represented histories.
2. **Exponentially many routes need not be explicitly duplicated**: BAD-SEED gives a polynomial shared representation.
3. **A naive self-containing diagonal tableau does not close** because the computation being encoded grows with the size of the formula containing the encoding.

And one decisive bypass remains:

\[
\boxed{
\text{if the only required external answer is }SAT(F),
\text{ then under }A\in P\text{ the wrapper may simply return }A(F).
}
\]

Therefore a successful wrapper route still needs an independently required intermediate consumer/resource theorem.

## 8. Status

**PROVED/EXACT**
- TABLEAU-SELF-CONTAINMENT-GAP1 in the declared time-unrolled model.

**COMPUTATIONAL / ACCOUNTING**
- numerical fixed-point and size-ratio diagnostics.

**NOT PROVED**
- any universal lower bound against succinct encodings of arbitrary computations;
- any contradiction from recursion/self-reference alone;
- P versus NP.

**OPEN**
- a model-preserving succinct construction that escapes the size recurrence without changing the problem;
- an independently SAT-forced intermediate consumer;
- the representation-independent acquisition lower bound.

P versus NP remains OPEN.
