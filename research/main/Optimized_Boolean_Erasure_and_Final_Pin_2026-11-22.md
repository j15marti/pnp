# Optimized value removal for UNSAT 3-SAT

Date: 22 November 2026, America/Los_Angeles. Target: **OPTIMIZED-BOOLEAN-ERASURE1**. Continuation of SHARED-OBSTRUCTION-COST1.

## What this continuation establishes

The optimized removal order can preserve a two-clause contradiction while almost every variable value is unknown. For every UNSAT strict 3-CNF with a reference assignment violating exactly one clause, keeping at most four carefully chosen values supplied preserves a two-row obstruction. Some sources need only two supplied values. This is an exact characterization of source support, with separate accounting for acquiring and establishing it.

A new explicit compiler shows that all pre-final levels can attain the smallest possible source obstruction while the last value removal restores arbitrary 3-SAT. On a verified 15-variable, 20-clause example, the fresh minimum-core sequence is

\[
\boxed{1,\ \underbrace{2,\ldots,2}_{13\text{ independent levels}},\ 4,\ 20.}
\]

All 20 clauses are necessary at the final level. For computation, the same four-row argument handles every pre-final level in near-linear time and logarithmic auxiliary space, including full parsing. The final family preserves both SAT labels and therefore inherits the applicable SAT time-space and cumulative-memory exclusions.

The general growing-level analysis also improves the earlier feasible resource bounds. A paid residual-type table, followed by elementary branching, yields

\[
T=\widetilde O\bigl(N+\operatorname{poly}(r)\lambda^r\bigr),
\qquad S_{\rm aux}=O(r^3+r\log N+\log N),
\]

where \(\lambda^3=\lambda^2+\lambda+1\) and \(\lambda\approx1.839286755\). These are upper bounds for a legitimate route, not a claim that it is the fastest possible algorithm. No general superpolynomial lower bound is established.

## 1. Exact problem and optimization contract

Let F be an UNSAT strict 3-CNF on n variables: every source clause has exactly three distinct variables and is non-tautological. Residual clauses can have width zero through three. Let a full assignment alpha violate exactly one source clause C*. Choose the first erased variable x from C*. For each nested release set R containing x, supply only

\[
\rho_R=\alpha|_{V\setminus R},\qquad r=|R|.
\]

Every \((F,\rho_R)\) is a new static input. No earlier computation, full alpha, core locator or verdict is available unless it is explicitly supplied and counted in that input. The source formula remains available. Algorithms must be correct on both satisfiable and unsatisfiable residuals.

The designation "UNSAT variable" refers here to a variable in the uniquely violated reference clause. UNSAT is a property of the whole formula, rather than an intrinsic label attached to one variable. Some UNSAT formulas do not have a reference assignment violating only one clause, for example a conjunction of two independent UNSAT components. The stated starting condition is a hypothesis. Every minimally UNSAT formula has such assignments; the compiler below supplies one uniformly for both source labels.

Let

\[
\mu(R)=\min\{|K|:K\subseteq F,\ K|_{\rho_R}\text{ is UNSAT}\}.
\tag{1}
\]

The rows in K are original source rows. Their cardinality counts source rows. Acquiring those rows and the associated pin fields is charged separately when assessing machine resources. Minimum cardinality, inclusion-minimality and cheapest computation are separate notions. [1]

The analyst may optimize alpha and the release order when studying the source. Turning that choice into an algorithm requires charging its discovery. The machine is fixed before adversarial inputs are selected. Minimizing separately over a new machine for every input would permit hardcoding and would not be a uniform lower-bound problem.

N always denotes complete encoded input length. For an explicit concrete convention, use \(1^n0\), then the Elias gamma code of \(m+1\), then three signed identifiers per clause with identifier width \(w=\lceil\log_2(n+1)\rceil\), and a two-bit value-or-unknown code per variable. Thus

\[
N=n+2+2\lfloor\log_2(m+1)\rfloor+3m(1+w)+2n.
\tag{2}
\]

