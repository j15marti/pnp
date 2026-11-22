# Boolean erasure levels: charged resource points and speedup transfers

Research date: 2026-11-22. This note continues `Static_Restriction_Resource_Transfer.md` and `Shortest_Obstructions_and_Charged_Incompatibility_2026-11-22.md`.

## 1. Main advance

For Boolean width at most three, the residual formula can be compiled into a table of at most

\[
L_3(r)=1+2r+4\binom r2+8\binom r3=O((r+1)^3)
\tag{1}
\]

distinct clause types on its \(r\) unknown variables. All compilation and indexing work is charged. This improves the direct assignment-stream bound \(\widetilde O(N2^r)\) to the attainable decision bound

\[
\boxed{T=\widetilde O\!\left(N+L_3(r)2^r\right),
\quad S_{\rm aux}=O\!\left(L_3(r)+r\log N+\log N\right).}
\tag{2}
\]

The term \(r\log N\) pays for a map from original variable identifiers to the unknown slots when that map is constructed in workspace. It can be omitted if an appropriate indexed map is supplied as part of the counted read-only input. The tilde in this note hides only fixed powers of \(\log(N+2)\), not arbitrary factors polynomial in \(r\).

Consequently, for

\[
r=c\log_2 N+o(\log N),
\]

there is a uniform correct solver with

\[
\boxed{T\le N^{\max\{1,c\}+o(1)},\quad
S_{\rm aux}=N^{o(1)},\quad
C_{\rm aux}\le N^{\max\{1,c\}+o(1)}.}
\tag{3}
\]

These are upper-bound witnesses, not a characterization of the exact fastest solver. An elementary clause-branching argument improves (3) further. Let \(\lambda\) be the positive root greater than one of \(\lambda^3=\lambda^2+\lambda+1\), and put \(\beta=\log_2\lambda\). Then

\[
\lambda=1.839286755214161\ldots,\qquad
\beta=0.879146421606638\ldots.
\]

The same charged compilation followed by depth-first clause branching gives

\[
\boxed{T=\widetilde O(N+\operatorname{poly}(r)\lambda^r),\quad
S_{\rm aux}=O(L_3(r)+r\log N+\log N).}
\tag{3a}
\]

For logarithmic \(r\), both the time and auxiliary-CM upper exponents become \(\max\{1,\beta c\}\), with subpolynomial workspace. This yields the conditional restriction-compression exclusion

\[
\boxed{c<\frac{2\cos(\pi/7)}{\log_2\lambda}
=2.0496446229193555\ldots,}
\tag{3b}
\]

when the required both-label, locally accessible, quasilinear reduction exists. This is the threshold furnished by one elementary complete procedure. No optimality or strongest-known upper-bound claim is made. Compilation alone already improves the predecessor's threshold from \(c<0.801937\ldots\) to \(c<1.801937\ldots\).

An optimized near-satisfying assignment can also give a cheap path with arbitrarily many unknowns. The guarded source family below has a two-row obstruction through all but its last two unpinning steps. Its final unpin nevertheless encodes arbitrary strict 3-SAT. These two facts coexist because the earlier pinned restrictions do not preserve SAT labels.

## 2. Fresh inputs and the charged model

The input is a source 3-CNF formula and a supplied partial assignment, leaving exactly \(r\) variables unknown. Every level is a new static input. No earlier computation or answer is retained between levels. A correct algorithm must handle both SAT and UNSAT residual inputs.

Let \(N\) be the complete encoded input length: source rows, variable identifiers, headers, supplied values, unknown flags, and every supplied index or locator. Input variables and rows are explicitly represented in the canonical source format. In particular, the declared variable count cannot be exponentially larger than the source representation through a free binary header.

