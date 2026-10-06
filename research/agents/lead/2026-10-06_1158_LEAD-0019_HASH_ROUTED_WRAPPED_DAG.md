# LEAD-0019 — HASH-ROUTED WRAPPED-DAG formalization and hostile audit

Timestamp: 2026-10-06 11:58 PT  
Agent: LEAD  
Global status: **P versus NP remains OPEN.**

## 1. Motivation

The plain WRAPPED-CSE construction exposes one canonical answer-preserving restriction path

\[
F_0\to F_1\to\cdots\to F_x.
\]

The proposed extension makes each stage value-directed: a hash/provenance/state value selects a different legal next direction or transformation. Across possible hash states or inputs, the family of possible continuation histories can be exponential.

This report formalizes that extension as an actual-execution computation/source DAG and tests whether exponential route multiplicity can itself be promoted to hardness.

## 2. Actual-execution wrapped computation DAG

Fix a deterministic exact SAT decider \(A\), input formula \(F\), and fixed wrapper seed/state \(s\).

Define

\[
D_W(A,F;s)=(V,E,\tau,\lambda,\Omega)
\]

as the time-unrolled dependency DAG of the realized ordinary execution of the wrapper with every ordinary invocation of \(A\) inlined.

Each node \(v\in V\) has:

- time label \(\tau(v)\);
- operation type \(\lambda(v)\);
- authority \(\Omega(v)\in\{\mathrm{ORDINARY},\mathrm{EXTERNAL}\}\);
- typed input edges from the exact values/source cells on which it depends.

Allowed node classes include SOURCE, READ, COMPUTE, WRITE/RETAIN, RESTRICT, HASH, ROUTE, OUTPUT, and EXTERNAL.

Ordinary SAT calls are not primitive SAT nodes: their actual computation is inlined. This prevents hiding the desired lower bound inside an uncharged call to \(A\).

Because all edges point from earlier-produced values/source reads to later uses, the time-unrolled object is acyclic even if the underlying machine revisits memory locations or modules.

## 3. Cross-call sharing

A wrapper implementation may reuse information computed during an earlier call.

If a value \(q\) is computed once and retained, later uses point to the same value node:

\[
q\longrightarrow u_i,\qquad q\longrightarrow u_j.
\]

Its computation is charged once; retention/live-space is charged according to the selected model.

If \(q\) is discarded and later recomputed, the recomputation creates new operation nodes and is charged again.

If \(q\) is reread from immutable source, the source object is not recomputed, but each declared read/access operation is charged.

Thus DAG sharing is not forbidden. It is part of the model.

## 4. Work and space measures

For node costs \(c(v)\),

\[
C_{\rm work}(D)=\sum_{v\in V_{\rm ordinary}}c(v).
\]

For a realized schedule \(\sigma\), let

\[
C_{\rm space}(D,\sigma)
\]

be the maximum charged live ordinary state under that schedule.

A pebbling-style quantity may also be defined as a restricted-model diagnostic:

\[
\operatorname{Peb}(D)=
\min_{\sigma\text{ legal}}
\{\text{space or time-space cost of evaluating }D\}.
\]

Guard: pebbling lower bounds on a chosen DAG are not unrestricted SAT lower bounds unless correctness forces every arbitrary solver to instantiate a model-matched hard DAG.

## 5. HASH-ROUTED-WRAPPER1

At wrapper stage \(i\), maintain residual \(F_i\), parent SAT value \(b_i=\operatorname{SAT}(F_i)\), hash/state \(h_i\), and unassigned-variable set \(U_i\).

A route selector chooses

\[
v_i=R_i(h_i,F_i,U_i).
\]

The wrapper queries

\[
b_{i,0}=A(F_i\upharpoonright(v_i=0)).
\]

It selects the answer-preserving bit

\[
a_i=
\begin{cases}
0,&b_{i,0}=b_i,\\
1,&b_{i,0}\ne b_i,
\end{cases}
\]

and sets

\[
F_{i+1}=F_i\upharpoonright(v_i=a_i).
\]

Then update

\[
h_{i+1}
=
H_i(h_i,\operatorname{Enc}(F_i),v_i,a_i,b_{i,0},b_i).
\]

More generally, after choosing the answer-preserving restriction the hash may select among a family of fully charged SAT-preserving transformations \(T_{i,j}\), with

\[
j=G_i(h_{i+1}).
\]

This realizes the proposed feature: the value at a node selects a different direction/function, so different value histories induce different future computations.

## 6. ROUTE-DIVERSITY1 — PROVED/EXACT counting

If stage \(i\) has at most \(q_i\) legal route choices, the number of possible route strings of depth \(d\) is at most

\[
N_{\rm route}\le\prod_{i<d}q_i.
\]

For constant \(q_i=q\ge2\),

