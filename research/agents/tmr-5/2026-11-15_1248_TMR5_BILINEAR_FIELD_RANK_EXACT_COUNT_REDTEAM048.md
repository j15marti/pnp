# TMR-5/048: Bilinear rank-field collapse, polynomial exact #SAT and independent multicut reproduction

**November 15, 2026, 12:48 PST | TMR-5 / PNP Machine Bottleneck Redteam | Tracks A/C, B audit**  
**Scientific status:** PROVED/EXACT for the explicitly scoped algebraic family; independent mathematical peer review OPEN. Finite evidence COMPUTATIONAL. General SAT-machine and circuit lower-bound transfer OPEN. **P versus NP OPEN.**

## 1. Candidate, quantifiers, and falsifiers

For every integer k>=1 and **every explicitly supplied** binary k-by-k matrix B of binary rank r, define the fixed-formula assignment indicator
\[
 f_B(x,y)=x^\top B y\bmod2,\qquad x,y\in\{0,1\}^k.
\]
M_B is the 2^k-by-2^k 0/1 x:y matrix of this one relation, NOT the SAT decision language on formula encodings. The candidate independently checks TMR-2/051's special case B=I and TMR-4/052's switch-product transfer, then extends the rank spectrum and exact counting to every B.

Precommitted falsifiers: (F1) DISJ has rank 2^k yet linear circuits; (F2) field characteristic changes rank, and Walsh-Hadamard is not invertible over F2; (F3) an explicit B admits Gaussian elimination without constructing the exponentially large truth matrix; (F4) alternative variable orders, legal sharing, strictly charged auxiliary gates and exact counting can defeat an apparent ordered-frontier barrier.

## 2. New general bilinear theorem and symbolic proof

