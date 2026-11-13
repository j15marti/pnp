#!/usr/bin/env node
"use strict";
/*
 * LSPV-4/578: UTF-8 evidence byte frontier for the EXACT archived /341 checker
 * and LSPV-1/609's fixed 12-vertex satisfiable SOURCE packet.
 *
 * Invocation from the repository: node experiments/arc/lspv4_578_native341_string_byte_orbit.cjs
 * This replays the UNCHANGED original checker in fresh Node.js processes.
 * It is NOT the complete historical R_mix341 checker.
 */
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const cp = require("node:child_process");
const crypto = require("node:crypto");
const assert = require("node:assert/strict");

const root = path.resolve(__dirname, "../..");
const checkerPath = path.join(root, "experiments/arc/lspv2_341_independent_verify.js");
const packetPath = path.join(root, "results/raw/arc/2026-11-12_2100_LSPV1_609_BRIDGE_SLICE_SAT_ACCEPTED.json");
const pins = {
  checker: "fcb7d4ced8f922de14c0bda16263a8cc7853e8e0",
  packet: "8d6d9bc7f2940a77edf2a07fcb72af111ba5b928"
};
function gitBlob(bytes) {
  return crypto.createHash("sha1").update("blob " + bytes.length + "\0").update(bytes).digest("hex");
}
const checkerBuffer = fs.readFileSync(checkerPath);
const packetBuffer = fs.readFileSync(packetPath);
assert.equal(gitBlob(checkerBuffer), pins.checker, "original checker hash mismatch");
assert.equal(gitBlob(packetBuffer), pins.packet, "original source packet hash mismatch");
const pretty = packetBuffer.toString("utf8");
const packet = JSON.parse(pretty);
assert.equal(packet.fixtures.length, 1);
const target = packet.fixtures[0].proof.find(p => p.id === "d17");
assert(target && target.rule === "AND3");
assert.equal(target.support, "102");
assert.equal(target.table, 153);
assert.equal(packet.fixtures[0].clauses.length, 48);
assert.equal(packet.fixtures[0].proof.length, 47);
const compactBytes = Buffer.byteLength(JSON.stringify(packet), "utf8");
const originalBytes = packetBuffer.length;
assert.equal(compactBytes, 10690);
assert.equal(originalBytes, 28120);

function gate(s) {
  return s.length === 3 &&
    new Set(s).size === 3 &&
    [0, 1, 10].every(x => s.includes(x));
}
function expectedTable(s) {
  let table = 0;
  for (let m = 0; m < 8; m++) {
    const bits = Array(18).fill(0);
    for (let j = 0; j < s.length; j++) bits[s[j]] = (m >> j) & 1;
    if (bits[0] === bits[1]) table |= 1 << m;
  }
  return table;
}
function independentUtf8(s) {
  let n = 0;
  for (const ch of s) {
    const v = ch.codePointAt(0);
    n += v < 128 ? 1 : v < 2048 ? 2 : v < 65536 ? 3 : 4;
  }
  return n;
}
function stringPacket(s, table) {
  const item = JSON.parse(pretty);
  const p = item.fixtures[0].proof.find(d => d.id === "d17");
  p.support = s;
  p.table = table;
  return JSON.stringify(item);
}

const histogram = {};
const byOrientation = {front: {}, back: {}};
let accepted = 0, rejected = 0;
for (let code = 0; code < 65536; code++) {
  const u = String.fromCharCode(code);
  for (const side of ["front", "back"]) {
    const s = side === "front" ? "10" + u : u + "10";
    const expected = code !== 48 && code !== 49;
    const ok = gate(s);
    assert.equal(ok, expected, "unexpected runtime support acceptance");
    if (!ok) { rejected++; continue; }
    accepted++;
    assert.equal(expectedTable(s), side === "front" ? 153 : 195, "wrong actual truth table");
    const jsonLiteral = JSON.stringify(s);
    const numBytes = Buffer.byteLength(jsonLiteral, "utf8");
    assert.equal(numBytes, independentUtf8(jsonLiteral), "UTF-8 discrepancy");
    assert([5,6,7,10].includes(numBytes));
    histogram[numBytes] = (histogram[numBytes] || 0) + 1;
    byOrientation[side][numBytes] = (byOrientation[side][numBytes] || 0) + 1;
  }
}
assert.equal(accepted, 131068);
assert.equal(rejected, 4);
assert.deepEqual(histogram, {5:184, 6:3854, 7:122880, 10:4150});
assert.deepEqual(byOrientation.front, {5:92,6:1927,7:61440,10:2075});
assert.deepEqual(byOrientation.back, byOrientation.front);

