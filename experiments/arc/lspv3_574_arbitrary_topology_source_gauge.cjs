#!/usr/bin/env node
"use strict";
// LSPV-3/574. Original archived /386 checker, no new verifier or grammar.
// From j15marti/pnp root: node experiments/arc/lspv3_574_arbitrary_topology_source_gauge.cjs
const fs=require("node:fs"),path=require("node:path"),os=require("node:os");
const cp=require("node:child_process"),crypto=require("node:crypto"),assert=require("node:assert/strict");
const root=path.resolve(__dirname,"../..");
const checkerPath="experiments/arc/lspv2_386_independent_verify.js";
const seedPath="results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json";
const expectedBlobs={
 [checkerPath]:"338305c0ce101704205e57543756b8127074a986",
 [seedPath]:"08aa169b5db49b2ddd1cb5a9b6890fcc3b790916"
};
const clone=x=>JSON.parse(JSON.stringify(x));
const blob=t=>crypto.createHash("sha1").update("blob "+Buffer.byteLength(t)+"\0"+t).digest("hex");
for(const [p,digest] of Object.entries(expectedBlobs))assert.equal(blob(fs.readFileSync(path.join(root,p),"utf8")),digest,"original pinned blob mismatch: "+p);
const base=JSON.parse(fs.readFileSync(path.join(root,seedPath),"utf8"));
const L=base.records.length,E=base.spec.edges.length;
const masks=[0,11,21,30,38,45,51,56];
function canonical(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);}
function sign(lit,mask){return Math.abs(lit)<=E && (mask & (1<<(Math.abs(lit)-1))) ? -lit : lit;}
function reorder(p,indices){
 assert.equal(indices.length,p.records.length);
 assert.equal(new Set(indices).size,indices.length);
 const ni=new Map(indices.map((old,i)=>[old,i]));
 const q=clone(p);q.records=indices.map(old=>{
  const rec=clone(p.records[old]);rec.parents=rec.parents.map(x=>ni.get(x));return rec;
 });
 return q;
}
function sourceFirst(p){
 const sources=[],rest=[];
 p.records.forEach((r,i)=>(r.kind==="SOURCE"?sources:rest).push(i));
 return reorder(p,[...sources,...rest]);
}
function action(p,mask){
 const q=clone(p),swap=new Map();
 const t=c=>canonical(c.map(x=>sign(x,mask)));
 for(let i=0;i<p.records.length;i++){
  const r=p.records[i];if(r.kind!=="SOURCE")continue;
  const tc=JSON.stringify(t(r.c));
  const j=p.records.findIndex(s=>s.kind==="SOURCE" && s.source===r.source && JSON.stringify(s.c)===tc);
  if(j<0)throw Error("no same-source clause bijection for mask "+mask+" source "+i);
  swap.set(i,j);
 }
 assert.equal(new Set(swap.values()).size,swap.size,"nonbijective SOURCE map");
 q.gate_defs=q.gate_defs.map(([id,z,a,b])=>[id,z,sign(a,mask),sign(b,mask)]);
 q.records=q.records.map((r)=>{
  if(r.kind==="SOURCE")return clone(r);
  const x=clone(r);x.c=t(r.c);
  if(x.kind==="RES")x.pivot=sign(r.pivot,mask);
  x.parents=r.parents.map(j=>p.records[j].kind==="SOURCE"?swap.get(j):j);
  return x;
 });
 return q;
}
const temp=fs.mkdtempSync(path.join(os.tmpdir(),"lspv3_574_"));
function native(label,p){
 const filepath=path.join(temp,"input.json");
 fs.writeFileSync(filepath,JSON.stringify(p)+"\n");
 const r=cp.spawnSync(process.execPath,[path.join(root,checkerPath),filepath],{encoding:"utf8",timeout:25000,maxBuffer:4*1024*1024});
 let info={label,accepted:r.status===0 && !r.error,status:r.status,error:r.error?String(r.error):null,stderr:(r.stderr||"").slice(0,500)};
 if(info.accepted){const o=JSON.parse(r.stdout);info.paid=o.paid;info.assertions=o.assertions;info.negativeTests=o.negativeTests;info.sources=o.sources;info.res=o.res;info.def=o.def;}
 return info;
}
const witnessOrder=Array.from({length:L},(_,i)=>i).filter(i=>i!==0);
witnessOrder.splice(witnessOrder.indexOf(23)+1,0,0);
const interleaved=reorder(base,witnessOrder);
const naive=action(interleaved,11);
const normalized=sourceFirst(interleaved);
const repaired=action(normalized,11);
const outcomes=[];
function expect(label,p,accepted){
 const o=native(label,p);assert.equal(o.accepted,accepted,label+": "+o.stderr);
 outcomes.push(o);
}
try{
 expect("original seed",base,true);
 expect("legal interleaved SOURCE",interleaved,true);
 expect("naive unscheduled cycle action",naive,false);
 assert(naive.records[22].parents.includes(23),"expected forward parent at RES 22");
 expect("source-first normal form",normalized,true);
 expect("rescheduled cycle-11 action",repaired,true);
 assert.deepEqual(interleaved.records.filter(r=>r.kind==="SOURCE"),repaired.records.filter(r=>r.kind==="SOURCE"),"SOURCE record multiset/order changed");
 assert.equal(repaired.summary.paid_total,53);
 for(const mask of masks)expect("legal fixed-source cycle "+mask,action(normalized,mask),true);
 let composition=0;
 for(const x of masks)for(const y of masks){
  assert.deepEqual(action(action(normalized,x),y),action(normalized,x^y),"kernel composition failed");
  composition++;
 }
 const hostiles=[
  ["bad signed SOURCE",p=>p.records.find(r=>r.kind==="SOURCE").c[0]*=-1],
  ["bad parent pointer",p=>p.records.find(r=>r.kind==="RES").parents[0]=999],
  ["bad Resolution pivot",p=>p.records.find(r=>r.kind==="RES").pivot=999],
  ["underpaid logical work",p=>p.summary.paid_total--],
  ["bad defining facet",p=>p.records.find(r=>r.kind==="DEF").c[0]*=-1],
  ["reused paid wire",p=>p.gate_defs[1][1]=p.gate_defs[0][1]]
 ];
 for(const [name,mutate] of hostiles){const p=clone(repaired);mutate(p);expect(name,p,false);}
 const result={run:"LSPV3/574",date_pst:"2026-11-11 10:24 PST",engine:"original archived /386 as actual Node OS subprocess, not replacement checker",
  originalBlobs:expectedBlobs,sourceRecordRule:"keep each SOURCE object byte-for-byte after parsing, reorder whole records and reindex references",
  candidate:"all topological accepted /386 certificates admit fixed-source cycle action after source-first rescheduling",
  forbiddenNaive:"SOURCE 0 moved to new ordinal 23 while a RES at 22 references old SOURCE 1; mask11 source map requires parent 23 after current 22",
  masks,acceptedNativeMasks:masks.length,kernelCompositionChecks:composition,
  work:{resolution:51,paidGateOwners:2,freeFacetViews:6,total:53},
  positiveOriginalCheckerExecutions:outcomes.filter(x=>x.accepted).length,
  negativeOriginalCheckerExecutions:outcomes.filter(x=>!x.accepted).length,
  outcomes,limitations:"Full historical mixed R_mix341 and external original-CNF hash are not authenticated; no optimal W or SAT decision-time lower bound; OS wall/RSS are not machine-model resource bounds."};
 console.log(JSON.stringify(result,null,2));
 if(process.argv.includes("--write")){
  const dir=path.join(root,"results/raw/arc");
  for(const [name,p] of [["2026-11-11_1024_LSPV3_574_INTERLEAVED_NATIVE386_PACKET.json",interleaved],
     ["2026-11-11_1024_LSPV3_574_NAIVE_FORWARD_PARENT_REJECTED.json",naive],
     ["2026-11-11_1024_LSPV3_574_REPAIRED_SOURCE_FIXED_PACKET.json",repaired]]){
   fs.writeFileSync(path.join(dir,name),JSON.stringify(p)+"\n");
  }
  fs.writeFileSync(path.join(dir,"2026-11-11_1024_LSPV3_574_NATIVE386_RESCHEDULE_OS_RAW.json"),JSON.stringify(result,null,2)+"\n");
 }
}finally{fs.rmSync(temp,{recursive:true,force:true});}
