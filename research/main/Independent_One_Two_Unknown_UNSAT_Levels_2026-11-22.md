# Independent one- and two-unknown UNSAT levels

22 November 2026, America/Los_Angeles.

Named dependency: STATIC-RESTRICTION-FRONTIER1.

## 1. The corrected question

The user clarified that variable removals define separate static problems. At each level, a fresh solver receives the original formula and the variable values that remain supplied. There is no prior execution, saved verdict, earlier proof, or shared history between levels. The purpose is to characterize the shortest logically sufficient route and the simultaneous resource frontier, not to prescribe or search for an algorithm.

This supersedes sequential-machine interpretations of this particular erasure experiment. Mathematical comparisons between the levels remain legitimate. Their execution costs are not added.

For a fixed finite domain D and constraint language Gamma, let

\[
I_r=(F,U,\rho),\qquad |U|=r,
\]

where rho assigns every variable outside U. Its decision question is

\[
\exists a\in D^U:\ F(\rho\cup a)=1.
\tag{1}
\]

Both SAT and UNSAT inputs are allowed. An analyst can focus on an UNSAT formula without telling the solver that every allowed input is UNSAT. Supplied values are input data; finding those values is not part of the static task. N is the complete encoded length of the formula, supplied values, and any metadata.

At each fixed r, a different fixed level-specific solver is permitted. An assertion about all growing r must retain uniformity and one polynomial bound. Choosing a separate hardcoded program for each individual input is not the fastest-uniform-algorithm question.

### Results obtained

PROVED/EXACT:

1. Boolean one-unknown UNSAT has exactly two minimal obstruction shapes; its minimum source core has size at most two.
2. Boolean two-unknown UNSAT has five core shapes, twelve labeled minimal cores, and minimum source-core size at most four.
3. For these Boolean levels, the minimum number of binary-resolution inferences is exactly core size minus one, after residual normalization.
4. For the actual strict symmetric C5 relation, the worst-case minimum core sizes are H_0=1, H_1=2, H_2=4.
5. One globally UNSAT strict-C5 formula with seven variables and nine clauses realizes the exact independent profile 1,2,4, starting from a complete assignment violating only one clause.
6. Source-core cardinality has a polynomial ceiling in r for a fixed finite template of fixed arity. Thus the initial doubling cannot be extrapolated into an exponential source-core lower bound.
7. A stated quasilinear local, both-label-preserving SAT compression into explicit residuals with sufficiently few choice bits contradicts known simultaneous time-space lower bounds.

COMPUTATIONAL:

The finite strict-C5 support closures contain twelve one-variable relations and 157 two-variable relations. They require four and eight fixed bits, respectively, under an exact source-free contextual-interface contract. The scalar decision output is a separate one-bit contract.

OPEN:

An unrestricted lower bound on the cost of acquiring or establishing the requisite incompatibility at growing levels; a universal transformation of an arbitrary polynomial solver into an already forbidden simultaneous region.

## 2. Four measures that answer different parts of the question

For each source constraint C, let

\[
B_\rho(C)=\{a\in D^U:C(\rho\cup a)=0\}.
\]

Then

\[
I_r\text{ is UNSAT}
\iff
\bigcup_{C\in F}B_\rho(C)=D^U.
\tag{2}
\]

Define the minimum source-core size

\[
\mu_r(F,\rho)=
\min\{|J|:J\subseteq F,\ \bigcup_{C\in J}B_\rho(C)=D^U\}.
\tag{3}
\]

This is the fewest original constraints sufficient to refute every completion, conditional on the supplied values. It identifies a shortest source-evidence route without prescribing how it is discovered. For Boolean CNF, the blocking sets are subcubes; the cover interpretation is standard in the minimal-unsatisfiability literature [1].

For a fixed template Gamma, define H_r(Gamma) as the supremum of mu_r(F,rho) over its permitted UNSAT fresh residual instances with exactly r unknowns. The source formula and the supplied values may vary across this class.

The complete residual support is

