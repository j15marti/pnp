# A resource-preserving FLMV lower bound for the compact odd-tournament problem

22 November 2026, America/Los_Angeles

The result below excludes a uniform deterministic solver with near-linear time and subpolynomial auxiliary workspace for the compact construction. It transfers an existing lower bound; it does not prove P differs from NP. The asymptotic parameter is the length of the compact description, not the number of alphabet values.

## 1. External theorem and conventions

Let phi=(1+sqrt(5))/2. FLMV prove that, for every fixed 1<c<phi, there is a constant d>0 such that SAT has no deterministic random-access algorithm using both O(n^c) time and O(n^d) workspace. Read-only input is excluded from workspace. Their Section 3 extends the lower bound to standard locally encoded NP-complete problems, including the standard 3SAT source used below [1].

Our algorithms are uniform, always correct, and use this machine model or a model whose relevant simulations cost only polylogarithmic factors. Use the usual bounded read-only input interface, with input positions and boundary markers addressable in O(log n) bits. Address construction and all work/index registers are charged. All preprocessing and computation of reduction bits are charged. No nonuniform advice table or free circuit-evaluation oracle is supplied.

Subpolynomial workspace means n^{o(1)}: for every constant epsilon>0, the workspace is eventually bounded by O(n^epsilon). Near-linear time here means n^{1+o(1)}, which includes n times any fixed power of log n.

## 2. Local reduction transfer lemma

Let Q be a decision problem. Suppose a uniform reduction R from SAT, or from a source to which the same FLMV bounds apply, has the following properties for an n-bit source instance F:

1. Correctness: F is satisfiable if and only if R(F) belongs to Q.
2. Output length: L=|R(F)| is at most n(log n)^a, for a constant a.
3. Indexed access: given an output position i, the bit R(F)[i] can be produced from read-only random-access F in (log n)^b time and O(log n) workspace, for a constant b.
4. The output length and necessary O(log n)-bit header parameters can be obtained in n polylog(n) time and O(log n) workspace.

Then a Q algorithm with time T(L) and workspace S(L) yields a source algorithm with

\[
T_{\rm source}(n)=O\!\left(n\operatorname{polylog}n+
T(n\operatorname{polylog}n)\operatorname{polylog}n\right),
\]
\[
S_{\rm source}(n)=O\!\left(S(n\operatorname{polylog}n)+\log n\right).
\]

Use nondecreasing upper envelopes for T and S if necessary.

**Proof.** Keep the target algorithm's work configuration and a virtual input-head position. Whenever it asks for input bit i, run the indexed-access procedure, return that bit, and reuse the procedure's scratch space on the next request. At most T(L) input requests occur. The virtual input position needs O(log L)=O(log n) bits. The work configuration and reduction scratch space coexist, so their space costs add. The length/header initialization contributes the first time term. The simulator never materializes R(F). These observations give the displayed bounds. QED.

This lemma requires more than a near-linear-time, logarithmic-space streaming reduction. If a streaming reduction must be restarted and run nearly to completion for every requested output bit, simulation can take quadratic time. Storing the entire reduced instance instead can require linear workspace. Indexed access avoids both losses.

## 3. The forbidden solver theorem

**Theorem.** Under the local-reduction hypotheses above,

\[
Q\notin\mathrm{DTISP}[L^{1+o(1)},L^{o(1)}].
\]

**Proof.** Suppose a single correct target solver meets both bounds. The transfer lemma gives source time n^{1+o(1)} and workspace n^{o(1)}. Take c=3/2<phi, and let d>0 be the corresponding constant in the external theorem. For sufficiently large n, the simulated solver fits time O(n^{3/2}) and workspace O(n^d), contradicting that theorem. Finitely many smaller input lengths can be handled by constant-size adjustments to the machine. QED.

More generally, for every fixed 1<=c<phi,

\[
Q\notin\mathrm{DTISP}[L^{c+o(1)},L^{o(1)}].
\]

