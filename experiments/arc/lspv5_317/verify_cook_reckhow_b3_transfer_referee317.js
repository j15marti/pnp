#!/usr/bin/env node
"use strict";

const fs = require("fs");
const crypto = require("crypto");
const rawPath = "results/raw/arc/lspv5_317/cook_reckhow_b3_transfer_referee317.json";
const started = process.hrtime.bigint();
const data = JSON.parse(fs.readFileSync(rawPath, "utf8"));
let assertions = 0;
function check(value, message) { assertions++; if (!value) throw new Error(message); }

function clauseFalse(clause, mask) {
  return clause.every(lit => {
    const value = Boolean(mask & (2 ** (Math.abs(lit) - 1)));
    return !(lit > 0 ? value : !value);
  });
}
function label(formula) {
  for (let mask = 0; mask < 2 ** formula.vars; mask++) {
    if (formula.clauses.every(c => !clauseFalse(c, mask))) return "SAT";
  }
  return "UNSAT";
}
function verifyTT(formula, proof) {
  if (!Array.isArray(proof) || proof.length !== 2 ** formula.vars) return false;
  return proof.every((record, mask) => {
    if (!record || Object.keys(record).sort().join(",") !== "assignment,falsified_clause") return false;
    const index = record.falsified_clause;
    return record.assignment === mask && Number.isInteger(index) && index >= 0 && index < formula.clauses.length && clauseFalse(formula.clauses[index], mask);
  });
}
function contradictoryUnits(v) {
  const clauses = [];
  for (let i = 1; i <= v; i++) clauses.push([i], [-i]);
  return {vars:v, clauses};
}
function pairedSat(v) { return {vars:v, clauses:Array.from({length:v}, (_,i)=>[i+1])}; }
function makeTT(formula) {
  const proof = [];
  for (let mask = 0; mask < 2 ** formula.vars; mask++) {
    const index = formula.clauses.findIndex(c => clauseFalse(c, mask));
    proof.push({assignment:mask, falsified_clause:index});
  }
  return proof;
}

let records = 0;
for (const row of data.controls) {
  const u = contradictoryUnits(row.variables);
  const s = pairedSat(row.variables);
  const p = makeTT(u);
  check(label(u) === "UNSAT" && row.unsat_label === "UNSAT", `UNSAT label v=${row.variables}`);
  check(label(s) === "SAT" && row.paired_label === "SAT", `SAT label v=${row.variables}`);
  check(p.length === 2 ** row.variables && p.length === row.tt_paid_records, `record count v=${row.variables}`);
  check(verifyTT(u, p), `TT verification v=${row.variables}`);
  check(!verifyTT(s, p), `SAT rejection v=${row.variables}`);
  records += p.length;
}
check(records === data.measurements.truth_table_records_verified, "aggregate TT records");

const base = contradictoryUnits(4);
const baseProof = makeTT(base);
const bad = [];
bad.push(baseProof.slice(0,-1));
let p = JSON.parse(JSON.stringify(baseProof)); p[1].assignment=0; bad.push(p);
p = JSON.parse(JSON.stringify(baseProof)); p[0].assignment=1; bad.push(p);
p = JSON.parse(JSON.stringify(baseProof)); p[0].falsified_clause=999; bad.push(p);
p = JSON.parse(JSON.stringify(baseProof)); p[0].falsified_clause=1; bad.push(p);
p = JSON.parse(JSON.stringify(baseProof)); p[0].extra=0; bad.push(p);
bad.push({records:baseProof});
bad.forEach((proof,i)=>check(!verifyTT(base,proof),`independent corruption ${i+1}`));
check(data.malformed_tt_rejections.length === 10, "producer TT malformed count");
check(data.malformed_decider_rejections.length === 3, "producer D_A malformed count");
check(data.classification.equivalence_under_fixed_correct_A === "PROVED", "equivalence classification");
check(data.classification.B1_Rmix341 === "OPEN" && data.classification.B2_Rmix341 === "OPEN" && data.classification.B3_Rmix341 === "OPEN", "B classification");

const elapsed = Number(process.hrtime.bigint()-started)/1e9;
const sha = crypto.createHash("sha256").update(fs.readFileSync(rawPath)).digest("hex");
console.log(JSON.stringify({verified:true,assertions,truth_table_records_rebuilt:records,raw_sha256:sha,node_wall_seconds:elapsed,node_peak_rss_kib:process.resourceUsage().maxRSS},null,2));