\[
N_{\rm route}\le q^d=2^{\Theta(d)}.
\]

Thus an exponential family of potential continuations is compatible with a polynomial-depth wrapper.

## 7. ROUTE-IDENTITY-CAP1 — PROVED/EXACT information guard

A realized route \(r=(r_1,\ldots,r_d)\) can be identified using at most

\[
\log_2 N_{\rm route}
\le
\sum_{i<d}\log_2 q_i
\]

bits.

If \(d=\operatorname{poly}(n)\) and \(q_i=\operatorname{poly}(n)\), route identity itself has only polynomial bit complexity even when \(N_{\rm route}\) is exponential.

Therefore

\[
\boxed{
\text{exponentially many possible routes}
\not\Rightarrow
\text{superpolynomial storage/work}.
}
\]

## 8. HASH-ROUTE-CLOSE1 — PROVED/EXACT

Suppose:

1. the wrapper runs \(d(n)=\operatorname{poly}(n)\) stages;
2. \(h_i\) has polynomial length;
3. each hash/route/transition evaluator is polynomial time from its succinct index and inputs;
4. \(A\) is polynomial time;
5. intermediate/formula lengths remain polynomial.

Then the one realized hash-routed wrapper execution is polynomial time.

The number of unchosen continuations does not enter the runtime.

This theorem relativizes.

## 9. Explicit-function-table guard

Suppose a \(b\)-bit hash selects one of \(2^b\) transition functions.

If there is a polynomial-time universal evaluator

\[
\operatorname{Eval}(j,x)=T_j(x),
\]

then one selected transition remains polynomial-time evaluable. Exponential family size alone is not hard.

If the wrapper literally contains \(2^b\) unrelated transition descriptions, then the wrapper/program description itself is exponential unless \(b=O(\log n)\). The exponential information was inserted into the wrapper rather than forced by SAT.

## 10. Composition guard

Even if hash values choose noncommuting functions and there are exponentially many possible compositions

\[
T_{d,r_d}\circ\cdots\circ T_{1,r_1},
\]

one realized polynomial-depth composition remains polynomial-time computable when each selected transition is polynomial time.

Trajectory uniqueness does not alter this closure.

## 11. Easy-family computational hostile control

A hash-directed self-reduction was implemented on planted 2-SAT.

At each stage:
1. a BLAKE2-based 64-bit state selected the next unassigned variable;
2. an exact polynomial-time 2-SAT decision on the zero-restriction selected the answer-preserving child;
3. the state was updated from the previous hash, chosen variable, selected bit, child result, and parent result.

Across 4,096 seeds:

| n | distinct realized variable-order routes | SAT calls/run | correctness |
|---:|---:|---:|---:|
| 8 | 3,906 | 9 | 4,096/4,096 |
| 10 | 4,095 | 11 | 4,096/4,096 |
| 12 | 4,096 | 13 | 4,096/4,096 |

For \(n=12\), all 4,096 tested initial states produced distinct route histories while every run remained an easy polynomial-time 2-SAT computation.

Status: **COMPUTATIONAL CONTROL**, not an asymptotic theorem.

Conclusion:

\[
\boxed{
\text{very high route diversity can occur on an easy SAT family}.
}
\]

So route diversity alone cannot be the hardness invariant.

## 12. Branching-program / pebbling scope guard

Strong lower bounds are known for restricted branching-program models and pebbling/time-space models, but those results constrain their declared representations/models. They do not automatically constrain arbitrary polynomial-time SAT algorithms.

The hash-routed wrapper must not be silently identified with an OBDD, FBDD, read-once branching program, or fixed pebbling schedule.

## 13. Where a genuine hardness theorem could enter

The hash-routed DAG becomes potentially load-bearing only if SAT correctness forces more than one realized route to matter to the same ordinary computation/state.

### BRANCH-COMPLETE-ACQ1 — CANDIDATE / OPEN

Construct an independently SAT-forced consumer \(U^\star\) and route family \(\mathcal R\) such that, at a declared state/cut, correctness requires one ordinary representation \(S\) to support

\[
\Psi_{U^\star}(S,r)
\qquad
\text{for all }r\in\mathcal R.
\]

For source state \(X\), define the complete response signature

\[
\Sigma(X)
=
(\Psi_{U^\star}(X,r))_{r\in\mathcal R}.
\]

States with different signatures may not be safely merged.

Existing branch-complete/precommitment logic can then force STORE-or-REACQUIRE. But two further theorems are still required:

1. SAT-FORCING: the multi-route consumer must be required by SAT correctness, not invented by the wrapper;
2. ACQUISITION COST: reacquiring/recomputing the needed distinctions must be unconditionally expensive in the ordinary unrestricted model.

Without both, the construction remains instrumentation.

## 14. Wrapper-created future challenge guard

