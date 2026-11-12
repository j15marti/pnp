'use strict';
// LSPV-5/500: exact archived /341 CLI replay plus composition of two
// previously published parser aliases. No historical all-rule claim.
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const cp = require('node:child_process');
const assert = require('node:assert/strict');

const checkerPath = 'experiments/arc/lspv2_341_independent_verify.js';
const basePath = 'results/raw/arc/2026-11-11_1824_LSPV3_582_STRING_CHARGE_SAT_ACCEPTED_PACKET.json';
const rotatedPath = 'results/raw/arc/2026-11-11_1924_LSPV3_583_ROTATED_SUPPORT_SAT_ACCEPTED_PACKET.json';
const rawPath = 'results/raw/review/2026-11-11_1948_LSPV5_500_NATIVE341_CLI_SOUNDNESS_RAW.json';
const witnessPath = 'results/raw/review/2026-11-11_1948_LSPV5_500_HYBRID_ALIAS_SAT_ACCEPTED.json';

const expected = {
  checkerBlob: 'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
  baseBlob: '6cf9b0fe1e5a9419e8967d836c707c385418b810',
  rotatedBlob: '5d78d8f6eb5934bf805ee90736b1f88d4acd2729'
};
function gitBlob(buf) {
  return crypto.createHash('sha1').update('blob ' + buf.length + '\0').update(buf).digest('hex');
}
function sha256(buf) { return crypto.createHash('sha256').update(buf).digest('hex'); }
const checkerBytes = fs.readFileSync(checkerPath);
const baseBytes = fs.readFileSync(basePath);
const rotatedBytes = fs.readFileSync(rotatedPath);
assert.equal(gitBlob(checkerBytes), expected.checkerBlob);
assert.equal(gitBlob(baseBytes), expected.baseBlob);
assert.equal(gitBlob(rotatedBytes), expected.rotatedBlob);

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lspv5-500-'));
let serial = 0;
function runRaw(name, bytes) {
  const p = path.join(tmp, String(serial++).padStart(2, '0') + '-' + name + '.json');
  fs.writeFileSync(p, bytes);
  const r = cp.spawnSync(process.execPath, [checkerPath, p], {encoding:'utf8', timeout:10000});
  return {
    name,
    accepted:r.status===0,
    status:r.status,
    signal:r.signal,
    stdout:r.stdout.trim(),
    stderr:r.stderr.trim(),
    bytes:bytes.length,
    sha256:sha256(bytes)
  };
}
function compact(obj) { return Buffer.from(JSON.stringify(obj) + '\n'); }
function deep(obj) { return JSON.parse(JSON.stringify(obj)); }
function expectAccepted(result) {
  assert.equal(result.accepted, true, result.name + ': ' + result.stderr);
  const parsed = JSON.parse(result.stdout);
  assert.equal(parsed.checks, 3273);
  assert.equal(parsed.cases[0].proofNodes, 47);
  return parsed;
}
function expectRejected(result) { assert.equal(result.accepted, false, result.name); }

const base = JSON.parse(baseBytes);
const rotated = JSON.parse(rotatedBytes);
const positive = [];
positive.push(runRaw('published-base-string-charge-support-012', baseBytes));
positive.push(runRaw('published-rotated-support-120', rotatedBytes));

const hybrid = deep(rotated);
hybrid.fixtures[0].charges[0] = '000000001';
const hybridBytes = compact(hybrid);
fs.mkdirSync(path.dirname(witnessPath),{recursive:true});
fs.writeFileSync(witnessPath, hybridBytes);
positive.push(runRaw('new-hybrid-support-120-padded-charge', hybridBytes));
for (const r of positive) expectAccepted(r);

const f = hybrid.fixtures[0];
const bits = '101001000000100000';
function clauseSat(clause) {
  return clause.literals.some(lit => {
    const bit = Number(bits[Math.abs(lit)-1]);
    return lit > 0 ? bit===1 : bit===0;
  });
}
const sourceSatisfied = f.clauses.filter(clauseSat).length;
assert.equal(sourceSatisfied, 48);
const badNode = f.proof.find(x=>x.id===50);
assert.equal(badNode.support, '120');
assert.equal(badNode.table, 90);
assert.deepEqual(badNode.row, {mask:'0x1003', rhs:1});
let realLhs = 0;
for (let e=0;e<18;e++) if (((BigInt(badNode.row.mask)>>BigInt(e))&1n)===1n) realLhs ^= Number(bits[e]);
assert.equal(realLhs, 0);
assert.equal(badNode.row.rhs, 1);