\[
S_r(F,\rho)=D^U\setminus\bigcup_{C\in F}B_\rho(C).
\tag{4}
\]

An exact reusable support representation is stronger than the decision whether S_r is empty. Its required number of states depends on the permitted future contexts.

The minimum input-observation certificate is another quantity. For a valid input class X_r and an UNSAT input I, it is the minimum number of raw input positions whose values agree only with UNSAT members of X_r. Equivalently, the observed positions must hit the difference set between I and every permitted SAT alternative. This is ordinary certificate complexity [2]. It counts authenticated observations, not reasoning steps after those observations.

Finally, the attainable resource set consists of simultaneous bounds

\[
(T_A(N,r),S_A(N,r),CM_A(N,r))
\]

for one fixed correct solver A. Componentwise minima achieved by different solvers need not be simultaneously achievable. A semantic certificate size, proof length, observation count, and this resource frontier are related objects, not interchangeable numbers.

For r=1 and r=2, the following derivations characterize all shortest source obstructions, not merely one proposed procedure.

## 3. One Boolean unknown: a complete disjunction

Substitute the supplied values, discard true clauses, delete false fixed literals, remove repeated literals, and discard tautologies. This describes a mathematical residual; raw-source normalization is charged separately.

With only x unknown, the nontrivial clause types are

\[
\bot,\qquad x,\qquad\neg x.
\]

Let E,P,M denote the presence of those types. Then

\[
\boxed{\operatorname{UNSAT}=E\lor(P\land M).}
\tag{5}
\]

There are exactly two minimal source-evidence routes:

1. A clause already false under the supplied values, regardless of x.
2. One active clause forcing x=1 and another active clause forcing x=0.

Here active means that all fixed literals in the original clause are false. Thus

\[
\mu_1\le2,
\]

with equality precisely when there is no empty residual clause and both opposite units are necessary.

The full satisfying support can be empty, {0}, {1}, or {0,1}. An exact contextual interface therefore has four possible states and needs two fixed bits. Returning UNSAT alone does not require emitting that interface.

## 4. Two Boolean unknowns: joint compatibility and all minimal routes

The nontrivial residual types are

\[
\bot;\quad x,\neg x,y,\neg y;\quad
x\vee y,\ x\vee\neg y,\ \neg x\vee y,\ \neg x\vee\neg y.
\]

A unit blocks an edge of the four-assignment square. A binary clause blocks one point. An empty clause blocks the whole square.

Up to negating or renaming variables, every minimal UNSAT core has one of the following shapes:

| Shape | Representative | Source core size |
|---|---|---:|
| Empty clause | {bottom} | 1 |
| Opposite units | {x, not x} | 2 |
| Two compatible units and one point blocker | {x, y, not x OR not y} | 3 |
| One unit and two point blockers | {x, not x OR y, not x OR not y} | 3 |
| All four point blockers | All four binary clause types | 4 |

Proof of completeness: exclude empty clauses and opposite units. The remaining units fix t distinct variables, where t is zero, one, or two. They leave respectively four, two, or one assignments. Each binary clause blocks one point, so those surviving points need respectively four, two, or one binary blockers. Additional clauses are redundant in a minimal core. QED.

An exact disjunctive characterization makes the boundary conditions explicit. Let U_xb mean a unit forcing x=b, and U_yb a unit forcing y=b. Let Q_bc be the binary clause false only at (x,y)=(b,c). Then UNSAT is the OR of:

\[
E;
\quad U_{x0}U_{x1};
\quad U_{y0}U_{y1};
\tag{6}
\]

\[
\bigvee_b U_{xb}Q_{b0}Q_{b1};
\quad
\bigvee_c U_{yc}Q_{0c}Q_{1c};
\tag{7}
\]

\[
\bigvee_{b,c}U_{xb}U_{yc}Q_{bc};
\quad Q_{00}Q_{01}Q_{10}Q_{11}.
\tag{8}
\]

Products in (6)-(8) mean logical AND of presence facts. These are twelve labeled minimal cores: one singleton, two pairs, eight triples, and one quadruple.

