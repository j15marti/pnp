#!/usr/bin/env node
'use strict';

// LSPV-5/482: accepted prototype-sensitive identifier corpus for the pinned
// recovered /341 SOURCE/AND3/XOR checker. The checker itself correctly uses
// Map. This falsifies a proposed P2-C3 transformer that replaces Map with an
// ordinary `{}` dictionary. It is not a full historical R_mix341 audit.

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const cp = require('node:child_process');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');

// The audit is developed from a scratch root but published under
// experiments/review/. Resolve both layouts without changing the tested bytes.
const root = fs.existsSync(path.join(__dirname, 'experiments', 'arc'))
  ? __dirname : path.resolve(__dirname, '..', '..');
const producerPath = path.join(root, 'experiments/arc/lspv2_341_mixed_tseitin_min_dag.js');
const checkerPath = path.join(root, 'experiments/arc/lspv2_341_independent_verify.js');
const expectedGitBlob = {
  producer: '4081022e8a3841d79f751a3d3a7a10decbb026da',
  checker: 'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0'
};

function sha256(bytes) { return crypto.createHash('sha256').update(bytes).digest('hex'); }
function gitBlob(bytes) {
  return crypto.createHash('sha1').update(Buffer.from(`blob ${bytes.length}\0`)).update(bytes).digest('hex');
}
assert.equal(gitBlob(fs.readFileSync(producerPath)), expectedGitBlob.producer);
assert.equal(gitBlob(fs.readFileSync(checkerPath)), expectedGitBlob.checker);

const produced = cp.spawnSync(process.execPath, [producerPath], {
  encoding: 'utf8', maxBuffer: 16 * 1024 * 1024, timeout: 20000
});
assert.equal(produced.status, 0, produced.stderr);
const all = JSON.parse(produced.stdout);
const fixture0 = all.fixtures.find(x => x.graph.name === 'K4');
assert(fixture0 && fixture0.clauses.length === 16 && fixture0.proof.length === 15);

function clone(x) { return JSON.parse(JSON.stringify(x)); }
function rewriteIds(f, mapping) {
  for (const c of f.clauses) if (mapping.has(c.id)) c.id = mapping.get(c.id);
  for (const p of f.proof) {
    if (mapping.has(p.id)) p.id = mapping.get(p.id);
    p.parents = p.parents.map(id => mapping.has(id) ? mapping.get(id) : id);
  }
  for (const d of f.deleted) if (mapping.has(d.sourceId)) d.sourceId = mapping.get(d.sourceId);
  return f;
}

const mapping = new Map([
  ['s0', '__proto__'], ['s1', 'constructor'], ['s2', 'toString'],
  ['s3', 'hasOwnProperty'], ['d0', 'valueOf'], ['d1', 'isPrototypeOf'],
  ['d14', '__defineGetter__']
]);
const hostile = rewriteIds(clone(fixture0), mapping);
const dangling = clone(hostile);
dangling.proof[0].parents[0] = 's0';
const duplicate = clone(hostile);
duplicate.clauses[1].id = '__proto__';

function packet(f) {
  return Buffer.from(JSON.stringify({
    fixtures: [f], summary: [all.summary.find(x => x.name === 'K4')]
  }), 'utf8');
}

function runChecker(raw) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'pnp-lspv5-482-'));
  const file = path.join(dir, 'packet.json');
  try {
    fs.writeFileSync(file, raw);
    const run = cp.spawnSync(process.execPath, [checkerPath, file], {
      encoding: 'utf8', maxBuffer: 16 * 1024 * 1024, timeout: 20000
    });
    let parsed = null;
    try { parsed = JSON.parse(run.stdout); } catch {}
    return { accepted: run.status === 0 && parsed !== null, status: run.status,
      parsed, stderr: run.stderr.slice(0, 320) };
  } finally { fs.rmSync(dir, { recursive: true, force: true }); }
}

const baselineBytes = packet(fixture0);
const hostileBytes = packet(hostile);
const danglingBytes = packet(dangling);
const duplicateBytes = packet(duplicate);
const baselineRun = runChecker(baselineBytes);
const hostileRun = runChecker(hostileBytes);
const danglingRun = runChecker(danglingBytes);
const duplicateRun = runChecker(duplicateBytes);
assert(baselineRun.accepted && hostileRun.accepted);
assert.equal(baselineRun.parsed.checks, 1401);
assert.equal(hostileRun.parsed.checks, 1401);
assert(!danglingRun.accepted && !duplicateRun.accepted);

