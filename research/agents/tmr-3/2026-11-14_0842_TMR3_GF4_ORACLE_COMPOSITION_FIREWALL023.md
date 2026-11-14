# TMR-3/023: GF(4) interpolation oracle gap, linear streaming extension, and the same-machine sharing firewall

**Pacific timestamp:** November 14, 2026, 08:42 PST (America/Los_Angeles).  
**Role:** TMR-3, PNP Time-Space Tradeoffs. **Repository:** j15marti/pnp, main publication proposed through a conflict-safe research branch.  
**New result:** GF4-OR23, **CANDIDATE/RESTRICTED**, complete elementary symbolic proofs below, requiring independent TMR-2/TMR-5 review.  
**Executed finite controls:** **COMPUTATIONAL**. **P versus NP:** **OPEN**.

## 1. Exact objective and concrete service

The ultimate target remains one fixed finite total deterministic multitape 3-SAT decider A across all encoded lengths L, with all real transitions T_A(F) and writable visited cells S_A(F) charged, and

$$
\forall A\ \forall k\ge 1\ \forall C>0\ \forall L_0\ \exists F:
|F|\ge L_0\ \land\ T_A(F)>C(|F|+1)^k.
$$

This report does **not** establish that target. It attacks an intermediate proposal in the November 14 semantic-composition handoff: infer a compulsory high cost for actual Turing-machine block functions from (a) the number of monomials of their canonical multilinear extension, or (b) the number of queries needed when the function is available only as an opaque Boolean-value oracle.

The service here is deliberately **one specific local time-block function**, Boolean OR of b input bits, which a fixed finite-control machine can compute during a single source scan. Its arithmetic extension is evaluated at a fixed non-Boolean point of a constant-size field. The difference between implicit machine descriptions and opaque oracles is the object under test.

## 2. Characteristic-two algebra and unrestricted-workspace oracle bound

Fix $K=\mathrm{GF}(4)=\mathrm{GF}(2)[\alpha]/(\alpha^2+\alpha+1)$. Represent its four elements by two-bit words $a+b\alpha$. In particular $\alpha\ne 0,1$ and $1+\alpha\ne 0$.

For an arbitrary Boolean function $f:\{0,1\}^b\to\{0,1\}$, define its unique multilinear extension over K by

$$
\widetilde f(z)=\sum_{a\in\{0,1\}^b}
f(a)\prod_{i:a_i=1}z_i\prod_{i:a_i=0}(1+z_i).
\tag{1}
$$

**GF4-OR23-A, deterministic black-box lower bound:** A deterministic algorithm which is given $b$ and unit-cost query access ONLY to the Boolean values $f(a)$, and must output $\widetilde f(\alpha,\ldots,\alpha)$ exactly for **every** Boolean function f, needs at least $2^b$ distinct oracle queries in the worst case, regardless of its workspace.

**Proof.** Run the algorithm against the identically-zero oracle. If it queries fewer than $2^b$ locations, choose an unqueried $a^*$. The identically-zero function and the point function $g(a)=[a=a^*]$ have identical transcripts on all queried locations. Their correct extensions differ by

$$
\prod_{i:a_i^*=1}\alpha\prod_{i:a_i^*=0}(1+\alpha),
$$

which is nonzero in the field. The algorithm cannot give the same correct answer on both functions. Therefore it must query every point on the zero oracle. Extra workspace, adaptive selection, cached replies, and repeated queries cannot change this conclusion. This is a **black-box value-oracle** result, NOT a lower bound on evaluation from a succinct circuit or a source-readable machine program.

The model even gifts the oracle answers in one step; implementing queries physically would require at least that many actual transitions and may cost more. No free oracle is used in the purported SAT proof chain.

## 3. A fixed, costed machine violates the tempting descriptive transfer

Define $\mathrm{OR}_b(x)=x_1\lor\cdots\lor x_b$. In K, its multilinear extension is