The full support has sixteen possible states, so four fixed bits suffice and are necessary for a source-free exact interface handling all pin contexts. This is not a four-bit lower bound on every offline solver's workspace.

### Exact shortest binary-resolution proof

For r<=2, the minimum number g of binary-resolution inferences from the normalized input clauses is

\[
\boxed{g=\mu_r-1.}
\tag{9}
\]

The listed cores have refutations using respectively zero, one, two, or three inferences. For the lower bound, take the ancestor DAG of the final empty clause. If it has g binary inference vertices and b distinct source leaves, its underlying connected graph has at least b+g-1 edges and at most 2g premise edges. Thus b<=g+1. The used source leaves must be UNSAT, so b>=mu_r. Hence g>=mu_r-1.

This is an exact proof-path characterization in binary resolution, including shared DAG proofs. It is not a lower bound on arbitrary machine instructions, nor does it include finding and normalizing the source clauses.

## 5. The actual strict symmetric T5 relation

Use the fixed relation C on D={0,1,2,3,4} whose permitted unordered triples are

\[
012,\quad123,\quad234,\quad340,\quad401.
\tag{10}
\]

All permutations of these triples are accepted. Each source clause has three distinct variable names. This is the symmetric relation in the project's current exhaustive handoff [3]. The ordered tournament relation R in other reports is distinct.

Supplied values may repeat across different fixed names. If that makes a constraint false regardless of its remaining unknowns, it supplies an immediate one-row obstruction.

### One unknown

For fixed a,b, let

\[
U(a,b)=\{x:C(x,a,b)\}.
\]

The nonempty possibilities are five singletons and five doubletons:

\[
\{0,2\},\{0,3\},\{1,3\},\{1,4\},\{2,4\}.
\tag{11}
\]

Call this ten-set family H. The doubletons form a five-cycle. A pairwise-intersecting collection of its edges has a common vertex, because a collection of pairwise-intersecting graph edges without a common vertex would contain a triangle. A singleton in the collection also forces a common point.

Consequently H is Helly-2: every empty intersection of its members contains two disjoint members. Thus a one-unknown UNSAT residual has a false constant row, an empty unary row, or two disjoint unary supports.

\[
\boxed{H_1(C_5)=2.}
\tag{12}
\]

This one-unknown result was already present in the recent project discussion. The following two-unknown theorem extends the characterization.

### Two unknowns

Each residual row is constant, unary on x, unary on y, or

\[
M_a=\{(x,y):C(x,y,a)\}.
\]

Let S_x and S_y be the intersections of the unary supports, and J the fixed values appearing in binary rows. Absent a false constant row, the exact support is

\[
\boxed{
S=(S_x\times S_y)\cap\bigcap_{a\in J}M_a.
}
\tag{13}
\]

Nonempty separate unary supports are insufficient; their allowed pairs must meet the binary relation.

### The sharp four-row theorem

Every two-unknown UNSAT residual has an UNSAT source subcollection of at most four rows.

Proof. Empty constant or unary rows settle the one-row case. If either collection of unary rows has empty intersection, Helly-2 supplies a two-row core. Assume both unary intersections are nonempty.

There are no contradictions without binary rows in this remaining case. If two distinct binary relations M_a,M_b occur, their intersection is either empty or exactly two reversed pairs (u,v),(v,u). Indeed the unary table shows that two distinct fixed values can both complete a given pair only when they are its unique allowed doubleton. An empty intersection gives a two-row core. Otherwise select one further row rejecting each of the two candidate pairs. At most four rows suffice.

Suppose just one distinct binary relation M_a occurs. Every nonempty unary intersection is D, a doubleton represented by one row, or a singleton represented by at most two rows.

If S_x=D or a doubleton, combine zero or one x-row with at most two y-rows and the binary row. At most four suffice.

If S_x={p}, take at most two x-rows forcing p. For p=a, M_a rejects every pair already. For p!=a, its possible y-neighbors are U(p,a), a member of H. Its intersection with all y-unary supports is empty. Helly-2 gives either two contradictory y-rows, or one y-row disjoint from U(p,a). In the latter case the two x-rows, binary row, and that y-row suffice. QED.

