#!/usr/bin/env node
'use strict';
// LSPV-5/488 red-team of LSPV-4/543 slot premise, using the UNCHANGED original /386 CLI
// in OS Node subprocesses. Run from repo root:
//   node experiments/review/lspv5_488_slot_premise_redteam.cjs
// Families (all canonical JSON.stringify output, no whitespace):
//   Q_m : seed + top-level ignored field "pad" of m ASCII bytes   (N fixed = 49)
//   S_m : seed + record-level ignored field "pad" on record 0      (N fixed = 49)
//   P_{k,m}: LSPV-4/543 k-facet family combined with pad m          (N = 49+k)
// Shows: accepted-packet length L is unbounded at fixed N, so the 2N slot lower bound
// is NOT Omega(L) over accepted packets; min slots over accepted length-L packets is O(1)
// in L (here 98). Upper envelope remains linear by the 543 family.
const fs=require('fs'),os=require('os'),path=require('path'),crypto=require('crypto');
const assert=require('assert/strict');const {spawnSync}=require('child_process');
const root=path.resolve(__dirname,'../..');
const original=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedPath=path.join(root,'results/raw/arc/2026-11-11_0336_LSPV4_540_OWNER_FACET_CROSS_CONE_ACCEPTED.json');
function blob(p){const b=fs.readFileSync(p);return crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex')}
const checkerBlob=blob(original), seedBlob=blob(seedPath);
assert.equal(checkerBlob,'338305c0ce101704205e57543756b8127074a986','checker blob drift');
assert.equal(seedBlob,'25b5c1f95734f6eae36bdbb4a17c948c00753cff','seed blob drift');
const seed=JSON.parse(fs.readFileSync(seedPath,'utf8'));
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-488-'));
function extend(k){const d=structuredClone(seed);
  const f=Array.from({length:k},()=>({kind:'DEF',c:[1,-8],parents:[],gate:0}));
  d.records=f.concat(d.records.map(r=>({...r,parents:r.parents.map(n=>n+k)})));
  d.summary.def_views+=k;d.summary.live_records+=k;return d}
function run(text,tag){const f=path.join(temp,tag+'.json');fs.writeFileSync(f,text);
  const t0=process.hrtime.bigint();
  const p=spawnSync(process.execPath,[original,f],{encoding:'utf8',timeout:25000,maxBuffer:4*1024*1024});
  const ms=Number(process.hrtime.bigint()-t0)/1e6;
  const ok=p.status===0&&!p.error;let out=null;
  if(ok)out=JSON.parse(p.stdout.trim().split('\n').filter(Boolean).at(-1));
  return {ok,out,ms:Math.round(ms),err:ok?null:(p.error?String(p.error):p.stderr.trim().split('\n').find(l=>/^[A-Za-z]*Error:/.test(l))||'nonzero')}}
const rows=[],controls=[];
try{
 const pads=[0,1000,10000,100000,1000000];
 for(const fam of ['Q','S'])for(const m of pads){
  const d=structuredClone(seed);const s='a'.repeat(m);
  if(fam==='Q')d.pad=s;else d.records[0].pad=s;
  const text=JSON.stringify(d);const c=run(text,fam+m);
  assert.equal(c.ok,true,fam+m+' rejected: '+c.err);
  assert.equal(c.out.paid,31);assert.equal(c.out.records,49);assert.equal(c.out.negativeTests,11);
  rows.push({family:fam,k:0,m,L:Buffer.byteLength(text),N:49,paid:31,slot_lb_2N:98,
    slots_per_byte:+(98/Buffer.byteLength(text)).toExponential(3),accepted:true,assertions:c.out.assertions,wall_ms:c.ms});
 }
 for(const [k,m] of [[16,100000],[128,1000000]]){
  const d=extend(k);d.pad='a'.repeat(m);const text=JSON.stringify(d);const c=run(text,'P'+k+'_'+m);
  assert.equal(c.ok,true);assert.equal(c.out.paid,31);assert.equal(c.out.records,49+k);
  rows.push({family:'P',k,m,L:Buffer.byteLength(text),N:49+k,paid:31,slot_lb_2N:2*(49+k),
    slots_per_byte:+(2*(49+k)/Buffer.byteLength(text)).toExponential(3),accepted:true,assertions:c.out.assertions,wall_ms:c.ms});
 }
 // Hostile controls: padding must not mask any defect; malformed JSON rejected.
 const base=()=>{const d=structuredClone(seed);d.pad='a'.repeat(100000);return d};
 const muts={
  bad_paid:d=>{d.summary.paid_total--}, bad_records:d=>{d.summary.live_records++},
  bad_parent:d=>{d.records.at(-1).parents[0]=d.records.length+1},
  bad_source:d=>{d.spec.charge[0]^=1}, no_owner:d=>{d.gate_defs=[]},
  pad_as_record_field_type:d=>{d.records[0].c='a'.repeat(1000)},
 };
 for(const [n,f] of Object.entries(muts)){const d=base();f(d);const c=run(JSON.stringify(d),'bad_'+n);
  assert.equal(c.ok,false,'accepted hostile '+n);controls.push({name:n,rejected:true,reason:c.err.slice(0,160)})}
 {const t=JSON.stringify(base());const bad=t.slice(0,-2)+'\u0001"}';const c=run(bad,'bad_ctrlchar');
  assert.equal(c.ok,false);controls.push({name:'malformed_control_char_in_pad',rejected:true,reason:c.err.slice(0,160)})}
 {const t=JSON.stringify(base());const c=run(t.slice(0,-1),'bad_trunc');
  assert.equal(c.ok,false);controls.push({name:'truncated_json',rejected:true,reason:c.err.slice(0,160)})}
 const minRatio=Math.min(...rows.map(r=>r.slots_per_byte));
 console.log(JSON.stringify({run:'LSPV-5/488',checker:'experiments/arc/lspv2_386_independent_verify.js',checker_blob:checkerBlob,
  seed_blob:seedBlob,node:process.version,mode:'OS Node subprocess, unchanged original CLI',rows,controls,
  min_slots_per_byte:minRatio,all_passed:true,
  caveat:'Slot counts are source-code JS reference-slot bounds, not RSS/heap bytes; wall_ms is implementation timing only; no SAT or proof-language lower bound.'},null,1));
}finally{fs.rmSync(temp,{recursive:true,force:true})}
