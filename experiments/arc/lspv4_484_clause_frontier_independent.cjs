#!/usr/bin/env node
'use strict';
// Independently implemented 3^H status enumeration, not the Python 5^H optimizer.
// Only original signed cubic Tseitin clauses; no native FLMV or R_mix341 check.
const assert = require('node:assert/strict');
const graphs=[
 ['K4',4,Array.from({length:4},(_,i)=>Array.from({length:4-i-1},(_,k)=>[i,i+k+1])).flat()],
 ['K33',6,Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>[i,j+3])).flat()],
 ['Q3',8,Array.from({length:8},(_,i)=>Array.from({length:3},(_,k)=>[i,i^(1<<k)]).filter(([i,j])=>i<j)).flat()]
];
let checks=0,totalStates=0;
const results=[];
for(const [name,n,edges] of graphs){
 let minHalf=999,minBalanced=999,exampleHalf=null,exampleBalanced=null;
 const total=3**n;totalStates+=total;
 for(let code=0;code<total;code++){
   let t=code,s=[],nFull=0,nPart=0;
   for(let v=0;v<n;v++){const r=t%3;t=Math.floor(t/3);s.push(r);if(r===2)nFull++;if(r===1)nPart++;}
   let frontier=0;
   for(const [u,v] of edges)if(s[u]===1||s[v]===1||(s[u]===2&&s[v]===0)||(s[u]===0&&s[v]===2))frontier++;
   const lo=4*nFull+nPart,hi=4*nFull+3*nPart;
   if(lo<=2*n&&hi>=2*n&&frontier<minHalf){minHalf=frontier;exampleHalf=s;}
   if(lo<=Math.floor(8*n/3)&&hi>=Math.ceil(4*n/3)&&frontier<minBalanced){minBalanced=frontier;exampleBalanced=s;}
   checks++;
 }
 const epsilon=(()=>{let min=Infinity;
 for(let mask=1;mask<(1<<n)-1;mask++){
  let k=0;for(let i=0;i<n;i++)k+=((mask>>i)&1);
  if(k>n/2)continue;
  let c=0;for(const [u,v] of edges)c+=((mask>>u)&1)!==((mask>>v)&1)?1:0;
  min=Math.min(min,c/k);
 }return min;})();
 assert(minHalf+1e-12>=epsilon*n/(epsilon+2));checks++;
 assert(minBalanced+1e-12>=2*epsilon*n/(3*(epsilon+2)));checks++;
 let byParity=[];
 for(let parity=0;parity<=1;parity++){
   let incidence=Array.from({length:n},()=>[]);
   edges.forEach(([u,v],i)=>{incidence[u].push(i);incidence[v].push(i)});
   let clauses=[];
   for(let v=0;v<n;v++)for(let a=0;a<8;a++){
      const bits=[a&1,(a>>1)&1,(a>>2)&1];
      if((bits[0]^bits[1]^bits[2])!==(v===0?parity:0))clauses.push(incidence[v].map((edge,j)=>({edge,neg:!!bits[j]})));
   }
   assert.equal(clauses.length,4*n);checks++;
   let count=0;
   for(let mask=0;mask<(1<<edges.length);mask++)if(clauses.every(row=>row.some(lit=>Boolean((mask>>lit.edge)&1)!==lit.neg)))count++;
   assert.equal(count,parity?0:(1<<(edges.length-n+1)));checks++;
   byParity.push(count);
 }
 results.push({name,H:n,minimum_half_clause_frontier:minHalf,minimum_balanced_subset_frontier:minBalanced,
  witness_status_half:exampleHalf,witness_status_balanced:exampleBalanced,even_odd_model_counts:byParity});
}
console.log(JSON.stringify({agent:'LSPV4',run:484,method:'3^H status exact feasibility',results,states:totalStates,assertions:checks,failures:0,native_machine:false},null,2));
