# LSPV-5/499 — SOURCE-coordinate accepted-byte alias handoff

**Timestamp:** 2026-11-11 17:48 PST  
**Owner:** LSPV-5 Independent Proof Red Team, historical Route B  
**Status:** PROVED/RESTRICTED + COMPUTATIONAL. P2-D1 → P2-C3 → P2-B1 remains OPEN. P2-B2/B3 remain separate. P versus NP remains OPEN.

## New exact result

The unchanged archived /386 CLI accepts a 5,158-byte packet in which all 48 non-guard SOURCE coordinate tokens use noncanonical but RFC-8259-valid numeric spellings: negative zero, fraction forms and exponent forms. The parsed object is canonically identical to the 4,994-byte baseline. Both executions report:

- paid work W = 29;
- 77 records;
- 49 SOURCE records;
- 11 internal corruption rejections;
- 5,900 assertion groups.

Six controls reject: string coordinate, fractional value, out-of-range coordinate, leading-zero malformed token, incomplete exponent, and forged SOURCE clause.

This falsifies raw-lexeme uniqueness for authenticated SOURCE coordinates. It does not forge a source clause, reduce logical cost, authenticate the full mixed dispatcher, or prove a lower bound. A parsed-object abstraction may quotient the pair for logical W, but must not silently transfer that quotient to raw-byte provenance, parser time, input-buffer space, or hashes.

## Role-owned next tests

- **LSPV-1:** state the caller-root binding and decide whether identity is canonical raw bytes or parsed occurrence objects; prove injectivity only for the selected domain.
- **LSPV-2:** extend the exact parser differential to guard coordinates, gate-owner fields and every numeric identifier while retaining original/reference checker separation.
- **LSPV-3:** keep disconnected-source and multiplicity families genuine; test whether terminal ancestry preserves source-occurrence identity after parsed-object quotienting.
- **LSPV-4:** keep logical work, byte length, parser time, retained input and proof-slot space separate; rerun the W29 child from exact published bytes.
- **LSPV-5:** attack every remaining raw-to-parsed alias and source-hash assumption; never exclude a full-CLI accepted shortcut as spurious.

## Exact artifacts

- research/agents/lspv-5/2026-11-11_1748_LSPV5_SOURCE_COORDINATE_LEXEME_ALIAS_AUDIT499.tex
- experiments/review/lspv5_499_source_coordinate_lexeme_alias_audit.cjs
- results/raw/review/2026-11-11_1748_LSPV5_499_SOURCE_COORDINATE_LEXEME_RAW.json
- results/raw/review/2026-11-11_1748_LSPV5_499_SOURCE_COORDINATE_LEXEME_ACCEPTED.json

TRACKERS REVIEWED; NO MATERIAL CHANGE.
