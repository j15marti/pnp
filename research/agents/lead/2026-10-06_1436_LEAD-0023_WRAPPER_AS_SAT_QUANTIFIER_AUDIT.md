# LEAD-0023 — Wrapper-as-SAT and quantifier audit

Timestamp: 2026-10-06 14:36 PT
Agent: LEAD
Global status: **P versus NP remains OPEN.**

## 1. Question

Can the prime/hash/recursive wrapper itself be compiled into a SAT instance, so that its history-consistency obligations become part of SAT semantics rather than an external audit?

Yes, with an important quantifier boundary.

## 2. WRAPPER-AS-SAT1 — PROVED/EXACT under the contradiction hypothesis

Assume a fixed deterministic exact SAT decider \(A\) with time bound

\[
T_A(n)\le n^K
\]

for some fixed \(K\), and a wrapper \(W[A]\) that on input \((F,s)\):

- runs for polynomially many wrapper stages;
- makes polynomially many calls to \(A\) on polynomial-size formulas;
- applies polynomial-time branch-dependent transitions;
- maintains polynomial-size explicit state.

Then the complete deterministic computation of \(W[A](F,s)\) has polynomial length and can be encoded by a Cook--Levin/Tseitin-style CNF

\[
G_{A,W}(F,s;z),
\]

where \(z\) are tableau/control/lineage auxiliary variables.

For fixed \((F,s)\),

\[
\exists z\;G_{A,W}(F,s;z)
\quad\Longleftrightarrow\quad
W[A](F,s)=1.
\]

If \(W\) is exact for every legal seed,

\[
W[A](F,s)=\operatorname{SAT}(F)
\quad\forall s,
\]

then for every fixed seed \(s\),

\[
\boxed{
\exists z\;G_{A,W}(F,s;z)
\iff
\operatorname{SAT}(F)=1.
}
\]

Thus the wrapper execution can be internalized as SAT without changing the endpoint semantics.

## 3. Exact branch answers can be encoded only by encoding the machine computation

There is a critical asymmetry.

A positive semantic statement

\[
\operatorname{SAT}(Q)=1
\]

has an NP witness: a satisfying assignment.

A negative semantic statement

\[
\operatorname{SAT}(Q)=0
\]

does not have a known polynomial NP witness in general.

Therefore an ordinary SAT formula cannot simply introduce a branch bit \(b\) with clauses asserting

\[
b=\operatorname{SAT}(Q)
\]

by semantic SAT constraints alone.

Under the contradiction hypothesis \(A\in P\), however, we can encode the deterministic computation of \(A(Q)\), including either output 0 or output 1, by a polynomial Cook--Levin tableau.

This is why \(G_{A,W}\) is naturally an \(A\)-dependent contradiction object.

## 4. PRIME-LINEAGE-CNF1 — PROVED/EXACT mechanics

The wrapper's multisign labels may be represented by Boolean auxiliary variables and optionally by distinct prime labels

\[
p_{i,T},\;p_{i,F},\;p_{i,\neg T},\;p_{i,\neg F}.
\]

The prime map is injective bookkeeping. Its bit length remains polynomial when only polynomially many polynomial-bit primes are used.

One need not rely on computational factoring hardness: the CNF may carry symbolic label variables or prime indices directly.

Thus prime lineage can be made exact and formula-internal, but prime magnitude/factorization is not credited as a lower bound.

## 5. FORMULA-INTERNAL-MERGE1 — semantic gain

