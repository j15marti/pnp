# LSPV-2/589: Fixed original SOURCE, alternative native-accepted refutation cones

**2026-11-12 20:35 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED theorem plus COMPUTATIONAL original-OS replay | P versus NP OPEN**

## Candidate, falsifiers, and novelty boundary

Candidate: three separately accepted original-/386 native byte certificates, with **identical complete original SOURCE, charge specification and once-paid owner bank**, select three different terminal-live component refutations, all W29. Extend to five odd K4 components. Distinguish mandatory SOURCE records, the common intersection of essential SOURCES, and a minimum UNSAT-source support.

F1: a transported signed source, pivot or RES edge is wrong. F2: all purported alternatives actually have the same terminal source ancestry. F3: all original sources are individually essential or no 17-source UNSAT core exists. F4: wrong signed SOURCE, wrong pivot, cross-component parent, underpayment, missing original SOURCE, or forged terminal is accepted. All falsifiers excluded in the declared exact experiments.

Prior work: LSPV-1/448 proved the abstract min-over-disjoint-odd-components theorem under separately declared semantic R_mix341. LSPV-3/569 accepted four parity-orbit SOURCE variants 100,010,001,111 under /386, but the 111 proof refuted only component zero. LSPV-2/574 and /587 proved native SOURCE padding/byte pivotality, and /588 gave terminal-live original-source RES projection. **This increment is fixed-input accepted-byte OR choice**, not the discovery of disjointness or a complexity lower bound.

Original unchanged restricted /386 checker: experiments/arc/lspv2_386_independent_verify.js, Git blob 338305c0ce101704205e57543756b8127074a986, SHA256 22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113. Pinned original accepted W29 seed: results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json, SHA256 0d8b1894f91d00c554727a92fed35b2bb58f2b1602f2a3cfcb949effda43ceb0. Independent signed original K4 source: results/raw/arc/574_k01_SIGNED_SOURCE.cnf, SHA256 3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c. The /386 original checker accepts only its restricted SOURCE/paid DEF/RES grammar and has self-test acceptance quirks. It is not the authoritative **full** historical R_mix341 dispatcher.

## Theorem 589.1: exactly k alternative minimal UNSAT SOURCE cores

For each odd integer k≥3, take k disjoint labeled K4 graphs, each with an odd parity charge on its first vertex and zero charge on its other vertices. Let g=6k+1 be one common guard. Put all sixteen signed parity-blocking clauses of every component into the SOURCE, adding -g to each clause, and also include unit [g]. There are exactly 16k+1 mandatory source occurrences. Declare one conservative paid owner z=6k+2 with operands (1,4), but leave the owner unused by the terminal RES DAG.

The **inclusion-minimal UNSAT subsets** of the fixed guarded SOURCE are exactly the k sets S_j consisting of the unit [g] and all sixteen guarded clauses of component j. Each S_j has 17 records; their union contains all 16k+1 mandatory original SOURCE records, whereas their intersection contains just [g]. Consequently no nonguard SOURCE clause is indispensable to the full formula, although all original SOURCE records are compulsory for acceptance by this checker.

Proof: If [g] is absent, g=false satisfies all guarded clauses. If [g] is present, g=true and components decouple into odd-parity K4 Tseitin formulas. Each component is UNSAT because XORing its four vertex equations yields 0=1. Each proper subcollection of its sixteen clauses is SAT, by the bridgeless cubic source-deletion lemma (independently verified over all 64 possible original K4 assignments for each deletion). Source subsets are UNSAT iff one whole component and [g] are included. This gives precisely the claimed inclusion-minimal sets. QED.

For every component j, transport the original 28-step W29 RES suffix by exact signed edge/guard renaming, parent index rebasing and pivot transport to the j-th component, keeping **every** SOURCE record, SOURCE order, in-band spec and owner bank identical across j. The unchanged full /386 CLI accepts each with 28 paid RES identities and one globally once-paid owner: W=29. The **terminal source cone** is exactly S_j. The construction proves an upper bound, not W29 optimality.

Under explicitly source-bound sound at-most-binary-premise paid inference and no free multi-source merger, write μ(F) for the minimum number of original SOURCE clauses in any UNSAT subset. The connected terminal-ancestry edge count implies q≥μ(F)-1. Here μ(F)=17 gives q≥16. Substituting all 16k+1 compulsory SOURCE records would incorrectly give q≥16k, contradicted by native-accepted W29 witnesses at k=3 and k=5. Substituting only the intersection of minimal UNSAT cores gives q≥0 and discards the valid restricted lower envelope. A cost-sound MAY abstraction must preserve legal **OR choices of original SOURCE cores**, with exact signed terminal ancestry, not force all recorded SOURCES into the terminal cone.

## Executed unchanged original-checker experiment

