# Shortest obstructions and fully charged incompatibility

Research date: 22 November 2026. Named dependency: **SHARED-OBSTRUCTION-COST1**, continuing **STATIC-RESTRICTION-FRONTIER1**.

## Result and scope

The variable-removal study now has an exact rule for its source evidence: after a value is released, the smallest obstruction is the smallest **union** of suitable obstructions for all possible values, with shared source rows counted once. The complete family of inclusion-minimal obstructions must be retained in this characterization. Keeping only a shortest obstruction from each slice can give the wrong answer.

The cost of establishing incompatibility is a separate quantity. Three-variable Boolean examples have the same smallest obstruction size but different exact resolution costs. Other sound representations avoid that particular resolution cost. A complete accounting must therefore keep discovery, access, representation construction, shared reasoning, storage and output in one execution, while allowing a larger obstruction if it is cheaper to use.

For the project's strict symmetric five-value relation, the exact finite obstruction bound extends from 1, 2, 4 to **1, 2, 4, 5**. The new upper bound at three unknowns is computer-assisted, with a complete enumeration and independent implementation. A symbolic witness and a globally UNSAT source attain the sequence at separate fresh restrictions.

These results strengthen the characterization. They do not establish a superpolynomial computation lower bound. No argument here requires counting assignments, executing every slice, using resolution, materializing all supports, or performing another local inference after earlier charged work already determines the answer.

## 1. Independent levels and the meaning of shortest

Let the source formula have labeled rows

\[
F=\bigwedge_{j=1}^{m} C_j.
\]

A partial assignment \(\rho\) supplies values for some variables. The remaining \(r\) variables are unknown. Each pair \((F,\rho)\) is a fresh static input. A machine receives no earlier level's execution state. The full encoded length \(N\) includes the formula, supplied values, identifiers and headers.

For a row set \(J\subseteq[m]\), let \(F_J\) be its conjunction. Define

\[
\mathcal U_\rho=\{J:F_J|_\rho\text{ is UNSAT}\},\qquad
\mathcal M_\rho=\operatorname{Min}_{\subseteq}\mathcal U_\rho,
\]

and

\[
\mu(F,\rho)=\min_{J\in\mathcal U_\rho}|J|.
\]

Set \(\mu=+\infty\) on satisfiable residuals. An inclusion-minimal core loses UNSAT when any row is deleted. A minimum core has the smallest cardinality among all cores. These notions differ; this distinction is standard in core extraction. [1]

Equivalently, each row forbids a subset \(B_j\) of the completion domain \(D^r\). A core is a row set whose forbidden subsets cover \(D^r\). This is a semantic description of the contradiction. It imposes no representation or computational procedure.

The algorithms under discussion must be correct on both SAT and UNSAT inputs. An analyst's choice of a globally UNSAT source does not supply an all-UNSAT promise to the machine. A near-satisfying full assignment with one violated row supplies a starting slice; its one violated row does not, by itself, establish global UNSAT.

## 2. Exact recursion across a released value

Let \(x\) be unknown under \(\rho\), and write \(\rho_v=\rho\cup\{x=v\}\) for each \(v\in D\). The parent has fewer supplied values than these slices.

### Theorem 1: exact shared-source recursion

\[
\boxed{\mathcal U_\rho=\bigcap_{v\in D}\mathcal U_{\rho_v}.}
\tag{1}
\]

If the parent is UNSAT, then

\[
\boxed{
\mathcal M_\rho=
\operatorname{Min}_{\subseteq}
\left\{\bigcup_{v\in D}K_v:
K_v\in\mathcal M_{\rho_v}\text{ for every }v\right\}.
}
\tag{2}
\]

Consequently,

\[
\boxed{\mu(F,\rho)=
\min_{K_v\in\mathcal M_{\rho_v}}
\left|\bigcup_{v\in D}K_v\right|.}
\tag{3}
\]

**Proof.** A given subset of source rows is incompatible with all completions exactly when it is incompatible with all completions having \(x=v\), for every value \(v\). This proves (1). Any union in (2) blocks every slice and is a parent obstruction.

Conversely, take a parent-minimal core \(K\). In each slice, choose an inclusion-minimal core \(K_v\subseteq K\). Their union is a parent obstruction contained in \(K\), so minimality makes the union equal \(K\). Finally, an inclusion-minimal union cannot contain a smaller parent obstruction: that obstruction would itself contain slice-minimal cores yielding a smaller union. This proves (2), and taking cardinalities proves (3).

