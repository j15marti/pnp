# LSPV-1/389: logarithmic-support all-proof bit budget and five-role handoff

**November 4, 2026, 04:58 PST**. Scope: restricted typed-interface metatheorem, not a theorem about every presentation of the full unchanged mixed calculus. Independent specialist mathematical review pending; P versus NP remains **OPEN**.

## Authenticated mathematics

The existing fixed proof calculus is **unchanged**: \`R_mix341\`, source \`research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex\`, Git blob \`c87acd11d32ccfc3b7acd3667ef11daeb60079cb\`. Free original signed clauses; one paid node each for RES, AND3, GF(2) XOR, LOCAL-CONVERT and conservative two-input DEF. At most two antecedent nodes; only paid DEF creates reusable fresh global variables.

Published anchor Haken (1985): for all sufficiently large h and **all ordinary shared-DAG Resolution** refutations of unary PHP(h+1,h), at least 2^(c h) lines; explicit source N=Theta(h^3 log h) signed indexed bits. Cook (1976) provides polynomial Extended Resolution proofs. No ordinary-Resolution bound is transferred to R_mix341, Res(XOR) or arbitrary machine time.

**Restricted exact metatheorem 389:** For a typed derivation with q paid nodes, N signed source bits, at most a observed private circuit ports per paid continuation and every live port syntactically dependent on ≤ b=max(1,ceil(c log2(N+q+2))) previously authenticated boundary wires, and with value-extensional downstream rules and an explicit polynomially serialized non-circuit grammar, there is a same-node-count, same-source refutation of at most

\`\`\`
G <= (a q+1)b 2^b            private payload gates
bits <= K_(a,c) M^max(3,c+2) log2(M+2), M=N+q+2
\`\`\`

All correlations between live output ports are preserved for all boundary assignments. Complete derivation proof and resource ledger: [formal report](../agents/lspv-1/2026-11-04_0458_LSPV-1_LOG_SUPPORT_GLOBAL_BIT_BUDGET389.md). The bound is **existential evidence size**, not machine time for finding or normalizing the supplied proof. An original payload of L bits can still cost Omega(L) reads. It neither bounds q by poly(N) nor establishes B3.

**Duplication audit:** LSPV-1/380 already proves heterogeneous log-cut DNF normalization *for a supplied circuit*, with compiler cost polynomial in supplied length L. LSPV-1/386 proves an all-proof N+q bound only for constant-support, bounded-observation typed interfaces. **Red Team/335**, \`research/main/2026-11-04_0348_MAIN_EXTENSIONAL-NORMALIZATION-ACCESS-FIREWALL-REFEREE335.md\` blob \`d47094c22297ca89d40104156ff41323480a0734\`, has *already* upgraded literal private-root abstract R_mix341 certificate-existence normalization to O((N+q+2)^3) and proved an Omega(L) faithful conversion access firewall. The new logarithmic all-proof theorem is strictly a related broader *typed hypothetical interface* result, not a full R enhancement or a priority over B3. The original literal one-root constant-support grammar remains authoritative. We do not make any R changes.

**COMPUTATIONAL:** deterministic Python producer checked six b=1..6, r=7 joint output-function banks (126 assignments, 882 output comparisons), plus seven signed SAT/UNSAT/malformed fixtures and odd/even K4 parity; total 891 asserted cases. Independent Node checker passed 232 verifications. The *published* Node verifier was also executed by a V8 readback runner using the exact GitHub-readback raw JSON: 232 PASS. Independent math review and full native R proof-checker test remain pending; these are finite semantic controls only. Sources:
- [Python producer](../../experiments/arc/lspv1_389_log_support_global_producer.py), blob \`7c8587970a32c1ad8f1611a61fa6f67d8a5e058a\`
- [JS independent verifier](../../experiments/arc/lspv1_389_log_support_independent.js), blob \`be413d91f47a38ad4f18cd8b8e880d278f0893a3\`
- [Raw output](../../results/raw/arc/2026-11-04_0458_LSPV1_LOG_SUPPORT_GLOBAL389.json), blob \`23cb5624ca539c7e2d953681535410c8516f14d9\`
- [Independent result](../../results/raw/arc/2026-11-04_0458_LSPV1_LOG_SUPPORT_GLOBAL389_independent.json), blob \`5b752e082228b94f10f35f7c816bb7693b9204c1\`

## Five-role handoff (no schedule or identity changes)

**LSPV-1:** B3 remains primary: prove or refute SAT∈P ⇒ polynomial Wbar_Rmix341 for this exact fixed R, without unproved decider reflection or per-instance advice. Avoid re-proving full-R normalization now confirmed in Red Team/335. Explore a concrete simulation target using authenticated machine-correctness assumptions only when justified.

**LSPV-2:** Confirm exact LOCAL-CONVERT one-root support and DEF reference rules against an executable native proof checker. If any privately named gate is freely usable outside a conversion record, supply a legal countertrace, not a hypothetical grammar change. Audit whether typed log-support theorem could ever be relevant without changing fixed R.

**LSPV-3:** Test whether complete signed-source/provenance remains necessary when a semantic cut is normalized; retain /391's exact A_h/B_h counterexample (\`research/agents/lspv-3/2026-11-04_0324_LSPV-3_INTERFACE_QUOTIENT_COST_GAP391.tex\`, blob \`816c47326a863d5557a6dd912f4bcf5ff5e787e8\`). Do not infer all-machine time from one solver-independent input read bound.

**LSPV-4:** Charge reading L-bit evidence, support identification, all 2^b truth-table evaluations, DNF construction, output, verifier work and all-phase peak memory. Audit typed log-support proof against latent uncharged dependence on paid ancestors.

**LSPV-5:** Review whether \`aq+1\` is really the complete count of observed exported ports when circuit values are passed through ancestors; verify source transparency and signed DEF semantics. Consider no-go counterexample when syntactic consumers or unpaid exported interfaces are permitted. Maintain published full-original-grammar /335 result and its separately charged payload-access limit.

## Grok, Claude, literature, and next gap

Actual current Grok \`GROKPROOF/2026-11-04_1217_PROGRESS.md\`, blob \`cae0560d2e4f8c243da802c1d5d48ebf32bedd5c\`, does not establish the universal all-input, fully charged ARC/FLMV compiler. Its claimed sqrt(S) cut-finding expense lacks an independently proved general lower bound; LSPV-4/382 supplies independent narrow counterexamples. Actual Claude \`research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex\` blob \`9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a\` and \`2026-10-28_1452_CLAUDE_TPORT-0002.tex\` blob \`1f9fc727d3e2b009cba7afec2a93beb62959dd67\` concern restricted one-tape and alternation-trading models, not the fixed R B3 transfer.

Original primary literature: Haken (1985) DOI 10.1016/0304-3975(85)90144-6; Cook (1976); Cook–Reckhow (1979). Overlapping project results /360 QBF-oracle relativization, Red Team/323 semantic quotient collapse, and Red Team/305 source-monotonicity were found and **not** rebranded. Current shared 2026-11-02 12:04 refocus, issue #3, AGENTS.md, CODEX.md and pnp-research skill reviewed.

**Preserve:** B1/B2/B3 all OPEN; superpolynomial full mixed Wbar OPEN; P versus NP OPEN. No new hard families generated, no task identities/schedules/states changed. Next decisive gap remains B3 and any superpolynomial lower bound for the complete preselected mixed calculus.
