#!/usr/bin/env node
'use strict';
// LSPV-3/468: compact source-level reproduction. Full Python producer and
// separately written Node checker are provided in the accompanying archive.
// No claim of authoritative historical R_mix341 accepted-byte replay.
const crypto=require('crypto'),assert=require('assert');
const graphs={K4:[4,[]],K33:[6,[]],cube:[8,[]]};
for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)graphs.K4[1].push([i,j]);
for(let i=0;i<3;i++)for(let j=3;j<6;j++)graphs.K33[1].push([i,j]);
for(let i=0;i<8;i++)for(let j=i+1;j<8;j++)if(((i^j).toString(2).replace(/0/g,'').length)===1)graphs.cube[1].push([i,j]);
function sat(c,a){return c.some(l=>!!(a&(1<<(Math.abs(l)-1)))===(l>0));}
function run(name,h,edges){
 let inc=Array.from({length:h},()=>[]);
 edges.forEach(([u,v],i)=>{inc[u].push(i+1);inc[v].push(i+1)});
 inc.forEach(a=>a.sort((a,b)=>a-b));
 let C=[],src='p cnf '+edges.length+' '+(4*h)+'\n';
 for(let v=0;v<h;v++){
  for(let a=0;a<8;a++){const bits=[(a>>2)&1,(a>>1)&1,a&1];if((bits[0]^bits[1]^bits[2])===(v===0?1:0))continue;
   let clause=inc[v].map((e,i)=>bits[i]?-e:e);C.push(clause);src+=clause.join(' ')+' 0\n';
  }
 }
 assert(C.length===4*h);
 let all=0,even=0;
 for(let a=0;a<(1<<edges.length);a++){
  if(C.every(c=>sat(c,a)))all++;
  if(inc.every(z=>z.reduce((p,e)=>p^((a>>(e-1))&1),0)===0))even++;
 }
 assert(all===0);assert(even===1<<(edges.length-h+1));
 let deletion=0;
 for(let j=0;j<C.length;j++){
  let witness=false;
  for(let a=0;a<(1<<edges.length);a++)if(C.every((c,k)=>k===j||sat(c,a))){witness=true;break;}
  assert(witness);deletion++;
 }
 return {name,vertices:h,variables:edges.length,source_clauses:C.length,paid_AND3:3*h,paid_XOR:h-1,paid_total:4*h-1,even_models:even,deletion_witnesses:deletion,source_sha256:crypto.createHash('sha256').update(src).digest('hex')};
}
console.log(JSON.stringify(Object.entries(graphs).map(([n,[h,e]])=>run(n,h,e)),null,2));