$$
P_b(z)=1+\prod_{i=1}^b(1+z_i)
      =\sum_{\emptyset\ne S\subseteq[b]}\prod_{i\in S}z_i.
\tag{2}
$$

Thus its exact algebraic normal form has $2^b-1$ **nonzero** distinct monomials, with no cancellation. Nevertheless the factored polynomial has just b constant-field multiplications and can be evaluated in one input scan with one two-bit accumulator. The original Boolean OR is even simpler, one bit of finite control.

**GF4-OR23-B, uniform same-machine upper bound:** There exists **one fixed finite total deterministic locally moving single-read-only-input-head machine B**, independent of b, that accepts a mode bit and either (0) any length-b binary OR payload or (1) any sequence of b two-bit GF(4) elements. It outputs respectively $\mathrm{OR}_b$ or $P_b(z)$, and classifies malformed odd-length field payloads. All symbols are explicitly present in the input, with delimiters. Counting source moves/reads, endmarker, each output write and halt, for its actual bit length L,

$$
T_B(x)\le L+5,\qquad S_B(x)\le 2,
\tag{3}
$$

where S counts every writable output cell visited; accumulator and carry are finite control. There is no preprocessing advice, table lookup, free arithmetic or unbounded word. GF(4) multiplication is a fixed four-by-four finite transition table. This machine is a **restricted block service**, not an all-input general 3-SAT decider.

**Proof / program:** On mode 0, read each bit once and OR into one control bit. On mode 1, read two bits per field element, hold a one-bit pending high digit, and update the two-bit accumulator $p\leftarrow p(1+z_i)$. On the right endmarker output $1+p$ using two charged cell writes; reject odd-length field payloads in a fixed terminal state. Start-marker and mode transitions are charged. Every step moves the source head by at most one cell, and only at most two writable output cells are ever visited. There are finitely many machine states independent of L. An explicit physical-step interpreter appears in the native test source.

**The gap is exponential in the exact same parameter b:** the white-box fixed machine uses $O(b)$ time and constant writable space, even while the canonical ANF has $2^b-1$ terms and a generic opaque-function extension algorithm needs $2^b$ Boolean-value queries. Hence no theorem of the form

$$
\text{ANF monomial count or generic extension oracle complexity}
\ \Longrightarrow\ \text{mandatory block-machine evaluation transitions}
$$

holds without an independently proved **representation- and input-aware transfer**.

A string encoding the expanded ANF literally takes exponential output length, but computing its value does not require materializing the expansion. The time and memory used to print an expanded representation are costs of that representation, not of the function.

## 4. Sharing and recomputation: another explicitly scoped failure

Consider a fixed repeated-node Boolean DAG: $v_0=x$ and $v_i=v_{i-1}\wedge v_{i-1}$ for $1\le i\le h$. A naive binary recursive expression evaluator visits $2^{h+1}-1$ node *occurrences*. The DAG has only $h+1$ distinct nodes, and one fixed sequential evaluator computes it in $O(h)$ transitions using $O(1)$ reusable value space plus charged source/layout costs. A more aggressive algebraic simplification directly returns x. This is a concrete witness that prescribed tree-unfolding work, even when mathematically correct for that evaluator, does not impose a uniform bound on every algorithm.

For our finite controls h=20, the unfolded evaluator has 2,097,151 occurrences versus 21 distinct DAG nodes. This is **COMPUTATIONAL** corroboration of the exact recurrence, not an actual dynamic interpreter of two million steps.

## 5. Simultaneous time/space ledger and scope

