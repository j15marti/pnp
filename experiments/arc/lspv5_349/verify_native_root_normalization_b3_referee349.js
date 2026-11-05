#!/usr/bin/env node
"use strict";

// Independent REFEREE349 checker.  It imports no producer code.
const fs = require("fs");
const path = process.argv[2] || "results/raw/arc/2026-11-04_1748_LSPV5_349_NATIVE_ROOT_NORMALIZATION_B3.json";
const d = JSON.parse(fs.readFileSync(path, "utf8"));
let checks = 0;
function check(x, m) { if (!x) throw new Error(m); checks++; }

function evalCircuit(gates, bits) {
  const v = [];
  gates.forEach((g, i) => {
    if (g.op === "IN") { check(Number.isInteger(g.i) && g.i >= 0 && g.i < bits.length, "input"); v.push(bits[g.i]); }
    else if (g.op === "CONST") { check(g.b === 0 || g.b === 1, "constant"); v.push(g.b); }
    else if (g.op === "NOT") { check(Number.isInteger(g.p) && g.p >= 0 && g.p < i, "not parent"); v.push(1-v[g.p]); }
    else {
      check(["AND","OR","XOR"].includes(g.op), "binary op");
      check(Number.isInteger(g.p) && Number.isInteger(g.q) && g.p >= 0 && g.q >= 0 && g.p < i && g.q < i, "binary parents");
      v.push(g.op === "AND" ? (v[g.p]&v[g.q]) : g.op === "OR" ? (v[g.p]|v[g.q]) : (v[g.p]^v[g.q]));
    }
  });
  return v;
}

check(d.report === "REFEREE349", "report tag");
check(d.status.trace_b3.includes("B3 OPEN"), "B3 open");
check(d.authoritative_interpretation.local_convert.includes("root"), "root-only");
check(d.authoritative_interpretation.internal_wire.includes("paid fresh DEF"), "paid definitions");
const w = d.minimal_export_witness;
const vals0 = evalCircuit(w.gates, [0]);
const vals1 = evalCircuit(w.gates, [1]);
check(vals0.at(-1) === 0 && vals1.at(-1) === 1, "root equals x");
check(vals0[1] === 1 && vals1[1] === 0, "internal equals not x");
check(w.root_table.join("") === "01", "root table");
check(w.internal_gate_1_table.join("") === "10", "internal table");
check(w.root_implied === true && w.internal_implied === false, "implication classification");

for (const r of d.normalization.records) {
  check(r.support >= 1 && r.support <= 3, "support");
  check(r.table.length === (1 << r.support), "table length");
  check(r.table.every(x => x === 0 || x === 1), "table bits");
}
check(d.normalization.random_circuits === d.normalization.records.length, "circuit count");
let last = new Map();
for (const b of d.normalization.bit_bound_samples) {
  check(Number.isInteger(b.bits) && b.bits >= 16*b.n, "bit bound");
  const old = last.get(b.n) || 0;
  check(b.bits >= old, "monotone q");
  last.set(b.n, b.bits);
}

const tf = d.trace_firewall;
check(tf.reject_all_trace[1].label === "UNSAT", "bad reject label");
check(tf.sat_source.includes("p cnf 1 1") && tf.sat_source.includes("1 0"), "SAT source");
check(tf.correct_trace[1].label === "UNSAT", "good reject label");
check(tf.unsat_source.includes("1 0") && tf.unsat_source.includes("-1 0"), "UNSAT source");
check(tf.conclusion.includes("do not establish decider correctness"), "trace conclusion");
check(d.controls.native_valid === 5, "five native rules");
check(d.controls.native_malformed === 6, "malformed records");
check(d.controls.malformed_sources === 5, "malformed sources");
check(Number.isInteger(d.checks) && d.checks > 1000, "producer count");

console.log(JSON.stringify({status:"PASS", checks}));