Unused pin codes are invalid. A parser checks the declared format when its contract requires complete authentication. The read-only input, writable auxiliary storage and input-inclusive physical storage conventions are kept distinct.

## 2. One value removed: exactly two source clauses

Normalize alpha(x)=0 and the x-literal of C* to x. With only x unknown, C* becomes the unit x. Every other source row was true under alpha, so its residual cannot be empty. All residual rows are true, x, or not-x.

Since F is UNSAT, the assignment obtained by flipping only x cannot satisfy F. It now satisfies C*, so another source clause D becomes false. D's unique true literal under alpha was its not-x literal. After erasing x, D becomes not-x. Therefore

\[
\boxed{\mu(\{x\})=2,\qquad\text{obstruction }\{x,\neg x\}.}
\tag{3}
\]

No singleton obstruction exists because every residual row is individually satisfiable. This proves both sufficiency and minimality.

Write \(\mathcal D_x(\alpha)\) for all clauses whose unique alpha-true literal is the x-literal opposite C*'s. The minimum cores at this level are exactly \(\{C^*,D\}\), with \(D\in\mathcal D_x(\alpha)\). All possible partners remain eligible.

### Necessary information and acquisition

After clause simplification is established, one needs the presence of both unit polarities. If C* and its type are already known, the remaining semantic question is one bit: does an opposite unit occur? This is not necessarily a one-step computation from the raw input.

For m unordered row slots, consider residual types X=x, N=not-x and T=true, with exactly one X. Alpha(x)=0 then violates exactly one row. The residual is UNSAT iff an N occurs. A deterministic adversary can force every slot to be queried: answer T on the first m-2 new probes, X on the next, and N on the last. Until the last probe, replacing the unseen N by T gives a permitted SAT comparison with the same observations. The exact worst-case record-query count is m. If X's location and type are supplied, the remaining worst case is m-1. Verified locators for both rows reduce acquisition to those rows and their pins.

The acquisition companion gives strict-3-CNF realizations using constant-size forced-anchor gadgets. Its positive inputs are globally UNSAT; its SAT comparison inputs retain the same unique-violation reference. The lower bound persists even when this fixed reference assignment is supplied. It does not establish the same exact bound after optimizing over every possible supplied reference.

With indexed supplied values, a complete scan gives the attainable random-access bit bounds

\[
T=\widetilde O(N),\qquad S_{\rm aux}=O(\log N),\qquad
C_{\rm aux}=\widetilde O(N).
\tag{4}
\]

Families with constant-size row records give worst-case \(T=\Omega(N)\) and \(C_{\rm aux}=\Omega(N)\). Thus the time and auxiliary-CM bounds match up to logarithmic factors in this raw-access setting. The logarithmic workspace figure is an upper bound with addresses included; no representation-independent growing workspace lower bound is inferred from two necessary source clauses.

## 3. Two values removed: exact classification

Erase y as well as x. The restriction of alpha to the unknowns still satisfies every row except C*. Consequently every UNSAT core contains C*. Normalize the reference x=y=0.

| Position of y | Residual C* | Exact possible minimum-core sizes |
|---|---|---:|
| y is outside C* | x | 2 or 3 |
| y is inside C* | x OR y | 3 or 4 |

### Case A: y is outside C*

C* still forces x=1. The two remaining candidates are (1,0) and (1,1). If an opposite unit not-x occurs, two rows suffice. Otherwise two separate rows are needed to exclude those two candidates, giving a three-row core.

Equivalently, \(\mu=2\) exactly when at least one partner \(D\in\mathcal D_x(\alpha)\) omits y. Destroying a particular known pair does not prove that every pair has been destroyed.

Representative cores are

\[
\{x,\neg x\},\qquad
\{x,\neg x\lor y,\neg y\}.
\]

### Case B: y is inside C*

C* becomes x OR y, excluding only 00. A negative unit not-x or not-y, if present, fixes one variable and reduces the remaining contradiction to a third row. Hence \(\mu=3\).

