# TMR-5/050: Exact one-switch closure rank lower bound for shared branching programs

**2026-11-15 14:48 PST | TMR-5 / PNP Machine Bottleneck Redteam | Tracks A/C with Track B firewall**

**Status:** PROVED/EXACT for the explicitly scoped mathematical theorem; independent mathematical peer review OPEN. New finite independent experiment is COMPUTATIONAL. No unrestricted circuit or SAT-machine lower bound is claimed. **P versus NP remains OPEN.**

## 1. One candidate and four precommitted falsifiers

**Candidate ONS050:** Combine the *original* TMR-2/053 exact neighborhood-union row-rank theorem with the *original* TMR-4/053 adaptive side-switch communication rectangles. Strengthen the latter at exactly one owner switch by separately charging the number of X-side routing records and Y-side residual records. Quantify whether any such lower bound survives shared-node DAGs rather than unrolled trees.

- **F1:** A shared, acyclic, deterministic binary program with a single owner switch might reuse one Y entry for two distinct neighborhood residuals.
- **F2:** Reconvergent X routing might create r distinct exits from fewer than r-1 X test records.
- **F3:** Interleaved DISJ has rank 2^k but a linear-size, genuinely legal BP and circuit. Any claimed bound covering it without a switch restriction is false.
- **F4:** Complete bipartite, empty, singleton, selector, Horn/2SAT, affine, unique-solution, padding, alternate-basis and input-encoding controls may trivialize the proposed resource transfer.

The candidate concerns the 0/1 assignment-evaluation matrix of **one fixed formula**, not SAT as a Boolean function of formula encodings. Every original graph edge crosses one declared cut. No special oracle or prohibited algebraic shortcut is excluded.

## 2. Exact strengthened theorem

Let G=(A disjoint union B,E) be any finite simple bipartite graph, with only cross edges. Its relation is

\[
D_G(x,y)=\prod_{(a,b)\in E}(1-x_a y_b)
\]

evaluated as a Boolean function. Put

\[
U(S)=\bigcup_{a\in S}N(a),\quad
r=|\{U(S):S\subseteq A\}|.
\]

By the subset-zeta row independence proof in TMR-2/053, **for every field** rank(D_G)=r, and the transpose has exactly r distinct column residuals as well.

A *one-switch BP* is a single fixed deterministic acyclic binary branching program with V distinct nonterminal test-node IDs, each labelled by an input variable on A or B. Tests can repeat and the order may depend on the input; arbitrary reconvergence is legal. The root has a fixed side, and every root-to-terminal path changes sides at most once. The only memory is the current node ID; terminals are 0 and 1. Every actual test is charged. No free switch, alternate machine, unrolled graph or advice is inserted.

**THEOREM ONS050-A, PROVED/EXACT in this model.** Every such program computing D_G satisfies

\[
\boxed{V\ge 2(r-1).}
\]

**Proof.** Assume the root tests A variables; the other case follows by transposition and equality of row and column rank. Let V_A,V_B be the numbers of A- and B-labelled internal nodes actually reachable from the root.

Fix a complete A assignment x. Until the first switch, all decisions depend only on x. Its A-phase exits at one specific B-node, or a terminal. This exit must compute the residual Boolean function g_x(y)=1[U(x)\cap\operatorname{supp}(y)=\varnothing]. Distinct unions U(x) give different residuals, so at least r distinct exits are reachable. Since g_x(0^B)=1 for every x, none of these exits can be the 0 terminal. For every nonempty U(x), g_x is nonconstant and must enter a B-labelled internal node; the r-1 distinct nonempty unions require r-1 **different** B entry nodes. Hence V_B>=r-1. This remains true with arbitrary graph sharing because a deterministic entry node has a fixed remaining Y-only function.

Now restrict the DAG to A-labelled nodes reachable before the switch and their outgoing arcs. It contains V_A internal nodes and at least r distinct exit vertices, all reachable from the A root. Every such vertex other than the root has indegree >=1 from this reachable restricted DAG, so at least V_A+r-1 distinct arcs occur. But each A test node has exactly two outgoing arcs, so 2V_A>=V_A+r-1, whence V_A>=r-1. Adding the two disjoint node populations gives V>=2(r-1). If the root is a terminal, then r=1 and the bound is zero. QED.

**Exact matching corollary ONS050-B.** For the k-edge matching relation DISJ_k, r=2^k, and the minimum size over **all one-switch deterministic acyclic shared binary BPs** is

\[
\boxed{V_{1\text{-switch}}(\mathrm{DISJ}_k)=2^{k+1}-2.}
\]

The lower bound is ONS050-A. A grouped X-then-Y diagram attains it: a full binary X decision tree has 2^k-1 distinct internal test nodes and routes each x subset to its unique canonical Y residual, where the 2^k-1 nonempty subsets produce exactly 2^k-1 distinct shared Y subprogram roots. Every path switches at most once. This is a size theorem, not an exponential per-input evaluation-time theorem: a grouped evaluation still tests at most 2k input bits.

**Tradeoff ONS050-C (independent synthesis of peers, restricted).** TMR-4/053's accepting-transcript factorization yields for an arbitrary b-switch deterministic shared acyclic BP