function namespaceOnly(f, kind) {
  let dict;
  if (kind === 'map') dict = new Map();
  else if (kind === 'null-object') dict = Object.create(null);
  else dict = {};
  const has = id => kind === 'map' ? dict.has(id)
    : kind === 'null-object' ? Object.prototype.hasOwnProperty.call(dict, id)
      : dict[id] !== undefined;
  const get = id => kind === 'map' ? dict.get(id) : dict[id];
  const put = (id, value) => kind === 'map' ? dict.set(id, value) : (dict[id] = value);
  try {
    for (const c of f.clauses) {
      if (has(c.id)) throw Error('duplicate source');
      put(c.id, { kind: 'source', id: c.id });
    }
    for (const p of f.proof) {
      if (has(p.id)) throw Error('duplicate paid');
      if (p.parents.length !== 2 || !get(p.parents[0]) || !get(p.parents[1])) throw Error('missing parent');
      put(p.id, { kind: 'paid', id: p.id });
    }
    return { accepted: true, prototypeIsObjectPrototype: kind === 'object' ? Object.getPrototypeOf(dict) === Object.prototype : null };
  } catch (e) {
    return { accepted: false, error: e.message,
      prototypeIsObjectPrototype: kind === 'object' ? Object.getPrototypeOf(dict) === Object.prototype : null };
  }
}

const namespace = {
  baselineMap: namespaceOnly(fixture0, 'map'),
  hostileMap: namespaceOnly(hostile, 'map'),
  baselineObject: namespaceOnly(fixture0, 'object'),
  hostileObject: namespaceOnly(hostile, 'object'),
  hostileNullObject: namespaceOnly(hostile, 'null-object')
};
assert(namespace.baselineMap.accepted && namespace.hostileMap.accepted);
assert(namespace.baselineObject.accepted);
assert(!namespace.hostileObject.accepted);
assert(namespace.hostileNullObject.accepted);

// A second common failure mode: assign without a prior own-property check.
const polluted = {};
const beforeProto = Object.getPrototypeOf(polluted);
polluted.__proto__ = { marker: 'source-record' };
const uncheckedAssignment = {
  prototypeChanged: Object.getPrototypeOf(polluted) !== beforeProto,
  inheritedMarker: polluted.marker,
  ownsProtoKey: Object.prototype.hasOwnProperty.call(polluted, '__proto__')
};
assert(uncheckedAssignment.prototypeChanged && uncheckedAssignment.inheritedMarker === 'source-record');
assert(!uncheckedAssignment.ownsProtoKey);

let models = 0;
for (let mask = 0; mask < 64; mask++) {
  if (hostile.clauses.every(c => c.literals.some(lit =>
    lit > 0 ? ((mask >> (lit - 1)) & 1) === 1 : ((mask >> (-lit - 1)) & 1) === 0))) models++;
}
assert.equal(models, 0);

const result = {
  experiment: 'LSPV-5/482', timestamp: '2026-11-10 22:48 PST', node: process.version,
  scope: 'Pinned recovered /341 SOURCE/AND3/XOR K4 fixture checker only; full historical R_mix341 parser remains unauthenticated.',
  pinnedGitBlobs: expectedGitBlob,
  mapping: Object.fromEntries(mapping),
  K4: { variables: 6, clauses: 16, modelsOf64: models, paidNodes: 15 },
  packets: {
    baseline: { bytes: baselineBytes.length, sha256: sha256(baselineBytes), accepted: baselineRun.accepted, assertions: baselineRun.parsed.checks },
    prototypeKeys: { bytes: hostileBytes.length, sha256: sha256(hostileBytes), accepted: hostileRun.accepted, assertions: hostileRun.parsed.checks,
      base64: hostileBytes.toString('base64') },
    danglingControl: { bytes: danglingBytes.length, sha256: sha256(danglingBytes), accepted: danglingRun.accepted, stderr: danglingRun.stderr },
    duplicateControl: { bytes: duplicateBytes.length, sha256: sha256(duplicateBytes), accepted: duplicateRun.accepted, stderr: duplicateRun.stderr }
  },
  namespace,
  uncheckedAssignment,
  theorem: 'The recovered checker accepts live SOURCE and paid IDs named __proto__, constructor, toString, hasOwnProperty, valueOf, isPrototypeOf, and __defineGetter__. Map preserves them, while an ordinary-object namespace is not semantics-preserving; Map or a null-prototype own-property dictionary is required.',
  status: 'PROVED/RESTRICTED + COMPUTATIONAL transformer counterexample; P2-D1 P2-C3 P2-B1 and separate B3 OPEN; P versus NP OPEN.'
};
const rawPath = path.join(root, 'results/raw/arc/2026-11-10_2248_LSPV5_482_PROTOTYPE_KEY_NAMESPACE_RAW.json');
fs.mkdirSync(path.dirname(rawPath), { recursive: true });
fs.writeFileSync(rawPath, JSON.stringify(result, null, 2) + '\n');
const display = clone(result); display.packets.prototypeKeys.base64 = `[${result.packets.prototypeKeys.base64.length} base64 chars]`;
console.log(JSON.stringify(display, null, 2));
