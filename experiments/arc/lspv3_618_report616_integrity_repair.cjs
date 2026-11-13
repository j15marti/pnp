'use strict';
// LSPV-3/618 exact report-616 publication-integrity checker.
// Run from any directory with node <repo>/experiments/arc/lspv3_618_report616_integrity_repair.cjs.
// Requires pinned Git blobs in the current repository checkout.
const assert = require('node:assert/strict');
const cp = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const ROOT = path.resolve(__dirname, '../..');
const BEFORE = '9f50f61932b676a60c86edafa80ce672edbe00ae';
const AFTER = 'c1fc4553a79d8dbc70993013b6f6cc9028627377';
const SENTINEL = 'END_OF_VERIFIED_REPORT::LSPV-3::616';
const readBlob = (sha) => cp.execFileSync('git', ['cat-file', 'blob', sha], {
  cwd: ROOT, encoding: 'utf8', maxBuffer: 4 * 1024 * 1024
});
const expectedRepair = (before) => before.replace(/\s+$/, '') + '\n\n' + SENTINEL + '\n';
const validRepair = (before, after) =>
  after === expectedRepair(before) && after.trimEnd().endsWith(SENTINEL) &&
  after.split(SENTINEL).length === 2;

const before = readBlob(BEFORE);
const after = readBlob(AFTER);
assert.equal(before.length, 8375);
assert.equal(after.length, 8412);
assert(validRepair(before, after), 'scientific body modified or sentinel missing');
const negative = [
  ['missing sentinel', before],
  ['wrong role', after.replace(SENTINEL, 'END_OF_VERIFIED_REPORT::LSPV-3::617')],
  ['duplicated sentinel', after + SENTINEL + '\n'],
  ['changed scientific body', 'CORRUPTED\n' + after],
  ['nonterminal sentinel', after + 'extra text\n'],
  ['silent whitespace mutation', before.replace('P2-D1', 'P2-D1 ') + '\n\n' + SENTINEL + '\n']
];
for (const [name, candidate] of negative) {
  assert.equal(validRepair(before, candidate), false, name);
}
const main = fs.readFileSync(path.join(ROOT, 'main.tex'), 'utf8');
const begin = '% BEGIN LSPV-3 OWNED';
const end = '% END LSPV-3 OWNED';
const i = main.indexOf(begin), j = main.indexOf(end);
assert(i >= 0 && j > i, 'ownership markers');
assert.equal(main.split(begin).length, 2);
assert.equal(main.split(end).length, 2);
const region = main.slice(i, j);
assert(region.includes('LSPV-3/616'));
assert(region.includes('LSPV-3/617'));
console.log(JSON.stringify({
  status: 'PASS', scope: 'report integrity only, not native proof checker',
  original_git_blob: BEFORE, repaired_git_blob: AFTER,
  original_characters: before.length, repaired_characters: after.length,
  scientific_body_preserved: true, exact_final_marker: SENTINEL,
  hostile_controls_rejected: negative.map(([name]) => name),
  main_lspv3_ownership_unchanged: true, affected_proof_status: 'OPEN'
}, null, 2));
