#!/usr/bin/env node
'use strict';
/*
 LSPV-3/563: archived /386 original-checker nested DEF-facet/RES proof corpus.
 Run from complete j15marti/pnp checkout:
 node experiments/arc/lspv3_563_nested_386_owner_chain.cjs [raw-output.json]
 Node >=18. Not the missing complete R_mix341 parser.
*/
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),
cp=require('node:child_process'),crypto=require('node:crypto'),
assert=require('node:assert/strict');
const repo=path.resolve(__dirname,'../..');
const checker=path.join(repo,'experiments/arc/lspv2_386_independent_verify.js');
const baseFile=path.join(repo,'results/raw/arc/2026-11-10_2124_LSPV3_561_ARCHIVED_386_NATIVE_PACKET.json');
const pinned={checker:'338305c0ce101704205e57543756b8127074a986',
 base:'d0fa96a155672f8f6a6a3428eacafa15e79b9e88'};
const clone=x=>JSON.parse(JSON.stringify(x));
function gitBlob(b){return crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex')}
assert.equal(gitBlob(fs.readFileSync(checker)),pinned.checker);
assert.equal(gitBlob(fs.readFileSync(baseFile)),pinned.base);
const base=JSON.parse(fs.readFileSync(baseFile,'utf8'));
assert.deepEqual(base.gate_defs,[[0,8,1,2]]);
assert.equal(base.records.length,69);
function extend(obj){
 const p=clone(obj),old=p.records;
 const map=i=>i<20?i:i===20?23:i===21?26:i+5;
 const rebase=r=>({...clone(r),parents:r.parents.map(map)});
 p.gate_defs.push([1,9,8,-3]);
 p.records=[
  ...old.slice(0,20).map(rebase),
  {kind:'DEF',c:[8,-9],parents:[],gate:1},
  {kind:'DEF',c:[-3,-9],parents:[],gate:1},
  {kind:'DEF',c:[3,-8,9],parents:[],gate:1},
  rebase(old[20]),
  {kind:'RES',c:[-2,3,-7,-9],parents:[20,23],pivot:8},
  {kind:'RES',c:[-2,3,-7,-8],parents:[22,24],pivot:9},
  rebase(old[21]),
  ...old.slice(22).map(rebase)
 ];
 p.records[26].parents=[19,25];
 p.summary={source:17,def_views:6,resolution:51,paid_gates:2,paid_total:53,live_records:74};
 return p;
}
const packet=extend(base);
assert.equal(Buffer.byteLength(JSON.stringify(packet)),4421);
assert.deepEqual(packet.records.filter(r=>r.kind==='SOURCE'),
 base.records.filter(r=>r.kind==='SOURCE'));
assert.deepEqual(packet.records[26].c,base.records[21].c);
function rename(p){
 const q=clone(p);q.gate_defs[1][1]=10;
 for(const r of q.records){
  r.c=r.c.map(x=>Math.abs(x)===9?Math.sign(x)*10:x)
   .sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
  if(r.pivot===9)r.pivot=10;
 }
 return q;
}
function analyze(p){
 const seen=new Set();
 function visit(i){if(seen.has(i))return;seen.add(i);
  for(const j of p.records[i].parents)visit(j);}
 visit(p.records.length-1);
 const owners=new Map(p.gate_defs.map(([id,z,a,b])=>[id,{z,a,b}]));
 const active=new Set([...seen].filter(i=>p.records[i].kind==='DEF').map(i=>p.records[i].gate));
 function close(id){
  const def=owners.get(id);assert(def);
  for(const x of [def.a,def.b])for(const [k,d] of owners)
   if(Math.abs(x)===d.z&&!active.has(k)){active.add(k);close(k);}
 }
 for(const id of Array.from(active))close(id);
 const source=p.records.filter(r=>r.kind==='SOURCE').map(r=>r.c);
 let models=0;
 for(let a=0;a<128;a++)
  if(source.every(c=>c.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0))))models++;
 const depths=[];
 for(const r of p.records)depths.push(r.parents.length?
  1+Math.max(...r.parents.map(j=>depths[j])):0);
 return {sources:source.length,modelsOnSevenVariables:models,
  reachableRecords:seen.size,
  reachableSources:[...seen].filter(i=>p.records[i].kind==='SOURCE').length,
  reachableFacets:[...seen].filter(i=>p.records[i].kind==='DEF').sort((a,b)=>a-b),
  reachableOwnerClosure:[...active].sort(),
  allDetourNodesReachable:[20,22,23,24,25,26].every(i=>seen.has(i)),
  longestResolutionParentChain:Math.max(...depths)};
}
const analysis=analyze(packet);
assert.equal(analysis.modelsOnSevenVariables,0);
assert.equal(analysis.reachableSources,17);
assert.deepEqual(analysis.reachableOwnerClosure,[0,1]);
assert(analysis.allDetourNodesReachable);
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-563-'));
function native(p,name){
 const data=Buffer.from(JSON.stringify(p)),f=path.join(temp,name+'.json');
 fs.writeFileSync(f,data);
 const r=cp.spawnSync(process.execPath,[checker,f],
  {encoding:'utf8',maxBuffer:8e6,timeout:30000});
 const accepted=r.status===0&&!r.error;
 const info=accepted?JSON.parse(r.stdout.trim()):null;
 return {name,accepted,bytes:data.length,
  sha256:crypto.createHash('sha256').update(data).digest('hex'),
  assertions:info?info.assertions:null,paid:info?info.paid:null,
  diagnostic:accepted?null:String(r.stderr||r.error||'rejected').slice(0,600)};
}
const mutations=[
 ['swapped_gate_order',p=>p.gate_defs.reverse()],
 ['wrong_signed_operand',p=>p.gate_defs[1][3]=3],
 ['duplicate_gate_output',p=>p.gate_defs[1][1]=8],
 ['duplicate_gate_owner',p=>p.gate_defs[1][0]=0],
 ['missing_nested_owner',p=>p.gate_defs.pop()],
 ['bad_nested_facet',p=>p.records[22].c=[-3,-8,9]],
 ['bad_nested_resolution',p=>p.records[24].c=[2,3,-7,-9]],
 ['wrong_nested_pivot',p=>p.records[25].pivot=8],
 ['forward_parent',p=>p.records[25].parents[1]=73],
 ['underpaid_nested_owner',p=>p.summary.paid_gates=1],
 ['underpaid_total',p=>p.summary.paid_total=52],
 ['original_source_mutated',p=>p.records[1].c=[1,-2,3,-7]],
 ['wrong_root',p=>p.records[73].c=[1]]
];
try{
 const accepts=[native(base,'base'),native(packet,'nested'),native(rename(packet),'renamed')];
 accepts.forEach(r=>assert(r.accepted,'expected original accept '+r.name));
 assert.equal(accepts[0].assertions,4492);
 assert.equal(accepts[1].assertions,4663);
 assert.equal(accepts[1].paid,53);
 const rejects=mutations.map(([name,mut])=>{const p=clone(packet);mut(p);return native(p,name)});
 rejects.forEach(r=>assert(!r.accepted,'unexpected original accept '+r.name));
 const output={run:'LSPV-3/563',status:'PROVED/RESTRICTED + COMPUTATIONAL',
  checkerExecution:'unchanged original /386 Node CLI, 11 built-in negative controls',
  fullHistoricalRmix341Authenticated:false,pinned,analysis,
  accepts,rejects,originalGuardedSourcesUntouched:true,
  paidLogicalWork:{baseline:50,new:53,resolution:51,owners:2,freeFacetViews:6},
  witnessBytes:JSON.stringify(packet).length,
  limitation:'No full /341 native mixed checker, no RES-to-AND3 port, no physical memory measurement.'};
 const target=process.argv[2]||path.join(repo,'results/raw/arc/2026-11-10_2324_LSPV3_563_NESTED_386_NODE_RAW.json');
 fs.mkdirSync(path.dirname(target),{recursive:true});
 fs.writeFileSync(target,JSON.stringify(output,null,2)+'\n');
 console.log(JSON.stringify({target,positives:accepts.length,negatives:rejects.length,
  cost:53,bytes:4421,sourceModels:0,sha256:accepts[1].sha256}));
}catch(e){console.error(e.stack||e);process.exitCode=1}
finally{fs.rmSync(temp,{recursive:true,force:true})}
