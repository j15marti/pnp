#!/usr/bin/env node
'use strict';
const A=require('node:assert/strict');
const clauses=[[1,2],[1,-2],[-1]];
function clause(c,w){return c.some(l=>Boolean(w&(1<<(Math.abs(l)-1)))===(l>0));}
function affine(mask,rhs,x,y){return Number(((mask&1?x:0)^(mask&2?y:0))===rhs);}
let exact=0, accepted=0, falseReject=0,checks=0;
for(let table=0;table<16;table++) for(let mask=0;mask<4;mask++)for(let rhs=0;rhs<2;rhs++){
 let equiv=true;
 for(let y=0;y<=1;y++)for(let x=0;x<=1;x++){
   if(((table>>(x+2*y))&1)!==affine(mask,rhs,x,y))equiv=false;
   checks++;
 }
 if(equiv){exact++;if(mask===3)accepted++;else falseReject++;}
 A(!equiv||[0,1,2,3].includes(mask));checks++;
}
A.deepEqual([exact,accepted,falseReject],[8,2,6]);checks++;
let sat=0,unsat=0;
for(let w=0;w<4;w++){
 if(clauses.slice(0,2).every(c=>clause(c,w)))sat++;
 if(clauses.every(c=>clause(c,w)))unsat++;
 let x=w&1, y=(w>>1)&1;
 A.equal(Number(clause(clauses[0],w)&&clause(clauses[1],w)),x);checks++;
 A.equal(affine(1,1,x,y),x);checks++;
 A.equal(affine(0,1,x,y),0);checks++;
}
A.equal(sat,2);A.equal(unsat,0);checks+=2;
console.log(JSON.stringify({status:'PASS',checks,exact,accepted,falseReject,sat,unsat}));