const negative = [];
let x;
x=deep(hybrid); x.fixtures[0].charges[0]=1;
negative.push(runRaw('numeric-charge-1',compact(x)));
x=deep(hybrid); x.fixtures[0].proof.find(q=>q.id===50).support=[0,1,12];
negative.push(runRaw('typed-support-array-with-rotated-table',compact(x)));
x=deep(hybrid); x.fixtures[0].proof.find(q=>q.id===50).support='210';
negative.push(runRaw('unsupported-string-permutation',compact(x)));
x=deep(hybrid); x.fixtures[0].proof.find(q=>q.id===50).table=102;
negative.push(runRaw('unadjusted-rotated-table',compact(x)));
x=deep(hybrid); x.fixtures[0].clauses[0].literals[0]=999;
negative.push(runRaw('forged-source-literal',compact(x)));
x=deep(hybrid); x.fixtures[0].proof[0].parents[0]='missing-source';
negative.push(runRaw('missing-parent',compact(x)));
x=deep(hybrid); x.fixtures[0].proof.at(-1).row.rhs=0;
negative.push(runRaw('bad-terminal-sink',compact(x)));
for (const r of negative) expectRejected(r);

const out = {
  run:'LSPV-5/500',
  timestamp:'2026-11-11 19:48 PST',
  model:'unchanged archived /341 checker as direct Node OS CLI subprocess',
  checker:{path:checkerPath,git_blob:gitBlob(checkerBytes),sha256:sha256(checkerBytes),bytes:checkerBytes.length},
  prerequisites:[
    {path:basePath,git_blob:gitBlob(baseBytes),sha256:sha256(baseBytes),bytes:baseBytes.length},
    {path:rotatedPath,git_blob:gitBlob(rotatedBytes),sha256:sha256(rotatedBytes),bytes:rotatedBytes.length}
  ],
  positive,
  negative,
  hybrid:{
    path:witnessPath,
    bytes:hybridBytes.length,
    sha256:sha256(hybridBytes),
    git_blob:gitBlob(hybridBytes),
    charge_lexeme_value:hybrid.fixtures[0].charges[0],
    support_lexeme:badNode.support,
    table:badNode.table,
    paid_records:f.proof.length,
    source_clauses:f.clauses.length,
    satisfying_assignment:bits,
    satisfied_source_clauses:sourceSatisfied,
    advertised_row:badNode.row,
    real_row_lhs:realLhs,
    advertised_row_holds:realLhs===badNode.row.rhs
  },
  result:'The direct archived /341 CLI accepts a composed string-charge/support-string packet whose original 48-clause source is SAT and whose advertised node-50 affine row is false under the displayed satisfying assignment.',
  status:'COMPUTATIONAL exact accepted-byte soundness failure for recovered /341 fixture only',
  limitations:[
    'not the complete historical R_mix341 dispatcher',
    'does not authenticate Resolution, LOCAL-CONVERT, paid DEF, contexts, branch joins or deletion',
    '47 parsed proof records are not a minimum-work or machine-resource lower bound',
    'accepted checker path must remain in an acceptance-complete abstraction; a trusted mathematical proof semantics must reject it at a separate source/type gate'
  ]
};
fs.mkdirSync(path.dirname(rawPath),{recursive:true});
fs.writeFileSync(rawPath, JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify({
  run:out.run,
  direct_cli_accepts:positive.length,
  direct_cli_rejects:negative.length,
  hybrid_bytes:out.hybrid.bytes,
  hybrid_sha256:out.hybrid.sha256,
  source_satisfied:String(sourceSatisfied)+'/48',
  false_row:String(realLhs)+' != '+String(badNode.row.rhs),
  historical_full_mix341_authenticated:false
},null,2));

