#!/usr/bin/env node
"use strict";
/*
 * LSPV-3/602: exact charge-type acceptance quotient of the ORIGINAL /341
 * fixture verifier, not the missing full historical R_mix341 grammar.
 *
 * Run at repository root:
 *   node experiments/arc/lspv3_602_native341_charge_exact_quotient.cjs
 *   node experiments/arc/lspv3_602_native341_charge_exact_quotient.cjs /tmp/raw602.json
 *
 * The archived verifier source is executed WITHOUT changing its mathematical
 * body, through Node vm for the 625-case matrix and as its actual Node CLI
 * subprocess for the discriminating positive/negative and hostile controls.
 * The wrapper supplies only original file, argv and console I/O.
 */
const fs = require("node:fs");
const path = require("node:path");
const os = require("node:os");
const vm = require("node:vm");
const cp = require("node:child_process");
const crypto = require("node:crypto");
const assert = require("node:assert/strict");

const ROOT = path.resolve(__dirname, "../..");
const CHECKER = path.join(ROOT, "experiments/arc/lspv2_341_independent_verify.js");
const SEED = path.join(ROOT, "results/raw/arc/2026-11-12_1725_LSPV3_600_NATIVE341_K4_EDGE_SUFFIX_ACCEPTED.json");
const EXPECTED_CHECKER_BLOB = "fcb7d4ced8f922de14c0bda16263a8cc7853e8e0";
const EXPECTED_SEED_BLOB = "393d13265192b4e43073c6f6559bc22b6a71ece5";

function gitBlob(bytes) {
  return crypto.createHash("sha1").update("blob " + bytes.length + "\0").update(bytes).digest("hex");
}
function sha256(bytes) { return crypto.createHash("sha256").update(bytes).digest("hex"); }
const checkerBytes = fs.readFileSync(CHECKER);
const seedBytes = fs.readFileSync(SEED);
assert.equal(gitBlob(checkerBytes), EXPECTED_CHECKER_BLOB, "original checker drift");
assert.equal(gitBlob(seedBytes), EXPECTED_SEED_BLOB, "original signed source/seed drift");
const checkerSource = checkerBytes.toString("utf8");
const seed = JSON.parse(seedBytes.toString("utf8"));
assert.deepEqual(seed.fixtures[0].charges, [1,0,0,0]);
assert.equal(seed.fixtures[0].clauses.length, 16);
assert.equal(seed.fixtures[0].proof.length, 15);
const originalSources = JSON.stringify(seed.fixtures[0].clauses);
const clone = x => JSON.parse(JSON.stringify(x));
function packet(charges, mutation) {
  const q = clone(seed);
  q.fixtures[0].charges = clone(charges);
  if (mutation) mutation(q);
  if (mutation === undefined) assert.equal(JSON.stringify(q.fixtures[0].clauses), originalSources);
  return q;
}
function replayOriginalVM(q) {
  const printed = [];
  try {
    vm.runInNewContext(checkerSource, {
      require: name => {
        if (name !== "fs") throw Error("unexpected module " + name);
        return {readFileSync: () => JSON.stringify(q)};
      },
      process: {argv: [process.execPath, CHECKER, "in-memory.json"]},
      console: {log: s => printed.push(s)}
    }, {filename: CHECKER, timeout: 30000});
    assert.equal(printed.length, 1);
    return {accepted: true, assertions: JSON.parse(printed[0]).checks};
  } catch (e) {
    return {accepted: false, error: String(e.message)};
  }
}
function acceptPredicate(c) {
  // For this fixed K4 original source, each source clause forbids a pattern
  // whose parity is 0 at vertex zero, 1 at vertices one/two/three.
  // Undefined ToPrimitive conversion means the checker rejects.
  try {
    const toInt32 = c.map(v => v | 0);
    return toInt32.reduce((a,b) => a ^ b, 0) === 1 &&
      c.every((v,i) => v !== (i === 0 ? 0 : 1));
  } catch (e) { return false; }
}
const alphabet = [0,1,"0","1",null], cases = [];
let accepted = 0, originalAssertions = 0;
for (const a of alphabet) for (const b of alphabet)
for (const c of alphabet) for (const d of alphabet) {
  const charges = [a,b,c,d], expected = acceptPredicate(charges);
  const observed = replayOriginalVM(packet(charges));
  assert.equal(observed.accepted, expected, "original verifier mismatch for " + JSON.stringify(charges));
  if (observed.accepted) {accepted++;originalAssertions += observed.assertions;}
  cases.push({charges, toInt32: charges.map(x => x | 0), expected, ...observed});
}
assert.equal(cases.length,625);
assert.equal(accepted,128);
assert.equal(originalAssertions,179328);

