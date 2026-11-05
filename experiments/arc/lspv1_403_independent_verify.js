#!/usr/bin/env node
/* Independent finite verifier for LSPV-1/403; recomputes labels and source retention.
   Usage: node lspv1_403_independent_verify.js raw.json */
'use strict';
const fs=require('fs'),assert=require('assert');
const raw=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
function sat(F){
 const m=Math.max(0,...F.flat().map(Math.abs));
 for(let a=0;a<(1<<m);a++){
  if(F.every(c=>c.some(l=>Boolean(a&(1<<(Math.abs(l)-1)))===(l>0))))return true;
 }
 return false;
}
function canonical(n){return Array.from({length:n},(_,i)=>[i+1]);}
let checks=0;assert.equal(raw.id,'LSPV1_403_CLOCKED_SAT_PRESERVATION');checks++;
assert.equal(raw.rows.length,108);checks++;
for(const row of raw.rows){
 const {n,halt_step:h}=row,F=canonical(n),trigger=h!==null&&h<=n;
 const G=trigger?[...F,[n+1],[-(n+1)]]:F;
 assert.equal(row.trigger,trigger);checks++;
 assert.equal(row.sat_before,sat(F));checks++;
 assert.equal(row.sat_after,sat(G));checks++;
 assert.equal(row.retained_source,JSON.stringify(G.slice(0,n))===JSON.stringify(F));checks++;
 assert.equal(row.output_clause_count,G.length);checks++;
}
const expected={sat_units:true,unsat_units:false,horn_sat:true,horn_unsat:false,twosat_sat:true,twosat_unsat:false,tseitin_even:true,tseitin_odd:false};
assert.equal(raw.controls.length,8);checks++;
for(const row of raw.controls){assert.equal(row.sat,expected[row.name]);checks++;assert.equal(row.unchanged,true);checks++;}
assert.equal(raw.malformed_rejections,7);checks++;
assert.equal(raw.theorem_verified_by_finite_test,false);checks++;
console.log(JSON.stringify({checks,rows:raw.rows.length,controls:raw.controls.length}));
