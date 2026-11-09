# LSPV-3/516: Exact seven-node Resolution criterion across all Q4 matching strict-3CNFs

**2026-11-08 17:05 PST | Route B | PROVED/RESTRICTED and COMPUTATIONAL | P versus NP OPEN**

Proof-chain node **[P2-L3-516]** refines [P2-L3-515], [P2-L3-514], [P2-D1], [P2-D3], [P2-C3]. [P2-B1], [P2-B2], [P2-D1], and [P2-C3] remain OPEN. No agent, task, schedule, weights, or Route A/B allocation changed.

## IDEA, falsifiers and revision

**Initial hypothesis:** The four-record external XLRUP contradictory parity certificate works for every strict-3CNF induced by a perfect matching of the four-cube, while a seven-node ordinary-Resolution refutation exists **if and only if** the matching omits some coordinate direction. This is a focused finite control on the historical RES/AND3/LOCAL-CONVERT transfer, **not** a candidate asymptotic hard family.

Four registered falsifiers: F1 an omitted or duplicated matching in two independent enumerators; F2 a source clause not indispensable or an assignment falsifying multiple sources; F3 a full-direction matching with a valid seven-inference ordinary Resolution refutation; F4 an uncovered XLRUP full parity encoding clause or a redundant source hint in a direct eight-hint row. None fired. Negative controls tested a corrupted pivot and one changed original literal.

**Revision:** The two four-direction matching orbits have different finite optimal *tree* Resolution costs, nine and eleven, while both obstruct seven-inference **shared DAG** Resolution. Do not infer from the existing /515 eight-node DAG witness that the second orbit also has an eight-node DAG proof.

## Original source and semantics

The graph Q4 has vertices in {0,1}^4 and edges between assignments of Hamming distance one. Let M be a perfect matching, consisting of eight disjoint edges. For each edge e={a,b} differing in coordinate j, introduce the **original** width-three signed clause C_e over the other three coordinates that is false precisely on the two assignments a,b. The input F_M is the conjunction of these eight clauses. It has four original Boolean variables, eight proper strict-3CNF clauses, and no auxiliary source clauses.

Every complete assignment falsifies exactly its unique matching-edge source. Therefore F_M is UNSAT and deletion of **any** original clause yields exactly two SAT assignments. All eight sources are indispensable. The /515 fixture is one instance: its original 86-byte DIMACS has SHA-256 ea6fa67341bc9ebb8b167df6f45b357276392cd5ed5b8b77f5b98bf380b19422.

## Theorem 516.1: all matching instances admit the same external four-record XOR port

For each of the two opposite four-variable parity rows, the strict published XLRUP clause-to-XOR rule checks that each of the eight full-width parity CNF clauses contains one of its cited original source clauses. Every edge in M has one even- and one odd-parity endpoint; its source clause subsumes **exactly one** forbidden full-width clause of either parity. Therefore all eight source IDs are required for **each direct row**. Two eight-hint i x records, one binary x record, and one empty export i cx record suffice: **four external records, 16 explicit source-hint references**.

This establishes soundness of the exact external rule application for all matchings, with independent local format-subset checks. It is **not** a native four-node historical R_mix341 derivation. The official CakeML cake_xlrup executable was **not run for these 272 instances**. The earlier LSPV-5/446 official replay concerned different /514 instances. XLRUP ignores source comments and does not itself bind a named original byte SHA; an explicit external source-hash wrapper is required for exact byte identity.

## Theorem 516.2: exact seven-node binary Resolution criterion

Let d_j(M) count edges of matching M oriented in coordinate j. Then, for **ordinary binary DAG Resolution**:

$$
W_{\mathrm{Res}}(F_M)=7
\quad\Longleftrightarrow\quad
(\exists j\in\{1,2,3,4\})\, d_j(M)=0.
$$

**Necessity.** All eight original clauses are indispensable. A refutation with seven two-premise, unit-cost Resolution nodes must be a read-once tree with these eight source leaves; any sharing would require a surplus inference. The falsifying set of each resolvent lies in the union of its parents' falsifying sets. The original eight sets are disjoint, partitioning all 16 assignments. The final empty clause falsifies all 16 assignments, so every containment in a seven-node read-once proof is equality. The root is a Resolution of complementary unit clauses in some variable x_j, whose falsifying sets are opposite eight-element halfcubes. Every original source edge must lie entirely inside one halfcube, so no matching edge is directed along j.

**Sufficiency.** If direction j is absent, split the matching into two independent perfect matchings of the two three-cubes at x_j=0 and x_j=1. In any matching of the three-cube each coordinate-direction edge count is even because each corresponding halfcube has four vertices; with only four edges, at least one of the three directions is absent. Split each three-cube accordingly, then each two-cube matching resolves its two source clauses to the clause excluding its fixed external coordinates. Resolving upwards produces opposite units on x_j and the empty clause. The construction uses exactly four first-level RES nodes, two second-level RES nodes, and one final RES node: **seven paid distinct nodes, depth three**, all original sources used and all AND premises discharged. No free case-split or discharge rule is added.

A four-direction matching thus needs **at least eight ordinary Resolution nodes**, whether shared or not. The /515 explicit eight-node oriented shared-DAG proof establishes equality on one of the two full-direction Q4 orbits (orbit size 32). The other full-direction orbit (size 8) has no established exact shared-DAG minimum in this run.

## Exhaustive finite verification

