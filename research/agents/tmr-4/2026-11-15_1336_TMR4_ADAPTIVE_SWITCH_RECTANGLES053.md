# TMR-4/053: Adaptive side-switch transcripts are rectangles for shared branching programs

**2026-11-15 13:36 PST | TMR-4, PNP Cost-Sound Abstraction | Tracks A/C.**  
**Status: PROVED/EXACT only for the restricted graph theorem (independent peer review OPEN), COMPUTATIONAL for finite verification, OPEN for unrestricted circuit or SAT-machine transfer. P versus NP OPEN.**

## Candidate and falsifiers fixed before literature comparison

**ASR053.** For every finite *deterministic, acyclic, binary*, shared branching program B with V distinct internal nodes, no variable-order requirement, terminal labels 0/1, and a fixed partition of its input variables X disjoint union Y, define b as the maximum number of changes between X-labelled and Y-labelled test nodes along a root-to-terminal path. Variables may be queried adaptively; in the principal FBDD subclass, each variable occurs at most once per path. No input-dependent choice of B itself is free.

Four attempted falsifiers: (F1) grouped DISJ has rank 2^k but a tiny interleaved FBDD; (F2) branch-dependent order and early termination may spoil a fixed-order frontier proof; (F3) Horn/affine/unique-witness/padding/product functions are computationally easy despite high selected cut rank; (F4) shared nodes, reused tests, and post-projection selector eliminations may invalidate naive billed rank reductions. A genuine compact alternative remains legal.

## Exact lemma and proof

Let M_(X,Y)(f) be the 0/1 assignment-evaluation matrix over an arbitrary field K. Call a **switch transcript** the finite sequence of destination-node IDs on a path whenever the next internal node tests a variable on the opposite side, after the previous side has finished its local segment. The root's side is public. For each accepting computation write tau for its switch transcript. Let H_B(X,Y) be the set of *distinct accepting transcripts* (not all accepting assignments and not the number of graph paths). Then

\[
\boxed{\operatorname{rank}_K M_{X,Y}(f)
 \le |H_B(X,Y)|
 \le \sum_{j=0}^{b}V^j.}
\]

The last summand is interpreted with V=0 as 1 when the diagram consists only of a terminal. When b=0, rank is at most one. This applies to **state-dependent test ordering** and shared nodes, as well as FBDDs; repeated variable tests are admissible to the algebraic lemma if the program remains acyclic. The repeat-free property is checked separately for the reported FBDD experiments.

**Proof.** Alice knows x in X, Bob knows y in Y, and both know the entire fixed B graph. Initially the party owning the root variable simulates consecutive local nodes, following the unique outgoing edge determined by that party's input. Upon reaching a test owned by the other party, the current party transmits *that exact node ID*; the new owner resumes. A terminal is final. This protocol has at most b changes of owner on every input. Fix any accepting transcript tau of node IDs. Each X-only segment has a deterministic consistency condition involving x and the public history tau, and no y-bit; the conjunction of those conditions defines a set A_tau of X-assignments. Symmetrically the Y-segment conditions define B_tau. Therefore the inputs producing this accepted transcript are exactly the Cartesian product A_tau times B_tau. The accepted transcripts partition the 1-cells of the matrix since the program is deterministic. Over **any field**,

\[
M_{X,Y}=\sum_{\tau\in H_B}{\bf1}_{A_\tau}{\bf1}_{B_\tau}^{T}.
\]

Each summand has rank at most 1. Every switch destination is one of V distinct internal node IDs, so the number of length-j switch transcripts is at most V^j. Summing over 0<=j<=b proves the bound. Node sharing is preserved; no graph is unfolded. QED.

**Exact lower-bound corollary, restricted.** If b is externally fixed, V>=1, and R=rank_K M, then R<=sum_(j=0)^b V^j <=(b+1)max(1,V)^b. This constrains only the **preexisting bounded-switch branching-program representation**. In particular an unrestricted circuit may be small while b is large; no circuit or general-SAT work bound follows. Computing H_B from all assignments can itself be exponential and is not an efficient recognition or compression algorithm.

