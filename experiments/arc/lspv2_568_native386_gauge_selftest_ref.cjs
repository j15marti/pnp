#!/usr/bin/env node
'use strict';
/* LSPV-2/568 differential: original checker vs a clearly marked REFERENCE
 * self-test correction. Not an R_mix341 implementation or a new authoritative checker.
 * Inputs are pinned exact original Git blobs, all checker runs are OS subprocesses.
 * Usage: node experiments/arc/lspv2_568_native386_gauge_selftest_ref.cjs
 */
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const os=require('node:os');
const cp=require('node:child_process');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checkerPath=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const inputPath=path.join(root,'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json');
const expected={
  checker:'338305c0ce101704205e57543756b8127074a986',
  seed:'318c52d99977ea4e91bc8554051138a700c1dc94'
};
const gitBlob=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
const sha256=b=>crypto.createHash('sha256').update(b).digest('hex');
function pinned(p,sha){const b=fs.readFileSync(p);assert.equal(gitBlob(b),sha,p+' differs from original project');return b;}
const original=pinned(checkerPath,expected.checker).toString('utf8');
const base=JSON.parse(pinned(inputPath,expected.seed).toString('utf8'));
function sorted(a){return [...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);}
function transform(original,mask){
  const p=structuredClone(original),flip=new Set();
  p.spec.edges.forEach(([u,v],j)=>{if((mask>>>j)&1){flip.add(j+1);p.spec.charge[u]^=1;p.spec.charge[v]^=1;}});
  const lit=x=>flip.has(Math.abs(x))?-x:x;
  for(const g of p.gate_defs){g[2]=lit(g[2]);g[3]=lit(g[3]);}
  for(const r of p.records){r.c=sorted(r.c.map(lit));if(r.kind==='RES')r.pivot=lit(r.pivot);}
  return p;
}
// Independent source occurrence checker, separate from original parser.
function sourceRows(spec){
  const {h,edges,charge,guard}=spec;
  const occ=Array.from({length:h},()=>[]);
  edges.forEach(([u,v],i)=>{occ[u].push(i+1);occ[v].push(i+1);});
  const rows=[];
  for(let v=0;v<h;v++){
    assert.equal(occ[v].length,3);
    for(let m=0;m<8;m++){
      const parity=((m&1)+((m>>1)&1)+((m>>2)&1))%2;
      if(parity===charge[v])continue;
      const row=sorted([...occ[v].map((e,i)=>((m>>i)&1)?-e:e),-guard]);
      rows.push(JSON.stringify([v,row]));
    }
  }
  rows.push(JSON.stringify([-1,[guard]]));
  return rows.sort();
}
function sourceBound(p){
  const declared=p.records.filter(r=>r.kind==='SOURCE').map(r=>JSON.stringify([r.source,r.c])).sort();
  return JSON.stringify(declared)===JSON.stringify(sourceRows(p.spec));
}
// Patch exactly one self-test line: remove the charge[0] == 1 assumption.
// All proof-rule logic, parsing and built-in corruptions remain literally identical.
const needle='let evenCharge=[0,...charge.slice(1)];';
assert.equal(original.split(needle).length,2,'unique source patch expected');
const corrected=original.replace(needle,'let evenCharge=[charge[0]^1,...charge.slice(1)];');
assert.equal(corrected.length-original.length,10,'unexpected patch delta');
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-568-'));
function run(executable,p,name){
  const packet=Buffer.from(JSON.stringify(p)+'\n');
  fs.writeFileSync(path.join(temp,'packet.json'),packet);
  const res=cp.spawnSync(process.execPath,[executable,path.join(temp,'packet.json')],{encoding:'utf8',timeout:15000,maxBuffer:1e6});
  let parsed=null;
  try{parsed=JSON.parse((res.stdout||'').trim());}catch(_e){}
  return {name,accept:res.status===0&&!!parsed,paid:parsed?.paid??null,assertions:parsed?.assertions??null,
    negativeTests:parsed?.negativeTests??null,stderr:(res.stderr||'').trim().slice(0,260),sha256:sha256(packet),bytes:packet.length};
}
const parsedResults={
  id:'LSPV-2/568',status:'PROVED/RESTRICTED + COMPUTATIONAL',
  originalCheckerGitBlob:expected.checker,baseProofGitBlob:expected.seed,
  wrapperPatch:{before:needle,after:'let evenCharge=[charge[0]^1,...charge.slice(1)];',modifiedCharacters:corrected.length-original.length,
    checkerLabel:'REFERENCE SELF-TEST REPAIR, NEVER HISTORICAL AUTHORITY'},
  node:process.version,platform:process.platform,
  positive:[],corruptions:[],summary:{}
};
try{
  const repairedPath=path.join(temp,'REFERENCE_checker_fixed_even_selftest.js');
  fs.writeFileSync(repairedPath,corrected);
  for(let mask=0;mask<64;mask++){
    const p=transform(base,mask);
    assert.equal(sourceBound(p),true,'signed original SOURCE mismatch mask='+mask);
    const orig=run(checkerPath,p,'original-'+mask);
    const rep=run(repairedPath,p,'reference-'+mask);
    const q0=((mask&1)!==0?1:0)^((mask&2)!==0?1:0)^((mask&4)!==0?1:0);
    const expectedOrig=q0===0;
    assert.equal(orig.accept,expectedOrig,'original CLI unexpected acceptance '+mask);
    assert.equal(rep.accept,true,'corrected reference rejected source-sound proof '+mask);
    assert.equal(rep.paid,29,'cost drift at '+mask);
    if(orig.accept)assert.equal(orig.paid,29);
    parsedResults.positive.push({mask,charge:p.spec.charge,sourceBound:true,
      original:orig,reference:rep,expectedOriginal:expectedOrig});
    if(mask===1){fs.writeFileSync(path.join(root,'results/raw/arc/2026-11-11_1712_LSPV2_568_ORIGINAL_REJECTED_REFERENCE_ACCEPTED.json'),JSON.stringify(p)+'\n');}
  }
  let control=transform(base,1);
  const bads=[
    ['signed_source_forgery',p=>{let r=p.records.find(x=>x.kind==='SOURCE'&&x.source===0);r.c=sorted(r.c.map((x,i)=>i===0?-x:x));}],
    ['resolution_wrong_sign',p=>{p.records.find(r=>r.kind==='RES').pivot*=-1;}],
    ['paid_gate_undercharge',p=>{p.summary.paid_total-=1;}],
    ['stale_charge_vector',p=>{p.spec.charge=[...base.spec.charge];}],
    ['duplicate_original_occurrence',p=>{p.records[0].c=[...p.records[1].c];}],
  ];
  for(const [name,mut] of bads){let x=structuredClone(control);mut(x);let out=run(repairedPath,x,name);assert.equal(out.accept,false,'reference erroneously accepted '+name);parsedResults.corruptions.push(out);}
  const sums={originalAccept:parsedResults.positive.filter(x=>x.original.accept).length,
    originalReject:parsedResults.positive.filter(x=>!x.original.accept).length,
    referenceAccept:parsedResults.positive.filter(x=>x.reference.accept).length,
    referenceReject:parsedResults.positive.filter(x=>!x.reference.accept).length,
    originalAssertionGroups:parsedResults.positive.reduce((z,r)=>z+(r.original.assertions||0),0),
    referenceAssertionGroups:parsedResults.positive.reduce((z,r)=>z+(r.reference.assertions||0),0),
    repairedHostileRejected:parsedResults.corruptions.length,
    sourceBound:parsedResults.positive.every(x=>x.sourceBound)
  };
  parsedResults.summary=sums;
  assert.deepEqual([sums.originalAccept,sums.originalReject,sums.referenceAccept,sums.referenceReject,sums.repairedHostileRejected],[32,32,64,0,5]);
}finally{fs.rmSync(temp,{recursive:true,force:true});}
const outfile=path.join(root,'results/raw/arc/2026-11-11_1712_LSPV2_568_ORIGINAL_OS_VS_REFERENCE_SELFTEST_RAW.json');
fs.writeFileSync(outfile,JSON.stringify(parsedResults,null,2)+'\n');
console.log(JSON.stringify({output:outfile,...parsedResults.summary,rawSha256:sha256(fs.readFileSync(outfile))},null,2));
