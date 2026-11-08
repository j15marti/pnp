# LSPV-5/440: unicyclic residual analysis raises the exact proper-Resolution floor to 17

**2026-11-08 10:45 PST | Route B independent red team | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Affected tracker IDs:** new `[P2-L5-440]`; strengthens `[P2-L5-439]` and `[P2-L1-510]`, and refines `[P2-L1-507]`, `[P2-L1-509]`, `[P2-F13]`. `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]` remain OPEN. `[P1-01]`, `[P1-03]`, `[P1-04]` were reviewed with no material change.

## IDEA and falsifiers fixed before search

Initial hypothesis: combining `[P2-L1-510]` with `[P2-L5-439]` makes any hypothetical 16-inference proof unicyclic, and peeling a sink goal makes its residual a connected tree with exactly 15 inference vertices and all 16 source vertices. Exact recursive tree decomposition should therefore decide the remaining 16-node case.

Four falsifiers were fixed before search:

1. an explicit legal 16-node exact proper-Resolution DAG;
2. any of the 20 exact sink-parent branches admitting a 15-inference residual tree;
3. failure of the graph identity or of residual connectedness, so that the residual need not be a tree;
4. a duplicate-clause, source-alias, repeated-parent, target-placement or context-scope case omitted by the recurrence.

The finite cancellation gadget is only a validation control. Established Tseitin and pigeonhole families remain the primary lower-bound benchmarks; no finite result below is promoted to historical mixed-calculus or all-algorithm hardness.

## SEARCH: complete project continuity

- Starting `main` head `f5e034614082ab097fd02acbc5f433736af39fa1`.
- Complete `proof1.txt`: blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 characters.
- Complete `proof2.txt`: blob `2850e9a15e3eaa15925189b5d8faf27e37c2175c`, 470,474 characters.
- Current issue #3: all 1,360 comments read across 14 pages. Latest relevant nodes included `[P2-L5-439]`, `[P2-L1-510]`, `[P2-L3-506]`, and the `/439` reconciliation comment.
- Governing five-role handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, blob `033b54b87b7cbe94912af5cf67daa52859143a07`; `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`; `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`; repository skill blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`.
- Peer files actually read: `research/agents/lspv-1/2026-11-08_1000_LSPV1_MULTIROOT_CYCLE_BUDGET510.md` blob `b5041eb141d814f1d3d82aa1d3ed90e5734edb5a`; `research/agents/lspv-2/2026-11-08_0915_LSPV2_AUTHENTICATED_INDEXED_RECOGNIZER497.md` blob `51272c1031372adabb3e254ff4a3638eefb672f7`; `research/agents/lspv-3/2026-11-08_0924_LSPV3_SINGLE_GADGET_TYPED_EXP_GAP506.md` blob `0e795deb54e54242f0fa4748678127c50b0b9eda`; `research/agents/lspv-4/2026-11-08_0936_LSPV4_HAMMING_AUTHENTICATION498.md` blob `46f726cafd6ddbee8cb370a1f394c76dedc68d8b`; own reconciled `research/main/2026-11-08_1010_MAIN_TERMINAL_PEEL16_REFEREE439.md` blob `bea8842ae6b4905a069106193f3142f532ec40b4`.
- Current actual Grok file `GROKPROOF/2026-11-08_1130_PROGRESS.md`, blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70`; current Claude world-ledger `research/agents/claude/world-ledger/README.md`, blob `de75a371ce3143a4495e6892df7fb04794a6b708`. Neither supplies the missing historical mixed-rule transfer or B3.

### Primary literature and queries

Actual queries included `shortest Resolution proof branch and bound exact`, `unicyclic Resolution proof DAG lower bound`, `multi conclusion Resolution proof tree decomposition`, `circular Resolution proof DAG`, and `Res(XOR) lower bounds tree-like`.

- Sidorov, van der Linden, Correia, de Weerdt and Demirović, *How to Discover Short, Shorter, and the Shortest Proofs of Unsatisfiability* (arXiv:2411.07955; JAIR 86, 2026), gives exact shortest-proof search with layer-list symmetry breaking and proved pruning. It does not state this simultaneous-target unicyclic residual theorem.
- Peitl and Szeider, *Finding the Shortest Resolution Proofs in Theory and Practice*, and `peitl/short-proof/short.py`, remain exact-minimization controls; their single-refutation encoding does not automatically authenticate this multi-target recurrence.
- Atserias and Lauria, *Circular (Yet Sound) Proofs*, explicitly changes the proof object by permitting circular flow. It therefore warns against treating a cyclic search-state graph as a legal acyclic dependency DAG.
- The inspected Res(XOR) lower-bound source (DOI `10.1016/j.apal.2019.102722`) is model-qualified and tree-like/substitution scoped. It does not transfer to all historical `R_mix341` rules.
- Haken's ordinary Resolution lower bound for PHP and Tseitin/Urquhart-style ordinary Resolution bounds remain restricted-system controls; Cook extended Resolution and GF(2) elimination remain mandatory shortcut controls.

A separate Google-branded client was unavailable; public web search and primary-source pages were used.

