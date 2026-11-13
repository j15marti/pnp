# LSPV-3/621: Independent unchanged-original D1 qualification replay on a self-contained SAT source

**November 13, 2026, 12:24 PST | LSPV-3 Hypergraph & Proof Certificates | historical Route B | COMPUTATIONAL independent original-body replay and source enumeration; P versus NP OPEN.**

**Proof IDs:** Recovered \`/341\` candidate for [P2-D1] is **FAIL for semantically sound UNSAT verification on its full accepted operational language**; recovered \`/386\` is source-domain **RESTRICTED** and cannot be promoted to the complete mixed calculus. Actual historical full \`R_mix341\` [P2-D1] is **OPEN/NOT QUALIFIED**; [P2-C3] and [P2-B1] OPEN; independent [P2-B2/B3] OPEN. No new calculus, rule weight, schedule, role, or transfer is proposed.

## Candidate, exact falsifiers, and prior-art boundary

The candidate tested before repository searches was that the **unchanged historical /341 original checker** accepts a **single self-contained certificate** of a literal SAT source, including its built-in hostile self-tests. The simultaneous controls test that the unchanged /386 original checker admits its odd K4 SOURCE/DEF/RES certificate but does not accept genuinely mixed LOCAL-CONVERT or AND3 record kinds.

F1: the frozen /341 body rejects the complete one-fixture /557 packet, or the packet differs from its pinned original Git blob.

F2: the original 48 signed CNF clauses have zero models, the published model fails, or the external independently pinned DIMACS order differs from the packet's signed SOURCE order.

F3: changing the malformed charge \`"1"\` to numeric \`1\`, changing \`support:"012"\` to the correctly typed \`[0,1,12]\`, or altering the in-band source leaves the same complete packet accepted.

F4: the /386 body accepts a real LOCAL-CONVERT or AND3 record; a separately attached SAT-source/assumption sidecar is actually interpreted and bound by either checker.

**Results:** All four falsifiers are contradicted in their testable restricted cases. F4 is a negative result **only about the two named archived checkers**, not about any unidentified historical dispatcher. No complete original mixed-rule authority was recovered.

**Prior work not newly claimed:** LSPV-3/551 first exhibited a SAT-source false acceptance in a two-fixture /341 packet. LSPV-3/557 published the self-contained, one-fixture SAT packet used here and an original-body hosted replay. LSPV-3/553 classified the exact source models; LSPV-3/615 and /620 separated hash-binding from entailment; LSPV-1/624 found the unique first false affine base row. This run supplies **fresh independent unchanged-body replay of the already published one-fixture certificate, fresh signed-source cross-authentication and twelve differential original-body controls**. It is not a newly discovered flaw or a proof-complexity theorem.

## Immutable source and operation authority

| Independently fetched GitHub file | Git blob SHA-1 |
|---|---|
| \`experiments/arc/lspv2_341_independent_verify.js\` | \`fcb7d4ced8f922de14c0bda16263a8cc7853e8e0\` |
| \`results/raw/arc/2026-11-10_1724_LSPV3_557_SINGLE_SAT_PACKET.json\` | \`6cf9b0fe1e5a9419e8967d836c707c385418b810\` |
| \`results/raw/arc/2026-11-13_1128_LSPV3_620_ACCEPTED_341_SAT_SOURCE.cnf\` | \`c6f8bbf09baf6547de6fea04ac74dd0ecb32f6bd\` |
| \`experiments/arc/lspv2_386_independent_verify.js\` | \`338305c0ce101704205e57543756b8127074a986\` |
| \`results/raw/arc/2026-11-11_0407_LSPV2_555_ACCEPTED_LIVE_DEF_RES_K1.json\` | \`aeeb555c4dcf7f510a9a501c8afc609b629a9298\` |

The /341 code dispatches SOURCE records, \`AND3\` and \`XOR\`, with no RES/DEF/LOCAL-CONVERT dispatcher. The /386 code dispatches \`SOURCE\`, free \`DEF\` facet views and chronological strict \`RES\`, with once-paid globally declared gate owners. It requires a cubic odd-charge graph, guard, complete source ledger and an empty final RES clause. /386 charges \`W=RES+gate_defs\`, and its accepted K4 example has \`W=30+3=33\`. Neither program takes a separately authenticated external original CNF as an input argument. The complete mixed \`R_mix341\` spelling, parent cross-types, assumptions, discharge, private/exported ports and full family coverage remain **UNKNOWN/MAY**, not forbidden under the hypothetical full system.

## Fresh independent executable-body results

Verbatim checker JS was fetched by the linked GitHub connector and evaluated by V8 \`new Function\`. The only adapters supplied \`require(fs)\`, \`process.argv\`, and \`console.log\`; /386 also required a JSON-deep-clone adapter for its built-in hostile tests and a **diagnostic-output-only** hash stub. Neither mathematical checker body was edited or independently reimplemented. **This is original-code execution in hosted V8, not a Node operating-system subprocess.**

The original /557 packet has **one** 12-vertex, 18-variable SAT-source fixture, **48 signed original strict-3CNF SOURCE clauses**, **47 paid AND3/XOR nodes**, a syntactically terminal \`0=1\` affine row, and **8,574 original UTF-8 file bytes including trailing newline** (8,573 compact JSON bytes). It contains malformed native charge String \`"1"\`, malformed node-50 support String \`"012"\`, and one genuine source-deletion witness for source 0. The frozen /341 program's entire built-in negative harness ran and accepted the packet with **3,273 assertion groups**.

The independently fetched source DIMACS reproduces the original 48 signed literal arrays in their exact order. Exhaustive Boolean enumeration of all \`2^18=262,144\` assignments finds **64 models**. The explicit model \`101001000000100000\` satisfies all 48 clauses, while the all-zero assignment violates only SOURCE 0, making the packet's single non-null deletion witness legitimate. Source-hash identity and literal SAT checking are distinct from native verifier acceptance.

| Experiment on unchanged checker | Expected | Fresh observed |
|---|---|---|
| /341 published single SAT packet | ACCEPT | ACCEPT, 3,273 assertions |
| /341 replace String charge with numeric 1 | REJECT | \`source forbidden pattern parity\` |
| /341 change \`support:"012"\` to \`[0,1,12]\` | REJECT | \`invalid affine alias\` |
| /341 mutate original signed SOURCE literal | REJECT | \`signed incidence mismatch\` |
| /341 corrupt terminal row RHS | REJECT | \`bad GF2 elimination\` |
| /341 append unrecognized external SAT-source sidecar | ACCEPT | ACCEPT, same 3,273 assertions |
| /341 append unrecognized context/assumption sidecar | ACCEPT | ACCEPT, same 3,273 assertions |
| /386 original guarded odd K4 | ACCEPT | ACCEPT, 3,509 assertions, W=33 |
| /386 change charge parity to even | REJECT | \`not odd\` |
| /386 change record kind to LOCAL-CONVERT | REJECT | \`record kind or clause at 21\` |
| /386 change record kind to AND3 | REJECT | \`record kind or clause at 21\` |
| /386 append external SAT-source/context sidecar | ACCEPT | ACCEPT, same 3,509 assertions, W=33 |

**All 12/12 expected original-checker outcomes occurred: 5 ACCEPT and 7 REJECT.** The added metadata has no historic binding semantics; its acceptance shows absence of external binding, not a valid context/discharge operation. The accepted SAT source was an actual in-band source of the /341 proof, not a substituted sidecar. The /386 actual in-band guarded odd K4 source is UNSAT; its extra SAT sidecar is untrusted and ignored, so this does **not** demonstrate that /386's strict RES inference rules are unsound.

## Exact failure mechanism and the four noninterchangeable claims

The /341 source charge String \`"1"\` contributes numeric one under JavaScript XOR but evades a strict comparison to numeric forbidden-pattern parity. The selected SOURCE quartet at vertex zero enforces \`x_1 XOR x_2 = 1\`, leaving edge \`x_13\` locally unrestrained. The eleven other even vertex equations imply \`x_1 XOR x_2 XOR x_13 = 0\` in every original-source model. The /341 verifier accepts a row with mask \`0x1003\`, RHS \`1\`, because String \`"012".includes(12)\` tests a substring, whereas indexed table evaluation uses characters 0,1,2 rather than edges 0,1,12. The accepted native row is false on all 64 source models. This mechanism and uniqueness of the first bad row were proved already by LSPV-1/624; the new replay checks its two exact causal native type repairs.

1. **Parser acceptance:** YES for the frozen /341 one-fixture packet.
2. **Checker acceptance:** YES, 3,273 native assertions passed in this fresh V8 execution.
3. **Entailment from original signed CNF:** **NO** for the claimed affine row; 64 source models exist.
4. **Closed logical refutation of original input:** **NO**, notwithstanding a syntactically accepted terminal \`0=1\`. Its false premise makes it an invalid UNSAT derivation.

**Scoped qualification theorem:** For this exact \`V_341\` and one-fixture packet \`P\`, \`V_341(P)=ACCEPT\` but the signed original source \`F(P)\` has 64 satisfying assignments. Consequently \`V_341\` is not a sound UNSAT proof predicate on the entirety of its original accepted-byte language, and no completed-goal-preserving sound abstraction can identify all \`V_341\` accepts with semantically correct UNSAT proofs. This follows immediately from the accepted SAT counterexample; the theorem and its two constituent facts are previously established, now independently replayed. **It does not classify the still-unrecovered full historical \`R_mix341\` authority.**

In CEGAR the path must be retained as an actual accepted operational execution. If the abstract goal is *semantic* UNSAT, this path is a counterexample to the underlying candidate system's soundness, not a spurious path removed by refinement. A separately revised checker might reject it, but is a **new** calculus and cannot silently inherit R_mix341's authority or tariffs.

## Work, evidence, and the independent transfer gate

This /341 certificate reports 47 distinct paid inference nodes, count once over the complete shared proof DAG; it does not establish shortest proof cost or even a valid logical proof. The /386 control reports W=33, including three once-paid gate declarations and 30 paid RES. The 8,574 serialized bytes and V8 checker-assertion counts are evidence/probe metrics, **not** ideal logical work, discovery cost, proof verification time, span, peak memory, or FLMV machine bounds. Full original-checker OS subprocess timings and native memory usage were not measured.

Gate T [P2-B2/B3] remains independently OPEN. A sufficient conditional target is SAT in P implies polynomial \`Wbar_R(F_n)\` on the exact same explicit hard family and the same qualified proof system. A universal same-R compiler from every correct deterministic SAT decider is stronger, not assumed. LSPV-2/604 compiles one DPLL conflict tree to a restricted /386 SOURCE+RES core and does **not** translate arbitrary faster algorithms; the original CLI's built-in hostile tests add a separate acceptance caveat. A rejecting computation in a different model is not a source-bound proof of UNSAT here. Missing accepted proofs do not constitute proof-size lower bounds.

Neither a strict quasipolynomial \`N^((log N)^c)\` upper bound nor a fixed superlinear lower bound resolves P versus NP without the required quantifiers and transfer. A strict quasipolynomial growth function with fixed c>0 is already superpolynomial, but proving an upper bound of that form establishes no superpolynomial *lower* bound.

## Corpus, references, and reproducibility

Read both root trackers: \`proof1.txt\` blob \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`, full \`proof2.txt\` blob \`930c5eeddafce656717f28055a7a9a755f44737c\` via Git blob (1,051,196 characters; contents API returned empty). Read issue #3 including recent /620 and LSPV-1/624 comments, \`AGENTS.md\`, \`CODEX.md\`, the project skill, November 13 two-gate user handoff and LSPV-1 total-progress review, original /341 and /386 executables, prior /557, /620, /624, LSPV-2/539 and /547 reference-rule warnings, LSPV-2/604 and LSPV-4/591 transfer controls, and current Grok 2026-11-13 05:26 note. Revisited original relevant 539-549 corpus through repository search; no source-authenticated unified mixed-rule checker was found. This is **not** a full exhaustive peer/Grok/Claude corpus reexecution.

Primary references consulted: Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, *J. Symbolic Logic* 44 (1979), 36-50, DOI [10.2307/2273702](https://doi.org/10.2307/2273702), which requires proof-system soundness; Cousot and Cousot, *Abstract Interpretation*, POPL (1977), DOI [10.1145/512950.512973](https://doi.org/10.1145/512950.512973), which motivates concrete-step soundness; Clarke et al., *Counterexample-guided Abstraction Refinement*, CAV (2000), DOI [10.1007/10722167_15](https://doi.org/10.1007/10722167_15), which distinguishes spurious abstraction traces from real executions. None authenticates the absent historical mixed checker.

**Published code:** \`experiments/arc/lspv3_621_independent_native_os_gate_replay.cjs\` (verbatim archived original checker in a fresh OS Node subprocess for each test when run in a repository checkout; syntactically parsed in hosted V8, **not executed as an OS program during this run**). **Fresh raw result ledger:** \`results/raw/arc/2026-11-13_1224_LSPV3_621_NATIVE_DUAL_GATE_FRESH_V8_RAW.json\`. OS Node original-checker replay was not possible in this runtime because the container cannot resolve github.com to obtain a local checkout. Connected V8 did execute both exact checker bodies as specified. Repository-wide preflight, Node OS execution, full LaTeX compilation, and actual machine-time/peak-space measurement remain **NOT RUN**.

**Research disposition:** recover one demonstrably different, immutable, source-hashed *historical* mixed authority with actual accepted RES-to-AND3 and DEF-facet-to-LOCAL-CONVERT records, source-bounded both-label coverage, and explicit context discharge; or keep the historical full D1 unqualified. Do not promote /341, /386, REF547, or CANON as substitutes. Coordinate independently executed OS replays with LSPV-5, rule interfaces with LSPV-2, paid tariff with LSPV-4 and full-chain theorem quantifiers with LSPV-1.

**TRACKERS REVIEWED; NO MATERIAL CHANGE** to proof1.txt or proof2.txt. Root \`main.tex\` must retain the P2-D1 qualification FAIL for the recovered /341 sibling and OPEN for the unidentified full mixed authority. Only an LSPV-3-owned, status-preserving literature/evidence insert is authorized. P versus NP remains **OPEN**.

END_OF_REPORT::LSPV-3::621::2026-11-13_1224
