#!/usr/bin/env node
'use strict';

// LSPV-5/503: independent P2-C3 red-team replay against the unchanged
// archived /386 checker.  The audit harness is not a replacement checker and
// does not claim to authenticate the missing full historical R_mix341 grammar.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const assert = require('assert');
const {spawnSync} = require('child_process');

const root = path.resolve(__dirname, '../..');
const checkerPath = 'experiments/arc/lspv2_386_independent_verify.js';
const acceptedPath = 'results/raw/arc/2026-11-12_0312_LSPV2_572_ACCEPTED_TOPOLOGICAL_01234.json';
const rejectedPath = 'results/raw/arc/2026-11-12_0312_LSPV2_572_REJECTED_FORWARD_40123.json';
const outPath = 'results/raw/review/2026-11-12_0448_LSPV5_503_OWNER_ORDER_ERASURE_CEGAR_RAW.json';

function blob(bytes) {
  return crypto.createHash('sha1').update(Buffer.from(`blob ${bytes.length}\0`)).update(bytes).digest('hex');
}
function sha256(bytes) { return crypto.createHash('sha256').update(bytes).digest('hex'); }
function pin(rel, expectedBlob) {
  const bytes = fs.readFileSync(path.join(root, rel));
  assert.equal(blob(bytes), expectedBlob, `Git blob drift: ${rel}`);
  return bytes;
}
const checkerBytes = pin(checkerPath, '338305c0ce101704205e57543756b8127074a986');
const acceptedBytes = pin(acceptedPath, 'a681b3fb26083055206a3e13ebde4bbf1ee2a0a8');
const rejectedBytes = pin(rejectedPath, '95e983ad36039ed69958a15cbc5477cd252634d8');
const accepted = JSON.parse(acceptedBytes);
const rejected = JSON.parse(rejectedBytes);

function packetBytes(packet) { return Buffer.from(JSON.stringify(packet) + '\n'); }
function runNative(packet) {
  const tmpDir = path.join(root, 'results/raw/review/503_cases');
  fs.mkdirSync(tmpDir, {recursive: true});
  const bytes = packetBytes(packet);
  const file = path.join(tmpDir, `packet_${sha256(bytes).slice(0, 20)}.json`);
  fs.writeFileSync(file, bytes);
  const p = spawnSync(process.execPath, [path.join(root, checkerPath), file], {
    encoding: 'utf8', timeout: 9000, maxBuffer: 1024 * 1024
  });
  const ok = p.status === 0;
  return {
    verdict: ok ? 'ACCEPT' : 'REJECT',
    sha256: sha256(bytes),
    bytes: bytes.length,
    stdout: ok ? JSON.parse(p.stdout.trim()) : null,
    diagnostic: ok ? null : (p.stderr || p.stdout).match(/Error: [^\n]+/)?.[0] || 'checker rejection'
  };
}

// The hostile abstraction keeps all packet fields but replaces the chronological
// owner declaration list by its owner-ID-sorted set representation.
function alphaUnordered(packet) {
  const q = structuredClone(packet);
  q.gate_defs = q.gate_defs.slice().sort((a, b) => a[0] - b[0]);
  return packetBytes(q);
}

const owners = new Map(accepted.gate_defs.map(row => [row[0], row]));
const producerByWire = new Map(accepted.gate_defs.map(row => [Math.abs(row[1]), row[0]]));
const deps = new Map();
for (const [id, row] of owners) {
  deps.set(id, row.slice(2).map(Math.abs).filter(w => producerByWire.has(w)).map(w => producerByWire.get(w)));
}
function topological(order) {
  const seen = new Set();
  for (const id of order) {
    if (!deps.get(id).every(p => seen.has(p))) return false;
    seen.add(id);
  }
  return true;
}
function firstPrefixFailure(order) {
  const declared = new Set();
  for (let i = 0; i < order.length; i++) {
    const id = order[i];
    const missing = deps.get(id).filter(p => !declared.has(p));
    if (missing.length) return {index: i, owner: id, missingProducers: missing};
    declared.add(id);
  }
  return null;
}
function permutations(xs) {
  if (!xs.length) return [[]];
  return xs.flatMap((x, i) => permutations(xs.filter((_, j) => j !== i)).map(r => [x, ...r]));
}

const all = [];
const projectionHashes = new Set();
for (const order of permutations([...owners.keys()].sort((a, b) => a - b))) {
  const packet = structuredClone(accepted);
  packet.gate_defs = order.map(id => owners.get(id));
  const native = runNative(packet);
  const legal = topological(order);
  assert.equal(native.verdict, legal ? 'ACCEPT' : 'REJECT', `native/order mismatch ${order.join('')}`);
  const projection = alphaUnordered(packet);
  const projectionHash = sha256(projection);
  projectionHashes.add(projectionHash);
  all.push({order: order.join(''), legal, native: native.verdict, packetSHA256: native.sha256,
    projectionSHA256: projectionHash, firstPrefixFailure: firstPrefixFailure(order), diagnostic: native.diagnostic});
}

