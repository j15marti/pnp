#!/usr/bin/env node
'use strict';
// LSPV-1/581 original /386 CLI replay. Node >= 18. Run from the repository root.
// node experiments/arc/lspv1_581_two_fresh_signed_weakening.cjs
const assert=require('node:assert/strict');
const fs=require('node:fs'),crypto=require('node:crypto'),os=require('node:os');
const path=require('node:path'),cp=require('node:child_process');
const root=path.resolve(__dirname,'../..');
const verifier=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const original=path.join(root,'results/raw/arc/2026-11-11_1200_LSPV1_579_BRIDGE_DP_W61.json');
const witness=path.join(root,'results/raw/arc/2026-11-11_1400_LSPV1_581_TWO_FRESH_WEAKENING_ACCEPTED.json');
const clone=x=>JSON.parse(JSON.stringify(x));
const key=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function gitBlob(file){const b=fs.readFileSync(file);return crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');}
assert.equal(gitBlob(verifier),'338305c0ce101704205e57543756b8127074a986');
assert.equal(gitBlob(original),'807aaf7b7cf5e4a4feb29c2599f9e582ea140e30');
const seed=JSON.parse(fs.readFileSync(original,'utf8'));
function make(){
 const p=clone(seed);p.gate_defs.push([1,18,1,2],[2,19,1,-3]);
 const last=p.records.pop();
 assert.deepEqual(p.records[13].c,[1,-4,6,-16]);
 p.records.push(
 {kind:'DEF',c:key([-1,-2,18]),parents:[],gate:1},
 {kind:'DEF',c:key([1,-18]),parents:[],gate:1},
 {kind:'RES',c:key([-2,-4,6,-16,18]),parents:[13,100],pivot:1},
 {kind:'RES',c:key([1,-2,-4,6,-16]),parents:[102,101],pivot:18},
 {kind:'DEF',c:key([-1,3,19]),parents:[],gate:2},
 {kind:'DEF',c:key([1,-19]),parents:[],gate:2},
 {kind:'RES',c:key([-2,3,-4,6,-16,19]),parents:[103,104],pivot:1},
 {kind:'RES',c:key([1,-2,3,-4,6,-16]),parents:[106,105],pivot:19},
 last);
 p.summary={source:41,resolution:64,def_views:4,paid_gates:3,paid_total:67,live_records:109};
 return p;
}
const packet=make();
const bytes=JSON.stringify(packet);
assert.equal(bytes,fs.readFileSync(witness,'utf8'),'witness byte mismatch');
assert.equal(packet.records.length,109);
assert.deepEqual(packet.records.slice(0,41),seed.records.slice(0,41));
assert.deepEqual(packet.records.at(-1),seed.records.at(-1));
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv1-581-'));
function native(name,p,expected){
 const file=path.join(tmp,name+'.json');
 fs.writeFileSync(file,JSON.stringify(p));
 const run=cp.spawnSync(process.execPath,[verifier,file],{encoding:'utf8',timeout:25000});
 const accepted=run.status===0;
 assert.equal(accepted,expected,name+' unexpected original CLI result: '+run.stderr);
 let data=null;if(accepted){data=JSON.parse(run.stdout.trim().split('\n').at(-1));assert.equal(data.negativeTests,11);}
 return {name,expected,accepted,checks:data?.assertions??null,paid:data?.paid??null,rejection:accepted?null:run.stderr.trim().slice(-240)};
}
const cases=[
 ['baseline_579',seed,true],
 ['two_fresh_owners',packet,true],
 ['bad_facet_1',q=>{q.records[100].c=[-1,2,18]},false],
 ['bad_res_pivot_18',q=>{q.records[103].pivot=-18},false],
 ['bad_facet_2',q=>{q.records[104].c=[-1,-3,19]},false],
 ['forward_parent',q=>{q.records[106].parents[1]=108},false],
 ['undercharge',q=>{q.summary.paid_total=66},false],
 ['undefined_facet_owner',q=>{q.records[105].gate=9},false],
 ['owner_wire_collision',q=>{q.gate_defs[2][1]=18},false],
 ['source_forgery',q=>{q.records[13].c=[1,2,6,-16]},false],
 ['wrong_last_resolvent',q=>{q.records[107].c=[1,-2,-4,6,-16]},false],
 ['wrong_terminal_parent',q=>{q.records.at(-1).parents=[40,107]},false]
];
try{
 const results=cases.map(([name,arg,expected])=>{
  const p=typeof arg==='function'?clone(packet):arg;
  if(typeof arg==='function')arg(p);
  return native(name,p,expected);
 });
 console.log(JSON.stringify({status:'COMPUTATIONAL original OS Node CLI',checker_sha:gitBlob(verifier),seed_sha:gitBlob(original),witness_sha:gitBlob(witness),bytes:Buffer.byteLength(bytes),cases:results},null,2));
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
