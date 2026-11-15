# TMR-3/054: End-to-end canonical streaming-graph reconstruction with charged virtual access

**2026-11-15 15:30 PST | PNP Time-Space Tradeoffs | Track B | STREAMGRAPH054**

**Result:** PROVED/EXACT for the fixed-state, binary streaming-machine class and explicitly declared virtual indexed-source/forward-replay interfaces; independent mathematical review OPEN. Finite execution is COMPUTATIONAL. This is an actual blank-start input-to-output model, not a preloaded-checkpoint suffix. It is NOT an improvement to the general Cook--Mertz Tree Evaluation algorithm or Williams's arbitrary-multitape time-space simulation. P versus NP remains OPEN.

## 1. End-to-end target, candidate and falsifiers

**Target chain:** binary original input \(x\) -> a fixed deterministic machine with a *previously written* work-symbol dependency -> its authentic \(B\)-block movement graph -> authenticated blank-start anchor construction -> paid virtual graph/node-bit accesses -> height-\(B\) restricted comb-tree evaluator -> exact YES/NO output -> simultaneous time/space ledger.

**Candidate:** for the canonical reachable configurations of any fixed finite-state streaming machine of the type below, checkpoint *state and head position* can be reconstructed with periodic anchors, unlike the unrestricted all-preloaded-checkpoint service of TMR-3/053. The provider and evaluator can be instantiated end-to-end with explicit \(Q\), source/index and anchor-tape read costs, and a legal streaming shortcut. This closes a narrowly scoped interface-construction arrow, not the generic evaluator arrow.

Falsifiers stated before source/corpus search:

1. A query answers only the movement bit but not the actual work-state/head-position checkpoint or an original-source read is free.
2. The stored anchors, their sequential-tape retrieval, query addresses, all \(Q\) uses or source rereads exceed the claimed peak space/time.
3. The result silently covers arbitrary preloaded checkpoint states, arbitrary work-tape revisits or a general TreeEval operation instead of the fixed-state canonical source model.
4. An adversarial input-head seek or legal streaming fusion defeats a purported *unconditional* near-linear runtime lower bound for querying the graph.

## 2. Concrete blank-start machine and output

Fix a constant \(C\ge2\) and a fixed total transition table
\(\delta:[C]\times\{0,1\}\to[C]\times\{0,1\}\).
On a read-only original binary word \(x_1,\ldots,x_B\) with an explicit endmarker, a fixed-control deterministic multitape machine starts with its writable tapes blank. The initial blank in writable STATE cell 0 is interpreted as \(q_0=0\) (no separate initialization transition), and MOVE's head starts at cell 0. At input step \(i\), the *actual written symbol* \(q_{i-1}\) at STATE[0] and source symbol \(x_i\) determine \((q_i,m_i)=\delta(q_{i-1},x_i)\). The same paid transition rewrites STATE[0] as \(q_i\), advances the input head, and advances MOVE's head one cell right iff \(m_i=1\). Then a terminal step outputs whether \(p_B\ge\lceil B/2\rceil\), with \(p_i=\sum_{j\le i}m_j\). The terminal test can be performed by a separate simulator with an \(\lceil\log_2(B+1)\rceil\)-bit counter, rather than by materializing MOVE's complete visited tape; a physical original-machine terminal comparator would itself need to be implemented and charged if attached to the concrete MOVE-head service.

Precisely scoped physical service: the original head-motion suffix has \(B\) paid input/update/movement transitions plus a paid stop; STATE occupies one accessed work cell and MOVE visits \(p_B+1\) writable cells. The source is one canonical blank-start input, NOT an arbitrary preloaded checkpoint. To realize the stated Boolean decision on the original locally headed machine, add a third blank work tape LENGTH whose head advances right once on each of the same \(B\) input steps, ending at position \(B\). At the endmarker a finite-state comparator moves LENGTH left twice per one MOVE left step until one reaches the detectable left boundary. It accepts iff LENGTH reaches the left boundary no later than MOVE, exactly when \(2p_B\ge B\), with an explicit empty-input accepting case. This adds at most \(O(B)\) physical transitions without visiting more than \(B+1\) LENGTH and \(p_B+1\) MOVE cells. Hence the completed original decider has \(T_{\rm orig}=\Theta(B)\) and \(S_{\rm orig}=\Theta(B)\). The executable checks the \(B\)-step update/graph prefix and the mathematical Boolean threshold, not the original terminal comparator's native transition table. The graph movement label at block \(i\) is genuinely \(m_i\), determined by a previously written work symbol. The decision relation is explicitly \(F_\delta(x)=[p_B\ge\lceil B/2\rceil]\). There is no connection to SAT hardness.

