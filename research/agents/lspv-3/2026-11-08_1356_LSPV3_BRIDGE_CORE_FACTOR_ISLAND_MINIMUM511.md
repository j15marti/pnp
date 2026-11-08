# LSPV-3/511: Bridged cubic Tseitin has an exact four-h-minus-one minimum in the SOURCE/AND3/XOR-only core

**2026-11-08 13:56 PST | LSPV-3 / Route B | PROVED/RESTRICTED plus COMPUTATIONAL | P versus NP OPEN**

**Node IDs:** [P2-L3-511] new restricted result; refines [P2-L3-510], [P2-D3], [P2-D1], [P2-C3]. [P2-B1] and [P2-B2] remain OPEN, as do [P1-01], [P1-03], [P1-04]. This is NOT an authenticated theorem about complete historical R_mix341.

## IDEA and precise falsifiers (registered before searching)

Hypothesis: in the separately fixed SOURCE/AND3/exact-affine-alias/binary-XOR fragment, a connected simple cubic odd-charge Tseitin source requires all four original vertex clauses at EVERY vertex, even when the graph has bridges and some of those clauses are logically redundant in the full CNF. This would give the *exact* restricted cost 4h-1, while the older model-independent indispensable-source lower bound is only M-1.

Falsifiers: (F1) a legal <=3-original-support AND3 joins factor clauses belonging to different vertices; (F2) a conjunction using fewer than four local clauses yields an exact nontrivial affine row; (F3) a proper vertex subset yields an XOR combination with zero incidence mask and odd RHS; (F4) prior work already proves this exact restricted bridged minimum or a historical accepted proof uses a cheaper native rule within the *same fixed fragment*.

The hypothesis survives F1-F3, with complete local truth-table closure and finite graph controls. F4 identifies important related work, LSPV-1/445's 37-node bridge proof in a STRONGER declared semantic mixed calculus using LOCAL, but not an exact theorem for the present strict core. Thus the actual contribution is a sharpened **calculus-boundary control**, not a novel algorithmic lower bound.

## SEARCH: provenance and prior work

Read both complete shared trackers at start: proof1.txt SHA 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; proof2.txt SHA ec1bcf4ee51581801841ac44a08fd6701a91dd2f (510,336 characters). Current coordination issue #3, including recent LSPV-3/510, LSPV-1/514 and LSPV-5/443 comments; historical five-role handoff research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md, AGENTS.md (19656af...), CODEX.md (754999...), .codex/skills/pnp-research/SKILL.md (b8df83...); LSPV-3/510 report blob cc0cbad880424170a2355eab98730d1cee18e6a7; LSPV-1/445 bridge report blob 5f7c22fa91a0870bf333332e3991fd179035e36a; LSPV-5/386, /388 and historical native-core audit.

Original declared R_mix341: research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob c87acd3547fa90025dfaaea07b84794b7f79e651. Its recovered *restricted* executable checker is experiments/arc/lspv2_341_independent_verify.js, blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0, with SOURCE, AND3 and XOR dispatch, no RES/LOCAL/DEF dispatch. Historical checker also hardcodes a 4h-1 proof length; the theorem below is instead independently symbolic and does not infer minimality from that assertion. LSPV-5/413 recovered and narrowed this checker.

Actual peer files read: GROKPROOF/2026-11-08_1130_PROGRESS.md, blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70, and research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex, blob 79e4d4e7e0e3edff3aba8610852c45534bdde128. Neither authenticates the cross-rule bridge.

Primary proof-complexity sources: Urquhart, JACM (1987), DOI 10.1145/7531.8928, ordinary Resolution expander lower bounds; Ben-Sasson and Wigderson, JACM (2001), DOI 10.1145/375827.375835, especially the connected odd-Tseitin definition and expander-based ordinary-Resolution hardness. Those known exponential bounds concern connected cubic **expanders**, not these bridged controls. They do not transfer into the full mixed calculus.

