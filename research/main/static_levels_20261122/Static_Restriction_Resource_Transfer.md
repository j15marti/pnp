# Static restriction levels, uncertainty weight, and simultaneous resource exclusions

Research date: 22 November 2026, America/Los_Angeles.

Named continuation: STATIC-RESTRICTION-FRONTIER1.

Status: exact elementary implications, scoped published-theorem transfers, and an explicit conditional restriction-compression obstruction. The one-unknown and two-unknown problems are independent static input classes. No sequential-state or retained-history premise is imposed. No unrestricted separation or equality theorem is claimed. This contributor has not performed an independent formal-kernel verification.

## 1. Respecting the independent-level question

The purpose of the user’s erasure experiment is to characterize the least information and simplest possible route to a correct answer at each level. Each level starts afresh with the formula and the values still supplied. It is not one execution that has already seen a more informative state, and it is not a proposal to implement a particular algorithm.

For a formula or fixed-template constraint system F, let rho be a supplied partial assignment. Define the level-r decision class by inputs (F,rho) leaving exactly r variables unknown, with acceptance precisely when F restricted by rho has an extension. Both SAT and UNSAT residuals must be admitted. An analysis that promises every input is UNSAT would permit the constant answer and would no longer characterize decision against opposite-label alternatives.

The original full formula need not be satisfiable. If it is globally UNSAT, every restriction remains UNSAT. This does not invalidate the independent-level experiment: it means that a correct proof of compulsory work must compare the selected UNSAT instances with the SAT instances that the same solver is required to handle.

The input length N includes F, the supplied values, unknown-variable identifiers or flags, delimiters, and every other input field. The cost of discovering rho is outside this static problem when rho is supplied. It comes back into the budget if a later reduction or solver must produce rho from an unrestricted input.

## 2. A resource frontier, not a pointwise fastest machine

For each fixed correct deterministic algorithm A, let T_A(N,r), S_A(N,r), and C_A(N,r) denote worst-case time, peak auxiliary workspace, and auxiliary cumulative memory on the declared level-r class. Each resource is measured for that same algorithm and machine convention.

The useful object is the set of simultaneous upper-bound triples achievable by fixed uniform algorithms. A lower-bound statement rules out a region of that set. It need not assume that one universally fastest algorithm exists or that a minimum is attained.

Three quantifier guards are necessary.

1. Fix A before choosing input length and instance. A separate machine selected for one individual input or one finite length can contain a hardcoded finite answer table. Pointwise minimization over those machines is not an asymptotic uniform complexity bound.
2. Do not minimize time with one solver and space or CM with another and treat the minima as one achievable point. A simultaneous exclusion concerns one implementation satisfying all caps.
3. It is legitimate to analyze every fixed r separately. The statement that each fixed r has a polynomial bound, with constants or exponents depending on r, does not by itself provide a polynomial bound uniform in growing r.

An explicit algorithm can be used as a witness that a resource point is attainable. Such an upper-bound witness limits how expensive a fastest possible solver could be. Its role here is mathematical characterization, not a change of the project into algorithm construction.

## 3. Domain weight and relation-access cost

For unknown variables with finite domains D_1,...,D_r, define

\[
M=\prod_{i=1}^{r}|D_i|,
\qquad
w=\log_2 M=\sum_{i=1}^{r}\log_2|D_i|.
\tag{1}
\]

M is the number of possible completions and w is their total choice weight. Domain-one variables can be removed from this bookkeeping.

For Boolean inputs, one and two unknowns give M=2 and M=4. For the fixed five-element strict T5 template, they give M=5 and M=25. For a variable domain of size q, they give M=q and M=q^2. These are candidate counts, not compulsory operation counts.

Suppose a candidate completion can be checked in time V(N,w) and workspace W(N,w), including all reads and relation evaluation. Sequentially checking the candidates gives the attainable bounds

\[
T\le M V(N,w),
\qquad
S_{\rm aux}\le W(N,w)+O(w+I),
\tag{2}
\]

where I is the identifier/counter bookkeeping needed by the encoding. No lower bound of M operations follows from (1). A clause may eliminate many candidates, and an algebraic or symbolic representation may certify all of them at once.

The qualification about V is essential. Evaluation of a fixed finite relation has constant logical complexity. Evaluation of a supplied circuit describing a relation is itself computation and cannot be treated as a unit-cost oracle.

