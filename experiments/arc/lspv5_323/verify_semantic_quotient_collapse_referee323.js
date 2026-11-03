#!/usr/bin/env node
"use strict";
const fs = require("fs"), path = require("path");
const root = path.resolve(__dirname, "../../..");
const rawPath = path.join(root, "results/raw/arc/lspv5_323/semantic_quotient_collapse_referee323.json");
const raw = JSON.parse(fs.readFileSync(rawPath, "utf8"));
let checks = 0;
function ok(condition, message) { checks++; if (!condition) throw new Error(message); }
function assignments(n) {
  const out = [];
  for (let a = 0; a < (1 << n); a++) out.push(Array.from({length:n}, (_,i)=>(a >> i) & 1));
  return out;
}
function models(clauses, n) {
  return assignments(n).filter(bits => clauses.every(clause =>
    clause.some(lit => bits[Math.abs(lit)-1] === (lit > 0 ? 1 : 0))));
}
function relation(fixture) {
  const tuples = new Set(models(fixture.clauses, fixture.variables).map(bits =>
    JSON.stringify(fixture.boundary.map(index => bits[index-1]))));
  return Array.from(tuples).sort().map(JSON.parse);
}
function same(a,b) { return JSON.stringify(a) === JSON.stringify(b); }

ok(raw.artifact === "SEMANTIC-QUOTIENT-ALGORITHM-MINIMUM-COLLAPSE-REFEREE323", "artifact");
const fixtures = raw.controls.fixtures;
for (const [name, fixture] of Object.entries(fixtures)) {
  ok(models(fixture.clauses, fixture.variables).length === fixture.model_count, `${name} models`);
  ok(same(relation(fixture), fixture.relation), `${name} relation`);
}
for (const name of raw.controls.closed_unsat_names) ok(same(fixtures[name].relation, []), `${name} closed UNSAT`);
for (const name of raw.controls.closed_sat_names) ok(same(fixtures[name].relation, [[]]), `${name} closed SAT`);
ok(same(fixtures.equality_boundary.relation, [[0,0],[1,1]]), "equality");
ok(same(fixtures.equality_aux_boundary.relation, [[0,0],[1,1]]), "aux equality");
ok(same(fixtures.guarded_unsat_internal.relation, [[0]]), "guarded UNSAT internal");
ok(same(fixtures.guarded_sat_sibling.relation, [[0],[1]]), "guarded SAT sibling");
for (let b = 0; b <= 3; b++) ok(raw.controls.quotient_class_counts[String(b)] === 2 ** (2 ** b), `quotient b=${b}`);
ok(raw.controls.malformed_rejected === 8, "malformed controls");
ok(raw.controls.hardcoded_total_decider_checks.length === 49, "hardcode check count");
ok(raw.controls.hardcoded_total_decider_checks.every(item => item.correct), "hardcode correctness");
ok(raw.classification.B1 === "OPEN" && raw.classification.B2 === "OPEN" && raw.classification.B3 === "OPEN", "bridges open");
ok(raw.classification.P_vs_NP === "OPEN", "P vs NP open");
console.log(JSON.stringify({status:"PASS", checks, raw:rawPath}));
