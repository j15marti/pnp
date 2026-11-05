#!/usr/bin/env node
"use strict";
/* Independent semantic verifier for LSPV-2/414.
   Does NOT import the gate producer, derives H directly from the CNF.
   Run node experiments/arc/lspv2_414_independent_verify.js */
const fs=require("fs"),assert=require("assert");
const raw=JSON.parse(fs.readFileSync("results/raw/arc/2026-11-05_0312_LSPV2_414_PAID_DEF_SUPPORT3_raw.json","utf8"));
const cs=raw.metadata.clauses;
const literal=(l,b)=>l>0?((b>>(l-1))&1)===1:((b>>(-l-1))&1)===0;
const disjunction=(c,b)=>c.some(l=>literal(l,b));
const sat=(formula)=>{
 for(let b=0;b<4;b++)if(formula.every(c=>disjunction(c,b)))return true;
 return false;
};
const H=(formula,b)=>(((b>>6)&1)===1)||
 [3,4,5,6].every(j=>((b>>(j-1))&1)===1) && formula.every(c=>disjunction(c,b));
let checks=0;
assert.equal(raw.rows.length,256);checks++;
for(const row of raw.rows){
 const formula=cs.filter((_,i)=>(row.mask&(1<<i))!==0);
 assert.equal(sat(formula),row.sat);checks++;
 const ess=[];
 for(let v=1;v<=7;v++){
   let necessary=false;
   for(let b=0;b<128;b++){
     if(H(formula,b)!==H(formula,b^(1<<(v-1)))){necessary=true;break;}
   }
   if(necessary)ess.push(v);
   checks++;
 }
 assert.deepEqual(ess,row.support);checks++;
 const count=7+formula.length+formula.reduce((n,c)=>n+c.filter(l=>l<0).length,0)+formula.filter(c=>c.length===2).length;
 assert.equal(row.gates,count);assert.equal(row.out,count+7);checks+=2;
 for(let b=0;b<128;b++){
    const F=(((b>>6)&1)===1)&&[1,2,3,4,5,6].every(j=>disjunction([7,j],b));
    assert(!F||H(formula,b));checks++;
 }
}
assert.equal(raw.total.UNSAT,161);assert.equal(raw.total.SAT,95);
assert.equal(raw.total.small_support,161);checks+=3;
assert.deepEqual(raw.rows[3].support,[7]);checks++;
for(const v of [3,4,5,6]){assert(raw.rows[1].support.includes(v));checks++;}
console.log(JSON.stringify({status:"PASS",checks,rows:raw.rows.length,source:"independent direct CNF semantics"}));