Two independent perfect-matching enumerators (Python first-unmatched recursion and JavaScript even-to-odd bipartite recursion) both enumerate **272** distinct Q4 matchings. Direction-count taxonomy:

| Sorted nonzero direction counts | Matchings | Seven-node ordinary RES |
| --- | ---: | --- |
| (8) | 4 | yes |
| (6,2) | 48 | yes |
| (4,4) | 36 | yes |
| (4,2,2) | 144 | yes |
| (2,2,2,2) | 40 | **no** |
| **Total** | **272** | **232 yes, 40 no** |

Cube-coordinate permutations and translations produce eight automorphism orbits with sizes 4,8,12,24,32,48,48,96. The 40 full-support instances form exactly two orbits of 32 and 8. Exhaustive finite Resolution-tree dynamic programming over the 81 possible four-variable non-tautological clauses gives **minimum tree costs nine and eleven** on those two orbits, respectively. This is finite tree search, not a proof of the minimum shared-DAG cost of the second orbit.

Python reference verifier: 31,935 assertion groups; 272 source partitions, deletion witnesses and paired eight-hint coverage checks; 232 explicit seven-node certificates and oriented pivots; all eight orbit representatives; malformed pivot and altered original-source negative controls. Wall time 4.77032 s; tracemalloc peak 844,493 bytes, **excluding Python interpreter/RSS, network, GitHub, caches, output/readback**. Independently authored and run Node.js: **8,976** assertions, matching direction counts, UNSAT source partitions and paired parity hint coverages. Source code and raw outputs are separate artifacts. Python code SHA-256 039f3bd434938d7e15d4bc1e8955d31b0164aec0c75d48b33cb4c703a3da02a3; raw JSON SHA-256 f253c4a0f8a67eb01f7128dd8c0be0a325ddda0d8feb6f881a6939b39e2942cf.

## Established family/theorem/encoding/method/remaining-transfer ledger

| Element | Exact model-qualified record |
| --- | --- |
| Published hard family | Odd-charge Tseitin on suitable connected cubic expanders, h vertices, 3h/2 edge variables and 4h original proper signed 3-clauses, one source for each forbidden local wrong-parity triple. Standard explicit decimal-index DIMACS has N=Theta(h log h) bits. |
| Lower-bound theorem | Urquhart, Hard Examples for Resolution, JACM 1987, DOI 10.1145/7531.8928; 2^Omega(h) ordinary shared-DAG Resolution lower bounds on suitable expander/charge families. Ben-Sasson and Wigderson, Short Proofs Are Narrow, JACM 2001, DOI 10.1145/375827.375835, provides resolution width/size tools. Not all-machine hardness. |
| Strong upper control | Historical declared SOURCE/AND3/XOR fragment on original Tseitin: 3h local AND3 inferences plus h-1 binary XOR inferences, 4h-1 paid nodes. This defeats an unqualified ordinary-Resolution-to-all-mixed lower-bound transfer. Cook ER and GF(2) shortcuts must remain legal upper-bound controls. |
| This Q4 study | Focused finite original-source certificate/control only, **not** an asymptotic 3-SAT hardness family. Source capacity seven, external four-record port, 16 hints, geometry-sensitive Resolution minimum. |
| Open transfer | Authenticate historical RES-to-factor, paid DEF defining facets, LOCAL-CONVERT, exported/private wires and assumption discharge, then derive all-legal-rule lower bounds and noncircular same-system B3. Equisatisfiability alone does not transfer lower bounds. |

## IDEA -> SEARCH -> ITERATE source ledger and governance

Read **both complete** proof1.txt (preflight SHA 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b) and proof2.txt (preflight SHA 5de28fd3141765e8452d78fe5210981ad61c4ed6), issue #3 including /515 and /446; governing five-role handoff research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (historical commit 4e29ed7646f484707767acb6e63ec5f38afd98a8), AGENTS.md blob 19656af..., CODEX.md 754999f..., skill b8df83..., original native /341 rule declaration research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb, its recovered partial checker experiments/arc/lspv2_341_independent_verify.js, LSPV-3/515 report f9aed3b802319f83fb26e2719592319cb55b93d4 and handoff. Read actual GROKPROOF/2026-11-08_1130_PROGRESS.md blob 6942a99f... and research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex blob 79e4d4...; neither authenticates missing historical rule bytes.

Required other-repository review: konard/p-vs-np scripts/proof_status.json blob 93b77ed3...; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693e... and REVIEW_ADDENDUM.md blob 6a7cc2...; meelgroup/frat-xor format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f and cake_xlrup/README.md blob c71de809...; peitl/short-proof README.md 93d2090...; berkeley-abc/abc README.md 88a9d1...; openai/math README.md cc5b0a.... These establish neither historical R_mix341 nor B3. Searched primary research and GitHub by ordinary web search. No dedicated Google-branded interface was available. No claims of novelty or official checker execution.

Root main.tex retrieval returned SHA 42fd637c90bb8eec6b7a8e181990c6650b725fd2 with **zero content bytes**; safely left unchanged, not a whole-document reconciliation. Every inference weight, five agent IDs, titles, schedules, enabled states, and two Route A/three Route B ownership preserved.

**Next gap:** Demonstrate *native accepted-byte* four-source-hint-to-binary RES/AND3/LOCAL-CONVERT source-authenticated simulation with fully charged nodes/facets, or give an exact legal obstruction in the true historical grammar. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. P versus NP OPEN.
