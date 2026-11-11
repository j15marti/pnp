'use strict';
/*
  LSPV-1/577. Unchanged archived /386 checker acceptance-language red team.
  Run from repository root:
    node experiments/arc/lspv1_577_386_cli_arraylike_counterexample.cjs
  Uses Node 18+, original pinned verifier and original signed /575 source.
  Prints machine-readable evidence. Does not modify the native checker.
*/
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const {spawnSync} = require('node:child_process');
const root = path.resolve(__dirname, '../..');
const checkerPath = path.join(root, 'experiments/arc/lspv2_386_independent_verify.js');
const packetPath = path.join(root, 'results/raw/arc/2026-11-11_0900_LSPV1_575_BRIDGE_GUARDED_DP_NATIVE_ACCEPTED.json');
const checkerBytes = fs.readFileSync(checkerPath);
const packetBytes = fs.readFileSync(packetPath);
function gitBlobSha(bytes) {
  return crypto.createHash('sha1')
    .update(Buffer.from('blob ' + bytes.length + '\0'))
    .update(bytes).digest('hex');
}
assert.equal(gitBlobSha(checkerBytes), '338305c0ce101704205e57543756b8127074a986',
  'original checker changed');
assert.equal(gitBlobSha(packetBytes), 'd5de0f477cd736ec5fd7b01be18350f9cb594fd2',
  'original signed packet changed');
const checkerText = checkerBytes.toString('utf8');
const begin = checkerText.indexOf('let tests=0;');
const end = checkerText.indexOf('for(const f of process.argv.slice(2)){');
assert(begin !== -1 && end > begin, 'original checker anchors missing');
const checkProof = new Function(checkerText.slice(begin, end) + '\nreturn checkProof;')();
const original = JSON.parse(packetBytes.toString('utf8'));
const clone = x => JSON.parse(JSON.stringify(x));
function variant(name) {
  const d = clone(original);
  if (name === 'original_array') return d;
  if (name === 'empty_owner_array') {
    d.gate_defs = [];
    d.summary.paid_gates = 0;
    d.summary.paid_total--;
    return d;
  }
  const rows = Object.fromEntries(d.records.map((r, i) => [String(i), r]));
  rows.length = name === 'object_string_length' ? '103'
    : name === 'object_fractional_length' ? 102.5
    : name === 'object_short_length' ? 102 : 103;
  if (name === 'object_bad_last') rows['102'].c = [17];
  d.records = rows;
  return d;
}
function checkCore(d) {
  try { return {accepted: true, result: checkProof(d, {control: true})}; }
  catch (e) { return {accepted: false, error: String(e.message)}; }
}
const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'lspv1-577-'));
const names = [
  'original_array', 'object_numeric_length', 'object_string_length',
  'object_fractional_length', 'object_short_length', 'object_bad_last',
  'empty_owner_array'
];
const rows = [];
try {
  for (let i = 0; i < names.length; i++) {
    const name = names[i], d = variant(name);
    const fn = path.join(dir, 'case-' + i + '.json');
    fs.writeFileSync(fn, JSON.stringify(d) + '\n', 'utf8');
    const c = checkCore(d);
    const osRun = spawnSync(process.execPath, [checkerPath, fn], {
      encoding: 'utf8', timeout: 30000, maxBuffer: 2 * 1024 * 1024
    });
    const accepted = osRun.status === 0 && !osRun.error;
    rows.push({
      name, records_is_array: Array.isArray(d.records),
      length_value: d.records.length, final_pivot: d.records[102].pivot,
      gate_owners: d.gate_defs.length, core_accept: c.accepted,
      cli_accept: accepted, cli_status: osRun.status,
      core_error: c.error || null,
      cli_stderr_tail: (osRun.stderr || '').slice(-500),
      cli_stdout: (osRun.stdout || '').trim()
    });
  }
} finally { fs.rmSync(dir, {recursive: true, force: true}); }
const expected = [
  [true, true], [true, false], [true, false], [true, false],
  [false, false], [false, false], [true, false]
];
rows.forEach((r, i) => {
  assert.equal(r.core_accept, expected[i][0], r.name + ' mathematical core');
  assert.equal(r.cli_accept, expected[i][1], r.name + ' original full CLI');
});
for (const r of rows) {
  const corrected = r.core_accept && r.records_is_array &&
    r.gate_owners > 0 && r.final_pivot !== 999999;
  assert.equal(r.cli_accept, corrected, r.name + ' corrected iff');
}
const evidence = {
  title: 'LSPV-1/577 original /386 array-like parsed-records counterexample',
  status: 'COMPUTATIONAL + PROVED/RESTRICTED source-code criterion',
  checker_git_blob: gitBlobSha(checkerBytes),
  packet_git_blob: gitBlobSha(packetBytes),
  checker_sha256: crypto.createHash('sha256').update(checkerBytes).digest('hex'),
  packet_sha256: crypto.createHash('sha256').update(packetBytes).digest('hex'),
  node: process.version, runtime: 'original unchanged native Node subprocess',
  tested: rows.length, cases: rows,
  theorem: 'Full CLI iff Core AND Array.isArray(records) AND nonempty gate_defs AND final pivot != 999999, for JSON-parseable single-file packets.'
};
process.stdout.write(JSON.stringify(evidence, null, 2) + '\n');
