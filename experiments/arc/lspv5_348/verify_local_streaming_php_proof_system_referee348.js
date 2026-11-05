#!/usr/bin/env node
"use strict";

// Independent no-producer-import verifier for REFEREE348.
const fs = require("fs");
const crypto = require("crypto");
const path = "results/raw/arc/2026-11-04_1648_LSPV5_348_LOCAL_STREAMING_PHP.json";
const data = JSON.parse(fs.readFileSync(path, "utf8"));
let checks = 0;
function ok(x, msg) { if (!x) throw new Error(msg); checks++; }
function sha(s) { return crypto.createHash("sha256").update(s).digest("hex"); }

function variable(p, hole, h) { return (p - 1) * h + hole; }
function php(h) {
  const clauses = [];
  for (let p = 1; p <= h + 1; p++) {
    const c = [];
    for (let j = 1; j <= h; j++) c.push(variable(p, j, h));
    clauses.push(c);
  }
  for (let j = 1; j <= h; j++) {
    for (let p = 1; p <= h + 1; p++) {
      for (let q = p + 1; q <= h + 1; q++) clauses.push([-variable(p, j, h), -variable(q, j, h)]);
    }
  }
  return {n: h * (h + 1), clauses};
}
function encode(n, clauses) {
  return `p cnf ${n} ${clauses.length}\n` + clauses.map(c => c.concat([0]).join(" ")).join("\n") + "\n";
}
function parse(source) {
  if (typeof source !== "string" || !source.endsWith("\n")) throw new Error("newline");
  const lines = source.slice(0, -1).split("\n");
  const head = lines[0].split(/\s+/);
  if (head.length !== 4 || head[0] !== "p" || head[1] !== "cnf") throw new Error("header");
  const n = Number(head[2]), m = Number(head[3]);
  if (!Number.isInteger(n) || !Number.isInteger(m) || n < 0 || m < 0 || lines.length !== m + 1) throw new Error("counts");
  const clauses = [];
  for (const line of lines.slice(1)) {
    if (!line.length) throw new Error("blank");
    const a = line.split(/\s+/).map(Number);
    if (a.some(x => !Number.isInteger(x)) || a[a.length - 1] !== 0 || a.slice(0, -1).some(x => x === 0 || Math.abs(x) > n)) throw new Error("literal");
    clauses.push(a.slice(0, -1));
  }
  return {n, clauses};
}
function sat(clauses, assignment) {
  return clauses.every(c => c.some(lit => (((assignment >> (Math.abs(lit) - 1)) & 1) === (lit > 0 ? 1 : 0))));
}
function firstFalse(clauses, assignment) {
  for (let i = 0; i < clauses.length; i++) if (!sat([clauses[i]], assignment)) return i;
  return null;
}
function scanProof(source, h) {
  const bytes = Buffer.from(source, "ascii");
  const out = [{op:"START", h, pos:-1}];
  for (let i = 0; i < bytes.length; i++) out.push({op:"SCAN", h, pos:i, byte:bytes[i]});
  out.push({op:"ACCEPT_PHP", h, pos:bytes.length});
  return out;
}
function verifyScan(source, proof) {
  try { parse(source); } catch (_) { return false; }
  if (!proof.length || proof[0].op !== "START" || proof[0].h < 1 || proof[0].pos !== -1) return false;
  const h = proof[0].h, expected = encode(php(h).n, php(h).clauses), bytes = Buffer.from(source, "ascii");
  if (proof.length !== bytes.length + 2) return false;
  for (let i = 0; i < bytes.length; i++) {
    const x = proof[i + 1];
    if (x.op !== "SCAN" || x.h !== h || x.pos !== i || x.byte !== bytes[i]) return false;
  }
  const z = proof[proof.length - 1];
  return source === expected && z.op === "ACCEPT_PHP" && z.h === h && z.pos === bytes.length;
}
function verifyTable(source, proof) {
  let parsed; try { parsed = parse(source); } catch (_) { return false; }
  const {n, clauses} = parsed;
  if (n > 30 || proof.length !== (1 << n) + 2) return false;
  const start = proof[0];
  if (start.op !== "TABLE_START" || start.n !== n || start.idx !== -1) return false;
  for (let a = 0; a < (1 << n); a++) {
    const node = proof[a + 1], j = firstFalse(clauses, a);
    if (node.op !== "TABLE" || node.idx !== a || node.clause !== j) return false;
  }
  const end = proof[proof.length - 1];
  return end.op === "ACCEPT_TABLE" && end.n === n && end.idx === (1 << n);
}