Choose c' strictly between c and phi. Polylogarithmic reduction overhead and the o(1) term can be absorbed into the gap c'-c, while subpolynomial space fits the positive polynomial-space bound corresponding to c'. The strict inequality c<phi is essential to this inference.

The conclusion rules out one algorithm satisfying both resource bounds on all inputs. It is not a pointwise claim that every instance takes L^phi steps, and it does not exclude a near-linear solver using substantially more workspace.

## 4. The compact target to which we apply the lemma

Write R(a,b,c) for the relation requiring a to beat exactly one of b,c and lose to the other. Equal values fail.

The compact input is an integer B>=2 in binary and a Boolean circuit H with 2 ceil(log_2 B) explicitly represented input wires. For base labels i<j<B, H(i,j) specifies whether i beats j. A fixed interpreter reverses the answer for j<i and rejects equality. Thus every well-formed H defines a tournament, without requiring a difficult semantic validity check.

The interpreter completes the base tournament to a regular tournament on q=2B+1 values. Use originals v_i=i, copies v_i'=B+i, and z=2B. Within originals and within copies retain the base orientation. For distinct i,j, let v_i beat v_j' exactly when v_j beats v_i in the base tournament. Also let v_i beat v_i', let z beat every original, and let every copy beat z.

If v_i has h_i base wins, its completed outdegree is

\[
h_i+(B-1-h_i)+1=B.
\]

Its copy has the same total, and z also has B wins. Hence the completed tournament is regular and has odd order.

The decision problem asks whether some x<q satisfies the fixed two-clause expression

\[
G(x)=R(x,0,1)\land R(2B,x,B).
\]

The second clause accepts exactly the original labels, because z beats originals and loses to copies. This is the previously constructed one-unknown-variable problem. The circuit H is part of the input and can vary between instances with the same alphabet size. The result does not assert hardness for a single fixed cyclic tournament at each size.

## 5. A locally computable compiler into this target

Use a fixed-record 3CNF source F on k explicitly represented Boolean variables with h clauses, and let n denote its encoded length. The header gives k and h; it is followed by k fixed declaration slots and h clause slots, each containing three sign/index records. Variable-index fields have width ceil(log_2(k+1)); all record offsets follow arithmetically from the header. In particular k+h=O(n). Pad with at most two unused variables to ensure k>=2. This does not change satisfiability.

For source hardness, choose this format while generating the local Cook–Levin instances used in the standard 3SAT version of [1, Section 3]. The encoding choice preserves their local access property: each bounded-arity Boolean constraint is replaced by a constant-size 3CNF gadget; reserve a fixed number of clause and auxiliary-variable slots for each constraint; number an auxiliary variable by its constraint slot and its constant-size local index; and pad unused clause slots with tautologies. Literal records are then determined by one local constraint descriptor and O(log n)-bit index arithmetic. Variable declarations and fixed-width padding cost at most logarithmic factors. Thus this representation retains quasilinear size, polylogarithmic requested-bit generation, and logarithmic scratch space. This invokes the standard local Cook–Levin completeness construction; it does not assert that an arbitrary parenthesized SAT text can be reformatted with equally cheap indexed access.

Set

\[
B=2^k+2,\qquad q=2^{k+1}+5,\qquad
\ell=\lceil\log_2 B\rceil=k+1.
\]

Let base labels 0 and 1 be anchors. For every k-bit y, let u_y=2+int(y). Orient 0 toward 1, 1 toward every u_y, and u_y toward 0 if and only if F(y)=1. Orient candidate pairs by their numerical order. Then

\[
R(u_y,0,1)\iff F(y)=1.
\]

The two anchors fail by equality. After regular completion, the second clause filters out all added labels. Consequently

\[
F\text{ is satisfiable}\iff \exists x\,G(x).
\]

The required H circuit, evaluated only on canonical base pairs i<j<B, is

\[
H_F(i,j)=\neg\bigl([i=0]\land[j\ge2]\land
F((j-2)\bmod2^k)\bigr).
\]