\[
r\le\sum_{j=0}^{b}V^j\le(V+1)^{b+1}.
\]

Consequently, if V>=1 and b>=1,

\[
\boxed{
b\ge \frac{\log_2 r}{\log_2(V+1)}-1,\qquad
V\ge\left(\frac{r}{b+1}\right)^{1/b}.
}
\]

For matching and V<=k^d, fixed d>0, this yields b=Omega(k/log k). This is **not** a bound on arbitrary circuits or on unrestricted SAT algorithms. The legal interleaved DISJ_k BP has V=2k and b=2k-1, thereby evading the one-switch lower bound. The linear-size depth-two circuit likewise remains fully legal. For K_(k,k), r=2 despite k^2 cross edges, and a simple grouped shared BP has V=2k,b=1.

## 3. Independent reproduction and exact finite controls

The source `experiments/tmr/tmr5_one_switch_closure050.js` was independently written, not copied from the TMR-2/4 verifiers. It constructs its own neighborhood matrices, computes modular elimination over GF(2) and GF(101), independently builds shared DAGs using syntactic node-ID hash consing, executes every original assignment, counts actual owner switches, checks each accepting transcript's rectangle, and compares every rank and size inequality.

**Actually executed hosted V8:** 524 exact matrix pairs (matching k=1..6, complete K_(k,k) k=1..6 and all 512 labelled bipartite 3-by-3 edge sets), 512 separately built grouped cross-graph programs, 18 additional full controls (grouped/interleaved match and grouped complete graphs for k=1..6), 49,148 actual assignment traces, 264 accepting transcript rectangles, **453,817 assertions and zero failures**. No pseudorandomness or seed. Source revision `tmr5-one-switch-closure050.v1`, prime 101. Every 3-by-3 graph passed r=rank(D), r-1=rank(J-D), rank(D+(J-D))=1 and its grouped-BP correctness, b<=1 and two-sided V_A,V_B>=r-1.

The distribution across all 512 3-by-3 bipartite graphs for r=1,2,3,4,5,6,8 was respectively **1,49,144,198,78,36,6**. For k=4 matching: grouped V=30, b=1, r=16, while interleaved V=8, b=7, r=16. For k=4 complete bipartite: V=8,b=1,r=2. These are COMPUTATIONAL checks; the preceding symbolic proofs give the all-size restricted scope. No native Node binary, full repository test suite, or Lean kernel build was executed in this run.

## 4. Same-realization ledger and model mismatch firewall

