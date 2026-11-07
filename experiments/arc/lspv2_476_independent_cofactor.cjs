#!/usr/bin/env node
'use strict';
// LSPV-2/476: independently implemented pure-cofactor cardinality checks.
// This script is NOT a general SAT solver or a native FLMV simulation.
const assert = require('node:assert/strict');
function testGraph(name, vertices, edges) {
  const neighbors = Array.from({length:vertices},()=>[]);
  edges.forEach(([a,b],i)=>{neighbors[a].push(i+1);neighbors[b].push(i+1)});
  assert(neighbors.every(a=>a.length===3));
  const packets=[];
  for(let v=0;v<vertices;v++){
    const ns=neighbors[v], clauses=[];
    for(let mask=0;mask<8;mask++){
      const parity=((mask&1)+((mask>>1)&1)+((mask>>2)&1))&1;
      if(parity!==(v===0?1:0))
        clauses.push(ns.map((x,j)=>mask&(1<<j)?-x:x));
    }
    assert.equal(clauses.length,4); packets.push(clauses);
  }
  let checks=0, assignments=0;
  const allSubsets=[];
  function choose(next, selected, k){
    if(selected.length===k){allSubsets.push(selected.slice());return}
    for(let i=next;i<=edges.length;i++){
      selected.push(i);choose(i+1,selected,k);selected.pop()
    }
  }
  for(let k=0;k<=Math.min(3,edges.length);k++)choose(1,[],k);
  for(const ids of allSubsets){
    for(let mask=0;mask<(1<<ids.length);mask++){
      const assignment=new Map(ids.map((x,j)=>[x,Boolean(mask&(1<<j))]));
      let survived=0, untouched=0, touched=0;
      for(const packet of packets){
        if(packet[0].some(l=>assignment.has(Math.abs(l))))touched++;
        else untouched++;
        for(const clause of packet){
          if(!clause.some(l=>assignment.has(Math.abs(l))
                && assignment.get(Math.abs(l))===(l>0)))survived++;
        }
      }
      assert(touched<=2*ids.length);
      assert(survived>=4*untouched);
      assert(survived>=4*vertices-4*ids.length);
      assert(untouched>=vertices-2*ids.length);
      assignments++;checks+=4;
    }
  }
  if(edges.length<=15) {
    let models=0;
    for(let assignment=0;assignment<2**edges.length;assignment++)
      if(packets.flat().every(c=>c.some(l=>
        Boolean(assignment&(2**(Math.abs(l)-1)))===(l>0))))models++;
    assert.equal(models,0);checks++;
  }
  return {name,vertices,edges:edges.length,assignments,checks};
}
const K4=[];
for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)K4.push([i,j]);
const cube=[];
for(let i=0;i<8;i++)for(let j=0;j<3;j++){const k=i^(1<<j);if(k>i)cube.push([i,k])}
const Petersen=[];
for(let i=0;i<5;i++){
  Petersen.push([i,(i+1)%5],[i,i+5],[i+5,5+(i+2)%5]);
}
const results=[
  testGraph('K4',4,K4),testGraph('cube',8,cube),
  testGraph('Petersen',10,Petersen)
];
const ledger={
  status:'PASS', tests:results,
  assertion_groups:results.reduce((a,x)=>a+x.checks,0),
  total_cofactors:results.reduce((a,x)=>a+x.assignments,0),
  scope:'literal original-variable cofactors on supplied odd-charge cubic sources; independent implementation, NOT FLMV or mixed-calculus proof'
};
process.stdout.write(JSON.stringify(ledger,null,2)+'\n');
