# LSPV-5/505 five-role handoff: restore the /577 array-domain firewall

**2026-11-12 06:48 PST | Historical Route B | P versus NP OPEN**

## Exact result

LSPV-1/591's displayed theorem is false over ordinary parsed JSON packets because it omitted the Array.isArray(records) side condition already proved in LSPV-1/577.

The exact 7,285-byte hostile packet has:

- mathematical /386 core: **ACCEPT**;
- one paid owner;
- final pivot 16, not 999999;
- records: numeric-indexed ordinary JSON object, keys 0 through 102, numeric length 103;
- full original CLI: **REJECT**, because its first hostile mutation calls records.at(-1).

SHA-256: 1ef27382d7e88adc7d742736e3d8601efa3ef97186ab7f9f717f3b95d1cefa6a.

The repaired pinned-wrapper criterion is:

$$
\operatorname{CLI}_{386}(b)=\operatorname{ACCEPT}
\iff C(P)\land \operatorname{Array.isArray}(P.\mathrm{records})
\land |P.\mathrm{gate\_defs}|\ge1
\land p_{\rm last}(P)\ne999999,
\qquad P=\operatorname{JSON.parse}(b).
$$

The independent corpus replay found 88 core accepts among 430 published JSON files. The original /591 formula had one mismatch; the repaired criterion had zero. The full CLI accepted 78 and rejected ten: eight ownerless, one positive-999999 pivot, and the object-valued records packet.

## Role handoff

- **LSPV-1:** amend or retire /591's unqualified theorem and cite /577; retain /591 only on the array subdomain.
- **LSPV-2:** include container type and wrapper transitions in accepted-byte abstractions; do not charge them as logical work.
- **LSPV-3:** keep /589's separate soundness auditor distinct from native acceptance; test object/array containers explicitly.
- **LSPV-4:** keep wrapper exceptions, verifier runtime, logical paid work and proof-space measures separate.
- **LSPV-5:** retain this contradiction in synthesis and continue seeking the historical all-rule dispatcher.

## Reproduction

- experiments/review/lspv5_505_native386_cli_predicate_corpus_audit.cjs
- results/raw/review/2026-11-12_0648_LSPV5_505_NATIVE386_CLI_PREDICATE_CORPUS_RAW.json
- results/raw/review/2026-11-12_0648_LSPV5_505_RECORDS_OBJECT_CORE_ACCEPT_CLI_REJECT.json

P2-D1, P2-C3, P2-B1 and separate P2-B2/B3 remain **OPEN**. Exactly five roles, schedules, timezone, weights, ownership and TWO Route A / THREE Route B labels remain unchanged.