If neither negative unit is present, the three other allowed assignments must be excluded by their individual binary clauses. The core is the four-clause square:

\[
\{x\lor y,\ x\lor\neg y,\ \neg x\lor y,\ \neg x\lor\neg y\},
\]

and \(\mu=4\). Positive units cannot occur among the other rows because they would also be false at alpha. A three-row example is \(\{x\lor y,\neg x,\neg y\}\).

All four cases have strict-3-CNF source realizations with the required globally UNSAT and unique-reference-violation properties. Full constructions are in the source-support companion.

### Resources at this level

The two unknown identifiers fit in logarithmic bookkeeping. A four-bit completion mask, or a nine-bit clause-type presence table, is sufficient after paid simplification. Scanning source rows gives the same feasible resource exponents as (4). Worst-case acquisition still requires linearly many raw rows; a supplied, verified short obstruction can be cheaper to acquire.

The local logical contradiction uses only constant-size information. All costs of finding, reading and simplifying the relevant rows remain in the execution. No fixed inference count is asserted for every sound implementation.

## 4. The exact optimized plateau

For a critical partner D, define its retained boundary

\[
B_D=\bigl(\operatorname{vars}(C^*)\cup\operatorname{vars}(D)\bigr)\setminus\{x\}.
\]

Strict width three gives \(2\le|B_D|\le4\). For any release set R containing x,

\[
\boxed{\mu(R)=2\iff
\exists D\in\mathcal D_x(\alpha):R\cap B_D=\varnothing.}
\tag{5}
\]

**Proof.** Retaining B_D leaves C* and D as opposite units, proving sufficiency. Conversely, two nonempty Boolean clauses can be jointly UNSAT only when they are opposite units: each must forbid exactly half the cube, with complementary halves. Every core includes C*, and C* contains x among the unknowns. Thus its only unknown must be x, the other row must be an x-critical partner, and all their remaining variables must still be pinned. This proves necessity.

Let

\[
h(\alpha,x)=\min_{D\in\mathcal D_x(\alpha)}|B_D|.
\]

Then

\[
\boxed{\max\{|R|:x\in R,\ \mu(R)=2\}=n-h(\alpha,x),
\quad 2\le h\le4.}
\tag{6}
\]

Retain an optimal boundary and release all other variables first. The entire initial interval satisfies \(\mu_r=2\). Switching among different partners cannot extend the endpoint because the endpoint itself must have a surviving partner.

Therefore every admitted source has an order preserving a two-clause obstruction through at least n-4 unknowns. Sources with h=2 preserve it through n-2 unknowns, the best possible strict-3-CNF endpoint for a two-row core.

The four-pin guarantee is sharp even if alpha and x are optimized. Take a minimally UNSAT linear strict 3-CNF, where every two distinct clauses share at most one variable. Such formulas exist. [2] Every critical pair shares exactly x and has four distinct other variables, so h=4 for every admissible starting choice. This is structural sharpness, not a computational hardness theorem.

Given alpha and C*, one can find an optimal partner for a fixed x by scanning the source under alpha with x flipped. A constant number of scans compares the three choices in C*. If a flip satisfies every row, it is a SAT witness. Finding a contradictory pinned slice is not a decision procedure for original SAT: a satisfiable source can also have such a slice.

## 5. General fresh levels and distinguishability

Let \(d=|R\cap\operatorname{vars}(C^*)|\), so \(1\le d\le3\). Every core contains C*. Two elementary bounds are

\[
\boxed{d+1\le\mu(R)\le
\min\left\{m,L_3(r),1+2^r-2^{r-d}\right\},}
\tag{7}
\]

where

\[
L_3(r)=1+2r+4\binom r2+8\binom r3.
\tag{8}
\]

For the lower bound, flip one of C*'s d unknown literals from alpha at a time. Each flip repairs C*. Another row must block it. A row that was true at alpha cannot become false under two distinct single-variable flips, so d distinct additional rows are needed.

