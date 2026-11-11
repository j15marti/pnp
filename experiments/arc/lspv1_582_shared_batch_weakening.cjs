#!/usr/bin/env node
'use strict';
// LSPV-1/582: exact four-clause shared-AND2-owner weakening original CLI replay.
// From the repository root: node experiments/arc/lspv1_582_shared_batch_weakening.cjs
const assert=require('node:assert/strict');
const fs=require('node:fs'),crypto=require('node:crypto'),path=require('node:path');
const os=require('node:os'),cp=require('node:child_process');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedFile=path.join(root,'results/raw/arc/2026-11-11_1200_LSPV1_579_BRIDGE_DP_W61.json');
const packetFile=path.join(root,'results/raw/arc/2026-11-11_1503_LSPV1_582_SHARED_OWNER_BATCH_WEAKENING_PACKET.json');
const blob=file=>{const b=fs.readFileSync(file);return crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');};
const clone=x=>JSON.parse(JSON.stringify(x));
const key=x=>[...new Set(x)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
assert.equal(blob(checker),'338305c0ce101704205e57543756b8127074a986');
assert.equal(blob(seedFile),'807aaf7b7cf5e4a4feb29c2599f9e582ea140e30');
assert.equal(blob(packetFile),'d3afbee95a49e528134dc036da482a6399297d6d');
const seed=JSON.parse(fs.readFileSync(seedFile,'utf8'));
function construct(){
 const p=clone(seed),sink=p.records.pop();
 p.gate_defs.push([1,18,1,3]); // fresh z = original literal x1 AND x3
 const positive=p.records.push({kind:'DEF',c:key([18,-1,-3]),parents:[],gate:1})-1;
 const negative=p.records.push({kind:'DEF',c:key([-18,1]),parents:[],gate:1})-1;
 assert.equal(positive,100);assert.equal(negative,101);
 const clauses=[0,3,13,14];const produced=[];
 for(const i of clauses){
  const c=p.records[i].c;
  assert(c.includes(1)&&!c.includes(3)&&!c.includes(-3));
  const k=p.records.push({kind:'RES',c:key([...c.filter(x=>x!==1),18,-3]),parents:[i,positive],pivot:1})-1;
  const j=p.records.push({kind:'RES',c:key([...c,-3]),parents:[k,negative],pivot:18})-1;
  produced.push(j);
 }
 p.records.push(sink);
 p.summary={source:41,resolution:68,def_views:2,paid_gates:2,paid_total:70,live_records:111};
 assert.deepEqual(produced,[103,105,107,109]);
 return p;
}
const packet=construct();
const exact=fs.readFileSync(packetFile,'utf8');
assert.equal(JSON.stringify(packet),exact,'published byte-exact packet changed');
assert.equal(Buffer.byteLength(exact),7160);
assert.deepEqual(packet.records.slice(0,41),seed.records.slice(0,41));
assert.deepEqual(packet.records.at(-1),seed.records.at(-1));
assert.equal(packet.summary.paid_total,70);
const observed=packet.records.slice(100,110),usedParents=new Set(observed.flatMap(r=>r.parents));
assert(usedParents.has(100)&&usedParents.has(101));
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv1-582-'));
function original(name,d,accept){
 const file=path.join(tmp,name+'.json');fs.writeFileSync(file,JSON.stringify(d));
 const r=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:30000});
 const ok=r.status===0;
 assert.equal(ok,accept,name+' original checker result: '+r.stderr.slice(-700));
 let outcome=null;
 if(ok){outcome=JSON.parse(r.stdout.trim().split('\n').at(-1));assert.equal(outcome.negativeTests,11);}
 return {name,expected:accept,accepted:ok,paid:outcome?.paid??null,assertions:outcome?.assertions??null,
         error:ok?null:r.stderr.trim().slice(-220)};
}
const tests=[
 ['seed_W61',seed,true],
 ['four_clause_shared_owner_W70',packet,true],
 ['underpaid_W69',q=>{q.summary.paid_total=69;},false],
 ['forged_facet',q=>{q.records[100].c=[-1,3,18];},false],
 ['reversed_second_pivot',q=>{q.records[104].pivot=-18;},false],
 ['owner_freshness_collision',q=>{q.gate_defs[1][1]=17;},false],
 ['wrong_second_resolvent',q=>{q.records[109].c=[1,-3,4,6,-16];},false],
 ['future_parent',q=>{q.records[106].parents[1]=110;},false],
 ['tampered_original_source',q=>{q.records[13].c=[1,4,6,-16];},false],
 ['wrong_facet_owner',q=>{q.records[100].gate=99;},false],
 ['missing_facet',q=>{q.records.splice(101,1);},false],
 ['changed_guard',q=>{q.spec.guard=18;},false]
];
try{
 const results=tests.map(([name,m,expected])=>{const d=typeof m==='function'?clone(packet):m;if(typeof m==='function')m(d);return original(name,d,expected);});
 let sat=0;const spec=packet.spec;
 for(let mask=0;mask<(1<<spec.edges.length);mask++){
  const xor=Array(spec.h).fill(0);
  spec.edges.forEach(([a,b],i)=>{const bit=(mask>>i)&1;xor[a]^=bit;xor[b]^=bit;});
  if(xor.every((bit,i)=>bit===spec.charge[i]))sat++;
 }
 assert.equal(sat,0,'the original odd-charge Tseitin source must be UNSAT');
 console.log(JSON.stringify({status:'OS Node original /386 CLI replay',checker_blob:blob(checker),seed_blob:blob(seedFile),
  packet_blob:blob(packetFile),source_unchanged:true,byte_length:exact.length,added_gate_owners:1,
  shared_free_facet_records:2,added_resolutions:8,source_clause_indices:[0,3,13,14],
  result_indices:[103,105,107,109],paid_delta:9,independent_original_edge_assignments:1<<spec.edges.length,
  original_satisfying_assignments:sat,results},null,2));
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
