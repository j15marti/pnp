#!/usr/bin/env node
// LSPV-2/394 independent signed-bit exhaustive checker; zero external libraries
'use strict';
const assert=require('node:assert/strict');
const pool=[[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]];
const bad=(F,b)=>F.reduce((q,C)=>q+(C.some(x=>Boolean(b&(1<<(Math.abs(x)-1)))===(x>0))?0:1),0);
function pad(F,r){let n=F.reduce((a,C)=>Math.max(a,...C.map(Math.abs)),0);
const H=[];for(let C of F){H.push([...C]);for(let j=1;j<=r;j++){H.push([...C,n+j]);H.push([...C,-n-j]);}}return [H,n+r];}
function resolve(A,B,p){const a=new Set(A),b=new Set(B);
assert(a.has(p)&&b.has(-p)||a.has(-p)&&b.has(p));
const c=new Set([...a,...b]);c.delete(p);c.delete(-p);
for(let x of c)assert(!c.has(-x));return [...c];}
let assertions=0,sat=0,unsat=0;
for(let mask=0;mask<256;mask++){
 const F=pool.filter((c,i)=>mask&(1<<i));
 let d=4;for(let a=0;a<4;a++)d=Math.min(d,bad(F,a));
 d===0?sat++:unsat++;
 for(let r=1;r<=3;r++){
  let [H,n]=pad(F,r);assert.equal(H.length,(2*r+1)*F.length);
  assert.equal(new Set(H.map(C=>[...C].sort((a,b)=>a-b).join(','))).size,H.length);assertions+=2;
  let min=Infinity;
  for(let a=0;a<(1<<Math.max(n,2));a++){
   let q=bad(H,a);assert.equal(q,(r+1)*bad(F,a));min=Math.min(min,q);assertions++;
  }
  assert.equal(min,(r+1)*d);assertions++;
 }
}
assert.equal(sat,95);assert.equal(unsat,161);assertions+=2;
const tri=[[1,2],[-1,-2],[2,3],[-2,-3],[1,3],[-1,-3]];
const proof=tri.map(C=>[...C]);
for(let [i,j,p] of [[0,5,1],[6,3,2],[1,4,1],[8,2,2],[7,9,3]])proof.push(resolve(proof[i],proof[j],p));
assert.equal(proof.at(-1).length,0);assertions++;
for(let r=1;r<=4;r++){
 const [H,n]=pad(tri,r);let d=Infinity;
 for(let a=0;a<(1<<n);a++){d=Math.min(d,bad(H,a));assert.equal(bad(H,a),(r+1)*bad(tri,a));assertions++;}
 assert.equal(d,r+1);assertions++;
}
let malformed=0;
for(let badSource of [null,0,{},[[0]],[[1,-1]]]){
 const good=Array.isArray(badSource)&&badSource.every(C=>Array.isArray(C)&&C.length>0&&C.every(x=>Number.isInteger(x)&&x!==0)&&C.every(x=>!C.includes(-x)));
 assert.equal(good,false);malformed++;assertions++;
}
console.log(JSON.stringify({subsets:256,sat,unsat,pairs:768,assertions,malformed_rejected:malformed,triangle_resolution_nodes:5,status:'COMPUTATIONAL'},null,2));
