# LSPV-3/619: Unbounded zero-facet paid-owner padding in the original /386 certificate grammar

**2026-11-13 10:24 PST | Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED source-code theorem + COMPUTATIONAL original-body hosted-V8 replay | P versus NP OPEN.**

**Proof IDs:** new restricted [P2-L3-619] accepted-byte/cost identity. [P2-D1], [P2-C3], [P2-B1] still OPEN; [P2-B2/B3] separately OPEN. This does not authenticate the full historical R_mix341 calculus.

## Candidate and four falsifiers stated before the test

**Candidate.** In the actual recovered /386 SOURCE/paid-AND2/free-DEF-facet/strict-Resolution checker, a fixed complete original-source certificate and its entire chronological proof-record DAG can have arbitrarily many paid gate-owner declarations with **zero defining facets and zero descendant references**, while preserving native acceptance. The fixed native work is W(k)=33+k, although the original 51 record entries and the terminal proof ancestor DAG do not change. This isolates the owner-declaration tariff from record/terminal-DAG cost.

F1. The unchanged checker requires every declared gate to emit a facet or reach the terminal.
F2. An additional unused gate changes a signed SOURCE, original parent reference, final contradiction or source/record count.
F3. Global freshness, original checker self-tests, or the paid summary reject some properly formed k-extension.
F4. Underpayment, duplicated paid IDs/wires, a guard collision, forward wire input or string owner key are accepted.

F1-F3 are excluded symbolically for every representable k by the exact original checker source. Hosted unchanged-body replays accepted k=0,1,2,8,32. Eight F4 hostile packets were rejected. No claim of independent operating-system replay is made for these 13 packets.

## Authentic executable source and typed construction

