#!/usr/bin/env node
'use strict';
// LSPV-1/599 2026-11-12 12:02 PST. Node >=18; no dependencies.
// Run from any directory: node experiments/arc/lspv1_599_native386_clause_cache_normal_form.cjs [output.json]
// Unmodified ORIGINAL /386 checker is executed in separate OS processes.
// NOT a verifier for the missing full historical R_mix341.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const cp=require('node:child_process'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const pins={
 checker:['experiments/arc/lspv2_386_independent_verify.js','338305c0ce101704205e57543756b8127074a986'],
 w33:['results/raw/arc/580_LIVE_TWO_BRANCHES_W33.json','1879118e4e4f4244961f75f62e6207da67f0f345'],
 w31:['results/raw/arc/580_DEF_THEN_RES_W31.json','6b2c343ab68634767b87bf0f7bce771529cb0c41'],
 w29:['results/raw/arc/2026-11-12_0424_LSPV3_587_NATIVE_CONSTANT_FACET_ACCEPTED_PACKET.json','4177ec15a0c7253378d5652a6b13b7152601d300'],
 w44:['results/raw/arc/2026-11-12_1100_LSPV1_597_NATIVE386_LIVE16_W44_ACCEPTED.json','a9514ed6d28d19403d745a583c3096d36cd1a399']
};
function gitBlob(b){return crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex')}
for(const [tag,[p,sha]] of Object.entries(pins))
 assert.equal(gitBlob(fs.readFileSync(path.join(root,p))),sha,'pin '+tag);
function normalize(d){
 assert(Array.isArray(d.records)&&d.records.at(-1).kind==='RES');
 const rows=d.records,rootOld=rows.length-1,mid=[],oldToMid=new Map(),byClause=new Map();
 const key=r=>JSON.stringify(r.c);
 function push(i,r){
  const j=mid.length;mid.push({...r,parents:[]});oldToMid.set(i,j);
  if(!byClause.has(key(r)))byClause.set(key(r),j);
 }
 // Every SOURCE remains, but free, zero-parent facets can precede every RES.
 for(let i=0;i<rows.length;i++)if(rows[i].kind==='SOURCE')push(i,rows[i]);
 for(let i=0;i<rows.length;i++)if(rows[i].kind==='DEF'){
  if(byClause.has(key(rows[i])))oldToMid.set(i,byClause.get(key(rows[i])));
  else push(i,rows[i]);
 }
 for(let i=0;i<rows.length;i++)if(rows[i].kind==='RES'){
  const r=rows[i];
  if(i!==rootOld&&byClause.has(key(r))){oldToMid.set(i,byClause.get(key(r)));continue}
  const parents=r.parents.map(j=>{assert(oldToMid.has(j));return oldToMid.get(j)});
  assert(parents.every(j=>j<mid.length));
  const j=mid.length;mid.push({...r,parents});oldToMid.set(i,j);
  if(!byClause.has(key(r)))byClause.set(key(r),j);
 }
 // Delete dead RES/DEF, never mandatory SOURCE, and lock original terminal RES.
 const live=new Set();
 function visit(i){if(live.has(i))return;live.add(i);for(const p of mid[i].parents)visit(p)}
 visit(oldToMid.get(rootOld));
 const out=[],rename=new Map();
 for(let i=0;i<mid.length;i++)if(mid[i].kind==='SOURCE'||live.has(i)){
  assert(mid[i].parents.every(j=>rename.has(j)));
  rename.set(i,out.length);out.push({...mid[i],parents:mid[i].parents.map(j=>rename.get(j))});
 }
 const count=kind=>out.filter(r=>r.kind===kind).length;
 return {spec:structuredClone(d.spec),gate_defs:structuredClone(d.gate_defs),records:out,
  summary:{source:count('SOURCE'),def_views:count('DEF'),resolution:count('RES'),
    paid_gates:d.gate_defs.length,paid_total:count('RES')+d.gate_defs.length,
    live_records:out.length}};
}
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv1-599-'));
function native(d,accept,label){
 const file=path.join(temp,'packet.json');fs.writeFileSync(file,JSON.stringify(d)+'\n');
 const r=cp.spawnSync(process.execPath,[path.join(root,pins.checker[0]),file],
   {encoding:'utf8',timeout:30000,maxBuffer:16*1024*1024});
 if(r.error)throw r.error;
 assert.equal(r.status===0,accept,label+': '+String(r.stderr).slice(-400));
 return accept?JSON.parse(r.stdout):{error:String(r.stderr).slice(-300)};
}
const cases=[],hostiles=[];
try{
 let w33norm;
 for(const tag of ['w33','w31','w29','w44']){
  const d=JSON.parse(fs.readFileSync(path.join(root,pins[tag][0]),'utf8'));
  const n=normalize(d);
  assert.deepEqual(normalize(n),n,'idempotence');
  assert.deepEqual(d.records.filter(x=>x.kind==='SOURCE'),n.records.filter(x=>x.kind==='SOURCE'));
  assert.deepEqual(d.records.at(-1).c,n.records.at(-1).c);
  assert(n.summary.paid_total<=d.summary.paid_total);
  const a=native(d,true,tag+' original'),b=native(n,true,tag+' normal'),c=native(normalize(n),true,tag+' idempotent');
  assert.equal(a.paid,d.summary.paid_total);assert.equal(b.paid,n.summary.paid_total);
  assert.equal(c.paid,n.summary.paid_total);assert.equal(a.negativeTests,11);
  const anc=new Set();function visit(i){if(anc.has(i))return;anc.add(i);for(const p of n.records[i].parents)visit(p)}
  visit(n.records.length-1);
  assert(n.records.every((r,i)=>r.kind!=='RES'||anc.has(i)),'all paid RES terminal-live');
  cases.push({tag,blob:pins[tag][1],paid_before:a.paid,paid_after:b.paid,
   records_before:d.records.length,records_after:n.records.length,
   RES_before:d.summary.resolution,RES_after:n.summary.resolution,
   DEF_before:d.summary.def_views,DEF_after:n.summary.def_views,
   original_assertions:a.assertions,normalized_assertions:b.assertions,
   idempotent_assertions:c.assertions});
  if(tag==='w33')w33norm=n;
 }
 const bad=[
  ['forged_source',o=>o.records[0].c=[-o.spec.guard]],
  ['undercharge',o=>o.summary.paid_total--],
  ['wrong_pivot',o=>o.records.at(-1).pivot=1],
  ['forward_parent',o=>o.records.at(-1).parents[0]=o.records.length+1],
  ['invalid_gate_input',o=>o.gate_defs[0][2]=o.spec.guard]];
 for(const [name,mut] of bad){
  const o=structuredClone(w33norm);mut(o);const x=native(o,false,name);
  hostiles.push({name,rejected:true,error:x.error});
 }
}finally{fs.rmSync(temp,{recursive:true,force:true})}
const result={id:'LSPV-1/599',model:'Original /386 full CLI, OS Node subprocesses',
 proof_status:'PROVED/RESTRICTED plus COMPUTATIONAL',checker_blob:pins.checker[1],
 positive_cases:cases.length*3,
 positive_assertions:cases.reduce((s,r)=>s+r.original_assertions+r.normalized_assertions+r.idempotent_assertions,0),
 negative_cases:hostiles.length,cases,hostiles,
 scope:'Only SOURCE/DEF/RES sibling; full historical R_mix341 OPEN',
 open:['P2-D1','P2-C3','P2-B1','P2-B2','P2-B3'],P_vs_NP:'OPEN'};
if(process.argv[2])fs.writeFileSync(path.resolve(process.argv[2]),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