This gives the bounds

\[
\max_v\mu(F,\rho_v)\le\mu(F,\rho)
\le\min\left\{m,\sum_v\mu(F,\rho_v)\right\}.
\tag{4}
\]

At one unknown, each completely specified slice has a singleton violated-row obstruction. Equation (3) is the smallest collection of rows covering all possible values. At two unknowns, it is the smallest shared union of one-unknown obstructions. The same identity remains valid as more values are released.

This is a characterization of all sufficient source evidence. It does not require a solver to create separate branch proofs. In particular, (4) supplies no additive lower bound on computation.

### Why minimum slice sizes alone are insufficient

Consider the 2-CNF formula

\[
F=(x\lor y)\land(x\lor\neg y)
\land(\neg x\lor z)\land(\neg x\lor\neg z)
\land u\land v\land(\neg u\lor\neg v).
\tag{5}
\]

With \(x=0\), the unique minimum core is the first pair. With \(x=1\), it is the second pair. Both have size two, and their union has size four. However,

\[
H=\{u,v,\neg u\lor\neg v\}
\]

is a three-row inclusion-minimal core in both slices and in the parent. The parent has no two-row core: its two independent components require four and three rows, respectively. Thus \(\mu(F)=3\).

Even choosing optimally among every minimum-cardinality slice core misses the parent optimum. Larger slice-minimal cores can share more source rows. This example is in an easy formula class; it establishes an information loss in the proposed characterization, not hardness. The complete truth-table audit independently confirms both minimal-core families and their union identity.

### What is monotone under release

For nested restrictions of a fixed source, \(\rho_{r+1}\subseteq\rho_r\),

\[
\mu(F,\rho_r)\le\mu(F,\rho_{r+1}).
\tag{6}
\]

Any subset contradictory under the weaker restriction remains contradictory under the stronger one. Inclusion-minimal core families need not themselves nest. Neither computation time nor proof-search cost inherits (6), and independent level costs must not be added.

## 3. An exact minimum-information statement with a declared interface

List all distinct nontrivial atomic residual types on \(r\) unknowns as \(R_1,\ldots,R_M\), regarded as subsets of the completion domain. Let a bit \(z_j\) say whether type \(R_j\) occurs. Define

\[
U_r(z)=1\quad\Longleftrightarrow\quad
\bigcap_{j:z_j=1}R_j=\varnothing.
\tag{7}
\]

For Boolean width at most \(k\),

\[
M_k(r)=\sum_{j=0}^{\min(k,r)}2^j\binom rj.
\]

For the strict symmetric five-value template,

\[
M_{C_5}(r)=1+10r+5\binom r2+\binom r3.
\tag{8}
\]

The initial one represents the false row; true rows impose no condition. Duplicate rows never improve minimum cardinality, although locating a useful occurrence can cost work. Fixed-arity source-core cardinality therefore has a polynomial ceiling. Counting exponentially many completions or different cores cannot reverse this bound.

### Theorem 2: positive certificate complexity equals minimum core size

For an UNSAT mask \(z\), let \(C_1(U_r,z)\) be the fewest observed mask coordinates, allowing both zeros and ones, that force output 1 on every completion. Then

\[
\boxed{C_1(U_r,z)=\mu(z).}
\tag{9}
\]

**Proof.** Observing the selected bits of a core certifies UNSAT. Conversely, take any 1-certificate and let \(P\) be its observed one positions. The mask with exactly the positions in \(P\) set to one satisfies all observations, including the observed zeros. It must therefore be UNSAT. Adding constraints preserves UNSAT, so the positive observations in \(P\) alone suffice. Every certificate contains a core among its positive observations, giving the opposite inequality.

This is the usual decision-tree meaning of a certificate, specialized here by an elementary proof. [2] It measures how much source information fixes the answer, not the effort to determine that the information is sufficient.

The canonical cube is realizable by genuine sources. For C5, use supplied anchors with values 0 through 4 and a sixth, distinct name also supplied value 0. Give every atomic type a fixed source-record slot. An active slot contains its designated clause; an inactive slot contains a fixed true clause. An everywhere-false slot uses distinct names with two equal supplied values. All source clauses still have three distinct variable names. Every mask is legal and has exactly the required residual semantics.

