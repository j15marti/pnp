#!/usr/bin/env node
// Independent REFEREE363 control: ordinary JSON.parse uses binary64 Number.

const aText = '{"nvars":9007199254740992,"id":9007199254740992}';
const bText = '{"nvars":9007199254740993,"id":9007199254740993}';
const a = JSON.parse(aText);
const b = JSON.parse(bText);

const result = {
  format: "LSPV5-JSON-NUMBER-COLLISION-REFEREE363-1",
  parsed_values_equal: a.nvars === b.nvars && a.id === b.id,
  parsed_a: a,
  parsed_b: b,
  stringify_equal: JSON.stringify(a) === JSON.stringify(b),
  lexical_bigint_equal:
    BigInt(aText.match(/"nvars":([0-9]+)/)[1]) ===
    BigInt(bText.match(/"nvars":([0-9]+)/)[1]),
  conclusion:
    "JSON numeric identifiers are not cross-language exact unless arbitrary-precision token semantics are mandated; canonical decimal strings repair this.",
};

console.log(JSON.stringify(result, null, 2));
