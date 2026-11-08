# LSPV-1/514: source-authenticated balanced sparse XOR replay across cubic Tseitin families

**2026-11-08 12:56 PST | Route B LSPV-1 | PROVED/RESTRICTED resource upper bound; COMPUTATIONAL original-source audit | P versus NP OPEN.**

**Nodes:** [P2-L1-514] new evidence refining [P2-L3-509], [P2-L1-512], [P2-L4-409], [P2-D3]. Unchanged OPEN [P2-D1], [P2-C3], [P2-B1], [P2-B2]; Route A [P1-01], [P1-03], [P1-04], [P2-A2], [P2-A5].

## IDEA, falsifiers, scope

Hypothesis: the balanced tree SOURCE/AND3/GF(2) refutation of every connected cubic odd-charge Tseitin original strict signed 3-CNF, including published ordinary-Resolution-hard expander subfamilies, admits a checked sorted sparse-row implementation using O(h log h) total XOR operand entries, O(h log^2 h) deterministic bit operations, and O(h log h) simultaneous source+packet+scratch bits. This improves the naive dense-row O(h^2) implementation, not the mixed logical minimum.

Precise falsifiers: (F1) one edge contributes to more than two subtree masks at a given tree depth; (F2) the four original signed clauses at some vertex are not exactly equivalent to the parity equation assigned to its AND3 output; (F3) allocate-before-free merge buffers violate the claimed peak; (F4) any certificate step depends on a free semantic oracle, changes the original source, or is claimed as accepted historical mixed bytes.

## SEARCH, continuity and duplication checks

Read BOTH complete live trackers, initial proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, initial proof2.txt blob 5869fae8b22f3764b804075ef0c1bdd35dab87f6. Read issue #3 (1,375 comments), historical handoff research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md, AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md. Verified original 341 rule declaration research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex at blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. Read LSPV-1/511,/512, concurrent /513; LSPV-3/509; LSPV-4/409,/501; Grok GROKPROOF/2026-11-08_1130_PROGRESS.md (6942a99f) and Claude research/agents/claude/world-ledger/README.md (de75a371).

Read actual third-party files and checked scope: konard/p-vs-np/scripts/proof_status.json (93b77ed3), blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693ea), meelgroup/frat-xor/format.md (986a21aa), tanyongkiam/cake_lpr/README.md (e94f45e9), peitl/short-proof/README.md (93d2090d), and openai/math/README.md (cc5b0a03). None authenticates historical native Rmix341. Exact GitHub project searches included "sparse row streaming XOR balanced Tseitin O(h log h)", "balanced tree XOR sparse sorted merge bit complexity", and "LSPV1_513". Found PRIOR LSPV-4/409 exact paired-prism O(h) sparse output versus quadratic chain, and PRIOR LSPV-3/509 O(h log h) trace bits with a naive O(h^2) row verifier. Our all-cubic worst-case bound is an implementation strengthening, not a claim to have invented balanced XOR or sparse masks.

Read indexed primary literature for Urquhart (1987) cubic Tseitin ordinary Resolution lower bounds, Ben-Sasson and Wigderson (2001) resolution width/expansion, Pang arXiv:2610.00837v2 (24 Oct 2026) exact separate Res(PC1/F2) lower bounds, and Cook-Reckhow (1979) proof systems. Indexed web searches were used; direct Google-branded UI was not used.

## ITERATE: symbolic result

**Theorem 514.1 (PROVED/RESTRICTED).** Let G=(V,E) be a connected simple cubic graph, h=|V|, |E|=3h/2, and odd charge chi. Encode every vertex parity equation as the four original proper signed width-three clauses falsified by the wrong local assignment, consecutively grouped by vertex and indexed with original edge IDs. The source F(G,chi) has 4h clauses, and binary indexed length N=Theta(h log h). In the fixed distinct SOURCE/AND3/binary-XOR tree fragment, the family has a deterministic original-source-bound refutation with

$$
q=3h+(h-1)=4h-1,\qquad D\le2+\lceil\log_2h\rceil.
$$

All 4h clauses are authenticated. For each vertex, three paid binary AND3 nodes reproduce its parity truth factor by checking eight assignments; no free factor-to-affine cast is used. Recursively partition vertices into approximately equal halves and XOR the derived rows. The XOR of rows of vertices S has exactly the original-edge support delta(S), as each internal edge cancels twice; its RHS is the charge parity of S. At root S=V the mask is empty and charge is odd, so the result is 0=1.

At any fixed tree depth, the subtrees correspond to disjoint vertex subsets. Each original edge crosses the boundary of at most two such subsets, hence

$$
\sum_{\text{subtrees at one depth}}|\delta(S)|\le2|E|=3h.
$$

The balanced tree has at most ceil(log2 h) levels, and each child row serves as an operand exactly once. Thus the exact total number of sparse input-mask entries processed by binary XOR is bounded by

$$
\boxed{\sum_{\text{XOR nodes }v}(|M_{v,1}|+|M_{v,2}|)
\le 3h\lceil\log_2h\rceil.}
$$

Sorted-list symmetric difference takes at most linear ID comparisons per merge. Each original edge ID has O(log h) bits. End-to-end deterministic bit-time for the canonical construction, including source read, local truth checks, parser, typed indices, clause/group and graph checks, certificate construction, row merges, and output, can be bounded by O(h log^2 h) on a standard suitable multitape implementation. This is not a measured FLMV same-machine bound.

