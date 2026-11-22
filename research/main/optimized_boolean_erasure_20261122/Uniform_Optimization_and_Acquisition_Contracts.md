# Optimized fresh Boolean erasures: uniformity, acquisition, and charged resources

Research date: 22 November 2026. This note supplies elementary proofs and explicit input contracts for the optimized-erasure continuation. It does not prove a superpolynomial SAT lower bound.

## 1. The precise optimization problem

Let F be a strict 3-CNF on n named variables: every source clause contains exactly three literals on distinct variables. Let alpha be a full assignment violating exactly one source clause C*. Let x be a designated variable occurring in C*. For an erased set E containing x, define the fresh input

\[
I(F,\alpha,E)=(F,\rho_E),
\qquad \rho_E=\alpha|_{V\setminus E},
\qquad |E|=r.
\]

The reference alpha is used by the analyst. Its erased values are not automatically supplied to the solver. Whenever a construction gives the solver alpha as additional information, that stronger input contract is stated explicitly.

If F is globally UNSAT, every such fresh residual is UNSAT. A solver nevertheless must be correct on the declared class of both SAT and UNSAT inputs. Giving it an all-UNSAT promise would permit the constant answer and would change the question.

Write mu(F,rho) for the minimum number of original source rows whose residual conjunction is UNSAT. Define the optimized semantic quantity

\[
\mu_r^*(F,\alpha,x)
=\min_{E:\ |E|=r,\ x\in E}\mu(F,\rho_E).
\tag{1}
\]

This is a legitimate pointwise structural invariant. It says nothing by itself about finding the optimizing pins or about executing the corresponding proof.

For computation, first fix a uniform correct solver A and then evaluate the cost vector

\[
\mathbf R_A(F,\alpha,E)
=(T_A(I),S_A(I),C_A(I))
\tag{2}
\]

on each fresh input. Different resource coordinates cannot be minimized using different algorithms or different representations and then treated as one attainable vector. Nor may a new algorithm be hardcoded separately for each input and called the uniform optimum.

An all-method lower bound that survives an analyst's favorable choice of E would need the order

\[
\forall A\ \forall p\ \forall N_0\ \exists(F,\alpha,r):
\quad\forall E\in\mathcal E_r(F,\alpha,x),
\quad |I(F,\alpha,E)|\ge N_0,
\quad T_A(I(F,\alpha,E))>p(|I(F,\alpha,E)|),
\tag{3}
\]

or the corresponding exclusion of a simultaneous resource region. Here the triples (F,alpha,r) range over globally UNSAT sources with the stated unique-violation reference; A remains correct on both labels of the full input domain. The admissible r range and source family must be specified. This is stronger than showing that one badly chosen erasure is slow. It is also distinct from evaluating a supplied favorable erasure at no charge for discovering that erasure.

A single nested erasure order and separately optimized erasures at every level are different characterizations. The plateau construction below supplies one nested order that works simultaneously at all its stated levels, while every solver execution still starts fresh. Costs of these independent executions are not added to obtain a lower bound on any one of them.

### Why the first-erased-variable condition matters

Without the requirement that E intersect C*, the analyst can keep all three variables of C* pinned at their falsifying reference values. Every erasure set outside those variables then leaves an immediate empty residual clause, through r=n-3. If pins are chosen without even fixing alpha, falsifying any one source clause has the same effect, including for globally satisfiable formulas.

Thus unrestricted best-pin optimization can collapse the intermediate UNSAT problem. The designated x condition prevents this particular one-row obstruction: C* retains at least one unknown literal. Every other source clause was true at alpha and therefore still has an extension. Hence

\[
\mu(F,\rho_E)\ge2
\tag{4}
\]

for every UNSAT residual in the designated-x experiment.

## 2. A two-row plateau for every globally UNSAT near-assignment source

Let alpha^x be obtained by flipping only x. The unique false clause C* becomes true. Since F is globally UNSAT, some other clause D is false under alpha^x. Because D was true under alpha and only x changed, D contains the opposite x literal and has all its other literals false under both assignments.