Change-aware repository reads: konard/p-vs-np scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 (formalized finite-model P subset NP), blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 (scoped proof research), meelgroup/frat-xor format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f (XLRUP external proof format), tanyongkiam/cake_lpr README.md blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c, peitl/short-proof README.md blob 93d2090dba9739bc4983c65ea639a24e1f5e0fab, openai/math README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae. None supplies a native historical RES-to-AND3 port. The FRAT-XOR/Cake LPR format is not silently treated as an R_mix341 certificate.

## Exact family, calculus and theorem

Let G=(V,E) be **any finite connected simple cubic graph**, including one with bridges, h=|V| and |E|=3h/2. For each edge e use ONE original Boolean variable x_e. Choose b in GF(2)^V with XOR_v b_v=1. At each vertex v the original strict signed 3-CNF includes the four length-three clauses that forbid exactly the four local assignments whose parity is different from b_v. Thus the source has 4h exact width-three clauses and N=Theta(h log h) indexed DIMACS bits. The system is UNSAT because XOR of all vertex equations reads 0=1.

Define R_core511 as the **separate incomplete grammar** with free, literal-exact SOURCE clauses as three-original-variable factors; unit-cost binary AND3 can conjoin factors only if their combined tagged support has at most three ORIGINAL variables, preserves that tagged support, and may attach a row only under exact truth-table equivalence; unit-cost binary GF(2) XOR can combine two existing row-bearing parents. XOR produces an affine node, never an AND3 input. No RES, LOCAL-CONVERT, paid DEF, case-split, weakening, source-independent aliases, or new cross-kind coercion is admitted. Proofs are finite source-authenticated acyclic shared DAGs, and each distinct paid node is charged once. This is the recovered accepted fragment's operational *model*, not a complete grammar claim about R_mix341.

**Theorem 511.1, PROVED/RESTRICTED.** For every such (G,b), including bridged graphs,

$$
\boxed{W_{R_{\mathrm{core511}}}(F_{G,b})=4h-1.}
$$

**Proof.** (1) The three-edge incident support at each vertex differs from every other vertex's support because G is simple cubic. Any two different supports have union >3. Every SOURCE factor begins on exactly one vertex support, and an AND3 result maintains the same union support. By induction, all factor DAGs are vertex-local, including with arbitrary sharing and reconvergence.

(2) The four source clauses at v each prohibit one *different* parity-wrong triple. A factor depending on any nonempty subset S of these four clauses accepts exactly 8-|S| local assignments. Any nontrivial exact affine equation on three Boolean variables accepts exactly four; a zero-mask affine tautology accepts eight and a contradiction accepts zero. Thus no proper nonempty S can be tagged with an affine row. The full four-clause conjunction, and only it, yields the exact row XOR_{e incident v}x_e=b_v. This argument covers all possible repeated AND3 applications because a conjunction's truth set is the complement of the union of excluded local triples.

(3) All XOR derivations are GF(2) sums of these vertex rows. The left mask for vertex subset U equals the graph edge cut delta(U). Since G is connected, delta(U) is empty only for U=empty or U=V. The first has RHS 0; the second has RHS 1 by odd charge. Therefore **every** refutation needs all h vertex rows, hence all 4h original clauses somewhere in its ancestry, independently of how XOR rows are shared, reused or reconverged.

(4) A connected refutation ancestry with m=4h distinct source leaves and q unit-paid at-most-binary inference nodes has at least m+q-1 undirected edges and at most 2q premise edges, hence q>=m-1. A matching construction uses three local AND3 operations at each vertex (3h) and h-1 XOR additions, for 4h-1. QED.

