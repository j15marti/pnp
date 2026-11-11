#!/usr/bin/env node
'use strict';

// LSPV-5/487: compose LSPV-1/569 duplicate-facet normalization with
// LSPV-5/485 binary64 parent aliases on an actual live /386 DEF->RES edge.
// This is a finite archived-/386 audit, not a full R_mix341 theorem.

const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const {spawnSync} = require('child_process');

const root = path.resolve(__dirname, '../..');
const checker = path.join(root, 'experiments/arc/lspv2_386_independent_verify.js');
const seedPath = path.join(root, 'results/raw/arc/2026-11-10_2124_LSPV3_561_ARCHIVED_386_NATIVE_PACKET.json');
const clone = x => structuredClone(x);
const check = (b, m) => { if (!b) throw new Error(m); };
const sha256 = b => crypto.createHash('sha256').update(b).digest('hex');
const gitBlob = b => crypto.createHash('sha1').update(Buffer.concat([
  Buffer.from(`blob ${b.length}\0`), b
])).digest('hex');
const encode = p => Buffer.from(JSON.stringify(p) + '\n', 'utf8');

const checkerBytes = fs.readFileSync(checker);
const seedBytes = fs.readFileSync(seedPath);
const seed = JSON.parse(seedBytes);
check(gitBlob(checkerBytes) === '338305c0ce101704205e57543756b8127074a986', 'checker drift');
check(seed.records.length === 69 && seed.summary.paid_total === 50, 'seed counters');
check(JSON.stringify(seed.records[17]) === JSON.stringify({kind:'DEF',c:[1,-8],parents:[],gate:0}), 'facet 17');
check(JSON.stringify(seed.records[20].parents) === '[17,1]' && seed.records[20].pivot === 1, 'live consumer 20');

function withLiveDuplicate(p) {
  const q = clone(p);
  const old = q.records;
  const records = old.slice(0, 20).map(clone);
  records.push(clone(old[17])); // new record 20, identical to owner/facet record 17
  for (let i = 20; i < old.length; i++) {
    const r = clone(old[i]);
    r.parents = r.parents.map(j => j >= 20 ? j + 1 : j);
    if (i === 20) r.parents[0] = 20; // make the repeated facet terminal-cone live
    records.push(r);
  }
  q.records = records;
  q.summary.def_views += 1;
  q.summary.live_records += 1;
  return q;
}

function normalizeDuplicate(p, duplicate = 20, retained = 17) {
  const q = clone(p);
  q.records = q.records.filter((_, i) => i !== duplicate).map(r => ({
    ...r,
    parents: r.parents.map(j => j === duplicate ? retained : j > duplicate ? j - 1 : j)
  }));
  q.summary.def_views -= 1;
  q.summary.live_records -= 1;
  return q;
}

const repeated = withLiveDuplicate(seed);
const repeatedCanonical = encode(repeated);
const needle = '"parents":[20,1]';
check(repeatedCanonical.toString('utf8').split(needle).length === 2, 'unique live parent occurrence');
const aliasText = repeatedCanonical.toString('utf8').replace(needle, '"parents":[20.000000000000001,1]');
const outsideText = repeatedCanonical.toString('utf8').replace(needle, '"parents":[20.000000000000004,1]');
const aliasBytes = Buffer.from(aliasText, 'utf8');
const outsideBytes = Buffer.from(outsideText, 'utf8');
const aliasParsed = JSON.parse(aliasBytes);
check(aliasParsed.records[21].parents[0] === 20, 'rounding-cell alias did not decode to 20');
check(!Number.isInteger(JSON.parse(outsideBytes).records[21].parents[0]), 'outside alias unexpectedly integer');

const normalized = normalizeDuplicate(aliasParsed);
check(JSON.stringify(normalized) === JSON.stringify(seed), 'normal form failed exact semantic recovery');
check(JSON.stringify(normalizeDuplicate(repeated)) === JSON.stringify(seed), 'exact duplicate recovery');

const dangling = clone(repeated);
dangling.records.splice(20, 1); // intentionally no parent redirection or reindexing
dangling.summary.def_views -= 1;
dangling.summary.live_records -= 1;

