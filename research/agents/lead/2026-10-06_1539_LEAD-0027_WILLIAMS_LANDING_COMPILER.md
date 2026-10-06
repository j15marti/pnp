# LEAD-0027 — Williams-landing compiler audit

Timestamp: 2026-10-06 15:39 PT  
Agent: LEAD  
Global status: **P versus NP remains OPEN.**

## 1. Endpoint verified

Ryan Williams, *Alternation-Trading Proofs, Linear Programming, and Lower Bounds* (STACS 2010, Theorem 3.9; TOCT 2013), proves for polynomially bounded SAT time \(t\) and space \(s\):
\[
t(N)s(N)=\Omega\!\left(N^{\gamma-\varepsilon}\right)
\quad\text{for every }\varepsilon>0,
\qquad
\gamma=2\cos(\pi/7)=1.8019377358\ldots.
\]

Therefore a model-matched SAT compiler with
\[
T(N)\le N^{C+o(1)},\qquad S(N)\le N^{\rho+o(1)}
\]
contradicts the theorem whenever
\[
\boxed{C+\rho<\gamma.}
\]

This is the endpoint. The compiler remains OPEN.

## 2. WILLIAMS-LANDING-REGION2 — PROVED/EXACT accounting

For a one-type fractional SAT recursion with local work exponent \(r\), at most
\(N^{\eta+o(1)}\) child SAT instances, each of length at most
\(N^{\theta+o(1)}\), fixed \(\theta<1\), RECURCLOSE1 gives
\[
C=\max\left\{r,\frac{\eta}{1-\theta}\right\}.
\]

With explicit child materialization and local workspace exponent \(\sigma\),
\[
\rho=\max\{\sigma,\theta\}.
\]

Hence the exact conditional Williams landing condition is
\[
\boxed{
\max\left\{r,\frac{\eta}{1-\theta}\right\}
+\max\{\sigma,\theta\}
<
2\cos(\pi/7).
}
\]

For the important baseline \(r=1,\sigma=0\):
\[
\boxed{
\max\left\{1,\frac{\eta}{1-\theta}\right\}+\theta<1.8019377358.
}
\]

Concrete admissible targets:
\[
(\theta,\eta)=(1/2,1/2)\Rightarrow(C,\rho)=(1,1/2),\quad C+\rho=3/2;
\]
\[
(\theta,\eta)=(2/3,1/3)\Rightarrow(C,\rho)=(1,2/3),\quad C+\rho=5/3;
\]
\[
(\theta,\eta)=(3/4,1/5)\Rightarrow(C,\rho)=(1,3/4),\quad C+\rho=7/4;
\]
\[
(\theta,\eta)=(0.8,0.15)\Rightarrow(C,\rho)=(1,0.8),\quad C+\rho=1.8.
\]

For constant fanout \(\eta=0\) with linear local work, explicit children are sufficient whenever
\[
\boxed{\theta<\gamma-1=0.8019377358\ldots.}
\]

## 3. MACRO-DIAMOND-WILLIAMS1 — conditional architecture

A useful final wrapper should operate in macro-diamonds rather than one-variable diamonds.

At macro state size \(N\), it should perform cheap source/control work and produce at most
\[
N^{\eta+o(1)}
\]
explicit SAT children, each of size
\[
N^{\theta+o(1)},\qquad\theta<1,
\]
with an exact combiner preserving the parent SAT answer.

The same construction must recurse uniformly on every child.

No invocation of the original hypothetical SAT algorithm \(A\) is permitted on a current-scale or \(N^{1-o(1)}\)-scale SAT instance before the contraction has happened.

If the above landing inequality holds, recursive closure enters the Williams forbidden product region.

## 4. PRECONTRACTION-A-GUARD2 — PROVED/EXACT accounting

Let the hypothetical SAT decider have unknown polynomial exponent \(K\).

A direct call to \(A\) on a query of size
\[
N^{\delta+o(1)}
\]
contributes
\[
N^{\delta K+o(1)}
\]
before multiplicity charges.

If \(\delta=1-o(1)\), the compiled exponent retains the unknown \(K\). Therefore:

\[
\boxed{
\text{the final Williams compiler may not use }A
\text{ to choose its early macro branches before genuine contraction.}
}
\]

This is the present failure of the SAT-native reconvergent wrapper: its A/B branch bits are obtained by calling \(A\) on restrictions that are still current-scale.

