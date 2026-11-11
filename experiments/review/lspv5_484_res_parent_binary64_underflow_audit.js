'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const cp = require('child_process');

const root = path.resolve(__dirname, '../..');
const checker = path.join(root, 'experiments/arc/lspv2_386_independent_verify.js');
const packet = path.join(root, 'results/raw/arc/2026-11-10_2212_LSPV2_549_DUAL_NATIVE_POLYGLOT_PACKET.json');
const outPath = path.join(root, 'results/raw/arc/2026-11-11_0251_LSPV5_484_RES_PARENT_BINARY64_UNDERFLOW_RAW.json');

function sha256(buf) { return crypto.createHash('sha256').update(buf).digest('hex'); }
function gitBlob(buf) { return crypto.createHash('sha1').update(`blob ${buf.length}\0`).update(buf).digest('hex'); }
function run(bytes, label) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'lspv5-484-'));
  const file = path.join(dir, `${label}.json`);
  fs.writeFileSync(file, bytes);
  const p = cp.spawnSync(process.execPath, [checker, file], {encoding: 'utf8'});
  fs.rmSync(dir, {recursive: true, force: true});
  let parsed = null;
  if (p.status === 0) {
    parsed = JSON.parse(p.stdout.trim());
    delete parsed.file;
  }
  return {accepted: p.status === 0, status: p.status, parsed, stderr: p.stderr.trim().split('\n').slice(-2).join('\n')};
}

const base = fs.readFileSync(packet);
const source = base.toString('utf8');
const needle = '"parents":[16,0]';
const escaped = needle.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
if ((source.match(new RegExp(escaped, 'g')) || []).length !== 1) throw new Error('expected one target parent');

// Exact rational inequality: 10^-324 < 2^-1075, half the least positive
// binary64 subnormal. Round-to-nearest-ties-to-even therefore maps 10^-k
// to +0 for every integer k >= 324, and -10^-k to -0.
if (!(10n ** 324n > 2n ** 1075n)) throw new Error('underflow inequality failed');

const baseline = run(base, 'baseline');
if (!baseline.accepted) throw new Error('baseline rejected');

const exponents = [324, 325, 400, 1000, 1000000];
const positive = [];
const negative = [];
for (const k of exponents) {
  for (const sign of ['', '-']) {
    const token = `${sign}1e-${k}`;
    const text = source.replace(needle, `"parents":[16,${token}]`);
    const parsed = JSON.parse(text);
    const value = parsed.records[22].parents[1];
    const expectedNegativeZero = sign === '-';
    if (expectedNegativeZero ? !Object.is(value, -0) : !Object.is(value, 0)) throw new Error(`wrong parse for ${token}`);
    if (!Number.isInteger(value)) throw new Error(`underflow result not integer for ${token}`);
    if (parsed.records[value] !== parsed.records[0]) throw new Error(`array alias failed for ${token}`);
    const outcome = run(Buffer.from(text), `underflow-${sign ? 'neg' : 'pos'}-${k}`);
    if (!outcome.accepted) throw new Error(`checker rejected ${token}`);
    const same = ['paid','def','res','records','sources','sourceBits','oddModels','evenModels','guardFalseModels']
      .every(key => outcome.parsed[key] === baseline.parsed[key]);
    if (!same) throw new Error(`outcome changed for ${token}`);
    const row = {token, exponent:k, bytes:Buffer.byteLength(text), sha256:sha256(Buffer.from(text)), parsed_negative_zero:Object.is(value,-0), accepted:true, same_outcome:same};
    (sign ? negative : positive).push(row);
  }
}

const controls = [];
for (const token of ['5e-324', '1e-323', '1e400', '"1e-324"']) {
  const text = source.replace(needle, `"parents":[16,${token}]`);
  let value = null;
  try { value = JSON.parse(text).records[22].parents[1]; } catch (e) { value = `parse-error:${e.message}`; }
  const outcome = run(Buffer.from(text), `control-${controls.length}`);
  controls.push({token, parsed:String(value), integer:typeof value === 'number' && Number.isInteger(value), finite:typeof value === 'number' && Number.isFinite(value), accepted:outcome.accepted});
  if (outcome.accepted) throw new Error(`control accepted: ${token}`);
}

const canonicalHostile = JSON.parse(source.replace(needle, '"parents":[16,1e-324]'));
const canonical = Buffer.from(JSON.stringify(canonicalHostile));
const canonicalRun = run(canonical, 'canonical');
if (!canonicalRun.accepted || canonical.toString('utf8').includes('1e-324')) throw new Error('canonical repair failed');

const result = {
  run: 'LSPV-5/484',
  timestamp_pst: '2026-11-11 02:51 PST',
  status: 'COMPUTATIONAL parameterized accepted-byte counterexample plus PROVED/RESTRICTED underflow lemma',
  inputs: {
    checker: path.relative(root, checker), checker_git_blob: gitBlob(fs.readFileSync(checker)),
    packet: path.relative(root, packet), packet_git_blob: gitBlob(base), packet_sha256: sha256(base)
  },
  exact_inequality: {claim:'10^324 > 2^1075, hence 10^-324 < 2^-1075', checked_bigint:true},
  mutation: {record_index:22, parent_position:1, baseline_raw:'0', family:'±1e-k for every integer k >= 324'},
  positive_underflow_accepts: positive,
  negative_underflow_accepts: negative,
  rejected_controls: controls,
  baseline_outcome: baseline.parsed,
  canonical: {accepted:canonicalRun.accepted, bytes:canonical.length, sha256:sha256(canonical)},
  interpretation: {
    concrete:'The pinned /386 verifier accepts mathematically nonzero decimal JSON parent tokens ±10^-k as positional parent 0 for every tested k>=324 because binary64 conversion underflows.',
    symbolic:'ECMAScript round-to-nearest-even maps every ±10^-k, k>=324, to signed zero because 10^-324 is below half the least positive binary64 subnormal.',
    abstraction:'A byte-authenticated or mathematical-decimal-authenticated abstraction cannot treat parsed Number equality as raw or exact-decimal identity.',
    repair:'Parse parent tokens with an exact JSON-decimal grammar, require exact mathematical integrality and range before conversion, then serialize unique unsigned decimal; or reject any noncanonical raw spelling.',
    limitation:'This is restricted to one archived /386 parent field and proves no full R_mix341 grammar, proof-size lower bound, machine lower bound or B1/B2/B3 bridge.'
  }
};
fs.mkdirSync(path.dirname(outPath), {recursive:true});
fs.writeFileSync(outPath, JSON.stringify(result, null, 2)+'\n');
console.log(JSON.stringify(result, null, 2));