For the upper bound, every other row in an inclusion-minimal core has a private assignment satisfying all remaining rows, including C*. Those private assignments are distinct. C* admits exactly \(2^r-2^{r-d}\) assignments. The clause-type bound follows because duplicate types and true rows cannot be necessary in a minimal core.

For r at most three, every integer in the following ranges is realizable, with sufficient supplied padding variables:

| Unknowns r | Unknown literals d in C* | Possible mu |
|---:|---:|---|
| 1 | 1 | 2 |
| 2 | 1 | 2,3 |
| 2 | 2 | 3,4 |
| 3 | 1 | 2 through 5 |
| 3 | 2 | 3 through 7 |
| 3 | 3 | 4 through 8 |

The earlier expression \(Q_r=2^r-2^{r-t_r}\) therefore has an exact role with \(t_r=d\):

\[
\mu(R)-1\le Q_r.
\tag{9}
\]

It is an upper bound on additional rows in a minimal obstruction. It is not a lower bound requiring Q_r tests or operations.

### Three meanings of minimum information

On the complete residual-type presence cube, the minimum positive certificate size is exactly mu, as proved in the preceding continuation. This is the source-information meaning of a certificate. [3] It does not charge the effort to establish that those observed constraints are incompatible.

For a different service, suppose C* and the normalized reference are fixed side information and a source-free summary must answer every later context. This service ranges over both SAT and UNSAT residual sources satisfying that reference promise; restricting it to globally UNSAT sources would leave only empty supports. When r is at most three, every subset of C*'s allowed region is realizable. There are \(2^q\) supports, with \(q=2^r-2^{r-d}\), requiring exactly q fixed summary bits:

| r | d | Conditional contextual bits q |
|---:|---:|---:|
| 1 | 1 | 1 |
| 2 | 1 | 2 |
| 2 | 2 | 3 |
| 3 | 1 | 4 |
| 3 | 2 | 6 |
| 3 | 3 | 7 |

Every allowed point can be individually forbidden by a width-at-most-three clause, preserving the reference promise. Distinct supports can be separated by a context that forbids every other allowed point using its point-forbidding clause. Each such clause is true at the reference, so this distinguishing context preserves the unique-reference-violation promise. This proves the count and distinguishability. For r greater than three, point-forbidding clauses would exceed width three; this full-support count must not be extrapolated.

The current decision after computation is one bit: empty or nonempty support. The q-bit lower bound belongs to the reusable contextual service, not to every UNSAT algorithm's workspace. Shannon entropy additionally requires a distribution. Counting supports alone does not establish a compulsory transcript entropy or a runtime lower bound.

At every level, the exact source recurrence from the preceding report remains valid:

\[
\mathcal M_{\rho}=\operatorname{Min}_{\subseteq}
\left\{\bigcup_v K_v:K_v\in\mathcal M_{\rho\cup\{x=v\}}\right\}.
\tag{10}
\]

It preserves all inclusion-minimal choices and shared rows. No execution of those slices or addition of their independently minimized costs is required.

## 6. An optimized path whose last pin carries arbitrary 3-SAT

Take any strict 3-CNF H with n_H variables and m_H clauses. Add fresh variables p,x,a,b and one fresh s_C for each source clause. Start with four guards:

\[
\begin{aligned}
G_1&=p\lor x\lor a,&G_2&=p\lor x\lor\neg a,\\
G_3&=p\lor\neg x\lor b,&G_4&=p\lor\neg x\lor\neg b.
\end{aligned}
\tag{11}
\]

Replace \(C=\ell_1\lor\ell_2\lor\ell_3\) by

\[
(\neg p\lor\ell_1\lor s_C)
\land(\neg s_C\lor\ell_2\lor\ell_3).
\tag{12}
\]

Call this strict 3-CNF F(H). It has

\[
n_F=n_H+m_H+4,\qquad m_F=2m_H+4.
\]

### Decision and core identities

