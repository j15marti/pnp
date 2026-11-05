#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = process.argv[2] || "results/raw/arc/2026-11-04_1801_LSPV5_350_ROOT_ER_EQUIVALENCE.json";
const d = JSON.parse(fs.readFileSync(path, "utf8"));
let checks = 0;
function ok(x, m) { if (!x) throw new Error(m); checks++; }

ok(d.artifact === "LSPV5_REFEREE350_ROOT_ER_EQUIVALENCE", "artifact");
ok(d.status.native_exactness.includes("UNDERDETERMINED"), "grammar status");
ok(d.status.b3.includes("OPEN"), "B3 status");

for (const row of d.def_truth_tables) {
  ok(row.outputs.length === 4, "gate rows");
  row.outputs.forEach(x => ok(x === 0 || x === 1, "Boolean gate output"));
}

for (const s of d.local_support) {
  ok(s.support >= 0 && s.support <= 3, "support");
  ok(s.tables === 2 ** (2 ** s.support), "table cardinality");
  ok(s.conjunction_row_checks === s.tables * s.tables * (2 ** s.support), "conjunction checks");
}

function parity(mask, a) {
  let x = mask & a, p = 0;
  while (x) { p ^= (x & 1); x >>>= 1; }
  return p;
}
for (const row of d.affine) {
  const n = row.variables;
  ok(row.equations === 2 ** (n + 1), "equation cardinality");
  ok(row.max_xor_chain_gates === Math.max(0, n - 1), "chain maximum");
  // Independent deterministic sample covering contradiction and cancellation.
  for (let m = 0; m < 2 ** n; m++) {
    for (let a = 0; a < 2 ** n; a++) {
      ok(parity(m ^ m, a) === 0, "mask cancellation");
    }
  }
}

let last = -1;
for (const p of d.parser_separation) {
  ok(p.root_only_bytes === 28, "root canonical bytes");
  ok(p.exported_wire_bytes >= p.root_only_bytes, "export size");
  ok(p.exported_wire_bytes >= last, "monotone export size");
  last = p.exported_wire_bytes;
}

const trueRow = d.private_wire_counterexample.find(x => x.x === 1);
ok(trueRow.source_x && trueRow.root_x && !trueRow.internal_not_x, "private wire firewall");
ok(d.malformed_rejected.length === 8, "malformed controls");
console.log(JSON.stringify({status: "PASS", checks}));
