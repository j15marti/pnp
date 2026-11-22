# Charged UNSAT transport with adjacent local witnesses

> Repository publication note: This report was completed before the subsequent user request to direct and activate the agents. Section 16 records the original research run. Publication adds this note and updates the two companion-file links; the mathematical text and its stated review status are unchanged. Original report SHA-256: `154970e4b1cd35c318f99d2a93ee76cece328d4dcae90144178d9c29da43a27c`.

**Research date:** 21 November 2026, America/Los_Angeles  
**Named dependency:** CHARGED-UNSAT-TRANSPORT1  
**Target:** Convert minimum distinguishable information into compulsory computation on an actual UNSAT execution, using the project's charged machine model.  
**Status:** PROVED/EXACT for the stated deterministic single-tape model and ordered input encoding. Unrestricted superpolynomial SAT lower bounds remain OPEN.  
**Review:** The construction, crossing transfer, cumulative accounting, matching upper bound, and static-method ceiling were independently reconstructed by collaborating agents. This is internal mathematical review, not external peer review or a proof-assistant kernel verification.

## 1. Main result and its integration point

There is an explicit family of proper 3-CNF formulas with all the following properties.

Each formula is the conjunction of a Horn part and a dual-Horn part. The input supplies a satisfying assignment for each part, and the two assignments differ in exactly one bit. Each assignment violates exactly one clause of the whole formula. Nevertheless, every fixed correct solver in the project's deterministic single-tape model has UNSAT inputs in this family requiring, on the same execution,

\[
\boxed{
T=\Omega_A(N^2),\qquad
CM_{\min}=\Omega_A(N^3),\qquad
CM_{\mathrm{phys}}=\Omega_A(N^3).
}
\tag{1}
\]

Here \(N\) is the full encoded input length, including both supplied assignments and the final-release variable identifier. The constants can depend on the fixed solver \(A\).

This is a compulsory transport theorem for decision, directly on UNSAT instances. The handoff's bitstring decision example has logarithmic losses; the present construction attains the full quadratic and cubic orders for the Boolean compatibility task. A strengthened strict T5 decision theorem is not asserted. The counting and decision constructions remain distinct.

The bounds are tight in order on this family: one fixed all-input-correct solver authenticates the family and decides it using

\[
T=O(N^2),\qquad S=O(N),\qquad CM_{\mathrm{phys}}=O(N^3).
\tag{2}
\]

A second result explains why this particular method stops there. For any static separated-input family of the type used below, its distinguishing-information demand satisfies

\[
\boxed{Dh\le N^2/8,\qquad Dh^2\le N^3/27.}
\tag{3}
\]

Thus the charged model closes a genuine lower-bound step, while also exposing a precise obstruction to superpolynomial amplification by static distinguishability alone.

No claim of historical priority is made. The crossing technique is classical; the cumulative extension is reconstructed from the supplied project handoff. [1,3]

### Candidate and four falsifiers

The candidate was: preserve the one-bit compatibility construction while replacing a bitstring comparison by a permutation comparison, and apply the handoff's crossing and cumulative-information proofs to the target's actual layout.

The four load-bearing falsifiers were:

1. A diagonal formula might fail to be UNSAT, or a distinct-index hybrid might fail to be SAT.
2. The compiler or witness metadata might mix the two input indices across the purported separated blocks.
3. The cumulative argument might combine different inputs or count one physical transition several times.
4. A legal family recognizer might show that the resulting bound is polynomial and cannot be used as a superpolynomial bridge.

The first three were excluded by the proofs below. The fourth is realized by the matching upper bound and sets the theorem's scope.

## 2. The charged model

Use the model of the attached handoff, rather than a unit-cost machine with free random access. [1, §§5–6]

The fixed deterministic machine has one physical read/write tape, one head, a fixed finite tape alphabet, and \(Q\ge2\) control states. Input, work, stored addresses, and output occupy that tape. A transition reads and writes the scanned cell and moves by at most one cell. Output and its terminator start at a fixed left origin. There is no independently moving input head, external work store, original-input oracle, or free clock affecting continuation.

Let \(C_t(I)\) be the complete configuration immediately after transition \(t\). Fix the physical convention: \(s_t(I)\) is one plus the length of the smallest tape interval containing the origin, head, and all nonblank cells, with a fixed constant-factor conversion from cells to bits. Contents, support, head position, and finite control have a faithful binary encoding of length \(O_A(s_t)\). This standard span charge, rather than an arbitrary larger charge, is used in every physical upper and lower bound below.

On one execution define

\[
T_A(I)=\text{number of transitions},\qquad
S_A(I)=\max_{0\le t\le T_A(I)}s_t(I),
\]

\[
CM_{\mathrm{phys},A}(I)=\sum_{t=1}^{T_A(I)}s_t(I),
\]