Set

\[
B=(\operatorname{vars}(C^*)\cup\operatorname{vars}(D))\setminus\{x\}.
\tag{5}
\]

There are between two and four distinct names in B. Retain their alpha values and erase x and any other variables outside B. Then C* and D reduce to opposite units on x. Consequently,

\[
\boxed{\mu(F,\rho_E)=2
\quad\text{whenever}\quad
x\in E\subseteq V\setminus B.}
\tag{6}
\]

The upper bound comes from the pair; the lower bound is (4). Thus one erasure order has

\[
\mu_r^*=2
\quad\text{for every }1\le r\le n-|B|,
\tag{7}
\]

and in particular through n-4 whenever that range is nonempty. Minimizing |B| among the clauses falsified by alpha^x improves the guaranteed plateau. The minimum is always at least two and at most four.

This proves a strong structural fact about the favorable path. Releasing many variables need not make the smallest obstruction grow at all. All those extra unknowns can be irrelevant to a persistent two-row contradiction.

### Choosing this plateau need not hide expensive advice

If F and alpha are supplied with indexed value access, find C* by a scan, flip the designated x virtually, and scan for a violated D. The scan stores only x, a constant number of variable identifiers, a row counter, and a current best B. It takes near-linear time up to encoding factors and O(log N) auxiliary bits. Trying the three possible first variables of C* requires only a constant number of scans.

If no D is found for a selected x, alpha^x is a satisfying assignment of the original formula. If D is found, the construction gives a contradictory restricted instance even when the original formula happens to be satisfiable by a different assignment. Therefore producing the plateau is not an answer-preserving reduction from original SAT to a small-unknown UNSAT test.

Finding alpha itself is a separate task when it is not supplied. Some formulas have no assignment violating exactly one row. Nothing here provides such an assignment for arbitrary input formulas. On the guarded family in Section 7, however, alpha is uniformly available as all zeros for both labels, so the final-stage hardness example does not depend on hidden advice.

## 3. Three different acquisition contracts

The following are distinct problems. They should not share an unqualified resource claim.

### A. Raw clauses and indexed supplied values

The input contains the formula and the value-or-unknown array. Row positions and relevant clause contents are not supplied as a trusted certificate. Every necessary access is charged.

When x is a fixed canonical variable name or its identifier is included in the fresh input, a correct uniform solver can scan for opposite residual unit clauses on x using O(log N) auxiliary bookkeeping. If it finds them, it rejects. If it does not, it invokes a general correct fallback. The fallback is irrelevant on the two-row plateau inputs but makes the same machine correct on every input in its declared decision domain.

With indexed read-only input and fixed-width records, this gives the following attainable point on the plateau family:

\[
T=\widetilde O(N),\qquad
S_{\rm aux}=O(\log N),\qquad
C_{\rm aux}=\widetilde O(N).
\tag{8}
\]

This is an upper bound, not a requirement to read every source. A contradiction in known prefix rows can be recognized sooner when their offsets and the needed metadata are available through the counted input contract. Otherwise header discovery and authentication are added. Section 4 gives a family on which locating the relevant evidence really does require linearly many row probes.

The x-access premise matters. If the useful variable is only existentially known to exist and its identifier is not supplied, a one-pass table of unit polarities for all n variables uses O(n) bits. A simple small-space alternative rescans for each variable and may use O(nm) row work. The designated-variable scan cannot be attributed to arbitrary unmarked inputs without paying for its selection.

### B. Supplied row locator, verified against the source

Suppose two row indices and their intended common unknown are supplied. A general correct solver can read those rows and their pin fields, verify that the residuals are opposite units, and reject. Failed verification leads to a general fallback. A locator is a candidate, not a promise that its claim is true.