The machine is a deterministic random-access bit model. Logical bit operations and address construction are charged. A Boolean vector of length \(2^r\) is not a unit-cost object. Read-only input is excluded from auxiliary workspace. Source value pins have an indexed representation, and the necessary unknown-slot map is either supplied within \(N\) or built and charged. An arbitrary unsorted serialization with expensive lookup is not silently assigned this access interface.

For live usable auxiliary storage \(s_t\), including addresses, registers, indices, retained representations, and memory-management data, define

\[
T=\text{number of charged steps},\qquad
S_{\rm aux}=\max_t s_t,\qquad
C_{\rm aux}=\sum_{t=0}^{T}\max\{1,s_t\}.
\tag{4}
\]

The upper bound \(C_{\rm aux}\le(T+1)\max\{1,S_{\rm aux}\}\) is valid. The reverse inequality with \(T S_{\rm aux}\) is not generally valid, since a peak need not be retained for the whole execution.

All parsing, validation, map construction, representation construction, recomputation, and output are inside the charged interval. A near-linear preprocessing stage using logarithmic or polylogarithmic workspace has near-linear auxiliary CM up to polylogarithmic factors. A materialized input-sized writable copy changes that space and CM accounting.

## 3. Four explicit feasible points

Write

\[
M=2^r,
\qquad Q=r+\log N+U,
\]

where \(U=O(r\log N)\) if an unknown-identifier map is constructed and retained, and \(U=0\) if the needed map is accessible directly from counted read-only input. A sorted read-only unknown-identifier array can serve as the latter map through charged binary searches. Constructing such an array in workspace incurs the former cost.

### 3.1 Assignment streaming

Maintain one \(r\)-bit completion, scan the source, and evaluate every clause under the supplied pins and that completion. A source scan uses \(N\operatorname{polylog}N\) bit time, including identifier lookup and address construction. Repeat until a model is found or all completions have been tested. This gives

\[
T_{\rm stream}=\widetilde O(NM),\qquad
S_{\rm stream}=O(Q),\qquad
C_{\rm stream}=\widetilde O(NM Q).
\tag{5}
\]

Under the rank-indexed read-only convention, the space is \(O(r+\log N)\). Without that convention, the retained unknown-ID map is explicitly included in \(Q\). Neither convention treats verification of the source or its indexing as free.

### 3.2 A retained dense forbidden-assignment mask

Allocate \(M\) bits indicating which assignments have been excluded. Every residual clause forbids one subcube. Generate that clause's membership test while scanning the mask and OR its result into the appropriate entries. A separate length-\(M\) mask need not be retained for every row. At most three unknown-slot tests determine each membership bit; the counter and input-address work are charged.

For \(m\) source clauses, a conservative bound using sequential mask scans is

\[
T_{\rm mask}=\widetilde O\!\left(N+(m+1)M\right),
\quad S_{\rm mask}=O(M+Q),
\]

\[
C_{\rm mask}=\widetilde O\!\left((N+(m+1)M)(M+Q)\right).
\tag{6}
\]

Since \(m\le N\), the simpler bounds \(\widetilde O(N2^r)\) time and \(\widetilde O(N2^r(2^r+Q))\) auxiliary CM also hold. When the mask dominates the other workspace, this latter CM bound is \(\widetilde O(N4^r)\).

A packed-word implementation may process several bits per word operation on a word-RAM. That speedup belongs to the declared word model. In the bit model, constructing and combining a word's bits has a cost. For \(r=O(\log N)\), word lengths and these simulation factors are polylogarithmic, so the polynomial exponent comparisons below are unchanged. No \(2^r\)-bit operation is charged as one step.

The mask bound uses consecutive tape-cell scans, with an incremented assignment counter; it does not reconstruct an arbitrary \(r\)-bit mask address for every cell. If a different implementation uses full-address random access per mask bit, an additional conservative factor \(O(r)\) should be included. This distinction does not affect the logarithmic-\(r\) exponents or the clause-type compilation bound.

### 3.3 Compile clause types, then stream assignments

