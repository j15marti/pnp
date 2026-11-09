# LSPV-3/515: Strict-3CNF Q4 matching, XLRUP source-hint arity and exact typed proof costs

2026-11-08 16:27 PST. Route B. **PROVED/RESTRICTED**, **COMPUTATIONAL**. P versus NP OPEN. Proof-chain evidence [P2-L3-515] refines [P2-D1], [P2-D3], [P2-C3], [P2-L3-514], peer [P2-L5-446]. Full [P2-D1]/[P2-C3], superpolynomial all-rule [P2-B1], and noncircular B3 [P2-B2] remain OPEN.

## IDEA and four falsifiers

Test a source-authenticated UNSAT proper strict 3CNF whose eight clauses partition the Boolean four-cube into eight disjoint edges. F1: not a perfect partition or a source not essential. F2: either proposed XLRUP parity row fails strict hint coverage. F3: a legal semantic-support shrink or RES-to-factor shortcut refutes the claimed core obstruction. F4: an ordinary DAG Resolution proof uses only seven charged nodes. F1/F2/F4 do not fire; F3 DOES in a DISTINCT free support-shrink AND3 calculus with seven nodes. The original hypothesis must therefore be scoped to fixed-support core, not historical all-rule R_mix341.

## SEARCH and continuity

Read complete current proof1.txt and proof2.txt prior to writing, historical five-role refocus 2026-11-02_1204, current GitHub issue #3 including LSPV-5/446 and LSPV-1/518, AGENTS.md blob 19656af102604d5f0a721d548cf2e4e72a063561, CODEX.md 754999f50de93cdb693ed37bc8110d31e9e698ef and pnp skill b8df83a7b0b1428f349b0e02ce1387d979e8db7f. Recovered historical original /341 rule declaration research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb; partial recovered checker experiments/arc/lspv2_341_independent_verify.js blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0; /514 report blob d145f7c84571ff09c407f11bb2e39aed499339bb. Grok real file GROKPROOF/2026-11-08_1130_PROGRESS.md blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70; Claude research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex blob 79e4d4e7e0e3edff3aba8610852c45534bdde128. Read both mandatory research repos: konard/p-vs-np scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 and proofs/complexity/README.md 7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and REVIEW_ADDENDUM.md 6a7cc2f8962d3fcfcfc1778b1d3d8f5dc8d56d70. Neither authenticates historical R_mix341. Read actual FRAT-XOR strict format meelgroup/frat-xor format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f and cake_xlrup/README.md blob c71de8090d1731cf6a1b6ea70b11170e0d4a3209; tanyongkiam/cake_lpr README.md and openai/math README.md. Web research confirmed Urquhart 1987 and Ben-Sasson/Wigderson 2001 hard expander-Tseitin ordinary Resolution scope, plus FRAT-XOR primary syntax. No Google-specific interface. Hard-family ledger remains original signed proper cubic-expander odd-charge Tseitin, 4h clauses, N=Theta(h log h) bits, ordinary shared-DAG Resolution 2^Omega(h) with expander hypotheses. This is NOT a hard-family lower bound for all mixed rules; the new Q4 instance is a focused typed counterexample only.

## Exact source and signed hypergraph

Use vertices 0..15 of Q4 and matching edges (0,1),(2,3),(4,6),(5,13),(7,15),(8,12),(9,11),(10,14), with two edges in each coordinate direction. For every edge include the strict width-three signed clause falsified precisely at its two endpoints. Canonical DIMACS original source (86 bytes; SHA-256 ea6fa67341bc9ebb8b167df6f45b357276392cd5ed5b8b77f5b98bf380b19422):

~~~text
p cnf 4 8
2 3 4 0
-2 3 4 0
1 -3 4 0
-1 2 -3 0
-1 -2 -3 0
1 2 -4 0
-1 3 -4 0
1 -2 -4 0
~~~

Every of 16 assignments falsifies exactly one clause. Deleting ANY source clause produces exactly two satisfying assignments. Thus the original proper strict 3CNF is UNSAT and all 8 sources indispensable.

## Theorem A: four records in external strict XLRUP (PROVED/RESTRICTED)

Each of the two XOR rows over all four variables has eight CNF-encoding clauses. For each forbidden assignment, the matching edge's three-literal original source clause is contained in its four-literal encoding clause. Therefore strict published i x hint covering succeeds for BOTH opposite parity equations with all eight original source IDs as hints.

~~~text
i x 1 -1 2 3 4 0 1 2 3 4 5 6 7 8 0
i x 2 1 2 3 4 0 1 2 3 4 5 6 7 8 0
x 3 0 1 2 0
i cx 9 0 3 0
~~~

Proof: 94 ASCII bytes, 4 EXTERNAL records, 16 explicit source-hint references, weighted record depth 3 under unit-record unlimited parallel model. This is NOT four paid historical R_mix341 nodes. Independently validated format subset only, NOT official CakeML checker replay on this witness. External exact original SOURCE byte binding requires a separate byte-hash wrapper, following peer [P2-L5-446], because the format itself binds parsed clauses rather than a named byte string.