On read-only random-access input, when row offsets and needed metadata are available through the counted indexed input contract, this takes polylogarithmic bit time and auxiliary cumulative memory, and O(log N) auxiliary workspace. The addresses and supplied-value accesses are charged. Otherwise add header discovery and any required authentication, conservatively within a near-linear scan with logarithmic auxiliary bookkeeping. It is not necessary to inspect every source clause after an actual contradictory subset has been obtained and verified.

In particular, a unary header 1^n0 can precede the clause records. Knowing that a witness occupies the first two clause rows does not by itself give their absolute addresses or the signed-identifier width. Read-only access and indexed pin fields do not silently provide pre-parsed row metadata. A faster header-location procedure, if used, must be proved and charged under its own validity and access premises.

On a single sequential input tape, however, a locator does not teleport the head. Reaching a distant row can require Theta(N) movement. A trusted externally authenticated row copy is yet another input contract; it cannot be substituted for an unverified claim about distant source contents.

### C. Supplied canonical presence mask

The input is already the residual-type vector z. For width at most three,

\[
M_3(r)=\sum_{j=0}^{\min(3,r)}2^j\binom rj.
\tag{9}
\]

The first term is the empty clause. For r=1,2,3 the lengths are 3,9,27 bits. Computation on this representation excludes the work of determining which residual types occur in the raw source.

At r=1, the three flags are e for an empty clause, p for x, and q for not-x. The exact decision is

\[
U_1=e\lor(p\land q).
\tag{10}
\]

Under the stronger known near-assignment promise with alpha(x)=0 and C* containing x, e=0 and p=1. Decision then reduces to the single q bit. Section 4 shows that computing this one bit from unmarked raw rows can require every row probe. There is no contradiction: the representations expose different information.

Construction of the canonical mask from raw input is permissible, but its reads, writes, indexing, storage, and lifetime belong in the same run. It is not free evidence.

## 4. Exact worst-case acquisition with one or two unknowns

Consider m variable row slots over the residual alphabet

\[
X=(x),\qquad N=(\neg x),\qquad T=\text{true},
\]

with m at least two. Promise exactly one X slot. The reference assignment x=0 violates exactly one row. The residual is UNSAT if and only if some slot is N.

### Theorem 1: unmarked acquisition needs exactly m probes

In the deterministic exact clause-query model, there is a permitted UNSAT input on which every correct algorithm needs all m distinct row probes.

**Proof.** Answer T on the first m-2 newly probed slots. Put X in the penultimate newly probed slot. Until the last slot is examined, two completions remain consistent with every observation and the promise: the last slot can be T, giving SAT, or N, giving UNSAT. Therefore the solver must probe the last slot. Choose N there. The resulting input is a fixed legal UNSAT input for that deterministic solver, requiring m probes. Reading all m slots is an upper bound. QED.

The adversary does not choose the input after seeing a random computation. For each fixed deterministic algorithm its answers define one ordinary input. This is the standard quantifier order required by a worst-case deterministic lower bound.

If the X position and type are supplied for free, the problem is OR on the other m-1 slots. Its exact worst-case UNSAT acquisition is m-1 probes. If both an X and an N locator are supplied and must be verified, two source-row probes suffice under unit-cost row access.

For two unknowns, add an independent free variable y. The same family and proof apply. Consequently the difference between one and two unknown values does not eliminate the raw acquisition lower bound. The hard inputs still have a two-row shortest obstruction.

### A strict 3-CNF realization with globally UNSAT positive inputs

Use variables x,a,b,c, and replace the three row types by

\[
X=(x\lor a\lor b),\qquad
N=(\neg x\lor a\lor b),\qquad
T=(\neg c\lor a\lor b).
\tag{11}
\]

Force a=b=c=0 using the ordinary strict-3-CNF gadget

\[
(\neg w\lor u\lor v)\land
(\neg w\lor u\lor\neg v)\land
(\neg w\lor\neg u\lor v)\land
(\neg w\lor\neg u\lor\neg v)
\tag{12}
\]

for each w in {a,b,c}, with auxiliary names u,v distinct from x,a,b,c. The auxiliaries may be shared between the three gadgets. Each gadget entails w=0; if w=1 its four clauses forbid all four assignments to u,v.

