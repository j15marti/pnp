#!/usr/bin/env node
'use strict';
// Stage connector-fetched files with one transport-added LF removed, then run
// the unchanged current peer scripts in isolated temporary repository roots.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const cp = require('node:child_process');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '../..');
const cases = [
  {
    role: 'LSPV-2/566',
    script: 'experiments/arc/lspv2_566_native386_wire_alpha.cjs',
    args: [],
    files: [
      'experiments/arc/lspv2_386_independent_verify.js',
      'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json',
      'results/raw/arc/2026-11-11_0812_LSPV2_559_EXTERNAL_K4_SIGNED_SOURCE.cnf'
    ]
  },
  {
    role: 'LSPV-3/579',
    script: 'experiments/arc/lspv3_579_terminal_live_batch_copy.cjs',
    args: [],
    files: [
      'experiments/arc/lspv2_386_independent_verify.js',
      'results/raw/arc/2026-11-11_1324_LSPV3_577_LIVE_COMPLEMENTARY_NATIVE386_PACKET.json'
    ]
  },
  {
    role: 'LSPV-4/552',
    script: 'experiments/arc/lspv4_552_fanout_reference_firewall.cjs',
    args: ['--native'],
    files: [
      'experiments/arc/lspv2_386_independent_verify.js',
      'results/raw/arc/2026-11-11_1436_LSPV4_551_W61_MIN_SLOT_THEN_BYTE_AREA_ACCEPTED.json'
    ]
  }
];
function stage(temp, rel, stripOneLf) {
  const source = path.join(root, rel);
  const target = path.join(temp, rel);
  fs.mkdirSync(path.dirname(target), {recursive: true});
  let bytes = fs.readFileSync(source);
  if (stripOneLf && bytes.at(-1) === 10) bytes = bytes.subarray(0, bytes.length - 1);
  fs.writeFileSync(target, bytes);
}
const results = [];
for (const item of cases) {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'lspv5-497-peer-'));
  try {
    stage(temp, item.script, false);
    for (const rel of item.files) stage(temp, rel, rel !== 'experiments/arc/lspv2_386_independent_verify.js');
    const script = path.join(temp, item.script);
    let staged_probe = null;
    if (item.role === 'LSPV-3/579') {
      const p = JSON.parse(fs.readFileSync(path.join(temp, item.files[1]), 'utf8'));
      staged_probe = [3, 5, 6].map(i => ({i, c: p.records[i].c}));
    }
    const run = cp.spawnSync(process.execPath, [script, ...item.args], {
      encoding: 'utf8', timeout: 30000, maxBuffer: 8 * 1024 * 1024
    });
    const result = {
      role: item.role,
      original_script_unmodified: true,
      passed: run.status === 0,
      exit_status: run.status,
      stdout: run.stdout.trim(),
      stderr: run.stderr.trim(),
      staged_probe
    };
    if (item.role === 'LSPV-3/579' && run.status !== 0) {
      const original = fs.readFileSync(script, 'utf8');
      const needle = "d.records=[...seed.records.slice(0,cut),...extra,...oldTail];";
      const replacement = "d.records=[...seed.records.slice(0,cut).map(copy),...extra,...oldTail];";
      assert.equal(original.split(needle).length, 2, 'repair target must occur exactly once');
      const repaired = original.replace(needle, replacement);
      const repairedPath = path.join(temp, 'experiments/arc/lspv3_579_terminal_live_batch_copy_repaired.cjs');
      fs.writeFileSync(repairedPath, repaired);
      const rr = cp.spawnSync(process.execPath, [repairedPath], {
        encoding: 'utf8', timeout: 30000, maxBuffer: 8 * 1024 * 1024
      });
      result.minimal_repair = {
        edit: 'deep-copy seed.records.slice(0,cut) before hostile mutations',
        repaired_script_sha256: crypto.createHash('sha256').update(repaired).digest('hex'),
        exit_status: rr.status,
        passed: rr.status === 0,
        stdout: rr.stdout.trim(),
        stderr: rr.stderr.trim()
      };
    }
    results.push(result);
  } finally {
    fs.rmSync(temp, {recursive: true, force: true});
  }
}
const report = {status: results.every(x => x.passed) ? 'PASS' : 'PEER_REPLAY_FAILURE',
  staged_transport_lf_removed: true, results};
const out = path.join(root, 'results/raw/review/2026-11-11_1548_LSPV5_497_PEER_REPLAY_RAW.json');
fs.mkdirSync(path.dirname(out), {recursive: true});
fs.writeFileSync(out, JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify(report, null, 2));