## Theorem B: fixed-support SOURCE/AND3/XOR fragment cannot refute (PROVED/RESTRICTED)

The original clauses have four distinct three-variable supports, each with exactly two clauses. A fixed-support AND3 can only combine parents within the SAME triple, because different source supports union to FOUR original variables. For each support the only reachable truth-table factors are its two source clauses (each satisfying 7/8 local assignments) and their conjunction (6/8). None equals a nontrivial affine equation, and none is false. Thus no XOR seed, no GF(2) contradiction and no fixed-support-core refutation. Crucially, if legal RES/LOCAL conversions or FREE semantic support shrink are allowed, this obstruction does NOT apply. The original historical fully accepted mixed grammar remains unverified.

## Theorem C: ordinary shared-DAG Resolution has EXACT minimum eight (PROVED/RESTRICTED)

All eight source clauses are indispensable. Binary-premise source capacity gives at least seven paid nodes. If only seven nodes refuted F by pure Resolution, the proof would be a read-once tree with all eight source leaves, no sharing. The falsifying sets of sources are pairwise disjoint and sum to the entire 16 assignments. Since the root empty clause also falsifies all 16 assignments and each resolvent's falsifying set is contained in the UNION of its parents' falsifying sets, every inference would have to preserve union EXACTLY. The root must resolve opposite unit clauses on some variable xj, partitioning the cube into its two halfcubes. But there are source matching edges crossing BOTH halfcubes in EVERY coordinate direction, so no such source can belong to either child subtree without violating the exact-partition requirement. Therefore at least eight RES nodes are necessary. An explicit original-source oriented refutation exists:

~~~text
9  : RES(1,2)   = ( 3, 4)
22 : RES(4,5)   = (-1,-3)
28 : RES(6,8)   = ( 1,-4)
37 : RES(3,22)  = (-3, 4)
50 : RES(7,22)  = (-1,-4)
57 : RES(9,37)  = ( 4)
62 : RES(28,50) = (-4)
65 : RES(57,62) = ()
~~~

The derived node 22 is shared, counted ONCE; the DAG has 8 original sources and 8 paid inferences, with 16 premise references and cycle excess 1. Therefore W_ordinary_Resolution(F)=8. Since declared R_mix341 contains RES with unit cost, its model-level minimum is bounded by 7<=W_Rmix341(F)<=8, **not certified exact**, because unresolved rule interfaces may permit 7.

## Theorem D: distinct stronger systems can reach seven (PROVED/RESTRICTED)

In a SEPARATELY PROPOSED calculus allowing one AND3 inference to shrink its factor support to the exact minimal semantic support for FREE, seven binary AND3 conjunctions using pairs (1,2),(4,5),(6,8),(3,7),(9,10),(11,12),(13,14) produce an all-false factor. Their minimal supports are {3,4},{1,3},{1,4},{1,3,4},{1,3,4},{1,3,4},empty. Last factor is exactly annotatable as GF(2) 0=1. Binary source-capacity lower bound 7 proves this distinct minimum EXACT. A distinct proposed free RES-to-factor port also yields a seven-node typed derivation (three RES plus four AND3). Neither permission is presumed historical. The single-node charge and support/port type rules materially change proof minimum.

## Actual verification and full resources

Separately implemented and executed Python (conversation fallback) produced 70 assertion groups and 8 corrupted-source/certificate rejections, 16 full assignment checks, eight deletion-controls each with 2 SAT witnesses, 12 fixed-support reachable factors / zero affine rows, exact oriented eight-RES certificate, and both seven-node controls. Python Resolution discovery constructed 57 candidates in four rounds, examined 1858 candidate resolvents, then trimmed to 8 used nodes. Python wall time 0.053015 seconds, tracemalloc peak 97578 bytes, EXCLUDING interpreter RSS, GitHub reads/writes, network and caches. The independently written published JS was executed in V8 with 6 negative controls and all the stated core/Resolution/free-shrink checks. No actual official cake_xlrup or complete historical R_mix341 binary was executed on THIS witness. The ideal after-the-fact minimum deliberately excludes discovery costs; an implementation upper bound must charge source reads, parsing, failed search, candidate generation, verification, all output and simultaneous peak storage. Finite experiments are not asymptotic computational lower bounds.

## Proof-chain and publication safeguards

Material new evidence: [P2-L3-515], refining [P2-D1], [P2-C3], [P2-D3], [P2-L3-514] and peer [P2-L5-446]. [P2-D1], [P2-C3], [P2-B1], [P2-B2] still OPEN, P versus NP OPEN. No change to historical R_mix341 rules/weights, five agents, IDs, titles, schedules, enabled states or 2 Route A / 3 Route B allocation. Main.tex full read returned ZERO bytes despite nonempty blob; no unsafe modification. All report, code, raw and handoff paths are owned by LSPV-3.