If the wrapper itself asks, after following one route, what would have happened on every unchosen route, it has strengthened SAT into a different task.

That burden cannot be charged to an arbitrary SAT decider unless a separate reduction proves SAT correctness entails that service.

Likewise, outputting all \(q^d\) branches trivially costs exponential output but no longer represents ordinary SAT decision.

## 15. Hash/provenance exactness guard

A fixed-width \(b\)-bit hash has only \(2^b\) states and collisions are unavoidable.

It is valid as:
- a deterministic route selector;
- lossy provenance instrumentation.

It is not an exact SAME_REALIZATION identifier.

An injective transcript code is exact but has length proportional to the polynomial trace under the \(A\in P\) assumption.

Cryptographic one-wayness or collision resistance cannot serve as an unconditional hardness premise.

## 16. Interaction with the 2^k / 2^x program

The route family may have

\[
|\mathcal R|=2^k.
\]

But the existence of \(2^k\) potential routes gives only \(k\) bits of route identity.

To use the project's \(2^k/2^x\) framework, one must define an independently required continuation quotient whose live mass is actually \(2^k\), then prove legal operations cannot collapse it cheaply.

Hash-generated route multiplicity cannot be substituted for \(\kappa_U\) by definition.

## 17. HASH-CONTSEP1 — CANDIDATE

A potentially useful intermediate target is:

For a source family \(F_n\), prove that many hash-directed nodes have pairwise future-inequivalent continuation behavior under a SAT-forced consumer, so DAG merging is illegal.

This could establish a lower bound on a declared decision-DAG/state representation.

However:
- representation size is not automatically runtime;
- an unrestricted algorithm may use a different representation;
- SOURCE-TRANSPORT/model matching would still be needed.

## 18. Actual wrapped-DAG lower-bound target

Let \(\mathfrak D(A,F)\) be the actual-execution wrapped DAG after:
- inlining all ordinary calls to \(A\);
- crediting legal sharing;
- charging reads, recomputation, writes, route/hash work, and restriction construction;
- marking only genuine oracle answers EXTERNAL.

The direct target is

\[
\boxed{
\forall A\text{ exact polynomial SAT-decider candidate}\;
\exists^\infty n\;\exists F_n:
\quad
C(\mathfrak D(A,F_n))=n^{\omega(1)}.
}
\]

This would directly contradict the assumption that \(A\) is polynomial.

Status: **OPEN**. As stated it is essentially an unrestricted SAT lower bound; the DAG formalization makes accounting exact but does not prove it.

## 19. What the DAG formalization buys

It resolves several bookkeeping ambiguities:

1. the wrapper no longer hides calls to \(A\);
2. cross-call sharing is credited exactly;
3. recomputation is charged rather than mistaken for retained state;
4. source rereads are explicit;
5. ordinary versus EXTERNAL authority is visible;
6. hash-directed route choices are typed computation nodes;
7. any pebbling/branching-program theorem can be checked for exact model match.

## 20. Status ledger

**PROVED/EXACT**
- actual deterministic wrapper executions admit a time-unrolled computation/source DAG;
- legal cross-call sharing can be represented and charged once;
- ROUTE-DIVERSITY1;
- ROUTE-IDENTITY-CAP1;
- HASH-ROUTE-CLOSE1 under its polynomial evaluator assumptions;
- explicit arbitrary exponential transition tables merely move exponential information into the wrapper;
- one realized polynomial-depth composition of polynomial-time selected functions remains polynomial time.

**COMPUTATIONAL CONTROL**
- planted 2-SAT hash-directed wrapper: thousands of distinct routes with polynomial exact computation.

**CANDIDATE / OPEN**
- BRANCH-COMPLETE-ACQ1;
- HASH-CONTSEP1;
- SAT-forced multi-route consumer;
- superpolynomial ordinary-source acquisition/recomputation theorem;
- model-preserving transfer from arbitrary SAT computation to a restricted DAG/pebbling/branching-program model.

**FORBIDDEN INFERENCES**
- exponential number of potential hash routes implies exponential runtime;
- unique/noncommuting route compositions imply hardness;
- fixed-width hash multiplicity implies exact provenance;
- full binary restriction-tree size equals cost of the one realized wrapper execution.

## 21. Next experiment

The next useful test is not to increase hash branch count. It is to search for a SAT-forced cross-route obligation.

For small n:
1. generate the hash-routed restriction family;
2. quotient nodes by exact future SAT-continuation behavior;
3. measure how aggressively routes merge;
4. compare 3-SAT with 2-SAT, XOR/Tseitin, Horn, and bounded-treewidth controls;
5. test whether any continuation-separation quantity survives semantic quotienting substantially better on the intended hard family;
6. do not interpret finite growth as an asymptotic lower bound.