The witness table \(q_i=q_{i-1}\oplus x_i\), \(m_i=q_i\) creates \(2^B\) distinct authentic graph words as \(x\) varies, because prefix parity is a bijection on binary words. It does NOT create \(2^B\) graphs on one fixed original input. Direct source recomputation of prefix parity is a genuine legal shortcut.

## 3. The end-to-end indexed-source provider

**Theorem 054-A (PROVED/EXACT, model-scoped).** Fix \(B\ge1\), \(1\le L\le B\), constant \(C,\delta\), and a standard deterministic *indexed read-only source-symbol* primitive whose address generation and reading take \(O(\operatorname{polylog}B)\) bit-machine operations. Writable anchor storage is an ordinary **sequentially headed** tape; no free random-access work array exists. There is one blank-start, uniform simulator which:

* makes one forward pass over and authenticates the binary input;
* stores \(R=\lceil B/L\rceil\) anchors at times \(0,L,2L,\ldots <B\), each recording \((q_a,p_a)\);
* responds correctly to every adaptive request \(j\in\{1,\ldots,B\}\) for the authentic \((q_j,p_j,m_j)\), by scanning to the preceding anchor and replaying at most \(L\) actual source transitions;
* evaluates the height-\(B\) left-comb arithmetic tree with leaves \(m_j\), internal functions \(v_j=v_{j-1}+m_j\), \(v_0=0\), and root YES iff \(v_B\ge\lceil B/2\rceil\), in the deterministic query order \(1,\ldots,B\).

The evaluator uses **exactly \(Q=B\)** leaf requests. Setting
\(w=\lceil\log_2 C\rceil+\lceil\log_2(B+1)\rceil\), the same complete implementation obeys

\[
S_{\rm total}(B,L)=O(Rw+\log B)
\]

writable bits and

\[
T_{\rm total}(B,L,Q)
=O\bigl((B+Q(L+Rw))\operatorname{polylog}(B+2)\bigr)
\]

actual bit-machine time in the declared indexed-input model, including initial authentication, anchor writing, sequential anchor-tape seeking, source-symbol index arithmetic, all query replays, the \(O(\log B)\)-bit comb accumulator and the final output. This upper bound is conservative, not a native instruction trace. The actual number of read source symbols in the finite implementation is exactly \(B+\sum_{\rm queries}(j-a_j)\), where \(a_j=L\lfloor(j-1)/L\rfloor\); its anchor tape scan reads/visits \((\lfloor(j-1)/L\rfloor+1)w\) bit cells per request when restarted from anchor 0.

**Proof.** After the initial pass each anchor has its authentic \((q_a,p_a)\) by induction on source positions. For request \(j\), retrieve \(a_j\) by scanning the sequential anchor tape, copy the \(w\)-bit record into the controller and iterate the fixed \(\delta\) over source bits \(x_{a_j+1},\ldots,x_j\). Determinism gives the exact \((q_j,p_j,m_j)\), even when addresses and query order are adaptive. The original source is not modified and no materialized \(B\)-bit graph is stored. After the \(j\)-th comb update its accumulator equals \(p_j\); hence its final YES/NO is correct for every binary source, including ties. Each stored checkpoint uses \(w\) bits; live source/query indices, scratch, accumulator and response use \(O(\log B)\) additional cells, simultaneously with the anchors. The preprocessing examines \(B\) source bits. Each request uses at most \(L\) indexed source reads and scans at most \(Rw\) physical anchor bit cells, with polylogarithmic overhead for addresses and arithmetic. Thus summing the **paid** disjoint stages yields the displayed bounds. No uncertain shared resource lower bound is added separately. QED.

For \(L=\lceil\sqrt B\rceil\), this single-machine *upper* ledger gives \(S=O(\sqrt B\log B)\) and \(T=O(B^{3/2}\operatorname{polylog} B)\) for \(Q=B\). These are bounds as a function of the true \(B\)-bit source and the true \(B\)-step original service. **They are not a new generic \(T^{1/3}\)-space simulation**: identifying \(T=B\cdot\sqrt B\) by padding idle transitions would be an illegitimate achievement claim. The arbitrary-height Cook--Mertz function family is not realized here.

