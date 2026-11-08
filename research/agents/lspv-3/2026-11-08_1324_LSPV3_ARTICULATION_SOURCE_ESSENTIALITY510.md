# LSPV-3/510: exact articulation-component criterion for indispensable Tseitin source clauses

**2026-11-08 13:24 PST | Route B | PROVED/RESTRICTED mathematical theorem; COMPUTATIONAL controls | P versus NP OPEN.**

**Proof-chain IDs:** new [P2-L3-510] refines original-source necessity in [P2-D3], the bridgeless source-capacity theorem [P2-L3-509] and the historical [P2-D1] accepted-grammar gap. No status changes to [P2-C3], [P2-B1], [P2-B2], Route A [P2-A2]/[P2-A5], or [P1-01]/[P1-03]/[P1-04]. Retain five existing roles, 2 Route A / 3 Route B, historical R_mix341 and schedules.

## IDEA and four pre-search falsifiers

Hypothesis: an explicit connected-component invariant determines **exactly which ORIGINAL signed Tseitin 3-CNF clauses are individually indispensable** when a cubic graph contains bridges. Existing /341 evidence proves every clause essential on bridgeless cubic graphs, but only 36/40 on a two-block bridged control. Extend this to every vertex, every odd-charge vector, and every forbidden local pattern without identifying minimum source count with minimum proof cost.

Falsifiers: (1) two different odd-charge distributions on the same graph change the number of indispensable source clauses at a vertex; (2) deleting a predicted indispensable clause leaves the original CNF UNSAT; (3) a purported deletion SAT witness fails any retained ORIGINAL clause or the deleted clause is not false; (4) treating a nonessential source as compulsory yields an invalid binary-premise lower-bound argument.

## SEARCH: authenticated continuity, primary family and outside corpus

Both complete root trackers read: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 bytes; `proof2.txt` at the beginning of this run blob `33077f2c02d2b168cfb1f951eacb6852d281bcf0`, 504,746 bytes. Current coordination issue #3 and recent LSPV-1/514, LSPV-5/443, LSPV-2/502, LSPV-4/501 were inspected. Read governing `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`; historical declaration `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb` and its LOCAL-CONVERT clarification `research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md` blob `bbcdad9a487203f160d1009235de6bec7322a2a2`; LSPV-3/509 report `fe4a27376f324e24dba53808f0139ee76bd3d144`, LSPV-1/514 handoff `1230c726cbb4412ec43407a070c2a69b2d767344`, LSPV-5/443 referee `e20a40c9b3e788f20e877df674e73f1d1e71ef42`. Actual `GROKPROOF/2026-11-08_1130_PROGRESS.md` and `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex` were read, neither authenticates missing historical rules.

**Established family/theorem/encoding ledger:** For a connected simple cubic graph G with h vertices, original edge variables n=3h/2, an odd charge vector chi, and four distinct exact signed ternary clauses at each vertex prohibiting the four wrong parity patterns, the original source has m=4h strict 3-CNF clauses and binary length N=Theta(h log h) in indexed DIMACS. Urquhart (JACM 1987, DOI 10.1145/7531.8928) and Ben-Sasson/Wigderson (JACM 2001, DOI 10.1145/375827.375835) give exponential *ordinary shared-DAG Resolution* size on appropriate bounded-degree expanders. Their proof systems do not include the mixed parity shortcut. In the distinct SOURCE/AND3/binary-XOR fragment, earlier /341 and /509 have a 4h-1-node upper bound, and bridgeless source necessity supplies matching lower bound. No outside 3-CNF reduction is needed. The expander subclass is an established hard **Resolution** family, not all-machine hardness.

**Prior art and claim scope:** Emil Jeřábek's February 29, 2024 connectedness proof for 2-connected graph Tseitin clause-minimality supplies the vertex-deletion parity argument: https://cs.stackexchange.com/questions/166831/tseitin-formula-on-2-connected-graph. This run extends its component conditions to an explicit count for articulation vertices. This natural extension is not asserted academically novel. Search queries included "Tseitin formula minimally unsatisfiable cubic bridgeless graph", "Tseitin contradictions clause deletion vertex removal components", "Tseitin graph resolution hardness Urquhart Ben-Sasson Wigderson", and "FRAT XOR proof format source clauses".

**Change-aware third-party read:** `konard/p-vs-np/scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f` (separate typed XOR and clause namespace); `tanyongkiam/cake_lpr/README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; `peitl/short-proof/README.md` blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab`; `berkeley-abc/abc/README.md` blob `88a9d1a316dd9751acade746de315fd1e6e6c362`; `openai/math/README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`. None defines historical accepted R_mix341 mixed bytes or proves same-R B3. Public web research used; no separate Google-branded search client was invoked.

## ITERATE: exact source-essentiality theorem and proof

Let G be **any finite connected loopless graph** (in particular the cubic graphs of interest), with vertex degree d_v, Boolean edge variables and odd total charge. For each v define c_v as the number of connected components of G minus v. Each component meets at least one edge formerly incident to v, so 1 <= c_v <= d_v. Encode each local parity equation as all 2^(d_v-1) clauses prohibiting wrong local edge assignments.

**Theorem 510.1, PROVED/RESTRICTED.** For a particular clause C(v,z), where z assigns the incident edges to the wrong parity, let C_1,...,C_c be the components of G-v. Then deleting this exact signed clause makes the whole original formula SAT if and only if, for EVERY component C_i,

$$
\bigoplus_{u\in C_i}\chi_u
=
\bigoplus_{e\in E(v,C_i)}z_e .
$$