const E = packet.fixtures[0].graph.edges.length;
assert.equal(E, 18);
let sourceModels = 0, falseRows = 0;
for (let mask = 0; mask < 1 << E; mask++) {
  const satisfies = packet.fixtures[0].clauses.every(c =>
    c.literals.some(l => {
      const b = (mask >> (Math.abs(l) - 1)) & 1;
      return (l > 0 && b === 1) || (l < 0 && b === 0);
    })
  );
  if (!satisfies) continue;
  sourceModels++;
  const x0 = mask & 1, x1 = (mask >> 1) & 1, x10 = (mask >> 10) & 1;
  if ((x0 ^ x1 ^ x10) !== 0) falseRows++;
}
assert.equal(sourceModels, 64);
assert.equal(falseRows, 64);

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "lspv4_578_"));
const tempInput = path.join(tmp, "input.json");
const nativeRuns = [];
try {
  function run(label, data, accept) {
    fs.writeFileSync(tempInput, data, "utf8");
    const out = cp.spawnSync(process.execPath, [checkerPath, tempInput],
      {encoding: "utf8", maxBuffer: 16*1024*1024});
    if (out.error) throw out.error;
    const acceptedOS = out.status === 0;
    assert.equal(acceptedOS, accept, label + ": " + (out.stderr || "").slice(0,350));
    let checks = null;
    if (acceptedOS) {
      const value = JSON.parse(out.stdout);
      checks = value.checks;
      assert.equal(checks, 5155, label + " assertion-count mismatch");
    }
    nativeRuns.push({label, accepted: acceptedOS, checks, bytes: Buffer.byteLength(data, "utf8")});
  }
  run("original-compact", JSON.stringify(packet), true);
  run("original-pretty", pretty, true);
  for (const z of [0x32,0x61,0x7f,0x80,0x07ff,0x0800,0x2028,0xD800,0xDC00,0,10,34,92]) {
    for (const side of ["front","back"]) {
      const s = side === "front" ? "10" + String.fromCharCode(z) : String.fromCharCode(z) + "10";
      const table = side === "front" ? 153 : 195;
      const data = stringPacket(s, table);
      assert.equal(Buffer.byteLength(data, "utf8"), compactBytes +
        Buffer.byteLength(JSON.stringify(s), "utf8") - 5);
      run("U+" + z.toString(16).toUpperCase().padStart(4,"0") + "-" + side, data, true);
    }
  }
  for (const n of [1,99,4096]) run("prefix-whitespace-" + n, " ".repeat(n) + pretty, true);
  const array = JSON.parse(pretty);
  array.fixtures[0].proof.find(d => d.id === "d17").support = [0,1,10];
  run("forged-integer-array", JSON.stringify(array), false);
  run("wrong-local-table", stringPacket("102",195), false);
  run("repeated-support", stringPacket("100",153), false);
} finally {
  fs.rmSync(tmp, {recursive: true, force: true});
}
assert.equal(nativeRuns.filter(x=>x.accepted).length, 31);
assert.equal(nativeRuns.filter(x=>!x.accepted).length, 3);
const logicalWork = packet.fixtures[0].proof.length;
const parentApplications = packet.fixtures[0].proof.reduce((n,p)=>n+p.parents.length,0);
const referenceIDBytes = packet.fixtures[0].proof.reduce((n,p)=>n+
  p.parents.reduce((m,id)=>m+Buffer.byteLength(String(id),"utf8"),0),0);
assert.equal(logicalWork,47);assert.equal(parentApplications,94);assert.equal(referenceIDBytes,262);
const summary = {
  scope:"original archived /341 fixture checker only, NOT historical full R_mix341",
  checkerGitBlob:pins.checker, originalPacketGitBlob:pins.packet,
  acceptedDecodedStrings:accepted, rejectedLocalStringCandidates:rejected,
  literalUtf8BytesHistogram:histogram, byOrientation, models:sourceModels,
  sourceModelsFalsifyingClaimedRow:falseRows,
  canonicalCompactPacketMinBytes:compactBytes,
  canonicalCompactPacketMaxBytes:compactBytes+5,
  actualOriginalPrettyPacketBytes:originalBytes,
  logicalWork, sourceClauses:48, parentApplications, parentReferenceIDBytes:referenceIDBytes,
  originalCheckerAcceptedOS:31, originalCheckerRejectedOS:3,
  successfulOriginalCheckerAssertionsEach:5155,
  whitespacePrefixLanguage:"all n>=0 preserve parsed packet and W47; accepted input bytes=28120+n",
  nativeRunCases:nativeRuns,
  status:"PROVED/RESTRICTED symbolic exact orbit plus COMPUTATIONAL original Node replay; no general SAT result"
};
console.log(JSON.stringify(summary,null,2));
