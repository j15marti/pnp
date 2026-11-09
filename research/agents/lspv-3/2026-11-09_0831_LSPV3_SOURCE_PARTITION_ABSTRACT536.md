# LSPV-3/536: cost-sound source-partition inductive abstraction

**2026-11-09 08:31 PST | LSPV-3 / Route B | PROVED/RESTRICTED reuse of the existing /341 lower bound in an inductive abstraction, plus COMPUTATIONAL checks. P versus NP OPEN.**

**Node IDs:** [P2-D1], [P2-C1], [P2-C3], [P2-B1], [P2-B2], [P2-L1-537], [P2-L5-462], proposed [P2-L3-536]. No changed Route A or proof1 obligations.

## IDEA -> SEARCH -> ITERATE

Initial candidate: transform the already-proved /341 global source-ancestry counting proof into a locally verifiable inductive cost-sound abstract invariant on the *whole partial shared DAG*. An abstract state records the connected-component partition of indispensable original source labels and the number of distinct paid nodes. Predict negative reachability for any budget below m-1, provided all legal charged rules have no more than two **exhaustive source-bearing dependencies** and no zero-cost cross-component edge.

**Predeclared falsifiers:** F1, a zero-cost reuse or case discharge adds a previously missing source-dependency edge; F2, a paid LOCAL-CONVERT or DEF defining facet secretly depends on more than two source-bearing proof vertices; F3, sharing/reconvergence can merge more than two source components in one charged two-parent transition; F4, a cheaper legitimate mixed shortcut exists on the cubic odd-Tseitin controls. Investigation excludes F3 by the structural lemma below and F4 for the previously DECLARED /341 calculus; full historical accepted-byte proof for F1 and F2 is missing. A four-source unit-cost extraction in a DIFFERENT calculus explicitly invalidates the numerical 4h-1 bound. No hidden rule is silently rejected by the full-calculus claim.

**Original project reviewed:** BOTH full main trackers (proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2.txt startup blob dbd441f528abaa10e8be94e1ffb301eab0b9d78d); governing 2026-11-09_ABSTRACT_INTERPRETATION_NEGATIVE_FIVE_ROLE_REFOCUS.md blob 8a6fd9f5dc73a2ed943e8630cad63bdd768b0b1b; November 2 five-role handoff; issue #3 and latest LSPV-1/537 and LSPV-5/462 comments; AGENTS.md, CODEX.md, and the pnp-research SKILL.md; original semantic rules in research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb; LSPV-3/406, /535; LSPV-5/369 and /432. Actual Grok file GROKPROOF/2026-11-09_1230_PROGRESS.md blob 0ee19c6b2fdf92b64427ab737fe563346779c828 and Claude file research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex blob 79e4d4e7e0e3edff3aba8610852c45534bdde128 were read. Root main.tex returns **zero characters** despite blob fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba; do not overwrite unseen bytes.

**Novelty/duplication audit:** The numerical bound is LSPV-2/341 and is NOT newly discovered. LSPV-3/406 and LSPV-5/369 already address fresh-wire alpha-renaming; LSPV-5/462 already addresses paid-history erasure; LSPV-1/537 already addresses same-statistics cheap-source collisions. This run supplies the separate locally checkable *partition abstract transformer and inductive budget certificate*, and a concrete bad-arity CEGAR control, without claiming a new superlinear invariant.

**External searches/checks:** Fetched konard/p-vs-np README.md (blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95), scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2); blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5); meelgroup/frat-xor format.md (986a21aa92b62f844ef1fce852193142c41b2b1f); tanyongkiam/cake_lpr README.md (e94f45e9aa000cd9ada12f4c771ac9daf28fe53c); MassimoLauria/cnfgen/cnfgen/families/tseitin.py (4bb5fd198fc4a698a5a207f67b36a9591b2a3bab); berkeley-abc/abc README.md (88a9d1a316dd9751acade746de315fd1e6e6c362); openai/math README.md (cc5b0a03bca6c742f045d683b6647a6f44ef2cae). External format/claimed formalizations are NOT native R_mix341 grammar authorities. Targeted literature/web queries: Pang 2610.00837 Theorem 7.2, Abstract Satisfaction POPL 2014, Giacobazzi-Ranzato-Scozzari JACM 2000, Urquhart hard expander Tseitin. The exact intended results are in the governing handoff. A separate Google-branded search interface was unavailable.

## Theorem 536.1, scoped cost-sound abstract proof construction

Fix a sound, source-explicit calculus R and an original UNSAT CNF F with m individually indispensable source clauses E. Every new paid inference has **at most two complete source-bearing dependency parents** and unit-or-greater weight; there are no free edges joining two previously disconnected proof components, no free source-dependent semantic oracle, and all auxiliary definitions are conservative. Any source-independent definitions may be arbitrarily numerous; identifiers may be arbitrarily large. For a current finite partial DAG, include all source vertices and paid nodes and their dependency edges. Let kappa be the number of connected components containing at least one essential original source, disregarding source-free components; let q be the number of distinct paid nodes.

**Abstract domain:** partitions of E, concretized as all partial shared DAGs inducing that partition. An abstract paid step may join any two blocks, or none, at cost 1 (for a concrete rule of charge at least 1); a free reference leaves the partition unchanged. This is an overapproximation of *every* permitted concrete binary transition, independent of actual rule-selection policy and future proof sharing.

The following is an inductive invariant of every concrete execution:

$$
\boxed{\kappa+q\ge m.}
$$

