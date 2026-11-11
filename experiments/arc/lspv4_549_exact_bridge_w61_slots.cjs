'use strict';
// LSPV-4/549: source-fixed archived /386 proof-DAG resource audit.
// Run in repository root: node experiments/arc/lspv4_549_exact_bridge_w61_slots.cjs
// Requires Node 18+; pinned exact original /386 CLI is invoked as a subprocess.
const fs=require('fs'),crypto=require('crypto'),os=require('os'),path=require('path'),cp=require('child_process'),assert=require('assert').strict;
const BASE='results/raw/arc/2026-11-11_1200_LSPV1_579_BRIDGE_DP_W61.json';
const WITNESS='results/raw/arc/2026-11-11_1236_LSPV4_549_BRIDGE_W61_BYTE_SAFE_FIVE_SLOT.json';
const CHECKER='experiments/arc/lspv2_386_independent_verify.js';
const SHAS={
 [BASE]:'807aaf7b7cf5e4a4feb29c2599f9e582ea140e30',
 [WITNESS]:'d12f02d2b665c172f806f09e23770d9b76980172',
 [CHECKER]:'338305c0ce101704205e57543756b8127074a986'
};
function hash(b){return crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex')}
function read(f){const b=fs.readFileSync(f);assert.equal(hash(b),SHAS[f],'PINNED ORIGINAL BYTES CHANGED '+f);return JSON.parse(b.toString('utf8'))}
const old=read(BASE),now=read(WITNESS),checkerText=fs.readFileSync(CHECKER);
assert.equal(hash(checkerText),SHAS[CHECKER]);
const n0=41,NR=60;
const identity=x=>JSON.stringify(x);
assert.equal(identity(old.spec),identity(now.spec));
assert.equal(identity(old.records.slice(0,n0)),identity(now.records.slice(0,n0)));
assert.equal(identity(old.gate_defs),identity(now.gate_defs));
assert.equal(identity(old.summary),identity(now.summary));
assert.equal(now.records.length,101);
assert.equal(now.summary.paid_total,61);
assert.equal(now.summary.resolution,60);
assert.equal(now.summary.paid_gates,1);
assert.equal(now.summary.source,41);
function canon(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}
function replay(p){
 const known=[];
 for(let i=0;i<p.records.length;i++){
  const r=p.records[i];assert.equal(identity(r.c),identity(canon(r.c)),'clause canonical '+i);
  if(i<n0){assert.equal(r.kind,'SOURCE');assert.deepEqual(r.parents,[]);}
  else {
   assert.equal(r.kind,'RES');
   assert.equal(r.parents.length,2);
   assert(r.parents.every(x=>Number.isInteger(x)&&x>=0&&x<i),'parents '+i);
   const [a,b]=r.parents.map(j=>known[j]),v=r.pivot;
   assert(Number.isInteger(v)&&v!==0&&a.includes(v)&&b.includes(-v),'pivot '+i);
   const c=canon([...a.filter(x=>x!==v),...b.filter(x=>x!==-v)]);
   assert(!c.some(x=>c.includes(-x)),'tautology '+i);
   assert.equal(identity(c),identity(r.c),'resolvent '+i);
  }
  known.push(r.c);
 }
 assert.deepEqual(known.at(-1),[]);
 return true;
}
replay(old);replay(now);
const key=r=>identity({c:r.c,pivot:r.pivot,pa:r.parents.map(i=>old.records[i]?.c)});
function signatures(p){return p.records.slice(n0).map(r=>identity({c:r.c,pivot:r.pivot,parentClauses:r.parents.map(i=>p.records[i].c)})).sort()}
assert.deepEqual(signatures(now),signatures(old),'paid node identities changed');
const rows=now.records.slice(n0),n=rows.length,bits=Array.from({length:n},(_,i)=>1n<<BigInt(i)),all=(1n<<BigInt(n))-1n;
const pred=rows.map(r=>r.parents.filter(k=>k>=n0).reduce((s,k)=>s|bits[k-n0],0n));
const succ=Array(n).fill(0n);
for(let i=0;i<n;i++)for(const j of rows[i].parents.filter(k=>k>=n0).map(k=>k-n0))succ[j]|=bits[i];
const w=rows.map(r=>JSON.stringify(r.c).length);
function live(mask){const un=all^mask;let L=[];for(let j=0;j<n;j++)if((mask&bits[j])&&(succ[j]&un))L.push(j);return L}
function reuse(mask,i,mode){const un=all^mask;return rows[i].parents.filter(p=>p>=n0).map(p=>p-n0).find(j=>(succ[j]&un)===bits[i]&&(mode!=='byte'||w[j]>=w[i]))}
function schedule(p){
 const R=p.records.slice(n0),b=Array.from({length:n},(_,i)=>1n<<BigInt(i)),S=Array(n).fill(0n);
 for(let i=0;i<n;i++)for(const pr of R[i].parents)if(pr>=n0)S[pr-n0]|=b[i];
 let mask=0n,peaks={fresh:0,inplace:0,byte:0},signed=0,byteValue=0,area=0,eligible=0;
 for(let i=0;i<n;i++){
  const un=all^mask,ls=[];for(let j=0;j<n;j++)if((mask&b[j])&&(S[j]&un))ls.push(j);
  const ends=R[i].parents.filter(j=>j>=n0).map(j=>j-n0).filter(j=>(S[j]&un)===b[i]);
  const safe=ends.filter(j=>JSON.stringify(R[j].c).length>=JSON.stringify(R[i].c).length);
  const l=ls.length;area+=l;eligible+=Number(safe.length>0);
  peaks.fresh=Math.max(peaks.fresh,l+1);
  peaks.inplace=Math.max(peaks.inplace,l+Number(ends.length===0));
  peaks.byte=Math.max(peaks.byte,l+Number(safe.length===0));
  signed=Math.max(signed,ls.reduce((s,j)=>s+R[j].c.length,0)+(safe.length?0:R[i].c.length));
  byteValue=Math.max(byteValue,ls.reduce((s,j)=>s+JSON.stringify(R[j].c).length,0)+(safe.length?0:JSON.stringify(R[i].c).length));
  mask|=b[i];
 }
 return {peaks,liveArea:area,eligibleNonexpanding:eligible,peakSignedLiteralPayload:signed,peakSerializedClausePayload:byteValue};
}
function exhaustive(cap,mode){
 let q=[0n],seen=new Set(q),head=0,edges=0,furthest=0;
 while(head<q.length){
  const mask=q[head++],un=all^mask,ls=live(mask);if(mask===all)return {cap,mode,completed:true,states:seen.size,transitions:edges,furthest:n};
  let k=0;for(let x=mask;x;x&=x-1n)k++;furthest=Math.max(furthest,k);
  for(let i=0;i<n;i++){
   if((mask&bits[i])||(pred[i]&un))continue;
   const cost=ls.length+Number(mode==='fresh'||reuse(mask,i,'inplace')===undefined);
   if(cost>cap)continue;edges++;const nm=mask|bits[i];
   if(!seen.has(nm)){seen.add(nm);q.push(nm);}
  }
 }
 return {cap,mode,completed:false,states:seen.size,transitions:edges,furthest};
}
const f5=exhaustive(5,'fresh'),i4=exhaustive(4,'inplace'),a=schedule(old),b=schedule(now);
assert.deepEqual([f5.completed,f5.states,f5.transitions,f5.furthest],[false,993927,2185554,52]);
assert.deepEqual([i4.completed,i4.states,i4.transitions,i4.furthest],[false,181387,590930,51]);
assert.deepEqual(b.peaks,{fresh:6,inplace:5,byte:5});
assert.equal(b.eligibleNonexpanding,36);
assert.deepEqual(a.peaks,{fresh:10,inplace:9,byte:10});
function run(f){return cp.spawnSync(process.execPath,[CHECKER,f],{encoding:'utf8',maxBuffer:1024*1024})}
for(const f of [BASE,WITNESS]){
 const x=run(f);assert.equal(x.status,0,'original OS /386 checker did not accept '+f+' '+x.stderr);
 assert(x.stdout.includes('"paid":61')&&x.stdout.includes('"negativeTests":11'),'original CLI output '+x.stdout);
}
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-549-'));
let rejected=0;
try{
 const changes=[
  p=>{p.records[0].c=[-p.spec.guard]},
  p=>{p.summary.paid_total=60},
  p=>{p.records.at(-1).parents[0]=p.records.length+10},
  p=>{p.records.at(-1).pivot=999999},
  p=>{p.records.at(-1).c=[1]}
 ];
 for(let i=0;i<changes.length;i++){
  const m=structuredClone(now);changes[i](m);
  const f=path.join(dir,'invalid'+i+'.json');fs.writeFileSync(f,JSON.stringify(m)+'\n');
  const x=run(f);assert.notEqual(x.status,0,'original OS checker accepted hostile '+i);rejected++;
 }
}finally{fs.rmSync(dir,{recursive:true,force:true})}
const out={scope:'exact original archived /386 sibling checker; full historical R_mix341 remains OPEN',source:BASE,witness:WITNESS,checker:CHECKER,work:61,resolution:60,sources:41,paidOwners:1,originalSchedule:a,newSchedule:b,exhaustive:{freshCap5:f5,inplaceCap4:i4},originalOSCliAccepts:2,originalBundledHostiles:22,extraHostilesRejected:rejected};
console.log(JSON.stringify(out,null,2));
