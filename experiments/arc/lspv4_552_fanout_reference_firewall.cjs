#!/usr/bin/env node
'use strict';
// LSPV-4/552, execute in a complete j15marti/pnp checkout.
// node experiments/arc/lspv4_552_fanout_reference_firewall.cjs
// node experiments/arc/lspv4_552_fanout_reference_firewall.cjs --native
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const cp=require('node:child_process'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const file=path.join(root,'results/raw/arc/2026-11-11_1436_LSPV4_551_W61_MIN_SLOT_THEN_BYTE_AREA_ACCEPTED.json');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const raw=fs.readFileSync(file),d=JSON.parse(raw);
const S=41,R=60;
assert.equal(d.records.length,S+R);
assert.equal(d.summary.paid_total,61);
assert.equal(d.summary.source,S);
assert.equal(d.summary.resolution,R);
assert.equal(d.gate_defs.length,1);
assert.ok(d.records.slice(0,S).every(r=>r.kind==='SOURCE'));
assert.ok(d.records.slice(S).every(r=>r.kind==='RES'));
const cmp=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function replay(obj){
 const seen=[];
 for(let i=0;i<obj.records.length;i++){
  const r=obj.records[i];assert.deepEqual(r.c,cmp(r.c));
  assert.ok(r.c.every(x=>!r.c.includes(-x)));
  assert.ok(r.parents.every(j=>Number.isSafeInteger(j)&&j>=0&&j<i));
  if(r.kind==='RES'){
   assert.equal(r.parents.length,2);
   const A=seen[r.parents[0]],B=seen[r.parents[1]];
   assert.ok(A.includes(r.pivot)&&B.includes(-r.pivot));
   assert.deepEqual(r.c,cmp([...A.filter(x=>x!==r.pivot),...B.filter(x=>x!==-r.pivot)]));
  }
  seen.push(r.c);
 }
 assert.deepEqual(seen.at(-1),[]);
}
const fan=Array(S+R).fill(0);
d.records.forEach(r=>r.parents.forEach(i=>fan[i]++));
assert.ok(fan.slice(S,-1).every(x=>x===1));
assert.equal(fan.at(-1),0);
const sourceRefs=d.records.slice(S).flatMap(r=>r.parents).filter(i=>i<S);
const resultRefs=d.records.slice(S).flatMap(r=>r.parents).filter(i=>i>=S);
assert.equal(sourceRefs.length,61);
assert.equal(resultRefs.length,59);
const sumDigits=xs=>xs.reduce((a,j)=>a+String(j).length,0);
const sourceDigits=sumDigits(sourceRefs);
const resultDigits=sumDigits(resultRefs);
const predicted=sourceDigits+sumDigits(Array.from({length:R-1},(_,i)=>S+i));
assert.equal(sourceDigits,108);
assert.equal(resultDigits,118);
assert.equal(predicted,226);
const native=process.argv.includes('--native');
let rng=0x552cad;function rnd(){rng=(Math.imul(rng,1664525)+1013904223)>>>0;return rng/4294967296}
function reorder(mode){
 const done=new Set(Array.from({length:S},(_,i)=>i));
 const pending=new Set(Array.from({length:R},(_,i)=>S+i));
 const map=new Map(Array.from({length:S},(_,i)=>[i,i])),res=[],order=[];
 while(pending.size){
  const ready=[...pending].filter(i=>d.records[i].parents.every(j=>done.has(j)));
  assert.ok(ready.length);
  const i=mode==='first'?ready[0]:mode==='last'?ready.at(-1):ready[Math.floor(rnd()*ready.length)];
  const r=d.records[i];res.push({...r,parents:r.parents.map(j=>map.get(j))});
  order.push(i);map.set(i,S+res.length-1);pending.delete(i);done.add(i);
 }
 const obj={...d,records:d.records.slice(0,S).concat(res)};
 replay(obj);
 const refs=res.flatMap(r=>r.parents);
 assert.equal(sumDigits(refs),predicted);
 assert.equal(Buffer.byteLength(JSON.stringify(obj)+'\n'),raw.length);
 return {obj,order};
}
replay(d);
const first=reorder('first'),last=reorder('last');
for(let i=0;i<2001;i++)reorder('random');
// Combinatorial nonnative control: one paid node reused twice across the 9/10 index boundary.
function counter(order){
 const ix=new Map(Array.from({length:9},(_,i)=>['s'+i,i]));
 const graph={a:['s0','s1'],b:['s2','s3'],c:['a','s4'],sink:['a','c']};
 let digits=0;
 for(const v of order){for(const p of graph[v]){assert.ok(ix.has(p));digits+=String(ix.get(p)).length}ix.set(v,ix.size)}
 return digits;
}
assert.equal(counter(['a','b','c','sink']),9);
assert.equal(counter(['b','a','c','sink']),11);
let checkerOutput=null;
if(native){
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-552-'));
 try{
  checkerOutput=[];
  for(const [tag,obj] of [['first',first.obj],['last',last.obj]]){
   const p=path.join(tmp,tag+'.json');fs.writeFileSync(p,JSON.stringify(obj)+'\n');
   const run=cp.spawnSync(process.execPath,[checker,p],{encoding:'utf8',timeout:60000});
   assert.equal(run.status,0,run.stderr);
   checkerOutput.push({tag,stdout:run.stdout.trim(),accepted:true});
  }
  const bad=structuredClone(first.obj);bad.summary.paid_total--;
  const p=path.join(tmp,'bad.json');fs.writeFileSync(p,JSON.stringify(bad)+'\n');
  const run=cp.spawnSync(process.execPath,[checker,p],{encoding:'utf8',timeout:60000});
  assert.notEqual(run.status,0,'native checker accepted underpayment');
  checkerOutput.push({tag:'underpayment',accepted:false});
 }finally{fs.rmSync(tmp,{recursive:true,force:true})}
}
console.log(JSON.stringify({id:'LSPV-4/552',src:S,res:R,paid:61,source_refs:61,result_refs:59,
 source_digits:108,result_digits:118,reference_digits:226,packet_bytes:raw.length,
 topological_replays:2003,early_prefix:first.order.slice(0,15),late_prefix:last.order.slice(0,15),
 nonnative_shared_control:{reference_digits_early:9,reference_digits_late:11},
 original_native_os_checker:native?checkerOutput:'not executed (pass --native)'},null,2));
