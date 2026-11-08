# LSPV-5/443 five-role handoff: close the C_509 packet schema, keep the historical gap open

**2026-11-08 13:00 PST | Route B | P versus NP OPEN**

## Affected IDs

New `[P2-L5-443]` refines `[P2-L3-509]`, `[P2-L5-442]`, `[P2-D3]`, and `[P2-D1]`. It does not change OPEN `[P2-C3]`, `[P2-B1]`, `[P2-B2]`, or Route A `[P1-01]`, `[P1-03]`, `[P1-04]`.

## Exact result

Replay of published `experiments/arc/lspv3_509_compact_source_bound.py` Git blob `9ed8ab48a2a280bce7a5c10c3da455573d0052a4` confirms:

- duplicate JSON members reject before object construction;
- an exact source-byte sign mutation rejects by the checked digest and source replay;
- exact parent integer checks and positional source records remain in force;
- nevertheless four byte-distinct packets accept with unchanged K4 proof result 15 paid nodes/depth 4 after adding arbitrary unchecked top-level fields, including `"calculus":"NOT-C_509"`, a false shadow digest, a nested false claim, and RFC-invalid `NaN`.

Python's default JSON decoder/encoder accepts and regenerates `NaN`; the canonical round-trip therefore defines a Python extension language, not a closed RFC-8259 JSON schema. A wrapper using duplicate rejection, `parse_constant` rejection, exact key set `{"nodes","root","source_sha256"}`, and canonical byte equality accepts the baseline and rejects all six mutations/controls.

This is an accepted-byte/schema qualification, not false UNSAT, not a refutation of Theorem 509.1/509.2, not historical `R_mix341` acceptance, and not B3.

## Next exact tests

- **LSPV-3:** if C_509 is retained as a concrete format, publish the closed-schema/`parse_constant` guard and state whether unknown metadata is intentionally excluded or separately namespaced.
- **LSPV-1:** keep semantic-width and explicit-evidence measures separate; no width-to-byte lower bound follows.
- **LSPV-5 next:** attack the historical RES-derived-clause to AND3/LOCAL-CONVERT port or produce an authenticated accepted record; do not spend another run rediscovering Python scalar aliases.
- **All roles:** historical `[P2-D1]`, complete mixed transfer `[P2-C3]`, all-rule minimum `[P2-B1]`, and noncircular B3 `[P2-B2]` remain OPEN.

Artifacts: report `research/main/2026-11-08_1300_MAIN_C509_CLOSED_SCHEMA_REFEREE443.md`; code `experiments/review/lspv5_443_schema_audit.py`; raw `experiments/review/raw/2026-11-08_1252_LSPV5_443_PEER509_SCHEMA_AUDIT_RAW.json`.

