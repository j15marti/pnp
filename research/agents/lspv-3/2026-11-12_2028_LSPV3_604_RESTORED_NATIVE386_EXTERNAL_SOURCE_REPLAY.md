# LSPV-3/604: Restored byte-exact external signed SOURCE for archived /386 checker

**2026-11-12 20:28 PST | Hypergraph & Proof Certificates | historical Route B | VERIFIED REPAIR + COMPUTATIONAL ORIGINAL-CHECKER REPLAY | P versus NP OPEN**

## Load-bearing target, four falsifiers and outcome

**Candidate [P2-L3-604].** Recover the previously missing *actual repository file* \`results/raw/arc/574_k01_SIGNED_SOURCE.cnf\` without modifying a single old certificate or verifier, by byte-identical restoration from the already published \`2026-11-12_1412_LSPV2_583_SIGNED_K4_SOURCE.cnf\`. This repairs a documented reproducibility blocker for archived native-/386 source-bound replayers. It is not a new grammar, mathematical proof rule, or acceptance claim for full R_mix341.

**F1:** recovered bytes differ from the previously declared SHA-256 \`3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c\`. **F2:** the 17 recovered signed DIMACS clauses differ in polarity, order, multiplicity or guard from the accepted W29 packet's 17 SOURCE records. **F3:** the original unchanged /386 checker rejects W29 or accepts a corrupted terminal pivot. **F4:** the recovered formula is SAT on any of its 128 complete seven-variable assignments. None occurred in the respective checks below. F3 was checked with the unchanged original mathematical/checker CLI *body* executed in hosted V8, not an OS Node subprocess; a complete independently runnable Node OS driver is newly published.

## Exact recovered source and authentication

| Item | Exact authoritative location | Git blob SHA |
|---|---|---|
| Restored signed source, 215 bytes | \`results/raw/arc/574_k01_SIGNED_SOURCE.cnf\` | \`e8bc4300f1f4518cb447edaf3f699bcee4839803\` |
| Previously published byte-identical source | \`results/raw/arc/2026-11-12_1412_LSPV2_583_SIGNED_K4_SOURCE.cnf\` | \`e8bc4300f1f4518cb447edaf3f699bcee4839803\` |
| Original W29 paid proof | \`results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json\` | \`318c52d99977ea4e91bc8554051138a700c1dc94\` |
| Archived original native checker | \`experiments/arc/lspv2_386_independent_verify.js\` | \`338305c0ce101704205e57543756b8127074a986\` |

Independent OS Python and \`sha256sum\`/Git blob verification of the 215 source bytes yielded exactly the previously pinned SHA-256 \`3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c\` and Git blob \`e8bc4300f1f4518cb447edaf3f699bcee4839803\`. GitHub \`create_file\` restored the **missing** expected path in commit \`955f955b63aa151aa0ff444d7444cddb92752475\`. Immediate fresh \`fetch_file\` returned identical entire content and the exact same 215-byte blob. No existing file was overwritten.

The document is exactly header \`p cnf 7 17\` followed by sixteen width-four signed clauses (each containing negative guard \`-7\`) and the unit \`7 0\`. The recovered 17 clause vectors agree **position by position**, not merely as an equisatisfiable or unordered substitute, with the W29 packet's signed SOURCE records. Each original occurrence remains distinguishable by original record index. The source is odd-charge K4 with charges (1,0,0,0): setting the guard true enforces four vertex parities whose XOR is inconsistent; setting it false contradicts the positive guard unit. Exhaustive independent Python enumeration of all 128 assignments found zero models. This validates this source instance, not the complete historical calculus.

## Unchanged original verifier and hostile replay

The original /386 JavaScript body was fetched by its Git blob and run in hosted V8; only \`fs.readFileSync\`, \`process.argv\`, \`structuredClone\` and the **unmeasured digest-output adapter** were supplied. The original checker accepted W29 with **3,542 original assertion groups**, **11 bundled original hostile controls**, **17 SOURCE**, **28 RES**, **one paid DEF/AND2 owner**, **45 records**, and paid logical work **W=29**. It reported zero odd-charge edge models, eight even-charge models and 64 guard-false edge assignments. A separately injected terminal \`pivot=999\` was rejected with \`Error: bad pivot signs 44\`. Cryptographic digest output from the hosted verifier was **not measured**; external source SHA-256 was measured independently in the operating-system container.

A fully specified original-Node **OS subprocess** reproducer has been published at \`experiments/arc/lspv3_604_restored_signed_source_replay.cjs\`. It checks four pinned SHA-256 values, source bytes against the old /583 copy, all 17 signed SOURCE records, exhaustive seven-variable classification, calls the unchanged original OS checker on the W29 packet and a hostile pivot mutation, checks the eleven original bundled negative tests and writes a complete raw JSON ledger. Its JavaScript source passed hosted-V8 syntax validation and exact GitHub readback. The independent OS subprocess path has **not** been executed during this run. Consequently this report does not claim a new OS replay verdict.

Machine-readable observed results: \`results/raw/arc/2026-11-12_2028_LSPV3_604_RESTORED_SOURCE_AUTH_REPLAY_RAW.json\`. The source itself is the required raw source artifact. Fixed proof tariff: 28 paid Resolution plus one paid gate, W29; separate raw source evidence 215 bytes. No measured concrete interpreter time, span, or peak memory is asserted.

## Scope, full-calculus semantics and CEGAR implications

This is a **verified repair of a missing named external SOURCE artifact** referenced by multiple existing original-/386 drivers, including LSPV-2/575, /576, /578, /579, /581, /584, /585 and /586. It unblocks their filesystem lookup and original-source hash gates in a complete checkout. It does **not** retroactively establish that every driver succeeds, since each still requires its own fresh execution and possibly additional absent artifacts.

The original /386 checker consumes the source embedded in its packet; the **independently signed DIMACS equality check is a separate replay condition**, not a claim that the historical original checker inherently binds to an external source hash. The two separate historical checkers still cannot be composed into a single accepted R_mix341 mixed proof (LSPV-2/549, LSPV-3/592, LSPV-5/516). All unknown original rules, including genuine Resolution-to-AND3, DEF-facet-to-LOCAL-CONVERT, fresh/exported/private wires, assumption discharge, reconvergence, joins and deletion, remain MAY transitions for a cost-sound abstraction. The concrete state must retain external signed-source commitment, per-source occurrences, globally once-paid event identities, whole DAG and contexts. Cost-soundness for P2-C3 and a full-rule P2-B1 lower bound are still unproved.

**CORPUS REVIEWED:** verified current \`proof1.txt\` blob \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`; \`proof2.txt\` blob \`f678f707880da4dfc97dabf778430c6dc816cb1f\` (full content retrieval returned zero characters; see blocker); issue #3 and its active instructions; AGENTS.md, CODEX.md, pnp-research skill; current LSPV-2/539 and /583-/587 native material, LSPV-3/539-/549 and /591-/603 reports, LSPV-5/516, Grok 2026-11-12 and Claude world-ledger/one-tape context, both original restricted checkers and source artifacts. Direct current main.tex \`fetch_file\` at blob \`bccd6d37a287d52f0095c92731a5008a35281ca2\` likewise returned **zero readable characters**, even with line ranges. Historical reports were used only as context, not as authority for newly claimed execution.

**DUPLICATION / CONTRADICTION AUDIT:** the guarded K4 bytes were already published in LSPV-2/583. This is **not a new SAT family or original native certificate**. The new, separately verified event is restoring the missing canonical \`574_k01_SIGNED_SOURCE.cnf\` path, thereby satisfying a preexisting source-file dependency. LSPV-5/516 independently flagged the missing file. Its correction of the separate LSPV-3/603 dual-escape runner-label defect is acknowledged; no duplicate correction is claimed here.

**WHAT CHANGED RELATIVE TO ROOT MAIN:** external source artifact reproducibility changed from missing to present; no new proof node closes. **ADOPTED:** exact prior W29 and native source pins; **REJECTED:** substituting a new grammar or treating verifier acceptance as unqualified proof soundness; **RETIRED:** none.

**TRACKERS REVIEWED; NO MATERIAL CHANGE** to the proof-chain statuses or original file contents. **Read-access qualification:** complete \`proof2.txt\` and \`main.tex\` could not be obtained by the available GitHub connector (current blob SHAs returned, no content). An optimistic-SHA whole-file rewrite or unauthorized partial edit was therefore unsafe. Root \`main.tex\` LSPV-3 ownership reconciliation is **BLOCKED AND UNPERFORMED**, explicitly handed off for a full-checkout merge. The repository-wide preflight, Node OS replay and LaTeX compile were not run. All five existing PNP roles were checked enabled at their original hourly Pacific :00/:12/:24/:36/:48 schedules, preserving two Route A (LSPV-2/4) and three Route B (LSPV-1/3/5); nothing was rescheduled, duplicated, or renamed.

**Affected IDs:** [P2-D1] OPEN (external /386 source artifact restored, full mixed grammar still missing); [P2-C3] OPEN; [P2-B1] OPEN; separate [P2-B2] and [P2-B3] OPEN; [P1-01], [P1-03], [P1-04] OPEN. **P versus NP OPEN.**

**Next decisive experiment:** Execute the new original-OS driver in a complete checkout, audit all formerly missing-source drivers against their pinned SHA, then continue searching for a *single authoritative historical* mixed dispatcher accepting an actual cross-rule parent inference. No inference about ideal minimum cost is permitted from unused ports or unsound source metadata.

## Primary references

- Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, Journal of Symbolic Logic **44** (1979), 36–50, https://doi.org/10.2307/2273702 .
- Cousot and Cousot, *Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs*, POPL (1977), https://doi.org/10.1145/512950.512973 .
- Original project pinned /386 and /341 implementations above. External proof-format grammars such as FRAT-XOR do not authenticate R_mix341.
