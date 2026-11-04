#!/usr/bin/env node
/* Independently reconstruct LSPV-1/400 support-inflation witnesses. */
'use strict';
const fs=require('fs');
const assert=require('assert/strict');
const file=process.argv[2]||'results/raw/arc/2026-11-04_1400_LSPV1_SUPPORT_RETRACTION400.json';
const raw=JSON.parse(fs.readFileSync(file,'utf8'));
assert.equal(raw.title,'LSPV1-400');
let count=0;
const eq=(a,b)=>{assert.deepEqual(a,b);count++};
const truth=(clause,a)=>clause.some(l=>a[Math.abs(l)]===(l>0));
const gate=(z,a,b)=>[[-z,a],[-z,b],[z,-a,-b]];
for(const row of raw.cases){
 const k=row.k,p=2*k-1,r=2*k;
 eq(row.evaluator_clauses,3*k+1);
 eq(row.original_clauses,k+1);
 eq(row.chain_gate_nodes,k);
 eq(row.evaluator_original_variables,2*k);
 eq(row.paid_proof_nodes,4);
 eq(row.proof_resolvents,[[p],[-k],[-p]]);
 eq(row.final_AND3_table,[0,0]);
 eq(row.support_before,1);eq(row.support_after,k);
 eq(row.origin_support,Array.from({length:k},(_,i)=>i+1));
 eq(row.original_formula_unsat_by_opposite_units,true);
 eq(row.sibling_formula_sat,true);
 for(let j=2;j<=k;j++){
   let z=k+j-1,a=j===2?1:k+j-2,b=j;
   for(let va of [false,true])for(let vb of [false,true]){
    const assignment={[a]:va,[b]:vb,[z]:(va&&vb)};
    for(let C of gate(z,a,b)){eq(truth(C,assignment),true);}
   }
 }
 for(let vp of [false,true])for(let vx of [false,true]){
  let assignment={[p]:vp,[k]:vx,[r]:vp&&!vx};
  for(let C of gate(r,p,-k)){eq(truth(C,assignment),true);}
 }
 const cl=[[r],[-r,p],[-r,-k],[-p,k]];
 const R=(A,B,x)=>{assert(A.includes(x)&&B.includes(-x));
   return [...new Set(A.filter(y=>y!==x).concat(B.filter(y=>y!==-x)))].sort((a,b)=>a-b)};
 const pos=R(cl[0],cl[1],r),negx=R(cl[0],cl[2],r),negp=R(negx,cl[3],-k);
 eq([pos,negx,negp],row.proof_resolvents);
}
for(const broken of [null,{}, {cases:[]}]){
  try {assert.equal(broken.title,'LSPV1-400');throw Error('false accept');}
  catch(e){assert.notEqual(e.message,'false accept');count++;}
}
console.log(JSON.stringify({status:'PASS',cases:raw.cases.length,assertions:count}));