The first two guards imply p OR x; the last two imply p OR not-x. Together they force p=1. Under p=1, each private-auxiliary pair (12) is satisfiable exactly when its original clause is. Hence

\[
\boxed{F(H)\text{ is SAT}\iff H\text{ is SAT}.}
\tag{13}
\]

For UNSAT H,

\[
\boxed{\mu(F(H))=4+2\mu(H).}
\tag{14}
\]

To prove (14), every UNSAT subset must contain all four guards. If one is omitted, set p=0, choose x,a,b to satisfy the remaining guards, and set every s_C=0. All remaining clause-pair rows are then satisfied, regardless of H.

With all four guards present, p=1. A complete pair enforces its original clause. A single half of a pair imposes no restriction on H's variables because its private s_C can always satisfy it. Thus an UNSAT subset needs complete pairs for an UNSAT subset of H, and any such subset suffices. Inclusion-minimal cores correspond exactly.

### Optimized removals

The all-zero reference violates only G1, independently of H's SAT label. Erase a first and retain p=x=0. G1,G2 become opposite units a,not-a. Erase b, every H-variable and every s_C in any order. The core remains two rows through r=n_F-2.

Next erase x, retaining only p=0. The four guards form a four-row contradiction. Finally erase p. The answer is the arbitrary H decision from (13).

\[
\boxed{
\mu_r=2\ (1\le r\le n_F-2),\quad
\mu_{n_F-1}=4,\quad
\mu_{n_F}=4+2\mu(H).
}
\tag{15}
\]

The pre-final source sizes are optimal. Along the near-assignment path no empty clause exists, so mu is at least two. With only one supplied variable, every surviving strict-3-CNF clause has at least two unknown literals and excludes at most one quarter of the completion cube, so at least four rows are necessary. With no supplied values, the corresponding floor is eight. These are mathematical coverage arguments, not instructions to count completions.

For computation, the same four guard rows imply p=1 at every stage. A correct recognizer can combine that implication with the still-supplied p=0, regardless of which other values are known. This uses a slightly larger core at some levels, but avoids requiring minimum-core discovery. Full parsing and recognition fit (4). Each fresh execution pays again; no earlier state is reused.

### A verified 15-variable, 20-clause instance

Let H be all eight signed full clauses on three variables. Then \(\mu(H)=8\), and F(H) has 15 variables and 20 clauses. In encoding (2), its source occupies 325 bits and its pin array 30 bits, totaling 355 bits at every level.

| Unknown values | Remaining crucial pins | Exact minimum core |
|---|---|---:|
| 0 | All reference values | 1 |
| 1 through 13 | p=x=0 | 2 |
| 14 | p=0 | 4 |
| 15 | None | 20 |

The script checks all 32,768 assignments of the final formula and gives a satisfying witness for every one of its 20 single-row deletions. This proves its exact minimum core is 20. It also tests all 256 subsets of H's eight possible clauses, preserving both labels in 255 SAT cases and 1 UNSAT case, and checks the unique all-zero violation in every compiled source. Total direct-search assignment evaluations: 496,130. The symbolic compiler proof covers arbitrary H; the finite tests audit its implementation.

## 7. Resource frontier for general r

Write \(s_t\) for live auxiliary bits, including addresses, metadata, retained tables and caches. On one run,

\[
T=\text{charged steps},\qquad S=\max_t s_t,\qquad
C_{\rm aux}=\sum_{t=0}^{T}\max\{1,s_t\}.
\tag{16}
\]

All parsing, preprocessing, access, representation construction, switching, failed work, recomputation and output are included. Shared physical events count once. With all input bits retained,

\[
C_{\rm phys}=\Theta(N(T+1)+C_{\rm aux}).
\tag{17}
\]

### Paid clause-type compilation

Substitute the supplied values and store which of the L_3(r) residual types occur. Build a map from original unknown-variable identifiers to their residual slots, costing O(r log N) bits unless a corresponding counted read-only index is supplied. Type-index arithmetic and all lookups are charged. Duplicate source rows need not be revisited for every possible assignment.

