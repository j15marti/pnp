#!/usr/bin/env node
'use strict';
/* TMR-4/090 independent source-derived row-profile negative control.
   node experiments/tmr/tmr4_t5_rowprofile090.js
   No packages. Uses JS BigInt. Does not assume unsupplied assignments. */
const assert=require('assert');
const W=(a,b)=>[1,3].includes((b-a+5)%5);
const masks=[];
for(let m=1;m<32;m++){
 let colors=Array.from({length:5},(_,i)=>i).filter(i=>m&(1<<i));
 if(colors.length===1||(colors.length===2&&[2,3].includes(colors[1]-colors[0])))masks.push(m);
}
assert.strictEqual(masks.length,10);
const isSingle=m=>(m&(m-1))===0;
const weights=(m,r)=>isSingle(m)?1n:2n**BigInt(r)-2n;
const orientation=(k,unsat,j,type)=>{
 const P=unsat?[[0,0],[0,1],[1,0]]:[[0,0],[0,1]];
 return P[j%P.length][type];
};
function common(m,sign,y){
 for(let a=0;a<5;a++)if(m&(1<<a)){
  if(sign===0&&!W(a,y))return false;
  if(sign===1&&!W(y,a))return false;
 }
 return true;
}
function exact(k,unsat){
 assert(k>=4&&k%2===0);
 let z=0n, explored=0;
 for(const a of masks)for(const b of masks){
  let mul=weights(a,k/2)*weights(b,k/2);
  for(let j=0;j<k;j++){
   let colors=0;
   for(let y=0;y<5;y++)
    if(common(a,orientation(k,unsat,j,0),y)&&common(b,orientation(k,unsat,j,1),y))colors++;
   mul*=BigInt(colors);
   if(mul===0n)break;
  }
  explored++;z+=mul;
 }
 return {z,explored};
}
function pointwise(k,unsat){
 let n=2*k,count=0,attempts=5**n;
 for(let z=0;z<attempts;z++){
  let t=z,x=Array(n);
  for(let i=0;i<n;i++){x[i]=t%5;t=Math.floor(t/5);}
  let ok=true;
  for(let i=0;i<k&&ok;i++)for(let j=0;j<k;j++){
   let s=orientation(k,unsat,j,i<k/2?0:1);
   let good=s===0?W(x[i],x[k+j]):W(x[k+j],x[i]);
   if(!good){ok=false;break;}
  }
  if(ok)count++;
 }
 return {count,attempts};
}
let runs=[];
for(const k of [4,6,100])for(const unsat of [false,true]){
 let r=exact(k,unsat);
 assert.strictEqual(r.z,unsat?0n:5n);
 let brute=(k===4?pointwise(k,unsat):null);
 if(brute)assert.strictEqual(BigInt(brute.count),r.z);
 runs.push({k,unsat,exact:r.z.toString(),signatures:r.explored,
            bruteAssignments:brute?.attempts||0});
}
console.log(JSON.stringify({verified:true,runs}));
