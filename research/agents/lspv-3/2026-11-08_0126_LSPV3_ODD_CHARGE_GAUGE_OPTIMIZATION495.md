# LSPV-3/495 | Charge-gauge optimized original one-hot Tseitin proofs with paid CAST3

**2026-11-08 01:26 PST | Route B, Hypergraph & Proof Certificates | PROVED/RESTRICTED mathematical upper bound; COMPUTATIONAL independent checks; full historical mixed transfer OPEN.**

**Exact proof-chain IDs:** [P2-L3-495] (new restricted evidence), [P2-L3-494], [P2-L3-492], [P2-L3-493], [P2-D1], [P2-C3], [P2-F13], [P2-B1], [P2-B2]. Companion all-input nodes [P1-01], [P1-03], [P1-04] remain OPEN. Both root trackers were fully read. Nothing in this report establishes P versus NP.

## IDEA and falsifiers specified before source review

Hypothesis: for the ORIGINAL q=2 one-hot, odd-charge cubic-graph Tseitin source, changing the globally consistent choice of one-hot representative on each original edge permits a 13h-node source-authenticated refutation in the *previously declared distinct* R_cast494 paid RES/CAST3/AND3/XOR calculus for **every odd charge vector**, removing the k-1 unnecessary charged conversions from LSPV-3/494 when k>1.

Four falsifiers: (F1) the required representative choices have an inconsistent GF(2) incidence system; (F2) representation switching changes the original CNF or silently supplies new source axioms; (F3) conversion count, local affine-alias semantics, or final parity cancellation fails for any odd charge; (F4) the recovered historical R_mix341 checker authenticates this as a native proof. F1 is falsified by the connected-incidence rank argument below; F2/F3 are falsified by exact construction, exhaustive small controls and direct semantic tests; F4 remains UNPROVED because recovered historical /341 accepts SOURCE/AND3/XOR only, not the required RES/CAST3 parent interfaces. This is an *explicit model limitation*.

## SEARCH: original published hardness family and prior art

Primary paper: Shuo Pang, A Degree–Size Relation for Resolution over Polynomials, arXiv:2610.00837v2 (24 Oct 2026), section 7.1, Theorem 7.2(b), https://arxiv.org/html/2610.00837v2 . This paper's exponential refutation-size bound is for fixed-degree expander **q=2 one-hot Tseitin** sources in syntactic Res(PC_r/F3) with fixed r, **not** for R_cast494, historical R_mix341 or all algorithms. No source reduction is used here. Original source uses 3h Boolean indicator variables and 7h clauses of width at most 3; explicit source bit size N=O(h log(h+2)). This is source UNSAT and target restricted-system hardness, not certified general computation hardness.

Historical project evidence actually read: root proof1.txt and proof2.txt, five-role November 2 handoff (historic ref 4e29ed7646f484707767acb6e63ec5f38afd98a8), current issue #3, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, original LSPV-2/341 rule prose (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb) and recovered source/AND3/XOR checker (fcb7d4ced8f922de14c0bda16263a8cc7853e8e0). Prior /492 code blob 024fd147aa07d1d378d38bbc060e2bf84cef0111, /494 code blob 5ecef3b6dbb762f0d373ee0485c8e1ff58cbd3d3, and LSPV-5/412 historical grammar nonuniqueness were reused, not rediscovered. LSPV-1/498 and /499 describe *different* restricted random-3CNF transfer systems with no historical full mixed simulation.

Outside claims and critiques actually opened: konard/p-vs-np/scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2) and proofs/complexity/README.md (7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5), REVIEW_ADDENDUM.md (6a7cc2f8962d3fcfcfc1778b1d3d8f5dc8d56d70); meelgroup/frat-xor/format.md (986a21aa92b62f844ef1fce852193142c41b2b1f); tanyongkiam/cake_lpr/README.md (e94f45e9aa000cd9ada12f4c771ac9daf28fe53c); peitl/short-proof/README.md (93d2090dba9739bc4983c65ea639a24e1f5e0fab); and openai/math/README.md (cc5b0a03bca6c742f045d683b6647a6f44ef2cae). Independent Grok file GROKPROOF/2026-11-08_0320_PROGRESS.md (72edb3140d8ed798d0905a827f85d3428728e396) and Claude research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex (79e4d4e7e0e3edff3aba8610852c45534bdde128) were inspected as critique, not theorem authorities. Google-specific branded UI was not separately available; general web research and GitHub connector searches were used. No novelty priority is inferred from the searches. Required adversarial controls include Haken's ordinary DAG Resolution PHP lower bound, Cook's Extended Resolution shortcut, and GF(2) Tseitin elimination.

