#!/usr/bin/env node
"use strict";

// Independent no-producer-import verifier for REFEREE315.
const fs = require("fs");
const crypto = require("crypto");

const RAW = "results/raw/arc/lspv5_315/local_convert_payload_firewall_referee315.json";
const K_VALUES = [1, 2, 3, 5, 8, 16, 32, 64, 128, 256, 512, 1024];
let assertions = 0;
function check(condition, message) {
  assertions++;
  if (!condition) throw new Error(message);
}

function litValue(lit, a) {
  const v = a[Math.abs(lit)];
  return lit > 0 ? v : !v;
}
function clauseValue(clause, a) { return clause.some((lit) => litValue(lit, a)); }

const SAT_SOURCE = [[1], [1, 2]];
const UNSAT_SOURCE = [[1], [1, 2], [-1]];
function models(source) {
  const out = [];
  for (let mask = 0; mask < 4; mask++) {
    const a = {1: Boolean(mask & 1), 2: Boolean(mask & 2)};
    if (source.every((c) => clauseValue(c, a))) out.push(a);
  }
  return out;
}

function build(bits) {
  const gates = [];
  const constants = [];
  for (const bit of bits) {
    const id = gates.length;
    gates.push({id, op: "CONST", value: bit});
    constants.push(id);
  }
  let root = constants[0];
  for (const id of constants.slice(1)) {
    const next = gates.length;
    gates.push({id: next, op: "AND", args: [root, id]});
    root = next;
  }
  const x = gates.length;
  gates.push({id: x, op: "VAR", var: 1});
  const output = gates.length;
  gates.push({id: output, op: "AND", args: [x, root]});
  return {support: [1], gates, output};
}

function evaluate(payload, assignment) {
  check(Array.isArray(payload.gates), "gates must be an array");
  const values = [];
  for (let i = 0; i < payload.gates.length; i++) {
    const g = payload.gates[i];
    check(g.id === i, "noncanonical gate id");
    if (g.op === "CONST") {
      check(g.value === 0 || g.value === 1, "bad constant");
      values.push(Boolean(g.value));
    } else if (g.op === "VAR") {
      check(payload.support.includes(g.var), "variable outside support");
      values.push(assignment[g.var]);
    } else if (["AND", "OR", "XOR"].includes(g.op)) {
      check(Array.isArray(g.args) && g.args.length === 2, "bad arity");
      check(g.args.every((a) => Number.isInteger(a) && a >= 0 && a < i), "bad reference");
      const [a, b] = g.args.map((j) => values[j]);
      values.push(g.op === "AND" ? a && b : g.op === "OR" ? a || b : a !== b);
    } else if (g.op === "NOT") {
      check(Array.isArray(g.args) && g.args.length === 1 && Number.isInteger(g.args[0]) && g.args[0] >= 0 && g.args[0] < i, "bad NOT");
      values.push(!values[g.args[0]]);
    } else {
      throw new Error("bad opcode");
    }
  }
  check(Number.isInteger(payload.output) && payload.output >= 0 && payload.output < values.length, "bad output");
  return values[payload.output];
}

function parent(a) { return clauseValue(SAT_SOURCE[0], a) && clauseValue(SAT_SOURCE[1], a); }
function legal(payload) {
  check(JSON.stringify(payload.support) === "[1]", "noncanonical support");
  for (let mask = 0; mask < 4; mask++) {
    const a = {1: Boolean(mask & 1), 2: Boolean(mask & 2)};
    if (parent(a) && !evaluate(payload, a)) return false;
  }
  return true;
}

const started = process.hrtime.bigint();
const rawBytes = fs.readFileSync(RAW);
const raw = JSON.parse(rawBytes.toString("utf8"));
check(raw.status === "PASS", "raw status");
check(raw.artifact === "LOCAL-CONVERT-PAYLOAD-FIREWALL-REFEREE315", "artifact name");
check(models(SAT_SOURCE).length === 2, "SAT source model count");
check(models(UNSAT_SOURCE).length === 0, "UNSAT source model count");
check(raw.fixed_sources.sat_model_count === 2 && raw.fixed_sources.unsat_model_count === 0, "raw labels");

let flips = 0;
let gateRecords = 0;
for (let rowIndex = 0; rowIndex < K_VALUES.length; rowIndex++) {
  const k = K_VALUES[rowIndex];
  const good = build(Array(k).fill(1));
  check(legal(good), `all-one chain ${k}`);
  check(good.gates.length === 2 * k + 1, `gate count ${k}`);
  gateRecords += good.gates.length;
  for (let i = 0; i < k; i++) {
    const bits = Array(k).fill(1); bits[i] = 0;
    check(!legal(build(bits)), `single-zero ${k}:${i}`);
    flips++;
  }
  const row = raw.chains[rowIndex];
  check(row.k === k && row.gate_records === 2 * k + 1, `raw chain row ${k}`);
  check(row.charged_nodes_under_U === 2 && row.forced_constant_probes_on_legal_input === k, `raw charges ${k}`);
}
check(raw.counts.single_zero_illegal_neighbors === flips, "flip total");
check(raw.counts.legal_chain_gate_records === gateRecords, "gate total");
check(raw.counts.random_cvp_reductions === 512, "random count");
check(raw.counts.random_true + raw.counts.random_false === 512, "random labels");
check(raw.counts.sat_source_controls === K_VALUES.length + 512, "SAT controls");
check(raw.counts.unsat_global_controls === K_VALUES.length + 512, "UNSAT controls");
check(raw.counts.malformed_rejected === 12, "malformed controls");
check(raw.counts.corrupt_rejected === 5, "corrupt controls");
check(raw.ledger.largest_k === 1024 && raw.ledger.largest_gate_records === 2049, "largest fixture");
check(raw.theorem.validity_equivalence.includes("iff"), "equivalence statement");
check(raw.theorem.scope.includes("B3"), "scope firewall");

// Independently reject representative malformed/corrupt payloads.
const malformed = [];
let p = build([1,1,1]); p.gates[0].id = 2; malformed.push(p);
p = build([1,1,1]); p.gates[0].op = "NAND"; malformed.push(p);
p = build([1,1,1]); p.gates[0].value = 7; malformed.push(p);
p = build([1,1,1]); p.gates[3].args = [3,0]; malformed.push(p);
p = build([1,1,1]); p.support = [2]; malformed.push(p);
p = build([1,1,1]); p.output = 100; malformed.push(p);
let rejected = 0;
for (const bad of malformed) {
  try { if (!legal(bad)) rejected++; } catch (_) { rejected++; }
}
check(rejected === malformed.length, "independent malformed rejection");

const elapsed = Number(process.hrtime.bigint() - started) / 1e9;
const digest = crypto.createHash("sha256").update(rawBytes).digest("hex");
console.log(JSON.stringify({
  status: "PASS",
  raw_sha256: digest,
  independent_assertions: assertions,
  replayed_chain_lengths: K_VALUES.length,
  replayed_single_zero_neighbors: flips,
  independent_malformed_rejected: rejected,
  verifier_wall_seconds: elapsed,
  verifier_peak_rss_kib: Math.ceil(process.memoryUsage().rss / 1024)
}));
