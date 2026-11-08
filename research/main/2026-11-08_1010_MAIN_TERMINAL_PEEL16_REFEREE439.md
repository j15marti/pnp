# LSPV-5/439: terminal peeling raises the exact proper-Resolution floor to 16

**2026-11-08 10:10 PST | Route B independent red team | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Affected tracker IDs:** new `[P2-L5-439]`; strengthens `[P2-L5-438]` and `[P2-L1-509]`, and refines `[P2-L1-507]`, `[P2-L1-508]`, `[P2-F13]`. `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]` remain OPEN. `[P1-01]`, `[P1-03]`, `[P1-04]` were reviewed with no material change.

## IDEA and falsifiers fixed before search

Initial hypothesis: the abstract 15-merge connected-overlap DAG from `[P2-L1-509]` cannot be realized by the exact proper-clause oriented Resolution grammar used by `[P2-L1-507]`. Four falsifiers were registered before searching:

1. an independently replayable 15-node ordinary-Resolution witness;
2. a counterexample showing that a proposed canonical ordering deletes a valid proof;
3. any optimizer certificate failing exact pivot, source-authentication or acyclicity replay;
4. timeout or incomplete enumeration, which would be recorded as no result rather than a lower bound.

The first implementation attempted a recursively canonical backward frontier. It was **rejected before publication**: expanding an arbitrary frontier clause can double-count it if that clause is later used by another required goal. The repaired proof uses only a target known to be a sink of the minimum DAG and exhausts all possible sink choices.

## SEARCH: complete project continuity

- Starting `main` head `88e04f163738c843070a36963b371d9193fe1724`.
- Complete `proof1.txt`: blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 characters.
- Complete `proof2.txt`: blob `371ba561c782179b82260f58711bbdd0844156bc`, 465,781 characters.
- Current issue #3: all 1,357 comments read across 14 pages; latest relevant nodes included `[P2-L1-509]`, `[P2-L3-506]`, `[P2-L5-438]`, and Route-A source-authentication control `[P2-L4-498]`.
- Governing five-role handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, blob `033b54b87b7cbe94912af5cf67daa52859143a07`; `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`; `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`; repository skill blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`.
- Peer files actually read: `research/agents/lspv-1/2026-11-08_0900_LSPV1_TERMINAL_OVERLAP509.md` blob `53a6a24625d2a2163e7493136399e2e0319558ee`; `research/agents/lspv-3/2026-11-08_0924_LSPV3_SINGLE_GADGET_TYPED_EXP_GAP506.md` blob `0e795deb54e54242f0fa4748678127c50b0b9eda`; `research/agents/lspv-4/2026-11-08_0936_LSPV4_HAMMING_AUTHENTICATION498.md` blob `46f726cafd6ddbee8cb370a1f394c76dedc68d8b`; prior red-team `/438` blob `ffd848d223db4a63ff100c63fcc115e399f84c4c`.
- Current actual Grok file `GROKPROOF/2026-11-08_1130_PROGRESS.md`, blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70`; current Claude world-ledger README `research/agents/claude/world-ledger/README.md`, blob `de75a371ce3143a4495e6892df7fb04794a6b708`. Neither supplies historical mixed-rule transfer or B3.

### Primary literature and queries

Actual queries included `shortest resolution proof branch and bound layer list exact`, `shortest Resolution proof SAT encoding symmetry breaking`, `Resolution DAG sharing lower bounds source overlap`, and `proof complexity exact resolution minimization`.

- Sidorov, van der Linden, Correia, de Weerdt and Demirović, *How to Discover Short, Shorter, and the Shortest Proofs of Unsatisfiability* (arXiv:2411.07955; JAIR 86, 2026), Theorem 2 and Sections 4.1--4.5: layer lists break proof-line permutation symmetries; frontier and dominance pruning are proved for their refutation problem. This motivated canonical search, but the paper does not automatically cover a SAT source with three simultaneous derived target clauses.
- Peitl and Szeider's shortest-Resolution SAT encoding and `peitl/short-proof/short.py` were inspected as an exact-optimization control. Its proof-line symmetry treatment does not by itself authenticate this multi-target model.
- *Intersection Theorems: A Potential Approach to Proof Complexity Lower Bounds* (ITCS 2026) explicitly presents a Resolution convention containing Cut, Weakening and Excluded Middle. That is a different grammar from the present exact proper-resolvent model; those rules were not silently imported.
- Bhattacharya, Chattopadhyay and Dvořák, CCC 2024, separate regular from general Resolution over parities. This is a direct warning that restricted Res(XOR) bounds cannot be promoted to the full mixed calculus.

