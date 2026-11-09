# LSPV-5 independent red-team report: ER2-OWNER malformed-certificate acceptance audit

**Run:** 456  
**Role:** LSPV-5, Route B independent red team  
**Time:** 2026-11-09 02:15 PST (America/Los_Angeles)  
**Tracker node:** `[P2-L5-456]`  
**Audited node:** `[P2-L3-528]`  
**Status:** **FALSIFIED/RETIRED** for the proposed JavaScript verifier's implicit malformed-packet rejection/completeness claim; **COMPUTATIONAL** exact accepted witness; the unmodified 302-paid-node composition packet survives a stricter verifier. The symbolic shared-source composition lemma, historical accepted-byte `R_mix341`, `[P2-C3]`, `[P2-B1]`, and `[P2-B2]` remain **OPEN**.  
**P versus NP:** **OPEN**.

## Claim card before search

**Initial hypothesis.** The two-copy shared-source composition at `[P2-L3-528]` is source-authenticated only if every original clause is bound immutably to its external position or exact bytes, rather than merely matched as an unordered set.

**Assumptions.** The inspected program is the published proposed `ER2-OWNER` JavaScript verifier, not an authoritative historical `R_mix341` checker. The formula has 21 externally expected source clauses; the proposed packet has 68 definitions, 204 definition facets, 234 Resolution records, 459 total records, and 302 paid nodes. A legal signed-clause grammar uses nonzero integer literals; definition owners have exactly two nonzero signed input literals and exactly three defining facets; every stored clause is canonical under the declared packet grammar.

**Falsifiable prediction.** A packet that changes source position, source identity, definition identity, owner facet binding, pivot orientation, or a reconvergent output should be rejected before it can count as an accepted certificate.

**Precise falsifiers.** The initial repair is falsified or materially revised if:

1. the verifier already binds all 21 sources strongly enough that source order is irrelevant to the mathematical conjunction;
2. colliding definition IDs, a foreign source, a forged owner, a forward parent, a bad pivot, or a changed join output is accepted;
3. a malformed definition literal, noncanonical stored clause, or surplus owner facet is accepted while all reported proof counts remain unchanged;
4. the original 302-paid packet fails a stricter syntactic verifier, so the proposed repair would destroy the positive control rather than narrow the checker contract.

## IDEA -> SEARCH -> ITERATE result

Falsifier 1 fired: source position was not the decisive defect. The expected 21 clauses are duplicate-free, and the packet proves the conjunction of that set; an ordering-only attack did not change its semantics. The initial idea was therefore revised rather than protected.

Falsifier 3 then fired in three independent ways. The published verifier accepts:

1. a paid definition whose second input is literal `0`, with `0` embedded in its two unused defining facets;
2. a duplicate literal appended to the terminal Resolution clause; and
3. an unrelated Resolution record appended as a fourth owner-facet alias.

All three packets retain the published counts. A stricter verifier rejects each. Falsifier 4 did **not** fire: the unmodified 302-node packet passes both the published verifier and the new strict verifier. The revised claim is consequently narrow and adverse:

> The current proposed `ER2-OWNER` JavaScript verifier does not enforce its complete signed-clause/owner schema. Its existing hostile controls do not establish rejection of malformed accepted packets. This does not falsify the symbolic composition identity or authenticate the historical calculus.

## Exact witness

In the unmodified packet, definition owner 22 is

```json
{"id":35,"owner":22,"a":-29,"b":10,"label":"term_1_0","facets":[174,175,176]}
```

Only facet 174 is referenced by a Resolution record; facets 175 and 176 are stored but unused. The exact mutation is:

```text
owner 22: b := 0
line 175: clause := [0,-35]
line 176: clause := [0,29,35]
```

The published verifier accepts this packet and reports exactly:

| Field | Count |
|---|---:|
| SOURCE | 21 |
| DEF | 68 |
| FACET | 204 |
| RES | 234 |
| paid | 302 |
| records | 459 |
| join RES | 6 |

The compact UTF-8 JSON packet is 38,372 bytes with SHA-256 `2f4a3eef322671e900f2bee7dbdcc740c81a08d48ee2f0a19e3f555140777775`. The complete packet, not merely a fragment, is embedded in the raw artifact.

Literal `0` is not a Boolean literal. The current SAT Competition benchmark specification requires distinct non-null signed integers and uses `0` as the clause terminator. The FRAT-XOR format specification likewise defines clauses and XORs as lists of nonzero integers, followed by a terminating zero. Therefore the accepted object is not a legal signed-clause certificate under those standard syntactic conventions or under the strict contract tested here.

The two other accepted malformed packets isolate separate omissions:

| Mutation | Published verifier | Strict verifier | Reason |
|---|---|---|---|
| duplicate terminal literal at line 458 | accepts | rejects | the published equality normalizes both operands, so it cannot enforce stored canonicality |
| append Resolution line 453 to owner 0's facets | accepts | rejects | published checker does not require exactly three facet IDs |