## 4. Explicit fixed-template static levels have small attainable resource points

Consider an explicitly represented fixed-template CSP or bounded-width CNF. Assume:

1. The constraint relation is fixed and can be evaluated with constant-size logical operations after its arguments are obtained.
2. Supplied values are accessible from a canonical read-only array, or an equivalent representation with polylogarithmic lookup cost.
3. Unknown variable identifiers are explicitly available and consistent with the supplied-value representation.
4. All encoding checks, address construction, and input accesses are charged.

For w=O(log N), the unknown identifiers can be retained in O(r log N)=polylog(N) bits, since the fixed nontrivial domain gives r=O(w). A candidate completion needs O(w) bits. Each constraint can be checked using polylogarithmic lookup work and bookkeeping. A complete check takes N polylog(N) time and polylog(N) auxiliary workspace.

Consequently,

\[
T\le 2^w N\operatorname{polylog}N,
\qquad
S_{\rm aux}=\operatorname{polylog}N
\quad\text{when }w=O(\log N).
\tag{3}
\]

For one or two unknown variables over a fixed finite domain,

\[
T=\widetilde O(N),\qquad
S_{\rm aux}=\operatorname{polylog}N,
\qquad C_{\rm aux}=\widetilde O(N)
\tag{4}
\]

is therefore an attainable point. Here C_aux includes a positive per-step baseline and sums live auxiliary bits. The CM upper bound follows by summing the workspace bound along the same execution.

If all N encoded input bits are retained and physically counted for the full execution, this implementation also has

\[
S_{\rm phys}=O(N+\operatorname{polylog}N),
\qquad C_{\rm phys}=\widetilde O(N^2).
\tag{5}
\]

Equations (4) and (5) are compatible: the resources use different memory conventions.

These bounds are encoding-sensitive. An unsorted list of supplied values may require costly rescans for lookup, and an index built during preprocessing must be charged. The near-linear and polylog-space claim is made for the stated access convention; it is not asserted for every serialization or an uncharged parser.

No lower bound on the exact fastest running time is supplied by (3). In familiar clause-probe models, small certificates can still require a linear number of probes to locate in the worst case. Such an acquisition lower bound must specify the probes and source family separately.

## 5. Conditional static restriction transfer theorem

The following statement gives a direct connection between the independent-level characterization and a simultaneous forbidden region.

### Theorem 1: low-weight restriction compression is excluded under a local transfer

Let L be a standard SAT source to which the published small-workspace lower bound applies. Suppose a uniform reduction maps every n-bit source to an explicit fixed-template residual instance with the following properties:

1. Correctness on both labels: the source is SAT if and only if the residual instance is SAT.
2. Complete output length N is at most n times a fixed polylogarithmic factor.
3. Each requested output bit can be generated in polylogarithmic time and O(log n) workspace from read-only random-access source input.
4. Output length and headers can be determined in n polylog(n) time and O(log n) workspace.
5. The target encoding satisfies Section 4's inexpensive supplied-value access convention.
6. For a fixed constant c>=0, uncertainty weight satisfies

\[
w\le c\log_2 N+o(\log N).
\tag{6}
\]

Then the reduction and (3) imply a uniform correct SAT solver with

\[
T(n)\le n^{1+c+o(1)},
\qquad S(n)=n^{o(1)}.
\tag{7}
\]

Consequently such a reduction is impossible if

\[
\boxed{c<2\cos(\pi/7)-1
=0.8019377358\ldots.}
\tag{8}
\]

**Proof.** The target witness in (3) takes time N^{1+c+o(1)} and polylogarithmic workspace. Simulate its read-only target input on demand. Each target input query costs only a polylogarithmic factor and O(log n) additional scratch space. There is no materialized N-bit writable target buffer. Header setup contributes n polylog(n) time. This gives (7). Under (8), choose a fixed exponent a strictly between 1+c and 2 cos(pi/7). Polylogarithmic overhead and the o(1) term are absorbed by the strict gap. The resulting solver contradicts the published subpolynomial-workspace SAT time bound [2,3]. QED.

Using only the original FLMV endpoint gives the weaker threshold

\[
c<\varphi-1=0.6180339887\ldots,
\qquad \varphi=(1+\sqrt5)/2.
\tag{9}
\]

