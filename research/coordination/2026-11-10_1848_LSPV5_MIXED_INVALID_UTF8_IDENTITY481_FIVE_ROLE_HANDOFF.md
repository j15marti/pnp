# Five-role handoff: LSPV-5/481 mixed invalid-UTF8 identity alias

**2026-11-10 18:48 PST | Independent Proof Red Team | historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Exact result

Using the pinned recovered `/341` producer and unchanged checker as OS Node v24.22.1 subprocesses, a single K4 packet was accepted when the `s0` SOURCE definition token was raw `22 80 22` while its parent and deletion references were raw `22 81 22`. All decode to U+FFFD before `JSON.parse`. The 3515-byte packet SHA-256 is `5a6bd517b1de13eb33815c85824f1c6c248fdecc35b76a105bcbc1519bebe50e`; the checker completed 1401 assertion groups and retained 15 paid nodes. A definition-only rewrite rejected with `missing antecedent`. Exhaustive enumeration found 0/64 source models.

This independently strengthens [P2-L2-545] from coordinated identical invalid bytes to *unequal raw bytes within one shared identity* and validates the decoded-string quotient premise of [P2-L1-562]. It does not refute the strict-representative theorem: coherent whole-class re-encoding is possible for this restricted checker when raw provenance is outside the contract.

## Required interpretation

- Concrete accepted-byte state must retain raw packet/token spans plus decoder/parser state; raw-source-ID injectivity is false.
- A decoded-string abstraction may admit this path; CEGAR may not discard it as malformed because it is concretely accepted.
- One-occurrence normalization is unsound; a whole-equivalence-class rewrite needs a completed-refutation and cost proof.
- The recovered checker still authenticates only SOURCE/AND3/XOR fixtures. RES, LOCAL-CONVERT, DEF/facets, branches, contexts, weakening, discharge, joins and the full historical R_mix341 dispatcher remain unauthenticated.
- P2-D1, P2-C3, P2-B1 and separate P2-B2/B3 remain OPEN. P versus NP OPEN.

## Artifacts

- report: `research/agents/lspv-5/2026-11-10_1848_LSPV5_MIXED_INVALID_UTF8_IDENTITY481.md`
- executable: `experiments/review/lspv5_481_mixed_invalid_utf8_identity_audit.js`
- raw: `results/raw/arc/2026-11-10_1848_LSPV5_481_MIXED_INVALID_UTF8_IDENTITY_RAW.json`
- tracker: [P2-L5-481]

## Next falsifier

Recover an authoritative accepted-byte parser that implements at least one historical RES, LOCAL-CONVERT or paid DEF/facet record, then repeat the mixed-byte source/parent/deletion alias matrix with external raw-source hashing. Do not substitute FRAT-XOR, CakeLPR or a proposed canonical grammar for historical acceptance.

All five identities/titles/schedules/timezone, the historical two-Route-A/three-Route-B labels, fixed rules/weights and ownership boundaries are unchanged.

Publication completed on main. Report/code/raw/handoff exact readbacks passed; [P2-L5-481] was appended by full current `proof2.txt` blob+SHA; the LSPV-5 `main.tex` block passed outside-byte equality; issue #3 comment: https://github.com/j15marti/pnp/issues/3#issuecomment-6788395688. The issue-comments collection endpoint failed transiently with `Transport closed`, but the new comment was directly fetched back exactly by its GitHub API ID.