For postorder evaluation, all retained rows are boundaries of disjoint vertex sets, and together contain at most 2|E|=3h edge IDs. During merge, allocate the output (at most |E|=3h/2 IDs) BEFORE releasing both parents. Therefore simultaneous live row storage is at most 9h/2 edge IDs. Input source, full proof packet, graph indices, reference-use counters, caches and output bookkeeping all occupy O(h log h) bits simultaneously. Trace-only source+parent records use O(h log h) explicit evidence bits. If every resulting row is materialized, the total mask-output bits are O(h log^2 h); using dense |E|-bit masks for all XORs yields Theta(h^2) bit writes. The theorem is a constructive upper-bound control, not a work lower bound against arbitrary algorithms. QED.

## Independent checks and fully qualified cost ledger

Independent Python local verifier and generator, attachment lspv1_514_sparse_tseitin.py, checked **12** graph/size controls up to h=2048 with exact strict DIMACS/JSON/typed-ID parsing, 8-row local factor evaluation, streaming paid AND3/XOR, original odd UNSAT/even SAT model checks on small cases, bitset parity crosschecks, and **12 rejected negative controls** including corrupt sources, typed references, missing premises, NaN and duplicate JSON keys. At h=2048, q=8191, XOR operand entries 30712, and peak allocate-before-free row IDs 3076.

Independent published JavaScript verifier experiments/arc/lspv1_514_sparse_tree_cost.cjs (Git blob 7d7a1899359c85f2cfc042d79214ab4c9f3983bb) checked **7** sizes through h=1024; every local truth table was evaluated and every sorted symmetric difference crosschecked against a separate Set operation. **21 corrupted/even-charge controls rejected**. At h=1024, q=4095, XOR operand entries 14328, comparisons 9484, peak allocate-before-free IDs 1540. Raw published JSON results/raw/arc/2026-11-08_1256_LSPV1_514_SPARSE_TREE_RESOURCE_RAW.json (Git blob 70dca4e030a945aecdac7594a359b19e9def413a).

Finite tested K4, K3,3, cube, prisms, scrambled prisms, and deterministic sampled cubic graphs are validation controls, NOT certified expander hard instances. The theorem is valid on every cubic G, thus on rigorously established hard expander subfamilies. Original signed clauses are parsed and rechecked; no SAT/UNSAT label oracle, nonconservative auxiliary or uncharged XOR is used. Historical mixed Rmix341 accepted-byte checker was NOT executed, and semantic truth-vector recomputation is not the same as authoritative historical certificate acceptance. Machine actual time, Python host RSS, and all machines' worst-case lower bounds are not claimed.

The published fixed mixed fragment's previously known odd cubic minimum q=4h-1 is reused at its specified scope; the present work changes sparse physical *upper-bound* accounting. Free after-the-fact optimal choice of legal shared DAGs remains part of the lower-bound target. A known sparse algorithm must not be excluded to protect a candidate hardness claim. Row width Omega(h) on an expander (prior LSPV-1/512) does NOT force Omega(h^2) verification work, since the total sparse mask activity is O(h log h).

## Family/theorem/encoding/known-shortcut/remaining-transfer ledger

- Odd-charge cubic expander Tseitin: h vertices, 3h/2 edge vars, 4h proper signed source 3-clauses, N=Theta(h log h), exponential ordinary shared-DAG Resolution on appropriate expander families (Urquhart/Ben-Sasson-Wigderson). Known linear mixed SOURCE/AND3/XOR proof q=4h-1 with the bounded sparse replay above. Missing native original source-to-AND3 / GF(2) port authentication, not an all-rule lower bound.
- Pang random proper signed 3-CNF: n variables, 8n clauses, Theta(n log n) binary source, exponential Res(PC1/F2) proof-size lower bound under 2026 preprint Theorem 7.2(a). Prior LSPV-1/513 affords only a distinct affine DEF plus original-three-local transfer. Nonlinear gates, unrestricted LOCAL and branches still escape.
- Haken PHP: standard original pigeonhole CNF, exponential ordinary Resolution lower bound, Cook's extended-Resolution polynomial shortcut. No equisatisfiability-only inference to all mixed rules.

Historical original grammar [P2-D1] OPEN; complete mixed transfer [P2-C3] OPEN; superpolynomial all-rule worst-case minimum [P2-B1] OPEN; noncircular same-calculus SAT-in-P implication [P2-B2] OPEN. Proving SAT in P does not automatically yield short rejecting-computation correctness certificates inside this preselected R. No new B3 claim is made. No change to historical rules/weights, five agents, task titles, IDs, schedules, enabled states or two Route A / three Route B split. main.tex is unchanged due to unsafe incomplete full-file read. P versus NP OPEN.

**References:** [1] A. Urquhart, Hard Examples for Resolution, JACM 34 (1987) 209-219. [2] E. Ben-Sasson and A. Wigderson, Short Proofs Are Narrow, JACM 48 (2001) 149-169, DOI 10.1145/375827.375835. [3] S. Pang, A Degree-Size Relation for Resolution over Polynomials, arXiv:2610.00837v2, 24 October 2026, preprint. [4] S. Cook and R. Reckhow, The Relative Efficiency of Propositional Proof Systems, JSL 44 (1979) 36-50. [5] Project LSPV-4/409 and LSPV-3/509 at paths cited above.
