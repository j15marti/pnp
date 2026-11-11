# LSPV-3/569: disconnected-component parity orbits under the original archived /386 checker

**2026-11-11 05:24 PST | Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED source-orbit theorem + COMPUTATIONAL unchanged-checker replay | P versus NP OPEN.**

## Candidate and four falsifiers, registered before targeted source/byte audit

**Candidate [P2-D1/P2-C3]:** On a fixed disconnected cubic source graph, one scalar "total charge odd" is insufficient to classify source-preserving edge-flip/gauge transport. The exact invariant is the vector of parity charges on individual connected components. Nevertheless, distinct globally odd component-charge classes can each possess a separately source-authenticated, accepted original archived /386 certificate of the same fixed logical price. This is a **source-transformation and abstract-state refinement** result, not a mixed-rule lower bound.

F1: transporting the first K4 source to another component changes the fixed labeled graph or fails clause/source/parent checking. F2: the unchanged original CLI rejects a separately constructed odd-component witness or charges its one gate owner more than once. F3: the fourth odd class (111) cannot be certified without paying to refute all three UNSAT components. F4: inaccurate charge, source, owner, paid-summary or signed-literal mutations pass. The proof excludes F1 at the semantic level, original-checker positives exclude F1–F3 for the test graph, and six negatives reject F4. A **different** question, full R_mix341 grammar authentication, remains unresolved.

## Original sources, search and nonduplication

