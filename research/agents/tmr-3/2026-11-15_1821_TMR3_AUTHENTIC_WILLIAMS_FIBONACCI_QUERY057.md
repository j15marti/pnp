# TMR-3/057: A genuine Williams computation graph with Fibonacci tree-unrolling cost

**2026-11-15 18:21 PST | Track B / C3-WILLIAMS-IMAGE-QUERY-BRIDGE**

**Status:** PROVED/EXACT only for a precisely declared authenticated blank-start machine and a specified duplicate-recomputing tree evaluator. Independent mathematical review OPEN; finite checks COMPUTATIONAL. No general improved Tree Evaluation simulation, SAT lower bound or P-versus-NP separation.

## Candidate and four falsifiers

**Candidate:** Construct a single fixed, blank-start, finite-control work-tape machine whose actual Williams block-respecting graph has predecessor edges from time blocks i-1 and i-2 into block i for all i>=3. Show that a no-cache recursive evaluator of this actual graph makes Fibonacci-many node calls, although the same authentic source language admits a streaming, logarithmic-workspace algorithm.

F1: The claimed edge i-2 to i might not match an actual previous block visit. Verify original work-head positions and intervening blocks.

F2: One of the inputs might be semantically unnecessary. Verify the node function depends on both the previous state and old work cell across authentic original inputs.

F3: The construction might require hidden input-length advice, preloaded tapes, uncounted parsing or an invalid time-block interpretation. Use one fixed program with paid source authentication and blank-tape setup.

F4: A legitimate sharing, caching, pebbling or algebraic shortcut could remove the exponential cost. Preserve that shortcut; the result must be stated only against the specified no-memoization evaluator, not the Cook-Mertz evaluator.

## Exact source and fixed physical machine

For every b>=3, B>=1 and x=(x_1,...,x_B) in {0,1}^B, set

\[
X_{b,B,x}=1^{b-1}0\,\prod_{j=1}^{B}(x_j1^{b-2}0),
\qquad N=b(B+1).
\]

A uniform sequential-input grammar authenticator counts the header length b using O(log N) writable bits, checks all B records and rejects any malformed binary source. Conservatively its bit-machine time is O(N log N), workspace O(log N); it rewinds the original read-only head for a subsequent paid pass.

One fixed finite-control machine, independent of b,B,x, begins with a blank locally headed work tape and a read-only source head. During the header, b-1 genuine moves position the work head at cell b-1. It maintains one state bit p=0 and one direction bit d=right. At the first symbol x_j of each b-character record it reads the actual work-cell symbol a (blank=0), writes and remembers

\[
c_j=p\oplus a\oplus x_j.
\]

During the b-2 filler symbols it keeps the work head stationary. On the final zero it moves the work head one cell in direction d and reverses d. Thus the active work position is b-1 for odd stages and b for even stages; within a b-step time block, the work head accesses only one block and crosses the boundary on the final transition. The read-only source head accesses the corresponding fresh b-cell record. The machine ends by outputting p=c_B. The authentication phase adds no free preloaded data or oracle.

The actual processing suffix pays exactly N source-symbol steps (plus a terminal stop), b-1+B work-head moves, and visits precisely b+1 work cells, including the setup sweep. Its two physically distinct active cells are updated at alternating stages. Set c_{-1}=c_0=0. At stage j, the actual work-cell symbol equals c_{j-2}, because the last same-cell visit was stage j-2, or blank at stages 1 and 2. Therefore for every source word

\[
\boxed{c_j=c_{j-1}\oplus c_{j-2}\oplus x_j.}
\]

For j>=3, previous-state and old-cell inputs can be varied independently by earlier authentic input symbols, so neither dependency is a phantom source. The work-tape subgraph of Williams's Section 3.2 construction has both the mandated consecutive-time edge i-1 to i and the distinct most-recent-same-block edge i-2 to i for every i>=3. Source and other tape edges are additional legitimate dependencies.

## Theorem 057-A: exact unrolled-query count

Consider the fixed tree evaluator recursively expanding BOTH predecessors of stage j whenever it computes c_j, with no caching, sharing or algebraic simplification. Its positive-index stage invocation count Q_j obeys Q_{-1}=Q_0=0 and

\[
Q_j=1+Q_{j-1}+Q_{j-2}.
\]

With the Fibonacci convention F_0=0, F_1=1, induction gives

\[
\boxed{Q_B=F_{B+2}-1=2^{\Omega(B)}.}
\]

The authentic graph has only O(B) distinct stage nodes and constant indegree, yet its direct no-sharing unfolding makes exponentially many stage invocations. Each invocation is an actual charged operation. A source-rescanning, locally headed, depth-first implementation has the same-run conservative ledger

\[
Q=F_{B+2}-1,\quad
\Omega(Q)\le T_{\rm DFS}=O(N^2Q+N^2),\quad
S_{\rm DFS}=O(B\log(N+2)).
\]

Every original-input seek, stack return value, node index, and output is charged. This is a lower bound on THIS PARTICULAR evaluator's query volume, not on any optimal evaluation strategy, Cook-Mertz, or all original source algorithms.

Choose b=s, B=s^2 for integers s>=3. Then N=s^3+s, B=Theta(N^{2/3}) and

\[
\boxed{Q=2^{\Omega(N^{2/3})}.}
\]

Therefore the inference "the graph is succinct and each node is cheap, so this unrolled evaluator has polynomial running time" is false on an actual block-respecting Williams image. This directly addresses the open C3-WILLIAMS-IMAGE-QUERY-BRIDGE step left after TMR-3/056, whose generic quantified tree did not establish this special-image fact.

## Theorem 057-B: a legal, cheap, same-source algorithm

