#!/usr/bin/env node
// LSPV-4/524. Original /341 checker V8 replay plus exact inference-DAG surplus audit.
// Usage: node experiments/arc/lspv4_524_fanout_surplus_audit.cjs
// Requires a local j15marti/pnp checkout; no third-party dependencies.
'use strict';
const fs=require('fs'), vm=require('vm'),crypto=require('crypto');
function assert(x,msg){if(!x)throw Error(msg);}
function gitSha(s){const b=Buffer.from(s);return crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');}
function audit(roots,steps,sink){
 const table=new Map(roots.map(id=>[id,{id,parents:[],weight:0}])),out=new Map(roots.map(id=>[id,0]));
 for(const p of steps){
  assert(!table.has(p.id),'duplicate ID');
  assert(p.parents.every(x=>table.has(x)),'invalid parent or order');
  assert(new Set(p.parents).size===p.parents.length,'duplicate parent');
  table.set(p.id,p);out.set(p.id,0);
  for(const x of p.parents)out.set(x,out.get(x)+1);
 }
 assert(table.has(sink),'missing sink');
 const seen=new Set([sink]),todo=[sink];
 while(todo.length)for(const x of table.get(todo.pop()).parents)if(!seen.has(x)){seen.add(x);todo.push(x);}
 assert(seen.size===table.size,'unreachable SOURCE or inference');
 const m=roots.length,q=steps.length;
 const fanout=[...out].filter(([id])=>id!==sink).reduce((a,[id,v])=>a+v-1,0);
 const penalty=steps.reduce((a,p)=>a+2-p.parents.length,0);
 assert(q-m+1===fanout+penalty,'surplus-budget identity');
 return {m,q,paidWork:steps.reduce((a,x)=>a+x.weight,0),fanout,penalty,
  paidShared:steps.filter(x=>out.get(x.id)>1).length};
}
function fake(id,parents,weight=1){return {id,parents,weight};}
const controls={
 tree:audit(['s0','s1','s2'],[fake('d0',['s0','s1']),fake('d1',['d0','s2'])],'d1'),
 shared:audit(['s0','s1','s2'],[fake('d0',['s0','s1']),fake('d1',['d0','s2']),fake('d2',['d0','d1'])],'d2'),
 free:audit(['s0','s1','s2'],[fake('z0',['s0','s1'],0),fake('d0',['z0','s2'])],'d0'),
 unary:audit(['s0','s1'],[fake('u0',['s0']),fake('d0',['u0','s1'])],'d0')
};
assert(controls.tree.fanout===0&&controls.shared.fanout===1&&controls.shared.paidShared===1,'fanout controls');
assert(controls.free.paidWork===1&&controls.free.m-1===2,'zero-cost firewall');
assert(controls.unary.penalty===1,'unary penalty');
const paths=['experiments/arc/lspv2_341_mixed_tseitin_min_dag.js',
 'experiments/arc/lspv2_341_independent_verify.js'];
const shas=['4081022e8a3841d79f751a3d3a7a10decbb026da',
 'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0'];
const src=paths.map((p,i)=>{let s=fs.readFileSync(p,'utf8');assert(gitSha(s)===shas[i],'pin mismatch '+p);return s;});
const producerLog=[];
vm.runInNewContext(src[0],{console:{log:s=>producerLog.push(s)}},{timeout:90000});
assert(producerLog.length===1,'producer log');
const data=JSON.parse(producerLog[0]),verifierLog=[];
vm.runInNewContext(src[1],{console:{log:s=>verifierLog.push(s)},
 require:name=>{assert(name==='fs','import');return {readFileSync:()=>JSON.stringify(data)};},
 process:{argv:['node','341','in-memory-original.json']}},{timeout:90000});
assert(verifierLog.length===1,'verifier log');
const result=JSON.parse(verifierLog[0]);
assert(result.checks===30714&&result.cases.length===7,'native checker regression');
const native=data.fixtures.map(f=>{
 const roots=f.clauses.map(c=>c.id);
 const steps=f.proof.map(p=>fake(p.id,p.parents));
 const a=audit(roots,steps,f.proof.at(-1).id);
 assert(a.q===a.m-1&&a.fanout===0&&a.penalty===0,'native saturated tree');
 const bytes=x=>Buffer.byteLength(JSON.stringify(x));
 return {...a,graph:f.graph.name,essential:f.properties.essential,
  fixtureBytes:bytes(f),proofBytes:bytes(f.proof),sourceClausesBytes:bytes(f.clauses),
  deletionWitnessBits:f.deleted.reduce((a,x)=>a+(x.assignment?.length||0),0),
  deletionJsonBytes:bytes(f.deleted)};
});
console.log(JSON.stringify({status:'COMPUTATIONAL/RESTRICTED',originalSourceBlobs:shas,
 originalCheckerAssertions:result.checks,controls,native},null,2));