\[
CM_{\min,A}(I)=\sum_{t=1}^{T_A(I)}
K_U(C_t(I)\mid A).
\tag{4}
\]

Take \(U\) to be a fixed prefix-universal description convention. The input \(I\) and time \(t\) are not free decoder side information. These minimum descriptions need not be efficiently discoverable or decodable. They are an information measure, not a second implementation.

The cumulative-memory concept sums storage over execution time; the distinction from peak memory is also standard in the broader literature. The particular cubic theorem here comes from the project's crossing argument, not from importing a general cumulative-memory theorem. [4]

### Cap ledger

For one fixed proposed cap

\[
T_A(N)\le K N^a,\qquad a\ge1,
\tag{5}
\]

where \(K,a\) are independent of the input, local head motion gives

\[
S_A=O_A(N+T_A),
\qquad
CM_{\mathrm{phys},A}=O_A(T_A(N+T_A)).
\tag{6}
\]

Describing the original input and the transition index permits replay of a complete configuration:

\[
CM_{\min,A}
\le O_A\!\left(T_A(N+\log(T_A+2))\right).
\tag{7}
\]

Consequently,

| Resource | Ceiling implied by the cap |
|---|---:|
| Time | \(O(N^a)\) |
| Peak physical storage | \(O(N^a)\) |
| Physical cumulative storage | \(O(N^{2a})\) |
| Self-contained minimum-description CM | \(O(N^{a+1})\) |

A fixed program has constant description size. Its repeated execution, movements, and accesses are charged when they happen. Neither the program nor the solver must store a transcript of its execution.

## 3. A decision-sensitive permutation family

The clause width is fixed at three throughout the final construction. Use \(r\ge3\) for the family parameter to avoid confusing it with the \(k\) in \(k\)-SAT.

For permutations \(\pi,\sigma\) of \(\{1,\ldots,r\}\), start with

\[
F^0_{\pi,\sigma}(X,Y)=
\left[\bigwedge_{i=1}^{r}(\neg X_i\lor Y_{\pi(i)})\right]
\land
\left[\bigvee_{i=1}^{r}X_i\right]
\land
\left[\bigwedge_{i=1}^{r}(\neg X_i\lor\neg Y_{\sigma(i)})\right].
\tag{8}
\]

The left constraints depend only on \(\pi\), the middle constraint is common, and the right constraints depend only on \(\sigma\).

### Lemma 1. Exact decision relation

\[
\boxed{F^0_{\pi,\sigma}\text{ is UNSAT}\iff\pi=\sigma.}
\tag{9}
\]

**Proof.** When \(\pi=\sigma\), any \(X_i=1\) would force both \(Y_{\pi(i)}=1\) and \(Y_{\pi(i)}=0\). Thus all \(X_i\) must be zero, contradicting their OR.

When \(\pi\ne\sigma\), choose an index \(i\) with \(\pi(i)\ne\sigma(i)\). Set \(X_i=1\), all other \(X_j=0\), \(Y_{\pi(i)}=1\), and every other \(Y_j=0\). In particular \(Y_{\sigma(i)}=0\). This satisfies every clause. \(\square\)

There are \(r!\) diagonal UNSAT inputs, and every off-diagonal hybrid is SAT. The orientation matters: the handoff's witness-packing ceiling for SAT diagonals and UNSAT off-diagonals does not apply here. [1, §13.5]

### Proper 3-CNF conversion

For every binary clause \(a\lor b\), insert

\[
(a\lor b\lor p)\land(a\lor b\lor\neg p),
\tag{10}
\]

with one common fresh \(p\). This conjunction equals \(a\lor b\) for both values of \(p\), so sharing \(p\) is sound.

For \(r=3\), use the single middle clause \(X_1\lor X_2\lor X_3\). For \(r\ge4\), introduce \(t_1,\ldots,t_{r-3}\) and use

\[
(X_1\lor X_2\lor t_1),
\]

\[
(\neg t_j\lor X_{j+2}\lor t_{j+1})
\quad(1\le j\le r-4),
\]

\[
(\neg t_{r-3}\lor X_{r-1}\lor X_r).
\tag{11}
\]

Existentially eliminating the \(t_j\) gives the OR in (8). If all \(X_i=0\), the first clause forces \(t_1=1\), the internal clauses propagate ones, and the last clause fails. If some \(X_i=1\), one valid choice is \(t_j=\neg(X_1\lor\cdots\lor X_{j+1})\).

Call this proper 3-CNF \(F_{\pi,\sigma}\). Its exact size is

\[
\boxed{n_0=3r-2,\qquad m_0=5r-2.}
\tag{12}
\]

Its ordered list contains \(2r\) left clauses, \(r-2\) middle clauses, and \(2r\) right clauses. The conversion preserves (9).

## 4. The adjacent-witness compiler

Apply the compiler from the preceding compatibility report. [2] Introduce \(y,u,v\) and one fresh \(z_C\) per source-clause occurrence.