| Service or chosen representation | Bound | Space model | Scope |
|---|---:|---|---|
| Opaque arbitrary Boolean f at $\alpha^b$ | $\ge 2^b$ **oracle queries**, even with unbounded workspace | arbitrary | Exact deterministic value-oracle query theorem |
| Expanded ANF of $\mathrm{OR}_b$ | $2^b-1$ monomials | potentially exponential materialized description | Output representation size, not evaluation time |
| Factored $P_b$ on explicit GF(4) values | $T\le L+5$, $S\le2$, $L=1+2b$ | **same fixed B** | Fully charged finite-control local-input machine |
| Boolean OR on explicit b bits | $T\le L+5$, $S\le2$, $L=1+b$ | **same fixed B** | Same total machine, different mode |
| Prescribed unfolded shared DAG | $2^{h+1}-1$ node occurrences | interpreter-dependent | Not an all-algorithm necessity |
| Sequential shared-DAG evaluation | $O(h)$ plus actual encoding/address costs | O(1) reusable values, address/control bookkeeping charged | One chosen implementation |

The streaming source bit length L is not the encoded length of an arbitrary 3-CNF. Likewise b here is the local block arity, not the number of clauses or assignments. A larger Williams/Cook-Mertz simulation cannot substitute equation (3) for a universal bit-generator without proving that its actual node functions have the requisite factorization and that producing/accessing them has been charged.

Williams (STOC 2025) uses implicit Tree Evaluation with maximum height $h=O(t/b)$, constant fan-in and node-value bit length $\Theta(b)$; the Cook-Mertz procedure yields an upper space bound $O(db+h\log(db))$. This is a space statement with potentially expensive running time. The compositional use of implicit functions does not establish a simultaneous polynomial-time/small-space compiler, nor does it require the OR block to be hard. See primary sources [1,2].

The FLMV SAT lower bound [3] excludes restricted simultaneous random-access time/space regions, not all polynomial workspace. Claude's ONETAPE-0001 [4] shows a separate physical input-transport cost that also hits nondeterministic computations. None yields the all-k SAT lower bound. This run does not rederive FLMV constants or transfer its model.

## 6. Executed finite evidence and controls

Native CPython executed in the local container (not a hosted V8 wrapper) with exact GF(4) bit-pair arithmetic, and a physical current-cell scan interpreter:

* 64 associative field-multiplication triple checks, plus identity and commutativity controls.
* 1,022 nonzero independent point-function interpolation weights over b=1..9.
* 276 complete Boolean truth-table function checks over b=1,2,3.
* 16,383 exhaustive physical-mode input strings of lengths 0..13: 13,652 valid outputs, 2,731 malformed classifications, $T-L\le5$, at most two visited writable output cells, zero failures.
* 16 CNF controls with independent assignment enumeration and exact GF(4) extension evaluation: Horn, Horn-UNSAT, 2-SAT, a proper 3-CNF XOR parity pattern, duplicates, shared variables, disjoint products, renaming, and both $U_r$ UNSAT and nearest SAT neighbors for r=1..4.
* 21 recurrence/description size controls for shared DAG depth 0..20, with no model-dependent lower bound claimed.

**Exact native original execution:** local source SHA-256 `b5996137c57a490f453a89551a9edbb49c8965029f57c93f8f6663e2b76c485b`; original full raw output saved locally. **Exact GitHub-byte native replay completed.** After publication I fetched the native source from GitHub, reconstructed its exact bytes locally, checked `git hash-object` = published Git blob `a042e1a022339ceeb4854ed8221027162050e80a`, and executed those bytes directly under native CPython. The SHA-256 of the exact GitHub-byte source is `214b0487ff9ca63a98185ee7aa829e2818670c80f3e877ad3357dc09e44e7345`. Its complete numeric outputs **match** the independent original runner (1,022/276/9/16,383/13,652/2,731/2/5 and zero failures). The two original/published native sources are not byte-identical, and neither has been misrepresented as such. A separate compact GitHub reproduction source is published but was not executed; use the exact GitHub-byte native source as authoritative. The immutable raw ledger records both native execution hashes.

**Published and exact-native-replayed files:** `experiments/tmr/tmr3_gf4_extension023_native.py`, `experiments/tmr/tmr3_gf4_extension023.py`, and `results/raw/tmr/2026-11-14_0841_TMR3_GF4_ORACLE_COMP023_RAW.json`. Verify before promotion. No OS-native generic 3-SAT TM compiler, original peer code replay, LaTeX build or full repository preflight was executed.

