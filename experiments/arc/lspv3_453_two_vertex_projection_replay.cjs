#!/usr/bin/env node
// LSPV-3/453. Standalone strict original-source RES projection control.
// Semantic subgrammar of historical R_mix341; NOT the authoritative byte checker.
// node experiments/arc/lspv3_453_two_vertex_projection_replay.cjs
"use strict";
const assert=require("node:assert/strict");
const clean=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||((x<0)?1:-1));
const satisfies=(C,a)=>C.some(l=>a.get(Math.abs(l))===(l>0?1:0));
function local(variables,charge){
  const out=[];
  for(let b=0;b<2**variables.length;b++){
    const bits=variables.map((_,j)=>(b>>j)&1);
    if(bits.reduce((x,y)=>x^y,0)!==charge)
      out.push(clean(variables.map((v,j)=>bits[j]?-v:v)));
  }
  return out;
}
function check(d){
  const z=d,left=[...Array.from({length:d-1},(_,i)=>i+1),z],
        right=[z,...Array.from({length:d-1},(_,i)=>d+i+1)],
        boundary=[...left.slice(0,-1),...right.slice(1)];
  const A=local(left,1),B=local(right,0),res=[];
  for(let i=0;i<A.length;i++)for(let j=0;j<B.length;j++){
    let first,second;
    if(A[i].includes(z)&&B[j].includes(-z)){first=A[i];second=B[j];}
    else if(B[j].includes(z)&&A[i].includes(-z)){first=B[j];second=A[i];}
    else continue;
    const clause=clean([...first.filter(v=>v!==z),...second.filter(v=>v!==-z)]);
    assert.deepEqual(clause.map(Math.abs),boundary);
    res.push({clause,sourceParents:[i,j]});
  }
  const k=boundary.length;
  assert.equal(res.length,2**(k-1));
  assert.equal(new Set(res.map(q=>q.clause.join(","))).size,res.length);
  let bad=0;
  for(let bits=0;bits<2**k;bits++){
    const a=new Map(boundary.map((v,j)=>[v,(bits>>j)&1]));
    const parity=[...a.values()].reduce((x,y)=>x^y,0);
    const legal=[0,1].some(t=>{
      a.set(z,t);return [...A,...B].every(c=>satisfies(c,a));
    });
    assert.equal(legal,parity===1);
    const failures=res.filter(q=>!satisfies(q.clause,a));
    assert.equal(failures.length,legal?0:1);
    if(!legal)bad++;
  }
  return {d,boundaryBits:k,sourceClauses:A.length+B.length,
          exactOutputClauses:res.length,singleBadContextBlockerNodes:1,
          rejectedBoundaryAssignments:bad};
}
const cases=[2,3,4,5].map(check);
console.log(JSON.stringify({status:"PASS",cases},null,2));