The complete canonical source length is \(\Theta(M(r)\log(r+2))\). A source bit in a given record depends on at most one mask bit. This is an actual restricted input family for arbitrary source solvers, not a preprocessing requirement imposed on those solvers. Converting an arbitrary sparse source to this dense layout can expand its size cubically in \(r\); polynomial equivalence does not automatically preserve a near-linear reduction or small workspace.

The distinction between acquisition and computation is now explicit. A bit-query model can read all \(M(r)\) coordinates in \(M(r)\) probes and then assigns a decision label to the leaf for free. Consequently pure source distinguishability cannot prove a superpolynomial query lower bound on this representation. Uniform computation of that leaf label is the remaining computational problem. The fact that \(U_r\) is monotone does not restrict a solver to monotone gates, monotone reasoning, or one chosen proof system.

## 4. Three unknown Boolean values: equal obstruction size, different inference cost

Let

\[
\begin{aligned}
A&=\neg x\lor\neg y,&B&=y\lor\neg z,&C&=x\lor z,\\
D&=\neg x\lor y\lor z,&E&=x\lor\neg y\lor\neg z.
\end{aligned}
\]

Their forbidden assignments partition the cube:

| Row | Private forbidden assignments |
|---|---|
| A | 110, 111 |
| B | 001, 101 |
| C | 000, 010 |
| D | 100 |
| E | 011 |

Every row is necessary, so \(\mu(F)=5\). The first three rows allow exactly 011 and 100; the final two exclude these remaining possibilities.

Let \(g_{\rm res}\) count ordinary non-tautological binary-resolution inferences, permitting source reuse and DAG sharing. The following five inferences suffice:

\[
\begin{aligned}
\operatorname{res}_z(D,B)&=\neg x\lor y,\\
\operatorname{res}_y(\neg x\lor y,A)&=\neg x,\\
\operatorname{res}_y(E,B)&=x\lor\neg z,\\
\operatorname{res}_z(x\lor\neg z,C)&=x,\\
\operatorname{res}_x(x,\neg x)&=\bot.
\end{aligned}
\]

Four cannot suffice. No input is a unit, and no input pair derives a unit. In a four-step refutation, the final step needs opposite units among just three earlier derived clauses. A shared first nonunit would have to derive both polarities in one additional step each, forcing it to contain both polarities. A non-tautological clause cannot do that. The companion supplies the complete case argument.

For comparison,

\[
G=\{x\lor y,x\lor\neg y,\neg x\lor y\lor z,
\neg x\lor y\lor\neg z,\neg x\lor\neg y\}
\]

also has a five-row minimum core, but four resolution inferences suffice: derive \(x\), derive \(\neg x\lor y\), derive \(\neg x\), then resolve the units. Thus

\[
\boxed{\mu(F)=\mu(G)=5,\qquad g_{\rm res}(F)=5,\quad g_{\rm res}(G)=4.}
\tag{10}
\]

The complete finite Boolean audit found 869 nonempty minimal cores, plus the singleton empty clause. Exactly eight of the 266 size-five cores require five rather than four resolution inferences. The remaining cores attain \(g_{\rm res}=\mu-1\). The 869 cores form 43 symmetry orbits. A separate breadth-first audit verifies the five-step optimum of F.

This remains a proof-language result. F's five forbidden-set masks are 192,34,5,16,8 under the assignment order 000 through 111. Four binary OR operations combine them to 255, followed by an all-ones comparison. Mask construction, clause acquisition and the comparison are charged. This is not a common-machine speed comparison. It proves that an extra resolution inference cannot be declared a universal extra evidence-combination requirement.

For context, shortest resolution proof length and the time required to find such a proof are separate research questions. The cited proof-search literature concerns resolution and does not supply an unrestricted SAT lower bound. [3,4]

## 5. Three unknown C5 values: exact obstruction bound five

The strict symmetric relation \(C(a,b,c)\) accepts permutations of 012,123,234,340,401 on \(D=\{0,1,2,3,4\}\). This is distinct from the ordered tournament relation used elsewhere in the project.

With supplied values written as constants for readability, use

