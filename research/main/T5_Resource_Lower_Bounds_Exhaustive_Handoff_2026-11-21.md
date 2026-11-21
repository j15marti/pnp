# Exhaustive research handoff: strict T5, exact counting, and resource lower bounds

Prepared 21 November 2026, America/Los_Angeles.

## 0. Read this first

The project is trying to establish an unconditional superpolynomial lower bound for exact counting, principally for a fixed five-valued constraint problem called strict T5. The longer-term objective is a P versus NP separation. The approach charges actual computation, input and instruction access, addresses, storage, information movement, cumulative memory, and the construction or discovery of useful representations.

The current work does **not** prove an unrestricted superpolynomial lower bound for strict #T5, #SAT, or SAT. It does contain complete polynomial lower bounds for every correct solver in a specified single-tape model, superpolynomial lower bounds for explicit representation tasks and restricted counting architectures, and several general transfer lemmas that identify what additional theorem would refute a polynomial time cap.

The main unresolved issue is precise: a scalar exact counter need not construct the full witness relation, visit every assignment, or separately answer every conceptual residual query. A useful lower-bound measure must start large on the chosen family and have a provably bounded decrease under every operation the claimed model permits. We have these two properties together for restricted architectures. For unrestricted circuits we have the local progress property, but not the required large initial value.

This handoff consolidates the recovered original source archive, the subsequent CM continuation, three later research notes, finite verification scripts, and selected earlier project controls. The original crossing and cumulative proofs were retrieved and inspected during this handoff. Their status is therefore stronger than the provisional “inherited, pending source audit” descriptions in some earlier notes. No claim of historical novelty is made for the constructions or elementary deductions.

### Principal conclusions and their scope

| Statement | Status and scope |
|---|---|
| Exact strict #T5 requires \(T=\Omega(N^2)\) and self-contained configuration CM \(=\Omega(N^3)\) on the sparse matching layouts | Audited project theorem for every fixed correct deterministic sole-tape solver |
| These time and CM demands can hold simultaneously on almost all diagonal inputs, for each fixed solver | Audited strengthening using a union bound |
| A separate strict T5 decision family requires \(T=\Omega(N^2/\log N)\), CM \(=\Omega(N^3/\log^2 N)\) | Audited, same physical model; a different family from the count-only matching instances |
| Strict symmetric T5 has an explicit Boolean-circuit reduction | Audited gadgets; decision equivalence and a known-multiplier count reduction |
| Bounded-degree, high-treewidth graph witness predicates require large DNNF and DLDD representations | Published representation results and derived applications |
| Adaptive branching obeys a common treewidth potential | Proved for the specified uncached recursion architecture |
| Typed DLDD completion has a rigorous local progress bound | Proved; arbitrary scalar shortcuts have an unbounded, presently uncontrolled expansion ratio |
| Ordinary full-state conditional entropy measures remaining computational work | False; it is zero for a correct deterministic complete state |
| Properly decoded entropy-transfer demands imply time lower bounds | Proved conditional accounting lemma; sufficiently strong compulsory demands are missing |
| Suitable conditional pseudoentropy implies count-circuit hardness | Proved comparator criterion; the required target-specific distribution is missing |
| General count-circuit size implies time and CM lower bounds | Proved transfer using machine simulation and distinct configurations |
| These results prove \(P\ne NP\) | No |

The next model should preserve these distinctions and choose one missing bridge to work on, rather than treating the existence of several resource measures as an additional lower bound.

## 1. Research objective and quantifiers

Let \(A\) be one fixed deterministic solver, correct on every permitted input. Fix one input encoding and one machine model. Constants depending on \(A\) are allowed; an input-dependent solver, advice string, decoder, or program is a different hypothesis.

The cap being tested is

\[
T_A(N)\le K N^a
\]

for fixed constants \(K,a\). To rule out polynomial time, the required logical form is

\[
\forall A\text{ correct}\ \forall a,K,N_0\
\exists N\ge N_0\ \exists x\in\mathcal X_N:
t_A(x)>KN^a.
\]

An eventual \(N^{\omega(1)}\) worst-case lower bound is sufficient, but stronger than necessary. Infinitely many violations of every proposed global polynomial cap suffice.

The earlier variable-count formulation was \(T(n,m)\le Kn^c\). It is meaningful only when the permitted clause count is controlled, or when the dependence on \(m\) is retained. An explicitly listed instance can have arbitrarily many repeated clauses, so an unrestricted bound in \(n\) alone ignores input size.

### Counting and decision are separate goals

An exact counting algorithm can decide satisfiability by testing whether the count is positive. A lower bound for counting does not reverse this implication. In particular, every instance in the NAND graph family below is satisfiable.

The circuit gadget reduction establishes that the general strict T5 decision problem is NP-complete. Nevertheless, a superpolynomial lower bound for the exact-count map alone would establish a counting separation, not by itself a P versus NP separation. A decision lower bound or another justified bridge is required.

## 2. What “distinguishable states” can mean

The initial questions concerned the maximum number of distinguishable states of \(k\)-SAT or #SAT. Several different quantities must remain separate.

For Boolean formulas with \(n\) variables there are \(2^n\) assignments. A count is an integer between \(0\) and \(2^n\), so there are at most \(2^n+1\) possible count outputs, represented by at most \(n+1\) binary bits. Fixed clause regimes may realize fewer counts.

For a five-valued instance there are \(5^n\) assignments and at most \(5^n+1\) possible counts, with \(O(n)\) output bits. The analyzed template can impose additional restrictions, such as an anchor symmetry factor; the interval bound is only an upper bound.

For \(N\)-bit encoded inputs there are at most \(2^N\) possible input strings. A deterministic truth table produced from an input is a function of those \(N\) bits even if it has exponentially many coordinates.

If a faithful configuration description uses \(S\) bits, it has at most \(2^{O(S)}\) possibilities under the specified coding convention. A requirement to distinguish \(M\) alternatives therefore normally yields a storage requirement of order \(\log M\), not \(M\).

Most importantly, a large universe of possibilities does not prove that one correct aggregate computation must visit or separately represent every possibility. The crossing proof below supplies a genuine compulsory distinction through valid hybrid inputs. The representation theorems supply one through restricted representation semantics. Neither inference follows from assignment counting alone.

## 3. Exact target definition and the ordered-clause issue

### 3.1 The template actually used in the recovered archive

The original archive explicitly defines a fixed **symmetric** ternary relation \(C\) over \(\mathbb Z_5=\{0,1,2,3,4\}\). Its allowed unordered triples are

\[
012,\quad123,\quad234,\quad340,\quad401.
\]

All six permutations of each listed triple are allowed. Thus \(C\) has 30 ordered satisfying tuples, and every satisfying tuple has three distinct values.

A strict input is a conjunction of this one relation. Each clause has three distinct variable names. The variables initially have the entire five-valued domain. There are no per-clause relation tags, literal signs, primitive NOT literals, or input constants. All domain restrictions and Boolean operations below are implemented by ordinary \(C\)-clauses.

### 3.2 A different ordered relation appeared in the earlier verbal description

The tournament was described as

\[
A>B,D;\quad B>C,E;\quad C>D,A;\quad D>E,B;\quad E>A,C.
\]

Using \(A=0,\ldots,E=4\), vertex \(i\) beats \(i+1\) and \(i+3\) modulo five.

Let \(R(x,y,z)\) mean that the first value beats exactly one of the other two and loses to the other. This ordered relation has 40 satisfying tuples. It is not \(C\). A transitive tournament triple has a middle vertex satisfying the ordered rule, although the triple is not a directed cycle.

For example, \(R(0,2,3)\) holds, while \(C(0,2,3)\) does not.

### 3.3 An exact conversion resolves the distinction without silently changing definitions

For every triple of values,

\[
\boxed{C(x,y,z)\iff R(x,y,z)\land R(y,x,z).}
\]

A cyclic triple has one win and one loss at both displayed first coordinates. A transitive triple has only one middle vertex, so two distinct coordinates cannot both pass that test. Tuples with repeated values satisfy neither side.

Replacing each \(C\)-clause by these two \(R\)-clauses preserves every assignment and the exact count. It introduces no new variables, doubles \(m\), preserves distinct variable names inside clauses, and increases the encoded length by only a constant factor. All \(C\)-based constructions can therefore be transferred to this ordered \(R\) problem by this explicit conversion.

There is also a smaller repair for the NAND graph gadget alone: under \(R\), use \(R(X_u,a_0,Y_v)\), not \(R(a_0,X_u,Y_v)\). The latter accepts all four permitted left/right pairs and makes every graph edge redundant. The repaired ordering forbids exactly simultaneous selection.

The original transport matching gadget happens to work directly under both relations. The original decision pinning and the complete Boolean OR construction do not survive a blind \(C\)-to-\(R\) substitution. Use the two-clause conversion when transferring the full theorem stack.

The finite audit appended below checks all 125 value triples, all ten anchor frames, the graph truth tables, both matching families, and the decision gadgets. This is a definition correction in the handoff, not a claim that the old archive used the ordered relation.

## 4. Input encoding, syntax information, and physical computation

The fixed explicit encoding is

\[
1^n0\ \gamma(m+1)\ [m\text{ triples}],
\qquad
w=\lceil\log_2(n+1)\rceil,
\]

where \(\gamma\) is Elias gamma coding and each variable identifier occupies \(w\) bits. Hence

\[
\boxed{N=n+1+2\lfloor\log_2(m+1)\rfloor+1+3mw
=\Theta(n+m\log n).}
\]

The unary declaration ensures \(n\le N\). This matters because counting declared unused variables must not demand an exponentially long answer from a logarithmic-length variable declaration.

Clause positions are implicit in a fixed-width list. An explicit address table is charged if an implementation stores one; it is not a mandatory second address field attached to every already encoded identifier.

For the symmetric relation, set \(J=\binom n3\). Conditional on known \(n,m\):

| Exact syntax to reconstruct | Number of possible objects |
|---|---:|
| Ordered list of \(m\) canonically sorted clauses, repetition allowed | \(J^m\) |
| Ordered list of \(m\) distinct clauses | \(J!/(J-m)!\) |
| Unordered set of \(m\) distinct clauses | \(\binom Jm\) |
| Unordered multiset of \(m\) clauses | \(\binom{J+m-1}{m}\) |
| Ordered list preserving all three argument positions | \((6J)^m\) |

The minimum fixed-length lossless code for each specified class is the ceiling of the logarithm of its cardinality. These are syntax bounds, not minima over all answer-preserving semantic representations. Ranking and decoding may be computationally expensive. A short code does not give free random access.

For \(n=2005,m=4005\), \(w=11\) and \(N=134{,}194\) bits. The clause data occupy \(132{,}165\) bits; the header occupies \(2{,}029\). The optimal joint ordered canonical clause-data code requires \(121{,}436\) bits; the distinct-clause-set code requires \(79{,}277\). These encode different reconstruction requirements.

A candidate assignment is not part of the initial instance. Its representation is workspace only if the solver stores it. The fixed relation is part of the problem definition and fixed program, not a separate truth table replicated per clause.

## 5. Machine model and resource definitions

The primary model is a fixed deterministic Turing machine with:

- one physical read/write tape and one head;
- a fixed finite tape alphabet and \(Q\ge2\) control states;
- input, work, code if stored, and output on that tape;
- primitive transitions reading and writing the scanned cell and moving by at most one cell;
- a canonical binary output and terminator starting at a fixed left origin;
- no independently moving input head, original-input oracle, external work store, or free clock affecting future behavior.

The crossing results concern this model. Random access, multiple tapes, and wider words require their own simulations or lower-bound proofs. Polynomial-time equivalence under suitable bit-cost simulations can support a superpolynomial separation, but it does not preserve the concrete quadratic exponent automatically.

Use \(C_t(x)\) for the full configuration immediately after transition \(t\). For the finite crossing formulas, charge \(t=1,\ldots,t_A(x)\). Other notes sometimes use pretransition configurations; their asymptotic statements are compatible, but finite formulas should use one convention consistently.

Define

\[
T_A(N)=\max_{x\in\mathcal X_N}t_A(x),\qquad
S_A(N)=\max_{x,t}s_A(x,t),
\]

\[
M_{\rm phys,A}(N)=\max_x\sum_{t=1}^{t_A(x)}s_A(x,t),
\]

\[
M_{\min,A}(N)=
\max_x\sum_{t=1}^{t_A(x)}K_U(C_t(x)\mid A).
\]

Here \(s_A\) is a faithful physical charge sufficient to encode the complete state, including tape support or locations, head and control, stored addresses, and any continuation-relevant state. A contiguous tape-span convention works. Counting only nonblank payload while giving unbounded locations away does not.

\(K_U\) denotes a fixed universal description convention, preferably prefix complexity when invoking Kraft's inequality. The input and the time index are not free side information. The decoder and solver are fixed.

The original archive also uses \(CM_{\rm code}\) for any fixed faithful self-contained configuration code. Its crossing lower bound applies even to canonically selected shortest descriptions; it does not require an efficient encoding or decoding procedure.

### Program size and execution are different charges

A fixed uniform program has fixed description length \(B\), independent of \(N\). Executing a loop \(T\) times does not require \(T\) source-code lines or storing an execution transcript. Instruction fetches and movements are charged when physically performed.

The archive supplies a movable stored-code simulation: an \(O(B)\)-cell code block travels beside the simulated head. For a fixed source program, this gives constant program-dependent overhead per source transition and \(O(S+B)\) storage. It defeats an automatic claim that every instruction fetch must traverse the entire input.

Primitive traffic is \(O(T)\) fixed-alphabet symbols, while CM sums residence over time. Cubic CM can coexist with quadratic traffic. Do not call both quantities “total bits.”

## 6. What a time cap actually forces

A sole-tape machine can expand its visited span by only a constant number of cells per transition:

\[
S_A=O_A(N+T_A).
\]

Therefore

\[
M_{\rm phys,A}\le T_AS_A
=O_A(T_A(N+T_A)).
\]

A complete configuration can be described using the fixed program, original input, and transition index. Replay reconstructs it:

\[
M_{\min,A}
\le O_A\!\left(T_A(N+\log(T_A+2))\right).
\]

This is a description-length bound, not a same-time small-space implementation. Prefix delimiters are absorbed by the displayed big-O bound.

Under \(T_A(N)\le KN^a\), \(a\ge1\),

\[
\boxed{S_A=O(N^a),\quad
M_{\rm phys,A}=O(N^{2a}),\quad
M_{\min,A}=O(N^{a+1}).}
\]

In variable-count form, if \(N=O(n^d)\) and \(T=O(n^c)\),

\[
S=O(n^{\max(c,d)}),\qquad
M_{\rm phys}=O(n^{c+\max(c,d)}).
\]

Polynomial time does not imply linear workspace. The linear-space assumption would produce a sharper \(O(N^{a+1})\) physical-CM ceiling, but it is an additional assumption.

Conversely, exhaustive assignment enumeration gives a fully paid strict #T5 algorithm with

\[
T=O(5^nN^2),\qquad S_{\rm total}=O(N),
\]

and physical or explicit-description CM at most \(O(5^nN^3)\). Thus an unconditional superpolynomial peak-space necessity is impossible here. Space must enter through a tradeoff conditional on fast time.

## 7. Anchor frames and the two matching constructions

### 7.1 Ten-frame anchor

Introduce five anchor variables and impose

\[
\mathcal A=\bigwedge_{i=0}^4 C(a_i,a_{i+1},a_{i+2}),
\]

with subscripts modulo five. Every pair of anchor names appears together in a clause, so all five values differ. The allowed triples are complements of the edges of an ordinary five-cycle. Therefore the satisfying assignments are exactly

\[
a_i=s+i\pmod5
\quad\text{or}\quad
a_i=s-i\pmod5,
\]

for five choices of \(s\): ten frames. The anchors are variables, not literal constants.

### 7.2 Original transport matching family

The original archive uses

\[
C(a_1,a_2,V)\iff V\in\{a_0,a_3\},
\]

and, on this Boolean domain,

\[
C(a_4,X,Y)\iff X\ne Y.
\]

For \(\pi,\sigma\in S_k\), introduce \(X_1,\ldots,X_k,Y_1,\ldots,Y_k\) and list:

\[
\mathcal A\ ;\
\bigwedge_i C(a_4,X_i,Y_{\pi(i)})\ ;\
\mathcal D\ ;\
\bigwedge_i C(a_4,X_i,Y_{\sigma(i)}),
\]

where \(\mathcal D\) is the common block of all \(2k\) Boolean-domain clauses.

Then

\[
n=2k+5,\quad m=4k+5=2n-5,
\]

\[
\boxed{Z(F_{\pi,\sigma})=10\,2^{c(\pi^{-1}\sigma)}.}
\]

The union of the two matchings has one component for each cycle of \(\pi^{-1}\sigma\), and each component has two valid assignments. Consequently diagonal counts equal \(10\cdot2^k\), while all off-diagonal counts are smaller.

There are \(k!\) diagonals, all satisfiable. The matching structure is easy to count by cycle decomposition when suitable access is available. This is an information-transport family, not an intrinsically difficult counting promise problem.

A no-repeated-clause version replaces each matching edge by a fresh equality gadget

\[
\operatorname{Eq}(U,V;Z)=
C(a_1,a_2,Z)\land C(a_4,U,Z)\land C(a_4,Z,V).
\]

