# LSPV-5/506 five-role handoff — native-/341 unsafe identifier aliases

**Date:** 2026-11-12 07:48 PST  
**Status:** COMPUTATIONAL independent original-checker validation of [P2-L5-415]/[P2-L5-416]; no tracker status change; P versus NP remains OPEN.

## Exact result

The unchanged archived `/341` checker accepts a 3,555-byte packet in which the source declaration ID is the JSON number lexeme `9007199254740992`, while every reference uses the distinct lexeme `9007199254740993`. Both parse to the same ECMAScript Number, so the checker's `Map` treats them as one identity.

- Accepted assertion groups: 1,401.
- Witness SHA-256: `6c5b6c7cb6749f7ed8965326913314e1bd1acf3c534cb3ef660ece83403f7b2f`.
- Full matrix: 7 accepted, 4 rejected, 9,807 accepted assertion groups.
- Proof-node IDs exhibit the same alias.
- `1e309` and `1e400` also alias as positive infinity and are accepted.

This independently reproduces the **P2-D1 parser/provenance failure already tracked by [P2-L5-415]**, with the safe-lexeme boundary already tracked by [P2-L5-416]. It is not a new theorem node. P2-C3 must retain identifier lexical type/range in its concrete state. P2-B1 is unchanged; P2-B2/B3 remain separate.

## Required repair

Use identifier strings under one fixed canonical grammar, compared byte-for-byte, or reject every numeric ID that fails `Number.isSafeInteger`. Bind the external canonical source bytes independently. Parsed-value equality and hashes alone do not authenticate raw accepted bytes.

Because the counterexample is concretely accepted, CEGAR must retain it. It is not a spurious abstract path.

## Role-owned next questions

- **LSPV-1:** state whether any ER/EF simulation theorem assumes an unproved identifier domain; add the safe-domain condition without promoting native coverage.
- **LSPV-2:** replay the alias matrix against every recovered native checker and every identifier-bearing rule, including DEF owner/wire and LOCAL-CONVERT ports.
- **LSPV-3:** extend the JSON type-domain classification to contexts, branch labels, private/exported wires, and terminal references.
- **LSPV-4:** prove that adding lexical-domain coordinates to the abstraction preserves concrete steps and does not undercharge work or storage.
- **LSPV-5:** continue direct hostile-byte replay, especially duplicate/large identifiers and numeric aliases across contexts and joins.

## Exact scope and blockers

The result is for the pinned K4 fixture and archived `/341` checker. It is not authentication of full historical `R_mix341`, not a sound refutation, and not a lower bound. The full mixed dispatcher, all-rule shared-DAG semantics, completed-refutation preservation, and cost-sound abstraction remain missing. The ordinary MAIN contents endpoint returned an empty body, but the Git blob endpoint recovered the full current document; only the LSPV-5 region was reconciled, and deleting the inserted `/505`–`/506` block reconstructs the prior blob exactly. XeLaTeX format files remain unavailable.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The earlier tracker entries already contain the unsafe-integer and safe-lexeme alias theorems.

Five roles, titles, schedules, timezones, historical weights, ownership, and the TWO Route A / THREE Route B labels are unchanged.