\[
A=C(x,1,4),\quad B=C(y,3,4),\quad D=C(x,y,1),\quad
E=C(y,z,1),\quad F=C(y,z,3).
\tag{11}
\]

A forces \(x=0\). B then permits \(y\in\{0,2\}\), while D with \(x=0\) permits \(y\in\{2,4\}\), forcing \(y=2\). E now permits \(z\in\{0,3\}\), while F permits \(z\in\{1,4\}\). Their intersection is empty.

Every row is essential. Deleting A,B,D,E,F respectively permits \((x,y,z)=(2,0,4),(0,4,0),(0,0,4),(0,2,1),(0,2,0)\). This is a symbolic five-row lower witness.

There are 46 nonempty atomic residual types on three unknowns: 30 unary, 15 binary, 1 ternary. Complete enumeration gives:

| Core size | Number of inclusion-minimal cores |
|---:|---:|
| 2 | 135 |
| 3 | 950 |
| 4 | 4,265 |
| 5 | 285 |
| Larger | 0 |

The singleton false row is separate. Hence the universal finite bound is

\[
\boxed{H_3=5.}
\]

The upper bound is **computer-assisted**, not an extrapolation from random samples. The enumerator keeps private assignments for each selected row. If a private set becomes empty, that row is redundant and remains redundant after further constraints. Every sorted prefix of a minimal core stays irredundant, so pruning cannot discard a core. No artificial core-size cap was imposed. Independent C++ and Python implementations reproduce the counts; Python also checks all 5,635 reported cores and every deletion directly on all 125 tuples.

### A globally UNSAT source attaining the independent profile

Replace the constants in (11) by five anchor variables \(a_i\), and add \(C(a_i,a_{i+1},a_{i+2})\) for \(i\bmod5\). These five anchor rows force a dihedral frame. Every frame normalizes to the displayed constants, so the original eight-variable, ten-row source is globally UNSAT.

At reference values \((a_0,\ldots,a_4,x,y,z)=(0,1,2,3,4,0,2,0)\), only F is violated. The fresh levels are:

| Unknown values | Shortest source obstruction | Size |
|---|---|---:|
| None | F | 1 |
| z | E,F | 2 |
| y,z | B,D,E,F | 4 |
| x,y,z | A,B,D,E,F | 5 |

All anchors remain supplied in this table. The source has no satisfying assignment even when they are not supplied; the table does not assert the global unpinned source has a five-row core. An exhaustive global audit checked all 390,625 assignments and all minimum cores for these restrictions. Under the canonical encoding specified in the C5 companion, the formula occupies 136 bits and the value-or-unknown array 24 bits, so every fresh input has 160 bits.

Splitting the three-unknown witness on x illustrates exact sharing. The x=0 slice uses B,D,E,F. All four nonzero x slices can use A. The union has five rows, whereas adding slice minimum sizes gives eight.

### Exact contextual information is a different service

The complete intersection closure contains 3,403 distinct three-variable supports. Any two differ on a tuple; coordinate singleton pins form a legal context selecting that tuple. Thus a source-free summary required to answer every future context must distinguish all 3,403 supports, needing 12 fixed bits. Together with the prior levels:

| C5 unknowns | Maximum minimum core | Exact support states | Fixed contextual-summary bits |
|---:|---:|---:|---:|
| 1 | 2 | 12 | 4 |
| 2 | 4 | 157 | 8 |
| 3 | 5 | 3,403 | 12 |

Identified variable slots, the fixed template and the exact contextual interface are assumed. These are neither arbitrary offline workspace lower bounds nor requirements for the current final decision. A computed answer itself occupies one bit.

## 6. The charged cost of establishing incompatibility

The quantities to retain for a concrete evidence route are its source support, acquisition/discovery work, incompatibility computation and complete resource vector. A smaller support need not yield a cheaper decision.

For example, a sequentially encoded formula can start with the contradictory triple \(u,v,\neg u\lor\neg v\), have a long tautological filler, and end with \(z,\neg z\). Its minimum core has size two at the tail. A fixed correct solver can reject after recognizing the prefix. An algorithm required to identify a minimum core must distinguish this input from the one with the final \(\neg z\) replaced by z, requiring a long traversal on a single input tape. This is an exact control for the additional minimum-core output task, not a random-access lower bound.

