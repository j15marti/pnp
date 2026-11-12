#!/usr/bin/env node
'use strict';
/* LSPV-5/501: independent exact composition audit for the pinned archived /386
 * checker. This is not an implementation or completion of historical R_mix341.
 * Run from the repository root with Node >=18; no external packages.
 */
const assert=require('node:assert/strict');
const cp=require('node:child_process');
const crypto=require('node:crypto');
const fs=require('node:fs');
const os=require('node:os');
const path=require('node:path');
const root=path.resolve(__dirname,'../..');
const checkerPath=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedPath=path.join(root,'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json');
const checkerBytes=fs.readFileSync(checkerPath),seedBytes=fs.readFileSync(seedPath);
const gitblob=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
const sha256=b=>crypto.createHash('sha256').update(b).digest('hex');
assert.equal(gitblob(checkerBytes),'338305c0ce101704205e57543756b8127074a986','checker drift');
assert.equal(gitblob(seedBytes),'318c52d99977ea4e91bc8554051138a700c1dc94','seed drift');
const seed=JSON.parse(seedBytes),N=seed.records.length;
assert.equal(N,45); assert.deepEqual(seed.gate_defs,[[0,8,1,4]]);
assert.deepEqual(seed.summary,{source:17,def_views:0,resolution:28,paid_gates:1,paid_total:29,live_records:45});
const clone=x=>JSON.parse(JSON.stringify(x));
const bytes=x=>Buffer.from(JSON.stringify(x)+'\n','utf8');
const resOld=seed.records.map((r,i)=>r.kind==='RES'?i:null).filter(i=>i!==null);
assert.equal(resOld.length,28);
function shiftFor(slots,oldIndex){return oldIndex+slots.filter(s=>s<=oldIndex).length;}
function interleave(packet,rawSlots,rebase=true){
  const slots=[...rawSlots].sort((a,b)=>a-b);
  assert(slots.every(s=>Number.isSafeInteger(s)&&s>=0&&s<N));
  const out=clone(packet); out.records=[];
  for(let i=0;i<N;i++){
    for(const s of slots)if(s===i)out.records.push({kind:'DEF',gate:0,c:[1,-8],parents:[]});
    const r=clone(packet.records[i]);
    if(rebase)r.parents=r.parents.map(p=>shiftFor(slots,p));
    out.records.push(r);
  }
  out.summary.def_views+=slots.length; out.summary.live_records+=slots.length;
  return out;
}
function flipAt(packet,i){const r=packet.records[i];assert.equal(r.kind,'RES');r.parents=[r.parents[1],r.parents[0]];r.pivot=-r.pivot;}
function swapOwner(packet){const g=packet.gate_defs[0];assert.deepEqual(g,[0,8,1,4]);g[2]=4;g[3]=1;}
function beforeThenInsert(slots,owner,flipOld){
  const p=clone(seed);if(owner)swapOwner(p);for(const i of flipOld)flipAt(p,i);return interleave(p,slots,true);
}
function insertThenAfter(slots,owner,flipOld){
  const ordered=[...slots].sort((a,b)=>a-b),p=interleave(seed,ordered,true);if(owner)swapOwner(p);for(const i of flipOld)flipAt(p,shiftFor(ordered,i));return p;
}
function sourceModels(packet){
  const src=packet.records.filter(r=>r.kind==='SOURCE').map(r=>r.c);let count=0;
  for(let a=0;a<(1<<7);a++)if(src.every(c=>c.some(l=>l>0?((a>>(l-1))&1):!((a>>(-l-1))&1))))count++;
  return count;
}
assert.equal(sourceModels(seed),0,'guarded K4 source must be UNSAT');
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-lspv5-501-'));
function native(packet,label,expected){
  const body=bytes(packet),file=path.join(temp,label+'.json');fs.writeFileSync(file,body);
  const t0=process.hrtime.bigint();const r=cp.spawnSync(process.execPath,[checkerPath,file],{cwd:root,encoding:'utf8',timeout:20000,maxBuffer:1<<20});
  if(r.error)throw r.error;const accepted=r.status===0;assert.equal(accepted,expected,label+' '+r.stderr);
  const parsed=accepted?JSON.parse(r.stdout.trim().split(/\r?\n/).at(-1)):null;
  if(accepted){assert.equal(parsed.paid,29);assert.equal(parsed.res,28);assert.equal(parsed.def,1);assert.equal(parsed.sources,17);assert.equal(parsed.negativeTests,11);}
  return {label,accepted,bytes:body.length,sha256:sha256(body),git_blob:gitblob(body),paid:parsed?.paid??null,records:parsed?.records??null,assertions:parsed?.assertions??null,negative_tests:parsed?.negativeTests??null,elapsed_ms:Number(process.hrtime.bigint()-t0)/1e6,rejection:accepted?null:(r.stderr.match(/Error: [^\n]+/)||[])[0]||String(r.stderr).slice(0,220)};
}
const masks=[[],resOld,[resOld[0]],[resOld.at(-1)],resOld.filter((_,j)=>j%2===0),resOld.filter((_,j)=>j%3===0)];
let commutationChecks=0,distinct=new Set();
for(let s=0;s<N;s++)for(const owner of [false,true])for(const mask of masks){
  const a=beforeThenInsert([s],owner,mask),b=insertThenAfter([s],owner,mask);
  assert.deepEqual(a,b,'composition must commute');commutationChecks++;
  distinct.add(sha256(bytes(a)));
}
assert.equal(distinct.size,N*2*masks.length,'selected presentations must be byte-distinct');
const positives=[],negatives=[];
try{
  positives.push(native(seed,'baseline',true));
  for(let s=0;s<N;s++)for(const owner of [false,true]){
    const mask=resOld.filter((_,j)=>(j+s)%3===0);
    positives.push(native(insertThenAfter([s],owner,mask),'k1_gap_'+s+'_owner_'+Number(owner),true));
  }
  const multis=[[0,0],[0,44],[1,22],[12,12],[15,16],[22,44],[44,44],[0,5,19,44],Array(64).fill(22)];
  for(let j=0;j<multis.length;j++)positives.push(native(insertThenAfter(multis[j],j%2===0,resOld),'multi_'+j,true));
  const witness=insertThenAfter([0,5,19,44],true,resOld);
  assert.equal(sourceModels(witness),0);assert.deepEqual(witness.spec,seed.spec);assert.equal(witness.summary.paid_total,29);
  const hostiles={
    stale_parents:()=>interleave(seed,[0,5,19,44],false),
    false_facet:()=>{const p=clone(witness);p.records.find(r=>r.kind==='DEF').c=[1,-9];return p;},
    one_sided_pivot:()=>{const p=clone(witness),r=p.records.find(x=>x.kind==='RES');r.pivot=-r.pivot;return p;},
    one_sided_parent_swap:()=>{const p=clone(witness),r=p.records.find(x=>x.kind==='RES');r.parents.reverse();return p;},
    changed_owner_operand:()=>{const p=clone(witness);p.gate_defs[0]=[0,8,4,5];return p;},
    forged_source:()=>{const p=clone(witness),r=p.records.find(x=>x.kind==='SOURCE');r.c[0]=-r.c[0];return p;},
    underpaid:()=>{const p=clone(witness);p.summary.paid_total--;return p;},
    foreign_owner:()=>{const p=clone(witness);p.records.find(r=>r.kind==='DEF').gate=99;return p;},
    forward_parent:()=>{const p=clone(witness),r=p.records.find(x=>x.kind==='RES');r.parents[0]=p.records.length;return p;},
    unsupported_local_convert:()=>{const p=clone(witness);p.records.find(r=>r.kind==='DEF').kind='LOCAL-CONVERT';return p;}
  };
  for(const [name,make] of Object.entries(hostiles))negatives.push(native(make(),'reject_'+name,false));
  const rawRel='results/raw/review/2026-11-12_0248_LSPV5_501_NATIVE386_JOINT_ORBIT_RAW.json';
  const witnessRel='results/raw/review/2026-11-12_0248_LSPV5_501_JOINT_ORBIT_ACCEPTED.json';
  const witnessBytes=bytes(witness);
  const result={run:'LSPV-5/501',timestamp:'2026-11-12 02:48 PST',scope:'unchanged pinned archived /386 SOURCE/RES/AND2-owner/free-DEF-facet checker only; not full historical R_mix341',status:'PROVED/RESTRICTED exact syntactic orbit theorem plus COMPUTATIONAL original Node OS validation',checker_git_blob:gitblob(checkerBytes),seed_git_blob:gitblob(seedBytes),source_models:0,source_clause_count:17,base:{records:N,resolution:28,paid_owner:1,paid_total:29},theorem:{statement:'For every k>=0, every multiset of k among 45 pre-record gaps, every subset of the 28 signed RES occurrences, and either ordering of the nondegenerate AND2 owner inputs, the transformations commute and produce a distinct checker-accepted presentation with unchanged source, empty sink and W29.',orbit:'binom(k+44,44)*2^29',qualifier:'symbolic theorem is for the declared pinned /386 transition relation; OS replay is a finite validation sample'},commutation_checks:commutationChecks,selected_distinct_hashes:distinct.size,positive_cases:positives.length,hostile_rejections:negatives.length,positive_assertion_groups:positives.reduce((a,x)=>a+x.assertions,0),witness:{path:witnessRel,bytes:witnessBytes.length,sha256:sha256(witnessBytes),git_blob:gitblob(witnessBytes),slots:[0,5,19,44],owner_swapped:true,res_flipped:28,paid_total:29},positives,negatives,limits:['No historical mixed dispatcher/caller authenticated','No LOCAL-CONVERT, AND3, GF(2), branching, context, discharge, join, deletion or preprocessing grammar inferred','Presentation multiplicity is not a family lower bound or SAT decision lower bound','P2-D1, P2-C3, P2-B1 and separate P2-B2/B3 remain OPEN','P versus NP remains OPEN']};
  fs.mkdirSync(path.join(root,'results/raw/review'),{recursive:true});
  fs.writeFileSync(path.join(root,witnessRel),witnessBytes);fs.writeFileSync(path.join(root,rawRel),JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify({raw:rawRel,witness:result.witness,checker:result.checker_git_blob,seed:result.seed_git_blob,commutation_checks:commutationChecks,positive_cases:positives.length,hostile_rejections:negatives.length,positive_assertion_groups:result.positive_assertion_groups,source_models:result.source_models,orbit:result.theorem.orbit},null,2));
}finally{fs.rmSync(temp,{recursive:true,force:true});}
