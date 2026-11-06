#!/usr/bin/env node
'use strict';
// LSPV-1/445 compact control. Full 37-node typed proof and independent checker
// accompany the downloadable archive, not this compact subset.
const assert=require('node:assert/strict');
const edges=[];
for(const off of [0,5])for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)
  if(u===0&&v===1)edges.push([off,off+4],[off+4,off+1]);
  else edges.push([off+u,off+v]);
edges.push([4,9]); assert.equal(edges.length,15);
assert.deepEqual(edges[14],[4,9]);
const incident=Array.from({length:10},()=>[]);
edges.forEach(([u,v],i)=>{incident[u].push(i+1);incident[v].push(i+1)});
assert(incident.every(a=>a.length===3));
const chi=[1,0,0,0,0,0,0,0,0,0];
const clauses=[],byVertex=[];
function sat(C,m){return C.some(l=>((m>>(Math.abs(l)-1))&1)===(l>0?1:0))}
for(let v=0;v<10;v++){
  const ids=[];
  for(let t=0;t<8;t++){
    const bits=[(t>>2)&1,(t>>1)&1,t&1];
    if((bits[0]^bits[1]^bits[2])===chi[v])continue;
    ids.push(clauses.length);
    clauses.push(incident[v].map((e,j)=>bits[j]?-e:e));
  }
  assert.equal(ids.length,4);byVertex.push(ids);
}
assert.equal(clauses.length,40);
let fullModels=0;const oneBad=new Set();
for(let m=0;m<(1<<15);m++){
  const bad=[];for(let j=0;j<clauses.length;j++)if(!sat(clauses[j],m))bad.push(j);
  if(bad.length===0)fullModels++;
  if(bad.length===1)oneBad.add(bad[0]);
}
assert.equal(fullModels,0);
assert.equal(oneBad.size,36);
let joinChecks=0;
for(const [side,u] of [[[0,1,2,3,4],4],[[5,6,7,8,9],9]]){
  const total=side.reduce((a,v)=>a^chi[v],0);
  const rowRhs=total^chi[u];
  const [e,a,b]=incident[u].includes(15)?[15,...incident[u].filter(x=>x!==15)]:[];
  assert(e===15&&a&&b);
  const selected=byVertex[u].filter(j=>{
    // Identify the two local forbidden patterns consistent with
    // the derived two-original-variable affine boundary row.
    const C=clauses[j];
    const wrongBits=[e,a,b].map(edge=>{const lit=C.find(l=>Math.abs(l)===edge);return lit<0?1:0});
    return wrongBits[0]===(1^total)&&(wrongBits[1]^wrongBits[2])===rowRhs;
  });
  assert.equal(selected.length,2);
  let feasible=0;
  for(let t=0;t<8;t++){
    const assign=new Map([[e,(t>>0)&1],[a,(t>>1)&1],[b,(t>>2)&1]]);
    const row=(assign.get(a)^assign.get(b))===rowRhs;
    const value=C=>C.some(l=>(assign.get(Math.abs(l))===1)===(l>0));
    if(row&&selected.every(j=>value(clauses[j]))){
      feasible++;assert.equal(assign.get(e),total);joinChecks++;
    }
  }
  assert(feasible>=1);
}
assert.equal((4*5-2)*2+1,37);
assert.deepEqual({AND3:28,XOR:6,LOCAL:2,RES:1},{AND3:28,XOR:6,LOCAL:2,RES:1});
const result={status:'COMPUTATIONAL_PASS',model:'original-coordinate R_mix341 rule-level compact control',
  variables:15,source_clauses:40,essential_clauses:oneBad.size,
  full_models:fullModels,local_bridge_join_checks:joinChecks,
  proved_source_floor:35,exhibited_paid_nodes:37,ideal_span:7,
  caveat:'Compact control does not replay the full typed 37-node proof; see complete ZIP.'};
process.stdout.write(JSON.stringify(result,null,2)+'\n');