One or two fixed-domain unknowns have w=O(1), hence c=0, and satisfy the forbidden compression target. The contradiction is with a hypothetical local reduction of all SAT inputs to those easy levels, not with their tractability.

An arbitrary supplied partial assignment does not provide the needed reduction. It preserves the UNSAT direction,

\[
F\text{ UNSAT}\Longrightarrow F|_\rho\text{ UNSAT},
\]

but can destroy every witness of a satisfiable F. Producing a restriction that preserves both labels for arbitrary F is an additional computational and correctness requirement. Selecting restrictions only on a known UNSAT family does not establish it.

More general output expansion rescales the target. If a sufficiently local reduction has N<=n^{lambda+o(1)}, then the same argument gives source time exponent lambda(1+c), plus any larger initialization exponent. The comparison must use that source exponent, not 1+c alone.

## 6. Why the compact forbidden-region target already has one unknown

The actual compact project language Q is different from the fixed strict symmetric T5 template. Its input contains a binary integer B>=2 and a Boolean circuit H describing canonical edges of a B-vertex base tournament. A fixed interpreter supplies reverse edges and a regular completion on q=2B+1 values.

Its ordered relation R(a,b,c) requires a to beat exactly one of b,c and lose to the other; equal values fail. Its decision expression is

\[
\exists x<q:\quad R(x,0,1)\land R(2B,x,B).
\tag{10}
\]

This language has one unknown variable and two relation occurrences. The circuit H varies between inputs, including at fixed q. No hardness claim for a single fixed cyclic tournament at every q follows.

The predecessor [4] supplies the following compiler from its fixed-record 3CNF source F with k explicitly represented variables and h clauses:

\[
B=2^k+2,\qquad q=2^{k+1}+5,
\]

\[
H_F(i,j)=\neg\left(
[i=0]\land[j\ge2]\land
F((j-2)\bmod2^k)
\right)
\quad(i<j<B).
\tag{11}
\]

The candidate label 2+int(y) satisfies the first relation precisely when F(y)=1. The second relation filters the regular-completion labels and retains originals. Thus (10) has a witness exactly when F does.

H_F has O(k+h) gates in a fixed layout. Its full encoding has length O((k+h)log(k+h))=O(n log n). A requested output bit depends on arithmetic over O(log n)-bit indices and, for clause gates, a constant number of fixed source records. The predecessor gives polylogarithmic requested-bit generation and O(log n) scratch space.

The source format is chosen within the standard local Cook-Levin construction. This does not assert equally cheap arbitrary-text SAT normalization. The original local completeness invocation is a stated inherited premise; this continuation inspected the symbolic compiler and primary model statements but did not independently formalize Cook-Levin.

The important parameter is

\[
w=\log_2 q=\Theta(k),
\]

not the one variable name. Furthermore, the relation-access circuit retains the source predicate. The fixed-template scan theorem from Section 4 does not apply to H as a free lookup operation.

### Consequences for proposed one-variable characterizations

1. A complete solver with T=poly(N,log q) for compact Q would give a polynomial-time SAT solver. It would not contradict the existing fixed-polynomial forbidden regions merely because it is polynomial.
2. A complete solver with near-linear time and subpolynomial auxiliary workspace would contradict FLMV through the local compiler.
3. A bound T=poly(log q) that ignores circuit length is already impossible as a uniform bound on all compact inputs. At fixed q=13, a supplied long circuit can encode OR of arbitrarily many independent constant bits. Its answer requires acquiring those input dependencies in the worst case.
4. Fixed q does not make a supplied circuit cost-free. It gives a constant number of candidate evaluations, but those evaluations still depend on circuit size and structure.

## 7. Existing simultaneous exclusions and their hypotheses

The following are published source theorems or project transfers from them. They concern a correct uniform solver on all inputs of an eligible language, using complete encoded length N. Strict slack absorbs local-reduction and machine-simulation overheads.

### 7.1 Time and auxiliary workspace

FLMV [1] exclude

\[
T=N^{1+o(1)},\qquad S=O(N^{1-\epsilon})
\tag{12}
\]

for each fixed epsilon>0. More generally their explicit curve excludes simultaneous exponents a and b when 1<a<phi and b<D(a), with

\[
f_0(a)=1,\qquad f_{j+1}(a)=\frac{a f_j(a)}{1+f_j(a)},
\]

