'use strict';

// LSPV-5/513: independent OS-CLI replay and canonical normalizer for the
// array-like `deleted` evidence field accepted by the pinned /341 checker.
// This authenticates only that checker's accepted JSON sublanguage.

const assert = require('assert');
const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');
const {spawnSync} = require('child_process');

const checkerPath = 'experiments/arc/lspv2_341_independent_verify.js';
const packetPath = 'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json';
const expectedCheckerBlob = 'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0';
const expectedPacketBlob = 'fe27fe1011d0021e721ccaeb747ed58da65d7464';
const sha256 = x => crypto.createHash('sha256').update(x).digest('hex');
const gitBlob = x => crypto.createHash('sha1').update('blob ' + Buffer.byteLength(x) + '\0').update(x).digest('hex');
const compact = x => JSON.stringify(x);
const clone = x => JSON.parse(compact(x));
const checkerText = fs.readFileSync(checkerPath, 'utf8');
const packetText = fs.readFileSync(packetPath, 'utf8');
assert.strictEqual(gitBlob(checkerText), expectedCheckerBlob, 'pinned checker changed');
assert.strictEqual(gitBlob(packetText), expectedPacketBlob, 'pinned packet changed');
const baseline = JSON.parse(packetText);

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lspv5-513-'));
let serial = 0;
function runNative(packet) {
  const raw = compact(packet);
  const input = path.join(tmp, `case-${serial++}.json`);
  fs.writeFileSync(input, raw);
  const p = spawnSync(process.execPath, [checkerPath, input], {encoding:'utf8', timeout:30000});
  if (p.status !== 0) {
    return {accepted:false, status:p.status, signal:p.signal, error:(p.stderr || p.stdout).trim().slice(0,240), inputBytes:Buffer.byteLength(raw)};
  }
  const parsed = JSON.parse(p.stdout);
  return {accepted:true, status:p.status, output:parsed, stdoutSha256:sha256(p.stdout), inputBytes:Buffer.byteLength(raw)};
}

function arrayToObject(items, extras=true) {
  const out = {length:items.length};
  for (let i=items.length-1; i>=0; --i) out[String(i)] = clone(items[i]);
  if (extras) {
    out['00'] = {sourceId:'IGNORED_NUMERIC_ALIAS', assignment:null};
    out['4294967295'] = {sourceId:'IGNORED_LARGE_INDEX', assignment:null};
    Object.defineProperty(out, '__proto__', {value:{pollute:'IGNORED'}, enumerable:true, writable:true, configurable:true});
    out.outside = {fake:'IGNORED_METADATA'};
  }
  return out;
}

function objectify(packet, extras=true) {
  const out = clone(packet);
  for (const fixture of out.fixtures) fixture.deleted = arrayToObject(fixture.deleted, extras);
  return JSON.parse(compact(out)); // exercise actual JSON object semantics
}

function normalizeDeleted(packet) {
  const out = clone(packet);
  for (const fixture of out.fixtures) {
    const d = fixture.deleted;
    if (Array.isArray(d)) continue;
    if (d === null || typeof d !== 'object' || !Number.isInteger(d.length) || d.length < 0) {
      throw new Error('noncanonical deleted container');
    }
    const a = new Array(d.length);
    for (let i=0; i<d.length; ++i) a[i] = d[i];
    fixture.deleted = a;
  }
  return out;
}

function sameNative(a,b,label) {
  assert(a.accepted && b.accepted, `${label}: expected two accepts`);
  assert.deepStrictEqual(a.output,b.output,`${label}: native output changed`);
  assert.strictEqual(a.stdoutSha256,b.stdoutSha256,`${label}: stdout changed`);
}

const baseRun = runNative(baseline);
assert(baseRun.accepted, 'baseline rejected');
const objectPacket = objectify(baseline, true);
const objectRun = runNative(objectPacket);
sameNative(baseRun, objectRun, 'object equivalence');
const normalized = normalizeDeleted(objectPacket);
const normalizedRun = runNative(normalized);
sameNative(baseRun, normalizedRun, 'normalized equivalence');
assert.deepStrictEqual(normalized, baseline, 'canonical image differs from original array packet');
assert.deepStrictEqual(normalizeDeleted(normalized), normalized, 'normalizer not idempotent');

const objectBytes = Buffer.byteLength(compact(objectPacket));
const normalizedBytes = Buffer.byteLength(compact(normalized));
assert(normalizedBytes < objectBytes, 'canonical array did not reduce compact serialized bytes');
assert.strictEqual(normalizedBytes, Buffer.byteLength(compact(baseline)));

