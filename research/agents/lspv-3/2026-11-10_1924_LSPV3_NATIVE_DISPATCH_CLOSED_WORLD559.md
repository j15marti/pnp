# LSPV-3/559: closed-world audit of the recovered /341 inference dispatcher

**November 10, 2026, 19:24 PST | Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED code-property, COMPUTATIONAL 84-probe original-body replay | P versus NP OPEN**

## IDEA and falsifiers, before source search

**Candidate related to [P2-D1].** The recovered original /341 checker is a closed-world SOURCE/AND3/XOR *fixture* validator. It cannot be used to authenticate even one historical RES, paid DEF, LOCAL-CONVERT or explicit branch/discharge instruction, regardless of how a caller spells a JSON record. If this is true, searching for a mixed-rule accepted packet by only mutating inputs to this executable is a provably sterile research strategy; one must recover a separate authoritative mixed checker/specification or keep those transitions explicitly unknown.

Predeclared falsifiers: (F1) a paid RES opcode is accepted in the original checker; (F2) a paid DEF or LOCAL-CONVERT opcode is accepted; (F3) a branch/discharge opcode bypasses its dispatch; (F4) valid original AND3/XOR controls fail or wrong-kind records are silently reinterpreted as legal alternate rules.

**ITERATION.** Direct inspection found the exhaustive two-case dispatch. Exact original-body execution then rejected all F1-F3 probes and retained correct F4 acceptance/type controls. This is a scope-closure result on the available checker, not recovery of the missing grammar.

## Theorem 559.1: the available executable cannot authenticate five-rule proofs

Fix the historical specialized independent verifier, Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0, without modification. Let $V_{341}$ be its actual acceptance predicate on a JSON fixture packet. Every packet it accepts satisfies

$$
V_{341}(P)=\mathrm{accept}
\;\Longrightarrow\;
\forall p\in P.\mathrm{fixtures}[i].\mathrm{proof}:
\quad
p.\mathrm{rule}\in\{\mathrm{AND3},\mathrm{XOR}\}.
$$

**Proof (exact code inspection).** Its mandatory proof loop first checks the fixed $4V-1$ record count and iterates over every inference record. Its sole rule dispatch is an if branch for strict string equality with AND3, an else-if branch for strict equality with XOR, and a final unconditional throw with error text "unknown rule." A successful return cannot pass that throw. Consequently, no accepted packet processed by this executable contains a paid rule spelled RES, DEF, LOCAL-CONVERT, SPLIT_AND, or any other third opcode. This holds for every accepted packet, not only the tested cubic graphs. QED.

The theorem is about **the pinned executable**, not the accepted-byte grammar of the larger historical *mathematically declared* $R_{\mathrm{mix341}}$. That declaration additionally lists binary Resolution, LOCAL-CONVERT, and conservative unit-paid two-input DEF. Its full native byte syntax, DEF facet ownership and selectors, outputs, private/exported wires, branch contexts and discharge were not present in the executable and remain unauthenticated.

**Practical no-go.** Calling this executable as an oracle, no number of RES/DEF/LOCAL-CONVERT candidate byte packets can provide positive native acceptance. A separately written parser or a patched checker would define a distinct language until historical authority is independently established. Nor does rejection by this incomplete checker prove that the proposed mathematical inference is illegal.

## Executed original-code falsification matrix

Fetched and ran the original producer code (blob 4081022e8a3841d79f751a3d3a7a10decbb026da) and original checker body (blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0) in connected V8, with only command-line fs.readFileSync / console.log replaced by in-memory adapters. No original mathematical code was edited. All seven producer fixtures were jointly accepted in the baseline with **30,714 assertions**.

For each of the seven original graph fixtures K4, K3,3, Cube, Petersen, Prism6, Prism16 and bridged K4x2, mutate either the first legal AND3 inference or the last legal XOR inference to one of six opcodes: RES, DEF, LOCAL-CONVERT, SPLIT_AND, AND3 and XOR. Each mutation ran the **entire pinned checker**, retaining unchanged packet content other than the selected opcode.

