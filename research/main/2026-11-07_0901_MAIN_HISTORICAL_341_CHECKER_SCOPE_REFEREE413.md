# REFEREE413 — Historical /341 chain recovered; checker authenticates only the exhibited source/AND3/XOR sublanguage

**2026-11-07 09:01 PST | LSPV-5 Independent Red Team | Route B primary | PROVED/EXACT provenance and checker-scope result; COMPUTATIONAL exact replay | P versus NP OPEN**

Affected tracker nodes: **[P2-D1]**, correction to **[P2-L5-412]**, and new evidence **[P2-L5-413]**. Related nodes **[P2-C3]**, **[P2-B1]**, **[P2-B2]** remain OPEN. Route-A nodes **[P1-01]**, **[P1-03]**, **[P1-04]** were reviewed and are unchanged.

## 1. IDEA: claim card and registered falsifiers

**Initial hypothesis.** The commit introducing the historical $R_{\mathrm{mix341}}$ report either contains or names the producer/checker that decides whether a RES-produced clause is a legal AND3 parent. If so, exact historical bytes should select between the EXTENSIONAL and TAGGED audit completions from [P2-L5-412].

**Exact quantifiers.** For the finite repository history of the five /341 commits and the four exact executable/data artifacts they introduce, determine every rule tag accepted by the historical independent verifier and whether an accepted trace can contain RES -> AND3.

**Model/resource.** Git commit/blob identity, exact UTF-8 bytes, Node v24.22.1 execution, and host-language verification. This is not a proof-search lower bound, not a native Turing-machine trace and not a new calculus.

**Falsifiers registered before SEARCH.**

1. No executable/data artifact exists in the report commit or adjacent /341 history.
2. The recovered verifier implements only the exhibited source/AND3/XOR fragment, not RES, LOCAL-CONVERT or DEF.
3. The recovered checker accepts RES but assigns a parent type incompatible with AND3.
4. Repository/API access is incomplete, so commit/file identity cannot be established.

The initial prediction was falsified by item 2 after item 1 was first supported for the report commit alone.

## 2. SEARCH: repository archaeology and primary controls

### 2.1 Exact historical chain

Path-scoped commit history and commit diffs recovered the complete sequence:

| Commit | Exact artifact | Git blob | Result |
|---|---|---|---|
| 'c3e8eb6aacb161a33996cf9076c80bf0f2c93df7' | 'experiments/arc/lspv2_341_mixed_tseitin_min_dag.js' | '4081022e8a3841d79f751a3d3a7a10decbb026da' | producer |
| 'a064552941d16c1c75bcd0d6aae599a49be15816' | 'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json' | 'fe27fe1011d0021e721ccaeb747ed58da65d7464' | proof/source packet |
| '45945352d8287da86dcb1ff25c6068faa8432718' | 'experiments/arc/lspv2_341_independent_verify.js' | 'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0' | independent verifier |
| '5d80c973c875faa4bed8251ba1d7d5ef2c6d960b' | 'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341_independent.json' | '42ba4cad6dc165aa9e96a29011df5602d33281b9' | verifier record |
| '2d1dd3a438033d2bf51a0dbdfd4a4665ffb129a7' | 'research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex' | 'c87acd3547fa90025dfaaea07b84794b7f79e651' | theorem/report |

The report-introducing commit itself changes only the 109-line TeX report. The four executable/data artifacts are in immediately preceding commits. The **current** governing handoff explicitly links all four artifacts; the historical handoff at user-specified commit '4e29ed7646f484707767acb6e63ec5f38afd98a8' predates those appended links. This corrects the false sentence “No official historical checker ran” in [P2-L5-412].

### 2.2 Continuity and peer reads

Read both complete trackers: 'proof1.txt' blob '96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b' and then-current 'proof2.txt' blob '144cf39923ae638d14cd87395df3cdc6a12638c4'. Read current issue #3 through comment '6710087313'; historical and current five-role handoff; 'AGENTS.md' blob '19656af102604d5f0a721d548cf2e4e72a063561'; 'CODEX.md' blob '754999f50de93cdb693ed37bc8110d31e9e698ef'; research instructions and references blobs 'b8df83a7...', 'c211e9f5...', '25b38dc0...'; LSPV-1/478, LSPV-1/479, and LSPV-3/476 actual reports; Grok 'GROKPROOF/2026-11-06_2316_PROGRESS.md' blob 'a20fb8b...'; Claude world-ledger README blob 'de75a371...' and report blob '79e4d4e7...'.