After substituting supplied values, each row is true, false, or a clause of width at most three on the unknown slots. Remove satisfied rows, repeated literals and tautologies. A false residual row immediately proves UNSAT. Otherwise normalize each remaining row by sorting its at most three signed slot identifiers and set its bit in the clause-type presence table of size \(L_3(r)\).

Initializing the table and constructing the identifier map are charged. A source row has a canonical type index computable with arithmetic on \(O(\log N)\)-bit integers. The complete source is scanned once. The table contains only presence information, since duplicate clauses do not change the decision question. Original row locators are not needed for this decision algorithm; outputting a particular core would be a separate requested service.

Then enumerate assignments and evaluate the distinct residual types. This gives

\[
T_{\rm types}=\widetilde O\!\left(N+L_3(r)M\right),
\quad S_{\rm types}=O\!\left(L_3(r)+Q\right),
\]

\[
C_{\rm types}=\widetilde O\!\left((N+L_3(r)M)(L_3(r)+Q)\right).
\tag{7}
\]

The improvement over (5) comes from paying for the long source once. When \(r=O(\log N)\), all distinct residual clause types fit in polylogarithmic workspace, even when the original source is much longer.

These are three feasible implementations, not three lower bounds. Their resource components are kept together; taking the time of one implementation and the space of another would not establish an attainable simultaneous point.

### 3.4 An elementary branching improvement after compilation

The compiled representation also permits algorithms that do not examine every full assignment. At a recursive search node, reduce its clauses under the current partial assignment. An empty clause closes that branch as UNSAT; no remaining clauses supplies a satisfying extension. Otherwise choose any remaining clause with distinct unknown variables.

For a width-three clause \(\ell_1\lor\ell_2\lor\ell_3\), partition its satisfying assignments by their first true literal:

\[
\ell_1=1;\qquad
\ell_1=0,\ \ell_2=1;\qquad
\ell_1=0,\ \ell_2=0,\ \ell_3=1.
\tag{7a}
\]

The branches are disjoint, cover all models satisfying the clause, and fix one, two, and three previously unknown values, respectively. A binary clause gives only the first two branches; a unit gives only the first. Each branch therefore has strictly fewer unknowns, and the method is sound and complete for both SAT and UNSAT inputs.

If \(V(h)\) bounds the number of visited search nodes with \(h\) unknowns, the width-three case satisfies

\[
V(h)\le1+V(h-1)+V(h-2)+V(h-3),
\]

with finite base cases at \(h=0,1,2\); the shorter-clause cases only reduce this bound. The defining equation for \(\lambda\) implies \(V(h)=O(\lambda^h)\). For example, an inductive bound of the form \(A\lambda^h-1/2\), with a sufficiently large fixed \(A\), absorbs the additive one exactly.

Each node can rescan the immutable type catalog and reduce its clauses using the current assignment, taking \(\operatorname{poly}(r)\) bit work. The implementation retains one catalog, a tri-valued assignment, and a depth-first undo/branch stack. Each frame records only a constant number of variable indices and branch metadata. The stack uses \(O(r\log(r+2))\) bits; no separate residual catalog is retained for every depth.

Consequently,

\[
T_{\rm branch}=\widetilde O\!\left(N+\operatorname{poly}(r)\lambda^r\right),
\quad S_{\rm branch}=O(L_3(r)+Q+r\log(r+2)),
\]

\[
C_{\rm branch}=\widetilde O\!\left(
(N+\operatorname{poly}(r)\lambda^r)
\,(L_3(r)+Q+r\log(r+2))\right).
\tag{7b}
\]

Since \(r\le N\), the general retained-ID-map bound already absorbs the stack term. At logarithmic \(r\), all nonexponential terms are polylogarithmic. This elementary improvement shows directly why a completion count is not a compulsory operation count. Other complete procedures remain allowed; the displayed branching recurrence is an upper-bound witness, not a mandated proof architecture.

