#!/usr/bin/env node
'use strict';
// LSPV-2/583; REFERENCE reverse-realization compiler, not authoritative R_mix341 or /386 checker.
// node experiments/arc/lspv2_582_native386_costsound_compact.cjs [repoRoot] [output.json]
const fs=require('fs'),path=require('path'),cp=require('child_process'),os=require('os'),cr=require('crypto'),assert=require('assert/strict');
const root=path.resolve(process.argv[2]||'.'),base='results/raw/arc/';
const names={seed:base+'2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json',structural:base+'2026-11-12_1212_LSPV2_581_ACCEPTED_K16_SYNTACTIC_W61.json',expanded:base+'2026-11-12_1212_LSPV2_581_ACCEPTED_K16_LIVE_W93.json'};
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js'),src=fs.readFileSync(path.join(root,base+'574_k01_SIGNED_SOURCE.cnf'));
const sha=b=>cr.createHash('sha256').update(b).digest('hex');
assert.equal(sha(fs.readFileSync(checker)),'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113');
assert.equal(sha(src),'3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c');
function native(obj){const f=path.join(os.tmpdir(),'pnp583_'+process.pid+'_'+(++native.i)+'.json');fs.writeFileSync(f,typeof obj==='string'?obj:JSON.stringify(obj));const r=cp.spawnSync(process.execPath,[checker,f],{encoding:'utf8',timeout:25000});fs.unlinkSync(f);return {accept:r.status===0,exit:r.status,assertions:r.status===0?JSON.parse(r.stdout).assertions:null,error:r.status===0?null:r.stderr.slice(0,160)};}native.i=0;
function norm(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}

function externalClauses(){const t=src.toString('utf8').trim().split(/\s+/);assert.equal(t[0],'p');assert.equal(t[1],'cnf');const n=Number(t[2]),m=Number(t[3]);const cs=[];let r=[];for(const token of t.slice(4)){const v=Number(token);assert(Number.isSafeInteger(v));if(v===0){cs.push(norm(r));r=[];}else{assert(Math.abs(v)<=n);r.push(v);}}assert.equal(r.length,0);assert.equal(cs.length,m);return cs.map(JSON.stringify).sort();}
function alpha(data){assert.deepEqual(data.records.filter(r=>r.kind==='SOURCE').map(r=>JSON.stringify(norm(r.c))).sort(),externalClauses(),'external signed SOURCE mismatch');let seen=new Set(),paid=0,paidFirst=0,duplicate=0,views=0,sources=0,depth=[];const trace=[];
 for(let i=0;i<data.records.length;i++){const r=data.records[i],k=JSON.stringify(r.c);assert(r.parents.every(p=>p<i&&p>=0));if(r.kind==='RES'){
 assert.equal(r.parents.length,2);const [A,B]=r.parents.map(p=>data.records[p].c);assert(A.includes(r.pivot)&&B.includes(-r.pivot));assert.deepEqual(norm([...A.filter(x=>x!==r.pivot),...B.filter(x=>x!==-r.pivot)]),r.c);}
 const newClause=!seen.has(k);seen.add(k);if(r.kind==='RES'){paid++;paidFirst+=Number(newClause);duplicate+=Number(!newClause);}else if(r.kind==='DEF')views++;else if(r.kind==='SOURCE')sources++;else throw Error('unrecognised opcode');
 depth[i]=r.kind==='RES'?1+Math.max(...r.parents.map(p=>depth[p])):0;trace.push({i,rule:r.kind,ports:r.parents,clause:r.c,scope:'ROOT',paidDelta:r.kind==='RES'?1:0,abstractDelta:r.kind==='RES'&&newClause?1:0});}
 assert.deepEqual(data.records.at(-1).c,[]);assert.equal(data.summary.paid_total,paid+data.gate_defs.length);assert(trace.every(x=>x.abstractDelta<=x.paidDelta));return {sourceSHA256:sha(src),sourceOccurrences:sources,paidOwners:data.gate_defs.length,freeFacets:views,RES:paid,duplicateRES:duplicate,concreteWork:paid+data.gate_defs.length,abstractWork:paidFirst+data.gate_defs.length,span:Math.max(...depth),terminal:true,scope:'ROOT',traceSHA256:sha(JSON.stringify(trace))};}

