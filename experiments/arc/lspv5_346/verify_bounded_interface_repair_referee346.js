#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const root = path.resolve(__dirname, "../../..");
const rawPath = path.join(root, "results/raw/arc/2026-11-04_1445_LSPV5_346_BOUNDED_INTERFACE_REPAIR.json");
const bytes = fs.readFileSync(rawPath);
const data = JSON.parse(bytes.toString("utf8"));
let checks = 0;
function ok(x, msg) { if (!x) throw new Error(msg); checks++; }

ok(data.run === "REFEREE346", "run id");
ok(data.status.bounded_named_interface_repair === "PROVED_RESTRICTED", "status");
ok(data.status.B1 === "OPEN" && data.status.B2 === "OPEN" && data.status.B3 === "OPEN", "bridges open");
ok(data.status.P_vs_NP === "OPEN", "pnp open");

for (const row of data.random_resolution_closure.samples) {
  ok(row.proper_clause_bound === 3 ** row.b, "3^b bound");
  ok(row.max_added_resolution_nodes_observed <= row.proper_clause_bound, "observed closure bound");
  ok(row.samples > 0, "samples positive");
}
ok(data.random_resolution_closure.sat_instances > 0, "SAT controls");
ok(data.random_resolution_closure.unsat_instances > 0, "UNSAT controls");
ok(data.random_resolution_closure.entailed_clauses_checked > 0, "entailed clauses");

for (const row of data.unbounded_origin_support_atomic_repair) {
  ok(row.transitive_original_support >= 4, "growing support");
  ok(row.named_interface === 1 && row.repair_nodes === 1, "atomic repair");
}
for (const row of data.guarded_php_tiny_output_firewall) {
  ok(row.conclusion_named_support === 1, "tiny output support");
  ok(row.gamma_models > 0 && row.z_false_models === 0, "Gamma entails z");
  ok(row.source_deletion_z_false_witnesses === row.guarded_clauses, "deletion controls");
}
for (const row of data.shared_fanout) {
  ok(row.shared_dag_repair_nodes === 1, "shared once");
  ok(row.tree_unfolded_repair_nodes === row.fanout, "tree copies");
  ok(row.dependency_references === row.fanout, "references charged separately");
}
for (const row of data.parity_countercontrol) {
  ok(row.dense_cnf_blockers === 2 ** (row.b - 1), "parity blockers");
  ok(row.compact_xor_rows === 1, "one XOR row");
  ok(row.compact_xor_serialized_bits_upper === 2 * row.b + 1, "XOR bits");
}
for (const row of data.logarithmic_thresholds) {
  ok(row["3^b"] <= row.M, "log threshold");
}
ok(data.malformed.tested === data.malformed.rejected, "malformed rejected");
ok(data.assertions > 1000, "producer assertion floor");

console.log(JSON.stringify({
  verifier: "REFEREE346-independent-js",
  checks,
  raw_sha256: crypto.createHash("sha256").update(bytes).digest("hex")
}, null, 2));
