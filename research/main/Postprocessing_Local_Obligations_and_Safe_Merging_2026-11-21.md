# What survives preprocessing: local obligations and safe merging

**Research date:** 21 November 2026, America/Los_Angeles.  
**Primary result:** DYNAMIC-LOCAL-VIEW-DICHOTOMY1.  
**Status:** PROVED/EXACT implications with explicitly stated hypotheses; the all-input hypotheses needed for either P=NP or P!=NP remain OPEN.  
**Review:** Two collaborators independently checked the label-merging theorem and its UNSAT-only range refinement. The reachable-state certificate and physical-cost extension received separate mathematical checks. A third collaborator constructed and exhaustively audited the parity-cycle control. These are same-conversation internal reviews, not external peer review or proof-assistant verification.

## 1. The strengthened target

The question is whether a correct SAT algorithm must perform another local computation after paying for preprocessing, relocation, and a shared representation. There is no unconditional positive suffix bound: the paid prefix can already have computed and placed the answer. The current transport/prepayment theorem correctly permits its residual obligation to vanish.

This continuation makes two implications explicit.

First, at an actual machine checkpoint, reachable opposite-answer configurations define a family of differing physical cells. Correctness forces the real suffix to read a hitting set for that family. A fractional capacity constraint credits sharing, a first-clearing rule permits disjoint dynamic phases, and origin-anchored geometry yields a separate physical cumulative-cost bound.

Second, disappearance of local ambiguity has a constructive consequence when it happens uniformly in a sufficiently small family of summaries. A polynomial-time label procedure whose equal labels never mix SAT and UNSAT yields a polynomial SAT algorithm if the number of labels attained by **UNSAT formulas alone** is polynomially bounded. No efficient decoder from labels to answers is required. Exact self-reduction and merging supply the decision procedure.

The first implication does not prove that a large residual family survives every cheap preprocessor. The second does not construct the required label procedure. They specify the missing structural theorem in both directions.

### Relation to existing work

The underlying hitting/packing and self-reduction arguments are established techniques. Fractional certificate complexity is described explicitly in Ben-David, Hatami, and Tal, Section 2.4 [1]. Sparse-hard-set pruning supplies the literature context for the constructive implication [2]. No historical novelty is claimed.

Repository recovery found earlier source-transversal and cache results: PREPROCESSING-CACHE-FIREWALL173 and ARC-CHECKPOINT-RESIDUAL148 already exclude recharging original source differences after they have been observed [3,4]. The current Redteam report gives a reachable-configuration criterion and disjoint-block examples [5]. The current Synthesis report prices normalization overhead [6]. Those are predecessors, not newly discovered results here.

The present integration adds the general weighted snapshot formulation, explicit disjoint first-clearing phases, a finite-cap ceiling for those snapshot certificates, and the uniform label-merging implication with the weaker UNSAT-only range hypothesis. It replaces an unspecified demand for further work with a defined quantity and a constructive alternative.

## 2. Fixed machine, encoded source, and costs

For the local lower statements, fix one total correct deterministic Boolean SAT decider A. The machine has one physical writable tape indexed by integers, one head, a fixed finite alphabet Gamma, and a fixed finite control. One transition reads the scanned symbol, writes, moves by at most one cell, and changes state. The input initially occupies cells 0 through N-1; the head starts at 0. Fixed initialization markers can be absorbed into a constant adjustment or the encoding.

Canonical answer and terminator occupy a fixed finite set O near the origin. The output is interpreted only under the required termination convention. All retained input, relocated copies, caches, addresses, scratch data, and output are part of the same complete configuration C_t. There is no free source oracle, independent input head, or unrecorded clock.

Let s_t be the physical origin-anchored span after transition t, in the prior report's bit-scaled convention: one plus the length of the smallest interval containing the origin, head, and all nonblank cells, multiplied by a fixed alphabet factor. Define

\[
T_A(F),\qquad
CM_{\mathrm{phys}}^{>\tau}=\sum_{t=\tau+1}^{T_A(F)}s_t,
\qquad
CM_{\min}^{>\tau}=\sum_{t=\tau+1}^{T_A(F)}K_{\mathcal U}(C_t\mid A).
\]

Only A is free in the last conditional description. The input, transition index, and checkpoint are not free. The earlier faithful encoding inequality K(C_t|A)<=lambda_A s_t remains available. A physical lower bound does not imply a minimum-description lower bound by reversing that inequality.

Every lower-bound checkpoint below is an actual point on the chosen execution. It need not be efficiently selected for a purely mathematical lower-bound statement. By contrast, the constructive label theorem requires a uniform polynomial-time procedure for acquiring its summaries.

Four falsifiers guide this run:

1. A supposed opposite-answer checkpoint is unreachable, or its cached state/output differs in an ignored field.
2. One retained summary distinguishes many opponents, but those opponents are charged as independent operations.
3. Successive obligations count the same execution transitions again, or a wrapper has already paid the lower demand during reconstruction.
4. A homogeneous label family is treated as cheaply acquired without a uniform algorithm, or its range bound ignores varying residual lengths.

## 3. Reachable opposite-answer configurations

Let C=C_tau(F) be an actual checkpoint on an UNSAT input F. Choose a finite family C^(1),...,C^(m) of configurations of the same machine A such that each configuration:

- is actually reachable on a valid SAT input;
- has the same control state and head position as C;
- agrees with C on all canonical output cells O.

Different checkpoint times are allowed because time is not an external input to continuation. The family can be a proved subset of all eligible opponents. The theorem does not give the solver this family or require it to enumerate it.

Define snapshot difference sets

\[
D_j=\{i:\operatorname{tape}(C)_i\ne\operatorname{tape}(C^{(j)})_i\}.
\tag{1}
\]

Each set is finite and nonempty. An empty set, together with equal control and head, would give identical complete configurations with opposite required answers. Determinism forbids that. If there are no eligible opponents, all the certificate values below are defined to be zero.

This construction preserves every paid cache. A difference in an answer flag is a real difference in (1); it cannot be omitted because it makes an intended lower bound smaller.

## 4. A suffix must hit every difference set

**Theorem 1 (actual suffix observation).** Let R be the set of cell coordinates scanned by the actual execution after tau and through its final transition. Then

\[
R\cap D_j\ne\varnothing\qquad(1\le j\le m).
\tag{2}
\]

**Proof.** Fix j and suppose no coordinate in D_j is scanned. Couple the actual continuation with the continuation from C^(j). They begin with equal control and head. Every scanned cell either has equal snapshot contents or was already overwritten identically during the coupled computation. Therefore their next writes, moves, and states agree. A first visit to a differing cell would read it before writing, and is excluded by the supposition. Their output cells begin equal and receive identical writes. When the actual run halts, the opponent run halts with the same output, contrary to correctness. This proves (2). □

Let hit(D) denote the minimum size of a set meeting every D_j. Each transition scans only one cell, so

\[
\boxed{T_A(F)-\tau\ge |R|\ge\operatorname{hit}(D).}
\tag{3}
\]

No prescribed formula-processing order, proof system, or computation graph is imposed. This is a lower bound on the actual continuation, conditional on the proved reachable opponents.

## 5. Fractional charges preserve sharing

Choose weights w_j>=0 satisfying

\[
\sum_{j:i\in D_j}w_j\le1
\quad\text{for every coordinate }i.
\tag{4}
\]

Then

\[
\sum_jw_j
\le\sum_{i\in R}\sum_{j:i\in D_j}w_j
\le |R|
\le T_A(F)-\tau.
\tag{5}
\]

The maximum feasible total weight is the fractional packing number nu*(D), equal to the fractional hitting value by finite linear-programming duality. This is standard fractional-certificate reasoning [1]. Our direct inequality (5) does not require the algorithm to solve that linear program.

Three cases show what the capacity condition measures.

| Difference family | Valid conclusion |
|---|---|
| m pairwise disjoint nonempty sets | Weight one on each forces at least m scans. |
| Every set contains one shared cache address c | The packing is at most one, regardless of the number of opponents. |
| m sets, with each coordinate contained in at most kappa sets | Uniform weight 1/kappa gives at least m/kappa scans. |

If the correct answer is already in the matched control state or committed output, there may be no opposite-answer opponent at all. The corresponding value is zero. These are legitimate outcomes of preprocessing.

### A local potential during one phase

Fix a snapshot family and weights. Let

\[
\Phi(t)=\sum_{j:\ D_j\text{ has not been scanned since the checkpoint}}w_j.
\tag{6}
\]

A scan at i decreases Phi by at most the left side of (4), hence by at most one. Correctness forces Phi to reach zero before termination. This potential is independently defined by the snapshot and the actual subsequent first hits; it is not defined as optimal remaining runtime.

## 6. Tape travel and physical cumulative cost

Let h be the checkpoint head coordinate. Under unit head movement, the scanned positions in a nonempty suffix form an interval [l,r] containing h. The interval must meet every D_j. A walk that starts at h and scans both endpoints needs at least

\[
(r-l)+\min\{h-l,r-h\}
\]

moves before its last required scan. With the declared read-before-move convention, q transitions have only q-1 intervening moves between the first and last scanned positions. Thus

\[
\boxed{
T_A(F)-\tau\ge
1+\min_{\substack{l\le h\le r\\ [l,r]\cap D_j\ne\varnothing\ \forall j}}
\left((r-l)+\min\{h-l,r-h\}\right)
}
\tag{7}
\]