The all-zero reference assignment satisfies every gadget and T or N row, and falsifies exactly the unique X row. An N slot makes the unpinned original formula globally UNSAT. With no N slot, x=1 and a=b=c=0 satisfy the source. Thus the SAT comparisons respect the same near-assignment promise as the UNSAT inputs.

For the fresh one-unknown level, pin every variable except x to zero. For two unknowns add y and leave x,y free; a known always-true row can make y occur if the source convention requires occurrence. The lower bound is exactly m for the variable slots and Theta(m) in the total row count, since the forcing gadgets add only constantly many rows.

This lower bound remains valid even if the full reference alpha and the fact that it has exactly one violated row are supplied as extra hints. It is therefore not an artifact of hiding the erased reference bit. It does not require a promise that every source is UNSAT.

In a charged machine implementation, the row lower bound gives T=Omega(m) and C_aux=Omega(m). Encoding overhead can add logarithmic factors. It gives no model-independent superconstant workspace lower bound: a sequential scan can maintain only a few logical flags, while a random-access bit model may also charge logarithmic address registers.

## 5. Minimum distinguishing information and contextual summaries

For the canonical Boolean mask, define

\[
U_r(z)=1\iff \text{the selected residual clauses are jointly UNSAT}.
\]

For any UNSAT z, its positive decision-tree certificate complexity equals its shortest source-core size:

\[
C_1(U_r,z)=\mu(z).
\tag{13}
\]

Observing a core suffices. Conversely, replace a certificate by the mask that retains only its observed one positions. That mask satisfies the whole certificate, including its zero observations, so it is UNSAT. The observed positive positions alone therefore contain a core. This argument makes no inference-system or monotone-circuit restriction.

An exact contextual summary is a different service. It must represent the entire feasible relation S contained in {0,1}^r so that every later legal context can be tested. At r at most three, every subset S is realizable: forbid each excluded tuple with its own width-r clause. Hence there are exactly

\[
2^{2^r}
\]

support states, requiring 2^r fixed bits in an exact source-free summary. In particular:

| Unknown values | Atomic-mask bits | Exact support states | Exact contextual-summary bits |
|---:|---:|---:|---:|
| 1 | 3 | 4 | 2 |
| 2 | 9 | 16 | 4 |
| 3 | 27 | 256 | 8 |

Two different supports are distinguishable by the context of unit clauses selecting a tuple in their symmetric difference. Unit residuals are realizable from strict 3-CNF using suitable pinned anchors.

For r greater than three, full 2^(2^r) realizability must not be assumed for width-three formulas on those same r variables. The number of distinct supports obeys

\[
|\mathcal S_r|\le\min\{2^{2^r},2^{M_3(r)}\}.
\tag{14}
\]

For example, a width-three clause on r>3 variables cannot forbid just one full tuple. Auxiliary existential projection is a different representation and must specify which variables are counted in r.

Neither the support-state count nor the certificate count is a general offline workspace requirement. A final decision is one bit; a machine may reread source information, use algebra, share summaries, or avoid constructing this interface.

### Conditional contextual information when the violated row is known

There is a sharper exact statement under the near-assignment promise. Fix the normalized reference alpha=0 and the known residual clause C*, including its coordinates and signs. Suppose C* contains d of the r unknown variables. Its allowed region A has

\[
q=|A|=2^r-2^{r-d}
\tag{14a}
\]

points, because the other 2^(r-d) completions falsify C*. Every feasible support is contained in A.

For r at most three, every subset S of A is realizable while preserving C* as the unique clause false at alpha: retain C* and add the width-r clause forbidding each point in A minus S. Each such point differs from alpha, so its forbidding clause is true at alpha. Short clauses can be padded to strict width three using false pinned anchors. If desired, anchor-forcing gadgets of the form (12) preserve the reference promise and make the original source's satisfiability match support nonemptiness.