Following the same source authentication, retain two previous-value bits (a,p) initialized (0,0). Read each x_j and update

\[
(a,p)\leftarrow(p,a\oplus p\oplus x_j).
\]

Return p. Induction using the displayed physical-cell recurrence establishes complete both-label correctness on all authenticated inputs, while malformed words are rejected. One standard multitape source implementation has simultaneously

\[
\boxed{T_{\rm direct}=O(N\log(N+2)),\quad
S_{\rm direct}=O(\log(N+2)).}
\]

It does not claim to reconstruct the original tape's b+1 visited cells; it computes the same decision output. Thus the exponential no-cache tree is a LEGAL ALGORITHMIC SHORTCUT FALSIFIER, not evidence of intrinsic computation hardness.

## Full same-realization ledger

| Execution | Paid time | Peak writable space |
|---|---|---|
| One grammar authentication and source rewind | O(N log N) | O(log N) |
| Original genuine work-tape processing suffix | N+O(1) source steps; b-1+B real work moves | b+1 visited original work cells |
| No-cache recursive evaluator, including source seeks and output | Omega(Q), upper O(N^2 Q+N^2) | O(B log N) stack/index/registers |
| Direct source-aware simulator, including grammar checks | O(N log N) | O(log N) |

The resources in different rows are not borrowed across different machines to manufacture a favorable DTISP pair. The source graph edge relation itself can be generated from parity of time index in O(log B) auxiliary space. Graph ACCESS is cheap here but naive repeated node VALUE evaluation is not. The original machine has a cheap streaming shortcut, so no universal time or space lower bound follows.

## Four required gates

| Gate | Verdict and reason |
|---|---|
| DISJ sanity | **PASS restricted:** the proof uses neither static cut rank nor a general-circuit work lower bound. The construction itself is a cheap affine/XOR control. |
| Relativization | **NOT APPLICABLE WITH REASON:** no separation is claimed. Nonrelativizing P-versus-NP steps, algebrization and Natural Proofs premises are not invoked. |
| Simultaneous DTISP | **PASS within each declared execution**; **OPEN for general Williams and SAT transfer**. The naive time lower bound and direct simulator space upper bound are never merged into a fictitious same-machine result. |
| Configuration counting | **PASS as an upper-bound consistency check only:** deterministic total halting runs satisfy T<=2^{O(S+log N)}. No probabilistic or quantum consequence is claimed. |

Additional Horn, 2-SAT, treewidth, unique-solution, local-basis, randomized-isolation and auxiliary-variable controls are not direct hypotheses of this machine-graph theorem. Compact computation, caching and recomputation remain legal. Historical /341 remains FAIL as a full UNSAT authority, /386 RESTRICTED. P versus NP OPEN.

## Executed reproducibility and historical reconciliation

Standard-library CPython 3.13.5, revision **tmr3-fibonacci-williams057-v2**, seed 20261115, run twice; raw JSON byte identical. **96,239 assertions, zero failures;** 2,604 authenticated binary sources, 124,476 real source-symbol steps, 29,664 authentic two-parent edge checks, 864 actual unrolled recursive evaluations, and 360 malformed-source rejections. All large-B Fibonacci counts were computed symbolically with arbitrary-precision integers; no exponential tree was physically traversed.

At b=8, B=64, encoded N=520, the physical suffix makes 520 source steps and visits nine writable cells; the specified recursion would make exactly **27,777,890,035,287** stage-node calls. This finite comparison is an illustration, not asymptotic proof by testing.

Files: research/agents/tmr-3/2026-11-15_1821_TMR3_AUTHENTIC_WILLIAMS_FIBONACCI_QUERY057.md; experiments/tmr/tmr3_fibonacci_williams057.py; results/raw/tmr/2026-11-15_1821_TMR3_WILLIAMS_FIB057_PY_RAW.json; owned root main3_PNP_TIME_SPACE_TRADEOFFS.tex and compact TMR-3 handoff. Executed source blob 529f004b925dcff51ea31563d8148e18a99241d5, raw blob 5c39382b98be8e4a983ed98032b13521cbe1e473. No independent native finite-TM transition-table compilation, full repository checkout/preflight, LaTeX build or generic Cook-Mertz execution was performed.

Originals consulted: governing end-to-end and compatible SAT-compression directives; full prior TMR-3/056 owned manuscript and stacked draft /054-/056, all five current TMR handoffs and relevant peer manuscript sections, recent issue #3 records; primary Williams 2025 Section 3.2 and Cook-Mertz 2024 theorem statement; classical graph-pebbling literature. Fibonacci expansion itself is old and no priority over classical dynamic programming or pebbling is claimed.

## ONE next load-bearing lemma

**C3-NONASSOCIATIVE-SHARING:** on the actual general Williams block-respecting image, construct and fully charge a generic node-value evaluator or virtual checkpoint provider that avoids the naive exponential duplicated calls even when transitions cannot be compressed into two affine bits. Prove the adaptive query count Q(B,b), every actual source/node access, all retained state and same-run time and peak space; then establish any genuinely improved height exponent, or falsify the proposed improvement with a source-authenticated counterexample. No unrestricted SAT separation or general cube-root-space improvement has been shown.

### Primary references

[1] R. Ryan Williams, *Simulating Time With Square-Root Space*, STOC 2025, Section 3.2, https://arxiv.org/html/2502.17779 .

[2] J. Cook and I. Mertz, *Tree Evaluation Is in Space O(log n log log n)*, STOC 2024, https://doi.org/10.1145/3618260.3649664 .

[3] D. A. Carlson, *On Reducing the Space Requirements of a Straight-Line Algorithm*, SIAM J. Comput. 1984, https://doi.org/10.1137/0605042 .

END_OF_VERIFIED_REPORT::TMR3::057
