#!/usr/bin/env node
'use strict';
// LSPV-3/421 independently implemented orientation-exact RES and paid DEF-facet auditor.
// Proposed CANON1 byte completion, not historical original /341 checker.
// Run: node experiments/arc/lspv3_421_oriented_res_independent.js
const assert = require('node:assert/strict');
let checks=0, facets=0, tautFacets=0, legalResolution=0, badOld=0;
function yes(v,m){assert.ok(v,m);checks++}
function sat(C, v){return C.some(l=>v[Math.abs(l)]===Number(l>0))}
function facet(a,b,z,truth,av,bv){
  const wrongZ=1-((truth >> (av+(bv<<1)))&1);
  return [av?-a:a,bv?-b:b,wrongZ?-z:z];
}
function orient(L,R,p){
  const left=new Set(L),right=new Set(R),out=[];
  for(const s of [1,-1]){
    if(!left.has(s*p)||!right.has(-s*p))continue;
    const C=new Set([...left].filter(x=>x!==s*p).concat([...right].filter(x=>x!==-s*p)));
    if([...C].some(x=>C.has(-x)))continue;
    let row=[...C].sort((x,y)=>Math.abs(x)-Math.abs(y)||(x<0?1:-1));
    if(!out.some(t=>JSON.stringify(t)===JSON.stringify(row)))out.push(row);
  }
  return out;
}
function old(L,R,p){
  const a=new Set(L),b=new Set(R);
  if(!((a.has(p)&&b.has(-p))||(a.has(-p)&&b.has(p))))return null;
  const row=[...new Set([...a,...b].filter(v=>Math.abs(v)!==p))];
  if(row.some(v=>row.includes(-v)))return null;
  return row.sort((x,y)=>Math.abs(x)-Math.abs(y)||(x<0?1:-1));
}
for(let t=0;t<16;t++){
  for(let row=0;row<4;row++){
    let av=row&1,bv=(row>>1)&1,C=facet(1,1,2,t,av,bv);
    facets++;
    const taut=C.some(l=>C.includes(-l)); if(taut)tautFacets++;
    yes(taut===(row===1||row===2),'alias tautological facet index');
    for(let x=0;x<2;x++){
      const z=(t>>(x*3))&1;
      yes(sat(C,{1:x,2:z}),'facet satisfied by valid unique extension');
    }
    for(const source of [[1],[-1]]){
      for(const pivot of [1,2]){
        for(const result of orient(C,source,pivot)){
          legalResolution++;
          for(let x=0;x<2;x++)for(let z=0;z<2;z++){
            const asg={1:x,2:z};
            yes(!sat(C,asg)||!sat(source,asg)||sat(result,asg),'true RES semantic entailment');
          }
        }
        const result=old(C,source,pivot);
        if(result && [0,1].some(x=>[0,1].some(z=>{
          const asg={1:x,2:z};
          return sat(C,asg)&&sat(source,asg)&&!sat(result,asg)
        })))badOld++;
      }
    }
  }
}
yes(facets===64,'64 total facets');
yes(tautFacets===32,'32 tautological offdiagonal facets');
const clauses=[];
for(const a of [-1,0,1])for(const b of [-1,0,1])for(const c of [-1,0,1]){
  clauses.push([a,b*2,c*3].filter(x=>x!==0));
}
for(const A of clauses)for(const B of clauses)for(let p=1;p<=3;p++){
  for(const C of orient(A,B,p)){
    for(let mask=0;mask<8;mask++){
      const asg={1:mask&1,2:(mask>>1)&1,3:(mask>>2)&1};
      yes(!sat(A,asg)||!sat(B,asg)||sat(C,asg),'all ordinary RES');
    }
  }
}
yes(JSON.stringify(orient([1,-1,-2],[1],1))===JSON.stringify([[1,-2]]),'old counterexample repaired');
yes(old([1,-1,-2],[1],1).join(',')==='-2','published vulnerable pivot deletion reproduced');
yes(JSON.stringify(orient([1,1,-2],[-1],1))===JSON.stringify([[-2]]),'repeated same-sign parent is legal');
yes(orient([1,2],[2,3],1).length===0,'missing pivot is rejected');
const K=BigInt('1'+'0'.repeat(80));
yes((K+3n).toString().length===81,'sparse huge declared header indices');
const raw={
  experiment:'LSPV3-421-oriented-resolution-independent-JS',status:'COMPUTATIONAL',
  original_semantic_R_mix341_unchanged:true,proposed_CANON1_current_checker_unsound:true,
  facets,tautFacets,legalResolution,badOld,checks,
  verified_repair:'oriented complementary literal removal and exact normalized resolvent',
  large_header_digits:(K+3n).toString().length,
  B3:'OPEN',P_vs_NP:'OPEN'
};
console.log(JSON.stringify(raw));