**Theorem BILCOUNT048-A (PROVED/EXACT restricted):** For all k>=1, B in F2^(k-by-k), r=rank_F2(B) and any field K,
\[
\boxed{\operatorname{rank}_K M_B=
\begin{cases}
r&\text{if characteristic }K=2,\\
2^r-1&\text{otherwise},
\end{cases}}
\]
and the number of distinct Boolean rows is exactly 2^r. Furthermore,
\[
\boxed{\#\{(x,y):f_B(x,y)=1\}=(2^r-1)2^{2k-r-1}.}
\]

**Proof.** Binary Gaussian elimination supplies invertible L,R satisfying L^TBR=diag(I_r,0). The corresponding invertible binary changes of coordinates for x and y permute Boolean input tuples. Hence, over EVERY coefficient field, the truth matrix differs from the r-dimensional inner-product-mod-two truth matrix only by repeated rows/columns and row/column permutations. These do not alter rank or distinct-row count. The number of satisfying input pairs acquires the multiplicity 2^(2(k-r)).

For IP_r, over characteristic two the evaluation matrix equals the sum of r coordinate outer products. Its singleton-coordinate r-by-r minor is I_r, so rank is r. Its 2^r distinct rows encode 2^r distinct linear forms. For characteristic other than two, H_(u,v)=(-1)^(u dot v) is the Sylvester matrix. It obeys HH^T=2^r I and is invertible; M=(J-H)/2. The u=0 row is zero. A dependence among the remaining M rows would express a dependence among the independent H rows, since J's row is H_0, so the M rank is 2^r-1.

Exactly 2^k-2^(k-r) choices of x give B^T x nonzero. Each of those defines a nonzero linear form in y, accepting precisely 2^(k-1) y values. Multiplication gives the formula. The r=0 case is zero. QED.

This generalizes TMR-2/051's B=I and rational-field result to **arbitrary binary bilinear forms and every field characteristic**. The argument is elementary, and no literature priority is claimed.

## 3. Explicit exact-counting shortcut, including strict 3CNF transfer

**Corollary BILCOUNT048-B (uniform restricted #SAT algorithm):** From the k^2 explicitly encoded bits of B, a single deterministic read-only-input bit Turing machine copies B, computes rank r by Gaussian elimination and writes the closed-form (at most 2k-bit) count. A conservative same-execution ledger is O(k^5) bit operations and O(k^2) peak writable bits, including access/index arithmetic, matrix storage, scratch and output. An even simpler O(k^2) source scan finds one B_ij=1, yielding explicit witness x=e_i, y=e_j, or recognizes B=0 as UNSAT. No truth table, oracle, exponential number, or precomputed advice is used.

Construct a functional Tseitin CNF for the O(k^2)-gate AND/XOR circuit evaluating f_B. Every original x,y assignment has **exactly one** auxiliary extension; the output constraint accepts iff f_B=1. Thus its full CNF count is the expression above. The conversion uses O(k^2) distinct gates, variables, clauses and wire occurrences and O(k^2 log k) bits to serialize (all polynomial, not uncharged). Standard constant-zero pin gadgets pad short clauses to strict proper ternary clauses when required. For B=I, the original fully specified TMR-2/051 strict ternary compiler has V=4k+2, C=7k+4, 21k+12 literal occurrences and the same count (2^k-1)2^(k-1). That exact strict-clause compiler was inspected but not independently exhaustive-recompiled in this run.

When r=k, the odd-characteristic cut rank is 2^k-1 while **exact #SAT is still computable in polynomial time** from B. This is a stronger control than merely exhibiting an easy SAT witness. A universal rank-to-#SAT-runtime implication assigning superpolynomial cost is **FALSIFIED** by this explicit legal Gaussian shortcut. The canonical structural encoding can be recognized and B recovered with polynomial overhead, but no general polynomial #3SAT algorithm follows: other inputs still require an unrestricted correct fallback.

The grouped x-first/y-second complete read-once BDD has width 2^r because all 2^r residual rows differ. For B=I, interleaving x_i,y_i yields width <=4 and a linear-size shared circuit; changing order is legal and not free if finding it incurs costs. For arbitrary dense B the binary normalization can take O(k^3) elimination time and O(k^2) state, and any resulting changed-basis circuit must be charged. No large grouped cut rank forces a general SAT machine to materialize the matrix.

## 4. Independent reproduction of TMR-4/052

The source's restricted switch-product theorem states that for any fixed original-variable order pi and any bipartition X:Y, if D_pi(X:Y) lists adjacent order switches and q_i counts distinct prefix residual functions, then
\[
\operatorname{rank}_K(M_{X:Y}(f))\le\prod_{i\in D_\pi(X:Y)}q_i
\]
over any field K. Independently: expand the deterministic complete residual-state automaton into sums over states at each switch boundary. Each complete selection of boundary states contributes the product of an X-only scalar function and a Y-only scalar function, thus one rank-one outer product. There are at most product q_i such tuples. Shared BDD node identities are not double charged, and the result is a restricted representation theorem, not a machine-time tariff.

I independently enumerated all 720 orders and all 62 proper bipartitions of six original variables for both DISJ_3 and IP_3. Residual truth tables and matrix ranks were independently constructed over GF2 and F65521: **89,280 order/partition/function comparisons, zero failures**, with 3,168 tight odd-prime comparisons per function. The false unqualified rank<=one-frontier transfer remains defeated: DISJ_3 grouped rank=8, legal interleaved peak=3, and O(k) general gates. TMR-4/052 remains **PASS/RESTRICTED** under its actual fixed-order switch-aware model.

## 5. Independent finite replay and exact provenance

Standalone standard-library Python 3 program: experiments/tmr/tmr5_bilinear_exactcount048.py, revision tmr5-bilinear048-v1; deterministic seed **202611151248** (only k=4 seeded choices), prime **65521**, no dependencies. It exhausts all k-by-k binary B for k=1,2,3 (2+16+512 matrices); checks 131 distinct seeded/structured matrices at k=4 and identity B at k=5. For every B it exhausts all 4^k original x,y assignments and independently checks both ranks, row count, satisfying-pair count and nonemptiness. DISJ/full-singleton rank controls run for k=1..5. All interleaved IP prefix residual counts are checked k=1..4. The fully separate TMR-4 multicut test covers 89,280 comparisons.

**137,258 executable assertions; zero failures.** Raw result: results/raw/tmr/2026-11-15_1248_TMR5_BILINEAR048_PY_RAW.json. Regenerate with Python 3 and compare parsed JSON. Local exact Git blob SHA before publication: source 1d46b5cb015e6d486201d3fd2ff7b0d7c4feae07; raw c4839321f41cc6ae5e67ff52511bb43988d70384. Full postmerge blob readback is required.

| k and B=identity | GF2 rank | odd-char rank | exact #satisfying pairs |
| ---: | ---: | ---: | ---: |
| 1 | 1 | 1 | 1 |
| 2 | 2 | 3 | 6 |
| 3 | 3 | 7 | 28 |
| 4 | 4 | 15 | 120 |
| 5 | 5 | 31 | 496 |

The experimental matrix enumerator uses exponential memory to *check* the theorem. The separate Gaussian counting algorithm uses polynomial time and O(k^2) workspace. Finite evidence is COMPUTATIONAL, not a proof of unrestricted bounds.

## 6. Mandatory four gates

| Gate | Verdict | Exact scope |
| --- | --- | --- |
| DISJ sanity | **PASS scoped; FAIL proposed general rank-to-hardness** | DISJ has exponential rank, linear circuit and all-zero witness. Full-rank bilinear controls have polynomial exact #SAT. |
| Relativization, algebrization, Natural Proofs | **PASS scoped; OPEN unrestricted** | These algebraic identities are relativizing intermediate facts. No nonrelativizing general SAT proof step has been supplied or claimed. |
| Simultaneous DTISP | **NOT APPLICABLE WITH REASON** to a separation; **PASS same-realization counter** | One explicit Gaussian counting machine has T=O(k^5) and S=O(k^2), but those are not an FLMV forbidden pair. General hierarchy transfer and Tree Evaluation same-time-and-space remain OPEN. |
| Deterministic configuration counting | **PASS guard only** | The total input-read-only Gaussian machine obeys T<=2^O(S+log N), with N=Theta(k^2); this is a runtime UPPER bound, not a lower bound. Quantum/randomized extensions do not follow automatically. |

Controls retained: Horn/2SAT, affine/Gaussian, bounded treewidth, expander Horn, equality, autarkies, independent products, padding, shared gates, input rereading, compact circuits, unique-assignment full tensor rank one, Valiant-Vazirani's randomized promise, functional auxiliaries and coefficient-bit charges. Historical /341 full logical UNSAT authority **FAIL**, /386 **RESTRICTED**.

## 7. Ranked synthesis and next repair

| Rank | Dependency | Verdict |
| ---: | --- | --- |
| 1 | TMR-2/051 IP rank, cofactor width and count on B=I | **PASS/RESTRICTED**, algebra independently proved |
| 2 | New every-B exact rank/count and uniform Gaussian shortcut | **PROVED/EXACT RESTRICTED**, peer review OPEN |
| 3 | TMR-4/052 switch-product multicut rank | **PASS/RESTRICTED**, proof plus 89,280 replay comparisons |
| 4 | TMR-1/051 Williams P=NP implies NEXP not subset P/poly conditional class audit | **PASS/CONDITIONAL**, NOT an NP-level separation |
| 5 | TMR-3/050-051 explicit graph-enumeration and configuration protocol | **RESTRICTED/OPEN**, not arbitrary Tree Evaluation or FLMV |
| 6 | Static rank or grouped OBDD width forces general SAT/#SAT runtime | **FAIL**, actual cheap paths |
| 7 | Fully charged unrestricted circuit/SAT-machine bridge and superpolynomial obstruction | **OPEN** |

**Weakest surviving load-bearing lemma:** no candidate invariant yet survives both every-B polynomial Gaussian exact counting and legal compact/shared circuits while compelling arbitrary SAT-machine work.

**Next peer repair:** TMR-2/4 should formulate one *charged, uniform, representation-aware* dynamic invariant that stays small on bilinear B of arbitrary growing rank, DISJ and Horn-expanders, then prove a nontrivial fixed-model circuit/branching-program transfer. TMR-1 must not relabel NEXP/E^NP targets as NP; TMR-3 must produce one matched full time/space Tree Evaluation realization. No OPEN load-bearing gate is promoted.

**State/corpus and source versions.** Read the 2026-11-15 SAT-compression directive FIRST (SHA 7b8804dc7587abc5134055b5b0d16a143055ca5a), TMR replacement directive, AGENTS.md, CODEX.md, pnp-research skill, current five TMR handoffs, issue #3 and relevant originals TMR-1/051 (SHA 5a97902607d6ccfd682b245c01a50f74b23a1329), TMR-2/051 (f720d5482637709f48f0b955d9020fa6643d027e), TMR-4/052 (5753712fdd848be1b81125d5427c7431bb71d67f), and TMR-3/049. Primary literature checked: Bryant, *Graph-Based Algorithms for Boolean Function Manipulation* (1986), https://doi.org/10.1109/TC.1986.1676819 ; Alman and Williams, *Probabilistic Rank and Matrix Rigidity* (2016), https://arxiv.org/abs/1611.05558 , including its inner-product/Hadamard setting. Neither Lean paper nor full suite rebuilt. Root proof1.txt was visible (SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343); proof2.txt (SHA 930c5eeddafce656717f28055a7a755f44737c) and main.tex (SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34) returned empty connector bodies, so no complete-current-body shared edit was attempted. Local git fetch/preflight was blocked by container DNS. **TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE.** All five scheduled tasks and ownership preserved. **P versus NP OPEN.**
