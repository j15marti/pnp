#!/usr/bin/env node
'use strict';

// LSPV-5/504: independent deletion-normalizer audit against the unchanged
// archived /386 CLI. This is not a replacement checker and does not
// authenticate the unavailable full historical R_mix341 dispatcher.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const assert = require('assert');
const {spawnSync} = require('child_process');

const root = path.resolve(__dirname, '../..');
const checkerPath = 'experiments/arc/lspv2_386_independent_verify.js';
const seedPath = 'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json';
const ownersPath = 'results/raw/arc/2026-11-12_0312_LSPV2_572_ACCEPTED_TOPOLOGICAL_01234.json';
const outPath = 'results/raw/review/2026-11-12_0548_LSPV5_504_OWNER_SUBSET_SENTINEL_CEGAR_RAW.json';
const acceptedPath = 'results/raw/review/2026-11-12_0548_LSPV5_504_ROOT_SENTINEL_ACCEPTED.json';
const rejectedPath = 'results/raw/review/2026-11-12_0548_LSPV5_504_CHILD_SENTINEL_REJECTED.json';

function gitBlob(bytes) {
  return crypto.createHash('sha1').update(Buffer.from(`blob ${bytes.length}\0`)).update(bytes).digest('hex');
}
function sha256(bytes) { return crypto.createHash('sha256').update(bytes).digest('hex'); }
function pin(rel, expected) {
  const bytes = fs.readFileSync(path.join(root, rel));
  assert.equal(gitBlob(bytes), expected, `Git blob drift: ${rel}`);
  return bytes;
}
const checkerBytes = pin(checkerPath, '338305c0ce101704205e57543756b8127074a986');
const seedBytes = pin(seedPath, '318c52d99977ea4e91bc8554051138a700c1dc94');
const ownersBytes = pin(ownersPath, 'a681b3fb26083055206a3e13ebde4bbf1ee2a0a8');
const seed = JSON.parse(seedBytes);
const ownerPacket = JSON.parse(ownersBytes);
const owners = ownerPacket.gate_defs;
assert.equal(owners.length, 5);
assert.equal(seed.summary.def_views, 0);
assert.equal(seed.summary.resolution, 28);
assert.equal(seed.records.filter(r => r.kind === 'DEF').length, 0);

const producer = new Map(owners.map((r, i) => [Math.abs(r[1]), i]));
const deps = owners.map(r => r.slice(2).map(Math.abs).filter(w => producer.has(w)).map(w => producer.get(w)));
assert.deepEqual(deps, [[], [], [0], [1], [2, 3]]);

function packetFor(mask, order = null) {
  const p = structuredClone(seed);
  const ids = order || owners.map((_, i) => i).filter(i => mask & (1 << i));
  p.gate_defs = ids.map(i => structuredClone(owners[i]));
  p.summary.paid_gates = ids.length;
  p.summary.paid_total = p.summary.resolution + ids.length;
  return p;
}
function packetBytes(p) { return Buffer.from(JSON.stringify(p) + '\n'); }
function runNative(p) {
  const dir = path.join(root, 'results/raw/review/504_cases');
  fs.mkdirSync(dir, {recursive: true});
  const bytes = packetBytes(p);
  const file = path.join(dir, `${sha256(bytes).slice(0, 24)}.json`);
  fs.writeFileSync(file, bytes);
  const q = spawnSync(process.execPath, [path.join(root, checkerPath), file], {
    encoding: 'utf8', timeout: 9000, maxBuffer: 1024 * 1024
  });
  const ok = q.status === 0;
  return {
    verdict: ok ? 'ACCEPT' : 'REJECT',
    sha256: sha256(bytes), bytes: bytes.length,
    stdout: ok ? JSON.parse(q.stdout.trim()) : null,
    diagnostic: ok ? null : (q.stderr || q.stdout).match(/Error: [^\n]+/)?.[0] || 'checker rejection'
  };
}
function downwardClosed(mask) {
  for (let i = 0; i < owners.length; i++) {
    if (!(mask & (1 << i))) continue;
    if (!deps[i].every(j => mask & (1 << j))) return false;
  }
  return true;
}
function alphaCountOnly(p) {
  return Buffer.from(JSON.stringify({
    spec: p.spec, records: p.records, summary: p.summary,
    owner_count: p.gate_defs.length
  }) + '\n');
}

const cases = [];
for (let mask = 0; mask < 32; mask++) {
  const p = packetFor(mask);
  const native = runNative(p);
  const expected = mask !== 0 && downwardClosed(mask);
  assert.equal(native.verdict, expected ? 'ACCEPT' : 'REJECT', `mask ${mask.toString(2).padStart(5, '0')}`);
  cases.push({
    mask, bits: mask.toString(2).padStart(5, '0'), owners: p.gate_defs.map(r => r[0]),
    predecessorClosed: downwardClosed(mask), expected: expected ? 'ACCEPT' : 'REJECT',
    native: native.verdict, diagnostic: native.diagnostic,
    paid: p.summary.paid_total, bytes: native.bytes, sha256: native.sha256
  });
}

