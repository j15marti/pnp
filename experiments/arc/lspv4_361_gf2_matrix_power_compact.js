#!/usr/bin/env node
"use strict";
// Reproducer of ROW/XOR fragment matrix powering proof, no dependencies.
// "ROW" expands to three charged AND3 inferences, not one unit-cost axiom.
// Run: node experiments/arc/lspv4_361_gf2_matrix_power_compact.js
const assert=require("assert"), crypto=require("crypto");
let count=0;
const check=(x)=>{assert.ok(x);count++}, equal=(a,b)=>{assert.deepStrictEqual(a,b);count++};
function fixture(h,odd){
  let edges=[];
  if(h===4){for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)edges.push([i,j]);}
  else {let t=h/2;for(let i=0;i<t;i++)edges.push([i,(i+1)%t]);
    for(let i=0;i<t;i++)edges.push([t+i,t+(i+1)%t]);
    for(let i=0;i<t;i++)edges.push([i,t+i]);}
  let clauses=[],rows=[];
  for(let v=0;v<h;v++){
    let ids=edges.flatMap(([a,b],i)=>(a===v||b===v)?[i+1]:[]);
    equal(ids.length,3);
    let rhs=(odd&&v===0)?1:0,refs=[];
    for(let p=0;p<8;p++){
      let bits=[p&1,(p>>1)&1,(p>>2)&1], parity=bits[0]^bits[1]^bits[2];
      if(parity!==rhs){refs.push(clauses.length);
        clauses.push(ids.map((id,j)=>bits[j]?-id:id));}
    }
    rows.push({ids,rhs,refs});
  }
  let ops=[],last=0;
  for(let i=1;i<h;i++){ops.push([last,i]);last=h+ops.length-1;}
  return {clauses,rows,ops,final:last,n:edges.length};
}
function validateSource(F){
  for(let row of F.rows){
    let expected=[];
    for(let p=0;p<8;p++){
      let b=[p&1,(p>>1)&1,(p>>2)&1];
      if((b[0]^b[1]^b[2])!==row.rhs)
        expected.push(row.ids.map((id,j)=>b[j]?-id:id).sort((a,b)=>a-b).join(","));
    }
    let actual=row.refs.map(i=>F.clauses[i].slice().sort((a,b)=>a-b).join(","));
    equal(actual.sort(),expected.sort());
  }
  for(let j=0;j<F.ops.length;j++)for(let p of F.ops[j])
    check(Number.isInteger(p)&&p>=0&&p<F.rows.length+j);
}
function matrixCoeff(F){
  const K=F.rows.length+F.ops.length, D=2*K;
  let B=Array.from({length:D},()=>Array(D).fill(0));
  F.ops.forEach(([a,b],j)=>{B[a][F.rows.length+j]^=1;B[b][F.rows.length+j]^=1});
  for(let i=0;i<K;i++){B[i][K+i]=1;B[K+i][K+i]=1;}
  function mult(X,Y){
    let Z=Array.from({length:D},()=>Array(D).fill(0));
    for(let i=0;i<D;i++)for(let k=0;k<D;k++)if(X[i][k])
      for(let j=0;j<D;j++)Z[i][j]^=Y[k][j];
    return Z;
  }
  let product=Array.from({length:D},(_,i)=>Array.from({length:D},(_,j)=>+(i===j)));
  for(let e=0;e<K;e++)product=mult(product,B);
  return F.rows.map((_,i)=>product[i][K+F.final]);
}
function recursionCoeff(F){
  let K=F.rows.length+F.ops.length, calls=0,maxDepth=0;
  function edge(i,j){
    if(i<K&&j<K){if(j<K&&j>=F.rows.length){
      let [a,b]=F.ops[j-F.rows.length];return (+(a===i))^(+(b===i));}
      return 0;}
    if(i<K&&j>=K)return +(i===j-K);
    if(i>=K&&j>=K)return +(i===j);
    return 0;
  }
  function p(u,v,e,depth){
    calls++;maxDepth=Math.max(maxDepth,depth);
    if(e===0)return +(u===v);if(e===1)return edge(u,v);
    let l=Math.floor(e/2),ans=0;
    for(let mid=0;mid<2*K;mid++){
      if(p(u,mid,l,depth+1))ans^=p(mid,v,e-l,depth+1);
    }
    return ans;
  }
  let coeff=F.rows.map((_,i)=>p(i,K+F.final,K,1));
  return {coeff,calls,maxDepth};
}
function evaluate(F,coeff){
  let mask=new Set(),rhs=0;
  F.rows.forEach((row,i)=>{
    if(coeff[i]){
      for(let v of row.ids){if(mask.has(v))mask.delete(v);else mask.add(v);}
      rhs^=row.rhs;
    }
  });
  return {mask:[...mask].sort((a,b)=>a-b),rhs};
}
function countModels(F){
  let total=0;
  for(let a=0;a<(1<<F.n);a++)
    if(F.clauses.every(C=>C.some(l=>!!(a&(1<<(Math.abs(l)-1)))===(l>0))))total++;
  return total;
}
let cases=[];
for(let h of [4,6])for(let odd of [false,true]){
  let F=fixture(h,odd);validateSource(F);
  let direct=matrixCoeff(F),slow=recursionCoeff(F);
  equal(direct,slow.coeff);
  let result=evaluate(F,slow.coeff);
  equal(result.mask,[]);equal(result.rhs,odd?1:0);
  equal(countModels(F),odd?0:(h===4?8:16));
  for(let c=0;c<F.clauses.length;c++){
    let G={...F,clauses:F.clauses.map(x=>x.slice())};G.clauses[c][0]*=-1;
    check(countModels(G)>0);
    let changed=F.rows.some(row=>row.refs.some(k=>G.clauses[k][0]!==F.clauses[k][0]));
    check(changed);
  }
  cases.push({h,odd,models:countModels(F),q:3*F.rows.length+F.ops.length,
    K:F.rows.length+F.ops.length,calls:slow.calls,depth:slow.maxDepth});
}
// A repeated XOR parent cancels, not a graph-simple edge.
let R={rows:[{},{}],ops:[[0,0],[2,1]],final:3};
equal(matrixCoeff(R),[0,1]);equal(recursionCoeff(R).coeff,[0,1]);
let seed=153;
for(let t=0;t<40;t++){
  let r=2+t%4,K=r+1+t%3,ops=[];
  for(let j=0;j<K-r;j++){
    seed=(Math.imul(seed,1664525)+1013904223)>>>0;let a=seed%(r+j);
    seed=(Math.imul(seed,1664525)+1013904223)>>>0;let b=seed%(r+j);
    ops.push([a,b]);
  }
  let F={rows:Array.from({length:r},()=>({})),ops,final:K-1};
  equal(matrixCoeff(F),recursionCoeff(F).coeff);
}
const result={pass:true,checks:count,cases,duplicate_parent_coefficients:[0,1],
  host_rss_KiB:Math.round(process.memoryUsage().rss/1024),
  qualification:"ROW/XOR certificate checking only; q=3r+t, no B1/B2/B3"};
console.log(JSON.stringify(result,null,2));