for a nonempty opponent family. A return to the origin is not added unless the machine's final-head convention actually requires it. Equation (7) is an observation-route relaxation, not an upper bound on the computational task.

For physical CM, put c(i)=max(1,|i|). A transition scanning i ends with head at i-1, i, or i+1. The after-state origin-anchored span is therefore at least c(i) in cell units, and at least the same quantity under a bit factor >=1. For more general units retain the explicit fixed conversion factor.

Give the difference sets nonnegative weights v_j satisfying

\[
\sum_{j:i\in D_j}v_j\le c(i).
\tag{8}
\]

Charge only the first scan of each coordinate in the suffix. Different first scans occur at different transitions. Equation (2) gives

\[
\boxed{
CM_{\mathrm{phys}}^{>\tau}
\ge\sum_{i\in R}c(i)
\ge\sum_jv_j.
}
\tag{9}
\]

Because R is an interval, another valid lower bound is the minimum of sum_{i=l}^r c(i) over the hitting intervals in (7). Erasing previously used tape symbols does not invalidate the origin-to-head span charge.

No analogous large CM_min bound follows from coordinate magnitude alone. A remote coordinate can have a short description. The earlier permutation-prefix injection cannot be silently transferred to a new family.

## 7. Successive phases without repeated charges

**Theorem 2 (disjoint clearing phases).** At an actual checkpoint tau_0, prove an opponent family and feasible weights of total W_0. Let sigma_0 be the first actual time by which every snapshot difference set has been scanned. Theorem 1 guarantees sigma_0<=T_A(F), and (5) gives sigma_0-tau_0>=W_0.

Choose the next actual checkpoint tau_1>=sigma_0. Prove a new eligible opponent family there, and repeat. For any finite sequence of such phases,

\[
\boxed{
T_A(F)-\tau_0\ge\sum_jW_j.
}
\tag{10}
\]

**Proof.** Every phase has its own first-hit potential (6). Its drop is bounded by its actual transitions. The intervals (tau_j,sigma_j] are disjoint, so their transition charges can be added. Any gaps are extra actual work. The same argument applies to the physical weights in (8), with their own feasible witnesses. □

The new family at tau_(j+1) is a mathematical obligation that must be proved. It is not automatically supplied by another variable erasure, by the number of residual descriptions, or by the presence of the original source on tape. Previously read information may be encoded in a joint cache that destroys the next proposed alternatives.

The phase families may be analysis objects rather than efficiently discoverable objects. That is permitted for a lower-bound proof. However, if a wrapper is introduced to construct a convenient checkpoint, the resulting demand must exceed the wrapper's acquisition overhead as well as the original proposed cap. The normalization tariff in [6] remains necessary.

## 8. A finite-cap ceiling for a static checkpoint

Suppose the base checkpoint and **every opponent checkpoint used in the certificate** were reached within B transitions, on inputs of length at most N, with N>=1. All initial nonblank cells and all possible writes lie within the enclosing interval

\[
U=[-B,N-1+B],\qquad |U|=N+2B.
\tag{11}
\]

The input marker convention may add a fixed constant. Every D_j is a nonempty subset of U. Consequently

\[
\boxed{
\nu^*(D)\le\operatorname{hit}(D)\le N+2B.
}
\tag{12}
\]

For a direct packing proof, sum the capacity inequalities over U:

\[
\sum_jw_j\le\sum_j|D_j|w_j
=\sum_{i\in U}\sum_{j:i\in D_j}w_j
\le|U|.
\]

A path visiting all of U has O(N+B) length, so the observation-route quantity in (7) also has that ceiling. The weighted physical certificate is at most

\[
\sum_{i\in U}\max(1,|i|)=O((N+B)^2).
\tag{13}
\]

These are ceilings on these **static certificate values**, not upper bounds on remaining SAT computation. Observing all cells does not grant free retention or a free decoder. Nor do the ceilings rule out a cap-dependent contradiction in which a proved residual bound exceeds the remaining slack. They show that exponentially many rivals alone cannot create exponential one-checkpoint observation weight in polynomially many physical cells.

A bound on the base checkpoint alone is insufficient for (11). Opponents with unbounded preprocessing could have arbitrarily distant tape contents. The common reachability cap must be explicit.

## 9. A stronger constructive theorem: only UNSAT labels need a small range

Let F_3 be a fixed explicit encoding of CNF formulas of width at most three, allowing units, binary clauses, the empty clause, and the empty conjunction. Let sat(G) be its satisfiability bit.

Suppose a fixed uniform algorithm h has these properties.

**Acquisition:** h(G) is an explicit string computed in time p(|G|), for one fixed polynomial p. Exact string comparison is charged.

**Sound collisions:** for all valid G,H,

\[
|G|=|H|\ \land\ h(G)=h(H)
\quad\Longrightarrow\quad
\operatorname{sat}(G)=\operatorname{sat}(H).
\tag{14}
\]

