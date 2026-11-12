#!/usr/bin/env node
'use strict';
/*
 LSPV-3/591: archived /341 accepted-byte BigInt row.mask JSON-array fiber.
 Execute in a complete repository checkout:
   node experiments/arc/lspv3_591_native341_bigint_mask_types.cjs [output.json]
 Runs the UNCHANGED original historical-subset verifier in real Node OS
 subprocesses. This runner is separately published; hosted-V8 evidence
 was performed earlier and is NOT an OS-replay result.
 This is NOT an implementation of the missing full R_mix341 calculus.
*/
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const cp = require('node:child_process');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');

const root = path.resolve(__dirname, '../..');
const checkerRel = 'experiments/arc/lspv2_341_independent_verify.js';
const seedRel = 'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json';
const witnessRel = 'results/raw/arc/2026-11-12_0827_LSPV3_591_NATIVE341_ALL_SEVEN_ARRAY_MASKS_ACCEPTED.json';
const pins = {
  [checkerRel]: 'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
  [seedRel]: 'fe27fe1011d0021e721ccaeb747ed58da65d7464'
};
function blob(buffer) {
  return crypto.createHash('sha1')
    .update(Buffer.from('blob ' + buffer.length + '\0'))
    .update(buffer).digest('hex');
}
function sha(buffer) { return crypto.createHash('sha256').update(buffer).digest('hex'); }
for (const [file, expected] of Object.entries(pins)) {
  assert.equal(blob(fs.readFileSync(path.join(root, file))), expected,
    'Original source byte drift: ' + file);
}
const source = JSON.parse(fs.readFileSync(path.join(root, seedRel), 'utf8'));
const base = source.fixtures[0];
assert.equal(base.graph.n, 4);
assert.equal(base.clauses.length, 16);
assert.equal(base.proof.length, 15);
const rowPositions = base.proof.flatMap((p,i) => p.row ? [i] : []);
assert.deepEqual(rowPositions, [2,5,8,11,12,13,14]);
const expectedValues = [7,25,42,52,30,52,0];
assert.deepEqual(rowPositions.map(i => Number(BigInt(base.proof[i].row.mask))), expectedValues);

const copy = x => JSON.parse(JSON.stringify(x));
function packet(selector) {
  const fixture = copy(base);
  rowPositions.forEach((position,k) => {
    if ((selector >>> k) & 1) {
      fixture.proof[position].row.mask = [expectedValues[k]];
    }
  });
  return {fixtures:[fixture], summary:[null]};
}
const witness = JSON.stringify(packet(127));
assert.equal(fs.readFileSync(path.join(root, witnessRel), 'utf8'), witness,
  'Published native-accepted witness does not reproduce byte-for-byte');

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lspv3-591-'));
const rows = [];
function replay(name, obj, expected) {
  const input = Buffer.from(JSON.stringify(obj), 'utf8');
  const filename = path.join(tmp, 'packet.json');
  fs.writeFileSync(filename, input);
  const result = cp.spawnSync(process.execPath,
    [path.join(root,checkerRel),filename],
    {cwd:root,encoding:'utf8',timeout:30000,maxBuffer:4*1024*1024});
  assert.equal(result.error, undefined, 'Unable to launch original Node verifier: ' + name);
  const accepted = result.status === 0;
  assert.equal(accepted, expected,
    name + ' OS verdict mismatch: ' + String(result.stderr).slice(0,350));
  let native = null;
  if (accepted) {
    native = JSON.parse(result.stdout.trim());
    assert.equal(native.checks,1401, 'original assertion count ' + name);
    assert.equal(native.cases.length,1);
    assert.equal(native.cases[0].proofNodes,15);
    assert.equal(native.corruptions,5, 'original bundled negative tests ' + name);
  }
  const line = {name, accepted, expected, sizeBytes:input.length,
    packetSha256:sha(input), originalAssertions:native ? native.checks : null,
    originalBundledHostiles:native ? native.corruptions : null,
    exitStatus:result.status, firstError:accepted ? null :
      (result.stderr || result.stdout).trim().split(/\r?\n/)[0]};
  rows.push(line);
  return line;
}
try {
  for (let selector=0;selector<128;selector++) {
    replay('mask_subset_' + selector,packet(selector),true);
  }
  const hostiles = [
    ['duplicate_array_element',f=>{ f.proof[2].row.mask=[7,7]; }],
    ['null_terminal_mask',f=>{ f.proof[14].row.mask=null; }],
    ['wrong_terminal_parity',f=>{ f.proof[14].row.rhs=0; }],
    ['missing_and3_parent',f=>{ f.proof[2].parents[0]='missing'; }],
    ['forged_signed_source',f=>{ f.clauses[0].literals[0]=999; }],
    ['unsupported_local_convert',f=>{ f.proof[2].rule='LOCAL-CONVERT'; }]
  ];
  for (const [name,change] of hostiles) {
    const f=copy(base); change(f);
    replay('hostile_'+name,{fixtures:[f],summary:[null]},false);
  }
  const out={
    id:'LSPV-3/591',
    authority:'ORIGINAL archived /341 verifier, actual OS Node subprocess',
    checkerGitBlob:pins[checkerRel],
    seedGitBlob:pins[seedRel],
    witnessPath:witnessRel,
    sourceClauses:16,paidLogicalWork:15,annotatedRowCount:7,
    positive:rows.filter(x=>x.accepted).length,
    negative:rows.filter(x=>!x.accepted).length,
    originalAssertionGroups:rows.filter(x=>x.accepted)
      .reduce((s,x)=>s+x.originalAssertions,0),
    originalBundledNegativeControls:rows.filter(x=>x.accepted)
      .reduce((s,x)=>s+x.originalBundledHostiles,0),
    rows,
    limitations:'Archived SOURCE/AND3/XOR fixture checker, not complete historical R_mix341. In-band source, not external source-bound. Separate OS reproduction of previously hosted-V8 tests.'
  };
  if (process.argv[2]) {
    const outpath = path.resolve(process.argv[2]);
    fs.mkdirSync(path.dirname(outpath),{recursive:true});
    fs.writeFileSync(outpath, JSON.stringify(out,null,2)+'\n');
  }
  console.log(JSON.stringify({id:out.id,status:'PASS',
    positives:out.positive,negatives:out.negative,
    assertions:out.originalAssertionGroups,hostiles:out.originalBundledNegativeControls,
    checkerGitBlob:out.checkerGitBlob},null,2));
} finally {
  fs.rmSync(tmp,{recursive:true,force:true});
}