### Fixed and logarithmic numbers of unknowns

For every fixed \(r\), each route gives the conservative point

\[
T=\widetilde O(N),\qquad S_{\rm aux}=O(\log N),\qquad
C_{\rm aux}=\widetilde O(N).
\tag{8}
\]

For \(r=c\log_2 N+o(\log N)\), the following exponents are attainable upper bounds. A space exponent zero means subpolynomial space, not constant space.

| Route | Time exponent | Auxiliary-space exponent | Auxiliary-CM exponent |
|---|---:|---:|---:|
| Repeated source scans | \(1+c\) | 0 | \(1+c\) |
| Retained dense mask | \(1+c\) | \(c\) | \(1+2c\) |
| Charged clause-type compilation | \(\max\{1,c\}\) | 0 | \(\max\{1,c\}\) |
| Type compilation and elementary clause branching | \(\max\{1,\beta c\}\) | 0 | \(\max\{1,\beta c\}\) |

If all \(N\) input bits are physically resident for the entire run, physical CM is instead

\[
C_{\rm phys}=N(T+1)+\sum_t s_t
=\Theta(NT+C_{\rm aux})
\tag{9}
\]

up to the harmless positive-baseline convention. Thus the type-compilation/enumeration route has physical-CM upper exponent \(1+\max\{1,c\}\), while its auxiliary-CM exponent is \(\max\{1,c\}\). With elementary branching, the corresponding exponents are \(1+\max\{1,\beta c\}\) and \(\max\{1,\beta c\}\). The extra input residence must not be omitted or later counted twice.

## 4. Optimized near-assignment paths can stay cheap at large r

Suppose an UNSAT strict 3-CNF has a full assignment \(\alpha\) violating exactly one row \(C_*\). Choose a variable \(x\) of that row. Flipping only \(x\) makes \(C_*\) true, so some other row \(D\) must become false. Therefore \(C_*\) and \(D\), after \(x\)'s value is erased, become opposite units under \(\alpha\)'s remaining values.

Keep

\[
B=(\operatorname{vars}(C_*)\cup\operatorname{vars}(D))\setminus\{x\}
\]

pinned. There are at most four guard variables in \(B\). Erasing every other value preserves the same two-row contradiction. No new singleton contradiction can appear when restrictions are relaxed, so the minimum source-core size remains exactly two throughout this guarded portion.

This semantic existence claim does not make the two rows free to locate. A fixed correct recognizer can exploit them in near-linear time and logarithmic space when a candidate row is explicitly locatable, for example when \(C_*\) is the first source row, or when a checked locator is supplied in the counted input. It remembers that row's remaining variable and polarity and scans for the opposing unit. If recognition fails, it invokes a complete fallback. Discovering an arbitrary opposing pair among an unordered collection of variable identifiers is a different task and is not assigned a free index here.

The explicit guarded family in the next section places the useful rows first. It therefore gives a sound correct solver whose executions on those pinned inputs have

\[
T=\widetilde O(N),\qquad S_{\rm aux}=O(\log N),\qquad
C_{\rm aux}=\widetilde O(N),
\tag{10}
\]

even when \(r\) is almost the number of source variables. Complete input authentication can be included in that bound. If well-formed inputs and indexed pins are already the input convention, merely recognizing the fixed guard rows can take less than a full source scan.

Equation (10) concerns this recognized structured family. It is not a near-linear algorithm for all large-\(r\) residual 3-SAT instances.

## 5. A final unpin can preserve full SAT hardness

Let \(H\) be a strict 3-CNF with \(n\) variables and \(m\) clauses. Introduce fresh \(p,x,a,b\), plus one fresh \(s_C\) per source clause \(C\). Put the following four rows first:

\[
(p\lor x\lor a),\quad(p\lor x\lor\neg a),\quad
(p\lor\neg x\lor b),\quad(p\lor\neg x\lor\neg b).
\tag{11}
\]