**Small UNSAT image:** for fixed integers C>=1,c>=0 and every encoded length s (round any initial polynomial upper bound upward to this form),

\[
\left|\{h(G): |G|=s,\ G\text{ UNSAT}\}\right|
\le q(s):=C(s+1)^c.
\tag{15}
\]

The number of labels attained by SAT formulas need not be polynomial. No decoder from h(G) to sat(G) is assumed. The procedure need not preserve the full assignment relation of G.

**Restriction encoding:** residuals of an N-bit input can be generated in polynomial time and encoded in at most L(N) bits, for a fixed polynomial upper bound L with nonnegative integer coefficients. Keep original variable identifiers. Let n be the number of distinct appearing variables; n<=N, even if the largest encoded identifier is much larger.

**Theorem 3 (UNSAT-image merging).** Under these hypotheses, width-at-most-three SAT is in P, and hence P=NP.

### Algorithm

Fix a valid integer polynomial upper bound

\[
B(N)=\sum_{s=0}^{L(N)}C(s+1)^c.
\tag{16}
\]

List the appearing variables x_1,...,x_n in a fixed order. Maintain a frontier of residual formulas, initially just F.

For i=1,...,n:

1. Replace each retained G by its two restrictions G|_(x_i=0) and G|_(x_i=1). If x_i no longer occurs, both are simply G.
2. For every child H, compute the exact key (|H|,h(H)).
3. Retain one residual for every distinct key.
4. If there are more than B(N) distinct keys, return SAT.

At any stage, a directly satisfied residual can return SAT and a residual with an empty clause can be discarded. These shortcuts are optional. After the n-th level all residuals are Boolean constants; evaluate them directly and return the OR of their values.

### Correctness proof

At every stage before a return, the invariant is

\[
\operatorname{sat}(F)
=\bigvee_{G\text{ retained}}\operatorname{sat}(G).
\tag{17}
\]

Branching preserves (17) because sat(G)=sat(G|_(x_i=0)) OR sat(G|_(x_i=1)). Merging preserves it by (14): replacing several copies of the same decision value with one does not change the disjunction. Logical equivalence of their full functions is unnecessary.

If the frontier has more than B(N) distinct keys, it cannot consist entirely of UNSAT formulas. All UNSAT keys across the permitted residual lengths are counted in (16). At least one retained residual is SAT, so (17) justifies returning SAT. This argument never identifies which label denotes SAT.

If overflow never occurs, at most B(N) representatives survive each level. After n levels every original appearing variable has been assigned in every represented branch, so direct constant evaluation completes the decision. □

### Why this weakens the required hypothesis

It is enough to make the UNSAT image small. The solver can have arbitrarily many different SAT labels globally: reaching too many distinct labels on a frontier is itself a sound SAT certificate under (15).

The valid polynomial bound in (16) must be available as fixed constants in the constructed decider. This is an existential uniform theorem, so constants from a proved bound may be built into one finite program. There is no advice varying with input length. Unlike the stronger all-label range version, this overflow implementation does use a chosen range bound.

The elementary argument is in the family of self-reduction and co-sparse pruning techniques [2]. We do not claim a new general complexity-collapse theorem. Its use here removes an unnecessary demand for a direct decoder or preservation of the entire shared boundary function.

### Full charged polynomial ledger

Let P(N) bound acquisition time p(s) for s<=L(N), let R(N) bound restriction construction, and put D(N)=N+L(N)+P(N)+R(N)+1. Explicit keys have length O(P(N)+log(L(N)+2)). For the contextual keys below, P(N) bounds the entire call on (F,i,G), including paid access to the root F and all framing fields.

At the start of a level there are at most B representatives, hence at most 2B children. Naive pairwise exact key comparisons suffice. A conservative fixed-multitape work bound is

\[
U(N)=O\!\left(N^2+N(B(N)+1)^2D(N)\right).
\tag{18}
\]

This includes parsing, constructing the original variable list, restrictions, label computation, copying, failed duplicate comparisons, and output. Retained formulas and keys occupy polynomial space. No semantic equality oracle or hash-equality assumption is used.

A faithful single-tape simulation can store a fixed number of virtual tapes with marker tracks and sweep the used interval for each virtual transition. Since the virtual computation uses at most O(U) cells, this gives the conservative same-implementation bounds

\[
T_1=O(U^2),\qquad S_1=O(U),\qquad
CM_{\mathrm{phys},1}=O(U^3),\qquad CM_{\min,1}=O(U^3).
\tag{19}
\]

The last inequality uses the explicit configuration-encoding upper bound. The transformation preserves polynomial computability; it does not preserve a previously proposed solver exponent by a constant factor.

### Proper-3-only inputs

