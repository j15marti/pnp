#!/usr/bin/env node
'use strict';
// Reproducer for LSPV-1/607. This launches the UNMODIFIED archived /341
// checker as an OS Node subprocess. It is NOT a replacement full R_mix341 checker.
// Usage: node experiments/arc/lspv1_607_two_sided_native_membership.cjs [output.json]
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const os=require('node:os');
const cp=require('node:child_process');
const crypto=require('node:crypto');
const root=path.resolve(__dirname,'../..');
const rel={
 checker:'experiments/arc/lspv2_341_independent_verify.js',
 original:'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json',
 forged:'results/raw/arc/2026-11-10_1224_LSPV3_551_ACCEPTED_SAT_PACKET.json'
};
const expectedBlobs={checker:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
 original:'fe27fe1011d0021e721ccaeb747ed58da65d7464',
 forged:'706947c767361e7c979b8208677eb983d33838f4'};
const sha256=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
const checker=path.join(root,rel.checker);
const checkerBytes=fs.readFileSync(checker);
const originalBytes=fs.readFileSync(path.join(root,rel.original));
const forgedBytes=fs.readFileSync(path.join(root,rel.forged));
const original=JSON.parse(originalBytes),forged=JSON.parse(forgedBytes);
const clone=x=>JSON.parse(JSON.stringify(x));
const fixture=forged.fixtures.find(f=>f.graph && f.graph.edges.length===18);
assert(fixture && fixture.clauses.length===48 && fixture.proof.length===47);
const witness=Array.from('101001000000100000',Number);
const clauseSat=(c,a)=>c.literals.some(l=>a[Math.abs(l)-1]===Number(l>0));
const nSat=fixture.clauses.filter(c=>clauseSat(c,witness)).length;
assert.equal(nSat,48,'forged-accepted original source must have a genuine SAT witness');
assert.equal(fixture.charges[0],'1','preserve original string charge token');
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv1-607-'));
function run(name,pkt){
 const input=JSON.stringify(pkt),file=path.join(tmp,name+'.json');
 fs.writeFileSync(file,input+'\n');
 const p=cp.spawnSync(process.execPath,[checker,file],{
  encoding:'utf8',timeout:30000,maxBuffer:12*1024*1024});
 if(p.error)throw p.error;
 let parsed=null;
 if(p.status===0){parsed=JSON.parse(p.stdout);}
 return {case:name,accept:p.status===0,exitStatus:p.status,
         checks:parsed?.checks??null,
         bytes:Buffer.byteLength(input),
         inputSha256:sha256(Buffer.from(input)),
         outputSha256:p.status===0?sha256(Buffer.from(p.stdout)):null,
         error:p.status!==0?(p.stderr||p.stdout).trim().slice(0,500):null};
}
try{
 const padded=clone(original);
 const first=padded.fixtures[0].proof[0];
 const paidCopy=clone(first);
 paidCopy.id='PAID_REDUNDANT_AND3_607';
 padded.fixtures[0].proof.splice(1,0,paidCopy);
 const badRule=clone(original);
 badRule.fixtures[0].proof[0].rule='RES';
 const metadata=clone(forged);
 metadata.fixtures[1].externalOriginalInput='p cnf 18 48\n'+
  metadata.fixtures[1].clauses.map(c=>c.literals.join(' ')+' 0').join('\n');
 const rows=[
  run('seven_original',original),
  run('satisfiable_forged_source',forged),
  run('fresh_redundant_AND3',padded),
  run('unknown_RES_rule',badRule),
  run('ignored_external_source_metadata',metadata)
 ];
 assert.deepEqual(rows.map(x=>x.accept),[true,true,false,false,true]);
 assert.equal(rows[0].checks,30714);
 assert.equal(rows[1].checks,2273);
 assert.equal(rows[4].checks,2273);
 assert.match(rows[2].error,/proof candidate length/);
 assert.match(rows[3].error,/unknown rule/);
 const result={
  id:'LSPV-1/607',
  date:'2026-11-12T19:00:00-08:00',
  status:'PROVED/RESTRICTED combined theorem; COMPUTATIONAL original-checker OS replay',
  checker:rel.checker,
  originalSource:rel.original,
  forgedSource:rel.forged,
  historicGitBlobs:expectedBlobs,
  standaloneCheckerSha256:sha256(checkerBytes),
  originalPacketSha256:sha256(originalBytes),
  forgedPacketSha256:sha256(forgedBytes),
  satWitness:'101001000000100000',
  satOriginalSignedClauses:nSat,
  forgedPaidNodes:fixture.proof.length,
  originalK4Paid:original.fixtures[0].proof.length,
  insertedK4Paid:padded.fixtures[0].proof.length,
  cases:rows,
  disclaimer:'Unchanged archived SOURCE/AND3/XOR fixture checker; NOT full historical R_mix341 grammar or SAT proof of lower bound'
 };
 const out=JSON.stringify(result,null,2)+'\n';
 if(process.argv[2])fs.writeFileSync(process.argv[2],out);
 process.stdout.write(out);
}finally{
 fs.rmSync(tmp,{recursive:true,force:true});
}