Replace each source clause \(C=(\ell_1\lor\ell_2\lor\ell_3)\) by

\[
(\neg p\lor\ell_1\lor s_C),\qquad
(\neg s_C\lor\ell_2\lor\ell_3).
\tag{12}
\]

Call the resulting strict 3-CNF \(F(H)\). It has

\[
n_F=n+m+4,\qquad m_F=2m+4.
\tag{13}
\]

The guards force \(p=1\), and at \(p=1\) each pair (12), after existentially choosing \(s_C\), is equivalent to its source clause. Hence

\[
\boxed{F(H)\text{ SAT}\iff H\text{ SAT}.}
\tag{14}
\]

At the all-zero reference assignment, exactly the first guard row is false, independently of whether \(H\) is satisfiable. Erase \(a\) first and keep \(p=x=0\). The first two rows become \(a\) and \(\neg a\). Erase \(b\), all original variables, and all \(s_C\) in any order while keeping those two pins. The two-row obstruction persists through \(r=n_F-2\).

Next release \(x\), leaving only \(p=0\). The four guards give a four-row minimal obstruction. Finally release \(p\). The decision is now exactly the original arbitrary SAT decision by (14). For an UNSAT source, the companion obstruction argument gives the profile

\[
\mu_r=2\quad(1\le r\le n_F-2),\qquad
\mu_{n_F-1}=4,\qquad
\mu_{n_F}=4+2\mu(H).
\tag{15}
\]

For computational cost, a single uniform recognizer can use the same four-row implication \(\text{guards}\Rightarrow p=1\) at every pre-final stage. Together with the supplied \(p=0\), this already refutes the input, irrespective of which other values remain supplied. Thus the near-linear/logarithmic-space bound holds throughout the path without requiring discovery of a shortest two-row core. This is an explicit example of allowing a larger source support when its shared recognition is simpler.

An alternative order, erasing \(x\) first and keeping \(p=a=b=0\), gives a longer profile with a three-row stage before the four-row stage. Its resource interpretation is the same: the few final guard releases can contain the transition to unrestricted hardness.

For example, when \(H\) contains all eight full clauses on three variables, \(n_F=15\), \(m_F=20\), and (15) is 2 for levels 1 through 13, then 4, then 20. These numerical values are symbolic consequences of the displayed compiler and the eight-clause cube obstruction; this resource note performs no new enumeration.

### Complete encoded-length and local-access accounting

For the project's canonical explicit-variable, fixed-record source format,

\[
N_F=O((n+m)\log(n+m))=\widetilde O(N_H).
\tag{16}
\]

An all-unknown value array contributes only \(O(n_F)\) further bits and is included in this bound. The output header and length can be determined in \(\widetilde O(N_H)\) time and \(O(\log N_H)\) workspace. A requested output bit is a guard constant, an auxiliary identifier computed from a row index, or a bit of one of a constant number of source literal records. Thus requested-bit generation takes polylogarithmic time and logarithmic workspace. Arithmetic and input accesses are charged.

A simulation can generate requested output bits on demand, without creating a writable \(N_F\)-bit output buffer. Setup has \(\widetilde O(N_H)\) auxiliary CM. Subsequent simulation multiplies the target's time and auxiliary CM by at most polylogarithmic factors and adds logarithmic scratch space. Therefore any strict-gap polynomial-exponent time-space or auxiliary-CM exclusion for eligible SAT transfers to the final unpinned family.

The earlier \(p=0\) restrictions are UNSAT for both satisfiable and unsatisfiable \(H\). They are not a both-label SAT reduction. Cheap recognition of those stages does not violate any published SAT lower bound.

## 6. What a speedup would and would not contradict

The published small-workspace SAT time endpoint used here is

\[
\alpha=2\cos(\pi/7)=1.8019377358\ldots.
\tag{17}
\]

