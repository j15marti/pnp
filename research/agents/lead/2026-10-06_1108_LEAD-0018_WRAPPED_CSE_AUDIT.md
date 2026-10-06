# LEAD-0018 — WRAPPED-CSE hostile audit

Timestamp: 2026-10-06 11:08 PT  
Agent: LEAD  
Global status: **P versus NP remains OPEN.**

## Question

Can the entire near-total reduction accounting
\[
K_{0\to t}=\log_2\frac{\kappa_U(S_0)}{\kappa_U(S_t)}
\ge k-O(\log n)
\]
be moved into a fixed wrapper around an arbitrary hypothetical polynomial-time exact SAT decider \(A\), thereby bypassing the arbitrary-internal-state part of CSE?

## Corpus / controls

Reviewed current `main2.tex`, `main3.tex`, EXTCONSUMER1, CSE1, RECURCLOSE1, SELECTCHARGE1, LOCALITY-NOT-CONTRACTION1, RESTRICTED-ACCESS-ELIMINATION1, RED trace-wrapper controls, and the October 6 SRAS/provenance updates. Literature control: standard downward self-reducibility of SAT (decision-to-search by restrictions) is classical; Mahaney-style pruning requires additional membership-preserving semantic structure.

## WRAPPED-SELFRED1 — PROVED/EXACT

Let \(A\) be any exact SAT decider. Define wrapper \(W[A]\) on an \(n\)-variable CNF \(F\).

1. Compute \(b=A(F)\).
2. Maintain a restriction \(\rho_i\) with
   \[
   \operatorname{SAT}(F\upharpoonright \rho_i)=b.
   \]
3. For the next variable \(x_{i+1}\), query
   \[
   b_0=A(F\upharpoonright(\rho_i,x_{i+1}=0)).
   \]
4. If \(b_0=b\), set \(x_{i+1}=0\). Otherwise set \(x_{i+1}=1\).

The second branch is guaranteed to preserve \(b\): if \(b=1\) and the zero child is UNSAT, the one child must be SAT; if \(b=0\), every child is UNSAT and hence \(b_0=b\).

Therefore after \(x\) restriction steps,
\[
\operatorname{SAT}(F\upharpoonright\rho_x)=\operatorname{SAT}(F)
\]
and exactly \(x\) variables have been fixed. The wrapper uses \(x+1\) calls to \(A\).

This holds on both SAT and UNSAT inputs.

## WRAPPED-ASSIGNMENT-CONTRACTION1 — PROVED/EXACT

At the level of the raw assignment domain, fixing \(x\) distinct variables reduces
\[
2^n\longrightarrow 2^{n-x}.
\]
Choosing
\[
x=n-d\lceil\log_2 n\rceil
\]
leaves at most
\[
2^{d\lceil\log_2 n\rceil}=n^{d+O(1/\log n)}
\]
raw suffix assignments. Thus the wrapper explicitly realizes the BRTHRESH1 scale
\[
x=n-O(\log n).
\]

For 3-CNF, once only \(O(\log n)\) variables remain, duplicate/tautological width-\(\le3\) clauses can be canonicalized into only \(\operatorname{polylog}(n)\) distinct possible clauses. This is an output-size observation, not a hardness theorem.

## KAPPA-MISMATCH-GUARD1 — PROVED/EXACT logical guard

The equality
\[
x
=
\log_2\frac{\kappa_U(S_0)}{\kappa_U(S_t)}
\]
does **not** follow merely from fixing \(x\) variables.

The wrapper proves assignment-domain contraction. SRAS \(K_U\), however, is defined from continuation-equivalence classes for an independently justified consumer \(U\).

- If \(U\) is only the final SAT decision, the consumer has very little semantic resolution; fixing variables does not force \(2^x\) continuation-class reduction.
- If \(U\) is chosen to distinguish all assignment coordinates, then \(x\) can be made to look like the desired contraction, but that consumer is wrapper-imposed unless a separate SAT-correctness theorem requires it.
- If \(U=W_{\rm EXT}\) asks SAT under all restrictions, following one adaptive restriction path does not construct a summary that answers every restriction.

Therefore the wrapper may maintain the **numerical counter** \(x\), but it cannot simply declare the SRAS identity \(K_U=x\) without a consumer theorem.

This is the first substantive limitation of the proposal.

## WRAPPED-CURRENT-SCALE1 — PROVED/EXACT accounting

Suppose an \(m\)-variable residual is decided by \(A\) in
\[
T_A(m)=m^{K+o(1)}.
\]
The standard wrapper fixes variables one at a time. To reach \(L=O(\log n)\) live variables its SAT-call work is
\[
\sum_{m=L}^{n} T_A(m)
=
\Theta(n^{K+1+o(1)})
\]
in the variable-count normalization.

More generally, with encoding length \(N\), the wrapper makes \(O(n)\) calls whose early instances remain current-scale:
\[
\delta=1
\]
in SELECTCHARGE1 notation. Hence the explicit charge contains the unknown exponent \(K\); the wrapper does not create a fixed fractional query exponent \(\theta<1\).

Finite numerical check of the sum for \(K\in\{1,2,3,5,10\}\) and \(n=10^3,10^4\) agrees with the integral estimate
\[
\sum_{m=1}^{n}m^K\sim \frac{n^{K+1}}{K+1}.
\]

This is the second decisive limitation.

## Why batching does not repair the current-scale issue