Thus maintain a Pareto collection of available evidence routes. It can include a longer core with cheap recognition, a shorter core with expensive discovery, an algebraic summary, a learned-clause DAG or a joint representation. A general decision algorithm need not explicitly output any core. Phase-specific costs can be displayed, but they can only be added when their physical events are disjoint.

Fix one uniform correct implementation A before choosing its input. On one execution, record

\[
T_A(I),\qquad S_A(I)=\max_t s_t,\qquad
C_A(I)=\sum_{t=0}^{T_A(I)}\max\{1,s_t\}.
\tag{12}
\]

The declared auxiliary convention counts live writable storage, including addresses, retained summaries, caches and relocation metadata. An input-inclusive physical convention must separately count retained input. All preprocessing, discovery, switching, failed attempts, representation construction, accesses, recomputation and output belong to the same run. Shared physical storage is counted once.

### A charging lemma that survives shared computation

Let actual execution events have nonnegative weights \(w_e\). If obligation i charges fractions \(\alpha_{i,e}\ge0\) with

\[
\sum_i\alpha_{i,e}\le1\quad\text{for every event }e,
\]

then

\[
\sum_i\sum_e\alpha_{i,e}w_e\le\sum_e w_e.
\tag{13}
\]

This follows by exchanging finite sums. Time events are machine steps. Cumulative-storage events are live-bit/time pairs, plus a baseline event whenever no auxiliary bit is live. With overlap at most d, summed obligation charges are bounded by d times the actual cost.

To infer a lower bound, both the compulsory charge per obligation and the capacity/overlap premise must be proved from correctness. Many branches, constraints or semantic exclusions do not establish either premise. A shared calculation may settle many obligations simultaneously. Equation (3) proves source-row sharing exactly; it does not prove a bound on execution-event sharing.

There is no universal mandatory extra local operation after unrestricted preprocessing. A correct solver can perform its whole decision as preprocessing and retain its verdict. Returning that verdict takes constant additional work; the preceding computation is still fully charged. A lower bound must attach to the whole realization, or justify why a specific already-produced state leaves an unresolved task.

The project's attached *Saturation and Projection with Charged Access* report supplies a compatible earlier control: an exponentially large CNF projection can have a compact affine representation. Its construction/selection/evaluation ledger is retained here. A blowup in one representation is not imported as a universal cost requirement.

## 7. A bridge that includes every sound solver

### Arbitrary decision gives inclusion-minimal core extraction

Fix any correct decider A for the canonical masks. Start with an UNSAT mask; consider selected bits in sequence, temporarily removing one and asking A whether the remaining mask is UNSAT. Keep a deletion exactly when UNSAT persists.

This uses at most M+1 calls including initial decision. A retained bit was indispensable when tested. Later deletions only remove constraints, so removing that bit at the end remains satisfiable. The final mask is therefore inclusion-minimal. Let \(T_A(M),S_A(M)\) bound A on every mask of length M, including modified masks. Under a compatible read-only-input simulation,

\[
T_{\rm extract}\le(M+1)T_A(M)+O(M^2),\qquad
S_{\rm extract}\le S_A(M)+O(M).
\tag{14}
\]

The persistent mask stays live during each call, giving the additional cumulative-storage term \(O(M)\sum_iT_{A,i}\), beyond the sum of callee costs and bookkeeping. This preserves polynomial feasibility. It does not preserve a sharp exponent or make minimum-cardinality extraction compulsory. No restriction is imposed on A's reasoning.

### A verifier can admit an arbitrary correct computation

For every fixed total correct A, define

\[
V_A(I,1^t)=1\iff A(I)\text{ reports UNSAT within }t\text{ steps}.
\tag{15}
\]

The unary allowance has length t, making bounded simulation polynomial in the verifier's full input length. Soundness follows from A's correctness. Every UNSAT input has such a proof; verification pays for the simulation. This admits every sound inference method used by A without introducing a free UNSAT rule. No effective enumeration of all sound programs is assumed.

Existence of short proofs and efficient discovery of them are different. A fixed sound search-and-verification procedure that finds a proof on every UNSAT input within a polynomial cap yields a polynomial decider: run to the cap, report UNSAT if verification succeeds, and SAT otherwise. Short proofs merely existing does not give that deterministic search.

