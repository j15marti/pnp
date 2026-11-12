#!/usr/bin/env node
'use strict';
// LSPV-5/497: independent OS replay of the exact LSPV-1/582 shared-owner packet.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const cp = require('node:child_process');
const crypto = require('node:crypto');

const root = path.resolve(__dirname, '../..');
const checker = path.join(root, 'experiments/arc/lspv2_386_independent_verify.js');
const seedFile = path.join(root, 'results/raw/arc/2026-11-11_1200_LSPV1_579_BRIDGE_DP_W61.json');
const packetFile = path.join(root, 'results/raw/arc/2026-11-11_1503_LSPV1_582_SHARED_OWNER_BATCH_WEAKENING_PACKET.json');
const rawOut = path.join(root, 'results/raw/review/2026-11-11_1548_LSPV5_497_ORIGINAL_386_SHARED_OWNER_REPLAY_RAW.json');
const gitBlob = b => crypto.createHash('sha1').update('blob ' + b.length + '\0').update(b).digest('hex');
const sha256 = b => crypto.createHash('sha256').update(b).digest('hex');
const clone = x => JSON.parse(JSON.stringify(x));

const checkerBytes = fs.readFileSync(checker);
const seedBytes = fs.readFileSync(seedFile);
const packet = JSON.parse(fs.readFileSync(packetFile, 'utf8'));
const packetBytes = Buffer.from(JSON.stringify(packet));
assert.equal(gitBlob(checkerBytes), '338305c0ce101704205e57543756b8127074a986');
assert.equal(gitBlob(seedBytes), '807aaf7b7cf5e4a4feb29c2599f9e582ea140e30');
assert.equal(gitBlob(packetBytes), 'd3afbee95a49e528134dc036da482a6399297d6d');
assert.equal(packetBytes.length, 7160);

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lspv5-497-'));
function run(name, value, expected) {
  const bytes = Buffer.from(JSON.stringify(value));
  const file = path.join(tmp, name + '.json');
  fs.writeFileSync(file, bytes);
  const r = cp.spawnSync(process.execPath, [checker, file], {encoding: 'utf8', timeout: 30000});
  const accepted = r.status === 0;
  assert.equal(accepted, expected, name + ': ' + r.stderr.slice(-500));
  let parsed = null;
  if (accepted) {
    parsed = JSON.parse(r.stdout.trim().split('\n').at(-1));
    assert.equal(parsed.negativeTests, 11);
  }
  return {
    name, expected, accepted, exit_status: r.status,
    exact_input_bytes: bytes.length, exact_input_sha256: sha256(bytes),
    paid: parsed?.paid ?? null, records: parsed?.records ?? null,
    negativeTests: parsed?.negativeTests ?? null,
    assertions: parsed?.assertions ?? null,
    rejected_tail: accepted ? null : r.stderr.trim().slice(-300)
  };
}

const tests = [
  ['seed_W61', JSON.parse(seedBytes), true],
  ['shared_owner_W70', packet, true],
  ['underpaid_W69', q => { q.summary.paid_total = 69; }, false],
  ['forged_facet', q => { q.records[100].c = [-1, 3, 18]; }, false],
  ['reversed_second_pivot', q => { q.records[104].pivot = -18; }, false],
  ['owner_freshness_collision', q => { q.gate_defs[1][1] = 17; }, false],
  ['wrong_second_resolvent', q => { q.records[109].c = [1, -3, 4, 6, -16]; }, false],
  ['future_parent', q => { q.records[106].parents[1] = 110; }, false],
  ['tampered_original_source', q => { q.records[13].c = [1, 4, 6, -16]; }, false],
  ['wrong_facet_owner', q => { q.records[100].gate = 99; }, false],
  ['missing_facet', q => { q.records.splice(101, 1); }, false],
  ['changed_guard', q => { q.spec.guard = 18; }, false]
];

try {
  const results = tests.map(([name, source, expected]) => {
    const value = typeof source === 'function' ? clone(packet) : source;
    if (typeof source === 'function') source(value);
    return run(name, value, expected);
  });
  const report = {
    report: 'LSPV-5/497 independent original /386 CLI replay',
    checker_blob: gitBlob(checkerBytes),
    seed_blob: gitBlob(seedBytes),
    packet_blob: gitBlob(packetBytes),
    packet_exact_bytes: packetBytes.length,
    source_records_byte_equal_to_seed: JSON.stringify(packet.records.slice(0, 41)) === JSON.stringify(JSON.parse(seedBytes).records.slice(0, 41)),
    paid_owner_count: packet.summary.paid_gates,
    paid_resolution_count: packet.summary.resolution,
    declared_paid_total: packet.summary.paid_total,
    reused_facet_indices: [100, 101],
    weakening_result_indices: [103, 105, 107, 109],
    results
  };
  fs.mkdirSync(path.dirname(rawOut), {recursive: true});
  fs.writeFileSync(rawOut, JSON.stringify(report, null, 2) + '\n');
  process.stdout.write(JSON.stringify(report, null, 2) + '\n');
} finally {
  fs.rmSync(tmp, {recursive: true, force: true});
}