After this pass, direct assignment evaluation gives

\[
T_{\rm enum}=\widetilde O(N+L_3(r)2^r),\qquad
S=O(L_3(r)+r\log N+\log N).
\tag{18}
\]

This improves the repeated-full-scan bound \(\widetilde O(N2^r)\). The table's construction and initialization are included.

### An elementary sound alternative already improves the exponent

Choose any unresolved clause. For three remaining literals, partition its satisfying extensions according to the first true literal:

\[
\ell_1=1;\qquad
\ell_1=0,\ell_2=1;\qquad
\ell_1=0,\ell_2=0,\ell_3=1.
\]

The branches fix one, two and three variables. Unit and binary clauses have fewer branches. With h variables still unknown, the search-node count satisfies

\[
V(h)\le 1+V(h-1)+V(h-2)+V(h-3),
\]

so \(V(r)=O(\lambda^r)\). Each node scans an immutable catalog of size polynomial in the original r, yielding total search work \(O(\operatorname{poly}(r)\lambda^r)\), where

\[
\lambda^3=\lambda^2+\lambda+1,\qquad
\lambda\approx1.839286755214161.
\]

A depth-first realization retains one immutable type table, an assignment and an undo stack, rather than copies of the table at every depth. Consequently

\[
\boxed{
T=\widetilde O(N+\operatorname{poly}(r)\lambda^r),\quad
S=O(L_3(r)+r\log N+\log N),\quad
C_{\rm aux}\le(T+1)\max\{1,S\}.
}
\tag{19}
\]

No fastest-known or optimality claim is made for this elementary bound. Better algebraic, structural or algorithmic routes remain eligible. It supplies a concrete feasible point that any proposed lower bound must respect.

Let \(\beta=\log_2\lambda\approx0.879146421606638\). For \(r=c\log_2N+o(\log N)\), (19) gives

\[
\boxed{T\le N^{\max\{1,\beta c\}+o(1)},\quad
S=N^{o(1)},\quad
C_{\rm aux}\le N^{\max\{1,\beta c\}+o(1)}.}
\tag{20}
\]

At any fixed number of removed values, these reduce to (4). Every family with r=O(log N) has a polynomial feasible point in this explicit-access model. Any superpolynomial hard family must therefore escape that parameter range. The long two-unit plateau shows that r much larger than log N still does not guarantee hardness.

## 8. Applying the forbidden regions to an actual speedup

The applicable exclusions concern a class preserving SAT hardness and one execution's simultaneous resources. The pinned prefixes of F(H) are UNSAT for both SAT and UNSAT H, so they do not preserve the original answer. Their cheap resource points can lie below SAT's boundaries without contradiction.

The final, completely unpinned F(H) does preserve both labels. Its complete length is \(\widetilde O(N_H)\); output headers and lengths can be prepared in near-linear time and logarithmic workspace. The parsed header counts are retained in logarithmic auxiliary storage. A requested output bit is a guard constant, generated auxiliary ID or a bit from a constant number of source records. Local access costs polylogarithmic time and logarithmic scratch. On-demand simulation avoids an uncharged input-sized writable copy. Thus strict-gap exponent exclusions transfer to this final family.

Write \(T=N^{a+o(1)}\), \(S=N^{b+o(1)}\). The following are the existing exclusions used here in their eligible deterministic random-access setting, with strict gaps absorbing the local simulation overhead. [4,5]

| Resource claim on a SAT-equivalent class | Forbidden condition |
|---|---|
| Subpolynomial auxiliary space | \(a<\kappa=2\cos(\pi/7)\approx1.8019377358\) |
| Simultaneous time-space product | \(a+b<\varphi=(1+\sqrt5)/2\) |
| One published simultaneous point | \(a<1.24,\ b<0.666\) |
| Another published simultaneous point | \(a<1.32,\ b<0.5\) |
| Auxiliary CM under small initial state and bounded growth | \(\gamma<1.24\) in \(C_{\rm aux}=N^{\gamma+o(1)}\) |