Native Node.js v22.16.0 original-OS replays tested k=3 and k=5, selecting each of their k components. Positive exact-byte results: **8/8 accepted**, with **59,000 original accepted assertion groups and 88 built-in original negative controls**. Six separately generated hostile packets were all **rejected**: forged SOURCE, incorrect signed pivot, a cross-component parent, an underpaid summary, deletion of a compulsory SOURCE record, and a forged terminal clause. Total **14/14 expected native verdicts**, deterministic, no randomness.

| Fixed original source | SOURCE rows | Accepted distinct cones | SOURCE ancestors in each | W |
|---|---:|---:|---:|---:|
| Three odd K4 components (111) | 49 | 3 | 17 | 29 |
| Five odd K4 components (11111) | 81 | 5 | 17 | 29 |

All three k=3 published exact accepted-byte packets retain the *identical* first 49 records. Their lengths including LF are respectively 4993, 5078, 5126 bytes, SHA-256:
1. 7a514e4dd20f8c77c84ef700ffd66af48e44bce6b1dba0105a2c1ac98772f9d4
2. 4a972f132d1045c8da01f75a827236e7d8737c127832a1151473d66037c571cf
3. 1effde5610a56b6f9981d70b64c02bbd9a4865e876b0de2b70cba1fae7ade205

An independently authored auxiliary Python signed-SOURCE and chronological RES auditor executed and passed **1,316 checks**, including complete original SOURCE clause reconstruction and 16 independent single-clause deletion controls. It is **not** the original checker. The full source-bound original replayer, separate original checker, exact independent signed source, all packets, comprehensive raw JSON and independent audit are archived in the companion ZIP; the GitHub compact raw ledger retains the exact accepted and rejected SHA-256 verdicts.

## Cost-sound abstraction and proof obligations

The full concrete state must retain the exact complete SOURCE and source digest, choice-dependent source ancestry, exact paid RES identities and owner bank, signed parents, chronological pivots and once-only fixed costs. A MAY abstraction should distinguish mandatory SOURCE set M, core intersection E, and an *existential legal complete-core selection*, not conflate them. An abstract refinement demanding every compulsory SOURCE be terminal-live is **falsified by genuine original-/386 accepted W29 packets**. Conversely an unsound cross-component parent is rejected and must be excluded by a proven signed-parent rule, not by silently suppressing unknown historical operations.

Logical paid work W=29, certificate bytes, source input size, construction time, dependency span, OS verification time and physical peak RAM are distinct resource axes. No physical RSS bound, native all-rule proof minimum, general SAT decision-time floor or B3 bridge is proved. The original checker has an unused paid owner requirement stemming from its own corruption tests, not a legitimate general fixed proof tariff. No historical single-checker RES-to-AND3 or DEF-to-LOCAL-CONVERT transition was acquired.

Evidence paths: report at this path; executable experiments/arc/lspv2_589_alternative_core_replay.cjs; compact 14-case results results/raw/arc/2026-11-12_2035_LSPV2_589_FIXED_SOURCE_OR_CORE_OS_RAW.json; exact packets results/raw/arc/589_k3_component0_complete_cli.json, component1_complete_cli.json, component2_complete_cli.json; five-role coordination handoff research/coordination/2026-11-12_2035_LSPV2_FIXED_SOURCE_OR_CORE_FIVE_ROLE_HANDOFF589.md.

Corpus review: BOTH root proof1.txt (blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343) and full proof2.txt (blob f678f707880da4dfc97dabf778430c6dc816cb1f, recovered via Git blob because normal contents API returned zero), root main.tex (blob bccd6d37a287d52f0095c92731a5008a35281ca2), issue #3 and recent peer comments; AGENTS.md, CODEX.md, repo pnp-research skill, latest handoffs, historical /341 declaration and /341 and /386 checker code; LSPV-2 /539–549 and /587–588, LSPV-1/448, LSPV-3/569 and /598, LSPV-5/516. Primary scholarship: Cook–Reckhow, JSL 1979, DOI 10.2307/2273702; Cousot–Cousot, POPL 1977, DOI 10.1145/512950.512973; Clarke et al., CAV 2000, DOI 10.1007/10722167_15. The distinct FRAT-XOR/XLRUP specification does not authenticate the missing historical grammar.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both proof trackers and root main.tex left unchanged. [P2-D1], full [P2-C3], [P2-B1], separate [P2-B2] and [P2-B3], [P1-01/03/04] and P versus NP remain **OPEN**. All five existing research roles, historical TWO Route A/THREE Route B labels, schedules, identities, weights and ownership boundaries preserved; no automation modified.

**Next target:** Acquire one authoritative original historical checker accepting a genuine externally source-bound RES-to-AND3 or paid DEF-to-LOCAL-CONVERT dependency, with rejected corrupted signed-port controls. Only then develop all-rule cost-sound alpha/gamma and test B1 and separate B3.
