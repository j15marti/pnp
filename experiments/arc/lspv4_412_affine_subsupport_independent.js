#!/usr/bin/env node
// Independent signed-clause and affine truth-table referee for LSPV-4/412.
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const input = process.argv[2] || 'results/raw/arc/2026-11-05_0436_LSPV4_412_AFFINE_SUBSUPPORT.json';
const raw = JSON.parse(fs.readFileSync(input,'utf8'));
const source = [[1,2],[1,-2],[-1]];
const evalC = (c,word) => c.some(l => Boolean(word&(1<<(Math.abs(l)-1))) === (l>0));
const pairFactor = (x,y) => Number(evalC(source[0],x|(y<<1)) && evalC(source[1],x|(y<<1)));
const rowValue = (mask,rhs,x,y) => Number((((mask&1?x:0)^(mask&2?y:0))===rhs));
let matches=0, rejected=0, accepted=0, checks=0;
for(let vec=0;vec<16;vec++)
 for(let mask=0;mask<4;mask++)
  for(let rhs=0;rhs<2;rhs++){
   let same=true;
   for(let y=0;y<2;y++)for(let x=0;x<2;x++){
     same = same && (((vec>>(x+2*y))&1)===rowValue(mask,rhs,x,y));
     checks++;
   }
   const rule = same && mask===3; // published CANON1 equality filter
   if(same){matches++;if(rule)accepted++;else rejected++;}
   assert(!rule || same);checks++;
  }
assert.deepEqual([matches,accepted,rejected],[8,2,6]);checks++;
for(let y=0;y<2;y++)for(let x=0;x<2;x++){
 assert.equal(pairFactor(x,y),x);checks++;
 assert.equal(pairFactor(x,y),rowValue(1,1,x,y));checks++;
 assert.equal(Number(!evalC([-1],x|(y<<1))),x);checks++;
 assert.equal(rowValue(0,1,x,y),0);checks++;
}
let sat=0,unsat=0;
for(let word=0;word<4;word++){
 if(source.slice(0,2).every(c=>evalC(c,word)))sat++;
 if(source.every(c=>evalC(c,word)))unsat++;
 checks+=2;
}
assert.equal(sat,2);assert.equal(unsat,0);checks+=2;
assert.equal(raw.exhaustive_affine_pairs.false_rejected,rejected);checks++;
assert.equal(raw.exhaustive_affine_pairs.exact,matches);checks++;
assert.equal(raw.exhaustive_affine_pairs.canon1_accepted,accepted);checks++;
console.log(JSON.stringify({status:'PASS',checks,exact:matches,canon1Accepted:accepted,canon1FalseRejects:rejected,satModels:sat,unsatModels:unsat}));