Read current complete root `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and `proof2.txt` blob `7db80e8b55a7f5c348fbb2ed8decd3ceaa2657f3`, issue #3 with recent role comments, AGENTS.md, CODEX.md, pnp-research SKILL.md, recent handoffs and the original declaration `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. Read original distinct /341 checker `experiments/arc/lspv2_341_independent_verify.js` blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0` and archived /386 original checker `experiments/arc/lspv2_386_independent_verify.js` blob **`338305c0ce101704205e57543756b8127074a986`**. The latter implements SOURCE, paid `gate_defs` owners, zero-extra-paid DEF facets and strict RES, **not** all five declared mixed operations.

Also read actual LSPV-3/565 and /566, LSPV-2/539–549, /552, /555, LSPV-4/541, LSPV-5/486, LSPV-1/560, Grok `GROKPROOF/2026-11-11_0620_PROGRESS.md`, and Claude `research/agents/claude/world-ledger/README.md`. GitHub code/history searches for Rmix341/LOCAL-CONVERT/RES AND3 found declared or distinct reference calculi, not an authoritative complete native checker. The original /566 test already proved that disjoint unions of K4 can retain W=29 when only the **first** component is odd. LSPV-3/565 already proved connected-graph charge-gauge equivalence. **The increment here is the complete component-parity classification and three additional fixed-graph original-checker accepted orbits, including 111, without pretending an illegal cross-component gauge flip.**

Primary literature: Cook and Reckhow, *J. Symbolic Logic* 44 (1979), 36–50, https://doi.org/10.2307/2273702 (system-specific proof cost); Cousot and Cousot, POPL 1977, https://doi.org/10.1145/512950.512973 (sound abstract interpretation); Clarke et al., CAV 2000, https://doi.org/10.1007/10722167_15 (CEGAR). Graph-incidence rank is proved below without invoking any complexity-theory transfer. FRAT-XOR and CakeLPR implement **other** proof formats.

## Theorem 569.1: complete component-parity quotient of signed source charge

For ANY finite undirected graph G with vertex set V, edge set E, and connected components C_1,...,C_c, let B be its vertex–edge incidence matrix over GF(2), with 1 at both endpoints of each non-loop edge. For charge vectors b,b' in GF(2)^V, there is an edge-complementation vector f satisfying

$$
Bf=b\oplus b'
$$

**if and only if** for every component j,

$$
\bigoplus_{v\in C_j}b_v=\bigoplus_{v\in C_j}b'_v.
$$

Further, rank(B)=|V|-c; its image is precisely the subspace of vectors with even parity on each component. Among charge vectors with **globally odd** parity, there are exactly 2^(c-1) edge-flip orbits. In particular, for the fixed disjoint union of three K4, c=3 and rank B=12-3=9, and the four globally odd component signatures are **100, 010, 001, 111**.

**Proof:** Every incidence column has two 1s in the same connected component, so any Bf has parity 0 on each component. Conversely, in a spanning tree of a component, recursively select the unique leaf edge to correct an arbitrary even-parity target on its leaf, delete the leaf, and continue. The final root discrepancy is zero by the parity hypothesis. Thus all even-per-component vectors are in the image. The image dimension is the sum over components of (|C_j|-1), namely |V|-c. The parity map onto GF(2)^c therefore parametrizes exactly 2^c cosets; exactly half have total parity 1. QED.

This is a **known elementary linear-algebra property**, proved here to fix the exact abstraction. It does **not** mean two odd charge vectors with *different* component signatures are linked by a legal variable-complementation transport.

## Accepted-byte experiment and active sink selection

Original input: `results/raw/arc/2026-11-11_0224_LSPV3_566_K4x3_CLI_ACCEPTED_PACKET.json`, blob `4656b801feba72b84133bacad5ae18692a83fe03`. Fixed **labeled** three-component graph: 12 vertices and 18 edges, guard variable 19; one paid conservative AND2 gate declaration, output 20; 48 signed guarded vertex SOURCE clauses plus the positive guard unit. The source is a guarded width-four CNF, **not** an unguarded proper strict-three CNF. Every original source occurrence is separately independently rechecked against the specification; source sets cannot be silently moved or weakened. Crucially, the original /386 executable reconstructs and checks these clauses from the **packet's own spec**, not an independently supplied immutable external DIMACS hash. Our source-exact comparison is relative to the fixed pinned graph/spec and does not close external original-source binding for full R_mix341.

Construct `010` and `001` by exact component swaps, permuting signed literals, source indices, gate inputs and RES pivot signs while leaving the labeled edge list unchanged. Construct `111` by replacing the eight affected signed SOURCE rows for vertices 4 and 8 with their exact opposite-charge rows; retain the first-component proof unchanged, so the two added odd components have no paid descendants in the refutation cone. This is legal for the **archived /386 checker**, which demands complete original SOURCE membership but does not demand all SOURCEs lie in the terminal ancestry.

| Component charge | Full original checker | Original assertion groups | Source records | Paid owners | Paid RES | Total W | Packet bytes incl. LF |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 100 | ACCEPT | 5,900 | 49 | 1 | 28 | **29** | 4,993 |
| 010 | ACCEPT | 5,900 | 49 | 1 | 28 | **29** | 5,059 |
| 001 | ACCEPT | 5,900 | 49 | 1 | 28 | **29** | 5,108 |
| 111 | ACCEPT | 5,900 | 49 | 1 | 28 | **29** | 4,993 |

All have 77 chronological records, 11 accepted built-in negative-control tests, and the same whole-DAG paid work. A lower-bound abstraction that charges extra whenever multiple disconnected source components independently contradict would **overcharge** the 111 accepted packet. A coarse abstraction that assumes global odd charges are all linked by a *single* legal edge-flip operation instead admits spurious transport: the 100-to-010 transformation does not lie in im B.

Six separate corruptions rejected by the unchanged original checker: charge/source mismatch; even total charge; incorrect paid total; forged source vertex identifier; illegal DEF gate input; wrong signed SOURCE clause. All test predictions matched. The code result is **COMPUTATIONAL**, not a proof of an all-input checker property; the elementary orbit theorem is symbolic.

**Execution provenance:** The original complete /386 verification body, including its 11 negative tests, was actually executed in hosted V8 with filesystem-content and diagnostic SHA-output adapters; the mathematical verification logic was unchanged. The published standalone Node.js runner pins original Git blob IDs and uses real OS Node child processes **when executed in a complete checkout**, but this OS path was not executed in this research environment. No native process timings, high-water space, GPU costs or new SHA-256 digest of V8 data are claimed.

## Typed proof-DAG and abstract-transformer implications

A sound source abstraction must retain at least `(fixed source bytes/digest, connected-component partition, per-component charge syndrome, source occurrences)`; a charge-gauge quotient may identify source configurations only when all component parities agree. This is an exact equivalence classification for **the edge-complementation action on sources**, not a substitute for the full shared proof-DAG configuration. The latter must also retain paid owner identities, parent chronologies, free defining views, active and discharged branch contexts, fresh/exported/private interfaces, and terminal goal.

For the **archived /386** abstract state, add an exact tagged component signature and a set of first-paid owners and RES node identities; a genuine source-preserving witness creation costs 1 per owner and 1 per distinct RES record, 0 for original SOURCE/facet accesses, with no double counting. The observed four separately source-bound certificates each have W=29. A potential CEGAR invariant excluding the 111 witness by forcing every contradictory component into the sink is **refuted by genuine unchanged original-checker acceptance** and must be retained; a proposed 100-to-010 one-edge-gauge abstract path is **spurious** and may be refined by the proved component signature, without excluding any legal edge-flip transform.

This supplies a named **P2-C3 source-interface refinement** only. It does not supply all-rule alpha/gamma, context/branch preservation, or full-calculus abstract transformers, and it does not establish a general proof minimum or decision-time bound. Historical logical W=29 is not the 4.9–5.1 kB evidence length; proof selection is retrospective and free. Evidence bits, actual checker time, DAG span, machine space and proof discovery remain separate. The source/paid-DAG unit-bound proof of /341 and the full /386 CLI's internal mutation tests cannot be conflated. Notably, /566 proved the original mathematical /386 core can accept the W=28 version with its unused gate removed, while the full CLI rejects it for an ineffective built-in negative test. Thus W29 is an **accepted witness cost, not an asserted optimum**.

## Published reproducibility and exact Git blobs

- OS-Node subprocess reproduction and code: `experiments/arc/lspv3_569_component_syndrome_native.cjs`, blob **4f1bcc5bba75cf4c9ea222c8449f12f5cf111124**; hosted V8 syntax preflight passed, OS execution not observed.
- Executed original-body V8 raw acceptance/rejection ledger: `results/raw/arc/2026-11-11_0524_LSPV3_569_ORBIT_NATIVE_V8_RAW.json`, blob **d32f210fec2dadd22297c0bd9925032f8c699896**.
- Exact 010 accepted packet: `results/raw/arc/2026-11-11_0524_LSPV3_569_COMPONENT_010_ACCEPTED_PACKET.json`, blob **0ca43ad60d21cf93b77cb04abd6fc3bc31126551**.
- Exact 111 accepted packet: `results/raw/arc/2026-11-11_0524_LSPV3_569_COMPONENT_111_ACCEPTED_PACKET.json`, blob **fcaed9d70a0cdce5496e777b7f82e2023bcdce56**.
- 100 is original /566 seed; 001 is deterministically emitted by the pinned code. Original full /386 checker blob **338305c0ce101704205e57543756b8127074a986**.
- All four newly created artifacts above were independently read back with exact paths, full content, and Git blob SHA.

## Status, manuscript blocker and next falsifier

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both complete current root proof trackers were reviewed, and neither gains a full-calculus theorem; no root tracker update was warranted. Exact SHA of root `main.tex` as reported by the connector was `5c117868624d40e93251b35934453eba6a746cb3`, but both full-file and line-scoped `fetch_file` returned **empty content** for the oversized manuscript. A safe exact outside-owned-region-preserving LSPV-3 edit/readback was therefore **not possible**, so `main.tex` was deliberately left unchanged. This is a publication/synthesis blocker, not a mathematical source.

**[P2-D1], [P2-C3], [P2-B1] and separately [P2-B2/B3] all remain OPEN.** No authoritative single checker has yet authenticated all declared historical R_mix341 operations, including RES-to-AND3, GF(2), LOCAL-CONVERT, paid DEF/facets, branching and discharge, shared reconvergence, weakening, deletion and interface visibility. Keep all unknown full-calculus transitions as conservative MAY operations until original source evidence is recovered. The immediate next target is one genuinely heterogeneous, fully source-bound accepted-byte certificate under a **single** historical complete checker, with two hostile wrong-type/port controls.

All five existing agents, titles, identities, schedules, Pacific timezone, historical fixed rule weights, ownership bounds and historical TWO Route A / THREE Route B labels were preserved. **P versus NP remains OPEN.**
