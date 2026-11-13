#!/usr/bin/env node
'use strict';
/* LSPV-2/596: original /386 CLI differential replay. Not R_mix341. */
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const crypto=require('node:crypto'),cp=require('node:child_process'),A=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const ck=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const inFile=path.join(root,'results/raw/arc/2026-11-13_0212_LSPV2_595_TRIPLEX_W85_ACCEPTED.json');
const outFile=path.join(root,'results/raw/arc/2026-11-13_0308_LSPV2_596_NATIVE386_W81_ACCEPTED.json');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const read=p=>fs.readFileSync(p),copy=x=>JSON.parse(JSON.stringify(x));
A.equal(hash(read(ck)),'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113');
A.equal(hash(read(inFile)),'4bd50ef54044187a5b9811d87b19c640e55bd4f70d024d057ff5fb57226e5d46');
const initial=JSON.parse(read(inFile));
function support(d){
 const terms=[],h=[];
 d.records.forEach((r,i)=>{
  let z;
  if(r.kind==='SOURCE')z=new Set([i]);
  else if(r.kind==='DEF')z=new Set();
  else if(r.kind==='RES'){const [a,b]=r.parents;A(a<i&&b<i);z=new Set([...h[a],...h[b]]);}
  else throw Error('unrecognized original /386 opcode');
  h.push(z);if(r.c.length===0)terms.push({index:i,source:[...z].sort((a,b)=>a-b)});
 });
 return terms;
}
function quotient(d){
 const old=d.records,rows=[],link=new Map(),cache=new Map(),removed=[];
 old.forEach((x,i)=>{
  const r=copy(x),k=JSON.stringify(r.c);
  if(r.kind==='RES'){
   r.parents=r.parents.map(p=>{A(link.has(p));return link.get(p)});
   if(i!==old.length-1&&r.c.length===0){
    A(!old.slice(i+1).some(t=>t.parents?.includes(i)));
    removed.push({oldIndex:i,reason:'nonterminal-empty'});return;
   }
   if(i!==old.length-1&&cache.has(k)){
    link.set(i,cache.get(k));removed.push({oldIndex:i,reason:'prior-equal-signed-clause'});return;
   }
  }
  const j=rows.length;rows.push(r);link.set(i,j);if(!cache.has(k))cache.set(k,j);
 });
 const nres=rows.filter(x=>x.kind==='RES').length;
 return {proof:{spec:copy(d.spec),gate_defs:copy(d.gate_defs),records:rows,
  summary:{source:rows.filter(x=>x.kind==='SOURCE').length,
   def_views:rows.filter(x=>x.kind==='DEF').length,resolution:nres,
   paid_gates:d.gate_defs.length,paid_total:nres+d.gate_defs.length,
   live_records:rows.length}},removed};
}
const {proof,removed}=quotient(initial);
const before=support(initial),after=support(proof);
A.deepEqual(before.map(x=>x.index),[76,104,132]);
A.deepEqual(after.map(x=>x.index),[128]);
A.deepEqual(after[0].source,before[0].source);
A.equal(before.length,3);A.equal(after.length,1);
A.deepEqual(removed.map(x=>x.oldIndex),[76,103,104,131]);
A.equal(proof.summary.paid_total,81);
const bytes=Buffer.from(JSON.stringify(proof)+'\n');
A.equal(hash(bytes),'85d353148d9e4ddc6f39f1d9666158665439fdab41f9e72ade6ae7ca56990562');
A.deepEqual(bytes,read(outFile));
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-596-')),cases=[];
function verify(name,obj,expected){
 const b=Buffer.from(JSON.stringify(obj)+'\n'),f=path.join(tmp,name+'.json');
 fs.writeFileSync(f,b);
 const p=cp.spawnSync(process.execPath,[ck,f],{encoding:'utf8',timeout:20000,maxBuffer:4000000});
 A.equal(p.status===0,expected,name+': '+p.stderr.slice(0,200));
 const o=p.status===0?JSON.parse(p.stdout):null;
 cases.push({name,verdict:expected?'ACCEPT':'REJECT',sha256:hash(b),bytes:b.length,
  assertions:o?.assertions??null,internal_negative_tests:o?.negativeTests??null});
}
try{
 verify('original_W85',initial,true);verify('quotient_W81',proof,true);
 const negatives=[
  ['bad_source',x=>x.records[0].c=[-x.spec.guard]],
  ['bad_pivot',x=>x.records.at(-1).pivot=9999],
  ['underpayment',x=>x.summary.paid_total--],
  ['unsupported_AND3',x=>x.records.at(-1).kind='AND3'],
  ['future_parent',x=>x.records.at(-1).parents[1]=x.records.length],
  ['invalid_gate_wire',x=>x.gate_defs[0][1]=x.spec.guard]
 ];
 negatives.forEach(([n,fn])=>{let x=copy(proof);fn(x);verify(n,x,false)});
 const fake=copy(proof);
 fake.records.at(-1).annotations={claimedSupports:before.map(x=>x.source)};
 verify('annotation_cannot_restore_provenance',fake,true);
 A.notDeepEqual(support(fake).map(x=>x.source),fake.records.at(-1).annotations.claimedSupports);
}finally{fs.rmSync(tmp,{recursive:true,force:true})}
const raw={id:'LSPV-2/596',scope:'Archived original /386 SOURCE/DEF/RES CLI only',
 status:'PROVED/RESTRICTED + COMPUTATIONAL',node:process.version,
 originalSha256:hash(read(inFile)),outputSha256:hash(bytes),
 before,after,removed,cases,
 totals:{accept:cases.filter(x=>x.verdict==='ACCEPT').length,
 reject:cases.filter(x=>x.verdict==='REJECT').length,
 assertionGroups:cases.reduce((s,x)=>s+(x.assertions||0),0)}};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(raw,null,2)+'\n');
console.log(JSON.stringify(raw.totals));