## ITERATE: Theorem 495.1 (PROVED/RESTRICTED)

Let G=(V,E) be a connected simple cubic graph with h=|V| (necessarily even), |E|=3h/2, and odd charge b in F2^V. Let T(G,b) be Pang's **unaltered original** one-hot source. For each edge e, introduce no new original variables: use its existing indicators a_(e,0), a_(e,1). Original edge clauses are (a_(e,0) OR a_(e,1)) and (NOT a_(e,0) OR NOT a_(e,1)). For each vertex v and each local edge-value triple s of parity unequal to b_v, the original vertex clause is OR_{e_j incident to v} NOT a_(e_j,s_j). The original source has exactly 3h variables and 7h clauses, and is UNSAT because XOR of all vertex equations is 0=1.

The **distinct** R_cast494 is a fixed sound, complete, effective, unit-paid rule system: original source-labelled clause axioms, correctly oriented binary ordinary Resolution, paid unary CAST3 converting one already derived clause with <=3 variables into its IDENTICAL truth-table factor, AND3 of two factor parents with combined original-variable support <=3, and binary exact GF(2) equation addition. Original SOURCE clauses are factors, whereas a RES output is NOT automatically a factor. All distinct paid nodes are charged once; source clauses are free. CAST3 and its historical LOCAL-CONVERT equivalence remain unverified.

Choose a globally consistent original edge representative r_e = a_(e,c_e), c_e in F2. Let t_v = XOR_{e incident v} c_e. At vertex v, exactly one of its four forbidden source triples equals its representative triple if and only if t_v != b_v. Such a vertex requires exactly three CAST3s in this four-leaf normalization; otherwise it requires four. Each edge position disagrees with its chosen representative in exactly two of the four forbidden triples at its incident vertex, independently of charge. Accordingly **6h** oriented RES steps using the original edge-clause axioms always suffice.

Each edge contributes to two t_v values; therefore XOR_v t_v=0. Since h is even and XOR_v b_v=1, the hypothetical target t_v=1 XOR b_v for *every* vertex is inconsistent (its total parity is 1). At least one vertex must therefore use four casts. Fix a root v0 and put t_v=1 XOR b_v for all nonroot v, and t_v0=b_v0. This target now has even total parity and is realized by the connected vertex-edge incidence matrix, which has rank h-1 over F2. A spanning-tree reverse-leaf algorithm constructs c in O(h) bit operations. Exactly one vertex uses four CAST3s and h-1 use three, totaling **3h+1 CAST3**. This is the **minimum only within the globally consistent representative-based four-leaf construction**, not within all legal proof DAGs.

The four normalized local clauses per vertex combine with three AND3 nodes to an exact parity factor (three-bit exhaustive Boolean table) and an affine alias on the existing representative bits:
    
$$
\bigoplus_{e\ni v} r_e
 = b_v \oplus \bigoplus_{e\ni v}(1\oplus c_e).
$$

Adding all h equations by a balanced binary XOR tree cancels each r_e twice and yields 0=1. The complete exhibited paid-node budget is

$$
q_{\mathrm{RES}}=6h,\quad
q_{\mathrm{CAST3}}=3h+1,\quad
q_{\mathrm{AND3}}=3h,\quad
q_{\mathrm{XOR}}=h-1,
\qquad
\boxed{q=13h},\quad
D\le6+\lceil\log_2 h\rceil.
$$

Therefore W_Rcast494(T(G,b)) <=13h for **EVERY odd b** on connected cubic G. Prior LSPV-3/494 gave 13h+k-1 for k charge-one vertices; its k-1 excess is an avoidable representation choice. This is a constructive upper bound in a **proposed separate calculus**, not historical mixed proof acceptance, not a global optimum, and not an all-algorithm lower bound. The charge-gauge identity itself is elementary and not asserted novel.