If h accepts only clauses of exactly three distinct literals, retain the actual width-at-most-three residuals in the frontier. Compile a copy K(G) into proper 3-CNF solely for label extraction, using a fixed polynomial equisatisfiable compiler. Use (|K(G)|,h(K(G))) as the key and increase L to the polynomial compiled-length bound. Constant true/false residuals can be handled directly. Fresh helper variables are never added to the frontier's branching schedule. This prevents helper recursion from invalidating the n-level argument.

### Decision is the preserved quantity

The algorithm preserves the OR of satisfiability values. It does not preserve model counts, so no polynomial exact-counting consequence is claimed. A SAT overflow does not identify which representative is satisfiable. Polynomial witness search follows by applying the completed decision algorithm through standard variable-by-variable self-reduction; retaining frontier provenance alone does not handle that overflow case.

### A weaker condition tied to one formula's variable removals

Global sparsity across unrelated UNSAT formulas is stronger than the frontier proof needs. Fix the original variable order of each root F. A uniform polynomial-time key procedure may take (F,i,G), where G is a restriction of F after the first i original variables have been assigned. Include any necessary length and framing fields in its explicit key.

Assume equal keys at the same root and level preserve satisfiability for **every** root, including SAT roots. Assume also that, for every UNSAT root F of length N and every level i, the entire level of its restriction tree attains at most B(N) different keys, for one fixed polynomial B. The same branch-and-merge algorithm, with overflow threshold B(N), is polynomial and correct. A deduplicated frontier is a subset of the full restriction level; overflow contradicts the UNSAT-root width bound, so implies SAT. Otherwise polynomial width and the n-level invariant finish the decision.

This form directly concerns the user's removed values and remaining variables. It permits different roots to have unrelated labels and permits the key to use paid root/context information. It requires neither an exponentially materialized restriction tree nor a direct key decoder. Its two substantive hypotheses remain sound merging on both labels and a proved polynomial width on every UNSAT root. Neither is established for a general explicit procedure here.

## 10. Uniform local-view consequence

Let a uniform procedure select an actual checkpoint C_tau of the fixed machine A on every valid s-bit input, with tau<=p(s)=s^{O(1)} actual transitions of A from its standard initial configuration. Selection, simulation, recognition, and view extraction must each take polynomial time in s. This may be a fixed time cutoff or another polynomially recognizable stopping rule. The bound on actual transitions, in addition to the acquisition bound, is what bounds the head coordinate in (21).

Extract the view consisting of control state, absolute head coordinate, the symbols in a uniformly polynomial-time computable integer radius r(s) around the head, and the canonical output cells. Suppose

\[
r(s)\le a\log_2(s+2)+b
\tag{20}
\]

for fixed constants a,b. With fixed state set Q and alphabet Gamma, the number of views at input length s is at most

\[
|Q|\,(2p(s)+1)\,|\Gamma|^{2r(s)+1+|O|}=s^{O(1)}.
\tag{21}
\]

The head address, field framing, simulation, and extraction have polynomial acquisition cost. For a proper-3-only solver, use the residual-copy compiler described above.

**Corollary 4.** If equal extracted views at the same input length always have the same SAT status, Theorem 3 produces a polynomial SAT algorithm without a direct view decoder.

Conversely, if SAT is in P, choose a polynomial-time decider A that computes its answer and normalizes a constant-size answer view. Thus existence of **some** fixed correct A and uniform checkpoint procedure with universally decision-homogeneous logarithmic views is equivalent to polynomial-time SAT. The forward implication applies to any fixed A satisfying its premises. The converse does not assert that every deliberately slow solver reaches a useful checkpoint quickly.

If a particular view procedure fails homogeneity, actual same-length SAT and UNSAT inputs share the view. Their configurations satisfy the local coupling premise: a correct continuation must reach outside the shared radius and read a distinction. Reaching outside already costs at least r(s)+1 moves. This is a genuine local lower bound, but it is only logarithmic at the radius in (20).

The dichotomy does not decide which outcome holds for a proposed procedure. Assuming survival of an opposite-answer collision for every eligible solver and polynomial-time checkpoint/view procedure would already assume a condition equivalent to the desired hardness. A lower-bound proof must instead establish the required failures and their dynamic accumulation.

More generally, if the relevant label budget is B(N) and label acquisition remains polynomial, the construction costs polynomial(N,B(N)). A quasipolynomial label budget gives a quasipolynomial upper bound. Nothing here proves that general SAT has such a budget.

## 11. A proper 3-CNF control with every clause essential

The following control tests whether clause criticality and adjacent near-satisfying assignments prevent cache collapse. They do not.

For r>=3 and b in {0,1}^r, use x_1,...,x_r,p with cyclic indices. Encode

\[
x_i\oplus x_{i+1}=b_i\quad(1\le i\le r).
\tag{22}
\]

