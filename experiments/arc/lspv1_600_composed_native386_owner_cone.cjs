#!/usr/bin/env node
'use strict';
// LSPV-1/600, 2026-11-12 Pacific. Node 18+, standard library only.
// Execute: node experiments/arc/lspv1_600_composed_native386_owner_cone.cjs [raw-output.json]
// Uses unmodified archived /386 FULL CLI in separate Node OS processes.
// This is NOT an authentication of historical unified R_mix341.
const fs=require('node:fs'), path=require('node:path'), os=require('node:os');
const cp=require('node:child_process'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const pins={
 checker:['experiments/arc/lspv2_386_independent_verify.js','338305c0ce101704205e57543756b8127074a986'],
 seed:['results/raw/arc/580_LIVE_TWO_BRANCHES_W33.json','1879118e4e4f4244961f75f62e6207da67f0f345']
};
function gitBlob(b){return crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex')}
for(const [k,[f,sha]] of Object.entries(pins))assert.equal(gitBlob(fs.readFileSync(path.join(root,f))),sha,'Git blob '+k);
const seed=JSON.parse(fs.readFileSync(path.join(root,pins.seed[0]),'utf8'));
const clone=structuredClone;
const clauseKey=r=>JSON.stringify(r.c);
const canon=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function resolve(a,b,p){
 assert(a.includes(p)&&b.includes(-p),'signed resolution inputs');
 const c=canon([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
 assert(!c.some(x=>c.includes(-x)),'taut resolvent');return c;
}
function summary(d){
 const num=s=>d.records.filter(r=>r.kind===s).length;
 d.summary={source:num('SOURCE'),def_views:num('DEF'),resolution:num('RES'),
  paid_gates:d.gate_defs.length,paid_total:num('RES')+d.gate_defs.length,live_records:d.records.length};return d;
}
// 599's cost-nonincreasing signed-clause cache, followed by terminal-ancestor garbage collection.
function cacheCone(d){
 const rr=d.records,terminal=rr.length-1,mid=[],oldToMid=new Map(),memo=new Map();
 function push(i,r,parents=[]){const j=mid.length;mid.push({...r,parents});oldToMid.set(i,j);
  if(!memo.has(clauseKey(r)))memo.set(clauseKey(r),j)}
 for(let i=0;i<rr.length;i++)if(rr[i].kind==='SOURCE')push(i,rr[i]);
 for(let i=0;i<rr.length;i++)if(rr[i].kind==='DEF'){
  if(memo.has(clauseKey(rr[i])))oldToMid.set(i,memo.get(clauseKey(rr[i])));
  else push(i,rr[i]);
 }
 for(let i=0;i<rr.length;i++)if(rr[i].kind==='RES'){
  const r=rr[i];
  if(i!==terminal&&memo.has(clauseKey(r))){oldToMid.set(i,memo.get(clauseKey(r)));continue}
  const parents=r.parents.map(p=>{assert(oldToMid.has(p),'parent remapping');return oldToMid.get(p)});
  assert(parents.every(j=>j<mid.length));push(i,r,parents);
 }
 const live=new Set();function visit(i){if(live.has(i))return;live.add(i);for(const p of mid[i].parents)visit(p)}
 visit(oldToMid.get(terminal));
 const out=[],rename=new Map();
 for(let i=0;i<mid.length;i++)if(mid[i].kind==='SOURCE'||live.has(i)){
  assert(mid[i].parents.every(j=>rename.has(j)));
  rename.set(i,out.length);out.push({...mid[i],parents:mid[i].parents.map(j=>rename.get(j))});
 }
 return summary({spec:clone(d.spec),gate_defs:clone(d.gate_defs),records:out});
}
// 590's dependency-closed unused-owner pruning, with a paid CLI sentinel if none is used.
function ownerCone(d){
 const out=clone(d),byId=new Map(out.gate_defs.map(g=>[g[0],g]));
 const byWire=new Map(out.gate_defs.map(g=>[g[1],g]));
 const need=new Set();
 function add(g){assert(g);if(need.has(g[0]))return;need.add(g[0]);
  for(const x of [g[2],g[3]]){const parent=byWire.get(Math.abs(x));if(parent)add(parent)}
 }
 for(const r of out.records){
  if(r.kind==='DEF')add(byId.get(r.gate));
  for(const x of r.c){const owner=byWire.get(Math.abs(x));if(owner)add(owner)}
 }
 if(need.size===0){assert(out.gate_defs.length>0);need.add(out.gate_defs[0][0])}
 out.gate_defs=out.gate_defs.filter(g=>need.has(g[0]));
 return summary(out);
}
function composite(d){return ownerCone(cacheCone(d))}
function addOwners(d,k){
 assert(k>=1&&k<=20);const out=clone(d);
 out.gate_defs=[[0,8,1,4]];
 const inserted=[];
 for(let j=1;j<k;j++){
  out.gate_defs.push([j,8+j,7+j,2]);
  inserted.push({kind:'DEF',gate:j,c:canon([-(8+j),7+j]),parents:[]});
 }
 // Prefix has the 17 SOURCE + 3 DEF facets in the pinned W33 original.
 const before=out.records.slice(0,20),after=out.records.slice(20);
 const shift=inserted.length;
 out.records=[...before,...inserted,...after.map(r=>r.kind==='RES'?{...r,parents:r.parents.map(p=>p>=20?p+shift:p)}:r)];
 return summary(out);
}
// Genuine terminal-live fresh AND2 alias z=x1 AND x1. It adds two free
// owner-correct DEF facets and replaces one signed x1 resolution with THREE
// real paid RES nodes, sharing the same conclusion and all later ancestry.
function liveAliasDetour(k){
 const base=cacheCone(seed);assert.equal(base.summary.paid_total,29);
 assert(base.records.slice(0,17).every(r=>r.kind==='SOURCE'));
 assert(base.records.slice(17).every(r=>r.kind==='RES'));
 const out=clone(base),first=17,alias=8;
 out.gate_defs=[[0,alias,1,1]];
 for(let j=1;j<k;j++)out.gate_defs.push([j,8+j,7+j,2]);
 const facetPositive={kind:'DEF',gate:0,c:[-1,8],parents:[]};
 const facetNegative={kind:'DEF',gate:0,c:[1,-8],parents:[]};
 const prefix=out.records.slice(0,17),rr=[...prefix,facetPositive,facetNegative];
 for(let j=1;j<k;j++)rr.push({kind:'DEF',gate:j,c:canon([7+j,-(8+j)]),parents:[]});
 const fplus=17,fminus=18,oldToNew=new Map(prefix.map((_,i)=>[i,i]));
 for(let i=17;i<out.records.length;i++){
  const r=out.records[i],parents=r.parents.map(j=>{assert(oldToNew.has(j));return oldToNew.get(j)});
  if(i===first){
   assert.equal(r.pivot,1);assert.equal(parents.length,2);
   const A=rr[parents[0]].c,B=rr[parents[1]].c;
   const A1=resolve(A,rr[fplus].c,1),B1=resolve(rr[fminus].c,B,1);
   const pA=rr.length;rr.push({kind:'RES',c:A1,parents:[parents[0],fplus],pivot:1});
   const pB=rr.length;rr.push({kind:'RES',c:B1,parents:[fminus,parents[1]],pivot:1});
   const result=resolve(A1,B1,alias);assert.deepEqual(result,r.c);
   oldToNew.set(i,rr.length);rr.push({kind:'RES',c:result,parents:[pA,pB],pivot:alias});
  }else{oldToNew.set(i,rr.length);rr.push({...r,parents})}
 }
 out.records=rr;return summary(out);
}
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv1-600-'));
const checker=path.join(root,pins.checker[0]);
function native(d,expect,label){
 const f=path.join(temp,'packet.json'),b=Buffer.from(JSON.stringify(d)+'\n');fs.writeFileSync(f,b);
 const p=cp.spawnSync(process.execPath,[checker,f],{encoding:'utf8',maxBuffer:16*1024*1024,timeout:20000});
 if(p.error)throw p.error;const ok=p.status===0;
 assert.equal(ok,expect,label+' '+String(p.stderr).slice(0,300));
 const obj=ok?JSON.parse(p.stdout):null;
 if(ok){assert.equal(obj.paid,d.summary.paid_total);assert.equal(obj.negativeTests,11)}
 return {accepted:ok,logical_work:d.summary.paid_total,owners:d.gate_defs.length,
  res:d.summary.resolution,def_facets:d.summary.def_views,records:d.records.length,
  sha256:crypto.createHash('sha256').update(b).digest('hex'),bytes:b.length,
  assertions:obj?.assertions??null,error:ok?null:String(p.stderr).slice(0,160)};
}
const results=[],hostiles=[];
try{
 for(const type of ['cached_source','live_alias'])for(const k of [1,2,3,5,8,12]){
  const start=type==='cached_source'?addOwners(seed,k):liveAliasDetour(k);
  const n=cacheCone(start),u=ownerCone(n),again=composite(u);
  assert.deepEqual(u,again,'composite idempotence '+type+' '+k);
  assert.deepEqual(start.records.filter(x=>x.kind==='SOURCE'),u.records.filter(x=>x.kind==='SOURCE'));
  assert.deepEqual(start.records.at(-1).c,u.records.at(-1).c);
  const stage0=native(start,true,type+'-'+k+' original');
  const stage1=native(n,true,type+'-'+k+' cache');
  const stage2=native(u,true,type+'-'+k+' composite');
  const stage3=native(again,true,type+'-'+k+' idempotent');
  assert(stage0.logical_work>=stage1.logical_work&&stage1.logical_work>=stage2.logical_work);
  assert.equal(stage2.logical_work,type==='cached_source'?29:31);
  if(type==='cached_source')assert.equal(stage2.owners,1);
  else{assert.equal(stage2.owners,1);assert(u.records.some(r=>r.kind==='DEF'&&r.gate===0));
   assert(u.records.some(r=>r.kind==='RES'&&r.pivot===8));}
  results.push({type,k,stages:[stage0,stage1,stage2,stage3]});
 }
 const orig=liveAliasDetour(3),minimal=composite(orig);
 const cases=[
  ['remove_required_owner',d=>{d.gate_defs=[];summary(d)}],
  ['change_required_facet',d=>{d.records.find(r=>r.kind==='DEF').c=[1,8]}],
  ['corrupt_signed_source',d=>{d.records[0].c=[-1,2,3,-7]}],
  ['underpay_owner',d=>{d.summary.paid_total--}],
  ['bad_owner_forward_dependency',d=>{d.gate_defs=[[0,8,9,1],[1,9,1,2]];summary(d)}],
  ['wrong_terminal_pivot',d=>{d.records.at(-1).pivot=999999}]
 ];
 for(const [name,mut] of cases){const d=clone(minimal);mut(d);
  hostiles.push({name,run:native(d,false,name)})}
}finally{fs.rmSync(temp,{recursive:true,force:true})}
const raw={id:'LSPV-1/600',date:'2026-11-12 13:00 PST',status:'PROVED/RESTRICTED + ORIGINAL OS COMPUTATIONAL',
  checker_git_blob:pins.checker[1],seed_git_blob:pins.seed[1],node:process.version,
  theorem:'Cache+cone then dependency-closed paid-owner pruning preserves full /386 CLI, exact source and terminal; idempotent, never increases paid work',
  complete_cli_positive_runs:results.length*4,complete_cli_negative_runs:hostiles.length,
  builtin_corruption_controls:results.length*4*11,
  positive_assertion_groups:results.reduce((s,x)=>s+x.stages.reduce((a,b)=>a+b.assertions,0),0),
  results,hostiles,open:['P2-D1','P2-C3','P2-B1','P2-B2','P2-B3'],P_vs_NP:'OPEN',
  caveat:'Only pinned archived SOURCE/DEF/strict-RES /386 checker; not unified R_mix341 or a global proof optimum'};
const file=process.argv[2];if(file)fs.writeFileSync(path.resolve(file),JSON.stringify(raw,null,2)+'\n');
console.log(JSON.stringify({id:raw.id,positive:raw.complete_cli_positive_runs,negative:raw.complete_cli_negative_runs,
  builtin:raw.builtin_corruption_controls,assertions:raw.positive_assertion_groups,
  examples:results.filter(x=>x.k===1||x.k===12).map(x=>({type:x.type,k:x.k,costs:x.stages.map(y=>y.logical_work),owners:x.stages.map(y=>y.owners)})),
  hostiles:hostiles.map(x=>x.name),rawfile:file},null,2));
