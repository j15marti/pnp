#!/usr/bin/env node
'use strict';
/* LSPV-4/567: exact alpha-renamed guard-ID byte/resource firewall.
   Original /386 checker is REQUIRED and invoked unchanged via Node OS.
   Run from repo root: node experiments/arc/lspv4_567_guard_id_byte_firewall.cjs
*/
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const crypto=require('node:crypto'),child=require('node:child_process'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const expected='22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113';
assert.equal(crypto.createHash('sha256').update(fs.readFileSync(checker)).digest('hex'),expected,'original checker drift');
const inputs=[
 'results/raw/arc/2026-11-12_1031_LSPV4_566_W38_P45_AREA958_NATIVE386_ACCEPTED.json',
 'results/raw/arc/2026-11-12_1031_LSPV4_566_W39_P45_AREA748_NATIVE386_ACCEPTED.json'];
const key=c=>c.sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function rename(d,g){
 const a=structuredClone(d),old=a.spec.guard;a.spec.guard=g;
 for(const r of a.records){
   r.c=key(r.c.map(v=>Math.abs(v)===old?Math.sign(v)*g:v));
   if(r.pivot!==undefined&&Math.abs(r.pivot)===old)r.pivot=Math.sign(r.pivot)*g;
 }
 return a;
}
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-567-'));
const results=[];
try{
 for(const file of inputs){
  const base=JSON.parse(fs.readFileSync(path.join(root,file),'utf8'));
  const n0=Buffer.byteLength(JSON.stringify(base)),g0=base.spec.guard;
  const occurrences=1+base.records.reduce((a,r)=>a+r.c.filter(x=>Math.abs(x)===g0).length+(r.pivot!==undefined&&Math.abs(r.pivot)===g0?1:0),0);
  const parentOccurrences=base.records.reduce((a,r)=>a+r.parents.reduce((s,p)=>s+base.records[p].c.filter(x=>Math.abs(x)===g0).length,0),0);
  const scans=base.records.reduce((a,r)=>a+r.parents.reduce((s,p)=>s+Buffer.byteLength(JSON.stringify(base.records[p].c)),0),0);
  let cases=[];
  for(const g of [11,99,1009,1000003,2147483647,Number.MAX_SAFE_INTEGER,6,8,2**53]){
   const obj=rename(base,g),txt=JSON.stringify(obj),f=path.join(temp,'proof.json');fs.writeFileSync(f,txt);
   const proc=child.spawnSync(process.execPath,[checker,f],{encoding:'utf8',maxBuffer:8*1024*1024});
   const expectedAccept=(g>=11&&Number.isSafeInteger(g));
   assert.equal(proc.status===0,expectedAccept,'native acceptance mismatch guard '+g);
   const newSize=Buffer.byteLength(txt),digits=String(g).length;
   assert.equal(newSize,n0+(digits-1)*occurrences,'byte occurrence identity');
   let output=null;if(proc.status===0){output=JSON.parse(proc.stdout.trim());assert.equal(output.negativeTests,11)}
   cases.push({guard:g,accepted:proc.status===0,bytes:newSize,parentScanProxy:scans+(digits-1)*parentOccurrences,assertions:output?.assertions??null,
      stdoutSha256:crypto.createHash('sha256').update(proc.stdout).digest('hex'),
      stderr:proc.status===0?null:proc.stderr.slice(0,240)});
  }
  results.push({input:file,baseBytes:n0,occurrences,parentOccurrences,baseScan:scans,cases});
 }
 console.log(JSON.stringify({run:'LSPV-4/567',originalCheckerSHA256:expected,environment:process.version,results},null,2));
}finally{fs.rmSync(temp,{recursive:true,force:true})}
