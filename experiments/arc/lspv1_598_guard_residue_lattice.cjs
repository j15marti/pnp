#!/usr/bin/env node
'use strict';
// LSPV-1/598, 2026-11-12 11:23 PST. Run at repository root:
// node experiments/arc/lspv1_598_guard_residue_lattice.cjs [output.json]
// Uses original archived /386 checker in untouched Node OS subprocesses.
// This is NOT a checker for complete historical R_mix341.
const fs=require('node:fs'), cp=require('node:child_process');
const path=require('node:path'), os=require('node:os');
const assert=require('node:assert/strict'), crypto=require('node:crypto');
const root=path.resolve(__dirname,'../..');
const paths={
 checker:'experiments/arc/lspv2_386_independent_verify.js',
 seed:'results/raw/arc/2026-11-12_0424_LSPV3_587_NATIVE_CONSTANT_FACET_ACCEPTED_PACKET.json',
 witness:'results/raw/arc/2026-11-12_1100_LSPV1_597_NATIVE386_LIVE16_W44_ACCEPTED.json'
};
const pins={
 checker:'338305c0ce101704205e57543756b8127074a986',
 seed:'4177ec15a0c7253378d5652a6b13b7152601d300',
 witness:'a9514ed6d28d19403d745a583c3096d36cd1a399'
};
function gitBlob(bytes){return crypto.createHash('sha1').update('blob '+bytes.length+'\0').update(bytes).digest('hex')}
for(const [tag,p] of Object.entries(paths))
 assert.equal(gitBlob(fs.readFileSync(path.join(root,p))),pins[tag],'pinned '+tag);