These supports remain pairwise distinguishable even if future contexts must preserve the one-false-row promise. For a point beta in the symmetric difference of two supports, add the full-width clauses forbidding every point of A except beta. All these context clauses are true at alpha; together with the existing C* they select exactly beta. Thus there are exactly 2^q supports conditional on this fixed side information, and an exact source-free all-context summary needs exactly q bits:

| Unknown values r | Unknown literals d in C* | Conditional support states | Conditional summary bits q |
|---:|---:|---:|---:|
| 1 | 1 | 2 | 1 |
| 2 | 1 | 4 | 2 |
| 2 | 2 | 8 | 3 |
| 3 | 1 | 16 | 4 |
| 3 | 2 | 64 | 6 |
| 3 | 3 | 128 | 7 |

The known C* metadata is not included in q. If its identity must also be stored or discovered, that has its own cost. The statement ranges over both SAT and UNSAT near-assignment sources; a promise that every residual is UNSAT would permit only the empty support and destroy the state-count argument. For r>3, point-specific width-r clauses no longer belong to the same width-three representation, so the equality cannot be extrapolated from this proof.

## 6. Whole-run time, space, and cumulative storage

For one fixed implementation on one input, use

\[
T,\qquad S=\max_t s_t,\qquad
C_{\rm aux}=\sum_{t=0}^{T}\max\{1,s_t\}.
\tag{15}
\]

All actual preprocessing, pin selection performed by the machine, row discovery, address arithmetic, representation construction, failed work, shared computation, and output are included. Shared physical bits are counted once. Separate fresh levels have separate runs.

Always,

\[
T\le C_{\rm aux}\le(T+1)\max\{1,S\}.
\tag{16}
\]

If initial workspace is at most s0 and workspace grows by at most g bits per step, then

\[
S=O(s_0+\sqrt{gC_{\rm aux}}).
\tag{17}
\]

To see this, if S is at least 2s0, look backward from a time attaining S through roughly S/(2g) steps. Storage remains at least S/2 throughout those steps, giving C_aux at least S squared divided by 4g, up to harmless rounding. Otherwise S is already bounded by 2s0. A free bulk-allocation primitive violates the bounded-growth premise and cannot silently be used with (17).

With polylogarithmic s0 and g, a bound C_aux=O(N^gamma) gives, on that same realization,

\[
T=O(N^\gamma),\qquad
S=\widetilde O(N^{\gamma/2}).
\tag{18}
\]

This is the valid bridge to a simultaneous time-space exclusion, provided the decision language and reduction meet its model and locality hypotheses. A lower bound for one resource cannot be paired with the best upper bound of a different algorithm.

### General fixed-level upper bounds

A direct completion check gives the familiar attainable bound of roughly 2^r complete source evaluations. It is not compulsory. With indexed supplied values, one can instead scan once to deduplicate the residual clauses into the M3(r)-bit mask and then check the completions against that mask. A straightforward uniform implementation has

\[
T=\widetilde O(N+M_3(r)2^r),\qquad
S=O(M_3(r)+r\log N),
\tag{19}
\]

with every mask construction and access charged. The O(r log N) term stores the unknown names for translating source identifiers. A word/bit access convention and an indexed supplied-value array are required for the stated near-linear scan. Unsorted value lists can require additional indexing or rescans.

At every fixed r, (19) gives near-linear time and polylogarithmic auxiliary space and cumulative memory. At r=c log2 N for fixed c,

\[
T=N^{\max\{1,c\}+o(1)},\qquad
S=N^{o(1)},\qquad
C_{\rm aux}=N^{\max\{1,c\}+o(1)}.
\tag{20}
\]

This improves the coarser repeated-raw-scan exponent 1+c. Under the previously established near-linear local SAT transfer and standard subpolynomial-space lower bound, a hypothetical answer-preserving compression to r at most c log2 N would therefore be excluded for c<2cos(pi/7), with strict slack absorbing overhead. This is the valid enumeration-based threshold, not the strongest upper-bound route in the continuation. The proof is conditional on that local reduction; the existence of easy erasures on known UNSAT sources does not supply it.

