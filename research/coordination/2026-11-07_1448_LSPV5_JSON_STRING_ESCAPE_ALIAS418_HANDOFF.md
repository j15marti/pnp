# LSPV-5/418 five-role handoff: JSON string escape aliases

**2026-11-07 14:48 PST | Route B red team | `[P2-D1]`, `[P2-D3]`, `[P2-L5-418]` | P versus NP OPEN.**

## Result

The exact recovered `/341` checker accepts six byte-distinct packets in which literal proof-critical strings are replaced by Unicode-escaped spellings with the same decoded value:

- source ID `s0` at its definition and a parent reference;
- derived ID `d0` at its definition and a parent reference;
- object-member names `id` and `parents`.

Every acceptance reproduced the baseline checker-output hash. Four ID controls decoding to `x0`, two member-name controls decoding to `jd`/`qarents`, and malformed `\uZZZZ` all rejected. Independent raw-token verification rejected all 13 noncanonical/malformed packets; 34 assertions passed.

## Scope and repair

RFC 8259 makes equal-decoding string equality standard JSON behavior. Therefore this is a raw-byte provenance/canonical-language gap, not a logical JSON-object soundness failure by itself. Canonical globally unique string IDs repair numeric aliasing only when the language also fixes canonical raw serialization. Combine:

1. duplicate decoded-name rejection `[P2-L5-417]`;
2. canonical raw string spelling `[P2-L5-418]`;
3. globally unique string IDs `[P2-L5-415/416]`;
4. affine coordinate validation `[P2-L5-414]`.

All are proposed parser repairs pending historical authority. No RES/LOCAL-CONVERT/DEF/branch/discharge syntax is authenticated, no proof is shortened, and `[P2-C3]`, `[P2-B1]`, `[P2-B2]` remain OPEN.

## Reproduction

```bash
python experiments/review/lspv5_418_json_string_escape_alias.py
node experiments/review/verify_lspv5_418_json_string_escape_alias.mjs
```

Expected: Python 13 cases (6 accept/7 reject); Node 34 assertions; baseline stdout SHA-256 `af477923155e6e4340a643a4df5b437751b443f03993bbc04dbe73c8587bf7be`.

## Next exact target

Locate historical bytes/specification establishing whether packet identity is canonical raw bytes or decoded JSON objects. If canonical bytes are intended, test the combined strict parser against authenticated records for every historical rule. Do not infer full mixed hardness or B3 from this parser result.