const root0 = packetFor(1 << 0);
const root1 = packetFor(1 << 1);
const child2 = packetFor(1 << 2);
const root0Run = runNative(root0);
const root1Run = runNative(root1);
const child2Run = runNative(child2);
assert.equal(root0Run.verdict, 'ACCEPT');
assert.equal(root1Run.verdict, 'ACCEPT');
assert.equal(child2Run.verdict, 'REJECT');
assert(alphaCountOnly(root0).equals(alphaCountOnly(child2)));
assert.equal(root0.summary.paid_total, child2.summary.paid_total);
assert.deepEqual(root0.records, child2.records);
assert.deepEqual(root0.spec, child2.spec);

const hostileDefs = [
  ['underpay', root0, p => { p.summary.paid_total--; }],
  ['forged_source', root0, p => { p.records[0].c = [-1, 2, 3, -7]; }],
  ['guard_input', root0, p => { p.gate_defs[0][2] = p.spec.guard; }],
  ['owner_output_collision', root0, p => { p.gate_defs[0][1] = 7; }],
  ['unsupported_AND3', root0, p => { p.records[17].kind = 'AND3'; }],
  ['terminal_pivot_sentinel', root0, p => { p.records.at(-1).pivot = 999999; }],
  ['duplicate_owner_id', packetFor((1 << 0) | (1 << 1)), p => { p.gate_defs[1][0] = 0; }],
  ['non_topological_order', packetFor((1 << 0) | (1 << 2)), p => { p.gate_defs.reverse(); }]
];
const hostiles = hostileDefs.map(([name, base, mutate]) => {
  const p = structuredClone(base); mutate(p); const r = runNative(p);
  assert.equal(r.verdict, 'REJECT', `hostile accepted: ${name}`);
  return {name, verdict: r.verdict, diagnostic: r.diagnostic, sha256: r.sha256};
});

fs.mkdirSync(path.dirname(path.join(root, outPath)), {recursive: true});
fs.writeFileSync(path.join(root, acceptedPath), packetBytes(root0));
fs.writeFileSync(path.join(root, rejectedPath), packetBytes(child2));
const result = {
  schema: 'LSPV5-504-NATIVE386-OWNER-SUBSET-SENTINEL-CEGAR/v1',
  timestamp: '2026-11-12 05:48 America/Los_Angeles',
  scope: 'Pinned ordinary /386 SOURCE/paid-AND2-owner/strict-RES CLI only; not the full historical R_mix341 dispatcher or an asymptotic lower bound.',
  pins: {
    checker: {path: checkerPath, gitBlob: gitBlob(checkerBytes)},
    seed: {path: seedPath, gitBlob: gitBlob(seedBytes), sha256: sha256(seedBytes)},
    ownerBank: {path: ownersPath, gitBlob: gitBlob(ownersBytes), sha256: sha256(ownersBytes)}
  },
  ownerDependencies: deps.map((predecessors, owner) => ({owner, predecessors})),
  theorem: {
    testedSubsets: cases.length,
    nativeAccepted: cases.filter(x => x.native === 'ACCEPT').length,
    nativeRejected: cases.filter(x => x.native === 'REJECT').length,
    nonemptyPredecessorClosedSubsets: cases.filter(x => x.mask !== 0 && x.predecessorClosed).length,
    assertionGroupsOnAccepted: cases.filter(x => x.native === 'ACCEPT').reduce((s, x) => s + runNative(packetFor(x.mask)).stdout.assertions, 0),
    hostileRejections: hostiles.length,
    classification: 'For this complete five-owner finite DAG, full original CLI acceptance iff the retained subset is nonempty and predecessor-closed.'
  },
  countOnlyCollision: {
    projectionSHA256: sha256(alphaCountOnly(root0)),
    rootOwner0: root0Run,
    alternateRootOwner1: root1Run,
    childOwner2: child2Run,
    equalSource: JSON.stringify(root0.spec) === JSON.stringify(child2.spec),
    equalRecords: JSON.stringify(root0.records) === JSON.stringify(child2.records),
    equalSummaryAndWork: JSON.stringify(root0.summary) === JSON.stringify(child2.summary),
    abstractOwnerCount: 1,
    repairedState: 'exact signed owner tuple plus recursively predecessor-closed owner IDs, declared-output wires, declaration order, and once-paid IDs'
  },
  cegar: {
    acceptedRootSentinelsRemain: [0, 1],
    provedSpuriousChildSingletons: [2, 3, 4],
    rule: 'Replay each cheap abstract sentinel concretely. Refine only rejected non-closed preimages; retain every accepted root-sentinel path.'
  },
  hostiles,
  cases,
  statuses: {P2_D1: 'OPEN', P2_C3: 'OPEN', P2_B1: 'OPEN', P2_B2_B3: 'OPEN', P_vs_NP: 'OPEN'}
};
fs.writeFileSync(path.join(root, outPath), JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify({
  schema: result.schema, theorem: result.theorem, collision: result.countOnlyCollision,
  rawPath: outPath, rawSHA256: sha256(fs.readFileSync(path.join(root, outPath))),
  acceptedPath, rejectedPath
}, null, 2));
