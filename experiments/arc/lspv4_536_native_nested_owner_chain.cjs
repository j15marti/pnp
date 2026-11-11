'use strict';
// LSPV-4/536: original /386 nested-owner chain resource audit.
// Run from any directory: node experiments/arc/lspv4_536_native_nested_owner_chain.cjs
// Requires Node >=20; no third-party modules. Outputs JSON to stdout.
// Reads the two original blobs and validates their exact Git blob hashes before use.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '../..');
const checkerPath = path.join(root, 'experiments/arc/lspv2_386_independent_verify.js');
const seedPath = path.join(root, 'results/raw/arc/2026-11-10_2124_LSPV3_561_ARCHIVED_386_NATIVE_PACKET.json');
const native = fs.readFileSync(checkerPath, 'utf8');
const seedRaw = fs.readFileSync(seedPath);
function blobSha(bytes) {
  const hdr = Buffer.from('blob ' + bytes.length + '\0');
  return crypto.createHash('sha1').update(hdr).update(bytes).digest('hex');
}
assert.equal(blobSha(Buffer.from(native, 'utf8')), '338305c0ce101704205e57543756b8127074a986');
assert.equal(blobSha(seedRaw), 'd0fa96a155672f8f6a6a3428eacafa15e79b9e88');
const seed = JSON.parse(seedRaw.toString('utf8'));
const clone = x => JSON.parse(JSON.stringify(x));
const canonical = xs => [...new Set(xs)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function family(k) {
  assert(Number.isSafeInteger(k) && k>=0 && k<=128);
  const d=clone(seed), r=seed.records, rec=r.slice(0,20).map(clone);
  d.gate_defs=clone(seed.gate_defs);
  for(let i=1;i<=k;i++){
    const p=7+i, z=8+i;
    d.gate_defs.push([i,z,p,-3]);
    rec.push({kind:'DEF',c:canonical([p,-z]),parents:[],gate:i});
    rec.push({kind:'DEF',c:canonical([-3,-z]),parents:[],gate:i});
    rec.push({kind:'DEF',c:canonical([3,-p,z]),parents:[],gate:i});
  }
  rec.push(clone(r[20]));
  let current=rec.length-1;
  for(let i=1;i<=k;i++){
    const z=8+i;
    rec.push({kind:'RES',c:canonical([-2,3,-7,-z]),parents:[20+3*(i-1),current],pivot:z-1});
    current=rec.length-1;
  }
  for(let i=k;i>=1;i--){
    const z=8+i;
    rec.push({kind:'RES',c:canonical([-2,3,-7,-(z-1)]),parents:[22+3*(i-1),current],pivot:z});
    current=rec.length-1;
  }
  for(let j=21;j<r.length;j++){
    const row=clone(r[j]);
    row.parents=row.parents.map(p=>p<20?p:p===20?current:p+5*k);
    rec.push(row);
  }
  d.records=rec;
  d.summary={source:17,def_views:3+3*k,resolution:49+2*k,paid_gates:1+k,
             paid_total:50+3*k,live_records:69+5*k};
  return d;
}
function invokeOriginal(d) {
  const payload=Buffer.from(JSON.stringify(d), 'utf8');
  const messages=[];
  const mockFs={readFileSync:()=>payload};
  const context={
    require:mod=>mod==='fs'?mockFs:mod==='crypto'?crypto:mod==='assert'?assert:require(mod),
    process:{argv:['node','original_386.js','packet.json']},
    console:{log:s=>messages.push(String(s))},
    structuredClone, Buffer
  };
  vm.runInNewContext(native,context,{timeout:15000});
  assert.equal(messages.length,1);
  return JSON.parse(messages[0]);
}
function dependency(d) {
  const rows=d.records,depth=[],ownerDepth=[],used=new Set(),stack=[rows.length-1];
  const outputs=new Map();
  for(const [id,z,a,b] of d.gate_defs) {
    const parent=outputs.get(Math.abs(a));
    ownerDepth[id]=1+(parent===undefined?0:ownerDepth[parent]);
    outputs.set(z,id);
  }
  for(const row of rows) {
    if(row.kind==='SOURCE')depth.push(0);
    else if(row.kind==='DEF')depth.push(ownerDepth[row.gate]);
    else depth.push(1+Math.max(...row.parents.map(i=>depth[i])));
  }
  while(stack.length){
    const i=stack.pop();
    if(used.has(i))continue;
    used.add(i);
    stack.push(...rows[i].parents);
  }
  const activeFacetIds=[...used].filter(i=>rows[i].kind==='DEF');
  const owners=new Set(activeFacetIds.map(i=>rows[i].gate));
  // The paid owner z_i can itself depend on the paid owner of an input wire.
  for(let i=d.gate_defs.length-1;i>=0;i--)if(owners.has(i)){
    const input=Math.abs(d.gate_defs[i][2]);
    const creator=outputs.get(input);
    if(creator!==undefined)owners.add(creator);
  }
  return {source_ancestry:[...used].filter(i=>rows[i].kind==='SOURCE').length,
    active_facets:activeFacetIds.length,active_owners:owners.size,
    total_ancestry_records:used.size,sink_depth_with_paid_owner_edges:depth.at(-1)};
}
function removeDeadFacets(d,k){
  const old=d.records,removal=new Set([18]);
  for(let i=1;i<=k;i++)removal.add(21+3*(i-1));
  const map=new Map(),next=[];
  for(let j=0;j<old.length;j++)if(!removal.has(j)){map.set(j,next.length);next.push(clone(old[j]));}
  for(const r of next)r.parents=r.parents.map(p=>{
    assert(map.has(p),'dead facet had a live dependent');return map.get(p);
  });
  const e=clone(d);e.records=next;
  e.summary.def_views-=(1+k);e.summary.live_records-=(1+k);
  return e;
}
function sourceModels(d) {
  let sat=0;
  const source=d.records.filter(x=>x.kind==='SOURCE');
  for(let a=0;a<(1<<d.spec.guard);a++){
    const ok=source.every(x=>x.c.some(l=>l>0?((a>>(l-1))&1)===1:((a>>(-l-1))&1)===0));
    if(ok)sat++;
  }
  return sat;
}
const positive=[];
for(const k of [0,1,2,3,4,8,16,32]){
  const full=family(k),short=removeDeadFacets(full,k);
  const orig=invokeOriginal(full),slim=invokeOriginal(short),dep=dependency(full);
  assert.equal(sourceModels(full),0);
  assert.equal(orig.paid,50+3*k);assert.equal(slim.paid,orig.paid);
  assert.equal(dep.source_ancestry,17);assert.equal(dep.active_facets,2+2*k);
  assert.equal(dep.active_owners,1+k);
  assert.equal(dep.sink_depth_with_paid_owner_edges,10+2*k);
  positive.push({k,full_bytes:Buffer.byteLength(JSON.stringify(full)),
    sliced_bytes:Buffer.byteLength(JSON.stringify(short)),
    ...full.summary,reference_edges:2*full.summary.resolution,...dep,
    original_assertions:orig.assertions,original_built_in_negatives:orig.negativeTests,
    original_sliced_assertions:slim.assertions});
}
const controls={
  reverse_owners:d=>d.gate_defs.reverse(),
  duplicate_owner:d=>{d.gate_defs[2][0]=1;},
  duplicate_output:d=>{d.gate_defs[2][1]=9;},
  incorrect_nested_input:d=>{d.gate_defs[2][2]=4;},
  wrong_facet:d=>{d.records[26].c=[1,-10];},
  signed_pivot:d=>{d.records.find(r=>r.kind==='RES'&&r.pivot===10).pivot=-10;},
  understated_charge:d=>{d.summary.paid_total--;},
  modified_original_source:d=>{d.records[0].c=[-1,2,3,-7];},
  future_parent:d=>{d.records[33].parents[0]=d.records.length;},
  corrupted_sink:d=>{d.records.at(-1).c=[-6];},
  missing_owner:d=>{d.gate_defs.splice(1,1);d.summary.paid_gates--;d.summary.paid_total--;}
};
const negative=[];
for(const [label,mutate] of Object.entries(controls)){
  const d=family(4);mutate(d);
  let rejected=false,diagnostic='';
  try{invokeOriginal(d);}catch(e){rejected=true;diagnostic=String(e.message||e);}
  assert(rejected,'original checker accepted hostile control '+label);
  negative.push({label,rejected,diagnostic});
}
const result={
  status:'RESTRICTED original archived /386 accepted language ONLY, not complete R_mix341',
  originalCheckerGitBlob:'338305c0ce101704205e57543756b8127074a986',
  originalSeedGitBlob:'d0fa96a155672f8f6a6a3428eacafa15e79b9e88',
  runtime:'Node vm, original checker body and 11 built-in hostile tests unchanged',
  model:'Original guarded K4 signed SOURCE/paid DEF owner/free facets/strict RES',
  all_k_with_safe_ids:'For each k fitting JS safe integers and available memory; runner tests k <= 32',
  theorem:{W:'50+3*k',R:'98+4*k',records:'69+5*k',owners:'1+k',
           facets:'3+3*k',active_facets:'2+2*k',active_owners:'1+k',
           owner_edge_span:'10+2*k',sliced_records:'68+4*k',sliced_W:'50+3*k'},
  positive,negative,
  input_sat_models:0,
  no_generalization:'No authenticated full mixed dispatcher, no unrestricted proof lower bound, no physical high-water memory measurement.'
};
process.stdout.write(JSON.stringify(result,null,2)+'\n');
