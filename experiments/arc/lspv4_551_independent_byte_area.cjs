'use strict';
// LSPV-4/551 independent exact W61 fixed-DAG lexicographic area optimizer.
// Native checked proof system: archived /386 SOURCE/paid-AND2/RES sibling only.
// Run: node experiments/arc/lspv4_551_independent_byte_area.cjs [--native-check]
const fs=require('fs'),crypto=require('crypto'),cp=require('child_process');
const assert=require('assert').strict;
const SOURCE='results/raw/arc/2026-11-11_1236_LSPV4_549_BRIDGE_W61_BYTE_SAFE_FIVE_SLOT.json';
const OLD='results/raw/arc/2026-11-11_1331_LSPV4_550_W61_MINAREA_FIVE_SLOT_ACCEPTED.json';
const BYTE='results/raw/arc/2026-11-11_1436_LSPV4_551_W61_MIN_BYTE_AREA_FIVE_SLOT_ACCEPTED.json';
const SLOT='results/raw/arc/2026-11-11_1436_LSPV4_551_W61_MIN_SLOT_THEN_BYTE_AREA_ACCEPTED.json';
const CHECKER='experiments/arc/lspv2_386_independent_verify.js';
const hashes={
 [SOURCE]:'d12f02d2b665c172f806f09e23770d9b76980172',
 [OLD]:'cbc7044e84bac8e4e1683a2f1637c98f632bdb14',
 [BYTE]:'a975b7ec8a095421f78bf2567f442b587b5d2596',
 [SLOT]:'fb5556522e5b476345a6dc30bad14d628e23cebf',
 [CHECKER]:'338305c0ce101704205e57543756b8127074a986'
};
function blob(bytes){return crypto.createHash('sha1').update('blob '+bytes.length+'\0').update(bytes).digest('hex');}
function source(p){const b=fs.readFileSync(p);assert.equal(blob(b),hashes[p]);return JSON.parse(b.toString());}
const original=source(SOURCE),baseline=source(OLD),byteProof=source(BYTE),slotProof=source(SLOT);
assert.equal(blob(fs.readFileSync(CHECKER)),hashes[CHECKER]);
const n0=41, N=60, R=original.records.slice(n0);
assert.equal(original.records.length,101);
const bits=Array.from({length:N},(_,i)=>1n<<BigInt(i)),ALL=(1n<<BigInt(N))-1n;
const P=R.map(r=>r.parents.filter(p=>p>=n0).map(p=>p-n0));
const pred=P.map(ps=>ps.reduce((m,p)=>m|bits[p],0n));
const succ=Array(N).fill(0n);
for(let i=0;i<N;i++)for(const p of P[i]){assert(p<i);succ[p]|=bits[i];}
const W=R.map(r=>JSON.stringify(r.c).length);
const canon=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function replay(proof){
 assert.deepEqual(proof.spec,original.spec);
 assert.deepEqual(proof.gate_defs,original.gate_defs);
 assert.deepEqual(proof.summary,original.summary);
 assert.deepEqual(proof.records.slice(0,n0),original.records.slice(0,n0));
 const out=[];
 proof.records.forEach((r,i)=>{
  assert.deepEqual(r.c,canon(r.c),'noncanonical '+i);
  if(i<n0){assert.equal(r.kind,'SOURCE');assert.deepEqual(r.parents,[]);}
  else{
   assert.equal(r.kind,'RES');const [a,b]=r.parents;
   assert(a<i&&b<i&&a>=0&&b>=0,'parent '+i);
   assert(out[a].includes(r.pivot)&&out[b].includes(-r.pivot),'pivot '+i);
   const result=canon([...out[a].filter(x=>x!==r.pivot),
                     ...out[b].filter(x=>x!==-r.pivot)]);
   assert(!result.some(x=>result.includes(-x)),'taut '+i);
   assert.deepEqual(r.c,result,'resolvent '+i);
  }
  out.push(r.c);
 });
 assert.deepEqual(out.at(-1),[]);
}
const signature=(p,r)=>JSON.stringify([r.c,r.pivot,r.parents.map(j=>p.records[j].c)]);
const lookup=new Map(R.map((r,i)=>[signature(original,r),i]));
assert.equal(lookup.size,60);
function orderOf(p){
 replay(p);
 const o=p.records.slice(n0).map(r=>lookup.get(signature(p,r)));
 assert.deepEqual([...o].sort((a,b)=>a-b),Array.from({length:N},(_,i)=>i));
 return o;
}
function metrics(order){
 let mask=0n,byteSteps=0,slotSteps=0,peakBytes=0,peakSlots=0;
 for(const i of order){
  const un=ALL^mask,live=[];
  for(let j=0;j<N;j++)if((mask&bits[j])&&(succ[j]&un))live.push(j);
  const b=live.reduce((s,j)=>s+W[j],0);
  const safe=P[i].some(j=>(succ[j]&un)===bits[i]&&W[j]>=W[i]);
  assert(live.length+Number(!safe)<=5);
  byteSteps+=b;slotSteps+=live.length;
  peakBytes=Math.max(peakBytes,b+(safe?0:W[i]));
  peakSlots=Math.max(peakSlots,live.length+Number(!safe));
  mask|=bits[i];
 }
 assert.equal(mask,ALL);
 return {byteSteps,slotSteps,peakBytes,peakSlots};
}
function optimum(type){
 const start=Date.now(),queue=[0n],best=new Map([[0n,[0,0]]]),back=new Map();
 let ready=0,legal=0,relaxed=0;
 for(let h=0;h<queue.length;h++){
  const mask=queue[h],un=ALL^mask,live=[];
  for(let j=0;j<N;j++)if((mask&bits[j])&&(succ[j]&un))live.push(j);
  const b=live.reduce((s,j)=>s+W[j],0),step=type==='bytes'?[b,live.length]:[live.length,b];
  const old=best.get(mask),candidate=[old[0]+step[0],old[1]+step[1]];
  for(let i=0;i<N;i++){
   if((mask&bits[i])||(pred[i]&un))continue;
   ready++;
   const safe=P[i].some(p=>(succ[p]&un)===bits[i]&&W[p]>=W[i]);
   if(live.length+Number(!safe)>5)continue;
   legal++;
   const to=mask|bits[i],previous=best.get(to);
   if(!previous||candidate[0]<previous[0]||
       (candidate[0]===previous[0]&&candidate[1]<previous[1])){
     if(!previous)queue.push(to);
     best.set(to,candidate);back.set(to,[mask,i]);relaxed++;
   }
  }
 }
 const order=[];let m=ALL;
 while(m){const [prev,i]=back.get(m);order.push(i);m=prev;}
 order.reverse();
 return {objective:type,cost:best.get(ALL),states:best.size,ready,legal,relaxed,order,
         metrics:metrics(order),elapsedSeconds:(Date.now()-start)/1000};
}
const by=optimum('bytes'),sl=optimum('slots');
assert.deepEqual(by.cost,[1925,157]);
assert.deepEqual(sl.cost,[156,1930]);
for(const r of [by,sl]){
 assert.equal(r.states,1129302);assert.equal(r.ready,12982502);assert.equal(r.legal,4107280);
}
assert.deepEqual(orderOf(byteProof),by.order);
assert.deepEqual(orderOf(slotProof),sl.order);
const prior=metrics(orderOf(baseline));
assert.equal(prior.byteSteps,1995);assert.equal(prior.slotSteps,156);
assert.equal(by.metrics.peakSlots,5);assert.equal(sl.metrics.peakSlots,5);
const native={performed:process.argv.includes('--native-check')};
if(native.performed){
 native.results={};
 for(const p of [OLD,BYTE,SLOT]){
  const rr=cp.spawnSync(process.execPath,[CHECKER,p],{encoding:'utf8',maxBuffer:1048576});
  assert.equal(rr.status,0,rr.stderr||('native rejection '+p));
  const j=JSON.parse(rr.stdout.trim());
  assert.equal(j.paid,61);assert.equal(j.negativeTests,11);
  native.results[p]=j;
 }
}
console.log(JSON.stringify({checker:'archived /386 only',by,sl,old550:prior,native,
 historical_R_mix341_authenticated:false},null,2));