// In the archived /386 fragment ONLY, every conservative owner is global and
// every RES port depends solely on its signed parent clause values.
function facets(z,a,b){return [[-z,a],[-z,b],[z,-a,-b]].map(norm).filter(c=>!c.some(x=>c.includes(-x)));}
function reverseLift(p){
 assert(Array.isArray(p.records));assert(p.gate_defs.length>0,'CLI owner sentinel');
 assert.equal(p.records.at(-1).kind,'RES');
 assert.deepEqual(p.records.at(-1).c,[]);
 assert.notEqual(p.records.at(-1).pivot,999999,'CLI pivot sentinel');
 assert.deepEqual(p.records.filter(r=>r.kind==='SOURCE').map(r=>JSON.stringify(r.c)).sort(),externalClauses());
 const rec=[],first=new Map();
 function add(r){const i=rec.length;rec.push(r);if(!first.has(JSON.stringify(r.c)))first.set(JSON.stringify(r.c),i);return i;}
 for(const r of p.records.filter(r=>r.kind==='SOURCE'))add(structuredClone(r));
 for(const [gate,z,a,b] of p.gate_defs)for(const c of facets(z,a,b)){
  if(!first.has(JSON.stringify(c)))add({kind:'DEF',c,parents:[],gate});
 }
 const prep=rec.length;
 let reused=0;
 for(let i=0;i<p.records.length;i++){
  const r=p.records[i];if(r.kind==='SOURCE'||r.kind==='DEF')continue;
  assert.equal(r.kind,'RES');
  const final=i===p.records.length-1;
  if(!final&&first.has(JSON.stringify(r.c))){reused++;continue;}
  const ports=r.parents.map(j=>{
   assert(j<i);const index=first.get(JSON.stringify(p.records[j].c));
   assert.notEqual(index,undefined,'known signed parent value missing');
   return index;
  });
  const [A,B]=ports.map(j=>rec[j].c),v=r.pivot;
  assert(A.includes(v)&&B.includes(-v),'signed pivot');
  assert.deepEqual(norm([...A.filter(x=>x!==v),...B.filter(x=>x!==-v)]),r.c,'strict resolvent');
  add({kind:'RES',c:[...r.c],parents:ports,pivot:v});
 }
 const live=new Set(),q=[rec.length-1];
 while(q.length){const i=q.pop();if(live.has(i))continue;live.add(i);q.push(...rec[i].parents);}
 const keep=rec.map((r,i)=>({r,i})).filter(({r,i})=>r.kind==='SOURCE'||live.has(i));
 const renum=new Map(keep.map(({i},j)=>[i,j]));
 const records=keep.map(({r})=>({...r,parents:r.parents.map(j=>{assert(renum.has(j));return renum.get(j);})}));
 const counts={source:records.filter(r=>r.kind==='SOURCE').length,def_views:records.filter(r=>r.kind==='DEF').length,
 resolution:records.filter(r=>r.kind==='RES').length,paid_gates:p.gate_defs.length};
 const out={spec:structuredClone(p.spec),gate_defs:structuredClone(p.gate_defs),records};
 out.summary={...counts,paid_total:counts.resolution+counts.paid_gates,live_records:records.length};
 assert(out.summary.paid_total<=p.summary.paid_total);
 return {out,reused,preloaded:prep-counts.source,retainedViews:counts.def_views};
}
const cases=[],negative=[];
const all={...names};
for(let i=4;i<process.argv.length;i++)all['extra'+(i-3)]=process.argv[i];
for(const [label,filename] of Object.entries(all)){
 const bytes=fs.readFileSync(path.isAbsolute(filename)?filename:path.join(root,filename));
 const p=JSON.parse(bytes),before=native(bytes.toString());
 assert(before.accept,label+': original CLI rejected '+before.error);
 const {out,reused,preloaded,retainedViews}=reverseLift(p);
 const after=native(out);assert(after.accept,label+': lifted CLI rejected '+after.error);
 const again=reverseLift(out).out;assert.deepEqual(out,again,'compiler not idempotent');
 cases.push({label,sourceSHA256:sha(src),inputSHA256:sha(bytes),inputWork:p.summary.paid_total,
 outputWork:out.summary.paid_total,inputRecords:p.records.length,outputRecords:out.records.length,
 inputBytes:bytes.length,outputBytes:Buffer.byteLength(JSON.stringify(out)),
 outputSHA256:sha(JSON.stringify(out)),reused,preloaded,retainedViews,
 originalAssertions:before.assertions,outputAssertions:after.assertions});
}
const baselineProof=reverseLift(JSON.parse(fs.readFileSync(path.join(root,names.seed)))).out;
const mutations=[
 ['forged_source',d=>d.records[0].c=[-d.spec.guard]],
 ['underpayment',d=>d.summary.paid_total--],
 ['terminal_pivot_sentinel',d=>d.records.at(-1).pivot=999999],
 ['ownerless',d=>{d.gate_defs=[];d.summary.paid_gates=0;d.summary.paid_total=d.summary.resolution;}],
 ['false_owner_facet',d=>{Object.assign(d,JSON.parse(fs.readFileSync(path.join(root,names.expanded))));const f=d.records.find(r=>r.kind==='DEF');assert(f);f.c=[123456];}],
 ...['AND3','XOR','LOCAL-CONVERT','SPLIT','WEAKEN','DISCHARGE','JOIN','DELETE','GF(2)'].map(kind=>['unknown_'+kind,d=>d.records.at(-1).kind=kind])
];
for(const [label,f] of mutations){const d=structuredClone(baselineProof);f(d);const verdict=native(d);assert(!verdict.accept,'unsupported /386 hostile accepted: '+label);negative.push({label,accepted:verdict.accept,error:verdict.error});}
const result={id:'LSPV-2/583',status:'COMPUTATIONAL original OS + PROVED/RESTRICTED reverse serialization',
 scope:'archived /386 global-AND2-owner / ROOT signed SOURCE-DEF-RES; NOT full R_mix341',
 checkerSHA256:sha(fs.readFileSync(checker)),sourceSHA256:sha(src),
 cases,negative,positiveNativeAccepts:cases.length*2,negativeNativeRejects:negative.length,
 open:['P2-D1','P2-C3','P2-B1','P2-B2','P2-B3','P versus NP'],
 tracker:'TRACKERS REVIEWED; NO MATERIAL CHANGE'};
if(process.argv[3])fs.writeFileSync(process.argv[3],JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({positiveNativeAccepts:result.positiveNativeAccepts,
 negativeNativeRejects:result.negativeNativeRejects,
 work:cases.map(x=>[x.label,x.inputWork,x.outputWork])}));
