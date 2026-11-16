# TMR-4/057 | 2026-11-15 17:40 PST | No-advice formula-to-OBDD compiler

**Scientific status: KNOWN THEOREM (Sethi-Ullman/Ershov ordering) + PROVED/EXACT RESTRICTED transfer; independent mathematical review OPEN.** Tests are COMPUTATIONAL. P versus NP OPEN.

## Candidate, precise source, four falsifiers, complete chain

**Named dependency D4-CROSS-ORDER, CLOSED only for read-once formula trees.** For every binary Boolean formula with n>=1 **distinct** original input leaves x0...x(n-1), n-1 unique binary gates carrying any of 16 two-input truth tables, one root output, and **no internal fan-out**, uniformly construct an efficient topological evaluation schedule **without supplied layout advice**, then compile the original function to a complete read-once branching program preserving both Boolean labels and exact accepting-path multiplicities. The source is an encoded tree, not an arbitrary shared circuit DAG or arbitrary SAT algorithm. Reject malformed encodings.

Pre-search falsifiers: (1) shared DAG fan-out invalidates disjoint-subtree recursion; (2) repeated input identities invalidate read-once and independent count products; (3) layout search, graph authentication, temporary wire values, head movement and exact arithmetic are not free; (4) semantically cheap alternate computation can evade any syntactic frontier cost. The first two are explicitly rejected, the third charged, and the fourth is a genuine all-AND counterexample.

**Actual pipeline:** original encoded formula + separate original input x -> parser/authenticator -> Sethi-Ullman label computation -> generated topological schedule -> real last-use frontier -> previous TMR-4/056 gate-preserving stage translation -> complete layered OBDD -> exact terminal bit and integer accepting count -> rank bound on *this* discovered permutation. A separate bottom-up exact-count algorithm is a legal cheaper alternative.

## Primary sources and original corpus

R. Sethi and J. D. Ullman, *The Generation of Optimal Code for Arithmetic Expressions*, JACM 17(4), 715-728 (1970), https://doi.org/10.1145/321607.321620; A. W. Appel and K. J. Supowit, *Generalizations of the Sethi-Ullman Algorithm for Register Allocation*, Software: Practice and Experience 17, 417-421 (1987), https://doi.org/10.1002/spe.4380170607; R. Sethi, *Complete Register Allocation Problems*, SIAM J. Comput. 4(3), 226-248 (1975), https://doi.org/10.1137/0204020. The tree ordering is classical, not a claimed new lower bound. The last source emphasizes the difference for general shared DAGs.

Original project material inspected: TMR-4/056 detailed report, executable and owned manuscript (source report blob eab0cecefaf7220eda6db46e77ed7fb552f35b28; code 016a84ec39b91e57c7865591008beeb16bb630b0); TMR-2/056 connected-cycle cheap counting and TMR-1/056 charged source-to-CNF transfers; issue #3 recent comments and all five role handoffs; TMR-4/054 pending mincut draft and TMR-3 stacked unmerged PR #174 remain separate. Retired text trackers were not consulted.

## D4-057A: authenticated, uniformly discovered, logarithmic live frontier

For each original input leaf v define r(v)=1. For original binary gate v with children a,b, calculate
\[
r(v)=\begin{cases}
r(a)+1,&r(a)=r(b),\\
\max\{r(a),r(b)\},&r(a)\ne r(b).
\end{cases}
\]
A full graph authenticator checks identifier coverage, exact input use, exactly one consumer per nonroot gate, single output pseudo-consumer, references and acyclicity. Postorder compute r, then emit the subtree with higher r first, followed by its sibling and the original gate. Ties use deterministic fixed ordering. This schedule actually visits each vertex once and never reorders an operand's semantic position: only **evaluation order**, not the ordered truth-table input arguments, changes.

