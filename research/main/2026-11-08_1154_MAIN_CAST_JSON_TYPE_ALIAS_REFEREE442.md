# LSPV-5/442: JSON scalar-type and canonical-clause aliases in the published CAST checker

**2026-11-08 11:54 PST | Route B independent red team | COMPUTATIONAL counterexample + PROVED/RESTRICTED repair lemma | P versus NP OPEN**

**Affected proof-chain IDs:** new `[P2-L5-442]`; evidence/gap refinement of `[P2-L3-508]`, `[P2-L3-507]`, `[P2-D3]`, and `[P2-D1]`. The separate-calculus mathematical construction in `[P2-L3-508]` is not refuted. Historical all-rule transfer `[P2-C3]`, superpolynomial minimum `[P2-B1]`, and noncircular same-calculus B3 `[P2-B2]` remain **OPEN**.

## Claim card and IDEA

- **Target:** falsify or repair the claim that the published compact `R_CAST507(w)` executable authenticates its JSON trace bytes and source records.
- **Quantifiers:** for the published Python predicate `check`, does every accepted JSON packet have the declared integer/canonical source, parent, and cost representation?
- **Model:** CPython JSON decoding followed by the exact published semantic checker; this is the distinct typed `R_CAST507(w)`, not historical `R_mix341`.
- **Same realization:** GitHub blob `6ef7c3faf76326a30f139b1f8d13a60be097fcba` at `experiments/arc/lspv3_508_paid_cast_replay.py`; locally replayed connector text differs only by a terminal LF and has SHA-256 `0a5c4eae786018a5893ff03b7a3c993266e8d2f4d89f0f95f090aff0b46b9efc`.
- **Prediction:** semantic normalization and Python numeric equality admit byte-distinct aliases unless exact JSON types and canonical arrays are checked before semantic replay.
- **Weakest material result:** one accepted non-integer or noncanonical packet suffices to falsify raw-evidence authentication for this executable without touching the construction theorem.

Pre-search falsifiers:

1. every literal, parent ID, pivot and cost is checked with exact integer type rather than numeric equality;
2. every source clause is compared as the exact canonical array, not after set/sort normalization;
3. all byte-distinct mutations reject while the baseline accepts;
4. an already-published strict wrapper rejects such aliases without rejecting the baseline.

## SEARCH and continuity

Both live root trackers were fetched completely at initial head `3f573364e79a0d5ff50ce1b621eb9abd471e8a6e`: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 characters) and `proof2.txt` blob `6f2103674963296f3710a6d3533adf329995d640` (486,870 characters). Exact active nodes read include `[P2-L3-508]`, `[P2-L1-511]`, `[P2-L5-441]`, `[P2-D1]`, `[P2-D3]`, `[P2-C3]`, `[P2-B1]`, and `[P2-B2]`. Current issue #3 body and its last page through comment `6726299545` were read; issue reported 1,369 comments.

Continuity sources actually read:

- historical five-role handoff at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, blob `033b54b87b7cbe94912af5cf67daa52859143a07`;
- `AGENTS.md` `19656af102604d5f0a721d548cf2e4e72a063561`, `CODEX.md` `754999f50de93cdb693ed37bc8110d31e9e698ef`, project skill `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`, red-team modes `c211e9f545f94b636b119f1e721b475a31e925f9`, and protocol `25b38dc02bc0b0331ed03b0a4c7ff1b1e2a4ed00`;
- historical declaration `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`, LOCAL-CONVERT addendum blob `bbcdad9a487203f160d1009235de6bec7322a2a2`, and actual restricted /341 verifier blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`;
- peer /508 report blob `152d477c62730bc9e53aba412a8267a21db3380e`, compact checker blob `6ef7c3faf76326a30f139b1f8d13a60be097fcba`, raw blob `77cfdfe477f6b99de8f8f382f541c9448f8b8cf6`, and handoff blob `7147ce78fdc638ef57ee40263ece272c3813c511`;
- peer /511 report blob `9fe0b0b2ab49f97b2315aa1586565d471d8d5bba` and code blob `10e2edf381b7a844f1fb6fa42e04255137bf31f5`;
- actual Grok `GROKPROOF/2026-11-08_1130_PROGRESS.md` blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70` and Claude `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` blob `79e4d4e7e0e3edff3aba8610852c45534bdde128`. Neither supplies native mixed-rule authentication or B3.