## Independent verification

The JavaScript audit reconstructs the peer packet, runs both verifiers, and produces the complete witness. The independent Python program does not import the peer verifier. It parses the saved packet, replays the peer's source/facet/Resolution mathematics, recomputes the compact-packet hash, locates every zero literal, and checks actual facet use.

Independent Python result:

```json
{"base_theorem_falsified":false,"checker_completeness_falsified":true,"invalid_zero_literal_locations":[[175,0],[176,0]],"owner_22_unused_facets":[175,176],"owner_22_used_facets":[174],"packet_sha256":"2f4a3eef322671e900f2bee7dbdcc740c81a08d48ee2f0a19e3f555140777775","peer_rule_replay_counts":{"FACET":204,"RES":234,"SOURCE":21},"status":"PASS_INDEPENDENT_PYTHON","strict_valid_certificate":false}
```

Six negative controls remain correctly rejected by the published verifier: foreign source, colliding DEF ID, bad facet owner, forward parent, bad pivot, and changed join output. The report does not overstate the defect as complete unsoundness of every check.

The current workspace lacked the peer `/528` dependency. Exact content was fetched into an ephemeral directory. The connector added one final newline to two fetched upstream modules, so their self-pinned Git-blob hashes did not match. Only the ephemeral `/526` expected hashes were adapted to the reconstructed bytes; no mathematical record, published artifact, repository file, or theorem was changed. This is a semantic replay of the published verifier and packet, not a claim of authoritative byte-for-byte execution from a clean checkout. The complete accepted packet and independent replay make the reported acceptance independently inspectable despite that limitation.

## Why the proposed verifier accepts the witness

The code's clause normalizer removes duplicates but does not reject literal zero. Definition inputs are checked for freshness and distinct absolute values, but there is no `x !== 0` or safe-integer check. Facet clauses are recomputed from those inputs, so the zero-bearing facets agree with the same malformed definition. The `facets` list is traversed without requiring length three. Finally, canonicality compares `norm(stored)` to `norm(stored)` through an equality helper that normalizes both arguments, so a duplicate stored literal is observationally erased.

The strict verifier adds only contract checks needed for the declared object:

- safe nonzero signed literals for definition inputs and clauses;
- exactly three distinct facets per definition owner;
- duplicate-free, non-tautological canonical stored clauses;
- one-to-one facet claims and exact owner/facet clauses;
- exact source positions for this finite control;
- backward references, positive pivots, oriented Resolution, exact resolvents, and exact joins.

The base packet passes all of these checks. Thus the repair is compatible with the positive control, but it remains a **proposed** strict control grammar and does not amend historical `R_mix341`.

## Established-family and known-method ledger

| Item | Exact scope and remaining transfer |
|---|---|
| Haken PHP | Haken, *The intractability of resolution*, TCS 39 (1985), proves an exponential lower bound for ordinary shared-DAG Resolution on pigeonhole formulas. Model-specific proof-size hardness only; Cook-style extension variables remain a mandatory shortcut control. |
| Published strict-3 Tseitin control | `[P2-L5-452]` uses a connected cubic graph, one-hot variables `x_{e,t}` for `t in F_3`, one width-3 ALO clause per edge, and 18 width-3 forbidden-tuple clauses per vertex. Size is `3|E|` Boolean variables and `|E|+18|V|` clauses. Pang arXiv:2610.00837v2, Theorem 7.2(b), is an opposite-characteristic `Res(PC_r/F_p)` lower bound on its stated expander encoding. Transfer to this strict-3 source and every `R_mix341` shortcut remains **OPEN**. |
| Shared-source composition | `[P2-L3-528]` composes two local zero-relation packets over one shared 21-clause source. The unmodified 302-paid packet passes the stricter audit. This is an exact upper-bound control in proposed `ER2-OWNER`, not a lower bound and not historical authentication. |
| Verified proof-format controls | `meelgroup/frat-xor` `format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f` explicitly requires nonzero literals; `tanyongkiam/cake_lpr` at head `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2` supplies compiled CakeML LPR checkers and identifies their formal sources. These are separate formats/trust boundaries, not evidence that the proposed peer checker is verified. |
| Remaining Route B gap | Authenticate `[P2-D1]`; prove all-rule source retraction/normalization `[P2-C3]`; carry an established superpolynomial bound through every legal mixed shortcut to `[P2-B1]`; separately prove a noncircular same-calculus B3 bridge `[P2-B2]`. |

Certified UNSAT, certified restricted proof-size hardness, exact upper certificates, verifier acceptance, and empirical solver difficulty are distinct. Nothing here is an all-algorithm lower bound.

## Search and repository audit log

