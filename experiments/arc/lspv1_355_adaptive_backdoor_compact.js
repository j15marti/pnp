#!/usr/bin/env node
'use strict';
// LSPV-1 355 compact publicly executable signed source, RES DAG, and witness verifier.
// node experiments/arc/lspv1_355_adaptive_backdoor_compact.js
const crypto=require('crypto');
let assertions=0;const ok=(c,m)=>{if(!c)throw Error(m||'check failed');assertions++};
function run(d) {
 const k=2**d,n=4*k-1,cs=[],info=[];
 for(let l=0;l<k;l++) {
  const guard=Array.from({length:d},(_,h)=>{const prefix=l>>(d-h),bit=(l>>(d-h-1))&1,v=2**h+prefix;return bit?-v:v});
  for(let mask=0;mask<8;mask++) {
   const blockers=[0,1,2].map(j=>((mask>>j)&1)?-(k+3*l+j):(k+3*l+j));
   cs.push([...guard,...blockers]);info.push([l,mask]);
  }
 }
 const rows=cs.map(c=>c.slice());let paid=0;
 function res(a,b,p){
  const A=rows[a],B=rows[b];ok(A.includes(p)&&B.includes(-p),'invalid pivot');
  const C=[...new Set(A.filter(t=>t!==p).concat(B.filter(t=>t!==-p)))];
  ok(!C.some(x=>C.includes(-x)),'tautology');rows.push(C);paid++;return rows.length-1;
 }
 let frontier=[];
 for(let l=0;l<k;l++){
  let curr=Array.from({length:8},(_,i)=>8*l+i);
  for(let bit=2;bit>=0;bit--){
   let next=[];for(let j=0;j<curr.length/2;j++)next.push(res(curr[j],curr[curr.length/2+j],k+3*l+bit));
   curr=next;
  }
  frontier.push(curr[0]);
 }
 for(let level=d-1;level>=0;level--){
  const next=[];for(let j=0;j<frontier.length/2;j++)next.push(res(frontier[2*j],frontier[2*j+1],2**level+j));
  frontier=next;
 }
 ok(frontier.length===1&&rows[frontier[0]].length===0,'no contradiction');
 ok(paid===8*k-1,'paid count');
 let witnessed=0,flipped=0;
 for(let index=0;index<cs.length;index++){
  const [l,mask]=info[index],a=Array(n+1).fill(0);
  for(let depth=0;depth<d;depth++)a[2**depth+(l>>(d-depth))]=(l>>(d-depth-1))&1;
  for(let bit=0;bit<3;bit++)a[k+3*l+bit]=(mask>>bit)&1;
  const evalLit=t=>a[Math.abs(t)]===(t>0?1:0);
  for(let j=0;j<cs.length;j++)ok(cs[j].some(evalLit)===(j!==index),'deletion witness');
  for(const t of cs[index]){ok(!evalLit(t)&&evalLit(-t),'bad sign flip');flipped++}
  witnessed++;
 }
 const text='p cnf '+n+' '+cs.length+'\n'+cs.map(a=>a.join(' ')+' 0\n').join('');
 return {depth:d,leaves:k,variables:n,clauses:cs.length,exact_W:paid,
  strong_static_backdoor_lower:k,strong_static_backdoor_upper:2*k-1,
  adaptive_depth:d+1,adaptive_easy_leaves:2*k,
  source_bytes:Buffer.byteLength(text),sha256:crypto.createHash('sha256').update(text).digest('hex'),
  deletion_sat_witnesses:witnessed,sign_flip_sat_witnesses:flipped};
}
const cases=Array.from({length:7},(_,d)=>run(d));
console.log(JSON.stringify({status:'COMPUTATIONAL; exact all-size proof is in the report',
 independent_producer_check_assertions:assertions,cases},null,2));