| Resource | Complete charge / restriction | Status |
|---|---|---|
| Graph source | Every node has one variable ID and two outgoing IDs; stored description uses O(V(log V+log n)) bits and 2V physical arcs, with sharing counted **once** | Explicit BP, NOT free source |
| One BP evaluation | At most V paid tests because the graph is acyclic; every observed branch is charged; owner switch count b is measured on that **same** trace | Exact restricted graph step model |
| Source acquisition and compilation | Constructing the shared graph, discovering an order, preprocessing, switching, unsuccessful attempts and all source reads are **additional** costs | Cannot hide in V |
| Physical TM implementation | Random access to a stored graph has address, head-motion, read and cache overhead; any actual writable workspace, graph materialization and input access must be charged | No claimed TM speed bound |
| Independent verifier | Enumerated up to 2^(2k) original assignments per graph; performs rank elimination on dense 2^k-by-2^k matrices; retains exponential matrices | NOT a fast SAT solver |
| Correct total SAT algorithm | DISJ and all-negative 2CNF have all-zero satisfying witness; a total solver may check it cheaply and use fully paid fallback elsewhere | Genuine cheap path retained |
| Track C interface | TMR-1/053 CNF normalization and E^NP quantitative hierarchy transfer remain conditional on the pinned solver and full source-model validation | NOT a new circuit-to-SAT lower bound |
| Track B interface | TMR-3/053 (draft PR #157) distinguishes preloaded checkpoint graphs from ordinary blank-start machine runs; no sublinear-height tree-evaluation theorem follows | RESTRICTED; unrestricted OPEN |

The restricted graph size lower bound can be exponential while **evaluation uses O(k) BP tests**. It must not be advertised as a decision-time lower bound, a circuit lower bound, or a lower bound on source acquisition of every computational model. All shortcuts using input rerereads, caches, shared circuits, Gaussian elimination, Horn/2SAT, extension variables, autarkies and recomputation remain legal.

## 5. Mandatory four-gate table

| Gate | Verdict | Rationale |
|---|---|---|
| DISJ sanity | **PASS restricted; FAIL unrestricted transfer** | DISJ_k has rank 2^k, exact one-switch BP size 2^(k+1)-2, but legal interleaved BP size 2k, b=2k-1, and linear-size depth-two circuit. |
| Relativization | **PASS restricted; OPEN unrestricted** | DAG/communication counting is a combinatorial intermediate statement. No fully relativizing P-vs-NP separation; the precise nonrelativizing step, algebrization and Natural Proofs audits remain OPEN. |
| Simultaneous DTISP | **NOT APPLICABLE WITH REASON for the BP theorem; OPEN for SAT transfer** | One representation's V and b are not matched physical T(N), S(N) in an FLMV forbidden region. Graph setup, accesses, sequential work and aggregate live state remain charged, no borrowed time or space. |
| Configuration counting | **PASS guard only** | For fixed total deterministic read-only-input machines T<=2^{O(s+log N)}, or <=2^{O(s)} for s>=log N. This is a runtime upper bound and cannot establish necessary work; no automatic probabilistic/quantum transfer. |

Historical /341 is **FAIL** as full UNSAT logical authority and /386 stays **RESTRICTED**. Unique-solution tensors remain rank 1, and invertible local cut bases leave rank unchanged; Walsh-Hadamard is not invertible over GF(2). Valiant-Vazirani isolation is randomized and promise-sensitive. No padding, original-assignment counting, or representation entropy is charged as compulsory physical work.

## 6. Ranked peer dependencies, corpus, sources and next repair

| Priority | Source / component | Verdict |
|---|---|---|
| 1 | TMR-2/053 zeta neighborhood ranks r,r-1,1 | **PASS restricted**, independent algebra and complete 3x3 graph audit |
| 2 | TMR-4/053 adaptive accepting-switch rectangles | **PASS restricted**, independently replayed matching and complete controls |
| 3 | ONS050-A two-sided one-switch V>=2(r-1) | **PROVED/EXACT restricted**, external peer review OPEN |
| 4 | ONS050-B tight matching minimum 2^(k+1)-2 | **PROVED/EXACT restricted**, external peer review OPEN |
| 5 | TMR-1/053 fixed-density normalization and E^NP bridge | **PASS at stated conditional source/model scope**; Anthropic Lean kernel and TM transport NOT independently rerun |
| 6 | TMR-3/053 preloaded all-checkpoint selector (draft #157) | **RESTRICTED**, no blank-start source transfer or improved Tree Evaluation evaluator |
| 7 | Circuit-to-bounded-switch BP compiler for every circuit | **OPEN**; unrestricted transfer would be false if it ignored DISJ |
| 8 | Same-execution strict SAT DTISP and nonrelativizing NP bridge | **OPEN**; P versus NP **OPEN** |

**Corpus reviewed:** current SAT-compression directive first (blob `7b8804dc7587abc5134055b5b0d16a143055ca5a`), five latest TMR handoffs, original TMR-2/053 and TMR-4/053 mathematical reports, code and raw data (blobs `1edb926f`, `b3994d37`, `28d2ea5e`, `30b753b6`), original TMR-1/053 report and pinned Anthropic MainResults.lean, TMR-3/053 draft PR #157, root proof1.txt (complete SHA `06f7ebc8`), proof2.txt and main.tex current SHAs `930c5eed` and `6ac34c5d`, AGENTS.md, CODEX.md, repository skill and issue #3. The oversized proof2/main contents returned empty and were NOT fully recovered; no shared edits. Full repo checkout/preflight could not be performed through this connector-only execution. No new information supersedes original /341 or /386 statuses.

**Duplication / contradiction:** TMR-2/053 supplied exact r; TMR-4/053 supplied the general b-switch rank inequality. The *new* two-sided r-1+r-1 one-switch node-size theorem and matching tightness are distinct. They strengthen only the restricted subclass, not the unrestricted circuit or machine result. Nothing in canonical main.tex is promoted.

**NEXT PEER REPAIR (one target):** TMR-4 and TMR-2 independently verify the two-sided one-switch proof for arbitrary shared acyclic diagrams including repeated tests and reconvergent X/Y phases; then test whether a concrete circuit subclass admits a fully charged compiler to BPs with a provably bounded b. The compiler must reject or correctly account for DISJ's interleaved shortcut, or the transfer fails.

**TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE.** P versus NP remains OPEN.

### Primary source and exact peer locations

1. TMR-2/053 exact zeta ranks: https://github.com/j15marti/pnp/blob/main/research/agents/tmr-2/2026-11-15_1412_TMR2_NEIGHBORHOOD_ZETA_CUT_RANK053.md
2. TMR-4/053 switch rectangles: https://github.com/j15marti/pnp/blob/main/research/agents/tmr-4/2026-11-15_1336_TMR4_ADAPTIVE_SWITCH_RECTANGLES053.md
3. Mehlhorn and Schmidt, communication matrix rank method (1982): https://people.mpi-inf.mpg.de/~mehlhorn/ftp/LasVegasDeterminismVLSI.pdf
4. Wegener, *Branching Programs and Binary Decision Diagrams*, Ch. 6: https://doi.org/10.1137/1.9780898719789.ch6
5. Baker, Gill and Solovay, *Relativizations of the P =? NP Question* (1975): https://doi.org/10.1137/0204037
6. Anthropic MainResults.lean, pinned statement, not kernel rerun: https://github.com/anthropics/formal-math/blob/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth/MainResults.lean
7. TMR-3/053 draft PR #157: https://github.com/j15marti/pnp/pull/157

END_OF_VERIFIED_REPORT::TMR5::050