Prime/hash control operations may occur at current scale if their own charged local work fits \(r\), but an unresolved SAT-semantic call may not.

## 5. Cheap same-scale wrapper control is not itself fatal

CYCLEGAIN1 already shows that an individual same-scale typed control edge need not destroy exponent erasure if the complete well-founded return cycle contains genuine contraction.

Thus a design of the form
\[
\text{SAT source}
\to
\text{same-scale prime/hash/control state}
\to
\text{contracted SAT child }N^\theta
\]
is compatible with the recurrence analysis provided:

1. the same-scale edge does not invoke \(A\);
2. the wrapper/control state is not materialized as a current-scale SAT child;
3. the complete return cycle genuinely contracts;
4. all local work and workspace are charged.

The missing object is the contracted SAT child.

## 6. MACRO-LINEAGE-SPACE1 — PROVED/EXACT accounting

Suppose one realized recursive path has at most \(N^{\eta+o(1)}\) child choices at source size \(N\), and child size at most \(N^{\theta+o(1)}\).

At level \(j\), recording the selected child index needs at most
\[
\eta\theta^j\log_2 N+o(\log N)
\]
bits.

Summing over the \(O(\log\log N)\) nontrivial levels:
\[
\sum_{j\ge0}\eta\theta^j\log_2N
=
\frac{\eta}{1-\theta}\log_2N.
\]

Therefore:
\[
\boxed{
\text{the exact realized macro-route lineage can be retained in }O(\log N)
\text{ bits.}
}
\]

A level/index-keyed prime representation is also polylogarithmic-bit after charging its indices.

This changes the role of the prime model. Per-variable exact prime lineage is potentially linear-space on sparse inputs and is unsuitable as live Williams state. Prime lineage should instead label macro-branch choices after fractional contraction has been achieved.

For \(N=2^{80}\), the finite accounting experiment gives approximately:

- \((\theta,\eta)=(1/2,1/2)\): 5 nontrivial levels, 77.5 route bits;
- \((2/3,1/3)\): 8 levels, 76.9 route bits;
- \((3/4,1/5)\): 11 levels, 61.3 route bits.

These are accounting examples, not a shrinker construction.

## 7. OBLIVIOUS-COVER-GUARD1 — PROVED/EXACT

Consider a formula-independent family of \(q\) partial assignments on \(n\) variables, each leaving at most \(\ell\) variables live.

If the family is required to preserve satisfiability for every formula having an arbitrary unique satisfying assignment \(a\in\{0,1\}^n\), the restriction cylinders must cover the Boolean cube.

Each restriction covers at most \(2^\ell\) full assignments. Hence
\[
\boxed{q\,2^\ell\ge2^n.}
\]

Therefore
\[
\boxed{q\ge2^{n-\ell}.}
\]

In particular, if \(q=\operatorname{poly}(n)\),
\[
\ell\ge n-O(\log n).
\]

So a formula-independent polynomial-fanout block restriction cannot yield a fixed fractional live-variable exponent.

For \(n=512\):

- \(\ell=\lceil n^{1/2}\rceil=23\) requires at least \(2^{489}\) oblivious children;
- \(\ell=\lceil n^{2/3}\rceil=64\) requires at least \(2^{448}\);
- \(\ell=\lceil n^{0.8}\rceil=148\) requires at least \(2^{364}\).

The successful shrinker must therefore be genuinely source-dependent.

## 8. SUMMARY-COVER-GUARD1 — PROVED/EXACT

Suppose the restriction family is allowed to depend only on a \(B\)-bit summary \(z(F)\), with at most \(q\) restrictions per summary and at most \(\ell\) live variables per restriction.

There are at most \(2^Bq2^\ell\) assignment cylinders available across all summary classes. Applying the same unique-witness control gives
\[
\boxed{
B+\log_2q+\ell\ge n.
}
\]

Thus a small summary plus polynomially many children cannot select a strongly shrinking restriction on this control family.

For the numerical target \(\ell=n^{2/3}\), \(q=n^{1/3}\), the lower bound on \(B\) approaches \(n-o(n)\).

This does not rule out repeated rereading of the full source \(F\), nor a source-dependent semantic compressor. It rules out obtaining the Williams shrinker merely from a short hash/route summary.

## 9. Current wrapper components against the Williams target

### Prime/multisign lineage
Useful for exact identity/accounting, but not itself contraction. Per-variable explicit retention can be linear-space. Macro-level lineage is compatible with \(N^{o(1)}\) space.

