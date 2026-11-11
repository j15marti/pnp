'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const cp = require('child_process');

const root = path.resolve(__dirname, '../..');
const checker = path.join(root, 'experiments/arc/lspv2_386_independent_verify.js');
const packet = path.join(root, 'results/raw/arc/2026-11-10_2212_LSPV2_549_DUAL_NATIVE_POLYGLOT_PACKET.json');
const outPath = path.join(root, 'results/raw/arc/2026-11-11_0421_LSPV5_485_RES_PARENT_BINARY64_ROUNDING_CELL_RAW.json');

function sha256(buf) { return crypto.createHash('sha256').update(buf).digest('hex'); }
function gitBlob(buf) { return crypto.createHash('sha1').update(`blob ${buf.length}\0`).update(buf).digest('hex'); }
function run(bytes, label) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'lspv5-485-'));
  const file = path.join(dir, `${label}.json`);
  fs.writeFileSync(file, bytes);
  const p = cp.spawnSync(process.execPath, [checker, file], {encoding: 'utf8'});
  fs.rmSync(dir, {recursive: true, force: true});
  let parsed = null;
  if (p.status === 0) { parsed = JSON.parse(p.stdout.trim()); delete parsed.file; }
  return {accepted:p.status === 0, status:p.status, parsed, stderr:p.stderr.trim().split('\n').slice(-2).join('\n')};
}

const base = fs.readFileSync(packet);
const source = base.toString('utf8');
const needle = '"parents":[16,0]';
if ((source.split(needle).length - 1) !== 1) throw new Error('expected one target parent');
const baseline = run(base, 'baseline');
if (!baseline.accepted) throw new Error('baseline rejected');

// Adjacent spacings at exactly 16 are asymmetric: upward 2^-48 and downward
// 2^-49.  Hence the round-to-nearest-even cell of 16 is bounded by
// 16-2^-50 and 16+2^-49.  Both exact midpoint ties round to 16 because the
// binary64 significand of 16 is even and both adjacent significands are odd.
const lowerTie = '15.99999999999999911182158029987476766109466552734375';
const upperTie = '16.0000000000000017763568394002504646778106689453125';
const acceptedTokens = [
  '16.000000000000001',
  '16.0000000000000001',
  '1.6000000000000001e1',
  '15.9999999999999999',
  lowerTie,
  upperTie
];
const accepts = [];
for (const token of acceptedTokens) {
  const text = source.replace(needle, `"parents":[${token},0]`);
  const value = JSON.parse(text).records[22].parents[0];
  if (!Object.is(value, 16) || !Number.isInteger(value)) throw new Error(`did not round to 16: ${token}`);
  const outcome = run(Buffer.from(text), `accept-${accepts.length}`);
  if (!outcome.accepted) throw new Error(`checker rejected ${token}`);
  const same = ['paid','def','res','records','sources','sourceBits','oddModels','evenModels','guardFalseModels']
    .every(key => outcome.parsed[key] === baseline.parsed[key]);
  if (!same) throw new Error(`outcome changed for ${token}`);
  accepts.push({token, exact_noninteger:true, parsed:value, accepted:true, same_outcome:same, bytes:Buffer.byteLength(text), sha256:sha256(Buffer.from(text))});
}

const rejectedTokens = [
  '16.000000000000004',
  '15.999999999999998',
  '16.0000000000000017763568394002504646778106689453126',
  '15.99999999999999911182158029987476766109466552734374'
];
const rejects = [];
for (const token of rejectedTokens) {
  const text = source.replace(needle, `"parents":[${token},0]`);
  const value = JSON.parse(text).records[22].parents[0];
  const outcome = run(Buffer.from(text), `reject-${rejects.length}`);
  rejects.push({token, parsed:value, integer:Number.isInteger(value), accepted:outcome.accepted});
  if (outcome.accepted) throw new Error(`outside-cell control accepted: ${token}`);
}

const result = {
  run:'LSPV-5/485', timestamp_pst:'2026-11-11 04:21 PST',
  status:'COMPUTATIONAL accepted-byte counterexample plus PROVED/RESTRICTED binary64-cell lemma',
  inputs:{checker:path.relative(root,checker), checker_git_blob:gitBlob(fs.readFileSync(checker)), packet:path.relative(root,packet), packet_git_blob:gitBlob(base), packet_sha256:sha256(base)},
  mutation:{record_index:22,parent_position:0,baseline_raw:'16',accepted_exact_cell:'[16-2^-50, 16+2^-49] under round-to-nearest-ties-to-even'},
  exact_midpoints:{lower:lowerTie, upper:upperTie},
  accepted_exact_nonintegers:accepts,
  rejected_outside_controls:rejects,
  baseline_outcome:baseline.parsed,
  interpretation:{
    concrete:'The pinned /386 verifier accepts exact noninteger JSON decimals, including both exact binary64 midpoint ties around 16, as integer Resolution parent 16.',
    abstraction:'Parsed Number equality is not exact-decimal identity; a cost-sound accepted-byte abstraction must retain or validate exact numeric lexemes before rounding.',
    cegar:'Every listed cheap path was replayed through the unchanged checker and is genuine, not abstractly spurious.',
    repair:'Lex exact JSON numbers, decide mathematical integrality before binary64 conversion, impose a canonical unsigned decimal integer syntax and range, then resolve the parent.',
    limitation:'Restricted to one archived /386 Resolution-parent field; ancestry and cost are unchanged. This proves no full R_mix341 grammar, semantic unsoundness, lower bound, or B1/B2/B3 bridge.'
  }
};
fs.mkdirSync(path.dirname(outPath),{recursive:true});
fs.writeFileSync(outPath,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