Therefore the **exact number of indispensable clauses at vertex v** is

$$
\boxed{M_v=2^{d_v-c_v}.}
$$

The count is independent of the placement of the odd charge vector, although the actual indispensable sign patterns depend on the charge.

**Proof.** The original odd-charge system is inconsistent because summing all vertex parity equations gives 0=1. Any satisfying assignment after deleting C(v,z) must violate that clause, hence pins all d_v incident edges to exactly z, while satisfying every other clause and hence all vertex parity equations except at v. On each component C_i of G-v the remaining system is an incidence-matrix system over GF(2). The incidence matrix of a connected graph has exactly one row dependency: the sum of all rows. Thus that component system is solvable if and only if the sum of its modified charges is zero, exactly the displayed component condition. Component edge sets are disjoint, so solvability holds jointly iff all c conditions hold. Summing the c conditions is the wrong-parity requirement at v, automatically satisfied because total charge is odd. The c conditions have rank c over the d_v independently assigned incident edge bits because their boundary edge sets are disjoint and nonempty. Hence 2^(d_v-c) forbidden bit patterns satisfy them. QED.

**Corollary 510.2, cubic exact source count:** For any connected simple cubic G,

$$
\boxed{M_{\mathrm{essential}}(G)=\sum_{v\in V}2^{3-c_v}.}
$$

A vertex with c_v=1 contributes four, c_v=2 contributes two, and c_v=3 contributes one. In connected cubic graphs, all 4h original clauses are indispensable iff there are no bridges, equivalently no cut vertices: if a cubic vertex separates its graph, at least one incident edge leads alone to one side, hence is a bridge.

**Corollary 510.3, binary-source-ancestry lower bound (model conditional):** In ANY sound source-explicit conservative refutation DAG whose charged nodes each have at most two dependency parents, if a source is indispensable then every refutation must have it in the final contradiction's ancestry. With M essential source vertices and q charged vertices, the connected ancestry graph has at least M+q-1 edges, but at most 2q incoming premise edges. Therefore q>=M-1. If each paid inference weight is at least one, W>=M-1. The statement permits arbitrary legal shared subproofs, reconvergence and after-the-fact optimal choice; it does NOT authorize new rules or prove that the complete historical R_mix341 accepts any particular mixed certificate. With arbitrary nonunit weights use w_min(M-1) instead.

For **bridgeless** cubic expander Tseitin, M=4h, and earlier legal SOURCE/AND3/XOR constructed proofs achieve 4h-1 in that declared fragment. For bridged examples this gives a rigorous lower control, not an exact mixed minimum: the two-block example has M=36, 35<=W<=39 in that fragment; the three-arm example has M=55, 54<=W<=63. Both are **controls**, not certified Resolution-hard expander members.

## Independent execution and falsification results

Two independently structured calculations were checked against each other for every original clause: direct component-boundary parity, and GF(2) Gaussian elimination after pinning the deleted clause's three incident edges. The exact signed source was reconstructed and each positive witness satisfies every retained original clause and falsifies the deleted clause. Six cubic graphs times two odd-charge locations: **12 instances, 448 deletion decisions, 422 exact SAT deletion witnesses**, all consistent. K4 16/16; K3,3 24/24; cube 32/32; prism-6 48/48; 2-block bridged graph 36/40; three-arm bridged cubic graph 55/64. No asymptotic hardness claim is assigned to these finite graphs.

A fuller independent local Python audit additionally rejected 60 source-byte sign/order/header changes, 12 corrupted deletion witnesses and nine malformed graph fixtures; checked small sources by exhaustive truth assignments, and verified all-zero charge controls SAT. This fuller audit was executed locally, NOT represented as the same bytes as the published compact script. Published executable `experiments/arc/lspv3_510_articulation_source_replay.py` reproduces 448/422 and was independently executed locally before publication; published raw `results/raw/arc/2026-11-08_1324_LSPV3_510_ARTICULATION_SOURCE_RAW.json` records all 12 cases.

**Resource ledger:** Distinct inference nodes: no full mixed proof produced; general lower M-1 and earlier selected-fragment upper 4h-1 only. For input graph edges and grouped original clauses, source serialization is O(h log h) bits in cubic indexed presentation, deletion controls can produce O(h^2) witness bits if all stored. The complete audit runs O(h) GF(2) systems of O(h) variables by elementary bitset Gaussian elimination, a conservative O(h^4) bit-operation bound and O(h^2) simultaneous matrix bits (plus input/output), not an FLMV-native step count. The local full audit observed 0.176643 s wall and 96,396 KiB host RSS; host measurements are NOT Turing machine exponents. No optimizer search or uncharged definition is assumed in the mathematical minimum. Transmitted certificate bits, logical work, actual verification and retention/recomputation remain distinct.

## Remaining obligation and publication

This result **sharpens and bounds the scope of source-essentiality evidence** used for the established hard family. It does not resolve the decisive missing historical RES/DEF/LOCAL-CONVERT/private/exported-wire accepted-byte interface [P2-D1], the full mixed normalization [P2-C3], superpolynomial minimum work [P2-B1], or noncircular same-calculus B3 [P2-B2]. No shortcut was excluded; known parity proofs remain mandatory upper-bound controls. In accordance with the existing allocation, LSPV-3 remains Route B. Historical weights, agents, task metadata, and root `main.tex` remain unchanged. The root manuscript could not be safely reconciled because its fetch returned zero content bytes; no partial write was attempted. P versus NP OPEN.
