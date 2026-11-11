'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const cp = require('child_process');

const root = path.resolve(__dirname, '../..');
const checker = path.join(root, 'experiments/arc/lspv2_386_independent_verify.js');
const packet = path.join(root, 'results/raw/arc/2026-11-10_2212_LSPV2_549_DUAL_NATIVE_POLYGLOT_PACKET.json');
const outPath = path.join(root, 'results/raw/arc/2026-11-11_0152_LSPV5_483_RES_PARENT_NEGATIVE_ZERO_RAW.json');

function sha256(buf) { return crypto.createHash('sha256').update(buf).digest('hex'); }
function gitBlob(buf) { return crypto.createHash('sha1').update(`blob ${buf.length}\0`).update(buf).digest('hex'); }
function run(bytes, label) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'lspv5-483-'));
  const file = path.join(dir, `${label}.json`);
  fs.writeFileSync(file, bytes);
  const p = cp.spawnSync(process.execPath, [checker, file], {encoding: 'utf8'});
  fs.rmSync(dir, {recursive: true, force: true});
  let parsed = null;
  if (p.status === 0) {
    parsed = JSON.parse(p.stdout.trim());
    delete parsed.file;
  }
  return {accepted: p.status === 0, status: p.status, stdout: p.stdout.trim(), stderr: p.stderr.trim(), parsed};
}

const base = fs.readFileSync(packet);
const source = base.toString('utf8');
const needle = '"parents":[16,0]';
if ((source.match(new RegExp(needle.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g')) || []).length !== 1) {
  throw new Error('expected exactly one target parent token');
}
const hostileText = source.replace(needle, '"parents":[16,-0]');
const quotedText = source.replace(needle, '"parents":[16,"0"]');
const negativeText = source.replace(needle, '"parents":[16,-1]');

const hostileParsed = JSON.parse(hostileText);
const target = hostileParsed.records[22].parents[1];
if (!Object.is(target, -0)) throw new Error('JSON.parse did not preserve negative zero');
if (hostileParsed.records[target] !== hostileParsed.records[0]) throw new Error('array lookup did not alias -0 to 0');

const baseline = run(base, 'baseline');
const hostile = run(Buffer.from(hostileText), 'hostile-negative-zero');
const quoted = run(Buffer.from(quotedText), 'quoted-zero');
const negative = run(Buffer.from(negativeText), 'negative-one');
if (!baseline.accepted || !hostile.accepted || quoted.accepted || negative.accepted) {
  throw new Error('unexpected acceptance matrix');
}

const canonical = Buffer.from(JSON.stringify(hostileParsed));
const canonicalRun = run(canonical, 'canonicalized');
if (!canonicalRun.accepted || canonical.toString('utf8').includes('-0')) throw new Error('canonical repair failed');

const sameOutcome = ['paid','def','res','records','sources','sourceBits','oddModels','evenModels','guardFalseModels']
  .every(k => baseline.parsed[k] === hostile.parsed[k]);
if (!sameOutcome) throw new Error('hostile outcome changed');

const result = {
  run: 'LSPV-5/483',
  timestamp_pst: '2026-11-11 01:52 PST',
  status: 'COMPUTATIONAL counterexample plus local repair lemma',
  inputs: {
    checker: path.relative(root, checker),
    checker_git_blob: gitBlob(fs.readFileSync(checker)),
    packet: path.relative(root, packet),
    packet_git_blob: gitBlob(base),
    packet_sha256: sha256(base)
  },
  mutation: {
    record_index: 22,
    parent_position: 1,
    baseline_raw: '0',
    hostile_raw: '-0',
    hostile_is_negative_zero: Object.is(target, -0),
    array_lookup_aliases_record_zero: hostileParsed.records[target] === hostileParsed.records[0]
  },
  acceptance: {
    baseline: baseline.accepted,
    hostile_negative_zero: hostile.accepted,
    quoted_zero_control: quoted.accepted,
    negative_one_control: negative.accepted,
    canonicalized_hostile: canonicalRun.accepted
  },
  outcomes_identical: sameOutcome,
  baseline_outcome: baseline.parsed,
  hostile_outcome: hostile.parsed,
  hostile: {bytes: Buffer.byteLength(hostileText), sha256: sha256(Buffer.from(hostileText))},
  canonical: {bytes: canonical.length, sha256: sha256(canonical), contains_negative_zero: canonical.toString('utf8').includes('-0')},
  interpretation: {
    concrete: 'The pinned /386 verifier accepts the distinct raw JSON parent tokens 0 and -0 as the same Resolution parent index.',
    abstraction: 'A byte-authenticated abstraction cannot identify raw parent tokens merely because JSON.parse and array indexing identify them.',
    repair: 'For this finite positional-parent fragment, parse, validate, and reserialize every parent as the unique decimal form of an integer in [0,i); reject noncanonical raw spellings if raw-byte provenance is required.',
    limitation: 'This does not authenticate the complete historical R_mix341 grammar and proves no proof-size or machine lower bound.'
  }
};
fs.mkdirSync(path.dirname(outPath), {recursive: true});
fs.writeFileSync(outPath, JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify(result, null, 2));