const good = ["0","1",0,0], bad = [0,1,0,0];
assert.deepEqual(good.map(x => x | 0), bad.map(x => x | 0));
assert.equal(replayOriginalVM(packet(good)).accepted, true);
assert.equal(replayOriginalVM(packet(bad)).accepted, false);
const hostileDefinitions = [
  ["forged_source",q => {q.fixtures[0].clauses[0].literals[0] = 999;}],
  ["unbound_parent",q => {q.fixtures[0].proof[0].parents[0] = "UNBOUND";}],
  ["wrong_terminal",q => {q.fixtures[0].proof.at(-1).row.rhs = 0;}],
  ["wrong_AND3_table",q => {q.fixtures[0].proof[0].table ^= 1;}],
  ["duplicate_edge",q => {q.fixtures[0].graph.edges[0] = q.fixtures[0].graph.edges[1].slice(0,2);}]
];
const hostileCases = hostileDefinitions.map(([name,change]) => ({
  name, charges: good, packet: packet(good,change)
}));
hostileCases.push({name:"non_coercible_object",
 charges:[1,{toString:0},0,0], packet:packet([1,{toString:0},0,0])});
for (const h of hostileCases) {
  const result = replayOriginalVM(h.packet);
  assert.equal(result.accepted,false,"hostile original VM accepted: "+h.name);
  h.vm = result;
}
const temp = fs.mkdtempSync(path.join(os.tmpdir(),"lspv3-602-"));
function replayOriginalOS(name,q) {
  const fp = path.join(temp,name+".json");
  fs.writeFileSync(fp,JSON.stringify(q)+"\n");
  const result = cp.spawnSync(process.execPath,[CHECKER,fp],{
    encoding:"utf8",timeout:30000,maxBuffer:4*1024*1024
  });
  let checkerResult=null;
  try {checkerResult=JSON.parse(result.stdout.trim());} catch (_) {}
  return {accepted:result.status===0,exitCode:result.status,
    originalChecks:checkerResult?.checks??null,
    firstError:(result.stderr||"").split("\n").find(s=>s.includes("Error:"))||"",
    rawSha256:sha256(fs.readFileSync(fp))};
}
let osControls=[];
try {
  for (const [name,charge,expected] of [
    ["correct_numeric",[1,0,0,0],true],
    ["coerced_string_accept",good,true],
    ["identical_int32_numeric_reject",bad,false],
    ["noncoercible_object",[1,{toString:0},0,0],false]
  ]) {
    const observed=replayOriginalOS(name,packet(charge));
    assert.equal(observed.accepted,expected,"OS checker "+name);
    osControls.push({name,charge,expected,...observed});
  }
  for (const h of hostileCases.slice(0,5)) {
    const observed=replayOriginalOS(h.name,h.packet);
    assert.equal(observed.accepted,false,"OS checker hostile "+h.name);
    osControls.push({name:h.name,expected:false,...observed});
  }
} finally {fs.rmSync(temp,{recursive:true,force:true});}
const ledger={
  schema:"LSPV3-602-ORIGINAL341-CHARGE-QUOTIENT/v1",
  checkerGitBlob:EXPECTED_CHECKER_BLOB,seedGitBlob:EXPECTED_SEED_BLOB,
  originalSignedSourceSha256:sha256(Buffer.from(originalSources)),
  ruleScope:"Archived original /341 SOURCE/AND3/XOR K4 only",
  cost:15,sources:16,
  premise:"Each JS charge must be coercible by bitwise ToInt32.",
  theorem:"ACCEPT iff XOR(ToInt32(c_v))===1 and each raw c_v !== the numeric opposite original charge.",
  lossOfInformation:"ACCEPT [\"0\",\"1\",0,0] and REJECT [0,1,0,0] have identical per-vertex ToInt32 values.",
  vm:{cases:cases.length,accepted,rejected:cases.length-accepted,
      assertionGroups:originalAssertions,mismatches:0,
      hostileRejections:hostileCases.length},
  os:{originalCheckerSubprocessExecutions:osControls.length,
      controls:osControls},
  cases,hostiles:hostileCases.map(h=>({name:h.name,vm:h.vm}))
};
const output = JSON.stringify(ledger,null,2)+"\n";
if(process.argv[2])fs.writeFileSync(process.argv[2],output);
process.stdout.write(JSON.stringify({status:"PASS",...ledger.vm,
 osCheckerRuns:osControls.length,sourceSha256:ledger.originalSignedSourceSha256})+"\n");