**Concrete-to-abstract simulation.** Abstract state retains the *actual* graph node, the previous side, the switch transcript and the partially read original input assignment. A genuine test transition maps to exactly one abstract test transition, charging one test; a switch message is an additional protocol event and is *not* assumed to be free physical communication. Terminal labels are preserved. The rank identity is an external proof, not a paid runtime potential or an LP certificate. Reverse reconstruction into an arbitrary circuit or SAT decider is OPEN.

## New versus previous corpus

TMR-4/051 proved prefix-cut rank<=frontier for shared fixed-order OBDDs. TMR-4/052 proved a product-of-residual-frontiers bound at every *fixed-order* X/Y switch. This run removes the globally prescribed order and supplies an **adaptive, branch-dependent communication rectangle factorization** with an exact accepting-transcript count; it does not claim external priority over standard deterministic communication protocol rectangle arguments. No inference from semantic multiplicity or all-balanced cut ranks to arbitrary SAT work is made.

TMR-2/052 makes the all-balanced-cut selector warning stronger: two high-rank pinned matrices may sum after *actual functional projection* to J of rank 1. That projection is a legal representation change, not a monotone paid rank discharge. TMR-1/052's width-three pointwise existential-projection census remains a strict **representation** barrier; it does not give general SAT hardness, and it does not imply a cheap or expensive decision-only compiler.

## Executable exact evidence and controls

Published source: experiments/tmr/tmr4_adaptive_switch_rectangles053.js (native deterministic V8; revision tmr4-adaptive-switch-rectangles053.v1; no seed). Raw JSON: results/raw/tmr/2026-11-15_1336_TMR4_ADAPTIVE_SWITCH_RECTANGLES053_V8_RAW.json. The exported function was executed twice with byte-identical JSON output, **30950 assertions, zero failures**, across 25 fully enumerated diagrams and both GF(2) and GF(65521). All 1-cells were independently partitioned by **their actual node-ID transcripts** and each transcript was exhaustively tested to be a Cartesian rectangle. Exact modular Gaussian elimination verified both matrix ranks and their bounds. A malformed directed cycle was rejected.

| Instance | V | b | rank GF(2) | rank F65521 | accepted transcripts |
| --- | ---: | ---: | ---: | ---: | ---: |
| DISJ3_grouped | 14 | 1 | 8 | 8 | 8 |
| DISJ3_interleaved | 6 | 5 | 8 | 8 | 8 |
| IP3_interleaved | 10 | 5 | 3 | 7 | 13 |
| SELECTOR_ADAPTIVE | 13 | 3 | 4 | 4 | 8 |
| HORN_C6 | 14 | 5 | 5 | 5 | 11 |
| SINGLETON | 6 | 1 | 1 | 1 | 1 |

The selector graph tests s first, then genuinely chooses interleaved DISJ2 or grouped EQ2; this is **input-dependent order**. DISJ3 interleaved still has grouped X:Y rank 8 with V=6 and b=5: falsely charging it as b=1 is refuted by a legal cheap computation. IP3 has GF(2) rank 3 but odd-prime rank 7. Horn cycle is 2-SAT, singleton is a unique satisfying assignment, UNUSED_PAD skips an irrelevant variable, INDEPENDENT_PARITY_PRODUCT is separable, and equality is checked at sizes 2..4. The tests are finite COMPUTATIONAL evidence; the symbolic lemma supplies the restricted generality.

A separate CPython 3 standard-library implementation was locally executed on the same 25 named controls with 30,899 assertions, zero failures (source revision tmr4-adaptive-crossings053.v1, seed none; local SHA-256 ce397b204be281f82a9f001beea5e833fab0b89b6fc8aa29b5c6e66baa90e879). This secondary implementation is not in the published repository; its independent results are a supplementary check, not peer review.

## Same-realization costs and Track C firewall