Peer relevance: [P2-B19], [P2-B20] give restricted ordinary-PC/Res(PC) transfer/lower-bound controls; [P2-L3-476] gives a source-only Resolution assumption retraction. None supplies the missing full historical mixed parser.

### 2.3 Required repositories and literature

Change-aware reads were unchanged from pinned versions:

- 'konard/p-vs-np': 'scripts/proof_status.json' blob '93b77ed3...'; 'proofs/complexity/README.md' blob '7ee9a11e...'. Its model-specific statements do not authenticate /341.
- 'blkph0x/p-vs-np-proof-research': 'METHOD_INDEX.md' blob '18d693ea...'; 'REVIEW_ADDENDUM.md' blob '6a7cc2f8...'. Claims remain scoped/unverified as recorded there.
- 'meelgroup/frat-xor/format.md' blob '986a21aa...'; 'tanyongkiam/cake_lpr/README.md' blob 'e94f45e9...'; 'peitl/short-proof/README.md' blob '93d2090d...'. These are distinct proof formats/checkers, not historical /341.
- 'openai/math/README.md' blob 'cc5b0a03...'; 'anthropics/formal-math/README.md' blob '1df53bfc...'. No native /341 artifact.

Primary-source search rechecked Cook–Reckhow (1979), Urquhart (1987), and Ben-Sasson–Wigderson (2001). Their proof-system and Resolution results do not decide this project-specific byte grammar. Public indexed search was available; there was no separately identified Google-branded interface, so no Google-specific execution is claimed.

## 3. ITERATE: exact replay and revised theorem

### Theorem 413.1 — exact historical /341 executable scope

For exact repository bytes at the blobs above:

1. Executing the producer yields a byte-for-byte identical 197,514-byte certificate packet.
2. Executing the independent verifier on that packet accepts and reproduces the 30,714-check historical record exactly.
3. The verifier's complete inference dispatch has exactly two tags: 'AND3' and 'XOR'; every other tag reaches 'throw Error("unknown rule")'.
4. It coerces each authenticated original clause to an internal 'factor'; 'AND3' requires 'factor × factor -> factor', and an optional affine alias is exhaustively checked against that factor. 'XOR' requires row-bearing parents and produces an 'affine' row.
5. Replacing the first exhibited 'AND3' tag independently by 'RES', 'LOCAL-CONVERT', or 'DEF' is rejected as 'unknown rule' in both Python- and Node-driven audits.

Therefore the recovered checker **authenticates the exhibited source/AND3/XOR Tseitin certificate sublanguage only**. It does **not** define accepted bytes for declared RES, LOCAL-CONVERT or DEF, and cannot decide whether a RES-produced clause is an AND3 parent. The TAGGED/EXTENSIONAL nonuniqueness from [P2-L5-412] still applies to the missing cross-rule composition, but the earlier claim that no historical checker was executed is false and is corrected here.

**Proof.** Items 1–2 are exact byte/output comparisons under recorded SHA-256 hashes. Items 3–4 follow by exhaustive inspection of the sole inference dispatch and its type guards. Item 5 is an actual hostile trace mutation through the exact verifier. No inference about unimplemented tags is made beyond the checker's explicit rejection.

### Independent challenge

Could an accepted 'AND3' parent smuggle a RES record using extra JSON fields? No: the dispatch key remains 'p.rule'; a 'RES' tag is rejected before insertion into the topological 'byId' map. Relabelling a semantic resolvent as 'AND3' would then have to satisfy the exact conjunction truth-table check, so it is not a native RES step. Conversely, absence of RES from this finite verifier does not delete RES from the declared prose calculus; it proves only that this checker is not the full mixed acceptance grammar.

## 4. Established-family ledger