The companion resource analysis uses a further elementary improvement. For a residual clause with three literals, divide assignments according to the first true literal. The disjoint branches fix one, two, or three variables, giving a search-tree bound polynomial(r) times lambda^r, where lambda is the positive root of lambda^3=lambda^2+lambda+1, approximately 1.839286. Shorter clauses give smaller recurrences. Charging each node's scan of the deduplicated residual mask uses polynomial(r)+O(r log N) auxiliary workspace and total time N+polynomial(r)lambda^r up to encoding factors. At r=c log2 N this gives exponent max(1,c log2 lambda), and hence the stronger conditional compression threshold c<2cos(pi/7)/log2(lambda), approximately 2.0496446. The same locality, encoding, uniformity, and answer-preservation premises remain necessary.

Having a polynomial bound separately for every fixed r is not the same as one polynomial bound uniform over all r up to n. The factor 2^r in (19) is constant in the first statement and may be exponential in the second. These bounds also show that any superpolynomial lower-bound family in this explicit-input model must escape r=O(log N); large r alone still does not force hardness, as the two-row plateau demonstrates.

### Input-inclusive physical memory is a different convention

If all N input bits are physically retained and counted from time zero, then S_phys is at least N and C_phys is at least N(T+1). The small-initial-state premise of (17) then fails for that physical memory total. If input loading is itself charged, its cost must also be stated. A prefix-based sublinear computation assumes already-present read-only input and counted access to the required row offsets and metadata; otherwise header discovery or authentication must be added. It does not claim that copying N bits into owned storage takes sublinear time.

## 7. A guarded source showing that the final release can contain arbitrary 3-SAT

Let H be an arbitrary strict 3-CNF, and introduce new variables p,x,a,b and one private s_C for each clause C=(l1 or l2 or l3) of H. Add the four guards

\[
\begin{aligned}
G_1&=(p\lor x\lor a),&
G_2&=(p\lor x\lor\neg a),\\
G_3&=(p\lor\neg x\lor b),&
G_4&=(p\lor\neg x\lor\neg b),
\end{aligned}
\tag{21}
\]

and for each C add

\[
A_C=(\neg p\lor l_1\lor s_C),\qquad
B_C=(\neg s_C\lor l_2\lor l_3).
\tag{22}
\]

Call the resulting strict 3-CNF F(H). All-zero alpha violates only G1, regardless of the signs appearing in H. The reference hint and its unique false-row position are uniformly computable for both SAT and UNSAT source formulas.

The four guards force p=1. Under p=1, the pair A_C,B_C has an extension in its private s_C exactly when C is true. Therefore

\[
F(H)\text{ is SAT}\iff H\text{ is SAT}.
\tag{23}
\]

If H has n_H variables and m_H clauses, F has n_F=n_H+m_H+4 variables and 2m_H+4 rows. In canonical fixed-record formats, new variable identifiers and output records are generated from a constant number of source fields and logarithmic-bit arithmetic. This gives polynomial, and under the stated local fixed-record convention near-linear up to logarithms, compilation with small requested-bit workspace. It is not a claim about arbitrary unparsed text formats.

### An optimized erasure path

Erase a first and retain p=x=0. The first two source rows become a and not-a. Release all other values except p,x in any order. At each fresh level,

\[
\mu=2\qquad(1\le r\le n_F-2).
\tag{24}
\]

Next release x, retaining only p=0. The four guards form a minimum core of size four. The split-clause component is simultaneously satisfiable with all s_C=0 and imposes no contradiction. Thus mu=4 at r=n_F-1.

Finally release p. If H is UNSAT, then

\[
\boxed{\mu(F(H))=4+2\mu(H).}
\tag{25}
\]