ok(data.run === "REFEREE348", "run tag");
ok(data.system.max_parent_arity === 1, "unary parents");
ok(data.system.fixed_opcodes.length === 6, "finite opcode alphabet");
for (const rec of data.php) {
  const f = php(rec.h), source = encode(f.n, f.clauses), proof = scanProof(source, rec.h);
  ok(rec.variables === f.n, `vars h=${rec.h}`);
  ok(rec.clauses === f.clauses.length, `clauses h=${rec.h}`);
  ok(rec.source_bytes === Buffer.byteLength(source), `bytes h=${rec.h}`);
  ok(rec.source_sha256 === sha(source), `digest h=${rec.h}`);
  ok(rec.trace_nodes === proof.length, `nodes h=${rec.h}`);
  ok(verifyScan(source, proof), `local scan h=${rec.h}`);
  const skip = proof.map(x => ({...x})); skip.splice(Math.floor(skip.length / 2), 1);
  ok(!verifyScan(source, skip), `skip reject h=${rec.h}`);
  const flip = proof.map(x => ({...x})); flip[1].byte ^= 1;
  ok(!verifyScan(source, flip), `byte reject h=${rec.h}`);
}

for (const rec of data.deletion_sat_siblings) {
  const f = php(rec.h), target = [-variable(1, 1, rec.h), -variable(2, 1, rec.h)];
  const at = f.clauses.findIndex(c => JSON.stringify(c) === JSON.stringify(target));
  const clauses = f.clauses.slice(0, at).concat(f.clauses.slice(at + 1));
  const source = encode(f.n, clauses);
  ok(at >= 0, `deleted collision h=${rec.h}`);
  ok(sha(source) === rec.source_sha256, `sibling digest h=${rec.h}`);
  ok(sat(clauses, rec.witness), `sibling witness h=${rec.h}`);
  ok(firstFalse(clauses, rec.witness) === null, `fallback blocker h=${rec.h}`);
  ok(!verifyScan(source, scanProof(source, rec.h)), `sibling special reject h=${rec.h}`);
}

for (const c of data.fallback_controls) {
  ok(verifyTable(c.source, c.proof), `fallback ${c.name}`);
  const bad = c.proof.map(x => ({...x})); bad[Math.min(2, bad.length - 2)].clause = 999999;
  ok(!verifyTable(c.source, bad), `corrupt fallback ${c.name}`);
}

const even = parse(data.paired_controls.even_k4);
let models = 0; for (let a = 0; a < (1 << even.n); a++) if (sat(even.clauses, a)) models++;
ok(models === 8 && data.paired_controls.even_k4_models === 8, "even K4 paired control");
const unit = parse(data.paired_controls.sat_unit);
ok(sat(unit.clauses, 1), "SAT unit witness");

const malformed = ["", "p cnd 1 1\n1 0\n", "p cnf 1 2\n1 0\n", "p cnf -1 0\n",
  "p cnf 1 1\n2 0\n", "p cnf 1 1\n1\n", "p cnf 1 1\n1 0 0\n", "p cnf 1 1\n1 0"];
for (const x of malformed) {
  let rejected = false; try { parse(x); } catch (_) { rejected = true; }
  ok(rejected, "malformed reject");
}
ok(data.malformed_count === malformed.length, "malformed count");

console.log(JSON.stringify({status:"PASS", checks}));