## 4. Exact static-forward coverage lemma and legal shortcut

**Theorem 054-B (PROVED/EXACT in the static-forward architecture).** Suppose a provider is constrained to store only checkpoints of the genuine state after selected times \(a\), must start each requested value \(m_j\) from the greatest checkpoint strictly before \(j\), and must perform at most \(L\) forward replay steps. Its set of checkpoint times including \(0\) must contain at least \(\lceil B/L\rceil\) entries. Uniform spacing \(0,L,2L,\ldots<B\) attains the bound.

**Proof.** The gaps from 0 through all internal checkpoint positions to the terminal boundary \(B\) are positive integers whose sum is \(B\); the replay requirement forces every gap to be at most \(L\). At least \(\lceil B/L\rceil\) gaps, hence that many checkpoint anchors before the terminal boundary, are needed. Uniform spacing is feasible. QED.

This is NOT a universal bit-space lower bound. An alternative compressed transition-monoid product, prefix-parity formula, reordered evaluator or cached query history can avoid these checkpoint records. LSPV-4/465 already proved a related exact static source-header checkpoint Pareto law; the current model changes the object to authenticated **work-dependent graph state**, includes the comb evaluator and charges the sequential anchor lookup and all \(Q\) node requests. We do not claim priority for the general checkpointing idea.

**End-to-end streaming control.** For this fixed-state class, a second one-pass simulator updates its own finite state and \(O(\log B)\)-bit count while reading the original source once. It decides the same \(F_\delta\) in \(O(B\operatorname{polylog} B)\) time and \(O(\log B)\) space without graph queries. This is a genuine compact and shared computation, not a defect to be outlawed. It proves why the \(Q=B\) black-box provider/evaluator cost is an **upper-bound construction**, never an intrinsic machine lower bound.

**Sequential source-head firewall.** Theorem 054-A's fast arbitrary requests assume charged *indexed* read-only input. Replacing it by an ordinary single locally moving input head adds up to \(\Theta(B)\) head movements **per request** under alternating far-apart replay queries. For \(B=64,L=8,Q=64\), the exact specified restarted-replay schedule uses 3,809 source head movements just to reposition for alternating queries \(64,1,\ldots\), before the separately counted bit reads and anchor moves. A generic claim \(O(Q L)\) under this sequential input model is false; caching, a changed schedule or a direct streaming algorithm remain legal escapes.

## 5. Relation to block-respecting reduction and hypothetical improved evaluator

Williams [1], Sections 2--3, constructs constant-fan-in implicit TreeEval instances using actual block-respecting machine configurations and the guessed head movement graph. The Cook--Mertz evaluator's \(O(db+h\log(db))\) space and its runtime are separately relevant. This report does not substitute a comb tree for Williams's unrestricted node functions or validate the guessed graph for an arbitrary adaptive work tape. It establishes that a **specific canonical work-dependent graph** has a fully generated physical input/query/evaluator interface and a legal compact implementation.

For any future generic evaluator issuing \(Q\) requests of cost \(A(B,L)\) with own time \(W\) and space \(S_E\), a composition must charge
\[
T_{\rm comp}=T_{\rm authenticate}+T_{\rm anchors}+W+\sum_{i=1}^{Q}T_{{\rm access},i}+T_{\rm output},
\qquad
S_{\rm comp}=\max_{\rm phases}S_{\rm live}
\]
on the **same implementation**, with Q and per-access positioning and state restoration proved. Simply substituting \(h=B\) and \(\alpha=1/2\) into an algebraic square-root template is not an implemented evaluator. Generic adaptive work-tape revisits may encode \(\Theta(B)\) independent checkpoint bits as in TMR-3/053, and the present constant-state regeneration does not cover them.

## 6. Mandatory four gates and hostile controls

