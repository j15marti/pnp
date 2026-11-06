#!/usr/bin/env node
'use strict';
// LSPV-3/437 compact standalone verification of strict 3-CNF one-wire source.
// Neither this nor the full reproducibility archive is the historical native byte checker.
const assert=require('assert'),crypto=require('crypto');
const B=[[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]];
const ok=(c,word)=>c.some(x=>{const b=(word>>(Math.abs(x)-1))&1;return x>0?b:1-b;});
function source(mask){let cs=[],id=5,p=id++,q=id++;
 for(let a of [1,-1])for(let b of [1,-1])cs.push([4,a*p,b*q]);
 for(let k=0;k<8;k++)if(mask&(1<<k)){
  const C=B[k];if(C.length===2)cs.push([-3,...C]);
  else {let d=id++;cs.push([-3,C[0],d],[-3,C[0],-d]);}}
 const v=id-1;
 for(let C of cs)assert(C.length===3&&new Set(C.map(Math.abs)).size===3);
 const dim='p cnf '+v+' '+cs.length+'\n'+cs.map(C=>C.join(' ')+' 0\n').join('');
 return {v,cs,dim,sha256:crypto.createHash('sha256').update(dim).digest('hex')};}
let sat=0,unsat=0,sourceAssignments=0,checks=0;
for(let mask=0;mask<256;mask++){
 const G=[0,1,2,3].some(y=>B.every((C,k)=>!(mask&(1<<k))||ok(C,y)));
 const {v,cs}=source(mask);let outputs=new Set(),atLeastOne=false;
 for(let w=0;w<2**v;w++){
   sourceAssignments++;
   if(!cs.every(C=>ok(C,w)))continue;
   atLeastOne=true;
   const s=(w>>2)&1,t=(w>>3)&1;
   assert(t===1);
   if(s)assert(B.every((C,k)=>!(mask&(1<<k))||ok(C,w&3)));
   outputs.add(s&t);
 }
 assert(atLeastOne);
 assert.equal(JSON.stringify([...outputs].sort()),JSON.stringify(G?[0,1]:[0]));
 if(G)sat++;else unsat++;
 checks+=4;
}
assert.equal(sat,95);assert.equal(unsat,161);
assert.equal(sourceAssignments,82944);
const diag=source(3),z=diag.v+1;
assert.equal(z,9);
function res(A,B,p){const SA=new Set(A),SB=new Set(B);
 assert((SA.has(p)&&SB.has(-p))||(SA.has(-p)&&SB.has(p)));
 const C=[...new Set([...A,...B].filter(x=>Math.abs(x)!==p))];
 assert(!C.some(x=>C.includes(-x)));
 return C.sort((a,b)=>a-b);}
const C=diag.cs;
const r1=res(C[4],C[5],7),r2=res(C[6],C[7],8);
assert.deepEqual(r1,[-3,1]);assert.deepEqual(r2,[-3,-1]);
const r3=res(r1,r2,1),r4=res(r3,[-z,3],3);
assert.deepEqual(r3,[-3]);assert.deepEqual(r4,[-9]);
assert([0,1,2,3].some(i=>((i>>1)&1)&(i&1)));
assert.throws(()=>res(C[4],C[5],3));
assert.throws(()=>res(r3,[-z,3],1));
for(let w=0;w<2**diag.v;w++)if(C.every(c=>ok(c,w)))assert.equal((w>>2&1)&(w>>3&1),0);
console.log(JSON.stringify({status:'restricted verified, native byte grammar open',cases:256,baseSAT:sat,baseUNSAT:unsat,guardedSourceSAT:256,sourceAssignments,gateLocalImpliesNotZ:false,facetAConditionalPaidNodes:5,source8DIMACSsha256:diag.sha256,checksPassed:checks+10}));