The next example proves sharpness:

\[
\boxed{H_2(C_5)=4.}
\tag{14}
\]

## 6. One globally UNSAT source with independent profile 1,2,4

Introduce anchors a_0,...,a_4 and impose

\[
C(a_i,a_{i+1},a_{i+2}),\qquad i=0,\ldots,4,
\tag{15}
\]

with subscripts modulo five. Add four rows:

\[
\begin{aligned}
A&=C(x,a_3,a_4),\\
B&=C(x,a_1,a_2),\\
D&=C(x,y,a_1),\\
E&=C(x,y,a_4).
\end{aligned}
\tag{16}
\]

This is a seven-variable, nine-row strict source.

Every pair of anchor names occurs in an anchor row, so a satisfying anchor assignment uses all five distinct values. The five allowed triple complements are the five edges of a cycle. The anchor assignment must therefore be one of its ten rotations or reflections. Since those permutations preserve C, checking the four remaining rows in the identity anchor frame is sufficient for global UNSAT.

Use the reference assignment

\[
(a_0,a_1,a_2,a_3,a_4,x,y)=(0,1,2,3,4,2,3).
\tag{17}
\]

Only B is false.

**Independent level zero.** All values are supplied. B alone certifies failure, so mu_0=1.

**Independent level one.** Remove only x's value; retain y=3 and a_i=i. Then

\[
B:\ x\in\{0,3\},
\qquad
D:\ x\in\{2\}.
\tag{18}
\]

Every single row has an extension but these two do not. Thus mu_1=2.

**Independent level two.** Remove x and y's values; retain a_i=i. Then

\[
A:\ x\in\{0,2\},\qquad B:\ x\in\{0,3\},
\]

so A and B together force x=0. Meanwhile,

\[
D\cap E=\{(2,3),(3,2)\}.
\tag{19}
\]

The requirements conflict. Moreover every row is indispensable:

| Deleted row | Satisfying pair for the other three |
|---|---|
| A | (3,2) |
| B | (2,3) |
| D | (0,1) |
| E | (0,2) |

Thus mu_2=4. The contradiction holds in every anchor frame, proving global UNSAT of the original unpinned source as well.

This exactly realizes the user's desired comparison: separate fresh inputs reveal different minimum obstruction structures, without transferring any computation between the levels.

Under the handoff's strict formula encoding, n=7,m=9,w=3 gives formula length 96 bits. If the fresh instance appends one three-bit value-or-unknown slot for each variable, all three levels have complete length 117 bits. Codes 0,...,4 denote supplied values and code 5 means unknown; other codes are invalid. This is a declared extension encoding, not a claim that the earlier source format already included pins.

## 7. Exact contextual information at the first levels

For Boolean CNF with r<=2, all support subsets are realizable by clauses excluding individual assignments. For strict C5, the available supports are more restricted.

The one-unknown C5 intersection closure consists of D, empty, five singletons, and five doubletons: twelve relations.

The complete two-unknown closure of twenty-five nonempty atomic relations, ten unary relations on each variable and five binary relations, has 157 elements. This finite exhaustive calculation has cardinality distribution

\[
\{0:1,\ 1:25,\ 2:60,\ 3:10,\ 4:35,\ 5:10,\ 6:5,\ 10:10,\ 25:1\}.
\]

| Template and level | Candidate tuples | Distinct supports | Fixed bits for exact contextual summary | Maximum minimum source core |
|---|---:|---:|---:|---:|
| Boolean, r=1 | 2 | 4 | 2 | 2 |
| Boolean, r=2 | 4 | 16 | 4 | 4 |
| Strict C5, r=1 | 5 | 12 | 4 | 2 |
| Strict C5, r=2 | 25 | 157 | 8 | 4 |

The summary lower bounds use an explicit contract: the identities and order of the unknown slots, domain labels, and decoder are fixed; after the source is unavailable, the summary must answer every compatible pin-context query. Distinct supports differ on a tuple; a context forcing that tuple distinguishes them. C5 can force each coordinate to a singleton using an ordinary row with fixed values.