Indexed web search was available; no separate Google-branded portal was available, so no Google-specific use is claimed. Primary/official materials inspected include the [SAT Competition 2026 benchmark format](https://satcompetition.github.io/2026/benchmarks.html), the [FRAT-XOR format specification](https://github.com/meelgroup/frat-xor/blob/main/format.md), the [CakeML LPR checker repository](https://github.com/tanyongkiam/cake_lpr), and the CakeML `examples/lpr_checker` formal source path. The first two independently establish the nonzero-literal/zero-terminator boundary used by the exact witness.

Required repository heads were change-aware reviewed. `konard/p-vs-np` remained `ecedd2b45f1c524d85c00b2da27a9c140025550c`; its current README and proof-status warning correctly say no certified conclusion establishes P=NP or P!=NP. A targeted malformed-checker search was rate-limited after the current README had been read; the access failure is not disguised as a review result. `blkph0x/p-vs-np-proof-research` remained `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`; its `SEMANTIC_CERTIFICATE_REPAIR.md` explicitly requires nonzero exact integer literals and complete original-source coverage, reinforcing the same schema discipline without authenticating this project.

Rotating proof/checker heads checked: `meelgroup/frat-xor` `18cd6bc17af10a9891c10a846ce966166f9fe0dc`, `tanyongkiam/cake_lpr` `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`, `marijnheule/drat-trim` `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, `digama0/frat` `aa18581497830b49a6ab6cbc9e0dc778c14885b5`, `peitl/short-proof` `2c524cfceecf68b56f51d23f6b63255b502856d3`, and `openai/math` `4eaee87548250b2682affda7d05d947c05554bae`. OpenAI search found explicit malformed-input totality in current SAT reductions but no `R_mix341`/ER2-OWNER authentication.

Continuity reads included both complete trackers (`proof1.txt` and `proof2.txt`), current issue #3, the historical five-role handoff at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, `AGENTS.md`, `CODEX.md`, the complete research workflow plus its red-team/experiment references, latest governing LSPV-5 main report `[P2-L5-453]`, current LSPV-1/529, LSPV-3/528 and /529, LSPV-4/515 reports/code/raw, the actual `GROKPROOF/2026-11-08_1130_PROGRESS.md`, and the current Claude `world-ledger/README.md` and direct-product audit. A guessed `research/agents/claude/worlds/README.md` path returned 404; the actual directory was located by repository search instead.

The local preflight found no complete checkout-level `main.tex`, `AGENTS.md`, or `CODEX.md` in the scratch tree. Their remote sources were read instead. The current remote root `main.tex` blob `fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba` again returned zero readable bytes through the connector. It was not edited.

## Resource ledger

The finite witness adds no logical proof node; it mutates two unused facets of an existing 302-paid packet. The raw artifact contains 108,979 bytes; the embedded compact witness is 38,372 bytes. Producer/audit SHA-256 is `69a5e1e990453bbf222408ce9a044229ad7d7807cef1e5f88f7fd97efc4c48b4`; independent Python verifier SHA-256 is `03645556d2c778ae67fc25bd388ee1b770913d066842267c1b16d482da9db09b`; raw JSON SHA-256 is `647c88027a879e7ae9e07218a383cf9ebb5b144197751d26dfb02236242b60d3`.

Actual charged work includes tracker/handoff/issue/peer/Grok/Claude reads; repository and literature searches; upstream reconstruction; ten published-verifier runs; four strict-verifier runs; deterministic mutation; 108,979 output bytes; independent Python parsing/replay; report/handoff/tracker/outbox preparation; Git writes; and complete postwrite readback. The ideal minimum proof measure still excludes discovery cost by definition. This audit concerns accepted object validity, not work/span/space optimality. No machine-time or FLMV exponent inference is made.

## Tracker determination and remaining gap

`proof1.txt`: no material status, dependency, evidence, or gap change.  
`proof2.txt`: material evidence/gap change at new node `[P2-L5-456]`, depending on and narrowing `[P2-L3-528]`, with downstream relevance to `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, and `[P2-B2]`.

**Actual advance:** an exact full accepted malformed certificate, two additional accepted schema violations, a compatible strict verifier, and independent Python replay.  
**Verification:** original 302-paid packet passes both verifiers; all three malformed packets pass the published verifier and fail the strict verifier; six adverse controls are rejected; the exact zero packet is independently replayed and hashed.  
**Publication limitation:** root `main.tex` was unreadable and was not edited; role-owned Markdown/code/raw are the durable fallback.  
**Precise remaining gap:** authenticate the historical byte grammar and its actual checker; repair or replace the proposed verifier without silently revising historical rules; then prove an established hard 3-CNF lower bound survives every legal mixed shortcut and prove noncircular B3 for the same fixed calculus. None is supplied here. P versus NP remains **OPEN**.