### Change-aware repository ledger

| Repository/path | Current head/blob | Result |
|---|---|---|
| `konard/p-vs-np/scripts/proof_status.json` | head `ecedd2b45f1c524d85c00b2da27a9c140025550c`; blob `93b77ed3d8fe456f81c690035f45f07910a247f2` | No delta closing historical grammar, all-rule transfer or B3. |
| `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` | head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`; blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` | Restricted-method inventory only. |
| `blkph0x/p-vs-np-proof-research/INDEPENDENT_AUDIT.md` | blob `b30515cced93d8911a6415555ee9ec1444502d93` | Uniform constructive transfer remains open. |
| `peitl/short-proof/short.py` | head `2c524cfceecf68b56f51d23f6b63255b502856d3`; blob `6508dae79e341d7015949d5919de29a132fbf267` | Exact shortest-Resolution control. |
| `meelgroup/frat-xor/format.md` | head `18cd6bc17af10a9891c10a846ce966166f9fe0dc`; blob `986a21aa92b62f844ef1fce852193142c41b2b1f` | Separate provisional XOR grammar, not historical `R_mix341`. |
| `tanyongkiam/cake_lpr/README.md` | head `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`; blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c` | Final release dated 2026-11-01; verified checker scope is not a minimum-proof theorem or same-calculus B3. |
| `marijnheule/drat-trim/README.md` | head `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; blob `eb6ffcc4a85ff1c74a5995b6caae4372381dcd47` | DRAT checking control, not this native mixed grammar. |
| `MassimoLauria/cnfgen/README.org` | head `24e633bdbed0d0998493bee99c42faf480c7dc96`; blob `9fba4e26f2a4cd10444a7226a7a3a7caa1762721` | Established formula generator; no all-rule transfer. |
| `openai/math/README.md` | head `4eaee87548250b2682affda7d05d947c05554bae`; blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae` | No relevant theorem. |
| `anthropics/formal-math/README.md` | head `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`; blob `1df53bfc14a022088d1b5757698f692bf79390b4` | No relevant theorem; repository status is not target proof. |

## ITERATE: the unicyclic residual lemma

Let the pruned union-of-ancestors graph use all $m=16$ authenticated source vertices and $q$ strict binary inference vertices. `[P2-L1-510]` proves the exact graph identity

$$
q=m-1+mu=15+mu,
$$

where $\mu$ is the undirected cyclomatic rank. Thus a hypothetical $q=16$ proof has $\mu=1$.

By `[P2-L5-439]`, peel a sink goal $C$ and its two incident parent edges. The remaining graph is connected. Removing that vertex from a connected unicyclic graph and retaining connectedness leaves 31 vertices and 30 edges, hence a tree. It contains all 16 source vertices and exactly 15 inference vertices.

### Complete recursive decision recurrence

For a source mask $M$ and a finite target-label set $T$, define $\operatorname{Tree}(M,T)$ to mean that one connected strict-binary exact proper-Resolution tree with precisely the selected source vertices derives every target in $T$.

1. If $|M|=1$, the tree has no inference node, so every target must equal that source clause.
2. If $|M|>1$, a pruned finite tree has a derived sink $C\in T$.
3. Enumerate every exact oriented Resolution parent/pivot option $A,B\to C$ from the complete 1,270-clause closure.
4. Deleting $C$ splits the underlying tree into exactly two components. Partition the remaining target obligations and the source mask between those components, with $A$ and $B$ forced into their respective components.
5. Recurse on both components; both are AND obligations. Alternative sink and parent choices are OR choices.

Every component with $r$ sources automatically contains $r-1$ inference vertices. The source-deletion indispensable masks used in `/439` are only necessary-condition pruning; they cannot remove a legal tree.

### Duplicate-clause normalization

A minimum acyclic proof has a unique-clause normal form. If two inference nodes carry the same clause, choose the earlier one in a topological order, redirect every outgoing reference from the later duplicate to the earlier node, and delete the later node. The redirection cannot create a cycle and preserves every downstream exact inference because clause syntax is identical. A hypothetical 16-node proof is already at the `/439` lower floor, so any such deletion would contradict minimality. The recurrence may still reuse the same label inside separate recursive components, which enlarges rather than shrinks the search space.

This closes the repeated-label and target-placement falsifier without silently adding weakening, discharge or semantic equality.

## Exact exhaustive result

The Python implementation and separately authored Node/V8 replay independently construct the complete exact proper-Resolution closure and apply the recurrence to every peeled branch:

- 1,270 reachable proper clauses;
- exact goal parent-option counts `6,8,6`;
- all 20 possible peeled-goal/parent branches tested;
- every residual-tree answer `false`;
- positive controls: the three previously certified individual minimum trees plus a two-source one-step tree, all recovered.

Therefore no 16-inference proof exists. With the 19-node accepted exact proper-Resolution certificate `[P2-L1-507]`,

$$
\boxed{17\le q_{\mathrm{proper\text{-}Res,three\ goals}}\le19.}
$$

Equivalently, every legal proof has $\mu\ge2$ in the `[P2-L1-510]` identity. This decides neither 17 nor 18.

## Independent verification and hostile controls

| Check | Python | Independent Node/V8 |
|---|---:|---:|
| Closure clauses | 1,270 | 1,270 |
| Goal parent branches | 20 | 20 |
| Surviving 16-node branches | 0 | 0 |
| Positive tree controls | 4/4 | 4/4 |
| Memo states | 231 | 296 |
| Parent options inspected in recurrence | 12,367 | 14,169 |
| Partition prunes | 77,643 | 78,588 |
| Internal elapsed time | 12.913 s | 4.686 s |
| Python maximum RSS | 28,032 KiB | not externally measured |

Different search orders produce different memo frontiers while agreeing on the complete branch verdicts. SHA-256 digests: Python `807fb71386351d24004642e2f7683f186193bb53767fbd393f510f7d1d38942a`; Node `e6ab10ca76d3cbe932b66ec42799a07e990f23d2b747af2a00713f8a9216ff66`; Python raw `38446a2b7ad2bf7e12385a203bbd32e8b5df1afee40d0d886024cc6dfdf2340e`; Node raw `03a4f587c0b065775e997e9a39a3bd5198ed0f6540e08895de8330c28e801533`. The historical `R_mix341` checker was not run, and no reimplementation is called an execution of it.

## Exact encoding and established-family/shortcut ledger

The finite control has variables $x_1,\ldots,x_7$ and four full truth-table factors. The 16 source clauses are exactly the `SOURCES_RAW` array in the published program: four clauses on each scopes $(1,2,4)$, $(2,3,5)$, $(1,5,6)$ and $(4,6,7)$. The first and third factors encode AND; the second and fourth encode XOR. Required clauses are $(-x_1\lor-x_3\lor x_7)$, $(x_1\lor-x_7)$ and $(x_3\lor-x_7)$. It is SAT, has eight source models, and has no hardness theorem.

| Family/control | Exact 3-CNF encoding and size | Established theorem/model | Known legal shortcuts | Remaining transfer |
|---|---|---|---|---|
| Odd-charge cubic-expander Tseitin | One edge variable per edge; for each degree-3 vertex, the four signed width-3 clauses falsifying assignments of the wrong parity. For $h$ vertices: $3h/2$ variables, $4h$ clauses, $\Theta(h\log h)$ binary bits. | Exponential ordinary shared-DAG Resolution on suitable expanders; proof-system qualified. | GF(2) elimination; source-local parity/factor derivations where declared. | Every-rule historical `R_mix341` transfer OPEN. |
| Haken PHP | Standard pigeon variables $p_{i,j}$, pigeon clauses $\bigvee_jp_{i,j}$ and collision clauses $\neg p_{i,j}\lor\neg p_{i',j}$. Not native 3-CNF without an explicit reduction. | Exponential ordinary shared-DAG Resolution. | Cook extended Resolution has polynomial shortcuts. | Exact 3-CNF lower-bound-preserving direction and mixed transfer OPEN; equisatisfiability is insufficient. |
| `/507`--`/510` cancellation control | Exact 16 proper 3-clauses above, 7 variables, three simultaneous target clauses. | No hardness theorem; finite exact proper-Resolution range now `17..19`. | Legal 19-node shared-DAG proof. | Exact optimum and historical native acceptance OPEN. |

Certified UNSAT, proof-size hardness and empirical solver difficulty remain distinct. The finite control is SAT. Haken and Tseitin lower bounds are not claims against all algorithms.

## Branching/shared-DAG and resource accounting

- The three goals and the two recursive child components are AND obligations. Sink/parent/source-partition choices are OR alternatives. Every possible legal choice was included before excluding 16.
- Distinct inference nodes are charged once; shared subproofs are not double-counted. The legal dependency graph is acyclic even if a search state repeats.
- Contexts never leak: each recursive component receives a disjoint authenticated source mask, and parent clauses are obligations in that component.
- No case-split, discharge, weakening, excluded-middle, semantic oracle or new historical opcode was inserted.
- Explicit evidence totals 24,471 bytes across two programs and two raw JSON results. Charged work also includes complete tracker and issue reads, literature/repository reads, closure construction, 128 assignments per source-deletion test, memo tables, parsing, output, publication and readback. Failed external `/usr/bin/time` measurement is recorded rather than hidden; internal timers and Python RSS are reported separately.
- Logical work, evidence bits, construction/search time, critical-path depth, and realizable time/peak space are not conflated. No proof-node count is interpreted as an FLMV same-machine bound.

## Revised claim and precise remaining gap

Evidence changed the initial hypothesis into a restricted theorem: exact tree decomposition eliminates all 20 unicyclic residual branches, raising the fixed finite proper-Resolution range from `16..19` to `17..19` and forcing $\mu\ge2$.

The next finite question is whether 17 or 18 nodes are attainable. The principal Route-B gaps are unchanged: authenticate the exact historical RES/LOCAL/DEF/GF(2)/branching accepted-byte grammar; transfer a published asymptotic lower bound across **every** legal mixed rule and shortcut; and prove a noncircular same-calculus B3. `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]` remain OPEN. **P versus NP OPEN.**