The CM implication follows from \(T\le C_{\rm aux}\) and

\[
S=O\bigl(s_0+\sqrt{gC_{\rm aux}}\bigr),
\]

where initial auxiliary size s_0 and per-step growth g are polylogarithmic. An input-inclusive physical measure starts with N resident bits and must not be substituted into this small-initial-auxiliary statement. If physical input residence is counted and subpolynomial auxiliary space is separately guaranteed, (17) converts the time endpoint into exclusion of a physical-CM exponent below \(1+\kappa\). Without that workspace premise, that conversion is not a standalone physical-CM theorem.

The withdrawn general time-space product exponent near 1.801 is not used. Williams' corrected Theorem 4.11, Table I and footnote 9 distinguish the product statement from the separate small-space endpoint. [4]

### The exclusions also constrain a uniform UNSAT-only guarantee

Suppose a fixed correct A obeys explicit time and space budgets on every UNSAT member of the final family F(H), with no such speed guarantee on its SAT members. Simulate A with those budgets. Return A's verdict if it halts within them; return SAT if a budget would be exceeded. An UNSAT input never reaches that cutoff, while a SAT input receives the correct answer in either case. This is a correct both-label solver.

For polynomially bounded, efficiently computable budgets, the monitored simulation costs polylogarithmic overhead, plus charged header/setup work and monitor storage. An auxiliary-CM budget likewise supplies a time bound because each step has positive charge; the monitor's own cumulative cost is included. Allocation must be explicitly accountable, and a contemplated overshoot must be prevented or bounded by the machine's per-step growth. Space alone does not give a time bound.

Therefore the strict-gap exclusions above apply even when a proposed speed guarantee covers only all UNSAT members of the final hard family. They do not follow from fast behavior on one chosen UNSAT sequence, and they do not make the answer-destroying pinned prefixes SAT-hard. This cutoff argument strengthens the connection to the user's UNSAT-specific target without assuming fast original runs on SAT inputs.

### A sharper conditional compression obstruction

Suppose a both-label SAT reduction, with the local-access and setup bounds just stated, produced fresh residuals with

\[
r\le c\log_2N+o(\log N).
\]

Combining it with (20) would violate the small-space endpoint whenever

\[
\boxed{c<\frac{\kappa}{\beta}
=\frac{2\cos(\pi/7)}{\log_2\lambda}
\approx2.0496446229.}
\tag{21}
\]

Such a complete reduction package is therefore impossible in that region. This strengthens the former repeated-scan threshold 0.801937 and the direct compiled-enumeration threshold 1.801937. It does not manufacture an answer-preserving reduction from the ability to choose convenient pins.

For a hypothetical speedup factor \(f=N^{\delta+o(1)}\) on the residual computation after compilation, with the same subpolynomial workspace and charged setup floor, the resulting upper time exponent is

\[
a_{\rm new}=\max\{1,\beta c-\delta\}.
\tag{22}
\]

A contradiction requires \(a_{\rm new}<\kappa\) on an actual SAT-equivalent class. A speedup that uses more memory must instead be checked against the full joint region. Separate fastest-time and smallest-space executions cannot be combined. If output length grows as \(N=n^{q+o(1)}\), exponents must be multiplied by q and compared after any larger setup cost is included.

Explicit dynamic primitive-instruction counts are another way to record charged time in a compatible instruction model. An encoded macro-operation must pay for its realization. A fixed algorithm's static code length need not grow with input length, so source-core growth does not provide a static program-size lower bound.

## 9. Status and the next proof obligation

The following are proved symbolically: exact one- and two-unknown characterizations; the h-pin plateau and its exact endpoint; the d-dependent source-information bounds; the guarded compiler's both-label equivalence and minimum-core identity; and the charged feasible resource bounds. The finite program independently audits the concrete compiler and 16 fresh levels. Conditional contextual-summary and forbidden-region claims retain their stated interfaces and transfer premises.