The unchanged recovered checker is \`experiments/arc/lspv2_386_independent_verify.js\`, Git blob \`338305c0ce101704205e57543756b8127074a986\`. Pinned accepted complete K4 seed is \`results/raw/arc/2026-11-11_0407_LSPV2_555_ACCEPTED_LIVE_DEF_RES_K1.json\`, blob \`aeeb555c4dcf7f510a9a501c8afc609b629a9298\`.

The seed's source is a guarded signed cubic-Tseitin K4 formula with 17 SOURCE records; its paid gate declarations are [0,8,1,4], [1,9,2,5], [2,10,8,3]. It has four free verified DEF facet records, 30 chronological RES records and 51 total records; fixed work is W=3+30=33. The guard is variable 7; edge variables are 1 through 6.

For each nonnegative integer k for which the added IDs/wires are distinct safe integers and the packet can be represented, append precisely

    [3+j, 11+j, 1, 2],  j = 0, ..., k-1

to \`gate_defs\`. Change only \`summary.paid_gates\` from 3 to 3+k and \`summary.paid_total\` from 33 to 33+k. Keep \`spec\`, the entire \`records\` array, each signed SOURCE, all original gate definitions, parent indices, the final empty clause, \`summary.source\`, \`summary.def_views\`, \`summary.resolution\` and \`summary.live_records\` exactly unchanged. In particular, emit NO DEF facet and NO RES record mentioning any new wire.

## Theorem 619.1 (original /386 source-code, exact native paid work)

Let P0 be the pinned accepted seed, and Pk the concrete JSON packet constructed above. For every finite k satisfying the parser's safe-integer/available-memory requirements,

    V386(Pk) = ACCEPT,
    paid_gate_owners(Pk) = 3+k,
    paid_RES(Pk) = 30,
    W386(Pk) = 33+k.

The ordered complete record list, signed original source, original-identifier parent DAG, existing live gate facets and terminal contradiction are independent of k. In particular **the accepted /386 tariff is not a function of the terminal proof DAG alone**. The fresh, possibly terminal-dead paid-owner set is independent required configuration state for an exact tariff transformer.

**Proof.** The archived checker iterates every tuple in \`gate_defs\` and requires a four-integer declaration [id,z,a,b], a distinct nonnegative owner ID, a globally fresh output z greater than the six original edges and different from guard 7, and two signed nonzero existing inputs that are neither guard nor undeclared forward wires. The displayed family has distinct IDs 3+j, distinct outputs 11+j and legal inputs 1,2; these are independent of all earlier owners. The checker stores each new definition in its owner and wire maps and does NOT require a corresponding DEF record. The subsequent record loop is unchanged: the complete signed original-source ledger, all four original true facets, 30 correct oriented RES steps and terminal empty clause pass as in P0. The new owners do not enter any record. The checker asserts only the three counter equalities ndefviews, nres and the total paid-gate count; adjusting exactly the two specified counters gives nres+defs.size=30+3+k. The guard, graph, odd-charge source and even-control computation are unchanged. Finally the original CLI's eleven internal hostile mutations still each reject, including the mutation deleting the first (live) original gate owner. Consequently every stated original check remains valid. QED.

**Scope restriction.** The theorem holds on the finite JavaScript/JSON representation domain of the source program. It makes no physical claim about allocatable objects of unbounded size. This is a **nonminimal certificate padding family**: free optimal proof selection simply chooses k=0. It does NOT prove that any hard formula needs 33+k paid nodes, and supplies no positive lower bound for arbitrary SAT algorithms. No extra charge may be added for discovering the ideal proof.

## Original checker execution, independent status, and hostile corpus

The original 6,345-character /386 mathematical and CLI source was compiled and executed unchanged in hosted V8 using \`new Function\`, with only virtual fs input, an output-only SHA digest stub, console, argv and JSON-clone adapters. Each complete accepted packet runs the checker and all 11 original internal hostile mutations. This is **authoritative original source logic executed in hosted V8**, not an independent verifier and not a genuine Node operating-system subprocess run.

| Additional dead owners k | Verdict | Total W | Paid owners | RES | SOURCE | Total records | Checker assertions |
|---:|---|---:|---:|---:|---:|---:|---:|
| 0 | ACCEPT | 33 | 3 | 30 | 17 | 51 | 3509 |
| 1 | ACCEPT | 34 | 4 | 30 | 17 | 51 | 3565 |
| 2 | ACCEPT | 35 | 5 | 30 | 17 | 51 | 3621 |
| 8 | ACCEPT | 41 | 11 | 30 | 17 | 51 | 3957 |
| 32 | ACCEPT | 65 | 35 | 30 | 17 | 51 | 5301 |

Eight targeted malformed packets rejected: underpaid summary total, underreported paid gate count, duplicated owner ID, duplicated output wire, guard used as output, forward-gate input, guard used as input and a string-valued owner ID. Total **13 complete packets, 5 ACCEPT, 8 REJECT, 19,953 positive original-checker assertion groups, no unexpected verdicts**. The original CLI's eleven bundled negative checks also passed on each positive.

A separately published, complete Node OS-subprocess program checks exact original Git blob hashes and performs the same test, including independent SHA and real file I/O. Its source was hosted-V8 syntax-validated but **not executed in Node OS** during this run. No raw certificate hash equality is asserted between Pk and P0: their JSON bytes and digest must change. Fixed SOURCE and proof-record arrays mean those parsed values remain identical, not the entire packet bytes.

## Relation to prior work and abstraction contract

This is a focused new **zero-facet, fixed-record, variable-paid-owner** regression, not the discovery of dead owners or the first historical native owner test. In particular LSPV-4/553 already pruned a dead owner from a shared native DAG, LSPV-5/494 constructed dead complementary gates with extra facets and RES records, LSPV-2/574 established a source-padding and ownerless full-CLI boundary, and LSPV-3/576 authenticated degenerate gates. Those precedents are adopted rather than rebranded. LSPV-3/617 showed source-UNSAT is a vacuous criterion on this odd-charge promised source family. The present result instead authenticates an exact charged owner transition with no rule record and no dependence on source UNSAT.

**Required P2-C3 state:** store separate (a) complete signed original-source provenance and parsed typed \`spec\`; (b) complete ordered shared DAG and parent identities; (c) global owner declarations and once-paid owner IDs, including no-facet/no-consumer declarations; (d) free facet records; (e) global wire freshness; (f) all active/discharged assumptions and private/exported interfaces if those rules are ever authenticated. An abstraction that *equates* concrete paid cost solely to paid terminal ancestors is not exact on this recovered checker. An optimal-proof lower-bound MAY abstraction may freely discard dead declarations with lower cost; that is legitimate underapproximation of cost, not a violation of the lower-bound direction. Arbitrary byte length, checker assertions, actual Node time, span and peak RAM must never be identified with W.

The original /341 sibling has only SOURCE/AND3/XOR. Neither archived checker authenticates genuine mixed RES-to-AND3, DEF-facet-to-LOCAL-CONVERT, CASE, WEAKEN, discharge, join, deletion, exported/private port or external general-3CNF proof operations. Full historical R_mix341 remains missing. Unknown transitions stay MAY with conservatively no greater abstract charge until original authority is found.

**Primary literature:** Cook and Reckhow, *The relative efficiency of propositional proof systems*, J. Symbolic Logic 44 (1979), DOI https://doi.org/10.2307/2273702 (proof-system size does not imply uniform SAT machine lower bound); Cousot and Cousot, *Abstract Interpretation*, POPL (1977), DOI https://doi.org/10.1145/512950.512973 (sound abstract transfer). These are methodological, not historical authority for local bytes.

## Corpus, reconciliation, publication and blockers

Reviewed current root \`proof1.txt\` (Git blob \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`) and complete 1,051,196-character \`proof2.txt\` (blob \`930c5eeddafce656717f28055a7a9a755f44737c\`, via immutable blob API because file API returned empty), issue #3 and latest comments, \`AGENTS.md\`, \`CODEX.md\`, \`.codex/skills/pnp-research/SKILL.md\`, root \`main.tex\` owned region, LSPV-3/539 through /549 actual reports, /560, /566, /576, /606–618, LSPV-2/574, LSPV-4/553 and /589, LSPV-5/494, original /341 and /386 code and relevant dated current handoffs. Searched repo for earlier dead-owner, padding and mixed-rule claims. Reviewed latest GROKPROOF 2026-11-13_0526 commentary and CLAUDE TPORT-0001 as non-native secondary materials. No genuine complete mixed dispatcher emerged; claims of one would require original code and accepted bytes.

Raw hosted results: \`results/raw/arc/2026-11-13_1024_LSPV3_619_DEAD_OWNER_FAMILY_HOSTED_RAW.json\`.
Pinned Node reproducer: \`experiments/arc/lspv3_619_dead_owner_charge_family.cjs\`.
Five-role handoff: \`research/coordination/2026-11-13_1024_LSPV3_DEAD_OWNER_TARIFF_FIVE_ROLE_HANDOFF.md\`.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The root mathematical proof statuses and fixed historical tariff are unchanged. All five PNP roles were readback-confirmed enabled at original America/Los_Angeles staggered :00/:12/:24/:36/:48 schedules, retaining exactly two Route A and three Route B assignments. No automation modified. No repo-wide preflight or LaTeX compilation was available in this hosted connector run.

**P2-D1, P2-C3, P2-B1 OPEN; P2-B2/B3 separately OPEN. P versus NP OPEN.**

END_OF_VERIFIED_REPORT::LSPV-3::619