For b_i=0 the binary clauses are (-x_i OR x_(i+1)) and (x_i OR -x_(i+1)); for b_i=1 they are (x_i OR x_(i+1)) and (-x_i OR -x_(i+1)). Replace each binary C by (C OR p) AND (C OR -p), with the same p throughout. This yields n=r+1 variables and m=4r proper clauses.

Use gamma(n+1), gamma(m+1), and the ordered signed triples. Each identifier has width w=ceil(log2(r+2)); signs occupy separate bits. The complete encoded length is

\[
\boxed{
N=2\lfloor\log_2(r+2)\rfloor+
2\lfloor\log_2(4r+1)\rfloor+2+12r(w+1)
=\Theta(r\log r).
}
\tag{23}
\]

This encoding is explicitly different from the earlier unary-header adjacent-witness transport encoding. Its parameters are not substituted into that earlier crossing theorem.

**Theorem 5 (parity and criticality).** The formula F_b is UNSAT exactly when XOR_i b_i=1. Every even member has exactly four models. Every odd member is minimally UNSAT; for every clause there is an assignment falsifying exactly that clause. There are pairs of such near-satisfying assignments at Hamming distance one.

**Proof.** The padding is equivalent to each binary clause. XORing (22) cancels every x_i, so odd total charge is inconsistent. For even total charge, choose x_1 freely and propagate; the final equation holds. The two complementary x-assignments and free p give four models.

For odd charge, delete one edge equation temporarily. The remaining path has two complementary solutions. Both violate the removed equation, but they falsify its two different binary clauses. Choose p to select either padded copy of the selected false binary clause. This produces, for every target clause, an assignment falsifying exactly that clause. Flipping only p switches the unique false padded clause. □

### Exact original and cached difference values

Flipping b_i changes exactly four sign positions in the encoded block i. Call this set D_i. These sets are pairwise disjoint. Starting with odd b, an even opponent b' differs in an odd index set S and has difference set union_(i in S) D_i. The original within-family packing is exactly r: disjoint singleton flips give r, and one representative sign from every block gives a hitting set of size r.

Now construct one fixed globally correct solver. It authenticates the exact family layout and computes the parity bit u. Failed admission uses a correct general SAT fallback. On successful admission it retains the entire input shifted to start at cell 3, places common uncommitted output symbols in cells 0,1, places u in cell 2, cleans scratch tracks, returns the head to 0, and enters a reserved common state READY. Fallback states are disjoint from READY.

Every SAT opponent reaching READY differs from an UNSAT base at cell 2. Within a fixed r the difference sets are exactly

\[
D'_S=\{2\}\cup\left(\bigcup_{i\in S}D_i+3\right).
\tag{24}
\]

Their packing is exactly one. This upper bound also covers admitted opponents of other sizes because the flag location is fixed. A constant-length suffix reads the flag and commits the output. If the answer is instead committed in the matched output or control before the checkpoint, there are no eligible opposite-answer opponents.

Thus this proper 3-CNF control exhibits

\[
\boxed{r\quad\longrightarrow\quad1\quad\longrightarrow\quad0}
\tag{25}
\]

for the relevant observation certificate: original family, shared flag, committed answer. The original source need not be discarded.

Authentication and parity evaluation take O(N) time on fixed multitapes: expected identifiers and clause patterns can be checked with O(w) work per explicit record. Preserving the source, normalization, and a faithful one-tape implementation give O_A(N^2) preprocessing time, O_A(N) span, and O_A(N^3) physical CM, with the same polynomial descriptive upper bound. No free input source is used. Since the source is retained, the O(1)-transition suffix has O(N) physical CM, not constant physical CM.

For r=4 and b=(1,0,0,0), n=5, m=16, w=3, N=206. In variable order (x_1,x_2,x_3,x_4,p), assignments (0,1,1,1,0) and (0,1,1,1,1) respectively falsify only (-x_4 OR x_1 OR p) and (-x_4 OR x_1 OR -p). Each falsifies only its displayed clause; both satisfy the other fourteen clauses. The certificate values are 4,1,0 at the three described stages.

This control is a falsifier for a general necessity claim, not evidence that all 3-CNF inputs have a parity algorithm.

## 12. Executed finite audits

Two standard-library Python stages ran separately under 30-second timeouts. No random seed was needed; both are exhaustive in their stated finite domains.

### Parity semantics and encoding

The collaborator's exact executed source and exact printed JSON were recovered without rerunning or replacing the measured timing. Runtime was 0.7187530950031942 seconds.

| Check | Count |
|---|---:|
| Formulas, r=3 through 7 | 248 |
| Complete assignments evaluated | 43,648 |
| Odd-parity UNSAT formulas | 124 |
| Clause-criticality checks | 3,056 |
| Oriented adjacent near-witness pairs | 3,056 |
| Single-charge-bit support checks | 1,528 |