| Outcome | Number of mutations |
|:--|--:|
| Valid opcode unchanged at a correctly typed position: accepted | 14 |
| RES / DEF / LOCAL-CONVERT / SPLIT_AND: exact unknown-rule rejection | 56 |
| Known opcode placed at the wrong node kind: type rejection | 14 |
| **Total** | **84** |

All 84 outcomes matched the code-derived prediction. There were no newly authenticated mixed-rule instances and no false promotion of a proposed grammar.

**Code:** experiments/arc/lspv3_559_native_dispatch_audit.cjs. The standalone script loads the two pinned original project files from a repository checkout and runs them unmodified through Node vm. It has passed a V8 syntax parse after stripping its Node shebang; the published script was **not independently run as an operating-system Node subprocess**. The exact test-matrix results above came from an equivalent execution of the original bodies in connected V8, not from an independent reimplementation. **Raw:** results/raw/arc/2026-11-10_1924_LSPV3_559_NATIVE_DISPATCH_MATRIX_RAW.json.

## Duplication and literature audit

This is **not an academically new theorem**. LSPV-5/413 had already identified the limited rule dispatcher; LSPV-1/553 and /559 and LSPV-3/542 stated the missing full-checker limitation. LSPV-3/556 showed byte-grammar underdetermination, and /558 established a separately bound source-canonical reconstruction only for the same existing SOURCE/AND3/XOR fragment. The new contribution is an exact, reproducible seven-graph by two-position by six-opcode original-body regression matrix, plus a decisive proof that this particular acceptance oracle cannot advance full native rule authentication.

Sources reviewed: original /341 mathematical declaration at research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex; original producer/checker; root proof1.txt and proof2.txt; issue #3; AGENTS.md, CODEX.md, research skill; relevant LSPV-1/558-560, LSPV-2/539-545, LSPV-3/536/542/551-558, LSPV-4/528-531, LSPV-5/412-416 and /463, Grok progress, Claude world ledger, latest five-role handoff. Change-aware source review: konard/p-vs-np scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5; meelgroup/frat-xor format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f. These are different proof systems, not missing native parser evidence.

Primary references: (1) Cook and Reckhow (1979), The Relative Efficiency of Propositional Proof Systems, JSL 44, 36–50, DOI 10.2307/2273702. (2) Cousot and Cousot (1977), Abstract Interpretation, POPL, DOI 10.1145/512950.512973. (3) Heule, Hunt, and Wetzler (2017), Efficient Certified RAT Verification, DOI 10.1007/978-3-319-63046-5_14. A certified LRAT/FRAT-XOR checker could independently validate **its own** grammar, never supply historical R_mix341 byte authority by fiat.

## Proof-chain decision and remaining work

**[P2-D1] OPEN:** only SOURCE/AND3/XOR executable acceptance is recovered. The source must be authenticated externally and prior reported malformed-type acceptance exploits remain genuine negative controls. **[P2-C3] OPEN:** no complete cost-sound concrete-to-abstract simulation of all five native rules. **[P2-B1] OPEN:** no superpolynomial all-rule minimum. **[P2-B2]/B3 OPEN:** no noncircular same-calculus decider-to-short-proof transfer. Root proof1 targets [P1-01], [P1-03], [P1-04] remain OPEN.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The dispatcher limitation was already recorded in the root tracker and multiple prior reports; the new regression matrix does not alter node status, weights or dependencies. No risky overwrite of the roughly 1MB root tracker or root main.tex was justified. Root manuscript requires no material LSPV-3 region change on this duplication-aware audit.

**Next decisive target:** archive-search original historical mixed-checker source, parser test suite, or a real accepted DEF-owner/defining-facet-to-RES certificate. If none exists, document its absence as a scientific infrastructure blocker instead of repeatedly proposing bytes or assuming a completion. No agent schedules, identities, roles, weights or Route A/B allocations were touched. P versus NP remains OPEN.
