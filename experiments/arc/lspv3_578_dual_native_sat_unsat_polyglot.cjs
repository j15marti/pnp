#!/usr/bin/env node
'use strict';
// LSPV-3/578. Reproduce the exact 14,032-byte dual-original-checker
// SAT/UNSAT source-mismatch packet and differential hostile controls.
// Requires Node >=18, the repository files below, and no package dependencies.
// This script invokes TWO separate original archived checkers as OS subprocesses.
// Passing both does NOT constitute a single R_mix341 mixed-calculus refutation.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const crypto = require('node:crypto');
const cp = require('node:child_process');
const assert = require('node:assert/strict');

const root = path.resolve(__dirname, '../..');
const files = Object.freeze({
  checker341: 'experiments/arc/lspv2_341_independent_verify.js',
  checker386: 'experiments/arc/lspv2_386_independent_verify.js',
  sat341: 'results/raw/arc/2026-11-11_0424_LSPV3_568_NUMERIC_WRAP32_SAT_ACCEPTED_PACKET.json',
  unsat386: 'results/raw/arc/2026-11-11_1324_LSPV3_577_LIVE_COMPLEMENTARY_NATIVE386_PACKET.json',
  dual: 'results/raw/arc/2026-11-11_1424_LSPV3_578_DUAL_CHECKER_SAT_UNSAT_PACKET.json'
});
const pinnedGitBlobs = Object.freeze({
  checker341: 'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
  checker386: '338305c0ce101704205e57543756b8127074a986',
  sat341: 'adb4864906029ecf7b1cd1cf7a4bf513218a13a8',
  unsat386: '5edeac8fbbe39764cfd3d075acd3c6ce7b5c87fe',
  dual: '1c3b400857ab2cfb7d78f37b2723945e6521a83a'
});
function gitBlob(buffer) {
  return crypto.createHash('sha1')
    .update(Buffer.concat([Buffer.from('blob ' + buffer.length + '\0'), buffer]))
    .digest('hex');
}
const contents = {};
for (const [key, rel] of Object.entries(files)) {
  const bytes = fs.readFileSync(path.join(root, rel));
  assert.equal(gitBlob(bytes), pinnedGitBlobs[key], 'source blob drift: ' + key);
  contents[key] = bytes;
}
const forged = JSON.parse(contents.sat341);
const sound = JSON.parse(contents.unsat386);
const dual = {
  ...forged,
  spec: sound.spec,
  gate_defs: sound.gate_defs,
  records: sound.records,
  summary: { length: forged.fixtures.length, ...sound.summary }
};
const packet = Buffer.from(JSON.stringify(dual) + '\n', 'utf8');
assert.equal(packet.length, 14032, 'unexpected dual certificate byte length');
assert.ok(packet.equals(contents.dual), 'exact dual certificate differs');
const assignment = '101001000000100000';
const f = dual.fixtures[0];
assert.equal(f.graph.edges.length, assignment.length);
const clauseSat = c => c.literals.some(lit =>
  assignment[Math.abs(lit) - 1] === (lit > 0 ? '1' : '0'));
assert.equal(f.clauses.length, 48);
assert.ok(f.clauses.every(clauseSat), 'claimed /341 source is not SAT');
assert.equal(dual.records.filter(r => r.kind === 'SOURCE').length, 49);
assert.equal(dual.summary.paid_total, 35);

const cases = [
  ['dual_baseline', true, true, d => {}],
  ['341_binary_charge', false, true, d => { d.fixtures[0].charges[0] = 1; }],
  ['341_typed_support', false, true, d => {
    const p = d.fixtures[0].proof.find(x => x.rule === 'AND3' && typeof x.support === 'string');
    assert.ok(p); p.support = [0, 1, 12];
  }],
  ['341_wrong_source_literal', false, true, d => {
    d.fixtures[0].clauses[0].literals[0] *= -1;
  }],
  ['341_wrong_terminal', false, true, d => {
    d.fixtures[0].proof.at(-1).row.rhs = 0;
  }],
  ['386_wrong_RES_pivot', true, false, d => {
    d.records.find(r => r.kind === 'RES').pivot = 999999;
  }],
  ['386_wrong_SOURCE', true, false, d => { d.records[0].c = [-7]; }],
  ['386_undercharge', true, false, d => { d.summary.paid_total--; }],
  ['386_gate_collision', true, false, d => { d.gate_defs[0][1] = d.spec.guard; }],
  ['both_malformed', false, false, d => {
    d.fixtures[0].charges[0] = 1;
    d.summary.paid_total--;
  }]
];
const scratch = fs.mkdtempSync(path.join(os.tmpdir(), 'lspv3-578-'));
const testfile = path.join(scratch, 'certificate.json');
function originalChecker(name, data) {
  fs.writeFileSync(testfile, JSON.stringify(data) + '\n', 'utf8');
  const result = cp.spawnSync(process.execPath,
    [path.join(root, files[name]), testfile],
    { encoding: 'utf8', maxBuffer: 32000000, timeout: 30000 });
  if (result.error) throw result.error;
  if (result.status !== 0) {
    return { accepted: false, error: result.stderr.trim().slice(0, 500) };
  }
  const output = JSON.parse(result.stdout);
  return name === 'checker341'
    ? { accepted: true, checks: output.checks, bundled_hostiles: output.corruptions,
        malformed_tests: output.malformed }
    : { accepted: true, assertions: output.assertions,
        bundled_hostiles: output.negativeTests,
        paid: output.paid, RES: output.res, DEF_owners: output.def };
}
const matrix = [];
try {
  for (const [name, expected341, expected386, change] of cases) {
    const changed = JSON.parse(JSON.stringify(dual));
    change(changed);
    const a = originalChecker('checker341', changed);
    const b = originalChecker('checker386', changed);
    assert.equal(a.accepted, expected341, name + ': /341 decision drift');
    assert.equal(b.accepted, expected386, name + ': /386 decision drift');
    if (name === 'dual_baseline') {
      assert.equal(a.checks, 3273);
      assert.equal(b.assertions, 6523);
      assert.equal(b.paid, 35);
      assert.equal(a.bundled_hostiles, 5);
      assert.equal(b.bundled_hostiles, 11);
    }
    matrix.push({ name, original341: a, original386: b,
      expected341, expected386, pass: true });
  }
} finally {
  fs.rmSync(scratch, { recursive: true, force: true });
}
const result = {
  id: 'LSPV-3/578',
  execution: 'actual OS Node subprocesses, unchanged separate archived checkers',
  source_binding: 'TWO DISTINCT IN-BAND SOURCE FORMULAS, NOT ONE SOURCE',
  actual_mixed_calculus_checker: false,
  packet_bytes: packet.length,
  packet_sha256: crypto.createHash('sha256').update(packet).digest('hex'),
  source341: { satisfiable: true, assignment,
    satisfied: f.clauses.filter(clauseSat).length, total: f.clauses.length,
    paid_AND3_XOR: f.proof.length },
  source386: { guarded_odd_parity_UNSAT: true,
    paid_RES: dual.summary.resolution,
    paid_gate_owners: dual.summary.paid_gates,
    free_facets: dual.summary.def_views, paid_total: dual.summary.paid_total },
  cases: matrix,
  all_pass: matrix.length === 10,
  proof_obligations: ['P2-D1', 'P2-C3', 'P2-B1', 'P2-B2/B3'],
  p_vs_np: 'OPEN'
};
console.log(JSON.stringify(result, null, 2));