Every expected semantics, criticality, adjacency, support-disjointness, and encoded-length check passed. The symbolic proof supplies the all-r theorem. The experiment is not a machine-time measurement.

### Snapshot accounting

The root audit enumerated all 127 nonempty hypergraphs on three distinguished cells. It independently enumerated rational vertices of the covering and packing programs, compared the interval formula with shortest paths in the observation relaxation, and checked first-hit potential drops and disjoint two-phase charging. Python 3.12.14; runtime 1.7700590589956846 seconds.

| Check | Count |
|---|---:|
| Hypergraphs | 127 |
| Exact rational primal/dual pairs | 254 |
| Route comparisons | 762 |
| Potential-step inequalities | 318,516 |
| Completed abstract walks | 12,510 |
| Disjoint two-phase checks | 12,033 |

All passed. The overlap triangle has fractional value 3/2 and integral hitting value 2; three independent cells have value 3; a common cache cell reduces the tested packing to 1.

These are accounting checks on abstract finite hypergraphs and walks. They do not certify reachability of arbitrary opponent configurations, recurrence of obligations for every SAT solver, a Kolmogorov complexity value, or an unrestricted asymptotic lower bound. The conditional label theorem was checked symbolically; no claimed general polynomial label constructor was executed.

## 13. Fixed-cap comparison and remaining dependency

For any fixed candidate cap T<=K N^a, the earlier same-model ceilings remain S=O(N^a), CM_phys=O(N^(2a)), and CM_min=O(N^(a+1)), with a>=1 and constants depending on the fixed implementation.

The sufficient dynamic contradiction is now explicit: on one valid UNSAT input, establish actual disjoint phases with feasible weights satisfying

\[
\tau_0+\sum_jW_j>K N^a.
\tag{26}
\]

Alternatively a separate same-execution physical sum can exceed its corresponding ceiling. A lower bound on one resource is not obtained by multiplying unrelated extrema or reversing a simulation inequality. Every independently chosen exponent a must be excluded for an unrestricted separation.

The constructive route requires one uniform h satisfying (14) and (15) on all valid inputs and the proper restriction domain, with proved polynomial acquisition. Polynomial cost plus syntactic labels alone does not suffice because their image can be exponential. A small label range alone does not suffice because opposite answers may collide. A semantic label obtainable only by an exponential SAT computation fails acquisition.

**Next named dependency: DYNAMIC-LOCAL-VIEW-DICHOTOMY1, structural premise.** On a compact decision-sensitive family with both labels, either establish a uniform safe label map with a sufficiently small UNSAT image and charge its acquisition, or construct enough successive reachable opposite-answer families after already paid work to satisfy (26). The latter must survive cached answers, shared products, algebra, relocation, and early termination. Neither universal premise is proved here.

### Scientific gates

| Gate | Status and reason |
|---|---|
| DISJ/equality sanity | PASS within scope. A common result cell collapses the observation certificate. No source-support quantity is promoted to a post-cache exponential demand. |
| Relativization | PASS as a scope check. The basic arguments do not supply a nonrelativizing separation. A semantic oracle that bypasses charged tape reads changes Theorem 1's interface. |
| Simultaneous DTISP | PASS. Snapshot, phase, and physical charges belong to one execution. Positive simulation costs are given as an explicit upper ledger, with exponent overhead. |
| Deterministic configurations | PASS. The proof uses actual reachable opposite-answer states and first differing reads. It does not infer runtime from a count of arbitrary states. |
| Dynamic recurrence under arbitrary preprocessing | OPEN. New families and their cumulative weight must be established; syntax stages do not imply execution phases. |
| General polynomial safe-label acquisition | OPEN. Theorem 3 is a conditional construction, not an implemented all-input SAT breakthrough. |

No circuit lower bound or proof-system lower bound is imported. Natural Proofs and algebrization do not provide the missing premise; no new step is claimed to overcome them. Counting and decision remain separate.

## 14. Recovery, source search, and publication provenance

Recovery began at repository head f05f8605ee0dfcd7e6acd8b4472cfa6af33582d3. AGENTS.md, CODEX.md, the research skill, the active dynamic directive, manuscript ownership, all six charged-role handoffs, and relevant original reports were recovered through connected reads. The workspace was not a full repository checkout, so the repository preflight script was not run. No historical manuscript ownership was assumed. The retired proof trackers were not opened or edited; an unsolicited broad-search hit was excluded from the evidence.

Relevant original revisions include Redteam's reachable/cache audit, Synthesis's normalization tariff, Accounting's star first-passage proof, and the October source-residual results, all identified by their full paths at the pinned recovery commit [3-7]. The existing prepayment theorem was read as the baseline [8]. No older counterexample or source-first-read lemma is relabeled new.

