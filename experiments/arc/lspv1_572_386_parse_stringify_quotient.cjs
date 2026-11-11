#!/usr/bin/env node
'use strict';
// LSPV-1/572: execute the UNMODIFIED archived /386 verifier on exact raw
// and JSON.parse -> JSON.stringify normalized byte packets.
// Run: node experiments/arc/lspv1_572_386_parse_stringify_quotient.cjs
//      node experiments/arc/lspv1_572_386_parse_stringify_quotient.cjs --write /tmp/572.json
const fs=require('node:fs');
const path=require('node:path');
const os=require('node:os');
const cp=require('node:child_process');
const crypto=require('node:crypto');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checkerPath=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedPath=path.join(root,'results/raw/arc/2026-11-11_0203_LSPV1_568_K4_DP_CLI29.json');
const expectedCheckerBlob='338305c0ce101704205e57543756b8127074a986';
const expectedSeedBlob='e3eb2a46857776089ab83f4ad50159ef622d2869';
const gitBlob=b=>crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
const sha256=b=>crypto.createHash('sha256').update(b).digest('hex');
const checkerBytes=fs.readFileSync(checkerPath),seedBytes=fs.readFileSync(seedPath);
assert.equal(gitBlob(checkerBytes),expectedCheckerBlob,'original checker blob mismatch');
assert.equal(gitBlob(seedBytes),expectedSeedBlob,'original K4 seed blob mismatch');
const seed=seedBytes.toString('utf8');
function replaceOne(s,from,to){
 assert.ok(s.includes(from),'mutation anchor absent: '+from);
 return s.replace(from,to);
}
const cases=[
 ['baseline',seed,true],
 ['shadowed_charge',replaceOne(seed,'"spec": {','"spec": {"charge":[0,0,0,0],'),true],
 ['guard_decimal',replaceOne(seed,'"guard": 7','"guard": 7.0'),true],
 ['parent_rounding',replaceOne(seed,'"parents": [\n        0,\n        4\n      ]','"parents": [\n        0,\n        4.0000000000000001\n      ]'),true],
 ['unused_infinite_number',replaceOne(seed,'"spec": {','"spec": {"ignored_extraneous":1e400,'),true],
 ['unused_surrogate_string',replaceOne(seed,'"spec": {','"spec": {"\\uD800":"\\uD801",'),true],
 ['escaped_key',replaceOne(seed,'"guard": 7','"\\u0067uard": 7'),true],
 ['underpaid',replaceOne(seed,'"paid_total": 29','"paid_total": 28'),false],
 ['forged_kind',replaceOne(seed,'"kind": "RES"','"kind": "LOCAL-CONVERT"'),false]
];
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-lspv1-572-'));
function originalCLI(s,filename){
 const file=path.join(tmp,filename);
 const bytes=Buffer.from(s,'utf8');fs.writeFileSync(file,bytes);
 const p=cp.spawnSync(process.execPath,[checkerPath,file],{encoding:'utf8',timeout:20000,maxBuffer:1024*1024});
 return {accept:p.status===0&&!p.error,exit:p.status,paid:p.status===0?JSON.parse(p.stdout.trim()).paid:null,
 assertions:p.status===0?JSON.parse(p.stdout.trim()).assertions:null,
 stderr:p.status===0?'':(p.stderr||String(p.error||'')).slice(0,350),
 sha256:sha256(bytes),bytes:bytes.length};
}
let rows=[];
try{
 for(let i=0;i<cases.length;i++){
  const [name,raw,expect]=cases[i];
  const norm=JSON.stringify(JSON.parse(raw));
  assert.equal(JSON.stringify(JSON.parse(norm)),norm,'canonicalization not idempotent');
  const orig=originalCLI(raw,'raw-'+i+'.json');
  const normalized=originalCLI(norm,'normalized-'+i+'.json');
  assert.equal(orig.accept,expect,'raw original mismatch for '+name);
  assert.equal(normalized.accept,expect,'normalized original mismatch for '+name);
  assert.equal(orig.paid,normalized.paid,'paid work changed for '+name);
  if(expect){assert.equal(orig.paid,29);assert.equal(normalized.paid,29);}
  rows.push({name,expected_accept:expect,raw:orig,normalized});
 }
} finally {
 for(const f of fs.readdirSync(tmp))fs.unlinkSync(path.join(tmp,f));
 fs.rmdirSync(tmp);
}
const result={
 title:'LSPV-1/572 archived /386 parse-serialize quotient, original OS CLI replay',
 checker_git_blob:expectedCheckerBlob,
 seed_git_blob:expectedSeedBlob,
 node:process.version,
 mode:'original unchanged Node.js executable through child_process; deterministic 9-pair tests',
 cases:rows,
 accepted_pairs:rows.filter(x=>x.raw.accept&&x.normalized.accept).length,
 rejected_pairs:rows.filter(x=>!x.raw.accept&&!x.normalized.accept).length,
 total_positive_assertions:rows.reduce((s,x)=>s+(x.raw.assertions||0)+(x.normalized.assertions||0),0),
 limitation:'Finite tests; the universal accepted-byte normalization theorem is independently established by source-code semantic reasoning. Does not extend to /341 or complete historical R_mix341.'
};
if(process.argv[2]==='--write'){
 assert.ok(process.argv[3],'--write requires destination path');
 fs.writeFileSync(process.argv[3],JSON.stringify(result,null,2)+'\n');
}
console.log(JSON.stringify(result,null,2));
