#!/usr/bin/env node
// TMR-4/079: independently reproducible finite template-edge orbit audit.
// Source uses original oriented beat edges only; never a 3-SAT encoding.
"use strict";
const assert=require("node:assert/strict");
const R=(a,b)=>[1,3].includes((b-a+10)%5);
const arcs=[];
for(let a=0;a<5;a++)for(let b=0;b<5;b++)if(R(a,b))arcs.push([a,b]);
function graph(seq){
  const E=new Set(["0,1"]);
  for(let i=0;i<seq.length;i++){
    const labels=[0,seq[i]].concat([0,1,2,3,4].filter(x=>x!==0&&x!==seq[i]));
    const v=[0,1,2+3*i,3+3*i,4+3*i];
    for(const pair of arcs)E.add(v[labels.indexOf(pair[0])]+","+v[labels.indexOf(pair[1])]);
  }
  const edges=Array.from(E,s=>s.split(",").map(Number)).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
  return {n:2+3*seq.length,edges};
}
function signature(t){
  const {edges}=graph([t]);
  const out=Array.from({length:5},()=>Array(5).fill(0));
  for(let a=0;a<5;a++)for(let b=0;b<5;b++)
    for(let c=0;c<5;c++)for(let d=0;d<5;d++)for(let e=0;e<5;e++){
      const x=[a,b,c,d,e];
      if(edges.every(pair=>R(x[pair[0]],x[pair[1]])))out[a][b]++;
    }
  return out;
}
const S1=signature(1), S3=signature(3);
for(let a=0;a<5;a++)for(let b=0;b<5;b++){
  assert.equal(S1[a][b],Number((b-a+5)%5===1));
  assert.equal(S3[a][b],Number((b-a+5)%5===3));
}
let assignments=0, instances=0;
for(let m=1;m<=2;m++)for(let mask=0;mask<(1<<m);mask++){
  const seq=Array.from({length:m},(_,i)=>mask&(1<<i)?3:1);
  const G=graph(seq), x=Array(G.n).fill(0);
  let brute=0;
  function loop(depth){
    if(depth===G.n){
      assignments++;
      if(G.edges.every(pair=>R(x[pair[0]],x[pair[1]])))brute++;
      return;
    }
    for(let a=0;a<5;a++){x[depth]=a;loop(depth+1);}
  }
  loop(0);
  let sigcount=0;
  for(let a=0;a<5;a++)for(let b=0;b<5;b++){
    let w=1;
    for(const t of seq)w*=t===1?S1[a][b]:S3[a][b];
    sigcount+=w;
  }
  assert.equal(brute,sigcount);
  assert.equal(brute,seq.every(t=>t===seq[0])?5:0);
  instances++;
}
console.log(JSON.stringify({instances,pointwise_full_assignments:assignments,source_arcs:"T5 R(x,y) iff (y-x)%5 in {1,3}", failures:0}));