Grouping \(b\) variable decisions into one wrapper phase does not by itself give a query of length \(n^\theta\) with fixed \(\theta<1\). To determine a branch preserving the parent SAT bit, the wrapper still needs semantic information about prefixes while most variables remain live.

- \(b=O(\log n)\): residual scale is \(n-O(\log n)\), still \(\theta=1\).
- \(b=\Theta(n)\): naively enumerating block assignments is exponential; finding the correct large block by ordinary small calls would itself require the missing compressor/selector.
- Producing a genuinely smaller query before paying current-scale SAT cost is exactly CONTRACTION-FORCING1/CSE again.

Thus standard self-reduction gives additive shrinkage, not the multiplicative/fractional shrinkage required by RECURCLOSE1 to erase \(K\).

## WRAPPED-ORACLE-SHADOW1 — PROVED/EXACT from RESTRICTED-ACCESS-ELIMINATION1

The wrapper accesses \(A\) only through SAT decision bits on explicit restrictions. A SAT oracle reproduces the complete adaptive wrapper transcript exactly.

Therefore WRAPPED-SELFRED1 is fully relativizing and supplies no nonrelativizing hinge.

SRAS may still record ordinary implementation calls as
\[
\Omega_G=\mathrm{ORDINARY}
\]
and oracle replacements as
\[
\Omega_G=\mathrm{EXTERNAL},
\]
but a downstream theorem must independently make that lineage distinction load-bearing.

## Finite computational sanity check

Implemented the wrapper with brute-force SAT as \(A\) on 100 random \(n=8\), \(m=28\) 3-CNFs. In all 100 cases, the wrapper's final residual retained the original SAT decision after restricting down to the declared \(O(\log n)\) variable target.

A separate tiny residual-function diagnostic showed why variable count must not be identified with continuation quotient size. For one random \(n=6\) 3-CNF, the number of distinct residual Boolean functions over all prefixes by depth was
\[
[1,2,4,5,5,3,2],
\]
while a random 2-CNF control gave
\[
[1,2,2,2,2,2,2].
\]
This finite diagnostic is **COMPUTATIONAL only** and is not a definition of the project SRAS \(\kappa_U\). It illustrates that residual semantic classes need not track \(2^x\) coordinate fixing monotonically.

## WRAPPED-CSE-BOUNDARY1 — PROVED/EXACT classification

The wrapper removes one genuine CSE nuisance:

> We no longer need to infer from the internal representation of \(A\) that some explicit restriction path exists. A fixed black-box wrapper can force an answer-preserving, source-bound restriction path for every exact \(A\).

But it does **not** establish either of the two load-bearing properties needed by the current CSE endpoint:

1. **consumer-valid near-total SRAS reduction**
   \[
   K_U\ge n-O(\log n)
   \]
   for an independently SAT-forced consumer \(U\); or
2. **\(K\)-independent fractional shrinkage/acquisition**
   with all SAT subqueries of size \(n^{\theta+o(1)}\), fixed \(\theta<1\), and no current-scale invocation of \(A\).

Hence WRAPPED-CSE solves **path exposure**, not **CSE contraction in the endpoint sense**.

## Consequence for the shortest proof path

A legitimate alternative shortest path can be stated as
\[
P=NP
\Rightarrow A\in P
\Rightarrow W[A]\text{ gives explicit answer-preserving }n-O(\log n)
\text{ assignment-domain contraction}
\]
followed by a new unconditional theorem saying this exact ordinary wrapped process cannot have polynomial total cost.

That would be a valid contradiction architecture. But the new lower bound would have to defeat the known wrapper implementation while not simply assuming SAT calls are expensive. It is therefore essentially the entire remaining hardness burden, and it must be nonrelativizing because a SAT oracle performs the same wrapper cheaply.

This route is cleaner than arbitrary trace extraction, but it does not make the central lower bound easier automatically.

## Status ledger

- WRAPPED-SELFRED1: **PROVED/EXACT**
- WRAPPED-ASSIGNMENT-CONTRACTION1: **PROVED/EXACT**
- KAPPA-MISMATCH-GUARD1: **PROVED/EXACT**
- WRAPPED-CURRENT-SCALE1: **PROVED/EXACT**
- WRAPPED-ORACLE-SHADOW1: **PROVED/EXACT**
- WRAPPED-CSE-BOUNDARY1: **PROVED/EXACT classification**
- wrapper gives \(n-O(\log n)\) raw assignment-domain contraction: **YES**
- wrapper proves \(K_U=n-O(\log n)\) for the existing SRAS consumer: **NO**
- wrapper gives fixed \(\theta<1\) smaller SAT queries: **NO**
- wrapper eliminates unknown exponent \(K\): **NO**
- wrapper nonrelativizes: **NO**
- arbitrary-algorithm CSE as currently required by RECURCLOSE1: **OPEN**
- ordinary-source acquisition lower bound: **OPEN**
- P versus NP: **OPEN**

## Next target

There are now two sharply separated options:

1. **Consumer route:** find an independently SAT-forced consumer \(U\) for which the wrapper's explicit restriction path provably yields
   \[
   K_U\ge n-O(\log n).
   \]
   This would repair KAPPA-MISMATCH-GUARD1.

2. **Acquisition route:** abandon the requirement that \(K_U=x\) and prove a lower bound directly for the canonical answer-preserving restriction process \(W[A]\), with ordinary calls expanded/charged rather than treated as SAT-oracle primitives.

The second route completely externalizes CSE but concentrates the proof burden into a nonrelativizing lower bound on the ordinary implementation of those adaptive decision calls.