assert.equal(all.length, 120);
assert.equal(all.filter(x => x.native === 'ACCEPT').length, 6);
assert.equal(all.filter(x => x.native === 'REJECT').length, 114);
assert.equal(projectionHashes.size, 1);
assert(alphaUnordered(accepted).equals(alphaUnordered(rejected)));
assert(alphaUnordered(accepted).equals(acceptedBytes));

const nativeAccepted = runNative(accepted);
const nativeRejected = runNative(rejected);
const nativeProjection = runNative(JSON.parse(alphaUnordered(rejected)));
assert.equal(nativeAccepted.verdict, 'ACCEPT');
assert.equal(nativeRejected.verdict, 'REJECT');
assert.equal(nativeRejected.diagnostic, 'Error: gate used before declared');
assert.equal(nativeProjection.verdict, 'ACCEPT');
assert.equal(nativeAccepted.stdout.paid, 33);
assert.equal(nativeProjection.stdout.paid, 33);

// Recheck the ten hostile controls from /572 under this exact checker.
const hostiles = [
  ['facet_wrong', d => { d.records[18].c = [-9, 1]; }],
  ['source_forged', d => { d.records[0].c = [-1, 2, 3, -7]; }],
  ['pivot_wrong', d => { d.records.at(-1).pivot = 1; }],
  ['cost_underpay', d => { d.summary.paid_total--; }],
  ['guard_input', d => { d.gate_defs[0][2] = d.spec.guard; }],
  ['duplicate_owner_id', d => { d.gate_defs[1][0] = 0; }],
  ['missing_owner', d => { d.gate_defs.pop(); }],
  ['future_dependency', d => { d.gate_defs[0][2] = 12; }],
  ['unsupported_AND3_in_386_only', d => { d.records[17].kind = 'AND3'; }],
  ['unsupported_LOCAL_CONVERT_in_386_only', d => { d.records[17].kind = 'LOCAL-CONVERT'; }]
].map(([name, mutate]) => {
  const d = structuredClone(accepted); mutate(d); const result = runNative(d);
  assert.equal(result.verdict, 'REJECT', `hostile accepted: ${name}`);
  return {name, verdict: result.verdict, diagnostic: result.diagnostic, sha256: result.sha256};
});

const result = {
  schema: 'LSPV5-503-OWNER-ORDER-ERASURE-CEGAR/v1',
  timestamp: '2026-11-12 04:48 America/Los_Angeles',
  scope: 'Pinned /386 restricted native owner-declaration phase only; not full historical R_mix341 authentication or an asymptotic lower bound.',
  pins: {
    checker: {path: checkerPath, gitBlob: blob(checkerBytes)},
    accepted: {path: acceptedPath, gitBlob: blob(acceptedBytes), sha256: sha256(acceptedBytes)},
    rejected: {path: rejectedPath, gitBlob: blob(rejectedBytes), sha256: sha256(rejectedBytes)}
  },
  ownerDependencies: [...deps].map(([owner, predecessors]) => ({owner, predecessors})),
  replay: {
    permutations: all.length,
    nativeAccepted: all.filter(x => x.native === 'ACCEPT').length,
    nativeRejected: all.filter(x => x.native === 'REJECT').length,
    checkerAcceptedAssertions: all.filter(x => x.native === 'ACCEPT').reduce((s, x) => {
      const packet = structuredClone(accepted); packet.gate_defs = x.order.split('').map(Number).map(id => owners.get(id));
      return s + runNative(packet).stdout.assertions;
    }, 0),
    uniqueOrderErasedStates: projectionHashes.size,
    commonProjectionSHA256: [...projectionHashes][0],
    hostileRejections: hostiles.length
  },
  cegarWitness: {
    concreteAccepted: nativeAccepted,
    concreteRejected: nativeRejected,
    zeroCostAbstractCanonicalization: {
      fromRejectedSHA256: nativeRejected.sha256,
      toProjectionSHA256: nativeProjection.sha256,
      abstractCost: 0,
      concreteRuleExists: false,
      replayVerdict: nativeProjection.verdict,
      classification: 'SPURIOUS: only the rejected preimage lacks a concrete chronological replay; the accepted projection remains genuine.'
    },
    repairedPrefixState: {
      state: '(declared owner IDs, available output wires, once-paid owner IDs)',
      rejectedOrder: rejected.gate_defs.map(row => row[0]).join(''),
      firstFailure: firstPrefixFailure(rejected.gate_defs.map(row => row[0])),
      rule: 'owner o may be declared iff every owner-produced input wire has a producer in the declared prefix; a fresh owner adds paid cost 1 exactly once.'
    }
  },
  hostiles,
  cases: all,
  statuses: {P2_D1: 'OPEN', P2_C3: 'OPEN', P2_B1: 'OPEN', P2_B2_B3_transfer: 'UNSUPPORTED', P_vs_NP: 'OPEN'}
};

fs.mkdirSync(path.dirname(path.join(root, outPath)), {recursive: true});
fs.writeFileSync(path.join(root, outPath), JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify({id: result.schema, replay: result.replay, witness: result.cegarWitness,
  rawPath: outPath, rawSHA256: sha256(fs.readFileSync(path.join(root, outPath)))}, null, 2));
