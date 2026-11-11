'use strict';
/*
 * LSPV-3/573, 2026-11-11 09:24 PST.
 * Run from a complete j15marti/pnp checkout:
 *   node experiments/arc/lspv3_573_source_slot_fixed_cycle.cjs
 *   node experiments/arc/lspv3_573_source_slot_fixed_cycle.cjs --write-raw
 *
 * AUTHORITY: original, unchanged archived /386 checker executed in a real
 * OS Node subprocess. This runner is a certificate transformer, NOT a new
 * checker and NOT the missing full historical R_mix341 calculus.
 */
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const crypto=require('node:crypto'),cp=require('node:child_process');
const assert=require('node:assert/strict');
const root=process.cwd();
const checkerPath=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedPath=path.join(root,'results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json');
const expected={
 checker:'338305c0ce101704205e57543756b8127074a986',
 seed:'08aa169b5db49b2ddd1cb5a9b6890fcc3b790916'
};
const sha256=s=>crypto.createHash('sha256').update(s).digest('hex');
const gitblob=s=>crypto.createHash('sha1').update('blob '+Buffer.byteLength(s,'utf8')+'\0'+s).digest('hex');
const checkerText=fs.readFileSync(checkerPath,'utf8');
const seedText=fs.readFileSync(seedPath,'utf8');
assert.equal(gitblob(checkerText),expected.checker,'wrong ORIGINAL checker blob');
assert.equal(gitblob(seedText),expected.seed,'wrong pinned original packet');
const seed=JSON.parse(seedText),clone=x=>JSON.parse(JSON.stringify(x));
const E=seed.spec.edges.length, V=seed.spec.h;
const canonical=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const flip=(x,mask)=>Math.abs(x)<=E&&((mask>>(Math.abs(x)-1))&1)?-x:x;
const flipC=(c,mask)=>canonical(c.map(x=>flip(x,mask)));
const sourcePos=seed.records.flatMap((r,i)=>r.kind==='SOURCE'?[i]:[]);
assert.equal(sourcePos.length,4*V+1);
assert.deepEqual(sourcePos,Array.from({length:sourcePos.length},(_,i)=>i),'need SOURCE prefix');
const prefix=JSON.stringify(seed.records.slice(0,sourcePos.length));
const sourcePosition=new Map(sourcePos.map(i=>{
 const r=seed.records[i];return [r.source+':'+JSON.stringify(r.c),i];
}));
function syndrome(mask){
 const syn=Array(V).fill(0);
 seed.spec.edges.forEach(([u,v],i)=>{
  if((mask>>i)&1){syn[u]^=1;syn[v]^=1;}
 });
 return syn.join('');
}
function transform(packet,mask){
 const dest=new Map();
 for(const i of sourcePos){
  const r=packet.records[i],k=r.source+':'+JSON.stringify(flipC(r.c,mask));
  const j=sourcePosition.get(k);
  if(j===undefined)return null;
  dest.set(i,j);
 }
 const out=clone(packet);
 out.gate_defs=packet.gate_defs.map(([id,z,a,b])=>[id,z,flip(a,mask),flip(b,mask)]);
 out.records=packet.records.map((r,i)=>{
  if(sourcePos.includes(i))return clone(r);
  const q=clone(r);
  q.c=flipC(r.c,mask);
  q.parents=r.parents.map(j=>dest.has(j)?dest.get(j):j);
  if(r.kind==='RES')q.pivot=flip(r.pivot,mask);
  return q;
 });
 assert.equal(JSON.stringify(out.records.slice(0,sourcePos.length)),prefix,
              'original SOURCE bytes at every index changed');
 return out;
}
const work=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-573-'));
const file=path.join(work,'candidate.json');
function original(packet){
 fs.writeFileSync(file,JSON.stringify(packet));
 const p=cp.spawnSync(process.execPath,[checkerPath,file],{encoding:'utf8',maxBuffer:4*1024*1024});
 if(p.error)throw p.error;
 if(p.status!==0)return {accepted:false,error:(p.stderr||p.stdout).trim().slice(0,500)};
 const lines=p.stdout.trim().split(/\r?\n/),last=JSON.parse(lines.at(-1));
 return {accepted:true,original_assertions:last.assertions,original_negative_tests:last.negativeTests,
         original_paid:last.paid,original_sha256:last.sha256};
}
function prefixFixed(packet){return JSON.stringify(packet.records.slice(0,sourcePos.length))===prefix;}
const acceptedMasks=[],rows=[],hostile={},pairchecks=[];
try{
 for(let mask=0;mask<(1<<E);mask++){
  const q=transform(seed,mask),syn=syndrome(mask);
  if(!q){assert.notEqual(syn,'0'.repeat(V));rows.push({mask,syndrome:syn,source_bijection:false});continue;}
  assert.equal(syn,'0'.repeat(V),'noncycle source position bijection');
  const proof=original(q);
  assert.equal(proof.accepted,true,'original checker rejected SOURCE-fixed action '+mask);
  assert.equal(proof.original_paid,seed.summary.paid_total);
  assert.equal(proof.original_negative_tests,11);
  assert.equal(prefixFixed(q),true);
  acceptedMasks.push(mask);
  rows.push({mask,syndrome:syn,source_bijection:true,accepted:proof.accepted,
    source_prefix_fixed:true,bytes:Buffer.byteLength(JSON.stringify(q)),...proof,
    changed_source_references:q.records.filter((r,i)=>r.parents.some((p,j)=>p!==seed.records[i].parents[j])).length});
 }
 assert.deepEqual(acceptedMasks,[0,11,21,30,38,45,51,56]);
 for(const a of acceptedMasks)for(const b of acceptedMasks){
  const x=transform(transform(seed,a),b),y=transform(seed,a^b);
  assert(x&&y);
  assert.deepEqual(x,y,'kernel group composition');
  pairchecks.push([a,b,a^b]);
 }
 const mask=11,witness=transform(seed,mask);
 const bad={wrong_parent:clone(witness),wrong_pivot:clone(witness),
   wrong_facet:clone(witness),underpay:clone(witness),
   duplicate_gate:clone(witness),source_corrupt:clone(witness)};
 bad.wrong_parent.records[23].parents[1]=1;
 bad.wrong_pivot.records[23].pivot=999;
 bad.wrong_facet.records[17].c=[1,-8];
 bad.underpay.summary.paid_total--;
 bad.duplicate_gate.gate_defs[1][1]=8;
 bad.source_corrupt.records[0].c[0]=998;
 for(const [name,q] of Object.entries(bad)){
  const r=original(q);assert.equal(r.accepted,false,'hostile accepted '+name);
  hostile[name]={...r,source_prefix_fixed:prefixFixed(q)};
 }
 const swapped=clone(witness);
 [swapped.records[0],swapped.records[1]]=[swapped.records[1],swapped.records[0]];
 for(const r of swapped.records)r.parents=r.parents.map(p=>p===0?1:p===1?0:p);
 const swappedCheck=original(swapped);
 assert.equal(swappedCheck.accepted,true,'source-row swap should remain historically legal');
 assert.equal(prefixFixed(swapped),false,'externally pinned source row was not changed');
 hostile.external_source_slot_swap={...swappedCheck,external_frozen_source_rejects:true};
 const raw={
  run:'LSPV-3/573',time:'2026-11-11 09:24 PST',
  calculus:'authentic archived /386 SOURCE/paid-DEF-facet/strict-Resolution SUBSET only',
  full_R_mix341_authenticated:false,
  source_checker_blob:expected.checker,seed_blob:expected.seed,
  source_prefix_sha256:sha256(prefix),source_prefix_rows:sourcePos.length,
  checked_masks:rows.length,source_fixed_original_accepts:acceptedMasks.length,
  source_unmappable_noncycle_masks:rows.filter(r=>!r.source_bijection).length,
  accepted_masks:acceptedMasks,group_pair_checks:pairchecks.length,
  original_checker_executed_as:'OS Node subprocess',rows,hostile,
  witness_mask:mask,witness_bytes:Buffer.byteLength(JSON.stringify(witness)),
  witness_sha256:sha256(JSON.stringify(witness)),
  witness_source_prefix_unchanged:true,paid_logical_work:53,proof_records:74,
  dependency_status:{'P2-D1':'OPEN','P2-C3':'OPEN','P2-B1':'OPEN','P2-B2/B3':'OPEN'},
  p_versus_np:'OPEN',
  caveat:'SOURCE-prefix precondition. Strict external slot binding is a new comparison firewall, NOT the archived checker language. No full mixed-rule claim.'
 };
 if(process.argv.includes('--write-raw')){
  const out=path.join(root,'results/raw/arc/2026-11-11_0924_LSPV3_573_SOURCE_SLOT_NATIVE_OS_RAW.json');
  fs.writeFileSync(out,JSON.stringify(raw,null,2)+'\n');
  const witnessOut=path.join(root,'results/raw/arc/2026-11-11_0924_LSPV3_573_FIXED_SOURCE_SLOT_CYCLE11_PACKET.json');
  fs.writeFileSync(witnessOut,JSON.stringify(witness));
 }
 console.log(JSON.stringify({result:'PASS',acceptedMasks,group_pair_checks:pairchecks.length,
  original_hostile_rejections:Object.keys(bad).length,external_source_slot_swap:hostile.external_source_slot_swap,
  source_prefix_sha256:raw.source_prefix_sha256,
  witness_bytes:raw.witness_bytes,witness_sha256:raw.witness_sha256,paid:53},null,2));
}finally{try{fs.rmSync(work,{recursive:true,force:true});}catch(_){}}