Required change-aware repository review found unchanged heads: `konard/p-vs-np@ecedd2b45f1c524d85c00b2da27a9c140025550c` with `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research@7dedc73f758dfbdc072e7aa29dfc08505761ebd5` with `METHOD_INDEX.md` `18d693ea71dfa433370eb7afbebc3106e32f03e5` and `INDEPENDENT_AUDIT.md` `b30515cced93d8911a6415555ee9ec1444502d93`. Both preserve missing uniform/general transfers. Also checked `frat-xor@18cd6bc`, `cake_lpr@033aad5`, `short-proof@2c524cf`, `drat-trim@2e3b2dc`, `cnfgen@24e633b`, `openai/math@4eaee875`, `anthropics/formal-math@16a5ce4`, and `abc@4b55d07`. The OpenAI GitHub query `JSON proof checker SAT certificate` returned no applicable file.

Primary/authoritative sources searched and read: Urquhart, *Hard examples for resolution*, JACM 34(1), DOI 10.1145/7531.8928; Ben-Sasson--Wigderson, *Short Proofs Are Narrow*, JACM 48(2), DOI 10.1145/375827.375835; Cook--Reckhow 1979; RFC 8259; Python JSON and built-in-type documentation. The first three establish proof-system-scoped controls, not mixed-calculus hardness. RFC 8259 distinguishes Boolean literals from numbers. Python documents JSON `true/false` decoding to `True/False`, integer-form numbers to `int`, real-form numbers to `float`, and that `bool` is a subclass of `int`. A Google-branded interactive client was unavailable; indexed web search was used and recorded honestly.

The repository preflight command failed because this workspace is not a checkout and lacks `.codex/skills/pnp-research/scripts/preflight.py`. Root `main.tex` returned blob `68188a24badda635a5983fda1c381cdb694fd497` with zero readable bytes; no unsafe partial or ownership-region rewrite was attempted.

## ITERATE: accepted packets

The published /508 compact program itself replays all 45 advertised graph/`k`/fee cases and rejects its 45 invalid-parent mutations. The independent adversarial program then constructs the published K4, `k=0`, `w=1` packet, serializes each mutation with `json.dumps(..., allow_nan=False)`, parses it with `json.loads`, and invokes the exact checker.

Baseline: work 15, weighted span 4, 1,557 packet bytes, SHA-256 `a54b961d5dafad12eafacd6f3e1f0535c5121a7aa98ca1990b3d627d5182654b`.

Seven byte-distinct packets accept with the same work and span:

| mutation | bytes | SHA-256 |
|---|---:|---|
| duplicate a SOURCE literal | 1,559 | `c0e7b4db61a1b9be3f0d16af4017221d5b539202b6ace6e594c0f5649a3ababd` |
| reverse a SOURCE literal array | 1,557 | `611bf5870439a002a1b65535f47dbf402cf542fa42337c9de72936d547d4db5f` |
| encode source literal 1 as `1.0` | 1,559 | `e99a5fff19b622e89103a09d54f21afaf5791b4e8cf779e564469a37b686f9c6` |
| encode source literal 1 as `true` | 1,560 | `f9d77d3873c8275b436f2d75859616d628949b94a704641e6f5034ffb56fd857` |
| encode parent IDs `[0,1]` as `[false,true]` | 1,564 | `6776e83801061cc216197f99c4ce9b52a24ff12f79a7632a7e62a183161e76e6` |
| encode unit cost `1` as `true` | 1,560 | `e55a7e9f6abccede8341c6fa7b53659c993d43074b0a5997e5ff8faaa38df628` |
| encode unit cost `1` as `1.0` | 1,559 | `6dd49ff026127fa8f1f08cfd887dfa2b1b6c243a442658fff7049ce576e4af84` |

Mechanism: `norm` removes duplicates and sorts literals before the source comparison; Python numeric equality makes `True == 1` and `1.0 == 1`; and `isinstance(False, int)` is true. Therefore source equality, parent typing, and cost checks do not bind the raw JSON scalar type or canonical clause array.

Four hostile controls reject: nonintegral literal `1.5`, string literal `"1"`, unit cost `false`, and parent ID `0.0`. Thus the result is not the claim that all malformed packets pass.

### Repair lemma

**PROVED/RESTRICTED.** For this packet language, a pre-semantic layer that requires `type(x) is int` for literals, parent IDs, pivots, costs, `n`, `root`, and `w`; requires nonzero literals and valid ranges; and requires every clause array to equal its canonical normalized list, rejects all seven aliases. The independently implemented layer accepts the baseline and rejects 7/7 aliases. Exact-type tests are necessary here because `isinstance(x,int)` intentionally includes Boolean values.

This is a sufficient repair for the tested fields, not a complete grammar theorem: duplicate JSON object member names, Unicode string aliases, number range limits, unknown keys, external source-file hashing, and historical rule tags remain separate obligations.

### Scope and independent challenge

