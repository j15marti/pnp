#!/usr/bin/env node
"use strict";

const fs = require("fs");
const crypto = require("crypto");
const rawPath = "results/raw/arc/lspv5_316/family_local_backtranslation_referee316.json";
const started = process.hrtime.bigint();
const data = JSON.parse(fs.readFileSync(rawPath, "utf8"));
let assertions = 0;
function check(value, message) { assertions++; if (!value) throw new Error(message); }

function php(pigeons, holes) {
  const variable = (p, h) => p * holes + h + 1;
  const clauses = [];
  for (let p = 0; p < pigeons; p++) clauses.push(Array.from({length: holes}, (_, h) => variable(p, h)));
  for (let h = 0; h < holes; h++) for (let p = 0; p < pigeons; p++) for (let q = p + 1; q < pigeons; q++) clauses.push([-variable(p, h), -variable(q, h)]);
  return {clauses, variables: pigeons * holes};
}
function models(cnf) {
  let count = 0;
  for (let mask = 0; mask < 2 ** cnf.variables; mask++) {
    const ok = cnf.clauses.every(clause => clause.some(lit => {
      const v = Boolean(mask & (2 ** (Math.abs(lit) - 1)));
      return lit > 0 ? v : !v;
    }));
    if (ok) count++;
  }
  return count;
}
function factorial(n) { let x = 1; for (let i = 2; i <= n; i++) x *= i; return x; }

for (const row of data.established_family_controls) {
  const u = php(row.unsat_pigeons, row.holes);
  const s = php(row.paired_sat_pigeons, row.holes);
  check(models(u) === 0 && row.unsat_models === 0, `PHP UNSAT h=${row.holes}`);
  check(models(s) === factorial(row.holes) && row.paired_sat_models === factorial(row.holes), `PHP SAT h=${row.holes}`);
  check(u.clauses.length === row.unsat_clauses, `PHP clause count h=${row.holes}`);
}

const edges = [];
for (let u = 0; u < 4; u++) for (let v = u + 1; v < 4; v++) edges.push([u, v]);
function tseitinModels(charges) {
  let count = 0;
  for (let mask = 0; mask < 2 ** edges.length; mask++) {
    let ok = true;
    for (let vertex = 0; vertex < 4; vertex++) {
      let parity = 0;
      edges.forEach((e, i) => { if (e.includes(vertex)) parity ^= (mask >> i) & 1; });
      ok = ok && parity === charges[vertex];
    }
    if (ok) count++;
  }
  return count;
}
check(tseitinModels([0,0,0,0]) === 8 && data.mandatory_xor_control.even_charge_models === 8, "even Tseitin control");
check(tseitinModels([1,0,0,0]) === 0 && data.mandatory_xor_control.odd_charge_models === 0, "odd Tseitin control");

const req = {direction:"R_to_P", proof_quantifier:"every_R_refutation", same_source:true, overhead:"polynomial_in_N_plus_R_cost"};
function valid(r) {
  return Object.entries(req).every(([k,v]) => r[k] === v) && typeof r.C === "number" && r.C > 0 && Number.isInteger(r.d) && r.d >= 1;
}
check(valid(data.valid_schema), "valid transfer schema");
check(data.malformed_schema_rejections.length === 8, "malformed count");

// Construct the same eight corruptions independently and reject each.
const base = data.valid_schema;
const bad = [
  {...base,direction:"P_to_R"}, {...base,proof_quantifier:"some_R_refutation"},
  {...base,proof_quantifier:"optimizer_output_only"}, {...base,same_source:false},
  {...base,overhead:"unbounded_computable"}, {...base,C:0}, {...base,d:0}, {...base,d:1.5}
];
bad.forEach((r, i) => check(!valid(r), `malformed schema ${i+1}`));

for (const row of data.synthetic_arithmetic_sanity) {
  const t = row.first_threshold;
  check(t !== null, "threshold exists");
  const rootLog = (row.synthetic_c * t.n - Math.log2(7)) / row.d;
  check(rootLog >= 1 + Math.log2(t.N_proxy), "subtraction-safe threshold");
  check(Math.abs((rootLog - 1) - t.certified_log2_floor) < 1e-9, "log floor arithmetic");
}
check(data.classification.B1 === "OPEN" && data.classification.B2 === "OPEN" && data.classification.B3 === "OPEN", "bridge classification");
const elapsed = Number(process.hrtime.bigint() - started) / 1e9;
const sha = crypto.createHash("sha256").update(fs.readFileSync(rawPath)).digest("hex");
console.log(JSON.stringify({verified:true, assertions, raw_sha256:sha, node_wall_seconds:elapsed, node_peak_rss_kib:process.resourceUsage().maxRSS}, null, 2));
