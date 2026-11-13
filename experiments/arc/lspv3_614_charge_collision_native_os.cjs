#!/usr/bin/env node
'use strict';
// P2-L3-614: complete original /341 CLI OS subprocess regression.
// Run from repository checkout:
// node experiments/arc/lspv3_614_charge_collision_native_os.cjs [raw-output.json]
// This is a REPLAYER, not a substitute checker. Requires the pinned originals.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const cp=require('node:child_process'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const corpus=path.join(root,'results/raw/arc/2026-11-10_1112_LSPV2_537_NATIVE_BYTE_CORPUS_RAW.json');
function gitBlob(file) {
 const b=fs.readFileSync(file);
 return crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');
}
assert.equal(gitBlob(checker),'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0');
assert.equal(gitBlob(corpus),'d5e2d22674b0af365e9b82e4f1b2af8307182ba6');
const seed=JSON.parse(JSON.parse(fs.readFileSync(corpus,'utf8')).minimal.packetBytes);
const cases=[
 ['original_numeric',[1,0,0,0],true],
 ['typed_collision',[false,'1',0,0],true],
 ['coerced_numeric',[0,1,0,0],false],
 ['bool_numeric',[false,1,0,0],false],
 ['numeric_string',[0,'1',0,0],false],
 ['strings_3_2',['3','2',0,0],true],
 ['numbers_3_2',[3,2,0,0],true],
 ['numbers_2_3',[2,3,0,0],true],
 ['string_one',['1',0,0,0],true],
 ['boolean_one',[true,0,0,0],true],
 ['array_one',[[1],0,0,0],true],
 ['null_zero',[1,null,0,0],true],
 ['object_zero',[1,{},0,0],true],
 ['array_zero',[1,[],0,0],true],
 ['large_int32_one',[4294967297,0,0,0],true],
 ['global_even',[0,0,0,0],false],
 ['wrong_int32_xor',[2,0,0,0],false],
 ['forbidden_numeric_at_two',[1,1,1,0],false],
 ['corrupt_res_op',[false,'1',0,0],false,'op'],
 ['corrupt_parent',[false,'1',0,0],false,'parent'],
 ['corrupt_sink',[false,'1',0,0],false,'sink'],
 ['corrupt_source',[false,'1',0,0],false,'source']
];
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-l3-614-'));
const input=path.join(dir,'packet.json');
const rows=[];
try {
 for(const [name,charges,expected,corruption] of cases) {
  const p=JSON.parse(JSON.stringify(seed)),f=p.fixtures[0];f.charges=charges;
  if(corruption==='op')f.proof[0].rule='RES';
  if(corruption==='parent')f.proof[0].parents[0]='forged';
  if(corruption==='sink')f.proof.at(-1).row.rhs=0;
  if(corruption==='source')f.clauses[0].literals[0]=999;
  const bytes=JSON.stringify(p)+'\n';fs.writeFileSync(input,bytes);
  const r=cp.spawnSync(process.execPath,[checker,input],{encoding:'utf8',timeout:25000,maxBuffer:8*1024*1024});
  if(r.error)throw r.error;
  const actual=r.status===0?'ACCEPT':'REJECT',wanted=expected?'ACCEPT':'REJECT';
  assert.equal(actual,wanted,name+': '+r.stderr);
  const checks=r.status===0?JSON.parse(r.stdout).checks:null;
  if(r.status===0)assert.equal(checks,1401);
  rows.push({name,charges,normalized:charges.map(x=>x|0),corruption:corruption||null,
   actual,expected:wanted,checks,error:r.status===0?null:r.stderr.slice(0,300),
   sha256:crypto.createHash('sha256').update(bytes).digest('hex')});
 }
 const positives=rows.filter(x=>x.actual==='ACCEPT');
 assert.equal(rows.length,22);assert.equal(positives.length,12);
 assert.equal(positives.reduce((s,x)=>s+x.checks,0),16812);
 const result={schema:'PNP_LSPV3_614_OS_PROCESS_REPLAY/v1',checker_blob:gitBlob(checker),
  corpus_blob:gitBlob(corpus),execution:'unchanged original checker as separate Node OS process',
  counts:{tests:22,accept:12,reject:10,positive_assertion_groups:16812},rows};
 if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+'\n');
 process.stdout.write(JSON.stringify(result,null,2)+'\n');
} finally {fs.rmSync(dir,{recursive:true,force:true});}