The table does not claim every offline decision algorithm must materialize these summaries. Its output remains one bit. Source positions, indices, parsing, and acquisition are additional costs.

## 8. Acquisition can exceed the shortest certificate

In a normalized-clause-record query model with m records, the worst-case deterministic acquisition cost is m reads for both Boolean levels. One scan is sufficient, and a last-record adversary supplies a matching lower bound.

For one unknown, reveal a unit x and then harmless true records, withholding a possible unit not-x until the last unread position. Before that last read, both a SAT completion of the input records and an UNSAT completion remain possible. The all-zero reference assignment violates just the first x in both alternatives, so this control can preserve the near-assignment premise.

For two unknowns, the fourth binary point blocker can be hidden in the last unread position. Reveal the blocker of the reference assignment only once and repeat other harmless-to-reference records as needed; the reference still violates only one row.

These are both-label adversaries for fresh instances, not arguments about carried history. They demonstrate that a two- or four-row certificate need not be found in two or four input reads.

The exact m-record bound is not automatically an exact N-bit or sole-tape time bound. A raw clause must be parsed and its supplied-value lookups paid. Giving the failed clause's position, a verified index, or a normalized record array changes the input and must be stated.

## 9. Simultaneous attainable points for the explicit fixed-template levels

Upper bounds are used here only to delimit what the ideal resource frontier can exclude. They are not a proposal to develop a SAT solver.

Let unknown domains be D_1,...,D_r, and define

\[
M=\prod_i|D_i|,\qquad
h=\log_2M.
\tag{20}
\]

This is a nominal number of choice bits, not the Shannon entropy of the decision. If one completion can be checked in time V and space W, repeated checking witnesses

\[
T\le M V,\qquad S_{\rm aux}\le W+O(h+\text{identifier bookkeeping}).
\tag{21}
\]

No lower bound requiring enumeration is inferred.

For an explicit fixed-arity, fixed finite template with supplied values in a canonical read-only addressable array, checking uses N times a polylogarithmic factor. If h=O(log N), unknown identifiers and values occupy polylogarithmic workspace. Therefore an attainable simultaneous point is

\[
T\le 2^hN\operatorname{polylog}N,\qquad
S_{\rm aux}=\operatorname{polylog}N.
\tag{22}
\]

For one or two fixed-domain unknowns, h=O(1). The same execution has

\[
T=\widetilde O(N),\quad S_{\rm aux}=\operatorname{polylog}N,\quad
CM_{\rm aux}=\widetilde O(N).
\tag{23}
\]

If that implementation retains all N input bits and charges their residence, its input-inclusive storage is O(N) and cumulative residence is

\[
CM_{\rm phys}=\widetilde O(N^2).
\tag{24}
\]

These statements concern the specified random-access model and input layout. They are not sole-tape motion bounds. An unsorted supplied-value list may require normalization or repeated scans. Translation to a physical single-tape machine must pay its simulation overhead.

There is no conflict between (23) and SAT forbidden regions: the explicit restricted classes have not been shown to preserve unrestricted SAT hardness under the required low-resource reductions.

## 10. Exact connection to the simultaneous forbidden regions

The applicable source theorems concern deterministic algorithms whose time and auxiliary workspace bounds hold simultaneously. Input is read-only and excluded from auxiliary workspace. FLMV excludes near-linear time with polynomially sublinear workspace [4]. Williams's corrected manuscript supplies the small-workspace endpoint 2cos(pi/7), the Table I pair (1.24,0.666), and the conservative time-space product region a+b<phi [5,6]. Transfers use strict exponent slack.

The older claimed general product exponent near 1.801 was withdrawn. The separate subpolynomial-workspace time endpoint remains valid. No withdrawn claim is used.

### Static restriction-compression exclusion

Suppose a uniform, both-label-preserving reduction takes an eligible n-bit SAT source to the explicit residual class of (22), with:

1. Complete target length N=n^{1+o(1)}.
2. Polylogarithmic time and logarithmic workspace to generate any requested output bit.
3. Target length and necessary header parameters computable in n^{1+o(1)} time and O(log n) workspace.
4. Cheap target supplied-value access and cheap fixed-template evaluation.
5. Choice weight

\[
h\le c\log_2N+o(\log N).
\tag{25}
\]

Then virtual input simulation and (22) give one SAT algorithm with

\[
T_{\rm SAT}\le n^{1+c+o(1)},\qquad
S_{\rm SAT}=n^{o(1)}.
\tag{26}
\]

Consequently such a reduction cannot satisfy

\[
\boxed{c<2\cos(\pi/7)-1=0.8019377358\ldots.}
\tag{27}
\]

Proof. Initialize the target length and headers using the stated near-linear-time, logarithmic-space procedure. Generate target bits on demand; do not materialize the target. Per-request polylogarithmic overhead and logarithmic scratch preserve the exponents in (26). Choose a fixed time exponent strictly between 1+c and 2cos(pi/7). The resulting SAT algorithm violates the published small-workspace exclusion. QED.

Using only the FLMV endpoint gives the weaker sufficient threshold c<phi-1.

This is a proved exclusion of a specified cheap universal reduction, not a lower bound on the easy residual class. Arbitrary supplied values preserve UNSAT but may destroy SAT. Therefore an erasure snapshot by itself does not supply the both-label-preserving reduction in this theorem. This qualification does not invalidate the independent per-level study.

### Auxiliary cumulative-memory transfer

Under the declared bounded-growth model, initially usable auxiliary state is at most polylog(N), all preprocessing is included in the charged interval, at least one bit is charged per step, and only polylog(N) new usable bits are permitted per step. Then

\[
T\le CM_{\rm aux},\qquad
S_{\max}\le\widetilde O(1+\sqrt{CM_{\rm aux}}).
\tag{28}
\]

The peak bound is an area argument for building memory. It is not the false equality CM=T*S_max. A time-space exclusion (a_0,b_0) therefore excludes a CM upper exponent gamma satisfying

\[
\gamma<\min(a_0,2b_0).
\tag{29}
\]

The published pair (1.24,0.666) gives gamma<1.24 for the compact target under the established local-reduction and machine-simulation hypotheses [5,7]. This is not an input-inclusive physical-CM theorem. Initially providing N writable auxiliary bits violates the small-initial-state premise.

## 11. Why compact T_q already has one unknown

The actual compact target Q in the recent forbidden-region notes has input (B,H), where H is a circuit specifying the base tournament. A fixed interpreter completes it to a regular tournament on q=2B+1 values. Its question is

\[
\exists x<q:\ R(x,0,1)\land R(2B,x,B).
\tag{30}
\]

R is the ordered one-win/one-loss relation, with equal values rejected. H is input-dependent; this is not fixed symmetric C5.

The inspected compiler from a k-variable source formula uses

\[
B=2^k+2,\qquad q=2^{k+1}+5,
\]

\[
H_F(i,j)=
\neg([i=0]\land[j\ge2]\land
F((j-2)\bmod2^k)).
\tag{31}
\]

Its target has one unknown name, but log_2(q)=Theta(k) choice bits. Candidate labels represent entire Boolean assignments. The circuit has O(k+m) gates and the complete target description is O(n log n) for the declared source encoding. Requested output bits are generated locally with the stated charged resources [7].

Thus a one-unknown count is not a complexity parameter by itself. Domain representation and the cost of evaluating the input relation matter. A polynomial(N,log q) solver for this compact language would imply P=NP; it would not automatically violate the fixed-polynomial resource regions. A near-linear-time, subpolynomial-workspace solver would violate the transferred region.

Even fixed q does not make an arbitrary supplied circuit free to evaluate. The fixed-template scan bounds require fixed, cheaply evaluated relations.

## 12. Why the first doubling does not give a separation

For every finite-domain residual,

\[
\mu_r\le\min(m,|D|^r),
\tag{32}
\]