On the exceptional pairs (0,u_y), this is NOT F(y), as required for the orientation from 0 toward u_y. On every other canonical pair it is 1, giving precisely the stated base tournament.

To implement H_F, choose one fixed gate layout:

1. O(k) regularly indexed gates form the guards and the k low bits of j-2. Ripple subtraction, AND, OR, and NOT suffice, with XOR expanded into constant-size Boolean gadgets if used.
2. Compile each source clause into three sign-dependent literal gates, two OR gates, and one running-conjunction gate. A positive literal can use an OR gate with the same input twice; a negative literal uses NOT. Initialize the running conjunction to true.
3. Append a constant number of gates combining F with the two guards and complementing the result.

There are O(k+h) gates. Use fixed-width gate records containing a gate tag and predecessor indices. Each record has O(log(k+h)) bits, so the entire compact instance has

\[
L=O((k+h)\log(k+h))=O(n\log n).
\]

An indexed output-bit procedure first determines the section, gate record, and field from the requested bit position. A guard/arithmetic gate record is determined by its index through arithmetic on O(log n)-bit numbers. A clause gate record needs at most one source literal record, obtained by fixed-record random access, followed by wire-index arithmetic. The binary header for B consists of a 1 in position k and a 1 in position 1; no integer with 2^k separately stored cells is constructed. Gate counts and field widths follow from the source header.

Thus each requested output bit costs polylog(n) time and O(log n) workspace. Any syntactic validation needed for the standard source format can be performed once by scanning its fixed-width records in n polylog(n) time and O(log n) space; malformed strings map to a fixed no-instance. Counts and records are checked against the actual input length before being used.

This proves the local-reduction hypotheses for that standard 3SAT source. Its FLMV eligibility uses the standard local completeness reductions discussed in [1, Section 3], not the assertion that every NP-complete encoding automatically preserves time and space. Composing the local source reduction with this compiler preserves polylogarithmic output-access cost and logarithmic scratch space.

Therefore the specified compact odd-tournament language has no uniform deterministic solver using both L^{1+o(1)} time and L^{o(1)} workspace. The stronger fixed-exponent exclusion in Section 3 also applies.

This local-compiler argument is symbolic. No new finite experiment is being offered as evidence for the asymptotic lower bound.

## 6. Relation to the charged resource project

The result measures the compact encoded input length L. The alphabet may be exponentially larger: q=2^{k+1}+5. Expanding the tournament table is unnecessary in the reduction and is not imposed on the hypothetical solver.

For an implementation of our charged model that can be simulated in the stated random-access model with only polylogarithmic overhead, the same exclusion follows. Ordinary charged bit operations, bounded-word addressing, and paid data movement can meet this condition. An operation that evaluates an arbitrary supplied circuit or searches an entire exponentially large table at unit cost would not.

FLMV workspace is auxiliary memory excluding read-only input. Our physical peak-memory measure may include that input, and physical CM sums retained storage across time. Those are different quantities. This theorem proves a simultaneous time/workspace exclusion; it supplies no independent CM lower bound. A separate simulation and accounting lemma would be required for a CM-specific conclusion.

A polynomial-time solver with larger time exponent or larger workspace remains compatible with this theorem. In particular, the excluded region is compatible with either P=NP or P!=NP. The advance here is a rigorous transfer of a known restricted lower bound to the compact one-variable, two-clause construction.

## References

1. Lance Fortnow, Richard Lipton, Dieter van Melkebeek, and Anastasios Viglas. *Time-Space Lower Bounds for Satisfiability*. Journal of the ACM 52(6), 835–865, 2005. Theorem 1.1 and Sections 2.1 and 3. Author manuscript: https://lance.fortnow.com/papers/files/tst.pdf
2. Project construction and predecessor: *T_odd proof continuation: tight explicit bounds, live-input memory, and a compact NP-complete target*, 22 November 2026. https://chatgpt.com/library?file_id=libfile_37b1d853fb7481918dd7186969a79c23&account_id=personal