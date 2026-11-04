#!/usr/bin/env node
'use strict';
// LSPV-3/402 original-variable support mismatch, independent strict verifier.
// node experiments/arc/lspv3_402_typed_and3_transfer_verify.js
const assert=require('assert/strict');
let count=0;
const gates=[[5,1,2],[6,5,3],[7,6,4],[8,7,-4]];
const sign=(l,v)=>(l>0?v[Math.abs(l)]:!v[Math.abs(l)]);
const facets=(z,a,b)=>[[-z,a],[-z,b],[z,-a,-b]];
const C=gates.flatMap(g=>facets(...g));
const sat=(cl,v)=>cl.some(l=>sign(l,v));
const proof=[[[8],[-8,7],8,[7]],[[8],[-8,-4],8,[-4]],[[-4],[-7,4],-4,[-7]]];
function res(a,b,p){
  if(!a.includes(p)||!b.includes(-p))throw Error('bad pivot');
  const c=[...new Set(a.filter(x=>x!==p).concat(b.filter(x=>x!==-p)))];
  if(c.some(x=>c.includes(-x)))throw Error('tautology');
  return c.sort((a,b)=>a-b);
}
for(const [a,b,p,out] of proof){assert.deepEqual(res(a,b,p),out);count++;}
for(let mask=0;mask<16;mask++){
  const v={};for(let j=1;j<=4;j++)v[j]=!!(mask&(1<<(j-1)));
  for(const [z,a,b] of gates)v[z]=sign(a,v)&&sign(b,v);
  for(const cl of C){assert(sat(cl,v));count++;}
  assert.equal(v[7],v[1]&&v[2]&&v[3]&&v[4]);count++;
  assert.equal(v[8],false);count++;
}
for(let mask=0;mask<256;mask++){
  const v={};for(let j=1;j<=8;j++)v[j]=!!(mask&(1<<(j-1)));
  assert(!([8].every(x=>sign(x,v))&&C.every(cl=>sat(cl,v))));count++;
}
for(let i=1;i<=4;i++){
  const all={1:true,2:true,3:true,4:true};
  for(const [z,a,b] of gates)all[z]=sign(a,all)&&sign(b,all);
  const off={1:true,2:true,3:true,4:true};off[i]=false;
  for(const [z,a,b] of gates)off[z]=sign(a,off)&&sign(b,off);
  assert.notEqual(all[7],off[7]);count++;
}
assert.deepEqual(res([7],[-7],7),[]);count++;
let fails=0;
for(const [a,b,p] of [[[8],[-8,7],7],[[8],[-8,7],-8],[[-8,7],[-8,-4],7]])
  try{res(a,b,p)}catch(e){fails++;}
assert.equal(fails,3);
console.log(JSON.stringify({
 schema:'LSPV3/402-independent-JS',status:'COMPUTATIONAL',checks:count,
 corrupt_pivots_rejected:fails,source_original_support:[7],
 retracted_original_support:[1,2,3,4],final_AND3_type_preserved:false,
 alternative_RES_last_node:true
},null,2));
