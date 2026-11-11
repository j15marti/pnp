'use strict';
/* LSPV-3/561. Run from j15marti/pnp root:
node experiments/arc/lspv3_561_archived_386_facet_bridge.cjs
Authenticates the distinct historical /386 checker, NOT R_mix341's full missing /341 parser. */
const fs=require('node:fs'),crypto=require('node:crypto'),vm=require('node:vm'),assert=require('node:assert/strict');
const sort=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
const edges=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)edges.push([i,j]);
let records=[],sources=[],facets=[],paidResolution=0;
function emit(kind,c,parents,other={}){
 records.push({kind,c:sort(c),parents,...other});return records.length-1;
}
for(let v=0;v<4;v++){
 let inc=edges.map(([a,b],i)=>a===v||b===v?i+1:null).filter(x=>x!==null);
 for(let pat=0;pat<8;pat++){
  let bits=[pat&1,(pat>>1)&1,(pat>>2)&1];
  if((bits[0]^bits[1]^bits[2])===(v===0?1:0))continue;
  let clause=inc.map((x,j)=>bits[j]?-x:x);
  sources.push({idx:emit('SOURCE',[...clause,-7],[],{source:v}),clause,v});
 }
}
const t=emit('SOURCE',[7],[],{source:-1});
for(const c of [[-8,1],[-8,2],[8,-1,-2]])facets.push(emit('DEF',c,[],{gate:0}));
function resolve(a,b,p){
 assert(a.includes(p)&&b.includes(-p),'complementary pivot');
 const c=sort([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
 return c.some(x=>c.includes(-x))?null:c;
}
function res(a,b,p){
 const c=resolve(records[a].c,records[b].c,p);assert(c!==null,'no tautological pivot');
 paidResolution++;return emit('RES',c,[a,b],{pivot:p});
}
const selected=sources.find(s=>s.v===0&&s.clause.includes(-1)&&s.clause.includes(-2));
const step1=res(facets[0],selected.idx,1),step2=res(facets[2],step1,8);
assert.deepEqual(records[step2].c,records[selected.idx].c,'exact source restoration');
let active=new Map();
for(const s of sources){
 const j=res(t,s.idx===selected.idx?step2:s.idx,7);
 assert.deepEqual(records[j].c,sort(s.clause));
 active.set(records[j].c.join(','),j);
}
for(let p=1;p<=6;p++){
 const pos=[...active.values()].filter(j=>records[j].c.includes(p));
 const neg=[...active.values()].filter(j=>records[j].c.includes(-p));
 const rest=new Map([...active].filter(([k,j])=>!records[j].c.includes(p)&&!records[j].c.includes(-p)));
 for(const a of pos)for(const b of neg){
  const c=resolve(records[a].c,records[b].c,p);
  if(c===null||rest.has(c.join(',')))continue;
  rest.set(c.join(','),res(a,b,p));
 }
 active=rest;if(active.has(''))break;
}
assert(active.has('')&&active.get('')===records.length-1,'final refutation');
const ancestry=new Set();
function trace(j){if(ancestry.has(j))return;ancestry.add(j);for(const p of records[j].parents)trace(p);}
trace(records.length-1);
for(const j of [selected.idx,facets[0],facets[2],step1,step2])
 assert(ancestry.has(j),'source/facet bridge is not dead');
for(const s of sources)assert(ancestry.has(s.idx),'every source in sink ancestry');
const packet={spec:{h:4,edges,charge:[1,0,0,0],guard:7},gate_defs:[[0,8,1,2]],records,
 summary:{source:17,def_views:3,resolution:paidResolution,paid_gates:1,paid_total:paidResolution+1,live_records:records.length}};
const json=Buffer.from(JSON.stringify(packet)+'\n');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
assert.equal(paidResolution,49);assert.equal(records.length,69);assert.equal(json.length,4144);
assert.equal(sha(json),'2259e61a1e0e1a80f3be29490199af9a7c7f5382ecaf151b0a924d47c738ebff');
const checkerPath='experiments/arc/lspv2_386_independent_verify.js';
const original=fs.readFileSync(checkerPath);
const gitblob=crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+original.length+'\0'),original])).digest('hex');
assert.equal(gitblob,'338305c0ce101704205e57543756b8127074a986');
function replay(p){
 const output=[];
 try{
  vm.runInNewContext(original.toString('utf8'),{
   require:n=>n==='fs'?{readFileSync:()=>Buffer.from(JSON.stringify(p))}:require(n),
   process:{argv:['node',checkerPath,'certificate.json']},
   console:{log:x=>output.push(x)},structuredClone
  },{filename:checkerPath,timeout:30000});
  assert.equal(output.length,1);
  return {accept:true,value:JSON.parse(output[0])};
 }catch(e){return {accept:false,error:String(e.message).slice(0,160)};}
}
const baseline=replay(packet);
assert.equal(baseline.accept,true,JSON.stringify(baseline));
assert.equal(baseline.value.assertions,4492);assert.equal(baseline.value.paid,50);
const negatives={
 wrong_owner:d=>d.records[17].gate=50,
 wrong_facet:d=>d.records[17].c=[1,8],
 wrong_pivot:d=>d.records[20].pivot=2,
 wrong_sink:d=>d.records.at(-1).c=[1],
 wrong_source:d=>d.records[1].c=[1,-2,3,-7],
 duplicate_gate:d=>d.gate_defs.push(d.gate_defs[0].slice()),
 unpaid_gate:d=>d.summary.paid_total=49,
 future_parent:d=>d.records[20].parents[0]=68,
 missing_owner:d=>d.gate_defs=[],
 bad_graph:d=>d.spec.edges[0]=d.spec.edges[1].slice()
};
const controls=[];
for(const [name,mutate] of Object.entries(negatives)){
 const clone=JSON.parse(JSON.stringify(packet));mutate(clone);
 const result=replay(clone);assert.equal(result.accept,false,'accepted '+name);
 controls.push({name,rejected:true,diagnostic:result.error});
}
const raw={role:'LSPV-3/561',status:'COMPUTATIONAL',
 scope:'Distinct archived /386 original checker, NOT full R_mix341',
 checker_git_blob:gitblob,certificate_sha256:sha(json),certificate_bytes:json.length,
 baseline:baseline.value,additional_negative_controls:controls,
 facets_on_sink_ancestry:[facets[0],facets[2]],
 all_16_original_sources_on_sink_ancestry:true,
 paid_resolution:49,paid_gate_owners:1,free_def_facet_records:3,
 original_body_verification:'original source run unchanged in Node vm, I/O stubs only'};
fs.writeFileSync('results/raw/arc/2026-11-10_2124_LSPV3_561_ARCHIVED_386_NATIVE_PACKET.json',json);
fs.writeFileSync('results/raw/arc/2026-11-10_2124_LSPV3_561_ARCHIVED_386_REPLAY_RAW.json',JSON.stringify(raw,null,2)+'\n');
console.log(JSON.stringify(raw,null,2));