It has \(n=4k+5,m=8k+5\), unique auxiliary extensions, the same count formula, and the same asymptotic crossing bounds.

### 7.3 Later NAND / independent-set family

For a bipartite graph \(G=(L,R,E)\), impose

\[
D_L(X_u)=C(a_0,a_1,X_u),
\qquad X_u\in\{a_4,a_2\},
\]

\[
D_R(Y_v)=C(a_0,a_4,Y_v),
\qquad Y_v\in\{a_1,a_3\}.
\]

Interpret the listed values as unselected, selected. An edge clause \(C(a_0,X_u,Y_v)\) forbids exactly the selected-selected pair. Therefore

\[
\boxed{Z(F_G)=10\,\#IS(G),}
\qquad
n=v+5,\quad m=v+|E|+5.
\]

For ordered \(R\), replace this edge by \(R(X_u,a_0,Y_v)\), or apply the universal two-clause conversion.

Using two matchings again gives the same \(n,m,D,N\) parameters as above, but now diagonal counts are

\[
\boxed{10\cdot3^k,}
\]

not \(10\cdot2^k\). An off-diagonal introduces an edge absent from the first matching; selecting exactly its two endpoints previously gave a valid independent set and is now forbidden. Hence every off-diagonal count is strictly smaller.

More precisely, the count factors as \(10\prod_\ell L_{2\ell}\) over permutation cycles of lengths \(\ell\), where \(L_j\) are Lucas numbers and \(L_2=3\) handles a doubled matching edge. This family also has degree at most two and treewidth at most two.

### 7.4 A separate decision family

Under \(C\),

\[
P_0(X)=C(a_1,a_4,X)\iff X=a_0,\qquad
P_1(X)=C(a_2,a_4,X)\iff X=a_3.
\]

For \(x,y\in\{0,1\}^k\), list frame, the \(x\)-pin block, a common \(k\)-clause domain block, and the \(y\)-pin block. This gives

\[
n=k+5,\quad m=3k+5,\quad
Z(G_{x,y})=
\begin{cases}10,&x=y,\\0,&x\ne y.\end{cases}
\]

There are \(2^k\) accepting diagonals. This supports decision lower bounds without using the all-satisfiable counting family as a decision argument.

## 8. The complete crossing and cumulative-information proof

### 8.1 Abstract family hypotheses

Suppose \(x_{u,v}=L_uMR_v\), with \(|U|=P\), a common header and block positions, and \(D\) selected boundaries inside \(M\). Every diagonal has one common answer; every off-diagonal has a different answer. For counting, the complete diagonal output including its terminator is left of each selected cut. For decision, diagonals accept and off-diagonals reject.

Correctness is required on the hybrids, not merely on the diagonal promise.

### 8.2 Full crossing-sequence injection

At a cut \(b\), record the state immediately after every crossing. The head begins left of the cut, so direction is determined by the crossing index.

Two diagonal computations with the same complete crossing sequence can be spliced: use left excursions from one and right excursions from the other. Matching entry states ensure the local histories fit. Equal sequence lengths ensure the same final side and a halting hybrid computation.

The hybrid then produces the diagonal answer, contradicting correctness. Thus

\[
u\longmapsto CS_b(u)
\]

is injective at every selected cut.

Counting distinct strings over a \(Q\)-symbol state alphabet gives an average crossing length \(\Omega(\log P/\log Q)\). Averaging over the same uniform diagonal distribution for every boundary yields

\[
\boxed{T=\Omega(D\log P/\log Q)}
\]

on some input. One physical step crosses at most one boundary.

### 8.3 Prefix plus current-configuration injection

Fix a cut \(b\) and crossing index \(j\). On diagonals reaching that crossing, the map

\[
u\longmapsto
\bigl(p_{b,j}(u),\operatorname{code}(A,C_{b,j}(u))\bigr)
\]

is injective, where \(p_{b,j}\) is the first \(j\) crossing states.

Indeed, if two such diagonals have the same prefix and current left tape contents, splice only through crossing \(j\). The hybrid then has the second diagonal's full current configuration: its right part came from that diagonal and its left part was assumed identical. Determinism gives the same future answer, a contradiction.

Absolute crossing times may differ. This is legitimate because there is no free external clock; everything affecting continuation is included in the configuration.

### 8.4 Finite cumulative bound

For integers \(r,s\ge0\), let

\[
E_j(s)=\frac{Q^j-1}{Q-1}+Q^j(2^s-1).
\]

The first term bounds diagonals with fewer than \(j\) crossings. The second bounds diagonals reaching crossing \(j\) with code length below \(s\): there are at most \(Q^j\) prefixes and \(2^s-1\) short binary codes.

Thus

\[
\boxed{
\mathbb E CM_{\rm code}\ge
Ds\sum_{j=1}^r
\max\left\{0,1-\frac{E_j(s)}P\right\}.
}
\]

All selected events occur at distinct transition times on each input. This is why the proof is a cumulative lower bound rather than a product of unrelated worst cases.

Set \(H=\log_2P\),

\[
r=\left\lfloor\frac{H}{4\log_2Q}\right\rfloor,\qquad
s=\lfloor H/4\rfloor.
\]

Then

\[
E_j/P\le P^{-3/4}/(Q-1)+P^{-1/2},
\]

and

\[
\boxed{CM_{\rm code}=\Omega(DH^2/\log Q).}
\]

For example, \(H\ge\max\{8,8\log_2Q\}\) ensures an existential lower bound \(DH^2/(128\log_2Q)\). Prefix-freeness is not needed for this finite counting proof.

### 8.5 Simultaneous high-probability strengthening

Let \(\ell=\log_2Q\), choose \(z\ge0\), and write \(h=H-z\ge0\). Set

\[
r=\lfloor h/\ell\rfloor,\qquad
s_j=\lfloor h-j\ell\rfloor.
\]

Since \(E_j(s_j)\le P2^{-z}\), a union bound over the \(Dr\) selected events gives

\[
\Pr\left[
T\ge Dr\ \land\
CM_{\rm code}\ge D\sum_{j=1}^r s_j
\right]\ge\max\{0,1-Dr2^{-z}\}.
\]

The same input satisfies both inequalities on the good event. No independence assumption is used. For \(D,H=\Theta(N)\), choosing \(z=O(\log N)\) gives failure at most any chosen inverse polynomial while retaining quadratic time and cubic CM.

The exceptional inputs may depend on the fixed solver. This is not one input proved hard simultaneously for all machines.

For \(k=1000,Q=256,z=33\), the exact integer calculation gives \(N=134{,}194\), \(D=65{,}999\), \(r=1062\), simultaneous \(T\ge70{,}090{,}938\), CM \(\ge297{,}465{,}940{,}872\), with success fraction at least \(99.381340\%\). These are theorem instantiations, not measured solver runtimes.

### 8.6 Applications and padding

For either sparse matching family,

\[
P=k!,\quad H=\Theta(k\log k),\quad
D=6kw-1=\Theta(k\log k),\quad
N=\Theta(k\log k).
\]

Thus every fixed correct sole-tape counter has

\[
\boxed{T=\Omega(N^2),\quad CM_{\rm code}=\Omega(N^3).}
\]

The statements hold along the constructed length sequence. Since successive lengths have bounded ratio, the worst case over lengths at most \(N\) extends them to all sufficiently large budgets \(N\).

The separate decision family has \(P=2^k\), \(H=k\), \(D=\Theta(k\log k)\), giving

\[
\boxed{T_{\rm decision}=\Omega(N^2/\log N),\quad
CM_{\rm code,decision}=\Omega(N^3/\log^2N).}
\]

For repeated-clause padding of the matching family, keep \(n=2k+5\), let \(m\ge2n-5\), and insert repetitions of an already enforced domain clause in the common middle. The outside blocks have \(n\) clauses, so

\[
D=3(m-n)w-1=\Theta(m\log n),\qquad H=\Theta(n\log n).
\]

Consequently

\[
\boxed{T=\Omega(mn\log^2n),\quad
CM_{\rm code}=\Omega(mn^2\log^3n)}
\]

for fixed \(Q\). The equalities with \(N^2,N^3\) apply to the sparse regime, not arbitrary larger \(m\).

For a cap \(T=O(n^c)\), this family requires \(m=O(n^{c-1}/\log^2n)\). Choosing larger \(m\) also enlarges \(N\), so it does not defeat every polynomial cap in total encoded length.

### 8.7 Qualified future-live variant

The archive also permits charging only current tape values that will be read before overwrite or survive unchanged into final observable output, with their positions, support, control, and head information. Prefix plus this location-charged snapshot is injective by a first-differing-read argument.

This is an analytical measure using the actual future. It is not a free liveness algorithm, an ordinary workspace convention excluding input, or a data-transfer bound. Output values surviving unread must be included.

## 9. Exact Boolean universality inside the symmetric template

The CM continuation provides a direct reduction from arbitrary OR/NOT Boolean circuits.

For every base wire \(B\), introduce fresh \(U_2,U_3,U_4\) and impose

\[
\mathcal B(B)=\bigwedge_{j=2}^4 C(a_j,B,U_j).
\]

This restricts \(B\) to \(\{a_0,a_1\}\), interpreted as \(0,1\), with exactly two helper extensions for either value.

For NOT, use

\[
C(a_2,P,X)\iff X=\neg P.
\]

For OR, introduce fresh \(Y,Z\) and use

\[
C(a_1,a_2,Y),\ C(a_0,a_1,Z),\
C(a_4,P,Y),\ C(a_3,Q,Z),\ C(X,Y,Z).
\]

The first four clauses uniquely select \(Y=a_3\) or \(a_0\) according as \(P=0\) or \(1\), and \(Z=a_4\) or \(a_2\) according as \(Q=0\) or \(1\). The final clause enforces \(X=P\lor Q\). Pin the circuit output with \(C(a_0,a_2,O)\).

For a circuit with \(p\) inputs, \(g_\lor\) OR gates, \(g_\neg\) NOT gates, and \(b=p+g_\lor+g_\neg\) base wires:

\[
n_{T5}=5+4b+2g_\lor,\qquad
m_{T5}=6+3b+5g_\lor+g_\neg,
\]

\[
\boxed{Z(F_{\mathcal C})=10\,2^b\,\#CircuitSAT(\mathcal C).}
\]

The multiplier is known and independent of the accepting input. Every accepting input uniquely fixes base wires and OR helpers. Only the balanced domain helpers and anchor symmetry supply multiplicity.

The reduction is linear in variables and clauses, and \(O((p+g)\log(p+g))\) in the chosen bit encoding. It gives satisfiability equivalence, NP membership and NP-completeness using standard Boolean SAT completeness [15], and a known-multiplier exact-counting reduction. It is not claimed to be parsimonious without the multiplier.

The two-\(R\)-clause conversion transfers these facts to the ordered relation with constant-factor size growth.

## 10. Representation lower bounds and what they actually cover

The matching families above have low width. The representation lower bounds instead use bounded-degree bipartite graphs with linear treewidth, obtainable from suitable expanders. Here \(v\) is graph vertex count and \(N=\Theta(v\log v)\).

Define the independent-set witness predicate

\[
f_G(x)=\bigwedge_{uv\in E}(\neg x_u\lor\neg x_v).
\]

### 10.1 All-field cut rank

Suppose every balanced vertex cut has at least \(\beta v\) crossing edges and maximum degree is \(\Delta\). Greedily extract a crossing induced matching of size at least \(\lfloor\beta v/(2\Delta^2)\rfloor\). Fix unmatched vertices to zero.

The resulting assignment submatrix is

\[
\begin{pmatrix}1&1\\1&0\end{pmatrix}^{\otimes k}.
\]

Its rank is \(2^k\) over every field because the base determinant is \(-1\). Therefore any separated sum across that cut, even with signs and cancellation, needs exponentially many terms. A binary tree tensor representation with one original graph variable per leaf has a balanced edge and therefore an exponential bond there.

This is a lower bound for the specified separated or tree representation. A cyclic network of the original local NAND factors remains compact. High rank does not force an unrestricted scalar algorithm to materialize a rank decomposition.

### 10.2 DNNF

A DNNF is an AND/OR circuit with negation only on inputs and disjoint variable supports at every AND. DAG sharing is allowed.

Published bounded-degree, bounded-arity monotone-CNF results give a DNNF lower bound exponential in treewidth [2]. Complement every graph input variable to transfer the result to \(f_G\):

\[
\boxed{DNNFsize(f_G)\ge2^{c_\Delta\operatorname{tw}(G)}.}
\]

For linear-width bounded-degree graphs,

\[
DNNFsize(f_G)=2^{\Omega(v)}
=2^{\Omega(N/\log N)}.
\]

The full three-bit-encoded T5 witness relation inherits this lower bound by conditioning the anchors and existentially forgetting all but each graph variable's selection bit. Conditioning and forgetting preserve DNNF size up to no increase.

An explicit compiler producing such a representation must take at least output-linear time. That is a genuine superpolynomial task lower bound. A scalar counter's specification does not require this output.

### 10.3 Positive multivariate arithmetic

Consider

\[
P_G(u,v)=\sum_{I\text{ independent}}
\prod_{i\notin I}u_i\prod_{i\in I}v_i.
\]

In a circuit using addition, multiplication, and nonnegative constants, remove zero and unused gates. Positivity prevents cancellation. Any overlap in vertex supports at a useful product would create a monomial using a vertex twice, which cannot occur in the output polynomial.

Thus useful products have disjoint vertex supports. Replace addition by OR, multiplication by AND, \(u_i\) by \(\neg x_i\), \(v_i\) by \(x_i\), and positive constants by true. This yields a DNNF of comparable size. Therefore positive symbolic arithmetic for the full polynomial also requires exponential size.

The ordinary independence polynomial

\[
I_G(z)=\sum_{I\text{ independent}}\prod_{i\in I}z_i
\]

can be converted to the two-weight polynomial with polynomial overhead by padding missing \(u_i\)'s at additions. The same lower bound follows.

This concerns formal multivariate computation over all weights. It does not lower-bound computing the single value \(I_G(1,\ldots,1)\). Negative constants, subtraction, cancellation, and numerical specialization are outside this argument.

## 11. Parameterized unavoidable progress for adaptive recursion

Normalize

\[
w(H)=\max\{0,\operatorname{tw}(H)\},\qquad w(\varnothing)=0.
\]

For degree bound \(\Delta\ge1\), let \(\rho_\Delta>1\) solve

\[
\rho_\Delta^{-1}+\rho_\Delta^{-(\Delta+1)}=1.
\]

For \(\Delta=3\), \(\rho_3=1.38027756909761411567\ldots\).

### 11.1 Deletion inequality

Adding a deleted set \(S\) to every bag of a tree decomposition of \(H-S\) proves

\[
w(H-S)\ge w(H)-|S|.
\]

### 11.2 Branch and component inequalities

The independent-set recurrence is

\[
Z(H)=Z(H-u)+Z(H-N_H[u]).
\]

Since \(|N_H[u]|\le\Delta+1\),

\[
\rho^{w(H-u)}+\rho^{w(H-N[u])}\ge\rho^{w(H)}.
\]

For connected components \(H_i\), \(w(H)=\max_iw(H_i)\), so

\[
\sum_i\rho^{w(H_i)}\ge\rho^{w(H)}.
\]

### 11.3 Frontier conservation

For an uncached recursion tree, arbitrary adaptive branching and component decomposition preserve the total pending weight. If terminal \(\lambda\) has certified width at most \(\kappa_\lambda\),

\[
\boxed{\sum_\lambda\rho^{\kappa_\lambda}\ge\rho^{w(G)}.}
\]

Equivalently, completed terminal allowance plus pending potential never falls below \(\rho^{w(G)}\).

If every terminal has width at most \(\kappa\), then

\[
L\ge\rho^{w(G)-\kappa}.
\]

For polynomially many terminals, some terminal must retain width \(w(G)-O(\log N)\).

### 11.4 Switching parameters

Useful structural certificates include:

| Terminal parameter | Width certificate |
|---|---:|
| Treewidth \(t\) | \(w\le t\) |
| Vertex-cover size \(c\) | \(w\le c\) |
| Feedback-vertex-set size \(f\) | \(w\le f+1\) |
| \(r\ge1\) remaining vertices | \(w\le r-1\) |

If terminal mode \(i\) certifies \(w\le b_i(k)\), the theorem becomes

\[
\sum_\lambda\rho^{b_{i_\lambda}(k_\lambda)}
\ge\rho^{w(G)}.
\]

This is a common structural potential, so choosing a different parameter adaptively is allowed.

Separate potentials cannot simply be minimized. For example, let each of two parent potentials equal \(M+1\), with child values \((M,1)\) and \((1,M)\). Both separately conserve their sum, but their pointwise minimum gives children totaling \(2\). A portfolio needs a common potential or a charged conversion.

### 11.5 Exact limitation

An \(O^*(2^k)\) algorithmic upper bound is not an \(\Omega(2^k)\) per-instance lower bound. A terminal could have an algebraic shortcut. Actual terminal work must be independently bounded below before converting structural conservation into time.

Likewise, an uncached tree cannot be charged as if every occurrence remained distinct work under memoization. The next section handles specified DAG sharing.

Fast transforms illustrate why apparent combinations are not necessarily separate compulsory operations: Slivovsky and Szeider reduce a naive \(4^k\) incidence-treewidth factor to \(2^k\) using zeta transforms and covering products [8].

## 12. Memoization, complement, DLDD, and typed completion

### 12.1 Lifting compatible counting DAGs to representations

An include/exclude graph branch lifts to

\[
f_H=
(\neg x_u\land f_{H-u})
\lor
\left(x_u\land\bigwedge_{z\in N(u)}\neg x_z
\land f_{H-N[u]}\right).
\]

Component products lift to decomposable AND. Identical relations on identical original named scopes may share pointers.

If a compatible DAG has \(R\) records and wires and distinct terminal relation diagrams of sizes \(B_i\), then

\[
DNNFsize(f_G)\le O\!\left(vR+\sum_iB_i\right).
\]

Equal scalar counts do not make two predicates interchangeable. Relabeling templates, isomorphic subproblems, and different variable scopes require a further analysis.

### 12.2 Why plain DNNF progress fails under complement

Although \(f_G\) can have exponential DNNF size,

\[
\neg f_G=\bigvee_{uv\in E}(x_u\land x_v)
\]

has a small ordinary DNF, hence a small DNNF. Once a counter knows the complemented count \(z\), it computes \(2^v-z\) cheaply.

Counting that overlapping DNF need not be easy. The counterexample instead shows that a local DNNF progress rule cannot charge complement as a small operation while ignoring its representation effect. Taking the minimum of the two polarity sizes makes complement cheap but destroys the starting lower bound.

### 12.3 DLDD permits complement

DLDDs allow constants, read-once variable decisions, unary internal NOT, arbitrary binary Boolean operations on disjoint variable scopes, and DAG sharing. The 2017 Beame–Li–Roy–Suciu result gives

\[
s\text{-node DLDD}\ \Longrightarrow\
2^{O((\log s)^2)}\text{-node FBDD}.
\]

FBDDs convert to DNNF linearly. Combining with the graph lower bound [2,3],

\[
\boxed{DLDDsize(f_G)\ge2^{c'_\Delta\sqrt{w(G)}}.}
\]

For linear-width graphs this is \(2^{\Omega(\sqrt{N/\log N})}\). Complement changes DLDD size by at most one.

The count of a DLDD is computed by probability identities. For disjoint functions \(f,g\), the probability of any binary operator \(h\) is

\[
\sum_{a,b\in\{0,1\}}h(a,b)\Pr[f=a]\Pr[g=b].
\]

NOT sends \(p\) to \(1-p\). A decision on a variable absent from its children uses \((p_0+p_1)/2\). Scopes and free-variable factors must be tracked.

The broader class allowing arbitrary deterministic OR, decomposable AND, and internal NOT is not automatically covered by this DLDD theorem. No required general lower bound for that broader class was proved here.

### 12.4 Completion potential

Let a typed library \(\mathcal K\) contain resolved entries \((g,S_g,Z_g)\): a named relation, its fixed original-variable scope, and its exact count.

Define

\[
R_F(\mathcal K)=
\min\{\text{additional DLDD nodes needed to represent }F
\text{ using available handles}\}.
\]

Let \(\kappa(g\mid\mathcal K)\) be the extension size needed to construct a new relation handle. Substituting one shared construction into an optimal later completion proves

\[
\boxed{R_F(\mathcal K)-R_F(\mathcal K\cup\{g\})
\le\kappa(g\mid\mathcal K).}
\]

Native NOT, decision, and disjoint-scope binary operations have constant extension cost; same-relation reuse has zero cost. Merely changing a parameter does not create progress. Deleting cached information cannot decrease the remaining completion requirement.

Initially \(R_F(\varnothing)\ge DLDDsize(F)-O(v)\); once the target handle is resolved, the remaining requirement is zero.

### 12.5 The exact shortcut defect

Partition actual computation into disjoint charged actions of cost \(q_j\ge1\), with \(W=\sum_jq_j\), and use joint extension costs for actions producing several handles. Then

\[
R_F(\varnothing)\le\sum_j\kappa_j.
\]

For any fixed baseline \(c\),

\[
R_F(\varnothing)\le cW+\sum_j[\kappa_j-cq_j]_+.
\]

Define

\[
\alpha=\max\left\{1,\max_j\frac{\kappa_j}{q_j}\right\}.
\]

The derived progress theorem is

\[
\boxed{\alpha W+O(v)\ge2^{c'_\Delta\sqrt{w(G)}}.}
\]

Native DLDD computations have \(\alpha=O(1)\), giving a superpolynomial architecture lower bound. No polynomial bound on \(\alpha\) for arbitrary scalar counters has been proved.

The entire unrestricted algorithm can be treated as one macro action. Its extension cost may then be enormous. The theorem still holds, but does not lower-bound actual runtime without control of that cost.

Under \(W\le KN^a\) and \(\alpha\le N^b\),

\[
w(G)=O((a+b+1)^2\log^2N).
\]

This is a necessary condition under the stated assumptions, not a general characterization of easy counting instances.

### 12.6 Parameterized terminals with sharing

A nice primal tree decomposition of width \(t\) with \(q\) bags yields a decision-DNNF with \(O(q2^{t+1})\) nodes: bag assignments index subcircuits; forget nodes give decisions; joins combine disjoint interiors.

If terminal modes yield sizes \(B_i\le Cv^d2^{\beta_i k_i}\), compatible DAG accounting gives

\[
\log(R+1)+\max_i\beta_i k_i+O(\log v)
\ge c'_\Delta\sqrt{w(G)}.
\]

This handles shared compatible work and heterogeneous parameters, while retaining the explicit limitation on unrestricted shortcuts.

## 13. Counterexamples every proposed universal bridge must survive

### 13.1 Exponentially many residuals on a tree

Let left vertices be \(X_1,\ldots,X_r\), each with a private right leaf \(P_i\), and add right connectors \(B_i\) adjacent to \(X_i,X_{i+1}\). The graph is a tree with \(3r-1\) vertices and maximum degree three.

Every left subset has a different right neighborhood because the private leaves identify it. There are \(2^r\) distinct residual functions.

Nevertheless the independent-set count satisfies

\[
z_0=1,\quad z_1=3,\quad z_r=5z_{r-1}-2z_{r-2},
\]

with values \(3,13,59,269,1227,5597,\ldots\). A two-state transfer matrix computes it in polynomial bit complexity.

In general, for a bipartite graph,

\[
\#IS(G)=\sum_{S\subseteq L}2^{|R|-|N(S)|}.
\]

Different residual functions may have the same scalar count. The unresolved task is computing the multiplicities of neighborhood sizes, not proving that many subsets exist.

### 13.2 High-width parity systems with easy counts

For a graph with edge variables, impose at each vertex

\[
\bigoplus_{e\ni u}x_e=c(u).
\]

The system is satisfiable exactly when the charge sum is even on every component. For a satisfiable system,

\[
\boxed{Z=2^{|E|-|V|+\operatorname{cc}(G)}.}
\]

Linear algebra or a spanning-tree construction counts and samples efficiently. Published results nevertheless give exponential DNNF requirements on bounded-degree, linear-width families [4,5]. The DLDD simulation implies superpolynomial DLDD requirements too.

This refutes a generic polynomial scalar-counting-to-witness-compilation ratio. A correct all-input solver can recognize the explicit affine subclass, solve it algebraically, and use exhaustive search elsewhere.

The Boolean-circuit-to-T5 reduction embeds this control inside general strict T5. With \(b\) base wires, its count is

\[
10\,2^{b+|E|-|V|+\operatorname{cc}(G)}.
\]

Conditioning and projecting its witness relation recovers the original Tseitin relation, so large witness-representation complexity survives. This does not refute a new bridge specific to the narrower NAND graph family, but it rules out an unrestricted generic bridge based only on witness width or representation size.

### 13.3 Syntactic width can survive trivial forced domains

In the NAND graph construction, adding \(C(a_2,a_3,Z)\) to every graph variable forces left variables to \(a_4\) and right variables to \(a_1\). All edges become satisfied and the count is ten.

The raw incidence or primal graph can retain large width until domain propagation removes forced variables. Any hardness claim using only unprocessed syntactic width must account for this.

### 13.4 Relocating all computation beyond the original cuts

For every correct sole-tape counter \(A\), the continuation constructs a correct \(B\) with

\[
T_B(x)=O_A(T_A(x)+N^2).
\]

\(B\) copies the input beyond the original region, simulates \(A\) there, preserves the answer, erases other state, and transports the answer back. Initialization and final output transport cross each original boundary only \(O(N)\) times. At those events complete configurations have \(O(N)\)-bit descriptions.

Therefore the **selected minimum-description charge at original input cuts** is at most \(O_A(N^3)\), regardless of how large the remote computation's total CM may be. This is an upper bound for \(\sum_{t\in E_{\rm orig}}K(C_t\mid B)\), or for an explicitly chosen compact current-configuration code. It is not an upper bound for every faithful code or physical storage convention. In particular, a convention charging all ever-visited cells can continue charging a large erased remote region.

For any cap exponent \(a\ge2\), this wrapper preserves \(O(N^a)\). A universal refutation of such caps cannot force supercubic minimum-description CM solely at the old fixed cuts. Dynamic cuts must cover subsequent joint computation and justify that spliced states are reachable from valid inputs.

### 13.5 Decision-diagonal witness packing

Suppose \(L_u\land\Gamma\land R_v\) uses the same \(n\) variables over a \(q\)-element domain, every diagonal is satisfiable, and every off-diagonal is unsatisfiable.

The diagonal witness sets are pairwise disjoint: a shared witness would satisfy both hybrids. Hence

\[
\sum_u Z(L_u\land\Gamma\land R_u)\le Z(\Gamma)\le q^n.
\]

If every diagonal has \(z\) witnesses, then \(Pz\le q^n\), so

\[
\log_2P\le n\log_2q-\log_2z.
\]

For T5, a \(k!\)-sized SAT-diagonal/UNSAT-off-diagonal family needs \(n=\Omega(k\log k)\). It cannot retain the \(n=\Theta(k)\) count-only matching parameters. The theorem does not cover the opposite orientation with unsatisfiable diagonals.

## 14. Entropy: valid statements and the full-state obstruction

Let \(X\) be a random permitted \(N\)-bit instance and \(Y=Z(X)\).

\[
H(X)\le N,\qquad H(Y\mid X)=0.
\]

For a deterministic solver correct on every input, a complete current configuration determines its continuation and output. Therefore

\[
\boxed{H(Y\mid C_t)=0.}
\]

This is true even when extracting the output computationally is difficult. Ordinary conditional entropy cannot serve as “remaining work” for a complete state.

If \(W(X)\) is the exponentially long vector of witness indicators, then

\[
H(W(X))\le H(X)\le N.
\]

Its coordinate entropies cannot be added as if the coordinates were independent. The full deterministic trace, including the input, also has entropy \(H(X)\). A sum of marginal configuration entropies can count repeated retention; it is not fresh information.

### Witness entropy

For a uniform witness \(U\) of one fixed satisfiable instance,

\[
H(U)=\log_2Z.
\]

For a bipartite graph with \(v\) vertices, one side has size at least \(v/2\) and every subset of that side is independent:

\[
2^{v/2}\le Z\le2^v,\qquad v/2\le H(U)\le v.
\]

This large entropy occurs on easy families too. For a connected cubic Tseitin graph with \(q\) vertices, the witness entropy is \(q/2+1\), yet counting is polynomial.

The branch identity

\[
\log Z=h_2(p)+p\log Z_0+(1-p)\log Z_1,\qquad p=Z_0/Z,
\]

describes the entropy of one randomly chosen branch followed by one witness. It does not prove the cost of evaluating both branch counts or the entire recursion tree.

For a satisfiable affine system with incidence matrix \(M\) and edge partition \(A,B\),

\[
I(U_A;U_B)=\operatorname{rank}(M_A)+\operatorname{rank}(M_B)
-\operatorname{rank}(M).
\]

This mutual information can be linear while a change of algebraic coordinates makes counting easy.

Exact counting also supports exact uniform sampling through a uniform rank and sequential unranking with at most one residual-count query per variable. Counting-to-sampling connections are classical [14]. The random-bit requirement alone can be only linear; it does not establish exponential arithmetic work.

## 15. A bounded-reuse entropy-transfer lemma

The useful entropy target is a set of actual reconstruction obligations.

Let \(U_j\) be required information, \(B_j\) the decoder's side information, and \(\Pi_j\) a conditionally prefix-free record satisfying

\[
H(U_j\mid B_j,\Pi_j)=0.
\]

Suppose a real charged event set \(E_j\) supports the record,

\[
|\Pi_j|\le b|E_j|+h_j,
\]

and every physical event belongs to at most \(r\) of these sets. Source coding and double counting give

\[
\sum_jH(U_j\mid B_j)
\le br\,\mathbb E[T]+\sum_j\mathbb E[h_j],
\]

or

\[
\boxed{
\mathbb E[T]\ge
\frac{\sum_jH(U_j\mid B_j)-\sum_j\mathbb E[h_j]}{br}.
}
\]

No independence assumption between demands is required. The reuse factor controls repeated charging.

Records must include whatever the decoder needs: values, addresses, task identities, termination or lengths, relevant registers, and timing if the model exposes it. Side information must include retained input and caches. On a bounded-word RAM under a polynomial resource cap, a record may cost \(O(\log N)\) bits per event; this is not a model-free constant.

Information-transfer arguments of this kind are established in dynamic data structures [7]. Online updates and queries there provide genuine required services. A static counter asked for one aggregate answer does not automatically provide analogous residual-query services.

The current matching proof uses external crossing transcripts indexed by a common random permutation, with one physical movement charged at one cut. It must not use \(H(\pi\mid\text{the other side's }\pi)\), which is zero on the diagonal distribution.

The missing unrestricted theorem would provide compulsory demands whose total conditional entropy exceeds the allowed \(brT\), while surviving relocation, cached information, symbolic aggregation, and algebraic shortcuts.

## 16. Conditional pseudoentropy as a possible unrestricted route

Ordinary entropy ignores computational effort. A computational version asks whether resource-bounded tests can distinguish the correct answer from an alternative answer with additional conditional uncertainty.

Let \(Y=f(X)\), and let \(\widetilde Y\) take values in the same finite alphabet of size \(M\), with the same input marginal. Suppose every distinguisher in a budget has advantage at most \(\varepsilon\) between \((X,Y)\) and \((X,\widetilde Y)\).

An exact solver \(A\) gives the equality test

\[
D_A(x,z)=[A(x)=z].
\]

It accepts true pairs with probability one. Let \(p=\Pr[\widetilde Y\ne f(X)]\). If this whole equality test fits the distinguisher budget, then \(p\le\varepsilon\).

An error-flag encoding yields

\[
H(\widetilde Y\mid X)\le h_2(p)+p\log_2(M-1).
\]

Thus, for \(0\le\varepsilon\le1-1/M\),

\[
\boxed{
H(\widetilde Y\mid X)>
h_2(\varepsilon)+\varepsilon\log_2(M-1)
}
\]

excludes that exact solver.

For normalized independent-set counts, use \(M=2^v+1\), \(v\ge1\), and

\[
\varepsilon=\frac1{100(v+1)},\qquad
H(\widetilde Y\mid X)\ge1.
\]

The threshold is below \(h_2(0.005)+0.01<0.06\), so one bit is sufficient numerically.

The average conditional min-entropy variant is also useful:

\[
\widetilde H_\infty(\widetilde Y\mid X)
=-\log_2\mathbb E_X\max_y\Pr[\widetilde Y=y\mid X].
\]

If this is at least one, every deterministic proposed answer matches with probability at most one half, so an exact solver gives distinguishing advantage at least one half. Do not replace this definition by the expectation of pointwise min-entropies.

The central premise has not been proved: no target-family fake-count distribution with the required indistinguishability against all cap-sized algorithms or circuits has been constructed.

Vadhan and Zheng develop conditional pseudoentropy [6]. Their specific sampling-hardness equivalence assumes a polynomial-sized output range; it cannot be invoked directly for a complete count with exponentially many possible values. The elementary equality-comparator implication above works for any finite alphabet.

## 17. The correct unrestricted circuit target

Three different functions must remain separate.

1. For fixed \(G\), the witness predicate \(x\mapsto f_G(x)\) has a small ordinary unrestricted circuit, essentially its original CNF.
2. For fixed \(G\), its scalar count \(Z(G)\) is a constant and can be hardwired. This does not charge discovering that constant.
3. Across all permitted \(N\)-bit instances, \(\operatorname{Count}_N:\operatorname{Enc}(F)\mapsto Z(F)\) is the relevant counting function.

Let \(C_N\) be the minimum number of noninput gates in one circuit computing the third map on every permitted encoding at length \(N\), with padded \(O(N)\)-bit outputs. Behavior outside the permitted domain may be arbitrary. Use a fixed fan-in-two AND/OR/NOT basis with unrestricted sharing and fanout.

The DNNF/DLDD lower bounds concern the first function in restricted circuit classes. They do not lower-bound \(C_N\).

### 17.1 Simulation ceilings

A direct local tableau with width \(O_A(S)\) and depth \(O_A(T)\) gives

\[
C_N\le O_A(TS)\le O_A(T(N+T)).
\]

Pippenger and Fischer give the sharper time-to-network simulation [1]. After input/output normalization,

\[
\boxed{C_N\le O_A((N+T)\log(N+T+2)).}
\]

For \(T\ge N\),

\[
\boxed{C_N\le O_A(T\log(T+2)).}
\]

The solver need not explicitly construct this circuit. It is an all-input representation of the computation.

The small-size simulation and the original-space tableau are alternative constructions. Do not assert that one simultaneously has the best size and width bounds without another theorem.

### 17.2 Lower-bound transfer

If \(C_N\ge L(N)\), then for \(T\ge N\),

\[
\boxed{T_A(N)=\Omega_A(L(N)/\log(L(N)+2)).}
\]

Without \(T\ge N\), the same conclusion holds when \(L(N)=\omega(N\log(N+2))\), after retaining the input term.

The implication cannot be reversed. A time lower bound does not establish a circuit lower bound.

## 18. Distinct configurations and the circuit-to-CM bridge

A deterministic halting run never repeats a complete configuration. A repeat would force the same future forever.

The shortest total length of injective binary descriptions of \(T\) distinct objects is

\[
rT-2^{r+1}+r+2,\qquad r=\lfloor\log_2(T+1)\rfloor,
\]

and therefore at least \(T\log_2T-O(T)\). Prefix-free descriptions satisfy the sharper lower bound \(T\log_2T\) by Kraft and Jensen.

Thus a worst-time input gives

\[
\boxed{M_{\min,A}(N)\ge T_A(N)\log_2T_A(N)-O_A(T_A(N)).}
\]

Combining this with the sharp simulation, for \(T\ge N\),

\[
C_N\le O_A(M_{\min,A})
\le O_A(M_{\rm phys,A}).
\]

In general a safe form is

\[
C_N\le O_A(N\log(N+2)+M_{\min,A}).
\]

Hence a sufficiently large unrestricted circuit lower bound gives

\[
\boxed{
T_A=\Omega_A(L/\log L),\qquad
M_{\min,A}=\Omega_A(L),\qquad
M_{\rm phys,A}=\Omega_A(L).
}
\]

Use \(T\ge N\) or \(L=\omega(N\log N)\) as above.

This proof does not interchange

\[
\max_x\sum_t s_t(x)
\quad\text{and}\quad
\sum_t\max_xs_t(x).
\]

The first can be smaller. A naive all-input tableau-area argument would not establish the desired per-run CM bound. The distinct-configuration proof avoids that error.

### Decoder conventions matter

With prefix complexity and the input freely supplied,

\[
\sum_tK(C_t\mid A,x)=T\log_2T+O(T).
\]

If both \(x\) and \(t\) are free, each state is \(O(1)\)-describable by replay. Neither measure is the self-contained input-charged CM used in the cubic crossing theorem.

For a uniformly computable sequence \(x_N\), \(K(x_N\mid A)=O(\log N)\), even if generating it is slow. Such a sequence cannot witness cubic minimum-description CM for an \(O(N^2)\)-time matching solver. The theorem is worst-case or high-probability over inputs, not a claim that a simple explicit diagonal sequence attains every descriptive lower bound.

At polynomial versus superpolynomial scale, the proved transfers make \(T\), physical CM, and self-contained descriptive CM equivalent for this model. They offer different proof targets; their coexistence is not extra independent hardness.

## 19. An unrestricted Boolean completion potential

Let \(\mathcal K\) contain Boolean functions of the original formula-encoding bits that are available as circuit handles. Define

\[
R_N(\mathcal K)=
\min\{\text{additional unrestricted Boolean gates needed for }
\operatorname{Count}_N\}.
\]

Inputs and constants are available; arbitrary overlaps and sharing are allowed. If \(\kappa_{\rm Bool}(g\mid\mathcal K)\) gates construct \(g\), shared substitution proves

\[
\boxed{
R_N(\mathcal K)-R_N(\mathcal K\cup\{g\})
\le\kappa_{\rm Bool}(g\mid\mathcal K).
}
\]

Each actual Boolean gate has extension cost at most one. Initially \(R_N(\varnothing)=C_N\); at completion it is zero.

Apply this to an all-input circuit, such as the machine simulation. A single input-dependent execution path is not automatically a circuit correct on every input.

This yields the precise contrast:

| Potential | Large starting value | Local progress coverage |
|---|---|---|
| Typed DLDD completion of a fixed witness relation | Proved on high-width graph families | Native operations; arbitrary shortcuts uncontrolled |
| Unrestricted Boolean completion of the encoded count map | Desired lower bound unproved | All Boolean gates |

One cannot combine the first row's starting bound with the second row's progress rule.

## 20. Combining entropy, circuits, time, space, and CM correctly

### 20.1 Cap ledger

For \(T_A=O(N^a)\), \(a\ge1\):

| Resource | Necessary ceiling |
|---|---:|
| Peak total physical storage | \(O(N^a)\) |
| Physical CM | \(O(N^{2a})\) |
| Self-contained minimum-description CM | \(O(N^{a+1})\) |
| Unrestricted count-circuit gates | \(O(N^a\log N)\) |
| Ordinary explicit encoding of that circuit | \(O(N^a\log^2N)\) bits |

Gate count is not the Shannon entropy or Kolmogorov complexity of the circuit description. Large structured circuits may have short generators.

A count-circuit bound \(C_N=\omega(N^a\log N)\), for example \(\Omega(N^{a+\varepsilon})\), defeats an \(O(N^a)\) cap. A bound only \(\Omega(N^a)\) does not do so through the logarithmic-overhead simulation.

For an \(O(N^3)\) cap, the ceilings are \(S=O(N^3)\), physical CM \(O(N^6)\), descriptive CM \(O(N^4)\), and count-circuit size \(O(N^3\log N)\). The existing sparse matching demands \(T=\Omega(N^2)\), CM \(=\Omega(N^3)\) fit below these ceilings.

### 20.2 Pseudoentropy to circuits

If the true/fake pair is \(\varepsilon\)-indistinguishable against circuits of at most \(B(N)\) gates and has the conditional entropy gap in Section 16, an exact count circuit plus an \(O(\ell(N))\)-gate equality comparator would contradict indistinguishability.

Therefore

\[
C_N>B(N)-O(\ell(N)).
\]

For \(B\gg N\log N\), this transfers to

\[
T=\Omega(B/\log B),\qquad M_{\min},M_{\rm phys}=\Omega(B).
\]

A superpolynomial \(B\) would complete an unrestricted counting route. Proving the indistinguishability premise is the missing problem-specific theorem.

### 20.3 Entropy and circuit demands normally combine by maximum

If \(\mathcal I_N\) is the proved entropy demand after record overhead, and \(C_N\ge L(N)\), then

\[
T_A(N)\ge
\max\left\{\frac{\mathcal I_N}{br},
\ \Omega_A(L(N)/\log(L(N)+2))\right\}.
\]

Adding or multiplying separate demands requires disjointness, bounded overlap, or a stronger scheduling theorem. The same operations may satisfy several resource accounts.

### 20.4 Space-sensitive circuit tradeoffs

Let \(C_N^{\le W}\) minimize size among layered count circuits of width at most \(W\), with wires between consecutive layers, buffers counted, and original inputs appearing only in layer zero.

The tableau gives

\[
C_N^{\le c_AS}\le O_A(TS).
\]

Thus a lower bound \(C_N^{\le W}\ge L(N,W)\) implies

\[
TS\ge\Omega_A(L(N,c_AS)).
\]

This is computational width, not treewidth of the input witness relation. Taking time from one simulation and space from a different slower simulation is invalid without a simultaneous guarantee.

## 21. Uniform discovery and external time-space context

General circuit families are nonuniform. Each length can have its own circuit without charging how it was found. A superpolynomial general count-circuit lower bound is stronger than necessary to exclude a uniform polynomial-time counter.

An equivalent uniform target is to rule out polynomial-time generation and evaluation of polynomial-size count circuits. A fixed polynomial-time counter gives a uniform polynomial tableau compiler; a polynomial generator followed by polynomial evaluation gives a polynomial counter.

This preserves the user's concern about charging discovery, selection, and compilation. It still needs an independent lower bound. Defining discovery cost to equal the unknown optimal counting time would be circular.

Established SAT time-space theorems illustrate legitimate simultaneous tradeoffs, not an already available superpolynomial separation:

- Fortnow, Lipton, van Melkebeek, and Viglas exclude \(N^c\) time together with sufficiently small \(N^d\) workspace for each \(c<\phi=(1+\sqrt5)/2\), in their random-access model [9].
- Williams's valid \(2\cos(\pi/7)\approx1.80194\) exponent is a time lower bound under subpolynomial workspace, and also under sufficiently small positive workspace exponents depending on \(c\) [11].
- An older claimed general product exponent \(1.801\) was retracted in the updated alternation-trading manuscript. Its Theorem 4.11 gives \(t(N)s(N)=\Omega(N^{\phi-\varepsilon})\) for polynomially bounded \(t,s\), under the paper's conventions [10].

These papers use workspace conventions distinct from input-charged total tape storage. Specific exponent transfers to T5 require a resource-efficient reduction, not merely NP-completeness.

## 22. Earlier project branches that constrain further work

Several earlier files contain controls worth preserving. They are not being promoted into unrestricted lower bounds.

### Replay obstruction for witness-liftable amplification

The earlier PROOF_NOTE proves that iterating a fixed polynomially witness-liftable transformation from one fixed solved seed gives a polynomial witness-finding replay program along that orbit. Increasing formula size or a restricted representation measure does not force universal witness-search hardness along the same orbit.

Its collision wrapper has deterministic oracle query complexity \(2^r+1\), but an oracle lower bound does not automatically apply to an algorithm given succinct circuit syntax. Fixed-width hashes have fixed output range and cannot yield an asymptotic separation merely by repeatedly hashing.

### Representation expansion and parity

Charged access records that auxiliary-free CNF for a parity projection can require \(2^{k-1}\) clauses while the same relation has one affine equation or a linear-size ordered decision diagram. Selection of a useful representation and replay of an already chosen one are different costs.

### Conditional resource contraction

The resource-contraction draft gives a recurrence conditional on a suitable supplied separator layout and a one-level solver. It does not prove universal availability, cheap discovery, or recursive closure of such layouts. A universal recursively composable splitter with a forbidden time-space endpoint would itself need the missing theorem.

The project also contains boundary-DAG, contextual-pruning, universal-witness-insufficiency, PC22 transfer, and block-protection drafts. Their presence is a record of explored directions. No unproved universal bridge in those drafts should override the theorem scopes and counterexamples in this handoff.

## 23. Errors and unsupported inferences to avoid

1. Do not turn \(2^n\) assignments into \(2^n\) compulsory steps.
2. Do not confuse syntax information, witness entropy, output information, and computational difficulty.
3. Do not silently switch symmetric \(C\) and ordered \(R\).
4. Do not merge the original \(10\cdot2^{c(\pi^{-1}\sigma)}\) matching family with the later NAND matching family.
5. Do not treat the low-width matching family and high-width expander family as the same instances.
6. Do not apply a diagonal promise algorithm where the crossing proof requires hybrid correctness.
7. Do not choose a different hard input at each cut or time and then add the demands.
8. Do not infer CM by multiplying unrelated time and peak-space lower bounds.
9. Do not give input, locations, time, advice, or decoder-specific information away for free.
10. Do not charge the same identifier or stored object twice merely because it has two interpretations.
11. Do not assume every instruction fetch traverses the input.
12. Do not infer a per-instance lower bound from an FPT upper bound.
13. Do not charge an uncached recursion tree to a memoized solver.
14. Do not treat equal-count objects as equal witness relations.
15. Do not assume all scalar algorithms compile efficiently to DNNF or DLDD.
16. Do not extend the DLDD theorem to arbitrary deterministic decomposable circuits with internal complement.
17. Do not transfer a formal multivariate polynomial lower bound to evaluation at all weights one.
18. Do not use \(H(Y\mid C_t)\) as remaining work for complete deterministic states.
19. Do not make virtual residual queries into required services without a decoder theorem.
20. Do not equate circuit gate count with shortest description length.
21. Do not reverse a time-to-circuit upper bound.
22. Do not identify \(\max_x\sum_t\) with \(\sum_t\max_x\).
23. Do not assume polynomial time implies linear space.
24. Do not combine the time of one algorithm with the space of another.
25. Do not amplify variable-count bounds by padding while ignoring the new input length.
26. Do not use an input-dependent program to refute a uniform cap, or a uniform cap to silently charge nonuniform circuit discovery.
27. Do not claim a count-only separation proves \(P\ne NP\).
28. Do not use ETH, SETH, #ETH, cryptographic assumptions, or a lower-bound conjecture as an unconditional premise.
29. Do not describe finite tests as proving an asymptotic lower bound over all machines.
30. Do not claim a historical theorem describes all present or possible model counters.

## 24. Recommended next proof tasks and success criteria

### Task A: extend a restricted shortcut class honestly

Choose a concrete new operation used by scalar counters, such as a particular symmetry quotient, elimination rule, or algebraic transform. Define its interface, physical cost, and effect on the typed completion potential.

Success is a proof controlling its cumulative shortcut defect while retaining the initial lower bound. A stronger restricted theorem is a legitimate result. A generic polynomial defect bound across all Boolean counting problems is already refuted by affine examples.

### Task B: compulsory dynamic information transfer

Fix one solver \(A\), cap \(KN^a\), and distribution or family. Construct actual decoders, side information, records, event charges, and reuse factor. Prove obligations remain necessary after input relocation and arbitrary joint computation.

Success is a lower demand exceeding \(brKN^a\). Counting hypothetical residual questions without proving the solver must answer them does not qualify.

### Task C: the encoded count circuit

Target \(C_N\) directly. The unrestricted gate-completion potential already has the correct local substitution property.

Success is a count-map circuit lower bound exceeding \(N^a\log N\) for the cap under study. A lower bound for fixed-instance verification, DNNF, a tree tensor network, or a positive polynomial is not this theorem.

### Task D: uniform discovery

Formalize an adequate circuit or certificate family and a generation/evaluation task. Seek a lower bound on the complete uniform process, with actual description and access charges.

Success must use a property independent of the desired counting lower bound. It must survive short hardwired answers and efficiently recognizable special subclasses.

### Task E: computational pseudoentropy

Specify \(X_N\) and \(\widetilde Y_N\), including validity and output range. Prove indistinguishability against every circuit or fixed program in the claimed budget, together with the entropy gap.

One conditional entropy bit can be enough. Proving indistinguishability, not producing an artificial random fake answer, is the difficult step.

### Task F: an independent decision path

If the target remains \(P\ne NP\), choose a decision-sensitive family or reduction that actually preserves the relevant hardness and resource budget. The existing pinning family supplies a polynomial tape lower bound; the general circuit reduction supplies NP-completeness. Neither is a superpolynomial decision theorem.

Before accepting any candidate universal lemma, test it on matching cycles, the private-leaf tree, high-width affine systems, forced-domain graph formulas, complemented predicates, relocated inputs, memoized relations, and transformed dynamic-programming tables.

## 25. Verification and reproducibility

The verification scripts check finite identities and implementations, not universal asymptotic hardness.

The original archive verifies ten frames, original matching counts, decision counts, distinct-name syntax, and exact encoding. The continuation verifies balanced Boolean gadgets, joint finite bounds, the private-leaf tree recurrence, and minimum injective description lengths.

The parameterized-progress audit reports:

- 832 induced subgraphs of four test graphs;
- 4,092 exact treewidth deletion, branch, and component checks;
- adaptive heterogeneous terminal counts agreeing with brute force;
- independent-set counts \(47,15,35,80\) for its four test graphs;
- 4,096 Boolean-operator probability checks;
- the parameter-switching counterexample;
- a high-precision value of \(\rho_3\).

The entropy audit reports:

- 1,088 branch-entropy identities;
- 27,131 error-entropy inequalities on finite rational grids;
- 10,000 checks of the illustrative pseudoentropy threshold;
- all 376 charge vectors across six small Tseitin graph examples;
- the expected matching mutual-information value.

The handoff's new semantic audit checks all 125 triples for the exact \(C\)-to-\(R\) conversion, all ten common anchor frames, both graph edge orders, original transport gadgets, decision pinning differences, Boolean gates, 617 permutation pairs through \(k=4\) for both matching families, and 340 decision bitstring pairs.

Complete verifier sources are appended. They use Python's standard library. Prior report output is retained in the source notes; the handoff records checks as finite validation, not evidence that no clever algorithm exists.

## 26. Provenance and source files

The core project records are:

- [T5 Bit Access Accounting source archive](https://chatgpt.com/library?file_id=libfile_639615cb49608191ba0d995ad3b809d5&account_id=personal), 20 November 2026. Contains CROSSING_PROOF, CUMULATIVE_PROOF, INPUT_ENCODING, RESOURCE_LEDGER, prior resource-model notes, and verifiers.
- [CM T5 Continuation](https://chatgpt.com/library?file_id=libfile_5b15e24a9c4c8191b7a29110e2ef7cc3&account_id=personal), 20 November 2026. Adds simultaneous bounds, NAND matching, Boolean universality, representation bounds, counterexamples, relocation, and witness packing.
- [CM Budget Extension](https://chatgpt.com/library?file_id=libfile_ce79026d8f448191a4f290d626b1bca7&account_id=personal), 20 November 2026. The time-cap and padding analysis was supplied in the conversation; this separate note was not independently reread for this handoff.
- [Parameterized Aggregate Progress](https://chatgpt.com/library?file_id=libfile_6b014b0aaa8c81919e054356c46107c6&account_id=personal), 21 November 2026.
- [Entropy and Unrestricted Counting](https://chatgpt.com/library?file_id=libfile_b0573d581d088191ac5f98340866246a&account_id=personal), 21 November 2026.
- [Unified Circuit, Entropy, and CM](https://chatgpt.com/library?file_id=libfile_f758560558688191921972d8783f20a5&account_id=personal), 21 November 2026.

The last three notes give expanded proofs and their original finite-audit outputs. This handoff supersedes ambiguity about predicate definitions and matching-family provenance. It does not silently rewrite the older documents.

Other supplied project sources include Charged access, PROOF_NOTE, resource_contraction_v2, boundary_dag_accounting, contextual-pruning and universal-witness-insufficiency notes, CP22/PC22 reports, random3sat_solver_hierarchy_extended_report, and Block_Protection_GC_Random3CNF_Draft. Selected controls from these are discussed above. Uninspected claims in older drafts are not certified by inclusion in the project.

## 27. Primary references

1. Nicholas Pippenger and Michael J. Fischer. *Relations Among Complexity Measures*. Journal of the ACM 26(2), 361-381, 1979. DOI 10.1145/322123.322138. [Author repository](https://scholarship.claremont.edu/hmc_fac_pub/597/).
2. Antoine Amarilli, Florent Capelli, Mikaël Monet, and Pierre Senellart. *Connecting Knowledge Compilation Classes and Width Parameters*. Corollary 8.5. [Author manuscript](https://arxiv.org/pdf/1811.02944).
3. Paul Beame, Jerry Li, Sudeepa Roy, and Dan Suciu. *Exact Model Counting of Query Expressions: Limitations of Propositional Methods*. ACM TODS 42(1), 2017. Definition 2.4 and Theorem 3.1. [Author manuscript](https://homes.cs.washington.edu/~beame/papers/numsat-journal.pdf).
4. Alexis de Colnet and Stefan Mengel. *Characterizing Tseitin-formulas with Short Regular Resolution Refutations*. 2021. Proposition 2 and Lemma 13. [Primary paper](https://arxiv.org/pdf/2103.09609).
5. Dmitry Itsykson, Artur Riazanov, and Petr Smirnov. *Tight Bounds for Tseitin Formulas*. SAT 2022, LIPIcs 236, Article 6. Lemma 2.16 and Theorem 4.1. [Primary paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol236-sat2022/LIPIcs.SAT.2022.6/LIPIcs.SAT.2022.6.pdf).
6. Salil Vadhan and Colin Jia Zheng. *Characterizing Pseudoentropy and Simplifying Pseudorandom Generator Constructions*. STOC 2012; full version revised 2013. [Primary paper](https://salil.seas.harvard.edu/sites/g/files/omnuum4266/files/salil/files/eccc2013.pdf).
7. Mihai Pătraşcu and Erik D. Demaine. *Logarithmic Lower Bounds in the Cell-Probe Model*. SIAM Journal on Computing 35(4), 932-963, 2006. [Primary paper](https://erikdemaine.org/papers/DynamicConnectivity_SICOMP/paper.pdf).
8. Friedrich Slivovsky and Stefan Szeider. *A Faster Algorithm for Propositional Model Counting Parameterized by Incidence Treewidth*. SAT 2020. [Author manuscript](https://ac.tuwien.ac.at/files/tr/ac-tr-20-006.pdf).
9. Lance Fortnow, Richard Lipton, Dieter van Melkebeek, and Anastasios Viglas. *Time-Space Lower Bounds for Satisfiability*. Journal of the ACM 52(6), 835-865, 2005. [Author manuscript](https://lance.fortnow.com/papers/files/tst.pdf).
10. Ryan Williams. *Alternation-Trading Proofs, Linear Programming, and Lower Bounds*. Updated author manuscript, Theorem 4.11 and correction in footnote 9. [Corrected version](https://people.csail.mit.edu/rrw/automated-lbs.pdf).
11. Ryan Williams. *Time-Space Tradeoffs for Counting NP Solutions Modulo Integers*. Computational Complexity 17, 2008. Theorem 1.2. [Author manuscript](https://www.cs.cmu.edu/~ryanw/mod-lbs-journal-final.pdf).
12. Paul Beame and Niels Kornerup. *Cumulative Memory Lower Bounds for Randomized and Quantum Computation*. ECCC TR23-005, 2023. [Primary paper](https://eccc.weizmann.ac.il/report/2023/005/download/). This supplies general CM context, not the project's exact T5 theorem.
13. Simone Bova, Florent Capelli, Stefan Mengel, and Friedrich Slivovsky. *A Strongly Exponential Separation of DNNFs from CNF Formulas*. 2015, Theorem 4. [Primary paper](https://arxiv.org/pdf/1411.1995).
14. Mark Jerrum, Leslie Valiant, and Vijay Vazirani. *Random Generation of Combinatorial Structures from a Uniform Distribution*. Theoretical Computer Science 43, 169-188, 1986. [Author-hosted paper](https://ics.uci.edu/~vazirani/JVV.pdf).
15. Stephen A. Cook. *The Complexity of Theorem-Proving Procedures*. STOC 1971. [Author's original scan](https://www.cs.toronto.edu/~sacook/homepage/1971.pdf).
16. John Duchi. *Lecture Notes on Statistics and Information Theory*. 2023. Source coding and Fano-type inequalities. [Author notes](https://web.stanford.edu/class/stats311/lecture-notes.pdf).
17. J. Hartmanis. *Computational Complexity of One-Tape Turing Machine Computations*. Journal of the ACM 15(2), 325-339, 1968. DOI 10.1145/321450.321464. This is a classical crossing-sequence source; the T5 family and cumulative extension are project derivations.

## 28. Ready-to-paste continuation instruction

Continue the strict T5 resource-lower-bound project from this handoff. Treat the symmetric ternary relation \(C\), the explicit bit encoding, and the complete deterministic sole-tape configuration model as the audited baseline. If using the ordered tournament relation \(R\), apply the proved \(C(x,y,z)\iff R(x,y,z)\land R(y,x,z)\) conversion or explicitly verify a specialized gadget.

Preserve the distinction between original transport matching, later NAND matching, separate decision pinning, and high-treewidth expander families. The quadratic time and cubic CM crossing theorems are proved model-specific results. The DNNF/DLDD and positive-polynomial lower bounds are representation-specific. The unconditional superpolynomial exact-counting and decision claims remain unproved.

Choose one missing bridge: NAND-specific shortcut-defect control, compulsory dynamic information transfer, unrestricted encoded-count circuit size, uniform circuit discovery, computational pseudoentropy, or a decision-sensitive tradeoff. State its quantifiers, model, demanded lower bound, and cap ceiling before attempting the proof.

For every proposed lemma, identify why its demand is unavoidable for an aggregate counter. Check it against the private-leaf tree, affine/Tseitin counting, complement, caching, variable renaming, forced domains, fast transforms, input relocation, and the distinction between witness predicates and count maps. A refuted candidate or a stronger restricted theorem should be recorded explicitly. Do not convert a conjectural bridge into a premise and then describe its consequence as an unconditional proof.

## Appendix: complete finite-audit programs

The programs below are complete, standalone Python scripts. Save each under its indicated filename and run with Python 3. They use only the standard library. Their checks support the finite gadget and accounting claims; they do not search all algorithms or prove a general lower bound by experiment.


### A1. Definition and construction audit

Filename: t5_semantic_construction_audit.py

```python
#!/usr/bin/env python3
"""Finite audit of the strict-cycle T5 construction and ordered-clause variant.

This verifies finite gadget identities and small matching instances. It does
not by itself prove an asymptotic lower bound. Only the Python standard library
is required. No source file is changed and no output file is written.
"""

from itertools import product, permutations
import json


COLORS = tuple(range(5))
ALLOWED = {frozenset((i, (i + 1) % 5, (i + 2) % 5)) for i in COLORS}


def beats(x, y):
    """A=0,...,E=4; A beats B,D, and similarly by cyclic translation."""
    return (y - x) % 5 in (1, 3)


def cycle_relation(x, y, z):
    return len({x, y, z}) == 3 and frozenset((x, y, z)) in ALLOWED


def first_relation(x, y, z):
    return len({x, y, z}) == 3 and (beats(x, y) != beats(x, z))


def anchor_frames(relation):
    return [a for a in product(COLORS, repeat=5)
            if all(relation(a[i], a[(i + 1) % 5], a[(i + 2) % 5])
                   for i in COLORS)]


def or_extensions(relation, a, p, q, x):
    return sum(relation(a[1], a[2], y)
               and relation(a[0], a[1], z)
               and relation(a[4], a[p], y)
               and relation(a[3], a[q], z)
               and relation(a[x], y, z)
               for y, z in product(COLORS, repeat=2))


def audit_semantics_and_gadgets():
    C, R = cycle_relation, first_relation
    expected_frames = {tuple((s + d * i) % 5 for i in COLORS)
                       for s in COLORS for d in (-1, 1)}
    c_frames, r_frames = anchor_frames(C), anchor_frames(R)
    assert set(c_frames) == set(r_frames) == expected_frames
    tuples = list(product(COLORS, repeat=3))
    assert sum(C(*t) for t in tuples) == 30
    assert sum(R(*t) for t in tuples) == 40
    assert all(C(x, y, z) == (R(x, y, z) and R(y, x, z))
               for x, y, z in tuples)

    counts = dict(frames=10, transport_rows=0, nand_rows=0,
                  base_domain_rows=0, not_rows=0, or_rows=0, output_pin_rows=0)
    for a in c_frames:
        # Original archive's Boolean transport family.
        for relation in (C, R):
            assert {x for x in COLORS if relation(a[1], a[2], x)} == {a[0], a[3]}
            for x, y in product((a[0], a[3]), repeat=2):
                assert relation(a[4], x, y) == (x != y)
                counts['transport_rows'] += 1
        assert {x for x in COLORS if C(a[1], a[4], x)} == {a[0]}
        assert {x for x in COLORS if C(a[2], a[4], x)} == {a[3]}
        assert {x for x in COLORS if R(a[1], a[4], x)} == {a[0], a[3]}
        assert {x for x in COLORS if R(a[2], a[4], x)} == {a[0], a[3]}

        # Later continuation's graph/independent-set family.
        left = (a[4], a[2])   # Boolean selected bit 0,1.
        right = (a[1], a[3])
        for relation in (C, R):
            assert {x for x in COLORS if relation(a[0], a[1], x)} == set(left)
            assert {y for y in COLORS if relation(a[0], a[4], y)} == set(right)
            assert {z for z in COLORS if relation(a[2], a[3], z)} == {a[1], a[4]}
        for p, q in product((0, 1), repeat=2):
            x, y = left[p], right[q]
            assert C(a[0], x, y) == (not (p and q))
            assert R(a[0], x, y)  # Old order is redundant under R.
            assert R(x, a[0], y) == (not (p and q))  # Corrected order.
            counts['nand_rows'] += 1

        # Strict-C Boolean circuit simulation, including exact multiplicities.
        for b in COLORS:
            extensions = sum(all(C(a[j], b, u[j - 2]) for j in (2, 3, 4))
                             for u in product(COLORS, repeat=3))
            assert extensions == (2 if b in (a[0], a[1]) else 0)
            counts['base_domain_rows'] += 1
        for p, x in product((0, 1), repeat=2):
            assert C(a[2], a[p], a[x]) == (x == 1 - p)
            counts['not_rows'] += 1
        for p, q, x in product((0, 1), repeat=3):
            assert or_extensions(C, a, p, q, x) == int(x == (p or q))
            counts['or_rows'] += 1
        for x in (0, 1):
            assert C(a[0], a[2], a[x]) == bool(x)
            counts['output_pin_rows'] += 1

    a = COLORS
    return {
        'cycle_relation_ordered_tuples': 30,
        'first_relation_ordered_tuples': 40,
        'cycle_as_two_first_relation_clauses': True,
        'finite_gadget_checks': counts,
        'one_edge_cycle_count': 30,
        'one_edge_unrepaired_first_relation_count': 40,
        'one_edge_repaired_first_relation_count': 30,
        'unrepaired_first_relation_or_output_extensions': [
            {'inputs': [p, q], 'output_0': or_extensions(R, a, p, q, 0),
             'output_1': or_extensions(R, a, p, q, 1)}
            for p, q in product((0, 1), repeat=2)
        ],
    }


def cycle_lengths(p, q):
    inverse = [0] * len(p)
    for i, value in enumerate(p):
        inverse[value] = i
    tau = [inverse[q[i]] for i in range(len(p))]
    seen, lengths = set(), []
    for i in range(len(p)):
        if i in seen:
            continue
        length, j = 0, i
        while j not in seen:
            seen.add(j)
            length += 1
            j = tau[j]
        lengths.append(length)
    return lengths


def lucas(n):
    a, b = 2, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def audit_matching_families(max_k=4):
    results, checked_pairs = [], 0
    for k in range(1, max_k + 1):
        ps = list(permutations(range(k)))
        transport_counts, nand_counts = set(), set()
        for p, q in product(ps, repeat=2):
            edges = {(i, k + p[i]) for i in range(k)} | {
                (i, k + q[i]) for i in range(k)}
            z_transport = z_nand = 0
            for mask in range(1 << (2 * k)):
                z_transport += all(((mask >> u) & 1) != ((mask >> v) & 1)
                                   for u, v in edges)
                z_nand += all(not (((mask >> u) & 1) and ((mask >> v) & 1))
                              for u, v in edges)
            lengths = cycle_lengths(p, q)
            assert z_transport == 2 ** len(lengths)
            expected_nand = 1
            for length in lengths:
                expected_nand *= lucas(2 * length)
            assert z_nand == expected_nand
            if p == q:
                assert z_transport == 2 ** k and z_nand == 3 ** k
            else:
                assert z_transport < 2 ** k and z_nand < 3 ** k
            transport_counts.add(10 * z_transport)
            nand_counts.add(10 * z_nand)
            checked_pairs += 1
        results.append({'k': k, 'permutations': len(ps),
                        'transport_t5_counts': sorted(transport_counts),
                        'nand_t5_counts': sorted(nand_counts)})
    return {'checked_permutation_pairs': checked_pairs, 'families': results}


def audit_decision_family(max_k=4):
    checked = 0
    for k in range(1, max_k + 1):
        bitstrings = list(product((0, 1), repeat=k))
        for x, y in product(bitstrings, repeat=2):
            count = sum(all(b[i] == x[i] == y[i] for i in range(k))
                        for b in bitstrings)
            assert 10 * count == (10 if x == y else 0)
            checked += 1
    return {'checked_bitstring_pairs': checked}


def main():
    print(json.dumps({'status': 'PASS',
                      'semantics': audit_semantics_and_gadgets(),
                      'matching_families': audit_matching_families(),
                      'decision_family': audit_decision_family()}, indent=2))


if __name__ == '__main__':
    main()
```


### A2. Original single-tape gadget and encoding audit

Filename: audit_single_tape_t5.py

```python
#!/usr/bin/env python3
"""Exhaustive finite audits of two strict-T5 families used in a tape argument.

Canonical values are 0,1,2,3,4.  Value a beats b exactly when
(b-a) mod 5 belongs to {1,3}; C(a,b,c) means a directed triangle.
Every constructed constraint has three distinct variable names.

Counting family, for permutations pi,sigma of range(k):
    n = 2*k+5, m = 4*k+5,
    #T5 = 10 * 2**cycles(pi^{-1} sigma).

Decision family, for bit strings x,y of length k:
    n = k+5, m = 3*k+5,
    #T5 = 10 if x == y, and 0 otherwise.

The counter is a generic all-domain GAC/backtracking implementation.  It
does not know anchor symmetries, intended pins, equality/inequality gadgets,
permutations, or either expected count formula.  The expected answers are
computed separately and compared only after counting finishes.

The binary encoding is 1**n 0 gamma(m+1), followed by the five-frame
prefix, left private block, domain-only common middle, and right private
block.  Variable identifiers are one-based, width ceil(log2(n+1)).
The script checks strict syntax, complete encoding roundtrips, and
invariance of the public prefix and middle for every fixed k.
It does NOT simulate a Turing machine or verify an asymptotic tape-time
lower bound.  Numerical crossing-bound examples evaluate an explicitly
conditional formula; they are not measured runtimes.

Python 3.10+; standard library only.  Default audit: all pairs for k=1..4.

Run:
    python3 audit_single_tape_t5.py
    python3 audit_single_tape_t5.py --output /absolute/path/audit_results.json
    python3 audit_single_tape_t5.py --max-k 2
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import platform
import time
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Sequence


VALUES = tuple(range(5))
ALL_VALUES_MASK = 31
Clause = tuple[int, int, int]


def check(condition: bool, message: str) -> None:
    """Use explicit checks so python -O does not disable the audit."""
    if not condition:
        raise AssertionError(message)


def beats(a: int, b: int) -> bool:
    return (b - a) % 5 in (1, 3)


def cycle(a: int, b: int, c: int) -> bool:
    return bool(
        (beats(a, b) and beats(b, c) and beats(c, a))
        or (beats(a, c) and beats(c, b) and beats(b, a))
    )


ALLOWED_TUPLES = tuple(
    t for t in itertools.product(VALUES, repeat=3) if cycle(*t)
)
ALLOWED_MASK_TUPLES = tuple(
    (1 << a, 1 << b, 1 << c) for a, b, c in ALLOWED_TUPLES
)
FRAME: tuple[Clause, ...] = tuple(
    (i, (i + 1) % 5, (i + 2) % 5) for i in range(5)
)


@dataclass(frozen=True)
class Instance:
    names: tuple[str, ...]
    clauses: tuple[Clause, ...]

    @property
    def n(self) -> int:
        return len(self.names)

    def check_syntax(self) -> None:
        if len(set(self.names)) != self.n:
            raise ValueError("Declared variable names are not unique.")
        for clause in self.clauses:
            if len(clause) != 3 or len(set(clause)) != 3:
                raise ValueError("A strict C clause needs three distinct names.")
            if not all(isinstance(v, int) and 0 <= v < self.n for v in clause):
                raise ValueError("A clause uses an undeclared variable.")


@dataclass(frozen=True)
class SplitInstance:
    names: tuple[str, ...]
    prefix: tuple[Clause, ...]
    left: tuple[Clause, ...]
    middle: tuple[Clause, ...]
    right: tuple[Clause, ...]

    @property
    def instance(self) -> Instance:
        return Instance(self.names, self.prefix + self.left + self.middle + self.right)


@lru_cache(maxsize=None)
def relation_supports(d0: int, d1: int, d2: int) -> tuple[int, int, int]:
    """Generic cached C-table supports for three arbitrary domain masks."""
    s0 = s1 = s2 = 0
    for b0, b1, b2 in ALLOWED_MASK_TUPLES:
        if d0 & b0 and d1 & b1 and d2 & b2:
            s0 |= b0
            s1 |= b1
            s2 |= b2
    return s0, s1, s2


def count_t5_gac(instance: Instance) -> tuple[int, dict[str, int]]:
    """Count exactly from unrestricted five-value domains on every variable.

    All constraints are processed as the same ternary relation.  MRV and
    incident-constraint counts choose branches.  No family-specific facts
    enter propagation, branching, memoization, or answer computation.
    """
    instance.check_syntax()
    n = instance.n
    clauses = instance.clauses
    incident: list[list[int]] = [[] for _ in range(n)]
    for ci, clause in enumerate(clauses):
        for v in clause:
            incident[v].append(ci)
    stats = {
        "recursive_calls": 0,
        "branch_nodes": 0,
        "failed_states": 0,
        "memo_hits": 0,
        "propagation_clause_visits": 0,
        "maximum_recursion_depth": 0,
    }
    memo: dict[tuple[int, ...], int] = {}

    def propagate(initial: tuple[int, ...]) -> tuple[int, ...] | None:
        domains = list(initial)
        queue = deque(range(len(clauses)))
        queued = [True] * len(clauses)
        while queue:
            ci = queue.popleft()
            queued[ci] = False
            stats["propagation_clause_visits"] += 1
            a, b, c = clauses[ci]
            supports = relation_supports(domains[a], domains[b], domains[c])
            if not all(supports):
                return None
            for v, supported in zip(clauses[ci], supports):
                reduced = domains[v] & supported
                if not reduced:
                    return None
                if reduced != domains[v]:
                    domains[v] = reduced
                    for neighbor in incident[v]:
                        if not queued[neighbor]:
                            queued[neighbor] = True
                            queue.append(neighbor)
        return tuple(domains)

    def visit(initial: tuple[int, ...], depth: int) -> int:
        stats["recursive_calls"] += 1
        stats["maximum_recursion_depth"] = max(
            stats["maximum_recursion_depth"], depth
        )
        domains = propagate(initial)
        if domains is None:
            stats["failed_states"] += 1
            return 0
        if domains in memo:
            stats["memo_hits"] += 1
            return memo[domains]
        undecided = [v for v, mask in enumerate(domains) if mask.bit_count() > 1]
        if not undecided:
            memo[domains] = 1
            return 1
        chosen = min(
            undecided,
            key=lambda v: (domains[v].bit_count(), -len(incident[v]), v),
        )
        stats["branch_nodes"] += 1
        total = 0
        for value in VALUES:
            bit = 1 << value
            if domains[chosen] & bit:
                child = list(domains)
                child[chosen] = bit
                total += visit(tuple(child), depth + 1)
        memo[domains] = total
        return total

    answer = visit((ALL_VALUES_MASK,) * n, 0)
    stats["memo_entries"] = len(memo)
    return answer, stats


def count_t5_brute_force(instance: Instance) -> int:
    """Small independent direct-predicate crosscheck, with no propagation."""
    instance.check_syntax()
    result = 0
    for values in itertools.product(VALUES, repeat=instance.n):
        if all(cycle(values[a], values[b], values[c]) for a, b, c in instance.clauses):
            result += 1
    return result


def validate_permutation(p: Sequence[int]) -> tuple[int, ...]:
    result = tuple(p)
    if sorted(result) != list(range(len(result))):
        raise ValueError("Not a permutation of range(k).")
    return result


def relative_cycle_count(pi: Sequence[int], sigma: Sequence[int]) -> int:
    """Number of cycles of pi^{-1} composed with sigma, including fixed points."""
    pi = validate_permutation(pi)
    sigma = validate_permutation(sigma)
    if len(pi) != len(sigma):
        raise ValueError("Permutation lengths differ.")
    inverse = [0] * len(pi)
    for i, image in enumerate(pi):
        inverse[image] = i
    relative = tuple(inverse[image] for image in sigma)
    seen: set[int] = set()
    cycles = 0
    for start in range(len(relative)):
        if start in seen:
            continue
        cycles += 1
        current = start
        while current not in seen:
            seen.add(current)
            current = relative[current]
    return cycles


def build_counting(pi: Sequence[int], sigma: Sequence[int]) -> SplitInstance:
    pi = validate_permutation(pi)
    sigma = validate_permutation(sigma)
    if not pi or len(pi) != len(sigma):
        raise ValueError("Need two nonempty permutations of the same length.")
    k = len(pi)
    names = tuple(f"a{i}" for i in range(5))
    names += tuple(f"X{i}" for i in range(k))
    names += tuple(f"Y{i}" for i in range(k))
    xs = tuple(5 + i for i in range(k))
    ys = tuple(5 + k + i for i in range(k))
    left = tuple((4, xs[i], ys[pi[i]]) for i in range(k))
    middle = tuple((1, 2, v) for v in xs + ys)
    right = tuple((4, xs[i], ys[sigma[i]]) for i in range(k))
    split = SplitInstance(names, FRAME, left, middle, right)
    split.instance.check_syntax()
    check(split.instance.n == 2 * k + 5, "Counting-family n mismatch.")
    check(len(split.instance.clauses) == 4 * k + 5, "Counting-family m mismatch.")
    return split


def validate_bits(bits: Iterable[int]) -> tuple[int, ...]:
    result = tuple(bits)
    if not result or any(bit not in (0, 1) for bit in result):
        raise ValueError("Need a nonempty zero-one string.")
    return result


def build_decision(x: Iterable[int], y: Iterable[int]) -> SplitInstance:
    x, y = validate_bits(x), validate_bits(y)
    if len(x) != len(y):
        raise ValueError("Bit-string lengths differ.")
    k = len(x)
    names = tuple(f"a{i}" for i in range(5)) + tuple(f"X{i}" for i in range(k))
    xs = tuple(5 + i for i in range(k))
    left = tuple((1 if bit == 0 else 2, 4, xs[i]) for i, bit in enumerate(x))
    middle = tuple((1, 2, v) for v in xs)
    right = tuple((1 if bit == 0 else 2, 4, xs[i]) for i, bit in enumerate(y))
    split = SplitInstance(names, FRAME, left, middle, right)
    split.instance.check_syntax()
    check(split.instance.n == k + 5, "Decision-family n mismatch.")
    check(len(split.instance.clauses) == 3 * k + 5, "Decision-family m mismatch.")
    return split


def gamma_encode(value: int) -> str:
    if value < 1:
        raise ValueError("Elias gamma codes encode positive integers.")
    binary = format(value, "b")
    return "0" * (len(binary) - 1) + binary


def gamma_decode(bits: str, position: int) -> tuple[int, int]:
    start = position
    while position < len(bits) and bits[position] == "0":
        position += 1
    if position >= len(bits):
        raise ValueError("Incomplete gamma code.")
    width = position - start + 1
    stop = position + width
    if stop > len(bits):
        raise ValueError("Incomplete gamma payload.")
    return int(bits[position:stop], 2), stop


def encode_split(split: SplitInstance) -> dict[str, str | int]:
    """Encode 1**n 0 gamma(m+1), then prefix/left/middle/right triples.

    Variable identifiers are one-based, each using w=ceil(log2(n+1))
    bits.  For n=0, w=0 and valid inputs have no clause records.
    """
    instance = split.instance
    instance.check_syntax()
    width = instance.n.bit_length()

    def encode_block(clauses: tuple[Clause, ...]) -> str:
        rows = ["".join(format(v + 1, f"0{width}b") for v in clause) for clause in clauses]
        check(all(len(row) == 3 * width for row in rows), "Nonconstant triple width.")
        return "".join(rows)

    header = "1" * instance.n + "0" + gamma_encode(len(instance.clauses) + 1)
    prefix = encode_block(split.prefix)
    left = encode_block(split.left)
    middle = encode_block(split.middle)
    right = encode_block(split.right)
    full = header + prefix + left + middle + right
    return {
        "identifier_width_bits": width,
        "triple_width_bits": 3 * width,
        "header": header,
        "prefix": prefix,
        "left": left,
        "middle": middle,
        "right": right,
        "full": full,
    }


def decode_instance(bits: str) -> tuple[int, tuple[Clause, ...]]:
    if any(bit not in "01" for bit in bits):
        raise ValueError("Nonbinary encoding.")
    n = 0
    while n < len(bits) and bits[n] == "1":
        n += 1
    if n >= len(bits):
        raise ValueError("Unterminated unary variable count.")
    m_plus_one, pos = gamma_decode(bits, n + 1)
    m = m_plus_one - 1
    width = n.bit_length()
    if n == 0 and m != 0:
        raise ValueError("A zero-variable input cannot contain strict clauses.")
    if len(bits) - pos != 3 * m * width:
        raise ValueError("Encoded triple payload has the wrong length.")
    clauses: list[Clause] = []
    for _ in range(m):
        row = tuple(int(bits[pos + j * width:pos + (j + 1) * width], 2) - 1 for j in range(3))
        pos += 3 * width
        if len(set(row)) != 3 or not all(0 <= v < n for v in row):
            raise ValueError("Decoded triple violates strict syntax.")
        clauses.append(row)  # type: ignore[arg-type]
    return n, tuple(clauses)


def check_encoding(split: SplitInstance) -> dict[str, str | int]:
    encoded = encode_split(split)
    decoded_n, decoded_clauses = decode_instance(str(encoded["full"]))
    check(decoded_n == split.instance.n, "Encoded n failed roundtrip.")
    check(decoded_clauses == split.instance.clauses, "Clauses failed roundtrip.")
    return encoded


def audit_relation_and_counter() -> dict:
    check(len(ALLOWED_TUPLES) == 30, "C should have exactly 30 ordered tuples.")
    unordered = [list(t) for t in itertools.combinations(VALUES, 3) if cycle(*t)]
    check(
        unordered == [[0, 1, 2], [0, 1, 4], [0, 3, 4], [1, 2, 3], [2, 3, 4]],
        "Unexpected unordered C triples.",
    )
    for values in itertools.product(VALUES, repeat=3):
        check(
            all(cycle(*values) == cycle(*(values[i] for i in order))
                for order in itertools.permutations(range(3))),
            "C is not symmetric.",
        )
    anchors = tuple(
        values for values in itertools.product(VALUES, repeat=5)
        if all(cycle(*(values[v] for v in clause)) for clause in FRAME)
    )
    expected_frames = {
        tuple((offset + direction * j) % 5 for j in range(5))
        for offset in VALUES for direction in (1, -1)
    }
    check(len(anchors) == 10 and set(anchors) == expected_frames, "Frame identity failed.")
    domains = [v for v in VALUES if cycle(1, 2, v)]
    pin_zero = [v for v in VALUES if cycle(1, 4, v)]
    pin_one = [v for v in VALUES if cycle(2, 4, v)]
    edge = [[u, v] for u, v in itertools.product(domains, repeat=2) if cycle(4, u, v)]
    check(domains == [0, 3], "Domain gadget failed.")
    check(pin_zero == [0] and pin_one == [3], "Pin gadget failed.")
    check(edge == [[0, 3], [3, 0]], "Opposite-value gadget failed.")

    controls = [
        ("empty", Instance((), ()), 1),
        ("unused_variable", Instance(("x",), ()), 5),
        ("one_clause", Instance(("x", "y", "z"), ((0, 1, 2),)), 30),
        ("one_clause_unused_variable", Instance(("x", "y", "z", "u"), ((0, 1, 2),)), 150),
        ("duplicate_clause", Instance(("x", "y", "z"), ((0, 1, 2), (0, 1, 2))), 30),
        ("two_disjoint_clauses", Instance(tuple(f"v{i}" for i in range(6)), ((0, 1, 2), (3, 4, 5))), 900),
        ("anchor_frame", Instance(tuple(f"a{i}" for i in range(5)), FRAME), 10),
    ]
    control_results = []
    for label, instance, expected in controls:
        actual, stats = count_t5_gac(instance)
        check(actual == expected, f"Counter control failed: {label}.")
        control_results.append({"label": label, "expected": expected, "actual": actual, "stats": stats})
    invalid = [
        Instance(("x", "y"), ((0, 0, 1),)),
        Instance(("x", "y", "z"), ((0, 1, 3),)),
        Instance(("x", "x", "z"), ((0, 1, 2),)),
    ]
    for instance in invalid:
        try:
            instance.check_syntax()
        except ValueError:
            pass
        else:
            raise AssertionError("Syntax checker accepted an invalid instance.")
    return {
        "ordered_C_tuples": len(ALLOWED_TUPLES),
        "unordered_C_triples": unordered,
        "anchor_assignments": len(anchors),
        "anchor_assignments_are_exactly_dihedral": True,
        "domain_C_a1_a2": domains,
        "pin_C_a1_a4": pin_zero,
        "pin_C_a2_a4": pin_one,
        "edge_C_a4_on_domain": edge,
        "counter_controls": control_results,
        "invalid_syntax_controls_rejected": len(invalid),
    }


def audit_family(family: str, max_k: int) -> dict:
    summaries = []
    all_cases = []
    brute_crosschecks = 0
    for k in range(1, max_k + 1):
        started = time.perf_counter()
        if family == "counting":
            inputs = tuple(itertools.permutations(range(k)))
            builder = build_counting
        elif family == "decision":
            inputs = tuple(itertools.product((0, 1), repeat=k))
            builder = build_decision
        else:
            raise ValueError("Unknown family.")
        reference = None
        left_encodings: dict[tuple[int, ...], str] = {}
        right_encodings: dict[tuple[int, ...], str] = {}
        observed_counts: set[int] = set()
        checked = 0
        for left_input, right_input in itertools.product(inputs, repeat=2):
            split = builder(left_input, right_input)
            encoded = check_encoding(split)
            if reference is None:
                reference = encoded
            check(encoded["middle"] == reference["middle"], "Public middle depends on private input.")
            check(encoded["prefix"] == reference["prefix"], "Frame prefix depends on private input.")
            check(encoded["header"] == reference["header"], "Header depends on private input.")
            check(len(str(encoded["full"])) == len(str(reference["full"])), "Full length varies at fixed k.")
            for side, key, previous in (
                ("left", left_input, left_encodings),
                ("right", right_input, right_encodings),
            ):
                if key in previous:
                    check(previous[key] == encoded[side], f"{side} block depends on the other party.")
                previous[key] = str(encoded[side])
            actual, stats = count_t5_gac(split.instance)
            if family == "counting":
                cycles = relative_cycle_count(left_input, right_input)
                expected = 10 * (1 << cycles)
                details = {"pi": list(left_input), "sigma": list(right_input), "relative_cycles": cycles}
            else:
                expected = 10 if left_input == right_input else 0
                details = {"x": list(left_input), "y": list(right_input), "equal": left_input == right_input}
            check(actual == expected, f"{family} count mismatch at k={k}, {details}.")
            if k == 1:
                brute = count_t5_brute_force(split.instance)
                check(actual == brute, f"Brute-force crosscheck failed for {family}, {details}.")
                brute_crosschecks += 1
                details["independent_brute_force_count"] = brute
            observed_counts.add(actual)
            checked += 1
            all_cases.append({
                "k": k,
                **details,
                "expected": expected,
                "actual": actual,
                "stats": stats,
            })
        check(reference is not None, "No cases generated.")
        check(checked == len(inputs) ** 2, "Did not test every pair.")
        check(len(set(left_encodings.values())) == len(inputs), "Left encodings are not injective.")
        check(len(set(right_encodings.values())) == len(inputs), "Right encodings are not injective.")
        representative = builder(inputs[0], inputs[0])
        summary = {
            "k": k,
            "inputs_per_party": len(inputs),
            "all_pairs_checked": checked,
            "n": representative.instance.n,
            "m": len(representative.instance.clauses),
            "observed_counts": sorted(observed_counts),
            "identifier_width_bits": reference["identifier_width_bits"],
            "triple_width_bits": reference["triple_width_bits"],
            "header_bits": len(str(reference["header"])),
            "common_frame_prefix_bits": len(str(reference["prefix"])),
            "left_bits": len(str(reference["left"])),
            "common_middle_bits": len(str(reference["middle"])),
            "internal_middle_cuts": len(str(reference["middle"])) - 1,
            "right_bits": len(str(reference["right"])),
            "total_encoded_bits": len(str(reference["full"])),
            "strict_syntax_checked_for_every_instance": True,
            "encoding_roundtrip_checked_for_every_instance": True,
            "common_middle_invariant": True,
            "common_frame_prefix_invariant": True,
            "each_private_block_depends_only_on_its_owner_input": True,
            "private_encodings_injective": True,
            "elapsed_seconds": round(time.perf_counter() - started, 6),
        }
        summaries.append(summary)
        print(
            f"{family}: k={k}, pairs={checked}, n={summary['n']}, m={summary['m']}, "
            f"counts={summary['observed_counts']}, seconds={summary['elapsed_seconds']}",
            flush=True,
        )
    return {
        "identity": (
            "#T5 = 10 * 2**cycles(pi^{-1} sigma)"
            if family == "counting" else "#T5 = 10 if x == y, else 0"
        ),
        "total_pairs_checked": len(all_cases),
        "independent_brute_force_crosschecks": brute_crosschecks,
        "by_k": summaries,
        "cases": all_cases,
    }


def conditional_crossing_examples() -> dict:
    """Evaluate exact arithmetic for a supplied conditional crossing bound.

    For a correct Q-state counter, the proof's finite formula is
    T_max >= ceil(D*r/2), where M=k!, r=max(0,floor(log_Q(M))-2),
    and D is the number of strictly internal common-middle boundaries.
    This routine checks the numerical formula and encoding lengths only.
    It neither constructs that counter nor proves the crossing lemma.
    """
    q = 256
    expected = {
        100: (9943, 4799, 65, 63, 151169),
        1000: (134194, 65999, 1066, 1064, 35111468),
        10000: (1820262, 899999, 14807, 14805, 6662242598),
    }
    examples = []
    for k in (100, 1000, 10000):
        identity = tuple(range(k))
        split = build_counting(identity, identity)
        encoded = check_encoding(split)
        n, m = split.instance.n, len(split.instance.clauses)
        width = n.bit_length()
        formula_length = n + 1 + 2 * (m + 1).bit_length() - 1 + 3 * m * width
        total_bits = len(str(encoded["full"]))
        check(total_bits == formula_length, "Exact encoding-length formula failed.")
        middle_bits = len(str(encoded["middle"]))
        check(middle_bits == 6 * k * width, "Domain-only middle-length formula failed.")
        d = middle_bits - 1
        input_count = math.factorial(k)
        floor_log_q = (input_count.bit_length() - 1) // 8
        r = max(0, floor_log_q - 2)
        lower_bound = (d * r + 1) // 2
        # Verify the short-sequence estimate with integers, without floating logs.
        short_sequences = (q ** (r + 1) - 1) // (q - 1)
        check(short_sequences * 2 <= input_count, "Short-sequence counting estimate failed.")
        check(
            (total_bits, d, floor_log_q, r, lower_bound) == expected[k],
            "Conditional example differs from its exact expected arithmetic.",
        )
        examples.append({
            "k": k,
            "n": n,
            "m": m,
            "identifier_width_bits": width,
            "total_encoded_bits_N": total_bits,
            "common_middle_bits": middle_bits,
            "strictly_internal_middle_boundaries_D": d,
            "factorial_bit_length": input_count.bit_length(),
            "floor_log_Q_factorial": floor_log_q,
            "r": r,
            "conditional_transition_lower_bound_ceil_Dr_over_2": lower_bound,
            "short_sequence_estimate_checked_with_exact_integers": True,
            "full_encoding_roundtrip_checked": True,
        })
    return {
        "status": "Conditional mathematical-bound arithmetic, not measured runtime; assumes a correct Q-state counter and the stated crossing-sequence lemma.",
        "Q": q,
        "formula": "r=max(0,floor(log_Q(k!))-2); T_max>=ceil(D*r/2)",
        "exact_log_method": "floor(log_256(k!)) = (factorial(k).bit_length()-1)//8",
        "examples": examples,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-k", type=int, choices=(1, 2, 3, 4), default=4)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("audit_results.json"))
    args = parser.parse_args()
    started = time.perf_counter()
    started_utc = datetime.now(timezone.utc).isoformat()
    relation = audit_relation_and_counter()
    counting = audit_family("counting", args.max_k)
    decision = audit_family("decision", args.max_k)
    crossing_examples = conditional_crossing_examples()
    cache = relation_supports.cache_info()
    result = {
        "all_checks_passed": True,
        "started_utc": started_utc,
        "python_version": platform.python_version(),
        "max_k": args.max_k,
        "scope": "Finite strict-C gadget counts and encoding checks only; no Turing-machine simulation or asymptotic lower-bound verification.",
        "counter": "Independent generic five-domain GAC, MRV backtracking, and memoization; no gadget-specific symmetry breaking or counting rules.",
        "encoding": "1**n 0 gamma(m+1), followed by the common five-frame prefix, left private block, common domain-only middle, and right private block; identifiers are one-based fixed-width binary, width=ceil(log2(n+1))=n.bit_length().",
        "relation_and_controls": relation,
        "counting_family": counting,
        "decision_family": decision,
        "conditional_crossing_examples": crossing_examples,
        "total_family_pairs_checked": counting["total_pairs_checked"] + decision["total_pairs_checked"],
        "relation_support_cache": {"hits": cache.hits, "misses": cache.misses, "entries": cache.currsize},
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {result['total_family_pairs_checked']} family pairs; wrote {args.output}")
    print(f"Elapsed seconds: {result['elapsed_seconds']}")


if __name__ == "__main__":
    main()
```


### A3. Original cumulative-bound arithmetic audit

Filename: audit_accounting.py

```python
#!/usr/bin/env python3
"""Exact arithmetic audit of the strict T5 bit-and-access accounting.

Run:
    python3 audit_accounting.py --output accounting_results.json

This script checks finite description counts and the numerical instantiation
of the proved inequalities. It does not implement an optimal Turing machine
or mechanically verify the universal crossing-sequence proof.

Only the Python standard library is required.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def ceil_log2(cardinality: int) -> int:
    """Minimum fixed code width for a nonempty finite class."""
    if cardinality < 1:
        raise ValueError("Cardinality must be positive.")
    return (cardinality - 1).bit_length()


def floor_log_base(value: int, base: int) -> int:
    """Exact floor(log_base(value)), with no floating-point rounding."""
    if value < 1 or base < 2:
        raise ValueError("Require value >= 1 and base >= 2.")
    low, high = 0, value.bit_length()
    while low < high:
        middle = (low + high + 1) // 2
        if pow(base, middle) <= value:
            low = middle
        else:
            high = middle - 1
    return low


def ceil_ratio(numerator: int, denominator: int) -> int:
    if denominator <= 0:
        raise ValueError("Denominator must be positive.")
    return -(-numerator // denominator)


def input_accounting(n: int, m: int) -> dict:
    if n < 3 or m < 0:
        raise ValueError("Require n >= 3 and m >= 0.")
    possible_clauses = math.comb(n, 3)
    width = n.bit_length()
    unary_n_header = n + 1
    gamma_m_header = 2 * ((m + 1).bit_length() - 1) + 1
    gamma_n_header = 2 * (n.bit_length() - 1) + 1
    joint_ordered = ceil_log2(pow(possible_clauses, m))
    multiset = math.comb(possible_clauses + m - 1, m)
    data = {
        "n": n,
        "m": m,
        "possible_canonical_clauses": possible_clauses,
        "variable_id_bits": width,
        "original_clause_data_bits": 3 * m * width,
        "original_header_bits": unary_n_header + gamma_m_header,
        "original_total_bits": unary_n_header + gamma_m_header + 3 * m * width,
        "binary_gamma_header_bits": gamma_n_header + gamma_m_header,
        "per_clause_rank_bits": ceil_log2(possible_clauses),
        "separate_clause_rank_total_bits": m * ceil_log2(possible_clauses),
        "joint_ordered_canonical_min_bits": joint_ordered,
        "joint_ordered_argument_preserving_min_bits": ceil_log2(
            pow(6 * possible_clauses, m)
        ),
        "multiset_min_bits": ceil_log2(multiset),
        "stored_assignment_three_bits_per_value": 3 * n,
        "stored_assignment_joint_min_bits": ceil_log2(pow(5, n)),
        "full_count_range_code_bits": ceil_log2(pow(5, n) + 1),
        "nonempty_custom_domain_masks_bits": 5 * n,
        "nonempty_custom_domains_joint_bits": ceil_log2(pow(31, n)),
        "fixed_domain_selector_bits_per_variable": 0,
        "fixed_relation_selector_bits_per_clause": 0,
    }
    if m <= possible_clauses:
        sets = math.comb(possible_clauses, m)
        orbit_lower = ceil_ratio(sets, math.factorial(n))
        data.update({
            "distinct_set_min_bits": ceil_log2(sets),
            "unlabeled_hypergraph_description_lower_bits": ceil_log2(orbit_lower),
            "unlabeled_count_is_lower_bound_not_exact": True,
        })
    return data


def matching_accounting(k: int, q: int) -> dict:
    if k < 2 or q < 2:
        raise ValueError("Require k >= 2 and q >= 2.")
    n, m = 2 * k + 5, 4 * k + 5
    encoding = input_accounting(n, m)
    size = encoding["original_total_bits"]
    d = 6 * k * encoding["variable_id_bits"] - 1
    count = math.factorial(k)
    floor_h = count.bit_length() - 1

    time_r = max(0, floor_log_base(count, q) - 2)
    time_lower = ceil_ratio(d * time_r, 2)

    # floor(H/(4 log_2 q)) = floor(log_(q^4)(k!)).
    cumulative_r = floor_log_base(count, q ** 4)
    cumulative_s = floor_h // 4
    q_to_r = pow(q, cumulative_r)
    early_halts_bound = (q_to_r - 1) // (q - 1)
    short_snapshot_bound = q_to_r * (pow(2, cumulative_s) - 1)
    bad_bound = early_halts_bound + short_snapshot_bound
    good_bound = max(0, count - bad_bound)
    event_budget = d * cumulative_r * cumulative_s

    cumulative_lower = ceil_ratio(event_budget * good_bound, count)
    half_bound_valid = 2 * bad_bound <= count
    conservative_half_lower = (
        ceil_ratio(event_budget, 2) if half_bound_valid else None
    )

    assert pow(q ** 4, cumulative_r) <= count
    assert pow(q ** 4, cumulative_r + 1) > count
    assert pow(2, 4 * cumulative_s) <= count
    assert pow(2, 4 * (cumulative_s + 1)) > count
    assert cumulative_lower >= (conservative_half_lower or 0)
    assert ceil_log2(count) <= ceil_log2(count * count)

    return {
        "k": k,
        "Q": q,
        "n": n,
        "m": m,
        "N_bits": size,
        "middle_boundaries_D": d,
        "diagonal_syntax_min_bits": ceil_log2(count),
        "full_ordered_matching_pair_min_bits": ceil_log2(count * count),
        "time_crossing_parameter_r": time_r,
        "transition_lower_bound": time_lower,
        "reserved_input_only_bit_time_lower": size * time_lower,
        "cumulative_crossing_parameter_r": cumulative_r,
        "cumulative_snapshot_parameter_s": cumulative_s,
        "cumulative_full_state_bit_time_lower": cumulative_lower,
        "cumulative_conservative_half_lower": conservative_half_lower,
        "half_good_probability_certified_exactly": half_bound_valid,
        "diagonal_distinct_clause_count": 3 * k + 5,
        "notes": [
            "Lower bounds are worst-case over the diagonal inputs of this size.",
            "Q is a hypothetical correct machine's control-state count.",
            "The cumulative bound charges self-contained state descriptions.",
            "The cumulative bound counts bit-steps, not bits transferred.",
            "The input-only reserved bound assumes all N cells stay reserved.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("accounting_results.json"))
    args = parser.parse_args()

    example = input_accounting(2005, 4005)
    cases = [matching_accounting(k, 256) for k in (100, 1000, 10000)]

    expected_example = {
        "possible_canonical_clauses": 1_341_349_010,
        "original_total_bits": 134_194,
        "joint_ordered_canonical_min_bits": 121_436,
        "joint_ordered_argument_preserving_min_bits": 131_789,
        "distinct_set_min_bits": 79_277,
        "multiset_min_bits": 79_277,
        "unlabeled_hypergraph_description_lower_bits": 60_169,
        "stored_assignment_joint_min_bits": 4_656,
    }
    for field, expected in expected_example.items():
        assert example[field] == expected, (field, example[field], expected)
    middle = cases[1]
    assert middle["transition_lower_bound"] == 35_111_468
    assert middle["cumulative_crossing_parameter_r"] == 266
    assert middle["cumulative_snapshot_parameter_s"] == 2132
    assert middle["cumulative_full_state_bit_time_lower"] == 37_428_824_888
    assert middle["reserved_input_only_bit_time_lower"] == 4_711_748_336_792

    report = {
        "status": "All exact arithmetic checks passed.",
        "scope": (
            "Arithmetic and finite counting-inequality audit; "
            "the mathematical proof is in CUMULATIVE_PROOF.md."
        ),
        "example": example,
        "matching_family": cases,
        "instruction_example": {
            "Q": 256,
            "G": 8,
            "directions": 3,
            "maximum_padded_rows": 2048,
            "dense_record_bits": ceil_log2(256 * 8 * 3),
            "explicit_record_bits": ceil_log2(256**2 * 8**2 * 3),
            "full_dense_table_bits_without_header": 2048 * ceil_log2(256 * 8 * 3),
            "is_an_implemented_solver": False,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(report["status"])
    print(f"Output: {args.output.resolve()}")
    for case in cases:
        print(
            f"k={case['k']}, N={case['N_bits']}, "
            f"T>={case['transition_lower_bound']}, "
            f"CM_state>={case['cumulative_full_state_bit_time_lower']}"
        )


if __name__ == "__main__":
    main()
```


### A4. CM continuation, Boolean gates, and joint bounds

Filename: cm_t5_continuation_audit.py

```python
#!/usr/bin/env python3
"""Finite audits for the strict T5 cumulative-memory continuation.

Uses only the Python standard library. All gadget checks enumerate the original
five-color relation. Large crossing bounds use integer arithmetic and Fraction.
"""

from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import product
from math import factorial
import json


ALLOWED = {
    frozenset((0, 1, 2)),
    frozenset((1, 2, 3)),
    frozenset((2, 3, 4)),
    frozenset((3, 4, 0)),
    frozenset((4, 0, 1)),
}


def relation(x, y, z):
    return len({x, y, z}) == 3 and frozenset((x, y, z)) in ALLOWED


def audit_gadgets():
    frames = [
        a for a in product(range(5), repeat=5)
        if all(relation(a[i], a[(i + 1) % 5], a[(i + 2) % 5])
               for i in range(5))
    ]
    assert len(frames) == 10
    rows = {"frames": 10, "domain_rows": 0, "not_rows": 0,
            "or_rows": 0, "pin_rows": 0, "nand_rows": 0}
    for a in frames:
        for b in range(5):
            extensions = sum(
                all(relation(a[j], b, u[j - 2]) for j in (2, 3, 4))
                for u in product(range(5), repeat=3)
            )
            assert extensions == (2 if b in (a[0], a[1]) else 0)
            rows["domain_rows"] += 1
        for p, x in product((0, 1), repeat=2):
            assert relation(a[2], a[p], a[x]) == (x == 1 - p)
            rows["not_rows"] += 1
        for p, q, x in product((0, 1), repeat=3):
            extensions = sum(
                relation(a[1], a[2], y)
                and relation(a[0], a[1], z)
                and relation(a[4], a[p], y)
                and relation(a[3], a[q], z)
                and relation(a[x], y, z)
                for y, z in product(range(5), repeat=2)
            )
            assert extensions == int(x == (p or q))
            rows["or_rows"] += 1
        for x in (0, 1):
            assert relation(a[0], a[2], a[x]) == bool(x)
            rows["pin_rows"] += 1
        left = [a[4], a[2]]
        right = [a[1], a[3]]
        for p, q in product((0, 1), repeat=2):
            assert relation(a[0], a[1], left[p])
            assert relation(a[0], a[4], right[q])
            assert relation(a[0], left[p], right[q]) == (not (p and q))
            rows["nand_rows"] += 1
    return rows


def tree_graph(r):
    # X_i: 0..r-1, P_i: r..2r-1, B_i: 2r..3r-2.
    edges = [(i, r + i) for i in range(r)]
    for i in range(r - 1):
        edges.extend(((i, 2 * r + i), (i + 1, 2 * r + i)))
    return 3 * r - 1, edges


def audit_tree_counts():
    results = []
    previous, current = 1, 3
    for r in range(1, 7):
        if r > 1:
            previous, current = current, 5 * current - 2 * previous
        v, edges = tree_graph(r)
        edge_masks = [(1 << u) | (1 << w) for u, w in edges]
        counted = sum(
            all(mask & edge != edge for edge in edge_masks)
            for mask in range(1 << v)
        )
        assert counted == current
        neighborhoods = set()
        for mask in range(1 << r):
            neighbors = 0
            for u, w in edges:
                if mask & (1 << u):
                    neighbors |= 1 << w
            neighborhoods.add(neighbors)
        assert len(neighborhoods) == 1 << r
        results.append({"r": r, "vertices": v,
                        "distinct_residuals": len(neighborhoods),
                        "independent_sets": counted,
                        "strict_t5_count": 10 * counted})
    return results


def joint_bound(k, q, z):
    assert k >= 1 and q >= 2 and z >= 0
    p = factorial(k)
    n = 2 * k + 5
    m = 4 * k + 5
    w = n.bit_length()  # ceil(log2(n + 1))
    encoded_length = n + 1 + 2 * ((m + 1).bit_length() - 1) + 1 + 3 * m * w
    d = 6 * k * w - 1
    b = p >> z
    q_power = q
    thresholds = []
    bad_sum = 0
    while q_power <= b:
        s = (b // q_power).bit_length() - 1
        assert s >= 0
        a_j = (q_power - 1) // (q - 1)
        e_j = a_j + q_power * ((1 << s) - 1)
        assert e_j <= b - 1
        thresholds.append(s)
        bad_sum += e_j
        q_power *= q
    r = len(thresholds)
    exact_failure = Fraction(d * bad_sum, p)
    simple_failure = Fraction(d * r, 1 << z)
    assert exact_failure <= simple_failure
    with localcontext() as ctx:
        ctx.prec = 30
        fail = Decimal(exact_failure.numerator) / Decimal(exact_failure.denominator)
        success_pct = 100 * (1 - fail)
    return {
        "k": k, "Q": q, "z": z, "n": n, "m": m, "w": w,
        "N": encoded_length, "D": d, "r": r,
        "sum_thresholds": sum(thresholds),
        "time_lower_bound": d * r,
        "cm_lower_bound": d * sum(thresholds),
        "exact_union_failure_decimal": str(fail),
        "success_percent_lower_bound_decimal": str(success_pct),
    }


def audit_description_lengths():
    results = []
    for t in range(1, 101):
        r = (t + 1).bit_length() - 1
        formula = r * t - (1 << (r + 1)) + r + 2
        lengths = []
        length = 0
        while len(lengths) < t:
            lengths.extend([length] * min(1 << length, t - len(lengths)))
            length += 1
        assert formula == sum(lengths)
        if t in (1, 2, 3, 4, 7, 100):
            results.append({"T": t, "minimum_injective_code_sum": formula})
    return results


def main():
    results = {
        "status": "PASS",
        "gadgets": audit_gadgets(),
        "tree_counterexample": audit_tree_counts(),
        "joint_bounds": [joint_bound(100, 256, 25),
                         joint_bound(1000, 256, 33)],
        "description_lengths": audit_description_lengths(),
    }
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
```


### A5. Parameterized aggregate progress

Filename: aggregate_progress_audit.py

```python
#!/usr/bin/env python3
"""Finite checks for the parameterized aggregate-progress research note.

Uses only Python's standard library. Exact rational arithmetic checks the
potential inequalities; exact elimination computes the small graph widths.
The asymptotic theorems require the proofs and sources in the note.
"""

from decimal import Decimal, localcontext, ROUND_CEILING
from fractions import Fraction
from functools import lru_cache
from itertools import product
import json


def graph(n, edges):
    adj = [0] * n
    for u, v in edges:
        assert u != v
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return tuple(adj)


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def induced(adj, mask):
    return tuple((neighbors & mask) if mask & (1 << u) else 0
                 for u, neighbors in enumerate(adj))


@lru_cache(None)
def exact_width(mask, adj):
    """Treewidth normalized to zero on empty graphs, via elimination orders."""
    if not mask:
        return 0
    candidates = list(bits(mask))
    low = [v for v in candidates if (adj[v] & mask).bit_count() <= 1]
    if low:
        candidates = low[:1]  # Isolated/leaf elimination is always optimal.
    answer = mask.bit_count() - 1
    for v in candidates:
        nb = adj[v] & mask
        new_mask = mask & ~(1 << v)
        after = list(adj)
        for u in bits(nb):
            after[u] = (after[u] | (nb & ~(1 << u))) & new_mask
        after[v] = 0
        candidate = max(nb.bit_count(), exact_width(new_mask, tuple(after)))
        answer = min(answer, candidate)
    return answer


def components(adj, mask):
    remaining = mask
    result = []
    while remaining:
        start = remaining & -remaining
        reached = 0
        frontier = start
        while frontier:
            reached |= frontier
            next_frontier = 0
            for v in bits(frontier):
                next_frontier |= adj[v] & mask
            frontier = next_frontier & ~reached
        result.append(reached)
        remaining &= ~reached
    return result


def brute_count(adj, mask):
    result = 0
    chosen = mask
    while True:
        if all(not (adj[v] & chosen) for v in bits(chosen)):
            result += 1
        if not chosen:
            break
        chosen = (chosen - 1) & mask
    return result


def audit_graph(name, adj):
    n = len(adj)
    delta = max((x.bit_count() for x in adj), default=0)
    assert delta <= 3
    base = Fraction(4, 3)  # Below rho_3: (3/4)+(3/4)^4 > 1.
    rule_checks = 0
    widths = {}
    for mask in range(1 << n):
        current = induced(adj, mask)
        widths[mask] = exact_width(mask, current)
    for mask in range(1 << n):
        width = widths[mask]
        for v in bits(mask):
            left = mask & ~(1 << v)
            right = mask & ~((1 << v) | adj[v])
            assert widths[left] >= width - 1
            assert widths[right] >= width - (delta + 1)
            assert base ** widths[left] + base ** widths[right] >= base ** width
            rule_checks += 1
        parts = components(adj, mask)
        if parts:
            assert width == max(widths[p] for p in parts)
            assert sum((base ** widths[p] for p in parts), Fraction()) >= base ** width
            rule_checks += 1

    terminal_allowance = Fraction()
    leaves = 0

    def adaptive_count(mask):
        nonlocal terminal_allowance, leaves
        # Heterogeneous, history-free thresholds suffice to test the invariant.
        threshold = 1 + int(mask.bit_count() % 2 == 0)
        if not mask or widths[mask] <= threshold:
            terminal_allowance += base ** threshold
            leaves += 1
            return brute_count(adj, mask)
        parts = components(adj, mask)
        if len(parts) > 1:
            count = 1
            for part in parts:
                count *= adaptive_count(part)
            return count
        v = max(bits(mask), key=lambda u: ((adj[u] & mask).bit_count(), u))
        return (adaptive_count(mask & ~(1 << v))
                + adaptive_count(mask & ~((1 << v) | adj[v])))

    full = (1 << n) - 1
    counted = adaptive_count(full)
    assert counted == brute_count(adj, full)
    assert terminal_allowance >= base ** widths[full]
    return {"graph": name, "vertices": n, "degree": delta,
            "treewidth": widths[full], "induced_graphs_checked": 1 << n,
            "rule_checks": rule_checks, "terminal_calls": leaves,
            "model_count": counted,
            "terminal_allowance": str(terminal_allowance),
            "initial_potential": str(base ** widths[full])}


def rho_bracket(delta):
    with localcontext() as ctx:
        ctx.prec = 70
        lo, hi = Decimal(1), Decimal(2)
        for _ in range(200):
            mid = (lo + hi) / 2
            if 1 / mid + mid ** (-(delta + 1)) > 1:
                lo = mid
            else:
                hi = mid
        return lo, hi


def numerical_bounds():
    with localcontext() as ctx:
        ctx.prec = 65
        lo, hi = rho_bracket(3)
        cases = []
        for width, threshold in ((30, 10), (60, 10), (120, 10)):
            a = (lo ** (width - threshold)).to_integral_value(rounding=ROUND_CEILING)
            b = (hi ** (width - threshold)).to_integral_value(rounding=ROUND_CEILING)
            assert a == b
            cases.append({"root_width": width, "max_terminal_width": threshold,
                          "terminal_calls_lower_bound": str(a)})
        return {"rho_3": str((lo + hi) / 2), "examples": cases}


def audit_decomposable_boolean_aggregation():
    cases = 0
    # Each child has two private Boolean inputs, hence a four-entry truth table.
    for f_table, g_table, operator in product(range(16), repeat=3):
        f = [(f_table >> a) & 1 for a in range(4)]
        g = [(g_table >> b) & 1 for b in range(4)]
        p, q = Fraction(sum(f), 4), Fraction(sum(g), 4)
        weights = ((1 - p) * (1 - q), (1 - p) * q,
                   p * (1 - q), p * q)
        predicted = sum((weights[i] for i in range(4) if operator & (1 << i)),
                        Fraction())
        actual = Fraction(sum((operator >> (2 * a + b)) & 1
                              for a in f for b in g), 16)
        assert predicted == actual
        assert Fraction(4 - sum(f), 4) == 1 - p
        cases += 1
    return cases


def main():
    c8 = graph(8, [(i, (i + 1) % 8) for i in range(8)])
    k33 = graph(6, [(i, j) for i in range(3) for j in range(3, 6)])
    cube = graph(8, [(i, i ^ (1 << j)) for i in range(8)
                     for j in range(3) if i < (i ^ (1 << j))])
    forest = graph(8, [(i, i + 1) for i in range(3)]
                         + [(4, 5), (4, 6)])
    results = {
        "status": "PASS",
        "graphs": [audit_graph(name, adj) for name, adj in
                   (("cycle_8", c8), ("K_3_3", k33),
                    ("cube", cube), ("forest_with_isolate", forest))],
        "numerical_bounds": numerical_bounds(),
        "independent_boolean_operator_cases": audit_decomposable_boolean_aggregation(),
        "switching_counterexample": {"parent_minimum": 101,
                                     "sum_child_minima": 2},
    }
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
```


### A6. Entropy and affine controls

Filename: entropy_audit.py

```python
#!/usr/bin/env python3
"""Finite checks accompanying the entropy / exact-counting proof note.

No dependencies beyond the Python standard library.
These checks verify examples and identities, not asymptotic lower bounds.
"""

from collections import Counter
from itertools import combinations
import json
from math import isclose, log2


def entropy(probabilities):
    return -sum(p * log2(p) for p in probabilities if p > 0)


def h2(p):
    return entropy((p, 1.0 - p))


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


def components(vertex_count, edges):
    adjacent = [set() for _ in range(vertex_count)]
    for a, b in edges:
        adjacent[a].add(b)
        adjacent[b].add(a)
    unseen = set(range(vertex_count))
    result = []
    while unseen:
        todo = [unseen.pop()]
        block = set(todo)
        while todo:
            for neighbor in adjacent[todo.pop()]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    block.add(neighbor)
                    todo.append(neighbor)
        result.append(block)
    return result


def tseitin_histogram(vertex_count, edges):
    counts = Counter()
    for assignment in range(1 << len(edges)):
        charges = 0
        for index, (a, b) in enumerate(edges):
            if (assignment >> index) & 1:
                charges ^= (1 << a) | (1 << b)
        counts[charges] += 1
    blocks = components(vertex_count, edges)
    expected_nonzero = 1 << (len(edges) - vertex_count + len(blocks))
    for charge in range(1 << vertex_count):
        feasible = all(
            sum((charge >> u) & 1 for u in block) % 2 == 0
            for block in blocks
        )
        expected = expected_nonzero if feasible else 0
        assert counts[charge] == expected, (vertex_count, edges, charge)
    return {
        "vertices": vertex_count,
        "edges": len(edges),
        "components": len(blocks),
        "charge_vectors_checked": 1 << vertex_count,
        "models_per_feasible_charge": expected_nonzero,
    }


def main():
    branch_checks = 0
    for z0 in range(33):
        for z1 in range(33):
            if z0 + z1 == 0:
                continue
            p = z0 / (z0 + z1)
            rhs = h2(p)
            if z0:
                rhs += p * log2(z0)
            if z1:
                rhs += (1.0 - p) * log2(z1)
            assert isclose(log2(z0 + z1), rhs, abs_tol=1e-12)
            branch_checks += 1

    fano_checks = 0
    for alphabet_size in range(2, 8):
        for numerators in compositions(12, alphabet_size):
            probabilities = [x / 12 for x in numerators]
            error_probability = 1 - probabilities[0]
            bound = h2(error_probability)
            bound += error_probability * log2(alphabet_size - 1)
            assert entropy(probabilities) <= bound + 1e-12
            fano_checks += 1

    thresholds = []
    for vertex_count in range(1, 10001):
        epsilon = 1 / (100 * (vertex_count + 1))
        value = h2(epsilon) + epsilon * vertex_count
        assert value < 0.06
        thresholds.append(value)

    cube_edges = [
        (x, x ^ (1 << bit))
        for x in range(8)
        for bit in range(3)
        if x < (x ^ (1 << bit))
    ]
    graphs = {
        "triangle": (3, [(0, 1), (1, 2), (0, 2)]),
        "square": (4, [(0, 1), (1, 2), (2, 3), (0, 3)]),
        "complete_four": (4, list(combinations(range(4), 2))),
        "cube": (8, cube_edges),
        "two_triangles": (
            6,
            [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)],
        ),
        "path_and_isolate": (4, [(0, 1), (1, 2)]),
    }
    graph_results = {
        name: tseitin_histogram(vertex_count, edges)
        for name, (vertex_count, edges) in graphs.items()
    }

    # One matching edge has the three equiprobable states 00, 01, 10.
    mutual_information_per_edge = 2 * h2(1 / 3) - log2(3)
    assert isclose(
        mutual_information_per_edge, 0.2516291673878229, abs_tol=1e-12
    )
    result = {
        "status": "PASS",
        "branch_entropy_identities": branch_checks,
        "error_entropy_inequalities": fano_checks,
        "count_thresholds_checked": len(thresholds),
        "largest_checked_threshold": max(thresholds),
        "matching_mutual_information_per_edge": mutual_information_per_edge,
        "tseitin_graph_checks": graph_results,
        "scope": "Finite examples and identities only; general proofs are in the note.",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
```


### A7. Observed output of the new definition audit

```json
{
  "status": "PASS",
  "semantics": {
    "cycle_relation_ordered_tuples": 30,
    "first_relation_ordered_tuples": 40,
    "cycle_as_two_first_relation_clauses": true,
    "finite_gadget_checks": {
      "frames": 10,
      "transport_rows": 80,
      "nand_rows": 40,
      "base_domain_rows": 50,
      "not_rows": 40,
      "or_rows": 80,
      "output_pin_rows": 20
    },
    "one_edge_cycle_count": 30,
    "one_edge_unrepaired_first_relation_count": 40,
    "one_edge_repaired_first_relation_count": 30,
    "unrepaired_first_relation_or_output_extensions": [
      {
        "inputs": [
          0,
          0
        ],
        "output_0": 1,
        "output_1": 1
      },
      {
        "inputs": [
          0,
          1
        ],
        "output_0": 1,
        "output_1": 1
      },
      {
        "inputs": [
          1,
          0
        ],
        "output_0": 0,
        "output_1": 1
      },
      {
        "inputs": [
          1,
          1
        ],
        "output_0": 0,
        "output_1": 1
      }
    ]
  },
  "matching_families": {
    "checked_permutation_pairs": 617,
    "families": [
      {
        "k": 1,
        "permutations": 1,
        "transport_t5_counts": [
          20
        ],
        "nand_t5_counts": [
          30
        ]
      },
      {
        "k": 2,
        "permutations": 2,
        "transport_t5_counts": [
          20,
          40
        ],
        "nand_t5_counts": [
          70,
          90
        ]
      },
      {
        "k": 3,
        "permutations": 6,
        "transport_t5_counts": [
          20,
          40,
          80
        ],
        "nand_t5_counts": [
          180,
          210,
          270
        ]
      },
      {
        "k": 4,
        "permutations": 24,
        "transport_t5_counts": [
          20,
          40,
          80,
          160
        ],
        "nand_t5_counts": [
          470,
          490,
          540,
          630,
          810
        ]
      }
    ]
  },
  "decision_family": {
    "checked_bitstring_pairs": 340
  }
}
```


### A8. Code integrity record

The following SHA-256 hashes identify the exact source strings embedded above. They are an integrity record, not a mathematical validation.

| Program | SHA-256 |
|---|---|
| t5_semantic_construction_audit.py | 6e7f884142110a88daab4169eb0ada20bb63cfe067ce91e45f1e22f2d672d5cf |
| audit_single_tape_t5.py | 4570c46ad1e2d8574075a48cae343d1529ae896e0ececf56f5a3b928cbbe4ff2 |
| audit_accounting.py | 22a777cc7ec9d1c2fc718914c8ea03ed541d171dd4c0dc03b61d417cb184b71e |
| cm_t5_continuation_audit.py | bffbedb7803e52590fbdba29ac82de5c7bdf172fa9c9a2fe2d7e0eb96560199d |
| aggregate_progress_audit.py | 7204f7b4a48cc8c67431350edebccfc9c042ec1af330657827d554db82e52642 |
| entropy_audit.py | ae1e23a5bb488bffdef0c827b3520a81030b4eeb37bbf80a3626ed2c35b4c98d |
