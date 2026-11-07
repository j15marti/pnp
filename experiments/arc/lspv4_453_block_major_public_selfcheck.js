#!/usr/bin/env node
// LSPV-4/453. Self-contained finite verifier for the restricted block-major join.
const assert = require('assert');
let checks = 0;
function enforce(z, u, v, sign=1) {
  return [[u,v],[u,-v],[-u,v],[-u,-v]].map(p=>[z*sign,...p]);
}
const examples = [
 {name:'independent SAT', k:2, blocks:[
   {private:[3,4],clauses:[[1,3,4]]},
   {private:[5,6],clauses:[[-2,5,-6]]}],label:true},
 {name:'jointly UNSAT but locally SAT',k:1,blocks:[
   {private:[2,3],clauses:enforce(1,2,3,1)},
   {private:[4,5],clauses:enforce(1,4,5,-1)}],label:false},
 {name:'shared separator SAT',k:1,blocks:[
   {private:[2,3],clauses:enforce(1,2,3,1)},
   {private:[4,5],clauses:enforce(1,4,5,1)}],label:true},
 {name:'original eight-clause contradiction',k:1,blocks:[
   {private:[2,3,4],clauses:Array.from({length:8},(_,mask)=>[2,3,4].map((v,i)=>(mask>>i)&1?v:-v))},
   {private:[5,6],clauses:[[1,5,6]]}],label:false}
];
function validate(f){
 if(!Number.isInteger(f.k)||f.k<0||!Array.isArray(f.blocks)||!f.blocks.length)return false;
 let seen=new Set();
 for(let b of f.blocks){
  if(!Array.isArray(b.private)||!b.private.length||!Array.isArray(b.clauses))return false;
  let p=new Set(b.private);
  if(p.size!==b.private.length||[...p].some(v=>!Number.isInteger(v)||v<=f.k||seen.has(v)))return false;
  b.private.forEach(v=>seen.add(v));
  for(let c of b.clauses)if(!Array.isArray(c)||c.length!==3||new Set(c.map(x=>Math.abs(x))).size!==3||c.some(x=>!Number.isInteger(x)||x===0||Math.abs(x)>f.k&&!p.has(Math.abs(x))))return false;
 }
 return true;
}
function evalClause(c,bits){return c.some(l=>!!((bits>>(Math.abs(l)-1))&1)===(l>0))}
function wholeSAT(f){const clauses=f.blocks.flatMap(b=>b.clauses),ids=[...new Set(clauses.flatMap(c=>c.map(l=>Math.abs(l))))];
 for(let mask=0;mask<2**ids.length;mask++){
  let x=0;ids.forEach((id,j)=>{if((mask>>j)&1)x|=1<<(id-1)});
  if(clauses.every(c=>evalClause(c,x)))return true;
 }return false;
}
function blockSAT(f,b,a){const rows=b.clauses.filter(c=>!c.some(l=>Math.abs(l)<=f.k&&!!((a>>(Math.abs(l)-1))&1)===(l>0))).map(c=>c.filter(l=>Math.abs(l)>f.k));
 for(let mask=0;mask<2**b.private.length;mask++){
  let x=0;b.private.forEach((id,j)=>{if((mask>>j)&1)x|=1<<(id-1)});
  if(rows.every(c=>evalClause(c,x)))return true;
 }return false;
}
function blockMajor(f){let state=Array(2**f.k).fill(true),calls=0;
 for(let b of f.blocks)for(let a=0;a<state.length;a++)if(state[a]){calls++;state[a]=blockSAT(f,b,a)}
 return {label:state.some(Boolean),calls};
}
for(let f of examples){assert(validate(f));checks++;const whole=wholeSAT(f), v=blockMajor(f);
 assert.strictEqual(whole,f.label);assert.strictEqual(v.label,whole);checks+=2;
 console.log(f.name, 'SAT='+v.label, 'guest_calls='+v.calls);
}
const malformed=JSON.parse(JSON.stringify(examples[0]));malformed.blocks[0].clauses[0]=[1,1,4];
assert(!validate(malformed));checks++;
console.log(JSON.stringify({passed:true,checks,examples:examples.length,malformed_rejected:1}));