- The counterexample falsifies **raw-evidence/source-record authentication for the published compact /508 executable**.
- It does **not** make the accepted derivation semantically unsound: all aliases decode to values that the checker treats as the same logical packet.
- It does **not** refute Theorem 508.1's constructive all-subset upper bound in the separately declared typed calculus.
- The published compact loop constructs prefix sets `j<k`, not arbitrary subsets `S`; this is an executable-coverage gap, not a counterexample to the local symbolic composition proof for arbitrary `S`.
- It supplies no evidence that historical `R_mix341` accepts CAST or these packets.

## Established-family ledger

| family | exact encoding/size | theorem/model | known shortcut/control | remaining transfer |
|---|---|---|---|---|
| odd cubic-expander Tseitin strict 3-CNF | edge variables; four signed proper 3-clauses per cubic vertex; `n=3h/2`, `m=4h`, indexed size `Theta(h log h)` | exponential ordinary shared-DAG Resolution on appropriate expanders (Urquhart; Ben-Sasson--Wigderson width/size) | native GF(2) summation gives a linear mixed proof when legal; /508's distinct CAST calculus gives another linear upper after gadgets | prove source-authenticated simulation/lower bound against **every** historical mixed rule; OPEN |
| all-subset gadgetized Tseitin `H_S` | replace each of `k` selected original clauses by three strict 3-clauses and two fresh variables; `m=4h+2k` | ordinary Resolution hardness transfers by the cited substitution/restriction direction in `[P2-L3-504]` | two RES + one paid CAST per gadget in distinct `R_CAST507(w)`; work `4h+2k-1+kw` | authenticate any historical RES-to-factor port and its fee; OPEN |
| Haken PHP | standard pigeonhole CNF | exponential ordinary Resolution | Cook/extended proofs are mandatory stronger controls | no all-rule mixed or arbitrary-algorithm consequence |

Certified UNSAT, ordinary-Resolution proof-size hardness, and empirical checker acceptance are three different statuses throughout.

## Branching/shared-DAG and B3 audit

The /508 packet is a context-free acyclic shared DAG; it performs no case split, assumption introduction, or discharge. It therefore does not test branch-local scope or AND-case completeness. Shared ancestors are counted once by its reachability check, while weighted critical path is separate from total work. No OR choice or branch reconvergence is silently added to historical `R_mix341`.

The result affects evidence binding under `[P2-D3]`; it supplies neither B1 nor B2 nor B3. In particular, a stricter checker validates only a proof packet. It does not prove that `SAT in P` yields polynomial `Wbar_R` for this same preselected calculus, and it does not formalize arbitrary decider correctness/reflection.

## Resource ledger

- Published checker replay: 45 valid cases and 45 invalid-parent rejections.
- Red-team packets: one baseline, seven accepted aliases, four rejected controls, and seven strict-layer rejections.
- Red-team program: 8,309 bytes; SHA-256 `37edf04385f29068ebeeabff1ab9b07d1fdea5e17be1fd6d87616c294006cb82`.
- Measured CPython run: 0.00545 seconds wall and 10,240 KiB `ru_maxrss` on this host. These are host measurements, not asymptotic bounds.
- Evidence packets: 1,557--1,564 bytes in this audit. Logical work/span remains 15/4 for accepted aliases; parsing, JSON allocation, hashing, copying, validation, output, source reads, and failed controls are additional actual work.
- Construction/search included repository and issue reads, external head/file reads, web search, peer-code replay, adversarial serialization, and strict-repair replay.
- No cache, retrieval, recomputation, reference, storage, or output phase is silently identified with ideal logical node weight.
- No FLMV exponent or same-machine claim is inferred.

## Status, publication, and next gap

**Actual advance:** a minimal byte-level family of seven accepted JSON aliases falsifies the compact /508 checker's raw type/canonical binding, and an independently checked exact-type/canonical-array layer repairs all seven while preserving the baseline. **Status:** COMPUTATIONAL counterexample; PROVED/RESTRICTED repair lemma for the tested packet fields.

Artifacts:

- report: `research/main/2026-11-08_1154_MAIN_CAST_JSON_TYPE_ALIAS_REFEREE442.md`;
- code: `experiments/review/lspv5_442_cast_json_alias_audit.py`;
- raw: `experiments/review/raw/2026-11-08_1154_LSPV5_442_CAST_JSON_ALIAS_RAW.json`;
- handoff: `research/coordination/2026-11-08_1154_LSPV5_CAST_JSON_ALIAS_442_HANDOFF.md`.

Publication commit and conflict-safe tracker/readback SHAs are recorded in the finalization addendum and issue #3 comment after the writes complete.

**Precise remaining gap:** authenticate the complete historical `R_mix341` accepted-byte language, including strict raw source identity, RES/LOCAL-CONVERT/DEF facets, exported/private wires, global freshness, and every cross-type port; then prove a full all-rule lower-bound transfer or find a legal shortcut. Same-calculus noncircular B3 remains OPEN. P versus NP remains OPEN.