Use

\[
P(y,u,v)=
(y\lor u\lor v)
\land(y\lor u\lor\neg v)
\land(y\lor\neg u\lor v)
\land(y\lor\neg u\lor\neg v).
\tag{13}
\]

Pointwise, \(P\equiv y\). For each ordered source clause \(C=(a\lor b\lor c)\), add

\[
(\neg y\lor a\lor z_C)
\land
(\neg z_C\lor b\lor c).
\tag{14}
\]

Let \(B_{\pi,\sigma}\) be the conjunction. Since

\[
\exists z_C\,
[(\neg y\lor a\lor z_C)\land(\neg z_C\lor b\lor c)]
\equiv \neg y\lor a\lor b\lor c,
\]

we obtain

\[
\boxed{
\exists(u,v,Z)\,B_{\pi,\sigma}
\equiv y\land F_{\pi,\sigma}.
}
\tag{15}
\]

In particular,

\[
\boxed{B_{\pi,\sigma}\text{ is UNSAT}\iff\pi=\sigma.}
\tag{16}
\]

The compiler is used for decision equivalence. No parsimonious model-count transformation is assumed.

### The local witnesses remain adjacent

Let \(H_{\pi,\sigma}\) contain clauses of \(B_{\pi,\sigma}\) with at most one positive literal; let \(D_{\pi,\sigma}\) contain those with at least two positive literals. Then \(H\) is Horn, \(D\) is dual-Horn, and \(B=H\land D\).

Define

\[
\alpha=(u=1,\text{ every other variable }0),
\qquad
\beta=(u=v=1,\text{ every other variable }0).
\tag{17}
\]

Every proper 3-Horn clause has at least two negative literals, so \(\alpha\models H\). At \(\beta\), every source pair is satisfied by \(\neg y\) or \(\neg z_C\), and the three dual-Horn selector clauses hold. Therefore

\[
\boxed{\alpha\models H,\quad\beta\models D,\quad d_H(\alpha,\beta)=1.}
\tag{18}
\]

The only clause falsified by \(\alpha\) is \(y\lor\neg u\lor v\); the only one falsified by \(\beta\) is \(y\lor\neg u\lor\neg v\).

Exact target counts are

\[
\boxed{n=8r-1,\qquad m=10r,\qquad |H|=8r-2,\qquad |D|=2r+2.}
\tag{19}
\]

For the permutation family, the number of variables shared by \(H,D\) is \(5r-2\). A large shared interface therefore coexists with the polynomial family solver proved below.

## 5. Explicit encoding and physical separation

We use the Boolean counterpart of the handoff's explicit unary-declaration encoding. This is stated explicitly because the preceding compatibility audit used a different gamma-coded variable header; its finite byte counts are not reused.

Give the source variables these identifiers:

\[
X_i=i,\quad Y_i=r+i,\quad p=2r+1,
\]

with the chain variables next, up to \(n_0=3r-2\). Then

\[
y=n_0+1,\quad u=n_0+2,\quad v=n_0+3,\quad z_j=n_0+3+j
\]

for source-clause positions \(1\le j\le m_0\).

Let

\[
w=\lceil\log_2(n+1)\rceil=\lceil\log_2(8r)\rceil.
\]

Encode the input as

\[
1^n0\ \gamma(m+1)\
[\text{ordered signed 3-literal clauses}]\
[\alpha]\
[\beta]\
[\text{\(w\)-bit identifier of \(y\)}].
\tag{20}
\]

Each literal uses one sign bit and a \(w\)-bit variable identifier. Each assignment uses exactly \(n\) bits, in increasing variable-ID order. The last field identifies the variable released last; the release order itself is a fixed common rule and is not silently encoded as a free arbitrary permutation.

Thus

\[
\boxed{
N=3n+2+2\lfloor\log_2(m+1)\rfloor+3m(w+1)+w
=\Theta(r\log r).
}
\tag{21}
\]

The unary declaration and explicit witnesses charge declared variables, including any unused ones in the map-family extension below.

Keep this clause order:

1. Four selector clauses.
2. \(4r\) compiled left clauses.
3. \(2r-4\) compiled middle clauses.
4. \(4r\) compiled right clauses.

The physical input factors as

\[
\boxed{I_{\pi,\sigma}=L_\pi\,M_r\,R_\sigma.}
\tag{22}
\]

The left block includes the common header and selector. The right block includes the common witness/release trailer. All fresh identifiers depend only on clause positions and \(r\), never jointly on \(\pi,\sigma\).

The middle has \(6(r-2)(w+1)\) bits. Select all its interior boundaries:

\[
\boxed{D=6(r-2)(w+1)-1=\Theta(N).}
\tag{23}
\]

