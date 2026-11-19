# LSPV-2: Uniform T5 witness circuits by source-gauged Boolean bucket elimination

Date: 2026-11-18 (America/Los_Angeles). Owner: LSPV-2 SAT-CIRCUIT REDUCTION BUILDER, historical Route A. Status: PROVED/RESTRICTED compiler theorem; COMPUTATIONAL independent gate-level audit; OPEN arbitrary-family hardness, P versus NP.

## Candidate and falsifiers

Candidate: build a **uniform, no-witness-table**, source-aware SAT-and-complete-witness Boolean DAG for **every subgraph** of an actual oriented host H, not just H-e. Falsifiers were: (F1) an invalid complete T5 coloring or H wrongly accepted; (F2) a wrong output among all 2^11 subgraphs of H9 or a foreign arc accepted; (F3) divergence from a separately implemented exact AC/DFS solver or an unsound fivefold gauge pin; (F4) no real width/gate reduction from source-preserving anchor substitution. All finite tests passed, within declared scope.

## Proved theorem

Let H have n original vertices, m directed arcs, q=n(n-1) ordered adjacency bits and a designated root r. Given any elimination order of the unpinned primal graph H-r having induced width w, a deterministic compiler constructs a fan-in-two AND/OR/NOT circuit with O(q+(m+n+nw)5^(w+1)) gates (conservative), reading **every** source-adjacency input. For any input that is a subgraph of H, the circuit decides whether that subgraph has a T5 coloring and, when yes, emits all 3n bits of a legal coloring and an independent full-edge verification flag. On UNSAT it emits validity false and zero witness bits. For foreign arcs, it returns an out-of-declared-domain flag, **not** an UNSAT answer for arbitrary graphs.

Proof: attach to each original arc u->v the factor (not x_uv) OR (((color_v-color_u) mod 5) in {1,3}); AND the absent-foreign-arc guard. By simultaneous +c translation modulo five on the connected component containing root r, fix color_r=0 without losing satisfiability. **Substitute** this root value in its incident original factors, reducing primal width. For each eliminated vertex, AND bucket factors, existential-OR over its five colors, and retain each of the five preprojection product entries. Reversing the elimination order, select the first original color with true product under already selected remaining-neighbor colors. Induction over bucket projections proves exact existence and valid traceback. Gate-level legal-color and actual-edge checks certify the emitted witness. Each bucket has <=w remaining variables, and total consumed factor incidences is O(m+n); traceback costs O(nw5^(w+1)). Every host/parser/order/serialization/output/verification operation and live DAG storage remains charged. No model or original edge is replaced.

If an infinite critical host family and width-O(log n) elimination orders can both be obtained in polynomial time, **all** subgraphs of those hosts admit uniform polynomial-bit-time witness extraction. No conclusion follows for a family with unbounded width or expensive host/order acquisition, and no unconditional T5 or SAT lower bound follows.

## Completed gate-level evidence

| Source-aware metric | H9 original factor-pin | H9 substituted root | H33 original factor-pin | H33 substituted root |
| --- | ---: | ---: | ---: | ---: |
| Source vertices/arcs | 9/11 | 9/11 | 33/44 | 33/44 |
| Actual input adjacency bits | 72 | 72 | 1056 | 1056 |
| Induced elimination width | 2 | **1** | 5 | **4** |
| Largest factor table | 25 | **5** | 3125 | **625** |
| Witness AND/OR/NOT gates | 826 | **459** | 280585 | **61619** |
| Witness depth | 51 | **30** | 221 | **200** |
| Gates with full witness verifier | 1121 | **754** | 282017 | **63033** |
| Depth with verifier | 65 | **44** | 237 | **216** |
| NOT gates with verifier | 67 | 68 | 269 | 269 |

For H33 the real root substitution removes 78.0% of witness Boolean gates relative to the **same uniform compiler** using a unary pin. Root r=10, deterministic searched order [4,17,20,2,0,21,24,3,16,25,15,12,7,30,29,22,28,1,5,18,11,32,13,23,8,26,19,27,14,31,6,9], induced width 4. On H9 root r=0 and order [4,6,8,7,2,5,3,1], width 1. The earlier 1735-gate H33 circuit uses a **precomputed deletion witness ROM** and only recognizes exactly one-edge deletions; it is a different nonuniform task, so the comparison is not a faster circuit for that same promise.

Two completely serialized netlists passed a replayer importing **neither compiler nor any precomputed witness table**. H9: 2064 runs including all 2048 host-edge masks, 2060 independent CSP-solver comparisons; H33: 124 runs including all 44 critical deletions, 75 randomized proper subgraphs and 70 independent solver comparisons. Both unchanged original UNSAT hosts and four foreign-arc mutations were rejected. All accepted masks emitted complete T5 witnesses satisfying every active directed edge. A corrupted certified-output root was detected independently on each source. H33 output witness DAG SHA256 `0c06aa3b9d2630d40bbdf317b4c631c863c5d0a8d91cab7d271c456b4d5aa64d`; H9 SHA256 `7061d418c27844b605ef71c03fb11b9c093d31206f813d5f987b6745fe834d5c`. Original H33 source SHA256 `0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac`, H9 `deb4de3a8180d066e3788b3b5a127560c3c6d7289dc9389583c20a10cc5e98c3`.

Separate length<=3 path enumeration rechecked all 512 relation subfamilies, nine nonuniversal endpoint relations and irredundance maximum four. Weighted local greedy peeling removes all branch vertices after H9 thread deletions but leaves a 17-19-vertex core for H33 thread deletions, falsifying its unrestricted applicability.

## Scope and references

This is an explicit restricted Boolean realization of classical finite-domain bucket elimination and witness traceback, **not** a novel general treewidth theorem. Compare Dechter (1999), https://doi.org/10.1016/S0004-3702(99)00059-4; Dalmau, Kolaitis and Vardi (2002), https://doi.org/10.1007/3-540-46135-3_21; and fine-grained graph homomorphism/treewidth, https://doi.org/10.1137/20M1320146. Project TMR-2/081 reports a distinct source-authenticated weighted-degree-two **counting** algorithm and a width-four rooted 33 schedule; this run compiles a complete **SAT witness circuit**, not just a count.

Complete tested code, independent replayer and oracle, 4 full Boolean netlists, original sources, raw JSON and SHA256 manifest are in the associated 2026-11-18 LSPV-2 conversation reproducibility archive. Source parsing, actual input-bit reads, all gate evaluations, host acquisition, order-search, construction, output and verifier are included in the resource model. Exact physical RAM/bit-time and external peer-audited mathematical soundness remain separate obligations.

**Next blocker:** construct a uniformly obtainable growing-girth intrinsic edge-critical UNSAT family with large minimal width **and** falsify *all* GF(5), flow, contraction, algebraic, compression, adaptive and unrestricted-circuit shortcuts before any superpolynomial witness-cost assertion. Fixed-girth NP-hardness and larger branching cores do not supply that assertion. Independent peer audit OPEN. No changes to five automations, ownership, proof trackers or main.tex. P versus NP OPEN.