The general Cook-Reckhow characterization relates polynomially bounded propositional proof systems to NP=coNP. A superpolynomial proof-size lower bound against every such system would establish NP≠coNP, a stronger target than P≠NP. The operational route can instead concern deterministic discovery or incompatibility computation. [5]

## 8. Uniformity and simultaneous resource exclusions

No superpolynomial pointwise lower bound can result from choosing a new optimal algorithm for each individual input. A fixed known UNSAT string can be hardcoded, recognized by comparison, and answered correctly, with a general solver on other strings. Its special-input runtime and code description can both be linear in that string's length.

A separation target must fix a correct uniform A first, then seek arbitrarily large bad inputs against each proposed polynomial cap. For Boolean fixed k≥3, one sufficient form is

\[
\forall A\ \forall p\ \forall N_0\ \exists I:
|I|\ge N_0,\ I\text{ UNSAT},\ T_A(I)>p(|I|),
\tag{16}
\]

where A ranges over total correct deciders and p over polynomial bounds. A polynomial bound on all UNSAT runs of some correct A would already yield polynomial decision by a timeout, even if its SAT runs were slower. Individual hard examples for one algorithm do not establish (16).

For the realizable C5 cube, proving that every fixed uniform implementation of \(U_r\) violates each polynomial cap on arbitrarily large inputs would also imply P≠NP. The SAT version of the corresponding residual language is in NP, and complementing a deterministic decision preserves polynomial time. A polynomial raw-source solver would therefore solve the UNSAT cube through its polynomial fixed-slot encoding. This implication needs no unproved NP-hardness claim about the specific template. The required unrestricted lower bound is still open.

The previous simultaneous resource frontier remains applicable only with its exact encoding and model-transfer premises. For explicit fixed-domain residuals with bounded r and canonically indexed supplied values, a feasible scan/evaluation point has near-linear random-access time and polylogarithmic auxiliary workspace. This bounds what an all-method lower bound can demand at any fixed level. It is an available route, not a claim that the user's exploration must implement it.

Known SAT time-space exclusions constrain one execution's joint resource vector. Williams' Table I includes the simultaneous exponents 1.24 and 0.666, while the separate subpolynomial-space endpoint is \(2\cos(\pi/7)\). [6] The earlier project transfer from small-initial-state auxiliary cumulative cost uses

\[
T\le C,\qquad S_{\max}\le\widetilde O(1+\sqrt C)
\]

under bounded per-step storage growth. With the already established local SAT transfer, strict \(C=O(N^\gamma)\), \(\gamma<1.24\), would enter a forbidden joint region. This is not an input-inclusive physical-CM statement or a transfer to arbitrary encodings. The new dense canonicalization has not been shown to preserve the required near-linear overhead. Separate best time and best space values from different algorithms cannot be combined into a joint point.

## 9. Proof status, controls and next dependency

| Claim | Status |
|---|---|
| Shared-union core-family recursion and monotonicity | PROVED, elementary symbolic |
| Per-slice minimum-cardinality choices can miss the parent minimum | PROVED, 2-CNF control plus exhaustive check |
| Realizable canonical cube and certificate/core identity | PROVED in the stated input interface |
| Boolean equal-core/different-resolution-cost witnesses | PROVED symbolically; independently audited |
| Complete Boolean three-variable classification | COMPLETE FINITE COMPUTATION with completeness argument |
| C5 universal H3≤5 | COMPLETE FINITE COMPUTATION with completeness argument |
| C5 five-row witness and global source/profile | PROVED symbolically; exhaustively audited |
| C5 3,403 contextual supports | COMPLETE FINITE COMPUTATION; 12-bit interpretation conditional on exact context service |
| Event-capacity charging and arbitrary-decider extraction | PROVED with declared machine accounting |
| Universal superpolynomial incompatibility cost | OPEN |

Four falsifiers remain active. First, if a proposed recurrence discards a larger slice-minimal core, test (5). Second, if it infers cost from minimum cardinality alone, test F and G. Third, if it forces a final local inference, test a shared computed verdict. Fourth, if it transfers a query, resolution or summary bound to every solver, test arbitrary computation of the canonical \(U_r\), including nonmonotone and algebraic methods.

