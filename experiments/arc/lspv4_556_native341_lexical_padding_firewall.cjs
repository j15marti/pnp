'use strict';
// LSPV-4/556. Run from repository root:
// node experiments/arc/lspv4_556_native341_lexical_padding_firewall.cjs
// Independent OS-process replay, not a replacement historical checker.
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const cp = require('node:child_process');
const assert = require('node:assert/strict');

const ROOT = process.cwd();
const checkerRel = 'experiments/arc/lspv2_341_independent_verify.js';
const fixtureRel = 'results/raw/arc/2026-11-11_1824_LSPV3_582_STRING_CHARGE_SAT_ACCEPTED_PACKET.json';
const checker = path.join(ROOT,checkerRel);
const fixture = path.join(ROOT,fixtureRel);
function blobSha(bytes) {
  return crypto.createHash('sha1').update(Buffer.from('blob ' + bytes.length + '\0')).update(bytes).digest('hex');
}
const checkerBytes = fs.readFileSync(checker);
const fixtureBytes = fs.readFileSync(fixture);
assert.equal(blobSha(checkerBytes),'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0','checker provenance');
assert.equal(blobSha(fixtureBytes),'6cf9b0fe1e5a9419e8967d836c707c385418b810','fixture provenance');
const seed = JSON.parse(fixtureBytes.toString('utf8'));
const bits = '101001000000100000';
assert.equal(bits.length,seed.fixtures[0].graph.edges.length);
function sat(c) {
  return c.literals.some(l => l > 0 ? bits[Math.abs(l)-1]==='1' : bits[Math.abs(l)-1]==='0');
}
const source = seed.fixtures[0].clauses;
assert.equal(source.length,48);
assert(source.every(sat),'Published original signed source must actually be SAT');
const temp = fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-556-'));
const file = path.join(temp,'packet.json');
function run(mut) {
  const obj=structuredClone(seed);
  mut(obj);
  const packet=JSON.stringify(obj)+'\n';
  fs.writeFileSync(file,packet,'utf8');
  const p=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:30000,maxBuffer:1<<21});
  if(p.error)throw p.error;
  const accepted=p.status===0;
  let checks=null;
  if(accepted){const output=JSON.parse(p.stdout);checks=output.checks;}
  return {accepted,bytes:Buffer.byteLength(packet),checks,error:accepted?null:(p.stderr||p.stdout||'').slice(0,300)};
}
try {
  const positives=[0,1,2,8,64,512,4096].map(k=>{
    const r=run(d=>{d.fixtures[0].charges[0]='0'.repeat(k)+'1'});
    assert(r.accepted,'positive k='+k+': '+r.error);
    return {k,bytes:r.bytes,checks:r.checks};
  });
  const negatives=[
    ['typed-numeric-1',d=>{d.fixtures[0].charges[0]=1}],
    ['string-zero',d=>{d.fixtures[0].charges[0]='0'}],
    ['nonnumeric-string',d=>{d.fixtures[0].charges[0]='ZZ1'}],
    ['forged-source',d=>{d.fixtures[0].clauses[0].literals[0]=999}],
    ['bad-parent',d=>{d.fixtures[0].proof[0].parents[0]=-91}],
    ['bad-sink',d=>{d.fixtures[0].proof.at(-1).row.rhs=0}]
  ].map(([name,mut])=>{
    const r=run(mut);assert(!r.accepted,'hostile control accepted: '+name);
    return {name,rejected:true};
  });
  const result={
    tag:'LSPV4_556_NATIVE341_OS_REPLAY',
    checker_blob:blobSha(checkerBytes),fixture_blob:blobSha(fixtureBytes),
    signed_source_clauses_satisfied:source.length,total_signed_source_clauses:source.length,
    paid_records:seed.fixtures[0].proof.length,positives,negatives
  };
  console.log(JSON.stringify(result,null,2));
} finally {
  fs.rmSync(temp,{recursive:true,force:true});
}