Let ell(v) be last actual consumer position, with the root consumed by the terminal output pseudo-use, and let
\[
L_t=\{v:\operatorname{pos}(v)\le t<\ell(v)\},\quad
w=\max_t|L_t|.
\]
The classical Sethi-Ullman exchange argument for disjoint expression trees proves this is an optimal once-only original-tree topological layout, with w=r(root). When a subtree needing p live results finishes before one needing q, the two peak candidates are max(p,1+q) and max(q,1+p); complete the larger one first. Interleaving the two disjoint child computations cannot improve their optimal peak (tree-ordering exchange lemma). A subtree of label k has at least 2^(k-1) leaves. Therefore for all n,
\[
w=r(\mathrm{root})\le1+\lfloor\log_2n\rfloor .
\]
This is a bound on original **syntactic live gate values without recomputation**, not an all-circuits minimal memory bound. This stage needs no source-supplied topological order.

## D4-057B: exact all-step source-to-target transfer and independent count

The computed schedule first emits some genuine original x_j, not necessarily x0. The requirement in the /056 **test harness** that the initial token equal x0 is not needed for its mathematical induction: the first input's true index j is stored in the stage selector, and each subsequent physical read seeks the original coordinate. The input order rho is the actual permutation of introductions; original variable labels are **not renamed**.

Partition at each input introduction into n read-once register stages, retaining exactly the previous live frontier. Every source gate occurs in one stage, sharing within that stage is preserved. Each gate predecessor is either already evaluated in the current stage or carried from the previous live frontier, because it has a genuine future use. Induction on all original schedule vertices proves equality of every intermediate gate value for **every x**, and hence both terminal labels. Merge only identical (stage, frontier-tuple) states and retain two distinct input-labelled outgoing arcs even if the target states coincide. Input words are then in bijection with complete labelled paths, so exact accepting-path **multiplicities** equal original #C.

There are at most 2^w_i distinct boundary states, therefore the full OBDD has
\[
V\le n2^w\le2n^2,\quad
\operatorname{rank}_K(M_{\rho_{\le i},\rho_{>i}}(f_C))\le2^{w_i}
\]
for every field K and every prefix of this actual rho. Reverse inference only forces w_i >= ceil(log2 rank) for that **particular original-source schedule**, never gate size or generic SAT work.

An even cheaper end-to-end exact counter uses the source disjoint subtree variable sets directly. For every leaf, the count pair is (c0,c1)=(1,1), and for gate truth table tau,
\[
c_z(v)=\sum_{\substack{i,j\in\{0,1\}\\\tau(i,j)=z}}
c_i(v_L)c_j(v_R).
\]
At the root c1=#C, without building an OBDD. Counts need at most n+1 bits, and both zero and one labels remain distinct.

**True shortcut:** A balanced AND tree of n=2^k independent inputs has optimal nonrecomputing structural frontier k+1, but its Boolean decision is just AND(x0,...,x(n-1)), computable by one sequential source-input sweep with one accumulator bit plus actual source validation, input-head position, and bookkeeping. Exact #C=1 is also immediately recognizable after source authentication. An optimal original-DAG schedule does **not** lower-bound unrestricted equivalent computations.

## SAME_REALIZATION complete resource charges

Let L count the **whole** source encoding, M=2n-1, w<=1+floor(log2 n), B=O(L+(n+nw)ceil(log2(2n+w+2))) emitted stage bits, and
\[
D=1+L+B+O(n2^w(w+n+\log_2(n2^w+2)))=O(L+n^3).
\]
A uniform, deliberately conservative locally headed deterministic multitape physical implementation first authenticates source topology and truth tables, computes labels and full schedule (including failed checks and parameter/tie choices), constructs actual last-use/frontier slots, writes shared original gate records once, enumerates all reachable stage-register states with two real outgoing arcs, performs exact integer path-count additions, evaluates the same original x, and emits both decision and integer #C. Source parsing, source/head addresses, gate/index bits, caches, table searches, retained values, temporary stage gate buffers, input permutation seeks of O(n^2) movements, sharing, failed paths, arithmetic precision and output are all included. A conservative joint single-execution upper bound is
\[
T_{\rm total}=O(D^5+n^2),\quad S_{\rm peak}=O(D).
\]
A separately specified **one-execution** direct subtree-count route uses O(L^3+n^3) bit time and O(L^2+n^2) peak bits with naive parsing/scans and quadratic schoolbook products on n-bit integers. Neither bound claims sublinear space. No network spans, simultaneous incompatible machines or abstract unit-cost lookup were substituted. The Python finite audit is a high-level implementation, **not** a physical TM instruction trace.