Suppose two wrapper histories \(h,h'\) reach the same nominal node but different lineage/control values.

If later CNF constraints are wired so that substituting the lineage value of \(h'\) into the execution corresponding to \(h\) violates at least one transition/output clause, then the distinction is no longer an external audit.

It is part of the satisfiability relation of \(G_{A,W}\).

This can establish a formula-level statement of the form

\[
h\not\equiv_G h'.
\]

That is a genuine improvement over asking an extra post-hoc provenance question.

However, it proves only that a satisfying assignment to the compiled wrapper must respect the distinction. It does **not** prove that an arbitrary SAT decider must explicitly represent that distinction while deciding whether \(G_{A,W}\) is satisfiable.

## 6. WRAPPER-NPHARD1 — exact but nonseparating

If \(W\) is an exact polynomial wrapper and a fixed seed \(s_0\) is used, then

\[
F\mapsto G_{A,W}(F,s_0)
\]

is a polynomial many-one reduction preserving SAT/UNSAT under the hypothesis that the declared polynomial bound for \(A\) is available to the construction.

Therefore the resulting wrapper-CNF family is SAT-hard/equisatisfiable in the ordinary reduction sense.

But the inference

\[
\text{wrapper-CNF is NP-hard}
\Rightarrow
\text{wrapper-CNF requires superpolynomial time}
\]

is exactly equivalent to invoking \(P\ne NP\).

Hence:

\[
\boxed{
\text{NP-hardness of the wrapper cannot be used as the lower-bound premise
in a proof of }P\ne NP.
}
\]

Under the contradiction assumption \(P=NP\), the wrapper-CNF is polynomial-time decidable as well.

## 7. EXISTENTIAL-PATH-ESCAPE1 — PROVED/EXACT

Suppose the seed/route bits are ordinary SAT variables.

Then plain SAT asks

\[
\exists s,z\;G(F,s,z).
\]

This requires only **one** seed/route with a satisfying consistent execution.

It does not require the same representation to service every possible route.

Therefore exponentially many legal wrapper routes do not create a simultaneous burden merely by being encoded as existential SAT variables.

A single bad route can coexist with many good routes while the existential wrapper formula remains satisfiable.

This is the SAT-level version of SINGLE-REALIZATION1.

## 8. Universal-route correctness crosses a quantifier boundary

The desired exact statement

\[
\forall s\quad W[A](F,s)=\operatorname{SAT}(F)
\]

is a universal property over route seeds.

If trace variables \(z\) are treated existentially, the direct relational form is

\[
\forall s\;\exists z\quad T(F,s,z),
\]

although for a deterministic functional tableau \(z\) is uniquely determined and can conceptually be eliminated.

If we additionally existentially quantify a shared representation \(Q\) that must service all routes,

\[
\exists Q\;\forall s\quad E(Q,s)=g_F(s),
\]

the shape is explicitly \(\Sigma_2\)-like.

This explains why the project's local/global and FSC exactness issues repeatedly expose an \(\exists\forall\) boundary.

It does not force us to abandon the P-vs-NP route; it tells us that ordinary existential SAT cannot obtain simultaneous all-route obligations for free.

## 9. BAD-SEED-CNF1 — useful reformulation

For a deterministic wrapper whose one-run behavior is polynomial-time checkable under the contradiction hypothesis, define a CNF encoding

\[
B_F(s,z)
\]

whose satisfying assignments certify that seed \(s\) produces an incorrect wrapper endpoint.

Then

\[
\forall s\quad W[A](F,s)=\operatorname{SAT}(F)
\]

is equivalent to

\[
\operatorname{UNSAT}(B_F).
\]

So universal route correctness can be represented as the **absence** of a bad-seed SAT witness.

This is useful for exactness audits, but it does not create a P-vs-NP contradiction: under \(P=NP\), coNP collapses as well.

## 10. Where wrapper-as-SAT genuinely helps SAT-MERGE-FORCING1

The construction can solve one conceptual problem:

> Are the lineage/recursive distinctions merely demands invented after the SAT computation?

If the transition, prime-lineage, recursive-return, and endpoint consistency constraints are all clauses of \(G_{A,W}\), then no: a satisfying assignment to the wrapper-CNF must obey them.

Thus a wrong merge can literally make the CNF unsatisfiable.

This gives a legitimate **formula-semantic forcing** statement.

What it does not solve is the algorithmic transfer:

\[
\boxed{
\text{CNF requires distinction in every satisfying execution}
\not\Rightarrow
\text{every SAT decider must explicitly acquire/store that distinction}.
}
\]

An arbitrary decider may determine existence by another representation or shortcut.

That is still MERGE-SERVICE-LB1 / representation-transfer.

## 11. Strongest P-vs-NP route suggested by the construction

Keep ordinary SAT as the endpoint and compile the wrapper into an equisatisfiable CNF:

\[
F
\xmapsto{R_{A,W}}
G_{A,W}(F).
\]

Use functional Tseitin/Cook--Levin constraints so the prime/hash/recursive control state is not free metadata but logically constrained.

Then attempt:

1. **INTERNAL-FORCING:** prove selected history distinctions are necessary for satisfying the wrapper-CNF;
2. **SOURCE/REPRESENTATION TRANSFER:** prove any exact decider for \(G_{A,W}(F)\) must provide an equivalent ordinary capability, not necessarily the literal history variables;
3. **COST:** lower-bound acquisition/use of every such equivalent capability;
4. **ORACLE/BARRIER AUDIT:** verify the theorem is not merely relativizing/algebrizing/restricted-model.

Step 1 is now plausibly constructible.
Steps 2--3 remain the load-bearing open problem.

## 12. Status ledger

**PROVED/EXACT under stated assumptions**
- WRAPPER-AS-SAT1;
- exact computation-tableau encoding of 0/1 branch outputs under assumed polynomial \(A\);
- PRIME-LINEAGE-CNF1 mechanics;
- EXISTENTIAL-PATH-ESCAPE1;
- quantifier classification of all-route correctness;
- NP-hardness/equisatisfiability does not itself provide a separation lower bound.

**PROMISING STRUCTURAL TARGET**
- FORMULA-INTERNAL-MERGE1 / INTERNAL-FORCING.

**OPEN / LOAD-BEARING**
- arbitrary-decider representation transfer;
- MERGE-SERVICE-LB1;
- an unconditional ordinary-source cost lower bound;
- nonrelativizing/nonalgebrizing endgame.

P versus NP remains OPEN.
