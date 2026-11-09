# LSPV-5/446 — official XLRUP replay and exact-source binding referee

2026-11-08 16:03 PST | Route B independent red team | **COMPUTATIONAL official-checker replay + PROVED/RESTRICTED interface/provenance refinement** | P versus NP **OPEN**.

Proof-chain evidence: new **[P2-L5-446]**, refining **[P2-L3-514]**, **[P2-D1]**, **[P2-C3]**, and checker-scope **[P2-L5-413]**. **[P2-B1]** and **[P2-B2]** remain OPEN. No historical rule, grammar, weight, role, ID, title, schedule, enabled state, or two-Route-A/three-Route-B allocation is changed.

## IDEA: hypothesis, assumptions, prediction, falsifiers

Initial hypothesis: any claimed historical `LOCAL`/`RES` certificate still relies on a declared or completed schema not fixed by `/341`, unless it identifies a pre-existing authoritative checker and byte grammar. Assumptions: the source is original signed strict cubic Tseitin 3-CNF; the external certificate uses the published XLRUP grammar; the historical target remains frozen `R_mix341` with paid at-most-binary antecedents.

Prediction: the LSPV-3/514 four-source certificate may pass an external checker, but that alone will neither bind exact original bytes nor make the four-hint `i x` record a legal unit-cost historical node.

Falsifiers registered before search:

1. a peer supplies exact accepted bytes and a historical checker at a pre-existing immutable SHA;
2. `/341` itself defines every serialized field, export, facet, and source-binding relation used;
3. an independent replay accepts the baseline and rejects source rebinding, malformed input, and scope leakage without wrapper additions;
4. a provenance-preserving simulation proves that the external four-hint macro is exactly historical rather than an extension.

Falsifier 3 partially fired at the external-format level: the actual pinned `cake_xlrup` binary accepts every /514 baseline and rejects the logical corruptions. It does **not** fire for exact source bytes, because a comment-only byte mutation is accepted. Falsifiers 1, 2, and 4 did not fire for historical `R_mix341`.

## Required continuity and source review

Complete current trackers were read before publication: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 UTF-8 characters; `proof2.txt` prewrite blob `9433aa08137817b830d26005c8775bf1d1f84589`, 540,330 characters. Exact affected IDs reviewed: [P2-L3-514], [P2-D1], [P2-C3], [P2-L5-413], [P2-B1], [P2-B2].

Also read: current issue #3 through comment `6728867584`; the 2026-11-02 five-role refocus at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`; `AGENTS.md` blob `19656af...`; `CODEX.md` blob `754999f...`; `.codex/skills/pnp-research/SKILL.md` blob `b8df83a...`; mode/protocol blobs `c211e9f545f94b636b119f1e721b475a31e925f9` and `25b38dc02bc0b0331ed03b0a4c7ff1b1e2a4ed00`; historical `/341` declaration blob `c87acd11...`; LSPV-3/514 report blob `d145f7c84571ff09c407f11bb2e39aed499339bb`, code blob `6dc6b857a22c99c20ba8c57103025dacd2b3a68b`, raw blob `7d9afcd4af760c0107ec5cad41bd5a011dce1c1d`, and handoff blob `ab28cf76edca851b72540efb542044c37101d899`.