**The physical blocks \(L,M,R\) are not the logical Horn and dual-Horn parts \(H,D\).** The latter are derived from clause signs. Arbitrarily regrouping the input into all Horn clauses followed by all dual-Horn clauses changes the physical layout and would require a new proof.

The solver is free to reorganize this ordered input after starting. Every transition used to do so belongs to its charged execution.

## 6. Compulsory information transfer and quadratic time

Fix one deterministic solver \(A\), correct on every valid input of this compatibility problem. Correctness on all hybrids is essential: a solver promised only diagonal UNSAT inputs could return UNSAT immediately.

Let

\[
P=r!,\qquad h=\log_2 P.
\tag{24}
\]

The elementary bounds \((r/2)^{\lfloor r/2\rfloor}\le r!\le r^r\), for large \(r\), give

\[
h=\Theta(r\log r)=\Theta(N).
\tag{25}
\]

At a selected cut \(b\), let \(CS_b(\pi)\) record the control state immediately after each crossing in the run on \(I_{\pi,\pi}\). The head starts left of the cut, so the crossing index determines direction.

### Lemma 2. Complete crossing sequences are injective

\[
\pi\longmapsto CS_b(\pi)
\quad\text{is injective for each selected cut.}
\tag{26}
\]

**Proof.** Suppose distinct \(\pi,\sigma\) had the same complete crossing sequence. Combine the left excursions of the run on \(I_{\pi,\pi}\) with the right excursions of the run on \(I_{\sigma,\sigma}\). The initial tape is precisely \(I_{\pi,\sigma}\). Matching entry states ensure every local excursion fits. Equal crossing counts imply the same final head side and a halting spliced computation.

The fixed-left output inherits the common diagonal answer, UNSAT. But \(I_{\pi,\sigma}\) is SAT by (16). This contradicts correctness. \(\square\)

The argument works with rejecting diagonal runs; the acceptance orientation is immaterial. Fixed-left output, or an equivalent labeled-halting convention, supplies the necessary answer consistency. The classical crossing method is described in Hartmanis's original paper. [3]

There are fewer than \(Q^j/(Q-1)\) strings of length below \(j\). Injectivity over \(P\) diagonals therefore forces average crossing length \(\Omega(h/\log Q)\) at every selected cut.

Average over the same uniform random \(\pi\) at every cut. Because a physical transition crosses at most one boundary,

\[
\mathbb E_\pi T_A(I_{\pi,\pi})
\ge \sum_b\mathbb E_\pi |CS_b(\pi)|
=\Omega(Dh/\log Q).
\tag{27}
\]

Thus some UNSAT diagonal has

\[
\boxed{T_A(I_{\pi,\pi})=\Omega_A(N^2).}
\tag{28}
\]

No assignment enumeration, resolution proof, recursion tree, or explicit compatibility table is required of the solver.

## 7. Cubic cumulative cost on the same execution

Time times a peak-space lower bound would be insufficient: the peaks might occur on different inputs or at different times. Instead, charge actual crossing events using complete configurations.

Let \(C_{b,j}(\pi)\) be the complete configuration at the \(j\)-th crossing of cut \(b\), if that crossing occurs. Let \(p_{b,j}(\pi)\) be its first \(j\) crossing states.

### Lemma 3. Prefix plus current configuration is injective

On diagonal inputs reaching crossing \(j\),

\[
\pi\longmapsto
\bigl(p_{b,j}(\pi),C_{b,j}(\pi)\bigr)
\quad\text{is injective.}
\tag{29}
\]

**Proof.** Suppose two distinct diagonal runs have the same prefix and full configuration. Splice their left and right histories only through crossing \(j\). The left tape comes from the first diagonal and the right tape from the second. Equality of the decoded complete configurations makes this precisely the second diagonal's complete current state.

The SAT hybrid would now have the identical future of an UNSAT diagonal, giving the wrong output. Absolute crossing times may differ, but the model has no free external clock; every continuation-relevant item is in the configuration. \(\square\)

### Finite counting bound

For integers \(j\ge1,s\ge0\), define

\[
E_j(s)=\frac{Q^j-1}{Q-1}+Q^j(2^s-1).
\tag{30}
\]

The first term bounds diagonals with fewer than \(j\) crossings, by Lemma 2. The second bounds diagonals reaching crossing \(j\) whose self-contained configuration code is shorter than \(s\), by Lemma 3. There are at most \(Q^j\) prefixes and \(2^s-1\) binary strings of length below \(s\).

Therefore

\[
\Pr_\pi[
\text{crossing \(j\) occurs and code length is at least \(s\)}
]
\ge \max\{0,1-E_j(s)/P\}.
\tag{31}
\]

For any nonnegative integers \(q,s\), summing distinct events gives

\[
\boxed{
\mathbb E_\pi CM_{\mathrm{code},A}(I_{\pi,\pi})
\ge Ds\sum_{j=1}^{q}\max\{0,1-E_j(s)/P\}.
}
\tag{32}
\]

