#!/usr/bin/env node
"use strict";

const fs = require("fs");
const p = "results/raw/arc/lspv5_328/local_convert_root_quotient_referee328.json";
const d = JSON.parse(fs.readFileSync(p, "utf8"));
let checks = 0;
function ok(x, m) { if (!x) throw new Error(m); checks++; }

ok(d.artifact === "LOCAL-CONVERT-ROOT-QUOTIENT-REFEREE328", "artifact");
ok(d.root_functions === 256, "root functions");
ok(d.antecedent_target_pairs === 65536, "pair count");
ok(d.semantic_jump_control.satisfiable_x_to_false === "rejected", "semantic jump");
ok(d.semantic_jump_control.false_to_false === "legal", "empty predecessor");
ok(d.k4.odd_models === 0 && d.k4.even_models === 8, "K4 labels");
ok(d.malformed_rejected === 8, "malformed");
for (const r of d.sensitivity) {
  ok(r.sensitive_constant_bits === r.k, "sensitivity");
  ok(r.gate_records === 2 * r.k + 1, "gate records");
  ok(r.paid_nodes === 2, "paid skeleton");
}
ok(d.checks === 67850, `producer checks ${d.checks}`);
console.log(JSON.stringify({artifact: d.artifact, independent_checks: checks, pass: true}));