The complete general minimum of time, space and CM after every release remains open. The new results show why a smooth per-variable cost recurrence cannot be assumed: all preliminary levels can have minimal source evidence and a common cheap refutation, while one final release restores the full decision problem. They also provide a concrete hard-preserving final family on which a proposed speedup can be tested correctly.

Four controls govern continuation: preserve all alternative partners when tracking a two-row core; include larger overlapping slice cores when applying the shared-union identity; include source acquisition and header discovery; and verify both SAT labels before invoking a forbidden region. No argument requires counting assignments, explicit truth-table materialization, a prescribed proof system or extra work after an already-computed verdict.

DISJ/query sanity is maintained by the finite input-probe ceiling. No relativization, algebrization or Natural-Proofs barrier bypass is claimed. Simultaneous DTISP exclusions are applied only after a complete local reduction. Deterministic configuration counting supplies no lower bound in this report. P versus NP remains OPEN; a valid polynomial all-input shortcut remains an admissible outcome.

## 10. Evidence and references

Detailed companions: `Optimized_Start_and_Source_Support.md`, `Uniform_Optimization_and_Acquisition_Contracts.md`, and `Boolean_Resource_Frontier_and_Speedup_Transfer.md`. Executable audit: `guarded_release_audit.py`; full results: `guarded_release_audit_results.json`. Publication paths and hashes are recorded in the accompanying provenance manifest.

Three collaborators developed the source, acquisition and resource components. The Boolean collaborator independently reviewed the compiler script and complete saved evidence without rerunning it. The compiler proof was independently checked by all three collaborators. These are same-project reviews, not external peer review or formal-kernel verification. No native tape/parser implementation or full-checkout preflight was run. Owner manuscripts and scheduler settings were preserved.

[1] Inês Lynce and João Marques-Silva. *On Computing Minimum Unsatisfiable Cores*. SAT 2004. https://www.satisfiability.org/SAT04/programme/110.pdf

[2] Dominik Scheder. *Unsatisfiable Linear k-CNFs Exist, for every k*. arXiv:0708.2336v1, 17 August 2007. https://arxiv.org/pdf/0708.2336. Also *Unsatisfiable Linear CNF Formulas Are Large and Complex*, STACS 2010. https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2010.2490

[3] Harry Buhrman and Ronald de Wolf. *Complexity Measures and Decision Tree Complexity: A Survey*. Section 4.1. https://homepages.cwi.nl/~rdewolf/publ/other/tcs.pdf

[4] Ryan Williams. *Alternation-Trading Proofs, Linear Programming, and Lower Bounds*. Corrected author copy, Theorem 4.11, Table I and footnote 9. https://people.csail.mit.edu/rrw/automated-lbs.pdf

[5] Lance Fortnow, Richard Lipton, Dieter van Melkebeek and Anastasios Viglas. *Time-Space Lower Bounds for Satisfiability*. https://lance.fortnow.com/papers/files/tst.pdf

Project antecedent: *Shortest Obstructions and Fully Charged Incompatibility*, main commit f2df35984424e038de224c401daec634f83c47b1, and the independent one/two-unknown report at 0751533f220dfcd9fdf0694ce45efc798cd17f3a. The present optimized path and final-pin compiler extend that semantic and accounting framework.

An additional bounded duplicate check inspected `research/agents/lspv-3/2026-11-09_0430_LSPV3_PINNED_TERNARY_LINEAR_RES532.md`, blob 03be13610552668d2f92183dca3e8c6ef4316904. That antecedent already gives a charged linear refutation for a pinned strict-3-CNF family despite a large flat boundary representation. It supports the same separation between representation size and actual refutation cost. This continuation makes no novelty claim for guard gadgets or pinned-instance tractability; its specific contribution is the optimized erasure characterization, exact minimum-core compiler identity, and their charged-resource consequences.
