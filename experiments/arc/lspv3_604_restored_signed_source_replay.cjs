#!/usr/bin/env node
'use strict';
/* LSPV-3/604. Native /386 source-artifact recovery replay.
 * Run from the j15marti/pnp root:
 * node experiments/arc/lspv3_604_restored_signed_source_replay.cjs [output.json]
 * Executes the unchanged historical /386 OS checker. It does not implement R_mix341.
 */
const fs=require('fs'),path=require('path'),os=require('os');
const crypto=require('crypto'),cp=require('child_process'),assert=require('assert/strict');
const root=path.resolve(__dirname,'../..');
const files={
  source:'results/raw/arc/574_k01_SIGNED_SOURCE.cnf',
  alias:'results/raw/arc/2026-11-12_1412_LSPV2_583_SIGNED_K4_SOURCE.cnf',
  seed:'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json',
  checker:'experiments/arc/lspv2_386_independent_verify.js'
};
const pins={
  source:'3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c',
  alias:'3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c',
  seed:'0d8b1894f91d00c554727a92fed35b2bb58f2b1602f2a3cfcb949effda43ceb0',
  checker:'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113'
};
const digest=b=>crypto.createHash('sha256').update(b).digest('hex');
const data={};for(const k of Object.keys(files)){
  data[k]=fs.readFileSync(path.join(root,files[k]));
  assert.equal(digest(data[k]),pins[k],'pinned source '+k);
}
assert.deepEqual(data.source,data.alias,'byte-identical recovered source');
const sourceLines=data.source.toString('utf8').trimEnd().split(/\r?\n/);
assert.equal(sourceLines[0],'p cnf 7 17');
const original=sourceLines.slice(1).map(line=>{
  const nums=line.trim().split(/\s+/).map(Number);
  assert.equal(nums.at(-1),0);return nums.slice(0,-1);
});
assert.equal(original.length,17);
const seed=JSON.parse(data.seed);
const recorded=seed.records.filter(r=>r.kind==='SOURCE').map(r=>r.c);
assert.deepEqual(original.map(JSON.stringify),recorded.map(JSON.stringify),
  'external signed SOURCE positions differ');
let models=0;
for(let a=0;a<128;a++){
  const holds=original.every(c=>c.some(l=>(((a>>(Math.abs(l)-1))&1)===Number(l>0))));
  models+=Number(holds);
}
assert.equal(models,0,'independent seven-variable exhaustive UNSAT control');
const checker=path.join(root,files.checker);
function execute(filename){
 const out=cp.spawnSync(process.execPath,[checker,filename],
   {encoding:'utf8',timeout:30000,maxBuffer:2000000});
 return {status:out.status,stdout:out.stdout,stderr:out.stderr};
}
const good=execute(path.join(root,files.seed));
assert.equal(good.status,0,'original native OS checker rejected exact W29 seed: '+good.stderr);
const positive=JSON.parse(good.stdout.trim());
assert.equal(positive.paid,29);
assert.equal(positive.res,28);
assert.equal(positive.def,1);
assert.equal(positive.sources,17);
assert.equal(positive.negativeTests,11);
const corrupt=JSON.parse(data.seed);corrupt.records.at(-1).pivot=999;
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-604-'));
let hostile;try{
 const f=path.join(dir,'bad.json');fs.writeFileSync(f,JSON.stringify(corrupt)+'\n');
 hostile=execute(f);assert.notEqual(hostile.status,0,'bad signed pivot accepted');
}finally{fs.rmSync(dir,{recursive:true,force:true});}
const ledger={
 schema:'LSPV3-604-RECOVERED-SIGNED-SOURCE-NATIVE386/v1',
 scope:'Restored identical source bytes and executed unchanged /386 Node CLI; full R_mix341 remains OPEN',
 originalFiles:files,sha256:pins,
 externalSourceBytes:data.source.length,originalVariables:7,originalClauses:17,
 signedClausesPositionByPositionEqual:true,assignmentsExhaustivelyChecked:128,sourceModels:models,
 originalVerifierPositive:{paid:positive.paid,res:positive.res,def:positive.def,
  sources:positive.sources,negativeTests:positive.negativeTests,assertions:positive.assertions},
 hostileBadPivotRejected:hostile.status!==0,
 hostileError:(hostile.stderr||'').split('\n').find(x=>x.includes('Error:'))||'',
 distinctResources:'logical work 29; evidence bytes, time, span and peak space not measured'
};
const output=JSON.stringify(ledger,null,2)+'\n';
if(process.argv[2])fs.writeFileSync(process.argv[2],output);
process.stdout.write(output);
