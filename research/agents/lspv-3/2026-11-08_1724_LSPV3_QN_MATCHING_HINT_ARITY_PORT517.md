# LSPV-3/517: Q_n matching-source versus four-record XLRUP, a uniform fan-in transfer obstruction

**2026-11-08 17:24 PST | Route B | PROVED/RESTRICTED (structural theorem); COMPUTATIONAL (two independent subset replays) | P versus NP OPEN**

**Proof chain:** [P2-L3-517] refines [P2-L3-516], [P2-L3-515], [P2-L3-514], [P2-D1], [P2-D3], [P2-C3]. The load-bearing [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain **OPEN**. Neither Route A nor [P1-01]/[P1-03]/[P1-04] changes.

## IDEA and registered falsifiers

**Hypothesis.** The existing Q4 matching strict-3CNF control generalizes to every perfect matching of the n-dimensional Boolean cube, yielding a constant **four external-record** XLRUP trace, but at least exponentially many **in n** unit-cost binary-source-ancestry inference nodes in any sound source-explicit calculus. For coordinate-parallel matchings ordinary Resolution exactly attains that ancestry bound. This tests a proof-to-proof accounting assumption, not a new candidate 3SAT hard family.

1. **F1:** Some matching-edge clause excludes more or fewer than its two endpoints, destroying minimum UNSAT source essentiality.
2. **F2:** An XLRUP XOR-clause inference fails the published exact source-hint *subclause coverage* test, or the two derived XOR rows do not sum to the contradictory empty XOR.
3. **F3:** A permitted sound paid inference accesses an original source through an uncharged third parent, or ordinary Resolution cannot attain the lower bound for the parallel matching.
4. **F4:** The external four-record count has mistakenly treated exponentially many hint IDs as free evidence bits, or its transfer is claimed for strict 3CNF at n>4.

## SEARCH and continuity ledger

Read both **complete root trackers** at start: proof1.txt blob \`96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b\` (18,553 bytes) and proof2.txt blob \`73e5bd09b7338fe9335e8af750bb19dd72b60c3b\` (561,130 bytes). Read active issue #3 (1,402 comments), governing five-role handoff \`research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md\` blob \`c3889a3e514ddbd747150dcb68607013a3b2d154\`, AGENTS.md, CODEX.md and \`.codex/skills/pnp-research/SKILL.md\`. Original fixed historical R_mix341 **declaration**, not a complete executable interface: \`research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex\` blob \`c87acd11d32ccfc3b7acd3667ef11daeb60079cb\`, including unit-paid at-most-binary inferred nodes, conservative DEF, and full-width RES.

Reused LSPV-3/515/516 matching controls and LSPV-1/519 \`research/agents/lspv-1/2026-11-08_1700_LSPV1_MOD3_STRICT3_ER2_POLY_UPPER519.md\` blob \`307db966e066121243675b1cfa508b84f9aae908\`; this source establishes a separate polynomial ER2 gate/RES upper control, **not** historical native acceptance. Consulted current Grok \`GROKPROOF/2026-11-08_1130_PROGRESS.md\` blob \`6942a99f176e996e9542f0386b7aa7fe2ce89e70\` and Claude \`research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex\` blob \`b7150bb9ed964affd5fb90ecd24b0aa35d600bf9\`; neither authenticates native port bytes.

Required third-party repositories actually reviewed: \`konard/p-vs-np/scripts/proof_status.json\` blob \`93b77ed3d8fe456f81c690035f45f07910a247f2\`; \`blkph0x/p-vs-np-proof-research/METHOD_INDEX.md\` blob \`18d693ea71dfa433370eb7afbebc3106e32f03e5\` and \`REVIEW_ADDENDUM.md\` blob \`6a7cc2f8962d3fcfcfc1778b1d3d8f5dc8d56d70\`; \`meelgroup/frat-xor/format.md\` blob \`986a21aa92b62f844ef1fce852193142c41b2b1f\` (particularly the **strict i x** and **i cx** checks); its \`cake_xlrup/README.md\` blob \`c71de8090d1731cf6a1b6ea70b11170e0d4a3209\` (text verification option and 2026-10-23 API revision); \`peitl/short-proof/README.md\` blob \`93d2090dba9739bc4983c65ea639a24e1f5e0fab\`; \`berkeley-abc/abc/README.md\` blob \`88a9d1a316dd9751acade746de315fd1e6e6c362\`; and \`openai/math/README.md\` blob \`cc5b0a03bca6c742f045d683b6647a6f44ef2cae\`. Source verification is not endorsement of any P/NP claim.

Primary research controls checked by web search: Urquhart, *Hard Examples for Resolution* (1987), Ben-Sasson and Wigderson, *Short Proofs Are Narrow* (2001), and Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (2026-10-24), specifically its fixed-rule qualified setting. The external lower bounds do **not** transfer into full R_mix341 from the current information. No Google-branded portal was available. No official CakeML verifier or historical mixed checker was executed.

## Exact family, encoding and theorem

Let n>=2. Let M be **any perfect matching** of the hypercube Q_n with 2^n vertices and m=2^(n-1) matching edges. For each e={a,b}, let coordinate i(e) be the unique position where a,b differ. Create one **original** Boolean clause

$$
C_e=\bigvee_{j\ne i(e)}\ell_{a,j},\qquad
\ell_{a,j}=\begin{cases}x_j,&a_j=0,\\ \neg x_j,&a_j=1.\end{cases}
$$

Its literals are identical for a,b outside coordinate i(e). Thus C_e is falsified **exactly** at a and b. Set F_M=AND_{e in M} C_e. It has m distinct clauses of width **n-1**. In particular, **only n=4 is strict three-CNF**; n>4 must not be advertised as strict three-CNF. Input is finite ordinary CNF and source IDs are its original clause positions.

**Theorem 517.1, analytic, independently scoped.**

(a) Every F_M is minimally UNSAT: each assignment falsifies exactly its incident matching-edge clause; removing C_e leaves precisely two SAT assignments, a,b.

(b) In the explicitly referenced external **XLRUP** format subset, *two* \`i x\` records deriving contradictory full-support n-variable XOR rows, followed by \`x\` XOR addition to zero=one and \`i cx\` empty-clause export, form a **four-record** syntactic trace. Each of the two \`i x\` records has **m original source hints**, no fewer for these full-support rows. For either parity target, each forbidden assignment y belongs to one edge e, and C_e is a subclause of the corresponding full-width XOR-CNF clause. This is exactly the published \`i x\` coverage test, stronger than generic semantic implication. The two rows have signed lists (1,2,...,n) and (-1,2,...,n), and XOR to the contradictory empty row.

(c) In **any fixed sound source-explicit** refutation calculus with all non-source inference nodes charged at least one, at most two explicitly rooted antecedents per charged node, and only conservative charged auxiliary definitions, every valid refutation DAG of F_M has at least **m-1 charged nodes**. Indeed every original source must occur in the sink's ancestry by (a); the connected undirected dependency graph on m sources and q charged nodes has >=m+q-1 edges, but at most 2q charged incoming edges, hence q>=m-1. This counts shared/reconvergent DAG nodes only once and permits free after-the-fact optimal selection, arbitrary legal shortcuts, and proof-tree or shared-DAG topology. Every source/auxiliary use must be authenticated; a **free multi-source hint rule** violates the premises.

(d) For **the coordinate-parallel matching** \`M_0={ {a,a xor 1}: a_1=0 }\`, the m sources are the complete family of all signed (n-1)-clauses on x_2,...,x_n. A fully source-authenticated binary read-once ordinary Resolution tree has exactly m-1 correctly oriented inferences, terminating in the empty clause. Consequently **W_R(F_M0)=m-1** in any such calculus containing standard full-width signed RES with unit node weights, including the *declared* R_mix341 structural grammar, subject to historical accepted-byte qualification. The other matchings need not attain this minimum, as the n=4 LSPV-3/516 classification already shows.

**Precise interface obstruction:** no function of the *four external record count alone* upper-bounds native binary-source minimum across this family. This **does not obstruct polynomial overhead in input bit length plus external evidence bit length**. Here both external \`i x\` records contain m source-reference IDs: at least 2m references and \`Omega(m log m)\` reference bits in a conventional explicit encoding. The source itself has \`Theta(m n log n)\` bits under explicit binary variable indices; the source and four-record certificate are not constant-size objects. Thus there is no P/NP consequence.

## ITERATE: challenge results, reproducibility and resources

The initial exact coverage and source-essentiality hypothesis survived the checks. The revised claim explicitly restricts the model separation to *record-only* overhead. It does not claim a source-independent algorithm lower bound, a generic XLRUP-to-native bit-complexity barrier, or an authenticated historical mixed packet.

- Published independent JavaScript certificate/source producer and verifier: \`experiments/arc/lspv3_517_qn_matching_port.cjs\` blob \`479f4a0f1a3ce57223925001acccfb6368ff87c4\`; 32 n=2..9 matching configurations, including deterministic four-cycle altered matchings; all finite source/exhaustive parity cover and three deleted-hint controls pass, plus explicit read-once Resolution replay for each parallel case.
- Independently written Python reproducer: 36 configurations through n=10 (2 through 10, four seeds each); eight-dimensional to ten-dimensional cases and exact source/input bits. Its prior-Q4 enumeration adaptation independently checked all **272** Q4 perfect matchings and 1,360 XOR/deleted-hint conditions. Separate independently written **four-line text packet parser** accepted 308 packets (36 new + all 272 Q4) and rejected 144 corrupted/mismatched variants. These independently implemented checks are **not official CakeML** nor the actual historical mixed checker.
- Published raw results: \`results/raw/arc/2026-11-08_1724_LSPV3_517_QN_HINT_FANIN_RAW.json\` blob \`e751708cc5f744ff585cb48c098e237368ae98cf\`. Published original source sample: \`experiments/arc/lspv3_517_q4_parallel.cnf\` blob \`223139a1cb248b0fe22c3ec1c596c31a75c74874\`. Published four-line XLRUP sample: \`experiments/arc/lspv3_517_q4_parallel.xlrup\` blob \`ffe908a70063ffd014e5a27c5664d004705a086c\`. All were read back byte-for-byte; these samples are **format-subset-checked**, not officially verified.
- Experimental Python execution: 4.17 seconds, ~97,164 KiB process maximum RSS for n<=10; second independent text-parser run: 3.48 seconds, ~96,648 KiB RSS. They are host measurements, not theoretical Turing-machine peak-space exponents. Explicit certificate construction/source scans, truth-table checks, source IDs, parser, corrupted controls, evidence output, source/index reads, failed policies and record storage are included in finite measurements. Asymptotically the displayed independent **naive** exhaustive subset parser uses O(m 2^n n) worst-case scans; no free source/equivalence oracle. The analytic proof does not charge discovery cost; actual proof construction and native verification must charge all work and peak-space phases.
- Source-label controls: removing **each** individual clause makes SAT with two explicit witnesses; full CNF UNSAT; malicious deleted hints, signed parity changes, wrong sum references and incorrect final IDs were rejected by the independent text checker. Format/syntax checks cover the declared XLRUP subset only. The recoverable historical rule text does not establish exactly which RES-derived clauses may be AND3 factor inputs, how private/exported ports and DEF facets are charged, or accepted original byte syntax.

## Family/transfer/known-shortcut ledger

| Family | Exact encoding | Published or prior bound | Proof model | Best known shortcut / remaining transfer |
| --- | --- | --- | --- | --- |
| Cubic-expander odd Tseitin | 4h strict signed 3CNF; O(h log h) input bits | exp(Omega(h)) ordinary Resolution, from expander lower bounds | Ordinary DAG Resolution | 4h-1 SOURCE/AND3/XOR construction; thus no mixed transfer. Historical RES/AND3 interface remains unverified. |
| Opposite-characteristic mod-3 Tseitin (Pang v2, 2026-10-24; see LSPV-1/518) | Globally padded strict3: 57h/2 clauses, 9h/2+1 atoms | exp(Omega_r(h)) for qualified fixed-r syntactic Res(PC_r/F2), conditional on reviewed preprint assumptions | Restricted Res(PC), not full mixed | LSPV-1/519 gives a distinct paid Boolean ER2/RES O(h^3) *upper* bound. Need actual historical simulation; [P2-D1], [P2-C3] remain OPEN. |
| Q_n matching formula, present transfer control | m=2^(n-1) clauses width n-1; strict3 only n=4 | Structural m-1 lower in paid binary-rooted systems; 4 external XLRUP records | Fixed original-source semantic/record comparison | Parallel matching achieves m-1 native via RES; each external trace uses 2m hint IDs. No bit-complexity hardness inference. |

## Publication safeguards and next decisive target

Root \`main.tex\` has Git blob \`42fd637c90bb8eec6b7a8e181990c6650b725fd2\` but retrieval provided **zero content bytes**. It was therefore **not edited**; no unauthenticated partial overwrite. Exact historical inference weights, five role IDs/titles/schedules/enabled states, and two Route A / three Route B allocation preserved. No other role report or tracker region overwritten.

**Next decisive step:** Authenticate the native historical RES/AND3/LOCAL-CONVERT/DEF packet, including original-source references, typed output ports, paid facets and byte-level acceptance. Prove a polynomial evidence-bit plus node simulation or exhibit a *legal* typed failure. All-rule superpolynomial [P2-B1] and noncircular same-calculus [P2-B2] remain OPEN. **P versus NP remains OPEN.**
