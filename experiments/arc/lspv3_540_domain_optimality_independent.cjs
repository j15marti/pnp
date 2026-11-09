#!/usr/bin/env node
'use strict';
/* Independently written verifier of LSPV3/540 local factor-domain lower bound.
   Rebuilds all strict 3-literal source facets from valuations, independently
   computes every 3-var factor, tests all distinguishing singleton contexts.
   Not an execution of historical R_mix341 checker. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
let tests = 0;
function ck(x,y,msg){tests++; assert.equal(x,y,msg)}
const bits = [1,2,4];
function literalsExcluding(assignment){return bits.map((b,i)=>((assignment & b)?-1:1)*(i+1))}
function evaluateClause(lits,v){return lits.some(l=>(Boolean(v & (1 << (Math.abs(l)-1)))===Boolean(l>0)))}
function factor(mask) {
 assert.ok(Number.isInteger(mask) && mask>=0 && mask<=254);
 const excluded=[];
 for(let p=0;p<8;p++) if(!(mask&(1<<p))) excluded.push(p);
 const records=[];
 for(const p of excluded){
   let clause=literalsExcluding(p), m=0;
   for(let v=0;v<8;v++) if(evaluateClause(clause,v)) m|=1<<v;
   records.push({id:'s'+p,tag:'SOURCE',mask:m,source:['s'+p],parents:[],clause});
 }
 let current=records[0];
 for(let i=1;i<excluded.length;i++){
   const next={id:'a'+i,tag:'AND3',mask:(current.mask & records[i].mask),parents:[current.id,records[i].id],source:[...new Set([...current.source,...records[i].source])].sort()};
   records.push(next);current=next;
 }
 return {records,root:current,paid:excluded.length-1};
}
function verify(proof){
 const known=new Map();let q=0;
 for(const e of proof.records){
   ck(known.has(e.id),false,'duplicate node');
   if(e.tag==='SOURCE'){
     ck(e.clause.length,3);
     ck(new Set(e.clause.map(x=>Math.abs(x))).size,3);
     let expected=0;
     for(let val=0;val<8;val++) if(evaluateClause(e.clause,val)) expected|=1<<val;
     ck(e.mask,expected,'source facet');ck(JSON.stringify(e.source),JSON.stringify([e.id]));
   }else if(e.tag==='AND3') {
     ck(e.parents.length,2);
     const [a,b]=e.parents.map(p=>known.get(p));
     ck(!!a,true);ck(!!b,true);
     ck(e.mask,a.mask & b.mask,'paid join');
     ck(JSON.stringify(e.source),JSON.stringify([...new Set([...a.source,...b.source])].sort()));q++;
   }else{throw Error('unsupported tag');}
   known.set(e.id,e);
 }
 ck(q,proof.paid);ck(known.has(proof.root.id),true);
}
let all = []; for(let i=0;i<255;i++) {let v=factor(i); verify(v);ck(v.root.mask,i);all.push(v)}
let singleton=[];for(let p=0;p<8;p++) {let v=factor(1<<p);verify(v);ck(v.paid,6);singleton.push(v)}
let pairCount=0;
for(let a=0;a<255;a++)for(let b=a+1;b<255;b++){
 const witness = Array.from({length:8},(_,i)=>i).find(i=>Boolean(a&(1<<i)) !== Boolean(b&(1<<i)));
 ck(witness===undefined,false);
 const C=singleton[witness].root.mask;
 ck((a&C)===0,(b&C)!==0,'nonempty observations must differ');
 ck(C,1<<witness);
 pairCount++;
}
ck(pairCount,32385);
ck((105 & 1),1);ck((104 & 1),0);
ck(all[105].paid,3);ck(all[104].paid,4);
let rejected=0;
let bad=factor(105);bad.records.at(-1).mask ^= 1;
try{verify(bad)}catch{rejected++}
bad=factor(105);bad.records.at(-1).parents[0]='external:999999999999999999999';
try{verify(bad)}catch{rejected++}
bad=factor(105);bad.records[0].source=['corrupted'];
try{verify(bad)}catch{rejected++}
bad=factor(105);bad.records.at(-1).id=bad.records[0].id;
try{verify(bad)}catch{rejected++}
bad=factor(105);bad.records[0].clause=[1,2,3];
try{verify(bad)}catch{rejected++}
ck(rejected,5);
const data={method:'independent Node.js exact source reconstruction and membership tests',pairCount, nonTrueFactors:all.length, singletonContexts:singleton.length,minimumBits:Math.ceil(Math.log2(all.length)), checks:tests, corruptRejected:rejected,peakRSSKiB:Math.round(process.memoryUsage().rss/1024),node:process.version};
console.log(JSON.stringify(data,null,2));
if (process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(data,null,2)+'\n');