### Reconvergent SAT-native A/B branches
Current version fails PRECONTRACTION-A-GUARD2 because the branch bits come from current-scale calls to \(A\).

### BAD-SEED
BAD-SEED compactly represents exponentially many wrapper routes, but the current BAD formula still carries/uses the source at current scale. Calling \(A(\mathrm{BAD}_F)\) therefore retains the unknown exponent \(K\).

### Wrapper-as-SAT
Formula-internal merge forcing is real, but the wrapper CNF is still current-scale and existential projection can bypass the history variables. It does not yet produce a smaller SAT child.

### Recursive feedback
Potentially useful: same-scale cheap control edges are permitted if the complete return cycle contracts. Feedback alone does not create contraction.

## 10. SOURCE-CARRY boundary

If a purported child explicitly contains an injective/decodable copy of the full \(N\)-bit source, its encoded length is \(\Omega(N)\), so it cannot have fixed \(\theta<1\).

This guard does not rule out lossy SAT-semantic compression: under \(P=NP\), the hypothetical decision bit itself is a one-bit semantic compression. The issue is acquisition.

Thus the required object is not an information-theoretic source compressor but a **fast semantic compressor derived from the code of \(A\) without running \(A\) at current scale**.

## 11. Connection to Williams 2024

Williams' 2024 self-improvement theorem for Circuit-SAT repeatedly embeds faster algorithms into new circuit instances. The paper explicitly asks whether self-improvement can be pushed all the way to the \(P=NP\) regime and notes bottlenecks preventing the current method from reaching that point.

The present Williams-landing compiler target is therefore not a routine consequence of known self-improvement. It is closely aligned with that open problem.

The potentially new ingredient offered by the current project is formula-internal recursive lineage / reconvergence. To be useful, it must generate a genuine pre-\(A\) macro-contraction, not merely additional state around a current-scale \(A\) call.

## 12. New single target: PRE-A-MACRO-SHRINK1

A sufficient concrete theorem would be:

> For every hypothetical exact polynomial-time SAT decider \(A\), there is a uniform source-dependent procedure \(R_A\) which, on an \(N\)-bit SAT instance \(F\), before invoking \(A\) on any \(N^{1-o(1)}\)-size instance, runs in \(N^{1+o(1)}\) local time and \(N^{o(1)}\) local workspace and constructs at most
> \[
> N^{1/3+o(1)}
> \]
> explicit SAT children of length at most
> \[
> N^{2/3+o(1)}
> \]
> together with an exact polynomial-time combiner satisfying
> \[
> \operatorname{SAT}(F)
> =
> \operatorname{COMBINE}
> \bigl(\operatorname{SAT}(G_1),\ldots,\operatorname{SAT}(G_q)\bigr).
> \]

Recursive closure would then give
\[
C=1,\qquad\rho=2/3,\qquad C+\rho=5/3<2\cos(\pi/7),
\]
contradicting the Williams endpoint.

The same theorem with one child and any fixed
\[
\theta<0.8019377358
\]
would also suffice if local work is near-linear and workspace does not exceed the child scale.

## 13. What must now be built

The prime/hash DAG should be redesigned as a **macro-contraction certificate**, not a variable-by-variable SAT-query router.

At each macro step it should attempt to:

1. use only source syntax, the fixed code of \(A\), and charged cheap computation;
2. quotient many variable-level histories into a polynomial-size family of macro states;
3. certify that the quotient preserves the parent SAT answer;
4. emit explicit smaller standard-SAT children before the first semantic call to \(A\);
5. store only macro-route lineage, not the full variable-level history.

The exact missing theorem is the semantic quotient/selector in steps 2--4.

## 14. Status

**PROVED/EXACT accounting/guards**
- Williams product landing inequality;
- PRECONTRACTION-A-GUARD2;
- MACRO-LINEAGE-SPACE1;
- OBLIVIOUS-COVER-GUARD1;
- SUMMARY-COVER-GUARD1;
- source-carry injective boundary.

**CONDITIONAL**
- MACRO-DIAMOND-WILLIAMS1;
- any concrete \((\theta,\eta)\) landing recipe.

**OPEN / LOAD-BEARING**
- PRE-A-MACRO-SHRINK1;
- source-dependent SAT-preserving macro quotient/selector;
- explicit model-matched child construction;
- nonrelativizing/nonalgebrizing hinge.

**P versus NP remains OPEN.**