\[
D(a)=\sup_{j\ge2}\min\left\{
\frac{1/f_j(a)-a}{j},a^{-j}
\right\}.
\tag{13}
\]

Use D(1)=1 as the limiting near-linear boundary.

The later subpolynomial-workspace exclusion reaches every fixed time exponent

\[
a<2\cos(\pi/7)=1.8019377358\ldots.
\tag{14}
\]

Williams's corrected manuscript [2], Table I, includes the simultaneous pair (a_0,b_0)=(1.24,0.666). Its Theorem 4.11 supplies the conservative product exclusion a+b<phi for polynomially bounded time and workspace. An older claimed general product exponent near 1.801 is withdrawn in footnote 9. The valid subpolynomial-space time endpoint (14) is a different statement and remains available.

The alternation-trading rule system has a proved limitation at the endpoint in (14) in the subpolynomial-space setting [3]. Merely iterating those rules does not exclude every polynomial exponent.

### 7.2 Auxiliary cumulative memory

For an execution let s_t be its live usable auxiliary storage, including addresses, registers, and memory-management metadata. Define

\[
C_{\rm aux}=\sum_{t=0}^{T}\max\{1,s_t\}.
\tag{15}
\]

The project transfer assumes:

1. Read-only input is excluded from auxiliary space and CM.
2. Initial auxiliary state is polylogarithmic, with no free preprocessed answer table.
3. Each charged step creates at most g(N)=polylog(N) usable bits.
4. All preprocessing is inside the charged interval.
5. The machine can be simulated in the published random-access model with only polylogarithmic time and peak-workspace overhead.

Under these premises,

\[
T\le C_{\rm aux},\qquad
S_{\max}=O\bigl(s_0+\sqrt{g(N)C_{\rm aux}}\bigr).
\tag{16}
\]

The peak estimate charges the area required to build a peak under bounded growth. It is not the generally invalid lower bound C>=T*S_max, nor the invalid inference S_max<=C/T.

A forbidden time-space rectangle (a_0,b_0) therefore excludes a standalone auxiliary-CM upper exponent

\[
\gamma<\min\{a_0,2b_0\}.
\tag{17}
\]

The pair (1.24,0.666) gives gamma<1.24. For example, C<=N^{1.23+o(1)} would imply time at most N^{1.23+o(1)} and workspace at most N^{0.615+o(1)}, strictly within that rectangle. This project consequence improves the earlier selected-FLMV-branch threshold 1.165373...; no claim that 1.24 is the sharp frontier is made.

Using (13), a time cap N^{a+o(1)} and CM cap N^{gamma+o(1)} are also excluded when, putting u=min(a,gamma),

\[
u<\varphi,\qquad \gamma/2<D(u).
\tag{18}
\]

These are auxiliary-memory statements with the full premises above, transferred to the actual compact Q through its local compiler. They do not automatically apply to every language called T5 or T_q.

### 7.3 Input-inclusive physical cumulative memory

If all N input bits remain resident throughout, physical CM includes NT. If input bits initially count as writable memory, then the execution starts with N usable bits; the small-initial-memory hypothesis of (16) fails for that total footprint.

The independent project input-residence theorem [5] uses an OR family at fixed q=13. With r independently encoded constant bits and N=Theta(r log r), bounded-dependency acquisition forces physical CM Omega(r^2)=Omega(N^2/log^2N), under its no-free-aggregation/no-free-recovery premises. This is an input-access lower bound already present for OR. It is not an exponential search lower bound and does not exclude polynomial time.

## 8. How these facts advance the original lower-bound route

The useful per-level record is

\[
(w,\text{residual support},\text{smallest checkable obstruction},
\text{access model},\text{simultaneous resource frontier}).
\tag{19}
\]

For one or two fixed-domain unknowns, the semantic possibility space is finite and small. Acquisition may still require inspecting a large supplied input. Neither a constant-size final answer nor a small obstruction certificate proves that locating and verifying it is constant-time.

The lower-bound bridge is separate: show that an unrestricted solver, perhaps under a hypothetical polynomial cap, must realize a forbidden simultaneous point, or prove a lower bound on all solvers in a class that retains the necessary hardness. The independent-level characterizations do not have to form a sequential algorithm. A contradiction with a theorem about algorithms does, however, require a justified implication from those characterizations to actual resource bounds or to compulsory operations.

