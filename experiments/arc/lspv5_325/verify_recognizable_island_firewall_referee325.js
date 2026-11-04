#!/usr/bin/env node
"use strict";
const fs = require("fs");
const p = "results/raw/arc/lspv5_325/recognizable_island_firewall_referee325.json";
const d = JSON.parse(fs.readFileSync(p, "utf8"));
let checks = 0;
function ok(x, m) { checks++; if (!x) throw new Error(m); }
ok(d.id === "REFEREE325", "id");
ok(d.theorem_anchor.system === "ordinary unrestricted shared-DAG Resolution", "model");
ok(d.theorem_anchor.quantifiers.includes("forall h>=h0 forall Resolution refutations"), "quantifiers");
ok(d.counterexample.encoder.includes("one fixed"), "uniform fixed encoder");
ok(d.counterexample.consequence.includes("=1"), "one-step target");
ok(d.algorithm_corollary.classification.includes("B1 fails"), "B classification");
ok(d.fixtures.length === 9, "fixture count");
const hard = d.fixtures.filter(x => x.branch === "hard_island");
const benign = d.fixtures.filter(x => x.branch === "benign");
ok(hard.length === 3, "hard branches");
ok(benign.length === 6, "benign branches");
for (const x of hard) {
  ok(x.label === "UNSAT", "hard label");
  ok(x.models === 0, "hard models");
  ok(x.resolution_output_cost === 1, "hard proof cost");
  ok(x.encoded_clauses === x.source_clauses + 2, "two units");
}
for (const x of d.fixtures.filter(x => /^PHP_\d+\^\d+$/.test(x.name) && x.label === "SAT")) {
  ok([1,2,6].includes(x.models), "SAT model count");
  ok(x.encoded_clauses === x.source_clauses + 1, "benign unit");
}
ok(d.compiler_checks === 54, "compiler checks");
ok(d.tseitin_control.odd_models === 0, "odd Tseitin");
ok(d.tseitin_control.even_models === 8, "even Tseitin");
ok(d.malformed_rejected === 10 && d.malformed_total === 10, "malformed");
ok(d.statuses.broad_common_envelope === "FALSIFIED", "envelope status");
ok(d.statuses.proof_carrying_model_relative_envelope === "OPEN", "repair status");
ok(d.statuses.Rmix341_superpolynomial_hardness === "OPEN", "mixed hardness");
ok(d.statuses.B3_Rmix341 === "OPEN", "B3");
ok(d.statuses.P_vs_NP === "OPEN", "P vs NP");
console.log(JSON.stringify({status:"PASS", checks}));