**Proof of (25).** Every UNSAT source subset needs all four guard rows. If one is missing, choose p=0, satisfy the remaining three guards, and set every s_C=0 to satisfy all split rows. With all four guards present p=1 is forced. A selected gadget with only A_C or only B_C imposes no restriction on H's variables, because its private s_C can satisfy that single clause. A complete pair imposes exactly C. An UNSAT subset must therefore contain complete pairs for an UNSAT subset of H, and these suffice with all four guards. Minimum cardinality is exactly four plus twice mu(H). QED.

If H is SAT, the last residual is SAT instead. All earlier p=0 levels are nevertheless UNSAT. Therefore the easy preceding levels do not preserve the original answer. The final release exposes the full original decision problem rather than inheriting a solved answer from those independent earlier instances.

The two-row plateau is sharp under the near-assignment first-erasure condition by (4). With only one variable pinned in strict 3-CNF, every residual clause still has at least two unknown literals and forbids at most one quarter of the completion cube. Consequently every UNSAT core has at least four rows. Pinning p=0 attains this minimum at the penultimate level. This is a source-support counting bound, not a requirement for an algorithm to enumerate assignments.

The helpful pair is deliberately in the first two source positions. When row offsets and needed metadata are available through the counted indexed read-only-input contract, a fixed correct solver can read those two rows and the p,x pin fields, verify the opposite units, and reject in polylogarithmic bit cost throughout (24), using a general correct fallback elsewhere. Otherwise add header discovery and any required authentication, conservatively yielding a near-linear bound. This qualification matters for a format beginning with the unary header 1^n0. After finding and verifying the contradiction, the solver need not inspect the remaining clauses. A separate workflow's full input-loading or authentication requirement must be charged explicitly.

The penultimate level is also recognizable from the first four rows and the supplied p=0 field: their fixed guard pattern is contradictory under that pin. At r=0 the first row is already false. One fixed solver can include these three recognizers and a general fallback. Every prefinal level therefore has a polylogarithmic recognition route when row offsets and needed metadata are available through the counted indexed input contract; otherwise add header discovery and authentication, conservatively near-linear. Generating the source F(H), relocating its rows, or loading it into counted owned storage is separate work whenever the task requires those actions during the same run.

Thus both facts coexist: raw acquisition has a genuine linear worst case even at one unknown, and a favorable fixed family can expose its contradiction at a prefix through almost every level. The final unrestricted level can still encode arbitrary strict 3-SAT. No universal extra local cost, monotone time increase, or per-erasure cost summation follows from the semantic profile.

## 8. What remains to prove for a separation

An analysis of the fastest favorable path must specify what the analyst may choose, what the machine is given, which choices are computed during the charged run, and which SAT comparisons remain permitted. It must also preserve the order of quantifiers over uniform solvers and large adversarial inputs.

The proved plateau blocks a universal argument that each release makes every useful obstruction more expensive. The guarded construction shows why nearly all intermediate levels can be easy while the final release retains the original hard decision question. The row-query adversary shows a genuine compulsory acquisition cost, but only linear in its represented source and under the declared query interface.

To cross from these facts to a superpolynomial lower bound, one still needs a theorem about the total computation of every fixed correct solver on the remaining unrestricted family. Semantic support, contextual state counts, input probes, and a chosen proof calculus cannot supply that theorem by themselves. Arbitrary preprocessing, algebraic combinations, alternative obstructions, and shared computation remain allowed and charged throughout.

## Provenance and validation scope

The proofs in this note are elementary derivations for the present continuation. No new external literature claim or finite enumeration is required for the row-query, plateau, or guarded-compiler arguments. The earlier primary-source SAT time-space theorem and its local-transfer hypotheses are used only conditionally in Section 6; they are documented in `fresh_static_levels/Static_Restriction_Resource_Transfer.md` and the integrated predecessor report. The root's independent finite audit of the guarded construction should be cited separately if its numerical example is included in the deliverable.

Related internal derivations: `obstruction_cost_levels/Universal_Evidence_Cost_Framework.md` and `obstruction_cost_levels/Shortest_Obstructions_and_Charged_Incompatibility_2026-11-22.md`. No repository mutation is performed by this contributor.
