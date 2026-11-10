#!/usr/bin/env node
/*
 LSPV-1/553: independent native-341 accepted-byte coverage audit.
 Usage from j15marti/pnp repository root:
   node experiments/arc/lspv1_553_native_checker_coverage.cjs
   node experiments/arc/lspv1_553_native_checker_coverage.cjs results/raw/arc/553_audit.json
 Requires Node >=18. Uses the UNMODIFIED historical producer and verifier
 as child processes. Does not modify R_mix341 or invent accepted opcodes.
*/
"use strict";
const fs = require("fs");
const os = require("os");
const path = require("path");
const crypto = require("crypto");
const { spawnSync } = require("child_process");
const assert = require("assert").strict;

const producerPath = "experiments/arc/lspv2_341_mixed_tseitin_min_dag.js";
const verifierPath = "experiments/arc/lspv2_341_independent_verify.js";
const expected = {
  producer: "4081022e8a3841d79f751a3d3a7a10decbb026da",
  verifier: "fcb7d4ced8f922de14c0bda16263a8cc7853e8e0"
};
function blobSha(bytes) {
  return crypto.createHash("sha1").update(Buffer.concat([
    Buffer.from("blob " + bytes.length + "\0", "ascii"), bytes
  ])).digest("hex");
}
for (const [label, file] of [["producer",producerPath],["verifier",verifierPath]]) {
  const got = blobSha(fs.readFileSync(file));
  assert.equal(got, expected[label], label + " differs from pinned original!");
}
function node(file, args) {
  return spawnSync(process.execPath, [file, ...args], {
    encoding: "utf8", maxBuffer: 20 * 1024 * 1024, timeout: 30000
  });
}
const generated = node(producerPath, []);
assert.equal(generated.status, 0, generated.stderr);
const packet = JSON.parse(generated.stdout);
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "lspv1-553-"));
function copy(obj) { return JSON.parse(JSON.stringify(obj)); }
function run(label, obj) {
  const filename = path.join(tmp, label + ".json");
  fs.writeFileSync(filename, JSON.stringify(obj), "utf8");
  const p = node(verifierPath, [filename]);
  const accepted = p.status === 0;
  return {label, accepted,
    checks: accepted ? JSON.parse(p.stdout).checks : null,
    first_case: accepted ? JSON.parse(p.stdout).cases[0] : null,
    diagnostic: accepted ? null : (p.stderr.match(/Verifier: [^\n]+|Error: unknown rule/) || [p.stderr.trim()])[0],
    source_sha256: crypto.createHash("sha256").update(fs.readFileSync(filename)).digest("hex")};
}
try {
  const base = run("baseline", packet);
  assert.equal(base.accepted,true);
  assert.equal(base.checks,30714);
  const originalFirst = packet.fixtures[0].proof[0];
  assert.equal(originalFirst.rule, "AND3");
  assert.equal(originalFirst.id,"d0");
  assert.deepEqual(originalFirst.parents, ["s0","s1"]);
  const src = packet.fixtures[0].clauses;
  const byId = new Map(src.map(c=>[c.id,c]));
  const parents = originalFirst.parents.map(id=>byId.get(id));
  assert(parents.every(Boolean));
  let semanticRows = 0;
  for(let mask=0;mask<8;mask++) {
    const bits = Array(packet.fixtures[0].graph.edges.length).fill(0);
    originalFirst.support.forEach((edge,j)=>bits[edge]=(mask>>j)&1);
    const litTrue = lit => lit>0?bits[lit-1]===1:bits[-lit-1]===0;
    const expectedValue = Number(parents.every(c=>c.literals.some(litTrue)));
    assert.equal((originalFirst.table>>mask)&1, expectedValue);
    semanticRows++;
  }
  const padded = copy(packet);
  const duplicate = copy(padded.fixtures[0].proof[0]);
  duplicate.id = "PAID_REDUNDANT_AND3_553";
  padded.fixtures[0].proof.splice(1,0,duplicate);
  const padding = run("legal_paid_duplicate", padded);
  assert.equal(padding.accepted,false);
  assert.equal(padding.diagnostic,"Verifier: proof candidate length");
  const srcUnbound = copy(packet);
  srcUnbound.fixtures[0].externalOriginalInput = "p cnf 1 1\n1 0\n";
  const metadata = run("unbound_satisfiable_input_metadata",srcUnbound);
  assert.equal(metadata.accepted,true);
  assert.equal(metadata.checks,base.checks);
  const missingRules = {};
  for (const rule of ["RES","LOCAL-CONVERT","DEF"]) {
    const probe=copy(packet);
    probe.fixtures[0].proof[0].rule=rule;
    missingRules[rule]=run("opcode_"+rule.replace(/[^a-zA-Z0-9]/g,"_"),probe);
    assert.equal(missingRules[rule].accepted,false);
    assert.equal(missingRules[rule].diagnostic,"Error: unknown rule");
  }
  const result = {
    id:"LSPV1-553-NATIVE-341-COVERAGE/v1",
    executed:"original pinned producer and original pinned verifier via Node child_process",
    source_blobs:expected,
    baseline:base,
    redundant_paid_AND3:{...padding, independent_truth_rows:semanticRows,
      interpretation:"valid in declared unit-paid, arbitrary-DAG AND3 semantics; refused by test-only length guard"},
    unbound_external_source_metadata:{...metadata,
      interpretation:"not an authenticated external source API; extra property is ignored"},
    unknown_opcode_dispatcher:missingRules,
    notes:"A negative probe using RES, LOCAL-CONVERT or DEF with AND3 parents is not evidence that a full native grammar cannot accept a well-typed step. Historical fuller checker not located; P2-D1 OPEN. Neither original checker nor this audit is an all-source SAT/UNSAT certifier. No FLMV or P-vs-NP implication."
  };
  const rendered = JSON.stringify(result,null,2)+"\n";
  if (process.argv[2]) fs.writeFileSync(process.argv[2],rendered,"utf8");
  else process.stdout.write(rendered);
} finally {
  for (const name of fs.readdirSync(tmp)) fs.rmSync(path.join(tmp,name));
  fs.rmdirSync(tmp);
}
