#!/usr/bin/env node
"use strict";

// Independent no-import verifier for REFEREE352 raw data.
const fs = require("fs");
const crypto = require("crypto");
if (process.argv.length !== 3) throw new Error("usage: verify_unlock_chain_referee352.js RAW.json");
const raw = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
let checks = 0;
function ok(x, msg) { if (!x) throw new Error(msg); checks++; }

function parse(text) {
  const lines = text.trimEnd().split("\n");
  const h = lines[0].split(/\s+/);
  if (h.length !== 4 || h[0] !== "p" || h[1] !== "cnf") throw new Error("header");
  const v = Number(h[2]), m = Number(h[3]);
  if (!Number.isInteger(v) || v < 1 || !Number.isInteger(m) || m < 0 || lines.length !== m + 1) throw new Error("counts");
  const clauses = [];
  for (const line of lines.slice(1)) {
    const xs = line.split(/\s+/).map(Number);
    if (!xs.length || xs[xs.length - 1] !== 0 || xs.slice(0, -1).some(x => !Number.isInteger(x) || x === 0 || Math.abs(x) > v)) throw new Error("clause");
    const c = xs.slice(0, -1);
    if (c.length < 1 || c.length > 2) throw new Error("width");
    clauses.push(c);
  }
  return {v, clauses};
}

function modelCount(v, clauses) {
  let count = 0;
  for (let b = 0; b < 2 ** v; b++) {
    let good = true;
    for (const c of clauses) {
      if (!c.some(l => (((b >> (Math.abs(l) - 1)) & 1) === (l > 0 ? 1 : 0)))) { good = false; break; }
    }
    if (good) count++;
  }
  return count;
}

function resolve(a, b, p) {
  if (!a.includes(p) || !b.includes(-p)) throw new Error("pivot");
  const out = [...new Set(a.filter(x => x !== p).concat(b.filter(x => x !== -p)))];
  out.sort((x, y) => Math.abs(x) - Math.abs(y) || Number(x < 0) - Number(y < 0));
  if (out.some(x => out.includes(-x))) throw new Error("tautology");
  return out;
}

function buildProof(v) {
  const p = [{rule:"START", counter:0}];
  for (let i = 1; i < 2 ** v; i++) p.push({rule:"TICK", parent:p.length - 1, counter:i});
  const unlock = p.length - 1;
  p.push({rule:"ACTIVATE", source:0, unlock, clause:[1]});
  const left = p.length - 1;
  p.push({rule:"ACTIVATE", source:1, unlock, clause:[-1]});
  const right = p.length - 1;
  p.push({rule:"RES", left, right, pivot:1, clause:[]});
  return p;
}

function verify(text, proof) {
  const {v, clauses} = parse(text);
  const vals = [];
  for (let i = 0; i < proof.length; i++) {
    const n = proof[i];
    if (n.rule === "START") {
      ok(i === 0 && n.counter === 0, "start"); vals.push(["T", 0]);
    } else if (n.rule === "TICK") {
      ok(Number.isInteger(n.parent) && n.parent >= 0 && n.parent < i, "tick ref");
      ok(vals[n.parent][0] === "T" && n.counter === vals[n.parent][1] + 1 && n.counter < 2 ** v, "tick");
      vals.push(["T", n.counter]);
    } else if (n.rule === "ACTIVATE") {
      ok(Number.isInteger(n.source) && n.source >= 0 && n.source < clauses.length, "source ref");
      ok(Number.isInteger(n.unlock) && n.unlock < i && vals[n.unlock][0] === "T" && vals[n.unlock][1] === 2 ** v - 1, "unlock");
      ok(JSON.stringify(n.clause) === JSON.stringify(clauses[n.source]), "source exact");
      vals.push(["C", n.clause]);
    } else if (n.rule === "RES") {
      ok(n.left < i && n.right < i && vals[n.left][0] === "C" && vals[n.right][0] === "C", "res refs");
      const out = resolve(vals[n.left][1], vals[n.right][1], n.pivot);
      ok(JSON.stringify(out) === JSON.stringify(n.clause), "res exact");
      vals.push(["C", out]);
    } else throw new Error("rule");
  }
  ok(vals.length > 0 && vals.at(-1)[0] === "C" && vals.at(-1)[1].length === 0, "root");
}

ok(raw.artifact === "REFEREE352_UNLOCK_CHAIN_GENERIC_B3_FIREWALL", "artifact");
ok(raw.status.R_mix341_B3 === "OPEN", "B3 status");
ok(raw.status.P_vs_NP === "OPEN", "P status");
ok(raw.calculus.max_premises === 2 && raw.calculus.unit_paid_nodes === true, "calculus");
for (const c of raw.cases) {
  const u = parse(c.unsat_source), s = parse(c.sat_source);
  ok(u.v === c.v && s.v === c.v, "v");
  ok(modelCount(c.v, u.clauses) === 0, "unsat");
  ok(modelCount(c.v, s.clauses) === 2 ** (c.v - 1), "sat");
  ok(c.token_nodes === 2 ** c.v, "token count");
  ok(c.exact_minimum_paid_nodes === 2 ** c.v + 3, "minimum formula");
  ok(c.Rmix341_exact_minimum_by_native_RES === 1, "same-source Rmix control");
  const proof = buildProof(c.v);
  ok(c.proof_node_count === c.exact_minimum_paid_nodes && proof.length === c.proof_node_count, "proof size");
  const digest = crypto.createHash("sha256").update(JSON.stringify(proof)).digest("hex");
  ok(digest === c.proof_sha256, "proof digest");
  verify(c.unsat_source, proof);
}
for (const s of raw.symbolic) {
  const v = s.v, N = s.N;
  ok(BigInt(s.q) === (1n << BigInt(v)) + 3n, "symbolic q");
  ok(N > 0 && s.counter_bits === v, "symbolic cost");
}

// A literal generic-bridge comparison: 2-SAT has a linear-time decider, yet
// this fixed calculus forces the recorded superpolynomial family.  The check
// says nothing about the distinct native R_mix341 calculus.
for (const v of [16, 32, 64]) {
  const row = raw.symbolic[v - 1];
  ok(BigInt(row.q) > BigInt(row.N) ** 2n, "eventual superquadratic witness");
}
console.log(JSON.stringify({independent_checks: checks, cases: raw.cases.length, status: "PASS"}));
