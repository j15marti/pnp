#!/usr/bin/env node
import fs from "node:fs";

const path = process.argv[2];
if (!path) throw new Error("usage: node verify_lspv5_401_clone_disjointization.mjs result.json");
const data = JSON.parse(fs.readFileSync(path, "utf8"));
let checks = 0;
const ok = (condition, message) => {
  checks++;
  if (!condition) throw new Error(message);
};

ok(data.status === "PASS", "status");
ok(data.scope.includes("not an authoritative checker"), "scope disclaimer");
for (const row of data.rows) {
  const m = row.m;
  ok(row.original_overlap_edges === m * (m - 1) / 2, `original K_${m}`);
  ok(row.cloned_gate_overlap_edges === 0, `cloned gates disjoint ${m}`);
  ok(row.equality_extension_overlap_edges === m * (m - 1) / 2, `equalities K_${m}`);
  ok(row.max_disjoint_equality_extensions === 1, `max equality independent set ${m}`);
  ok(row.truth_table.assignments_with_equalities === 2 ** (m + 1), `with equality count ${m}`);
  ok(row.truth_table.assignments_without_equalities === 2 ** (2 * m + 1), `without equality count ${m}`);
  ok(row.truth_table.mismatch_count_without_equalities > 0, `semantic mismatch ${m}`);
  const {x, y, original, cloned} = row.truth_table.first_mismatch;
  const expectedOriginal = x.slice(1).map(v => x[0] & v);
  const expectedCloned = x.slice(1).map((v, i) => y[i] & v);
  ok(JSON.stringify(original) === JSON.stringify(expectedOriginal), `original witness ${m}`);
  ok(JSON.stringify(cloned) === JSON.stringify(expectedCloned), `clone witness ${m}`);
  ok(JSON.stringify(original) !== JSON.stringify(cloned), `witness differs ${m}`);
}
for (const [k, value] of Object.entries(data.telescoping_identity)) {
  ok(value === true, `telescoping ${k}`);
}
ok(data.malformed_controls.valid_large_ids === true, "large IDs accepted");
for (const key of ["duplicate_clone_output", "nonfresh_clone_output", "missing_equality", "unknown_equality_target"]) {
  ok(data.malformed_controls[key] === false, `${key} rejected`);
}
console.log(JSON.stringify({status:"PASS", checks, rows:data.rows.length}));