| Family | Exact encoding/size | Established theorem/model | Known shortcut in /341 | Remaining transfer |
|---|---|---|---|---|
| Connected simple bridgeless cubic odd Tseitin $F_{G,\chi}$ | edge variable $x_e$; each degree-3 vertex contributes the four proper 3-clauses excluding wrong-parity local assignments; $n=3h/2$, $m=4h$, encoded length $\Theta(h\log h)$ under binary identifiers | suitable expander instances have exponential ordinary shared-DAG Resolution lower bounds (Urquhart; width route Ben-Sasson–Wigderson), restricted to Resolution | historical packet uses three AND3 nodes per vertex plus $h-1$ XOR nodes: $4h-1$; exact source/AND3/XOR packet replayed | authenticate all declared mixed tags and cross-rule views; a Resolution lower bound alone cannot lower-bound full mixed $W_R$ |
| Exact split strict-3CNF Tseitin controls [P2-B18]–[P2-B20] | 8h clauses, 11h/2 variables for the stated split; exact polarity variants separately tracked | restricted ordinary PC / Res(PC) degree-size results under stated field/degree assumptions | declared AND3/GF(2) reconstruction remains a linear mixed shortcut when legally available | prove precise native-byte legality or a lower-bound-preserving full mixed backtranslation |

Certified UNSAT, restricted proof-size hardness, and empirical solver difficulty remain distinct. No restricted-system lower bound is promoted to all algorithms or full $R_{\mathrm{mix341}}$.

## 5. Work, evidence, span and space ledger

- Logical replayed packets: K4/K3,3/cube/Petersen/prism6/prism16 contain 15/23/31/39/47/127 paid exhibited nodes; bridged control has 39 nodes without a minimum certificate.
- Explicit historical bytes: producer 6,500; certificate 197,514; verifier 9,359; verification record 1,469.
- Audit bytes: Python and independent Node sources plus raw JSON are separate artifacts.
- Host execution (one observed run, not an asymptotic theorem): producer 0.1588 s; verifier 0.2324 s; Python audit 0.5812 s; Node audit 0.6386 s. The process-family maximum child RSS observed during the sequence was 52,680 KiB. These measurements include runtime overhead and are not FLMV exponents.
- Repository work additionally included commit/path reads, blob authentication, issue/head reads, output serialization, three failed-tag executions, SHA computation and full tracker publication/readback. Discovery cost is excluded from the mathematical $W_R$ minimum but charged here as actual audit work.
- Work, critical path and realizable schedule are not equated. The historical packet is an acyclic shared DAG; no parallel-machine span claim is made.

## 6. Status, barriers and publication constraints

- **PROVED/EXACT:** commit/blob chain and exact checker rule-tag scope.
- **COMPUTATIONAL:** replay, output equality and hostile mutations on seven finite fixtures.
- **OPEN:** full historical accepted-byte grammar [P2-D1], all-rule normalization [P2-C3], superpolynomial full-mixed $\overline W_R$ [P2-B1], noncircular same-$R$ B3 [P2-B2].
- Relativization/algebrization/Natural-Proofs barriers are not implicated by this provenance theorem; they remain relevant to any later universal lower bound.
- The local preflight command could not run because '.codex/skills/pnp-research/scripts/preflight.py' is absent from this partial workspace. Root 'main.tex' fetched at blob '68188a24badda635a5983fda1c381cdb694fd497' with zero returned content, so it was not edited; no partial-root overwrite was attempted.

## 7. Artifacts and next target

- Audit: 'experiments/review/lspv5_413_historical_341_checker_audit.py'
- Independent verifier: 'experiments/review/verify_lspv5_413_historical_341_checker.mjs'
- Raw record: 'results/raw/review/2026-11-07_0858_LSPV5_HISTORICAL_341_CHECKER_AUDIT413.json'
- Handoff: 'research/coordination/2026-11-07_0901_LSPV5_HISTORICAL_341_CHECKER413_HANDOFF.md'

**Next exact target:** locate a later source-authenticated full mixed checker or construct a historically authorized accepted-byte packet containing at least one RES record consumed by AND3. Without that artifact, do not choose TAGGED or EXTENSIONAL by preference.

P versus NP remains OPEN.