A separate Google-branded client was unavailable; public web search and primary-source pages were used.

### Change-aware repository ledger

| Repository/path | Current head/blob | Result |
|---|---|---|
| `konard/p-vs-np/scripts/proof_status.json` | head `ecedd2b45f1c524d85c00b2da27a9c140025550c`; blob `93b77ed3d8fe456f81c690035f45f07910a247f2` | No delta closing historical grammar, mixed transfer or B3. |
| `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` | head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`; blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` | Restricted-method inventory only. |
| `blkph0x/p-vs-np-proof-research/INDEPENDENT_AUDIT.md` | blob `b30515cced93d8911a6415555ee9ec1444502d93` | Uniform constructive transfer remains open. |
| `peitl/short-proof/short.py` | head `2c524cfceecf68b56f51d23f6b63255b502856d3`; blob `6508dae79e341d7015949d5919de29a132fbf267` | Exact single-refutation optimizer control. |
| `pysathq/pysat/README.rst` | head `bf246f36581e5d5ed1aa6eacf11e5d6fd4b664bc`; blob `fefde10b1426a92a21425029892f3f49466bf03c` | Solver API; timeout is not evidence. |
| `arminbiere/cadical/README.md` | head `c60730422e758ef1cebe7aeddf2dda31c996bf04`; blob `6ebe4db86d628bac87e290389a6a18aea102a5a6` | SAT backend, not a proof-minimum theorem. |
| `MassimoLauria/cnfgen/README.org` | head `24e633bdbed0d0998493bee99c42faf480c7dc96`; blob `9fba4e26f2a4cd10444a7226a7a3a7caa1762721` | Established formula generator; no mixed transfer. |
| `meelgroup/frat-xor/format.md` | head `18cd6bc17af10a9891c10a846ce966166f9fe0dc`; blob `986a21aa92b62f844ef1fce852193142c41b2b1f` | Separate provisional XOR proof grammar. |
| `openai/math/README.md` | head `4eaee87548250b2682affda7d05d947c05554bae`; blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae` | No relevant transfer theorem. |
| `anthropics/formal-math/README.md` | head `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`; blob `1df53bfc14a022088d1b5757698f692bf79390b4` | No relevant theorem; formalization badges are not target proofs. |

## ITERATE: terminal-peel lemma

Let $F=\{S_0,\ldots,S_{15}\}$ be the exact 16 source clauses and let $T$ be a finite set of required derived clauses. For a clause $C$, define its individually indispensable-source set

$$
E(C)=\{i:\text{ some assignment satisfies }F\setminus\{S_i\}\text{ and falsifies }C\}.
$$

Any sound source-authenticated derivation of $C$ must contain every $S_i$ with $i\in E(C)$ in its ancestry. On targets $T$, join $C,D$ when $E(C)\cap E(D)\ne\varnothing$. If $m(T)$ is the cardinality of the union of the $E(C)$ and $c(T)$ is the number of connected components among their nonempty overlap sets, the connected-essentiality argument `[P2-L1-509]` gives, for binary inference,

$$
q(T)\ge m(T)-c(T).
$$

Now prune any minimum acyclic proof DAG for $T$. Every sink is a required target; otherwise that sink can be deleted. Choose a sink $C\in T$. In exact proper Resolution it has parents $A,B$ and one pivot. Removing the paid inference for $C$ leaves a DAG deriving

$$
T'=(T\setminus\{C\})\cup(\{A,B\}\setminus F).
$$

Because $C$ is a sink, it is not an ancestor of any remaining target, so the removed node is disjoint from the remaining derivation count. Therefore

$$
q(T)\ge 1+m(T')-c(T').
$$

This is an AND obligation over every possible sink goal and every exact parent/pivot choice; it is not a heuristic choice of one favorable derivation.

## Exact exhaustive result

The independent programs compute the complete exact proper-Resolution closure of the 16 sources:

- 1,270 distinct reachable proper clauses;
- fixed-point round additions `43, 444, 766, 1`;
- 253,208 exact unordered parent/pivot options over that closure;
- exact goal parent-option counts `6, 8, 6`.

All three possible sink goals and all 20 exact parent branches were tested. In **every** branch, $T'$ still has all 16 sources in the union of its indispensable sets and one connected overlap component. Hence

$$
m(T')-c(T')=16-1=15
$$

and therefore

$$
\boxed{q\ge16.}
$$

Together with the accepted 19-node upper certificate `[P2-L1-507]`, the exact finite range becomes

$$
\boxed{16\le q_{\mathrm{proper\text{-}Res,three\ goals}}\le19.}
$$

This falsifies the possibility that the abstract 15-merge provenance control from `[P2-L1-509]` is exact Resolution syntax. It does not decide 16, 17 or 18. A recursive terminal-peel challenge through depths 0,1,2,3 gave lower bounds `15,16,16,16` over `1,21,1,033,99,921` memoized target states, so deeper bounded lookahead did not justify 17.

## Independent verification and hostile controls

- Python: status `PROVED_RESTRICTED_COMPUTATIONAL`; full 20-branch table; 13.446 seconds; 48,428 KiB maximum RSS.
- Separately authored Node/V8: 1,270 clauses, 253,208 options, counts `6,8,6`, all 20 branches at floor 16; 30 assertions and three hostile controls PASS; measured wrapper 4.919 seconds and 98,824 KiB child maximum RSS.
- Wrong-pivot, source/goal alias and essential-source table corruptions were rejected.
- The historical `R_mix341` checker was not run. No independent reimplementation is called an execution of that checker.

## Established-family and shortcut ledger

| Family/control | Exact encoding and size | Established theorem/model | Known shortcuts | Remaining transfer |
|---|---|---|---|---|
| Odd-charge cubic-expander Tseitin | $h$ degree-3 vertices, $3h/2$ edge variables, four signed proper width-3 clauses per vertex, $4h$ clauses and $\Theta(h\log h)$ bits | Exponential ordinary shared-DAG Resolution on suitable expanders | GF(2) elimination and declared source-local factor proofs | Every-rule historical `R_mix341` transfer OPEN |
| Haken PHP | Standard PHP CNF; not native 3-CNF without a preservation theorem | Exponential ordinary Resolution | Cook extended-Resolution polynomial shortcut | Exact 3-CNF preservation and mixed transfer OPEN |
| `/507`--`/509` cancellation control | 16 signed proper 3-clauses, 7 variables, SAT with eight source models | No hardness theorem; finite exact proper-Resolution range now `16..19` | Legal 19-node shared proof | Exact optimum and native historical acceptance OPEN |

Certified UNSAT, proof-size hardness and solver difficulty remain separate. The cancellation gadget is SAT and is only an interface/derivation control. Haken and Tseitin restrictions are not all-algorithm lower bounds.

## AND/OR, sharing and resource accounting

- The three goals are simultaneous AND obligations. Alternative parent pairs are OR choices, but every possible sink and parent pair was covered by the lower-bound minimum.
- Shared clauses and inference nodes are counted once. The proof permits arbitrary branching and reconvergence subject to exact source contexts and acyclicity.
- No case split, discharge, weakening, excluded-middle, semantic oracle or new opcode was inserted into historical `R_mix341`.
- Charged implementation work includes both complete trackers, 1,357 issue comments, repository and literature reads, 128 assignments for each source-deletion test, closure construction, all 253,208 exact parent options, 20 terminal branches, 99,921 deeper challenge states, two implementations, parsing, output, publication and readback.
- Logical nodes, evidence bits, search/construction time, weighted span and realizable time/space schedules are not conflated. No proof-node count is interpreted as an FLMV machine bound.

## Post-publication reconciliation with `[P2-L1-510]`

While the publication receipt was being prepared, LSPV-1 independently published `[P2-L1-510]`. Its exact binary-DAG identity is compatible with this result: for the connected 16-source setting and strict binary Resolution it gives

$$
q=15+\mu,
$$

where $\mu$ is the undirected cyclomatic rank of the pruned union-of-ancestors graph. Combining that identity with the terminal-peel lower bound $q\ge16$ proves the additional restricted structural consequence $\mu\ge1$ for every legal three-goal exact proper-Resolution DAG. Thus the abstract 15-merge tree-like topology ($\mu=0$) is excluded syntactically, while 16--18 nodes remain open. The `15..19` sentence in `[P2-L1-510]` records its pre-`[P2-L5-439]` baseline and is superseded for the current range by this node; no peer-owned report or tracker node was rewritten.

## Status and precise remaining gap

**Actual advance:** terminal peeling closes the 15-node exact proper-Resolution case and raises the joint range from `15..19` to `16..19` for this fixed finite gadget.

**Remaining gap:** decide the 16--18-node exact proper-Resolution cases; then authenticate the exact historical RES/LOCAL/DEF/split/discharge accepted-byte grammar and prove or refute transfer across every legal mixed rule. The asymptotic all-rule minimum `[P2-B1]` and noncircular same-calculus B3 `[P2-B2]` remain OPEN. **P versus NP OPEN.**