The existing CM-contraction note [7] illustrates the unresolved bridge. Its recurrence includes parent residence:

\[
t'=\max\{1.1,0.825+t/4\},
\]

\[
\gamma'=\max\{1.35,0.825+\gamma/4,1.075+t/4\}.
\]

Its favorable limit would contradict a published region if a correct uniform solver-dependent transformation realized the contract for every hypothetical polynomial solver and remained applicable to every resulting solver. The universal transformation is unproved. The variable-removal characterization may help specify such a contract, but does not itself supply its uniformity, correctness, discovery cost, or retained-memory bounds.

## 9. Inspection and validation record

The four project source files below were read in full. The primary FLMV paper and corrected Williams manuscript were opened and the model, relevant theorem, and table locations inspected. The threshold arithmetic in (8), the elementary implications (3), (7), and (17), and the scope distinctions are symbolic; no numerical experiments or benchmark claims were added. No repository mutation was performed by this contributor.

The evidence is internal research review, not external peer review. The parent coordinator will independently inspect the relevant primary and project sources before citing the result.

### Exact local source pins

| Source | Bytes | SHA256 |
|---|---:|---|
| `/workspace/scratch/d4a6300046d1/T_Odd_FLMV_Transfer_2026-11-22.md` | 12953 | `f406b99dae861efa6b11a4f6b2e1fd4e08b5c583f0cc1bf1e41177d3ad64a1f2` |
| `/workspace/scratch/d4a6300046d1/T_q_FLMV_and_CM_Forbidden_Regions_2026-11-22.md` | 16576 | `d1fdd89651887dd465e28ba39e7d306cf665104a9fae16561eee59ff19587a67` |
| `/workspace/scratch/69bdcc57110a/entropy_work/Additional_T5_Tq_Forbidden_Regions_2026-11-22.md` | 10555 | `a713d9cdd827f41e3be99fbbaac160a2b1af8a31acfe18835a524cb15c3f9b43` |
| `/workspace/scratch/d4a6300046d1/PNP_CM_Contraction_Proof_Attempt_2026-11-22.md` | 16862 | `a6218cba2785fc82d6c79e5731b5d926e436babd4f19868b0ef0d77596017d58` |

## References

1. Lance Fortnow, Richard Lipton, Dieter van Melkebeek, and Anastasios Viglas. *Time-Space Lower Bounds for Satisfiability*. Journal of the ACM 52(6), 835-865, 2005. Author manuscript: https://lance.fortnow.com/papers/files/tst.pdf . Relevant locations: Section 2.1 for the model, Section 3 for local completeness, Theorem 5.7 equation (20), and Corollary 5.8.
2. Ryan Williams. *Alternation-Trading Proofs, Linear Programming, and Lower Bounds*. Corrected author manuscript: https://people.csail.mit.edu/rrw/automated-lbs.pdf . Relevant locations: small-space endpoint discussed on manuscript page A:2; correction footnote 9 on A:17; Table I and Theorem 4.11 on A:18. This note uses the corrected product bound, not the withdrawn stronger claim.
3. Samuel R. Buss and Ryan Williams. *Limits on Alternation-Trading Proofs for Time-Space Lower Bounds*. Computational Complexity 24, 533-600, 2015; CCC 2012 predecessor. https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/ . The endpoint and limitation are also stated in the corrected Williams manuscript inspected for this continuation.
4. Project. *A resource-preserving FLMV lower bound for the compact odd-tournament problem*, 22 November 2026. Exact local source pin above. https://chatgpt.com/library?file_id=libfile_819cb832841c8191b34eeeb439538d96&account_id=personal . Local file contents were used directly; no Library retrieval was performed.
5. Project. *Forbidden regions for compact T_q: time, workspace, and cumulative memory*, 22 November 2026. Exact local source pin above. https://chatgpt.com/library?file_id=libfile_12e7c9e98f948191a775423cc98dcfc8&account_id=personal .
6. Project. *Additional forbidden regions for T5 and compact T_q*, 22 November 2026. Exact local source pin above. The file's primary-source transfers are scoped to its stated compact language and declared auxiliary-memory model.
7. Project. *Using the T_q cumulative-memory region toward P versus NP*, 22 November 2026. Exact local source pin above. https://chatgpt.com/library?file_id=libfile_59805510f01c819198d654d42c495e23&account_id=personal .