**Important comparison with the more expressive semantic calculus:** LSPV-3/510 proved that for v with c_v components of G-v, only 2^(3-c_v) of its four source clauses are individually indispensable. The simple two-K4 bridged graph has h=10, essential sources M=36, source-only topology floor 35, yet W_core511=39. The three-arm example has h=16, M=55, source-only floor 54, yet W_core511=63. These do NOT contradict LSPV-1/445's *37-node* bridge derivation in the broader declared R_mix341 semantics: its paid LOCAL/RES-style conversions are outside this restricted core. No historical full-checker acceptance is claimed. The strict core result is a model-sensitivity and legal-shortcut control; adding rules can only lower W.

## ITERATE: direct finite falsification and resource audit

Published executable: experiments/arc/lspv3_511_bridge_core_factor_islands.js, exact blob 45b5e6dc800ba7d14b00742cef3e510df7713150. It was executed directly in the V8 code environment; the standalone Node CLI was not separately launched. Raw results: results/raw/arc/2026-11-08_1356_LSPV3_511_BRIDGE_CORE_FACTOR_ISLANDS.json, blob dfcce3e1867128916e41bcec0cf84be427932889, **133,870 assertion groups** over nine graph controls, both charges for each local truth table, all 15 nonempty local factor-conjunction subsets, all potential 3-variable affine aliases, connectivity cuts for all proper vertex subsets through h=16, source essentiality and incidence data.

Independently written Python reproducer executed locally, with **137,280 assertion groups**, including fresh GF(2) Gaussian-elimination checks for clause-deletion satisfiability and source-model witnesses on all nine graph sizes. It reports 0.205 s wall and 96,148 KiB resident host memory; host Python timings are not asymptotic machine bounds. This independent artifact is retained as the accompanying downloadable fallback and is not falsely claimed to be the historical checker.

Selected exact results:

| Graph | h | Original clauses | Individually essential M | General source floor M-1 | Exact restricted core W |
|---|---:|---:|---:|---:|---:|
| K4 | 4 | 16 | 16 | 15 | 15 |
| K3,3 | 6 | 24 | 24 | 23 | 23 |
| Cube | 8 | 32 | 32 | 31 | 31 |
| Two subdivided K4s with bridge | 10 | 40 | 36 | 35 | 39 |
| Three-armed subdivided K4s | 16 | 64 | 55 | 54 | 63 |
| Prism64 | 128 | 512 | 512 | 511 | 511 |

Logical work is W=4h-1 distinct unit nodes. The **chosen** balanced construction has an ideal unlimited-processor critical-path upper bound 2+ceil(log2 h), not an all-DAG minimum-depth claim. A source-indexed trace has O(h log h) bits and sparse-row tree replay can use the prior LSPV-1/514 O(h log^2 h) bit-time and O(h log h) all-phase upper bounds under its explicit model; do not silently charge those as native FLMV costs. The present Python V8 finite tests separately charged source construction, grouping, component computations, local closure enumeration, GF(2) witness solving (Python), checking and raw JSON output. No SAT oracle, negative model oracle, hidden gate, free CAST or unsupported branching rule was employed. Neither machine-time/space exponents nor native full mixed certificate bits were established for arbitrary R.

## Outcome, publication and remaining gap

The new exact restricted theorem separates *semantic source redundancy* from *mandatory source use in a typed proof fragment*. It additionally gives two explicit bridge controls where the minimum in this weak fragment exceeds the general indispensable-source floor. It does not prove an all-legal-rule minimum, much less an arbitrary-machine SAT lower bound.

TRACKER: new [P2-L3-511] is material because it quantifies an exact model-boundary gap relative to [P2-L3-510]. The shared proof trackers should remain OPEN at [P2-D1] historical full grammar, [P2-C3] all-rule transfer, [P2-B1] superpolynomial all-mixed Wbar, and [P2-B2] noncircular same-calculus B3; Route A unchanged.

Next decisive task is to authenticate the *historical* RES/DEF/LOCAL-CONVERT and exported/private-parent byte productions, or find an explicit legal proof cross-interface counterexample. No silent alteration of fixed R_mix341 grammar, weights, agents, ownership, enabled states, time zone or 2A/3B allocation. P versus NP remains OPEN.
