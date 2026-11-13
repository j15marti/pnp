'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const cp = require('child_process');

const root = path.resolve(__dirname, '../..');
const checker = path.join(root, 'experiments/arc/lspv2_341_independent_verify.js');
const fixture = path.join(root, 'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json');
const outPath = path.join(root, 'results/raw/arc/2026-11-13_0752_LSPV5_525_NATIVE341_DUPLICATE_MEMBER_RAW.json');
const acceptedPath = path.join(root, 'results/raw/arc/2026-11-13_0752_LSPV5_525_NATIVE341_DUPLICATE_MEMBER_ACCEPTED.json');

const sha256 = b => crypto.createHash('sha256').update(b).digest('hex');
const gitBlob = b => crypto.createHash('sha1').update(`blob ${b.length}\0`).update(b).digest('hex');
function replaceOnce(s, a, b) {
  if (!s.includes(a)) throw new Error(`missing mutation target: ${a}`);
  return s.replace(a, b);
}

// Lex the raw JSON before JSON.parse can erase duplicate decoded names.
function scanUniqueJSON(text) {
  let i = 0; const duplicates = [];
  const ws = () => { while (i < text.length && /[\x20\x09\x0a\x0d]/.test(text[i])) i++; };
  function stringToken() {
    ws(); const start = i;
    if (text[i++] !== '"') throw new SyntaxError(`string at ${start}`);
    let escaped = false;
    while (i < text.length) {
      const c = text[i++];
      if (escaped) { escaped = false; continue; }
      if (c === '\\') { escaped = true; continue; }
      if (c === '"') { const raw = text.slice(start, i); return {value: JSON.parse(raw), start}; }
      if (c < ' ') throw new SyntaxError(`control at ${i - 1}`);
    }
    throw new SyntaxError(`unterminated string at ${start}`);
  }
  function value(p) {
    ws(); const c = text[i];
    if (c === '{') return object(p);
    if (c === '[') return array(p);
    if (c === '"') { stringToken(); return; }
    const m = /^(?:-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?|true|false|null)/.exec(text.slice(i));
    if (!m) throw new SyntaxError(`value at ${i}`);
    i += m[0].length;
  }
  function object(p) {
    i++; ws(); const seen = new Map();
    if (text[i] === '}') { i++; return; }
    while (true) {
      const k = stringToken(); ws();
      if (text[i++] !== ':') throw new SyntaxError(`colon at ${i - 1}`);
      if (seen.has(k.value)) duplicates.push({path: p, key: k.value, first_offset: seen.get(k.value), duplicate_offset: k.start});
      else seen.set(k.value, k.start);
      value(`${p}.${k.value}`); ws();
      if (text[i] === '}') { i++; return; }
      if (text[i++] !== ',') throw new SyntaxError(`comma at ${i - 1}`);
      ws();
    }
  }
  function array(p) {
    i++; ws(); let n = 0;
    if (text[i] === ']') { i++; return; }
    while (true) {
      value(`${p}[${n++}]`); ws();
      if (text[i] === ']') { i++; return; }
      if (text[i++] !== ',') throw new SyntaxError(`comma at ${i - 1}`);
      ws();
    }
  }
  value('$'); ws();
  if (i !== text.length) throw new SyntaxError(`trailing bytes at ${i}`);
  return duplicates;
}

function runChecker(raw, label) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'lspv5-525-'));
  const file = path.join(dir, `${label}.json`);
  fs.writeFileSync(file, raw);
  const p = cp.spawnSync(process.execPath, [checker, file], {encoding: 'utf8'});
  fs.rmSync(dir, {recursive: true, force: true});
  let parsed = null;
  if (p.status === 0) { parsed = JSON.parse(p.stdout.trim()); delete parsed.file; }
  const stderrLines = p.stderr.trim().split('\n');
  return {accepted: p.status === 0, status: p.status, parsed, error: stderrLines.find(x => x.includes('Error:')) || stderrLines[0] || ''};
}

const checkerBytes = fs.readFileSync(checker);
const fixtureBytes = fs.readFileSync(fixture);
const canonical = JSON.stringify(JSON.parse(fixtureBytes));
if (scanUniqueJSON(canonical).length !== 0) throw new Error('canonical baseline has duplicates');

const variants = [
  ['source_id', '"id":"s0"', '"id":"ghost-source","id":"s0"', '"id":"s0","id":"ghost-source"'],
  ['escaped_source_id', '"id":"s0"', '"\\u0069d":"ghost-source","id":"s0"', '"id":"s0","\\u0069d":"ghost-source"'],
  ['clause_literals', '"literals":[1,2,3]', '"literals":[999],"literals":[1,2,3]', '"literals":[1,2,3],"literals":[999]'],
  ['proof_kind', '"kind":"factor"', '"kind":"RES","kind":"factor"', '"kind":"factor","kind":"RES"'],
  ['proof_rule', '"rule":"AND3"', '"rule":"LOCAL-CONVERT","rule":"AND3"', '"rule":"AND3","rule":"LOCAL-CONVERT"'],
  ['proof_parents', '"parents":["s0","s1"]', '"parents":["ghost"],"parents":["s0","s1"]', '"parents":["s0","s1"],"parents":["ghost"]'],
  ['proof_table', '"table":246', '"table":0,"table":246', '"table":246,"table":0'],
  ['deletion_sourceId', '"sourceId":"s0"', '"sourceId":"ghost","sourceId":"s0"', '"sourceId":"s0","sourceId":"ghost"']
];

