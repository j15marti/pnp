# LSPV-5/481: mixed ill-formed UTF-8 aliases inside one accepted shared SOURCE identity

**2026-11-10 18:48 PST | Independent Proof Red Team | historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Affected chain:** [P2-D1] -> [P2-C3] -> [P2-B1]. [P2-B2]/B3 are separate and remain OPEN. No grammar, weight, role, schedule, timezone, route label, task identity or ownership boundary is changed.

## IDEA: target and preregistered falsifiers

**Target claim.** A lossless byte-span normalizer can convert every recovered-checker-accepted SOURCE identifier representation into a strict typed fragment without changing source binding, parent identity, verdict or paid cost.

Four falsifiers were fixed before the search and experiment:

1. two decoded-equivalent Unicode spellings bind to different raw provenance;
2. a duplicate or aliased key changes the active definition span;
3. normalization creates an identity collision or a dangling parent;
4. invalid UTF-8 or noncanonical numbers lack a total verdict-preserving rewrite.

The exact test below realizes a sharper form of falsifier 1: *inside one packet*, the SOURCE definition and its live references use different raw invalid octets, but the original checker accepts because decoding quotients both to the same JavaScript string.

## SEARCH: authenticated scope, peer precedence and external controls

I read the complete current root `proof1.txt` and `proof2.txt`, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, the governing handoffs, and issue #3 through the latest comment set returned before the final publication phase. A later comments refetch twice failed with `Transport closed`; current peer state was therefore also checked directly from repository files. Relevant exact tracker IDs are [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1], [P2-B2], [P2-L2-545], [P2-L2-546], [P2-L3-559], [P2-L4-532] and [P2-L1-562].

Authenticated original restricted artifacts:

- producer `experiments/arc/lspv2_341_mixed_tseitin_min_dag.js`, Git blob `4081022e8a3841d79f751a3d3a7a10decbb026da`;
- checker `experiments/arc/lspv2_341_independent_verify.js`, Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`;
- historical mathematical declaration `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`.

The checker is authoritative only for the recovered fixed SOURCE/AND3/XOR fixture language. LSPV-3/559 proves its paid dispatcher has only AND3 and XOR; it does not authenticate historical RES, LOCAL-CONVERT, paid DEF/facets, branches, contexts, weakening, discharge or joins. LSPV-2/545 established acceptance when all occurrences use one invalid byte; LSPV-2/546 identified the distinct BOM/default-`TextDecoder` mismatch. LSPV-1/562 subsequently proved that replacement-decoding and re-encoding gives a strict UTF-8 representative for this restricted checker when no external raw-byte provenance is required. LSPV-4/532 separately bounds a proposed canonical test grammar, not the historical complete calculus.

The present run is not a new normalization theorem. It supplies the missing hostile *within-packet mixed-alias* replay and independently validates the decoded-string quotient premise of [P2-L1-562] using an unchanged checker subprocess.

Primary and required-corpus review:

- Node.js `Buffer` documentation specifies replacement decoding for invalid UTF-8; the WHATWG Encoding Standard separately exposes fatal versus replacement error modes. These are decoder semantics, not proof-complexity lower bounds.
- Cook--Reckhow (1979) supplies the fixed proof-system discipline; Cousot--Cousot (1977) supplies approximation-polarity discipline. Neither authenticates this historical parser.
- `meelgroup/frat-xor` documents a separate FRAT-XOR -> XLRUP elaboration and CakeML checker pipeline; `tanyongkiam/cake_lpr` documents a separate LPR/LRAT checker and explicit heap/stack limits. Neither is accepted-byte evidence for R_mix341.
- `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` explicitly restricts its proved claims to stated families and leaves unrestricted P versus NP open.
- `konard/p-vs-np/scripts/proof_status.json` inventories formal theorem names/axioms but contains no historical R_mix341 byte parser.
- Actual Grok `GROKPROOF/2026-11-11_0315_PROGRESS.md` and actual Claude `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` were located and reviewed for the native-grammar gap; neither supplies the missing full dispatcher.
- Google Drive searches for the checker/parser and R_mix341 grammar returned no matching source.

## ITERATE: exact accepted-byte experiment

The script runs the pinned producer in OS Node v24.22.1, extracts its K4 fixture, verifies the two Git blob hashes, and invokes the unchanged pinned checker as a separate OS process. The three JSON string tokens that originally spell `"s0"` occur at byte offsets 125 (SOURCE definition), 1075 (live parent) and 2587 (deletion witness).

The hostile packet replaces:

- definition token with raw bytes `22 80 22`;
- parent token with raw bytes `22 81 22`;
- deletion token with raw bytes `22 81 22`.

Node decodes each invalid single byte to U+FFFD before `JSON.parse`; consequently all three decoded identifiers are the same string even though their raw token bytes differ.

| Case | Bytes | SHA-256 | Strict UTF-8 | Checker | Assertions |
| --- | ---: | --- | --- | --- | ---: |
| baseline | 3518 | `fd6c0b8915dc1d72264d757c68629feded3d6edd53af8fa6d693aaa86db09a19` | yes | ACCEPT | 1401 |
| definition `0x80`, refs `0x81` | 3515 | `5a6bd517b1de13eb33815c85824f1c6c248fdecc35b76a105bcbc1519bebe50e` | no | **ACCEPT** | 1401 |
| all three `0x80` control | 3515 | `c2ad8fb4162fcd8c052243670c020d884c24a3f82618c1704b8353b047a9b020` | no | ACCEPT | 1401 |
| definition-only `0x80` control | 3517 | `bb55e8ce7e5a2228bb6ba20ac9990d3b9fb554961205d73a3a0d763fecfb1a04` | no | REJECT: missing antecedent | n/a |

The independent semantic control exhaustively enumerated all 64 assignments of the six-variable, 16-clause K4 source and found zero models. The proof has 15 paid nodes. Thus this is not a forged-SAT-source acceptance result: it is an exact representation/provenance result for a genuinely UNSAT fixture.

### Restricted theorem 481.1

For the pinned recovered `/341` checker, equality of raw byte spans is **not necessary** for a shared SOURCE identity: a definition occurrence containing raw `0x80` and reference occurrences containing raw `0x81` are accepted as one identity after replacement decoding. Therefore any concrete configuration intended to model exact accepted bytes must include the raw packet, decoder state/policy, decoded string and token spans. A raw-byte-injective SOURCE-identity invariant is false for this checker.

### CEGAR and abstraction polarity

Let a concrete configuration retain `(raw, decoder, decoded, parser, sourceMap, liveMap, pc, paid, verdict)`. The quotient abstraction may map identifiers to decoded JavaScript strings, but only under a proved decoder/parser transformer and only if external provenance is not defined over raw bytes. Its concretization for one decoded U+FFFD identifier contains multiple raw strings and mixed occurrence assignments.

This hostile packet is a genuine concrete accepted path, so CEGAR must **not** refine it away merely because it is ill-formed UTF-8. A strict representative construction may replace the whole decoded-equivalence class coherently; the dangling-parent control proves that independently rewriting only the defining occurrence is not verdict preserving. Completed-refutation preservation and `cost# <= cost_concrete` still require a separate proof. External source hashing over raw bytes remains outside [P2-L1-562] and outside this run.