DISJ sanity is respected by the M-probe ceiling and explicit interface scope. No nonrelativizing separation has been obtained. Simultaneous DTISP transfer remains conditional on already specified model and overhead hypotheses. Deterministic configuration counting supplies no lower bound here. No general circuit lower bound or Natural-Proofs/algebrization barrier bypass is claimed. The easy 2-CNF, affine-projection and shared-verdict controls prevent representation-specific work from being promoted.

The next load-bearing theorem is **a uniform lower or upper bound for establishing \(U_r(z)=1\), with access, discovery, construction and sharing included in a single resource vector**. A source-core invariant used toward a lower bound must connect to compulsory execution events for every fixed correct solver, with a proved overlap bound. A constructive shortcut remains a valid outcome if its all-input correctness and complete polynomial resource bound can be proved.

## 10. Evidence, provenance and review

Detailed derivations are in the companion notes:

* `obstruction_cost_20261122/Universal_Evidence_Cost_Framework.md`.
* `obstruction_cost_20261122/boolean/Boolean_Three_Unknown_Obstruction_and_Inference.md`.
* `obstruction_cost_20261122/t5/T5_Three_Unknown_Obstructions_and_Evidence_Cost.md`.

Reproducible code is under `experiments/obstruction_cost_20261122/`; immutable raw outputs are under `results/raw/obstruction_cost_20261122/`. The companion `Research_Provenance_and_Manifest.md` records searches, source pins, checksums and validation scope. Code and raw evidence remain separate from prose.

Three collaborators developed the Boolean, C5 and unrestricted-cost components. The Boolean collaborator independently reviewed the complete C5 note, enumeration, source construction and contextual-information scope. The coordinator checked the elementary proofs, exact sharing control, masks and quantifier/model boundaries. This is same-project internal review, not external peer review or a formal-kernel certificate.

All finite runs completed under bounded invocations. The C5 global source audit covers 390,625 assignments; the template audit covers every one of 5,635 nonempty minimal cores and its deletions. Boolean classification covers 869 nonempty minimal cores; the concrete minimum-resolution search first reaches contradiction at depth 5. No native bit-machine parser, tape simulation, formal proof kernel or full-repository preflight was run. No complete local checkout was available. No agent schedule or owner manuscript was changed.

## References

[1] Inês Lynce and João Marques-Silva. *On Computing Minimum Unsatisfiable Cores*. SAT 2004. Definitions distinguish minimal from minimum. https://www.satisfiability.org/SAT04/programme/110.pdf

[2] Harry Buhrman and Ronald de Wolf. *Complexity Measures and Decision Tree Complexity: A Survey*. Author manuscript, 13 December 1999; published in Theoretical Computer Science 288(1), 2002. Section 4.1. https://homepages.cwi.nl/~rdewolf/publ/other/tcs.pdf

[3] Albert Atserias and Moritz Müller. *Automating Resolution is NP-Hard*. Author manuscript, 3 September 2019. https://www.cs.upc.edu/~atserias/papers/automating-resolution-np-hard/automating-resolution-np-hard.pdf

[4] Konstantin Sidorov, Koos van der Linden, Gonçalo Homem de Almeida Correia, Mathijs de Weerdt and Emir Demirović. *How To Discover Short, Shorter, and the Shortest Proofs of Unsatisfiability: A Branch-and-Bound Approach for Resolution Proof Length Minimization*. arXiv:2411.07955, 2024. https://arxiv.org/abs/2411.07955

[5] Stephen A. Cook and Robert A. Reckhow. *The Relative Efficiency of Propositional Proof Systems*. Journal of Symbolic Logic 44(1), 1979, 36–50. Propositions 1.1 and 1.4. https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf

[6] Ryan Williams. *Alternation-Trading Proofs, Linear Programming, and Lower Bounds*. ACM Transactions on Computation Theory, 2013. Corrected author copy, Table I and footnote 9. https://people.csail.mit.edu/rrw/automated-lbs.pdf

Project antecedents: *Independent One- and Two-Unknown UNSAT Levels*, 22 November 2026, main commit 0751533f220dfcd9fdf0694ce45efc798cd17f3a; its `Static_Restriction_Resource_Transfer.md` companion; attached *Saturation and Projection with Charged Access*, 13 October 2026; pending TMR-4/098 relational-summary report at 6235f351e8f278e331c12e5d9368b977ea6dea49. The latter concerns ordered T5 and is used only for the relation-summary and cost-accounting distinction.