| Gate | Verdict |
|---|---|
| DISJ sanity | **PASS (restricted).** No assignment-cut rank, static tensor, or graph-count-to-SAT hardness claim. DISJ, Horn, 2-SAT, affine/Gaussian, equality, unique-solution and compact-circuit shortcuts remain admitted. |
| Relativization | **NOT APPLICABLE WITH REASON** to a P/NP separation, none claimed. The source-relative fixed-state identity is not a nonrelativizing separation. Algebrization and Natural Proofs are not invoked. |
| Simultaneous DTISP | **PASS** for the declared indexed-input source-to-output simulator: \(T\) and \(S\) are jointly paid on one implementation. **OPEN** for a general TreeEval and for an arbitrary SAT forbidden-region simulation, where the indexed-source model conversion must also be charged. |
| Deterministic configuration counting | **PASS** as an upper-bound consistency test for a deterministic total machine only. \(T\le2^{O(S+\log B)}\) is not a work lower bound; no probabilistic or quantum extension is asserted. |

Unknown arbitrary work-tape operations are MAY behavior. Real sharing, recomputation, cheap affine transitions, padding, input rereads, cached state, algorithm changes and source authentication are not silently excluded. Historical /341 remains FAIL as a full UNSAT logical authority; /386 remains RESTRICTED.

## 7. Reproducibility and corpus reconciliation

The standalone, pure-JavaScript revision \`tmr3-streamgraph054.v1\` was executed in hosted V8, deterministic seed 20261115 for sampled three-state transition tables. **12,023,735 assertions, zero failures**. The producer exhaustively checks all 256 two-state binary transition tables on all source words of length 1--7; it also checks 16 seeded three-state tables on all source words of length 1--8. It verifies 2,906,528 exact virtual queries, 73,184 complete-source decision/stream comparisons, 45 exact static-anchor minima by exhaustive subset enumeration, and a source-head-seek counterexample. Source-symbol replays and anchor bit-cell visits are counted separately. These finite results are COMPUTATIONAL. No native TM transition-table interpreter, full repository checkout or generic TreeEval kernel was executed; the symbolic theorems are independent of finite enumeration.

**Files on research branch:** \`research/agents/tmr-3/2026-11-15_1530_TMR3_END_TO_END_STREAMGRAPH054.md\`; \`experiments/tmr/tmr3_streamgraph054.js\`; \`results/raw/tmr/2026-11-15_1530_TMR3_STREAMGRAPH054_V8_RAW.json\`; owned manuscript \`main3_PNP_TIME_SPACE_TRADEOFFS.tex\`; historical handoff \`research/agents/tmr-3/handoff.md\`.

Current user-authorized [end-to-end manuscript directive](../../coordination/2026-11-15_END_TO_END_AGENT_MANUSCRIPTS.md) supersedes older file-routing rules. The retired text proof trackers were **not read or edited**. Own manuscript was fully available, with current SHA, and is to be reconciled in place. Original TMR-3/053 was read on draft PR #157 (not on main); old TMR-3/052 source-indexed shortcut was recovered through its handoff; LSPV-4/465 static checkpoints were checked for duplicate scope. Peer handoffs, the issue #3 record and Williams's original HTML paper were reviewed. Local Git clone was blocked by DNS, so repository preflight was not executed.

**Next load-bearing lemma:** a true all-canonical-work-tape **virtual bit-provider**, not limited to a constant-state streaming machine, that handles work-head revisits and writes with a proved \(Q\), access-time bound, simultaneous retained ancestor state, and a nontrivial height-sublinear evaluator whose node schedule cannot simply be streamed. That is where the selected Track B end-to-end program remains OPEN.

## References

[1] R. R. Williams, *Simulating Time With Square-Root Space*, STOC 2025, arXiv:2502.17779, Sections 2--3. https://arxiv.org/html/2502.17779

[2] J. Cook and I. Mertz, *Tree Evaluation Is in Space O(log n log log n)*, STOC 2024; SIAM Journal on Computing 2025, DOI:10.1137/24M1690126.

[3] TMR-3/053, *Work-dependent computation graphs and an exact checkpoint sketch/probe tariff*, draft PR #157, original report path \`research/agents/tmr-3/2026-11-15_1424_TMR3_WORK_DEPENDENT_GRAPH_INTERFACE053.md\`.

[4] LSPV-4/465, *Exact static-anchor checkpoint/recomputation resource frontier for typed TREE3*, original report \`research/agents/lspv-4/2026-11-07_0336_LSPV4_SPARSE_CHECKPOINT_PARETO465.md\`.