For every fixed \(t<\alpha\), the relevant deterministic random-access model excludes a correct SAT solver with time \(n^{t+o(1)}\) and workspace \(n^{o(1)}\). The corrected Williams manuscript states this endpoint and its model; FLMV supplies the local completeness framework and earlier time-space tradeoffs [1,2]. Strict exponent slack absorbs the charged polylogarithmic local-simulation overhead.

### Improved restriction-compression obstruction

Suppose a uniform reduction maps every eligible \(n\)-bit SAT source, on both labels, to a fresh residual 3-SAT instance with complete length \(N\le n\operatorname{polylog}n\), logarithmic-workspace/polylogarithmic-time requested-bit access, near-linear charged setup, and

\[
r\le c\log_2 N+o(\log N).
\]

Composing that reduction with clause-type compilation and elementary clause branching gives

\[
T(n)\le n^{\max\{1,\beta c\}+o(1)},\quad S(n)=n^{o(1)}.
\]

Consequently such a reduction is excluded whenever

\[
\boxed{c<\alpha/\beta=2.0496446229193555\ldots.}
\tag{18}
\]

The earlier direct-streaming argument only excluded \(c<\alpha-1\); compilation with exhaustive assignment enumeration gives the intermediate exclusion \(c<\alpha\). Elementary clause branching strengthens it again. None of these procedures supplies the missing reduction.

