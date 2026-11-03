#!/usr/bin/env node
'use strict';
// BVP354. Exact linear minimum over Rmix341 by essential-source argument.
// The code reconstructs legal pure-resolution certificates and all controls.
const assert=require('assert');
function canon(a) {
 const z=[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
 assert.equal(z.length,a.length);
 for (const q of z) assert.ok(!z.includes(-q));
 return z;
}
function source(n,b=1,f=0) {
 const c=i=>n+i,C=[[b?c(1):-c(1)]],ess=[0];
 for(let i=1;i<=n;i++){
   C.push([-i,c(i)], [i,-c(i)], [-c(i+1),i], [-c(i+1),c(i)], [-i,-c(i),c(i+1)]);
   ess.push(1+5*(i-1)+1,1+5*(i-1)+4);
 }
 C.push([f?c(n+1):-c(n+1)]); ess.push(C.length-1);
 return {C:C.map(canon),ess,v:2*n+1};
}
function value(C,a){return C.every(c=>c.some(x=>a[Math.abs(x)]===(x>0)));}
function resolve(a,b,p) {
 if(!a.includes(p)||!b.includes(-p))throw Error('illegal pivot');
 const r=[...new Set([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)])];
 if(r.some(x=>r.includes(-x)))throw Error('tautological resolvent');
 return canon(r);
}
function makeProof(n,C) {
 const z=C.length,db=[...C],P=[];let last=0;
 for(let i=1;i<=n;i++){
   const j=1+5*(i-1);
   const imp=resolve(db[j+1],db[j+4],i);
   P.push({l:j+1,r:j+4,p:i,out:imp}); const id=db.length;db.push(imp);
   const unit=resolve(db[last],db[id],n+i);
   P.push({l:last,r:id,p:n+i,out:unit});last=db.length;db.push(unit);
 }
 const fin=resolve(db[last],db[z-1],2*n+1);
 P.push({l:last,r:z-1,p:2*n+1,out:fin});
 return P;
}
function check(C,P) {
 const db=[...C];
 for(const row of P) {
   if(row.l<0||row.r<0||row.l>=db.length||row.r>=db.length)throw Error('non-topological');
   const got=resolve(db[row.l],db[row.r],row.p);
   if(JSON.stringify(got)!==JSON.stringify(row.out))throw Error('forged result');
   db.push(got);
 }
 if(!P.length||db.at(-1).length)throw Error('missing empty clause');
}
function witness(n,i,xi) {
 const a=Array(2*n+2).fill(false);
 for(let j=1;j<=n+1;j++)a[n+j]=(j<=i);
 for(let j=1;j<=n;j++)a[j]=(j<i)||(j===i&&xi===1);
 return a;
}
function enumerate(C,v) {
 let count=0;
 for(let mask=0;mask<2**v;mask++){
  const a=Array.from({length:v+1},(_,j)=>j>0&&Boolean((mask>>(j-1))&1));
  if(value(C,a))count++;
 }
 return count;
}
function run() {
 let checks=0;const cases=[];
 for(const n of [1,2,3,4,5,6,7,8,12,16,32,64]){
   const {C,ess,v}=source(n),P=makeProof(n,C);
   assert.equal(C.length,5*n+2);assert.equal(P.length,2*n+1);check(C,P);checks+=3;
   for(let i=1;i<=n;i++)for(let k=0;k<2;k++){
     const ix=1+5*(i-1)+(k?4:1),a=witness(n,i,k);
     assert.equal(value(C,a),false);
     assert.equal(value(C.filter((_,j)=>j!==ix),a),true);checks+=2;
   }
   assert.equal(new Set(ess).size,2*n+2);checks++;
   assert.equal(value(C.slice(1),Array(v+1).fill(false)),true);checks++;
   assert.equal(value(C.slice(0,-1),Array(v+1).fill(true)),true);checks++;
   assert.equal(value(source(n,0,0).C,Array(v+1).fill(false)),true);checks++;
   assert.equal(value(source(n,1,1).C,Array(v+1).fill(true)),true);checks++;
   if(n<=7){
     assert.equal(enumerate(C,v),0);
     assert.equal(enumerate(source(n,0,0).C,v),1);
     assert.equal(enumerate(source(n,1,1).C,v),1);checks+=3;
   }
   const forged=P.map(r=>({...r,out:[...r.out]}));forged[0].p+=v;
   assert.throws(()=>check(C,forged));assert.throws(()=>check(C,P.slice(0,-1)));checks+=2;
   cases.push({n,variables:v,clauses:C.length,essential_sources:2*n+2,proof_nodes:P.length,occurrences:C.reduce((s,c)=>s+c.length,0),exhaustive:n<=7});
 }
 return {status:'PROVED/EXACT symbolic construction; independently reproducible finite checks',
         theorem:'W_Rmix341(F_n)=2n+1',assertions:checks,cases,
         limits:'No asymptotic hard family; no transfer from rational PC; B1/B2/B3 OPEN'};
}
console.log(JSON.stringify(run(),null,2));
