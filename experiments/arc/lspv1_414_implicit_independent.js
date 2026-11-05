#!/usr/bin/env node
/* Independent LSPV-1/414 implicit W+Resolution verifier. No Python imports.
   Run: node lspv1_414_implicit_independent.js raw414.json
   This is EXHAUSTIVE finite testing, not a polynomial UNSAT verifier or an R_mix341 checker. */
'use strict';
const assert=require('node:assert/strict');
const crypto=require('node:crypto');
const fs=require('node:fs');
if(process.argv.length<3)throw Error('usage: node this.js raw414.json');
const data=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
let checks=0,sat=0,unsat=0,totalLeaves=0,treeChecks=0;
const hash=a=>crypto.createHash('sha256').update(JSON.stringify(a)).digest('hex');
function isFalse(c,a){return c.every(x=>x>0?!a[x-1]:!!a[-x-1]);}
function block(prefix){return prefix.map((b,i)=>b?-(i+1):i+1);}
function val(n,clauses,des){
  assert.equal(des.version,'IMPLICIT_BLOCKING_TREE_WRES_1');checks++;
  assert.equal(des.variables,n);checks++;
  assert.deepEqual(des.source_clauses,clauses);checks++;
  assert.equal(des.source_sha256,hash(clauses));checks++;
  for(let d=0;d<n;d++)for(let mask=0;mask<(1<<d);mask++){
    const pre=Array.from({length:d},(_,j)=>(mask>>j)&1);
    const left=new Set(block([...pre,0])),right=new Set(block([...pre,1]));
    assert(left.has(d+1)&&right.has(-(d+1)));checks++;
    left.delete(d+1);right.delete(-(d+1));
    assert.deepEqual([...new Set([...left,...right])].sort((a,b)=>a-b),
                     block(pre).sort((a,b)=>a-b));checks++;treeChecks++;
  }
  let broken=null,weakened=0,visited=0;
  for(let mask=0;mask<2**n;mask++){
    const a=Array.from({length:n},(_,j)=>(mask>>(n-1-j))&1);visited++;
    let j=-1;for(let k=0;k<clauses.length;k++)if(isFalse(clauses[k],a)){j=k;break;}
    if(j<0){broken=a;break;}
    const big=new Set(block(a));
    for(const literal of clauses[j]){assert(big.has(literal));checks++;}
    if(big.size!==new Set(clauses[j]).size)weakened++;
  }
  totalLeaves+=visited;
  return {valid:broken===null,enumerated_leaves:visited,
    canonical_explicit_derived_nodes:broken===null?(2**n-1)+weakened:null};
}
const all=[...data.records,...data.structured];
for(let idx=0;idx<all.length;idx++){
 const r=all[idx],v=val(r.n,r.clauses,r.descriptor);
 assert.equal(v.valid,r.verified.valid,r.case);checks++;
 assert.equal(v.enumerated_leaves,r.verified.enumerated_leaves,r.case);checks++;
 assert.equal(v.canonical_explicit_derived_nodes,
              r.verified.canonical_explicit_derived_nodes,r.case);checks++;
 let solution=false;
 for(let mask=0;mask<2**r.n;mask++){
   const a=Array.from({length:r.n},(_,j)=>(mask>>(r.n-1-j))&1);
   if(r.clauses.every(c=>!isFalse(c,a))){solution=true;break;}
 }
 assert.equal(v.valid,!solution,r.case);checks++;
 if(idx<256){if(solution)sat++;else unsat++;}
}
assert.equal(all.length,268);checks++;
assert.deepEqual([sat,unsat],[95,161]);checks++;
assert.equal(data.summary.malformed_sources_rejected,8);checks++;
assert.equal(data.summary.corrupted_or_mismatched_descriptors_rejected,4);checks++;
const unsatOriginal=all.find(x=>x.case==='OPPOSITE_UNITS_UNSAT');
assert.notEqual(hash([[1]]),unsatOriginal.descriptor.source_sha256);checks++;
const forged=all.find(x=>x.case==='POS_UNIT_SAT');
assert.equal(val(forged.n,forged.clauses,forged.descriptor).valid,false);checks++;
console.log(JSON.stringify({status:'PASS',independent_assertions:checks,
 tree_nodes_checked:treeChecks,prefix_or_full_leaf_visits:totalLeaves,
 all_fixture_cases:all.length,exhaustive_sat:sat,exhaustive_unsat:unsat,
 implicit_proof_is_not_Rmix341:true},null,2));