More generally, any uniform deterministic complete residual procedure using \(2^{\beta' r+o(r)}\operatorname{poly}(r)\) time and \(\operatorname{poly}(r)\) workspace, after charged type compilation, gives the conditional threshold \(c<\alpha/\beta'\) for \(\beta'>0\). This parameterized statement keeps every sound alternative available instead of treating one chosen search bound as a lower bound.

Simply selecting values to retain does not satisfy this hypothesis: an UNSAT formula remains UNSAT under every restriction, but a SAT formula may lose all its models. Optimizing a path on chosen UNSAT instances therefore cannot substitute for a reduction preserving both labels.

### Algebra for a proposed speedup

Suppose a complete algorithm improves the expensive phase by a factor \(f(N,r)=N^{d+o(1)}\) at \(r=c\log_2 N+o(\log N)\), while leaving the charged near-linear setup. The exponent implications are

| Baseline expensive phase | Resulting time exponent |
|---|---:|
| \(N2^r\) | \(\max\{1,1+c-d\}\) |
| \(L_3(r)2^r\) after compilation | \(\max\{1,c-d\}\) |
| \(\operatorname{poly}(r)\lambda^r\) after compilation | \(\max\{1,\beta c-d\}\) |

A subpolynomial-workspace implementation would contradict the endpoint only if this exponent is strictly below \(\alpha\), and only on a class retaining the both-label local SAT reduction. A speedup on the guarded UNSAT plateau has no such consequence. A speedup that needs more workspace must instead be compared with the applicable time-space region.

If a reduction expands length to \(N\le n^{\lambda+o(1)}\), target time exponent \(t\) becomes \(\lambda t\), subject to any larger setup exponent. Target workspace exponent \(s\) becomes \(\lambda s\), subject to reduction scratch space. The source exponent, not the unscaled target exponent, is the one compared with a SAT theorem.

## 7. Auxiliary-CM exclusions and memory-changing speedups

The corrected Williams manuscript's Table I supplies forbidden simultaneous time-space points, including \((1.24,0.666)\). Its Theorem 4.11 supplies the conservative product exclusion \(t+s<\varphi\), where \(\varphi=(1+\sqrt5)/2\). An earlier stronger general product claim near 1.801 is explicitly withdrawn in that manuscript; it is not used here [2].

For the project's standalone auxiliary-CM transfer, require the following additional model properties: initially only polylogarithmic auxiliary state; at most \(g(N)=\operatorname{polylog}N\) new usable bits per charged step; no free preprocessing; and simulation in the published random-access model with polylogarithmic overhead. Under these hypotheses,

\[
T\le C_{\rm aux},\qquad
S_{\rm aux}=O\!\left(s_0+\sqrt{g(N)C_{\rm aux}}\right).
\tag{19}
\]

For the second inequality, a peak of size \(S\) above the initial state requires a preceding interval of length proportional to \(S/g\) during which at least a constant fraction of the peak is live. Those live-bit/time pairs contribute \(\Omega(S^2/g)\). This argument uses bounded growth, not an assumption that the peak lasts throughout the run.

Hence the table point excludes a complete auxiliary-CM bound

\[
\boxed{C_{\rm aux}\le N^{\gamma+o(1)}
\quad\text{for any fixed }\gamma<1.24}
\tag{20}
\]

on the final unpinned hard family, with all local simulation overhead and setup charged. Indeed, it would give time exponent at most \(\gamma<1.24\) and space exponent at most \(\gamma/2<0.62<0.666\). This is a transferred project consequence under the declared CM premises, not a separate published CM theorem and not a claim of the sharp CM frontier.

More generally, a proven time-space forbidden rectangle \((t_0,s_0)\) yields a standalone auxiliary-CM exclusion for \(\gamma<\min\{t_0,2s_0\}\). If an implementation supplies explicit time and peak-space exponents \((t,s)\), then \(C_{\rm aux}\le N^{t+s+o(1)}\) is a valid upper bound. It may be loose when large space is transient. A speedup must be evaluated using the same implementation's complete resource vector; faster time alone does not imply lower CM.

Input-inclusive physical CM does not satisfy the small-initial-auxiliary-state premise when \(N\) resident input bits are counted from the beginning. Its residence tariff is (9), and it must be reported separately.

## 8. Scope and remaining proof obligation

The bounds above are feasible resource points and rigorously conditional exclusions. They show that fixed or logarithmic residual uncertainty can be processed with small workspace, that a carefully guarded large-uncertainty family can remain easy, and that a final released pin can restore a full both-label SAT reduction.

They do not establish the fastest possible time at every erasure level. They do not require assignment enumeration, mask construction, a particular proof system, or fresh local work after a charged representation already determines the answer. Any claimed lower bound must continue to allow shorter or longer cores, joint reasoning, algebraic shortcuts, caching, preprocessing and shared representations, with each physical event charged once.

The unresolved lower-bound step is to force every hypothetical fast complete solver into one of the excluded simultaneous resource regions, or to prove a stronger region. Counting released variables, possible assignments, or separate semantic branches supplies neither implication.

## References and verification record

[1] Lance Fortnow, Richard Lipton, Dieter van Melkebeek, and Anastasios Viglas. *Time-Space Lower Bounds for Satisfiability*. Journal of the ACM 52(6), 835-865, 2005. Author manuscript: <https://lance.fortnow.com/papers/files/tst.pdf>. Inspected Section 2.1 for the random-access model and the stated local completeness framework.

[2] Ryan Williams. *Alternation-Trading Proofs, Linear Programming, and Lower Bounds*. Corrected author manuscript: <https://people.csail.mit.edu/rrw/automated-lbs.pdf>. Inspected the small-space endpoint on page A:2, Table I and Theorem 4.11 on A:18, and correction footnote 9 on A:17. Accessed 2026-11-22.

The two predecessor project notes were read. This note's upper bounds, improved compression transfer, guarded compiler resource accounting, and CM implications are symbolic derivations. The displayed branching root was numerically evaluated by 100 bisection iterations on \((1,2)\), followed by scalar logarithm and cosine evaluation, giving \(\lambda=1.839286755214161\), \(\beta=0.879146421606638\), and \(\alpha/\beta=2.0496446229193555\). These decimal calculations are illustrative; the statements use the exact root and exact cosine expression. No benchmark or exhaustive-search result is claimed in this resource continuation.