Actual peer-model files read, not guessed: `GROKPROOF/2026-11-08_1130_PROGRESS.md` blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70`; `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` blob `79e4d4e7e0e3edff3aba8610852c45534bdde128`. Neither fixes historical mixed bytes or B3.

The repository preflight was actually executed in this non-checkout scratch root. It reported the exact expected mirror failures: missing root `main.tex`, missing unique root main, and missing local skill/AGENTS/CODEX files. This was an environment-layout limitation, not a theorem or checker failure.

## SEARCH: primary and repository evidence

### Official XLRUP source and theorem

- `meelgroup/frat-xor@18cd6bc17af10a9891c10a846ce966166f9fe0dc`, `format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`: strict `i x` requires every CNF-encoding clause of the output XOR to contain a hinted source clause; `i cx` requires exact XOR-to-clause encoding.
- Same repository, `cake_xlrup/README.md` blob `c71de8090d1731cf6a1b6ea70b11170e0d4a3209`: the distributed checker is built from CakeML commit `0f1aca3913a175c390f0fd0b3af04f43d49a0fde` and HOL4 commit `652d1f0aad5cd537ed1e5d470ba3444e70ba470e`; `--no-binary` selects the textual proof grammar.
- Pinned CakeML source `examples/cnf/xlrup/xlrupScript.sml` blob `79c537f75034bf95bf45abfeed3c1cdcf45ed955` states `check_xlrups_unsat_sound`: under `EVERY wf_xlrup`, nonzero input literals, and checker acceptance, no assignment satisfies the parsed clause and XOR sets. This theorem is about parsed `cfml`/`xorig`, not a hash of original source bytes.
- Current CakeML head `b3e6ea34ca1aed91a57703a30549260ce6f6448e` retains that same source blob. `tanyongkiam/cake_lpr@033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2` is a separate LPR distribution and does not authenticate historical `R_mix341`.

The distributed assembly `cake_xlrup.S` SHA-256 `4e08862087314ba00b72917214ea82f1c16c5d0063a12e0d72c8231252adcc2a` and `basis_ffi.c` SHA-256 `bd498883fdc0577d734a771fe8197c5ff571f2abdd769b8dc95d46818db5cbbc` were fetched from that immutable FRAT-XOR commit and built with its Makefile. The resulting static x86-64 binary SHA-256 is `56e2bc4aeddb362d632bf9f7056cfd604afb2f2e5f86d131d1d1dc554ef5b7bc`. The repository example returned exactly `s VERIFIED UNSAT`.

### Required change-aware corpus

- `konard/p-vs-np@ecedd2b45f1c524d85c00b2da27a9c140025550c`, unchanged; `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2` is a finite formal theorem ledger, not a general P/NP resolution.
- `blkph0x/p-vs-np-proof-research@7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, unchanged; `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` and `REVIEW_ADDENDUM.md` blob `6a7cc2f8962d3fcfc1778b1d3d8f5dc8d56d70` expressly remain model scoped.
- Rotating relevant sources: `digama0/frat@aa18581497830b49a6ab6cbc9e0dc778c14885b5`; `openai/math@4eaee87548250b2682affda7d05d947c05554bae`; `MassimoLauria/cnfgen@24e633bdbed0d0998493bee99c42faf480c7dc96`. None defines historical `R_mix341` or supplies B3.

Primary literature checked: Urquhart, *JACM* 34 (1987), DOI `10.1145/7531.8928`; Ben-Sasson--Wigderson, *JACM* 48 (2001), DOI `10.1145/375827.375835`; and the CAV 2024 certified approximate model-counting paper describing FRAT-XOR/XLRUP. The first two concern ordinary Resolution on suitable Tseitin/expansion families; the third supports an external verified CNF-XOR checker. None transfers an ordinary Resolution lower bound to the entire historical mixed calculus. No separate Google-branded interface was available or claimed.

## Family/theorem/encoding/known-method/remaining-transfer ledger

| Item | Exact record |
|---|---|
| Family | Connected cubic graph $G=(V,E)$, $h=|V|$, $|E|=3h/2$, odd vertex-charge vector. |
| Exact 3-CNF | One edge variable per edge. For each degree-three vertex, include the four width-three clauses forbidding assignments of the wrong parity. Thus $3h/2$ variables and exactly $4h$ original clauses. |
| Certified status | Odd total charge makes the system UNSAT. This run certifies six finite instances with the pinned external checker; finite controls are not an asymptotic lower-bound family. |
| Published lower bound | Suitable bounded-degree expander Tseitin formulas require exponential ordinary shared-DAG Resolution size (model-qualified Urquhart/width consequences). |
| External upper method | Four original clauses imply one vertex XOR by strict XLRUP `i x`; combine $h$ rows with $h-1$ binary `x` records; export contradiction by one `i cx`: exactly $2h$ external records. |
| Historical control | Native `/341` nodes have at most two paid proof antecedents. A four-hint external record is not automatically one historical node. The separate historical SOURCE/AND3/XOR $4h-1$ comparison remains only at its authenticated scope. |
| Remaining gap | A source-authenticated paid simulation inside the exact historical grammar, and then an all-legal-rule lower bound or noncircular same-calculus B3. Equisatisfiability and external acceptance are insufficient. |

Cook extended Resolution and GF(2)/Tseitin shortcuts remain mandatory upper-bound controls. This run uses the algebraic shortcut rather than excluding it.

## ITERATE: official replay, adversaries, and revised claim

The independent Python generator produced the same six named families as /514 and invoked the pinned binary in text mode. It did not call the peer JavaScript implementation. Results:

| Graph | $h$ | vars | clauses | XLRUP records | baseline | same proof + comment-only source mutation | logical corruptions rejected |
|---|---:|---:|---:|---:|---|---|---:|
| K4 | 4 | 6 | 16 | 8 | VERIFIED UNSAT | VERIFIED UNSAT | 6/6 |
| K3,3 | 6 | 9 | 24 | 12 | VERIFIED UNSAT | VERIFIED UNSAT | 6/6 |
| cube | 8 | 12 | 32 | 16 | VERIFIED UNSAT | VERIFIED UNSAT | 6/6 |
| Prism8 | 16 | 24 | 64 | 32 | VERIFIED UNSAT | VERIFIED UNSAT | 6/6 |
| Prism16 | 32 | 48 | 128 | 64 | VERIFIED UNSAT | VERIFIED UNSAT | 6/6 |
| Prism64 | 128 | 192 | 512 | 256 | VERIFIED UNSAT | VERIFIED UNSAT | 6/6 |

The 36 rejected controls cover missing or foreign source hints, foreign XOR parents, flipped XOR literals, nonempty final export, and a flipped original source literal. The binary prints a checking-failed diagnostic for each.

### Two precise interface findings

1. **COMPUTATIONAL official acceptance.** The /514 candidates are accepted by the actual pinned `cake_xlrup`, closing only the report's stated official-execution gap. This authenticates the external parsed inference sequence, not historical `R_mix341` legality.
2. **PROVED/RESTRICTED exact-byte provenance gap, computationally witnessed.** The XNF grammar ignores comments. Prefixing a new comment changes the SHA-256 and complete source bytes while leaving the parsed constraints and every ID fixed; the identical proof is accepted for all six cases. Hence bare XLRUP acceptance cannot establish equality to a separately named original byte string. An external byte hash or canonicalization contract is needed if exact-byte provenance is part of the target.

### Exit-status integration hazard

Every rejected corruption also returned process exit status `0`; the checker distinguishes acceptance by printing `s VERIFIED UNSAT`, while rejection prints `c Checking failed ...` on stderr. Therefore a wrapper that accepts solely on POSIX status `0` is unsound as an integration. This is **not** a failure of the HOL soundness theorem or of the checker's logical verdict. Correct automation must require the exact verified marker and reject any checking-failed diagnostic.

### Revised claim

The initial claim is narrowed: LSPV-3/514 is now independently **COMPUTATIONAL official-checker accepted** for six finite controls, and its strict external `2h` construction is strengthened at that external scope. It still is not a historical `R_mix341` upper bound because the four-hint-to-paid-binary simulation is OPEN. Exact source-byte identity is not supplied by the XLRUP grammar, and status-only process wrappers are unsafe. No superpolynomial full-mixed lower bound, B1/B2, or noncircular B3 follows.

## Resource ledger

The executable SHA-256 is `d6071f76a63eb7d3fcb091a7a7e6f86da0fd14b2780db2b7477d51edad6a86de`; raw JSON SHA-256 is `eb773131d688d57b93744f4f29379e0e0a1eedb7240a07106ec7248171f0dffe`.

- logical external records across the six baselines: 388; baseline source+proof evidence: 24,983 bytes;
- 48 isolated checker invocations; deterministic construction, no proof search or failed policies;
- measured replay wall time about 0.06 s, child CPU about 0.04 s, peak child RSS about 14 MiB in this container;
- parsing, source/index reads, construction, verification, corruption generation, output and recomputation are included in the Python run; no retained checker cache or cross-process proof state;
- assembly retrieval/build are separate one-time phases: 1,834,494-byte assembly, 9,636-byte C runtime, 1,219,416-byte static binary;
- proof minimum work, critical-path depth, and a realizable machine schedule remain distinct. The `$2h$` count is external logical-record work, not historical paid work and not runtime.

## Publication boundary and next gap

Artifacts:

- `experiments/review/lspv5_446_official_xlrup_audit.py`;
- `experiments/review/raw/2026-11-08_1603_LSPV5_446_OFFICIAL_XLRUP_RAW.json`;
- `research/coordination/2026-11-08_1603_LSPV5_OFFICIAL_XLRUP_446_HANDOFF.md`.

Precise next gap: either exhibit a legal paid original-source-authenticated historical simulation of each four-source `i x` conversion, including exact accepted bytes and provenance, or prove that no such polynomial simulation exists across **all** fixed legal rules. Separately, B3 still needs a noncircular same-calculus reflection/p-simulation bridge. P versus NP remains OPEN.

<!-- END_OF_VERIFIED_REPORT::LSPV-5::OFFICIAL-XLRUP-SOURCE-BINDING-REFEREE446 -->