by selecting one violated source row for each candidate tuple.

Fixed arity gives a stronger structural ceiling. In Boolean k-CNF,

\[
\mu_r\le
\min\left(m,2^r,\sum_{j=0}^{\min(k,r)}2^j\binom rj\right).
\tag{33}
\]

A minimal core has no duplicate normalized clause type. For fixed k this is polynomial in r.

For strict C5 the possible nontrivial residual row types number at most

\[
1+10r+5\binom r2+\binom r3.
\]

The terms are an empty obstruction, ten unary types per unknown, five binary types per pair, and one symmetric ternary type per triple. Therefore

\[
\boxed{
\mu_r\le\min\left(m,5^r,
1+10r+5\binom r2+\binom r3\right)=O(r^3).
}
\tag{34}
\]

This bounds the number of source constraints needed, not the computation needed to prove their joint inconsistency. A polynomial-size subformula can itself be difficult to refute. The whole source is already an m-row UNSAT subformula whenever the input is UNSAT.

For growing r, the unresolved quantity must include acquisition, proof evaluation, or another model-faithful processing cost. Counting source rows alone cannot establish superpolynomial computation. The results 1,2,4 are exact initial levels and a useful calibration of the desired analysis; they do not prove further doubling.

## 13. Validation, review, and source recovery

The Boolean standalone audit checked all 8 subsets of the three one-variable clause types and all 512 subsets of the nine two-variable clause types. It found respectively 5 and 417 UNSAT sets. All direct truth evaluations agreed with the presence formulas and core classifications. The two-variable minimal-core counts by size were 1,2,8,1.

The C5 template audit enumerated minimal empty intersections of 25 nonempty atomic residual relations through size 6 and obtained counts 75,230,10,0,0 at sizes 2,3,4,5,6. It also computed the complete 157-relation closure. Those earlier inline exact computations were preserved, not rerun merely to change record format.

The new global C5 stage examined all 78,125 assignments to the seven-variable nine-row source, found no models, checked all 10 anchor frames, the unique false reference row, the exact cores 1,2,4, and the four deletion witnesses. The companion standalone script can reproduce both template and global stages.

The Boolean collaborator independently read the complete C5 theorem, code, and both raw records and passed the symbolic proof, source construction, closure procedure, and scope. The C5 collaborator reviewed this report's logical sections and the 117-bit encoding. The resource collaborator reviewed its transfer sections and requested an explicit target-length/header initialization hypothesis, which has been added. The coordinator reviewed the proofs and actual compact-target compiler and additional-region note. Internal multi-agent review is not external peer review or formal proof-kernel verification.

The current AGENTS, CODEX, research skill, active directive, ownership directive, strict source definition, six role handoffs, prior local erasure reports, and materially relevant cross-chat notes were recovered. Starting main head was bf8e52241a80da97365fe86c6985c3ab15b991d9. The first 100 branch names were inventoried without claiming complete branch coverage, and the three issue324 entries since20:00 UTC were recovered. No complete checkout was present, so the repository preflight was not run. No retired proof tracker or owned peer manuscript was edited. No automation settings were changed.

Fresh primary literature retrieval covered minimal UNSAT cube covers, certificate versus query complexity, FLMV, Williams's corrected resource bounds, and the recent CSP non-redundancy streaming theorem. The latter has shift/model restrictions and is not imported as an unrestricted C5 RAM lower bound [8].

Fresh official-organization code searches for "minimal unsatisfiable" covered anthropics, openai, xai-org, google, google-research, and google-deepmind. OpenAI returned a rate-limit error, then no hits on one retry. Google returned OR-Tools troubleshooting documentation at 4782dbd0aa85621c8115cf33de1574a2e6757004, which was read. It discusses practical sufficient assumptions, not the present minimum-core theorem; no code or lower-bound claim was imported. Other searches returned no hits. Corporate profiles and Google's official organization policy were checked; xai-org currently links to x.ai under a changed display name.

