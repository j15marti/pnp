#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const child = require('node:child_process');
const assert = require('node:assert/strict');

const root = path.resolve(__dirname, '../..');
const paths = {
  checker: path.join(root, 'experiments/arc/lspv2_386_independent_verify.js'),
  seed: path.join(root, 'results/raw/arc/2026-11-12_1031_LSPV4_566_W38_P45_AREA958_NATIVE386_ACCEPTED.json'),
  peerRunner: path.join(root, 'experiments/arc/lspv4_569_free_facet_reference_width.cjs')
};
const pins = {
  checkerSha256: '22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113',
  checkerBlob: '338305c0ce101704205e57543756b8127074a986',
  seedBlob: '28fc9f41ec151a741e70274637c06629fb9a224f',
  peerRunnerBlob: '1f7b0e10dddb0fa76e507a5dbe09b1cccc2c694e'
};

const sha256 = b => crypto.createHash('sha256').update(b).digest('hex');
const gitBlob = b => crypto.createHash('sha1').update(`blob ${b.length}\0`).update(b).digest('hex');
const clone = x => JSON.parse(JSON.stringify(x));
const buffers = Object.fromEntries(Object.entries(paths).map(([k, p]) => [k, fs.readFileSync(p)]));
assert.equal(sha256(buffers.checker), pins.checkerSha256);
assert.equal(gitBlob(buffers.checker), pins.checkerBlob);
assert.equal(gitBlob(buffers.seed), pins.seedBlob);
assert.equal(gitBlob(buffers.peerRunner), pins.peerRunnerBlob);

const seed = JSON.parse(buffers.seed.toString('utf8'));
const firstRes = seed.records.findIndex(r => r.kind === 'RES');
const terminal = seed.records.length - 1;
assert.equal(firstRes, 23);
assert.equal(terminal, 57);
assert.equal(seed.summary.paid_total, 38);
const facet = clone(seed.records.find(r => r.kind === 'DEF'));
assert.deepEqual(facet, {kind: 'DEF', c: [1, -8], parents: [], gate: 0});

function variant(k, where) {
  const d = clone(seed);
  d.records = [];
  for (let i = 0; i < seed.records.length; i++) {
    if (i === where) for (let j = 0; j < k; j++) d.records.push(clone(facet));
    const r = clone(seed.records[i]);
    r.parents = r.parents.map(p => p >= where ? p + k : p);
    d.records.push(r);
  }
  d.summary.def_views += k;
  d.summary.live_records += k;
  return d;
}

function erasePadding(d, k, where) {
  const q = clone(d);
  const removed = q.records.splice(where, k);
  assert(removed.every(r => JSON.stringify(r) === JSON.stringify(facet)));
  q.records.forEach(r => { r.parents = r.parents.map(p => p >= where + k ? p - k : p); });
  q.summary.def_views -= k;
  q.summary.live_records -= k;
  return q;
}

function signature(d) {
  const kinds = Object.fromEntries(['SOURCE', 'DEF', 'RES'].map(k => [k, d.records.filter(r => r.kind === k).length]));
  return {
    spec: d.spec,
    gate_defs: d.gate_defs,
    paid_total: d.summary.paid_total,
    paid_gates: d.summary.paid_gates,
    resolution: d.summary.resolution,
    source: d.summary.source,
    kinds
  };
}

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lspv5-512-'));
function native(d, name, expect) {
  const pth = path.join(tmp, `${name}.json`);
  fs.writeFileSync(pth, JSON.stringify(d));
  const p = child.spawnSync(process.execPath, [paths.checker, pth], {encoding: 'utf8', maxBuffer: 16 * 1024 * 1024});
  assert.equal(p.status === 0, expect, `${name}: ${p.stderr}`);
  return expect ? JSON.parse(p.stdout.trim()) : {status: p.status, rejected: true, stderr: p.stderr.split('\n').find(x => x.startsWith('Error:')) || 'threw'};
}

const matrix = [];
const ks = [0, 1, 44, 77, 1024];
try {
  for (const k of ks) {
    const row = {k};
    for (const [label, where] of [['front', firstRes], ['late', terminal]]) {
      const packet = variant(k, where);
      assert.deepEqual(erasePadding(packet, k, where), seed);
      assert.deepEqual(signature(packet), {
        spec: seed.spec,
        gate_defs: seed.gate_defs,
        paid_total: 38,
        paid_gates: 3,
        resolution: 35,
        source: 17,
        kinds: {SOURCE: 17, DEF: 6 + k, RES: 35}
      });
      const out = native(packet, `${label}_${k}`, true);
      assert.equal(out.assertions, 3915 + 42 * k);
      assert.equal(out.paid, 38);
      assert.equal(out.negativeTests, 11);
      row[label] = {bytes: Buffer.byteLength(JSON.stringify(packet)), assertions: out.assertions, normalized_exactly_to_seed: true};
    }
    matrix.push(row);
  }

  const hostileBase = variant(77, firstRes);
  const controls = [
    ['source_clause_forged', d => { d.records[0].c = [-7]; }],
    ['free_facet_forged', d => { d.records[firstRes].c = [7]; }],
    ['free_facet_owner_forged', d => { d.records[firstRes].gate = 99; }],
    ['free_facet_parent_added', d => { d.records[firstRes].parents = [0]; }],
    ['terminal_pivot_forged', d => { d.records.at(-1).pivot = 123456; }],
    ['terminal_clause_forged', d => { d.records.at(-1).c = [1]; }],
    ['forward_reference', d => { d.records.at(-1).parents[0] = d.records.length; }],
    ['underpaid_total', d => { d.summary.paid_total--; }],
    ['wrong_free_facet_count', d => { d.summary.def_views--; }],
    ['deleted_original_parent', d => { d.records.at(-1).parents.pop(); }]
  ];
  const hostiles = controls.map(([name, mutate]) => {
    const d = clone(hostileBase); mutate(d); return {name, ...native(d, `hostile_${name}`, false)};
  });

  const result = {
    run: 'LSPV-5/512',
    status: 'PASS_COMPUTATIONAL_VALIDATION',
    node: process.version,
    platform: `${process.platform}/${process.arch}`,
    pins,
    source_bytes: Object.fromEntries(Object.entries(buffers).map(([k, b]) => [k, b.length])),
    theorem_scope: {
      sibling: 'archived /386 SOURCE/DEF/RES CLI only',
      seed: 'fixed W38 certificate',
      placements: ['before first RES', 'before terminal RES'],
      per_facet_positive_checks: 7,
      bundled_negative_controls_traversing_all_added_facets: 5,
      exact_cli_slope: 42,
      exact_formula: '3915 + 42*k'
    },
    seed_signature: signature(seed),
    matrix,
    hostiles,
    summary: {positive_packets_accepted: matrix.length * 2, hostile_packets_rejected: hostiles.length, semantic_drift_detected: false}
  };
  console.log(JSON.stringify(result, null, 2));
} finally {
  fs.rmSync(tmp, {recursive: true, force: true});
}