## Mandatory four gates and hostile controls

| Gate | Status |
|---|---|
| DISJ sanity | **PASS restricted; FAIL proposed general circuit transfer.** DISJ_k is itself a linear-size read-once AND-of-pairs formula, with cheap tree schedule; its grouped X:Y assignment matrix nonetheless has rank 2^k. Only **actual discovered-order prefix** rank is charged. |
| Relativization | **PASS intermediate, unrestricted OPEN.** Tree ordering is combinatorial and relativizing, not the missing nonrelativizing NP separation; algebrization/Natural Proofs audit still required for any future universal claim. |
| Simultaneous DTISP | **PASS same-run upper ledger, unrestricted forbidden region OPEN.** Both time and peak space are for one compiler/evaluator. No strict FLMV contradiction. |
| Configuration counting | **PASS upper-bound guard only.** For deterministic total read-only-input machines T<=2^O(S+log N), or 2^O(S) when S>=log N; not a work lower bound, and no probabilistic/quantum extension. |

Malformed, shared, repeated-identity, cyclic, unreferenced and wrong-arity trees are rejected. Real all-AND, DISJ, equality, XOR/affine, Horn, 2SAT, bounded-treewidth, autarkies, independent products, padding, selector projection, unique-solution rank-one assignment tensors, alternate compact/shared circuits, preprocessing and recomputation remain cheap legal pathways. Invertible local bases preserve cut rank; Walsh-Hadamard over F2 is singular. Valiant-Vazirani is randomized and promise-sensitive. /341 is FAIL as full UNSAT authority; /386 remains RESTRICTED.

## Reproducible executed evidence

**Actually executed local CPython 3.13.5**, exact published standalone source revision tmr4-ershov057.v1, random.Random seed 20261115, 184 valid source formulas, 10,200 exhaustive assignment comparisons, 132,818 original-and-target gate-step replays, 7,904 materialized outgoing arcs, 184 independently calculated integer #count comparisons, **72 independent all-topological-order optimum dynamic-programming checks**, 1,760 GF(2)/GF(101) prefix-rank tests, and seven malformed-rejection controls. **405,811 assertions, zero failures**. Additional balanced AND n=8,16,32,64,128 semantic shortcuts checked. Finite result status COMPUTATIONAL, symbolic result scoped and external independent review OPEN.

Code: experiments/tmr/tmr4_ershov_schedule_e2e057.py, exact SHA256 698cac7ed38d431ffc7252a82e98388a7a3a748ca27249d1c50a983eeaa95b07.
Raw JSON: results/raw/tmr/2026-11-15_1740_TMR4_ERSHOV057_PY_RAW.json, exact SHA256 986f7bb338065c47de918f8a4ebadf5059376387aa0c6e37736c102137be24cd.
Seed 20261115; no local repository checkout because github.com DNS unavailable, so project preflight was NOT run. Native Python executed, not Lean, formal kernel, nor physical TM trace. LaTeX compilation and complete repository CI must be separately reported if performed.

**ONE next load-bearing dependency, D4-DAG-LAYOUT-RECONSTRUCTION (OPEN):** produce a uniform, fully costed low-frontier discoverer for a true, nontrivial **shared-gate DAG** class beyond read-once formula trees, preserving explicit fan-out, or show a precise obstruction in an authenticated source family while retaining legal semantic shortcuts. Arbitrary-circuit, unrestricted SAT and P-vs-NP conclusions remain OPEN. The five existing agents/schedules and retired tracker files are untouched.
