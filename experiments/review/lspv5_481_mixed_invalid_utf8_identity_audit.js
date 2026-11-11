#!/usr/bin/env node
'use strict';

// LSPV-5/481: independent OS-Node replay of the pinned recovered /341
// SOURCE/AND3/XOR checker. This is not a full R_mix341 checker.
// The SOURCE definition uses raw 0x80 while its live parent/deletion
// references use raw 0x81. Node replacement decoding maps both to U+FFFD.

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const cp = require('node:child_process');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');

const root = __dirname;
const producerPath = path.join(root, 'experiments/arc/lspv2_341_mixed_tseitin_min_dag.js');
const checkerPath = path.join(root, 'experiments/arc/lspv2_341_independent_verify.js');
const expectedGitBlob = {
  producer: '4081022e8a3841d79f751a3d3a7a10decbb026da',
  checker: 'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0'
};

function sha256(bytes) {
  return crypto.createHash('sha256').update(bytes).digest('hex');
}
function gitBlob(bytes) {
  return crypto.createHash('sha1')
    .update(Buffer.from(`blob ${bytes.length}\0`))
    .update(bytes).digest('hex');
}
assert.equal(gitBlob(fs.readFileSync(producerPath)), expectedGitBlob.producer);
assert.equal(gitBlob(fs.readFileSync(checkerPath)), expectedGitBlob.checker);

const producer = cp.spawnSync(process.execPath, [producerPath], {
  encoding: 'utf8', maxBuffer: 16 * 1024 * 1024, timeout: 20000
});
assert.equal(producer.status, 0, producer.stderr);
const all = JSON.parse(producer.stdout);
const fixture = all.fixtures.find(x => x.graph.name === 'K4');
assert(fixture && fixture.clauses.length === 16 && fixture.proof.length === 15);
const base = Buffer.from(JSON.stringify({
  fixtures: [fixture],
  summary: [all.summary.find(x => x.name === 'K4')]
}), 'utf8');

function offsets(haystack, needle) {
  const out = [];
  for (let p = 0; (p = haystack.indexOf(needle, p)) >= 0; p += needle.length) out.push(p);
  return out;
}
function replaceAtOffsets(bytes, oldToken, replacements) {
  const where = offsets(bytes, oldToken);
  assert.equal(where.length, replacements.length);
  const chunks = [];
  let pos = 0;
  for (let i = 0; i < where.length; i++) {
    chunks.push(bytes.subarray(pos, where[i]), replacements[i]);
    pos = where[i] + oldToken.length;
  }
  chunks.push(bytes.subarray(pos));
  return { bytes: Buffer.concat(chunks), offsets: where };
}

const qS0 = Buffer.from('"s0"', 'ascii');
const bad80 = Buffer.from([0x22, 0x80, 0x22]);
const bad81 = Buffer.from([0x22, 0x81, 0x22]);
const mixed = replaceAtOffsets(base, qS0, [bad80, bad81, bad81]);
const all80 = replaceAtOffsets(base, qS0, [bad80, bad80, bad80]);
const definitionOnly = replaceAtOffsets(base, qS0, [bad80, qS0, qS0]);
assert(!mixed.bytes.equals(all80.bytes));
assert.equal(mixed.bytes.toString('utf8'), all80.bytes.toString('utf8'));
assert.equal(JSON.stringify(JSON.parse(mixed.bytes.toString('utf8'))),
             JSON.stringify(JSON.parse(all80.bytes.toString('utf8'))));

let models = 0;
for (let mask = 0; mask < 64; mask++) {
  const sat = fixture.clauses.every(c => c.literals.some(lit =>
    lit > 0 ? ((mask >> (lit - 1)) & 1) === 1 : ((mask >> (-lit - 1)) & 1) === 0));
  if (sat) models++;
}
assert.equal(models, 0);

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'pnp-lspv5-481-'));
const cases = [
  ['baseline', base, true],
  ['mixed_definition_80_references_81', mixed.bytes, true],
  ['all_occurrences_80_peer_control', all80.bytes, true],
  ['definition_only_80_dangling_control', definitionOnly.bytes, false]
];
const rows = [];
try {
  for (const [name, raw, expected] of cases) {
    const packet = path.join(tmp, `${name}.json`);
    fs.writeFileSync(packet, raw);
    const run = cp.spawnSync(process.execPath, [checkerPath, packet], {
      encoding: 'utf8', maxBuffer: 16 * 1024 * 1024, timeout: 20000
    });
    let parsed = null;
    try { parsed = JSON.parse(run.stdout); } catch {}
    const accepted = run.status === 0 && parsed !== null;
    assert.equal(accepted, expected, `${name}: ${run.stderr}`);
    if (accepted) {
      assert.equal(parsed.checks, 1401);
      assert.equal(parsed.cases[0].proofNodes, 15);
    }
    let strictUTF8 = true;
    try { new TextDecoder('utf-8', { fatal: true }).decode(raw); }
    catch { strictUTF8 = false; }
    rows.push({
      name, expected, accepted, bytes: raw.length, sha256: sha256(raw),
      strictUTF8, replacementCharacters: (raw.toString('utf8').match(/\ufffd/g) || []).length,
      assertionGroups: parsed?.checks ?? null,
      stderr: accepted ? '' : run.stderr.slice(0, 240)
    });
  }
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

const result = {
  experiment: 'LSPV-5/481',
  timestamp: '2026-11-10 18:48 PST',
  scope: 'Pinned recovered /341 SOURCE/AND3/XOR fixture checker only; full R_mix341 is not authenticated.',
  node: process.version,
  pinnedGitBlobs: expectedGitBlob,
  K4: { variables: 6, clauses: 16, modelsOf64: models, paidNodes: 15 },
  sourceS0RawOccurrences: {
    baselineOffsets: mixed.offsets,
    definitionTokenHex: bad80.toString('hex'),
    parentAndDeletionTokenHex: bad81.toString('hex'),
    decodedValue: '\ufffd'
  },
  mixedRawPacketBase64: mixed.bytes.toString('base64'),
  rows,
  theorem: 'A recovered-checker-accepted shared SOURCE identity need not have equal raw token bytes at definition, parent, and deletion occurrences; Node replacement decoding quotients them before JSON.parse.',
  status: 'PROVED/RESTRICTED + COMPUTATIONAL; P2-D1 P2-C3 P2-B1 and separate B3 OPEN; P versus NP OPEN.'
};
fs.writeFileSync(path.join(root, 'lspv5_481_mixed_invalid_utf8_identity_raw.json'), JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify({ ...result, mixedRawPacketBase64: `[${result.mixedRawPacketBase64.length} base64 chars]` }, null, 2));
