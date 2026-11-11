'use strict';
// LSPV-4/550, independent exact DAG shortest-area audit.
// Usage: node experiments/arc/lspv4_550_w61_byte_safe_area.js
// Original /386 sibling checker, NOT the unauthenticated historical R_mix341.
const fs=require('fs'),crypto=require('crypto'),assert=require('assert').strict;
const cp=require('child_process'),path=require('path'),os=require('os');
const BASE='results/raw/arc/2026-11-11_1236_LSPV4_549_BRIDGE_W61_BYTE_SAFE_FIVE_SLOT.json';
const NEW='results/raw/arc/2026-11-11_1331_LSPV4_550_W61_MINAREA_FIVE_SLOT_ACCEPTED.json';
const ORIGINAL='results/raw/arc/2026-11-11_1200_LSPV1_579_BRIDGE_DP_W61.json';
const CHECKER='experiments/arc/lspv2_386_independent_verify.js';
const HASH={
 [BASE]:'d12f02d2b665c172f806f09e23770d9b76980172',
 [NEW]:'cbc7044e84bac8e4e1683a2f1637c98f632bdb14',
 [ORIGINAL]:'807aaf7b7cf5e4a4feb29c2599f9e582ea140e30',
 [CHECKER]:'338305c0ce101704205e57543756b8127074a986'
};
function gitBlob(b){return crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');}
function pinned(p){let b=fs.readFileSync(p);assert.equal(gitBlob(b),HASH[p],'changed bytes: '+p);return JSON.parse(b.toString('utf8'));}
const before=pinned(BASE),after=pinned(NEW),first=pinned(ORIGINAL);
assert.equal(gitBlob(fs.readFileSync(CHECKER)),HASH[CHECKER]);
const N0=41,N=60,old=before.records.slice(N0),now=after.records.slice(N0);
assert.deepEqual(before.spec,after.spec);assert.deepEqual(before.gate_defs,after.gate_defs);
assert.deepEqual(before.summary,after.summary);
assert.deepEqual(before.records.slice(0,N0),after.records.slice(0,N0));
assert.deepEqual(first.records.slice(0,N0),after.records.slice(0,N0));
assert.equal(after.records.length,101);assert.equal(after.summary.paid_total,61);
const canon=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function replay(p){
 const seen=[];
 for(let i=0;i<p.records.length;i++){
  const r=p.records[i];assert.deepEqual(r.c,canon(r.c),'noncanonical '+i);
  if(i<N0){assert.equal(r.kind,'SOURCE');assert.deepEqual(r.parents,[]);}
  else{
   assert.equal(r.kind,'RES');assert.equal(r.parents.length,2);
   assert(r.parents.every(j=>Number.isInteger(j)&&j>=0&&j<i),'invalid parent '+i);
   const [a,b]=r.parents.map(j=>seen[j]),v=r.pivot;
   assert(Number.isInteger(v)&&v!==0&&a.includes(v)&&b.includes(-v),'pivot '+i);
   const res=canon([...a.filter(x=>x!==v),...b.filter(x=>x!==-v)]);
   assert(!res.some(x=>res.includes(-x)),'tautological '+i);
   assert.deepEqual(r.c,res,'resolvent '+i);
  }
  seen.push(r.c);
 }
 assert.deepEqual(seen.at(-1),[]);
}
replay(first);replay(before);replay(after);
const signature=p=>p.records.slice(N0).map(r=>JSON.stringify({
 c:r.c,pivot:r.pivot,parents:r.parents.map(j=>p.records[j].c)
})).sort();
assert.deepEqual(signature(after),signature(before),'changed paid RES multiset');
const bit=Array.from({length:N},(_,i)=>1n<<BigInt(i)),all=(1n<<BigInt(N))-1n;
const pred=old.map(r=>r.parents.filter(j=>j>=N0).reduce((s,j)=>s|bit[j-N0],0n));
const succ=Array(N).fill(0n),width=old.map(r=>JSON.stringify(r.c).length);
for(let i=0;i<N;i++)for(const j of old[i].parents)if(j>=N0)succ[j-N0]|=bit[i];
function popcount(m){let n=0;while(m){m&=m-1n;n++;}return n;}
function optimize(){
 const q=[0n],best=new Map([[0n,0]]),back=new Map();
 let ready=0,legal=0,relaxed=0;
 for(let head=0;head<q.length;head++){
  const mask=q[head],un=all^mask,ls=[];
  for(let j=0;j<N;j++)if((mask&bit[j])&&(succ[j]&un))ls.push(j);
  const l=ls.length,area=best.get(mask)+l;
  for(let i=0;i<N;i++){
   if((mask&bit[i])||(pred[i]&un))continue;
   ready++;
   const safe=old[i].parents.some(p=>p>=N0&&(succ[p-N0]&un)===bit[i]&&width[p-N0]>=width[i]);
   if(l+Number(!safe)>5)continue;
   legal++;
   const nm=mask|bit[i];
   if(!best.has(nm)){best.set(nm,area);back.set(nm,[mask,i]);q.push(nm);relaxed++;}
   else if(area<best.get(nm)){best.set(nm,area);back.set(nm,[mask,i]);relaxed++;}
  }
 }
 let m=all,order=[];
 while(m){assert(back.has(m));let [p,i]=back.get(m);order.push(i);m=p;}
 order.reverse();
 return {minimumArea:best.get(all),states:best.size,readyTransitions:ready,legalTransitions:legal,relaxations:relaxed,order};
}
function metrics(P){
 const R=P.records.slice(N0),succ=Array(N).fill(0n),bits=Array.from({length:N},(_,i)=>1n<<BigInt(i)),w=R.map(r=>JSON.stringify(r.c).length),all=(1n<<BigInt(N))-1n;
 for(let i=0;i<N;i++)for(const j of R[i].parents)if(j>=N0)succ[j-N0]|=bits[i];
 let area=0,areaLiterals=0,areaBytes=0,fresh=0,inplace=0,byteSafe=0,peakLiterals=0,peakBytes=0,eligible=0,refs=0;
 for(let i=0;i<N;i++){
  const mask=(1n<<BigInt(i))-1n,un=all^mask,ls=[];
  for(let j=0;j<i;j++)if(succ[j]&un)ls.push(j);
  const ends=R[i].parents.filter(j=>j>=N0).map(j=>j-N0).filter(j=>(succ[j]&un)===bits[i]);
  const safe=ends.filter(j=>w[j]>=w[i]),l=ls.length;
  const lits=ls.reduce((s,j)=>s+R[j].c.length,0),bytes=ls.reduce((s,j)=>s+w[j],0);
  area+=l;areaLiterals+=lits;areaBytes+=bytes;
  fresh=Math.max(fresh,l+1);
  inplace=Math.max(inplace,l+Number(ends.length===0));
  byteSafe=Math.max(byteSafe,l+Number(safe.length===0));
  peakLiterals=Math.max(peakLiterals,lits+(safe.length?0:R[i].c.length));
  peakBytes=Math.max(peakBytes,bytes+(safe.length?0:w[i]));
  eligible+=Number(safe.length>0);refs+=R[i].parents.length;
 }
 return {area,areaLiterals,areaCanonicalClauseBytes:areaBytes,peakFresh:fresh,
 peakInplace:inplace,peakNonexpanding:byteSafe,peakSignedLiteralPayload:peakLiterals,
 peakCanonicalClausePayloadBytes:peakBytes,eligibleNonexpanding:eligible,refCount:refs};
}
const opt=optimize(),prev=metrics(before),current=metrics(after),firstMetric=metrics(first);
const signatures=old.map(r=>JSON.stringify({c:r.c,pivot:r.pivot,parentClauses:r.parents.map(i=>before.records[i].c)}));
const S=new Map();signatures.forEach((s,i)=>{assert(!S.has(s));S.set(s,i);});
const actual=now.map(r=>S.get(JSON.stringify({c:r.c,pivot:r.pivot,parentClauses:r.parents.map(i=>after.records[i].c)})));
assert.deepEqual(actual,opt.order,'new packet is not exact optimum witness');
assert.equal(opt.minimumArea,156);assert.equal(opt.states,1129302);
assert.equal(opt.readyTransitions,12982502);assert.equal(opt.legalTransitions,4107280);
assert.equal(prev.area,234);assert.equal(current.area,156);
assert.equal(current.peakFresh,6);assert.equal(current.peakNonexpanding,5);assert.equal(current.peakCanonicalClausePayloadBytes,71);
assert.equal(current.refCount,120);
function runChecker(file){const x=cp.spawnSync(process.execPath,[CHECKER,file],{encoding:'utf8',maxBuffer:1024*1024});
 assert.equal(x.status,0,'unmodified /386 CLI failed '+file+': '+x.stderr);
 let j=JSON.parse(x.stdout.trim());assert.equal(j.paid,61);assert.equal(j.negativeTests,11);return j;}
const osChecks=[runChecker(ORIGINAL),runChecker(BASE),runChecker(NEW)];
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-550-'));
let hostiles=0;
try{
 const muts=[
  p=>p.records[0].c=[-p.spec.guard],
  p=>p.records.at(-1).pivot=999999,
  p=>p.summary.paid_total--,
  p=>p.records.at(-1).parents[0]=1000,
  p=>p.records.at(-1).c=[1]
 ];
 for(let j=0;j<muts.length;j++){
  let bad=structuredClone(after);muts[j](bad);
  const file=path.join(tmp,'hostile-'+j+'.json');fs.writeFileSync(file,JSON.stringify(bad)+'\n');
  let x=cp.spawnSync(process.execPath,[CHECKER,file],{encoding:'utf8'});
  assert.notEqual(x.status,0,'accepted hostile '+j);hostiles++;
 }
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
console.log(JSON.stringify({scope:'original /386 sibling fixed DAG; historical R_mix341 OPEN',opt,
 published549:prev,new550:current,original579:firstMetric,cliAcceptances:osChecks,
 bundledHostileRejections:33,extraHostilesRejected:hostiles},null,2));