const read=tag=>JSON.parse(fs.readFileSync(path.join(root,paths[tag]),'utf8'));
const seed=read('seed'), base=seed.records, g=seed.spec.guard, full=(1<<16)-1;
assert.equal(base.length,46);
assert.equal(g,7);
assert.equal(base.filter(r=>r.kind==='SOURCE').length,17);
assert.equal(base.filter(r=>r.kind==='RES').length,28);
assert(base.slice(18,45).every(r=>r.kind==='RES'&&r.pivot!==g&&r.c.includes(-g)));
const key=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function resolve(a,b,p){
 assert(a.includes(p)&&b.includes(-p),'bad signed parent');
 let c=key([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
 assert(!c.some(x=>c.includes(-x)),'tautological resolvent');
 return c;
}
function make(mask){
 const d=structuredClone(seed), rr=structuredClone(base.slice(0,18));
 const map=new Map(), ports=[];
 for(let i=1;i<=16;i++)if((mask>>(i-1))&1){
  map.set(i,rr.length);ports.push(rr.length);
  rr.push({kind:'RES',c:base[i].c.filter(x=>x!==-g),parents:[17,i],pivot:g});
 }
 for(let i=18;i<=44;i++){
  const r=base[i],parents=r.parents.map(j=>map.has(j)?map.get(j):j);
  const c=resolve(rr[parents[0]].c,rr[parents[1]].c,r.pivot);
  map.set(i,rr.length);rr.push({...r,parents,c});
 }
 const rootClause=rr.at(-1).c, withGuard=rootClause.includes(-g);
 if(withGuard){
  assert.deepEqual(rootClause,[-g]);
  rr.push({kind:'RES',c:[],parents:[17,rr.length-1],pivot:g});
 }else assert.deepEqual(rootClause,[]);
 d.records=rr;
 const paidRES=rr.filter(r=>r.kind==='RES').length;
 d.summary={source:17,def_views:1,resolution:paidRES,
  paid_gates:1,paid_total:paidRES+1,live_records:rr.length};
 const ancestors=new Set();
 function visit(i){if(ancestors.has(i))return;ancestors.add(i);
  for(const j of rr[i].parents){assert(j<i&&j>=0);visit(j)}}
 visit(rr.length-1);
 assert(ports.every(i=>ancestors.has(i)),'paid port not terminal live');
 assert(Array.from({length:16},(_,i)=>i+1).every(i=>ancestors.has(i)),
  'missing authentic original SOURCE');
 return {d,withGuard,ports:ports.length,ancestors:ancestors.size};
}
assert.deepEqual(make(0).d,seed,'k=0 must recover original');
assert.deepEqual(make(full).d,read('witness'),'k=16 must recover /597 W44');
// Exhaustive guard-state transfer on the SAME original 27-RES DAG.
// The bit for each original guarded input equals 1 if the direct
// guard-elimination port is absent. No extra proof rules are assumed.
let guarded=0,unguarded=0;
for(let mask=0;mask<=full;mask++){
 const flags=Array(base.length).fill(false);
 for(let i=1;i<=16;i++)flags[i]=!((mask>>(i-1))&1);
 for(let i=18;i<=44;i++){
  const p=base[i].parents;
  assert(!p.includes(17),'no guard pivot in body');
  flags[i]=flags[p[0]]||flags[p[1]];
 }
 assert.equal(flags[44],mask!==full,'guard transfer '+mask);
 flags[44]?guarded++:unguarded++;
}
assert.equal(guarded,65535);assert.equal(unguarded,1);
// Test 17 prefix masks plus 16 singleton and 16 co-singleton masks,
// for 47 unique native certificates.
const masks=new Set();
for(let k=0;k<=16;k++)masks.add((1<<k)-1);
for(let i=0;i<16;i++){masks.add(1<<i);masks.add(full^(1<<i))}
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv1-598-'));
const outcomes=[];
function native(name,d,shouldAccept){
 const fn=path.join(temp,'packet.json');
 fs.writeFileSync(fn,JSON.stringify(d)+'\n','utf8');
 const run=cp.spawnSync(process.execPath,[path.join(root,paths.checker),fn],
  {encoding:'utf8',maxBuffer:32*1024*1024,timeout:30000});
 if(run.error)throw run.error;
 const accepted=run.status===0;
 assert.equal(accepted,shouldAccept,name+': '+(run.stderr||'').slice(-400));
 return accepted?JSON.parse(run.stdout):{error:(run.stderr||'').slice(-250)};
}
try{
 for(const mask of [...masks].sort((a,b)=>a-b)){
  const x=make(mask),k=mask.toString(2).replace(/0/g,'').length;
  const expected=k===16?44:29+k;
  assert.equal(x.withGuard,k<16);
  assert.equal(x.ports,k);
  assert.equal(x.d.summary.paid_total,expected);
  const n=native('valid mask '+mask,x.d,true);
  assert.equal(n.paid,expected);
  assert.equal(n.negativeTests,11);
  outcomes.push({mask,k,guardResidue:x.withGuard,paid:n.paid,
   records:x.d.records.length,portAncestors:x.ports,
   native_assertions:n.assertions});
 }
 const negative=[
  ['bad_source',d=>d.records[1].c=[1,-7]],
  ['bad_pivot',d=>d.records.find(r=>r.kind==='RES').pivot=1],
  ['underpay',d=>d.summary.paid_total--],
  ['bad_terminal',d=>d.records.at(-1).c=[7]],
  ['bad_guard',d=>d.spec.guard=6],
  ['bad_parent',d=>d.records[18].parents.reverse()]
 ];
 for(const [name,mutate] of negative){
  const d=make(255).d;mutate(d);
  const result=native(name,d,false);
  outcomes.push({name,rejected:true,error:result.error});
 }
}finally{fs.rmSync(temp,{recursive:true,force:true})}
const positive=outcomes.filter(x=>x.mask!==undefined),negative=outcomes.filter(x=>x.rejected);
const raw={id:'LSPV-1/598',status:'COMPUTATIONAL',mode:'actual Node OS subprocess original checker',
 pins,source_guard:g,signed_sources:17,body_non_guard_RES:27,
 exhaustive_boolean_guard_replays:65536,guarded,unguarded,
 original_checker_positive_count:positive.length,
 original_checker_assertions:positive.reduce((a,r)=>a+r.native_assertions,0),
 positive_cases:positive,hostiles:negative,all_positive_accepted:true,
 all_hostiles_rejected:true,
 scope:'Archived /386 SOURCE/DEF/RES; NOT full historical R_mix341',
 conclusion:'Port-erasure needed at all sixteen terminal-ancestor leaves to omit final guard pivot in this exact DAG; NOT a global minimum work bound'};
if(process.argv[2])fs.writeFileSync(path.resolve(process.argv[2]),JSON.stringify(raw,null,2)+'\n');
console.log(JSON.stringify(raw,null,2));