This holds for any fixed faithful self-contained code, including canonically chosen shortest descriptions. Efficient encoding or decoding is unnecessary.

Take

\[
q=\left\lfloor\frac{h}{4\log_2Q}\right\rfloor,\qquad
s=\lfloor h/4\rfloor.
\]

Then \(E_j(s)/P\) tends rapidly to zero, and

\[
\mathbb E_\pi CM_{\min,A}(I_{\pi,\pi})
=\Omega(Dh^2/\log Q)
=\boxed{\Omega_A(N^3)}.
\tag{33}
\]

### Simultaneous time and CM

To put both demands on the same input, choose \(0\le z\le h\), set \(h'=h-z\), and use

\[
q=\lfloor h'/\log_2Q\rfloor,\qquad
s_j=\lfloor h'-j\log_2Q\rfloor.
\tag{34}
\]

For every \(j\le q\), \(E_j(s_j)\le P2^{-z}\). A union bound over the \(Dq\) events gives

\[
\boxed{
\Pr_\pi\left[
T_A(I_{\pi,\pi})\ge Dq
\ \land\
CM_{\min,A}(I_{\pi,\pi})\ge D\sum_{j=1}^{q}s_j
\right]\ge
\max\{0,1-Dq\,2^{-z}\}.
}
\tag{35}
\]

For any desired fixed inverse-polynomial failure probability, \(z=O_{A,c}(\log N)\) suffices and retains the quadratic and cubic orders. The exceptional permutations can depend on \(A\) and the fixed code.

A faithful physical storage convention has \(K(C_t\mid A)\le O_A(s_t)\). Thus the same execution also has

\[
CM_{\mathrm{phys},A}\ge\Omega_A(CM_{\min,A})
=\Omega_A(N^3).
\tag{36}
\]

## 8. Minimum distinguishable information as a conservation inequality

Lemma 3 gives a direct interpretation of the user's proposed information measure.

For a diagonal reaching crossing \(j=O(N)\),

\[
\boxed{
K(\pi\mid A,r)
\le
j\lceil\log_2Q\rceil
+
K(C_{b,j}(\pi)\mid A)
+
O_A(\log N).
}
\tag{37}
\]

A description supplies the cut \(b\), crossing index \(j\), the \(j\) states, and a shortest self-contained program for the current configuration. The first two fields need \(O(\log N)\) bits. A decoder enumerates the finitely many diagonal permutations, simulates their runs, and finds the unique matching prefix/configuration pair. It may take a long time; that is allowed for this untimed description-length argument.

Rearranging,

\[
K(C_{b,j}(\pi)\mid A)
\ge
K(\pi\mid A,r)
-j\lceil\log_2Q\rceil-O_A(\log N).
\tag{38}
\]

For an incompressible \(\pi\), information not yet accounted for by the crossing transcript must remain in the current configuration. Repeated residence of that information at distinct actual transitions creates cumulative cost. This does not require new Shannon information to be generated during computation.

The theorem does not assign cubic minimum-description CM to every explicit diagonal. For example, the identity permutation is generated from \(r\) by a short fixed program. On the quadratic family solver below, replay gives

\[
CM_{\min}(I_{\mathrm{id},\mathrm{id}})
=O(N^2\log N).
\tag{39}
\]

This is consistent with the almost-all and solver-dependent worst-case quantifiers. Physical expanded storage can still be larger.

## 9. A fully paid matching upper bound

The family remains computationally simple after its two pieces can be compared. This supplies a necessary control against overclaiming.

### Broader recognizable map family

Allow arbitrary maps \(f,g:\{1,\ldots,r\}\to\{1,\ldots,r\}\), not just permutations, in (8). The same proof gives

\[
B_{f,g}\text{ is UNSAT}\iff f=g.
\tag{40}
\]

This avoids an unnecessary permutation-validation task. Declared but unused \(Y\) variables are explicitly charged in (20).

A fixed multitape machine can authenticate the entire canonical family in \(O(N)\) bit operations and \(O(N)\) total storage. It checks the header, the exact selector, every source-pair pattern and auxiliary ID, the doubled padding literals, the OR chain, identifier ranges, both witnesses, the final-release identifier, and the input end. It copies the \(f(i)\) records and compares the \(g(i)\) records against them.

There are \(O(r)\) clause records of \(O(\log r)\) bits. The expected-identifier arithmetic, copying, and comparisons take \(O(\log r)\) time per record. Witness validation costs at most \(O(r\log r)\). Unary-header counters can be handled with amortized linear bit work. Huge or malformed declarations are checked against the input rather than trusted for unbounded initialization.

Only after authentication does the machine return UNSAT exactly when the map lists match. Otherwise, it uses a generic total exhaustive SAT fallback on the retained original input. Hence this is one correct solver for all permitted inputs, with a special speed guarantee only for the recognized family.

Simulate its fixed number of tapes on one physical tape, with finitely many tracks. The virtual computation uses \(O(N)\) steps and \(O(N)\) cells. A fixed number of full-span sweeps simulates each virtual step in \(O(N)\) physical transitions. Initialization, head markers, copies, and final left-origin output are included.

Therefore, on every member of the family,

\[
\boxed{
T=O(N^2),\quad S=O(N),\quad
CM_{\mathrm{phys}}=O(N^3),\quad CM_{\min}=O(N^3).
}
\tag{41}
\]

This matching upper bound is symbolic. The audit program does not claim to implement this Turing-machine simulation.

### Construction and conversion costs

For a canonical source and target of combined encoded length \(R\), the source-to-target compiler is implementable in \(O(R)\) bit time and \(O(R)\) space on a fixed multitape machine. The safe sole-tape bounds obtained by the same simulation are \(O(R^2)\) time, \(O(R)\) span, and \(O(R^3)\) physical CM. On this family, source and target lengths are within constant factors.

The target lower bound was proved directly from its own ordered layout. It was not transferred by subtracting a potentially quadratic compilation cost.

Every step used by an alternative representation, cache, learned fact, source relocation, or failed attempt is permitted and charged in the original whole-run lower bound. Shared physical cells count once.

## 10. Comparison with a proposed polynomial cap

The demands and ceilings are:

| Resource | Proved demand on UNSAT executions | Ceiling under \(T\le KN^a\) | Consequence |
|---|---:|---:|---|
| Time | \(\Omega(N^2)\) | \(O(N^a)\) | Excludes \(a<2\) |
| Minimum-description CM | \(\Omega(N^3)\) | \(O(N^{a+1})\) | Again excludes \(a<2\) |
| Physical CM | \(\Omega(N^3)\) | \(O(N^{2a})\) | Alone excludes \(a<3/2\) |
| Peak physical storage | Input-scale \(\Omega(N)\) | \(O(N^a)\) | No additional exclusion for \(a\ge1\) |

The time and descriptive-CM constraints identify the same threshold. Multiplying them does not produce a stronger exponent. Quadratic time remains consistent and is attained on this family by (41).

For a finite illustration, let \(r=1000\), \(Q=256\), and \(z=40\). Use \(h_0=\lfloor\log_2(r!)\rfloor=8529\), which safely replaces \(h\) in the finite inequality. The audit computes

\[
N=444038,\quad D=83831,\quad q=1061,
\]

\[
T\ge 88944691,
\qquad
CM_{\mathrm{code}}\ge 377214434531,
\tag{42}
\]

simultaneously on a fraction at least

\[
1-\frac{88944691}{2^{40}}
=0.9999191052747847
\tag{43}
\]

of the diagonal inputs, for each fixed correct machine with at most the stated number of states.

These are mathematical bound instantiations, not measured solver runtimes. The physical-CM implication includes the fixed encoding constants and is not assigned the identical finite numerical coefficient.

## 11. An exact ceiling for static separated-input distinguishability

### Theorem 2. Static demand ceiling

Suppose binary strings

\[
I_{u,v}=L_uMR_v
\]

have fixed block lengths \(\ell_L,\ell_M,\ell_R\), total \(N\), one common diagonal label, and the opposite label for every \(u\ne v\). Let \(P\) be the number of diagonal indices, \(h=\log_2P\), and \(D\) the number of selected boundaries inside \(M\).

Then

\[
Dh\le N^2/8,\qquad Dh^2\le N^3/27.
\tag{44}
\]

**Proof.** Both \(u\mapsto L_u\) and \(u\mapsto R_u\) must be injective. If \(L_u=L_v\) for \(u\ne v\), then \(I_{u,v}=I_{v,v}\), although their required labels differ. The right-side argument is identical.

Thus

\[
h\le\min(\ell_L,\ell_R),\qquad D\le\ell_M,
\]

so

\[
D+2h\le N.
\]

Therefore

\[
Dh\le h(N-2h)\le N^2/8,
\]

and

\[
Dh^2\le h^2(N-2h)\le N^3/27.
\]

The maxima occur at \(h=N/4\) and \(h=N/3\), respectively. \(\square\)

This theorem bounds the demands certified by this static crossing formula. It is not an upper bound on the running time of all SAT algorithms. The recognizable family additionally has the concrete upper bound (41).

The permutation construction achieves quadratic and cubic order within the method. Increasing the size of the static index set or adding common padding cannot by itself yield superpolynomial demand at unchanged input length. Hartmanis also explicitly discusses the quadratic limitation of this kind of separated equality construction. [3]

## 12. Connection to variable-value removal

Start at the near-solution \(\alpha\). Release every assigned value except \(y=0\), leaving \(y\) for last. Every such residual is UNSAT because \(P\equiv y\).

Immediately before the final release, all other variables are free. The same two supplied assignments satisfy their respective restricted Horn and dual-Horn blocks. After releasing \(y\), the decision is exactly (16).

This locates the charged family inside the user's erasure construction. The theorem lower-bounds the complete execution on the exposed instance, including any preprocessing or information relocation. It does not force those transitions to occur after the physical act of erasing the last value.

A solver can authenticate the complete formula and compare the two maps earlier, keep the one-bit result, return UNSAT at every stage with \(y=0\), and use the cached final result when \(y\) is released. That is a legal strategy and its earlier work is charged. Consequently, repeated erasure stages cannot be assigned independent copies of the same comparison cost without a new disjointness or bounded-reuse theorem.

Likewise, giving the fully processed input or a precomputed answer for free changes the starting-state model. Conditioning descriptive CM on the original input would also change the measure: replay then needs essentially the time index rather than another self-contained encoding of the source.

## 13. What would be needed beyond this result

A superpolynomial lower bound would require new compulsory work after static information transport can be completed. The handoff's bounded-reuse lemma gives a precise target. [1, §15]

For actual reconstruction obligations \(U_j\), decoder side information \(B_j\), and records \(\Pi_j\) that are conditionally prefix-free given \(B_j\), one would need

\[
H(U_j\mid B_j,\Pi_j)=0,
\]

\[
|\Pi_j|\le b|E_j|+h_j,
\]

where \(E_j\) consists of real charged events, \(h_j\) includes all framing and length metadata, and each event belongs to at most \(\rho\) obligation sets. Then

\[
\mathbb E[T]\ge
\frac{\sum_jH(U_j\mid B_j)-\sum_j\mathbb E[h_j]}
{b\rho}.
\tag{45}
\]

To contradict a fixed cap \(KN^a\), the numerator must exceed \(b\rho KN^a\) on the same input regime.

The unresolved premise is compulsory generation of sufficiently many such obligations for an arbitrary correct decision algorithm, with retained input, caches, alternate representations, and joint computation fully included. Virtual residual questions cannot be treated as machine events merely because a branching algorithm would ask them.

**Next named target:** DYNAMIC-COMPATIBILITY-OBLIGATION1. Construct a source-authenticated, decision-sensitive family and a post-transport obligation with a real decoder and bounded event reuse, or prove that a proposed obligation collapses under paid joint preprocessing. The present static permutation family cannot supply the required superpolynomial growth because (41) and (44) give explicit ceilings.

## 14. Gates and scope controls

| Gate | Status and reason |
|---|---|
| DISJ/equality sanity | PASS for the stated single-tape theorem. A polynomial map-equality shortcut is preserved and charged. Transfer of these exponents to unrestricted access FAILS. |
| Relativization | No barrier bypass is claimed. A nonlocal oracle or extra input head invalidates the physical locality premise. Unrestricted all-model separation remains OPEN. |
| Simultaneous DTISP/accounting | PASS. Equation (35) puts time and cumulative cost on the same diagonal execution; no unrelated time and space maxima are multiplied. |
| Deterministic configurations | PASS. The required prefix/configuration injection is proved by valid hybrids. A generic configuration-counting upper bound is not used as a work lower bound. |

The argument makes no ETH, SETH, cryptographic, or circuit-hardness assumption. It makes no assertion about randomized or quantum machines. It does not claim a Natural Proofs or algebrization-barrier bypass.

There is no exact-\((2P,2N)\) occurrence claim. Proper width three, distinct variables inside clauses, adjacent local witnesses, and exact decision semantics are the preserved properties.

The family has short logical refutations on diagonal inputs. This is compatible with physical comparison costs. The proof counts possible communication histories; it does not require the SAT solver itself to count satisfying assignments.

## 15. Finite validation and reproducibility

The companion complete program is [charged_unsat_transport_audit.py](../../experiments/charged_unsat_transport_20261121/charged_unsat_transport_audit.py). Raw results are [charged_unsat_transport_results.json](../../results/raw/charged_unsat_transport_20261121/charged_unsat_transport_results.json).

The run used Python 3.12.14, no random sampling, and a 30-second process limit. It finished in approximately 1.01 seconds.

| Audit item | Observed result |
|---|---:|
| Permutation pairs for \(r=3,4\) | 612 |
| Additional map-family controls | 8 |
| Total formula-pair instances | 620 |
| SAT instances | 586 |
| UNSAT instances | 34 |
| Source assignments enumerated | 596,736 |
| Assignment evaluations, including local/constructive checks | 599,176 |
| Clause evaluations | 3,888,018 |
| Assertions passed | 11,558 |

The audit exhaustively checks the source projection to the \(X,Y\) variables for all permutation pairs at \(r=3,4\), plus the small nonpermutation controls. It verifies proper clauses, exact sizes, local witnesses, unique failed selector clauses, exact encoded length, common middle, left/right dependence, and constructive compiled SAT witnesses.

The selector and guarded-pair projection identities are exhaustively checked locally. The program does not enumerate all assignments of every compiled target, simulate arbitrary solvers, compute Kolmogorov complexity, or experimentally prove the asymptotic lower bound. The proof is in §§3–11.

The large finite resource instantiations use integer arithmetic, including exact factorial bit lengths and each per-event exception bound. They are theorem arithmetic, not performance benchmarks.

Code SHA-256:

    98b46a013cabc3f969bcf58c08da2b1fd6937a26e1b46e75a06318e03d34d4f4

Raw-results SHA-256:

    6a69225a6c95b9f1a35123fec8f7b9b66223c4d6778316b7f7b851be827c23c2

## 16. Source recovery and bounded research record

The attached handoff was read locally. Its SHA-256 is

    c9a3a0f362c72dfad7548b0cd44723853f105dcdc6a4f9ea5fef4559d3bb2a33

and its UTF-8 length is 141,084 bytes, matching the repository assignment directive.

The preceding compatibility report was inspected for its exact compiler, local witnesses, erasure semantics, and cost qualifications.

Repository governance was recovered through connected reads. Relevant current blob identifiers were:

| Source | Blob |
|---|---|
| AGENTS.md | 01f05d238736da1a3a2a10c9586be3d882751212 |
| CODEX.md | 15639f62a254aa9cd36a949b9f9d81985e5ed538 |
| PNP research skill | 6f37fc1a1713b01abd91794d5523fb05a57efa2f |
| End-to-end directive | 8451d955f6cd5397de0895f8ebb46e30818842c3 |
| T5 assignment directive | 776c2622d69dbcbb1c7c0d1361f299970fb7f1cc |

This continuation is a standalone report. No assigned living manuscript, repository branch, issue, schedule, or agent identity was modified. Repository preflight and LaTeX compilation were not run; the current workspace was not used as a repository checkout or LaTeX manuscript build.

Fresh corpus searches included “UNSAT diagonal permutation crossing” and “one bit Horn compatibility charged.” They surfaced prior source-head locality/ordering reports and the Horn transport ceiling. Those search excerpts were treated as duplicate-route controls, not imported as new proof dependencies. The complete supplied handoff and the preceding compatibility report are the project dependencies used here.

Fresh literature searches targeted Hartmanis's single-tape crossing method, cumulative memory, and UNSAT/permutation variants. The original Hartmanis PDF was inspected for the model, crossing splicing, and the explicit quadratic limitation. The ECCC page for Beame–Kornerup was inspected as cumulative-memory context only.

Fresh organization-scoped searches covered Anthropic, OpenAI, xAI, Google Research, Google DeepMind, and Google OR-Tools. Queries included:

- “site:github.com/anthropics OR site:github.com/openai theorem proving SAT satisfiability formal verification”
- “site:github.com/xai-org OR site:github.com/google-research OR site:github.com/google-deepmind SAT theorem proving formal verification”
- “site:github.com/xai-org SAT satisfiability proof verification”
- “site:github.com/google-research SAT crossing sequence lower bound”
- “site:github.com/google/or-tools cp-sat solver”

OpenAI and Anthropic organization pages showed domain-verification information. OR-Tools was linked from Google's developer site. Other organization pages and candidate search hits were inspected only to bound the search; no ownership-dependent theorem claim, repository algorithm, purported formal proof, or unverified new complexity claim was imported. No external formal-math checkout was built. The bounded search yielded no additional verified theorem needed for this derivation.

## References

1. Project handoff. *T5 Resource Lower Bounds: Exhaustive Handoff*, 21 November 2026. Particularly §§5–6, 8, 13–15, 18, and 20. [Supplied handoff](https://chatgpt.com/library?file_id=libfile_143523a26af88191af89e205130f3445&account_id=personal).

2. Preceding project report. *Compulsory computation and compatibility at witness distance one*, 21 November 2026. [Report](https://chatgpt.com/library?file_id=libfile_86e19bf90cb4819192139fbb66c6d8ad&account_id=personal).

3. J. Hartmanis. *Computational Complexity of One-Tape Turing Machine Computations*. Journal of the ACM 15(2), 325–339, 1968. DOI: 10.1145/321450.321464. [Original paper](https://cse.iitkgp.ac.in/~goutam/toc/readingMaterial/computational-complexity-one-tape-Hart.pdf). Classical model and crossing technique; the present cumulative extension is attributed to the project handoff.

4. Paul Beame and Niels Kornerup. *Cumulative Memory Lower Bounds for Randomized and Quantum Computation*. ECCC TR23-005, revision 2, 26 June 2023. [Primary repository](https://eccc.weizmann.ac.il/report/2023/005/). General cumulative-memory context; not used to assert the specific UNSAT-family theorem.
