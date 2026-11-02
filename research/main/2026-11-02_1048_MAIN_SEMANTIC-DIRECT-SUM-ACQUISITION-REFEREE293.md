# SEMANTIC-DIRECT-SUM-ACQUISITION-REFEREE293

**Role:** LSPV-5 Formal Proof Red Team  
**Time:** 2026-11-02 10:48 PST, America/Los_Angeles  
**Status:** PROVED elementary deterministic source-probe theorem; COMPUTATIONALLY CHECKED finite controls; REPRESENTATION-SPECIFIC implementation audit; unrestricted superlinear SAT lower bound, contraction, and P versus NP remain OPEN.

## Controlling correction and exact obstruction

This run began with the verified five-page *General SAT Through Semantic Hypergraph Reduction* follow-up and its package, then the verified nine-page general signed-hypergraph report and package. The active target is arbitrary CNF-SAT, correct on both labels. The all-phase space correction is mandatory:

\[
s'\le \max\{\rho,\eta,\lambda,\lambda s\},
\]

where \(\rho\) covers preprocessing, parsing, order discovery, conversion, child generation, inference, combination, and checking—not merely state retained while a child call is pending.

The obstruction attacked here is the proposed inference that a minimal logical/semantic DAG and its shortest reduction path determine generalized computational work independent of algorithm. Post-projection relations may be tiny, and post-answer circuits may be constants, while acquiring the correct relation still requires source access. Conversely, a source-authenticated derivation DAG has a cost only after its allowed rules and representation are fixed.

## Construction

Let \(F_1,\ldots,F_t\) be proper 3-CNFs on disjoint private variables and disjoint occurrence-sign coordinates. For each block introduce a boundary bit \(x_j\) and fresh private \(y_{j,i}\), and replace every clause \((a_{j,i}\vee b_{j,i}\vee c_{j,i})\) by

\[
(\neg x_j\vee a_{j,i}\vee y_{j,i})\land
(\neg y_{j,i}\vee b_{j,i}\vee c_{j,i}).
\]

Call the conjunction over all blocks \(H\), and let \(R_H\subseteq\{0,1\}^t\) be its exact projected boundary relation. Existentially eliminating \(y_{j,i}\) gives \(\neg x_j\vee a_{j,i}\vee b_{j,i}\vee c_{j,i}\), hence

\[
x\in R_H\quad\Longleftrightarrow\quad
\forall j\;(x_j=0\ \lor\ F_j\in\mathrm{SAT}). \tag{1}
\]

The whole region is always SAT at \(x=0^t\). Define the designated query \(q_j=e_j\), with \(x_j=1\) and every other boundary bit zero. Then

\[
q_j\in R_H\quad\Longleftrightarrow\quad F_j\in\mathrm{SAT}. \tag{2}
\]

## Direct-sum acquisition/query theorem

Assume each \(F_j\) is clause-minimally UNSAT and has \(L_j\) independently addressable occurrence-sign fields. Fix a deterministic compiler \(C\) and an exact query procedure \(Q\). The compiler reads the joint source once and emits any descriptor: a source pointer, circuit, DAG, cache, program, table, or answer bits. Each designated query is then run from that descriptor; it may reread the source. All compiler and query probes are charged.

Let \(E_j\) be the sign coordinates of block \(j\), \(R_C\) those inspected by compilation, and \(R_j\) those inspected while answering \(q_j\). Then

\[
\boxed{|(R_C\cup R_j)\cap E_j|=L_j\quad\text{for every }j.} \tag{3}
\]

Consequently, for single-bit sign probes,

\[
\boxed{P_C+\sum_{j=1}^t P_{Q_j}\ge \sum_{j=1}^t L_j,} \tag{4}
\]

and ordinary probes exposing at most \(w\) sign bits require at least \(\lceil(\sum_jL_j)/w\rceil\) probes in aggregate. Extraneous reads only increase the charged cost.

**Proof.** Fix block \(j\), clause \(C\), and occurrence coordinate \(e\in C\). Clause minimality supplies an assignment satisfying \(F_j\setminus\{C\}\) and falsifying every literal of \(C\). Flipping only sign \(e\) makes the same assignment satisfy all of \(F_j\). Equation (2) therefore changes the exact answer to \(q_j\) from NO to YES. If neither compilation nor the \(q_j\) run inspected \(e\), determinism gives an identical combined transcript and output on the two same-skeleton sources, contradiction. Sum the disjoint block inequalities. ∎

The theorem also holds for a stateful session in the weaker but sufficient form that the union of all source coordinates inspected over compilation and all designated queries contains every sign coordinate.

## Tightness and the small-DAG counterexample

In the declared fixed-skeleton sign-probe model, choose arbitrary \(p_j\in[0,L_j]\). Compilation caches exactly \(p_j\) signs from block \(j\). Query \(q_j\) streams the other \(L_j-p_j\) signs as needed during exhaustive assignment evaluation. This gives equality in (4) on the minimally UNSAT base sources. No semantic oracle is used; the time is exponential.

On the joint base input, equation (1) gives

\[
R_H=\{0^t\}.
\]

After one sensitive sign flip in block \(j\), the relation is exactly \(\{0^t,e_j\}\). These relations have \(O(t)\) formulas, and each designated answer after acquisition has a zero-gate constant circuit. Nevertheless, the exact compile-plus-query session pays \(\sum_jL_j\) distinct sensitive-source probes. Therefore:

* **FALSIFIED:** minimal post-projection DAG size, minimal answer circuit size, or shortest path *after the answer is known* equals representation-independent generalized computation work.
* **SURVIVES ONLY WITH A MODEL:** if the DAG must start from the authenticated source and each edge is an allowed paid transformation, then its minimum path is a proof/compilation-system measure. It is not automatically a lower bound for every SAT algorithm.