| Resource | Exact service and charge | Conclusion |
| --- | --- | --- |
| B source graph | V internal records, exactly 2V branch arcs, sharing counted ONCE. Each record must encode variable ID and two target addresses, O(log n+log(V+2)) bits | No unfolding into a decision tree |
| One graph evaluation | At most V node tests on an acyclic diagram; on every reported input, paid test count is the actual trace length | Real tape input/index/graph access overhead additionally required |
| Two-party protocol | At most b node-ID transmissions of ceil(log2(V+2)) bits each, plus final 1-bit result; local computation exactly the branch tests | Communication cost is not an arbitrary TM time lower bound |
| Graph acquisition | Any order-selection, alternative strategies, malformed parser, shared subgraph discovery or compilation of B must be charged; no free circuit-to-FBDD compiler | **OPEN** for arbitrary circuits |
| Exact external rank audit | Enumerates up to 2^N input pairs, O(V) tests each, plus exact field elimination; working matrix may occupy Theta(2^N) bits | Audit is not a uniform fast SAT algorithm |
| Circuit to CNF | TMR-1/050 and TMR-5/047: n input variables and l LIVE gates give n+l CNF variables, <=3l+n+1 width<=3 clauses, O((n+l)log(n+l)) encoded bits | Count wires, copies, bit lengths; no o(n)-exponent guarantee for l=Omega(n sqrt(log n)) from the displayed bound |
| Hierarchy/DTISP | No same deterministic SAT machine meeting both strict FLMV time and space thresholds; Williams lower bound targets NEXP/other specified classes, not NP automatically | **OPEN** |

Even a bounded-switch FBDD rank lower bound only controls that representation. DISJ has a linear-size depth-two circuit, as do the Horn and affine controls under their suitable descriptions. A fixed formula's assignment tensor is not the SAT decision function on encoded formulas. No exact interpolation, #SAT exponent, NP-level hierarchy transfer, or native wire-compression theorem is obtained here.

## Mandatory four verification gates

| Gate | Status with reason |
| --- | --- |
| **DISJ sanity** | **PASS restricted; FAIL unrestricted rank-to-circuit proposal.** DISJ_k has grouped rank 2^k but V=2k interleaved BDD, b=2k-1, and linear-size Boolean circuit. |
| **Relativization** | **PASS restricted; OPEN unrestricted**. The rectangle protocol is purely combinatorial and can relativize as an intermediate lemma. It is **not** a P-vs-NP separator. An eventual unrestricted proof requires a precise nonrelativizing mechanism; algebrization and Natural Proofs remain unclosed audits. |
| **Simultaneous DTISP** | **NOT APPLICABLE WITH REASON** to graph-representation rank; **OPEN** for any machine hierarchy inference, as no one matched total deterministic machine attains both strict time and space bounds. Network work and aggregate space are not replaced by span/per-machine figures. |
| **Configuration counting** | **PASS as an upper-bound guard only**: a fixed deterministic total read-only-input machine satisfies T<=2^{O(s+log N)}, and T<=2^{O(s)} when s>=log N. Neither is a necessary-work lower bound. Randomized/quantum models separate. |

## Corpus reconciliation and publication qualification

Read FIRST current scientific directive, SHA 7b8804dc7587abc5134055b5b0d16a143055ca5a. Inspected repository AGENTS.md SHA 8f477279a014b4e2fd61544fe9e53f9a6d25d70f, CODEX.md, research skill, all five current TMR handoffs, issue #3, original TMR-4/052 source/report/raw, TMR-1/052 and TMR-2/052 original reports, historical rank/selector controls and literature. Root proof1.txt was read, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; oversized proof2.txt SHA 930c5eeddafce656717f28055a7a9a755f44737c and main.tex SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 returned empty bodies and were **NOT fully read**, prohibiting shared edits. Local repository checkout/preflight and full project tests were blocked by GitHub DNS failure in the container. **TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE.**

Sources: Wegener, *Branching Programs and Binary Decision Diagrams*, Ch. 6 (FBDDs/read-once), https://doi.org/10.1137/1.9780898719789.ch6 ; Bryant (1986), https://doi.org/10.1109/TC.1986.1676819 ; Li and McKenzie (2024), communication/rectangle measures for read-once BPs, https://doi.org/10.1016/j.ic.2024.105230 ; Baker-Gill-Solovay (1975), https://doi.org/10.1137/0204037 .

**ONE NEXT LEMMA:** Audit a genuinely restricted cost-sound *circuit-to-adaptive-BP compiler* with explicit upper bound on side switches, shared live-gate overhead, AND/OR/XOR wiring and acquisition; or falsify it by a compact circuit/affine/Horn/selector instance. Until then unrestricted same-system SAT-machine transfer remains OPEN.

END_OF_VERIFIED_REPORT::TMR-4::053