## Independent verification and hostile controls

The **GitHub-published code directly derived from the actual /492 producer and /494 paid typed verifier** reconstructed original clauses and all GF(2) rows, checked exact typed CAST3 parent scopes and AND3 factor premises, and replayed nine original one-hot packets in isolated JavaScript V8 (not the Node CLI wrapper). At h=4 (K4), h=6 (K3,3), and h=8 (cube) and k=1,3,5,7 where valid, every charge had q=52,78,104 respectively. Paid node spans were 8,9,9. **All 63 deliberately corrupted typed-packet controls were rejected** in this published-code replay. The exact derived published code and complete raw summary were fetched back byte-for-byte.

Separately authored stand-alone Node producer/checker was executed locally, not against the historical checker: 9 original-source certificates accepted, **72 malicious certificate mutations** rejected, **54 malformed/mismatched external DIMACS source controls** rejected, and independent SAT/UNSAT source model checks (odd: zero; even counterpart: 8,16,32). A separate Python exhaustively enumerated all 18,048 possible edge representatives across those nine small controls: CAST minimum always 3h+1, with 32/96/256 optimal edge gauges for K4/K3,3/cube. These are reproducibility checks, not asymptotic proofs. Full independent standalone code, raw/certificate packets, and SHA256 manifest are in the separately supplied LSPV3_495_GAUGE_OPTIMIZED_REPRO.zip.

**Committed/readback-verified reusable code and raw data:**
- experiments/arc/lspv3_495_gauge_onehot_base.cjs; blob a3ede13e3863619d420c1ccea0a4543afe5eb301.
- experiments/arc/lspv3_495_paid_gauge_onehot.cjs; blob 98578acd7afd83389ed602d9efbad7126d73de10.
- results/raw/arc/2026-11-08_0126_LSPV3_495_GAUGE_OPTIMIZED_V8.json; blob 896848c87374a9918af48efb8dbb29397e9511fb.

## Family/model/upper-bound ledger and remaining transfer

Family: Pang original q=2 one-hot odd-charge cubic-expander Tseitin (when G is in the published expander sequence). Size parameter h, 3h original indicator variables, 7h original 2/3-clauses, N=O(h log h). Established external hardness: exp(Omega(h)) in **syntactic** Res(PC_r/F3) for fixed r on specified expanders. Source UNSAT: elementary odd-charge parity. Known shortcut: exact linear GF(2) Gaussian elimination; explicit fully paid RES/CAST3/AND3/XOR proof q<=13h in R_cast494, no new source or uncharged conversions. Remaining transfer: historical accepted-byte RES parent views, original-source authentication, LOCAL-CONVERT authority, paid DEF facets, exported/private wires and unrestricted mixed proof-to-proof normalization.

The exhibited proof contains 13h distinct paid logical inference nodes and O(log h) ideal unit-weight span under unlimited-parallel binary-fanin scheduling. Output includes O(h log h) indexed original input bits plus O(h^2 log h) conservative dense masks and node references; an actual sequential producer pays all h gates and output-bit writing. A physical upper bound must separately include source parsing/index/head reads, connectedness recognition, GF(2) gauge solving, construction, failed strategies/restarts, truth-table checks, evidence serialization, caches and references, independent verification, and peak simultaneous storage. Source-external authentication is a distinct concern. This run makes **no** measured native Turing-machine steps/RSS/FLMV exponents, and its ideal proof-work minimum intentionally excludes discovery cost. No branch-local assumptions or split/discharge rules are used.

**OPEN:** [P2-D1] exact historical R_mix341 grammar/byte checker; [P2-C3] all-rule original-source normalization; [P2-B1] superpolynomial worst-case minimum work over **ALL historical mixed rules**; [P2-B2] genuinely noncircular B3 (SAT in P => polynomial Wbar in SAME R_mix341). Nothing closes [P1-01], [P1-03], [P1-04]. Root main.tex remains untouched because complete safe retrieval had been unavailable in prior runs; this run does not change rules, weights, task IDs, schedules, enabled states, or the existing 2 Route A / 3 Route B allocation. **P versus NP remains OPEN.**
