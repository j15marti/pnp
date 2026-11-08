# LSPV-5/443: closed-schema and RFC-JSON audit of the source-bound C_509 checker

**2026-11-08 13:00 PST | Route B independent red team | COMPUTATIONAL accepted-byte counterexample + PROVED/RESTRICTED repair | P versus NP OPEN**

**Affected proof-chain IDs:** new `[P2-L5-443]`, refining executable-evidence scope under `[P2-L3-509]`, `[P2-L5-442]`, `[P2-D3]`, and `[P2-D1]`. The source-bound construction and schedule in `[P2-L3-509]` are not refuted. Historical full mixed normalization `[P2-C3]`, an all-rule superpolynomial minimum `[P2-B1]`, and noncircular same-calculus B3 `[P2-B2]` remain **OPEN**. Route A nodes `[P1-01]`, `[P1-03]`, and `[P1-04]` are unchanged.

## Claim card and IDEA

- **Target:** adversarially test the exact accepted byte language of the published compact `C_509` SOURCE/AND3/XOR checker, especially its claim to require canonical JSON and exact external-source binding.
- **Quantifiers:** for every packet accepted by the published Python `verify(src, packet)`, is the packet an RFC-8259 JSON object in one closed declared schema, with the proof bound to the exact external CNF bytes?
- **Model:** CPython JSON decoding, the exact published executable at Git blob `9ed8ab48a2a280bce7a5c10c3da455573d0052a4`, and its separate trace-only calculus `C_509`; this is not historical `R_mix341`.
- **SAME_REALIZATION:** external DIMACS byte string, packet byte string, published checker bytes, and the returned work/span record from that same call.
- **Prediction before search:** post-parse exact-type and canonical-array checks remain insufficient if duplicate object names are erased by parsing or if the packet is not bound to the exact external source.
- **Weakest material result:** one accepted non-RFC or out-of-schema packet narrows the executable's byte-language claim without implying logical unsoundness.

Pre-search falsifiers:

1. duplicate names are rejected before object construction;
2. the packet contains and checks the exact digest of the independently supplied source bytes, with positional source references;
3. duplicate/source-reordered or source-mutated packets reject;
4. the newest peer checker already closes the top-level schema and rejects non-JSON numeric constants.

## SEARCH, continuity, and corpus reconciliation

Both complete live trackers were fetched at the start of substantive work: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 bytes) and `proof2.txt` blob `5869fae8b22f3764b804075ef0c1bdd35dab87f6` (500,085 bytes). Exact nodes read include `[P1-01]`, `[P1-03]`, `[P1-04]`, `[P2-D1]`, `[P2-D3]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]`, `[P2-L5-442]`, `[P2-L1-512]`, and `[P2-L3-509]`. Current issue #3 body and its last page through comment `6726979741` were read; the all-pages connector call failed with `Transport closed`, so no claim of a successful all-comment replay is made.

Continuity artifacts actually read:

- historical governing handoff at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, exact file blob `033b54b87b7cbe94912af5cf67daa52859143a07`;
- current `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`, `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`, the project skill and its red-team mode/protocol references;
- historical declaration `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`, historical independent checker blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`, and LOCAL-CONVERT addendum blob `bbcdad9a487203f160d1009235de6bec7322a2a2`;
- predecessor LSPV-4/501 report blob `6091af9a81f1aaa8cec8f7db1b90236fd2b1e452`, peer LSPV-1/512, LSPV-3/509 report blob `fe4a27376f324e24dba53808f0139ee76bd3d144`, its compact checker blob `9ed8ab48a2a280bce7a5c10c3da455573d0052a4`, raw blob `e2725ae5d99f84e2516955d722382e7ecb2a3521`, handoff blob `101e20b41602de5f3a4e4dbe09791852ee161f2b`, and LSPV-5/442;
- actual Grok `GROKPROOF/2026-11-08_1130_PROGRESS.md` blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70`, Claude world-ledger README and `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` blob `79e4d4e7e0e3edff3aba8610852c45534bdde128`. Neither authenticates historical mixed bytes or B3.

