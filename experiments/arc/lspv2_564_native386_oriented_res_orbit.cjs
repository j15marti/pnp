#!/usr/bin/env node
'use strict';
/*
LSPV-2/564. Reference byte constructor, NOT historical checker.
Run: node experiments/arc/lspv2_564_native386_oriented_res_orbit.cjs
Use exactly unchanged original /386 CLI in OS subprocess, Git blob-pinned.
*/
const fs=require('node:fs');
const path=require('node:path');
const os=require('node:os');
const cp=require('node:child_process');
const crypto=require('node:crypto');
const assert=require('node:assert/strict');
const root=process.cwd();
const SOURCE='results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json';
const CHECKER='experiments/arc/lspv2_386_independent_verify.js';
const read=p=>fs.readFileSync(path.join(root,p));
const blob=b=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');
const digest=b=>crypto.createHash('sha256').update(b).digest('hex');
assert.equal(blob(read(SOURCE)),'318c52d99977ea4e91bc8554051138a700c1dc94');
assert.equal(blob(read(CHECKER)),'338305c0ce101704205e57543756b8127074a986');
const seed=JSON.parse(read(SOURCE).toString('utf8'));
const clone=x=>structuredClone(x);
const recordIds=seed.records.flatMap((r,i)=>r.kind==='RES'?[i]:[]);
assert.equal(recordIds.length,28);
function flip(r){assert.equal(r.kind,'RES'); const q=[...r.parents].reverse();r.parents=q;r.pivot=-r.pivot;}
function transform(indices){const packet=clone(seed); for(const i of indices)flip(packet.records[i]); return packet;}
function bytes(p){return Buffer.from(JSON.stringify(p)+'\n','utf8');}
function native(p,dir,label){const f=path.join(dir,label+'.json');fs.writeFileSync(f,bytes(p));
 const r=cp.spawnSync(process.execPath,[path.join(root,CHECKER),f],{encoding:'utf8',timeout:12000,maxBuffer:2000000});
 return {accepted:r.status===0,stdout:r.stdout,stderr:r.stderr,status:r.status,bytes:bytes(p).length,
 sha256:digest(bytes(p)),blob:blob(bytes(p)),
 parsed:r.status===0?JSON.parse(r.stdout.trim().split('\n').at(-1)):null};}
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-564-'));
const positives=[],negatives=[],allOrbits=new Set();
try{
 function good(label,ids,save=false){const p=transform(ids);const r=native(p,tmp,label);assert(r.accepted,`${label}: ${r.stderr}`);
  assert.equal(r.parsed.paid,29);assert.equal(r.parsed.res,28);assert.equal(r.parsed.negativeTests,11);
  assert.equal(r.parsed.records,45);assert.equal(r.parsed.sources,17);assert.deepEqual(p.gate_defs,seed.gate_defs);
  assert.equal(p.records.filter(q=>q.kind==='RES').length,28);
  assert(!allOrbits.has(r.sha256));allOrbits.add(r.sha256);
  if(save)fs.writeFileSync(path.join(root,'results/raw/arc/2026-11-11_1312_LSPV2_564_ACCEPTED_ALL_ORIENTATIONS.json'),bytes(p));
  positives.push({label,flipped_indices:ids,sha256:r.sha256,git_blob:r.blob,utf8_bytes:r.bytes,paid:r.parsed.paid,
    records:r.parsed.records,assertions:r.parsed.assertions,original_checker:true,negative_tests:r.parsed.negativeTests});}
 good('seed',[]);
 for(const i of recordIds)good('single_'+i,[i]);
 good('all',recordIds,true);
 good('even',recordIds.filter((_,j)=>j%2===0));
 good('odd',recordIds.filter((_,j)=>j%2===1));
 good('every_third',recordIds.filter((_,j)=>j%3===0));
 // Deterministic independent 64-subset choices, with no pseudorandom ambiguity.
 for(let k=1;k<=64;k++){
  let x=(Math.imul(k,2654435761)>>>0),chosen=[];
  for(const i of recordIds){x=(Math.imul(x,1664525)+1013904223)>>>0;if(x&0x80000000)chosen.push(i)}
  if(!chosen.length||chosen.length===recordIds.length)continue;
  if(allOrbits.has(digest(bytes(transform(chosen)))))continue;
  good('deterministic_'+k,chosen);
 }
 const hostile={
  pivot_without_swap:p=>p.records[17].pivot=-p.records[17].pivot,
  swap_without_pivot:p=>p.records[17].parents.reverse(),
  pivot_zero:p=>p.records[17].pivot=0,
  invalid_parent_after_flipping:p=>{flip(p.records[17]);p.records[17].parents[0]=p.records.length+1},
  corrupt_conclusion_after_flipping:p=>{flip(p.records[17]);p.records[17].c=[-999]},
  source_polarity_change:p=>{flip(p.records[17]);p.records[0].c[0]=-p.records[0].c[0]},
  undercharge:p=>{flip(p.records[17]);p.summary.paid_total--}
 };
 for(const [label,mutate] of Object.entries(hostile)){
  const p=transform([]);mutate(p);const r=native(p,tmp,'bad_'+label);
  assert(!r.accepted,`wrongly accepted ${label}`);
  negatives.push({label,accepted:r.accepted,status:r.status,sha256:r.sha256,utf8_bytes:r.bytes,stderr_tail:r.stderr.slice(-450)});
 }
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
const raw={id:'LSPV-2/564',date:'2026-11-11 13:12 PST',status:'PASS',
 scope:'unchanged original archived /386 complete Node OS CLI, not historical full R_mix341',
 checker_git_blob:blob(read(CHECKER)),source_seed_git_blob:blob(read(SOURCE)),
 theorem:'For any accepted /386 certificate with R strict RES records, independent parent-swap plus pivot-sign flips yield 2^R distinct same-work accepted JSON packets.',
 n_res:recordIds.length,orbit_size:'2^28 = 268435456',all_verified:positives.length+negatives.length,
 positives:positives.length,negatives:negatives.length,all_positive_assertions:positives.reduce((a,x)=>a+x.assertions,0),
 positive_results:positives,hostiles:negatives,materials:'proof source and gate paid IDs unchanged',
 original_source_external_hash:'NOT bound by original checker; use independent binder for claims about external formula',
 not_authenticating:['AND3','GF(2)','LOCAL-CONVERT','BRANCH','DISCHARGE'],
 P2_D1:'OPEN',P2_C3:'OPEN',P2_B1:'OPEN',B3:'OPEN',P_versus_NP:'OPEN'};
fs.writeFileSync(path.join(root,'results/raw/arc/2026-11-11_1312_LSPV2_564_ORIENTED_RES_OS_RAW.json'),JSON.stringify(raw,null,2)+'\n');
console.log(JSON.stringify({status:'PASS',positive:raw.positives,negative:raw.negatives,assertions:raw.all_positive_assertions,
orbit:raw.orbit_size,accepted_all_path:'results/raw/arc/2026-11-11_1312_LSPV2_564_ACCEPTED_ALL_ORIENTATIONS.json'},null,2));