## 7. Dependencies, barriers and next test

**Independent review pending:** TMR-2/TMR-5 check nonzero GF(4) interpolation weights, the black-box adversary quantifiers, equation (2)'s all-n coefficients, and finite-control $T,S$ accounting. A field-dependent algebraic encoding is not a representation-independent lower bound. Relativization: the black-box lower bound is explicitly oracle-relativized and therefore does not transfer to white-box 3-SAT. Algebrization: we separately expose extension evaluation, and do not treat its formal degree or number of monomials as time. Natural proofs: no constructive large-circuit property is asserted.

**Next load-bearing target for TMR-3:** extract ONE exact implicit node function from the actual Williams/Cook-Mertz arbitrary multitape simulation. Construct a charged same-machine implementation of its generator and required interpolation/composition service, including adjacency discovery, repeated evaluation, field representation, and persistent/catalytic workspace, then measure the *joint* time/space closure. Try a legitimate factorization or cheap substitution. If false, preserve the smallest full-source counterexample and its actual cost trace.

The unrestricted SAT-to-composition necessity and the all-exponent resource implication remain **OPEN**. Neither a generic black-box extension lower bound nor the known square-root-space simulation resolves P versus NP.

## 8. Provenance and primary sources

[1] R. Ryan Williams. *Simulating Time with Square-Root Space*. Proceedings of STOC 2025, pages 13-23, DOI https://doi.org/10.1145/3717823.3718225 . Model: arbitrary time-t multitape machines; explicit bit-generation of implicit Tree Evaluation; principal conclusion $O(\sqrt{t\log t})$ space, NOT an all-machine polynomial-time joint bound.

[2] James Cook and Ian Mertz. *Tree Evaluation is in Space O(log n log log n)*. STOC 2024, DOI https://doi.org/10.1145/3618260.3649664 ; SIAM J. Comput. 2025 DOI https://doi.org/10.1137/24M1690126 . Space-efficient Tree Evaluation, different input-size accounting and no premise of polynomial time in the small-space mode.

[3] Lance Fortnow, Richard J. Lipton, Dieter van Melkebeek, Anastasios Viglas. *Time-Space Lower Bounds for Satisfiability*. JACM 52(6), 2005, DOI https://doi.org/10.1145/1101821.1101822 . Restricted simultaneous time/space lower bounds for random-access SAT.

[4] Claude ONETAPE-0001, repository original: research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex . The original's crossing-sequence argument is model-restricted; no superpolynomial deterministic SAT separation.

[5] TMR-2/022 original: research/agents/tmr-2/2026-11-14_0823_TMR2_MAXSAT_WALSH_SIGN_ROBUSTNESS022.md . The Walsh-flat maximum robustness recognizer is a cheap algebraic UNSAT control, not a universal solver.

[6] User-directed semantic-composition coordination: research/coordination/2026-11-14_0819_USER_CLAUDE_SEMANTIC_COMPOSITION_REVIEW.md . Its exact rational-midpoint test is complementary, not identical, to this characteristic-two GF(4) test.

**Preflight and integrity:** The authoritative November 13 replacement directive (SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4) was read first. Both proof trackers were read in full: proof1.txt 28,714 characters SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343 and proof2.txt 1,051,196 characters via authentic Git blob SHA 930c5eeddafce656717f28055a7a9a755f44737c. Root main.tex 2,542,866 characters recovered via authentic Git blob SHA 5ec8fffb16ec9a7f262e60321bf5aad172d153d8. AGENTS.md, CODEX.md, pnp-research skill, issue #3 through TMR-2/022, all five TMR handoffs, original TMR-3/020 and TMR-2/022, user coordination report and Claude ONETAPE were consulted. Full corpus-wide lint/preflight script unavailable in connector-only repository mode. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No main.tex modification (TMR-5 owns synthesis), no schedules/tasks changed. No prior result silently promoted.

END_OF_REPORT::TMR-3::023::2026-11-14_0842_PST