The complete root `main.tex` blob `68188a24badda635a5983fda1c381cdb694fd497` (1,776,883 bytes) was successfully fetched by blob after a prior range endpoint had returned no text. It was reviewed for existing LSPV-5 ownership markers and OPEN status. The repository preflight script was executed from its exact fetched source in this non-checkout workspace; it reported the expected local-mirror omissions rather than a theorem or checker failure.

Change-aware required repository review found these current heads: `konard/p-vs-np@ecedd2b45f1c524d85c00b2da27a9c140025550c` (`scripts/proof_status.json`: finite/formal theorem ledger), `blkph0x/p-vs-np-proof-research@7dedc73f758dfbdc072e7aa29dfc08505761ebd5` (`METHOD_INDEX.md`: explicitly model-scoped method ledger), `meelgroup/frat-xor@18cd6bc17af10a9891c10a846ce966166f9fe0dc` (separate typed theory format), `tanyongkiam/cake_lpr@033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2` (separately verified checker distribution), `marijnheule/drat-trim@2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, and `openai/math@4eaee87548250b2682affda7d05d947c05554bae`. None supplies historical `R_mix341` accepted bytes or the same-calculus B3 bridge. Repository text and badges were treated as evidence, not authority.

Primary/authoritative sources read:

- RFC 8259 sections 4, 6, 9, and 10: object names should be unique for interoperability; `NaN` and infinities are not permitted by the JSON number grammar; parsers may accept extensions, but generators of JSON text must emit the grammar.
- Python `json` documentation: the decoder accepts `NaN`, `Infinity`, and `-Infinity` by default outside the JSON specification; `parse_constant` can reject them; the encoder defaults to `allow_nan=True`.
- Ben-Sasson--Wigderson (JACM 2001), Definition 4.1, Lemma 4.2, Theorem 4.4 and Corollary 4.5: an odd-charge connected cubic Tseitin source is a width-three CNF with four clauses per vertex, and appropriate expanders have exponential ordinary Resolution size via the width bound. Urquhart (JACM 1987, DOI 10.1145/7531.8928) is the original ordinary-Resolution hard-family control.

A Google-branded interactive client was unavailable; public indexed web and connected GitHub were used. No official CakeLPR/XLRUP checker or authoritative historical `R_mix341` checker was executed.

### Duplication / contradiction audit

LSPV-5/442 had already shown Python scalar aliases in the distinct /508 checker, so this run did not relabel that result as new. LSPV-3/509 explicitly repairs duplicate-member detection, exact integer parent IDs, positional source references, and exact source-byte digest binding. The new result is narrower: its statement that the parser “requires canonical JSON” is too broad for the actual Python predicate, which accepts a Python-specific serialization extension and has no closed top-level schema.

Relative to root `main.tex`, no full mixed lower bound, B3, or P-versus-NP status changes. The only stale statement identified is executable-level: `C_509` should be described as accepting a canonical round-trip Python-object language with duplicate-member rejection, not as an RFC-canonical closed JSON schema.

## ITERATE: exact accepted bytes and revised claim

The exact published checker was fetched from `experiments/arc/lspv3_509_compact_source_bound.py`. Its SHA-256 is `64f17cf994a4bfc4265f2a058c2e08d81828b4f23406afcb306976af04a6eb13`, matching the locally replayed bytes, and its Git blob is `9ed8ab48a2a280bce7a5c10c3da455573d0052a4`.

The K4 baseline is exact source SHA-256 `ea08104837e167b9ebd06d8f50442d828e3ba4d81f79dff8c14a09ba30050096`, packet SHA-256 `6aeaf1de68e6928c501183e6d539203e2cdd50326add8134ca5bba750abbf30e`, 163 source bytes and 408 packet bytes. It accepts with 15 paid nodes and depth 4.

Four byte-distinct mutations also accept with unchanged logical result:

| exact mutation | packet bytes | packet SHA-256 |
|---|---:|---|
| add top-level `"calculus":"NOT-C_509"` | 431 | `1f744983705ebc9302fca3a4a8f59ebc048122d9d40d46e4d73a98afba8e9695` |
| add top-level false shadow source digest | 498 | `a8a94c613279f00cd0f41bc7732ae313fadedd8c02a1a538a00f3b2991c59e5f` |
| add top-level nested unchecked claim object | 452 | `51fea3d8d6015758bc467bac4b9aa8fc61d77003a892b0286c3fc4c8627d1065` |
| add top-level `"unchecked":NaN` | 424 | `a33f4264f77f32f3afc51daa293361aea4ee9db3fc6e2ef11f211cc726e19a21` |

Two hostile controls reject: a duplicate `root` member is caught by `object_pairs_hook`, and an exact source sign mutation is caught by the digest/source replay. Thus falsifiers 1--3 defeat the broad initial hypothesis. Falsifier 4 fails: there is no top-level closed-schema or `parse_constant` guard.

The mechanism is exact. The checker round-trips the parsed object with `json.dumps(..., sort_keys=True, separators=(",",":"))`, whose default `allow_nan=True` regenerates `NaN`; RFC 8259 does not permit that token. Unknown fields survive the round trip but are not constrained or used by proof replay. Therefore the accepted language is deterministic at the Python-object level, but it is neither a closed three-field schema nor RFC JSON for the `NaN` case.

### Repair lemma

**PROVED/RESTRICTED for the tested packet wrapper.** Before invoking the unchanged proof checker:

1. decode ASCII with `object_pairs_hook` rejecting duplicate names;
2. set `parse_constant` to a function that raises on `NaN`, `Infinity`, and `-Infinity`;
3. require the top-level value to be exactly a dictionary with key set `{"nodes","root","source_sha256"}`;
4. require byte equality with the canonical serialization.

This wrapper accepts the baseline and rejects all four accepted mutations, the duplicate-member packet, and the changed-source packet. It does not alter logical node weights, proof replay, or the exact source digest. It is not a complete historical grammar theorem and makes no cryptographic collision assumption necessary for soundness, because the existing checker recomputes semantics from the supplied external source bytes.

### Independent challenge and scope

The accepted unknown fields do not change `P=o["nodes"]`, `root=o["root"]`, or the checked `source_sha256`. Consequently this audit does **not** produce a false UNSAT acceptance and does not falsify Theorem 509.1 or 509.2. A caller that stores or displays the unchecked `calculus` or shadow digest could be confused, but that is a provenance/schema integration risk, not a proof-soundness counterexample in the tested predicate.

The C_509 construction remains a separate source-bound tree proof in a restricted SOURCE/AND3/XOR presentation. It has no branch assumptions, case discharge, RES, DEF, LOCAL-CONVERT, private/exported wires, or historical native record parser. Hence it cannot establish or refute the full branching/shared-DAG minimum, `[P2-B1]`, or B3.

## Established-family and shortcut ledger

| family | exact encoding and size | theorem/model | known shortcut/control | remaining transfer |
|---|---|---|---|---|
| odd-charge connected cubic Tseitin | edge variables; four signed strict 3-clauses per vertex; `n=3h/2`, `m=4h`, indexed source `Theta(h log h)` bits | exponential ordinary shared-DAG Resolution on suitable cubic expanders (Urquhart; Ben-Sasson--Wigderson) | `C_509`: 3h AND3 plus h-1 XOR, `q=4h-1`, depth `2+ceil(log2 h)`; source-bound recomputed rows | authenticate and lower-bound every legal historical mixed rule; OPEN |
| gadgetized Tseitin from `[P2-L3-504]` | replace selected source clauses by the established three-clause/two-variable gadget | ordinary-Resolution lower-bound retraction only in its proved direction | two RES plus paid CAST in distinct `R_CAST507(w)`; scalar/canonical aliases audited in `[P2-L5-442]` | authenticate historical RES-to-factor/CAST port and fees; OPEN |
| Haken PHP | canonical pigeonhole CNF | exponential ordinary Resolution | Cook Extended Resolution is a mandatory stronger shortcut control | no full mixed or arbitrary-algorithm consequence |

Certified UNSAT, proof-size hardness in ordinary Resolution, finite checker acceptance, and empirical solver difficulty remain separate statuses.

## Branching/shared-DAG and B3 audit

The published K4 packet is an acyclic proof tree, hence a special DAG. Multi-premise AND nodes require both parents; no OR alternative or omitted branch is present. Shared ancestors would be charged once by node identity, but the tree fixture does not test reconvergence, assumption scopes, retention/recomputation, or branch-local lemma leakage. No case-split, weakening, or discharge rule is silently added to historical `R_mix341`.

A stricter packet schema verifies only a supplied proof. It does not translate arbitrary polynomial-time SAT computations into short proofs, prove correctness/reflection of an arbitrary decider, or establish polynomial `Wbar_R` for the same fixed historical calculus. `[P2-B2]` remains OPEN.

## Resource ledger

- Exact peer replay: one baseline, four accepted schema/constant mutations, two rejected hostile controls.
- Repair replay: baseline accepted; all six mutations/controls rejected.
- Red-team program: 6,078 bytes; SHA-256 `776f4b205a73c95b05cff541af940d7635a74ffa1f9f21d47fe6bac42bdfb9cd`; Git blob `e38a80b753ae14ae87bd5867afce68a06602a763`.
- Raw result: 5,138 bytes; SHA-256 `d7bf19486bf13113c35a21fe4f8f5e8527052f94742ff63a8c6daf2791d97f77`; Git blob `278544ad28568344c210a4234ea3830682a81b2a`.
- Recorded host run: 0.00253 seconds wall and 9,856 KiB `ru_maxrss`; a rerun reproduced every Boolean outcome and proof result, with only timing/RSS fields varying. These are host measurements, not asymptotic or same-machine bounds.
- Parsing, source and packet reads, hashing, object construction, duplicate checks, proof replay, failed controls, output serialization, repository/index/head reads, and publication/readback are charged as actual phases distinct from ideal logical work 15.
- No discovery cost is inserted into ideal `W_R`; no cache/retrieval, reference, storage, recomputation, or parallel-span charge is silently identified with logical node weight.
- No FLMV exponent is inferred.

## Status, artifacts, and exact remaining gap

**Actual advance:** the broad initial duplicate/source-binding concern was falsified for the exact /509 checker. A narrower accepted-byte counterexample shows that its “canonical JSON” description must be qualified: arbitrary unknown top-level members and Python's non-standard `NaN` extension are accepted. A minimal closed-schema/`parse_constant` wrapper repairs every tested case without changing proof semantics.

Artifacts:

- report: `research/main/2026-11-08_1300_MAIN_C509_CLOSED_SCHEMA_REFEREE443.md`;
- code: `experiments/review/lspv5_443_schema_audit.py`;
- raw: `experiments/review/raw/2026-11-08_1252_LSPV5_443_PEER509_SCHEMA_AUDIT_RAW.json`;
- handoff: `research/coordination/2026-11-08_1300_LSPV5_C509_CLOSED_SCHEMA_443_HANDOFF.md`.

**Precise remaining gap:** authenticate the complete historical `R_mix341` accepted-byte language and every RES/AND3/GF(2)/DEF/LOCAL-CONVERT/private/exported/branch-discharge port with its fixed weight; then prove an all-rule superpolynomial lower bound or exhibit a legal shortcut. Independently, prove a noncircular same-calculus B3. P versus NP remains OPEN.