This does not reject source-authenticated reduction DAGs as useful restricted models. It rejects the model-independent promotion.

## Full work and peak-space charge

For the concrete fixed-width-support implementation, let \(P=\sum_jp_j\). A streaming grammar/support scan, sign-cache construction, source reads, exhaustive query, answer combination, and final witness/conflict check are all charged. Query \(j\) performs \(O(2^{n_j}L_j)\) literal tests in the worst case. Its abstract live-bit bound is

\[
S_{\rm peak}\le P+\max_j n_j+O(\log N), \tag{5}
\]

when the immutable fixed-width support is kept on the read-only input and clause offsets are computed arithmetically. A conventional parser that materializes the support must add that storage. The Python harness materializes Python objects and is **not** an FLMV tape simulation; equation (5) is the declared abstract implementation, not a measured host-RSS claim.

Materializing the guarded CNF requires \(M=\Theta(N)\) bits and therefore \(\rho=1\), even if freed before any query or guest call. A virtual accessor avoids that buffer but pays every source/index access. Moreover the exhaustive query uses \(n_j=\Theta(N/\log N)\) assignment-counter bits on these standard encodings, still exponent \(1-o(1)\), and exponential time. Thus this explicit implementation satisfies neither the \(\rho\le1/2\) baseline nor the contraction time target.

The direct-sum lower bound is linear input acquisition. It supplies no superlinear time bound and no positive polynomial workspace lower bound: input sensitivity and workspace are different resources.

## Falsifiers and outcomes

1. **Shared compilation makes the aggregate sensitive-source cost sublinear.** Falsified by (3)-(4); it may move probes between phases but cannot remove them.
2. **A singleton boundary relation or constant answer circuit makes total semantic-reduction work constant.** Falsified: the base relation is \(\{0^t\}\), yet all sensitive signs are acquired across the exact session.
3. **An \(N\)-bit temporary conversion buffer is compatible with square-root peak space if freed before queries.** Falsified: its local phase alone gives \(\rho=1\).
4. **The linear probe theorem implies exponential time or square-root-space failure for every algorithm.** Falsified. It is tight linear source access; the displayed exhaustive implementation is only a witness to tight phase allocation.
5. **Dense separator tables are mandatory.** Falsified on the four Tseitin controls by their compact GF(2) contradiction; this run does not promote dense-table width to unrestricted work.

## Independent finite controls

The producer and a no-producer-import verifier checked five clause-minimally UNSAT inputs: odd Tseitin encodings on \(K_4\), \(K_{3,3}\), the cube, and the Petersen graph, plus W1. Totals:

| Check | Result |
|---|---:|
| Complete source assignments | 70,208 |
| Sensitive sign coordinates | 396 |
| Same-skeleton SAT sign-flip witnesses | 396 |
| Compile/query splits per block | 3 |
| Malformed inputs rejected | 6 |
| Independent assertion groups | 421 |

At compile prefixes \(p=0,L/2,L\), every block had exactly \(p\) compilation coordinates, \(L-p\) new query coordinates, and \(L\) combined distinct coordinates. The finite exhaustive query made 845,994 sign probes in total at \(p=0\), 77,362 at half caching, and zero query probes after eager full-sign caching. These are host-language logical probe counts, not native instruction counts.

## Literature and project audit

Primary-paper searches performed before the proof work:

* `Darwiche Marquis Knowledge Compilation Map JAIR 2002 primary paper succinctness queries transformations` — confirms that succinctness, supported queries, and transformations are separate dimensions: https://doi.org/10.1613/jair.989
* `Fortnow Lipton van Melkebeek Viglas Time-Space Lower Bounds for Satisfiability author manuscript primary` — inspected the author manuscript and strict same-machine scope: https://lance.fortnow.com/papers/files/tst.pdf
* `Dechter Bucket Elimination unifying framework reasoning 1999 primary paper` — confirms representation/order-dependent induced-width costs and conditioning tradeoffs: https://ics.uci.edu/~csp/r48b.pdf
* `Boolean decision tree sensitivity all relevant variables deterministic query lower bound primary` — related decision-tree influence literature was found, but the present adversary is the elementary unread-bit transcript argument; no novelty is claimed.

GitHub searches:

* `semantic reduction acquisition query cost space rho` in `j15marti/pnp` found the immediately preceding LSPV-4/339 two-phase theorem and older acquisition ledgers. REFEREE293 therefore contributes the multi-query direct sum and the explicit minimal-DAG falsifier, not a duplicate one-block theorem.
* `SAT semantic reduction acquisition exact interface` in `github.com/openai` found no relevant certified SAT-interface implementation. This negative search proves no novelty.

The LSPV-4/339 report was independently read at commit `a9578a8ee1d3f6b29802fab937e4cea9e17e0c1e`. Issue #3 and the current general-SAT commits were inspected. No task, title, enabled/paused state, or schedule was changed.

## Exact remaining gap

The next missing result is not another small descriptor or table-width bound. It is either:

1. a representation-inclusive, all-input **superlinear** same-machine acquisition-plus-query lower bound surviving parity, circuits, lazy source references, early termination, and representation switches; or
2. an assumption-dependent, uniformly iterable arbitrary-\(A\) transformation satisfying \(N^{3/5+o(1)}\) sequential children, \(N^{1/2+o(1)}\) child length, \(N^{11/10+o(1)}\) all-phase local work, and \(N^{1/2+o(1)}\) all-phase peak space.

REFEREE293 proves neither. **P versus NP remains OPEN.**

## Reproduction

```bash
python3 experiments/arc/lspv5_293/semantic_direct_sum_referee293.py
python3 experiments/arc/lspv5_293/verify_semantic_direct_sum_referee293.py
```

