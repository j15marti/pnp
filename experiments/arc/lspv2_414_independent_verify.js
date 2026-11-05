#!/usr/bin/env node
"use strict";
/* Independent direct-semantic verifier of LSPV-2/414.
   Does not import the paid-gate producer and computes Boolean output without gate replay.
   node experiments/arc/lspv2_414_independent_verify.js */
const fs=require("fs"),assert=require("assert");
const raw=JSON.parse(fs.readFileSync("results/raw/arc/2026-11-05_0312_LSPV2_414_PAID_DEF_SUPPORT3_raw.json","utf8"));
const clauses=raw.metadata.clauses;
const literal=(l,b)=>l>0?((b>>(l-1))&1)===1:((b>>(-l-1))&1)===0;
const disjunction=(c,b)=>c.some(l=>literal(l,b));
const sat=(formula)=>[0,1,2,3].some(b=>formula.every(c=>disjunction(c,b)));
const H=(formula,b)=>(((b>>6)&1)===1)||
 ([3,4,5,6].every(j=>((b>>(j-1))&1)===1)&&formula.every(c=>disjunction(c,b)));
let checks=0;
function checkRow(row){
 if(!Number.isInteger(row.mask)||row.mask<0||row.mask>=256)throw Error("bad mask");
 const formula=clauses.filter((_,i)=>(row.mask&(1<<i))!==0);
 if(sat(formula)!==row.sat)throw Error("bad SAT");
 const ess=[];
 for(let v=1;v<=7;v++){
   let necessary=false;
   for(let b=0;b<128;b++)if(H(formula,b)!==H(formula,b^(1<<(v-1)))){necessary=true;break;}
   if(necessary)ess.push(v);
   checks++;
 }
 if(JSON.stringify(ess)!==JSON.stringify(row.support))throw Error("bad essential support");
 const count=7+formula.length+formula.reduce((n,c)=>n+c.filter(l=>l<0).length,0)+formula.filter(c=>c.length===2).length;
 if(count!==row.gates||row.out!==count+7)throw Error("bad gate count/output ID");
 checks+=4;
 for(let b=0;b<128;b++){
   const F=(((b>>6)&1)===1)&&[1,2,3,4,5,6].every(j=>disjunction([7,j],b));
   if(F&&!H(formula,b))throw Error("source-entailment failure");
   checks++;
 }
}
assert.equal(raw.rows.length,256);checks++;
raw.rows.forEach(checkRow);
assert.equal(raw.total.UNSAT,161);assert.equal(raw.total.SAT,95);
assert.equal(raw.total.small_support,161);checks+=3;
assert.deepEqual(raw.rows[3].support,[7]);checks++;
for(const v of [3,4,5,6]){assert(raw.rows[1].support.includes(v));checks++;}
const corrupted=[
 {...raw.rows[3],sat:true},
 {...raw.rows[3],support:[1,7]},
 {...raw.rows[3],gates:1},
 {...raw.rows[3],mask:999}
];
let rejected=0;
for(const row of corrupted){assert.throws(()=>checkRow(row));rejected++;}
console.log(JSON.stringify({status:"PASS",checks,rows:raw.rows.length,corrupted_rejected:rejected,source:"independent direct CNF semantics"}));