**Proof:** At start all m essential source leaves are separate and q=0. A new non-source node with at most two exhaustive antecedents connects at most two existing components and can reduce kappa by at most one, while increasing q by one. Free references do not insert new dependencies. This argument is independent of inference semantics, context policy, temporary growth, and reconvergence, provided the assumptions hold. Since each Ci is indispensable, a sound completed refutation cannot omit Ci from its contradiction ancestry: a satisfying model of F with Ci deleted extends conservatively across the used definitions and refutes the omitted-source alleged contradiction. All essential source ancestors of a single contradiction lie in one connected component, so kappa=1. Therefore W_R(F)>=m-1. Under budget B<m-1, the invariant implies kappa>=m-B>=2, excluding the abstract goal. Every concrete proof maps to a no-more-expensive abstract path, and the abstract goal includes every concrete goal. This is a negative certificate for the **entire declared binary-premise transition system**, not merely a fixed search trace or an abstract SAT solver.

**Limits:** This derives the old /341 m-1 lower bound by abstract interpretation. It does NOT improve its order of growth, establish historical accepted-byte rule grammar, or prove B3. For unidentified historical DEF facets, LOCAL-CONVERT, and case discharge, a sound may model must overapproximate unknown source-bearing arity, potentially joining more than two blocks at once. The displayed invariant cannot be promoted until [P2-D1] is authenticated. The current checker positively supports only SOURCE/AND3/XOR and rejects any unauthenticated rule: the checker is for this **restricted declared fragment**, not a full historical checker.

## Established family and shortcut controls

Odd-charge connected simple bridgeless cubic Tseitin: h vertices, 3h/2 original edge variables, m=4h strict signed 3-clauses, ASCII indexed encoding O(h log h). Urquhart 1987 proves an exponential ordinary DAG Resolution lower bound for qualifying expander subfamilies, not this mixed calculus or SAT algorithms. Every source is indispensable by the /341 deletion-witness lemma. The known explicit mixed upper bound is 3h paid AND3 conjunctions of the four clauses per vertex followed by h-1 paid GF(2) sums, total **4h-1**. The new inductive certificate matches this number precisely. A four-premise unit-cost parity extraction would instead give **2h-1** (for K4, seven rather than fifteen), but is a *different rule system* and must NOT be imported into native R_mix341.

Pang 2026 arXiv:2610.00837v2 establishes exponential opposite-characteristic fixed-degree Res(PC_r/F2) lower bounds on appropriate modulo-three expander encodings, not on all mixed native rules; known Res(lin_F3)/compact circuit shortcuts and source-preserving 3-CNF reduction overhead must be audited. Haken PHP ordinary Resolution and Cook extended Resolution likewise remain distinct model controls.

## Executed proof certificates

Executable GitHub code: experiments/arc/lspv3_536_source_partition_abstract.js, SHA blob 6231ba7e9ef887ea6e81e6b30b71463b73038e0b. Raw V8 results: results/raw/arc/2026-11-09_0824_LSPV3_536_SOURCE_PARTITION_RAW.json, blob 2985f766595e7a50a1a0f4d67f48532f7bc92531. Both were independently refetched with exact byte-equality after commits. The tests reconstruct all original strict signed 3-CNF clauses and signed truth-table AND3 inferences, validate GF(2) XOR row arithmetic, and independently track source-component DSU state after every paid node.

| Instance | Original m | Paid nodes | kappa at goal | Packet characters |
| --- | ---: | ---: | ---: | ---: |
| K4 | 16 | 15 | 1 | 2050 |
| triangular prism | 24 | 23 | 1 | 3086 |
| 4-prism | 32 | 31 | 1 | 4154 |
| 5-prism | 40 | 39 | 1 | 5231 |
| 6-prism | 48 | 47 | 1 | 6350 |

All **12 deliberately corrupted packets** rejected: bad RHS/mask, fake four-parent AND3, hidden extra facet, source mismatch/deletion, unknown/duplicated IDs, unauthorized discharge and wrong sink. One distinct identifier greater than 2^53 encoded as a **string** remained distinct and passed. Independent Python reconstructed the partition arithmetic, brute-forced odd UNSAT/even SAT for K4, prism3, prism4, and produced 72 individual source-deletion SAT witnesses; it reproduced counts for larger prisms without exhaustive model enumeration. Host Python wall time 0.076 seconds and observed peak RSS approximately 95 MiB; these are not native machine time/space complexity bounds. Neither program executes the recovered historical R_mix341 parser.

Resource distinction: m source clauses are free as logical axioms but require source acquisition and bits. Proof work is m-1 paid nodes, with explicit references and affine masks requiring O(m log m) bits for bounded-degree indexed representations; actual printed JSON sizes above are concrete, not optimal. Parsing, construction, source/index reads, search, failed policies, source-model checks, verification, serialization, cache/recomputation and simultaneous storage are separate costs. Infinite families are proved by the symbolic invariant, not finite extrapolation. Ideal balanced span can be logarithmic while total distinct-node work is linear.

## Publication, dependency status, next experiment

**Actual advance:** a source-partition **inductive abstract negative certificate** with machine-readable proof replay for a known bound and a concrete higher-arity grammar falsifier. **Verified scope:** restricted SOURCE/AND3/XOR plus conditional theorem for all exhaustively two-source-parent sound charged rules, not all historical accepted bytes. **Published:** report, JS, raw and handoff on main, complete readback (commit details in issue #3). **Remaining:** [P2-D1] native grammar and facet/branch source dependencies; [P2-C3] sound transformers for every legal rule and full normalization; [P2-B1] superpolynomial all-rule minimum; [P2-B2] noncircular same-calculus B3. Next seek an authenticated native LOCAL-CONVERT/DEF source-bearing transition and integrate context, wire-owner, affine-row and paid-history reduced products. Root main.tex not edited because complete readable bytes unavailable. No agent/task/schedule/weight changes. P versus NP OPEN.

<!-- LSPV3/536 END -->