Fresh primary queries included “fractional certificate complexity block sensitivity deterministic query lower bound Kulkarni Tal” and “SAT polynomial range reduction pruning self reducibility Mahaney theorem proof.” The primary ITCS 2017 paper was checked at Section 2.4, and Grochow's ECCC 2016 report at its self-reduction invariant and sparse/co-sparse pruning discussion. A repeat ECCC 2013 fetch returned 502; the already retrieved paper and the accessible ITCS definition sufficed. No inaccessible theorem was imported.

Fresh organization-scoped GitHub/web queries covered anthropics, openai, xai-org, google-research, google-deepmind, and Google OR-Tools. Anthropic and OpenAI profiles displayed verified corporate domains; the remaining profiles displayed their corresponding corporate websites, and third-party similarly named hits were excluded. Search results included formalization collections, solver tooling, and mathematical research artifacts. None supplied a proved universal postprocessing-obligation theorem or a safe polynomial-range SAT label map used here. No external repository code was executed or imported; no Lean/kernel build was claimed. Consequently no code revision from those repositories is a load-bearing dependency. Existing formalization claims were not promoted from search snippets.

Ordinary research did not change any scheduled automation, enabled state, role, or manuscript ownership. The complete report and audit evidence are additive coordinator artifacts. Any publication uses the current branch-head lease and exact readback; the final chat reports the actual publication result.

## References

1. S. Ben-David, P. Hatami, A. Tal. *Low-Sensitivity Functions from Unambiguous Certificates*. ITCS 2017, Section 2.4. https://drops.dagstuhl.de/storage/00lipics/lipics-vol067-itcs2017/LIPIcs.ITCS.2017.28/LIPIcs.ITCS.2017.28.pdf
2. J. A. Grochow. *NP-hard sets are not sparse unless P=NP: An exposition of a simple proof of Mahaney's Theorem, with applications*. ECCC TR16-162, 18 October 2016. https://eccc.weizmann.ac.il/report/2016/162/download
3. Project predecessor, *PREPROCESSING-CACHE-FIREWALL173*, 26 October 2026. https://github.com/j15marti/pnp/blob/f05f8605ee0dfcd7e6acd8b4472cfa6af33582d3/research/agents/lspv-5/2026-10-26_2255_LSPV-5_PREPROCESSING_CACHE_FIREWALL173.tex
4. Project predecessor, *ARC-CHECKPOINT-RESIDUAL148*, 26 October 2026. https://github.com/j15marti/pnp/blob/f05f8605ee0dfcd7e6acd8b4472cfa6af33582d3/research/agents/lspv-4/2026-10-26_2302_LSPV-4_ARC_CHECKPOINT_RESIDUAL148.tex
5. Project Redteam, *DYNAMIC-CACHE-FIBER-AUDIT1*, 21 November 2026. https://github.com/j15marti/pnp/blob/f05f8605ee0dfcd7e6acd8b4472cfa6af33582d3/research/agents/charged-redteam/PNP_Charged_redteam_2026-11-21_211500_Cache_Fiber_Audit.md
6. Project Synthesis, *DYNAMIC-NORMALIZATION-TARIFF1*, 21 November 2026. https://github.com/j15marti/pnp/blob/f05f8605ee0dfcd7e6acd8b4472cfa6af33582d3/research/agents/charged-synthesis/PNP_Charged_synthesis_2026-11-21_212100_Normalization_Tariff.md
7. Project Accounting, *DYNAMIC-STAR-FIRST-PASSAGE1*, 21 November 2026. https://github.com/j15marti/pnp/blob/f05f8605ee0dfcd7e6acd8b4472cfa6af33582d3/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-21_214300_Star_First_Passage.md
8. Project baseline, *CHARGED-UNSAT-PREPAYMENT1*. https://github.com/j15marti/pnp/blob/7ad8794c9a6df14d47c85f9ba4efdc76518c46e5/research/main/Charged_UNSAT_Preprocessing_Tradeoff_2026-11-21.md

## Reproducibility files

- `parity_cycle_audit.py`: exact previously executed source, SHA256 3dfd118f47562cce8a34c5892517ce115492c8bfcc6fa41e24f7728be26b8c08.
- `parity_cycle_results.json`: exact original output, SHA256 042f22687c778895fe5d1521e1159f5a6d2af23f31c8d2b729814fae6053f5e3.
- `residual_certificate_audit.py`: exact executed source, SHA256 57862f0e4d4645244fb6dbd5a71ab35c4ded58157ae72833e0cf4ea231b9cf31.
- `residual_certificate_results.json`: raw exact-arithmetic and accounting output.

From a directory containing the two scripts:

```bash
python parity_cycle_audit.py
python residual_certificate_audit.py
```

Timing fields will naturally differ on a rerun. The finite outputs do not supply either missing all-solver or all-input premise.
