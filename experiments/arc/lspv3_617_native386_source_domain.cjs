#!/usr/bin/env node
'use strict';
// LSPV-3/617, independently runnable OS-Node witness of original /386
// source-domain soundness no-go. This script DOES NOT implement a new checker.
// Run: node experiments/arc/lspv3_617_native386_source_domain.cjs [output.json]
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const cp=require('node:child_process'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checkerPath='experiments/arc/lspv2_386_independent_verify.js';
const seedPath='results/raw/arc/2026-11-11_0407_LSPV2_555_ACCEPTED_LIVE_DEF_RES_K1.json';
const pinned={
 checker:'338305c0ce101704205e57543756b8127074a986',
 seed:'aeeb555c4dcf7f510a9a501c8afc609b629a9298'
};
function blobSHA(b){return crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');}
function sha256(b){return crypto.createHash('sha256').update(b).digest('hex');}
const cb=fs.readFileSync(path.join(root,checkerPath));
const sb=fs.readFileSync(path.join(root,seedPath));
assert.equal(blobSHA(cb),pinned.checker,'original checker blob changed');
assert.equal(blobSHA(sb),pinned.seed,'original seed blob changed');
const seed=JSON.parse(sb.toString('utf8'));
const {h,edges,guard}=seed.spec,E=edges.length;
assert.deepEqual([h,E,guard],[4,6,7]);
const key=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function originalSource(charge){
 const result=[];
 for(let v=0;v<h;v++){
  const inc=edges.map(([a,b],i)=>a===v||b===v?i+1:null).filter(x=>x!==null);
  assert.equal(inc.length,3);
  for(let pattern=0;pattern<8;pattern++){
   const bits=[pattern&1,(pattern>>1)&1,(pattern>>2)&1];
   if((bits[0]^bits[1]^bits[2])!==charge[v])
    result.push(key([...inc.map((e,i)=>bits[i]?-e:e),-guard]));
  }
 }
 result.push([guard]);return result;
}
function sat(cnf,assignment){
 return cnf.every(clause=>clause.some(lit=>{
  const val=(assignment>>(Math.abs(lit)-1))&1;
  return lit>0?val===1:val===0;
 }));
}
const source=originalSource(seed.spec.charge);
assert.deepEqual(source.map(JSON.stringify).sort(),
 seed.records.filter(r=>r.kind==='SOURCE').map(r=>JSON.stringify(r.c)).sort(),
 'reconstructed source does not match signed original clauses');
const chargeCases=[];
for(let mask=0;mask<1<<h;mask++){
 const charge=Array.from({length:h},(_,v)=>(mask>>v)&1);
 const odd=charge.reduce((a,b)=>a^b,0)===1;
 const cnf=originalSource(charge);
 let models=0;
 for(let bits=0;bits<1<<E;bits++){
  const fullAssignment=bits|(1<<(guard-1)); // guard SOURCE [g] is TRUE
  if(sat(cnf,fullAssignment))models++;
 }
 const expected=odd?0:Math.pow(2,E-h+1);
 assert.equal(models,expected,'K4 parity/model-count regression '+mask);
 chargeCases.push({charge,odd,clauses:cnf.length,models,expected});
}
const testCases=[
 ['baseline',()=>{},true],
 ['wrong_res_pivot',p=>{p.records.at(-1).pivot=99998;},false],
 ['wrong_def_facet',p=>{p.records.find(r=>r.kind==='DEF').c=[p.spec.guard];},false],
 ['underpayment',p=>{p.summary.paid_total--;},false],
 ['wrong_source',p=>{p.records.find(r=>r.kind==='SOURCE').c=[-p.spec.guard];},false],
 ['unknown_opcode',p=>{p.records.at(-1).kind='LOCAL-CONVERT';},false],
 ['even_charge',p=>{p.spec.charge=[0,0,0,0];},false]
];
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-617-'));
const checkerCases=[];
try{
 for(let i=0;i<testCases.length;i++){
  const [name,change,expected]=testCases[i];
  const pkt=JSON.parse(sb.toString('utf8'));change(pkt);
  const bytes=Buffer.from(JSON.stringify(pkt)+'\n');
  const filename=path.join(tmp,'packet_'+i+'.json');
  fs.writeFileSync(filename,bytes);
  const proc=cp.spawnSync(process.execPath,[path.join(root,checkerPath),filename],
        {encoding:'utf8',maxBuffer:2*1024*1024});
  const accepted=proc.status===0;
  assert.equal(accepted,expected,'original CLI verdict '+name);
  const result=accepted?JSON.parse(proc.stdout):null;
  if(accepted){
   assert.equal(result.assertions,3509);
   assert.equal(result.negativeTests,11);
   assert.equal(result.paid,33);
  }
  checkerCases.push({name,expected,accepted,sha256:sha256(bytes),
     assertions:result?.assertions??null,bundledNegatives:result?.negativeTests??null,
     error:accepted?null:(proc.stderr||'').split('\n').find(s=>s.includes('Error:'))||String(proc.status)});
 }
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
const out={schema:'LSPV3-617-ORIGINAL386-RESTRICTED-SOURCE-DOMAIN/v1',
 date_pst:'2026-11-13 09:24 PST',status:'PROVED/RESTRICTED + COMPUTATIONAL',
 model:'Pinned /386 CLI only, NOT historical complete R_mix341',
 checker_blob:pinned.checker,seed_blob:pinned.seed,
 source_match:true,guard,edges:E,h,source_clauses:17,
 charge_cases:chargeCases,source_assertions:16*64,
 original_checker_cases:checkerCases,
 original_checker_executed:'OS Node subprocess, original source unchanged',
 disclaimer:'Script tests a fixed K4 family and does not prove native mixed-rule closure or a complexity lower bound. Logical work, bytes, physical time, span and peak space remain distinct.'
};
const output=process.argv[2];
if(output)fs.writeFileSync(output,JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify({status:'PASS',source_rows:chargeCases.length,
 odd_unsat:chargeCases.filter(x=>x.odd&&x.models===0).length,
 even_eight_models:chargeCases.filter(x=>!x.odd&&x.models===8).length,
 checker_cases:checkerCases.length,checker_passed:checkerCases.every(x=>x.accepted===x.expected)}));