const wrongFacet = clone(normalized);
wrongFacet.records[20].parents[0] = 18;

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lspv5-487-'));
const cases = [
  ['baseline', encode(seed), true],
  ['live_duplicate_exact', repeatedCanonical, true],
  ['live_duplicate_decimal_alias', aliasBytes, true],
  ['normalized_alias', encode(normalized), true],
  ['delete_without_redirect', encode(dangling), false],
  ['redirect_to_wrong_facet', encode(wrongFacet), false],
  ['parent_alias_outside_cell', outsideBytes, false]
];
const rows = [];
try {
  for (const [name, bytes, want] of cases) {
    const f = path.join(tmp, name + '.json');
    fs.writeFileSync(f, bytes);
    const before = process.resourceUsage();
    const t0 = process.hrtime.bigint();
    const wrapper = "const [checker,file]=process.argv.slice(1);process.argv=[process.execPath,checker,file];process.on('exit',()=>console.error('__RU__'+JSON.stringify(process.resourceUsage())));require(checker);";
    const proc = spawnSync(process.execPath, ['-e', wrapper, checker, f], {
      encoding: 'utf8', timeout: 30000, maxBuffer: 1024 * 1024
    });
    const elapsedNs = Number(process.hrtime.bigint() - t0);
    const after = process.resourceUsage();
    const accepted = proc.status === 0 && !proc.error;
    check(accepted === want, `${name}: wanted ${want}, status ${proc.status}, ${proc.stderr}`);
    let native = null;
    if (accepted) native = JSON.parse(proc.stdout.trim().split('\n').at(-1));
    rows.push({
      name, want, accepted, bytes: bytes.length, sha256: sha256(bytes), git_blob: gitBlob(bytes),
      decoded_live_parent: (() => { try { return JSON.parse(bytes).records[21]?.parents?.[0] ?? null; } catch { return null; } })(),
      elapsed_ns: elapsedNs,
      parent_user_cpu_us: after.userCPUTime - before.userCPUTime,
      parent_system_cpu_us: after.systemCPUTime - before.systemCPUTime,
      parent_max_rss_kib: after.maxRSS,
      child_max_rss_kib: Number((proc.stderr.match(/__RU__\{[^\n]*"maxRSS":(\d+)/) || [null, 0])[1]),
      native,
      first_stderr_line: accepted ? null : (proc.stderr || String(proc.error)).split('\n').find(s => s && !s.startsWith('__RU__')) || null
    });
  }
} finally {
  for (const f of fs.readdirSync(tmp)) fs.unlinkSync(path.join(tmp, f));
  fs.rmdirSync(tmp);
}

const report = {
  run: 'LSPV5_487',
  status: 'COMPUTATIONAL finite validation; archived /386 only; P versus NP OPEN',
  node: process.version,
  platform: `${process.platform}/${process.arch}`,
  checker_path: path.relative(root, checker),
  checker_git_blob: gitBlob(checkerBytes),
  seed_path: path.relative(root, seedPath),
  seed_git_blob: gitBlob(seedBytes),
  exact_recovery: JSON.stringify(normalized) === JSON.stringify(seed),
  repeated_records: repeated.records.length,
  normalized_records: normalized.records.length,
  paid_work_before: repeated.summary.paid_total,
  paid_work_after: normalized.summary.paid_total,
  rounding_control: {
    raw_token: '20.000000000000001',
    decoded_number: Number('20.000000000000001'),
    outside_token: '20.000000000000004',
    outside_decoded_number: Number('20.000000000000004')
  },
  cases: rows,
  controls: {
    positive_accepts: rows.filter(r => r.accepted).length,
    deliberate_rejects: rows.filter(r => !r.accepted).length,
    original_cli_negative_tests_across_positives: rows.filter(r => r.accepted).reduce((n,r) => n + r.native.negativeTests, 0),
    original_assertion_groups_across_positives: rows.filter(r => r.accepted).reduce((n,r) => n + r.native.assertions, 0)
  },
  limitation: 'Validates one live repeated facet plus one binary64 lexical alias. It does not prove the universal /569 normalizer, authenticate full R_mix341, or imply P2-C3/P2-B1.'
};
const out = path.join(root, 'results/raw/arc/2026-11-11_0558_LSPV5_487_LIVE_DUPLICATE_NORMAL_FORM_RAW.json');
fs.writeFileSync(out, JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify(report, null, 2));