const perFixture = baseline.fixtures.map((fixture, i) => {
  const one = clone(baseline);
  one.fixtures = [clone(fixture)];
  one.summary = [clone(baseline.summary[i])];
  const obj = objectify(one, true);
  const arr = normalizeDeleted(obj);
  const objRun = runNative(obj), arrRun = runNative(arr);
  sameNative(objRun,arrRun,`fixture ${i}`);
  const ob = Buffer.byteLength(compact(obj)), ab = Buffer.byteLength(compact(arr));
  assert(ab < ob, `fixture ${i}: no byte decrease`);
  return {index:i, graph:fixture.graph.name, sources:fixture.clauses.length, paid:fixture.proof.length,
    objectBytes:ob, canonicalArrayBytes:ab, savedBytes:ob-ab, nativeChecks:objRun.output.checks,
    stdoutSha256:objRun.stdoutSha256};
});

function mutateObject(name, fn) {
  const p = objectify(baseline, false);
  fn(p.fixtures[0].deleted);
  const objectResult = runNative(p);
  let normalizedResult, normalizeError = null;
  try { normalizedResult = runNative(normalizeDeleted(p)); }
  catch (e) { normalizeError = String(e); }
  assert(!objectResult.accepted, `${name}: hostile object accepted`);
  assert(normalizeError !== null || !normalizedResult.accepted, `${name}: hostile canonical image accepted`);
  return {name, objectAccepted:objectResult.accepted,
    canonicalAccepted:normalizedResult ? normalizedResult.accepted : null,
    normalizerRefused:normalizeError !== null,
    objectError:objectResult.error || null,
    canonicalError:normalizeError || (normalizedResult && normalizedResult.error) || null};
}

const hostile = [
  mutateObject('missing_numeric_member', d => { delete d['0']; }),
  mutateObject('wrong_length', d => { d.length--; }),
  mutateObject('string_length', d => { d.length=String(d.length); }),
  mutateObject('forged_source_id', d => { d['0'].sourceId='FORGED'; }),
  mutateObject('swapped_members', d => { const t=d['0']; d['0']=d['1']; d['1']=t; }),
  mutateObject('short_assignment', d => { d['0'].assignment='0'; }),
  mutateObject('scalar_member', d => { d['0']=0; })
];

const arrayForged = clone(baseline);
arrayForged.fixtures[0].deleted[0].sourceId='FORGED';
const arrayForgedRun = runNative(arrayForged);
assert(!arrayForgedRun.accepted, 'forged array witness accepted');

const result = {
  run:'LSPV-5/513', timestamp:'2026-11-12T16:48:00-08:00', node:process.version,
  provenance:{checkerPath, checkerGitBlob:gitBlob(checkerText), checkerSha256:sha256(checkerText),
    packetPath, packetGitBlob:gitBlob(packetText), packetSha256:sha256(packetText),
    execution:'authoritative checker as OS Node subprocess for every case'},
  target:'Every accepted parsed numeric-index deleted object in the pinned /341 checker has a source/goal/work-preserving canonical array image.',
  theoremScope:'Pinned recovered /341 SOURCE/AND3/XOR checker only; not the complete historical R_mix341 byte grammar.',
  baseline:{accepted:baseRun.accepted, bytes:baseRun.inputBytes, checks:baseRun.output.checks, stdoutSha256:baseRun.stdoutSha256},
  allFixturesObject:{accepted:objectRun.accepted, bytes:objectBytes, checks:objectRun.output.checks, stdoutSha256:objectRun.stdoutSha256},
  allFixturesCanonicalArray:{accepted:normalizedRun.accepted, bytes:normalizedBytes, checks:normalizedRun.output.checks,
    stdoutSha256:normalizedRun.stdoutSha256, savedBytes:objectBytes-normalizedBytes,
    exactBaselinePacket:compact(normalized)===compact(baseline), idempotent:compact(normalizeDeleted(normalized))===compact(normalized)},
  perFixture, hostile,
  forgedArrayRejected:!arrayForgedRun.accepted,
  totals:{positiveNativeCliRuns:3+2*perFixture.length, hostileObjectRejected:hostile.length,
    hostileCanonicalRejectedOrRefused:hostile.length, perFixtureSavedBytes:perFixture.reduce((s,x)=>s+x.savedBytes,0)},
  conclusion:'PROVED/RESTRICTED normalization lemma plus COMPUTATIONAL OS-CLI validation; P2-D1/C3/B1 OPEN; P2-B2/B3 separate; P versus NP OPEN.'
};

fs.rmSync(tmp,{recursive:true,force:true});
const outPath = process.argv[2];
if (outPath) fs.writeFileSync(outPath, JSON.stringify(result,null,2)+'\n');
process.stdout.write(JSON.stringify(result,null,2)+'\n');