const baseline = runChecker(canonical, 'baseline');
if (!baseline.accepted) throw new Error('baseline rejected');
const ledger = [];
for (const [name, target, acceptedReplacement, reversedReplacement] of variants) {
  const shadow = replaceOnce(canonical, target, acceptedReplacement);
  const reversed = replaceOnce(canonical, target, reversedReplacement);
  const shadowDup = scanUniqueJSON(shadow), reversedDup = scanUniqueJSON(reversed);
  if (shadowDup.length !== 1 || reversedDup.length !== 1) throw new Error(`${name}: duplicate scan mismatch`);
  const accepted = runChecker(shadow, `${name}-accepted`);
  const rejected = runChecker(reversed, `${name}-reversed`);
  if (!accepted.accepted || JSON.stringify(accepted.parsed) !== JSON.stringify(baseline.parsed)) throw new Error(`${name}: accepted replay mismatch`);
  if (rejected.accepted) throw new Error(`${name}: reversed hostile unexpectedly accepted`);
  ledger.push({name, accepted_sha256: sha256(Buffer.from(shadow)), accepted_duplicate: shadowDup[0], accepted_checker: accepted, reversed_sha256: sha256(Buffer.from(reversed)), reversed_duplicate: reversedDup[0], reversed_checker: rejected});
}

let composite = canonical;
for (const [, target, acceptedReplacement] of variants) composite = replaceOnce(composite, target, acceptedReplacement);
const compositeDuplicates = scanUniqueJSON(composite);
const compositeRun = runChecker(composite, 'composite');
if (compositeDuplicates.length !== variants.length || !compositeRun.accepted || JSON.stringify(compositeRun.parsed) !== JSON.stringify(baseline.parsed)) throw new Error('composite replay mismatch');

const lexical = {
  escaped_equivalent: scanUniqueJSON('{"id":1,"\\u0069d":2}'),
  sibling_reuse: scanUniqueJSON('{"a":{"id":1},"b":{"id":2}}')
};
if (lexical.escaped_equivalent.length !== 1 || lexical.sibling_reuse.length !== 0) throw new Error('lexical controls failed');

const result = {
  run: 'LSPV-5/525', timestamp_pst: '2026-11-13 07:52 PST', node: process.version,
  inputs: {
    checker: path.relative(root, checker), checker_sha256: sha256(fs.readFileSync(checker)),
    fixture: path.relative(root, fixture), fixture_sha256: sha256(fs.readFileSync(fixture)),
    canonicalized_baseline_sha256: sha256(Buffer.from(canonical))
  },
  status: 'COMPUTATIONAL independent OS-Node accepted-byte counterexample + PROVED/EXACT duplicate-decoded-member lemma',
  authority: {checker: path.relative(root, checker), checker_git_blob: gitBlob(checkerBytes), checker_sha256: sha256(checkerBytes), fixture: path.relative(root, fixture), fixture_git_blob: gitBlob(fixtureBytes), fixture_sha256: sha256(fixtureBytes)},
  baseline: {bytes: Buffer.byteLength(canonical), sha256: sha256(Buffer.from(canonical)), checker: baseline},
  cases: ledger,
  composite: {bytes: Buffer.byteLength(composite), sha256: sha256(Buffer.from(composite)), duplicates: compositeDuplicates, checker: compositeRun, saved_as: path.relative(root, acceptedPath)},
  lexical_controls: lexical,
  theorem: 'The historical /341 checker validates JSON.parse(text), not raw text. Therefore every raw JSON byte string that JSON.parse maps to an accepted parsed object is accepted; duplicate decoded member names are last-member-wins aliases and their earlier values are unauthenticated.',
  classification: {failure: 'P2-D1 byte/provenance authentication failure', not_shown: ['logical proof unsoundness', 'lower-bound counterexample', 'P2-C3', 'P2-B1', 'P2-B2/B3 transfer']},
  cegar: 'All eight cheap hostile paths and their composite were concretely replayed. They are genuine historical-checker paths and may not be removed by refinement. A unique-decoded-member guard would define a new versioned front end, not the historical accepted-byte language.',
  cost: 'Ignored earlier members do not change parsed logical work or accepted result. Raw parsing and uniqueness checking have physical cost but no historical logical weight in this checker.'
};
fs.mkdirSync(path.dirname(outPath), {recursive: true});
fs.writeFileSync(acceptedPath, composite);
fs.writeFileSync(outPath, JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify({run: result.run, accepted_cases: ledger.length, composite_duplicates: compositeDuplicates.length, baseline_checks: baseline.parsed.checks, baseline_cases: baseline.parsed.cases.length, raw: path.relative(root, outPath), accepted: path.relative(root, acceptedPath)}, null, 2));

