#!/usr/bin/env node
"use strict";
/* Macro-only host control; theorem proof is in role report. */
const A=require("assert").strict;
const graphs={K4:[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],
  PRISM3:[[0,1],[1,2],[2,0],[3,4],[4,5],[5,3],[0,3],[1,4],[2,5]],
  CUBE:Array.from({length:8},(_,i)=>[0,1,2].map(j=>[i,i^(1<<j)]))
      .flat().filter(([a,b])=>a<b)};
const rows=[];
for(const [name,edges] of Object.entries(graphs)){
 const h=Math.max(...edges.flat())+1, adjacency=Array.from({length:h},()=>[]);
 edges.forEach(([u,v],e)=>{adjacency[u].push(e);adjacency[v].push(e);});
 for(const odd of [1,0]){
  let sources=[];
  const ma=[];
  for(let v=0;v<h;v++){
   let ids=[],scope=adjacency[v],rhs=+(odd&&v===0);
   for(let a=0;a<8;a++){
    let bs=scope.map((_,j)=>(a>>j)&1);
    if((bs[0]^bs[1]^bs[2])===rhs)continue;
    ids.push(sources.length);
    sources.push(scope.map((e,j)=>bs[j]?-(e+1):e+1));
   }
   A.equal(ids.length,4);
   for(let a=0;a<8;a++){
     let bits=scope.map((_,j)=>(a>>j)&1);
     let con=ids.every(i=>sources[i].some(l=>
       (l>0)===!!bits[scope.indexOf(Math.abs(l)-1)]));
     A.equal(con,(bits[0]^bits[1]^bits[2])===rhs);
   }
   ma.push({ids,scope,rhs});
  }
  const valid=a=>sources.every(c=>c.some(l=>(l>0)===!!(a>>(Math.abs(l)-1)&1)));
  let models=0;for(let a=0;a<2**edges.length;a++)if(valid(a))models++;
  A.equal(models,odd?0:2**(edges.length-h+1));
  let cost=ma.length*3+h-1;
  A.equal(cost,4*h-1);
  rows.push({name,odd,variables:edges.length,clauses:sources.length,models,
    macroWeightedCost:cost,binaryExpansionCost:cost});
 }
}
console.log(JSON.stringify({run:"LSPV-2 LOCAL-MACRO345",rows},null,2));