| Gate | Status |
|---|---|
| Fresh independent starts | PASS: no cross-level retained state or summed execution costs |
| Both decision labels | PASS in stated problem classes and reduction hypotheses |
| Source definitions and encoding | PASS: symmetric C5, ordered R, compact Q, and Boolean CNF separated |
| Sharing / DISJ sanity | PASS in scope: one clause may reject many candidates; no forced enumeration |
| Simultaneous resource bounds | PASS as declared-model upper points and conditional local transfers |
| Deterministic configurations | No lower bound inferred from configuration counts |
| Relativization and other barriers | No claim of a new unrestricted barrier-crossing argument |
| Native tape / formal kernel validation | Not executed |
| Unrestricted superpolynomial acquisition or inference | OPEN |

## 14. Receiving dependency

Continue the static hierarchy at r=3, where genuine ternary residual constraints first remain, and distinguish source-core growth from the effort to establish incompatibility. A useful result should characterize minimal obstruction shapes or a cost-sound inference measure, with the model and all alternatives explicit.

The separate resource question is whether a hypothetical general polynomial solver can be transformed into a point inside an established forbidden region. The static compression theorem identifies one precise prohibited shortcut; it does not supply that universal transformation.

## References

1. Oliver Kullmann and Xishun Zhao. Parameters for minimal unsatisfiability: Smarandache primitive numbers and full clauses. arXiv:1505.02318v2. https://arxiv.org/pdf/1505.02318 . Used only for the established cube-cover viewpoint.
2. Harry Buhrman and Ronald de Wolf. Complexity measures and decision tree complexity: a survey. Theoretical Computer Science 288, 2002. Author copy https://homepages.cwi.nl/~rdewolf/publ/other/tcs.pdf . Sections 3.1 and 4.1 supply query/certificate definitions.
3. Project. T5 Resource Lower Bounds Exhaustive Handoff, 21 November 2026. https://github.com/j15marti/pnp/blob/bf8e52241a80da97365fe86c6985c3ab15b991d9/research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md . Definition blob a886f3387a8676b9cc86afbf3bebf22630109d49.
4. Lance Fortnow, Richard Lipton, Dieter van Melkebeek, Anastasios Viglas. Time-Space Lower Bounds for Satisfiability. JACM 52(6), 2005. https://lance.fortnow.com/papers/files/tst.pdf .
5. Ryan Williams. Alternation-Trading Proofs, Linear Programming, and Lower Bounds. Corrected author manuscript. https://people.csail.mit.edu/rrw/automated-lbs.pdf . Table I, Theorem 4.11, and correction footnote 9.
6. Samuel Buss and Ryan Williams. Limits on Alternation-Trading Proofs for Time-Space Lower Bounds. CCC 2012. https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/samCCC-cr.pdf .
7. Actual inspected cross-chat source notes: T_Odd_FLMV_Transfer_2026-11-22.md; T_q_FLMV_and_CM_Forbidden_Regions_2026-11-22.md; Additional_T5_Tq_Forbidden_Regions_2026-11-22.md; PNP_CM_Contraction_Proof_Attempt_2026-11-22.md. Exact paths and SHA256 pins are in the companion Static_Restriction_Resource_Transfer.md. The reverse-core note T5_Reverse_Unfixing_Core_and_Acquisition_2026-11-22.md uses ordered R for its particular mu_r=r+1 chain, not symmetric C5.
8. Amatya Sharma and Santhoshini Velusamy. Characterizing Streaming Decidability of CSPs via Non-Redundancy. ESA 2026. https://drops.dagstuhl.de/storage/00lipics/lipics-vol388-esa2026/html/LIPIcs.ESA.2026.131/LIPIcs.ESA.2026.131.html . Single-pass and language assumptions are not removed.

Companion evidence: Boolean_One_Two_Unknown_Characterization.md; T5_One_Two_Unknown_Core_Theorem.md; T5_Independent_Review_by_Boolean_Agent.md; Static_Restriction_Resource_Transfer.md; boolean_static_audit.py and its raw JSON; t5_one_two_unknown_audit.py and its two raw JSON records.