No abstract-state cardinality is interpreted as physical memory. No proof-DAG work is interpreted as live machine space. No nondeterministic verifier is converted into a deterministic UNSAT decider.

## Resource ledger

- **Logical proof work:** 15 distinct paid inference nodes in every accepting K4 case; unchanged by representation aliases.
- **Explicit input/evidence:** 3515 bytes for the hostile packet; the raw JSON result retains its complete 4688-character base64 encoding.
- **Construction:** pinned producer execution, fixture selection, three byte-span substitutions and two SHA/Git-blob checks.
- **Parsing/verification:** Node replacement decoding, `JSON.parse`, original checker traversal, 1401 assertion groups per accepted case.
- **Independent source control:** 64 complete assignments tested against 16 clauses.
- **Output/cache:** JSON rows, hashes, stderr prefix and full hostile bytes. Temporary packets are removed after replay.
- **Peak live space:** packet bytes, decoded string/object, checker maps and output coexist in the subprocess. This run measures no universal exponent and makes no RAM/FLMV transfer.
- **Search/retrieval/publication:** tracker and repository reads, required-repository reads, primary-source search, output hashing, GitHub write/readback and issue update are separately charged operational phases; none is inserted into the ideal 15-node proof minimum.

## Status and remaining gap

### Publication-stage peer delta

Four later same-evening peer artifacts were read before final issue publication. [P2-L1-563] shows that *per-parsed-ID* UTF-8 encode/decode is additionally lossy on distinct lone-surrogate identifiers, while preserving [P2-L1-562]'s whole-raw-packet theorem. [P2-L2-548] shows safe-integer ID transport and acceptance of a missing unreferenced terminal ID in the same restricted checker. [P2-L3-560] proves semantic soundness only for an explicitly external-source-bound typed under-approximation. [P2-L4-533] proves an exponential shortest-evidence-byte barrier only in its separately defined full-coordinate grammar. These are compatible with Theorem 481.1 and do not close the missing historical all-rule parser, MAY coverage or cost-transfer gap.

**Actual advance:** PROVED/RESTRICTED + COMPUTATIONAL hostile certificate showing unequal raw byte spellings can constitute one accepted shared SOURCE identity inside a single packet, with a rejecting one-sided-rewrite control and independent UNSAT replay.

**P2-D1:** still OPEN. Only the recovered SOURCE/AND3/XOR fixture checker is authenticated; the full historical accepted-byte grammar remains missing.

**P2-C3:** still OPEN. The complete all-native-rule concrete semantics, concrete-step inclusion, completed-refutation preservation and abstract-cost inequality have not been proved.

**P2-B1:** still OPEN. No all-rule superpolynomial lower bound follows. **P2-B2/B3:** separate and OPEN. P versus NP remains OPEN.

## Reproduction

Run from the repository root:

```bash
node experiments/review/lspv5_481_mixed_invalid_utf8_identity_audit.js
```

The script writes `lspv5_481_mixed_invalid_utf8_identity_raw.json` in the current repository root; the publication copy is under `results/raw/arc/`.

## Publication/readback record

This report, executable, raw evidence and handoff were read back byte-for-byte at Git blobs `9fce7e762fb447c877b8094bb2f3c80f4cce087a`, `a43f309585818ca322d6d8e84764c6420c72da50`, `3a135e7bce48aca814101f24c45e824c95140973` and `7f23bb9688c1d7f97ec88ecfc88662c0cb7dc330`, respectively. Root `proof2.txt` was changed only by the material [P2-L5-481] append using complete current content+SHA and read back once at blob `8f738a1c11f6ab94631a909dd5649e5ea4866553`; `proof1.txt` remains unchanged. Root `main.tex` was edited only inside the LSPV-5 ownership markers and read back at blob `2b335653f2e4d2582183663985d74326ed98e958`; deleting the new owned block reconstructs prior blob `55604640a49b28884a97591106f8c90ea00b51f5` exactly. Issue #3 comment `6788395688` was fetched back from the GitHub API with the complete intended body. The general issue-comments collection endpoint twice failed transiently with `Transport closed`; direct peer-file reads and direct single-comment readback were used, and this limitation is not disguised as a complete late-comment review.
